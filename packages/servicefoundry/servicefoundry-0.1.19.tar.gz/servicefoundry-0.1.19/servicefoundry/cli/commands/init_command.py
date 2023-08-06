import logging
import os
import os.path
import shutil
from types import SimpleNamespace

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
    set_workspace_in_context,
    uncompress_tarfile,
)
from servicefoundry.cli.commands.login_command import login_user
from servicefoundry.cli.const import TEMP_FOLDER
from servicefoundry.cli.util import get_space_choices, handle_exception

console = Console()
logger = logging.getLogger(__name__)

MSG_CREATE_NEW_SPACE = "Create a new workspace"


def get_init_command():
    def _init():
        # Get SFSClient
        tfs_client = ServiceFoundryServiceClient.get_client()

        # Get Session else do login
        try:
            get_session()
        except BadRequestException:
            do_login = questionary.select(
                "You need to login to create a service", ["Login", "Exit"]
            ).ask()
            if do_login == "Login":
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
                space_choices = get_space_choices(tfs_client)
                space_choices.append(
                    Choice(title=MSG_CREATE_NEW_SPACE, value=MSG_CREATE_NEW_SPACE)
                )
                space = questionary.select(param["prompt"], choices=space_choices).ask()

                if space == MSG_CREATE_NEW_SPACE:
                    cluster = tfs_client.session.get_cluster()
                    if not cluster:
                        raise Exception(
                            "No default cluster set to create workspace. "
                            "Use `sfy use cluster` to pick and set a default cluster"
                        )
                    new_space_name = questionary.text(
                        "Please provide a name for your workspace"
                    ).ask()
                    response = tfs_client.create_workspace(
                        cluster_id=cluster["id"], name=new_space_name
                    )
                    console.print("Please wait while your workspace is being created. ")
                    tfs_client.tail_logs(runId=response["runId"], wait=True)
                    console.print(
                        f"Done, created new workspace with name {new_space_name!r}"
                    )
                    space = response["workspace"]
                    # Set as default workspace if none is already set
                    if not tfs_client.session.get_workspace():
                        click.echo(
                            f"Setting {space['name']!r} as the default workspace. "
                            f"You can pick a different one using `sfy use workspace`"
                        )
                        set_workspace_in_context(client=tfs_client, workspace=space)

                space_fqn = space["fqn"]
                parameters[param["id"]] = space_fqn

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
            ### refactor this out.
            post_init_instruction = template_details.get("spec", {}).get(
                "postInitInstruction"
            )
            if post_init_instruction:
                console.print(
                    post_init_instruction.format(
                        parameters=SimpleNamespace(**parameters)
                    )
                )
            ###

        # Clean temp folder
        if os.path.exists(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)

    @click.command(help="Initialize new service for servicefoundry")
    def init():
        try:
            _init()
        except Exception as e:
            handle_exception(e)

    return init
