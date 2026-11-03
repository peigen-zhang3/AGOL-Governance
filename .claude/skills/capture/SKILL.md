---
name: capture
description: Capture a reusable tip, trick, gotcha, effective prompt, or data source as a client-free playbook candidate so other projects benefit. Use when the user says "add this to tips", "save this prompt", "note this gotcha", "the team should know this", or after solving a fiddly problem worth recording.
argument-hint: "[short description of the tip]"
allowed-tools: Read Edit Write Grep Glob Bash(git:*)
---

# Capture (tips, gotchas, prompts)

Team knowledge lives in the playbook (`morphum:team-knowledge`), not in the
project. Capture sends it there through the weekly harvest. Decisions go
through `remember`; this skill is for tips, gotchas, prompts and data
sources.

## Steps
1. **Search first**: is it already in `morphum:team-knowledge`
   (`knowledge/index.md`, `prompts/library.md`)? If so, say so; if the
   existing entry is wrong, propose a correction instead.
2. **Write it client-free** at the top of `references/playbook-candidates.md`
   (below the insert marker), in this format:
   ```markdown
   ### <title>  <!-- YYYY-MM-DD, <P0XXXX> -->
   **Kind:** tip | gotcha | prompt | data source | module idea
   **Topic:** arcgis | hydrology | data | container | git-and-files | reports | other
   **Context:** <the problem, generically>
   **Tip:** <the fix, the exact command or snippet>
   **From:** <decision-log entry, if any>
   ```
   No client names, people, addresses, locations tied to the client, record
   values or dataset ids that identify the client. The project code is fine
   (provenance). Use today's real date.
3. **Commit** with a trailer: `playbook-candidate: <one line>`.
4. **Project-specific too?** If the project itself must not forget it, also
   log it with `remember` (the project version can name the client).

## Playbook attached?
In a cloud session with `geospatial-playbook` attached (push), you may open
the playbook PR directly instead of waiting for the harvest: branch
`knowledge/<short-name>`, add the entry to the topic file under its insert
marker, update `knowledge/index.md`, PR to `main` (review expected,
reviewers `daniel-nutsford` and `peigen-zhang3`). Still write the candidate
here with a note "PR opened: <link>" so the harvest skips it.
