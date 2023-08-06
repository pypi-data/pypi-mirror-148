import zipfile

import rich_click as click
from requests.exceptions import ConnectionError
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel

from ..build.util import BadRequestException, DefinitionException


def handle_exception(exception):
    if type(exception) == BadRequestException:
        print_error(
            f"[cyan bold]statusCode[/]  {exception.status_code} \n"
            f"[cyan bold]message[/]     {exception.message}"
        )
    elif type(exception) == ConnectionError:
        print_error(f"Couldn't connect to Servicefoundry.")
    elif type(exception) == DefinitionException:
        print_error(f"[cyan bold]message[/]     {exception.message}")
    else:
        console = Console()
        console.print(exception)


def print_error(message):
    console = Console()
    text = Padding(message, (0, 1))
    console.print(
        Panel(
            text,
            border_style="red",
            title="Command failed",
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def print_message(message):
    console = Console()
    text = Padding(message, (0, 1))
    console.print(
        Panel(
            text,
            border_style="cyan",
            title="Success",
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def unzip_package(path_to_package, destination):
    with zipfile.ZipFile(path_to_package, "r") as zip_ref:
        zip_ref.extractall(destination)
