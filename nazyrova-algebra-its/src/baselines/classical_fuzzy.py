"""Classical fuzzy baseline (Table 5/7): same membership per element, NO ontology links."""
from membership import mu
def concept_only_mu(concept_x):
    # elements treated independently; links are not modelled -> link gaps unrepresentable
    return {c: mu(x) for c, x in concept_x.items()}
