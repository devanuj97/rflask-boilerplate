import os
from pathlib import Path
from typing import Any, Optional
import yaml


class Config:
    _config_dict: dict[str, Any]
    _config_path: Path 

    @staticmethod
    def load_config() -> None:
        Config._intialize_config()
        Config._process_custom_environment_variables()
        print(yaml.dump(Config._config_dict))
        
    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        keys = key.split(".")
        value = Config._config_dict
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    @staticmethod
    def has(key: str) -> bool:
        keys = key.split(".")
        value = Config._config_dict
        try:
            for k in keys:
                value = value[k]
            return True
        except (KeyError, TypeError):
            return False
    
    @staticmethod
    def _read(filename: str) -> dict[str, Any]:
        file_path = Config._config_path / filename
        yaml_content: dict[str, Any] = {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                yaml_content = yaml.safe_load(file)
        except FileNotFoundError as e:
            print(e)
        return yaml_content

    @staticmethod
    def _intialize_config() -> None:
        Config._config_path = Config._get_base_directory(__file__) / "config"
        default_content = Config._read("default.yml")
        app_env = os.environ.get("APP_ENV", "development")
        app_env_content = Config._read(f"{app_env}.yml")
        merge_content = Config._deep_merge(default_content, app_env_content)
        Config._config_dict = merge_content

    @staticmethod
    def _parse_value(value:Optional[str], value_format:str)-> Any:
        """
        Parse the environment variable value based on the specified format.
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


    @staticmethod
    def _replace_with_env_values(data:dict[str,Any]) -> dict[str,Any]:
        """
        Recursively traverse a dictionary and replace values with the corresponding environment variable values
        if the value in the dictionary matches a key in the environment variables.
        """
        if not isinstance(data, dict):
            return data

        keys_to_delete:list = []  # Collect keys to delete

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = Config._process_dict_value(value)
            elif isinstance(value, str):
                Config._process_str_value(data, key, value, keys_to_delete)

        Config._delete_keys(data, keys_to_delete)
        return data

    @staticmethod
    def _process_dict_value(value : dict[str,Any]) -> Any:
        """Process a dictionary value, replacing or recursively traversing it."""
        if "__name" in value:
            env_var_name = value["__name"]
            env_var_value = os.getenv(env_var_name)
            value_format = value.get("__format")
            return Config._parse_value(env_var_value, value_format) if value_format else env_var_value
        return Config._replace_with_env_values(value)

    @staticmethod
    def _process_str_value(data:dict[str,Any], key:str, value:str, keys_to_delete:list) -> None:
        """Process a string value, replacing it with an environment variable or marking for deletion."""
        env_value = os.getenv(value)
        if env_value is None:
            keys_to_delete.append(key)
        else:
            data[key] = env_value

    @staticmethod
    def _delete_keys(data:dict[str,Any], keys_to_delete:list) -> None:
        """Delete keys marked for deletion."""
        for key in keys_to_delete:
            del data[key]

    @staticmethod
    def _get_base_directory(current_file: str) -> Path:
        starting_index = current_file.find("app")
        base_directory = current_file[:starting_index+len("app")]
        return Path(base_directory)

    @staticmethod
    def _process_custom_environment_variables() -> None:
        """
        Reads keys from custom_env_contents, maps them to environment variables,
        and overrides them in the configuration if they exist.
        """
        custom_env_contents = Config._read("custom-environment-variables.yml")
        replaced_custom_env_contents = Config._replace_with_env_values(custom_env_contents)
        Config._deep_merge(Config._config_dict, replaced_custom_env_contents)

    @staticmethod
    def _deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """
        Recursively merges dict2 into dict1. Values from dict2 will overwrite those in dict1.
        If a value is a nested dictionary, it will be merged as well.
        """
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                # If both are dictionaries, merge them recursively
                dict1[key] = Config._deep_merge(dict1[key], value)
            else:
                # If not a dictionary, just overwrite or add the key-value pair
                dict1[key] = value
        return dict1    
