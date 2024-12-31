from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from modules.application.repository import ApplicationRepository
from modules.password_reset_token.internal.store.password_reset_token_model import PasswordResetTokenModel


class PasswordResetTokenRepository(ApplicationRepository):
    collection_name = PasswordResetTokenModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("token")
        validation_rules = {
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

        try:
            collection.database.command(
                {"collMod": cls.collection_name, "validator": validation_rules, "validationLevel": "strict"}
            )
        except OperationFailure as e:
            if "Collection does not exist" in str(e):
                print(f"Collection '{cls.collection_name}' does not exist. Skipping schema validation.")
            else:
                print(f"OperationFailure occurred for collection '{cls.collection_name}': {e.details}")
        except Exception as e:
            print(f"An unexpected error occurred for collection '{cls.collection_name}': {e}")

        return True
