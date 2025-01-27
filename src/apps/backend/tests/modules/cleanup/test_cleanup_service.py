from unittest.mock import patch

from modules.cleanup.cleanup_service import CleanupService
from modules.cleanup.internal.cleanup_manager import cleanup_manager
from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup


class TestCleanupService(BaseTestCleanup):
    @patch.object(cleanup_manager, "register_hook")
    def test_register_hook_decorator(self, mock_register_hook):
        """Test registering a regular cleanup hook using the decorator."""

        @CleanupService.register()
        def dummy_hook(params):
            pass

        mock_register_hook.assert_called_once_with(dummy_hook, final=False)

    @patch.object(cleanup_manager, "register_hook")
    def test_register_final_hook_decorator(self, mock_register_hook):
        """Test registering a final cleanup hook using the decorator."""

        @CleanupService.register(final=True)
        def dummy_final_hook(params):
            pass

        mock_register_hook.assert_called_once_with(dummy_final_hook, final=True)

    @patch.object(cleanup_manager, "execute_hooks")
    def test_execute_cleanup_hooks(self, mock_execute_hooks):
        """Test executing cleanup hooks through the service."""
        CleanupService.execute_cleanup_hooks(params=self.params)
        mock_execute_hooks.assert_called_once_with(params=self.params)
