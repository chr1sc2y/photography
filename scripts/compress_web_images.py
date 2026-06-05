#!/usr/bin/env python3
"""Resize JPEG gallery sources to a web-friendly maximum width."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


JPEG_SUFFIXES = {".jpg", ".jpeg"}


def collect_images(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in JPEG_SUFFIXES
        and ".compress-tmp" not in path.parts
    )


def scaled_dimensions(width: int, height: int, max_width: int) -> tuple[int, int]:
    if width <= max_width:
        return width, height

    scaled_height = height * max_width / width
    even_height = max(2, int(round(scaled_height / 2)) * 2)
    return max_width, even_height


def require_tool(name: str) -> str:
    tool = shutil.which(name)
    if not tool:
        print(f"{name} is required but was not found in PATH.", file=sys.stderr)
        sys.exit(1)
    return tool


def image_dimensions(ffprobe: str, image: Path) -> tuple[int, int]:
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=s=x:p=0",
            str(image),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height = result.stdout.strip().split("x")
    return int(width), int(height)


def compress_one(ffmpeg: str, ffprobe: str, image: Path, max_width: int, quality: int) -> bool:
    width, height = image_dimensions(ffprobe, image)
    target_width, target_height = scaled_dimensions(width, height, max_width)
    if (target_width, target_height) == (width, height):
        print(f"skip {image} width={width}")
        return False

    temp_dir = image.parent / ".compress-tmp"
    temp_dir.mkdir(exist_ok=True)
    temp = temp_dir / image.name
    before = image.stat().st_size

    try:
        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(image),
                "-map_metadata",
                "0",
                "-vf",
                f"scale={target_width}:{target_height}:flags=lanczos",
                "-q:v",
                str(quality),
                str(temp),
            ],
            check=True,
        )
        temp.replace(image)
        after = image.stat().st_size
        print(f"compressed {image} {width}x{height} -> {target_width}x{target_height}, {before} -> {after}")
        return True
    finally:
        temp.unlink(missing_ok=True)
        try:
            temp_dir.rmdir()
        except OSError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photos_dir", type=Path, help="Directory containing JPEG images.")
    parser.add_argument("--max-width", type=int, default=2048, help="Maximum output width.")
    parser.add_argument(
        "--quality",
        type=int,
        default=3,
        help="FFmpeg JPEG quality, where lower is better. Default 3 is suitable for gallery use.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    photos_dir = args.photos_dir.resolve()
    if not photos_dir.exists():
        print(f"Image directory not found: {photos_dir}", file=sys.stderr)
        sys.exit(1)

    ffmpeg = require_tool("ffmpeg")
    ffprobe = require_tool("ffprobe")
    images = collect_images(photos_dir)
    changed = 0

    for image in images:
        if compress_one(ffmpeg, ffprobe, image, args.max_width, args.quality):
            changed += 1

    print(f"images={len(images)} compressed={changed} skipped={len(images) - changed}")


if __name__ == "__main__":
    main()
