#!/usr/bin/env python3
"""fidelity.py — score a candidate icon against a raster reference, multi-scale.

The deterministic core of the create-mac-icon fidelity loop (see
references/fidelity-loop.md). Three subcommands:

  score      render candidate + reference at 1024/256/128/32/16, compute the
             metric stack per size, write score.json + residual/edge maps
  gate       Pareto-compare a candidate score.json against a baseline one:
             ACCEPT only if no size regresses beyond tolerance and small-size
             floors hold. Also detects negligible edits (oscillation guard).
  structure  static analysis of an SVG candidate BEFORE rendering: rejects
             <image> embeds (the base64 mimicry exploit), enforces the
             complexity envelope, checks named layer groups exist.

Design rules baked in (from the deep-research evidence, docs/svg-icon-fidelity-plan.md):
  - The harness owns the canvas: candidate viewBox is never trusted; both
    images are normalised to the same square renders (RLRF's viewBox hack).
  - No single metric: luminance field + SSIM carry large sizes, edge F1 +
    mask IoU carry 32/16 (deep-feature metrics are out of range there).
  - Degraded-but-honest tiers: LPIPS runs only if torch+lpips import; the
    JSON records which tier ran so a score is never silently weaker.
  - Complexity is a constraint checked in `structure`, never a reward.

Dependencies: numpy + Pillow (required), rsvg-convert on PATH for SVG
candidates, torch+lpips (optional, upgrades the material metric at 1024/256).
"""
import argparse
import hashlib
import json
import math
import pathlib
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

SIZES = (1024, 256, 128, 32, 16)
# Bump whenever a metric's definition changes. The gate refuses to compare
# scores computed under different versions: a candidate scored with a new
# metric against a baseline scored with the old one is not a comparison, and
# it silently produced a mixed verdict once before this existed.
METRIC_VERSION = 2  # 2: edge_f1 excludes the squircle rim
NEUTRAL = 128  # composite ground for alpha; both sides get the same one

# ---------------------------------------------------------------- rendering

def render_candidate(path: pathlib.Path, size: int) -> Image.Image:
    if path.suffix.lower() == ".svg":
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
            tmp = pathlib.Path(t.name)
        subprocess.run(
            ["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)],
            check=True,
        )
        im = Image.open(tmp).convert("RGBA")
        tmp.unlink(missing_ok=True)
        return im
    return Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)


def normalise_reference(path: pathlib.Path, size: int) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    if im.width != im.height:  # centre-crop to square; a reference should be square already
        s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2,
                      (im.width + s) // 2, (im.height + s) // 2))
    return im.resize((size, size), Image.LANCZOS)


def to_gray(im: Image.Image) -> np.ndarray:
    """Composite RGBA over the shared neutral ground, return float L in 0..1."""
    a = np.asarray(im, dtype=np.float64) / 255.0
    rgb, alpha = a[..., :3], a[..., 3:4]
    comp = rgb * alpha + (NEUTRAL / 255.0) * (1 - alpha)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2]

# ------------------------------------------------------------------ metrics

def box_mean(x: np.ndarray, w: int) -> np.ndarray:
    """Local mean via cumsum box filter, 'same' size (edge-padded)."""
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[: x.shape[0], : x.shape[1]]


