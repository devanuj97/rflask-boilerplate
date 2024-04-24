import urllib.parse 

from modules.communication.email_service import EmailService
from modules.communication.types import EmailRecipient, EmailSender, SendEmailParams
from modules.account.account_service import AccountService
from modules.account.errors import AccountBadRequestError
from modules.config.config_service import ConfigService
from modules.password_reset_token.internal.password_reset_token_reader import PasswordResetTokenReader
from modules.password_reset_token.internal.password_reset_token_util import PasswordResetTokenUtil
from modules.password_reset_token.internal.password_reset_token_writer import PasswordResetTokenWriter
from modules.password_reset_token.types import CreatePasswordResetTokenParams, PasswordResetToken

class PasswordResetTokenService:
    @staticmethod
    def create_password_reset_token(params: CreatePasswordResetTokenParams) -> PasswordResetToken:
        account = AccountService.get_account_by_username(username=params.username)
        token = PasswordResetTokenUtil.generate_password_reset_token()
        password_reset_token = PasswordResetTokenWriter.create_password_reset_token(
            account.id, token
        )
        PasswordResetTokenService.send_password_reset_email(
            account.id, account.first_name, account.username, token
        )
        password_reset_token_dict = {
            "id": str(password_reset_token.id),
            "account": account.id,
            "token": token,
            "is_used": password_reset_token.is_used,
            "is_expired": PasswordResetTokenUtil.is_token_expired(password_reset_token.expires_at),
            "expires_at": password_reset_token.expires_at,
        }

        return PasswordResetToken(
            id=password_reset_token_dict.get("id"),
            account=password_reset_token_dict.get("account"),
            token=password_reset_token_dict.get("token"),
            is_used=password_reset_token_dict.get("is_used"),
            is_expired=password_reset_token_dict.get("is_expired"),
            expires_at=password_reset_token_dict.get("expires_at"),
        )
    @staticmethod
    def get_password_reset_token_by_account_id(account_id: str) -> PasswordResetToken:
        return PasswordResetTokenReader.get_password_reset_token_by_account_id(account_id)

    @staticmethod
    def set_password_reset_token_as_used_by_id(password_reset_token_id: str) -> PasswordResetToken:
        return PasswordResetTokenWriter.set_password_reset_token_as_used(password_reset_token_id)

    @staticmethod
    def verify_password_reset_token(account_id: str, token: str) -> PasswordResetToken:
        password_reset_token = PasswordResetTokenService.get_password_reset_token_by_account_id(account_id)

        if password_reset_token.is_expired:
            raise AccountBadRequestError(
                f"Password reset link is expired for accountId {account_id}. Please retry with new link"
            )
        if password_reset_token.is_used:
            raise AccountBadRequestError(
                f"Password reset is already used for accountId {account_id}. Please retry with new link"
            )

        is_token_valid = PasswordResetTokenUtil.compare_password(
            password=token,
            hashed_password=password_reset_token.token
        )
        if not is_token_valid:
            raise AccountBadRequestError(
                f"Password reset link is invalid for accountId {account_id}. Please retry with new link."
            )

        return password_reset_token

    @staticmethod
    def send_password_reset_email(
        account_id: str, 
        first_name: str, 
        username: str, 
        password_reset_token: str
    ) -> None:

        web_app_host = ConfigService.get_web_app_host()
        default_email = ConfigService.get_mailer_config("default_email")
        default_email_name = ConfigService.get_mailer_config("default_email_name")
        forgot_password_mail_template_id = ConfigService.get_mailer_config("forgot_password_mail_template_id")

        template_data = {
            "first_name": first_name,
            "password_reset_link": f"{web_app_host}/accounts/{account_id}/reset_password?token={urllib.parse.quote(password_reset_token)}",
            "username": username
        }

        password_reset_email_params = SendEmailParams(
            template_id=forgot_password_mail_template_id,
            recipient=EmailRecipient(email=username),
            sender=EmailSender(email=default_email, name=default_email_name),
            template_data=template_data,
        )

        EmailService.send_email(params=password_reset_email_params) 
