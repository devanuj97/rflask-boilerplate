import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class OSSettings:
    INSPECTLET_KEY: Optional[str] = os.environ.get("INSPECTLET_KEY")
    MONGODB_URI: Optional[str] = os.environ.get("MONGODB_URI")
    SENDGRID: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {"api_key": os.environ.get("SENDGRID_API_KEY")}
    )
    MAILER: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {
            "default_email": os.environ.get("DEFAULT_EMAIL"),
            "default_email_name": os.environ.get("DEFAULT_EMAIL_NAME"),
            "forgot_password_mail_template_id": os.environ.get("FORGOT_PASSWORD_MAIL_TEMPLATE_ID"),
        }
    )
    OTP: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {
            "default_phone_number": os.environ.get("DEFAULT_PHONE_NUMBER"),
            "default_otp": os.environ.get("DEFAULT_OTP"),
        }
    )
    TWILIO: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {
            "account_sid": os.environ.get("TWILIO_ACCOUNT_SID"),
            "auth_token": os.environ.get("TWILIO_AUTH_TOKEN"),
            "messaging_service_sid": os.environ.get("TWILIO_MESSAGING_SERVICE_SID"),
        }
    )
    WEB_APP_HOST: Optional[str] = os.environ.get("WEB_APP_HOST")

    DATADOG: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {
            "datadog_api_key": os.environ.get("DATADOG_API_KEY"),
            "datadog_site_name": os.environ.get("DATADOG_SITE"),
            "datadog_app_name": os.environ.get("DATADOG_APP_NAME"),
            "datadog_log_level": os.environ.get("DATADOG_LOG_LEVEL")
        }
    )
