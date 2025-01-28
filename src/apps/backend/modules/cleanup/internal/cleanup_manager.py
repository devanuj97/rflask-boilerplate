import queue
import threading
from typing import Callable, List, Optional

from modules.account.errors import AccountNotFoundError
from modules.account.types import SearchAccountByIdParams
from modules.logger.logger import Logger


class CleanupManager:
    def __init__(self):
        self.cleanup_hooks: List[Callable] = []
        self.pre_cleanup_check: Optional[Callable] = None
        self.main_hook: Optional[Callable] = None
        self.task_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def register_pre_cleanup_check(self, func: Callable):
        """Register a pre-hook check."""
        self.pre_cleanup_check = func
        Logger.info(message=f"Registered pre-hook check: {func.__name__}")

    def register_hook(self, func: Callable, main: bool = False):
        """Register a cleanup hook."""
        if main:
            self.main_hook = func
            Logger.info(message=f"Registered main hook: {func.__name__}")
            return
        self.cleanup_hooks.append(func)
        Logger.info(message=f"Registered cleanup hook: {func.__name__}")

    def queue_cleanup(self, params: SearchAccountByIdParams):
        """Queue cleanup operation to be handled by the worker thread."""
        account = self.pre_cleanup_check(params=params)
        if not account:
            raise AccountNotFoundError(f"Account not found: {params.id}")

        try:
            self.main_hook(params=params)
            Logger.info(message=f"Successfully executed main cleanup hook: {self.main_hook.__name__}")
        except Exception as e:
            Logger.error(message=f"Main cleanup hook failed for account {params.id}: {e}")

        Logger.info(message=f"Queuing cleanup for account {params.id}")
        self.task_queue.put(params)

    def _worker(self):
        """Background worker that processes cleanup tasks from the queue."""
        while True:
            params = self.task_queue.get()
            if params is None:
                break  # Exit signal

            Logger.info(message=f"Processing cleanup for account {params.id}")
            try:
                self._execute_hooks(params)
            except Exception as e:
                Logger.error(message=f"Cleanup failed for account {params.id}: {e}")
            finally:
                self.task_queue.task_done()

    def _execute_hooks(self, params: SearchAccountByIdParams):
        """Execute cleanup hooks sequentially (can be modified for retries)."""
        for hook in self.cleanup_hooks:
            try:
                hook(params=params)
                Logger.info(message=f"Successfully executed cleanup hook: {hook.__name__}")
            except Exception as e:
                Logger.error(message=f"Cleanup hook {hook.__name__} failed for account {params.id}: {e}")

    def stop_worker(self):
        """Stop the worker thread gracefully."""
        self.task_queue.put(None)
        self.worker_thread.join()


# Global instance
cleanup_manager = CleanupManager()
