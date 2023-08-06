import logging

import rich_click as click

from servicefoundry.build.session_factory import logout_session
from servicefoundry.cli.util import handle_exception
from servicefoundry.build.exceptions import BadRequestException
from servicefoundry.cli.util import print_message

logger = logging.getLogger(__name__)


def get_logout_command():
    @click.command(help="Logout servicefoundry session")
    def logout():
        try:
            logout_session()
        except BadRequestException:
            print_message("You are already Logged out.")
        except Exception as e:
            handle_exception(e)

    return logout
