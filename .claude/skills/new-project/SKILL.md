---
name: new-project
description: Guided setup that turns the vanilla Morphum template into a real project. Gathers project context, grills the user to a shared understanding (morphum:grilling), picks the archetype, has the morphum-dev librarian add the starter and suggested modules from the playbook library, applies the project identity, and verifies the project runs. Use when the user wants to start/kick off/configure/initialise a new project, or says "set up this template", "new project", or "walk me through setup".
argument-hint: "[optional: project code / short name]"
allowed-tools: Read Edit Write Grep Glob AskUserQuestion Bash(uv run:*) Bash(uv sync:*) Bash(python:*) Bash(python3:*) Bash(git:*) Bash(cp:*)
---

# New project setup (interview)

Turn the vanilla template into a project by understanding it first, then
building it from playbook modules. Ask, then do; don't dump checklists.

## Step 0 — The playbook must be there
This skill needs `morphum:grilling` and `morphum-dev:librarian`. If either is
unavailable, **stop** and tell the user:

> The Morphum playbook plugins aren't loaded. Sign in to Claude Code
> (≥ 2.1.273, `claude --version`) with the Morphum Team account, check
> Customize → Plugins (or `/plugin`) lists `morphum` and `morphum-dev`, then
> run `/new-project` again.

Never fall back to guessing what a starter or module contains.

## Principles
- **Never write real secrets.** The user types credentials into `.env`; you
  scaffold `.env` from `.env.example` and say which keys to fill.
- **Simplest shape that satisfies the brief.** Recommend from the starter's
  design guidelines, starting at "a single flow".
- **Confirm before anything destructive** (a reset, an overwrite). Git is the
  undo; say so.
- Work on the user's branch; don't push unless asked.

## Front-loaded brief
When the user supplies the context up front and says "proceed": infer each
answer, write every inference into the brief's open questions as an
assumption with its source, and batch confirmations into ONE message at the
end. "Proceed" covers the reset; it never covers deleting the user's files.

## Step 1 — Context intake
Invite the user to drop the brief, schemas, data dictionaries and key
threads into `references/` (pasted threads go to `references/threads/`).
Read everything; summarise what you know (client, deliverable, area, data,
deadlines) and what's unknown. Search `morphum:team-knowledge` for similar
past work.

## Step 2 — Grill to shared understanding
Run `morphum:grilling`, scaled to the stakes. The tree covers at least:
- **Archetype** (FIRST question, your inference as the recommendation):
  Python pipeline (starter `starters/python-pipeline`), web app (ArcGIS JS +
  Calcite or MapLibre per `standards/web-apps.md`), hybrid, or static HTML.
  Only the Python starter exists today; for the others the librarian's
  `blueprints/` are the scaffold, and the gap is a playbook candidate.
- **Where it runs** (`morphum:team-knowledge` → `standards/where-to-run.md`):
  will real client data sit on a local machine, or will runs go to the
  shared box? Then `environment/claude-container` is added in Step 4,
  before any data arrives. Memory worries alone are not a reason.
- **Deliverable**, **method shape**, **data** (every source and where it
  lives: a file, the network share, AGOL, the catalogue, S3; who provides
  what), **QA expectations**, **risks**.
- **The pilot** (define it carefully; it is what every early run reads): an
  extent (a catchment, a zone, a bbox) or an attribute filter that is small
  enough to review quickly and covers the method's edge cases; the halo that
  covers the largest search distance; whether it may be tracked in git (client
  agreement, caps). Network-share sources: who pulls them on the host
  (`python -m src.sources pull --scope pilot`), since Claude never reads the
  share.

Write the settled understanding to `references/project-brief.md` in the
`remember` brief format and seed `references/decision-log.md`. Confirm.

## Step 3 — Identity
Ask in ONE numbered message, then echo back for confirmation:
1. **Accelo job code** (`P0XXXX`): the one identifier everywhere.
2. **Short name** (`flood-mapping`); the repo is `P0XXXX-<short-name>`.
3. **Client**, as it appears on report headers.
4. **Purpose**, one paragraph.

## Step 4 — Modules
Hand over to `morphum-dev:librarian`:
1. Suggest the starter plus modules the brief implies (AGOL publishing →
   `publishing/agol-schema`; DEMs and catchments →
   `analysis/whitebox-hydrology`; reports or UI → `design/design-tokens`,
   pulled in by the starter anyway; local client data or box runs →
   `environment/claude-container`). Confirm the list.
2. `add <starter> --with-requires`, then each module. Show the `setup`
   commands; run them on confirmation.
3. Python starter: if the method doesn't resemble the worked example, blank
   it **before** the identity edits (`python scripts/reset_pipeline.py`, dry
   run, confirm, `--force`; `--flow stages` only if the staged triggers
   hold), then work through `references/post-reset-TODO.md`. The rest of
   the Python checklist is `docs/pipeline-setup.md`.
4. Catalogue entries the brief needs: `morphum-dev:data-catalogue` copies
   them in, stamped.

## Step 5 — Apply identity
Sweep `grep -rn '<PLACEHOLDER'` and every `P00000` / "Project Template":
`CLAUDE.md` (purpose, Accelo job, client; replace the "Stack and run
commands" placeholder line with one sentence naming the starter, the
module's block below it carries the detail), `README.md`, and what the
starter names (`pyproject.toml`, `[project]` in `config/*.toml`), and with
the container module `docker/docker-compose.yml` `name:`.

## Step 6 — Verify
Every installed module's `check` commands green (Python: `uv sync --frozen`,
`uv run ruff check .`, `uv run pytest -q`, `uv run python main.py` (the pilot)).
Fix failures before moving on.

## Step 7 — Finalise
- Rewrite `README.md` for the project (what it is, quick start, data
  provenance), not the template.
- Stamp the brief's identity line with the template version (top entry of
  `docs/CHANGELOG.md`) and the Modules line (each module and version from
  `references/modules.lock`).
- `remember`: founding decision-log entries, including "Added modules …".
- Deferred or user-only items go to `references/post-setup-TODO.md` (the
  SessionStart hook nags while it exists). Then list what only the user can
  do: fill `.env`, provide real data, confirm layer ids on first `describe`;
  with the container module, start it (`./docker/start-claude.sh`) and run
  `./docker/verify-sandbox.sh` before copying client data in.
- Commit: lock, `.modules/` and installed files together.
