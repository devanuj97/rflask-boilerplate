from dataclasses import asdict

from pymongo import ReturnDocument

from modules.account.types import PhoneNumber
from modules.otp.errors import OtpExpiredError, OtpIncorrectError
from modules.otp.internal.otp_util import OtpUtil
from modules.otp.internal.store.otp_model import OtpModel
from modules.otp.internal.store.otp_repository import OtpRepository
from modules.otp.types import CreateOtpParams, Otp, OtpStatus, VerifyOtpParams


class OtpWriter:
    @staticmethod
    def expire_previous_otps(phone_number: PhoneNumber) -> None:
        phone_number_dict = asdict(phone_number)
        previous_otps = OtpRepository.collection().find({"phone_number": phone_number_dict, "active": True})
        for otp in previous_otps:
            OtpRepository.collection().update_one(
                {"_id": otp["_id"]}, {"$set": {"status": OtpStatus.EXPIRED, "active": False}}
            )

    @staticmethod
    def create_new_otp(*, params: CreateOtpParams) -> Otp:
        OtpWriter.expire_previous_otps(phone_number=params.phone_number)
        phone_number = PhoneNumber(**asdict(params)["phone_number"])
        otp_code = OtpUtil.generate_otp(length=4, phone_number=phone_number.phone_number)
        otp_bson = OtpModel(
            id=None, phone_number=phone_number, otp_code=otp_code, status=str(OtpStatus.PENDING), active=True
        ).to_bson()
        query = OtpRepository.collection().insert_one(otp_bson)
        otp = OtpRepository.collection().find_one({"_id": query.inserted_id})

        return OtpUtil.convert_otp_model_to_otp(OtpModel.from_bson(otp))

    @staticmethod
    def verify_otp(*, params: VerifyOtpParams) -> Otp:
        phone_number_dict = asdict(params.phone_number)
        otp = OtpRepository.collection().find_one(
            {"phone_number": phone_number_dict, "otp_code": params.otp_code}, sort=[("_id", -1)]
        )
        if otp is None:
            raise OtpIncorrectError()

        if not otp["active"]:
            raise OtpExpiredError()

        updated_otp = OtpRepository.collection().find_one_and_update(
            {"_id": otp["_id"]},
            {"$set": {"status": OtpStatus.SUCCESS, "active": False}},
            return_document=ReturnDocument.AFTER,
        )
        return OtpUtil.convert_otp_model_to_otp(OtpModel.from_bson(updated_otp))
