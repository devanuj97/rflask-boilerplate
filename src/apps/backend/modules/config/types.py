from dataclasses import dataclass


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_name: str
    datadog_log_level: str
    host: str
