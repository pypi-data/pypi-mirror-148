import logging
import os
import os.path
import shutil

import questionary
import rich_click as click
import yaml
from questionary import Choice
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.session_factory import get_session
from servicefoundry.build.util import (
    BadRequestException,
    download_file,
    uncompress_tarfile,
)
from servicefoundry.cli.commands.login_command import login_user
from servicefoundry.cli.const import TEMP_FOLDER

console = Console()
logger = logging.getLogger(__name__)

MSG_CREATE_NEW_SPACE = "Create a new space"


def get_init_command():
    @click.command(help="Initialize new service for servicefoundry")
    def init():
        # Get SFSClient
        tfs_client = ServiceFoundryServiceClient.get_client()

        # Get Session else do login
        try:
            get_session()
        except BadRequestException:
            doLogin = questionary.select(
                "You need to login to create a service", ["Login", "Exit"]
            ).ask()
            if doLogin == "Login":
                login_user()
            else:
                return

        # Setup temp folder to download templates
        if os.path.exists(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)
        os.mkdir(TEMP_FOLDER)

        # Static call to get list of templates
        templates = tfs_client.get_templates_list()

        # Choose a template of service to be created.
        template_choices = [
            Choice(f'{t["id"]} - {t["description"]}', value=t["id"]) for t in templates
        ]
        template_id = questionary.select("Choose a template", template_choices).ask()

        # Get package url for template
        package_url = tfs_client.get_template_by_id(template_id)["url"]

        # Download and untar package
        package_file = f"{TEMP_FOLDER}/{template_id}.tgz"
        template_folder = f"{TEMP_FOLDER}/{template_id}"
        download_file(package_url, package_file)
        uncompress_tarfile(package_file, template_folder)

        # Read template into template_details
        template_details = None
        with open(f"{template_folder}/template.yaml", "r") as stream:
            template_details = yaml.safe_load(stream)

        parameters = {}
        for param in template_details.get("spec", {}).get("parameters", []):
            if param["kind"] == "string":
                parameters[param["id"]] = questionary.text(
                    param["prompt"], default=param["default"]
                ).ask()
            elif param["kind"] in "number":
                while True:
                    value = questionary.text(
                        param["prompt"], default=str(param["default"])
                    ).ask()
                    if value.isdigit():
                        parameters[param["id"]] = int(value)
                        break
                    else:
                        print("Not an integer Value. Try again")
            elif param["kind"] == "options":
                parameters[param["id"]] = questionary.select(
                    param["prompt"], choices=param["options"]
                ).ask()
            elif param["kind"] == "tfy-workspace":
                spaces = tfs_client.list_workspace()

                choices_list = [
                    space["fqn"]
                    for space in spaces
                    if space["status"] == "CREATE_SPACE_SUCCEEDED"
                ]
                choices_list.append(MSG_CREATE_NEW_SPACE)

                param_id = questionary.select(
                    param["prompt"], choices=choices_list
                ).ask()

                if param_id == MSG_CREATE_NEW_SPACE:
                    new_space_name = questionary.text(
                        "Please provide a name for your workspace"
                    ).ask()
                    DEFAULT_CLUSTER_ID = "tfy-ctl-us-east-1-develop"
                    workspace = tfs_client.create_workspace(
                        DEFAULT_CLUSTER_ID, new_space_name
                    )
                    console.print(
                        "Your workspace is being created. You can check it's status with\n`servicefoundry list workspace`. Once the workspace is created\nplease choose that from the above list on running `servicefoundry init`"
                    )
                    return

                parameters[param["id"]] = param_id

        # Render param_value_dict into servicefoundry.yaml
        with open(f"{template_folder}/servicefoundry.yaml", "w") as template_file:
            yaml.dump(
                {
                    "template": f"truefoundry.com/v1/{template_id}",
                    "parameters": parameters,
                },
                template_file,
                sort_keys=False,
            )

        # Create new folder to hold template and rendered values.
        new_folder = parameters.get("service_name", f"{template_id}_service")

        if os.path.exists(new_folder):
            console.print(
                "Failed to create service code repository directory.", end=" "
            )
            console.print(new_folder, end=" ", style="red")
            console.print("already exists.")
        else:
            shutil.move(template_folder, new_folder)
            os.remove(f"{new_folder}/template.yaml")
            console.print(
                f"Your ServiceFoundry service code repository is created in [bold]{new_folder}![/]"
            )

        # Clean temp folder
        if os.path.exists(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)

    return init
