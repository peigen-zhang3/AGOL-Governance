# Template anatomy: vanilla core vs modules

Template v2 is **vanilla**: only what every Morphum project needs, whatever
it builds (pipeline, ETL, web app, static HTML). Everything stack-specific is
a **module** in the team playbook's library, copied in by the
`morphum-dev:librarian` and pinned. Team knowledge is **live** in the
`morphum` and `morphum-dev` plugins and never copied.

| Layer | Where | In a project |
|---|---|---|
| Vanilla core | this repo | copied once at project start; pull core fixes with `template-sync` |
| Modules | playbook library (`plugins/morphum-dev/skills/librarian/library/`) | copied in on request; recorded in `references/modules.lock`; untouched originals in `.modules/`; updates offered, never forced |
| Live knowledge | `morphum` and `morphum-dev` plugins | read in every session; nothing copied |

The rule that decides which layer a thing belongs to: **if Claude reads it,
it can be live; if code runs it, it is pinned in the project.**

## The vanilla core

| Path | What it is |
|---|---|
| `CLAUDE.md` | Absolute constraints, precedence, pinning rule, team playbook, update-notice fallback, sign-in check; placeholders the setup fills; `<!-- modules:insert -->` where module blocks go |
| `README.md` | The front door (rewritten per project at setup) |
| `.claude/settings.json` | Deny list for secrets, sandbox on, SessionStart hooks (env + `uv sync` when a `pyproject.toml` exists, unconfigured-template detection, post-setup nag, project memory) |
| `.claude/skills/` | `new-project`, `remember`, `capture`, `template-sync` |
| `.github/` | Hygiene CI + the `checks` job (runs when `pyproject.toml` exists), PR template with review tiers, issue templates, Dependabot for Actions |
| `.gitignore`, `.gitattributes`, `.env.example` | Secret and data rules, LF everywhere, the `.env` shape (modules insert their sections above `# modules:insert`) |
| `.pre-commit-config.yaml` | Hygiene hooks; modules insert theirs above `# modules:insert` |
| `references/` | `README.md`, `decision-log.md` and `playbook-candidates.md` stubs; the brief is born at `/new-project`; `modules.lock` arrives with the first module |
| `data/` | `README.md` (what each folder is, what git tracks, the opt-in `tracked/` rules) and `.gitkeep` placeholders |
| `docs/` | `GETTING_STARTED.md`, `git-workflow.md`, `claude-guide.md`, `CHANGELOG.md`, this page |
| `scripts/input_manifest.py` | Records the inputs a deliverable used (stdlib) |
| `tests/test_template_structure.py` | Stdlib structure test (core files, CLAUDE.md cap, `.gitignore` rules) |

## Modules (in the playbook library)

| Module | Brings |
|---|---|
| `environment/claude-container` | Opt-in: `docker/` (the fenced container, Herdr, Remote Control box, shared PostGIS), `docs/container.md`, `docs/remote-control-box.md`, the manual `sandbox.yml`. Added when real client data sits on a local machine or runs go to the box |
| `starters/python-pipeline` | `pyproject.toml`, `uv.lock`, `main.py`, `src/`, `tests/`, `scripts/`, `templates/`, `config/`, `tests/fixtures/`, the Python docs, a slim catalogue, ruff hooks, the Python CLAUDE.md block, skills `get-data`, `duckdb`, `agol-connect`, `run-pilot`, `new-report`, `sync-parameters`. Its own map: `docs/pipeline-anatomy.md` |
| `publishing/agol-schema` | AGOL schema as code: `scripts/agol/`, `config/agol/`, `docs/agol-*.md`, its test and skill |
| `analysis/whitebox-hydrology` | The Whitebox skill; installs the stack on demand |
| `design/design-tokens` | `assets/brand/` (brand.toml, CSS tokens, logos), `assets/clients/`, the Mermaid theme, `morphum-design` and `morphum-mermaid` |
| `design/basemap-switcher` | Spec only, for now |

Module files are yours to edit. A module marks some files `owned` (the
worked example, config, test fixture): those are never touched by updates.
Everything else is three-way merged against the untouched original, so
local edits survive.

## Live in the plugins

`morphum`: `team-knowledge` (tips by topic, standards, prompts), `grilling`,
`humanizer`. `morphum-dev`: `librarian` (the library), `data-catalogue`
(the full registry), `harvest`, `geospatial-conventions`, and the update
notice hook.

## v1 → v2
`MIGRATION_MAP.md` in the v2 PR lists where every v1.2 path went. Existing
projects follow the playbook's `standards/migrating-existing-project.md`.
