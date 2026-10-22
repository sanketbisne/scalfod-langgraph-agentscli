"""Cloud Trace and GenAI structured logging setup."""

import logging
import os


def setup_telemetry() -> None:
    """Configures structured logging and optional Cloud Trace exporter."""
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
