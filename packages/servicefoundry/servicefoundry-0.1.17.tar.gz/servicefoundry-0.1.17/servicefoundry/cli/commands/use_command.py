import logging

import questionary
import rich_click as click
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.util import format_cluster, format_workspace

console = Console()
logger = logging.getLogger(__name__)


def get_set_command():
    @click.group(name="use")
    def use_command():
        """
        Set servicefoundry default workspace/cluster

        \b
        Supported entities:
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
        tfs_client.session.set_cluster(format_cluster(cluster))
        tfs_client.session.save_session()
        return cluster

    @use_command.command(name="cluster")
    def use_cluster():
        attempt_set_cluster()

    @use_command.command(name="workspace")
    def use_workspace():
        attempt_set_cluster()
        tfs_client = ServiceFoundryServiceClient.get_client()
        spaces = tfs_client.list_workspace()
        if not spaces:
            click.echo(
                "No workspaces found. Create one using `servicefoundry create workspace <workspace-name>`"
            )
            return
        if len(spaces) == 1:
            space = spaces[0]
        else:
            spaces_choices = {
                space["name"]: space
                for space in spaces
                if space["status"] == "CREATE_SPACE_SUCCEEDED"
            }
            space = questionary.select(
                "Choose your workspace", choices=spaces_choices
            ).ask()
            space = spaces_choices[space]
        click.echo(f"Setting {space['name']!r} as the default workspace")
        tfs_client.session.set_workspace(format_workspace(space))
        tfs_client.session.save_session()

    return use_command
