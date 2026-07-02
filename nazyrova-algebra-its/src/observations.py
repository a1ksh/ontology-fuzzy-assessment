"""Compute the observed value x for each element from raw responses (Section 3.3).

x aggregates: difficulty-adjusted proportion correct (main signal) minus small
penalties from attempts and normalised time for uncertain solutions. For links,
x is taken from tasks requiring JOINT application of the two connected concepts.

TODO: implement using data/responses.csv + data/task_bank.csv, matching the exact
formula you used. Interface below is the contract consumed by the model.
"""
from __future__ import annotations
from typing import Dict, Tuple
import pandas as pd


def observed_x(responses: pd.DataFrame, task_bank: pd.DataFrame
               ) -> Tuple[Dict[str, float], Dict[Tuple[str, str], float]]:
    """Return (concept_x, link_x) in [0,1] for one learner. FILL IN."""
    raise NotImplementedError("Implement the x-aggregation used in Section 3.3.")
