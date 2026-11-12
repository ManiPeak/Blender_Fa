#!/usr/bin/env python3
"""Stage Blender's installed Windows tree, make a ZIP, and write its SHA-256."""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import tempfile
import zipfile


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_package(
    install_dir: pathlib.Path,
    project_root: pathlib.Path,
    upstream_root: pathlib.Path,
    output_dir: pathlib.Path,
    version: str,
    build_info: pathlib.Path,
) -> tuple[pathlib.Path, pathlib.Path]:
    install_dir = install_dir.resolve(strict=True)
    project_root = project_root.resolve(strict=True)
    upstream_root = upstream_root.resolve(strict=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    executable = install_dir / "blender.exe"
    if not executable.is_file() or executable.stat().st_size < 1024 * 1024:
        raise RuntimeError(f"Expected a real Blender executable at {executable}")
    if not (install_dir / "4.5").is_dir():
        raise RuntimeError("Blender 4.5 runtime data is missing from the install tree")

    safe_version = "".join(c for c in version if c.isalnum() or c in ".-_+")
    archive = output_dir / f"Blender-Farsi-{safe_version}-Windows-x64.zip"
    checksum = archive.with_suffix(archive.suffix + ".sha256")

    with tempfile.TemporaryDirectory(prefix="blender-farsi-package-") as temp:
        staging = pathlib.Path(temp) / "Blender-Farsi"
        app_dir = staging / "Blender"
        shutil.copytree(install_dir, app_dir)
        (staging / "LICENSE").write_bytes((project_root / "LICENSE").read_bytes())
        (staging / "NOTICE.md").write_bytes((project_root / "NOTICE.md").read_bytes())
        (staging / "BLENDER-COPYING").write_bytes((upstream_root / "COPYING").read_bytes())
        (staging / "build-info.txt").write_bytes(build_info.read_bytes())
        (staging / "README-Windows.txt").write_text(
            "Blender Farsi — Windows x64 prerelease\n\n"
            "Extract the entire archive and keep its folder structure intact.\n"
            "Launch Blender\\blender.exe. The executable depends on the included\n"
            "runtime files; it is not a standalone single-file program.\n\n"
            "To switch languages, use Language / زبان in Blender's top menu,\n"
            "then choose فارسی or English. Blender saves this as a user\n"
            "preference; it does not save or modify the current .blend file.\n\n"
            "This is an experimental build. Translation coverage is limited to\n"
            "Blender's bundled Persian catalog and may be incomplete.\n",
            encoding="utf-8",
        )
        with zipfile.ZipFile(
            archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True
        ) as zf:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(staging.parent).as_posix())

    checksum.write_text(f"{sha256_file(archive)}  {archive.name}\n", encoding="ascii")
    return archive, checksum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-dir", type=pathlib.Path, required=True)
    parser.add_argument("--project-root", type=pathlib.Path, required=True)
    parser.add_argument("--upstream-root", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--build-info", type=pathlib.Path, required=True)
    args = parser.parse_args()
    archive, checksum = create_package(
        args.install_dir,
        args.project_root,
        args.upstream_root,
        args.output_dir,
        args.version,
        args.build_info,
    )
    print(f"PACKAGE={archive}")
    print(f"SHA256_FILE={checksum}")
    print(f"SHA256={sha256_file(archive)}")


if __name__ == "__main__":
    main()
