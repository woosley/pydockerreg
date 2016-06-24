import click

from . import config
from . import client
from .shells.index import Index

@click.command()
@click.argument("url")
def cli(url):
    click.echo("connecting to {}....".format(url))
    created, config_path = config.load()
    if created:
        click.echo("No config found, created a new one at {}".format(config_path))
    session = client.session(url)
    res = session.get()
    if res.status_code != 200:
        raise Exception("registry returned {}, is it v2?".format(
            res.status_code))

    start_main(session)
    click.echo("goodbye")


def start_main(session):
    Index(session).run()
