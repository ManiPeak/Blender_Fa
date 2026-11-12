# Testing and evidence

## Executed in this workspace

- Environment inspection: Linux x86_64, Python 3.11.2, Git and GitHub CLI available; no Blender executable, CMake, Ninja, or Windows toolchain found.
- Upstream source inspection: pinned top-bar and localization source via GitHub API; verified the tag commit and existence of the Persian catalog.
- Patch application/syntax check: applied the patch to a temporary fixture containing the exact `space_topbar.py` source blob fetched from Blender `v4.5.9`; `git apply --check` succeeded and `python3 -m py_compile` succeeded on the patched file. This did not fetch or build the complete Blender source tree.
- Project static tests: `python3 -m unittest discover -s tests -v` — 6 tests passed, including ZIP staging/checksum helper tests using a synthetic fixture; `python3 scripts/validate_patch.py` passed; `python3 -m compileall -q scripts tests` passed; `git diff --check` passed.
- Windows build workflow: configured to build the pinned source, smoke-test `blender.exe`, verify preference persistence, create the full runtime ZIP, verify SHA-256, and upload a temporary artifact. The separate release workflow accepts alpha/beta tags only when a successful build artifact exists for that exact source commit. End-to-end Windows validation has not yet succeeded.

These do not exercise Blender. No application launch, UI rendering, file editing, language switching, performance timing, Windows package, or visual comparison result is claimed.

## Required Blender integration matrix

Record Blender build hash, OS, display resolution, scale, startup file, workspace, and test operator/file in each run.

| Area | Required verification | Status |
| --- | --- | --- |
| Launch/render | Launch and close, inspect console/log, normal UI rendering | Not run — executable unavailable |
| Layout | Compare original and modified anchor positions in multiple stock workspaces | Not run |
| Menu | Find the selector in top application menu; verify no stock menu/workspace relocation | Not run |
| Language | English → Persian → English, repeat, restart; inspect persisted language preference | Not run |
| Unsaved document | Modify a `.blend` without saving; change UI language; verify scene/document stays intact | Not run |
| Localization | Check translated and untranslated fallback strings; mixed Persian/Latin, digits, punctuation, paths, search/edit fields | Not run |
| Display scale | Verify menu sizing, clipping and shaping at 100%, 150%, and 200% | Not run |
| Modeling | Add/edit mesh, Object/Edit Mode, transforms, Outliner and object properties | Not run |
| Shading | Add modifier, material, nodes and inspect viewport | Not run |
| Animation/render | Set keyframes/playback, camera/light, render a basic scene | Not run |
| Responsiveness | Compare startup, redraw, menu interaction and viewport responsiveness against stock build | Not run |
| Windows package | Clean extraction/launch, dependencies, checksum and package metadata | Blocked — no Windows build host/toolchain |

## Layout comparison method

Use the same source build except for the project patch; same OS build, monitor resolution, UI scale, workspace, window size, startup scene, theme state, and capture method. Capture untouched upstream first, then modified. Compare top-bar baseline and workspace tabs, viewport boundaries, toolbar, Timeline, Outliner, Properties, status bar, and editor boundaries. Do not crop, retouch, or reposition the interface to imply preserved geometry. Save screenshots and a short result checklist under `docs/screenshots/` only after they are captured from real application runs.
