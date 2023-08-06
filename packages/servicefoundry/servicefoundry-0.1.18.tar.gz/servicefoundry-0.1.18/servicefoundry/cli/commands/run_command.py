import logging

import rich_click as click
from rich.console import Console

from servicefoundry.build.build import LOCAL, REMOTE, build_and_deploy
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.display_util import print_obj
from servicefoundry.cli.rich_output_callback import RichOutputCallBack
from servicefoundry.cli.util import handle_exception

console = Console()
logger = logging.getLogger(__name__)


def get_run_command():
    @click.command(help="Create servicefoundry run")
    @click.option("--local", is_flag=True, default=False)
    @click.option("--env", "-e", type=click.STRING)
    @click.argument("service_dir", type=click.Path(exists=True), nargs=1, default="./")
    def run(local, env, service_dir):
        try:
            build = LOCAL if local else REMOTE
            # @TODO Give ability to user confirmation.
            deployment = build_and_deploy(
                env=env,
                base_dir=service_dir,
                build=build,
                callback=RichOutputCallBack(),
            )
            print_obj("Deployment", deployment)
            if not CliConfig.get("json"):
                # tail logs
                tfs_client = ServiceFoundryServiceClient.get_client()
                tfs_client.tail_logs(deployment["runId"])
        except Exception as e:
            handle_exception(e)

    return run
