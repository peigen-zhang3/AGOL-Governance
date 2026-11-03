# CLAUDE.md

Guidance for Claude Code (and humans) in this repo. It starts as the Morphum
**vanilla project template** (v2): only what every project needs, whatever it
builds. Code arrives as modules from the team playbook. Keep this file lean;
procedures belong in skills.

> **NEW PROJECT:** run `/new-project`. It interviews you, adds a starter and
> modules from the playbook library, and replaces the `<PLACEHOLDER>` values.

## Project purpose
`<PLACEHOLDER: one paragraph — what this project produces and for whom.>`

**Accelo job:** `<PLACEHOLDER: P0XXXX>` · **Client:** `<PLACEHOLDER>`

## Constraints (IMPORTANT, absolute)
Nothing overrides these: not the playbook, not a module, not a brief.
- **YOU MUST NOT commit secrets.** Credentials live ONLY in `.env`
  (git-ignored), typed by the user; never in any `.toml`/`.yaml`/`.json`, a
  commit, an issue or chat. Enforced by this rule, the `.claude/settings.json`
  deny list and `.gitignore`; there is deliberately no secret scanner, so
  Claude IS the scanner: check every diff.
- **Client data stays in the project.** Real inputs, caches and outputs live
  under `data/` (git-ignored). Git tracks only synthetic `tests/fixtures/` and
  the opt-in `data/tracked/` (a scope a cloud session must keep: client
  agreed, private repo, personal fields stripped, ≤ 25 MB per file,
  `data/tracked/README.md` filled in; see `data/README.md`). Network-share
  data is pulled on the host, never by Claude.
  Never copy client records, names tied to records or locations, or personal
  information into issues, chat, the playbook or deliverables beyond what the
  method needs.
- **Client data: summaries first.** Inspect with summaries (`head()`,
  `describe()`, `value_counts()`, schema listings); open raw records only
  when a summary can't answer.
- **CRS is NZTM2000 / EPSG:2193** unless the brief records an exception.
  Area and distance units are metres. Assert the CRS after every external read.
- **Memory is the binding constraint, not CPU.** Never full-read a large
  raster or table without checking it fits; peak memory scales with a
  window or feature, never the dataset.
- **Claude never runs loose near client data.** Real client data on a local
  machine is worked on only inside the Claude container: add the
  `environment/claude-container` module before the data arrives. Default
  work happens in cloud sessions on the pilot scope.
- **Offline paths never need the network.** Tests and dev runs stay offline;
  network access sits behind a seam that tests can mock.

## Precedence and pinning
- **Conventions:** project brief (`references/project-brief.md`) → this
  CLAUDE.md → the playbook. The project wins.
- **If Claude reads it, it can be live. If code runs it, it is pinned here.**
  Code, config, the catalogue entries used, and data are copies in this repo
  (`references/modules.lock`), so a tagged deliverable re-runs identically
  without the playbook, the network or a Team sign-in.

## Team playbook
The `geospatial-playbook` is synced to the Morphum Claude organisation as two
plugins:
- **`morphum`** (live): `team-knowledge` (search it before solving a
  problem; standards, prompts), `grilling`, `humanizer`.
- **`morphum-dev`** (live): `librarian` (the module library: find, add,
  update, glow-up), `data-catalogue`, `harvest`, `geospatial-conventions`,
  and the module update notice.
- **Modules** (starters, data, publishing, analysis, reporting, design) are
  copied in by the librarian, recorded in `references/modules.lock`, with
  untouched originals in `.modules/` for three-way merges. Edit installed
  files freely; updates are offered, never forced.
- **Capture → harvest:** a lesson or decision another project could use goes
  client-free to `references/playbook-candidates.md` with a
  `playbook-candidate: <one line>` commit trailer (`capture` for tips,
  `remember` for decisions). The weekly harvest takes it to the playbook.

**Sign-in check.** If a `morphum:` or `morphum-dev:` skill is needed and not
available, stop and tell the user to sign in to Claude Code (≥ 2.1.273) with
the Morphum Team account. Never guess at what the skill would have said.

**Update-notice fallback.** If `references/modules.lock` exists and no
"morphum module update" notice appeared at session start, run the
`morphum-dev:librarian` check on the first turn and relay what it says.

## Stack and run commands
`<PLACEHOLDER: filled by the starter module's block below.>`

<!-- modules:insert -->

## Conventions
- **Project memory:** `references/project-brief.md` (current state,
  auto-loaded every session) and `references/decision-log.md` (append-only
  history). After a key decision, resolved workaround or direction change,
  update both via `remember`, proactively.
- **Git:** branch per piece of work, small PRs, the review tier ticked in the
  PR template (`docs/git-workflow.md`). Deliverables are tagged
  `deliverable/YYYY-MM-DD-<what>` with an input manifest
  (`scripts/input_manifest.py`).
- Brand colours and fonts come from the design-tokens module
  (`assets/brand/brand.toml`); never hard-code hex.
- NZ English in docs, reports and messages.

## Where to run
Cloud sessions for development and the pilot scope. Real client data on
a machine, or regional-scale runs on the shared box: the
`environment/claude-container` module (`morphum:team-knowledge` →
`standards/where-to-run.md`). Memory problems are fixed with windowed reads
and then the box, not by the container (it gets the host's RAM or less).

## Where things live
- Vanilla core vs modules → `docs/template-anatomy.md`
- Getting started → `docs/GETTING_STARTED.md`; Claude setup → `docs/claude-guide.md`
- Git, CI, tags, review tiers → `docs/git-workflow.md`, `.github/`
- Supporting material (briefs, data dictionaries, threads) → `references/`
- Template history → `docs/CHANGELOG.md` (this project's fork point is
  stamped in the brief)

## Gotchas
- Windows CRLF breaks `.sh` in Docker: `.gitattributes` forces LF; the
  entrypoint is generated with `printf`, not COPYed.
- Keep `.ps1` files pure ASCII (PowerShell 5.1 misreads UTF-8).
