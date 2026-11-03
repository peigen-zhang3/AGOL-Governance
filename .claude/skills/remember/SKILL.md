---
name: remember
description: Capture project memory — key decisions, resolved issues and workarounds, direction changes, data quirks, module adds and updates — into the living project brief and the append-only decision log, and flag the ones other projects could use as playbook candidates. Use when the user says "remember this", "log this decision", "note that for later"; and PROACTIVELY, without being asked, whenever a significant decision is made or revised, a gnarly issue gets resolved, an assumption is invalidated, or a module is added, updated or skipped.
allowed-tools: Read Edit Write Grep Glob
---

# Remember (project memory)

Two tiers, two jobs. Get the routing right and future sessions start smart.

| File | Job | Discipline |
|------|-----|-----------|
| `references/project-brief.md` | **Current state.** Auto-loaded into every session by the SessionStart hook. | Rewritten in place. Never append history. Cap ~1 page. |
| `references/decision-log.md` | **History.** The audit trail; read when someone asks "why". | Append-only, newest first, dated. Supersession recorded here. |

A revised decision touches **both**: the brief's bullet is *replaced*, and a
log entry records the change and what it supersedes.

## Brief format (create on first use if missing)

```markdown
# Project brief — <code> <short name>
_Current state only. Maintained via the `remember` skill; loaded automatically
each session. History lives in decision-log.md._

**Client:** <client> · **Accelo job code:** <P0XXXX> · **Template version:** <from docs/CHANGELOG.md at setup>
**Modules:** <name version, … from references/modules.lock>

## What we're building
<2–4 sentences: deliverable, client, method shape.>

## Decisions as they stand
- <decision> — <one-line why> (<yyyy-mm-dd>)

## Data notes & quirks
- <source/layer>: <the thing that will bite someone who doesn't know it>

## Workarounds in effect
- <workaround> — <root cause, and when it can be removed>

## Open risks / questions
- <risk> — <what would resolve it>
```

Keep the **Modules** line current: the harvest reads it.

## Log entry format (prepend under the header)

```markdown
## <yyyy-mm-dd> — <short title>
**What:** <the decision / resolution / change>
**Why:** <context that made it the right call>
**Supersedes:** <date + title of the entry it replaces, if any>
**Playbook:** candidate | no
```

## Playbook candidates
Mark `**Playbook:** candidate` when the entry would help another project (a
method choice that generalises, a data source behaviour, a tool quirk). Then:
1. Write a **client-free** version to `references/playbook-candidates.md`
   (format in that file): the lesson, no client names, people, places tied to
   the client, or record values. Point back to the log entry by date and
   title. **Never copy the log entry itself.**
2. Commit with a trailer line: `playbook-candidate: <one line>`.

The weekly harvest reads only that file and those trailers.

## Modules
Record every module add, update (with merge choice and conflicts) and skip
(with the reason) as a log entry, and update the brief's Modules line.

## Rules
- **Proactive capture is the point.** Trigger yourself on decisions (made or
  reversed), resolved bugs, data quirks, client instructions that change
  direction, invalidated assumptions, module changes. Don't ask; do it and
  mention it in one line.
- **Non-code layer only.** Code rationale lives in commits and comments.
- **Use real dates.** **Never store secrets.**
- Tips and gotchas (not decisions) go through `capture`.
- At a natural session close, scan for anything decided but not captured.
