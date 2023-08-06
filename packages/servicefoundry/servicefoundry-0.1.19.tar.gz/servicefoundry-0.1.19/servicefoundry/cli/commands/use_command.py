import logging

import questionary
import rich_click as click
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.util import set_cluster_in_context, set_workspace_in_context
from servicefoundry.cli.util import get_space_choices, handle_exception

console = Console()
logger = logging.getLogger(__name__)


def get_set_command():
    @click.group(name="use")
    def use_command():
        """
        Set default workspace

        \b
        Supported resources:
        - workspace
        - cluster
        """
        pass

    def attempt_set_cluster():
        tfs_client = ServiceFoundryServiceClient.get_client()
        clusters = tfs_client.list_cluster()
        if len(clusters) == 1:
            cluster = clusters[0]
        else:
            raise NotImplementedError("Could not set cluster.")
        set_cluster_in_context(tfs_client, cluster)
        return cluster

    @use_command.command(name="cluster")
    def use_cluster():
        try:
            attempt_set_cluster()
        except Exception as e:
            handle_exception(e)

    @use_command.command(name="workspace")
    @click.argument("workspace_name", required=False)
    def use_workspace(workspace_name=None):
        try:
            cluster = attempt_set_cluster()
            tfs_client = ServiceFoundryServiceClient.get_client()
            if workspace_name:
                spaces = tfs_client.get_workspace_by_name(
                    workspace_name=workspace_name, cluster_id=cluster["id"]
                )
                if len(spaces) > 1:
                    raise Exception(
                        "Error: More than one workspace found with the same name. Please contact truefoundry admin."
                    )
                elif not spaces:
                    raise Exception(
                        f"No workspace with name {workspace_name!r} found in current cluster ({cluster['id']}).\n"
                        f"Use `sfy list workspace` to see available workspaces OR "
                        f"`sfy use workspace` to pick one interactively",
                    )
                space = spaces[0]
            else:
                spaces = tfs_client.list_workspace()
                if not spaces:
                    raise Exception(
                        "No workspaces found. Create one using `sfy create workspace <workspace-name>`"
                    )
                elif len(spaces) == 1:
                    space = spaces[0]
                else:
                    space_choices = get_space_choices(tfs_client)
                    space = questionary.select(
                        "Choose your workspace", choices=space_choices
                    ).ask()
            click.echo(f"Setting {space['name']!r} as the default workspace")
            set_workspace_in_context(tfs_client, space)
        except Exception as e:
            handle_exception(e)

    return use_command
