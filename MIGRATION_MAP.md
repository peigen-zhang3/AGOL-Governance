# Move map: template v1.2 → v2 (vanilla core + playbook)

Every tracked path in template v1.2 and where it goes. Destinations:

- **Core**: stays in `Project-Template` (vanilla v2), edited where noted.
- **Starter**: `library/starters/python-pipeline` in the playbook (copied into a project by `modules.py add`).
- **Module**: another library module (`publishing/agol-schema`, `analysis/whitebox-hydrology`, `design/design-tokens`).
- **Playbook**: live knowledge in the `morphum` or `morphum-dev` plugin.
- **Delete**: removed, with the reason.

Module paths are relative to `plugins/morphum-dev/skills/librarian/library/`. Inside a module, `files/<path>` installs to `<path>` in the project unless noted.

## Core (stays in the template)

| Path | Change |
|---|---|
| `CLAUDE.md` | Rewritten as the vanilla core (< 120 lines): absolute constraints, precedence, pinning rule, team playbook, update-notice fallback, sign-in check. Python rules move to the starter's CLAUDE.md block |
| `README.md` | Rewritten for the v2 model |
| `.claude/settings.json` | Kept; `uv sync` guarded behind `[ -f pyproject.toml ]` |
| `.claude/settings.local.json.example` | Kept |
| `.claude/skills/new-project/` | Rewritten: grilling → archetype → librarian adds starter + modules → identity → verify |
| `.claude/skills/remember/` | Edited: `**Playbook:** candidate \| no`, candidates file, trailer, module adds/updates |
| `.claude/skills/capture-tip/` | Renamed `capture/`: writes client-free candidates, `playbook-candidate:` trailer |
| `.claude/skills/template-sync/` | Reduced to pulling vanilla-core updates |
| `.gitignore`, `.gitattributes` | Kept |
| `.env.example` | Kept; PostGIS and box sections move to the container module's block; `# modules:insert` added |
| `.github/pull_request_template.md` | Edited: review tier, reviewer line; Python checks made conditional |
| `.github/workflows/ci.yml` | Hygiene job kept (+ vanilla structure test); new `checks` job when `pyproject.toml` exists |
| `.github/dependabot.yml` | Kept |
| `.github/ISSUE_TEMPLATE/` | New: `task.yml`, `bug.yml`, `config.yml` |
| `.pre-commit-config.yaml` | Slimmed to hygiene hooks; ruff arrives as a starter block |
| `references/README.md` | Edited: memory files, candidates, `modules.lock`, `.modules/` |
| `references/decision-log.md`, `references/playbook-candidates.md` | New stubs |
| `data/inputs/.gitkeep`, `data/library/.gitkeep`, `data/outputs/.gitkeep`, `data/outputs-dev/.gitkeep` | Kept, except `outputs-dev/` (removed: runs write `data/outputs/<scope>/`); `data/cache/.gitkeep` added |
| `data/README.md` | New: the data folders, what git tracks, the opt-in `data/tracked/` rules (enforced by `.gitignore`, CI, pre-commit, structure test) |
| `docs/GETTING_STARTED.md` | Rewritten cloud-first; the container half moves to the module's `docs/container.md` |
| `docs/git-workflow.md`, `docs/claude-guide.md` | Edited for v2 |
| `docs/CHANGELOG.md` | `template-v2.0` entry |
| `docs/template-anatomy.md` | Rewritten as the vanilla/module map |
| `scripts/input_manifest.py` | New (stdlib): `deliverables/<tag>/inputs.json` |
| `tests/test_template_structure.py` | Replaced by a stdlib vanilla structure test (incl. the `.gitignore` checks) |

## Starter: `starters/python-pipeline`

