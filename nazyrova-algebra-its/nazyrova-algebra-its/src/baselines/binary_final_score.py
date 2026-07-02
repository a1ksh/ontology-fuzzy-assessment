"""Binary final-score baseline (Table 5): mark-based, no structure, cannot localise."""
def mastered(prop_correct_difficulty_adjusted: float, threshold: float = 0.60) -> bool:
    return prop_correct_difficulty_adjusted >= threshold
# NOTE: no ontology -> no gap localisation is produced ("-" in Table 5).
