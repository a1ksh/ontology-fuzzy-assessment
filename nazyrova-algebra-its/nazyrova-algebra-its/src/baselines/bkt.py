"""Bayesian Knowledge Tracing baseline + explicit gap-mapping rule.

This file documents and implements the mapping requested by reviewers:
how a per-concept BKT posterior is converted into concept/link-level gaps
(Section 3.8, "BKT-to-gap mapping").

RULE (must match the manuscript exactly):
  1. Fit BKT per concept (skill): parameters (p_init, p_learn, p_slip, p_guess).
  2. After a learner's response sequence, obtain posterior mastery p(L) per concept.
  3. Flag concept c as a FIRST-TYPE gap iff p(L_c) < tau  (tau = 0.5, Section 3.5).
  4. BKT has NO parameter for prerequisite links -> SECOND-TYPE (link) gaps are
     never flagged and are counted as MISSED.
  5. Gap-localisation % is computed against the SAME denominator as the proposed
     model: the full set of expert-identified gaps over BOTH concepts and links.

Consequently BKT localisation is entirely concept-level (reported 47.5%); the
shortfall vs. the ontology-based models is exactly the unformed-link gaps BKT
cannot represent.
"""
from __future__ import annotations
from typing import Dict, List, Mapping, Sequence, Tuple

TAU = 0.5


class BKTParams:
    """Per-skill BKT parameters. FILL WITH YOUR FITTED VALUES / settings."""
    def __init__(self, p_init: float, p_learn: float, p_slip: float, p_guess: float):
        self.p_init = p_init
        self.p_learn = p_learn
        self.p_slip = p_slip
        self.p_guess = p_guess


def bkt_posterior(responses: Sequence[int], params: BKTParams) -> float:
    """Standard BKT forward update -> posterior P(mastered) after the sequence.

    responses: ordered 0/1 correctness for tasks tagged with this concept.
    """
    pL = params.p_init
    for r in responses:
        # observation update
        if r == 1:
            num = pL * (1 - params.p_slip)
            den = num + (1 - pL) * params.p_guess
        else:
            num = pL * params.p_slip
            den = num + (1 - pL) * (1 - params.p_guess)
        pL_obs = num / den if den > 0 else pL
        # learning transition
        pL = pL_obs + (1 - pL_obs) * params.p_learn
    return pL


def bkt_gaps(concept_responses: Mapping[str, Sequence[int]],
             concept_params: Mapping[str, BKTParams],
             link_ids: Sequence[Tuple[str, str]],
             tau: float = TAU) -> Dict[str, List]:
    """Apply the mapping rule above.

    Returns concept_gaps (p(L) < tau) and link_gaps (ALWAYS empty for BKT:
    links are structurally unrepresentable and thus counted as missed).
    """
    concept_gaps = []
    for c, resp in concept_responses.items():
        if c in concept_params:
            if bkt_posterior(resp, concept_params[c]) < tau:
                concept_gaps.append(c)
    # BKT cannot represent prerequisite links -> never flagged (counted missed)
    link_gaps: List[Tuple[str, str]] = []
    return {"concept_gaps": concept_gaps, "link_gaps": link_gaps,
            "unrepresentable_links": list(link_ids)}
