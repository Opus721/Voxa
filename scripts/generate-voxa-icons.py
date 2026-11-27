#!/usr/bin/env python3
"""Rasterize the Voxa mark into the icon files Tauri and the tray expect.

The master is src/assets/voxa-mark.svg: the italic V from Libre Bodoni,
weight 600, outlined so generation does not need the font.

Every size, including the tray and the 16px exe frame, uses the medium
bleed: the letter is scaled about 20% past the left and bottom of a
#09090a rounded square, matching design/voxa-mark-bodoni-bleed-2.svg.
There is no fitted-letter variant.
"""

from __future__ import annotations

import io
import re
import struct
from pathlib import Path

import icnsutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "src-tauri" / "icons"
RES = ROOT / "src-tauri" / "resources"
MARK = ROOT / "src" / "assets" / "voxa-mark.svg"

WHITE = (255, 255, 255, 255)
ACCENT = (94, 106, 210, 255)
AMBER = (232, 179, 57, 255)
TILE = (9, 9, 10, 255)

# Placement copied from design/voxa-mark-bodoni-bleed-2.svg (1024px master).
BLEED_SCALE = 1.54151
BLEED_TX = -204.80
BLEED_TY = 48.00
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 256]


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


def _contours(ops: list[tuple[str, list[float]]], steps: int = 12) -> list[list[tuple[float, float]]]:
    """One polygon per subpath. Filling them separately unions overlaps.

    The Bodoni V is four contours. A single polygon would bridge the gaps
    and punch holes where a serif crosses a stroke.
    """
    contours: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    cx = cy = 0.0

    def line(x: float, y: float) -> None:
        nonlocal cx, cy
        current.append((x, y))
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
            if len(current) >= 3:
                contours.append(current)
            current = []
            cx, cy = n
            current.append((cx, cy))
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
            if current and current[0] != current[-1]:
                current.append(current[0])
            if len(current) >= 3:
                contours.append(current)
            current = []
    if len(current) >= 3:
        contours.append(current)
    return contours


def mark_contours() -> list[list[tuple[float, float]]]:
    text = MARK.read_text()
    match = re.search(r'd="([^"]+)"', text)
    if not match:
        raise SystemExit(f"no path in {MARK}")
    return _contours(_tokenize(match.group(1)))


def _map_points(contours, fn) -> list[list[tuple[float, float]]]:
    return [[fn(x, y) for x, y in contour] for contour in contours]


def paint_contours(canvas: Image.Image, contours, color, *, clip: bool) -> None:
    mask = Image.new("L", canvas.size, 0)
    draw = ImageDraw.Draw(mask)
    for contour in contours:
        if len(contour) >= 3:
            draw.polygon(contour, fill=255)
    if clip:
        size = canvas.size[0]
        rounded = Image.new("L", canvas.size, 0)
        ImageDraw.Draw(rounded).rounded_rectangle(
            (0, 0, size - 1, size - 1), radius=size * 0.22, fill=255
        )
        clipped = Image.new("L", canvas.size, 0)
        clipped.paste(mask, mask=rounded)
        mask = clipped
    color_layer = Image.new("RGBA", canvas.size, color)
    canvas.paste(color_layer, mask=mask)


def bleed_contours(contours, size: int):
    """Medium bleed, scaled from the 1024px design tile."""
    k = size / 1024
    scale = BLEED_SCALE * k
    tx = BLEED_TX * k
    ty = BLEED_TY * k
    return _map_points(contours, lambda x, y: (x * scale + tx, y * scale + ty))


def render(size: int, *, color, badge=None) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    contours = mark_contours()
    radius = size * 0.22
    ImageDraw.Draw(img).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=TILE)
    paint_contours(img, bleed_contours(contours, size), color, clip=True)
    if badge is not None:
        d = max(3, int(size * 0.22))
        margin = max(1, int(size * 0.06))
        x1 = size - margin
        y1 = size - margin
        ImageDraw.Draw(img).ellipse((x1 - d, y1 - d, x1, y1), fill=badge)
    return img


def save_png(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    return struct.unpack(">II", data[16:24])


def write_ico(path: Path) -> None:
    sizes = ICO_SIZES
    frames = [render(s, color=WHITE) for s in sizes]
    frames[-1].save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[:-1],
    )


