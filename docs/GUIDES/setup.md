# Setup Guide

## Codex

- Use the repository with `AGENTS.md` as the shared operating baseline.
- Use `scripts/workctl.py` for generic work.
- Use `scripts/expctl.py` for experiments.

## Claude Code

- `CLAUDE.md` imports the shared rules and core docs.
- Put reusable project subagents in `.claude/agents/`.
- Use the same generic work and experiment structure as Codex.

## Recommended First Commands

```bash
python3 scripts/workctl.py tree
python3 scripts/expctl.py tree
python3 scripts/workctl.py validate --all
python3 scripts/expctl.py validate --all
```
