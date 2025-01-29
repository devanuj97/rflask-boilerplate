from unittest.mock import ANY, MagicMock, patch

from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup

from modules.cleanup.internal.cleanup_manager import CleanupManager
from modules.cleanup.types import CreateAccountDeletionRequestParams


class TestCleanupManager(BaseTestCleanup):
    def setUp(self):
        """Setup for CleanupManager tests."""
        self.cleanup_manager = CleanupManager()

    @patch(
        "modules.cleanup.internal.cleanup_module_writer.CleanupModuleWriter.add_cleanup_module"
    )
    def test_register_hook(self, mock_add_cleanup_module):
        func = MagicMock(__name__="mock_func")
        self.cleanup_manager.register_hook(func, "mock_module", "MockClass")

        self.assertEqual(len(self.cleanup_manager.HOOKS), 1)
        hook = self.cleanup_manager.HOOKS[0]
        self.assertEqual(hook.module_name, "mock_module")
        self.assertEqual(hook.class_name, "MockClass")
        self.assertEqual(hook.function_name, "mock_func")
        mock_add_cleanup_module.assert_not_called()

    @patch(
        "modules.cleanup.internal.cleanup_module_writer.CleanupModuleWriter.add_cleanup_module"
    )
    def test_push_hooks(self, mock_add_cleanup_module):
        func = MagicMock(__name__="mock_func")
        self.cleanup_manager.register_hook(func, "mock_module", "MockClass")
        self.cleanup_manager.push_hooks()

        mock_add_cleanup_module.assert_called_once()
        self.assertEqual(len(self.cleanup_manager.HOOKS), 0)

    @patch(
        "modules.account.account_service.AccountService.get_account_by_id",
        return_value=True,
    )
    @patch("modules.account.account_service.AccountService.deactivate_account")
    @patch(
        "modules.cleanup.internal.account_deletion_request_writer.AccountDeletionRequestWriter.create_account_deletion_request"
    )
    def test_queue_account_deletion(
        self, mock_create_request, mock_deactivate_account, mock_get_account
    ):
        self.cleanup_manager.queue_account_deletion(self.params)

        mock_get_account.assert_called_once_with(params=self.params)
        mock_deactivate_account.assert_called_once_with(params=self.params)
        mock_create_request.assert_called_once_with(
            params=CreateAccountDeletionRequestParams(
                account_id=self.params.id, requested_at=ANY
            )
        )

    @patch(
        "modules.account.account_service.AccountService.get_account_by_id",
        return_value=None,
    )
    def test_queue_account_deletion_fails_if_account_not_found(self, mock_get_account):
        with self.assertRaises(Exception) as context:
            self.cleanup_manager.queue_account_deletion(self.params)

        self.assertTrue("Account not found" in str(context.exception))
        mock_get_account.assert_called_once_with(params=self.params)
