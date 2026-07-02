# Ontology–Fuzzy Assessment Model for Elementary Algebra (ITS)

Reproducibility package for the paper *“Intelligent Learning and Knowledge-Control
Tools for Elementary Algebra: An Ontology–Fuzzy Assessment Model and Adaptive
Architecture.”* It contains the anonymised dataset, the reference ontology, the
expert-rating protocol, the train/test split, the baseline settings, and the code
that reproduces **every reported number** (Cohen’s κ, RMSE, gap-localisation,
sensitivity, and topic-mastery).

> Status of this scaffold: the fully specified parts of the method (the
> piecewise-linear membership function, the multilevel aggregation, the gap
> diagnosis, and the BKT→gap mapping rule) are implemented and unit-tested.
> Parts that depend on the private data (`x`-aggregation, BKT fitting, and the
> end-to-end evaluation scripts) are provided as typed stubs marked `TODO`/`FILL`
> — drop in the data and settings to complete reproduction.

## What reviewers asked for → where it lives

| Requested artefact | Location |
|---|---|
| Anonymised dataset | `data/responses.csv` |
| Task-bank labels (540 tasks) | `data/task_bank.csv` |
| Ontology file (48 concepts, 86 links) | `data/ontology/ontology.json` |
| Expert-rating protocol | `expert_protocol/rating_protocol.md`, `data/expert_ratings.csv` |
| Train/test split | `data/splits/folds.csv` |
| BKT parameter settings + gap mapping | `config/config.yaml`, `src/baselines/bkt.py` |
| Fuzzy-membership code (eq. 6, 8) | `src/membership.py` |
| Ablation scripts (Table 7) | `experiments/eval_ablation.py` |
| Scripts reproducing κ / RMSE / localisation | `experiments/eval_agreement.py` |
| Sensitivity (0.85/0.90/0.95, Fig 6) | `experiments/sensitivity.py` |
| Topic-mastery (Table 6 / Fig 7) | `experiments/topic_mastery.py` |
| Statistical tests (bootstrap CI, Wilcoxon, Holm–Bonferroni) | `experiments/stats.py` |

## Repository layout

```
nazyrova-algebra-its/
├── README.md                     ← you are here
├── Makefile                      ← make setup / test / reproduce
├── config/config.yaml            ← thresholds, weights, seeds, BKT + split settings
├── data/
│   ├── README.md                 ← data dictionary + anonymisation notes
│   ├── responses.csv             ← anonymised learner responses
│   ├── task_bank.csv             ← 540 labelled tasks
│   ├── expert_ratings.csv        ← two raters + reconciled reference
│   ├── splits/folds.csv          ← stratified k-fold by learner
│   └── ontology/ontology.json    ← 48 concepts + 86 prerequisite links
├── src/
│   ├── membership.py             ← μ(x) + level aggregation      (eq. 6, 8)   [implemented]
│   ├── aggregation.py            ← topic→discipline→programme     (eq. 9–13)   [implemented]
│   ├── diagnosis.py              ← gap set, sim, gap types        (eq. 14–15)  [implemented]
│   ├── ontology.py               ← load/validate/transitive closure           [implemented]
│   ├── observations.py           ← compute x from raw responses   (Section 3.3) [TODO]
│   ├── model.py                  ← full ontology–fuzzy model                   [implemented]
│   └── baselines/
│       ├── binary_final_score.py ← mark-based, no structure  (Table 5)
│       ├── classical_fuzzy.py    ← fuzzy, no ontology        (Table 5/7)
│       └── bkt.py                ← BKT + explicit gap-mapping (Section 3.8)
├── experiments/
│   ├── run_all.py                ← one-command full reproduction
│   ├── eval_agreement.py         ← Table 5
│   ├── eval_ablation.py          ← Table 7
│   ├── sensitivity.py            ← Figure 6
│   ├── topic_mastery.py          ← Table 6 / Figure 7
│   └── stats.py                  ← significance tests
├── expert_protocol/rating_protocol.md
├── tests/test_membership.py      ← reproduces the Table 4 worked example
└── results/                      ← generated tables/figures land here
```

## Quick start

```bash
git clone <REPO_URL> && cd nazyrova-algebra-its
python -m venv .venv && source .venv/bin/activate
make setup           # pip install -r requirements.txt
make test            # unit test: reproduces the Table 4 example (a(t)=0.44, binary=75%)
make reproduce       # regenerates all tables/figures into results/
```

## The parts that are already reproducible

`make test` runs `tests/test_membership.py`, which recomputes the worked example
of Table 4 (topic *Polynomials*, 4 concepts + 4 links) directly from
`src/membership.py` and `src/aggregation.py` and checks:

- μ(0.94)=1.00, μ(0.81)=0.775, μ(0.47)=0.00, μ(0.63)=0.325, μ(0.58)=0.20, μ(0.52)=0.05
- topic estimate **a(t) ≈ 0.44** (≈ 44/100)
- binary count at 0.5 = **6/8 = 75%**

This anchors the deterministic core of the model to the paper before any data is added.

## Baselines and the BKT gap-mapping rule

All baselines receive the **same** observations, labels, and derived feature `x`;
they differ only in how estimates are formed (see the paper, Section 3.8).

- **Binary final-score** (`binary_final_score.py`): 60% threshold, no ontology →
  produces one number, cannot localise gaps (“—” in Table 5).
- **Classical fuzzy** (`classical_fuzzy.py`): same membership per element, no links.
- **BKT** (`bkt.py`): per-concept posterior `p(L)`; a concept is a **first-type**
  gap iff `p(L) < τ` (τ = 0.5). BKT has **no** link parameter, so **second-type
  (link) gaps are never flagged and are counted as missed**, against the same
  denominator (all expert-identified concept + link gaps) as the proposed model.
  Hence BKT’s localisation is entirely concept-level.

## Reproducing the reported values

| Output | Command | Writes |
|---|---|---|
| Table 5 (κ, RMSE, localisation) | `python experiments/eval_agreement.py` | `results/eval_agreement.csv` |
| Table 7 (ablation) | `python experiments/eval_ablation.py` | `results/eval_ablation.csv` |
| Figure 6 (sensitivity) | `python experiments/sensitivity.py` | `results/sensitivity.csv` |
| Table 6 / Figure 7 | `python experiments/topic_mastery.py` | `results/topic_mastery.csv` |
| All of the above | `python experiments/run_all.py` | `results/` |

Seeds and every threshold/weight live in `config/config.yaml`, so runs are
deterministic.

## To finish reproduction (checklist for the authors)

- [ ] Replace the schema rows in `data/*.csv` with the full anonymised data.
- [ ] Replace `data/ontology/ontology.json` with the full 48-concept / 86-link file.
- [ ] Fill `config.yaml → baselines.bkt` with the fitted (p_init, p_learn, p_slip,
      p_guess) or the settings + `fit: EM`.
- [ ] Fill `config.yaml → split.k` with the actual number of folds.
- [ ] Implement `src/observations.py::observed_x` with the exact `x`-aggregation used.
- [ ] Wire the four `experiments/*.py` runners to the data + `src`.
- [ ] Confirm IRB/consent and full anonymisation before publishing the data.

## Ethics & licensing

Code: MIT (`LICENSE`). Data: CC BY 4.0 **after** full anonymisation; confirm
consent/IRB. See `data/README.md`.

## Citation

See `CITATION.cff`. Archive a tagged release on Zenodo and cite the DOI in the paper’s
*Data and Code Availability* statement.
