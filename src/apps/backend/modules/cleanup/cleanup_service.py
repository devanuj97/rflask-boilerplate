from typing import Callable

from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.cleanup_manager import CleanupManager


class CleanupService:
    @staticmethod
    def register(module_name: str, class_name: str, main: bool = False) -> Callable:
        def decorator(func: Callable) -> Callable:
            CleanupManager.register_hook(
                func=func, module_name=module_name, class_name=class_name, main=main
            )
            return func

        return decorator

    @staticmethod
    def push_hooks() -> None:
        CleanupManager.push_hooks()

    @staticmethod
    def queue_account_deletion(*, params: SearchAccountByIdParams) -> None:
        CleanupManager.queue_account_deletion(params=params)
