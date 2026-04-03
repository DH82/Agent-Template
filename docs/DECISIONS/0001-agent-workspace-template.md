# 0001. Agent Workspace Template

## Status

Accepted

## Context

We needed a personal repository template that both Codex and Claude CLI could use consistently.
The repository already had experiment management, but it did not yet provide a unified operating model for generic work, zero-to-one project setup, and resumable execution state.

## Decision

Use the following structure:

- `PROJECT_FORM.md` for the user-owned brief
- `PROJECT_STATE.md` for the agent-owned execution state
- `RUN_PROMPT.md` for the repeated prompt
- `work/` for generic work
- `experiments/` for experiments
- `docs/` for structural guidance
- `scripts/` and `Taskfile.yml` for automation
- `.claude/agents/` for reusable Claude-specific subagents

## Consequences

- Agents have a clear starting point in new sessions.
- Product intent and execution state are separated.
- Generic work and experiments are easier to manage independently.
- The repository now depends more heavily on keeping `PROJECT_STATE.md`, `work/INDEX.md`, and `docs/FILE_INDEX.md` current.
