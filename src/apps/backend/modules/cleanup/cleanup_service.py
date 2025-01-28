from typing import Callable

from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.cleanup_manager import cleanup_manager


class CleanupService:
    @staticmethod
    def register(main: bool = False) -> Callable:
        """
        Returns a decorator for registering cleanup hooks.

        Example: For registering a cleanup hook for any module, use the following decorator:

        @CleanupService.register()
        def modulename_cleanup(params: SearchAccountByIdParams):
            pass

        The main hook is reserved for the final account deletion, hence, no other module should pass
        the `main` parameter as `True`.

        :param main: If True, registers the hook as the main hook.
        """

        def decorator(func: Callable) -> Callable:
            cleanup_manager.register_hook(func, main=main)
            return func

        return decorator

    @staticmethod
    def check() -> Callable:
        """
        Returns a decorator for registering a pre-hook check.

        This hook is reserved for checking if the account can be deleted. Hence, no other module
        than `account` should use this.
        """

        def decorator(func: Callable) -> Callable:
            cleanup_manager.register_pre_cleanup_check(func)
            return func

        return decorator

    @staticmethod
    def execute_cleanup_hooks(*, params: SearchAccountByIdParams) -> None:
        """
        Execute all cleanup hooks.
        """
        cleanup_manager.queue_cleanup(params=params)
