"""Sweep the three placement constants against the two arrangement statistics.

Each row rebuilds the generator with one setting, renders at 1024, and prints the
numbers r14 could not see (void, bearing entropy) beside the ones it could (count,
coverage, relief rms) and the envelope. The reference's own row is printed first.
Amplitude must not move: un-planed 3-13px relief rms is the control.
"""
import math, pathlib, re, subprocess, sys, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fidelity as F
from w3helpers import box, components
from w4 import dist_to_mark

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
SRC = A / "build_icon.py"
BASE = SRC.read_text()
ROUGH = np.load("rough.npy"); TRUED = np.load("trued.npy")
h = np.load("h1024.npy")
STN = {"left": (20, 520), "above": (230, 120), "trued": (700, 640)}


def patch(**kw):
    s = BASE
    for k, v in kw.items():
        s2 = re.sub(rf"^{k} = [-\d.]+", f"{k} = {v}", s, count=1, flags=re.M)
        assert s2 != s, k
        s = s2
    SRC.write_text(s)


def arrange(img, x0, y0, n=200):
    p = img[y0:y0+n, x0:x0+n]
    hp = box(p, 3) - box(p, 13)
    thr = 1.1 * hp.std()
    mask = np.abs(hp) > thr
    void = dist_to_mark(mask)[~mask]
    bins = np.zeros(12); cnt = 0
    for sign in (1, -1):
        for comp in components(sign * hp > thr):
            if len(comp) < 3:
                continue
            cnt += 1
            a = np.array(comp, float); a -= a.mean(0)
            ev, evec = np.linalg.eigh(a.T @ a / len(a))
            if ev[1] < 1e-9:
                continue
            vy, vx = evec[:, 1]
            bins[min(11, int((math.degrees(math.atan2(vy, vx)) % 180) / 15))] += \
                math.sqrt(ev[1]) * len(comp)
    bins /= max(bins.sum(), 1e-9)
    ent = -(bins[bins > 0] * np.log(bins[bins > 0])).sum() / math.log(12)
    return (void.mean(), np.quantile(void, .9), ent,
            10000.0 * cnt / (n * n), 100.0 * mask.mean())


def row(label, img, extra=""):
    cells = []
    for nm, (x0, y0) in STN.items():
        v, v9, e, c, cov = arrange(img, x0, y0)
        cells.append(f"{v:5.2f}{v9:5.1f}{e:6.3f}{c:6.0f}{cov:6.1f}")
    hp = box(img, 3) - box(img, 13)
    print(f"{label:26s} " + " ".join(cells) +
          f"  rms {hp[ROUGH].std():.4f}/{hp[TRUED].std():.4f} {extra}")


hdr = " ".join(f"{nm:^28s}" for nm in STN)
print(f"{'':26s} {hdr}")
print(f"{'setting':26s} " + " ".join(f"{'void':>5s}{'p90':>5s}{'ent':>6s}"
                                     f"{'n/10k':>6s}{'cov%':>6s}" for _ in STN))
row("REFERENCE", h)

for label, kw in [
        ("r14 baseline", {}),
        ("wander 10", {"GRAIN_WANDER": 10.0}),
        ("wander 18", {"GRAIN_WANDER": 18.0}),
        ("wander 26", {"GRAIN_WANDER": 26.0}),
        ("wander 18 node 38", {"GRAIN_WANDER": 18.0, "GRAIN_NODE": 38.0}),
        ("skew 24", {"GRAIN_SKEW_A": 24.0, "GRAIN_SKEW_B": 26.0}),
        ("skew 38", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0}),
        ("wander 18 skew 38", {"GRAIN_WANDER": 18.0, "GRAIN_SKEW_A": 38.0,
                               "GRAIN_SKEW_B": 40.0}),
]:
    patch(**kw)
    subprocess.run([sys.executable, "build_icon.py"], cwd=A, check=True,
                   stdout=subprocess.DEVNULL)
    n = len((A / "icon.svg").read_text())
    g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
    row(label, g, extra=f"{n}B")
    np.save(f"cand-{label.replace(' ', '_')}.npy", g)

SRC.write_text(BASE)
subprocess.run([sys.executable, "build_icon.py"], cwd=A, check=True,
               stdout=subprocess.DEVNULL)
