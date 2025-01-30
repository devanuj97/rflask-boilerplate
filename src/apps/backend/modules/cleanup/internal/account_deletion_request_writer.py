from dataclasses import asdict

from modules.cleanup.errors import AccountDeletionRequestNotFoundError
from modules.cleanup.internal.account_deletion_request_reader import (
    AccountDeletionRequestReader,
)
from modules.cleanup.internal.store.account_deletion_request_model import (
    AccountDeletionRequestModel,
)
from modules.cleanup.internal.store.account_deletion_request_repository import (
    AccountDeletionRequestRepository,
)
from modules.cleanup.types import (
    CreateAccountDeletionRequestParams,
    SearchAccountDeletionRequestParams,
)


class AccountDeletionRequestWriter:
    @staticmethod
    def create_account_deletion_request(
        *, params: CreateAccountDeletionRequestParams
    ) -> None:
        params_dict = asdict(params)

        AccountDeletionRequestReader.check_account_deletion_request_exists(
            params=params
        )

        account_deletion_request_bson = AccountDeletionRequestModel(
            **params_dict
        ).to_bson()
        AccountDeletionRequestRepository.collection().insert_one(
            account_deletion_request_bson
        )

    @staticmethod
    def remove_account_deletion_request(
        *, params: SearchAccountDeletionRequestParams
    ) -> None:
        account_deletion_request = (
            AccountDeletionRequestRepository.collection().find_one_and_delete(
                {"account_id": params.account_id}
            )
        )
        if account_deletion_request is None:
            raise AccountDeletionRequestNotFoundError(
                f"Account deletion request not found for account_id:: {params.account_id}"
            )
