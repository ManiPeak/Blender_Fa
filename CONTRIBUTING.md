# Contributing

Contributions should preserve Blender's native interface and keep claims proportional to evidence. This is currently an early source-patch prototype, not a built Blender distribution.

## Before changing the patch

- Read [`upstream.lock`](upstream.lock) and [`docs/architecture.md`](docs/architecture.md).
- Work against the exact pinned Blender commit. Do not update the pin implicitly.
- Keep the patch small and include a clear rationale. Do not modify existing Blender UI layout other than the requested compact menu item without screenshots and layout tests.
- Preserve upstream copyright/licensing headers and do not copy translations without preserving their attribution.
- Never add credentials, generated binaries, downloaded Blender source, or unverified screenshots to this repository.

## Validation

```bash
python3 scripts/validate_patch.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

When a complete pinned source checkout is available, check that the patch applies cleanly using `scripts/apply_patch.sh /path/to/blender-source`. Static checks are not substitutes for running the modified Blender. Changes to UI behavior require application testing and recorded evidence using [`docs/testing.md`](docs/testing.md).

Persian wording should be reviewed by a fluent technical Persian speaker. The glossary is explicitly a review draft; do not call draft terms approved translations.
