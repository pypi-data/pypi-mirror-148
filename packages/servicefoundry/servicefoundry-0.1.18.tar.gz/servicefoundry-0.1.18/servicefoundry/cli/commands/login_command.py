import logging
import webbrowser

import rich_click as click

from servicefoundry.build.clients.auth_service_client import AuthServiceClient
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.const import SESSION_FILE
from servicefoundry.build.session_factory import DEFAULT_TENANT_ID, get_session
from servicefoundry.build.util import (
    BadRequestException,
    format_cluster,
    format_workspace,
)

logger = logging.getLogger(__name__)


def try_set_use_context():
    client = ServiceFoundryServiceClient.get_client()
    workspaces = client.list_workspace()
    if len(workspaces) == 1:
        workspace = workspaces[0]
        # TODO (chiragjn): Temporarily just storing cluster id
        client.session.set_cluster(format_cluster({"id": workspace["clusterId"]}))
        click.echo(f"Setting {workspace['name']!r} as the default workspace")
        client.session.set_workspace(format_workspace(workspace))
        client.session.save_session()
        click.echo("You can now start creating services with `servicefoundry init`")
    else:
        clusters = client.list_cluster()
        if len(clusters) == 1:
            cluster = clusters[0]
            # click.echo(f"Setting {cluster['name']!r} as the default cluster")
            client.session.set_cluster(format_cluster(cluster))
            client.session.save_session()
        elif clusters:
            click.echo(
                f"More than one cluster found. Use `servicefoundry use cluster` to pick a default cluster"
            )

        if workspaces:
            click.echo(
                f"More than one workspace found. Use `servicefoundry use workspace` to pick a default workspace"
            )
        else:
            click.echo(
                "You can now create a workspace with `servicefoundry create workspace`"
            )


def login_user():
    auth_client = AuthServiceClient()
    url, user_code, device_code = auth_client.get_device_code(DEFAULT_TENANT_ID)
    click.echo(f"Login Code: {user_code}")
    click.echo(
        f"Waiting for your authentication. Go to url to complete the authentication: {url}"
    )
    try:
        webbrowser.open_new(url)
    except webbrowser.Error:
        pass
    session = auth_client.poll_for_auth(DEFAULT_TENANT_ID, device_code)
    session.save_session()
    click.echo(f"Successful Login. Session file will be stored at {SESSION_FILE}.")
    try:
        try_set_use_context()
    except Exception:
        logger.exception("Failed to set context")
        click.echo("Run `servicefoundry use workspace` to pick a default workspace")


def get_login_command():
    @click.command()
    def login():
        """
        Create a servicefoundry login

        \b
        Once logged in, you can initiate a new service with `servicefoundry init`
        and run the service with `servicefoundry run .`
        """
        try:
            session = get_session()
            user = session.get_user_details()
            out = (
                f"You are logged in as {user['username']} with email {user['email']}.\n"
                f"Initiate a new service by running ```servicefoundry init```"
            )
            print(out)
        except BadRequestException:
            login_user()

    return login
