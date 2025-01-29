from modules.cleanup.types import AccountDeletionRequestErrorCode
from modules.error.custom_errors import AppError


class AccountDeletionRequestNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            code=AccountDeletionRequestErrorCode.NOT_FOUND,
            http_status_code=404,
            message=message,
        )


class AccountDeletionRequestAlreadyExistsError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            code=AccountDeletionRequestErrorCode.REQUEST_ALREADY_EXISTS,
            http_status_code=409,
            message=message,
        )
