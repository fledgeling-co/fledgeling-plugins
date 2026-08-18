#!/usr/bin/env python3
"""Render the audit sheet's retina sources for every take.

Naming matches audit.html: <id>-{256,128,96,64,32}.png, displayed at
128/64/48/32/16 css px. The 48px row is the Finder-list and marketplace-tile
size, and an icon that survives 128 and 16 can still fail between them, which
is why audit_sheet.py's checker insists on it.

Take A's 64 and 32 sources come from `icon-small.svg`, not from the master.
That is deliberate: those are the files that actually ship at those sizes
(build_icon.py floors the specular at 64px and below), and a contact sheet
that shows something other than the shipped raster is measuring the wrong
artifact. 96 and above come from the master, on the same rule.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent
DEST = OUT / "audit-renders"
# 1024 is the hero the sheet displays and audit_sheet.py check requires a source
# for it, so leaving it out left every take without a hero render.
SIZES = (1024, 256, 128, 96, 64, 32)


def src_for(take, size):
    if take == "A":
        return "icon.svg" if size >= 96 else "icon-small.svg"
    return {
        "A1": "fidelity/runs/r03/baseline-r02.svg",
        "A0": "icon-src.svg",
        "B": "icon-engineB-arrow.svg",
        "C": "icon-engineC-clean.png",
        "Craw": "icon-engineC-raster.png",
    }[take]


def main():
    DEST.mkdir(exist_ok=True)
    for take in ("A", "A1", "A0", "B", "C", "Craw"):
        for size in SIZES:
            src = src_for(take, size)
            s = OUT / src
            d = DEST / f"{take}-{size}.png"
            if s.suffix == ".svg":
                subprocess.run(["rsvg-convert", "-w", str(size), "-h",
                                str(size), str(s), "-o", str(d)], check=True)
            else:
                Image.open(s).convert("RGBA").resize((size, size),
                                                     Image.LANCZOS).save(d)
        print(f"  {take}: {', '.join(str(s) for s in SIZES)}"
              f"  <- {src_for(take, 256)}"
              + (" / icon-small.svg at 64,32" if take == "A" else ""))


if __name__ == "__main__":
    sys.exit(main())
