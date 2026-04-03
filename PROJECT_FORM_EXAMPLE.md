# Project Form Example

This file shows how `PROJECT_FORM.md` can be filled.

Do not use this as the live source of truth. Fill `PROJECT_FORM.md` with your own project instead.

## 1. Project Identity

- Project name: Local Study Notes Web App
- One-line summary: Build a small web app that uploads local Markdown notes and lets the user search and filter them by tags.
- Owner: ldh
- Repository / workspace name: notes-app
- Preferred language for docs and communication: English

## 2. Why This Project Exists

- What problem are you solving? Personal study notes are scattered and hard to search or reorganize.
- Why does this matter now? The note set is large enough that manual folder organization no longer works well.
- Who is the primary user? Me
- What should be true when this project is successful? I can upload notes, search them, filter them by tag, and revisit them from a browser.

## 3. End State

- What do you want Codex to build from zero? A small full-stack note management web app
- What counts as a usable first version? Note upload, list view, search, tag filter, and local run support
- What counts as done for this project? It runs reliably on localhost with basic tests and a usable README
- What is explicitly out of scope for now? Login, cloud sync, mobile app, multi-user support

## 4. Core Deliverables

- Deliverable 1: A locally runnable web app
- Deliverable 2: Basic tests
- Deliverable 3: Setup and run instructions

## 5. Product / System Scope

### Must-have

- Feature 1: Markdown file upload
- Feature 2: Title and body search
- Feature 3: Tag-based filtering

### Nice-to-have

- Nice-to-have 1: Recently viewed sort
- Nice-to-have 2: Better preview UI

### Non-goals

- Non-goal 1: User accounts
- Non-goal 2: External SaaS integrations

## 6. User Flow

- Entry point: Run locally and open in a browser
- Main user action sequence: Upload notes -> inspect list -> search -> filter by tag -> open a note
- Expected final output or outcome: A local browser app that makes notes easy to find and revisit

## 7. Technical Preferences

- Preferred stack: web app
- Preferred language: TypeScript
- Preferred framework: Next.js or Vite + React, whichever is simpler
- Preferred database: SQLite or simple local file storage
- Preferred deployment target: local first
- Preferred package manager: pnpm
- Preferred testing strategy: unit tests for core logic plus a minimal smoke test

## 8. Constraints

- Time constraints: reach the first usable version quickly
- Budget constraints: no paid services
- Compute constraints: local laptop environment
- External API / service constraints: avoid external APIs if possible
- Security / privacy constraints: note data should stay local
- Licensing constraints: use standard open-source libraries only

## 9. Autonomy Rules For Codex

- Can Codex install dependencies? `yes`
- Can Codex choose the stack if unspecified? `yes`
- Can Codex reorganize files if needed? `yes`
- Can Codex add tests? `yes`
- Can Codex add CI / lint config? `ask first`
- Can Codex use mock data when real data is unavailable? `yes`
- Can Codex make reasonable product decisions when unspecified? `yes`

## 10. Quality Bar

- Required code quality level: small but clean
- Required documentation level: enough for a new user to run it
- Required test level: at least the core behavior must be checked
- Required demo quality: local demo should feel stable
- What should Codex prioritize when trade-offs appear? prefer a working first version over heavy structure

## 11. Validation And Acceptance

- How will you judge that the project is working? I can upload notes and search/filter them successfully
- What commands or scenarios should pass? install, dev server run, basic tests
- What demo or walkthrough should be possible at the end? a new user can run it locally from the README

## 12. Inputs And References

- Existing repos or code to reference: none
- Existing docs to reference: official Next.js or React docs
- UI inspiration: simple list + detail note UI
- Architecture inspiration: small maintainable personal tool
- Anything Codex must not imitate: heavy enterprise structure

## 13. Open Questions

- Open question 1: use SQLite or filesystem metadata for storage
- Open question 2: use a separate search index or start with simple string search

## 14. First Instruction To Codex

- First instruction: design the smallest usable vertical slice, create the first work folder, and start implementation.

## 15. Fill Policy

- If something is unspecified, Codex should decide pragmatically.
