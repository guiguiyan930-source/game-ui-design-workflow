from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import zipfile
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

    def test_guofeng_example_passes_strict_validation(self) -> None:
        report = validate(ROOT / "examples" / "guofeng-card-rpg", strict=True)

        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_factory_v2_example_passes_strict_validation(self) -> None:
        report = validate(ROOT / "examples" / "factory-v2-shop", strict=True)

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

    def test_detects_sprite_package_missing_item(self) -> None:
        temp_dir, project = self.copy_example()
        self.addCleanup(temp_dir.cleanup)
        package = project / "packages" / "home-ui-png.zip"
        replacement = project / "packages" / "replacement.zip"
        with zipfile.ZipFile(package) as source, zipfile.ZipFile(
            replacement, "w", zipfile.ZIP_DEFLATED
        ) as target:
            for name in source.namelist():
                if name != "items/home-ui-009.png":
                    target.writestr(name, source.read(name))
        replacement.replace(package)

        report = validate(project, strict=False)

        self.assertTrue(
            any("ZIP is missing item" in error for error in report.errors),
            report.errors,
        )

    def test_approved_sprite_pack_must_be_text_free(self) -> None:
        temp_dir, project = self.copy_example()
        self.addCleanup(temp_dir.cleanup)
        contract_path = project / "contracts" / "sprite-contract.yaml"
        contract = yaml.safe_load(contract_path.read_text())
        contract["review"]["text_free"] = False
        contract_path.write_text(yaml.safe_dump(contract, sort_keys=False))

        report = validate(project, strict=False)

        self.assertTrue(
            any("review.text_free=true" in error for error in report.errors),
            report.errors,
        )

    def test_detects_invalid_nine_slice_margins(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        project = Path(temp_dir.name) / "factory-v2-shop"
        shutil.copytree(ROOT / "examples" / "factory-v2-shop", project)
        contract_path = project / "contracts" / "component-contract.yaml"
        contract = yaml.safe_load(contract_path.read_text())
        contract["components"][0]["slice"]["margins"] = [200, 200, 10, 10]
        contract_path.write_text(yaml.safe_dump(contract, sort_keys=False))

        report = validate(project, strict=False)

        self.assertTrue(
            any("leave no stretchable center" in error for error in report.errors),
            report.errors,
        )


if __name__ == "__main__":
    unittest.main()
