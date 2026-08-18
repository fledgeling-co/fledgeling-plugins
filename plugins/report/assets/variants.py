#!/usr/bin/env python3
"""Render the appearance variants rubric #10 asks about, and measure them.

Rubric #10 is "survives Default / Dark / Clear / Tinted; identity not hostage to one
background colour", and until 19 Aug 2026 the `report` commission asserted a verdict
on it without rendering a single variant. This script renders them, so the sheet can
cite pixels instead of an argument.

What it does is a substitution in the `bg` layer only: the ground gradient's three
stops and the tile's crown highlight are swapped for another register, and every
other layer — the sheet, the ruling, the crease, the shadows — is left exactly as
authored. That is the whole point of the layer plan: if identity is carried by shape
and value rather than by one colour relationship, the object stays legible when the
ground moves, and if it is not, it disappears. Nothing here touches the shipped
`icon.svg`; the variants are written to `variant-renders/`.

A single-layer raster take has no `bg` group to substitute, which is not a limitation
of this script — it is the 76% failure mode the rubric is about, and the reason the
Engine C takes have no rows in the variant table.
"""

import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "variant-renders"

TAKES = {"master": "icon.svg", "A2": "icon-A2-fold-inverted.svg"}

# The default register each master is authored in, so the substitution is exact
# rather than a guess at what the stops currently are.
DEFAULT = ("#FFFDF8", "#F7F2E9", "#EFE8DB")

REGISTERS = {
    # macOS Dark: the tile ground goes to a deep neutral. The crown highlight is
    # dimmed with it, because a 0.92-opacity white crown on a dark ground is a
    # blown-out flare rather than a top light.
    "dark": {"stops": ("#2C3236", "#1C2226", "#12171A"), "crown": "0.16"},
    # Tinted: the system paints one hue through the tile. Grey-blue here, which is
    # the register that most often kills a warm porcelain-on-porcelain identity.
    "tinted": {"stops": ("#C9D2DC", "#AEBAC7", "#95A3B2"), "crown": "0.42"},
}


def variant(svg: str, stops: tuple[str, str, str], crown: str) -> str:
    for old, new in zip(DEFAULT, stops):
        svg = svg.replace(f'stop-color="{old}"', f'stop-color="{new}"', 1)
    return re.sub(r'(<stop offset="0" stop-color="#FFFFFF" stop-opacity=")0\.92(")',
                  rf"\g<1>{crown}\g<2>", svg, count=1)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    made = 0
    for take, src in TAKES.items():
        text = (HERE / src).read_text()
        missing = [s for s in DEFAULT if f'stop-color="{s}"' not in text]
        if missing:
            print(f"FAIL  {src} does not carry the expected ground stops {missing} — "
                  f"the substitution would silently do nothing", file=sys.stderr)
            return 1
        for name, reg in REGISTERS.items():
            tmp = OUT / f"_{take}-{name}.svg"
            tmp.write_text(variant(text, reg["stops"], reg["crown"]))
            for size in (256, 64):
                subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                                str(tmp), "-o", str(OUT / f"{take}-{name}-{size}.png")],
                               check=True)
                made += 1
            tmp.unlink()
        print(f"  {take}: dark, tinted at 256 and 64")
    print(f"\n{made} variant renders into {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
