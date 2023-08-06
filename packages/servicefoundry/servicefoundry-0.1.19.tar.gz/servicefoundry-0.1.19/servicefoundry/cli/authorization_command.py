import logging

import click

from servicefoundry.cli.display_util import print_obj

from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .util import handle_exception

logger = logging.getLogger(__name__)


def get_authorization_command():
    @click.group(name="auth", help="servicefoundry auth list|create|update|remove ")
    def authorize():
        pass

    @authorize.command(name="create", help="create auth")
    @click.argument("resource_type")
    @click.argument("resource_id")
    @click.argument("user_id")
    @click.argument("role")
    def create(resource_id, resource_type, user_id, role):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.create_authorization(
                resource_id, resource_type, user_id, role
            )
            print_obj(f"Auth for {resource_type}: {resource_id}", response)
        except Exception as e:
            handle_exception(e)

    @authorize.command(name="update", help="update auth")
    @click.argument("authorization_id")
    @click.argument("role")
    def update(authorization_id, role):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.update_authorization(authorization_id, role)
        except Exception as e:
            handle_exception(e)

    return authorize
