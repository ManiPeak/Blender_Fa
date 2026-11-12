# Building Blender Farsi

## Current state and verified environment

This workspace is Linux x86_64 (`uname` reports Linux 6.1.158), with Python 3.11.2 and Git available. It has about 20 GiB free disk and 3.8 GiB RAM. Blender, CMake, Ninja, GCC, Clang, and a Windows toolchain are not available on `PATH` (GCC is installed; the other compiler/build tools listed were absent). No Windows machine or Windows runner is attached. A complete Blender build and Windows package were therefore not attempted or produced. These facts block a genuine Windows x64 distribution and application-level test in this session.

## Locked source

`upstream.lock` selects Blender `v4.5.9` at `8bf95cbd38d1456c94e9d751f3804eea4d5b137b`. This project repo stores its source modification as a patch, avoiding a partial or misleading copy of Blender's history. The upstream source tree and its third-party dependency checkout are substantial; plan for multi-gigabyte storage, significant memory, a long build, and platform-specific prerequisites. The current 20 GiB / 3.8 GiB environment should not be assumed sufficient for a full native build.

## Prepare a source tree

From the project repository root, use a separate sibling checkout:

```bash
git clone --filter=blob:none --no-checkout https://github.com/blender/blender.git ../blender-upstream
git -C ../blender-upstream checkout --detach 8bf95cbd38d1456c94e9d751f3804eea4d5b137b
git -C ../blender-upstream apply --check "$PWD/patches/0001-topbar-language-selector.patch"
```

For a build, follow the official [Blender building handbook](https://developer.blender.org/docs/handbook/building_blender/) and platform-specific instructions for the pinned revision. Set up the prescribed compiler, CMake/Ninja or Make, Python, libraries, and `make update` dependencies on a machine that meets the handbook requirements. Then build the patched source following the instructions in that checkout. The exact generator, build target, compiler, dependency revisions, and configuration must be recorded from the actual machine; they are not known for this workspace.

The official upstream build instructions are authoritative. This repository does not yet provide a tested one-command build wrapper, Windows installer, or portable archive. Do not package a stock upstream binary and call it Blender Farsi.

## Windows x64 release gate

Before packaging:

1. Build the patched source with the supported Windows toolchain on a Windows x64 host/runner, recording source commit, compiler/tool versions, dependency revisions, CMake options, and OS build.
2. Launch the executable; verify the top menu, Persian/English toggling, saved preference after restart, and language fallback.
3. Run the core workflow and layout checks in [`testing.md`](testing.md); capture genuine application screenshots.
4. Confirm bundled runtime dependencies and license notices; do not call the result portable until verified on a clean Windows environment.
5. Produce a versioned archive and SHA-256 file, verify the checksum, inspect the archive, and test extraction/launch.
6. Only then publish a prerelease with truthful limitations.
