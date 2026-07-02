"""Full ontology-fuzzy model: ties membership, aggregation and diagnosis together."""
from __future__ import annotations
from typing import Dict, Tuple
from membership import mu
from aggregation import topic_mastery
from diagnosis import gap_set, classify_gaps, similarity


def score_learner(concept_x: Dict[str, float],
                  link_x: Dict[Tuple[str, str], float]) -> dict:
    concept_mu = {c: mu(x) for c, x in concept_x.items()}
    link_mu = {e: mu(x) for e, x in link_x.items()}
    return {
        "concept_mu": concept_mu,
        "link_mu": link_mu,
        "gaps": gap_set(concept_mu, link_mu),
        "gap_types": classify_gaps(concept_mu, link_mu),
        "similarity": similarity(concept_mu, link_mu),
    }
