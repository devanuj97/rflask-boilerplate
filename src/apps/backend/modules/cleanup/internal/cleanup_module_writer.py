from dataclasses import asdict

from modules.cleanup.internal.store.cleanup_module_model import CleanupModuleModel
from modules.cleanup.internal.store.cleanup_module_repository import (
    CleanupModuleRepository,
)
from modules.cleanup.types import CreateCleanupModuleParams


class CleanupModuleWriter:
    @staticmethod
    def add_cleanup_module(*, params: CreateCleanupModuleParams) -> None:
        params_dict = asdict(params)

        cleanup_module_bson = CleanupModuleModel(**params_dict).to_bson()
        CleanupModuleRepository.collection().insert_one(cleanup_module_bson)
