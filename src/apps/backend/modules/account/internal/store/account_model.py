from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from dataclasses import dataclass,asdict
from modules.account.types import PhoneNumber

@dataclass
class AccountModel:
    id: Optional[ObjectId|str]
    first_name: str
    hashed_password: str
    phone_number:Optional[PhoneNumber]
    last_name: str
    username: str
    active: bool = True
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        return {
            "_id": self.id if self.id else None,
            "active": self.active,
            "first_name": self.first_name,
            "hashed_password": self.hashed_password,
            "phone_number": asdict(self.phone_number) if self.phone_number else None,
            "last_name": self.last_name,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_bson(self) -> dict[str, Any]:
        data = asdict(self)
        if data.get("id") is not None:
            data["_id"] = data.pop("id")
        else:
            data.pop("id", None)
        return data
    
    @classmethod
    def from_bson(cls, bson_data: dict) -> "AccountModel":
        # Extract and handle the phone_number field
        phone_number_data = bson_data.get("phone_number")
        phone_number = PhoneNumber(**phone_number_data) if phone_number_data else None
        # Instantiate the model using the BSON data
        return cls(
            id=bson_data.get("_id"),
            active=bson_data.get("active",True),
            first_name=bson_data.get("first_name", ""),
            hashed_password=bson_data.get("hashed_password", ""),
            phone_number=phone_number,
            last_name=bson_data.get("last_name", ""),
            username=bson_data.get("username", ""),
            created_at=bson_data.get("created_at"),
            updated_at=bson_data.get("updated_at")
        )
    
    @staticmethod
    def get_collection_name() -> str:
        return "accounts"
