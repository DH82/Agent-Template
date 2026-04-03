# Agent Workspace Template

This `README.md` is for the person using the template, not for the agent.

The idea is simple:

- Write down what you want once.
- Reuse almost the same Codex prompt in every session.
- Let Codex keep the execution state in files so the project continues cleanly across sessions.

## What This Template Is For

Use this template when:

- you want to start a project from zero with Codex
- you want project context to live in files instead of chat history
- you want to separate product intent from execution state
- you want one repeated run prompt instead of rewriting long prompts every time

## Core Idea

The main files are:

- [PROJECT_FORM.md](PROJECT_FORM.md): the user-owned project brief
- [PROJECT_STATE.md](PROJECT_STATE.md): the Codex-owned execution state
- [RUN_PROMPT.md](RUN_PROMPT.md): the single repeated prompt for new sessions

Helpful supporting files:

- [PROJECT_FORM_EXAMPLE.md](PROJECT_FORM_EXAMPLE.md): an example brief
- [fill-project-form.md](docs/GUIDES/fill-project-form.md): how to fill the form well

The responsibility split is:

- you edit `PROJECT_FORM.md`
- Codex updates `PROJECT_STATE.md`
- you reuse `RUN_PROMPT.md` in later sessions

## Quick Start

1. Fill [PROJECT_FORM.md](PROJECT_FORM.md).
2. Be especially clear about:
   - what you want to build
   - what counts as the first usable version
   - what is out of scope for now
   - your technical preferences
   - how much autonomy Codex has
3. Run Codex in this repository.
4. Paste the prompt from [RUN_PROMPT.md](RUN_PROMPT.md).
5. Review the `work/`, `experiments/`, and `PROJECT_STATE.md` updates Codex makes.
6. In later sessions, reuse the same [RUN_PROMPT.md](RUN_PROMPT.md) unless project direction changed.

If a blank form feels hard to start from, read [PROJECT_FORM_EXAMPLE.md](PROJECT_FORM_EXAMPLE.md) first.

## What You Should Edit

You will usually edit:

- [PROJECT_FORM.md](PROJECT_FORM.md)
- selected result docs or reports when needed
- any direction-setting docs if project goals change

Update `PROJECT_FORM.md` first when:

- the product direction changes
- must-haves or non-goals change
- your stack preference changes
- you want to change Codex autonomy
- the definition of done changes

## What Codex Should Update

Codex should usually update:

- [PROJECT_STATE.md](PROJECT_STATE.md)
- the active folder under `work/`
- experiments under `experiments/` when needed
- `docs/` and related `README.md` files when structure changes

In short:

- `PROJECT_FORM.md` is owned by you
- `PROJECT_STATE.md` is maintained by Codex

## Recommended Session Loop

### First session

1. Fill `PROJECT_FORM.md`.
2. Paste `RUN_PROMPT.md`.
3. Let Codex create the first work folder and initialize project state.

### Later sessions

1. If direction changed, edit `PROJECT_FORM.md`.
2. Otherwise, paste `RUN_PROMPT.md` again.
3. Let Codex continue updating `PROJECT_STATE.md` and the relevant folders.

This avoids re-explaining the project in each session.

## Folder Guide

The main folders you will care about are:

- [work/](work): implementation, writing, research, planning, cleanup
- [experiments/](experiments): hypothesis, run, result, interpretation, publish flows
- [docs/](docs): structure and workflow guidance
- [templates/](templates): reusable file skeletons
- [scripts/](scripts): CLIs for creating, moving, and validating work

### When to use `work/`

Use `work/` for:

- feature implementation
- refactoring
- documentation
- research
- planning

### When to use `experiments/`

Use `experiments/` when the flow is:

- hypothesis
- execution
- result collection
- interpretation
- publish or decision

Typical cases:

- model comparison
- parameter tuning
- performance experiments
- log/result-based analysis
- pre-release verification experiments

## The Only Repeated Prompt

The repeated session prompt lives in [RUN_PROMPT.md](RUN_PROMPT.md).

The rule is simple:

- use it in the first session
- use it again in later sessions
- do not keep rewriting the prompt unless the operating model itself changes

That keeps Codex behavior stable across sessions.

## How To Get Better Results

You will usually get better results if the initial brief clearly states:

- the user and the problem
- the first-version scope
- non-goals
- quality expectations
- test expectations
- deployment target
- how much Codex should decide on its own

You will usually get worse results from vague briefs like:

- "build me some app"
- "just do something good"
- no must-have / non-goal split
- no definition of done

## Files You Usually Do Not Need To Edit Often

These files mainly support the template itself:

- [AGENTS.md](AGENTS.md)
- [CLAUDE.md](CLAUDE.md)
- [FILE_INDEX.md](docs/FILE_INDEX.md)
- [WORKFLOW.md](docs/WORKFLOW.md)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)

They are useful reference files, but they are not the normal starting point for a template user.

## Useful Commands

```bash
# show generic work structure
python3 scripts/workctl.py tree

# validate generic work structure
python3 scripts/workctl.py validate --all

# create a new generic work item
python3 scripts/workctl.py init repo_cleanup --title "Repository cleanup" --owner ldh

# show experiment structure
python3 scripts/expctl.py tree

# validate experiment structure
python3 scripts/expctl.py validate --all

# create a new experiment
python3 scripts/expctl.py init attention_ablation --title "Attention ablation" --owner ldh
```

## Recommended First Action

Start here:

1. Fill [PROJECT_FORM.md](PROJECT_FORM.md).
2. Paste [RUN_PROMPT.md](RUN_PROMPT.md) into Codex.

## License

This template is licensed under the MIT License. See [LICENSE](LICENSE).
