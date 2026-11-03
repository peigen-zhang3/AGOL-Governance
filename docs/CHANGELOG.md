# Template changelog

The template's own version history — projects note the version they forked from
(the `/new-project` setup stamps it into `references/project-brief.md`), and
`template-sync` pulls reference it. Since v2.0 this covers the vanilla core
only; modules keep their own CHANGELOGs in the playbook library. Tag releases `template-vX.Y` (see
`docs/git-workflow.md`). Newest first.

## template-v2.0 — 2026-10-26 (breaking)

**The template is now vanilla.** Projects are standalone, the team playbook
(`Morphum-Environmental/geospatial-playbook`) is the library, and this repo
holds only what every project needs, whatever it builds.

- **The model.** Three layers: this vanilla core (copied once); the
  playbook's live layer, synced to the Claude org as the `morphum` and
  `morphum-dev` plugins (knowledge, standards, prompts, data catalogue,
  librarian, harvest, the module update notice); and the playbook's library
  of **modules**, copied into a project on request and pinned in
  `references/modules.lock`, with untouched originals in `.modules/` for
  three-way merges. If Claude reads it, it can be live; if code runs it, it
  is pinned in the project.
- **What moved where** (full list: `MIGRATION_MAP.md` in the v2.0 PR):
  - the Python machinery and worked example (`pyproject.toml`, `uv.lock`,
    `main.py`, `src/`, `tests/`, `scripts/`, `templates/`, `config/`,
    `data/inputs-dev/` (now the test fixture), the Python docs, ruff hooks,
    and the `get-data`, `duckdb`, `agol-connect`, `run-sample` (now
    `run-pilot`), `new-report` and
    `sync-parameters` skills) → module `starters/python-pipeline`
    (`docs/template-anatomy.md` became its `docs/pipeline-anatomy.md`;
    `docs/TEMPLATE_SETUP.md` its `docs/pipeline-setup.md`);
  - AGOL schema as code → `publishing/agol-schema`; the Whitebox skill →
    `analysis/whitebox-hydrology`; `assets/` and the brand skills →
    `design/design-tokens`;
  - `docs/tips-and-tricks.md` → the playbook's knowledge base, split by
    topic; `docs/prompts/` → its prompt library; `docs/blueprints/` → the
    librarian's blueprints; the full `references/data-catalogue.toml` → the
    `data-catalogue` skill (projects pin the entries they use);
  - `grilling` and `humanizer` → the `morphum` plugin;
    `geospatial-conventions` → `morphum-dev`.
