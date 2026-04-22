from pythonjsonlogger import jsonlogger

from sigla_sdk.context import get_correlation_id


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        cid = get_correlation_id()
        if cid:
            log_record["correlation_id"] = cid

        if record.name == "django.server" or record.module == "basehttp":
            keys_to_remove = ["request", "server_time", "process", "thread"]
            for key in keys_to_remove:
                log_record.pop(key, None)
            log_record["module"] = "http_access"

        if "levelname" in log_record:
            log_record["level"] = log_record.pop("levelname")

