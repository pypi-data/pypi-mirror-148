from typing import Optional

import click

from .helper import handle_query
from .local_client_repository import LocalClientRepository
from ..exporter import to_json
from ..utils import handle_error_gracefully, allow_to_specify_endpoint


@click.group("dataconnect")
def data_connect_command_group():
    pass


@data_connect_command_group.command("query")
@click.argument("query")
@click.option(
    "-o",
    "--output",
    help="The path to the output file (Note: If the option is specified, there will be no output to stdout.)",
    required=False,
    default=None
)
@click.option(
    "-f",
    "--format",
    help="Output Format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True
)
@click.option(
    "--decimal-as",
    type=click.Choice(["string", "float"]),
    show_choices=True,
    default="string",
    show_default=True,
)
@allow_to_specify_endpoint
@handle_error_gracefully
def data_connect_query(endpoint_id: str,
                       endpoint_url: str,
                       query: str,
                       output: Optional[str] = None,
                       format: str = "json",
                       decimal_as: str = 'string'):
    """
    Perform a query with a Data Connect service
    """
    return handle_query(LocalClientRepository.get(endpoint_id, endpoint_url),
                        query,
                        format,
                        decimal_as,
                        output_file=output)


@click.group("tables")
def table_command_group():
    pass


@table_command_group.command("list")
@allow_to_specify_endpoint
@handle_error_gracefully
def list_tables(endpoint_id: str, endpoint_url: str):
    click.echo(to_json([t.dict() for t in LocalClientRepository.get(endpoint_id, endpoint_url).list_tables()]))


@table_command_group.command("get")
@click.argument("table_name")
@allow_to_specify_endpoint
@handle_error_gracefully
def get(endpoint_id: str, endpoint_url: str, table_name: str):
    click.echo(to_json(LocalClientRepository.get(endpoint_id, endpoint_url).table(table_name).info.dict()))


# noinspection PyTypeChecker
data_connect_command_group.add_command(table_command_group)
