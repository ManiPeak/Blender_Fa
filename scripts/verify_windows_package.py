#!/usr/bin/env python3
"""Validate the layout and metadata of a Windows Blender Farsi release ZIP."""
from __future__ import annotations

import argparse
import pathlib
import re
import zipfile
import tomllib


def verify(path: pathlib.Path, expected_project_commit: str | None = None) -> None:
    if not zipfile.is_zipfile(path):
        raise RuntimeError(f"Not a valid ZIP archive: {path}")
    with zipfile.ZipFile(path) as archive:
        files = {item.filename: item for item in archive.infolist() if not item.is_dir()}
        required = (
            "Blender-Farsi/Blender/blender.exe",
            "Blender-Farsi/Blender/4.5/",
            "Blender-Farsi/LICENSE",
            "Blender-Farsi/BLENDER-COPYING",
            "Blender-Farsi/NOTICE.md",
            "Blender-Farsi/build-info.txt",
            "Blender-Farsi/README-Windows.txt",
        )
        for name in required:
            if name.endswith("/"):
                if not any(entry.startswith(name) for entry in files):
                    raise RuntimeError(f"Runtime directory missing from package: {name}")
            elif name not in files:
                raise RuntimeError(f"Required package file missing: {name}")
        exe = files["Blender-Farsi/Blender/blender.exe"]
        if exe.file_size < 1024 * 1024:
            raise RuntimeError(f"Packaged blender.exe is unexpectedly small ({exe.file_size} bytes)")
        metadata = archive.read("Blender-Farsi/build-info.txt").decode("utf-8-sig")
        lock_path = pathlib.Path(__file__).resolve().parents[1] / "upstream.lock"
        expected_upstream = tomllib.loads(lock_path.read_text(encoding="utf-8"))["commit"]
        upstream = re.search(r"^Blender source commit: ([0-9a-f]{40})$", metadata, re.M)
        if not upstream or upstream.group(1) != expected_upstream:
            raise RuntimeError("Package metadata does not match the pinned Blender source commit")
        project = re.search(r"^Blender Farsi project commit: ([0-9a-f]{40})$", metadata, re.M)
        if not project:
            raise RuntimeError("Package metadata is missing the Blender Farsi project commit")
        if expected_project_commit and project.group(1) != expected_project_commit:
            raise RuntimeError("Package metadata does not match the tagged Blender Farsi project commit")
        print(f"Validated Windows archive: {path} ({len(files)} files)")
        print(f"Blender executable: {exe.file_size} bytes")
        print(f"Blender source commit: {upstream.group(1)}")
        print(f"Blender Farsi build commit: {project.group(1)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=pathlib.Path)
    parser.add_argument("--project-commit")
    args = parser.parse_args()
    verify(args.archive, args.project_commit)


if __name__ == "__main__":
    main()