- **Core skills.** `new-project` rewritten (grilling → archetype → the
  librarian adds the starter and modules → identity → verify; it stops if
  the plugins aren't loaded). `remember` gains `**Playbook:** candidate | no`
  and records module changes. `capture-tip` is now `capture`: client-free
  candidates in `references/playbook-candidates.md` with a
  `playbook-candidate:` commit trailer, harvested weekly. `template-sync`
  only pulls core updates.
- **CLAUDE.md** is the vanilla core (< 120 lines): absolute constraints,
  precedence (project brief → CLAUDE.md → playbook), the pinning rule, the
  team playbook, the sign-in check and the update-notice fallback. Modules
  insert their blocks above `<!-- modules:insert -->`.
- **CI, change of decision.** v1.1 took lint and tests off push/PR (the
  template rebuilt the geo stack on every merge). v2's core has no Python,
  so `ci.yml` adds a `checks` job that runs `uv sync --frozen`, ruff and
  pytest only when `pyproject.toml` exists: free on the template, a real
  gate for every Python project. `deep-checks.yml` is gone: lint-test and
  the reset seam run in the playbook's module tests; the sandbox job is
  kept as the manual `sandbox.yml` in the container module. The hygiene job also runs the new
  stdlib structure test.
- **Data boundaries: pilot by extent.** The dev tree is gone
  (`data/inputs-dev/`, `data/outputs-dev/`). Runs read the real sources
  through a scope: a pilot (an extent or attribute filter, the default) or
  the full run, each with its own `data/cache/<scope>/` and
  `data/outputs/<scope>/` (the Python starter's `docs/sources-and-scopes.md`).
  `data/README.md` defines `inputs/`, `cache/`, `outputs/`, `library/`
  (ignored) and a new **opt-in `data/tracked/`** for a scope a cloud session
  must keep (client agreed, private repo, personal fields stripped, ≤ 25 MB
  per file, ≤ 250 MB in total, a filled-in `data/tracked/README.md`).
  Synthetic test data lives in `tests/fixtures/`. `.gitignore`, the CI
  hygiene job and the structure test enforce it; named review runs inside
  `tracked/` stay ignored. The CLAUDE.md client-data constraint names both
  tracked folders and says network-share data is pulled on the host.
- **Deliverable inputs.** `scripts/input_manifest.py` writes
  `deliverables/<tag>/inputs.json` (path, sha256, size, mtime of
  `data/inputs/` and `data/cache/`) before a `deliverable/*` tag; data is never copied.
- **PR and issue templates.** Review tiers (self-merge / review recommended
  / review expected) and a Reviewer line; `task.yml` (Accelo job, project,
  acceptance criteria), `bug.yml`, and links to the playbook.
- **The Claude container is opt-in.** `docker/`, `.dockerignore`,
  `docs/remote-control-box.md` and the container half of `GETTING_STARTED.md`
  (now `docs/container.md`) move to the module
  `environment/claude-container`, with the manual `sandbox.yml` and its
  `.env.example` sections (PostGIS, box token) as a block. Most projects
  develop in cloud sessions and never need it. A new CLAUDE.md constraint
  keeps the guarantee: real client data on a local machine is worked on only
  inside the container, so setup adds the module before such data arrives.
  It is a security fence, not more memory. In the module: Claude Code pinned
  to 2.1.308 (npm `stable`, 2026-10-26); `run.sh` / `run.ps1` explain that
  `main.py` comes with the Python starter. In the core: the SessionStart
  `uv sync` runs only when `pyproject.toml` exists, and `GETTING_STARTED.md`
  is cloud-first.

**Starting a project:** "Use this template", open it in a Claude Code cloud
session signed in with the Morphum Team account (≥ 2.1.273), run
`/new-project`.

**Existing v1.x projects** keep working as they are. To adopt modules and
get update notices, follow the playbook's
[`standards/migrating-existing-project.md`](https://github.com/Morphum-Environmental/geospatial-playbook/blob/main/plugins/morphum/skills/team-knowledge/standards/migrating-existing-project.md).

## template-v1.2 — 2026-10-26

From P06236 (the first schema-as-code publish, Oct 2026):

- **AGOL schema as code:** `config/agol/schema.json` defines a hosted feature
  service (layers, fields, domains, indexes, relationships, views, folder,
  groups, version history). `scripts/agol/publish.py` builds it from ArcGIS
  Pro (`propy`, `GIS("pro")`: no credentials handled), `migrate.py` moves
  records into a new version through a mapping file and stops on any problem,
  `schema_doc.py` generates `docs/agol-schema.md`. Dry run by default; never
  replaces, edits or deletes existing content; a portal banner and
  `--portal` guard stop writes to the wrong org; `--diagnose` isolates which
  part of a definition AGOL rejects. Guide: `docs/agol-publishing.md`; skill:
  `agol-schema`; tests: `tests/test_agol_publish.py` (offline, no arcgis).
- **Nine AGOL publishing tips** in `docs/tips-and-tricks.md`, including the
  relationship call-order quirk, Pro's `datetime` clobbering, private groups,
  `create_view` renames and Survey123 photo keywords.

Bug fixes from P05841 (the first project set up on the one-config release):

- **AGOL extracts no longer stop at the server's record cap:** ArcGIS servers
  return at most their own `maxRecordCount` per page (often 1,000) and set
  `exceededTransferLimit`, but `agol_extract` stopped at the first page
  shorter than it asked for, so extracts were silently cut (1,000 of 4,286
  features in P05841). It now pages on the flag and raises on an `error` body
  instead of reading it as an empty page. Regression tests for both.
- **Reports are escaped:** `select_autoescape(["html", "xml"])` never matched
  `*.html.j2`, so every report rendered with autoescaping off and data text
  (an address, a name with `<` or `&`) went into the HTML raw. `render.py`
  adds `"j2"`; the shipped templates (the example, the reset stub and the test
  fixture) mark their brand CSS values `|safe`, since entities are not decoded
  inside `<style>`. New test: data text is escaped, brand fonts are not.
- **Parameter workbook rebuilt on tomlkit:** `sheet_to_config.py --write` used
  to re-serialise `config.toml` with tomli-w, deleting every inline comment,
  and read lists back as strings; `config_to_sheet.py` exported only a fixed
  list of `[STAGE_*]` blocks (nothing after a reshape) with blank unit and
  justification columns. Now the export takes every non-machinery table plus
  the `[[data]]` filters, with Unit and Description parsed from the inline
  comments and a README sheet (its model summary, `ABOUT`, is a
  `<PLACEHOLDER>` for setup). The import sets only the changed values in
  place, so comments and every other line survive byte for byte, reads lists
  as TOML literals, refuses unknown rows or unreadable values, and restores
  the original if the edited file fails to load. `tests/test_param_sheet.py`
  covers the round trip and proves the shipped config exports whole.
  Dependency: tomli-w → tomlkit.
- **Extract AOI from config, not a role:** `resolve_aoi` fell back to the
  example's `candidates` role, and a machinery test required that role, so
  renaming roles broke machinery. The fallback is now `[library].aoi_layer`
  (set to `CandidateSites` here); with no `--aoi`, `--aoi-layer` or
  `aoi_layer` the extract refuses.
- **Format gate green again:** four files failed `ruff format --check` with
  the locked ruff (0.15.20), and the pre-commit hook pinned ruff v0.6.9, which
  formats differently. Files reformatted; the hook now pins the locked
  version.
- **Pulling these into a project:** take `src/datalib.py`,
  `src/reporting/render.py`, both workbook scripts and
  `tests/test_param_sheet.py`, plus the `Library.aoi_layer` field from
  `src/config.py` (merge by hand if you changed `VALID_ROLES` or the stage
  keys); add `|safe` to brand values inside `<style>` in your own templates;
  in `pyproject.toml` swap `tomli-w` for `tomlkit>=0.13` and run `uv lock`;
  set `[library].aoi_layer`; write `ABOUT`; set the pre-commit ruff `rev` to
  the version in `uv.lock`.

Machinery from P05841:

- **Raster inputs in config:** any extra `[paths]` key (a DEM, a flow
  direction grid) is resolved like the core paths, including
  `PROJECT_DATA_ROOT`, and read with `cfg.paths.require("dem")`, which names
  a missing key. `[dev.paths]` may twin any key the base `[paths]` defines,
  and nothing else. Before, a raster input meant editing `src/config.py`.
- **`raster.write_array`:** writes a 2-D array as a single-band GeoTIFF
  (DEFLATE, tiled, CRS set, parent dirs created), the write-side companion of
  the windowed readers. `check_memory`'s docstring now says it guards the file
  read, not an analysis's working set: per-cell arrays (receivers,
  accumulators) can need 10–80 bytes a cell against the file's one.
- **A missing input is one line, exit 2:** `utils.read_layer` raises
  `FileNotFoundError` naming the file instead of a GDAL traceback, and
  `main.py` (and the reset's single-flow stub) print `Input error: ...` and
  exit 2, as config errors already did; `--debug` still shows the traceback.
  It is the usual first error after swapping the sample for real data.
- **`reset_pipeline.py`:** refuses to run on a configured project (the
  SessionStart / Deep checks detector: no `<PLACEHOLDER` in `CLAUDE.md`, no
  `P00000` in the config), where it would overwrite the real method with
  stubs; `--allow-configured` overrides. `/new-project` and
  `TEMPLATE_SETUP.md` now run the reset before the identity edits. Single-flow
  mode also removes `src/pipeline/__pycache__`, so the emptied package
  directory really goes, and the post-reset TODO lists the `new-report`
  skill's pointer to the example's report model and `[library].aoi_layer`.
  New `tests/test_reset_pipeline.py`.
- **Pulling these into a project:** take `src/raster.py` and `src/utils.py`;
  merge the `Paths.extra` / `require` / `_check_dev_overlay` changes into
  `src/config.py` by hand; add the `FileNotFoundError` handler around your
  flow or stage call in `main.py`. The reset script is for the template only.

Skills, data and docs from P05841:

- **`whitebox-hydrology` rewritten for whitebox-workflows 2.x** (the locked
  2.0.6): tools are called as `wbe.hydrology.<tool>(**kwargs)` (flat calls
  raise, positional arguments too); `write_raster` takes
  `options={"compress": True}`; `d8_flow_accum` `out_type` is
  `cells|ca|sca` and quietly turns an unknown value into `ca`; `d8_pointer`
  takes `esri_pntr=True`; accumulating a pointer re-read from a uint8 or
  int16 file saturates at 255 or 32,767 without a warning. One-off tools run
  with `uv run --group hydro` (the SessionStart `uv sync --frozen` removes a
  one-off group install). The documented snippet was run against 2.0.6.
- **Data catalogue:** nine Auckland Council / Watercare public ArcGIS layers
  (stormwater catchments, permanent streams, stormwater pipes and treatment
  facilities, council septic tank assets, local wastewater pipes, Watercare
  wastewater area of service and local catchments, the Unitary Plan Rural
  Urban Boundary), each checked with `datalib describe`, plus a note on LINZ
  elevation published as Cloud Optimised GeoTIFFs in the public
  `s3://nz-elevation` bucket. `datalib list` now sizes its key column to the
  longest key (keys over 20 characters broke the alignment).
- **Tips:** seven P05841 entries in `docs/tips-and-tricks.md` — grid
  alignment vs mass balance, memory budgets for working sets, Whitebox 2.x,
  imposing network directions on reach cells, ArcGIS `maxRecordCount`
  paging, reading a D8 grid's alignment off its flow paths, and one numpy
  routing engine for cells and reaches.
- **A real pilot subset as dev data:** allowed with the client's agreement, a
  private repo and personal fields stripped. `CLAUDE.md`, the CI data-guard
  comments, `docs/git-workflow.md`, `data/inputs-dev/README.md` and
  `/new-project` say so, and `reset_pipeline.py` no longer regenerates the
  synthetic sample when `data/inputs-dev/` already holds project data.
- **`/new-project`:** a front-loaded brief path (infer the answers, record
  them as assumptions in the brief, confirm once at the end; the prune still
  needs an explicit yes); the version stamp when the changelog's top entry
  is `Unreleased` (`template-v1.1+unreleased (forked <date>, initial commit
  <sha>)`), with `template-sync` PULL diffing from that initial commit.
- **Python blueprint:** a real prune list (the reset script and its test, the
  reset-seam job, `TEMPLATE_SETUP.md`, the other blueprints unless a web app
  is still possible, the sample machinery when the dev data is a pilot
  subset) and a README skeleton; `/new-project` Step 7 already pointed at
  both.

- **Per-project container path:** the project is mounted at
  `/workspace/<compose project name>` instead of `/workspace`. Claude Code
  files session history by working-directory path, so on a shared login volume
  every project's history was landing in one folder (`claude --continue` could
  resume another project's conversation). `verify-sandbox.sh` checks it.
  Existing history under the old path is simply no longer picked up.
- **template-sync works with the read-only sandbox:** PULL fetches straight into
  `refs/remotes/template/main` (no `git remote add`, which writes the now
  read-only `.git/config`). The template's test gate runs in its own venv
  (`UV_PROJECT_ENVIRONMENT=.venv`) so it can't overwrite the project's. The skill
  also names where to run it (a cloud session with both repos). Where the
  template can't be reached, `capture-tip` / `template-sync` leave a
  `template-candidate:` line in the commit so a later session finds them.
- **Pulling this release into an existing project** (via `template-sync`, from
  a cloud session or the host):
  1. Take `docker/` and `.dockerignore` whole.
  2. Take `src/config.py`, `main.py`, `src/datalib.py` and `src/db.py`.
  3. Move the paths from `config.dev.toml` into `[dev.project]` / `[dev.paths]`
     tables in `config.toml`, then delete the three variant files.
  4. In `pyproject.toml`, rename `[project.optional-dependencies]` to groups
     under `[dependency-groups]`, add `[tool.uv] default-groups` with the stacks
     the project uses, then run `uv lock`.
  5. Rebuild (`--build`) and run `./docker/verify-sandbox.sh`.
- **Box close-out:** `./docker/start-box.sh --close-out` stops the Remote
  Control server and removes the project's containers, network and
  venv/uv-cache volumes, then prints a checklist of what's left for a manual
  decision (data, `.env` keys incl. `GH_TOKEN`, session worktrees, the login
  volume). It deliberately deletes no data, secrets or logins.
- **One config, no variants:** `config.dev.toml`, `config.docker.toml` and
  `config.dev.docker.toml` are gone. `--dev` applies a `[dev]` overlay inside
  `config.toml` that may only set `[dev.paths]` and `[dev.project]`
  name/client — the loader rejects anything else, replacing the old
  "keep four files in lockstep" test. `--dev` now combines with `--config`.
  `PROJECT_DATA_ROOT` (env) anchors relative data paths, so sessions in git
  worktrees read the main checkout's data.
- **Optional stacks declared once:** the extras are now dependency groups,
  switched on per project in `[tool.uv] default-groups` (`pyproject.toml`).
  Cloud sessions, the container, CI and local runs all read that one line —
  no Dockerfile or CI edit to add a stack (`uv sync --extra X` →
  add `"X"` to `default-groups`).
- **One container image:** `docker/Dockerfile` now serves both `claude` and
  `pipeline` (`Dockerfile.claude` removed). It holds no code or packages:
  the project is mounted and packages sync into a per-project `/opt/venv`
  volume, so code and dependency changes never touch Docker. The pipeline
  service now runs non-root, behind the same fence, with read-only inputs.
  `run.sh` / `run.ps1` pass every argument straight to `main.py` (PowerShell
  users: `--dev`, not `-Dev`; `--sample` → `--dev --make-sample`).
- **Remote Control compute box:** `docker/start-box.sh` runs the container as
  an always-on `claude remote-control` server (tmux, auto-restart, git
  worktree per session, `auto` permission mode) on a spare Linux PC, driven
  from claude.ai/code or the Claude app. `--profile` gives each person on a
  shared box their own container, venv and login volume; `--mem`/`--cpus`
  cap it. A fine-grained `GH_TOKEN` in `.env` lets Claude push. Runbook:
  `docs/remote-control-box.md`.
- **Sandbox security audit + hardening** (details in the runbook's
  "Security model"): `docker/`, `.git/hooks`, `.git/config` and
  `.claude/settings.json` are read-only in the container (the agent could
  previously rewrite its own sandbox or plant git hooks the host would run);
  the fence is atomic, ignores signals and deletes its own sudo grant (it
  could previously be re-run and interrupted mid-flush); the Docker host is
  dropped and Docker networks are open on tcp/5432 only; unused setuid bits
  stripped; pids limit; IPv6 fence failure fatal when IPv6 is present; login
  volume selectable per person/project (`CLAUDE_CONFIG_VOLUME`). **Bug fix:**
  the image lacked `iproute2`, so the old fence silently allowed no Docker
  network and the shared PostGIS was unreachable. `docker/verify-sandbox.sh`
  proves the posture (22 checks) and runs in a new Deep checks `sandbox` job.
  Claude Code pin → 2.1.267.

- **CI slimmed to a hygiene gate:** push/PR CI (`ci.yml`) now runs only
  seconds-fast plain-shell guards — no secret-shaped files tracked (`.env`,
  keys, certs, mirroring the `.gitignore` secrets block), nothing under
  `data/` beyond the dev sample, no >10 MB blobs, and a probe that the
  `.gitignore` secret rules still fire. The heavyweight lint/test/smoke-run
  and `reset-seam` jobs moved unchanged to `deep-checks.yml`, **manual-only**
  (Actions → "Deep checks") — they were adding minutes to every merge. Lint
  and tests are run locally/by Claude before pushing
  (`ruff check . && uv run pytest -q`).
- **Herdr in the Claude container:** the sandboxed dev image now bakes in
  [Herdr](https://herdr.dev) (pinned, checksum-verified), a terminal
  multiplexer for coding agents. `./docker/start-herdr.sh` /
  `.\docker\start-herdr.ps1` open it in the same container/sandbox as
  `start-claude` (which gained the underlying `--herdr` / `-Herdr` mode) and
  idempotently preset, on the shared config volume: the Claude↔Herdr
  integration (pane restore after restarts) and the herdr agent skill
  (printed by the pinned binary itself, so skill and binary never drift) —
  Claude inside a Herdr pane can split panes, spawn helper agents and read
  their output; the skill self-guards on `HERDR_ENV=1` and stays dormant in
  plain sessions.
- **Project archetypes (`docs/blueprints/`):** the template now explicitly
  supports more than the Python pipeline. Machinery is split into a
  stack-agnostic **core** (security posture, memory, skills, brand, data
  governance, container) and per-archetype **stack machinery**; non-Python
  archetypes — web app (ArcGIS Maps SDK for JS) and hybrid — are defined as
  prescriptive *text blueprints* that `/new-project` scaffolds from at setup,
  deliberately not pre-built folder trees. The interview now confirms the
  archetype as its first grilling question (inferred from the brief), and
  gained a final **Finalise & prune** step: confirmed deletion of unused
  template machinery from the blueprint's prune list, README/CLAUDE.md
  rewritten from blueprint skeletons, deferred items tracked in
  `references/post-setup-TODO.md` with a SessionStart nag until worked off.
  `design-guidelines.md` scopes its shape section to the Python archetype
  (the always-on intents are stack-agnostic and restated per blueprint).
- **Clean landing root:** the repo root now holds five files (`README.md`,
  `CLAUDE.md`, `main.py`, `pyproject.toml`, `uv.lock`) plus dotfiles whose
  tools pin them there. All container machinery moved to `docker/`
  (Dockerfiles, `docker-compose.yml`, `run.*`, `start-claude.*`,
  `init-firewall.sh`, `shared-postgis/`); `GETTING_STARTED.md`,
  `TEMPLATE_SETUP.md` and this changelog moved to `docs/`. The start command
  is now `.\docker\start-claude.ps1` / `./docker/start-claude.sh`; wrappers
  anchor themselves to the project root, so they work from any cwd. The
  compose file gained an explicit top-level `name:` (with the file inside
  `docker/` the derived default would be "docker" for every project) —
  renaming it per project is a new TEMPLATE_SETUP step-2 item. Direct compose
  use is `docker compose -f docker/docker-compose.yml ...`.
- **New `humanizer` skill** (`.claude/skills/humanizer/`): edits prose —
  report text, docs, client-facing writing — to remove AI-generated-writing
  tells and read naturally. Vendored from the MIT-licensed skill based on
  Wikipedia's "Signs of AI writing" guide (LICENSE included alongside).

## template-v1.1 — 2026-08-09

Fixes and capabilities from the first end-to-end project test (P09999
culvert screening, forked at template-v1.0, reshaped to a single flow):

- **Data hygiene:** four `.gitignore` rules were dead — git has no inline
  comments, so `layer_map.json`, `data/library/*`, `config/*.xlsx` and
  `!docs/**/*.pdf` matched nothing; real client-data extracts would have been
  committed. Fixed, with a regression test. `.gitattributes` now forces LF on
  every text file (`* text=auto eol=lf`) so Windows clones keep
  `git checkout -- .` usable as the undo.
- **Seam fixes:** machinery tests decoupled from the worked example — the
  reporting machinery test renders its own fixture template, and role
  requirements moved from `config._validate` into the flow module
  (`_validate_sources` pattern). `docs/template-anatomy.md` marks the
  remaining example-coupled tests `Machinery*` with exactly what to touch.
- **Single flow is now the reset default:** `reset_pipeline.py --flow
  single|stages` — single-flow mode emits one `src/flow.py` and a stage-less
  `main.py`; the post-reset TODO names every stage-threaded file. The CI
  reset-seam job is gated on the unconfigured-template detector (it used to
  destroy a configured project's tree) and runs both shapes.
- **New `geoparquet_dataset` source** (`src/datalib.py`): hive-partitioned
  hosted GeoParquet (e.g. Overture Maps) read through DuckDB with the AOI
  pushed into the parquet scan — real AOI preflight counts, memory scales
  with the AOI, never the dataset. Overture buildings + land use catalogued
  (release pinned).
- **PDF export works in the Claude container:** `Dockerfile.claude` bundles
  Chromium's OS libraries; launch failures collapse to one actionable
  warning line (still never fatal).

## template-v1.0 — 2026-08-08

First versioned release. Everything to date, including:

- Guided `/new-project` interview (grilling-driven), auto-launched by
  `start-claude` on an unconfigured clone; robust two-signal detector.
- Containerised Claude Code with egress fence (`init-firewall.sh`), shared
  login volume, optional shared PostGIS; network-share clone guard.
- Three-stage worked example (opportunity screening) with a machine-enforced
  machinery/example seam and `scripts/reset_pipeline.py` blank-to-stub reset.
- Data library: governed LINZ/AGOL extracts (`get-data`), DuckDB SQL layer
  (`duckdb` skill), catalogue of authoritative sources.
- Two-tier project memory (`remember`): auto-loaded brief + decision log.
- Brand system: Morphum palette/logos/design-system foundation, client
  overrides, brand-themed Mermaid diagrams, editable self-contained reports.
- Skills: new-project, grilling, remember, capture-tip, template-sync,
  get-data, duckdb, run-sample, agol-connect, new-report, morphum-mermaid,
  morphum-design, sync-parameters, geospatial-conventions, whitebox-hydrology.
- CI: ruff + tests + sample smoke run + reset-seam job; config-variant
  lockstep enforced by test; uv-only dependency management.
