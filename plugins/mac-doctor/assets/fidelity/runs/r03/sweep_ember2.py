#!/usr/bin/env python3
"""Round 7 sweep A2 -- refining the ember ramp.

Sweep A settled the direction (hue down to ~12, value up ~12%, saturation up
~6%). Two things it left on the table, both read off C rather than assumed:

  * C's ember hue is not quite constant. Its core p10 sits at 10.5 degrees and
    its p90 at 14.6 -- the dark end is redder than the lit end. A single
    h_target flattens that.
  * C's core luminance spread is 0.256 against the master's 0.177. A uniform
    value gain moves the whole ramp and leaves the spread where it was, so a
    separate gain pushing each stop away from the ramp's own mid is what
    actually widens it.

So: hue interpolated by each stop's value between h_dark and h_lit, a spread
gain about the ramp mid, then the overall value and saturation gains.
"""
import colorsys
import itertools
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parents[2]
sys.path.insert(0, str(ASSETS))
import build_icon as B  # noqa: E402
from sweep_ember import RAMP, ORIG, hex2rgb, rgb2hex, sample, fmt  # noqa: E402


def ramp(h_dark, h_lit, v_gain, s_gain, spread):
    vs = {k: colorsys.rgb_to_hsv(*hex2rgb(v))[2] for k, v in ORIG.items()}
    lo, hi = min(vs.values()), max(vs.values())
    mid = sum(vs.values()) / len(vs)
    out = {}
    for k, hexcol in ORIG.items():
        _, s, v = colorsys.rgb_to_hsv(*hex2rgb(hexcol))
        f = (v - lo) / (hi - lo) if hi > lo else 0.5
        h = h_dark + f * (h_lit - h_dark)
        v2 = min(1.0, max(0.0, (mid + (v - mid) * spread) * v_gain))
        out[k] = rgb2hex(*colorsys.hsv_to_rgb(h / 360.0,
                                              min(1.0, s * s_gain), v2))
    return out


def main():
    ref = sample(ASSETS / "icon-engineC-clean.png")
    base = sample(ASSETS / "icon.png")
    print(f"C        core {fmt(ref['core'])}")
    print(f"r02      core {fmt(base['core'])}\n")

    B.GAP_HALF, B.PROTRUDE_FRAC = 40.0, 0.0
    best = []
    for hd, hl, vg, sg, sp in itertools.product(
            (10.0,), (15.0,), (1.10, 1.14), (1.06, 1.12),
            (1.00, 1.15, 1.30, 1.45)):
        cols = ramp(hd, hl, vg, sg, sp)
        for k, v in cols.items():
            setattr(B, k, v)
        tag = f"h{hd:.0f}-{hl:.0f}-v{vg:.2f}-s{sg:.2f}-x{sp:.2f}"
        svg = HERE / "sweep" / f"{tag}.svg"
        png = HERE / "sweep" / f"{tag}.png"
        svg.write_text(B.build())
        subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024",
                        str(svg), "-o", str(png)], check=True)
        s = sample(png)
        err = sum(abs(s["core"][p][c] - ref["core"][p][c])
                  for p in ("p10", "p50") for c in (0, 1))
        best.append((err, -s["core"]["spread"], tag, s, cols))
        print(f"  {tag}  core {fmt(s['core'])}  |RG err|={err}")
    for k, v in ORIG.items():
        setattr(B, k, v)
    print("\nbest by |RG err| then spread:")
    for e, ns, tag, s, cols in sorted(best)[:4]:
        print(f"  {tag}  err={e} spread={-ns:.3f}")
        print("   ", {k: v for k, v in cols.items()})


if __name__ == "__main__":
    main()
