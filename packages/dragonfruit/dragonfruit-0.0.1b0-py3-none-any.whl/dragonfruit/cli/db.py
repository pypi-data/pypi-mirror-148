import click

from dragonfruit import get_settings
from dragonfruit.cli.main import cli


@cli.group()
def db():
    raise NotImplementedError("This class is currently broken - sorry")


@db.command()
@click.option(
    "-p", "--profile", "profile", default=get_settings().default_profile, show_default=True
)
def summary(profile):
    # TODO: Update this with the new system
    pass


@db.command()
@click.option(
    "-p", "--profile", "profile", default=get_settings().default_profile, show_default=True
)
@click.argument("types", type=str)
def list(profile, types):
    # TODO Update this with the new system
    pass
