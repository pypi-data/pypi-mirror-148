import os

import click
import structlog

from hukudo.grafana import Grafana

logger = structlog.get_logger()


@click.group()
@click.option('-u', '--url', required=True, envvar='GRAFANA_URL')
@click.option('-k', '--api-key', required=True, envvar='GRAFANA_API_KEY')
@click.pass_context
def grafana(ctx, url, api_key):
    ctx.obj = Grafana(
        url=url,
        api_key=api_key,
    )
    log = logger.bind(instance=ctx.obj)

    try:
        root_ca = os.environ['GRAFANA_CLIENT_ROOT_CA']
        log.debug('CA', path=root_ca)
        ctx.obj.session.verify = root_ca
    except KeyError:
        pass

    try:
        crt = os.environ['GRAFANA_CLIENT_CRT']
        key = os.environ['GRAFANA_CLIENT_KEY']
        log.debug('client cert', crt=crt, key=key)
        ctx.obj.session.cert = (crt, key)
    except KeyError:
        pass


@grafana.group()
def dashboards():
    pass


@dashboards.command()
@click.pass_context
def export(ctx):
    """
    Exports dashboards as json files to a directory named after the Grafana domain.
    """
    log = logger.bind(instance=ctx.obj)
    log.info('export')
    from pathlib import Path
    from urllib.parse import urlparse

    root = Path('')
    grafana: Grafana = ctx.obj
    prefix = urlparse(grafana.session.url).netloc

    target = root / prefix
    target.mkdir(parents=True)

    for board in grafana.dashboards():
        filename = target / f'{board.id}.json'
        board.export(filename)
