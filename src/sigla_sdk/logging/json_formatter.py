from pythonjsonlogger import jsonlogger

from sigla_sdk.context import get_correlation_id
import elasticapm


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        cid = get_correlation_id()
        if cid:
            log_record["correlation_id"] = cid

        transaction_id = elasticapm.get_transaction_id()
        trace_id = elasticapm.get_trace_id()
        span_id = elasticapm.get_span_id()

        if transaction_id:
            log_record["trace.id"] = trace_id
            log_record["transaction.id"] = transaction_id
            log_record["span.id"] = span_id
            log_record["elasticapm_transaction_id"] = transaction_id
            log_record["elasticapm_trace_id"] = trace_id
            log_record["elasticapm_span_id"] = span_id

        apm_labels = getattr(record, "elasticapm_labels", None)
        if apm_labels:
            for key, value in apm_labels.items():
                if value is not None:
                    log_record[key] = value

        if record.name == "django.server" or record.module == "basehttp":
            keys_to_remove = ["request", "server_time", "process", "thread"]
            for key in keys_to_remove:
                log_record.pop(key, None)
            log_record["module"] = "http_access"

        if "levelname" in log_record:
            log_record["level"] = log_record.pop("levelname")

