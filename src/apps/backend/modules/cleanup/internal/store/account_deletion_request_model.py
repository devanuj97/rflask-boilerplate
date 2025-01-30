from datetime import UTC, datetime
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class AccountDeletionRequestModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    account_id: str = ""
    requested_at: datetime = datetime.now(UTC)

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_bson(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data

    @staticmethod
    def get_collection_name() -> str:
        return "account_deletion_requests"
