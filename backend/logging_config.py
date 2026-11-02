"""Structured Logging — JSON-formatted logs for production observability.

Usage:
    from backend.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info("Simulation started", extra={"instrument": "hplc", "user_id": 42})
"""
import logging
import json
import sys
from datetime import datetime, timezone
from .config import LOG_LEVEL, LOG_FORMAT


class JSONFormatter(logging.Formatter):
    """Outputs log records as single-line JSON for easy parsing by log aggregators."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Include extra fields (instrument, user_id, etc.)
        for key in ("instrument", "user_id", "compound_id", "endpoint",
                     "status_code", "duration_ms", "error"):
            val = getattr(record, key, None)
            if val is not None:
                log_entry[key] = val

        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class PrettyFormatter(logging.Formatter):
    """Human-readable colored output for local development."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        prefix = f"{color}{record.levelname:8s}{self.RESET}"
        return f"{prefix} [{record.name}] {record.getMessage()}"


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        if LOG_FORMAT == "json":
            handler.setFormatter(JSONFormatter())
        else:
            handler.setFormatter(PrettyFormatter())
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
        logger.propagate = False
    return logger
