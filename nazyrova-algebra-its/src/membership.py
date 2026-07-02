"""Fuzzy membership and level aggregation for a single knowledge element.

Implements the model of Section 3.3 of the manuscript:
  - piecewise-linear membership function mu(x)            (eq. 6)
  - level aggregation mu_C(c) = mu( sum_l lambda_l mu_R ) (eq. 8)

These parts are fully specified by the paper and are implemented exactly,
so the numerical example in Table 4 is reproducible from this file alone
(see tests/test_membership.py).
"""
from __future__ import annotations
from typing import Mapping

# Thresholds from Section 3.3 (Figure 3). Overridable via config.yaml.
X_LOW = 0.5    # below -> unmastered (contribution filtered out)
X_HIGH = 0.9   # at/above -> full mastery


def mu(x: float, x_low: float = X_LOW, x_high: float = X_HIGH) -> float:
    """Piecewise-linear membership function of a knowledge element (eq. 6).

    mu(x) = 0                         if x < x_low
          = (x - x_low)/(x_high-x_low) if x_low <= x < x_high
          = 1                         if x >= x_high
    """
    if x < x_low:
        return 0.0
    if x >= x_high:
        return 1.0
    return (x - x_low) / (x_high - x_low)


def aggregate_over_levels(mu_r: Mapping[str, float],
                          lambda_l: Mapping[str, float]) -> float:
    """Generalised degree of command of one concept/link (eq. 8).

    mu_C(c) = mu( sum_l lambda_l * mu_R(c, l) ),  with sum_l lambda_l = 1.

    Args:
        mu_r: level_id -> truth degree that the element is held at that level.
        lambda_l: level_id -> aggregation weight (must sum to 1).
    """
    s = sum(lambda_l[l] * mu_r.get(l, 0.0) for l in lambda_l)
    if abs(sum(lambda_l.values()) - 1.0) > 1e-9:
        raise ValueError("level weights lambda_l must sum to 1")
    return mu(s)
