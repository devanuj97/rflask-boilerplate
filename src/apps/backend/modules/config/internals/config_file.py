from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import yaml


class ConfigFile:
    """
    Represents a configuration file that can be loaded, merged, and updated with environment variables.
    """

    def __init__(self, filename: str, config_path: Path):
        self.filename = filename
        self.config_path = config_path
        self.content: dict[str, Any] = {}

    def load(self) -> None:
        """
        Loads the content of the configuration file.
        """
        file_path = self.config_path / self.filename
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.content = yaml.safe_load(file) or {}
        except FileNotFoundError:
            from modules.logger.logger import Logger

            Logger.error(message=f"Config file '{self.filename}' not found.")

    def merge(self, other: ConfigFile) -> None:
        """
        Merges the content of another ConfigFile into this one.
        """
        self.content = self._deep_merge(self.content, other.content)

    def replace_with_env_variables(self) -> None:
        """
        Replaces placeholders in the configuration file with corresponding environment variables.
        """
        self.content = self._replace_with_env_values(self.content)

    def get_content(self) -> dict[str, Any]:
        """
        Returns the loaded content of the config file.
        """
        return self.content

    @staticmethod
    def _deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """
        Deep merge two dictionaries.
        """
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                dict1[key] = ConfigFile._deep_merge(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    @staticmethod
    def _replace_with_env_values(data: dict[str, Any]) -> dict[str, Any]:
        """
        Replace dictionary values with corresponding environment variables if defined.
        """
        if not isinstance(data, dict):
            return data

        keys_to_delete: list = []

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = ConfigFile._process_dict_value(value)
            elif isinstance(value, str):
                ConfigFile._process_str_value(data, key, value, keys_to_delete)

        for key in keys_to_delete:
            del data[key]

        return data

    @staticmethod
    def _process_dict_value(value: dict[str, Any]) -> Any:
        """
        Process dictionary values, replacing environment variables where necessary.
        """
        if "__name" in value:
            env_var_name = value["__name"]
            env_var_value = os.getenv(env_var_name)
            value_format = value.get("__format")
            return ConfigFile._parse_value(env_var_value, value_format) if value_format else env_var_value
        return ConfigFile._replace_with_env_values(value)

    @staticmethod
    def _process_str_value(data: dict[str, Any], key: str, value: str, keys_to_delete: list) -> None:
        """
        Replace a string value with an environment variable if it exists. If not found, mark the key for deletion.
        """
        env_value = os.getenv(value)
        if env_value is None:
            keys_to_delete.append(key)
        else:
            data[key] = env_value

    @staticmethod
    def _parse_value(value: Optional[str], value_format: str) -> int | float | bool | None:
        """
        Parse a value based on the specified format ('boolean' or 'number').
        """
        if value is None:
            return None

        parsers = {
            "boolean": lambda x: x.lower() in ["true", "1"],
            "number": lambda x: int(x) if x.isdigit() else float(x),
        }

        parser = parsers.get(value_format)
        if not parser:
            raise ValueError(f"Unsupported format: {value_format}")

        try:
            return parser(value)
        except Exception as e:
            raise ValueError(f"Error parsing value '{value}' as {value_format}: {e}") from e
