import logging
import rich_click as click
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.cli.const import ENABLE_CLUSTER_COMMANDS
from servicefoundry.cli.display_util import print_obj

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


def get_create_command():
    @click.group(name="create")
    def create_command():
        """
        Servicefoundry create entities

        \b
        Supported entities:
        - workspace
        - secret-group
        - secret
        """
        pass

    if ENABLE_CLUSTER_COMMANDS:

        @create_command.command(name="cluster", help="create new cluster")
        @click.argument("name")
        @click.argument("region")
        @click.argument("aws_account_id")
        @click.argument("server_name")
        @click.argument("ca_data")
        @click.argument("server_url")
        def create_cluster(
            name, region, aws_account_id, server_name, ca_data, server_url
        ):
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                cluster = tfs_client.create_cluster(
                    name, region, aws_account_id, server_name, ca_data, server_url
                )
                print_obj("Cluser", cluster)
            except Exception as e:
                handle_exception(e)

    @create_command.command(name="workspace", help="create new workspace in cluster")
    @click.argument("space_name")
    @click.option(
        "--cluster_id", type=click.STRING, help="cluster id to create this space in."
    )
    def create_workspace(space_name, cluster_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            if not cluster_id:
                cluster = tfs_client.session.get_cluster()
                if cluster is None:
                    raise Exception(
                        "Cluster is neither passed in as option, nor set in context. "
                        "Use `servicefoundry use cluster` to set cluster context."
                    )
                cluster_id = cluster["id"]
            space = tfs_client.create_workspace(cluster_id, space_name)

            if not CliConfig.get("json"):
                tfs_client.tail_logs(space["runId"])

            print_obj("Workspace", space["workspace"])
        except Exception as e:
            handle_exception(e)

    @create_command.command(name="secret-group", help="create secret-group")
    @click.argument("secret_group_name")
    def create_secret_group(secret_group_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.create_secret_group(secret_group_name)
            print_obj(f"Secret Group", response)
        except Exception as e:
            handle_exception(e)

    @create_command.command(name="secret", help="create secret")
    @click.argument("secret_group_id")
    @click.argument("secret_key")
    @click.argument("secret_value")
    def create_secret(secret_group_id, secret_key, secret_value):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.create_secret(
                secret_group_id, secret_key, secret_value
            )
            print_obj(response["id"], response)
        except Exception as e:
            handle_exception(e)

    return create_command
