from pymongo.collection import Collection

from modules.application.repository import ApplicationRepository
from modules.otp.internal.store.otp_model import OtpModel
from pymongo.errors import OperationFailure

OTP_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["otp_code", "phone_number", "status", "active"],
        "properties": {
            "otp_code": {"bsonType": "string", "description": "must be a string and is required"},
            "phone_number": {
                "bsonType": "object",
                "required": ["country_code", "phone_number"],
                "properties": {
                    "country_code": {"bsonType": "string", "description": "must be a string"},
                    "phone_number": {"bsonType": "string", "description": "must be a string"},
                },
                "description": "must be an object with country_code and phone_number",
            },
            "status": {"bsonType": "string", "description": "must be a string and is required"},
            "active": {"bsonType": "bool", "description": "must be a boolean and is required"},
            "created_at": {"bsonType": "date", "description": "must be a valid date"},
            "updated_at": {"bsonType": "date", "description": "must be a valid date"},
            "_id": {"bsonType": "objectId", "description": "must be an ObjectId"},
        },
    }
}


class OtpRepository(ApplicationRepository):
    collection_name = OtpModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:

        collection.create_index("phone_number")
        add_validation_command = {
            "collMod": cls.collection_name, 
            "validator": OTP_VALIDATION_SCHEMA, 
            "validationLevel": "strict"
        }
        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            # If the collection does not exist, create it with the validation rules
            if "Collection does not exist" in str(e):
                collection.database.create_collection(cls.collection_name, validator=OTP_VALIDATION_SCHEMA)
            else:
                print("OperationFailure occurred for collection accounts",e.details)
        return True
