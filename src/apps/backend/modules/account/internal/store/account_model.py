from datetime import datetime
from typing import Optional
from bson import ObjectId
from dataclasses import dataclass
from modules.account.types import PhoneNumber
from modules.common.base_model import BaseModel

@dataclass
class AccountModel(BaseModel):
    id: Optional[ObjectId|str]
    first_name: str
    hashed_password: str
    phone_number:Optional[PhoneNumber]
    last_name: str
    username: str
    active: bool = True
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

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
