from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.sh"


class InstallScriptTests(unittest.TestCase):
    def run_installer(
        self, *args: str, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(INSTALLER), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_installs_all_skills_into_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)

            result = self.run_installer("--project", str(project))

            self.assertEqual(result.returncode, 0, result.stderr)
            installed = sorted((project / ".cursor" / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(installed), 6)

    def test_existing_skills_are_skipped_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.assertEqual(
                self.run_installer("--project", str(project)).returncode,
                0,
            )

            result = self.run_installer("--project", str(project))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("0 installed, 6 skipped", result.stdout)

    def test_force_replaces_existing_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.run_installer("--project", str(project))
            stale = (
                project
                / ".cursor"
                / "skills"
                / "game-ui-workflow"
                / "stale.txt"
            )
            stale.write_text("old")

            result = self.run_installer("--project", str(project), "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(stale.exists())

    def test_dry_run_does_not_create_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)

            result = self.run_installer(
                "--project", str(project), "--dry-run"
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((project / ".cursor").exists())
            self.assertIn("WOULD INSTALL", result.stdout)

    def test_personal_install_uses_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            env = os.environ.copy()
            env["HOME"] = temp

            result = self.run_installer("--personal", env=env)

            self.assertEqual(result.returncode, 0, result.stderr)
            installed = sorted((Path(temp) / ".cursor" / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(installed), 6)


if __name__ == "__main__":
    unittest.main()
