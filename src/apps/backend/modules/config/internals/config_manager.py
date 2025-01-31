import os
from pathlib import Path
from typing import Any, Optional

from modules.config.internals.config_file import ConfigFile


class ConfigManager:
    """
    Manages application configuration by loading, merging, and providing access to config values.
    """

    CONFIG_KEY_SEPARATOR: str = "."

    def __init__(self) -> None:
        self.config_store: dict[str, Any] = {}
        self.config_path = self._get_base_directory(__file__) / "config"

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Retrieve a configuration value using dot-separated keys.
        """
        value = self.config_store
        for k in key.split(self.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return default
            value = value[k]
        return value

    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        """
        value = self.config_store
        for k in key.split(self.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return False
            value = value[k]
        return True

    def load_config(self) -> None:
        """
        Load and merge configuration files from the config directory.
        """
        default_config = ConfigFile("default.yml", self.config_path)
        default_config.load()

        app_env = os.environ.get("APP_ENV", "development")
        app_env_config = ConfigFile(f"{app_env}.yml", self.config_path)
        app_env_config.load()
        default_config.merge(app_env_config)

        custom_env_config = ConfigFile("custom-environment-variables.yml", self.config_path)
        custom_env_config.load()
        custom_env_config.replace_with_env_variables()

        default_config.merge(custom_env_config)

        self.config_store = default_config.get_content()

    @staticmethod
    def _get_base_directory(current_file: str) -> Path:
        """
        Get the base directory of the project.
        """
        starting_index = current_file.find("app")
        base_directory = current_file[: starting_index + len("app")]
        return Path(base_directory)
