"""Run inside the just-built Blender executable on Windows CI.

This checks the bundled operator, both built-in locale settings, and persistence
across process restarts. It is a background smoke test, not a UI/render test.
"""

from __future__ import annotations

import os

import bpy


phase = os.environ["BLENDER_FARSI_PHASE"]
print(f"SMOKE_BEGIN phase={phase} blender={bpy.app.version_string} background={bpy.app.background}", flush=True)
print(f"SMOKE_OPERATOR_REGISTERED={hasattr(bpy.ops.wm, 'farsi_set_language')}", flush=True)
expected = {
    "set-fa": "fa_IR",
    "verify-fa": "fa_IR",
    "set-en": "en_US",
    "verify-en": "en_US",
}[phase]
view = bpy.context.preferences.view

if phase.startswith("set-"):
    if not hasattr(bpy.ops.wm, "farsi_set_language"):
        raise RuntimeError("Blender startup did not register wm.farsi_set_language")

    # Create unsaved scene data to make sure the language operator does not
    # replace, save, or otherwise discard the current document.
    marker = bpy.data.objects.new("unsaved_language_switch_probe", None)
    bpy.context.scene.collection.objects.link(marker)
    result = bpy.ops.wm.farsi_set_language(language=expected)
    if "FINISHED" not in result:
        raise RuntimeError(f"Language operator failed: {result!r}")
    if marker.name not in bpy.data.objects:
        raise RuntimeError("Language switch unexpectedly lost unsaved scene data")
    if view.language != expected or not view.use_translate_interface:
        raise RuntimeError(f"Language preference did not update to {expected}")
else:
    if view.language != expected or not view.use_translate_interface:
        raise RuntimeError(
            f"Preference did not persist: expected {expected}, got {view.language}"
        )

print(f"BLENDER_FARSI_SMOKE_OK phase={phase} language={view.language}")
