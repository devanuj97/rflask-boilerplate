from dataclasses import dataclass


@dataclass(frozen=True)
class PreviewSettings:
    LOGGER_TRANSPORTS: tuple[str, str] = ("console", "papertrail")
    SMS_ENABLED: bool = True
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True
