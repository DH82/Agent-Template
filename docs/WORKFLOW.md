# Workflow

This file defines the default operating flow for the repository.

## 1. Zero-to-One Project Loop

1. Fill `PROJECT_FORM.md`.
2. Let Codex read it and update `PROJECT_STATE.md`.
3. Let Codex choose the next highest-value action.
4. Let Codex create or continue the right `work/` or `experiments/` folder.
5. Let Codex update `PROJECT_STATE.md` and the relevant source-of-truth files.
6. Reuse `RUN_PROMPT.md` in the next session.

The goal is simple:
user intent stays in the project brief, execution state stays in the project state file, and the execution prompt stays stable across sessions.

## 2. New Generic Task

The standard flow is:

1. Create the task with `python3 scripts/workctl.py init <name> --title "<title>" --owner <owner>`
2. Write goals and done criteria in `TASK.md`
3. Write background and constraints in `CONTEXT.md`
4. Write the plan in `PLAN.md`
5. Update `TODO.md`, `LOG.md`, and `DECISIONS.md` during execution
6. Save outputs in `OUTPUT/`
7. Move the task when status changes

## 3. New Experiment

The standard flow is:

1. Create the experiment with `python3 scripts/expctl.py init <name> --title "<title>" --owner <owner>`
2. Fill the experiment `README.md` with hypothesis, metrics, and run plan
3. Save logs and results inside the experiment folder first
4. Promote shared outcomes into `results/`, `reports/`, or `publish/` when needed
5. Move status through `planned -> running -> completed -> published`

## 4. Documentation Discipline

- Keep important decisions in `DECISIONS.md` or `docs/DECISIONS/`
- Update `docs/FILE_INDEX.md` when structure changes
- Add a `README.md` when you add a new top-level folder

## 5. Team Extension

When turning this into a shared team template, add:

- `.github/ISSUE_TEMPLATE/`
- `.github/pull_request_template.md`
- CI or pre-commit validation
- shared lint and test tasks
- team-specific Claude subagents
