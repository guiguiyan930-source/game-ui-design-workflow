#!/usr/bin/env python3
"""Validate a game UI Spec-Kit project and its cross-file contracts."""

from __future__ import annotations

import argparse
import json
import re
import struct
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Run: python3 -m pip install -r requirements.txt")
    raise SystemExit(2)


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_FILES = ("spec.md", "research.md", "plan.md", "tasks.md", "quickstart.md")
CONTRACT_FILES = (
    "style-contract.yaml",
    "screen-contract.yaml",
    "component-contract.yaml",
    "asset-manifest.yaml",
)
OPTIONAL_CONTRACT_FILES = (
    "sprite-contract.yaml",
    "atlas-contract.yaml",
    "export-contract.yaml",
)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat incomplete draft values and warnings as validation errors.",
    )
    return parser.parse_args()


def load_yaml(path: Path, report: Report) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        report.error(f"{path}: invalid YAML: {error}")
        return {}
    if not isinstance(value, dict):
        report.error(f"{path}: YAML root must be a mapping")
        return {}
    return value


def require_mapping(
    value: dict[str, Any], key: str, source: str, report: Report
) -> dict[str, Any]:
    item = value.get(key)
    if not isinstance(item, dict):
        report.error(f"{source}: '{key}' must be a mapping")
        return {}
    return item


def require_list(
    value: dict[str, Any], key: str, source: str, report: Report
) -> list[Any]:
    item = value.get(key)
    if not isinstance(item, list):
        report.error(f"{source}: '{key}' must be a list")
        return []
    return item


def validate_id(value: Any, label: str, report: Report) -> bool:
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
        report.error(f"{label}: expected lowercase kebab-case ID, got {value!r}")
        return False
    return True


def validate_dimensions(value: Any, label: str, report: Report) -> None:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or not all(isinstance(item, int) and item > 0 for item in value)
    ):
        report.error(f"{label}: dimensions must be two positive integers")


def inspect_png(path: Path) -> tuple[list[int], bool]:
    with path.open("rb") as stream:
        header = stream.read(33)
        if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("invalid PNG signature or IHDR")
        width, height = struct.unpack(">II", header[16:24])
        color_type = header[25]
        has_alpha = color_type in {4, 6}
        while True:
            length_bytes = stream.read(4)
            if len(length_bytes) != 4:
                break
            length = struct.unpack(">I", length_bytes)[0]
            chunk_type = stream.read(4)
            if chunk_type == b"tRNS":
                has_alpha = True
            stream.seek(length + 4, 1)
            if chunk_type == b"IEND":
                break
    return [width, height], has_alpha


def parse_svg_length(value: str | None) -> int | None:
    if not value:
        return None
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(?:px)?\s*", value)
    return round(float(match.group(1))) if match else None


def inspect_svg(path: Path) -> tuple[list[int], bool]:
    root = ET.parse(path).getroot()
    width = parse_svg_length(root.get("width"))
    height = parse_svg_length(root.get("height"))
    if width is None or height is None:
        view_box = root.get("viewBox", "").replace(",", " ").split()
        if len(view_box) == 4:
            width = round(float(view_box[2]))
            height = round(float(view_box[3]))
    if width is None or height is None or width <= 0 or height <= 0:
        raise ValueError("SVG requires positive width/height or viewBox")
    return [width, height], True


def inspect_image(path: Path) -> tuple[list[int], bool] | None:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return inspect_png(path)
    if suffix == ".svg":
        return inspect_svg(path)
    return None


