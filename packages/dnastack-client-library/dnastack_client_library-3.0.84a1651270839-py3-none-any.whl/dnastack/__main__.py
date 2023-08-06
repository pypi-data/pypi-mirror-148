import click

from dnastack.cli.auth.commands import auth
from dnastack.cli.cli_config.commands import config_command_group
from dnastack.cli.collections.commands import collection_command_group
from dnastack.cli.dataconnect.commands import data_connect_command_group
from dnastack.cli.files.commands import drs_command_group
from .constants import (
    __version__,
)


@click.group("dnastack")
@click.version_option(__version__, message="%(version)s")
def dnastack():
    """DNAstack Client CLI

    https://www.dnastack.com
    """
    pass


@dnastack.command("version")
def get_version():
    click.echo(__version__)


# noinspection PyTypeChecker
dnastack.add_command(data_connect_command_group)
# noinspection PyTypeChecker
dnastack.add_command(config_command_group)
# noinspection PyTypeChecker
dnastack.add_command(drs_command_group)
# noinspection PyTypeChecker
dnastack.add_command(auth)
# noinspection PyTypeChecker
dnastack.add_command(collection_command_group)

if __name__ == "__main__":
    dnastack.main(prog_name="dnastack")
