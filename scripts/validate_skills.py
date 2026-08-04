#!/usr/bin/env python3
"""Validate Cursor skill metadata, size, and local Markdown references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        return [f"{path}: missing YAML frontmatter"]
    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as error:
        return [f"{path}: invalid frontmatter: {error}"]
    if not isinstance(metadata, dict):
        return [f"{path}: frontmatter must be a mapping"]

    name = metadata.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append(f"{path}: invalid skill name {name!r}")
    elif name != path.parent.name:
        errors.append(f"{path}: name must match directory {path.parent.name!r}")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: description is required")
    elif len(description) > 1024:
        errors.append(f"{path}: description exceeds 1024 characters")
    if len(text.splitlines()) >= 500:
        errors.append(f"{path}: SKILL.md must stay under 500 lines")

    for target in LINK_PATTERN.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        local_target = target.split("#", 1)[0]
        if local_target and not (path.parent / local_target).exists():
            errors.append(f"{path}: missing linked file {target!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "skills",
    )
    args = parser.parse_args()
    paths = sorted(args.skills_dir.glob("*/SKILL.md"))
    if not paths:
        print(f"ERROR: no skills found under {args.skills_dir}")
        return 1

    errors = [error for path in paths for error in validate_skill(path)]
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print(f"OK: validated {len(paths)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
