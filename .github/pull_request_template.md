# Summary

<!-- What does this change and why? One or two sentences. Link the issue. -->

## Changes

<!-- Bullet the substantive changes. Small PRs review better. -->

-

## Review tier

Tick one (see `docs/git-workflow.md`):

- [ ] **Self-merge**: docs, tips, internal or small work
- [ ] **Review recommended**: project code that affects deliverables
- [ ] **Review expected**: template release, deliverable tag, `docker/`, `.claude/`, CI

**Reviewer:** <!-- GitHub login, or "none (self-merge)" -->

## Testing

<!-- Paste the commands you actually ran. -->

- [ ] Each installed module's checks pass (Python: `uv run ruff check .`, `uv run pytest -q`, `uv run python main.py`)
- [ ] UI change: before-and-after screenshots attached

## Checklist

- [ ] No secrets, real client data, or large binaries committed — checked the diff yourself; no scanner runs
- [ ] Real data in `data/tracked/`? The client agreed, `data/tracked/README.md` lists every file, and the decision is logged
- [ ] New or changed parameters are in config **and** justified in the parameter docs
- [ ] Changed anything under `docker/` (container module)? Ran `./docker/verify-sandbox.sh` (or the manual Sandbox workflow)
- [ ] Module added, updated or skipped? `references/modules.lock`, `.modules/` and the decision log are in this PR
- [ ] Lesson for other projects? Written client-free to `references/playbook-candidates.md` with a `playbook-candidate:` trailer
- [ ] Docs / CLAUDE.md updated if behaviour or conventions changed
