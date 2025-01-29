from typing import List

from modules.cleanup.errors import (
    AccountDeletionRequestAlreadyExistsError,
    AccountDeletionRequestNotFoundError,
)
from modules.cleanup.internal.account_request_deletion_util import (
    AccountDeletionRequestUtil,
)
from modules.cleanup.internal.store.account_deletion_request_repository import (
    AccountDeletionRequestRepository,
)
from modules.cleanup.types import (
    AccountDeletionRequest,
    CreateAccountDeletionRequestParams,
    SearchAccountDeletionRequestParams,
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
    def get_account_deletion_request(
        *, params: SearchAccountDeletionRequestParams
    ) -> AccountDeletionRequest:
        account_deletion_request = (
            AccountDeletionRequestRepository.collection().find_one(
                {"account_id": params.account_id}
            )
        )

        if account_deletion_request is None:
            raise AccountDeletionRequestNotFoundError(
                f"Account deletion request not found for account_id:: {params.account_id}"
            )

        return AccountDeletionRequestUtil.convert_model_to_account_deletion_request(
            **account_deletion_request
        )

    @staticmethod
    def get_all_account_deletion_requests() -> List[AccountDeletionRequest]:
        account_deletion_requests = AccountDeletionRequestRepository.collection().find()
        return [
            AccountDeletionRequestUtil.convert_model_to_account_deletion_request(
                account_deletion_request
            )
            for account_deletion_request in account_deletion_requests
        ]
