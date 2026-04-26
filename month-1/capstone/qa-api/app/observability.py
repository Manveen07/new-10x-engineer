import os

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup_observability(app: FastAPI, service_name: str = "month1-qa-api") -> None:
    if os.environ.get("OTEL_SDK_DISABLED", "").lower() == "true":
        return

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    # Check if OTLP exporter is configured
    if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
        processor = BatchSpanProcessor(OTLPSpanExporter())
    else:
        processor = BatchSpanProcessor(ConsoleSpanExporter())

    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Auto-instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Auto-instrument async HTTPX clients
    HTTPXClientInstrumentor().instrument()

    # SQLAlchemy instrumentation will be bound when the engine is created.
