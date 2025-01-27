from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Optional

from modules.account.types import SearchAccountByIdParams
from modules.logger.logger import Logger


class CleanupManager:
    def __init__(self):
        self.cleanup_hooks: List[Callable] = []
        self.final_hook: Optional[Callable] = None

    def register_hook(self, func: Callable, final: bool = False):
        """Register a cleanup hook."""
        if final:
            self.final_hook = func
            Logger.info(message=f"Registered final cleanup hook: {func.__name__}")
            return
        self.cleanup_hooks.append(func)
        Logger.info(message=f"Registered cleanup hook: {func.__name__}")

    def execute_hooks(self, *, params: SearchAccountByIdParams):
        """Execute all hooks in parallel using ThreadPoolExecutor."""
        with ThreadPoolExecutor() as executor:
            future_to_hook = {executor.submit(hook, params=params): hook for hook in self.cleanup_hooks}

            for future in as_completed(future_to_hook):
                hook = future_to_hook[future]
                try:
                    future.result()
                    Logger.info(message=f"Successfully executed cleanup hook: {hook.__name__}")
                except Exception as e:
                    Logger.error(message=f"Cleanup hook {hook.__name__} failed for account {params.id}: {e}")

        if self.final_hook:
            self.final_hook(params=params)
            Logger.info(message=f"Successfully executed final cleanup hook: {self.final_hook.__name__}")


cleanup_manager = CleanupManager()
