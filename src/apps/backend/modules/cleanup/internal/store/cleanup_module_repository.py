from pymongo.collection import Collection

from modules.application.repository import ApplicationRepository
from modules.cleanup.internal.store.cleanup_module_model import CleanupModuleModel


class CleanupModuleRepository(ApplicationRepository):
    collection_name = CleanupModuleModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.delete_many({})
        collection.create_index("module_name")
        return True
