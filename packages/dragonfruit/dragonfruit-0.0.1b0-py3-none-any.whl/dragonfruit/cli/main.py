import click

import minkipy
import minkipy.cli

from dragonfruit.version import __version__


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
def gui():
    try:
        import mincepy_gui  # pylint: disable=import-outside-toplevel
    except ImportError:
        click.echo("mincepy_gui is not installed (try: pip install mincepy_gui)")
    else:
        project = minkipy.workon()
        conn_params = project.mincepy.get("connection_params", None)
        default_uri = None
        if isinstance(conn_params, str):
            default_uri = conn_params

        mincepy_gui.start(default_uri)


# Import all minki CLI commands directly into our CLI
for command in minkipy.cli.minki.commands.values():
    cli.add_command(command)
