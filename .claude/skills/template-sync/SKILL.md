---
name: template-sync
description: Pull vanilla-core improvements from the Morphum project template (Morphum-Environmental/Project-Template) into this project — CLAUDE.md core rules, .claude settings and core skills, .github/, core docs and scripts. Use when the user says "update from the template", "pull template improvements" or "sync with the template". Code modules are not template-sync's job: they update through the morphum-dev librarian.
argument-hint: "[paths...]"
allowed-tools: Read Edit Write Grep Glob Bash(git:*)
---

# Template sync (vanilla core, pull only)

Since v2 the template is only the vanilla core. Code, docs and skills for a
stack come from playbook modules and update through `morphum-dev:librarian`.
Improvements going the other way are playbook candidates (`capture`,
`remember`; a core fix uses a `template-candidate: <one line>` trailer and
the harvest raises it as a template issue).

## Where to run it
A Claude Code cloud session with this project attached is best: `.git/config`
and `.claude/settings.json` are read-only inside the project container.
(`docker/` is the `environment/claude-container` module now: the librarian
updates it.)

## Pull
1. Fetch the template into a ref (no `git remote add`, which writes
   `.git/config`):
   ```bash
   git fetch https://github.com/Morphum-Environmental/Project-Template.git \
     +main:refs/remotes/template/main
   ```
2. See what changed in the core since the fork (the fork's template version
   is in `references/project-brief.md`; `docs/CHANGELOG.md` on the template
   lists each release's migration steps):
   ```bash
   git diff --stat HEAD template/main -- .claude .github .gitignore \
     .gitattributes .env.example .pre-commit-config.yaml \
     docs/GETTING_STARTED.md docs/git-workflow.md docs/claude-guide.md \
     docs/template-anatomy.md scripts/input_manifest.py \
     tests/test_template_structure.py
   ```
3. Take paths one at a time: `git checkout template/main -- <path>`. Merge
   by hand: `CLAUDE.md` (keep the project's purpose, notes and module
   blocks), `.pre-commit-config.yaml` (keep module blocks),
   `.claude/settings.json` (keep project allows), `.env.example` (keep module
   blocks), `references/`.
4. Verify: the project's checks (each module's `check` commands).
5. Commit naming the template version pulled, and log it with `remember`.
