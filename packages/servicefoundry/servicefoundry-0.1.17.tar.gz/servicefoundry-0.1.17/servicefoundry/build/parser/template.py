import json
import re
from pathlib import Path

import requests
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from mako.template import Template

from ..clients.service_foundry_client import ServiceFoundryServiceClient
from ..const import BUILD_PACK, COMPONENT, BUILD_DIR
from ..model.build_pack import BuildPack
from ..util import read_text, download_file, uncompress_tarfile, DefinitionException

SPEC = "spec"
KIND = "kind"
OVERWRITES = "overwrites"


def load_yaml_from_file(file):
    with open(file) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise DefinitionException(f"File {file} is not in yaml format. {exc}")


def validate_schema(template, schema):
    schema = read_text(schema)
    schema = json.loads(schema)
    validate(instance=template, schema=schema)


class Parameters(dict):
    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)
        self.__dict__ = self


class SfTemplate:
    def __init__(self, template):
        try:
            validate_schema(template, "schema/template_schema.json")
        except ValidationError as err:
            raise DefinitionException(f"Template validation failed. {err.message}")

        self.template = template

    def generate_service_def(self, overrides):
        parameters = Parameters(overrides["parameters"])

        base_build_id = self.template[SPEC]["baseBuild"]
        base_component_id = self.template[SPEC]["baseComponent"]
        definition = DefinitionYaml(base_build_id, base_component_id)

        self._apply_overwrite(definition, self.template[SPEC][OVERWRITES], parameters)

        if OVERWRITES in overrides and overrides[OVERWRITES]:
            self._apply_overwrite(definition, overrides[OVERWRITES], parameters)
        return definition

    def _apply_overwrite(self, definition, overwrite_dict, parameters):
        for overwrite_key, overwrite_value in overwrite_dict.items():
            resolved_value = self._resolve_variables(
                overwrite_key, overwrite_value, parameters
            )
            definition.apply_overwrite(overwrite_key.split("."), resolved_value)

    def _resolve_variables(self, key, value, parameters):
        if isinstance(value, dict):
            ret_value = {}
            for k, v in value.items():
                ret_value[k] = self._resolve_variables(key, v, parameters)
            return ret_value
        if isinstance(value, list):
            ret_value = []
            for item in value:
                ret_value.append(self._resolve_variables(key, item, parameters))
            return ret_value
        if isinstance(value, int):
            return value
        # Check if it's a simple substitution
        match = re.match("^\$\{parameters\.([A-Za-z0-9]+)\}$", value)
        if match:
            variable = match.group(1)
            if variable in parameters:
                return parameters[variable]
            else:
                raise DefinitionException(
                    f"Failed to parse {key}. Parameters doesn't have {variable}"
                )
        try:
            template = Template(value)
            return template.render(parameters=parameters)
        except AttributeError as e:
            raise DefinitionException(f"Failed to parse {key}. {e}")


def get_template_file(template_id):
    Path(f"{BUILD_DIR}/template").mkdir(parents=True, exist_ok=True)
    template_folder = f"{BUILD_DIR}/template/{template_id}"

    if not Path(template_folder).is_dir():
        tfs_client = ServiceFoundryServiceClient.get_client(auth_required=False)
        package_url = tfs_client.get_template_by_id(template_id)["url"]
        package_file = f"{BUILD_DIR}/template/{template_id}.tgz"
        download_file(package_url, package_file)
        uncompress_tarfile(package_file, template_folder)
    return template_folder


def get_base_yaml(base_id):
    base_file = f'{BUILD_DIR}/template/{base_id}'

    if not Path(base_file).is_file():
        tfs_client = ServiceFoundryServiceClient.get_client(auth_required=False)
        package_url = tfs_client.get_base_by_id(base_id)['url']
        download_file(package_url, base_file)

    return load_yaml_from_file(base_file)


def get_template(template_name):
    split = template_name.split("/")
    if len(split) != 3:
        raise DefinitionException(f"Incorrect template {template_name}")
    template_id = split[2]
    template_folder = get_template_file(template_id)
    template_yaml = load_yaml_from_file(f"{template_folder}/template.yaml")
    return SfTemplate(template_yaml)


class DefinitionYaml:
    def __init__(self, base_build_id, base_component_id):
        self.base_def = {
            BUILD_PACK: get_base_yaml(base_build_id),
            COMPONENT: get_base_yaml(base_component_id),
        }

    def write(self, file="servicefoundry.lock.yaml"):
        with open(file, "w") as outfile:
            yaml.dump_all(self.base_def.values(), outfile, default_flow_style=False)

    def get_build_pack(self):
        return BuildPack(**self.base_def[BUILD_PACK][SPEC])

    def get_component(self):
        return self.base_def[COMPONENT]

    def apply_overwrite(self, key, value):
        self._apply_overwrite(self.base_def, key, value)

    def validate(self):
        try:
            validate_schema(self.base_def[BUILD_PACK], "schema/build_pack_schema.json")
        except ValidationError as err:
            raise DefinitionException(f"Build pack validation failed. {err.message}")

        try:
            validate_schema(self.base_def[COMPONENT], "schema/component_schema.json")
        except ValidationError as err:
            raise DefinitionException(f"Component validation failed. {err.message}")

    def _apply_overwrite(self, definition, keys, value):
        key = keys[0]
        if len(keys) == 1:
            definition[keys[0]] = value
            return
        if key in definition:
            self._apply_overwrite(definition[key], keys[1:], value)
        else:
            raise DefinitionException(f"{key} not found in {definition}")
