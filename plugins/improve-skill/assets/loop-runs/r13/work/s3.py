"""Pitch, re-swept on the final stream. Removing the (measured-inert) stagger draw
re-phases the LCG, which moves the emitted byte count by 8% on its own, so the pitch
that fits the envelope has to be chosen after the generator is in its final shape
rather than carried over from s2.
"""
import pathlib, re, subprocess, sys, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fidelity as F
from s2 import patch, row, A, SRC, BASE

if __name__ == "__main__":
    print(f"{'':24s} " + " ".join(f"{nm:^28s}" for nm in ("left", "above", "trued")))
    print(f"{'setting':24s} " + " ".join(f"{'void':>5s}{'p90':>5s}{'ent':>6s}"
                                         f"{'n/10k':>6s}{'cov%':>6s}" for _ in range(3)))
    row("REFERENCE", np.load("h1024.npy"))
    for pitch in (1.00, 0.94, 0.90, 0.87):
        patch(GRAIN_PITCH=pitch)
        subprocess.run([sys.executable, "build_icon.py"], cwd=A, check=True,
                       stdout=subprocess.DEVNULL)
        n = len((A / "icon.svg").read_text())
        g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
        row(f"pitch {pitch:.2f}", g, extra=f"{n}B")
    SRC.write_text(BASE)
