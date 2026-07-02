"""Hierarchical aggregation: element -> topic -> discipline -> programme.

Implements Section 3.4 of the manuscript (eq. 9-12). Fully specified by the
paper; reproducible without learner data given per-element mu values.
"""
from __future__ import annotations
from typing import Mapping, Sequence

W_C = 0.6  # weight of declarative (concept) knowledge   (w_C + w_E = 1)
W_E = 0.4  # weight of structural (link) knowledge


def topic_mastery(concept_mu: Sequence[float],
                  link_mu: Sequence[float],
                  w_c: float = W_C, w_e: float = W_E) -> float:
    """Degree of mastery of a topic (eq. 9).

    a(t) = w_C/|C| * sum mu_C + w_E/|E| * sum mu_E,  normalised by set sizes.
    """
    if abs((w_c + w_e) - 1.0) > 1e-9:
        raise ValueError("w_c + w_e must equal 1")
    term_c = (w_c / len(concept_mu)) * sum(concept_mu) if concept_mu else 0.0
    term_e = (w_e / len(link_mu)) * sum(link_mu) if link_mu else 0.0
    return term_c + term_e


def discipline_mastery(topic_values: Mapping[str, float],
                       topic_weights: Mapping[str, float]) -> float:
    """Weighted convolution of topic estimates (eq. 10). sum omega = 1."""
    if abs(sum(topic_weights.values()) - 1.0) > 1e-9:
        raise ValueError("topic weights omega must sum to 1")
    return sum(topic_weights[t] * topic_values[t] for t in topic_weights)


def programme_mastery(discipline_values: Mapping[str, float],
                      discipline_weights: Mapping[str, float]) -> float:
    """Weighted convolution of disciplinary estimates (eq. 12). sum beta = 1."""
    if abs(sum(discipline_weights.values()) - 1.0) > 1e-9:
        raise ValueError("discipline weights beta must sum to 1")
    return sum(discipline_weights[d] * discipline_values[d] for d in discipline_weights)


def to_hundred_point(k_j: float) -> float:
    """Linear map of an integral estimate to a 100-point scale (eq. 13)."""
    return 100.0 * k_j
