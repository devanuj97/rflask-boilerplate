from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CleanupModule:
    module_name: str
    class_name: str
    function_name: str
    main: bool = False


@dataclass(frozen=True)
class CreateCleanupModuleParams:
    module_name: str
    class_name: str
    function_name: str
    main: bool = False


@dataclass(frozen=True)
class AccountDeletionRequest:
    account_id: str
    requested_at: datetime


@dataclass(frozen=True)
class CreateAccountDeletionRequestParams:
    account_id: str
    requested_at: datetime


@dataclass(frozen=True)
class SearchAccountDeletionRequestParams:
    account_id: str


@dataclass(frozen=True)
class AccountDeletionRequestErrorCode:
    NOT_FOUND: str = "ACCOUNT_DELETION_REQUEST_ERR_01"
    REQUEST_ALREADY_EXISTS: str = "ACCOUNT_DELETION_REQUEST_ERR_02"
