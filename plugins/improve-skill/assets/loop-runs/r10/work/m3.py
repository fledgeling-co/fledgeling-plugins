"""Where are the candidate's SPURIOUS edges at 256 and 128?

Spurious = candidate edge with no reference edge within 1px.  Rendered as a red
overlay on the candidate, upscaled to 1024 so it can be eyeballed.
Also: missed reference edges in blue.
"""
import sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r10/work"
ref_png = A / "icon-engineC-f5665d-2.png"

for size in (256, 128, 1024):
    ca = F.render_candidate(A / "icon.svg", size)
    rb = F.normalise_reference(ref_png, size)
    g, h = F.to_gray(ca), F.to_gray(rb)
    ea, eb = F.sobel_edges(g), F.sobel_edges(h)
    keep = ~F.rim_mask(size)
    ea &= keep; eb &= keep
    spur = ea & ~F.dilate(eb)
    miss = eb & ~F.dilate(ea)
    base = np.stack([g, g, g], -1)
    base[spur] = [1.0, 0.1, 0.1]
    base[miss] = [0.1, 0.4, 1.0]
    im = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8))
    im = im.resize((1024, 1024), Image.NEAREST)
    im.save(W / f"edgemap-{size}.png")
    print(size, "spurious", spur.sum(), "of", ea.sum(), " missed", miss.sum(), "of", eb.sum())

    # coarse 8x8 grid of spurious density
    if size in (256, 128):
        k = size // 8
        grid = spur.reshape(8, k, 8, k).sum(axis=(1, 3))
        print("   spurious per 1/8 cell (rows top->bottom):")
        for row in grid:
            print("   ", " ".join(f"{v:4d}" for v in row))
