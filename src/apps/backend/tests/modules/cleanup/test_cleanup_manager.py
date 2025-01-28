from unittest.mock import MagicMock

from modules.account.errors import AccountNotFoundError
from modules.cleanup.internal.cleanup_manager import CleanupManager
from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup


class TestCleanupManager(BaseTestCleanup):
    def setUp(self):
        """Setup for CleanupManager tests."""
        self.cleanup_manager = CleanupManager()

    def test_register_pre_cleanup_check(self):
        mock_check = MagicMock(return_value=True)
        mock_check.__name__ = "mock_check"
        self.cleanup_manager.register_pre_cleanup_check(mock_check)
        self.assertEqual(self.cleanup_manager.pre_cleanup_check, mock_check)

    def test_register_main_hook(self):
        mock_main_hook = MagicMock()
        mock_main_hook.__name__ = "mock_main_hook"
        self.cleanup_manager.register_hook(mock_main_hook, main=True)
        self.assertEqual(self.cleanup_manager.main_hook, mock_main_hook)

    def test_queue_cleanup_success(self):
        mock_check = MagicMock(return_value=True)
        mock_check.__name__ = "mock_check"
        mock_main_hook = MagicMock()
        mock_main_hook.__name__ = "mock_main_hook"
        mock_hook = MagicMock()
        mock_hook.__name__ = "mock_hook"

        self.cleanup_manager.register_pre_cleanup_check(mock_check)
        self.cleanup_manager.register_hook(mock_main_hook, main=True)
        self.cleanup_manager.register_hook(mock_hook)

        self.cleanup_manager.queue_cleanup(self.params)
        self.cleanup_manager.stop_worker()

        mock_main_hook.assert_called_once_with(params=self.params)
        mock_hook.assert_called_once_with(params=self.params)

    def test_queue_cleanup_fails_if_account_not_found(self):
        mock_check = MagicMock(return_value=None)
        mock_check.__name__ = "mock_check"
        self.cleanup_manager.register_pre_cleanup_check(mock_check)

        with self.assertRaises(AccountNotFoundError):
            self.cleanup_manager.queue_cleanup(self.params)
