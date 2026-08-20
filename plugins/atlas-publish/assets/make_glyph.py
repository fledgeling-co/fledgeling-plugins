#!/usr/bin/env python3
"""Derive `glyph-path.txt` from the Atlas brand mark. Not run at build time.

The letterform in the icon is not drawn. It is the capital A of the Atlas script
wordmark, traced from the shipping brand asset and cut where the letter hands
over to the `t`. This script is how that file was made, kept beside it so the
provenance is reproducible rather than asserted.

    python3 make_glyph.py [path-to-atlas-icon.png]

Four steps:

1. Threshold the 1024x1024 black-on-white mark and trace it with potrace. The
   whole word comes back as one connected outline plus two counters, because
   the script is a single unbroken stroke.
2. Clip at x = 356 in the mark's own coordinate space. That is where the A's
   exit stroke would carry on into the `t`; measured off the render, the stroke
   there spans y 597-626 and is climbing at about 25 degrees. Cutting on a
   vertical leaves a flat butt for the gate to receive.
3. Outset by a 9-unit round-join stroke. This is the one liberty taken with the
   mark: a monoline drawn for a 1024 wordmark is about 30 units thick, which is
   1.0px at a 16px icon. The outset takes it to 1.4px and keeps the silhouette.
4. Re-trace the result at 4x supersampling and normalise to the 1024 space.

Requires `potrace` (brew install potrace), `rsvg-convert` and Pillow. The source
PNG lives in a different repository and is read-only; nothing here writes to it.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import svgpath

HERE = Path(__file__).resolve().parent
DEFAULT_MARK = Path(
    "/Users/lukerhodes/Dev/atlas-app/apps/atlas-app/assets/images/atlas-icon.png")

CUT_X = 356.0        # the A/t handover, in the mark's own 1024 coordinate space
FATTEN = 9.0         # uniform outset so the monoline carries mass at 16px
SUPERSAMPLE = 4
WORK = Path("/tmp/atlas-publish-glyph")


def trace(pbm: Path, out: Path, unit: str) -> str:
    subprocess.run(["potrace", "-s", "-o", str(out), "--alphamax", "1.0",
                    "--opttolerance", "0.15", "-u", unit, str(pbm)], check=True)
    text = out.read_text()
    m = re.search(r'<g transform="translate\(([-\d.]+),([-\d.]+)\) '
                  r'scale\(([-\d.]+),([-\d.]+)\)"[^>]*>\s*<path d="(.*?)"', text, re.S)
    if not m:
        raise SystemExit(f"potrace output in {out} did not match the expected shape")
    return m


def main() -> int:
    mark = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MARK
    if not mark.exists():
        raise SystemExit(f"no brand mark at {mark}")
    WORK.mkdir(parents=True, exist_ok=True)

    from PIL import Image

    # 1. threshold + trace the whole mark
    im = Image.open(mark).convert("L")
    im.point(lambda p: 0 if p < 128 else 255, "1").save(WORK / "mark.pbm")
    m = trace(WORK / "mark.pbm", WORK / "mark.svg", "10")
    tx, ty, sx, sy = (float(m.group(i)) for i in (1, 2, 3, 4))
    whole = svgpath.emit(svgpath.xf(svgpath.parse(m.group(5)), sx, 0, 0, sy, tx, ty))

    # 2 + 3. clip at the handover and outset, rendered at supersample
    px = 1024 * SUPERSAMPLE
    (WORK / "cut.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" '
        f'viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="#fff"/>'
        f'<defs><clipPath id="c"><rect x="0" y="0" width="{CUT_X}" height="1024"/>'
        f'</clipPath></defs><g clip-path="url(#c)"><path d="{whole}" fill="#000" '
        f'stroke="#000" stroke-width="{FATTEN}" stroke-linejoin="round"/></g></svg>')
    subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px),
                    "-o", str(WORK / "cut.png"), str(WORK / "cut.svg")], check=True)
    cut = Image.open(WORK / "cut.png").convert("L")
    cut.point(lambda p: 0 if p < 128 else 255, "1").save(WORK / "cut.pbm")

    # 4. re-trace and normalise back to the 1024 space
    m2 = trace(WORK / "cut.pbm", WORK / "cut-trace.svg", "10")
    tx, ty, sx, sy = (float(m2.group(i)) for i in (1, 2, 3, 4))
    subs = svgpath.xf(svgpath.parse(m2.group(5)), sx, 0, 0, sy, tx, ty)
    subs = svgpath.xf(subs, 1.0 / SUPERSAMPLE, 0, 0, 1.0 / SUPERSAMPLE, 0, 0)

    out = HERE / "glyph-path.txt"
    out.write_text(svgpath.emit(subs, 2))
    x0, y0, x1, y1 = svgpath.bbox(subs)
    print(f"wrote {out.name}: bbox ({x0:.2f}, {y0:.2f}) -> ({x1:.2f}, {y1:.2f})")
    print("Update GLYPH_BBOX in build_icon.py if this moved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
