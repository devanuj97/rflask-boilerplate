from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class CleanupModuleModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    module_name: str = ""
    class_name: str = ""
    function_name: str = ""
    main: bool = False

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_bson(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data

    @staticmethod
    def get_collection_name() -> str:
        return "cleanup_modules"
