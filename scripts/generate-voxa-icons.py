#!/usr/bin/env python3
"""Build the Voxa icon files from one 1024px raster.

The master is design/voxa-mark-bodoni-bleed-2.png: the Libre Bodoni italic
V, weight 600, medium bleed, white on #09090a. It matches a single
render of src/assets/voxa-mark.svg at 1024. Every smaller file is a
LANCZOS downscale of that image (halved until the next power of two,
then LANCZOS to the exact size). Nothing is redrawn per size.
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
MASTER_PNG = ROOT / "design" / "voxa-mark-bodoni-bleed-2.png"

WHITE = (255, 255, 255, 255)
TILE = (9, 9, 10, 255)

# Placement copied from design/voxa-mark-bodoni-bleed-2.svg (1024px master).
BLEED_SCALE = 1.54151
BLEED_TX = -204.80
BLEED_TY = 48.00
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]
# A redrawn polygon at 32px is ~40 RMSE from a LANCZOS of the master.
# Halving stays near 3. Anything above this means a size was repainted.
LANCZOS_RMSE_LIMIT = 6.0


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


def render_master() -> Image.Image:
    """The one polygon paint: 1024px. Smaller sizes never call this."""
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    radius = size * 0.22
    ImageDraw.Draw(img).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=TILE)
    paint_contours(img, bleed_contours(mark_contours(), size), WHITE, clip=True)
    return img


def load_master() -> Image.Image:
    master = Image.open(MASTER_PNG).convert("RGBA")
    if master.size != (1024, 1024):
        raise SystemExit(f"{MASTER_PNG.name} is {master.size}, expected 1024x1024")
    painted = render_master()
    if master.tobytes() != painted.tobytes():
        raise SystemExit(f"{MASTER_PNG.name} is not the 1024px render of {MARK.name}")
    return master


def downscale(master: Image.Image, size: int, cache: dict[int, Image.Image]) -> Image.Image:
    """Halve with LANCZOS down to the next power of two, then LANCZOS to `size`."""
    if size in cache:
        return cache[size].copy()
    if size <= 0:
        raise SystemExit(f"icon size must be positive, got {size}")
    step = master.size[0]
    img = master
    while step // 2 >= size and step % 2 == 0:
        step //= 2
        if step in cache:
            img = cache[step]
            continue
        img = img.resize((step, step), Image.Resampling.LANCZOS)
        cache[step] = img
    if img.size != (size, size):
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        cache[size] = img
    return img.copy()


def save_png(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGBA").save(path, "PNG", optimize=True)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    return struct.unpack(">II", data[16:24])


def png_bytes(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.convert("RGBA").save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def write_ico(path: Path, frames: dict[int, Image.Image]) -> None:
    """Vista-style icon: every frame is a 32-bit PNG, not a BMP mask."""
    sizes = [size for size in ICO_SIZES if size in frames]
    blobs = [png_bytes(frames[size]) for size in sizes]
    count = len(sizes)
    header = struct.pack("<HHH", 0, 1, count)
    offset = 6 + 16 * count
    entries = []
    for size, blob in zip(sizes, blobs):
        dim = 0 if size >= 256 else size
        entries.append(struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(blob), offset))
        offset += len(blob)
    path.write_bytes(header + b"".join(entries) + b"".join(blobs))


def write_icns(path: Path, cache: dict[int, Image.Image], master: Image.Image) -> None:
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
        icns.add_media(file=name, data=png_bytes(downscale(master, size, cache)))
    icns.write(path)


def rmse(a: Image.Image, b: Image.Image) -> float:
    pa = a.convert("RGBA").tobytes()
    pb = b.convert("RGBA").tobytes()
    if len(pa) != len(pb):
        raise SystemExit(f"rmse size mismatch {a.size} vs {b.size}")
    acc = 0
    for left, right in zip(pa, pb):
        acc += (left - right) ** 2
    return (acc / len(pa)) ** 0.5


def assert_frames_match_lanczos(master: Image.Image, frames: dict[int, Image.Image]) -> None:
    for size in (256, 32):
        direct = master.resize((size, size), Image.Resampling.LANCZOS)
        score = rmse(frames[size], direct)
        print(f"ico {size}px RMSE vs LANCZOS of master: {score:.3f}")
        if score > LANCZOS_RMSE_LIMIT:
            raise SystemExit(f"ico {size}px RMSE {score:.3f} exceeds {LANCZOS_RMSE_LIMIT}")


def main() -> None:
    master = load_master()
    cache: dict[int, Image.Image] = {1024: master}

    for path in sorted(ICONS.rglob("*.png")):
        w, h = png_size(path)
        side = max(w, h)
        image = downscale(master, side, cache)
        if (w, h) != (side, side):
            image = image.resize((w, h), Image.Resampling.LANCZOS)
        save_png(path, image)

    frames = {size: downscale(master, size, cache) for size in ICO_SIZES}
    assert_frames_match_lanczos(master, frames)
    write_ico(ICONS / "icon.ico", frames)
    write_icns(ICONS / "icon.icns", cache, master)

    # Windows can display any tray state as the shell icon.
    tray = downscale(master, 64, cache)
    for path in sorted(RES.glob("tray_*.png")):
        save_png(path, tray)
    for name in ("handy.png", "handy_warning.png", "recording.png", "transcribing.png"):
        save_png(RES / name, tray)

    sheet = write_contact_sheet(master, cache)
    save_png(ROOT / "design" / "voxa-icon-sizes.png", sheet)

    print("icons written")


def write_contact_sheet(master: Image.Image, cache: dict[int, Image.Image]) -> Image.Image:
    """Master beside each downscale, with 32px and 16px nearest-neighbor zooms."""
    sizes = ICO_SIZES
    zoom = 8
    label_h = 22
    pad = 16
    cell = 128
    cols = 1 + len(sizes)
    width = pad + cols * (cell + pad)
    zoom_row = pad + cell + label_h + pad
    height = zoom_row + 32 * zoom + label_h + pad + 16 * zoom + label_h + pad
    sheet = Image.new("RGBA", (width, height), (24, 24, 27, 255))
    draw = ImageDraw.Draw(sheet)

    def place(image: Image.Image, col: int, y: int, label: str) -> None:
        side = image.size[0]
        if side >= cell:
            shown = image.resize((cell, cell), Image.Resampling.LANCZOS)
        else:
            factor = max(1, cell // side)
            shown = image.resize((side * factor, side * factor), Image.Resampling.NEAREST)
        x = pad + col * (cell + pad)
        sheet.paste(shown, (x, y), shown)
        draw.text((x, y + cell + 4), label, fill=(255, 255, 255, 255))

    place(downscale(master, 256, cache), 0, pad, "master")
    for i, size in enumerate(sizes, start=1):
        place(downscale(master, size, cache), i, pad, f"{size}px")

    def zoomed(source: Image.Image, size: int, x: int, y: int, label: str) -> None:
        big = source.resize((size * zoom, size * zoom), Image.Resampling.NEAREST)
        sheet.paste(big, (x, y), big)
        draw.text((x, y + size * zoom + 4), label, fill=(255, 255, 255, 255))

    zoomed(downscale(master, 32, cache), 32, pad, zoom_row, "32px ×8")
    zoomed(
        master.resize((32, 32), Image.Resampling.LANCZOS),
        32,
        pad + 32 * zoom + pad,
        zoom_row,
        "32px LANCZOS ×8",
    )
    y16 = zoom_row + 32 * zoom + label_h + pad
    zoomed(downscale(master, 16, cache), 16, pad, y16, "16px ×8")
    zoomed(
        master.resize((16, 16), Image.Resampling.LANCZOS),
        16,
        pad + 16 * zoom + pad,
        y16,
        "16px LANCZOS ×8",
    )
    return sheet


if __name__ == "__main__":
    main()
