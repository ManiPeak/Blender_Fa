from __future__ import annotations

import pathlib
import subprocess
import tomllib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class PrototypeRepositoryTests(unittest.TestCase):
    def test_upstream_commit_is_pinned(self) -> None:
        lock = tomllib.loads((ROOT / "upstream.lock").read_text(encoding="utf-8"))
        self.assertEqual(lock["tag"], "v4.5.9")
        self.assertRegex(lock["commit"], r"^[0-9a-f]{40}$")

    def test_patch_is_parseable_and_touches_only_topbar(self) -> None:
        patch = ROOT / "patches/0001-topbar-language-selector.patch"
        result = subprocess.run(
            ["git", "apply", "--numstat", str(patch)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(len(result.stdout.strip().splitlines()), 1)
        self.assertIn("scripts/startup/bl_ui/space_topbar.py", result.stdout)

    def test_menu_is_native_and_has_both_languages(self) -> None:
        patch = (ROOT / "patches/0001-topbar-language-selector.patch").read_text(encoding="utf-8")
        for required in (
            "TOPBAR_MT_farsi_language",
            "wm.farsi_set_language",
            '"fa_IR"',
            '"en_US"',
            "save_userpref",
            "فارسی",
            "English",
        ):
            with self.subTest(required=required):
                self.assertIn(required, patch)

    def test_glossary_has_unique_terms(self) -> None:
        import csv
        with (ROOT / "docs/terminology/fa-glossary.csv").open(encoding="utf-8", newline="") as stream:
            terms = [row["English"] for row in csv.DictReader(stream)]
        self.assertGreaterEqual(len(terms), 10)
        self.assertEqual(len(terms), len(set(terms)))


if __name__ == "__main__":
    unittest.main()
