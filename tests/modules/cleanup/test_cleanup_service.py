from unittest.mock import MagicMock, patch

from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup

from modules.cleanup.cleanup_service import CleanupService


class TestCleanupService(BaseTestCleanup):
    @patch("modules.cleanup.internal.cleanup_manager.CleanupManager.register_hook")
    def test_register(self, mock_register_hook):
        func = MagicMock(__name__="mock_func")
        decorator = CleanupService.register(
            module_name="mock_module", class_name="MockClass"
        )
        decorated_func = decorator(func)

        mock_register_hook.assert_called_once_with(
            func=func, module_name="mock_module", class_name="MockClass", main=False
        )
        self.assertEqual(decorated_func, func)

    @patch("modules.cleanup.internal.cleanup_manager.CleanupManager.push_hooks")
    def test_push_hooks(self, mock_push_hooks):
        CleanupService.push_hooks()
        mock_push_hooks.assert_called_once()

    @patch(
        "modules.cleanup.internal.cleanup_manager.CleanupManager.queue_account_deletion"
    )
    def test_queue_account_deletion(self, mock_queue_account_deletion):
        CleanupService.queue_account_deletion(params=self.params)
        mock_queue_account_deletion.assert_called_once_with(params=self.params)
