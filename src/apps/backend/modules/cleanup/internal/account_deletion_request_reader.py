from typing import List

from modules.cleanup.errors import AccountDeletionRequestAlreadyExistsError
from modules.cleanup.internal.account_request_deletion_util import (
    AccountDeletionRequestUtil,
)
from modules.cleanup.internal.store.account_deletion_request_model import (
    AccountDeletionRequestModel,
)
from modules.cleanup.internal.store.account_deletion_request_repository import (
    AccountDeletionRequestRepository,
)
from modules.cleanup.types import (
    AccountDeletionRequest,
    CreateAccountDeletionRequestParams,
)


class AccountDeletionRequestReader:
    @staticmethod
    def check_account_deletion_request_exists(
        *, params: CreateAccountDeletionRequestParams
    ) -> None:
        account_deletion_request = (
            AccountDeletionRequestRepository.collection().find_one(
                {"account_id": params.account_id}
            )
        )

        if account_deletion_request:
            raise AccountDeletionRequestAlreadyExistsError(
                f"Account deletion request already exists for account_id:: {params.account_id}"
            )

    @staticmethod
    def get_all_account_deletion_requests() -> List[AccountDeletionRequest]:
        account_deletion_requests_data = (
            AccountDeletionRequestRepository.collection().find()
        )

        account_deletion_requests = [
            AccountDeletionRequestModel(**account_deletion_request_data)
            for account_deletion_request_data in account_deletion_requests_data
        ]

        return [
            AccountDeletionRequestUtil.convert_model_to_account_deletion_request(
                account_deletion_request
            )
            for account_deletion_request in account_deletion_requests
        ]
