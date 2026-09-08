"""
Safari Time - cut the symbol contact sheet into per-symbol images.

The sheet is a white page with two rows of five framed tiles and a text label
under each. Tiles are NOT on an even grid (the WILD and Elephant sit wider
than their neighbours), so nothing here assumes cell positions:

1. Row profile of the page body -> the two longest runs of "ink" rows are the
   tile bands (labels are short separate runs).
2. Column profile inside each band -> five runs of ink columns, one per tile.
3. Tight-crop each tile, float it on a transparent square by flood-filling the
   white surround from the corners, resize, save as WebP.

The medallion is a single tile and goes through steps 3 only.

    python -m engine.slice_art SHEET.jpg AFRICA.jpg [--size 512]
"""

from __future__ import annotations

import argparse
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "web", "assets", "symbols")

# Sheet order, row-major, exactly as drawn (lowest payout first).
SHEET_NAMES = ["j", "q", "k", "a", "giraffe", "zebra", "rhino", "elephant", "lion", "wild"]

INK = 232            # luminance below this counts as ink (glow is paler)
DENSITY = 0.04       # fraction of a row/column that must be ink to count
FORMAT = "webp"      # web/gamedata.js lists whichever of png/webp/jpg exists
QUALITY = 88


def ink_profile(img: Image.Image, axis: int) -> list:
    """Fraction of ink pixels per row (axis=0) or per column (axis=1)."""
    gray = img.convert("L")
    w, h = gray.size
    px = gray.load()
    if axis == 0:
        return [sum(1 for x in range(w) if px[x, y] < INK) / w for y in range(h)]
    return [sum(1 for y in range(h) if px[x, y] < INK) / h for x in range(w)]


def runs(profile: list, threshold: float, min_len: int = 1) -> list:
    """[(start, end), ...] for every stretch of the profile at/above threshold."""
    out, start = [], None
    for i, v in enumerate(profile + [0.0]):
        if v >= threshold and start is None:
            start = i
        elif v < threshold and start is not None:
            if i - start >= min_len:
                out.append((start, i))
            start = None
    return out


def longest(rs: list) -> tuple:
    return max(rs, key=lambda r: r[1] - r[0])


def tight_crop(region: Image.Image) -> Image.Image:
    y0, y1 = longest(runs(ink_profile(region, 0), DENSITY))
    band = region.crop((0, y0, region.width, y1))
    x0, x1 = longest(runs(ink_profile(band, 1), DENSITY))
    return region.crop((x0, y0, x1, y1))


def float_on_transparent(tile: Image.Image, size: int) -> Image.Image:
    """Square canvas, tile centred, white surround made transparent."""
    tile = tile.convert("RGBA")
    side = max(tile.size)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    canvas.paste(tile, ((side - tile.width) // 2, (side - tile.height) // 2))

    marker = (0, 255, 0, 255)
    for corner in ((0, 0), (side - 1, 0), (0, side - 1), (side - 1, side - 1)):
        ImageDraw.floodfill(canvas, corner, marker, thresh=40)
    px = canvas.load()
    for y in range(side):
        for x in range(side):
            if px[x, y] == marker:
                px[x, y] = (255, 255, 255, 0)
    return canvas.resize((size, size), Image.LANCZOS)


def save(img: Image.Image, name: str) -> str:
    out = os.path.join(OUT, f"{name}.{FORMAT}")
    if FORMAT == "webp":
        img.save(out, "WEBP", quality=QUALITY, method=6)
    else:
        img.save(out, optimize=True)
    return out


def slice_sheet(path: str, size: int) -> list:
    sheet = Image.open(path).convert("RGB")
    w, h = sheet.size
    # Skip the solid header and footer strips.
    body = sheet.crop((0, int(h * 0.075), w, int(h * 0.93)))

    bands = sorted(runs(ink_profile(body, 0), DENSITY), key=lambda r: r[0] - r[1])[:2]
    bands.sort()
    assert len(bands) == 2, bands

    written = []
    index = 0
    for y0, y1 in bands:
        band = body.crop((0, y0, w, y1))
        cols = runs(ink_profile(band, 1), DENSITY, min_len=int(w * 0.05))
        assert len(cols) == 5, f"expected 5 tiles in band {y0}-{y1}, found {cols}"
        for x0, x1 in cols:
            tile = tight_crop(band.crop((x0, 0, x1, band.height)))
            name = SHEET_NAMES[index]
            index += 1
            out = save(float_on_transparent(tile, size), name)
            written.append((name, tile.size, os.path.getsize(out)))
    return written


def slice_single(path: str, name: str, size: int) -> tuple:
    tile = tight_crop(Image.open(path).convert("RGB"))
    out = save(float_on_transparent(tile, size), name)
    return (name, tile.size, os.path.getsize(out))


def main(argv: list) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("africa")
    ap.add_argument("--size", type=int, default=512)
    args = ap.parse_args(argv)
    os.makedirs(OUT, exist_ok=True)
    results = slice_sheet(args.sheet, args.size) + [slice_single(args.africa, "africa", args.size)]
    for name, dims, size in results:
        print(f"{name:9s} crop {dims[0]}x{dims[1]}  ->  {size / 1024:6.1f} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
