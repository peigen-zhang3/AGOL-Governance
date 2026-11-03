# Git workflow

Lightweight rules that keep a small-team geospatial repo healthy. Large-file
and hygiene checks are automated; secrets are NOT — there is deliberately no
secret scanner (see CLAUDE.md Constraints: Claude reviews every diff, and the
`.claude/settings.json` deny list + `.gitignore` are the guardrails). This page
is the human part.

## Branching

- `main` is always runnable: every installed module's checks pass (Python:
  `uv run python main.py` on the pilot and `pytest`).
- Branch per piece of work: `feature/<short-name>`, `fix/<short-name>`,
  `docs/<short-name>`. Delete branches after merge.
- Prefer short-lived branches + small PRs over long-running ones — geospatial
  outputs make big merges painful to verify.

## Commits

- Imperative, present-tense subject ≤ 72 chars: *"Add stream-order filter to
  stage 2"*, not *"Added..."* / *"misc fixes"*.
- One logical change per commit. Parameter tuning is its own commit with the
  **justification in the body** (and mirrored to `docs/parameter-dictionary.md`).
- Never commit: `.env`, anything under `data/inputs/`, `data/cache/`, `data/outputs/`,
  generated reports, or rasters (outside the opt-in `data/tracked/`). `.gitignore` + the pre-commit large-file guard
  enforce the data rules — don't fight them with `git add -f`. Secrets have no
  automated net: check the diff yourself (and Claude checks every diff it writes).

## Pre-commit hooks (install once per clone)

```bash
pre-commit install        # Python starter: uv run pre-commit install
```

Runs a large-file guard (accidental rasters), whitespace and merge-marker
checks, and TOML/YAML checks on every commit; modules add their own (the
Python starter adds ruff). `pre-commit run -a` runs them across the whole tree.
There are deliberately no secret-scanning hooks (flaky baselines — see
`.pre-commit-config.yaml`); the never-commit-secrets rule lives in CLAUDE.md.

## Pull requests

- Tick a **review tier** in the PR template (GitHub Free: process, not
  enforcement):
  - *Self-merge*: docs, tips, internal or small work.
  - *Review recommended*: project code that affects deliverables.
  - *Review expected*: template releases, deliverable tags, `docker/`,
    `.claude/`, CI, and every playbook PR.
- CI (`.github/workflows/ci.yml`) must be green:
  - **hygiene** (seconds): no secret-shaped files tracked, nothing under
    `data/` beyond the dev data, no >10 MB blobs, the `.gitignore` secret
    rules still firing, and the stdlib structure test;
  - **checks** (only when `pyproject.toml` exists): `uv sync --frozen`,
    `ruff check .`, `pytest`. Before v2 lint and tests were local-only; the
    core has no Python now, so the job is free on the template and a real
    gate for every Python project.
- `docker/` changes (container module): run the manual **Sandbox** workflow
  (Actions tab) or `./docker/verify-sandbox.sh`. No secret-*content* scanner anywhere: that
  removal is deliberate (see `ci.yml`).
- Fill in the PR template: the tier, the reviewer, and the checkboxes
  reviewers can't infer from the diff.
- Screenshots of report or UI changes help: reviewers shouldn't have to run
  the code to see a styling change.

## Repo hygiene

- Tracked data lives in exactly two places (`data/README.md`): synthetic
  test data (`tests/fixtures/`) and the opt-in `data/tracked/` for a scope a
  cloud session must keep (client agreed, private repo, personal fields
  stripped, ≤ 25 MB per file and 250 MB in total, a filled-in
  `data/tracked/README.md`). CI enforces both; anything
  else under `data/` fails the hygiene job. Never `git add -f` around it.
- If a secret ever lands in history: rotate it immediately, then rewrite
  history (`git filter-repo`) — deleting the file in a new commit is not enough.
- Tags for delivered milestones: `deliverable/YYYY-MM-DD-<what>` (review
  expected) so a deliverable can always be reproduced from the exact commit.
  Real inputs aren't committed, so record them first:
  ```bash
  python3 scripts/input_manifest.py deliverable/YYYY-MM-DD-<what>
  git add deliverables/ && git commit -m "Record inputs for <what>"
  git tag deliverable/YYYY-MM-DD-<what>
  ```
  `deliverables/<tag>/inputs.json` holds each input's path, sha256, size and
  modified time (`data/inputs/` and the source cache `data/cache/`);
  nothing is copied. The modules and catalogue entries the run
  used are already pinned (`references/modules.lock`).
- On the **template repo itself**: tag releases `template-vX.Y` and record them
  in `docs/CHANGELOG.md`. Projects stamp their fork version into the project
  brief at setup, which gives `template-sync` pulls a known baseline.
- Module changes (`references/modules.lock`, `.modules/`) ride in the same PR
  as the files they changed, with a decision-log entry.
- Lessons for other projects: a `playbook-candidate: <one line>` trailer on
  the commit that adds them to `references/playbook-candidates.md`
  (`template-candidate:` for a template-core fix).
