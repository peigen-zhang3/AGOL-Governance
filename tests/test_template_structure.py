"""Structural guarantees for the vanilla template core (stdlib only).

    python3 tests/test_template_structure.py      # CI hygiene job
    pytest tests/test_template_structure.py       # also collected in projects

The template itself carries no stack: code arrives as playbook modules. So on
the template (no references/modules.lock) there is no src/ and CLAUDE.md
stays under the vanilla cap; once modules are installed those two checks
relax to the project cap. The .gitignore checks apply everywhere.
"""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VANILLA_CAP = 120
PROJECT_CAP = 200

REQUIRED = [
    "CLAUDE.md",
    "README.md",
    ".claude/settings.json",
    ".claude/skills/new-project/SKILL.md",
    ".claude/skills/remember/SKILL.md",
    ".claude/skills/capture/SKILL.md",
    ".claude/skills/template-sync/SKILL.md",
    ".github/workflows/ci.yml",
    ".github/pull_request_template.md",
    ".gitignore",
    ".gitattributes",
    ".env.example",
    ".pre-commit-config.yaml",
    "docs/CHANGELOG.md",
    "docs/git-workflow.md",
    "references/README.md",
    "references/playbook-candidates.md",
    "data/README.md",
    "scripts/input_manifest.py",
]


def has_modules() -> bool:
    return (ROOT / "references" / "modules.lock").exists()


class TestStructure(unittest.TestCase):
    def test_required_core_files_exist(self):
        missing = [p for p in REQUIRED if not (ROOT / p).exists()]
        self.assertFalse(missing, f"vanilla core files missing: {missing}")

    def test_template_has_no_stack_code(self):
        # Stack code and the container are modules (the container is opt-in).
        if has_modules():
            self.skipTest("modules installed: stack code is expected")
        for path in ("src", "pyproject.toml", "main.py", "docker"):
            self.assertFalse(
                (ROOT / path).exists(), f"{path} belongs in a starter module, not the core"
            )

    def test_claude_md_line_cap(self):
        cap = PROJECT_CAP if has_modules() else VANILLA_CAP
        n = len((ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(
            n, cap, f"CLAUDE.md is {n} lines (cap {cap}): move procedures into skills"
        )

    def test_module_insert_markers_present(self):
        # Modules insert their CLAUDE.md and pre-commit blocks above these.
        self.assertIn("<!-- modules:insert -->", (ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
        for rel in (".pre-commit-config.yaml", ".env.example"):
            self.assertIn("# modules:insert", (ROOT / rel).read_text(encoding="utf-8"), rel)

    def test_gitignore_has_no_inline_comments(self):
        # Git has NO inline comments in .gitignore: text after a pattern becomes
        # part of the pattern, silently disabling the rule. This shipped once.
        for i, line in enumerate((ROOT / ".gitignore").read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            self.assertNotIn(" #", line, f".gitignore:{i} has an inline comment: {line!r}")

    def test_gitignore_rules_actually_ignore(self):
        for path in (
            ".env",
            "data/inputs/x.gpkg",
            "data/library/x.txt",
            "layer_map.json",
            "config/x.xlsx",
        ):
            rc = subprocess.run(
                ["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT
            ).returncode
            self.assertEqual(rc, 0, f"{path} is NOT ignored — a .gitignore rule regressed")

    def test_data_folders_track_only_what_data_readme_says(self):
        # data/README.md: only the opt-in tracked/ (and tests/fixtures/) are
        # kept, and named review runs inside tracked/ stay ignored.
        def ignored(path: str) -> bool:
            rc = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT)
            return rc.returncode == 0

        for path in (
            "data/outputs/pilot/run.json",
            "data/outputs/full/x.gpkg",
            "data/cache/pilot/features.gpkg",
            "data/cache/pilot/features.json",
            "data/inputs/x.tif",
            "data/tracked/outputs/pilot/runs/trial/x.gpkg",
            "elsewhere/x.gpkg",
        ):
            self.assertTrue(ignored(path), f"{path} must be ignored")
        for path in (
            "tests/fixtures/example.gpkg",
            "data/tracked/cache/pilot/features.gpkg",
            "data/tracked/outputs/pilot/x.tif",
            "data/tracked/README.md",
            "data/README.md",
        ):
            self.assertFalse(ignored(path), f"{path} must be trackable")

    def test_module_files_are_not_ignored(self):
        # The lock, the untouched module copies and input manifests are committed.
        for path in (
            "references/modules.lock",
            ".modules/x@1.0.0/a.txt",
            "deliverables/t/inputs.json",
        ):
            rc = subprocess.run(
                ["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT
            ).returncode
            self.assertEqual(rc, 1, f"{path} is ignored but must be committed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
