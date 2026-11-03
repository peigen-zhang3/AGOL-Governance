#!/usr/bin/env python3
"""Record exactly which input files a deliverable was built from.

    python3 scripts/input_manifest.py deliverable/2026-11-14-draft-report
    python3 scripts/input_manifest.py <tag> --inputs data/inputs data/cache/full --force

Writes ``deliverables/<tag>/inputs.json``: path, sha256, size and modified
time for every file under ``data/inputs/`` and ``data/cache/`` (what the
sources read, per scope; folders that don't exist are skipped). Real data is never committed, so
this manifest is how a tagged deliverable proves which inputs it used and
how a re-run checks it has the same ones. It never copies or uploads data.
Commit the manifest in the deliverable's tagged commit. Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".gitkeep", ".DS_Store", "Thumbs.db"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):  # 1 MB at a time
            h.update(chunk)
    return h.hexdigest()


def manifest(inputs: Path) -> list[dict]:
    rows = []
    for p in sorted(inputs.rglob("*")):
        if p.is_file() and p.name not in SKIP:
            st = p.stat()
            rows.append(
                {
                    "path": p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p),
                    "sha256": sha256(p),
                    "size": st.st_size,
                    "mtime": dt.datetime.fromtimestamp(st.st_mtime, dt.UTC).isoformat(
                        timespec="seconds"
                    ),
                }
            )
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("tag", help="deliverable tag, e.g. deliverable/2026-11-14-draft-report")
    ap.add_argument(
        "--inputs",
        nargs="+",
        default=["data/inputs", "data/cache"],
        help="folders to record (default data/inputs data/cache)",
    )
    ap.add_argument("--force", action="store_true", help="overwrite an existing manifest")
    a = ap.parse_args(argv)

    folders = [(ROOT / f).resolve() for f in a.inputs]
    folders = [f for f in folders if f.is_dir()]
    if not folders:
        print(f"input_manifest: none of {a.inputs} is a folder", file=sys.stderr)
        return 1
    name = a.tag.removeprefix("deliverable/").strip("/")
    if not name or any(part in ("", "..") for part in name.split("/")):
        print(f"input_manifest: bad tag {a.tag!r}", file=sys.stderr)
        return 1
    out = ROOT / "deliverables" / name / "inputs.json"
    if out.exists() and not a.force:
        print(f"input_manifest: {out.relative_to(ROOT)} exists (use --force)", file=sys.stderr)
        return 1
    rows = [row for f in folders for row in manifest(f)]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "tag": a.tag,
                "created": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
                "inputs": a.inputs,
                "files": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    total = sum(r["size"] for r in rows)
    where = out.relative_to(ROOT)
    print(f"wrote {where}: {len(rows)} files, {total / 1e6:.1f} MB recorded (nothing copied)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
