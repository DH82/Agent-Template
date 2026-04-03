# Architecture

This template has three layers.

## 1. Instruction Layer

- `AGENTS.md`: shared operating rules
- `CLAUDE.md`: Claude entry file
- `.claude/agents/`: optional reusable Claude subagents

This layer defines how agents should behave inside the repository.

## 2. Workflow Layer

- `PROJECT_FORM.md`: user-owned brief
- `PROJECT_STATE.md`: agent-owned execution state
- `RUN_PROMPT.md`: repeated session prompt
- `work/`: generic work management
- `experiments/`: experiment management
- `scripts/workctl.py` and `scripts/expctl.py`: workflow automation
- `Taskfile.yml`: repeated command entrypoints

This layer keeps long-running work resumable across sessions.

## 3. Domain Layer

- `configs/`, `results/`, `logs/`, `reports/`, `publish/`, `notes/`

This layer holds real project artifacts.

## Design Principles

- Keep project intent in files, not in chat history.
- Separate user intent from execution state.
- Separate generic work from experiments.
- Keep entry files short and obvious.
- Prefer resumable progress over one-shot prompting.
