# Codex Zero-to-One Guide

This guide explains the operating model:
write the project brief once, then keep reusing the same run prompt.

## Core Idea

Remember these three files:

- `PROJECT_FORM.md`: user-owned project brief
- `PROJECT_STATE.md`: agent-owned project state
- `RUN_PROMPT.md`: repeated prompt for each session

Helpful extras:

- `PROJECT_FORM_EXAMPLE.md`
- `docs/GUIDES/fill-project-form.md`

## How To Use

1. Fill `PROJECT_FORM.md` clearly.
2. Start a new Codex session and paste `RUN_PROMPT.md`.
3. Let Codex update `work/`, `experiments/`, and `PROJECT_STATE.md`.
4. Reuse the same `RUN_PROMPT.md` in later sessions unless the project direction changed.

## What The Agent Should Do

- read the project goal from `PROJECT_FORM.md`
- maintain current state in `PROJECT_STATE.md`
- store implementation work in `work/`
- use `experiments/` when experimental workflows are needed
- keep important decisions in files, not only in chat

## What The User Should Update

- edit `PROJECT_FORM.md` when goals, scope, constraints, or autonomy rules change
- let Codex maintain `PROJECT_STATE.md` for normal execution progress

## Failure Modes To Avoid

- project intent exists only in chat
- each session uses a different prompt style
- progress is not recorded in `work/` and `PROJECT_STATE.md`