def validate_markdown(project: Path, report: Report) -> None:
    for name in MARKDOWN_FILES:
        path = project / name
        if not path.is_file():
            report.error(f"missing required document: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if "{{PROJECT_ID}}" in text:
            report.error(f"{path}: unresolved PROJECT_ID placeholder")
        if not text.strip():
            report.error(f"{path}: document is empty")


def validate_contract_headers(
    contracts: dict[str, dict[str, Any]], project_id: str, report: Report
) -> None:
    for name, data in contracts.items():
        if data.get("schema_version") != 1:
            report.error(f"{name}: schema_version must be 1")
        if data.get("project_id") != project_id:
            report.error(
                f"{name}: project_id {data.get('project_id')!r} "
                f"does not match directory {project_id!r}"
            )


def validate_style(style: dict[str, Any], report: Report) -> None:
    source = "style-contract.yaml"
    if style.get("status") not in {"draft", "approved"}:
        report.error(f"{source}: status must be draft or approved")
    for key in ("platform", "visual", "colors", "typography", "geometry", "effects"):
        require_mapping(style, key, source, report)
    platform = style.get("platform", {})
    if isinstance(platform, dict):
        validate_dimensions(platform.get("reference_size"), f"{source}: reference_size", report)
    visual = style.get("visual", {})
    colors = style.get("colors", {})
    incomplete = []
    if isinstance(visual, dict):
        incomplete.extend(
            f"visual.{key}" for key in ("theme", "mood") if not visual.get(key)
        )
    if isinstance(colors, dict):
        incomplete.extend(f"colors.{key}" for key, value in colors.items() if not value)
    tokens = style.get("tokens")
    if tokens is not None:
        if not isinstance(tokens, dict):
            report.error(f"{source}: tokens must be a mapping")
        else:
            for group, values in tokens.items():
                if not isinstance(values, dict):
                    report.error(f"{source}: tokens.{group} must be a mapping")
    if incomplete:
        report.warn(f"{source}: incomplete draft values: {', '.join(incomplete)}")


def validate_screens(
    screen_contract: dict[str, Any], report: Report
) -> tuple[set[str], dict[str, str]]:
    screens = require_list(screen_contract, "screens", "screen-contract.yaml", report)
    ids: set[str] = set()
    statuses: dict[str, str] = {}
    for index, screen in enumerate(screens):
        label = f"screen-contract.yaml: screens[{index}]"
        if not isinstance(screen, dict):
            report.error(f"{label}: must be a mapping")
            continue
        screen_id = screen.get("id")
        if not validate_id(screen_id, f"{label}.id", report):
            continue
        if screen_id in ids:
            report.error(f"{label}: duplicate screen ID {screen_id!r}")
        ids.add(screen_id)
        statuses[screen_id] = str(screen.get("status", ""))
        if screen.get("priority") not in {"must-have", "genre-specific", "optional"}:
            report.error(f"{label}: invalid priority {screen.get('priority')!r}")
        for key in ("entry_points", "primary_actions", "dependencies", "components", "states"):
            require_list(screen, key, label, report)
        output = require_mapping(screen, "output", label, report)
        for key in ("brief", "prompt", "image"):
            if key not in output:
                report.error(f"{label}.output: missing '{key}'")
    return ids, statuses


COMPONENT_CATEGORIES = {
    "background",
    "button",
    "frame",
    "panel",
    "card",
    "icon",
    "badge",
    "progress",
    "popup",
    "decoration",
    "currency",
    "character",
    "npc",
    "texture",
    "control",
    "container",
}
SLICE_TYPES = {"9-slice", "full", "1:1", "tile"}


def validate_slice(
    value: Any,
    dimensions: Any,
    label: str,
    report: Report,
) -> None:
    if not isinstance(value, dict):
        report.error(f"{label}: slice must be a mapping")
        return
    if value.get("type") not in SLICE_TYPES:
        report.error(f"{label}: invalid slice type {value.get('type')!r}")
    margins = value.get("margins")
    if (
        not isinstance(margins, list)
        or len(margins) != 4
        or not all(isinstance(item, int) and item >= 0 for item in margins)
    ):
        report.error(f"{label}: slice margins must be four non-negative integers")
        return
    if (
        value.get("type") == "9-slice"
        and isinstance(dimensions, list)
        and len(dimensions) == 2
        and all(isinstance(item, int) and item > 0 for item in dimensions)
    ):
        left, right, top, bottom = margins
        if left + right >= dimensions[0] or top + bottom >= dimensions[1]:
            report.error(f"{label}: 9-slice margins leave no stretchable center")


def validate_components(
    component_contract: dict[str, Any],
    screen_ids: set[str],
    report: Report,
) -> set[str]:
    source_screen_id = component_contract.get("source_screen_id")
    if source_screen_id not in screen_ids:
        report.error(
            "component-contract.yaml: source_screen_id must reference a known screen"
        )
    components = require_list(
        component_contract, "components", "component-contract.yaml", report
    )
    ids: set[str] = set()
    for index, component in enumerate(components):
        label = f"component-contract.yaml: components[{index}]"
        if not isinstance(component, dict):
            report.error(f"{label}: must be a mapping")
            continue
        component_id = component.get("id")
        if not validate_id(component_id, f"{label}.id", report):
            continue
        if component_id in ids:
            report.error(f"{label}: duplicate component ID {component_id!r}")
        ids.add(component_id)
        if component.get("category") not in COMPONENT_CATEGORIES:
            report.error(f"{label}: invalid category {component.get('category')!r}")
        if not isinstance(component.get("transparent_background"), bool):
            report.error(f"{label}: transparent_background must be boolean")
        validate_dimensions(component.get("target_size"), f"{label}.target_size", report)
        require_list(component, "states", label, report)
        if "slice" in component:
            validate_slice(
                component.get("slice"),
                component.get("target_size"),
                f"{label}.slice",
                report,
            )
        if "atlas_group" in component:
            validate_id(component.get("atlas_group"), f"{label}.atlas_group", report)
        if "export_targets" in component:
            targets = require_list(component, "export_targets", label, report)
            for target in targets:
                if target not in {"godot", "unity", "cocos", "generic"}:
                    report.error(f"{label}: invalid export target {target!r}")
    return ids


def validate_assets(
    project: Path,
    manifest: dict[str, Any],
    screen_ids: set[str],
    component_ids: set[str],
    report: Report,
) -> None:
    assets = require_list(manifest, "assets", "asset-manifest.yaml", report)
    ids: set[str] = set()
    for index, asset in enumerate(assets):
        label = f"asset-manifest.yaml: assets[{index}]"
        if not isinstance(asset, dict):
            report.error(f"{label}: must be a mapping")
            continue
        asset_id = asset.get("id")
        if not validate_id(asset_id, f"{label}.id", report):
            continue
        if asset_id in ids:
            report.error(f"{label}: duplicate asset ID {asset_id!r}")
        ids.add(asset_id)
        kind = asset.get("kind")
        if kind not in {"page", "component", "sprite-sheet", "package"}:
            report.error(
                f"{label}: kind must be page, component, sprite-sheet, or package"
            )
        if asset.get("screen_id") not in screen_ids:
            report.error(f"{label}: unknown screen_id {asset.get('screen_id')!r}")
        component_id = asset.get("component_id")
        if kind == "component" and component_id not in component_ids:
            report.error(f"{label}: unknown component_id {component_id!r}")
        status = asset.get("status")
        if status not in {"pending-generation", "generated", "approved", "stale"}:
            report.error(f"{label}: invalid status {status!r}")
        if kind != "package":
            validate_dimensions(asset.get("dimensions"), f"{label}.dimensions", report)
            if not isinstance(asset.get("transparent_background"), bool):
                report.error(f"{label}: transparent_background must be boolean")

        prompt_value = asset.get("prompt_path")
        prompt = project / str(prompt_value) if prompt_value else None
        if kind != "package" and (not prompt or not prompt.is_file()):
            report.error(f"{label}: prompt_path does not exist: {prompt_value!r}")

        path_value = asset.get("path")
        output = project / str(path_value) if path_value else None
        if status in {"generated", "approved"} and (not output or not output.is_file()):
            report.error(f"{label}: generated asset path does not exist: {path_value!r}")
        if (
            kind != "package"
            and output
            and output.is_file()
            and status in {"generated", "approved"}
        ):
            try:
                inspection = inspect_image(output)
            except (OSError, ValueError, ET.ParseError) as error:
                report.error(f"{label}: cannot inspect {path_value!r}: {error}")
            else:
                if inspection is None:
                    report.warn(
                        f"{label}: actual dimensions and alpha are not checked "
                        f"for {output.suffix or 'extensionless files'}"
                    )
                else:
                    actual_dimensions, has_alpha = inspection
                    if actual_dimensions != asset.get("dimensions"):
                        report.error(
                            f"{label}: manifest dimensions {asset.get('dimensions')!r} "
                            f"do not match actual {actual_dimensions!r}"
                        )
                    if asset.get("transparent_background") is True and not has_alpha:
                        report.error(
                            f"{label}: transparent_background=true but the file "
                            "has no alpha channel"
                        )
        if asset.get("approved") is True and status != "approved":
            report.error(f"{label}: approved=true requires status=approved")


def validate_sprite_contract(
    project: Path,
    sprite: dict[str, Any],
    screen_ids: set[str],
    component_ids: set[str],
    report: Report,
) -> None:
    source_name = "sprite-contract.yaml"
    if sprite.get("status") not in {"draft", "generated", "approved", "stale"}:
        report.error(f"{source_name}: invalid status {sprite.get('status')!r}")
    validate_id(sprite.get("pack_id"), f"{source_name}: pack_id", report)
    if sprite.get("text_policy") != "remove-all":
        report.error(f"{source_name}: text_policy must be remove-all")
    source = require_mapping(sprite, "source", source_name, report)
    detection = require_mapping(sprite, "detection", source_name, report)
    output = require_mapping(sprite, "output", source_name, report)
    items = require_list(sprite, "items", source_name, report)
    review = require_mapping(sprite, "review", source_name, report)
    semantic_mapping = sprite.get("semantic_mapping", {})
    semantic_required = (
        isinstance(semantic_mapping, dict)
        and semantic_mapping.get("required") is True
    )

    screen_id = source.get("screen_id")
    if screen_id not in screen_ids:
        report.error(f"{source_name}: unknown source screen_id {screen_id!r}")
    if detection.get("mode") not in {"auto", "alpha", "background"}:
        report.error(f"{source_name}: invalid detection mode")
    for key in (
        "alpha_threshold",
        "background_tolerance",
        "connect_gap",
        "min_area",
        "padding",
    ):
        if not isinstance(detection.get(key), int) or detection[key] < 0:
            report.error(f"{source_name}: detection.{key} must be non-negative")

    item_ids: set[str] = set()
    for index, item in enumerate(items):
        label = f"{source_name}: items[{index}]"
        if not isinstance(item, dict):
            report.error(f"{label}: must be a mapping")
            continue
        item_id = item.get("id")
        if not validate_id(item_id, f"{label}.id", report):
            continue
        if item_id in item_ids:
            report.error(f"{label}: duplicate item ID {item_id!r}")
        item_ids.add(item_id)
        bbox = item.get("bbox")
        if (
            not isinstance(bbox, list)
            or len(bbox) != 4
            or not all(isinstance(value, int) and value >= 0 for value in bbox)
            or bbox[2] <= 0
            or bbox[3] <= 0
        ):
            report.error(f"{label}: bbox must be [x, y, width, height]")
        validate_dimensions(item.get("dimensions"), f"{label}.dimensions", report)
        if semantic_required:
            if item.get("component_id") not in component_ids:
                report.error(f"{label}: component_id must reference a known component")
            validate_id(item.get("semantic_name"), f"{label}.semantic_name", report)
            if item.get("category") not in COMPONENT_CATEGORIES:
                report.error(f"{label}: invalid category {item.get('category')!r}")
            if not isinstance(item.get("state"), str) or not item.get("state"):
                report.error(f"{label}: state is required")
            validate_slice(
                item.get("slice"),
                item.get("dimensions"),
                f"{label}.slice",
                report,
            )
        path_value = item.get("path")
        path = project / str(path_value) if path_value else None
        if sprite.get("status") in {"generated", "approved"}:
            if not path or not path.is_file():
                report.error(f"{label}: PNG path does not exist: {path_value!r}")
            else:
                inspection = inspect_image(path)
                if inspection is None or path.suffix.lower() != ".png":
                    report.error(f"{label}: sprite item must be a PNG")
                else:
                    dimensions, has_alpha = inspection
                    if dimensions != item.get("dimensions"):
                        report.error(
                            f"{label}: dimensions {item.get('dimensions')!r} "
                            f"do not match actual {dimensions!r}"
                        )
                    if not has_alpha:
                        report.error(f"{label}: sprite PNG has no alpha channel")

    status = sprite.get("status")
    if status in {"generated", "approved"}:
        if not items:
            report.error(f"{source_name}: generated packs require items")
        sheet_value = source.get("sheet_path")
        sheet = project / str(sheet_value) if sheet_value else None
        if not sheet or not sheet.is_file():
            report.error(
                f"{source_name}: source sheet does not exist: {sheet_value!r}"
            )
        manifest_value = output.get("manifest_path")
        sprite_manifest = (
            project / str(manifest_value) if manifest_value else None
        )
        if not sprite_manifest or not sprite_manifest.is_file():
            report.error(
                f"{source_name}: split manifest does not exist: {manifest_value!r}"
            )
        package_value = output.get("package_path")
        package = project / str(package_value) if package_value else None
        if not package or not package.is_file():
            report.error(
                f"{source_name}: package_path does not exist: {package_value!r}"
            )
        elif not zipfile.is_zipfile(package):
            report.error(f"{source_name}: package is not a valid ZIP")
        else:
            with zipfile.ZipFile(package) as archive:
                names = set(archive.namelist())
            if "sprite-manifest.yaml" not in names:
                report.error(f"{source_name}: ZIP is missing sprite-manifest.yaml")
            for item in items:
                expected = f"items/{Path(str(item.get('path'))).name}"
                if expected not in names:
                    report.error(
                        f"{source_name}: ZIP is missing item {expected!r}"
                    )
    if status == "approved" and review.get("complete") is not True:
        report.error(f"{source_name}: approved packs require review.complete=true")
    if status == "approved" and review.get("text_free") is not True:
        report.error(f"{source_name}: approved packs require review.text_free=true")


def validate_atlas_contract(
    project: Path,
    atlas: dict[str, Any],
    component_ids: set[str],
    report: Report,
) -> str | None:
    source_name = "atlas-contract.yaml"
    status = atlas.get("status")
    if status not in {"draft", "packed", "approved", "stale"}:
        report.error(f"{source_name}: invalid status {status!r}")
    atlas_id = atlas.get("atlas_id")
    if not validate_id(atlas_id, f"{source_name}: atlas_id", report):
        atlas_id = None
    settings = require_mapping(atlas, "settings", source_name, report)
    output = require_mapping(atlas, "output", source_name, report)
    items = require_list(atlas, "items", source_name, report)
    review = require_mapping(atlas, "review", source_name, report)
    validate_dimensions(settings.get("max_size"), f"{source_name}: max_size", report)
    if not isinstance(settings.get("padding"), int) or settings["padding"] < 0:
        report.error(f"{source_name}: settings.padding must be non-negative")
    if settings.get("allow_rotation") is not False:
        report.error(f"{source_name}: allow_rotation must be false")

    semantic_names: set[str] = set()
    for index, item in enumerate(items):
        label = f"{source_name}: items[{index}]"
        if not isinstance(item, dict):
            report.error(f"{label}: must be a mapping")
            continue
        semantic_name = item.get("semantic_name")
        if validate_id(semantic_name, f"{label}.semantic_name", report):
            if semantic_name in semantic_names:
                report.error(f"{label}: duplicate semantic_name {semantic_name!r}")
            semantic_names.add(semantic_name)
        if item.get("component_id") not in component_ids:
            report.error(f"{label}: component_id must reference a known component")
        region = item.get("region")
        if (
            not isinstance(region, list)
            or len(region) != 4
            or not all(isinstance(value, int) and value >= 0 for value in region)
            or region[2] <= 0
            or region[3] <= 0
        ):
            report.error(f"{label}: region must be [x, y, width, height]")
        if "slice" in item:
            dimensions = region[2:] if isinstance(region, list) and len(region) == 4 else None
            validate_slice(item.get("slice"), dimensions, f"{label}.slice", report)

    if status in {"packed", "approved"}:
        image_value = output.get("image_path")
        data_value = output.get("data_path")
        image = project / str(image_value) if image_value else None
        data = project / str(data_value) if data_value else None
        if not image or not image.is_file():
            report.error(f"{source_name}: atlas image does not exist: {image_value!r}")
        if not data or not data.is_file():
            report.error(f"{source_name}: atlas data does not exist: {data_value!r}")
        else:
            try:
                parsed = json.loads(data.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                report.error(f"{source_name}: invalid atlas JSON: {error}")
            else:
                if not isinstance(parsed, dict) or not isinstance(parsed.get("sprites"), dict):
                    report.error(f"{source_name}: atlas JSON requires a sprites mapping")
        if not items:
            report.error(f"{source_name}: packed atlases require items")
    if status == "approved" and review.get("complete") is not True:
        report.error(f"{source_name}: approved atlases require review.complete=true")
    return atlas_id if isinstance(atlas_id, str) else None


def validate_export_contract(
    project: Path,
    export: dict[str, Any],
    atlas_id: str | None,
    report: Report,
) -> None:
    source_name = "export-contract.yaml"
    status = export.get("status")
    if status not in {"draft", "generated", "approved", "stale"}:
        report.error(f"{source_name}: invalid status {status!r}")
    if atlas_id and export.get("source_atlas_id") != atlas_id:
        report.error(f"{source_name}: source_atlas_id must match atlas-contract")
    targets = require_list(export, "targets", source_name, report)
    review = require_mapping(export, "review", source_name, report)
    for index, target in enumerate(targets):
        label = f"{source_name}: targets[{index}]"
        if not isinstance(target, dict):
            report.error(f"{label}: must be a mapping")
            continue
        if target.get("engine") not in {"godot", "unity", "cocos", "generic"}:
            report.error(f"{label}: invalid engine {target.get('engine')!r}")
        if target.get("format") != "json-manifest":
            report.error(f"{label}: format must be json-manifest")
        if not isinstance(target.get("native_project_files"), bool):
            report.error(f"{label}: native_project_files must be boolean")
        if target.get("native_project_files") is True:
            report.warn(
                f"{label}: native engine files are not generated by the built-in exporter"
            )
        if status in {"generated", "approved"}:
            path_value = target.get("manifest_path")
            path = project / str(path_value) if path_value else None
            if not path or not path.is_file():
                report.error(f"{label}: manifest does not exist: {path_value!r}")
            else:
                try:
                    parsed = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as error:
                    report.error(f"{label}: invalid JSON manifest: {error}")
                else:
                    if parsed.get("engine") != target.get("engine"):
                        report.error(f"{label}: JSON engine does not match contract")
    if status == "approved" and review.get("complete") is not True:
        report.error(f"{source_name}: approved exports require review.complete=true")


def validate(project: Path, strict: bool) -> Report:
    report = Report()
    if not project.is_dir():
        report.error(f"project directory does not exist: {project}")
        return report
    project_id = project.name
    validate_id(project_id, "project directory", report)
    validate_markdown(project, report)

    contracts: dict[str, dict[str, Any]] = {}
    for name in CONTRACT_FILES:
        path = project / "contracts" / name
        if not path.is_file():
            report.error(f"missing required contract: {path}")
            contracts[name] = {}
        else:
            contracts[name] = load_yaml(path, report)
    for name in OPTIONAL_CONTRACT_FILES:
        path = project / "contracts" / name
        if path.is_file():
            contracts[name] = load_yaml(path, report)

    validate_contract_headers(contracts, project_id, report)
    validate_style(contracts["style-contract.yaml"], report)
    screen_ids, _ = validate_screens(contracts["screen-contract.yaml"], report)
    component_ids = validate_components(
        contracts["component-contract.yaml"], screen_ids, report
    )
    validate_assets(
        project,
        contracts["asset-manifest.yaml"],
        screen_ids,
        component_ids,
        report,
    )
    if "sprite-contract.yaml" in contracts:
        validate_sprite_contract(
            project,
            contracts["sprite-contract.yaml"],
            screen_ids,
            component_ids,
            report,
        )
    atlas_id = None
    if "atlas-contract.yaml" in contracts:
        atlas_id = validate_atlas_contract(
            project,
            contracts["atlas-contract.yaml"],
            component_ids,
            report,
        )
    if "export-contract.yaml" in contracts:
        validate_export_contract(
            project,
            contracts["export-contract.yaml"],
            atlas_id,
            report,
        )
    if strict and report.warnings:
        report.errors.extend(f"strict: {warning}" for warning in report.warnings)
    return report


def main() -> int:
    args = parse_args()
    report = validate(args.project_dir.resolve(), args.strict)
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")
    if report.errors:
        print(f"FAILED: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1
    print(f"OK: {args.project_dir} ({len(report.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
