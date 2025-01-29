from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from modules.account.types import PhoneNumber


@dataclass(frozen=True)
class OtpStatus(StrEnum):
    EXPIRED: str = "EXPIRED"
    PENDING: str = "PENDING"
    SUCCESS: str = "SUCCESS"


@dataclass(frozen=True)
class Otp:
    id: str
    otp_code: str
    phone_number: Optional[PhoneNumber]
    status: str


@dataclass(frozen=True)
class OtpErrorCode:
    INCORRECT_OTP: str = "OTP_ERR_01"
    OTP_EXPIRED: str = "OTP_ERR_02"
    REQUEST_FAILED: str = "OTP_ERR_03"


@dataclass(frozen=True)
class CreateOtpParams:
    phone_number: PhoneNumber


@dataclass(frozen=True)
class VerifyOtpParams:
    otp_code: str
    phone_number: PhoneNumber
