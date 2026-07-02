"""Self-check: reproduce the corrected Table 4 example (topic "Polynomials").

Verifies the deterministic core (membership + aggregation) matches the
manuscript's numbers exactly. Run:  python -m pytest tests/  (or just run this file)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from membership import mu
from aggregation import topic_mastery

# Observed x values from Table 4 (corrected: 4 concepts + 4 links; the
# Basic-notions prerequisite "integer-exponent power" is aggregated elsewhere).
concept_x = {
    "monomial": 0.94,
    "polynomial": 0.81,
    "special_product_formulas": 0.47,
    "factoring": 0.63,
}
link_x = {
    ("monomial", "polynomial"): 0.90,
    ("polynomial", "special_product_formulas"): 0.58,
    ("polynomial", "factoring"): 0.52,
    ("special_product_formulas", "factoring"): 0.49,
}

EXPECTED_MU = {0.94: 1.0, 0.81: 0.775, 0.47: 0.0, 0.63: 0.325,
               0.90: 1.0, 0.58: 0.2, 0.52: 0.05, 0.49: 0.0}


def test_membership_values():
    for x, m in EXPECTED_MU.items():
        assert abs(mu(x) - m) < 1e-9, (x, mu(x), m)


def test_topic_estimate_is_0_44():
    cmu = [mu(x) for x in concept_x.values()]
    emu = [mu(x) for x in link_x.values()]
    a = topic_mastery(cmu, emu)   # w_C=0.6, w_E=0.4
    assert abs(a - 0.44) < 5e-3, a
    # binary count at 0.5 over the 8 elements = 6/8 = 75%
    xs = list(concept_x.values()) + list(link_x.values())
    binary = sum(1 for x in xs if x >= 0.5) / len(xs)
    assert abs(binary - 0.75) < 1e-9, binary


if __name__ == "__main__":
    test_membership_values()
    test_topic_estimate_is_0_44()
    print("OK: membership values and a(t) = 0.44, binary = 75% reproduced.")
