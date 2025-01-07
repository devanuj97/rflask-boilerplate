from bson.objectid import ObjectId
from pymongo import ReturnDocument

from modules.password_reset_token.errors import PasswordResetTokenNotFoundError
from modules.password_reset_token.internal.password_reset_token_util import PasswordResetTokenUtil
from modules.password_reset_token.internal.store.password_reset_token_model import PasswordResetTokenModel
from modules.password_reset_token.internal.store.password_reset_token_repository import PasswordResetTokenRepository
from modules.password_reset_token.types import PasswordResetToken


class PasswordResetTokenWriter:
    @staticmethod
    def create_password_reset_token(account_id: str, token: str) -> PasswordResetToken:
        token_hash = PasswordResetTokenUtil.hash_password_reset_token(token)
        expires_at = PasswordResetTokenUtil.get_token_expires_at()

        new_token_data = {
            "account": ObjectId(account_id),
            "expires_at": expires_at,
            "token": token_hash,
            "is_used": False,
        }
        created_token = PasswordResetTokenRepository.collection().insert_one(new_token_data)
        password_reset_token = PasswordResetTokenRepository.collection().find_one({"_id": created_token.inserted_id})
        return PasswordResetTokenUtil.convert_password_reset_token_model_to_password_reset_token(
            PasswordResetTokenModel.from_bson(password_reset_token)
        )

    @staticmethod
    def set_password_reset_token_as_used(password_reset_token_id: str) -> PasswordResetToken:
        updated_token = PasswordResetTokenRepository.collection().find_one_and_update(
            {"_id": ObjectId(password_reset_token_id)},
            {"$set": {"is_used": True}},
            return_document=ReturnDocument.AFTER,  # Return the updated document
        )
        if updated_token is None:
            raise PasswordResetTokenNotFoundError()

        return PasswordResetTokenUtil.convert_password_reset_token_model_to_password_reset_token(
            PasswordResetTokenModel.from_bson(updated_token)
        )
