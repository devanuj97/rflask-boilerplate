from modules.otp.internal.store.otp_model import OtpModel
from modules.otp.errors import OtpExpiredError, OtpIncorrectError
from modules.otp.internal.otp_util import OtpUtil
from modules.otp.types import CreateOtpParams, Otp, OtpStatus, VerifyOtpParams
from modules.otp.internal.store.otp_repository import OtpRepository
from modules.account.types import PhoneNumber

from pymongo import ReturnDocument


class OtpWriter:
    @staticmethod
    def expire_previous_otps(phone_number: PhoneNumber) -> None:
        previous_otps = OtpRepository.collection().find({"phone_number": phone_number, "active": True})
        for otp in previous_otps:
            OtpRepository.collection().update_one({"_id": otp["_id"]}, {"$set": {"status": OtpStatus.EXPIRED, "active": False}})
    
    @staticmethod
    def create_new_otp(*, params: CreateOtpParams) -> Otp:
        OtpWriter.expire_previous_otps(phone_number=params.phone_number)
        otp_code = OtpUtil.generate_otp(length=4)
        otp_bson = {
            "active": True,
            "otp_code": otp_code,
            "phone_number": params.phone_number,
            "status": OtpStatus.PENDING,
        }
        query = OtpRepository.collection().insert_one(otp_bson)
        otp = OtpRepository.collection().find_one({"_id": query.inserted_id})
        
        return OtpUtil.convert_otp_model_to_otp(OtpModel(**otp))
        
    @staticmethod
    def verify_otp(*, params: VerifyOtpParams) -> Otp:
        otp = OtpRepository.collection().find_one({"phone_number": params.phone_number, "otp_code": params.otp_code})
        if otp is None:
            raise OtpIncorrectError()
        
        if not otp["active"]:
            raise OtpExpiredError()
        
        updated_otp = OtpRepository.collection().find_one_and_update(
            {"_id": otp["_id"]},
            {"$set": {"status": OtpStatus.SUCCESS, "active": False}},
            return_document=ReturnDocument.AFTER,
        )
        return OtpUtil.convert_otp_model_to_otp(OtpModel(**updated_otp))
