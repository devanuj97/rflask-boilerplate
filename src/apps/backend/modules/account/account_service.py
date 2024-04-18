import json

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.account.types import AccountSearchByIdParams, CreateAccountParams, ResetPasswordParams
from modules.account.internal.account_writer import AccountWriter
from modules.account.internal.account_reader import AccountReader
from modules.account.types import Account


class AccountService:
  @staticmethod
  def create_account(*, params: CreateAccountParams) -> Account:
    account = AccountWriter.create_account(params=params)
    account_dict = json.loads(account.to_json())
    return Account(
      id=account_dict.get("id"),
      first_name=account_dict.get("first_name"),
      last_name=account_dict.get("last_name"),
      username=account_dict.get("username"),
    )
    
  @staticmethod
  def get_account_by_username(*, username: str) -> Account:
    account = AccountReader.get_account_by_username(username=username)
    account_dict = json.loads(account.to_json())
    return Account(
      id=account_dict.get("id"),
      first_name=account_dict.get("first_name"),
      last_name=account_dict.get("last_name"),
      username=account_dict.get("username"),
    )
    
  @staticmethod
  def reset_account_password(*, params: ResetPasswordParams):
    from modules.password_reset_token.password_reset_token_service import PasswordResetTokenService
    
    password_reset_token = PasswordResetTokenService.verify_password_reset_token(
      account_id=params.account_id,
      token=params.token,
    )
    
    updated_account = AccountWriter.update_password_by_account_id(
      account_id=params.account_id,
      password=params.new_password,
    )
    
    PasswordResetTokenService.set_password_reset_token_as_used_by_id(
      password_reset_token_id=password_reset_token.id,
    )
    
    return Account(
      id=str(updated_account.id),
      first_name=updated_account.first_name,
      last_name=updated_account.last_name,
      username=updated_account.username,
    )

  @access_auth_middleware
  @staticmethod
  def get_account_by_id(*, params: AccountSearchByIdParams) -> Account:
    account = AccountReader.get_account_by_id(
      params=params
    )
    return Account(
      id=str(account.id),
      first_name=account.first_name,
      last_name=account.last_name,
      username=account.username,
    )
