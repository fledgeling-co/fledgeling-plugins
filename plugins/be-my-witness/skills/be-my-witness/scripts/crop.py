#!/usr/bin/env python3
"""
crop.py — turn a screenshot into something a model can actually see.

A 1440x900 screenshot handed to a vision model whole is roughly 30 pixels of glyph
height per line of body text. Defects at that scale are not subtle, they are absent:
the model reports the page looks fine because, at the resolution it was given, it
does. Every real finding comes from a crop.

USAGE
    # the tiles prescan.py chose, upscaled and written out
    python3 crop.py shot.png --tiles-from prescan.json --out /tmp/tiles

    # a named region, at 2x
    python3 crop.py shot.png --region 0,0,480,300 --scale 2 --out /tmp/header.png

    # the SAME region from two images, side by side, for a paired look
    python3 crop.py shot.png --pair mock.png --region 0,0,480,300 --out /tmp/pair.png

    # an even grid when there is no prescan to guide it
    python3 crop.py shot.png --grid 3x2 --scale 2 --out /tmp/tiles

PAIRED CROPS MATTER. Cropping one image and comparing it against the whole of the
other reintroduces the framing error the crop was supposed to remove. --pair takes
the same rectangle from both and writes them adjacent with a divider, so what the
model sees is a like-for-like comparison.

DEPENDENCIES
    Pillow if present. Without it, falls back to `magick`/`convert`/`sips`, and if
    none of those exist it prints the crop commands it would have run so a human or
    another tool can do it.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def have_pillow() -> bool:
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def crop_pillow(src: Path, box, scale: float, dst: Path):
    from PIL import Image
    im = Image.open(src).convert("RGB")
    x, y, w, h = box
    x, y = max(0, x), max(0, y)
    w, h = min(w, im.width - x), min(h, im.height - y)
    if w <= 0 or h <= 0:
        raise SystemExit(f"crop {box} lies outside {src} ({im.width}x{im.height})")
    out = im.crop((x, y, x + w, y + h))
    if scale != 1:
        out = out.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst)
    return dst


def crop_cli(src: Path, box, scale: float, dst: Path):
    x, y, w, h = box
    dst.parent.mkdir(parents=True, exist_ok=True)
    tool = shutil.which("magick") or shutil.which("convert")
    if tool:
        cmd = [tool, str(src), "-crop", f"{w}x{h}+{x}+{y}", "+repage"]
        if scale != 1:
            cmd += ["-filter", "Lanczos", "-resize", f"{int(scale * 100)}%"]
        cmd += [str(dst)]
        subprocess.run(cmd, check=True)
        return dst
    if shutil.which("sips"):
        subprocess.run(["sips", "-c", str(h), str(w), str(src), "--out", str(dst)], check=True,
                       stdout=subprocess.DEVNULL)
        return dst
    print(f"[crop] no image tool available. Crop {box} of {src} at {scale}x into {dst} by other means.",
          file=sys.stderr)
    return None


def crop(src: Path, box, scale: float, dst: Path):
    return crop_pillow(src, box, scale, dst) if have_pillow() else crop_cli(src, box, scale, dst)


def pair(a: Path, b: Path, box, scale: float, dst: Path, gap: int = 16):
    """The same rectangle from both images, adjacent, with a divider between them."""
    if not have_pillow():
        ta, tb = dst.with_suffix(".a.png"), dst.with_suffix(".b.png")
        crop(a, box, scale, ta)
        crop(b, box, scale, tb)
        print(f"[crop] Pillow absent; wrote the two halves separately: {ta} {tb}", file=sys.stderr)
        return [ta, tb]
    from PIL import Image, ImageDraw
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    x, y, w, h = box
    ca = ia.crop((x, y, min(x + w, ia.width), min(y + h, ia.height)))
    cb = ib.crop((x, y, min(x + w, ib.width), min(y + h, ib.height)))
    if scale != 1:
        ca = ca.resize((int(ca.width * scale), int(ca.height * scale)), Image.LANCZOS)
        cb = cb.resize((int(cb.width * scale), int(cb.height * scale)), Image.LANCZOS)
    H = max(ca.height, cb.height)
    canvas = Image.new("RGB", (ca.width + gap + cb.width, H), (245, 245, 247))
    canvas.paste(ca, (0, 0))
    canvas.paste(cb, (ca.width + gap, 0))
    d = ImageDraw.Draw(canvas)
    d.rectangle([ca.width + gap // 2 - 1, 0, ca.width + gap // 2 + 1, H], fill=(140, 140, 150))
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst)
    return [dst]


def parse_region(s: str):
    parts = [int(v) for v in s.split(",")]
    if len(parts) != 4:
        raise SystemExit("--region takes x,y,w,h")
    return parts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="output file, or directory for --tiles/--grid")
    ap.add_argument("--region", help="x,y,w,h")
    ap.add_argument("--pair", type=Path, help="second image; takes the SAME region from both")
    ap.add_argument("--tiles-from", type=Path, help="prescan --json output; crops its inspectionTiles")
    ap.add_argument("--grid", help="COLSxROWS, e.g. 3x2, when there is no prescan to guide it")
    ap.add_argument("--scale", type=float, default=2.0, help="upscale factor (default 2)")
    args = ap.parse_args()

    written = []
    if args.region:
        box = parse_region(args.region)
        written = pair(args.image, args.pair, box, args.scale, args.out) if args.pair \
            else [crop(args.image, box, args.scale, args.out)]
    elif args.tiles_from:
        data = json.loads(args.tiles_from.read_text())
        for i, t in enumerate(data.get("inspectionTiles", [])):
            dst = args.out / f"tile-{i:02d}@{int(args.scale)}x.png"
            box = (t["x"], t["y"], t["w"], t["h"])
            written += pair(args.image, args.pair, box, args.scale, dst) if args.pair \
                else [crop(args.image, box, args.scale, dst)]
    elif args.grid:
        cols, rows = (int(v) for v in args.grid.lower().split("x"))
        if have_pillow():
            from PIL import Image
            W, H = Image.open(args.image).size
        else:
            raise SystemExit("--grid needs Pillow to read the image size; use --region instead")
        for r in range(rows):
            for c in range(cols):
                box = (c * W // cols, r * H // rows, W // cols, H // rows)
                dst = args.out / f"grid-r{r}c{c}@{int(args.scale)}x.png"
                written += pair(args.image, args.pair, box, args.scale, dst) if args.pair \
                    else [crop(args.image, box, args.scale, dst)]
    else:
        raise SystemExit("give one of --region, --tiles-from or --grid")

    for p in filter(None, written):
        print(p)


if __name__ == "__main__":
    main()
