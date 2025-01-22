from datetime import datetime
from typing import Optional
from bson import ObjectId
from dataclasses import dataclass
from modules.common.base_model import BaseModel


@dataclass
class PasswordResetTokenModel(BaseModel):
    id: Optional[ObjectId | str]
    account: ObjectId | str
    token: str
    expires_at: datetime
    is_used: bool = False

    @classmethod
    def from_bson(cls, bson_data: dict) -> "PasswordResetTokenModel":
        return cls(
            id=bson_data.get("_id"),
            account=bson_data.get("account"),
            token=bson_data.get("token", ""),
            expires_at=bson_data.get("expires_at", ""),
            is_used=bson_data.get("is_used", ""),
        )

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
