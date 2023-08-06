import json
from pathlib import Path
import click

__all__ = ("Settings", "get_settings")


class Settings:
    def __init__(self):
        self.app_dir = Path(click.get_app_dir("dragonfruit", roaming=False))
        self.settings_path = self.app_dir / "settings.json"
        if self.settings_path.exists():
            self._settings = self.read_settings()
        else:
            self._settings = {}

    def read_settings(self):
        self._check_settings_exists()
        with self.settings_path.open("r") as file:
            return json.load(file)

    def write_settings(self):
        with self.settings_path.open("w") as file:
            json.dump(self._settings, file, indent=4)

    def _check_settings_exists(self):
        if not self.settings_path.exists():
            msg = "No settings file found, expected: {}".format(self.settings_path)
            msg += '\nRun "fruit profile new" to set up a new profile.'
            raise ValueError(msg)

    @property
    def profiles(self):
        return self._settings.setdefault("profiles", {})

    @profiles.setter
    def profiles(self, profiles):
        self._settings["profiles"] = profiles

    def get_profile(self, profile=None):
        profile = profile or self.default_profile

        profiles = self.profiles
        if profile not in profiles:
            msg = 'No profile named "{}" was found'.format(profile)
            msg += '\nRun "fruit profile new" to set up a new profile.'
            raise ValueError(msg)
        return profiles.get(profile)

    @property
    def default_profile(self):
        return self._settings.get("default_profile", None)

    @default_profile.setter
    def default_profile(self, default_profile):
        self._settings["default_profile"] = default_profile


SETTINGS = None


def get_settings() -> Settings:
    global SETTINGS  # pylint: disable=global-statement
    if SETTINGS is None:
        SETTINGS = Settings()

    return SETTINGS
