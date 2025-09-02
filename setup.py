"""Setup configuration for hello_phoenix package."""

from setuptools import setup, find_packages

setup(
    name="hello-phoenix",
    version="0.1.0",
    description="Multi-agent greeting system with Phoenix tracing",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.1.1",
        "openai>=1.101.0",
        "arize-phoenix-otel>=0.13.0",
        "openinference-instrumentation-openai>=0.1.31",
        "openinference-instrumentation-langchain>=0.1.50",
        "langchain>=0.3.27",
        "langchain-openai>=0.3.31",
        "langgraph>=0.6.6",
    ],
    extras_require={
        "dev": [
            "pytest>=8.4.1",
            "pytest-asyncio>=1.1.0",
        ]
    },
)
