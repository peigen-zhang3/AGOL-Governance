# Getting started (first time? start here)

From zero to Claude working on a new project in three steps.

```
1. Create the repo       GitHub: "Use this template" → P0XXXX-<short-name> (private)
2. Open Claude Code      claude.ai/code → new cloud session on that repo
                         (or `claude` in a local clone, while no client data is there)
3. Run /new-project      Claude interviews you and builds the project from playbook modules
```

## 0. Prerequisites (once)
- A seat on the **Morphum Team** Claude plan, signed in. The team plugins
  (`morphum`, `morphum-dev`) load automatically: check Customize → Plugins,
  or `/plugin` in Claude Code.
- Claude Code **2.1.273 or later** if you run it locally (`claude --version`).
- GitHub org access (the Claude GitHub App covers cloud sessions; no
  personal token needed).

## 1. Create the repo
On GitHub: **Use this template** → name it `P0XXXX-<short-name>` (the Accelo
job code), private.

## 2. Open Claude Code
- **Cloud session (default):** claude.ai/code → new session → pick the repo.
  Right for building and for everything on sample or pilot data.
- **Local:** clone it and run `claude` in the folder. Fine for setup, but
  **never with real client data on that machine**: for that, the project
  adds the container module first (step 3), and you work inside it.

The SessionStart hook sees the unconfigured template and offers
`/new-project`.

## 3. The setup interview
`/new-project` asks about the project, confirms the archetype (Python
pipeline today; web and hybrid from blueprints), asks **where it will run**,
and has the playbook librarian add a starter and the modules the brief needs.
It then applies the project code, name and client and finishes with a green
run. If the team plugins are missing it stops and says so.

### Where it runs
| Situation | What setup adds |
|---|---|
| Sample or pilot data, cloud sessions | nothing extra |
| Real client data on a local machine | `environment/claude-container`: the fenced Docker container (no LAN, read-only cage). Its guide is `docs/container.md` |
| Regional-scale runs | the same module, run on the shared Remote Control box (`docs/remote-control-box.md`) |

Running out of memory is **not** a reason to add the container: it gets the
host's RAM or less. Fix the reads first (windowed I/O), then move the run to
the box. The playbook's `standards/where-to-run.md` has the full table.

## Day-to-day
- **Real data in:** list it in the starter's sources (files go in
  `data/inputs/`, git-ignored; AGOL, S3 and the network share are read in
  place). A pilot a cloud session must keep can be tracked in the opt-in
  `data/tracked/` (rules in `data/README.md`). Claude inspects data summaries-first.
- **Memory:** decisions and quirks go to the project brief and decision log
  (`remember`, proactive).
- **Lessons for the team:** `capture` → `references/playbook-candidates.md`,
  harvested weekly.
- **Module updates:** a session-start notice says when a module is behind;
  say "update <module>" or "glow-up" and Claude briefs you first.
- **Pilot first:** the Python starter runs a pilot scope of the real sources
  by default (`data/outputs/pilot/`); `--scope full` is the deliverable
  (`data/outputs/full/`), and `--run NAME` keeps a review variant apart. Each
  run writes a `run.json`.
- **Git:** branch, PR with a review tier ticked (`git-workflow.md`).

## Troubleshooting
| Symptom | Fix |
|---|---|
| `/new-project` says the plugins aren't loaded | Sign in with the Morphum Team account; update Claude Code to ≥ 2.1.273; check Customize → Plugins. Ask Danny if they're missing for everyone (org sync). |
| No "morphum module update" notice but `references/modules.lock` exists | Claude runs the check itself on the first turn (CLAUDE.md fallback); or ask "check module updates". |
| A cloud session runs out of memory or disk | It's a development surface: use a smaller pilot scope, fix the reads, or run on the box. |
