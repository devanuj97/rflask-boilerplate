import hashlib
import os
from datetime import datetime, timedelta

import bcrypt

from modules.config.config_service import ConfigService
from modules.password_reset_token.internal.store.password_reset_token_model import PasswordResetTokenModel
from modules.password_reset_token.types import PasswordResetToken


class PasswordResetTokenUtil:

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()

    @staticmethod
    def compare_password(*, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def generate_password_reset_token() -> str:
        return hashlib.sha256(os.urandom(60)).hexdigest()

    @staticmethod
    def hash_password_reset_token(reset_token: str) -> str:
        return bcrypt.hashpw(reset_token.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()

    @staticmethod
    def get_token_expires_at() -> datetime:
        default_token_expire_time_in_seconds = ConfigService[int].get_value(key="accounts.token_expires_in_seconds")
        return datetime.now() + timedelta(seconds=default_token_expire_time_in_seconds)

    @staticmethod
    def is_token_expired(expires_at: datetime) -> bool:
        return datetime.now() > expires_at

    @staticmethod
    def convert_password_reset_token_model_to_password_reset_token(
        password_reset_token_model: PasswordResetTokenModel,
    ) -> PasswordResetToken:
        return PasswordResetToken(
            id=str(password_reset_token_model.id),
            account=str(password_reset_token_model.account),
            token=password_reset_token_model.token,
            is_used=password_reset_token_model.is_used,
            is_expired=PasswordResetTokenUtil.is_token_expired(password_reset_token_model.expires_at),
            expires_at=str(password_reset_token_model.expires_at),
        )
