# Agent Operating Rules

This repository is a personal project template designed for Codex and Claude CLI.

## Default Reading Order

For any non-trivial task, read in this order:

1. `PROJECT_FORM.md`
2. `PROJECT_STATE.md`
3. `README.md`
4. `docs/WORKFLOW.md`
5. `docs/FILE_INDEX.md`
6. the relevant folder `README.md`
7. `work/INDEX.md` and the relevant work folder if continuing existing work

## Default Workflow

- Treat `PROJECT_FORM.md` as the user-owned project brief.
- Treat `PROJECT_STATE.md` as the agent-owned execution state.
- Create new generic work under `work/`.
- Create new experiments under `experiments/`.
- Do not leave important state only in chat.
- If structure changes, update `docs/FILE_INDEX.md` and relevant `README.md` files.
- Keep status, decisions, and next actions in repository files.

## Work Folder Rules

- Use `work/<status>/YYYY-MM-DD_<task_slug>/`.
- Default files are `TASK.md`, `CONTEXT.md`, `PLAN.md`, `TODO.md`, `LOG.md`, `DECISIONS.md`, and `task.json`.
- Update `TODO.md`, `LOG.md`, and `DECISIONS.md` as work progresses.
- Save final outputs in `OUTPUT/`.

## Experiment Folder Rules

- Use `experiments/<status>/YYYY-MM-DD_<experiment_name>/`.
- Move folders when status changes instead of copying them.
- Keep interpretation and publish decisions in the experiment `README.md`.

## Documentation Rules

- If you add a new top-level folder, add its `README.md`.
- Use obvious file names.
- Write continuation-critical state into `docs/`, `work/`, or `experiments/`.

## Completion Rules

- Keep `work/INDEX.md` current for completed work.
- Keep experiment status and `README.md` current for completed experiments.
- Keep `PROJECT_STATE.md` current for long-running projects.
- Move publish-ready outcomes into `reports/`, `publish/`, or `experiments/` as appropriate.
