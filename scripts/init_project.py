#!/usr/bin/env python3
"""Initialize a Spec-Kit workspace for a game UI project."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


PROJECT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create specs/<project-id> from repository templates."
    )
    parser.add_argument("project_id", help="Lowercase letters, numbers, and hyphens.")
    parser.add_argument(
        "--root",
        type=Path,
        help="Repository root. Defaults to the parent of this script directory.",
    )
    parser.add_argument(
        "--base-dir",
        default="specs",
        help="Project collection relative to root. Defaults to specs.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files; generated assets are never removed.",
    )
    return parser.parse_args()


def copy_template(source: Path, target: Path, project_id: str, force: bool) -> bool:
    if target.exists() and not force:
        return False
    text = source.read_text(encoding="utf-8").replace("{{PROJECT_ID}}", project_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return True


def initialize(
    root: Path, base_dir: str, project_id: str, force: bool
) -> tuple[Path, list[Path]]:
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError(
            "project_id must use lowercase letters, numbers, and single hyphens"
        )

    spec_templates = root / "templates" / "spec-kit"
    contract_templates = root / "templates" / "contracts"
    if not spec_templates.is_dir() or not contract_templates.is_dir():
        raise FileNotFoundError(f"templates not found under repository root: {root}")

    base_path = Path(base_dir)
    if base_path.is_absolute() or ".." in base_path.parts:
        raise ValueError("base_dir must be a safe path relative to the repository root")
    project_dir = root / base_path / project_id
    for relative in (
        "assets/pages",
        "assets/components",
        "prompts/pages",
        "prompts/components",
        "contracts",
    ):
        (project_dir / relative).mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for source in sorted(spec_templates.glob("*.md")):
        target = project_dir / source.name
        if copy_template(source, target, project_id, force):
            written.append(target)

    for source in sorted(contract_templates.glob("*.yaml")):
        target = project_dir / "contracts" / source.name
        if copy_template(source, target, project_id, force):
            written.append(target)

    for keep in (
        project_dir / "assets" / "pages" / ".gitkeep",
        project_dir / "assets" / "components" / ".gitkeep",
        project_dir / "prompts" / "pages" / ".gitkeep",
        project_dir / "prompts" / "components" / ".gitkeep",
    ):
        if not keep.exists():
            keep.touch()
            written.append(keep)

    return project_dir, written


def main() -> int:
    args = parse_args()
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    try:
        project_dir, written = initialize(
            root, args.base_dir, args.project_id, args.force
        )
    except (ValueError, FileNotFoundError) as error:
        print(f"ERROR: {error}")
        return 2

    print(f"Initialized: {project_dir}")
    print(f"Created or updated {len(written)} files.")
    if not written:
        print("No templates overwritten; use --force to refresh them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
