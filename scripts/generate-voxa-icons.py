#!/usr/bin/env python3
"""Rasterize the Voxa mark into the icon files Tauri and the tray expect.

The master is src/assets/voxa-mark.svg. This script redraws that same stroke
so icon generation does not depend on a system SVG renderer.
"""

from __future__ import annotations

import struct
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "src-tauri" / "icons"
RES = ROOT / "src-tauri" / "resources"

WHITE = (255, 255, 255, 255)
INK = (9, 9, 10, 255)
ACCENT = (94, 106, 210, 255)
AMBER = (232, 179, 57, 255)
TILE = (9, 9, 10, 255)


def draw_v(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float], color, width: float) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    left = (x0 + w * 0.08, y0 + h * 0.10)
    bottom = (x0 + w * 0.50, y0 + h * 0.90)
    right = (x0 + w * 0.92, y0 + h * 0.10)
    draw.line([left, bottom, right], fill=color, width=max(1, int(round(width))), joint="curve")
    r = width / 2
    for x, y in (left, bottom, right):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)


def render(size: int, *, tile: bool, color, badge=None) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if tile:
        radius = size * 0.22
        draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=TILE)
        inset = size * 0.22
        stroke = size * 0.075
    else:
        inset = size * 0.14
        stroke = size * 0.11
    draw_v(draw, (inset, inset, size - inset, size - inset), color, stroke)
    if badge is not None:
        d = max(3, int(size * 0.22))
        margin = max(1, int(size * 0.06))
        x1 = size - margin
        y1 = size - margin
        draw.ellipse((x1 - d, y1 - d, x1, y1), fill=badge)
    return img


def save_png(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    return struct.unpack(">II", data[16:24])


def main() -> None:
    # App icons: white V on a near-black rounded tile, every existing size.
    for path in ICONS.rglob("*.png"):
        w, h = png_size(path)
        side = max(w, h)
        save_png(path, render(side, tile=True, color=WHITE).resize((w, h), Image.Resampling.LANCZOS))

    master = render(1024, tile=True, color=WHITE)
    save_png(ICONS / "icon.png", master)

    # Windows .ico
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    master.save(
        ICONS / "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=[master.resize((s, s), Image.Resampling.LANCZOS) for s in ico_sizes[1:]],
    )

    # Tray and notification glyphs. "dark" files are the ink glyph for light trays.
    pairs = {
        "tray_idle.png": (WHITE, None),
        "tray_idle_dark.png": (INK, None),
        "tray_recording.png": (ACCENT, None),
        "tray_recording_dark.png": (ACCENT, None),
        "tray_transcribing.png": (WHITE, ACCENT),
        "tray_transcribing_dark.png": (INK, ACCENT),
        "tray_idle_warning.png": (WHITE, AMBER),
        "tray_idle_warning_dark.png": (INK, AMBER),
        "handy.png": (ACCENT, None),
        "handy_warning.png": (ACCENT, AMBER),
        "recording.png": (ACCENT, None),
        "transcribing.png": (WHITE, ACCENT),
    }
    for name, (color, badge) in pairs.items():
        save_png(RES / name, render(64, tile=False, color=color, badge=badge))

    # Logo preview for the PR.
    preview = render(256, tile=True, color=WHITE)
    out = Path("/opt/cursor/artifacts")
    out.mkdir(parents=True, exist_ok=True)
    save_png(out / "voxa-mark.png", preview)
    print("icons written")


if __name__ == "__main__":
    main()
