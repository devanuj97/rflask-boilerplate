from modules.object_id.utils import object_id_validate
from bson import ObjectId
from datetime import datetime
from typing import Annotated, Any, Optional
from pydantic import AfterValidator, BaseModel, Field, ConfigDict


PyObjectId = Annotated[ObjectId | str, AfterValidator(object_id_validate)]


class PasswordResetTokenModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(None, alias="_id")
    account: PyObjectId
    expires_at: datetime 
    token: str
    is_used: bool = False

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
