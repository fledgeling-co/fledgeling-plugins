"""Sweep GRAIN_GAP_MIN. A break has to survive both the renderer's antialiasing and,
at 1024, the 3px box the relief instrument itself smooths with; the first cut used
1.15 stroke widths and the marks fused harder than r13's did. Rebuild, render, and
report the three numbers the round is aimed at: marks/10k, median length, coverage.
"""
import math, os, re, subprocess, sys, pathlib, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
SRC = A / "build_icon.py"
orig = SRC.read_text()
h = np.load("h1024.npy")
sys.path.insert(0, str(pathlib.Path.cwd()))
import w3helpers as H


def build(**consts):
    txt = orig
    for k, v in consts.items():
        txt = re.sub(rf"^{k} = [-0-9.]+", f"{k} = {v}", txt, flags=re.M)
    SRC.write_text(txt)
    subprocess.run([sys.executable, str(SRC)], cwd=A, capture_output=True, check=True)
    return F.to_gray(F.render_candidate(A / "icon.svg", 1024)), (A / "icon.svg").stat().st_size


try:
    for gap in [float(a) for a in sys.argv[1:]] or [1.15, 1.8, 2.1, 2.5]:
        g, nb = build(GRAIN_GAP_MIN=gap)
        print(f"--- GRAIN_GAP_MIN = {gap}   svg {nb} bytes")
        H.report(h, g)
finally:
    SRC.write_text(orig)
