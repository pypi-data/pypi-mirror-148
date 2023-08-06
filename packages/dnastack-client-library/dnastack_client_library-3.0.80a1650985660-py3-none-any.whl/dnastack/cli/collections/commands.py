import click

from .local_client_repository import LocalClientRepository
from ..dataconnect.helper import handle_query
from ..exporter import normalize, to_json
from ..utils import handle_error_gracefully, allow_to_specify_endpoint


@click.group("collections")
def collection_command_group():
    pass


@collection_command_group.command(name="list", help="List collections")
@allow_to_specify_endpoint
@handle_error_gracefully
def list_collections(endpoint_id: str, endpoint_url: str):
    click.echo(to_json(normalize(LocalClientRepository.get(endpoint_id, endpoint_url).list_collections())))


@collection_command_group.command("query", help="Query data")
@click.argument("collection_name")
@click.argument("query")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True,
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
def query_collection(endpoint_id: str,
                     endpoint_url: str,
                     collection_name: str,
                     query: str,
                     format: str = "json",
                     decimal_as: str = 'string'):
    return handle_query(LocalClientRepository.get(endpoint_id, endpoint_url).data_connect(collection_name),
                        query,
                        format,
                        decimal_as)


@click.group("tables")
def table_command_group():
    """Data Client API for Collections"""
    pass


@table_command_group.command(
    "list",
    help="""
    List tables for a given collection

    ID_OR_SLUG_NAME is the ID or slug name of the target collection.
    """
)
@click.argument("id_or_slug_name")
@allow_to_specify_endpoint
@handle_error_gracefully
def list_tables(endpoint_id: str, endpoint_url: str, id_or_slug_name: str):
    click.echo(to_json([
        t.dict()
        for t in LocalClientRepository.get(endpoint_id, endpoint_url).data_connect(id_or_slug_name).list_tables()
    ]))


# noinspection PyTypeChecker
collection_command_group.add_command(table_command_group)
