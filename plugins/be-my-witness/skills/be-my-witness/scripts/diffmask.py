#!/usr/bin/env python3
"""
diffmask.py — turn a pixel diff into the thing a VLM should look at.

WHY THIS EXISTS

Two measured facts from the research, which only pay off together:

  1. Pixel diff on UI screenshots scores 100.00% change-accuracy and 0.00%
     no-change-accuracy (WUICC-bench). It is a near-perfect DETECTOR and a
     worthless DISCRIMINATOR: it finds every real change and also every
     anti-aliased edge, and cannot tell you which is which.
  2. A VLM handed two whole screenshots spends its attention hunting for the
     difference, and often does not find it.

So: let the detector detect, and give the discriminator a map. The industry
pattern is a TRI-IMAGE payload -- baseline, candidate, and the red/green diff as
a guiding mask -- which stops the model scanning and makes its job classification
rather than search.

THRESHOLDS

Defaults follow Playwright's, because they are the most widely exercised numbers
in the field: comparison in YIQ (which separates luma from chroma, so sub-pixel
colour shifts and anti-aliasing are tolerated), a per-pixel `threshold` of 0.2,
and a `maxDiffPixelRatio` of 0.01-0.05 above which the surfaces are treated as
materially different.

USAGE
    python3 diffmask.py a.png b.png --out diff.png --json
    python3 diffmask.py a.png b.png --threshold 0.2 --max-ratio 0.01

EXIT CODES
    0  differing pixels within maxDiffPixelRatio  (noise-level)
    1  above the ratio                            (worth a look)
    2  the two images are not the same size       (framing, not drift)
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path


def load(path: Path):
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("diffmask.py needs Pillow. Install it, or use prescan.py alone.")
    im = Image.open(path).convert("RGB")
    return im


def yiq(r, g, b):
    """Y, I, Q. Luma first: it is what carries structure, and chroma is where
    anti-aliasing noise lives."""
    return (0.29889531 * r + 0.58662247 * g + 0.11448223 * b,
            0.59597799 * r - 0.27417610 * g - 0.32180189 * b,
            0.21147017 * r - 0.52261711 * g + 0.31114694 * b)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("baseline", type=Path)
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--out", type=Path, help="write the red/green mask here")
    ap.add_argument("--threshold", type=float, default=0.2, help="per-pixel YIQ distance, 0 strict to 1 lax (default 0.2)")
    ap.add_argument("--max-ratio", type=float, default=0.01, help="share of pixels allowed to differ (default 0.01)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    from PIL import Image
    a, b = load(args.baseline), load(args.candidate)
    if a.size != b.size:
        msg = (f"{a.size[0]}x{a.size[1]} vs {b.size[0]}x{b.size[1]}: not the same size. "
               "This is a FRAMING difference; normalise the crop before comparing pixels.")
        print(json.dumps({"comparable": False, "reason": msg}, indent=1) if args.json else "! " + msg)
        sys.exit(2)

    w, h = a.size
    pa, pb = a.load(), b.load()
    # 35215 is the max possible YIQ distance, per pixelmatch.
    cutoff = 35215 * args.threshold * args.threshold
    mask = Image.new("RGB", (w, h))
    pm = mask.load()
    differing = 0
    for y in range(h):
        for x in range(w):
            r1, g1, b1 = pa[x, y]
            r2, g2, b2 = pb[x, y]
            if (r1, g1, b1) == (r2, g2, b2):
                Y, _, _ = yiq(r1, g1, b1)
                v = int(255 - (255 - Y) * 0.9)      # ghost the unchanged ground
                pm[x, y] = (v, v, v)
                continue
            y1, i1, q1 = yiq(r1, g1, b1)
            y2, i2, q2 = yiq(r2, g2, b2)
            dy, di, dq = y1 - y2, i1 - i2, q1 - q2
            delta = 0.5053 * dy * dy + 0.299 * di * di + 0.1957 * dq * dq
            if delta > cutoff:
                differing += 1
                # Red where the candidate is darker than the baseline, green where
                # lighter: direction is information a flat highlight throws away.
                pm[x, y] = (255, 60, 60) if y2 < y1 else (60, 200, 90)
            else:
                Y, _, _ = yiq(r1, g1, b1)
                v = int(255 - (255 - Y) * 0.9)
                pm[x, y] = (v, v, v)

    total = w * h
    ratio = differing / total
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        mask.save(args.out)

    result = {
        "comparable": True, "width": w, "height": h,
        "differingPixels": differing, "totalPixels": total,
        "diffRatio": round(ratio, 6),
        "threshold": args.threshold, "maxDiffPixelRatio": args.max_ratio,
        "aboveRatio": ratio > args.max_ratio,
        "mask": str(args.out) if args.out else None,
        "note": ("A diff ratio is a DETECTOR result, never a verdict. Pixel comparison "
                 "scores ~100% change-accuracy and ~0% no-change-accuracy on UI "
                 "screenshots: everything it flags still needs classifying."),
    }
    print(json.dumps(result, indent=1) if args.json
          else f"{differing}/{total} px differ ({ratio:.4%}) · above ratio: {result['aboveRatio']}"
               + (f" · mask: {args.out}" if args.out else ""))
    sys.exit(1 if result["aboveRatio"] else 0)


if __name__ == "__main__":
    main()
