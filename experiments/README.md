# Experiments

This folder stores experiments by lifecycle status.

Use `work/` for general implementation work.
Use `experiments/` only for reproducible hypothesis-run-result-interpretation workflows.

- `planned/`: not started yet
- `running/`: actively running
- `completed/`: run and first-pass interpretation finished
- `published/`: shared internally or externally
- `archive/`: long-term storage

Prefer creating experiments with `scripts/expctl.py init <name>`.

Standard experiment folder:

```text
YYYY-MM-DD_<experiment_name>/
  README.md
  experiment.json
  configs/
  scripts/
  logs/
  results/
  figures/
  publish/
```
