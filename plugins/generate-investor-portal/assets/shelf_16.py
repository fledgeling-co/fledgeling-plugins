#!/usr/bin/env python3
"""Put a candidate at 16px on the marketplace shelf, beside every sibling.

The reference is not the shelf. This renders every plugin's icon-256.png down to
16px, magnifies each 5x with no smoothing, and puts the candidate last, so a
16px identity collision with a sibling is visible before the commission ships.

    python3 shelf_16.py <candidate.png|candidate.svg> [out.png]
"""
import glob
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[3]
CELL, PAD, COLS = 80, 12, 9


def load16(path: Path) -> Image.Image:
    if path.suffix == ".svg":
        tmp = Path(tempfile.mkdtemp()) / "c.png"
        subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", str(path), "-o", str(tmp)], check=True)
        path = tmp
    return Image.open(path).convert("RGBA").resize((16, 16), Image.LANCZOS)


def main():
    cand = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/tmp/shelf16.png")
    cells = []
    for p in sorted(glob.glob(str(REPO / "plugins" / "*" / "assets" / "icon-256.png"))):
        name = os.path.basename(os.path.dirname(os.path.dirname(p)))
        if name == "generate-investor-portal":
            continue
        cells.append((name, load16(Path(p))))
    cells.append(("CANDIDATE", load16(cand)))

    rows = (len(cells) + COLS - 1) // COLS
    W = COLS * (CELL + PAD) + PAD
    H = rows * (CELL + 26) + PAD
    out = Image.new("RGB", (W, H), (247, 246, 243))
    d = ImageDraw.Draw(out)
    for i, (name, im) in enumerate(cells):
        x = PAD + (i % COLS) * (CELL + PAD)
        y = PAD + (i // COLS) * (CELL + 26)
        big = im.resize((CELL, CELL), Image.NEAREST)
        out.paste(big, (x, y), big)
        d.text((x, y + CELL + 4), name[:13], fill=(70, 70, 70))
    out.save(out_path)
    print(f"{len(cells)} tiles at 16px (magnified {CELL // 16}x) -> {out_path}")


if __name__ == "__main__":
    main()
