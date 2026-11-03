# data/

Where a file lives decides whether **git keeps it**, and every run writes into
its own **scope's** folder, so a pilot never lands where the deliverable run
was. Nobody has to remember a rule at commit time.

| Folder | Holds | Git |
|---|---|---|
| `inputs/` | real files placed by hand (sources can also live elsewhere: a network share, AGOL, S3) | ignored |
| `cache/<scope>/` | what each source read returned for that scope, with a `.json` sidecar | ignored |
| `outputs/<scope>/` | a scope's runs (`pilot/`, `full/`), incl. `runs/<name>/` review variants | ignored |
| `library/` | ad-hoc governed extracts of external data, date-stamped with provenance | ignored |
| `tracked/` | **opt-in**: the cache and outputs of a scope a cloud session must keep | **tracked** (with caps) |

`*.gpkg`, `*.tif`, `*.parquet`, `*.las`/`*.laz` and `*.gdb/` are ignored
everywhere except `tracked/` and `tests/fixtures/` (synthetic test data). CI
(`.github/workflows/ci.yml`) fails if anything else under `data/` is
committed. How sources and scopes work is the starter's job: the Python
starter documents it in `docs/sources-and-scopes.md`.

## `tracked/`: real data kept in git (opt-in)
A Claude Code cloud session is ephemeral: anything not committed is gone when
it ends. When a pilot (or a small full run) runs in a cloud session, set
`track = true` on its scope: the scope's cache and outputs then live here, so
the run survives and reviewers see the same files. Use it only when **all** of these hold:

- the client agreed to the data being held in the repository, and the repo
  is private;
- personal fields the method doesn't use are stripped;
- each file is **≤ 25 MB** and `tracked/` stays **≤ 250 MB** in total (CI
  enforces both; GitHub rejects files over 100 MB and every clone carries
  history forever);
- `tracked/README.md` exists and records each file (copy the block below),
  and the decision is in `references/decision-log.md` (`remember`).

Inside it: `tracked/cache/<scope>/` and `tracked/outputs/<scope>/`. Named
review runs under it (`runs/`) stay ignored. Past the caps, don't track: run
on the shared box, and record what a deliverable used with
`scripts/input_manifest.py` (hashes, no data).

Deleting a tracked file later does not remove it from history. If something
was committed that shouldn't have been: rotate anything sensitive, rewrite
history (`git filter-repo`), and tell Danny.

### `tracked/README.md` (copy this block)

```markdown
# Tracked data

**Agreed by:** <client contact role, date, where it's recorded>
**Repo private:** yes · **Personal fields stripped:** <which, or "none present">
**Decision log:** <date + title of the entry>

| File | What | Source | Extracted | Size |
|---|---|---|---|---|
| cache/<scope>/<source>.gpkg | <description> | <provider / dataset> | <yyyy-mm-dd> | <MB> |
```
