import logging
import os
from pathlib import Path

import click
from click import ClickException

import hukudo.chromedriver
from hukudo.log import LOG_LEVELS, configure_structlog_dev
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
    logging.basicConfig(format='%(msg)s')


# noinspection PyTypeChecker
root.add_command(grafana)


@root.group()
def chromedriver():
    pass


@chromedriver.command()
@click.argument('target_dir', type=click.Path(path_type=Path), required=False)
def download(target_dir):
    """
    Downloads the latest chromedriver for your Chrome Browser.
    Naming convention: chromedriver-${VERSION}.
    Example:

        hukudo chromedriver download /tmp/

    Results in `/tmp/chromedriver-
    """
    if target_dir is None:
        target_dir = Path()
    if not target_dir.is_dir():
        raise ClickException(f'not a directory: {target_dir}')
    try:
        hukudo.chromedriver.download_latest(target_dir)
    except FileExistsError as e:
        raise ClickException(f'file exists: {e}')


def main():
    root()
