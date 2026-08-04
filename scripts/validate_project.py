#!/usr/bin/env python3
"""Validate a game UI Spec-Kit project and its cross-file contracts."""

from __future__ import annotations

import argparse
import re
import sys
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
        if component.get("category") not in {
            "background",
            "control",
            "container",
            "icon",
            "character",
            "decoration",
        }:
            report.error(f"{label}: invalid category {component.get('category')!r}")
        if not isinstance(component.get("transparent_background"), bool):
            report.error(f"{label}: transparent_background must be boolean")
        validate_dimensions(component.get("target_size"), f"{label}.target_size", report)
        require_list(component, "states", label, report)
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
        if kind not in {"page", "component"}:
            report.error(f"{label}: kind must be page or component")
        if asset.get("screen_id") not in screen_ids:
            report.error(f"{label}: unknown screen_id {asset.get('screen_id')!r}")
        component_id = asset.get("component_id")
        if kind == "component" and component_id not in component_ids:
            report.error(f"{label}: unknown component_id {component_id!r}")
        status = asset.get("status")
        if status not in {"pending-generation", "generated", "approved", "stale"}:
            report.error(f"{label}: invalid status {status!r}")
        validate_dimensions(asset.get("dimensions"), f"{label}.dimensions", report)
        if not isinstance(asset.get("transparent_background"), bool):
            report.error(f"{label}: transparent_background must be boolean")

        prompt_value = asset.get("prompt_path")
        prompt = project / str(prompt_value) if prompt_value else None
        if not prompt or not prompt.is_file():
            report.error(f"{label}: prompt_path does not exist: {prompt_value!r}")

        path_value = asset.get("path")
        output = project / str(path_value) if path_value else None
        if status in {"generated", "approved"} and (not output or not output.is_file()):
            report.error(f"{label}: generated asset path does not exist: {path_value!r}")
        if asset.get("approved") is True and status != "approved":
            report.error(f"{label}: approved=true requires status=approved")


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
