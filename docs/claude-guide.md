# Working with Claude Code in this template

How the Claude-specific pieces fit together, and how to extend them.

## Files
| Path | Purpose | Committed? |
|------|---------|-----------|
| `CLAUDE.md` | Project memory, loaded in full every session. Vanilla < 120 lines; < 200 with module blocks. | yes |
| `.claude/settings.json` | Team-shared: permissions, sandbox, SessionStart hooks. | yes |
| `.claude/settings.local.json` | Personal overrides (extra permissions, model). | no (git-ignored) |
| `.claude/skills/<name>/SKILL.md` | Project skills: the four core ones, plus any a module installs. | yes |
| `references/modules.lock`, `.modules/` | Installed playbook modules and their untouched originals. | yes |

## Skills
**Core (this repo):**

| Skill | Use |
|-------|-----|
| `new-project` | Guided setup: interview, archetype, starter + modules via the librarian, identity, verify. |
| `remember` | Project memory (brief + decision log); flags playbook candidates; records module changes. |
| `capture` | Tips, gotchas, prompts, data sources → client-free `references/playbook-candidates.md`. |
| `template-sync` | Pull vanilla-core improvements from the template. |

**Live (team plugins, after sign-in with the Morphum Team account):**

| Plugin | Skills |
|--------|--------|
| `morphum` | `team-knowledge`, `grilling`, `humanizer` |
| `morphum-dev` | `librarian`, `data-catalogue`, `harvest`, `geospatial-conventions` |

**From modules** (installed into `.claude/skills/` by the librarian): for
example the Python starter brings `get-data`, `duckdb`, `agol-connect`,
`run-pilot`, `new-report`, `sync-parameters`; design-tokens brings
`morphum-design` and `morphum-mermaid`.

Check what's loaded with `/plugin` (plugins) and `/skills`. If the team
plugins are missing, sign in with the Morphum Team account on Claude Code ≥
2.1.273.

## How skills work (quick primer)
- A skill is a folder with a `SKILL.md` (YAML frontmatter + markdown). The
  folder name is the `/command`; plugin skills are namespaced
  (`morphum-dev:librarian`).
- `description` is how Claude decides when to load it: key use case first.
  `paths:` auto-activates a reference skill for matching files.
- Supporting files load only when the SKILL.md points to them.

## Extending
- **A repeatable procedure for this project only?** A project skill.
- **Useful to other projects?** A playbook candidate (`capture`), not a copy
  in the template.
- **A new hard rule?** One line in `CLAUDE.md` (`IMPORTANT:` / `YOU MUST`
  for rules that bite).

## The hooks
`.claude/settings.json` SessionStart, all `|| true`-guarded:
1. Exports `PYTHONPATH`; runs `uv sync --frozen` only when `pyproject.toml`
   exists.
2. Detects an **unconfigured template** (`<PLACEHOLDER` in `CLAUDE.md`, or
   `P00000` in `config/config.toml` once the Python starter is in) and
   offers `/new-project`. Mirrored in the container module's
   `docker/start-claude.sh` and `.ps1`.
3. Nags while `references/post-setup-TODO.md` exists.
4. Injects the first ~6 KB of `references/project-brief.md`.

The `morphum-dev` plugin adds one more: the **module update notice**
(`modules.py check`, read-only, no network). If it doesn't appear on some
surface, CLAUDE.md tells Claude to run the check on the first turn.
