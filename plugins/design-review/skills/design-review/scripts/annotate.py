#!/usr/bin/env python3
"""
annotate.py — crop components and overlay coordinate rulers.

Two jobs, both aimed at the same weakness: visual judgment of spatial
relationships is unreliable without a reference grid. Coordinate overlays on
screenshot edges measurably improve spatial critique and bounding-box accuracy
(+55% in the published study). Cropping matters for the same reason — at page
scale a 161px void reads as generous whitespace.

Requires Pillow:
    pip install Pillow

Usage:
    # grid over a full capture
    python annotate.py grid shots/1280x900-full.png --out annotated/full.png

    # crop a region, then grid it, upscaled for inspection
    python annotate.py crop shots/1280x900-full.png --box 0,0,1280,720 --scale 2 --out crops/hero.png

    # slice a tall capture into component-sized bands
    python annotate.py slice shots/1280x900-full.png --height 720 --out-dir crops/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is not installed.  pip install Pillow")

GRID_MINOR = 50
GRID_MAJOR = 100
GUTTER = 28

INK = (255, 0, 128, 255)      # magenta reads over both light and dark UI
MINOR = (255, 0, 128, 60)
MAJOR = (255, 0, 128, 120)
GUTTER_BG = (24, 24, 27, 235)


def _font(size: int = 11):
    for name in ("DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttc"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def add_grid(img: Image.Image, minor: int = GRID_MINOR, major: int = GRID_MAJOR,
             gutter: int = GUTTER) -> Image.Image:
    """Rulers along the top and left edges, with a faint grid over the image.

    The gutter sits outside the content so the overlay never hides what it is
    measuring.
    """
    base = img.convert("RGBA")
    w, h = base.size
    canvas = Image.new("RGBA", (w + gutter, h + gutter), GUTTER_BG)
    canvas.paste(base, (gutter, gutter))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    f = _font()

    for x in range(0, w + 1, minor):
        is_major = x % major == 0
        d.line([(gutter + x, gutter), (gutter + x, gutter + h)],
               fill=MAJOR if is_major else MINOR, width=1)
        tick = 10 if is_major else 5
        d.line([(gutter + x, gutter - tick), (gutter + x, gutter)], fill=INK, width=1)
        if is_major:
            d.text((gutter + x + 2, 4), str(x), fill=INK, font=f)

    for y in range(0, h + 1, minor):
        is_major = y % major == 0
        d.line([(gutter, gutter + y), (gutter + w, gutter + y)],
               fill=MAJOR if is_major else MINOR, width=1)
        tick = 10 if is_major else 5
        d.line([(gutter - tick, gutter + y), (gutter, gutter + y)], fill=INK, width=1)
        if is_major:
            d.text((3, gutter + y + 2), str(y), fill=INK, font=f)

    d.text((3, 3), "px", fill=INK, font=f)
    return Image.alpha_composite(canvas, overlay).convert("RGB")


def crop(img: Image.Image, box: tuple[int, int, int, int], scale: int = 1) -> Image.Image:
    x1, y1, x2, y2 = box
    x2 = min(x2, img.width)
    y2 = min(y2, img.height)
    out = img.crop((x1, y1, x2, y2))
    if scale > 1:
        # Nearest keeps 1px drift and hairlines visible; smoothing hides exactly
        # the defects a detail crop exists to find.
        out = out.resize((out.width * scale, out.height * scale), Image.NEAREST)
    return out


def slice_bands(img: Image.Image, band_height: int, overlap: int = 40):
    bands = []
    y = 0
    while y < img.height:
        y2 = min(y + band_height, img.height)
        bands.append(((0, y, img.width, y2), img.crop((0, y, img.width, y2))))
        if y2 >= img.height:
            break
        y = y2 - overlap
    return bands


def main():
    ap = argparse.ArgumentParser(description="Crop and annotate captures for visual review.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("grid", help="Overlay a coordinate grid")
    g.add_argument("image")
    g.add_argument("--out", required=True)
    g.add_argument("--minor", type=int, default=GRID_MINOR)
    g.add_argument("--major", type=int, default=GRID_MAJOR)

    c = sub.add_parser("crop", help="Crop a region, optionally gridded and upscaled")
    c.add_argument("image")
    c.add_argument("--box", required=True, help="x1,y1,x2,y2")
    c.add_argument("--out", required=True)
    c.add_argument("--scale", type=int, default=1, help="2-3 for defect inspection")
    c.add_argument("--no-grid", action="store_true")

    s = sub.add_parser("slice", help="Slice a tall capture into overlapping bands")
    s.add_argument("image")
    s.add_argument("--out-dir", required=True)
    s.add_argument("--height", type=int, default=720)
    s.add_argument("--overlap", type=int, default=40)
    s.add_argument("--grid", action="store_true")

    args = ap.parse_args()
    img = Image.open(args.image)

    if args.cmd == "grid":
        add_grid(img, args.minor, args.major).save(args.out)
        print(f"Wrote {args.out}")

    elif args.cmd == "crop":
        box = tuple(int(v) for v in args.box.split(","))
        if len(box) != 4:
            sys.exit("--box needs x1,y1,x2,y2")
        out = crop(img, box, args.scale)
        if not args.no_grid:
            out = add_grid(out)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        out.save(args.out)
        print(f"Wrote {args.out}  ({out.width}x{out.height})")

    elif args.cmd == "slice":
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for i, (box, band) in enumerate(slice_bands(img, args.height, args.overlap)):
            if args.grid:
                band = add_grid(band)
            p = out_dir / f"band-{i:02d}.png"
            band.save(p)
            print(f"  {p}  y={box[1]}-{box[3]}")
        print("\nOpen every band. A capture you did not open is not evidence.")


if __name__ == "__main__":
    main()
