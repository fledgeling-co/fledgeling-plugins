#!/usr/bin/env python3
"""Rebuild the master and put it on the review strip: 1024, 128, 32, 16.

    python3 preview.py            # rebuilds icon.svg, writes /tmp/gip-review.png
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SIZES = (1024, 256, 128, 96, 64, 32)


def render(src: Path, out_dir: Path, prefix: str):
    for s in SIZES:
        subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(src),
                        "-o", str(out_dir / f"{prefix}-{s}.png")], check=True)


def strip(prefix: str, out_dir: Path, dst: Path):
    hero = Image.open(out_dir / f"{prefix}-1024.png").convert("RGBA")
    shown = [(256, 128), (128, 64), (96, 48), (64, 32), (32, 16)]
    W = 1024 + 40 + 200
    out = Image.new("RGBA", (W, 1024), (250, 249, 246, 255))
    out.alpha_composite(hero, (0, 0))
    y = 10
    for src, css in shown:
        im = Image.open(out_dir / f"{prefix}-{src}.png").convert("RGBA").resize((css, css), Image.LANCZOS)
        out.alpha_composite(im, (1064, y))
        y += css + 18
    # the 16px squint, magnified 8x with no smoothing
    sq = Image.open(out_dir / f"{prefix}-32.png").convert("RGBA").resize((16, 16), Image.LANCZOS)
    out.alpha_composite(sq.resize((128, 128), Image.NEAREST), (1064, y + 10))
    out.convert("RGB").save(dst)


if __name__ == "__main__":
    subprocess.run([sys.executable, str(HERE / "build_icon.py")], check=True)
    tmp = Path("/tmp/gip-preview")
    tmp.mkdir(exist_ok=True)
    src = HERE / (sys.argv[1] if len(sys.argv) > 1 else "icon.svg")
    render(src, tmp, "p")
    strip("p", tmp, Path("/tmp/gip-review.png"))
    print("wrote /tmp/gip-review.png")
