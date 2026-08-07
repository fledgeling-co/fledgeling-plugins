"""What the SCORER sees at 1024/256/128: per-region SSIM and edge accounting.

Uses fidelity.py's own to_gray / ssim / sobel_edges so the numbers are the ones
the gate will use.
"""
import sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
cand_svg = A / "icon.svg"
ref_png = A / "icon-engineC-f5665d-2.png"

for size in (1024, 256, 128):
    ca = F.render_candidate(cand_svg, size)
    rb = F.normalise_reference(ref_png, size)
    g, h = F.to_gray(ca), F.to_gray(rb)
    ea, eb = F.sobel_edges(g), F.sobel_edges(h)
    keep = ~F.rim_mask(size)
    ea &= keep; eb &= keep
    tp_p = (ea & F.dilate(eb)).sum(); tp_r = (eb & F.dilate(ea)).sum()
    prec = tp_p / max(ea.sum(), 1); rec = tp_r / max(eb.sum(), 1)
    print(f"--- {size}px   cand edges {ea.sum():7d}  ref edges {eb.sum():7d}   "
          f"prec {prec:.3f}  rec {rec:.3f}  f1 {2*prec*rec/max(prec+rec,1e-9):.4f}")

    # SSIM map
    w = max(3, min(11, size // 4) | 1)
    c1, c2 = 0.01**2, 0.03**2
    mu_a, mu_b = F.box_mean(g, w), F.box_mean(h, w)
    va = F.box_mean(g*g, w) - mu_a**2
    vb = F.box_mean(h*h, w) - mu_b**2
    cov = F.box_mean(g*h, w) - mu_a*mu_b
    lterm = (2*mu_a*mu_b + c1) / (mu_a**2 + mu_b**2 + c1)
    cterm = (2*cov + c2) / (va + vb + c2)
    smap = np.clip(lterm*cterm, -1, 1)
    print(f"      ssim {smap.mean():.4f}   L-term {lterm.mean():.4f}  CS-term {cterm.mean():.4f}"
          f"   sd(cand) {np.sqrt(np.maximum(va,0)).mean():.4f} sd(ref) {np.sqrt(np.maximum(vb,0)).mean():.4f}")

    if size == 1024:
        np.save(A/"loop-runs/r10/work/g1024.npy", g)
        np.save(A/"loop-runs/r10/work/h1024.npy", h)
        np.save(A/"loop-runs/r10/work/ssim1024.npy", smap)
        np.save(A/"loop-runs/r10/work/cterm1024.npy", cterm)
        np.save(A/"loop-runs/r10/work/ea1024.npy", ea)
        np.save(A/"loop-runs/r10/work/eb1024.npy", eb)
