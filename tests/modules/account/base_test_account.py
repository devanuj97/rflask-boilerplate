import unittest
from typing import Callable

from modules.account.internal.store.account_repository import AccountRepository
from modules.account.rest_api.account_rest_api_server import AccountRestApiServer
from modules.config.config_service import ConfigService
from modules.logger.logger_manager import LoggerManager
from modules.otp.internal.store.otp_repository import OtpRepository


class BaseTestAccount(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        ConfigService.load_config()
        LoggerManager.mount_logger()
        AccountRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        AccountRepository.collection().delete_many({})
        OtpRepository.collection().delete_many({})
