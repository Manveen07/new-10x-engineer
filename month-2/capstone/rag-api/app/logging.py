import logging
import sys
from pythonjsonlogger import jsonlogger
from opentelemetry import trace

def setup_logging(log_level: str = "INFO") -> None:
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Discard existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Note: custom class allows injecting OpenTelemetry trace_id and span_id
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super().add_fields(log_record, record, message_dict)
            
            # Inject OpenTelemetry context if available
            span = trace.get_current_span()
            if span and span.get_span_context().is_valid:
                log_record["trace_id"] = f"{span.get_span_context().trace_id:x}"
                log_record["span_id"] = f"{span.get_span_context().span_id:x}"
            
            # Inject request_id if previously set in log_record
            if hasattr(record, "request_id"):
                log_record["request_id"] = record.request_id

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
