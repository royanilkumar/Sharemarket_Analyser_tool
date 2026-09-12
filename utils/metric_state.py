"""Explicit missing-data semantics for numeric market metrics."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MetricStatus(str, Enum):
    AVAILABLE = "available"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass(frozen=True)
class MetricValue:
    value: float | None
    status: MetricStatus
    source: str | None = None
    reason: str | None = None

    @property
    def is_available(self) -> bool:
        return self.status is MetricStatus.AVAILABLE and self.value is not None


def parse_metric(value: Any, source: str | None = None) -> MetricValue:
    """Parse legacy values without treating missing data as a real zero."""
    if value is None or value == "" or str(value).strip() in {"—", "--", "N/A", "NA"}:
        return MetricValue(None, MetricStatus.MISSING, source, "no source value")
    try:
        return MetricValue(float(value), MetricStatus.AVAILABLE, source)
    except (TypeError, ValueError):
        return MetricValue(None, MetricStatus.ERROR, source, "not numeric")


def display_metric(metric: MetricValue, missing: str = "—") -> float | str:
    return metric.value if metric.is_available else missing
