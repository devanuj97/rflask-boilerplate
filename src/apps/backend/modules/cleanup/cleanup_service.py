from typing import Callable

from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.cleanup_manager import cleanup_manager


class CleanupService:
    @staticmethod
    def register(final: bool = False):
        """
        Returns a decorator for registering cleanup hooks.
        :param final: If True, registers the hook as a final hook.
        """

        def decorator(func: Callable):
            cleanup_manager.register_hook(func, final=final)
            return func

        return decorator

    @staticmethod
    def execute_cleanup_hooks(*, params: SearchAccountByIdParams):
        """
        Execute all cleanup hooks.
        """
        cleanup_manager.execute_hooks(params=params)
