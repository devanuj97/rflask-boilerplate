from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from modules.account.internal.store.account_model import AccountModel
from modules.application.repository import ApplicationRepository

ACCOUNT_VALIDATION_SCHEMA = {
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

class AccountRepository(ApplicationRepository):
    collection_name = AccountModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("username")

        add_validation_command = {
            "collMod": cls.collection_name, 
            "validator": ACCOUNT_VALIDATION_SCHEMA, 
            "validationLevel": "strict"
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            # If the collection does not exist, create it with the validation rules
            if "Collection does not exist" in str(e):
                collection.database.create_collection(cls.collection_name, validator=ACCOUNT_VALIDATION_SCHEMA)
            else:
                print("OperationFailure occurred for collection accounts",e.details)
        return True
