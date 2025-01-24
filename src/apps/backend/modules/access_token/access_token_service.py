from datetime import datetime, timedelta

import jwt

from modules.access_token.errors import AccessTokenExpiredError, AccessTokenInvalidError
from modules.access_token.types import (
    AccessToken,
    AccessTokenPayload,
    EmailBasedAuthAccessTokenRequestParams,
    OTPBasedAuthAccessTokenRequestParams,
)
from modules.account.account_service import AccountService
from modules.account.internal.account_reader import AccountReader
from modules.account.types import Account, SearchAccountParams
from modules.config.config_service import ConfigService
from modules.otp.errors import OtpIncorrectError
from modules.otp.otp_service import OtpService
from modules.otp.types import OtpStatus, VerifyOtpParams


class AccessTokenService:
    @staticmethod
    def create_access_token_by_username_and_password(*, params: EmailBasedAuthAccessTokenRequestParams) -> AccessToken:
        account = AccountReader.get_account_by_username_and_password(
            params=SearchAccountParams(username=params.username, password=params.password)
        )

        return AccessTokenService.__generate_access_token(account=account)

    @staticmethod
    def create_access_token_by_phone_number(*, params: OTPBasedAuthAccessTokenRequestParams) -> AccessToken:
        account = AccountService.get_account_by_phone_number(phone_number=params.phone_number)

        otp = OtpService.verify_otp(params=VerifyOtpParams(phone_number=params.phone_number, otp_code=params.otp_code))

        if otp.status != OtpStatus.SUCCESS:
            raise OtpIncorrectError()

        return AccessTokenService.__generate_access_token(account=account)

    @staticmethod
    def __generate_access_token(*, account: Account) -> AccessToken:
        jwt_signing_key = ConfigService.get_token_signing_key()
        jwt_expiry = timedelta(days=ConfigService.get_token_expiry_days())
        expiry_time = datetime.now() + jwt_expiry
        payload = {"account_id": account.id, "exp": (expiry_time).timestamp()}
        jwt_token = jwt.encode(payload, jwt_signing_key, algorithm="HS256")
        access_token = AccessToken(token=jwt_token, account_id=account.id, expires_at=expiry_time.isoformat())

        return access_token

    @staticmethod
    def verify_access_token(*, token: str) -> AccessTokenPayload:

        jwt_signing_key = ConfigService.get_token_signing_key()

        try:
            verified_token = jwt.decode(token, jwt_signing_key, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            raise AccessTokenInvalidError("Invalid access token")
        except jwt.ExpiredSignatureError:
            raise AccessTokenExpiredError(message="Access token has expired. Please login again.")

        return AccessTokenPayload(account_id=verified_token.get("account_id"))
