#!/usr/bin/env python3
"""Round 7 sweep A3 -- the ember ramp, with the two traps sweep A2 fell into.

A2 reported an |RG err| of 12 for a ramp that is not usable, and the two
reasons are worth keeping:

  * **A multiplicative value gain clips, and clipping flattens the ramp it was
    supposed to brighten.** At v_gain 1.14 three of the five face stops pinned
    at V=1.0, so the section's shoulder, its minimum and its outer stop all
    became the same colour. The measured image spread still rose -- the
    specular and the bevel wall carry that number -- so the metric happily
    rewarded destroying the cross-section. Remapping V affinely into
    [v_lo, v_hi] instead keeps the ramp monotone by construction.
  * **An error term over R and G alone buys its score with blue.** C's median
    ember is (244,88,49): B=49, saturation 0.80. Driving saturation up to cut G
    also drove B to zero, which scores well on |RG| and is a different colour
    from the reference. The error is over all three channels here.
"""
import colorsys
import itertools
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parents[2]
sys.path.insert(0, str(ASSETS))
sys.path.insert(0, str(HERE))
import build_icon as B  # noqa: E402
from sweep_ember import RAMP, ORIG, hex2rgb, rgb2hex, sample, fmt  # noqa: E402


def ramp(h_dark, h_lit, v_lo, v_hi, s_gain):
    hsv = {k: colorsys.rgb_to_hsv(*hex2rgb(v)) for k, v in ORIG.items()}
    lo = min(v for _, _, v in hsv.values())
    hi = max(v for _, _, v in hsv.values())
    out = {}
    for k, (_, s, v) in hsv.items():
        f = (v - lo) / (hi - lo) if hi > lo else 0.5
        h = h_dark + f * (h_lit - h_dark)
        out[k] = rgb2hex(*colorsys.hsv_to_rgb(h / 360.0,
                                              min(1.0, s * s_gain),
                                              v_lo + f * (v_hi - v_lo)))
    return out


def err3(s, ref):
    return sum(abs(s["core"][p][c] - ref["core"][p][c])
               for p in ("p10", "p50") for c in (0, 1, 2))


def main():
    ref = sample(ASSETS / "icon-engineC-clean.png")
    base = sample(ASSETS / "icon.png")
    print(f"C        core {fmt(ref['core'])}")
    print(f"r02      core {fmt(base['core'])}  err={err3(base, ref)}\n")

    B.GAP_HALF, B.PROTRUDE_FRAC = 40.0, 0.0
    rows = []
    for hd, hl, vlo, vhi, sg in itertools.product(
            (9.0, 11.0), (14.0, 16.0), (0.70, 0.76, 0.82),
            (0.97, 1.00), (1.00, 1.05)):
        cols = ramp(hd, hl, vlo, vhi, sg)
        for k, v in cols.items():
            setattr(B, k, v)
        tag = f"h{hd:.0f}_{hl:.0f}-v{vlo:.2f}_{vhi:.2f}-s{sg:.2f}"
        svg = HERE / "sweep" / f"{tag}.svg"
        png = HERE / "sweep" / f"{tag}.png"
        svg.write_text(B.build())
        subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024",
                        str(svg), "-o", str(png)], check=True)
        s = sample(png)
        rows.append((err3(s, ref), tag, s, cols))
    for k, v in ORIG.items():
        setattr(B, k, v)

    for e, tag, s, cols in sorted(rows):
        print(f"  {tag}  core {fmt(s['core'])}  err={e}")
    print("\ntop 3 ramps:")
    for e, tag, s, cols in sorted(rows)[:3]:
        print(f"  {tag} err={e} spread={s['core']['spread']:.3f} "
              f"body={fmt(s['body'])}")
        for k in RAMP:
            print(f"      {k:18s} {ORIG[k]} -> {cols[k]}")


if __name__ == "__main__":
    main()
