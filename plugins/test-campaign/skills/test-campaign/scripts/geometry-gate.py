#!/usr/bin/env python3
"""Decide a visual difference on its bounding box and density, not on a ratio.

A whole-frame difference ratio cannot discriminate. Measured on a real one-step
spacing change: 558 divergent pixels of 1,296,000 is a ratio of 0.00043, which
every whole-frame threshold passes, while the diff bounding box was 114x13 at a
fill density of 0.377 and unmistakable.

The discriminating property is not how much changed but how CONCENTRATED it is.
Two images with the same ratio separate cleanly:

    localised  box 114x13    density 0.3765   FIRES
    scatter    box 1381x829  density 0.0005   does not

Portable by construction: pure image maths over two same-size images, no browser,
no project layout, no framework. Point it at any pair.

    geometry-gate.py a.png b.png
    geometry-gate.py a.png b.png --json
    geometry-gate.py --selftest        # synthetic pair, no files needed

`--stable a1.png a2.png b1.png b2.png` scores TWO renders of the same comparison
and reports whether they agree (IoU of the diff boxes). A visual defect needs two
renders that agree; disagreement is "cannot tell", not a pass. Never retry a hard
deterministic mismatch to obtain a green — that turns a real defect into a flake.

Needs Pillow for real files. `--selftest` runs without it.
"""
from __future__ import annotations
import argparse, json, sys

# Floors calibrated on the measurement above. `min_pixels` and `min_box` scale
# with frame area so the same numbers hold at another resolution; `min_density`
# does not, because density is already scale-free.
DEFAULTS = {"min_pixels_ppm": 150.0, "min_box_ppm": 400.0, "min_density": 0.12}


