import random
import string

from modules.config.config_service import ConfigService
from modules.otp.internal.store.otp_model import OtpModel
from modules.otp.types import Otp


class OtpUtil:
    @staticmethod
    def is_default_phone_number(phone_number: str) -> bool:
        default_phone_number = None
        if ConfigService[str].has_value(key="otp.default_phone_number"):
            default_phone_number = ConfigService[str].get_value(key="otp.default_phone_number")
            if default_phone_number and phone_number == default_phone_number:
                return True
        return False

    @staticmethod
    def generate_otp(length: int, phone_number: str) -> str:
        if OtpUtil.is_default_phone_number(phone_number):
            default_otp = ConfigService[str].get_value(key="otp.default_otp")
            return default_otp
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def convert_otp_model_to_otp(otp_model: OtpModel) -> Otp:
        return Otp(
            id=str(otp_model.id),
            otp_code=otp_model.otp_code,
            phone_number=otp_model.phone_number,
            status=otp_model.status,
        )
