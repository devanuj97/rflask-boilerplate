from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from dataclasses import dataclass,asdict

@dataclass
class PasswordResetTokenModel:
    id: Optional[ObjectId | str]
    account: ObjectId | str
    token: str
    expires_at: datetime
    is_used: bool = False
    
    def to_bson(self) -> dict[str, Any]:
        data = asdict(self)
        if data.get("id") is not None:
            data["_id"] = data.pop("id")
        else:
            data.pop("id", None)
        return data
    
    @classmethod
    def from_bson(cls, bson_data: dict) -> "PasswordResetTokenModel":
        return cls(
            id = bson_data.get("_id"),
            account = bson_data.get("account",),
            token = bson_data.get("token",""),
            expires_at = bson_data.get("expires_at",""),
            is_used = bson_data.get("is_used","")
        )

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
