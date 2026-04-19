from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_observability(app: FastAPI, service_name: str = "month1-qa-api") -> None:
    # Basic tracing setup, can be swapped for OTLP exporter in production
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    
    # Exporting spans to console for local visibility. 
    # In prod, this would be an OTLP exporter to Langfuse, Jaeger, etc.
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    
    # Auto-instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
