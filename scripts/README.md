# Scripts

This folder holds workspace automation.

## Main Entry Points

`workctl.py` and `expctl.py` are the main CLIs.

```bash
python3 scripts/workctl.py tree
python3 scripts/workctl.py guide work
python3 scripts/workctl.py init <name> --title "<title>" --owner <owner>
python3 scripts/workctl.py list
python3 scripts/workctl.py validate --all
python3 scripts/workctl.py move <task> completed

python3 scripts/expctl.py tree
python3 scripts/expctl.py guide experiments
python3 scripts/expctl.py init <name> --title "<title>" --owner <owner>
python3 scripts/expctl.py list
python3 scripts/expctl.py validate --all
python3 scripts/expctl.py move <experiment> running
```

## Contents

- `workctl.py`: create, move, validate, and index generic work
- `expctl.py`: create, move, and validate experiments
- `run/`: shared run scripts
- `collect/`: log/result collection scripts
- `analyze/`: analysis scripts
- `publish/`: publish preparation scripts

Guidelines:

- Keep only reusable workspace-level scripts here.
- Put one-off scripts inside the relevant work or experiment folder.
