#!/usr/bin/env python3
"""Round 7 sweep A -- the ember ramp's hue and value, measured against take C.

The ask was "brighter red", and the sampled gap said what that means:
C's ember sits at a near-constant hue of 12-13 degrees at every percentile,
where the master's ramp ran 16-26; and C is brighter through the midtones,
median V 0.957 against 0.882. So the edit is a hue rotation plus a value lift
applied to the seven face-and-wall stops, with the specular left alone (it
already matched C's brightest ember pixel).

Sweeps h_target x v_gain x s_gain, renders each, and reports the sampled
percentiles against C's under the same mask. Run from the assets directory.
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

# The face and wall stops. The specular, bounce and cut-face stay as they are:
# they already measure against C's brightest ember pixel.
RAMP = ["EM_WALL_LIT", "EM_WALL_DARK", "EM_FACE_IN", "EM_FACE_BOUNCE",
        "EM_FACE_DARK", "EM_FACE_SHOULDER", "EM_FACE_OUT"]
ORIG = {k: getattr(B, k) for k in RAMP}


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def rgb2hex(r, g, b):
    return "#%02X%02X%02X" % tuple(min(255, max(0, round(c * 255)))
                                   for c in (r, g, b))


def shift(hexcol, h_deg, v_gain, s_gain):
    r, g, b = hex2rgb(hexcol)
    _, s, v = colorsys.rgb_to_hsv(r, g, b)
    return rgb2hex(*colorsys.hsv_to_rgb(h_deg / 360.0,
                                        min(1.0, s * s_gain),
                                        min(1.0, v * v_gain)))


# --- the sampler -------------------------------------------------------------
# Two masks, both applied identically to candidate and reference.
#   body: the repo's established warm mask, plus a green bound so the porcelain
#         under the ember's spill does not count as ember.
#   core: a stricter cut that keeps only strongly-warm pixels -- the ramp
#         itself, with the anti-aliased skirt and the pale specular excluded.
def masks(I):
    body = (I[..., 0] > 140) & (I[..., 0] > I[..., 2] + 55) & \
           (I[..., 0] > I[..., 1] + 55)
    core = (I[..., 0] > 140) & (I[..., 0] > I[..., 1] + 100)
    return {"body": body, "core": core}


def sample(path):
    I = np.asarray(Image.open(path).convert("RGB"), dtype=float)
    out = {}
    for name, m in masks(I).items():
        px = I[m]
        if len(px) < 500:
            out[name] = None
            continue
        L = (0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]) / 255
        out[name] = dict(
            n=int(m.sum()),
            p10=tuple(int(v) for v in np.percentile(px, 10, axis=0)),
            p50=tuple(int(v) for v in np.percentile(px, 50, axis=0)),
            p90=tuple(int(v) for v in np.percentile(px, 90, axis=0)),
            peakR=int(px[:, 0].max()),
            spread=float(np.percentile(L, 95) - np.percentile(L, 5)),
        )
    return out


def fmt(s):
    return (f"p10={s['p10']} p50={s['p50']} p90={s['p90']} "
            f"peakR={s['peakR']} spread={s['spread']:.3f}")


def render(svg_text, tag):
    svg = HERE / "sweep" / f"{tag}.svg"
    png = HERE / "sweep" / f"{tag}.png"
    svg.write_text(svg_text)
    subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024",
                    str(svg), "-o", str(png)], check=True)
    return png


def main():
    (HERE / "sweep").mkdir(exist_ok=True)
    ref = sample(ASSETS / "icon-engineC-clean.png")
    print("REFERENCE C")
    for k, v in ref.items():
        print(f"  {k:5s} {fmt(v)}")

    base = sample(ASSETS / "icon.png")
    print("BASELINE r02 master")
    for k, v in base.items():
        print(f"  {k:5s} {fmt(v)}")

    print("\nSWEEP  (geometry held at the r02 values so this axis is isolated)")
    B.GAP_HALF, B.PROTRUDE_FRAC = 40.0, 0.0
    rows = []
    for h, vg, sg in itertools.product((12, 14, 16), (1.00, 1.06, 1.12),
                                       (1.00, 1.06)):
        for k in RAMP:
            setattr(B, k, shift(ORIG[k], h, vg, sg))
        tag = f"h{h}-v{vg:.2f}-s{sg:.2f}"
        png = render(B.build(), tag)
        s = sample(png)
        rows.append((tag, s))
        err = sum(abs(s["core"][p][c] - ref["core"][p][c])
                  for p in ("p10", "p50") for c in (0, 1))
        print(f"  {tag}  core {fmt(s['core'])}  |RG err|={err}")
    for k, v in ORIG.items():
        setattr(B, k, v)


if __name__ == "__main__":
    main()
