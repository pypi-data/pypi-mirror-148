import logging

import rich_click as click
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.cli.const import ENABLE_CLUSTER_COMMANDS, ENABLE_SECRETS_COMMANDS
from servicefoundry.cli.display_util import print_obj

from ..util import handle_exception

console = Console()
logger = logging.getLogger(__name__)

WORKSPACE_DISPLAY_FIELDS = [
    "name",
    # "id",
    "status",
    # "clusterId"
    # "namespace",
    "createdBy",
    "createdAt",
    # "updatedAt",
]

SERVICE_DISPLAY_FIELDS = ["id", "name", "metadata", "status"]

DEPLOYMENT_DISPLAY_FIELDS = [
    "id",
    "name",
    "serviceId",
    "createdBy",
    # "domain",
    # "createdAt",
    # "updatedAt",
]


def get_get_command():
    @click.group(name="get")
    def get_command():
        # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
        """
        Get servicefoundry resources

        \b
        Supported resources:
        - workspace
        - service
        - deployment
        """
        pass

    if ENABLE_CLUSTER_COMMANDS:

        @get_command.command(name="cluster", help="show cluster metadata")
        @click.argument("cluster_id")
        def get_cluster(cluster_id):
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                cluster = tfs_client.get_cluster(cluster_id)
                print_obj("Cluster", cluster)
            except Exception as e:
                handle_exception(e)

    @get_command.command(name="workspace", help="show workspace metadata")
    @click.argument("workspace_name")
    def get_workspace(workspace_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            cluster = tfs_client.session.get_cluster()
            if cluster is None:
                raise Exception(
                    "Cluster info not set. "
                    "Use `sfy use cluster` to set current cluster and rerun this command."
                )
            spaces = tfs_client.get_workspace_by_name(workspace_name, cluster["id"])
            if len(spaces) > 1:
                raise Exception(
                    "Error: More than one workspace found with the same name. Please contact truefoundry admin."
                )

            print_obj("Workspace", spaces[0], columns=WORKSPACE_DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    @get_command.command(name="service", help="show service metadata")
    @click.argument("service_id")
    def get_service(service_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            service = tfs_client.get_service(service_id)
            print_obj("Service", service, columns=SERVICE_DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    @get_command.command(name="deployment", help="show deployment metadata")
    @click.argument("deployment_id")
    def get_deployment(deployment_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            deployment = tfs_client.get_deployment(deployment_id)
            print_obj("Deployment", deployment, columns=DEPLOYMENT_DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    if ENABLE_SECRETS_COMMANDS:

        @get_command.command(name="secret-group", help="show secret-group")
        @click.argument("secret_group_id")
        def get_secret_group(secret_group_id):
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                response = tfs_client.get_secret_group(secret_group_id)
                print_obj(f"Secret Group", response)
            except Exception as e:
                handle_exception(e)

        @get_command.command(name="secret", help="show secret")
        @click.argument("secret_id")
        def get_secret(secret_id):
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                response = tfs_client.get_secret(secret_id)
                print_obj(response["id"], response)
            except Exception as e:
                handle_exception(e)

    @get_command.command(name="context", help="show current context")
    def get_current_context():
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            cluster = tfs_client.session.get_cluster()
            workspace = tfs_client.session.get_workspace()
            if workspace:
                click.echo(f"Workspace: {workspace['name']} ({cluster['id']})")
            elif cluster:
                click.echo(f"No workspaces found ({cluster['id']})")
            else:
                click.echo(
                    f"Context not set. Please use `sfy use workspace` to pick a default workspace"
                )
        except Exception as e:
            handle_exception(e)

    return get_command
