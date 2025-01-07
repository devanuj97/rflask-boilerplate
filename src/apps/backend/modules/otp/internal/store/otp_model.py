from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from modules.account.types import PhoneNumber
from dataclasses import dataclass,asdict

@dataclass
class OtpModel:
    id: Optional[ObjectId | str]
    otp_code: str
    phone_number: Optional[PhoneNumber]
    status: str
    active: bool
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def to_bson(self) -> dict[str, Any]:
        data = asdict(self)
        if data.get("id") is not None:
            data["_id"] = data.pop("id")
        else:
            data.pop("id", None)
        return data
    
    @classmethod
    def from_bson(cls,bson_data:dict)->"OtpModel":
        phone_number_data = bson_data.get("phone_number")
        phone_number = PhoneNumber(**phone_number_data) if phone_number_data else None
        return cls(
            id=bson_data.get("_id"),
            otp_code=bson_data.get("otp_code",""),
            phone_number=phone_number,
            status=bson_data.get("status",""),
            active=bson_data.get("active",""),
            created_at=bson_data.get("created_at"),
            updated_at=bson_data.get("updated_at")
        )

    @staticmethod
    def get_collection_name() -> str:
        return "otps"
