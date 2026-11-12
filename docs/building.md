# Building Blender Farsi

## Current state and verified environment

This workspace is Linux x86_64 (`uname` reports Linux 6.1.158), with Python 3.11.2 and Git available. It has about 20 GiB free disk and 3.8 GiB RAM. GCC 12.2.0 and GNU Make 4.3 are installed; Blender, CMake, Ninja, Clang, MSVC `cl.exe`, and a Windows toolchain are not available on `PATH`. No Windows machine or Windows runner is attached. The official handbook requires CMake, and the current handbook's compiler table lists Linux GCC 14.0.0 minimum; therefore this environment is not a suitable Blender build host. A complete Blender build and Windows package were not attempted or produced. These facts block a genuine Windows x64 distribution and application-level test in this session.

## Locked source

`upstream.lock` selects Blender `v4.5.9` at `8bf95cbd38d1456c94e9d751f3804eea4d5b137b`. This project repo stores its source modification as a patch, avoiding a partial or misleading copy of Blender's history. The upstream source tree and its third-party dependency checkout are substantial; plan for multi-gigabyte storage, significant memory, a long build, and platform-specific prerequisites. The current 20 GiB / 3.8 GiB environment should not be assumed sufficient for a full native build.

## Prepare a source tree

From the project repository root, use a separate sibling checkout:

```bash
git clone --filter=blob:none --no-checkout https://github.com/blender/blender.git ../blender-upstream
git -C ../blender-upstream checkout --detach 8bf95cbd38d1456c94e9d751f3804eea4d5b137b
git -C ../blender-upstream apply --check "$PWD/patches/0001-topbar-language-selector.patch"
```

For a build, follow the official [Blender building handbook](https://developer.blender.org/docs/handbook/building_blender/) and platform-specific instructions for the pinned revision. The handbook describes Blender's CMake build system and `make update` / `make` wrapper; its [Windows guide](https://developer.blender.org/docs/handbook/building_blender/windows/) calls for Git, CMake, Visual Studio 2022 with the Desktop Development with C++ workload, and the command-prompt workflow, then `make update` and `make`. It notes that dependency libraries are several gigabytes. The general handbook currently lists GCC 14.0.0 minimum for Linux; this workspace's GCC 12.2.0 and missing CMake do not meet that published Linux requirement. The handbook pages were inspected on 2026-11-12 and may evolve independently of the pinned 4.5.9 source. Set up the revision-appropriate compiler, CMake, Python, libraries, and dependencies on a machine meeting the handbook requirements. Record the exact generator, build target, compiler, dependency revisions, CMake options, and OS build from the actual machine; no build configuration is known for this workspace.

The official upstream build instructions are authoritative. This repository does not yet provide a tested one-command build wrapper, Windows installer, or portable archive. Do not package a stock upstream binary and call it Blender Farsi.

## Windows x64 release gate

Before packaging:

1. Build the patched source with the supported Windows toolchain on a Windows x64 host/runner, recording source commit, compiler/tool versions, dependency revisions, CMake options, and OS build.
2. Launch the executable; verify the top menu, Persian/English toggling, saved preference after restart, and language fallback.
3. Run the core workflow and layout checks in [`testing.md`](testing.md); capture genuine application screenshots.
4. Confirm bundled runtime dependencies and license notices; do not call the result portable until verified on a clean Windows environment.
5. Produce a versioned archive and SHA-256 file, verify the checksum, inspect the archive, and test extraction/launch.
6. Only then publish a prerelease with truthful limitations.
