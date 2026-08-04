from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_project import inspect_image, validate  # noqa: E402


class ValidateProjectTests(unittest.TestCase):
    def copy_example(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        project = Path(temp_dir.name) / "moon-palace-rpg"
        shutil.copytree(ROOT / "examples" / "moon-palace-rpg", project)
        return temp_dir, project

    def test_complete_example_passes_strict_validation(self) -> None:
        report = validate(ROOT / "examples" / "moon-palace-rpg", strict=True)

        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_detects_manifest_dimension_mismatch(self) -> None:
        temp_dir, project = self.copy_example()
        self.addCleanup(temp_dir.cleanup)
        manifest_path = project / "contracts" / "asset-manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text())
        manifest["assets"][0]["dimensions"] = [1, 1]
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))

        report = validate(project, strict=False)

        self.assertTrue(
            any("do not match actual" in error for error in report.errors),
            report.errors,
        )

    def test_detects_missing_png_alpha_channel(self) -> None:
        temp_dir, project = self.copy_example()
        self.addCleanup(temp_dir.cleanup)
        manifest_path = project / "contracts" / "asset-manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text())
        manifest["assets"][0]["transparent_background"] = True
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))

        report = validate(project, strict=False)

        self.assertTrue(
            any("has no alpha channel" in error for error in report.errors),
            report.errors,
        )

    def test_inspects_svg_dimensions_and_transparency(self) -> None:
        path = (
            ROOT
            / "examples"
            / "moon-palace-rpg"
            / "assets"
            / "components"
            / "primary-button-default-v1.svg"
        )

        self.assertEqual(inspect_image(path), ([640, 192], True))


if __name__ == "__main__":
    unittest.main()
