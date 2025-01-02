from datetime import datetime
from typing import Optional
from bson import ObjectId

class PasswordResetTokenModel:
    def __init__(
        self,
        id: Optional[ObjectId | str] = None,
        account: Optional[ObjectId | str] = None,
        expires_at: datetime = None,
        token: str = None,
        is_used: bool = False,
        **kwargs
    ):
        self.id = id if id else kwargs.get("_id", None)
        self.account = account if account else kwargs.get("account", None)
        self.expires_at = expires_at
        self.token = token
        self.is_used = is_used

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
