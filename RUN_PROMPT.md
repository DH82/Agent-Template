# Run Prompt

This file contains the single repeated prompt for ongoing Codex sessions.

How to use it:
- Reuse it in each new session with little or no change.
- Usually fill `PROJECT_FORM.md` first, then keep reusing this prompt.
- If project direction changes, edit `PROJECT_FORM.md` instead of changing this prompt.

```text
Continue this project from the current repository state.

Operate as the main implementation agent for a zero-to-one code project.

Before doing substantial work, read and use these files as the source of truth:
- `PROJECT_FORM.md`
- `PROJECT_STATE.md`
- `README.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/ARCHITECTURE.md`
- `work/INDEX.md`
- any currently relevant `work/` folder
- any currently relevant `experiments/` folder

Execution rules:

1. Treat `PROJECT_FORM.md` as the user-owned product brief.
2. Treat `PROJECT_STATE.md` as the agent-owned execution state.
3. If there is no suitable active work folder, create one aligned to the highest-priority unfinished objective.
4. If the request requires experiments, create or continue the right experiment folder.
5. Pick the single highest-value next action that moves the project toward a working end state.
6. Execute that action end-to-end instead of stopping at analysis when safe to proceed.
7. Update repository files so another agent can continue without chat history.
8. Update `PROJECT_STATE.md`, the active `work/` files, and any other affected source-of-truth files.
9. If you change structure, update `docs/FILE_INDEX.md` and related `README.md` files.
10. Validate your work whenever possible.

Behavior:

- Do not ask broad planning questions if `PROJECT_FORM.md` already gives enough direction.
- Do not create multiple competing plans.
- Do not leave important decisions only in chat.
- Do not guess blindly if a critical product decision is truly missing; ask one short blocking question.
- Prefer steady incremental progress over large speculative rewrites.
- Prefer a working vertical slice early.

At the start of the session, report briefly:
- current phase
- chosen target folder
- next action

At the end of the session, report briefly:
- what changed
- what was validated
- what remains
- the exact next recommended action
```
