"""Second placement sweep: bearing scatter, per-piece stagger, ridge pitch, and the
coordinate precision that pays for the last of them.

Sweep 1 said wander is inert on the void (3.60 -> 3.68 at +-9 units) while bearing
scatter is not, and that scatter is not only an arrangement lever: a ridge aimed 38
degrees off its family's axis crosses more of the tile, so the same ridge count buys
more ridge LENGTH and therefore more marks. That is the only free density this fixture
has, r14 having priced more ridges at +87KB.
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
ANG = math.radians(33.0)
UXf, UYf = math.cos(ANG), -math.sin(ANG)


def patch(**kw):
    s = BASE
    for k, v in kw.items():
        s2 = re.sub(rf"^{k} = [-\d.]+", f"{k} = {v}", s, count=1, flags=re.M)
        assert s2 != s, k
        s = s2
    SRC.write_text(s)


def aniso(img, x0, y0, n=160):
    """m7's spectral anisotropy and mean wavelength, so the round can be compared with
    the numbers already in the notes (reference 4.68 at band-mid, r14 11.43)."""
    p = img[y0:y0+n, x0:x0+n].astype(float)
    ry, rx = np.mgrid[0:n, 0:n]
    M = np.stack([np.ones(n*n), rx.ravel(), ry.ravel(), (rx*rx).ravel(),
                  (ry*ry).ravel(), (rx*ry).ravel()], 1)
    c, *_ = np.linalg.lstsq(M, p.ravel(), rcond=None)
    p = p - (M @ c).reshape(n, n)
    w = np.hanning(n)[:, None] * np.hanning(n)[None, :]
    P = np.abs(np.fft.fftshift(np.fft.fft2(p * w))) ** 2
    fy, fx = np.mgrid[0:n, 0:n] - n//2
    r = np.hypot(fx, fy)
    keep = (r >= n/60.0) & (r <= n/2.2)
    th = (np.degrees(np.arctan2(fy, fx)) + 90) % 180
    bins = np.array([P[keep & (th >= i*5) & (th < (i+1)*5)].sum() for i in range(36)])
    bins = bins / bins.sum()
    lam = (P[keep] * (n / np.maximum(r[keep], 1e-9))).sum() / P[keep].sum()
    return bins.max() / bins.mean(), lam


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
            vy, vx = evec[:, 1]
            bins[min(11, int((math.degrees(math.atan2(vy, vx)) % 180) / 15))] += 1
    bins /= max(bins.sum(), 1e-9)
    ent = -(bins[bins > 0] * np.log(bins[bins > 0])).sum() / math.log(12)
    return void.mean(), np.quantile(void, .9), ent, 10000.0*cnt/(n*n), 100.0*mask.mean()


def row(label, img, extra=""):
    cells = []
    for nm, (x0, y0) in STN.items():
        v, v9, e, c, cov = arrange(img, x0, y0)
        cells.append(f"{v:5.2f}{v9:5.1f}{e:6.3f}{c:6.0f}{cov:6.1f}")
    hp = box(img, 3) - box(img, 13)
    an, lam = aniso(img, 150, 430)
    print(f"{label:24s} " + " ".join(cells) +
          f"  rms {hp[ROUGH].std():.4f}/{hp[TRUED].std():.4f} an{an:5.2f} L{lam:4.1f} {extra}")


if __name__ == "__main__":
    print(f"{'':24s} " + " ".join(f"{nm:^28s}" for nm in STN))
    print(f"{'setting':24s} " + " ".join(f"{'void':>5s}{'p90':>5s}{'ent':>6s}"
                                         f"{'n/10k':>6s}{'cov%':>6s}" for _ in STN))
    row("REFERENCE", h)
    for label, kw in [
            ("as-is (stagger stream)", {}),
            ("skew 38", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0}),
            ("skew 52", {"GRAIN_SKEW_A": 52.0, "GRAIN_SKEW_B": 54.0}),
            ("skew 38 stag 8", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0,
                                "GRAIN_STAGGER": 8.0}),
            ("skew 38 stag 16", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0,
                                 "GRAIN_STAGGER": 16.0}),
            ("skew 38 stag 16 p0", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0,
                                    "GRAIN_STAGGER": 16.0, "GRAIN_PREC": 0}),
            ("...p0 pitch 0.86", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0,
                                  "GRAIN_STAGGER": 16.0, "GRAIN_PREC": 0,
                                  "GRAIN_PITCH": 0.86}),
            ("...p0 pitch 0.74", {"GRAIN_SKEW_A": 38.0, "GRAIN_SKEW_B": 40.0,
                                  "GRAIN_STAGGER": 16.0, "GRAIN_PREC": 0,
                                  "GRAIN_PITCH": 0.74}),
    ]:
        patch(**kw)
        subprocess.run([sys.executable, "build_icon.py"], cwd=A, check=True,
                       stdout=subprocess.DEVNULL)
        n = len((A / "icon.svg").read_text())
        g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
        row(label, g, extra=f"{n}B")
        np.save(f"c-{label.split()[0]}{len(label)}.npy", g)
    SRC.write_text(BASE)
    subprocess.run([sys.executable, "build_icon.py"], cwd=A, check=True,
                   stdout=subprocess.DEVNULL)
