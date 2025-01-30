from pymongo.collection import Collection

from modules.application.repository import ApplicationRepository
from modules.cleanup.internal.store.account_deletion_request_model import (
    AccountDeletionRequestModel,
)


class AccountDeletionRequestRepository(ApplicationRepository):
    collection_name = AccountDeletionRequestModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("account_id")
        return True
