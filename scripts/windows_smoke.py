"""Run inside Blender's actual Windows GUI for the language-switch smoke test.

A GUI is required because changing Blender's interface locale can refresh
native UI state. This test verifies operator registration, document safety,
and preference persistence across separate GUI process launches.
"""

from __future__ import annotations

import os
import pathlib
import traceback

import bpy


phase = os.environ["BLENDER_FARSI_PHASE"]
result_path = pathlib.Path(os.environ["BLENDER_FARSI_RESULT"])
expected = {
    "set-fa": "fa_IR",
    "verify-fa": "fa_IR",
    "set-en": "en_US",
    "verify-en": "en_US",
}[phase]


def run_test() -> None:
    try:
        view = bpy.context.preferences.view
        if not hasattr(bpy.ops.wm, "farsi_set_language"):
            raise RuntimeError("wm.farsi_set_language was not registered in Blender's GUI startup")
        if not hasattr(bpy.types, "TOPBAR_MT_farsi_language"):
            raise RuntimeError("The language menu was not registered in Blender's GUI startup")

        if phase.startswith("set-"):
            # Leave an unsaved scene object in memory: switching only language
            # preferences must not discard or save the current .blend document.
            marker = bpy.data.objects.new("unsaved_language_switch_probe", None)
            bpy.context.scene.collection.objects.link(marker)
            result = bpy.ops.wm.farsi_set_language(language=expected)
            if "FINISHED" not in result:
                raise RuntimeError(f"Language operator failed: {result!r}")
            if marker.name not in bpy.data.objects:
                raise RuntimeError("Language switch unexpectedly lost unsaved scene data")

        if view.language != expected or not view.use_translate_interface:
            raise RuntimeError(
                f"Expected persisted language {expected}, got {view.language}; "
                f"translate_interface={view.use_translate_interface}"
            )

        result_path.write_text(
            f"PASS phase={phase} language={view.language} blender={bpy.app.version_string}\n",
            encoding="utf-8",
        )
    except BaseException:
        result_path.write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        # Exit the GUI process after the result has been written for the runner.
        try:
            bpy.ops.wm.quit_blender()
        except Exception:
            pass
    return None


bpy.app.timers.register(run_test, first_interval=2.0)
