from typing import Callable

from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.cleanup_manager import cleanup_manager


class CleanupService:
    @staticmethod
    def register(main: bool = False):
        """
        Returns a decorator for registering cleanup hooks.
        :param main: If True, registers the hook as the main hook.
        """

        def decorator(func: Callable):
            cleanup_manager.register_hook(func, main=main)
            return func

        return decorator

    @staticmethod
    def check():
        """
        Returns a decorator for registering a pre-hook check.
        """

        def decorator(func: Callable):
            cleanup_manager.register_pre_cleanup_check(func)
            return func

        return decorator

    @staticmethod
    def execute_cleanup_hooks(*, params: SearchAccountByIdParams):
        """
        Execute all cleanup hooks.
        """
        cleanup_manager.queue_cleanup(params=params)
