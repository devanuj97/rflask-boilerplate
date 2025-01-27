from dataclasses import asdict

from bson.objectid import ObjectId
from phonenumbers import is_valid_number, parse
from pymongo import ReturnDocument

from modules.account.errors import AccountNotFoundError
from modules.account.internal.account_reader import AccountReader
from modules.account.internal.account_util import AccountUtil
from modules.account.internal.store.account_model import AccountModel
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.types import (
    Account,
    CreateAccountByPhoneNumberParams,
    CreateAccountByUsernameAndPasswordParams,
    PhoneNumber,
    SearchAccountByIdParams,
)
from modules.otp.errors import OtpRequestFailedError


class AccountWriter:
    @staticmethod
    def create_account_by_username_and_password(*, params: CreateAccountByUsernameAndPasswordParams) -> Account:
        params_dict = asdict(params)
        params_dict["hashed_password"] = AccountUtil.hash_password(password=params.password)
        del params_dict["password"]
        AccountReader.check_username_not_exist(params=params)
        account_bson = AccountModel(**params_dict).to_bson()
        query = AccountRepository.collection().insert_one(account_bson)
        account = AccountRepository.collection().find_one({"_id": query.inserted_id})

        return AccountUtil.convert_account_model_to_account(AccountModel(**account))

    @staticmethod
    def create_account_by_phone_number(*, params: CreateAccountByPhoneNumberParams) -> Account:
        params_dict = asdict(params)
        phone_number = PhoneNumber(**params_dict["phone_number"])
        is_valid_phone_number = is_valid_number(parse(str(phone_number)))

        if not is_valid_phone_number:
            raise OtpRequestFailedError()

        AccountReader.check_phone_number_not_exist(phone_number=params.phone_number)
        account_bson = AccountModel(**params_dict).to_bson()
        query = AccountRepository.collection().insert_one(account_bson)
        account = AccountRepository.collection().find_one({"_id": query.inserted_id})

        return AccountUtil.convert_account_model_to_account(AccountModel(**account))

    @staticmethod
    def update_password_by_account_id(account_id: str, password: str) -> Account:
        hashed_password = AccountUtil.hash_password(password=password)
        updated_account = AccountRepository.collection().find_one_and_update(
            {"_id": ObjectId(account_id)},
            {"$set": {"hashed_password": hashed_password}},
            return_document=ReturnDocument.AFTER,
        )
        if updated_account is None:
            raise AccountNotFoundError(f"Account not found: {account_id}")

        return AccountUtil.convert_account_model_to_account(AccountModel(**updated_account))

    @staticmethod
    def delete_account(*, params: SearchAccountByIdParams) -> None:
        params = SearchAccountByIdParams(id=params.id)
        account = AccountReader.get_account_by_id(params=params)
        if not account:
            raise AccountNotFoundError(f"Account not found: {params.id}")

        AccountRepository.collection().delete_one({"_id": ObjectId(account.id)})
