from __future__ import annotations


# Display-only coefficients for public KURGIN Index UI.
# These values do not change scoring formula or pricing formula.
SCORE_RANGE_SELECTOR_ORDER = [
    "standard",
    "high",
    "premium",
    "elite",
    "fair",
    "poor",
    "rejected",
]

SCORE_INDEX_RULES = {
    "standard": {"mode": "numeric", "coefficient": 1.00, "coefficient_label": "×1.00"},
    "high": {"mode": "numeric", "coefficient": 1.20, "coefficient_label": "×1.20"},
    "premium": {"mode": "numeric", "coefficient": 1.40, "coefficient_label": "×1.40"},
    "elite": {"mode": "numeric", "coefficient": 1.70, "coefficient_label": "×1.70"},
    "fair": {"mode": "request_caution", "coefficient": 0.00, "coefficient_label": "request / caution"},
    "poor": {"mode": "request", "coefficient": 0.00, "coefficient_label": "request"},
    "rejected": {"mode": "request", "coefficient": 0.00, "coefficient_label": "request"},
}
