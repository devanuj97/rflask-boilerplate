from typing import Callable, List

from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.account_deletion_request_reader import (
    AccountDeletionRequestReader,
)
from modules.cleanup.internal.account_deletion_request_writer import (
    AccountDeletionRequestWriter,
)
from modules.cleanup.internal.cleanup_manager import CleanupManager
from modules.cleanup.internal.cleanup_module_reader import CleanupModuleReader
from modules.cleanup.types import (
    AccountDeletionRequest,
    CleanupModule,
    SearchAccountDeletionRequestParams,
)


class CleanupService:
    @staticmethod
    def register(main: bool = False) -> Callable:
        """
        Register a function as a cleanup hook

        Example:
        ```
        @CleanupService.register()
        def modulename_cleanup():
            ...
        ```

        :param main: True if the function is the main cleanup function (final account deletion) hence not
        to be set by any module other than `account`
        :return: function decorator to register the function as a cleanup hook
        """

        def decorator(func: Callable) -> Callable:
            # noinspection PyUnresolvedReferences
            CleanupManager.register_hook(
                func=func,
                module_name=func.__module__,
                class_name=func.__qualname__.split(".")[0],
                main=main,
            )
            return func

        return decorator

    @staticmethod
    def push_hooks() -> None:
        CleanupManager.push_hooks()

    @staticmethod
    def execute_hook(
        *,
        cleanup_module: CleanupModule,
        account_deletion_request: AccountDeletionRequest
    ) -> None:
        CleanupManager.execute_hook(
            cleanup_module=cleanup_module,
            account_deletion_request=account_deletion_request,
        )

    @staticmethod
    def get_cleanup_modules() -> List[CleanupModule]:
        return CleanupModuleReader.get_cleanup_modules()

    @staticmethod
    def get_all_account_deletion_requests() -> List[AccountDeletionRequest]:
        return AccountDeletionRequestReader.get_all_account_deletion_requests()

    @staticmethod
    def queue_account_deletion(*, params: SearchAccountByIdParams) -> None:
        CleanupManager.queue_account_deletion(params=params)

    @staticmethod
    def remove_account_deletion_request(
        *, params: SearchAccountDeletionRequestParams
    ) -> None:
        AccountDeletionRequestWriter.remove_account_deletion_request(params=params)
