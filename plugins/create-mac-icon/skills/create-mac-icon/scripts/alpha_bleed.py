#!/usr/bin/env python3
"""alpha_bleed.py — kill the dark halo a downscaled RGBA icon grows on a light ground.

An icon exported with transparent corners usually stores RGB (0,0,0) in every fully
transparent pixel. Nothing shows it at 1:1, because alpha is 0. But a browser, a
README and the site all *downscale* it, and downscaling filters RGB and alpha
independently in straight (non-premultiplied) space, so the black in those corners
gets averaged into the silhouette's edge pixels. The result is a thin dark outline
hugging the shape, worst on a pale ground, and it survives every check anyone makes
of an icon because the file itself is correct at full size.

The fix is to flood the edge colour outward into the transparent region, so there is
no black left to average in. Alpha is never touched, so the icon is pixel-identical
everywhere it is actually visible.

    alpha_bleed.py <icon.png> [more.png ...]      # rewrite in place
    alpha_bleed.py <icon.png> --check             # report only, exit 1 if it would change
"""
from __future__ import annotations
import sys
import numpy as np
from PIL import Image


def bleed(path: str, apply: bool = True, passes: int = 24) -> tuple[int, bool]:
    im = Image.open(path).convert("RGBA")
    a = np.array(im).astype(np.float64)
    alpha = a[..., 3]
    rgb = a[..., :3]

    known = alpha > 0
    if known.all():
        return 0, False

    # How many transparent pixels would actually contaminate an edge. The test is
    # not "is this pixel dark" — an icon whose artwork runs black right up to the
    # silhouette produces dark transparent pixels legitimately, and `trawl` does
    # exactly that. The test is whether the pixel disagrees with the visible
    # neighbour it will be averaged against, because that disagreement is the only
    # thing a resampler can turn into a halo.
    touching = np.zeros_like(known)
    nsum = np.zeros(known.shape + (3,), dtype=np.float64)
    ncnt = np.zeros(known.shape, dtype=np.float64)
    # Same eight-neighbour set the fill uses, so the check and the fix agree; a
    # four-neighbour check against an eight-neighbour fill reports a residual that
    # is arithmetic rather than a defect.
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        m = np.roll(known, (dy, dx), (0, 1))
        touching |= m
        nsum += np.roll(rgb, (dy, dx), (0, 1)) * m[..., None]
        ncnt += m
    zone = ~known & touching
    nmean = np.zeros_like(rgb)
    ok = ncnt > 0
    nmean[ok] = nsum[ok] / ncnt[ok][..., None]
    delta = np.abs(rgb - nmean).max(axis=2)
    offenders = int((zone & (delta > 24)).sum())
    if not apply:
        return offenders, offenders > 0

    # Iterative dilation: each pass fills unknown pixels from the mean of their known
    # neighbours, then those count as known. Bounded rather than run to completion,
    # because only pixels a resampling kernel can reach matter and flooding a whole
    # 1024 canvas costs hundreds of passes for no visible gain. A 24px collar covers
    # a downscale as aggressive as 1024 to 64.
    out = rgb.copy()
    filled = known.copy()
    for _ in range(passes):
        if filled.all():
            break
        acc = np.zeros_like(out)
        cnt = np.zeros(filled.shape, dtype=np.float64)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            shifted = np.roll(out, (dy, dx), (0, 1))
            mask = np.roll(filled, (dy, dx), (0, 1))
            acc += shifted * mask[..., None]
            cnt += mask
        new = (~filled) & (cnt > 0)
        if not new.any():
            break                      # fully isolated region; nothing to bleed from
        out[new] = (acc[new] / cnt[new][..., None])
        filled |= new

    res = np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)
    # The whole point: alpha untouched, and RGB untouched wherever alpha > 0.
    orig = np.array(im)
    assert (res[..., 3] == orig[..., 3]).all(), "alpha changed"
    vis = orig[..., 3] > 0
    assert (res[..., :3][vis] == orig[..., :3][vis]).all(), "visible pixels changed"
    Image.fromarray(res, "RGBA").save(path)
    return offenders, True


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    dirty = 0
    for p in args:
        n, changed = bleed(p, apply=not check)
        verb = "clean" if n == 0 else ("would fix" if check else "fixed")
        print(f"{verb:>10}  {n:>6} transparent px that disagree with the edge they touch  {p}")
        dirty += 1 if n else 0
    # exit 1 only when something is actually wrong, so this can gate a build
    sys.exit(1 if (check and dirty) else 0)