def ssim(a: np.ndarray, b: np.ndarray) -> float:
    w = max(3, min(11, a.shape[0] // 4) | 1)  # odd window, scaled to image
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    mu_a, mu_b = box_mean(a, w), box_mean(b, w)
    va = box_mean(a * a, w) - mu_a**2
    vb = box_mean(b * b, w) - mu_b**2
    cov = box_mean(a * b, w) - mu_a * mu_b
    s = ((2 * mu_a * mu_b + c1) * (2 * cov + c2)) / ((mu_a**2 + mu_b**2 + c1) * (va + vb + c2))
    return float(np.clip(s, -1, 1).mean())


def sobel_edges(g: np.ndarray, thresh: float = 0.10) -> np.ndarray:
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > thresh * 4  # sobel max ~4 for 0..1 input


def dilate(m: np.ndarray, r: int = 1) -> np.ndarray:
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n: int, thresh: float = 0.86) -> np.ndarray:
    """The outer band of the squircle, in superellipse coordinates.

    A full-bleed SVG clipped to the mask renders a hard alpha boundary there;
    a raster reference usually does not. Measured on improve-skill at 32px: 75
    of the candidate's 341 edges sat on that rim against 2 of the reference's
    190. Comparing them measures the delivery format rather than the artwork,
    and it punishes the candidate for a boundary the design owns by definition.
    """
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def edge_f1(a: np.ndarray, b: np.ndarray) -> float:
    ea, eb = sobel_edges(a), sobel_edges(b)
    keep = ~rim_mask(a.shape[0])
    ea = ea & keep
    eb = eb & keep
    if not ea.any() and not eb.any():
        return 1.0
    tp_p = (ea & dilate(eb)).sum()   # candidate edges near a reference edge
    tp_r = (eb & dilate(ea)).sum()   # reference edges matched by candidate
    prec = tp_p / max(ea.sum(), 1)
    rec = tp_r / max(eb.sum(), 1)
    return float(2 * prec * rec / max(prec + rec, 1e-9))


def mask_iou(ca: Image.Image, cb: Image.Image):
    aa = np.asarray(ca)[..., 3] > 16
    ab = np.asarray(cb)[..., 3] > 16
    # Opaque full-bleed reference (GPT-Image output) makes coverage IoU vacuous
    if ab.mean() > 0.99 and aa.mean() > 0.99:
        return None
    return float((aa & ab).sum() / max((aa | ab).sum(), 1))


def try_lpips():
    try:
        import lpips  # noqa
        import torch  # noqa
        return lpips.LPIPS(net="alex", verbose=False)
    except Exception:
        return None


def lpips_dist(model, ga: Image.Image, gb: Image.Image) -> float:
    import torch
    def t(im):
        a = np.asarray(im.convert("RGB"), dtype=np.float64) / 127.5 - 1.0
        return torch.tensor(a).permute(2, 0, 1).unsqueeze(0).float()
    with torch.no_grad():
        return float(model(t(ga), t(gb)).item())

# ----------------------------------------------------------------- score

def composite_for(size: int, m: dict) -> float:
    """Per-size composite in 0..1 (higher better). Weights follow the plan:
    material terms carry large sizes, structure terms carry small ones."""
    lum = 1 - min(m["lum_delta"] * 4, 1.0)  # 0.25 mean-L delta -> floor
    if size >= 128:
        parts = [(0.40, m["ssim"]), (0.35, lum), (0.25, m["edge_f1"])]
        if m.get("lpips") is not None:
            parts = [(0.30, 1 - min(m["lpips"], 1.0)), (0.25, m["ssim"]), (0.25, lum), (0.20, m["edge_f1"])]
    else:
        parts = [(0.45, m["edge_f1"]), (0.35, m["ssim"]), (0.20, lum)]
        if m.get("mask_iou") is not None:
            parts = [(0.35, m["edge_f1"]), (0.25, m["mask_iou"]), (0.25, m["ssim"]), (0.15, lum)]
    return round(sum(w * v for w, v in parts), 4)


def cmd_score(args):
    cand, ref = pathlib.Path(args.candidate), pathlib.Path(args.reference)
    out = pathlib.Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    lp = try_lpips()
    tier = "full (lpips)" if lp else "numpy (no torch: luminance+ssim+edges only)"
    result = {"candidate": str(cand), "reference": str(ref), "tier": tier,
              "metric_version": METRIC_VERSION, "label": args.label, "sizes": {}}

    for size in SIZES:
        ci, ri = render_candidate(cand, size), normalise_reference(ref, size)
        gc, gr = to_gray(ci), to_gray(ri)
        m = {
            "lum_delta": round(float(np.abs(gc - gr).mean()), 4),
            "ssim": round(ssim(gc, gr), 4),
            "edge_f1": round(edge_f1(gc, gr), 4),
            "mask_iou": mask_iou(ci, ri),
            # Absolute and reference-free: how much figure-ground punch the
            # candidate has on its OWN. Every other metric here measures
            # similarity, and a reference with weak small-size contrast will
            # happily pull a candidate down toward it while the similarity
            # numbers rise. Two independent judges caught exactly that on
            # improve-skill loop r01 when the composite did not.
            "self_contrast": round(float(np.percentile(gc, 90) - np.percentile(gc, 10)), 4),
            "ref_self_contrast": round(float(np.percentile(gr, 90) - np.percentile(gr, 10)), 4),
        }
        if m["mask_iou"] is not None:
            m["mask_iou"] = round(m["mask_iou"], 4)
        if lp and size >= 256:
            m["lpips"] = round(lpips_dist(lp, ci, ri), 4)
        m["composite"] = composite_for(size, m)
        result["sizes"][str(size)] = m

        if size == 1024:  # artifacts the VLM critic reads alongside the renders
            resid = (np.abs(gc - gr) * 255).astype(np.uint8)
            Image.fromarray(resid).save(out / "residual-1024.png")
            for name, g in (("edges-candidate", gc), ("edges-reference", gr)):
                Image.fromarray((sobel_edges(g) * 255).astype(np.uint8)).save(out / f"{name}.png")
            ci.save(out / "candidate-1024.png")
            ri.save(out / "reference-1024.png")

    r64 = render_candidate(cand, 64)
    result["render_hash"] = hashlib.sha256(r64.tobytes()).hexdigest()[:16]
    (out / "score.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result["sizes"], indent=2))
    print(f"tier: {tier}\nwrote {out}/score.json + residual/edge maps")


def cmd_gate(args):
    cand = json.loads(pathlib.Path(args.candidate).read_text())
    base = json.loads(pathlib.Path(args.baseline).read_text())
    tol = args.tolerance
    verdict, reasons = "ACCEPT", []
    cv, bv = cand.get("metric_version", 1), base.get("metric_version", 1)
    if cv != bv:
        print(f"REFUSED: candidate scored under metric v{cv}, baseline under v{bv}. "
              f"Re-score the baseline before gating; a mixed comparison is not a verdict.")
        sys.exit(2)
    if cand.get("render_hash") == base.get("render_hash"):
        verdict = "REJECT"
        reasons.append("negligible edit: render hash unchanged (oscillation guard)")
    for size in map(str, SIZES):
        c, b = cand["sizes"][size]["composite"], base["sizes"][size]["composite"]
        if c < b - tol:
            verdict = "REJECT"
            reasons.append(f"{size}px composite regressed {b:.4f} -> {c:.4f}")
    for size in ("32", "16"):
        if cand["sizes"][size]["edge_f1"] < args.edge_floor:
            verdict = "REJECT"
            reasons.append(f"{size}px edge_f1 {cand['sizes'][size]['edge_f1']:.3f} below floor {args.edge_floor}")
        # Absolute legibility floor. The composite can rise at small sizes purely by
        # converging on a reference whose own contrast is weak, which reads to a human
        # as the icon going mushy. Judged evidence: improve-skill r01 scored 32/16 as
        # improved while two independent judges both said the block collapsed toward
        # mid-grey. Similarity is not legibility, so this is checked on the candidate
        # alone.
        c_sc = cand["sizes"][size].get("self_contrast")
        b_sc = base["sizes"][size].get("self_contrast")
        if c_sc is not None and b_sc is not None and c_sc < b_sc * (1 - args.contrast_drop):
            verdict = "REJECT"
            reasons.append(
                f"{size}px self_contrast {c_sc:.3f} fell more than {args.contrast_drop:.0%} "
                f"below baseline {b_sc:.3f} (legibility loss the similarity score does not see)")
    gain = sum(cand["sizes"][s]["composite"] - base["sizes"][s]["composite"] for s in map(str, SIZES))
    print(f"{verdict}  (net composite delta {gain:+.4f} across {len(SIZES)} sizes)")
    for r in reasons:
        print(f"  - {r}")
    sys.exit(0 if verdict == "ACCEPT" else 1)


def cmd_structure(args):
    p = pathlib.Path(args.candidate)
    text = p.read_text(errors="replace")
    issues = []
    if re.search(r"<\s*image[\s>]", text, re.I):
        issues.append("<image> element present: raster embedding is the metric-gaming exploit; forbidden")
    if re.search(r"<\s*script[\s>]", text, re.I):
        issues.append("<script> element present; forbidden")
    n = {
        "paths": len(re.findall(r"<\s*path[\s>]", text, re.I)),
        "gradients": len(re.findall(r"<\s*(linear|radial)Gradient", text, re.I)),
        "filters": len(re.findall(r"<\s*filter[\s>]", text, re.I)),
        "groups_named": len(re.findall(r"<\s*g[^>]*\bid\s*=", text, re.I)),
        "bytes": len(text.encode()),
    }
    if n["paths"] > args.max_paths:
        issues.append(f"{n['paths']} paths exceeds envelope {args.max_paths} (path-soup guard)")
    if n["bytes"] > args.max_bytes:
        issues.append(f"{n['bytes']} bytes exceeds envelope {args.max_bytes}")
    if n["groups_named"] < 2:
        issues.append("fewer than 2 named <g> layers: the layer plan (bg/mid/fg/highlight) is missing")
    print(json.dumps(n, indent=2))
    print("PASS" if not issues else "FAIL")
    for i in issues:
        print(f"  - {i}")
    sys.exit(0 if not issues else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score")
    s.add_argument("--candidate", required=True)
    s.add_argument("--reference", required=True)
    s.add_argument("--outdir", required=True)
    s.add_argument("--label", default="")
    s.set_defaults(fn=cmd_score)
    g = sub.add_parser("gate")
    g.add_argument("--candidate", required=True, help="candidate score.json")
    g.add_argument("--baseline", required=True, help="baseline score.json")
    g.add_argument("--tolerance", type=float, default=0.005)
    g.add_argument("--edge-floor", type=float, default=0.35)
    g.add_argument("--contrast-drop", type=float, default=0.06,
                   help="max fractional drop in the candidate's own 32/16px contrast vs baseline")
    g.set_defaults(fn=cmd_gate)
    st = sub.add_parser("structure")
    st.add_argument("--candidate", required=True)
    st.add_argument("--max-paths", type=int, default=400)
    st.add_argument("--max-bytes", type=int, default=200_000)
    st.set_defaults(fn=cmd_structure)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
