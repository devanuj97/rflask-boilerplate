from modules.account.internal.account_reader import AccountReader
from modules.account.internal.account_writer import AccountWriter
from modules.account.types import (
    Account,
    CreateAccountByPhoneNumberParams,
    CreateAccountByUsernameAndPasswordParams,
    PhoneNumber,
    ResetPasswordParams,
    SearchAccountByIdParams,
)
from modules.cleanup.cleanup_service import CleanupService
from modules.otp.otp_service import OtpService
from modules.otp.types import CreateOtpParams
from modules.password_reset_token.password_reset_token_service import (
    PasswordResetTokenService,
)


class AccountService:
    @staticmethod
    def create_account_by_username_and_password(
        *, params: CreateAccountByUsernameAndPasswordParams
    ) -> Account:
        return AccountWriter.create_account_by_username_and_password(params=params)

    @staticmethod
    def get_account_by_phone_number(*, phone_number: PhoneNumber) -> Account:
        return AccountReader.get_account_by_phone_number(phone_number=phone_number)

    @staticmethod
    def get_or_create_account_by_phone_number(
        *, params: CreateAccountByPhoneNumberParams
    ) -> Account:
        account = AccountReader.get_account_by_phone_number_optional(
            phone_number=params.phone_number
        )

        if account is None:
            account = AccountWriter.create_account_by_phone_number(params=params)

        create_otp_params = CreateOtpParams(phone_number=params.phone_number)
        OtpService.create_otp(params=create_otp_params)

        return account

    @staticmethod
    def reset_account_password(*, params: ResetPasswordParams) -> Account:

        account = AccountReader.get_account_by_id(
            params=SearchAccountByIdParams(id=params.account_id)
        )

        password_reset_token = PasswordResetTokenService.verify_password_reset_token(
            account_id=account.id, token=params.token
        )

        updated_account = AccountWriter.update_password_by_account_id(
            account_id=params.account_id, password=params.new_password
        )

        PasswordResetTokenService.set_password_reset_token_as_used_by_id(
            password_reset_token_id=password_reset_token.id
        )

        return updated_account

    @staticmethod
    def get_account_by_id(*, params: SearchAccountByIdParams) -> Account:
        return AccountReader.get_account_by_id(params=params)

    @staticmethod
    def deactivate_account(*, params: SearchAccountByIdParams) -> None:
        return AccountWriter.deactivate_account(params=params)

    @staticmethod
    @CleanupService.register(main=True)
    def delete_account_by_id(*, params: SearchAccountByIdParams) -> None:
        return AccountWriter.delete_account(params=params)