def diff_mask(a, b, threshold=16):
    """Per-pixel divergence as a set of (x, y). `a`/`b` are (w, h, flat RGB)."""
    (w, h, pa), (_, _, pb) = a, b
    out = set()
    for i in range(w * h):
        j = i * 3
        if (abs(pa[j] - pb[j]) + abs(pa[j+1] - pb[j+1]) + abs(pa[j+2] - pb[j+2])) > threshold:
            out.add((i % w, i // w))
    return out


def geometry(mask, w, h):
    if not mask:
        return {"pixels": 0, "box": None, "box_area": 0, "density": 0.0,
                "ratio": 0.0, "frame": w * h}
    xs = [p[0] for p in mask]; ys = [p[1] for p in mask]
    bw = max(xs) - min(xs) + 1
    bh = max(ys) - min(ys) + 1
    area = bw * bh
    return {
        "pixels": len(mask),
        "box": {"x": min(xs), "y": min(ys), "w": bw, "h": bh},
        "box_area": area,
        "density": len(mask) / area,
        "ratio": len(mask) / (w * h),
        "frame": w * h,
    }


def verdict(g, floors=DEFAULTS):
    """FIRES only when all three hold. Any one alone is defeatable.

    Pixels alone fires on a re-render. Box alone fires on two specks at opposite
    corners. Density alone fires on a 2x2 block. Together they describe "a real,
    concentrated change", which is what a defect looks like.
    """
    if not g["pixels"]:
        return {"fires": False, "why": ["identical"]}
    scale = g["frame"] / 1_000_000
    min_px = floors["min_pixels_ppm"] * scale
    min_box = floors["min_box_ppm"] * scale
    checks = [
        (g["pixels"] >= min_px, f"pixels {g['pixels']} vs floor {min_px:.1f}"),
        (g["box_area"] >= min_box, f"box {g['box']['w']}x{g['box']['h']} = {g['box_area']} vs floor {min_box:.1f}"),
        (g["density"] >= floors["min_density"], f"density {g['density']:.4f} vs floor {floors['min_density']}"),
    ]
    return {"fires": all(c[0] for c in checks),
            "why": [("above " if ok else "below ") + msg for ok, msg in checks]}


def iou(g1, g2):
    """Overlap of two diff boxes. Two renders agree when this is near 1."""
    b1, b2 = g1.get("box"), g2.get("box")
    if not b1 or not b2:
        return 1.0 if b1 == b2 else 0.0
    x = max(0, min(b1["x"]+b1["w"], b2["x"]+b2["w"]) - max(b1["x"], b2["x"]))
    y = max(0, min(b1["y"]+b1["h"], b2["y"]+b2["h"]) - max(b1["y"], b2["y"]))
    inter = x * y
    union = b1["w"]*b1["h"] + b2["w"]*b2["h"] - inter
    return inter / union if union else 0.0


def load(path):
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("geometry-gate: Pillow is required for image files (pip install pillow). "
                         "`--selftest` runs without it.")
    im = Image.open(path).convert("RGB")
    return im.width, im.height, list(im.tobytes())


def synth(w, h, rects):
    """A flat frame with filled rects, for the selftest."""
    px = [255] * (w * h * 3)
    for (x, y, rw, rh) in rects:
        for yy in range(y, min(y + rh, h)):
            for xx in range(x, min(x + rw, w)):
                i = (yy * w + xx) * 3
                px[i] = px[i+1] = px[i+2] = 0
    return (w, h, px)


def selftest() -> int:
    W = H = 400
    base = synth(W, H, [])
    # Localised: one dense block. Scatter: the same pixel count spread wide.
    n = 900
    local = synth(W, H, [(10, 10, 30, 30)])
    side = int(n ** 0.5)
    scatter = synth(W, H, [(i * 13 % (W - 2), i * 29 % (H - 2), 1, 1) for i in range(n)])

    gl = geometry(diff_mask(base, local), W, H)
    gs = geometry(diff_mask(base, scatter), W, H)
    gz = geometry(diff_mask(base, base), W, H)

    cases = [
        ("identical does not fire", not verdict(gz)["fires"]),
        ("localised fires", verdict(gl)["fires"]),
        ("scatter does not fire", not verdict(gs)["fires"]),
        ("scatter box is far larger than localised", gs["box_area"] > gl["box_area"] * 10),
        ("localised density exceeds scatter density", gl["density"] > gs["density"] * 10),
        ("two identical renders agree", iou(gl, gl) > 0.99),
        ("renders in different places disagree", iou(gl, gs) < 0.5),
    ]
    bad = 0
    for name, ok in cases:
        bad += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {name}")
    print(f"\n  localised  box {gl['box']['w']}x{gl['box']['h']}  density {gl['density']:.4f}  ratio {gl['ratio']:.6f}")
    print(f"  scatter    box {gs['box']['w']}x{gs['box']['h']}  density {gs['density']:.4f}  ratio {gs['ratio']:.6f}")
    print(f"\n{len(cases) - bad} of {len(cases)} rules fired as specified")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("images", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--stable", action="store_true",
                    help="four images: a1 a2 b1 b2 — two renders of the same comparison")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    if a.stable:
        if len(a.images) != 4:
            raise SystemExit("--stable needs four images: a1 a2 b1 b2")
        i = [load(p) for p in a.images]
        g1 = geometry(diff_mask(i[0], i[2]), i[0][0], i[0][1])
        g2 = geometry(diff_mask(i[1], i[3]), i[1][0], i[1][1])
        v1, v2 = verdict(g1), verdict(g2)
        agree = iou(g1, g2)
        state = ("defect" if v1["fires"] and v2["fires"] and agree >= 0.5
                 else "agrees" if not v1["fires"] and not v2["fires"]
                 else "unstable")
        out = {"state": state, "iou": agree, "render1": {**g1, **v1}, "render2": {**g2, **v2}}
        print(json.dumps(out, indent=1) if a.json else
              f"{state} — IoU {agree:.4f}; render1 {'fires' if v1['fires'] else 'quiet'}, "
              f"render2 {'fires' if v2['fires'] else 'quiet'}")
        return 1 if state == "defect" else 0

    if len(a.images) != 2:
        raise SystemExit("geometry-gate: two images, or --stable with four, or --selftest")
    x, y = load(a.images[0]), load(a.images[1])
    if (x[0], x[1]) != (y[0], y[1]):
        raise SystemExit(f"geometry-gate: sizes differ ({x[0]}x{x[1]} vs {y[0]}x{y[1]}). "
                         "Resize deliberately and say so; a silent resize invents pixels.")
    g = geometry(diff_mask(x, y), x[0], x[1])
    v = verdict(g)
    if a.json:
        print(json.dumps({**g, **v}, indent=1))
    else:
        print(f"{'FIRES' if v['fires'] else 'quiet'} — " + " · ".join(v["why"]))
        if g["box"]:
            print(f"  box {g['box']['w']}x{g['box']['h']} at ({g['box']['x']},{g['box']['y']}) "
                  f"· density {g['density']:.4f} · whole-frame ratio {g['ratio']:.6f}")
    return 1 if v["fires"] else 0


if __name__ == "__main__":
    sys.exit(main())
