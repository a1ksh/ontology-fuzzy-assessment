# Data dictionary and anonymisation

## Anonymisation
- No names, emails, or free-text identifiers. Learners are `L001`..`L214`.
- Released under CC BY 4.0. Confirm ethics/consent (IRB) before publishing.

## Files
| file | rows | description |
|------|------|-------------|
| responses.csv | ~ | anonymised learner responses (answer, time, attempts) |
| task_bank.csv | 540 | tasks with concept/link labels + difficulty |
| expert_ratings.csv | 214x134 | two raters + reconciled reference levels |
| splits/folds.csv | 214 | stratified k-fold assignment by learner |
| ontology/ontology.json | 48+86 | reference ontology (concepts + prerequisite links) |

Each CSV ships with a schema header + sample rows; replace with the full data.
