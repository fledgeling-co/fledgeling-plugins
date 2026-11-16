"""Scan every sampled frame of one video with be-my-witness's prescan, plus a
vectorised version of its diffmask metric between consecutive frames.

    python3 -I scan_frames.py <video-dir> <be-my-witness-scripts-dir>

prescan.analyse/verdicts are imported unchanged. The consecutive-frame diff uses
diffmask.py's formula (pixelmatch YIQ distance, per-pixel threshold 0.2) in numpy
on 640-wide copies, because the pure-Python original takes seconds per pair.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

video_dir = Path(sys.argv[1])
sys.path.insert(0, sys.argv[2])
import prescan  # noqa: E402

frames = sorted((video_dir / "frames").glob("f*.jpg"))
THRESH = 0.2
CUTOFF = 35215 * THRESH * THRESH


def yiq(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    y = r * 0.29889531 + g * 0.58662247 + b * 0.11448223
    i = r * 0.59597799 - g * 0.27417610 - b * 0.32180189
    q = r * 0.21147017 - g * 0.52261711 + b * 0.31114694
    return y, i, q


def small(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    return np.asarray(im.resize((640, round(640 * h / w))), dtype=np.float64)


out = []
prev = None
for idx, f in enumerate(frames):
    a = prescan.analyse(f)
    v = prescan.verdicts(a)
    checks = v[0] if isinstance(v, tuple) else v
    row = {
        "frame": f.name,
        "t": idx * 2,
        "meanLuminance": a["meanLuminance"],
        "contentfulCells": a["contentfulCells"],
        "blankCells": a["blankCells"],
        "isEvidence": bool(checks.get("isEvidence", True)) if isinstance(checks, dict) else None,
    }
    cur = small(f)
    if prev is not None and prev.shape == cur.shape:
        y1, i1, q1 = yiq(prev)
        y2, i2, q2 = yiq(cur)
        delta = 0.5053 * (y1 - y2) ** 2 + 0.299 * (i1 - i2) ** 2 + 0.1957 * (q1 - q2) ** 2
        diff = delta > CUTOFF
        row["diffFromPrev"] = round(float(diff.mean()), 4)
        if diff.any():
            ys, xs = np.nonzero(diff)
            h, w = diff.shape
            row["diffBoxFromPrev"] = [round(xs.min() / w, 3), round(ys.min() / h, 3),
                                      round((xs.max() - xs.min() + 1) / w, 3), round((ys.max() - ys.min() + 1) / h, 3)]
    else:
        row["diffFromPrev"] = None
    prev = cur
    out.append(row)

print(json.dumps({"frames": out, "method": "prescan.analyse/verdicts + numpy pixelmatch YIQ diff at 640w, threshold 0.2"}, indent=1))
