from datetime import UTC, datetime
from typing import Callable, List

from modules.account.errors import AccountNotFoundError
from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.account_deletion_request_writer import (
    AccountDeletionRequestWriter,
)
from modules.cleanup.internal.cleanup_module_writer import CleanupModuleWriter
from modules.cleanup.types import (
    CreateAccountDeletionRequestParams,
    CreateCleanupModuleParams,
)
from modules.logger.logger import Logger


class CleanupManager:
    HOOKS: List[CreateCleanupModuleParams] = []

    @staticmethod
    def register_hook(
        func: Callable, module_name: str, class_name: str, main: bool = False
    ) -> None:
        """Register a cleanup hook."""
        params = CreateCleanupModuleParams(
            module_name=module_name,
            class_name=class_name,
            function_name=func.__name__,
            main=main,
        )
        # CleanupModuleWriter.add_cleanup_module(params=params)
        CleanupManager.HOOKS.append(params)

        if main:
            Logger.info(message=f"Registered main hook: {func.__name__}")
            return
        Logger.info(message=f"Registered cleanup hook: {func.__name__}")

    @staticmethod
    def push_hooks() -> None:
        """Push all registered hooks to the database."""
        for hook in CleanupManager.HOOKS:
            CleanupModuleWriter.add_cleanup_module(params=hook)
        CleanupManager.HOOKS = []

    @staticmethod
    def queue_account_deletion(params: SearchAccountByIdParams) -> None:
        """Queue cleanup operation to be handled by the worker thread."""

        from modules.account.account_service import AccountService

        account = AccountService.get_account_by_id(params=params)
        if not account:
            raise AccountNotFoundError(f"Account not found: {params.id}")

        AccountService.deactivate_account(params=params)

        AccountDeletionRequestWriter.create_account_deletion_request(
            params=CreateAccountDeletionRequestParams(
                account_id=params.id, requested_at=datetime.now(UTC)
            )
        )
