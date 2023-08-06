import yaml

from .template import get_template
from ..exceptions import ConfigurationException

TEMPLATE = "template"


def parse(file):
    with open(file) as f:
        try:
            template_param = yaml.full_load(f)
        except yaml.YAMLError as exc:
            raise ConfigurationException(f"File {file} is not in yaml format.")
        if "template" not in template_param:
            raise ConfigurationException(f"File {file} has missing field '{TEMPLATE}'.")
        template_generator = get_template(template_param[TEMPLATE])
        out = template_generator.generate_service_def(template_param)
        return out
