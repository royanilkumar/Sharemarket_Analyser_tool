"""Structured logging helpers for daily pipeline runs."""

from __future__ import annotations

import json
import logging
import os
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in ("run_id", "stage", "status", "elapsed_ms", "rows", "errors"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        return json.dumps(payload, ensure_ascii=True)


def configure_pipeline_logging(log_path: str = "pipeline.log") -> logging.Logger:
    logger = logging.getLogger("sharemarket.pipeline")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream = logging.StreamHandler()
    stream.setFormatter(JsonFormatter())
    logger.addHandler(stream)

    if log_path:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)
    return logger


@contextmanager
def stage(logger: logging.Logger, name: str, run_id: str, **fields) -> Iterator[None]:
    started = time.perf_counter()
    logger.info(
        "stage_started",
        extra={"run_id": run_id, "stage": name, **fields},
    )
    try:
        yield
    except Exception:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        logger.exception(
            "stage_failed",
            extra={"run_id": run_id, "stage": name, "status": "failed", "elapsed_ms": elapsed_ms},
        )
        raise
    else:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        logger.info(
            "stage_completed",
            extra={"run_id": run_id, "stage": name, "status": "completed", "elapsed_ms": elapsed_ms},
        )
