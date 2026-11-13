# Release checklist

No release is currently available until the Windows build and package checks complete. `.github/workflows/windows-build.yml` builds the pinned source on Windows Server 2022, runs background smoke tests, packages the complete install tree as a ZIP, verifies SHA-256, and uploads a temporary workflow artifact. `.github/workflows/windows-release.yml` can publish only an alpha/beta tag that matches the exact commit of a successful build run, after rechecking the archived package and checksum. The `.exe` is included inside the ZIP with required DLLs and data; it is not a standalone single-file executable. Neither workflow has yet completed successfully end-to-end.

## Required evidence

- [ ] Exact upstream commit and project patch verified against it.
- [ ] Modified Blender build hash and Windows/compiler/dependency details recorded.
- [ ] Native UI and language-switch tests pass; failure/limitations documented.
- [ ] Original and modified screenshots captured under matching settings; layout preserved.
- [ ] Core modeling, shading, animation, save/open, and render smoke tests run.
- [ ] Package launches on intended clean Windows x64 environment with dependencies accounted for.
- [ ] License/third-party notices, installation steps, and changelog included.
- [ ] SHA-256 generated and independently verified; archive contents checked.
- [ ] README claims, assets, version, release notes, and limitations checked.
- [ ] Repository/tag permissions available; create and verify release only after all prerequisites above.
