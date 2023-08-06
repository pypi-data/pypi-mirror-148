import click
from dragonfruit.cli.main import cli
from dragonfruit import get_settings, DEFAULT_SETTINGS


@cli.group()
def profile():
    pass


@profile.command()
@click.option(
    "-p", "--profile", "profile_name", default="default", show_default=True, prompt="Profile"
)
def new(profile_name):
    settings = get_settings()
    if not settings.app_dir.exists():
        settings.app_dir.mkdir()

    try:
        settings.get_profile(profile_name)
    except ValueError:
        # Doesn't exist, continue
        pass
    else:
        # Does exist..check what to do
        if not click.confirm("Profile '{}' already exists.  Reset?.".format(profile_name)):
            click.echo("Exiting.")
            return 1

    settings.profiles[profile_name] = DEFAULT_SETTINGS
    if click.confirm("Make this profile default?"):
        click.echo('Storing profile "{}" as the default profile'.format(profile_name))
        settings.default_profile = profile_name

    settings.write_settings()
    click.echo(
        "Default settings written to '{}', change this to reflect your configuration".format(
            settings.settings_path
        )
    )

    return 0


@profile.command()
@click.argument("profile_name")
def default(profile_name):
    settings = get_settings()

    if profile_name not in settings.profiles:
        msg = 'Profile "{}" not in list of profiles.\n'.format(profile_name)
        msg += 'Run "fruit profile show" to see a list of available profiles"'
        click.echo(msg)
    settings.default_profile = profile_name
    settings.write_settings()


@profile.command()
@click.argument("profile_name")
def delete(profile_name):
    settings = get_settings()

    if profile_name == settings.default_profile:
        msg = 'Cannot delete current default profile "{}"'.format(profile_name)
        click.echo(msg)
        return
    profiles = settings.profiles
    if profile_name in profiles:
        del profiles[profile_name]
    else:
        msg = 'Profile "{}" not found.'.format(profile_name)
        click.echo(msg)
        return
    settings.write_settings()


@profile.command()
@click.option("-p", "--profile", "profile_name")
def list(profile_name):
    settings = get_settings()
    click.echo("Profiles in: {}".format(settings.settings_path.resolve()))

    profiles = settings.profiles

    if not profiles:
        click.echo("No profiles found.")
        return

    if profile_name:
        list_single_profile(profile_name)
    else:
        list_all_profiles()


def list_single_profile(profile_name):
    settings = get_settings()

    profiles = settings.profiles
    cur_profile = profiles.get(profile_name, None)
    if cur_profile:
        click.echo("Settings of profile {}:".format(profile_name))
        for key, value in cur_profile.items():
            click.echo("    {:<10} {}".format(key + ":", value))
    else:
        click.echo('No profile named "{}" was found'.format(profile_name))


def list_all_profiles():
    settings = get_settings()

    profiles = settings.profiles
    click.echo("Available profiles: (* denotes default)")
    for name in profiles.keys():
        if name == settings.default_profile:
            name = "{}*".format(name)
        click.echo("  - {}".format(name))


if __name__ == "__main__":
    profile()
