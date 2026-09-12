"""Central scoring thresholds.

Keep these values versioned with the code that consumes them. Recommendation
rows should persist the configuration version so later performance analysis can
separate rule-set changes from market effects.
"""

CONFIG_VERSION = "v17.8.1"

CAP_THRESHOLDS = {
    "LARGE": (60, 50),
    "MID": (63, 53),
    "SMALL": (66, 56),
    "MICRO": (70, 60),
}

AVOID_BELOW = 38
MIN_INFORMED_FOR_BUY = 3

# Gold / market gates used by reporting and the orchestrator.
GOLD_MIN_SCORE = 70
GOLD_MIN_MOS = 15
GOLD_MAX_MOS = 100
REGIME_TOLERANCE_PCT = 0.5

# Risk controls used by the multi-factor trade-plan calculation.
SL_MIN_PCT = 4.5
SL_MAX_PCT = 15.0
