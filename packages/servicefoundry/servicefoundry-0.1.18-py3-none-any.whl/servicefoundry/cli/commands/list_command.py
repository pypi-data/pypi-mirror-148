import logging
import rich_click as click
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.model.entity import Cluster, Workspace
from servicefoundry.cli.const import (
    ENABLE_AUTHORIZE_COMMANDS,
    ENABLE_CLUSTER_COMMANDS
)
from servicefoundry.cli.display_util import print_list

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


def get_list_command():
    @click.group(name="list")
    def list_command():
        """
        Servicefoundry list entities

        \b
        Supported entities:
        - workspace
        - service
        - deployment
        - secret-group
        - secret
        """
        pass

    if ENABLE_CLUSTER_COMMANDS:

        @list_command.command(name="cluster", help="list cluster")
        def list_cluster():
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                clusters = tfs_client.list_cluster()
                print_list("Clusters", clusters, Cluster().display_columns_ps)
            except Exception as e:
                handle_exception(e)

    @list_command.command(name="workspace", help="list workspaces")
    def list_workspace():
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            spaces = tfs_client.list_workspace()
            print_list("Workspaces", spaces, Workspace().display_columns_ps)
        except Exception as e:
            handle_exception(e)

    @list_command.command(name="service", help="list service in a workspace")
    @click.option(
        "--workspace", type=click.STRING, help="workspace to list services from."
    )
    def list_service(workspace):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            current_workspace = tfs_client.session.get_workspace()
            if workspace is None:
                # Name is not passed, if not in context raise and Exception
                if current_workspace is None:
                    raise Exception(
                        "workspace is not passed in as option nor is available in context. "
                        "Use `servicefoundry use workspace` to pick a default workspace."
                    )

                workspace_id = current_workspace["id"]
                workspace = current_workspace["name"]
            else:
                # Name is passed, if not same as context fetch and forward
                if workspace == current_workspace["name"]:
                    workspace_id = current_workspace["id"]
                else:
                    cluster_id = tfs_client.session.get_cluster()["id"]
                    spaces = tfs_client.get_workspace_by_name(workspace, cluster_id)
                    if len(spaces) > 1:
                        raise Exception("More than one space found with the same name.")

                    workspace_id = spaces[0]["id"]

            services = tfs_client.list_service_by_workspace(workspace_id)
            print_list(f"Services in Workspace ({workspace})", services)
        except Exception as e:
            handle_exception(e)

    @list_command.command(name="deployment", help="list deployment")
    @click.argument("service_id")
    def list_deployments(service_id):
        try:
            tfs_client: ServiceFoundryServiceClient = (
                ServiceFoundryServiceClient.get_client()
            )
            deployments = tfs_client.list_deployment(service_id)
            print_list(
                f"Deployments of Service: {service_id}",
                deployments,
            )
        except Exception as e:
            handle_exception(e)

    @list_command.command(name="secret-group", help="list secret groups")
    def list_secret_group():
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_secret_groups()
            print_list("Secret Groups", response)
        except Exception as e:
            handle_exception(e)

    @list_command.command(name="secret", help="list secrets in a group")
    @click.argument("secret_group_id")
    def list_secret(secret_group_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_secrets_in_group(secret_group_id)
            print_list("Secrets", response)
        except Exception as e:
            handle_exception(e)

    if ENABLE_AUTHORIZE_COMMANDS:

        @list_command.command(
            name="authorize", help="list authorization for a resource id."
        )
        @click.argument(
            "resource_type", type=click.Choice(["workspace"], case_sensitive=False)
        )
        @click.argument("resource_id")
        def list_authorize(resource_type, resource_id):
            try:
                tfs_client = ServiceFoundryServiceClient.get_client()
                response = tfs_client.get_authorization_for_resource(
                    resource_type, resource_id
                )
                print_list(f"Auth for {resource_type}: {resource_id}", response)
            except Exception as e:
                handle_exception(e)

    return list_command
