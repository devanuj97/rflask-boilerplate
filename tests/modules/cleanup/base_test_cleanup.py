import unittest
from typing import Callable

from modules.account.types import SearchAccountByIdParams


class BaseTestCleanup(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        self.params = SearchAccountByIdParams(id="67972da02287e045dcd2ea30")

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
