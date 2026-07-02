"""Reproduce: Figure 6 (full-mastery thresholds 0.85/0.90/0.95).

Loads config/config.yaml + data/, runs the model and baselines under the
cross-validation split, writes results to results/sensitivity.csv.
TODO: wire to src/observations.py once x-aggregation is implemented.
"""
import yaml, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def main():
    with open(os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")) as fh:
        cfg = yaml.safe_load(fh)
    raise NotImplementedError("Wire to data + src; write results/sensitivity.csv.")

if __name__ == "__main__":
    main()
