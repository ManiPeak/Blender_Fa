#!/usr/bin/env python3
"""Validate project-owned patch metadata without claiming a Blender build test."""
from __future__ import annotations

import pathlib
import re
import subprocess
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCK = tomllib.loads((ROOT / "upstream.lock").read_text(encoding="utf-8"))
PATCH = ROOT / "patches/0001-topbar-language-selector.patch"
text = PATCH.read_text(encoding="utf-8")
assert re.fullmatch(r"[0-9a-f]{40}", LOCK["commit"]), "upstream commit must be a full SHA"
assert LOCK["tag"] == "v4.5.9" and LOCK["version"].startswith("4.5.9")
assert "scripts/startup/bl_ui/space_topbar.py" in text
assert "TOPBAR_MT_farsi_language" in text
assert "wm.farsi_set_language" in text
assert '"fa_IR"' in text and '"en_US"' in text
assert "save_userpref" in text
assert "layout.menu(\"TOPBAR_MT_farsi_language\"" in text

# Let Git validate unified-diff syntax and report the expected changed file.
result = subprocess.run(
    ["git", "apply", "--numstat", str(PATCH)],
    cwd=ROOT,
    check=True,
    capture_output=True,
    text=True,
)
assert "scripts/startup/bl_ui/space_topbar.py" in result.stdout

# Keep the glossary machine-readable and avoid accidental duplicate source terms.
import csv
with (ROOT / "docs/terminology/fa-glossary.csv").open(encoding="utf-8", newline="") as stream:
    rows = list(csv.DictReader(stream))
assert rows and all(row["English"].strip() and row["Persian (review draft)"].strip() for row in rows)
assert len({row["English"] for row in rows}) == len(rows)

# Resolve every project-relative Markdown link/image used by the README.
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for target in re.findall(r"\]\(([^)]+)\)", readme):
    if target.startswith(("https://", "http://", "#", "mailto:")):
        continue
    path = target.split("#", 1)[0]
    if path:
        assert (ROOT / path).exists(), f"README references missing file: {target}"
for target in re.findall(r'<img[^>]+src="([^"]+)"', readme):
    if target.startswith(("https://", "http://")):
        continue
    assert (ROOT / target).exists(), f"README references missing image: {target}"

print(f"Static patch checks passed for Blender {LOCK['version']} ({LOCK['commit']}).")
print("This validates patch structure only; upstream application and Blender runtime remain untested.")
