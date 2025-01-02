from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from modules.account.internal.store.account_model import AccountModel
from modules.application.repository import ApplicationRepository


class AccountRepository(ApplicationRepository):
    collection_name = AccountModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("username")
        print("working")
        validation_rules = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["username", "hashed_password"],
                "properties": {
                    "username": {"bsonType": "string", "description": "must be a string and is required"},
                    "hashed_password": {"bsonType": "string", "description": "must be a string and is required"},
                    "first_name": {"bsonType": "string"},
                    "last_name": {"bsonType": "string"},
                    "active": {"bsonType": "bool"},
                    "phone_number": {
                        "bsonType": ["object", "null"],
                        "properties": {"country_code": {"bsonType": "string"}, "phone_number": {"bsonType": "string"}},
                        "description": "must be an object with country_code and phone_number",
                    },
                    "created_at": {"bsonType": "date"},
                    "updated_at": {"bsonType": "date"},
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