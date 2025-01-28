from unittest.mock import MagicMock

from modules.cleanup.cleanup_service import CleanupService
from modules.cleanup.internal.cleanup_manager import cleanup_manager

from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup


class TestCleanupService(BaseTestCleanup):
    def test_register_check_decorator(self):
        @CleanupService.check()
        def mock_check(params):
            return True

        self.assertEqual(cleanup_manager.pre_cleanup_check, mock_check)

    def test_register_main_hook_decorator(self):
        @CleanupService.register(main=True)
        def mock_main_hook(params):
            pass

        self.assertEqual(cleanup_manager.main_hook, mock_main_hook)

    def test_execute_cleanup_hooks(self):
        mock_check = MagicMock(return_value=True)
        mock_check.__name__ = "mock_check"
        mock_main_hook = MagicMock()
        mock_main_hook.__name__ = "mock_main_hook"
        mock_hook = MagicMock()
        mock_hook.__name__ = "mock_hook"

        cleanup_manager.register_pre_cleanup_check(mock_check)
        cleanup_manager.register_hook(mock_main_hook, main=True)
        cleanup_manager.register_hook(mock_hook)

        CleanupService.execute_cleanup_hooks(params=self.params)
        cleanup_manager.stop_worker()

        mock_main_hook.assert_called_once_with(params=self.params)
        mock_hook.assert_called_once_with(params=self.params)
