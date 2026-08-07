"""Per-region edge accounting at 256 / 128 / 1024, regions from the build's own geometry."""
import sys, pathlib, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
import fidelity as F
import build_icon as B   # rewrites icon.svg identically

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
Wd = A / "loop-runs/r10/work"


def poly_mask(pts, size, grow=0):
    im = Image.new("L", (1024, 1024), 0)
    d = ImageDraw.Draw(im)
    d.polygon([tuple(p) for p in pts], fill=255)
    if grow:
        d.line([tuple(p) for p in pts] + [tuple(pts[0])], fill=255, width=grow * 2)
    return np.asarray(im.resize((size, size), Image.BILINEAR)) > 96


CURL_BOX = [(120, 120), (470, 120), (470, 470), (120, 470)]

for size in (1024, 256, 128):
    ca = F.render_candidate(A / "icon.svg", size)
    rb = F.normalise_reference(A / "icon-engineC-f5665d-2.png", size)
    g, h = F.to_gray(ca), F.to_gray(rb)
    ea, eb = F.sobel_edges(g), F.sobel_edges(h)
    keep = ~F.rim_mask(size)
    ea &= keep; eb &= keep
    spur = ea & ~F.dilate(eb)
    miss = eb & ~F.dilate(ea)

    blk = poly_mask(B.SILHOUETTE, size)
    blk_band = poly_mask(B.SILHOUETTE, size, grow=14) & ~poly_mask(
        [(x, y) for x, y in B.SILHOUETTE], size)
    curl = poly_mask(CURL_BOX, size) & ~blk
    ground = ~blk & ~poly_mask(CURL_BOX, size)
    print(f"=== {size}px  (cand {ea.sum()} edges, ref {eb.sum()})")
    for name, m in [("block interior", blk), ("curl box", curl), ("ground", ground)]:
        print(f"   {name:15s} px%={100*m.mean():5.1f}  candE={( ea&m).sum():6d} refE={(eb&m).sum():6d}"
              f"  spurious={(spur&m).sum():6d}  missed={(miss&m).sum():6d}")
