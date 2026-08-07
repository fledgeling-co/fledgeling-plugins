"""Sweep GRAIN_WID. Shortening the mark spends coverage; the reference's mark is also
wider than ours at every station, so width is where that is bought back. Too much and
the absolute gap floor (1.9 stroke widths) eats the period and the count falls again.
"""
import re, subprocess, sys, pathlib, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
sys.path.insert(0, str(pathlib.Path.cwd()))
import fidelity as F
import w3helpers as H

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
SRC = A / "build_icon.py"
orig = SRC.read_text()
h = np.load("h1024.npy")
rough = np.load("rough.npy"); trued = np.load("trued.npy")


def band(img, lo, hi, m):
    return (H.box(img, lo) - H.box(img, hi))[m].std()


try:
    for wd in [float(a) for a in sys.argv[1:]] or [1.0, 1.20, 1.35]:
        SRC.write_text(re.sub(r"^GRAIN_WID = [-0-9.]+", f"GRAIN_WID = {wd}", orig, flags=re.M))
        subprocess.run([sys.executable, str(SRC)], cwd=A, capture_output=True, check=True)
        g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
        print(f"--- GRAIN_WID = {wd}   svg {(A / 'icon.svg').stat().st_size} bytes"
              f"   relief rms 3-13px: un-planed {band(g,3,13,rough):.4f} "
              f"(ref {band(h,3,13,rough):.4f})  trued {band(g,3,13,trued):.4f} "
              f"(ref {band(h,3,13,trued):.4f})")
        H.report(h, g)
finally:
    SRC.write_text(orig)
