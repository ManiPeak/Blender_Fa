# Source architecture and prototype decision

## Upstream inspected

The selected baseline is Blender `v4.5.9`, tag commit `8bf95cbd38d1456c94e9d751f3804eea4d5b137b` (see [`../upstream.lock`](../upstream.lock)). The exact upstream files were inspected through GitHub's source API:

- `scripts/startup/bl_ui/space_topbar.py`: Python-defined `TOPBAR_HT_upper_bar` and `TOPBAR_MT_editor_menus` assemble the existing top-level menu row; `TOPBAR_MT_editor_menus` is listed in that module's `classes` tuple.
- `scripts/modules/bl_i18n_utils/settings.py`: language identifier `fa_IR` is present (language ID 26), and `fa_IR` is included in the RTL gettext pre-processing set.
- `locale/po/fa.po`: Persian catalog is present (96,978 bytes in the inspected tag). It is community-maintained upstream and is not proof of complete coverage.
- `scripts/presets/interface_theme/Blender_Dark.xml` and `Blender_Light.xml`: native interface theme presets are part of this source tree.

The checkout available to this task is an unrelated-sized, one-commit, shallow Git repository with only a minimal README; the Blender source itself is not present. The implementation is therefore kept as a patch against the pinned upstream file rather than fabricated as a compiled product.

## Language control design

The prototype patch adds a native Python menu class and operator in Blender's existing `space_topbar.py` module, then adds the menu call at the end of the pre-existing top-level menu sequence. It relies on Blender's existing preference fields, setting `preferences.view.language` to `fa_IR` or `en_US` and enabling `use_translate_interface`. The menu's operator calls `bpy.ops.wm.save_userpref()` so the selection is intended to survive restart without writing to the current `.blend` document.

This is a source-level implementation, not a verified runtime result. Runtime tests must confirm the property-update redraw, the saved user preference, the behavior with unsaved document changes, and the UI's behavior if saving preferences fails. Blender 4.5.9 uses the configured translation catalog; missing or untranslated messages continue to fall back to source strings. RTL rendering/shaping is upstream behavior and must be exercised separately.

## Visual styling decision

The source tree exposes native interface theme presets. The design spec maps tokens to supported theme properties instead of adding global compositor blur or a custom draw loop. This repository does not yet ship a modified theme preset: theme property mapping and appearance need to be confirmed against a running Blender and high-DPI screenshot comparison before claiming visual refinements.

## Patch and review

`patches/0001-topbar-language-selector.patch` is deliberately small and source-local. Before applying, check it against the locked source commit:

```bash
git -C ../blender-upstream rev-parse HEAD
git -C ../blender-upstream apply --check ../Blender_Fa/patches/0001-topbar-language-selector.patch
```

The `TOPBAR_MT_editor_menus` list is the real menu row; the change does not create a side panel, alter editor areas, change workspace geometry, or replace native editors. The patch is GPL-2.0-or-later, consistent with the target source file's notice.
