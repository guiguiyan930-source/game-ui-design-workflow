#!/usr/bin/env python3
"""Pack semantic sprite PNG files into an atlas image and JSON metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from PIL import Image


def next_power_of_two(value: int) -> int:
    return 1 if value <= 1 else 1 << (value - 1).bit_length()


def relative_to_project(path: Path, project: Path) -> str:
    try:
        return str(path.resolve().relative_to(project.resolve()))
    except ValueError:
        return str(path.resolve())


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return value


def pack_items(
    project: Path,
    items: list[dict[str, Any]],
    max_size: tuple[int, int],
    padding: int,
    power_of_two: bool,
) -> tuple[Image.Image, list[dict[str, Any]]]:
    loaded: list[tuple[dict[str, Any], Image.Image]] = []
    names: set[str] = set()
    for index, item in enumerate(items):
        name = item.get("semantic_name") or item.get("id")
        if not isinstance(name, str) or not name:
            raise ValueError(f"sprite item {index} requires semantic_name or id")
        if name in names:
            raise ValueError(f"duplicate semantic sprite name: {name}")
        names.add(name)
        path_value = item.get("path")
        path = project / str(path_value) if path_value else None
        if not path or not path.is_file():
            raise FileNotFoundError(f"sprite PNG not found: {path_value!r}")
        loaded.append((item, Image.open(path).convert("RGBA")))

    loaded.sort(key=lambda pair: (-pair[1].height, -pair[1].width, str(pair[0].get("id"))))
    max_width, max_height = max_size
    cursor_x = padding
    cursor_y = padding
    row_height = 0
    packed: list[dict[str, Any]] = []
    placements: list[tuple[Image.Image, int, int]] = []
    used_width = 0
    used_height = 0
    for item, image in loaded:
        if image.width + padding * 2 > max_width:
            raise ValueError(f"sprite is wider than atlas: {item.get('id')}")
        if cursor_x + image.width + padding > max_width:
            cursor_x = padding
            cursor_y += row_height + padding
            row_height = 0
        if cursor_y + image.height + padding > max_height:
            raise ValueError("sprites do not fit within configured atlas max_size")
        placements.append((image, cursor_x, cursor_y))
        entry = {
            "id": item.get("id"),
            "semantic_name": item.get("semantic_name") or item.get("id"),
            "component_id": item.get("component_id"),
            "state": item.get("state", "default"),
            "source_path": item.get("path"),
            "region": [cursor_x, cursor_y, image.width, image.height],
            "pivot": [0.5, 0.5],
            "rotated": False,
        }
        if "slice" in item:
            entry["slice"] = item["slice"]
        packed.append(entry)
        cursor_x += image.width + padding
        row_height = max(row_height, image.height)
        used_width = max(used_width, cursor_x)
        used_height = max(used_height, cursor_y + image.height + padding)

    width = next_power_of_two(used_width) if power_of_two else used_width
    height = next_power_of_two(used_height) if power_of_two else used_height
    if width > max_width or height > max_height:
        raise ValueError("power-of-two atlas exceeds configured max_size")
    atlas = Image.new("RGBA", (max(1, width), max(1, height)), (0, 0, 0, 0))
    for image, x, y in placements:
        atlas.alpha_composite(image, (x, y))
    return atlas, packed


def build_atlas(
    project: Path,
    sprite_contract_path: Path,
    atlas_contract_path: Path,
    force: bool = False,
) -> dict[str, Any]:
    sprite = load_yaml(sprite_contract_path)
    atlas_contract = load_yaml(atlas_contract_path)
    settings = atlas_contract.get("settings", {})
    output = atlas_contract.get("output", {})
    if not isinstance(settings, dict) or not isinstance(output, dict):
        raise ValueError("atlas contract requires settings and output mappings")
    max_size_value = settings.get("max_size")
    if (
        not isinstance(max_size_value, list)
        or len(max_size_value) != 2
        or not all(isinstance(value, int) and value > 0 for value in max_size_value)
    ):
        raise ValueError("atlas settings.max_size must contain two positive integers")
    padding = settings.get("padding")
    if not isinstance(padding, int) or padding < 0:
        raise ValueError("atlas settings.padding must be non-negative")
    if settings.get("allow_rotation") is not False:
        raise ValueError("built-in atlas packing does not rotate sprites")

    image_path = project / str(output.get("image_path", ""))
    data_path = project / str(output.get("data_path", ""))
    for path in (image_path, data_path):
        if path.exists() and not force:
            raise FileExistsError(f"output already exists: {path}; use --force")
        path.parent.mkdir(parents=True, exist_ok=True)

    atlas, packed = pack_items(
        project,
        sprite.get("items", []),
        (max_size_value[0], max_size_value[1]),
        padding,
        settings.get("power_of_two") is True,
    )
    atlas.save(image_path, "PNG", optimize=True)
    sprites = {item["semantic_name"]: item for item in packed}
    data = {
        "schema_version": 1,
        "atlas_id": atlas_contract.get("atlas_id"),
        "image": relative_to_project(image_path, project),
        "size": [atlas.width, atlas.height],
        "sprites": sprites,
    }
    data_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    atlas_contract["status"] = "packed"
    atlas_contract["source_sprite_pack"] = sprite.get("pack_id")
    atlas_contract["items"] = packed
    atlas_contract_path.write_text(
        yaml.safe_dump(atlas_contract, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--sprite-contract",
        type=Path,
        help="Defaults to <project>/contracts/sprite-contract.yaml.",
    )
    parser.add_argument(
        "--atlas-contract",
        type=Path,
        help="Defaults to <project>/contracts/atlas-contract.yaml.",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = args.project.resolve()
    sprite_contract = (
        args.sprite_contract.resolve()
        if args.sprite_contract
        else project / "contracts" / "sprite-contract.yaml"
    )
    atlas_contract = (
        args.atlas_contract.resolve()
        if args.atlas_contract
        else project / "contracts" / "atlas-contract.yaml"
    )
    try:
        data = build_atlas(
            project,
            sprite_contract,
            atlas_contract,
            args.force,
        )
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"ERROR: {error}")
        return 2
    print(f"Packed {len(data['sprites'])} sprite(s) into {data['image']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
