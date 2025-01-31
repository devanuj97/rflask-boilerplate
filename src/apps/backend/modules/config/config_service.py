from typing import Generic, Optional, cast

from modules.common.types import ErrorCode
from modules.config.internals.config_manager import ConfigManager
from modules.config.types import T
from modules.error.custom_errors import MissingKeyError


class ConfigService(Generic[T]):
    config_manager: ConfigManager = ConfigManager()

    @classmethod
    def load_config(cls) -> None:
        """
        Load the configuration files
        """
        cls.config_manager.load_config()

    @classmethod
    def get_value(cls, key: str, default: Optional[T] = None) -> T:
        """
        Get the value of the key from the configuration
        """
        value: Optional[T] = cls.config_manager.get(key, default=default)
        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)
        return cast(T, value)

    @classmethod
    def has_value(cls, key: str) -> bool:
        """
        Check if the key exists in the configuration
        """
        return cls.config_manager.has(key)
