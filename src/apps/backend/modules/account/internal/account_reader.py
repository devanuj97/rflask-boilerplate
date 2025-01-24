from typing import Optional

from bson.objectid import ObjectId

from modules.account.errors import (
    AccountInvalidPasswordError,
    AccountNotFoundError,
    AccountWithPhoneNumberExistsError,
    AccountWithUserNameExistsError,
)
from modules.account.internal.account_util import AccountUtil
from modules.account.internal.store.account_model import AccountModel
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.types import (
    Account,
    CreateAccountByUsernameAndPasswordParams,
    PhoneNumber,
    SearchAccountByIdParams,
    SearchAccountParams,
)


class AccountReader:
    @staticmethod
    def get_account_by_username(*, username: str) -> AccountModel:
        account = AccountRepository.collection().find_one({"username": username})
        if account is None:
            raise AccountNotFoundError(f"Account with username:: {username}, not found")

        return AccountModel(**account)

    @staticmethod
    def get_account_by_username_and_password(*, params: SearchAccountParams) -> Account:
        account = AccountReader.get_account_by_username(username=params.username)
        if not AccountUtil.compare_password(password=params.password, hashed_password=account.hashed_password):
            raise AccountInvalidPasswordError("Invalid password")

        return AccountUtil.convert_account_model_to_account(account_model=account)

    @staticmethod
    def get_account_by_id(*, params: SearchAccountByIdParams) -> Account:
        account = AccountRepository.collection().find_one({"_id": ObjectId(params.id), "active": True})
        if account is None:
            raise AccountNotFoundError(f"Account with id:: {params.id}, not found")

        return AccountUtil.convert_account_model_to_account(AccountModel(**account))

    @staticmethod
    def check_username_not_exist(*, params: CreateAccountByUsernameAndPasswordParams) -> None:
        account = AccountRepository.collection().find_one({"username": params.username, "active": True})

        if account:
            raise AccountWithUserNameExistsError(f"Account already exist for username:: {params.username}")

    @staticmethod
    def get_account_by_phone_number_optional(*, phone_number: PhoneNumber) -> Optional[Account]:
        account = AccountRepository.collection().find_one({"phone_number": phone_number})
        if account is None:
            return None

        return AccountUtil.convert_account_model_to_account(AccountModel(**account))

    @staticmethod
    def get_account_by_phone_number(*, phone_number: PhoneNumber) -> Account:
        account = AccountReader.get_account_by_phone_number_optional(phone_number=phone_number)
        if account is None:
            raise AccountNotFoundError(f"Account with phone number:: {phone_number}, not found")

        return account

    @staticmethod
    def check_phone_number_not_exist(*, phone_number: PhoneNumber) -> None:
        account = AccountRepository.collection().find_one({"phone_number": phone_number, "active": True})

        if account:
            raise AccountWithPhoneNumberExistsError(f"Account already exist for phone number:: {phone_number}")
