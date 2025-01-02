from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from modules.account.types import PhoneNumber
import json

class OtpModel:
    def __init__(
        self,
        id: Optional[ObjectId | str] = None,
        active: bool = True,
        otp_code: str = "",
        phone_number: Optional[PhoneNumber|dict] = None,
        status: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs:Any
    )->None:
        # Use object_id_validate for the ID
        self.id = id if id else kwargs.get("_id", None)
        self.active = active
        self.otp_code = otp_code
        self.phone_number = PhoneNumber(**phone_number) if isinstance(phone_number, dict) else phone_number
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "_id": str(self.id) if self.id else None,
            "active": self.active,
            "otp_code": self.otp_code,
            "phone_number": self.phone_number.__dict__ if self.phone_number else None,
            "status": self.status,
            "created_at": self.created_at if self.created_at else None,
            "updated_at": self.updated_at if self.updated_at else None,
        }

    def to_bson(self) -> dict[str, Any]:
        data = self.to_dict()
        # Remove the _id if it's None
        if "_id" in data and data["_id"] is None:
            del data["_id"]

        return data

    @staticmethod
    def get_collection_name() -> str:
        return "otps"
