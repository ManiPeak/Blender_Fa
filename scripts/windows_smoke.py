"""Run inside Blender's actual Windows GUI for the language-switch smoke test.

A GUI is required because changing Blender's interface locale can refresh
native UI state. This test verifies operator registration, document safety,
and preference persistence across separate GUI process launches.
"""

from __future__ import annotations

import os
import pathlib
import traceback

phase = os.environ["BLENDER_FARSI_PHASE"]
result_path = pathlib.Path(os.environ["BLENDER_FARSI_RESULT"])
result_path.write_text(f"STARTED phase={phase}\\n", encoding="utf-8")

try:
    import bpy
    result_path.write_text(
        result_path.read_text(encoding="utf-8") + f"BPY_IMPORTED blender={bpy.app.version_string}\\n",
        encoding="utf-8",
    )
except BaseException:
    result_path.write_text(traceback.format_exc(), encoding="utf-8")
    raise

expected = {
    "set-fa": "fa_IR",
    "verify-fa": "fa_IR",
    "set-en": "en_US",
    "verify-en": "en_US",
}[phase]


def mark(message: str) -> None:
    with result_path.open("a", encoding="utf-8") as stream:
        stream.write(f"{message}\\n")


def run_test() -> None:
    try:
        mark("TIMER_ENTERED")
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
            mark("BEFORE_LANGUAGE_OPERATOR")
            result = bpy.ops.wm.farsi_set_language(language=expected)
            mark(f"AFTER_LANGUAGE_OPERATOR result={result!r}")
            if "FINISHED" not in result:
                raise RuntimeError(f"Language operator failed: {result!r}")
            if marker.name not in bpy.data.objects:
                raise RuntimeError("Language switch unexpectedly lost unsaved scene data")

        mark(f"CHECK_LANGUAGE language={view.language} translated={view.use_translate_interface}")
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
