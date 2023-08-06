import logging
import os

import click

from hukudo.logging import LOG_LEVELS, configure_structlog_dev
from .grafana.cli import grafana


@click.group()
@click.option(
    '-l',
    '--log-level',
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
    default=os.environ.get('LOGLEVEL', 'WARNING'),
)
def root(log_level):
    """
    For completion, add this to ~/.bashrc:

        eval "$(_HUKUDO_COMPLETE=bash_source hukudo)"

    See also https://click.palletsprojects.com/en/8.1.x/shell-completion/
    """
    configure_structlog_dev(log_level)
    logging.basicConfig(level=log_level, format='%(msg)s')


# noinspection PyTypeChecker
root.add_command(grafana)


def main():
    root()
