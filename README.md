# Morphum project template (v2, vanilla)

The starting point for every Morphum geospatial project, whatever it builds:
a pipeline, an ETL job, a web app or a static page. It carries only what
every project needs: the CLAUDE.md rules, security settings, hygiene CI, PR
and issue templates, project memory, and four core skills. The code (and,
when needed, the Claude container) comes from the team playbook's module
library, copied in and pinned when the project starts.

> **New here? Read [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md).**

## How it fits together

| Layer | Where | How a project gets it |
|---|---|---|
| Vanilla core | this repo | copied once ("Use this template") |
| Team playbook (live) | [`geospatial-playbook`](https://github.com/Morphum-Environmental/geospatial-playbook), synced to the Claude org as the `morphum` and `morphum-dev` plugins | live in every session: knowledge, standards, prompts, data catalogue, the librarian |
| Modules | the playbook's library: `starters/python-pipeline`, `publishing/agol-schema`, `analysis/whitebox-hydrology`, `design/design-tokens`, … | copied in by the librarian and pinned in `references/modules.lock`; updates are offered, never forced |

**If Claude reads it, it can be live. If code runs it, it is pinned in the
project**, so a tagged deliverable re-runs without the playbook.
[`docs/template-anatomy.md`](docs/template-anatomy.md) maps it all.

## Start a project

1. "Use this template" → a private repo named `P0XXXX-<short-name>` (the
   Accelo job code).
2. Open it in Claude Code signed in with the **Morphum Team** account
   (Claude Code ≥ 2.1.273): normally a cloud session.
3. Run **`/new-project`**. Claude interviews you, picks the archetype, adds
   the starter and modules, applies the identity, and finishes green.

Already have a v1.x project? See the playbook's
`standards/migrating-existing-project.md`.

## Where Claude runs
Cloud sessions by default, on sample or pilot data. When real client data
will sit on a local machine, or a run needs the shared Remote Control box,
setup adds the **`environment/claude-container`** module: the fenced Docker
container (write access to the project only, LAN dropped by a self-tested
firewall, read-only cage, no root after start-up), Herdr, the box scripts and
a shared PostGIS. It's a security fence, not more memory. See
[`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md#where-it-runs).

## What's inside

```
.
├── CLAUDE.md                 # core rules; modules add their blocks
├── README.md
├── .claude/
│   ├── settings.json         # deny list, sandbox, SessionStart hooks
│   └── skills/               # new-project, remember, capture, template-sync
├── .github/                  # ci.yml (hygiene + checks), sandbox.yml, PR/issue templates
├── data/                     # inputs, cache, outputs per scope (git-ignored), tracked (opt-in)
├── docs/                     # GETTING_STARTED, git-workflow, claude-guide,
│                             # template-anatomy, CHANGELOG
├── references/               # brief, decision log, playbook candidates, modules.lock
├── scripts/input_manifest.py # record a deliverable's inputs (sha256), never copy them
└── tests/test_template_structure.py
```

## Keep it improving
Lessons go to the playbook, not into copies of this template: `capture`
(tips) and `remember` (decisions) write client-free playbook candidates, and
the weekly harvest proposes them. Fixes to the core itself: a
`template-candidate:` commit trailer, or a PR here. Release history:
[`docs/CHANGELOG.md`](docs/CHANGELOG.md).
