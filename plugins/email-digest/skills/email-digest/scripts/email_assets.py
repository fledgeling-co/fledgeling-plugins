#!/usr/bin/env python3
"""email_assets.py - make email-sized derivatives from oversized source art.

The problem this exists for is specific and it is easy to miss until the send:
a site's banner assets are sized for a hero, and a hero is not an email. A
3200x1040 PNG averaging 663KB is a fine web asset and a bad email one, and
nothing about pointing an <img> at it will report a problem. The recipient just
waits.

It also enforces the two format rules that are not negotiable:

  * PNG out, always. Gmail strips <svg> from the DOM entirely, so a vector mark
    does not degrade in Gmail, it disappears.
  * No alpha on banners. A transparent PNG composited by a dark-mode client
    against its own background is a different picture than the one you tested,
    so banners are flattened onto a named ground.

Usage:
    python3 email_assets.py --banner src.png --out-dir dist/ [--column 536]
    python3 email_assets.py --icon src.png  --out-dir dist/ [--size 44]
    python3 email_assets.py --svg mark.svg  --out-dir dist/ --size 28

Emits at 2x the display size, because a 536px column on a retina screen wants a
1072px image, and reports the byte cost of each file it writes.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: pip install Pillow")

# The default column is 600px of card minus 32px of padding either side.
DEFAULT_COLUMN = 536
GROUND = (245, 243, 239)  # near-white, not #FFFFFF; see references/evidence.md


def report(path: pathlib.Path) -> None:
    kb = path.stat().st_size / 1024
    with Image.open(path) as im:
        w, h = im.size
    flag = "  <- over 200KB, compress further" if kb > 200 else ""
    print(f"  {path.name:38} {w}x{h}  {kb:6.1f} KB{flag}")


def flatten(im: Image.Image, ground: tuple[int, int, int]) -> Image.Image:
    """Composite onto a named ground rather than shipping alpha.

    A dark-mode client compositing a transparent PNG against its own background
    produces a picture nobody reviewed."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, ground)
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def do_banner(src: pathlib.Path, out: pathlib.Path, column: int) -> None:
    with Image.open(src) as im:
        target_w = column * 2
        ratio = target_w / im.width
        target_h = max(1, round(im.height * ratio))
        r = flatten(im, GROUND).resize((target_w, target_h), Image.LANCZOS)
        dst = out / f"{src.stem}-{target_w}.png"
        r.save(dst, optimize=True)
    report(dst)


def do_icon(src: pathlib.Path, out: pathlib.Path, size: int) -> None:
    with Image.open(src) as im:
        n = size * 2
        r = im.convert("RGBA").resize((n, n), Image.LANCZOS)
        dst = out / f"{src.stem}-{n}.png"
        # Icons keep their alpha: they sit on the card, and a squircle flattened
        # onto one ground looks wrong the moment a client repaints the other.
        r.save(dst, optimize=True)
    report(dst)


def do_svg(src: pathlib.Path, out: pathlib.Path, size: int) -> None:
    """Rasterise, because Gmail deletes the tag."""
    n = size * 2
    dst = out / f"{src.stem}-{n}.png"
    for cmd in (["rsvg-convert", "-w", str(n), "-h", str(n), "-o", str(dst), str(src)],
                ["magick", "-background", "none", "-density", "384",
                 str(src), "-resize", f"{n}x{n}", str(dst)],
                ["qlmanage", "-t", "-s", str(n), "-o", str(out), str(src)]):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if dst.exists():
                report(dst)
                return
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    sys.exit(f"could not rasterise {src}: install librsvg or ImageMagick. "
             "Shipping the SVG is not an option; Gmail strips the tag.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--banner", type=pathlib.Path, action="append", default=[])
    ap.add_argument("--icon", type=pathlib.Path, action="append", default=[])
    ap.add_argument("--svg", type=pathlib.Path, action="append", default=[])
    ap.add_argument("--out-dir", type=pathlib.Path, required=True)
    ap.add_argument("--column", type=int, default=DEFAULT_COLUMN,
                    help=f"content column width in CSS px (default {DEFAULT_COLUMN})")
    ap.add_argument("--size", type=int, default=44,
                    help="icon display size in CSS px (default 44)")
    a = ap.parse_args()

    if not (a.banner or a.icon or a.svg):
        ap.error("nothing to do: pass --banner, --icon or --svg")
    a.out_dir.mkdir(parents=True, exist_ok=True)

    for s in a.banner:
        do_banner(s, a.out_dir, a.column)
    for s in a.icon:
        do_icon(s, a.out_dir, a.size)
    for s in a.svg:
        do_svg(s, a.out_dir, a.size)

    print(f"\nWritten to {a.out_dir}. Every one needs an absolute URL on a host "
          "the recipient can reach:\na path that resolves on the site does not "
          "resolve in mail.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
