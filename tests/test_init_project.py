from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from init_project import initialize  # noqa: E402


class InitProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        shutil.copytree(ROOT / "templates", self.root / "templates")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_initializes_all_documents_and_contracts(self) -> None:
        project, written = initialize(self.root, "specs", "test-game", False)

        self.assertEqual(project, self.root / "specs" / "test-game")
        self.assertGreaterEqual(len(written), 13)
        self.assertTrue((project / "spec.md").is_file())
        self.assertTrue((project / "contracts" / "style-contract.yaml").is_file())
        self.assertIn(
            "test-game",
            (project / "contracts" / "style-contract.yaml").read_text(),
        )
        self.assertNotIn("{{PROJECT_ID}}", (project / "spec.md").read_text())

    def test_rejects_invalid_project_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "project_id"):
            initialize(self.root, "specs", "Bad Project", False)

    def test_rejects_unsafe_base_directory(self) -> None:
        with self.assertRaisesRegex(ValueError, "base_dir"):
            initialize(self.root, "../outside", "test-game", False)

    def test_force_does_not_remove_generated_assets(self) -> None:
        project, _ = initialize(self.root, "specs", "test-game", False)
        asset = project / "assets" / "pages" / "existing.png"
        asset.write_bytes(b"generated")

        initialize(self.root, "specs", "test-game", True)

        self.assertEqual(asset.read_bytes(), b"generated")


if __name__ == "__main__":
    unittest.main()
