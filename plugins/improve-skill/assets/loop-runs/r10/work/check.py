"""Pre-declared acceptance criteria for the r10 edit, checked before the gate is run.

  1. rough-plane band sd(3-12px) at 1024 within +-20% of the reference's ~0.016,
     and flat in radius from the key rather than falling away from it;
  2. the 128px SSIM-window sd must NOT rise (master 0.0540 vs reference 0.0379 -
     if it climbs, the amplitude is landing in the wrong band);
  3. rough-plane mean shift < 0.002 (the mean-balance that r02 lacked);
  4. trued-plane anisotropy moving off 13.1 toward the reference's 1.45.
"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r10/work"
N = 1024
g = F.to_gray(F.render_candidate(A / "icon.svg", N))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", N))
b = F.to_gray(F.render_candidate(W / "prev-icon.svg", N)) if (W / "prev-icon.svg").exists() else None


def gblur(a, s, n=N):
    k = np.fft.fftfreq(n)[:, None]**2 + np.fft.fftfreq(n)[None, :]**2
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2*np.pi**2*s**2*k)))


def erode(m, r):
    im = Image.fromarray((m*255).astype(np.uint8))
    while r > 0:
        s = min(9, 2*r+1); im = im.filter(ImageFilter.MinFilter(s)); r -= s//2
    return np.asarray(im) > 127


ys, xs = np.mgrid[0:N, 0:N]
u = (xs-511.5)/511.5; v = (ys-511.5)/511.5
inside = (np.abs(u)**5 + np.abs(v)**5)**0.2 < 0.80
bl = 957.0 + (292.0-957.0)*xs/N
clear = erode(~((g < 0.44) | (h < 0.44)), 46)
ROUGH = (ys < bl-70) & clear & inside
TRUED = (ys > bl+70) & clear & inside
rad = np.hypot(xs-75, ys-25)

print("1/  rough plane, band sd 3-12px, by radius from the key")
bpm, bpr = gblur(g, 0.8)-gblur(g, 4.0), gblur(h, 0.8)-gblur(h, 4.0)
bpb = gblur(b, 0.8)-gblur(b, 4.0) if b is not None else None
print("    r from key      px     prev      now      ref     now/ref")
for lo in range(0, 1200, 160):
    m = ROUGH & (rad >= lo) & (rad < lo+160)
    if m.sum() < 900:
        continue
    p = f"{bpb[m].std():.4f}" if bpb is not None else "  -   "
    print(f"     {lo:4d}-{lo+160:4d}  {m.sum():6d}   {p}   {bpm[m].std():.4f}   "
          f"{bpr[m].std():.4f}    {bpm[m].std()/bpr[m].std():5.2f}x")
print(f"    whole plane: now {bpm[ROUGH].std():.4f}   ref {bpr[ROUGH].std():.4f}")

print("\n2/  128px SSIM-window sd over the ground")
for lbl, img in (("now", g), ("ref", h)):
    s = np.asarray(Image.fromarray((img*255).astype(np.uint8)).resize((128, 128), Image.LANCZOS))/255.0
    m8 = np.asarray(Image.fromarray(((ROUGH | TRUED)*255).astype(np.uint8)).resize((128, 128), Image.BOX)) > 200
    mu = gblur(s, 1.4, 128)
    sd = np.sqrt(np.maximum(gblur(s*s, 1.4, 128) - mu*mu, 0))
    print(f"    {lbl}  window sd {sd[m8].mean():.4f}")

print("\n3/  plane means (mean-balance of the lit/shadowed pair)")
for rn, m in (("rough", ROUGH), ("trued", TRUED)):
    p = f"prev {b[m].mean():.4f}  " if b is not None else ""
    d = f"  shift {g[m].mean()-b[m].mean():+.4f}" if b is not None else ""
    print(f"    {rn}: {p}now {g[m].mean():.4f}  ref {h[m].mean():.4f}{d}")

print("\n4/  anisotropy, 3-40px band, clean patches")
PATCH = {"rough-far": (25, 690, 153, 818), "trued": (700, 820, 828, 948)}
n = 128
def spec(img, box):
    x0, y0, x1, y1 = box
    p = img[y0:y1, x0:x1].astype(float)
    yy, xx = np.mgrid[0:n, 0:n]
    M = np.stack([np.ones(n*n), xx.ravel(), yy.ravel(), (xx*xx).ravel(),
                  (yy*yy).ravel(), (xx*yy).ravel()], 1)
    c, *_ = np.linalg.lstsq(M, p.ravel(), rcond=None)
    p = p - (M @ c).reshape(n, n)
    sd = p.std()
    w = np.hanning(n)[:, None]*np.hanning(n)[None, :]
    P = np.abs(np.fft.fftshift(np.fft.fft2(p*w)))**2
    fy, fx = np.mgrid[0:n, 0:n]-n//2
    r = np.hypot(fx, fy)
    keep = (r >= n/40) & (r <= n/3)
    th = (np.degrees(np.arctan2(fy, fx))+90) % 180
    bins = np.array([P[keep & (th >= i*10) & (th < (i+1)*10)].sum() for i in range(18)])
    bins /= bins.sum()
    return sd, bins.max()/bins.mean()
for name, box in PATCH.items():
    row = []
    for lbl, img in (("prev", b), ("now", g), ("ref", h)):
        if img is None:
            continue
        sd, an = spec(img, box)
        row.append(f"{lbl} sd {sd:.4f} aniso {an:.2f}")
    print(f"    {name:10s} " + "   ".join(row))
