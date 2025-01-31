import logging
from logging.handlers import SysLogHandler

from modules.config.config_service import ConfigService
from modules.config.types import PapertrailConfig
from modules.logger.internal.base_logger import BaseLogger


class PapertrailLogger(BaseLogger):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create a console handler and set the level to INFO
        logger_config = PapertrailConfig(
            host=ConfigService[str].get_value(key="papertrail.host"),
            port=ConfigService[int].get_value(key="papertrail.port"),
        )
        papertrail_handler = SysLogHandler(address=(logger_config.host, logger_config.port))
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        papertrail_handler.setFormatter(formatter)

        self.logger.addHandler(papertrail_handler)

    def critical(self, *, message: str) -> None:
        self.logger.critical(msg=message)

    def debug(self, *, message: str) -> None:
        self.logger.debug(msg=message)

    def error(self, *, message: str) -> None:
        self.logger.error(msg=message)

    def info(self, *, message: str) -> None:
        self.logger.info(msg=message)

    def warn(self, *, message: str) -> None:
        self.logger.warning(msg=message)
