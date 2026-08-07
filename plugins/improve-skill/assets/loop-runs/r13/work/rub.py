"""Rubric checks the gate cannot see: figure-ground either side of the split, the
pair's mean-neutrality against r14, and the small-size read.

Figure-ground is the block's mass against the ground it sits on, taken as the ratio
of the two mean luminances - the value rubric #7 is on. The pair's neutrality is the
contract the whole dense-texture construction rests on, so a placement edit that adds
ridge length has to be shown not to have spent the planes' means.
"""
import pathlib, subprocess, sys, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
g = np.load("g1024.npy")
rough = np.load("rough.npy"); trued = np.load("trued.npy"); block = np.load("block.npy")
solid = block & (g < 0.42)
print(f"figure-ground   block {g[solid].mean():.4f}"
      f"   vs un-planed {g[rough].mean():.4f} = {g[rough].mean()/g[solid].mean():.2f}:1"
      f"   vs trued {g[trued].mean():.4f} = {g[trued].mean()/g[solid].mean():.2f}:1")
print(f"plane means     un-planed {g[rough].mean():.4f}  trued {g[trued].mean():.4f}"
      f"   split {g[trued].mean()-g[rough].mean():+.4f}")
print("r14 was         un-planed 0.6551  trued 0.8415   split +0.1864")

for s in (32, 16):
    a = F.to_gray(F.render_candidate(A / "icon.svg", s))
    print(f"{s}px  mean {a.mean():.4f}  p90-p10 {np.quantile(a,.9)-np.quantile(a,.1):.4f}"
          f"  min {a.min():.3f} max {a.max():.3f}")
