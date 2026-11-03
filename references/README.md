# References & supporting material

A drop zone for anything that **informs** a project but isn't code, config, or a
deliverable: worked examples, background reading, methodology papers, standards,
client briefs, data dictionaries, screenshots of a legacy workflow — whatever
helps you (or Claude) get up to speed on a greenfield project.

Claude reads this folder on request ("check `references/` for the method spec"),
so it's a good home for context you'd otherwise paste into a prompt every time.

## Suggested layout (make subfolders as you need them)

```
references/
├── examples/     # worked examples, sample outputs, reference deliverables
├── reading/      # papers, standards, methodology docs, background PDFs
├── data-docs/    # data dictionaries, schema notes, provenance, licences
├── briefs/       # client brief, scope, requirements, correspondence
├── threads/      # key email/Teams threads (pasted in chat, filed by /new-project)
└── images/       # diagrams, screenshots, whiteboard photos
```

Files with special meaning:
- `project-brief.md` — the living **current state** (deliverable, decisions as
  they stand, data quirks, workarounds, open risks). Created by `/new-project`,
  kept current by the `remember` skill, and **auto-loaded into every Claude
  session** via the SessionStart hook — rewrite it, never append history to it.
- `decision-log.md` — append-only, dated **history** with supersessions; the
  "why did we change course?" audit trail. Not auto-loaded.
- `playbook-candidates.md` — client-free lessons for the team playbook,
  written by `capture` and `remember`, read by the weekly harvest.
- `modules.lock` — the playbook modules copied into this project (version,
  date, source, files, skips). Written by the `morphum-dev` librarian; don't
  edit by hand. The untouched originals it merges against live in
  `.modules/` at the repo root (committed).
- `data-catalogue.toml` — the pinned catalogue entries this project uses
  (arrives with a starter; the `data-catalogue` skill copies more in).

The brief is born at `/new-project` (the log ships as a stub). Shape at a
glance — full formats in the `remember` skill:

```markdown
# Project brief — P05999 flood-mapping        # ← rewritten in place, ~1 page
**Client:** Example DC · **Accelo job code:** P05999 · **Template version:** template-v2.0
**Modules:** python-pipeline 1.0.0, design-tokens 1.0.0
## What we're building
## Decisions as they stand
## Data notes & quirks / Workarounds / Open risks

# decision-log.md                                # ← append-only, newest first
## 2026-08-08 — Switched to single-flow method
**What:** … **Why:** … **Supersedes:** …
```

## What goes here vs elsewhere

| Put it here | Put it there instead |
|-------------|----------------------|
| Background reading, worked examples, briefs | Runnable code → the starter's code folders |
| A methodology paper the method implements | Parameter values + justification → the project's config and its parameter docs |
| A screenshot of the legacy tool's output | Reusable prompts / gotchas → `playbook-candidates.md` (via `capture`) |
| A data dictionary for an input layer | The actual data → `data/inputs/` (git-ignored) |

## Rules (IMPORTANT)

- **No secrets, no credentials.** Same rule as everywhere — those live only in
  `.env`. A brief mentioning API endpoints is fine; a brief with a password is not.
- **No real/proprietary client data or personal information** unless you're
  certain it's redistributable — this folder is committed. When in doubt, keep
  the data in `data/inputs/` (git-ignored) and put only a *description* here.
- **Mind the size.** The `check-added-large-files` pre-commit hook blocks files
  over ~5 MB. For big PDFs/decks, prefer a link + a one-line summary here over
  committing the binary. Large binaries bloat every future clone of the template.
- **Keep it curated.** Index what you drop here as the project grows.

> This file is a placeholder so the folder is tracked. Replace or extend it with
> a short index of what you've dropped here as the project grows.