| Path | Note |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | `uv.lock` marked generated (regenerate, never text-merge) |
| `main.py`, `src/**` | Moves as one unit (`src/config.py` ↔ `src/datalib.py` ↔ `src/agol`) |
| `tests/**` except `test_agol_publish.py` and `test_template_structure.py` | |
| `tests/test_template_structure.py` (pipeline-seam half) | Becomes `tests/test_machinery_seam.py` |
| `scripts/config_to_sheet.py`, `scripts/sheet_to_config.py`, `scripts/make_sample_data.py`, `scripts/setup.sh` | |
| `scripts/reset_pipeline.py` | Adapted to the module layout (docs paths, detector) |
| `templates/report.html.j2` | |
| `config/config.toml`, `config/README.md` | |
| `data/inputs-dev/README.md`, `data/inputs-dev/SampleDatabase.gpkg` | Became the test fixture `tests/fixtures/example.gpkg`; the pilot scope replaces dev data |
| `docs/parameter-dictionary.md`, `docs/report-guide.md`, `docs/design-guidelines.md`, `docs/diagrams/pipeline-overview.mmd` | |
| `docs/TEMPLATE_SETUP.md` | Becomes `docs/pipeline-setup.md` |
| `references/data-catalogue.toml` | Starter ships the `[meta]` block plus the national LINZ entries; the full registry is in the playbook |
| `.pre-commit-config.yaml` ruff hooks | Inserted as a module block |
| `CLAUDE.md` run commands, architecture, Python constraints and conventions | Inserted as a module block |
| `.claude/skills/get-data`, `duckdb`, `agol-connect`, `run-sample`, `new-report`, `sync-parameters` | Copied into the project's `.claude/skills/` (`run-sample` renamed `run-pilot`) |

## Other modules

| Path | Module |
|---|---|
| `docker/**` (Claude Code pinned to 2.1.308; `run.*` explain the starter), `.dockerignore`, `docs/remote-control-box.md`, container half of `GETTING_STARTED.md` and `README.md` → `docs/container.md`, new manual `.github/workflows/sandbox.yml`, `.env.example` PostGIS + box sections (block), a CLAUDE.md block | `environment/claude-container` (opt-in: local client data or box runs) |
| `assets/brand/**`, `assets/clients/README.md` | `design/design-tokens` |
| `docs/diagrams/README.md`, `docs/diagrams/_brand.mmd` | `design/design-tokens` |
| `.claude/skills/morphum-design`, `.claude/skills/morphum-mermaid` | `design/design-tokens` |
| `scripts/agol/**`, `config/agol/**`, `docs/agol-publishing.md`, `docs/agol-schema.md`, `tests/test_agol_publish.py`, `.claude/skills/agol-schema` | `publishing/agol-schema` (requires the starter) |
| `.claude/skills/whitebox-hydrology` | `analysis/whitebox-hydrology` (skill only; `setup` lists the `uv add`) |
| *(new)* | `design/basemap-switcher` 0.1.0: spec stub for Ben |

## Playbook knowledge (live)

| Path | Destination |
|---|---|
| `docs/tips-and-tricks.md` | `morphum/skills/team-knowledge/knowledge/<topic>.md`, split by topic, indexed |
| `docs/prompts/library.md` | `morphum/skills/team-knowledge/prompts/library.md` |
| `docs/blueprints/**` | `morphum-dev/skills/librarian/blueprints/` (source for the coming web-app and hybrid starters) |
| `references/data-catalogue.toml` (full) | `morphum-dev/skills/data-catalogue/data-catalogue.toml` |
| `.claude/skills/grilling`, `.claude/skills/humanizer` | `morphum/skills/` |
| `.claude/skills/geospatial-conventions` | `morphum-dev/skills/` |

## Deleted

| Path | Why |
|---|---|
| `.github/workflows/deep-checks.yml` | `lint-test` and `reset-seam` become the playbook's `module-tests.yml`; the projects' own `checks` job covers lint and tests. The `sandbox` job is kept as a manual `sandbox.yml` in the container module, the only thing that proves the fence |
