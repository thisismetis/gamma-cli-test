import click
import pandas as pd
import yaml

from .utils import get_config

pd.set_option('max_colwidth', 200)


@click.group()
def gamma():
    """Hold place for command."""
    pass


@gamma.command()
def status():
    config = get_config()
    click.echo("Your current configuration is:")
    click.echo(yaml.dump(config, default_flow_style=False))
