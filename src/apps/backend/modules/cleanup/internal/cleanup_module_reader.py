from typing import List

from modules.cleanup.internal.cleanup_module_util import CleanupModuleUtil
from modules.cleanup.internal.store.cleanup_module_model import CleanupModuleModel
from modules.cleanup.internal.store.cleanup_module_repository import (
    CleanupModuleRepository,
)
from modules.cleanup.types import CleanupModule


class CleanupModuleReader:
    @staticmethod
    def get_cleanup_modules() -> List[CleanupModule]:
        cleanup_modules_data = CleanupModuleRepository.collection().find()

        cleanup_modules = [
            CleanupModuleModel(**cleanup_module_data)
            for cleanup_module_data in cleanup_modules_data
        ]

        return [
            CleanupModuleUtil.convert_model_to_cleanup_module(cleanup_module)
            for cleanup_module in cleanup_modules
        ]
