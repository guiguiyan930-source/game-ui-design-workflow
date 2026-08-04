from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from split_sprite_sheet import SplitSettings, split_sprite_sheet  # noqa: E402


class SpriteSheetSplitterTests(unittest.TestCase):
    def test_splits_transparent_sheet_and_builds_zip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "transparent.png"
            image = Image.new("RGBA", (120, 70), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rectangle((8, 10, 35, 42), fill=(220, 50, 40, 255))
            draw.ellipse((72, 14, 105, 47), fill=(40, 120, 230, 220))
            image.save(source)

            manifest = split_sprite_sheet(
                source,
                root / "items",
                root / "pack.zip",
                SplitSettings(prefix="ui", min_area=20, padding=3),
            )

            self.assertEqual(manifest["detected_mode"], "alpha")
            self.assertEqual(manifest["item_count"], 2)
            self.assertTrue((root / "items" / "ui-001.png").is_file())
            self.assertTrue((root / "items" / "ui-002.png").is_file())
            with zipfile.ZipFile(root / "pack.zip") as archive:
                self.assertEqual(
                    sorted(archive.namelist()),
                    [
                        "items/ui-001.png",
                        "items/ui-002.png",
                        "sprite-manifest.yaml",
                    ],
                )

    def test_removes_solid_background_from_items(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "solid.png"
            image = Image.new("RGB", (100, 60), (248, 248, 248))
            draw = ImageDraw.Draw(image)
            draw.rectangle((10, 12, 32, 38), fill=(15, 80, 160))
            draw.rectangle((65, 8, 88, 34), fill=(180, 70, 30))
            image.save(source)

            manifest = split_sprite_sheet(
                source,
                root / "items",
                root / "pack.zip",
                SplitSettings(prefix="icon", min_area=20, padding=2),
            )

            self.assertEqual(manifest["detected_mode"], "background")
            self.assertEqual(manifest["sampled_background"], [248, 248, 248])
            self.assertEqual(manifest["item_count"], 2)
            output = Image.open(root / "items" / "icon-001.png").convert("RGBA")
            self.assertEqual(output.getchannel("A").getextrema(), (0, 255))

    def test_filters_small_noise(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "noise.png"
            image = Image.new("RGBA", (80, 50), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rectangle((10, 10, 35, 35), fill=(255, 255, 255, 255))
            draw.point((70, 45), fill=(255, 255, 255, 255))
            image.save(source)

            manifest = split_sprite_sheet(
                source,
                root / "items",
                root / "pack.zip",
                SplitSettings(min_area=20, connect_gap=0),
            )

            self.assertEqual(manifest["item_count"], 1)

    def test_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "sheet.png"
            image = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
            ImageDraw.Draw(image).rectangle(
                (10, 10, 30, 30), fill=(255, 255, 255, 255)
            )
            image.save(source)
            output = root / "items"
            package = root / "pack.zip"
            split_sprite_sheet(source, output, package, SplitSettings())

            with self.assertRaises(FileExistsError):
                split_sprite_sheet(source, output, package, SplitSettings())


if __name__ == "__main__":
    unittest.main()
