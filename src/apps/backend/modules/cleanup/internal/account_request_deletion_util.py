from modules.cleanup.internal.store.account_deletion_request_model import (
    AccountDeletionRequestModel,
)
from modules.cleanup.types import AccountDeletionRequest


class AccountDeletionRequestUtil:
    @staticmethod
    def convert_model_to_account_deletion_request(
        account_deletion_request: AccountDeletionRequestModel,
    ) -> AccountDeletionRequest:
        return AccountDeletionRequest(
            account_id=str(account_deletion_request.account_id),
            requested_at=account_deletion_request.requested_at,
        )
