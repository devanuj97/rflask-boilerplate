from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionSettings:
    LOGGER_TRANSPORTS: tuple[str, str] = ("console", "datadog")
    SMS_ENABLED: bool = True
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True
