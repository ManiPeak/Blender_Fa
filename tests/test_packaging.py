from __future__ import annotations

import hashlib
import pathlib
import tempfile
import unittest
import zipfile

from scripts.package_windows import create_package

ROOT = pathlib.Path(__file__).resolve().parents[1]


class PackagingHelperTests(unittest.TestCase):
    def test_stages_complete_tree_and_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            install = root / "install"
            (install / "4.5").mkdir(parents=True)
            (install / "blender.exe").write_bytes(b"x" * (1024 * 1024))
            (install / "4.5" / "scripts").mkdir()
            (install / "4.5" / "scripts" / "test.py").write_text("pass\n")
            upstream = root / "upstream"
            upstream.mkdir()
            (upstream / "COPYING").write_text("upstream license\n")
            build_info = root / "build-info.txt"
            build_info.write_text("test build metadata\n")
            output = root / "output"

            archive, checksum = create_package(
                install,
                ROOT,
                upstream,
                output,
                "0.1.0-alpha.test",
                build_info,
            )
            with zipfile.ZipFile(archive) as zf:
                names = set(zf.namelist())
            self.assertIn("Blender-Farsi/Blender/blender.exe", names)
            self.assertIn("Blender-Farsi/Blender/4.5/scripts/test.py", names)
            self.assertIn("Blender-Farsi/BLENDER-COPYING", names)
            self.assertIn("Blender-Farsi/README-Windows.txt", names)
            expected = hashlib.sha256(archive.read_bytes()).hexdigest()
            self.assertTrue(checksum.read_text().startswith(expected + "  "))

    def test_refuses_missing_executable_or_runtime_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            install = root / "install"
            install.mkdir()
            upstream = root / "upstream"
            upstream.mkdir()
            (upstream / "COPYING").write_text("license")
            metadata = root / "build-info.txt"
            metadata.write_text("build")
            with self.assertRaises(RuntimeError):
                create_package(install, ROOT, upstream, root / "out", "test", metadata)


if __name__ == "__main__":
    unittest.main()
