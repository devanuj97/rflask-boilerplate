from modules.cleanup.internal.store.cleanup_module_model import CleanupModuleModel
from modules.cleanup.types import CleanupModule


class CleanupModuleUtil:
    @staticmethod
    def convert_model_to_cleanup_module(
        cleanup_module: CleanupModuleModel,
    ) -> CleanupModule:
        return CleanupModule(
            module_name=cleanup_module.module_name,
            class_name=cleanup_module.class_name,
            function_name=cleanup_module.function_name,
            main=cleanup_module.main,
        )
