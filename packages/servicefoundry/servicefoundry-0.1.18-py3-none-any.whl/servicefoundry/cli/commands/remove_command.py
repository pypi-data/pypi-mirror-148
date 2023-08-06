import logging

import rich_click as click
from rich import print_json
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.cli.const import ENABLE_CLUSTER_COMMANDS

from ..config import CliConfig
from ..util import handle_exception

console = Console()
logger = logging.getLogger(__name__)

WORKSPACE_DISPLAY_FIELDS = [
    "id",
    "name",
    "namespace",
    "status",
    "clusterId",
    "createdBy",
    "createdAt",
    "updatedAt",
]
DEPLOYMENT_DISPLAY_FIELDS = [
    "id",
    "serviceId",
    "domain",
    "deployedBy",
    "createdAt",
    "updatedAt",
]


def get_remove_command():
    @click.group(name="remove")
    def remove_command():
        """
        Servicefoundry remove entity by id

        \b
        Supported entities:
        - workspace
        - service
        - secret-group
        - secret
        - authorization
        """
        pass

    if ENABLE_CLUSTER_COMMANDS:

        @remove_command.command(name="cluster", help="remove cluster")
        @click.argument("cluster_id")
        def remove_cluster(cluster_id):
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                tfs_client.remove_cluster(cluster_id)
            except Exception as e:
                handle_exception(e)

    @remove_command.command(name="workspace", help="remove workspace")
    @click.argument("workspace_id")
    def remove_workspace(workspace_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            space = tfs_client.remove_workspace(workspace_id)
            if not CliConfig.get("json"):
                tfs_client.tail_logs(space["pipelinerun"]["name"])
            else:
                print_json(data=space)
        except Exception as e:
            handle_exception(e)

    @remove_command.command(name="service", help="remove service")
    @click.argument("service_id")
    def remove_service(service_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            deployment = tfs_client.remove_service(service_id)
            tfs_client.tail_logs(deployment["runId"])
        except Exception as e:
            handle_exception(e)

    @remove_command.command(name="secret-group", help="remove secret-group")
    @click.argument("secret_group_id")
    def remove_secret_group(secret_group_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.delete_secret_group(secret_group_id)
            print_json(data=response)
        except Exception as e:
            handle_exception(e)

    @remove_command.command(name="secret", help="remove secret")
    @click.argument("secret_id")
    def remove_secret(secret_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.delete_secret(secret_id)
            print_json(data=response)
        except Exception as e:
            handle_exception(e)

    @remove_command.command(name="auth", help="remove authorization")
    @click.argument("authorization_id")
    def remove_auth(authorization_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.delete_authorization(authorization_id)
            print_json(data=response)
        except Exception as e:
            handle_exception(e)

    return remove_command
