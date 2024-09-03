from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import EmailBasedAuthAccessTokenRequestParams
from modules.account.account_service import AccountService
from modules.account.types import CreateAccountByUsernameAndPasswordParams
from tests.modules.access_token.base_test_access_token import BaseTestAccessToken


class TestAccessTokenService(BaseTestAccessToken):
    def test_get_access_token(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        access_token = AccessTokenService.create_access_token_by_username_and_password(
            params=EmailBasedAuthAccessTokenRequestParams(username=account.username, password="password")
        )

        assert access_token.account_id == account.id
        assert access_token.token
        assert access_token.expires_at

    def test_verify_access_token(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        access_token = AccessTokenService.create_access_token_by_username_and_password(
            params=EmailBasedAuthAccessTokenRequestParams(username=account.username, password="password")
        )

        verified_access_token = AccessTokenService.verify_access_token(token=access_token.token)

        assert verified_access_token.account_id == account.id
