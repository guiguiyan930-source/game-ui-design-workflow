#!/usr/bin/env python3
"""Split a sprite sheet into transparent PNG elements and a ZIP package."""

from __future__ import annotations

import argparse
import shutil
import statistics
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageChops, ImageFilter


@dataclass(frozen=True)
class SplitSettings:
    mode: str = "auto"
    alpha_threshold: int = 8
    background_tolerance: int = 24
    connect_gap: int = 2
    min_area: int = 64
    padding: int = 4
    prefix: str = "element"


def sample_background(image: Image.Image) -> tuple[int, int, int]:
    rgb = image.convert("RGB")
    width, height = rgb.size
    step_x = max(1, width // 128)
    step_y = max(1, height // 128)
    samples: list[tuple[int, int, int]] = []
    for x in range(0, width, step_x):
        samples.append(rgb.getpixel((x, 0)))
        samples.append(rgb.getpixel((x, height - 1)))
    for y in range(0, height, step_y):
        samples.append(rgb.getpixel((0, y)))
        samples.append(rgb.getpixel((width - 1, y)))
    return tuple(
        round(statistics.median(pixel[channel] for pixel in samples))
        for channel in range(3)
    )


def make_foreground_mask(
    image: Image.Image,
    settings: SplitSettings,
) -> tuple[Image.Image, str, tuple[int, int, int] | None]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    mode = settings.mode
    if mode == "auto":
        alpha_min, _ = alpha.getextrema()
        mode = "alpha" if alpha_min < 255 else "background"

    if mode == "alpha":
        mask = alpha.point(
            lambda value: 255 if value > settings.alpha_threshold else 0
        )
        return mask, mode, None
    if mode != "background":
        raise ValueError(f"unsupported split mode: {mode}")

    background = sample_background(rgba)
    solid = Image.new("RGB", rgba.size, background)
    red, green, blue = ImageChops.difference(rgba.convert("RGB"), solid).split()
    difference = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    mask = difference.point(
        lambda value: 255 if value > settings.background_tolerance else 0
    )
    visible_alpha = alpha.point(
        lambda value: 255 if value > settings.alpha_threshold else 0
    )
    return ImageChops.multiply(mask, visible_alpha), mode, background


def connected_boxes(mask: Image.Image, min_area: int) -> list[tuple[int, int, int, int]]:
    binary = mask.convert("L")
    width, height = binary.size
    pixels = binary.tobytes()
    parents: list[int] = []
    runs: list[tuple[int, int, int, int]] = []
    previous: list[tuple[int, int, int]] = []

    def new_label() -> int:
        label = len(parents)
        parents.append(label)
        return label

    def find(label: int) -> int:
        while parents[label] != label:
            parents[label] = parents[parents[label]]
            label = parents[label]
        return label

    def union(left: int, right: int) -> None:
        root_left = find(left)
        root_right = find(right)
        if root_left != root_right:
            parents[root_right] = root_left

    for y in range(height):
        row_offset = y * width
        current: list[tuple[int, int, int]] = []
        x = 0
        while x < width:
            while x < width and pixels[row_offset + x] == 0:
                x += 1
            if x >= width:
                break
            start = x
            while x < width and pixels[row_offset + x] != 0:
                x += 1
            end = x
            overlaps = [
                label
                for prev_start, prev_end, label in previous
                if prev_start < end and start < prev_end
            ]
            label = overlaps[0] if overlaps else new_label()
            for other in overlaps[1:]:
                union(label, other)
            current.append((start, end, label))
            runs.append((y, start, end, label))
        previous = current

    stats: dict[int, list[int]] = {}
    for y, start, end, label in runs:
        root = find(label)
        if root not in stats:
            stats[root] = [start, y, end, y + 1, end - start]
        else:
            item = stats[root]
            item[0] = min(item[0], start)
            item[1] = min(item[1], y)
            item[2] = max(item[2], end)
            item[3] = max(item[3], y + 1)
            item[4] += end - start

    boxes = [
        (left, top, right, bottom)
        for left, top, right, bottom, area in stats.values()
        if area >= min_area
    ]
    return sorted(boxes, key=lambda box: (box[1], box[0]))


def tighten_and_pad(
    box: tuple[int, int, int, int],
    mask: Image.Image,
    padding: int,
) -> tuple[int, int, int, int] | None:
    local = mask.crop(box).getbbox()
    if local is None:
        return None
    left = box[0] + local[0]
    top = box[1] + local[1]
    right = box[0] + local[2]
    bottom = box[1] + local[3]
    width, height = mask.size
    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def prepare_output(directory: Path, force: bool) -> None:
    if directory.exists() and any(directory.iterdir()):
        if not force:
            raise FileExistsError(
                f"output directory is not empty: {directory}; use --force"
            )
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)


def split_sprite_sheet(
    source: Path,
    output_dir: Path,
    zip_path: Path,
    settings: SplitSettings,
    force: bool = False,
) -> dict[str, Any]:
    if not source.is_file():
        raise FileNotFoundError(f"sprite sheet not found: {source}")
    prepare_output(output_dir, force)
    if zip_path.exists():
        if not force:
            raise FileExistsError(f"package already exists: {zip_path}; use --force")
        zip_path.unlink()
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    image = Image.open(source).convert("RGBA")
    original_mask, detected_mode, background = make_foreground_mask(image, settings)
    detection_mask = original_mask
    if settings.connect_gap > 0:
        size = settings.connect_gap * 2 + 1
        detection_mask = original_mask.filter(ImageFilter.MaxFilter(size))
    boxes = connected_boxes(detection_mask, settings.min_area)

    items: list[dict[str, Any]] = []
    for box in boxes:
        crop_box = tighten_and_pad(box, original_mask, settings.padding)
        if crop_box is None:
            continue
        crop = image.crop(crop_box)
        if detected_mode == "background":
            crop.putalpha(original_mask.crop(crop_box))
        index = len(items) + 1
        item_id = f"{settings.prefix}-{index:03d}"
        filename = f"{item_id}.png"
        path = output_dir / filename
        crop.save(path, "PNG", optimize=True)
        items.append(
            {
                "id": item_id,
                "path": filename,
                "bbox": [
                    crop_box[0],
                    crop_box[1],
                    crop_box[2] - crop_box[0],
                    crop_box[3] - crop_box[1],
                ],
                "dimensions": [crop.width, crop.height],
                "transparent_background": True,
            }
        )

    if not items:
        raise ValueError("no sprite elements detected; adjust mode or thresholds")

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "source_sheet": source.name,
        "detected_mode": detected_mode,
        "sampled_background": list(background) if background else None,
        "settings": {
            "alpha_threshold": settings.alpha_threshold,
            "background_tolerance": settings.background_tolerance,
            "connect_gap": settings.connect_gap,
            "min_area": settings.min_area,
            "padding": settings.padding,
        },
        "item_count": len(items),
        "items": items,
    }
    manifest_path = output_dir / "sprite-manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(manifest_path, "sprite-manifest.yaml")
        for item in items:
            path = output_dir / item["path"]
            archive.write(path, f"items/{path.name}")
    manifest["package"] = str(zip_path)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input sprite-sheet image.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory. Defaults to <source-stem>-items.",
    )
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        help="ZIP path. Defaults to <source-stem>-png.zip.",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "alpha", "background"),
        default="auto",
    )
    parser.add_argument("--alpha-threshold", type=int, default=8)
    parser.add_argument("--background-tolerance", type=int, default=24)
    parser.add_argument("--connect-gap", type=int, default=2)
    parser.add_argument("--min-area", type=int, default=64)
    parser.add_argument("--padding", type=int, default=4)
    parser.add_argument("--prefix", default="element")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else source.with_name(f"{source.stem}-items")
    )
    zip_path = (
        args.zip_path.resolve()
        if args.zip_path
        else source.with_name(f"{source.stem}-png.zip")
    )
    settings = SplitSettings(
        mode=args.mode,
        alpha_threshold=args.alpha_threshold,
        background_tolerance=args.background_tolerance,
        connect_gap=max(0, args.connect_gap),
        min_area=max(1, args.min_area),
        padding=max(0, args.padding),
        prefix=args.prefix,
    )
    try:
        manifest = split_sprite_sheet(
            source, output_dir, zip_path, settings, args.force
        )
    except (FileNotFoundError, FileExistsError, ValueError, OSError) as error:
        print(f"ERROR: {error}")
        return 2
    print(f"Split {manifest['item_count']} element(s) into: {output_dir}")
    print(f"Package: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
