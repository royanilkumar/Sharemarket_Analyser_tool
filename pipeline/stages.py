"""Small, testable pipeline stages extracted from the master orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from screening.pre_screener import stage_1_filter, stage_2_fundamental_scorer
from screening.priority_ranker import get_top_100_candidates


@dataclass(frozen=True)
class ScreeningResult:
    universe: pd.DataFrame
    stage1: list[dict[str, Any]]
    stage2: pd.DataFrame
    selected: pd.DataFrame

    @property
    def counts(self) -> dict[str, int]:
        return {
            "universe": len(self.universe),
            "stage1": len(self.stage1),
            "stage2": len(self.stage2),
            "stage3": len(self.selected),
        }


def run_screening(universe: pd.DataFrame) -> ScreeningResult:
    """Run the three screening stages with a stable, inspectable result."""
    if universe is None or universe.empty:
        return ScreeningResult(
            universe=pd.DataFrame() if universe is None else universe,
            stage1=[],
            stage2=pd.DataFrame(),
            selected=pd.DataFrame(),
        )

    stage1 = stage_1_filter(universe.to_dict("records"))
    stage2 = stage_2_fundamental_scorer(pd.DataFrame(stage1))
    selected = get_top_100_candidates(stage2)
    return ScreeningResult(universe, stage1, stage2, selected)