def write_icns(path: Path) -> None:
    # Filename stems are what icnsutil uses to pick the icon type.
    named = {
        "icon_16x16.png": 16,
        "icon_16x16@2x.png": 32,
        "icon_32x32.png": 32,
        "icon_32x32@2x.png": 64,
        "icon_128x128.png": 128,
        "icon_128x128@2x.png": 256,
        "icon_256x256.png": 256,
        "icon_256x256@2x.png": 512,
        "icon_512x512.png": 512,
        "icon_512x512@2x.png": 1024,
    }
    icns = icnsutil.IcnsFile()
    for name, size in named.items():
        buf = io.BytesIO()
        render(size, color=WHITE).save(buf, format="PNG")
        icns.add_media(file=name, data=buf.getvalue())
    icns.write(path)


def main() -> None:
    for path in ICONS.rglob("*.png"):
        w, h = png_size(path)
        side = max(w, h)
        save_png(path, render(side, color=WHITE).resize((w, h), Image.Resampling.LANCZOS))

    master = render(1024, color=WHITE)
    save_png(ICONS / "icon.png", master)
    write_ico(ICONS / "icon.ico")
    write_icns(ICONS / "icon.icns")

    # Light and dark files are the same bleed tile. Recording tints the letter;
    # transcribing and warning keep a corner badge so the tray state still reads.
    pairs = {
        "tray_idle.png": (WHITE, None),
        "tray_idle_dark.png": (WHITE, None),
        "tray_recording.png": (ACCENT, None),
        "tray_recording_dark.png": (ACCENT, None),
        "tray_transcribing.png": (WHITE, ACCENT),
        "tray_transcribing_dark.png": (WHITE, ACCENT),
        "tray_idle_warning.png": (WHITE, AMBER),
        "tray_idle_warning_dark.png": (WHITE, AMBER),
        "handy.png": (WHITE, None),
        "handy_warning.png": (WHITE, AMBER),
        "recording.png": (ACCENT, None),
        "transcribing.png": (WHITE, ACCENT),
    }
    for name, (color, badge) in pairs.items():
        save_png(RES / name, render(64, color=color, badge=badge))

    write_contact_sheet(ROOT / "design" / "voxa-icon-sizes.png")

    out = Path("/opt/cursor/artifacts")
    out.mkdir(parents=True, exist_ok=True)
    save_png(out / "voxa-mark.png", render(256, color=WHITE))
    save_png(out / "voxa-icon.png", master)
    save_png(out / "voxa-tray-16.png", render(16, color=WHITE).resize((160, 160), Image.Resampling.NEAREST))
    save_png(out / "voxa-icon-sizes.png", Image.open(ROOT / "design" / "voxa-icon-sizes.png"))
    print("icons written")


def write_contact_sheet(path: Path) -> None:
    """Every shipped size, plus a nearest-neighbor zoom of the small ones."""
    sizes = ICO_SIZES
    zoom = 8
    label_h = 28
    pad = 24
    cell = 256
    cols = len(sizes)
    width = pad + cols * (cell + pad)
    height = pad + cell + label_h + pad + 16 * zoom + label_h + pad
    sheet = Image.new("RGBA", (width, height), (24, 24, 27, 255))
    draw = ImageDraw.Draw(sheet)
    for i, size in enumerate(sizes):
        icon = render(size, color=WHITE)
        shown = icon.resize((cell, cell), Image.Resampling.NEAREST)
        x = pad + i * (cell + pad)
        sheet.paste(shown, (x, pad))
        draw.text((x, pad + cell + 6), f"{size}px", fill=(255, 255, 255, 255))
        if size <= 32:
            big = icon.resize((size * zoom, size * zoom), Image.Resampling.NEAREST)
            sheet.paste(big, (x, pad + cell + label_h + pad))
            draw.text(
                (x, pad + cell + label_h + pad + size * zoom + 4),
                f"{size}px ×{zoom}",
                fill=(180, 180, 186, 255),
            )
    save_png(path, sheet)


if __name__ == "__main__":
    main()
