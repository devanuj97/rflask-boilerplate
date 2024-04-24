from modules.password_reset_token.types import PasswordResetTokenErrorCode
from modules.error.custom_errors import AppError

        
class PasswordResetTokenNotFoundError(AppError):
    code: PasswordResetTokenErrorCode;
    
    def __init__(
        self,
    ) -> None:
        super().__init__(
            code=PasswordResetTokenErrorCode.PASSWORD_RESET_TOKEN_NOT_FOUND,
            https_status_code=404,
            message=f"System is unable to find a token with this account",
        )
