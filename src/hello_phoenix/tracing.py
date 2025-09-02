"""Phoenix tracing setup for LangChain and OpenAI."""

import os

# pylint: disable=import-error
from dotenv import load_dotenv
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.instrumentation.langchain import LangChainInstrumentor
# pylint: enable=import-error


def setup_tracing(project_name="hello-phoenix"):
    """Setup Phoenix tracing for OpenAI and LangChain.

    Args:
        project_name: The Phoenix project name for organizing traces

    Returns:
        tracer_provider: The OpenTelemetry tracer provider
    """
    load_dotenv()

    endpoint = os.getenv(
        "PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces"
    )

    print(f"📡 Setting up tracing to: {endpoint}")
    print(f"📊 Phoenix Project: {project_name}")

    tracer_provider = register(
        project_name=project_name,
        endpoint=endpoint,
        auto_instrument=False,  # Disable auto-instrumentation to avoid conflicts
    )

    # Manually instrument only if not already instrumented
    try:
        OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    except Exception:  # pylint: disable=broad-exception-caught
        pass  # Already instrumented

    try:
        LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    except Exception:  # pylint: disable=broad-exception-caught
        pass  # Already instrumented

    print("✅ Tracing enabled for OpenAI and LangChain")

    return tracer_provider
