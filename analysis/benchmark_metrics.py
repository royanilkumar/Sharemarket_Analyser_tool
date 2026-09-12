"""Benchmark-relative return helpers for performance analysis."""

from __future__ import annotations

from typing import Iterable


def relative_return_pct(stock_return_pct: float, benchmark_return_pct: float) -> float:
    """Return stock outperformance versus a benchmark in percentage points."""
    return round(float(stock_return_pct) - float(benchmark_return_pct), 2)


def summarize_relative_returns(rows: Iterable[dict]) -> dict:
    """Summarize benchmark-relative returns without requiring pandas."""
    values = []
    for row in rows:
        try:
            values.append(relative_return_pct(row["stock_return_pct"], row["benchmark_return_pct"]))
        except (KeyError, TypeError, ValueError):
            continue
    if not values:
        return {"n": 0, "mean_relative_pct": None, "median_relative_pct": None}
    ordered = sorted(values)
    middle = len(ordered) // 2
    median = ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2
    return {"n": len(values), "mean_relative_pct": round(sum(values) / len(values), 2), "median_relative_pct": round(median, 2)}
