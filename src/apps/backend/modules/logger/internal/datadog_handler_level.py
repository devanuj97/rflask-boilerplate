from modules.config.config_service import ConfigService
import logging

class LogLevel:
    @staticmethod
    def get_level() -> int:
        ddconfig = ConfigService.get_datadog_config()
        level = ddconfig.datadog_log_level.lower()
        logging_levels = ["notset","debug","info","warning","error","critical"]
        if level.lower() not in logging_levels:
            return logging.DEBUG
        else :
            if level == logging_levels[0]:
                return logging.NOTSET
            elif level == logging_levels[1]:
                return logging.DEBUG
            elif level == logging_levels[2]:
                return logging.INFO
            elif level == logging_levels[3]:
                return logging.WARNING
            elif level == logging_levels[4]:
                return logging.ERROR
            else :
                return logging.CRITICAL
