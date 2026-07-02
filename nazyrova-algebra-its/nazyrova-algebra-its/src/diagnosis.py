"""Structural gap diagnosis (Section 3.5, eq. 14-15).

Distinguishes first-type gaps (unmastered concepts) from second-type gaps
(unformed links with mastered endpoints) - the latter being invisible to
per-concept and mark-based models.
"""
from __future__ import annotations
from typing import Mapping, Tuple, Dict, List

TAU = 0.5  # diagnostic threshold (lower bound of partial mastery)


def gap_set(concept_mu: Mapping[str, float],
            link_mu: Mapping[Tuple[str, str], float],
            tau: float = TAU) -> Dict[str, list]:
    """Gap set G (eq. 14): concepts and links with mu < tau."""
    concept_gaps = [c for c, m in concept_mu.items() if m < tau]
    link_gaps = [e for e, m in link_mu.items() if m < tau]
    return {"concept_gaps": concept_gaps, "link_gaps": link_gaps}


def classify_gaps(concept_mu: Mapping[str, float],
                  link_mu: Mapping[Tuple[str, str], float],
                  tau: float = TAU) -> Dict[str, list]:
    """First-type = unmastered concept; second-type = unformed link whose
    two endpoints are both mastered (mu >= tau)."""
    first, second = [], []
    for c, m in concept_mu.items():
        if m < tau:
            first.append(c)
    for (a, b), m in link_mu.items():
        if m < tau and concept_mu.get(a, 0.0) >= tau and concept_mu.get(b, 0.0) >= tau:
            second.append((a, b))
    return {"first_type": first, "second_type": second}


def similarity(concept_mu: Mapping[str, float],
               link_mu: Mapping[Tuple[str, str], float]) -> float:
    """Integral correspondence of individual to reference ontology (eq. 15)."""
    n = len(concept_mu) + len(link_mu)
    if n == 0:
        return 0.0
    return (sum(concept_mu.values()) + sum(link_mu.values())) / n
