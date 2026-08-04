#!/usr/bin/env python3
"""Export deterministic Godot, Unity, Cocos, or generic JSON atlas manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def margins(item: dict[str, Any]) -> list[int]:
    slice_value = item.get("slice", {})
    if isinstance(slice_value, dict) and slice_value.get("type") == "9-slice":
        value = slice_value.get("margins")
        if (
            isinstance(value, list)
            and len(value) == 4
            and all(isinstance(part, int) and part >= 0 for part in value)
        ):
            return value
    return [0, 0, 0, 0]


def export_godot(atlas: dict[str, Any]) -> dict[str, Any]:
    resources = {}
    for name, item in atlas["sprites"].items():
        resources[name] = {
            "texture": atlas["image"],
            "region": item["region"],
            "patch_margins": margins(item),
            "component_id": item.get("component_id"),
            "state": item.get("state"),
        }
    return {"texture": atlas["image"], "resources": resources}


def export_unity(atlas: dict[str, Any]) -> dict[str, Any]:
    sprites = []
    for name, item in atlas["sprites"].items():
        sprites.append(
            {
                "name": name,
                "rect": item["region"],
                "pivot": item.get("pivot", [0.5, 0.5]),
                "border": margins(item),
                "pixelsPerUnit": 100,
            }
        )
    return {"texture": atlas["image"], "spriteMode": "Multiple", "sprites": sprites}


def export_cocos(atlas: dict[str, Any]) -> dict[str, Any]:
    frames = {}
    for name, item in atlas["sprites"].items():
        x, y, width, height = item["region"]
        frames[name] = {
            "rect": {"x": x, "y": y, "width": width, "height": height},
            "offset": {"x": 0, "y": 0},
            "originalSize": {"width": width, "height": height},
            "capInsets": margins(item),
        }
    return {"texture": atlas["image"], "frames": frames}


def export_generic(atlas: dict[str, Any]) -> dict[str, Any]:
    return {"texture": atlas["image"], "sprites": atlas["sprites"]}


EXPORTERS = {
    "godot": export_godot,
    "unity": export_unity,
    "cocos": export_cocos,
    "generic": export_generic,
}


def export_manifests(
    project: Path,
    atlas_contract_path: Path,
    export_contract_path: Path,
    force: bool = False,
) -> list[Path]:
    atlas_contract = load_yaml(atlas_contract_path)
    export_contract = load_yaml(export_contract_path)
    atlas_output = atlas_contract.get("output", {})
    if not isinstance(atlas_output, dict):
        raise ValueError("atlas contract requires output mapping")
    atlas_data_path = project / str(atlas_output.get("data_path", ""))
    atlas = load_json(atlas_data_path)
    if not isinstance(atlas.get("sprites"), dict):
        raise ValueError("atlas JSON requires a sprites object")

    targets = export_contract.get("targets")
    if not isinstance(targets, list):
        raise ValueError("export contract requires targets list")
    written: list[Path] = []
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError("every export target must be a mapping")
        engine = target.get("engine")
        if engine not in EXPORTERS:
            raise ValueError(f"unsupported engine: {engine!r}")
        if target.get("native_project_files") is True:
            raise ValueError(
                f"{engine}: built-in exporter only writes JSON handoff manifests"
            )
        path_value = target.get("manifest_path")
        path = project / str(path_value) if path_value else None
        if not path:
            raise ValueError(f"{engine}: manifest_path is required")
        if path.exists() and not force:
            raise FileExistsError(f"output already exists: {path}; use --force")
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "engine": engine,
            "atlas_id": atlas.get("atlas_id"),
            "atlas_size": atlas.get("size"),
            **EXPORTERS[engine](atlas),
        }
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(path)

    export_contract["status"] = "generated"
    export_contract_path.write_text(
        yaml.safe_dump(export_contract, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--atlas-contract",
        type=Path,
        help="Defaults to <project>/contracts/atlas-contract.yaml.",
    )
    parser.add_argument(
        "--export-contract",
        type=Path,
        help="Defaults to <project>/contracts/export-contract.yaml.",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = args.project.resolve()
    atlas_contract = (
        args.atlas_contract.resolve()
        if args.atlas_contract
        else project / "contracts" / "atlas-contract.yaml"
    )
    export_contract = (
        args.export_contract.resolve()
        if args.export_contract
        else project / "contracts" / "export-contract.yaml"
    )
    try:
        paths = export_manifests(
            project,
            atlas_contract,
            export_contract,
            args.force,
        )
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"ERROR: {error}")
        return 2
    for path in paths:
        print(f"Exported: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
