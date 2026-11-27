#!/usr/bin/env python3
"""Rasterize the Voxa mark into the icon files Tauri and the tray expect.

The master is src/assets/voxa-mark.svg: the italic V from Instrument Serif,
outlined so generation does not need the font or a system SVG renderer.
"""

from __future__ import annotations

import re
import struct
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "src-tauri" / "icons"
RES = ROOT / "src-tauri" / "resources"
MARK = ROOT / "src" / "assets" / "voxa-mark.svg"

WHITE = (255, 255, 255, 255)
INK = (9, 9, 10, 255)
ACCENT = (94, 106, 210, 255)
AMBER = (232, 179, 57, 255)
TILE = (9, 9, 10, 255)


def _tokenize(d: str) -> list[tuple[str, list[float]]]:
    tokens = re.findall(r"[MLQCZ]|-?\d*\.?\d+", d)
    ops: list[tuple[str, list[float]]] = []
    i = 0
    while i < len(tokens):
        op = tokens[i]
        i += 1
        need = {"M": 2, "L": 2, "Q": 4, "C": 6, "Z": 0}[op]
        nums = [float(n) for n in tokens[i : i + need]]
        i += need
        ops.append((op, nums))
    return ops


def _flatten(ops: list[tuple[str, list[float]]], steps: int = 10) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    cx = cy = 0.0

    def line(x: float, y: float) -> None:
        nonlocal cx, cy
        pts.append((x, y))
        cx, cy = x, y

    def cubic(x1, y1, x2, y2, x, y) -> None:
        nonlocal cx, cy
        x0, y0 = cx, cy
        for i in range(1, steps + 1):
            t = i / steps
            u = 1 - t
            line(
                u**3 * x0 + 3 * u**2 * t * x1 + 3 * u * t**2 * x2 + t**3 * x,
                u**3 * y0 + 3 * u**2 * t * y1 + 3 * u * t**2 * y2 + t**3 * y,
            )

    for op, n in ops:
        if op == "M":
            cx, cy = n
            pts.append((cx, cy))
        elif op == "L":
            line(*n)
        elif op == "Q":
            x1, y1, x, y = n
            cubic(
                cx + 2 / 3 * (x1 - cx),
                cy + 2 / 3 * (y1 - cy),
                x + 2 / 3 * (x1 - x),
                y + 2 / 3 * (y1 - y),
                x,
                y,
            )
        elif op == "C":
            cubic(*n)
        elif op == "Z":
            if pts and pts[0] != pts[-1]:
                pts.append(pts[0])
    return pts


def mark_polygon() -> list[tuple[float, float]]:
    text = MARK.read_text()
    match = re.search(r'd="([^"]+)"', text)
    if not match:
        raise SystemExit(f"no path in {MARK}")
    box = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', text)
    if not box:
        raise SystemExit(f"no viewBox in {MARK}")
    return _flatten(_tokenize(match.group(1)))


def paint_mark(canvas: Image.Image, color, pad: float) -> None:
    poly = mark_polygon()
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    gw, gh = x1 - x0, y1 - y0
    w, h = canvas.size
    scale = min((w * (1 - pad * 2)) / gw, (h * (1 - pad * 2)) / gh)
    ox = (w - gw * scale) / 2 - x0 * scale
    oy = (h - gh * scale) / 2 - y0 * scale
    mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(mask).polygon([(ox + x * scale, oy + y * scale) for x, y in poly], fill=255)
    color_layer = Image.new("RGBA", canvas.size, color)
    canvas.paste(color_layer, mask=mask)


def render(size: int, *, tile: bool, color, badge=None) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if tile:
        radius = size * 0.22
        draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=TILE)
        # Draw the letter on a square so the italic doesn't kiss the tile edge.
        inner = max(1, int(size * 0.72))
        glyph = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
        paint_mark(glyph, color, pad=0.04)
        img.alpha_composite(glyph, ((size - inner) // 2, (size - inner) // 2))
    else:
        paint_mark(img, color, pad=0.08)
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
