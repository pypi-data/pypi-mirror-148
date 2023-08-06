import click

from dragonfruit.cli.main import cli
import dragonfruit.slurm as ms


@cli.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--sbatch_args",
    "-a",
    default="",
    help=(
        "Arguments to be passed on to the sbatch function. To pass multiple arguments,"
        ' use quotation marks.\nExample: -a "-N 1 -p xeon40 --ntasks-per-node=40"'
    ),
)
@click.option(
    "--depend/--no-depend",
    default=False,
    help=("Make the job depend on self. " "Only works if called from inside a slurm environment"),
)
@click.argument("scriptargs", nargs=-1)
def sbatch(filename, sbatch_args, script_args, depend):
    """Submit a dragonfruit job to a SLURM queue"""

    script = ms.py_to_sh(filename, script_args=script_args)

    # Create the flags and cmd call
    cmd = ms.create_command(sbatch_args=sbatch_args, depend_self=depend)

    # Call the script
    ms.submit_script(script, cmd)
