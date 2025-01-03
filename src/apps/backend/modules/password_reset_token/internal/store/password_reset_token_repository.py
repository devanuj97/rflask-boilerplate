from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from modules.application.repository import ApplicationRepository
from modules.password_reset_token.internal.store.password_reset_token_model import PasswordResetTokenModel

PASSWORD_RESET_TOKEN_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["account", "expires_at", "token", "is_used"],
        "properties": {
            "account": {"bsonType": "objectId", "description": "must be an ObjectId and is required"},
            "expires_at": {"bsonType": "date", "description": "must be a valid date and is required"},
            "token": {"bsonType": "string", "description": "must be a string and is required"},
            "is_used": {"bsonType": "bool", "description": "must be a boolean and is required"},
            "_id": {"bsonType": "objectId", "description": "must be an ObjectId"},
        },
    }
}


class PasswordResetTokenRepository(ApplicationRepository):
    collection_name = PasswordResetTokenModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("token")
        add_validation_command = {
            "collMod": cls.collection_name, 
            "validator": PASSWORD_RESET_TOKEN_VALIDATION_SCHEMA, 
            "validationLevel": "strict"
        }
        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            # If the collection does not exist, create it with the validation rules
            if "Collection does not exist" in str(e):
                collection.database.create_collection(cls.collection_name, validator=PASSWORD_RESET_TOKEN_VALIDATION_SCHEMA)
            else:
                print("OperationFailure occurred for collection accounts",e.details)
        return True

