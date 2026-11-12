## Blender Farsi 0.1.0 Alpha

This is an experimental Windows x64 source build based on Blender 4.5.9 LTS. The archive includes the complete installed Blender runtime tree; `Blender/blender.exe` is included but is **not** a standalone executable. Keep the extracted folder structure intact.

### Language menu

The build contains a small native top-menu selector for **فارسی** and **English**. It uses Blender's existing `fa_IR` and `en_US` interface preferences and saves user preferences. The Persian catalog is the upstream Blender catalog and is incomplete; this release does not claim full Persian localization.

### Verification and limitations

The release workflow records the exact source/project commits and Windows toolchain in `build-info.txt`. It builds the pinned Blender source, launches `blender.exe --version`, and launches Blender's Windows GUI to test menu/operator registration, Persian/English preference switching, preference persistence across restarts, and preservation of unsaved in-memory scene data.

These checks do **not** verify interactive UI rendering, visual layout against stock Blender, high-DPI/RTL text behavior, or Windows 10/11 desktop compatibility. Treat this as a developer preview, keep backups of important work, and report issues with the build metadata attached.
