from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_sprite_atlas import build_atlas  # noqa: E402
from export_engine_manifest import export_manifests  # noqa: E402


class AssetPipelineTests(unittest.TestCase):
    def copy_factory_example(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        project = Path(temp_dir.name) / "factory-v2-shop"
        shutil.copytree(ROOT / "examples" / "factory-v2-shop", project)
        return temp_dir, project

    def test_builds_semantic_atlas(self) -> None:
        temp_dir, project = self.copy_factory_example()
        self.addCleanup(temp_dir.cleanup)

        data = build_atlas(
            project,
            project / "contracts" / "sprite-contract.yaml",
            project / "contracts" / "atlas-contract.yaml",
            force=True,
        )

        self.assertEqual(len(data["sprites"]), 9)
        self.assertIn("shop-buy-button-normal", data["sprites"])
        self.assertEqual(
            data["sprites"]["shop-buy-button-normal"]["slice"]["type"],
            "9-slice",
        )
        self.assertTrue((project / data["image"]).is_file())

    def test_exports_three_engine_manifests(self) -> None:
        temp_dir, project = self.copy_factory_example()
        self.addCleanup(temp_dir.cleanup)
        paths = export_manifests(
            project,
            project / "contracts" / "atlas-contract.yaml",
            project / "contracts" / "export-contract.yaml",
            force=True,
        )

        self.assertEqual(len(paths), 3)
        godot = json.loads((project / "exports/godot/shop-ui.json").read_text())
        unity = json.loads((project / "exports/unity/shop-ui.json").read_text())
        cocos = json.loads((project / "exports/cocos/shop-ui.json").read_text())
        self.assertEqual(godot["engine"], "godot")
        self.assertEqual(
            godot["resources"]["shop-buy-button-normal"]["patch_margins"],
            [36, 36, 28, 28],
        )
        self.assertEqual(unity["spriteMode"], "Multiple")
        self.assertIn("shop-buy-button-normal", cocos["frames"])


if __name__ == "__main__":
    unittest.main()
