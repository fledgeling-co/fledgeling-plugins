from PIL import Image
import numpy as np

base = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r08/panel/bundle/"
A = np.array(Image.open(base + "A-1024.png").convert("RGB"), dtype=float)
B = np.array(Image.open(base + "B-1024.png").convert("RGB"), dtype=float)
R = np.array(
    Image.open(base + "REF-1024.png")
    .convert("RGB")
    .resize((A.shape[1], A.shape[0]), Image.Resampling.LANCZOS),
    dtype=float,
)
print("shapes", A.shape, B.shape, R.shape)
print("AB", round(abs(A - B).mean(), 2))
print("AR", round(abs(A - R).mean(), 2))
print("BR", round(abs(B - R).mean(), 2))
h, w = A.shape[:2]
regs = {
    "slab": (int(h * 0.3), int(h * 0.7), int(w * 0.25), int(w * 0.75)),
    "loop": (int(h * 0.1), int(h * 0.45), int(w * 0.05), int(w * 0.4)),
    "glow": (int(h * 0.4), int(h * 0.65), int(w * 0.35), int(w * 0.8)),
    "bgUL": (0, int(h * 0.3), 0, int(w * 0.3)),
    "bgLR": (int(h * 0.7), h, int(w * 0.7), w),
}
for n, (y0, y1, x0, x1) in regs.items():
    ar = abs(A[y0:y1, x0:x1] - R[y0:y1, x0:x1]).mean()
    br = abs(B[y0:y1, x0:x1] - R[y0:y1, x0:x1]).mean()
    ab = abs(A[y0:y1, x0:x1] - B[y0:y1, x0:x1]).mean()
    print(f"{n}: AR={ar:.1f} BR={br:.1f} AB={ab:.1f} closer={'A' if ar < br else 'B'}")

# warmth of UL bg (higher R-B = warmer)
for label, arr in [("A", A), ("B", B), ("R", R)]:
    c = arr[0 : h // 3, 0 : w // 3].mean((0, 1))
    print(f"{label} UL mean RGB={c.round(1)} warmth(R-B)={c[0]-c[2]:.1f}")

# glow strength: orange pixel count
for label, arr in [("A", A), ("B", B), ("R", R)]:
    orange = (
        (arr[:, :, 0] > 180)
        & (arr[:, :, 1] > 50)
        & (arr[:, :, 1] < 200)
        & (arr[:, :, 2] < 120)
    )
    print(f"{label} orange_px={orange.sum()} mean_orange={arr[orange].mean(0).round(1) if orange.any() else None}")

As = np.array(Image.open(base + "A-small.png").convert("RGB"), dtype=float)
Bs = np.array(Image.open(base + "B-small.png").convert("RGB"), dtype=float)
print("small AB", round(abs(As - Bs).mean(), 2), As.shape)
# split small strip into thirds roughly
ws = As.shape[1] // 3
for i, name in enumerate(["128", "32mag", "16mag"]):
    a = As[:, i * ws : (i + 1) * ws]
    b = Bs[:, i * ws : (i + 1) * ws]
    ao = ((a[:, :, 0] > 160) & (a[:, :, 1] > 40) & (a[:, :, 2] < 120)).sum()
    bo = ((b[:, :, 0] > 160) & (b[:, :, 1] > 40) & (b[:, :, 2] < 120)).sum()
    print(f"small {name}: orange A={ao} B={bo} meanA={a.mean():.1f} meanB={b.mean():.1f}")

# max-diff patches between A and B
d = abs(A - B).sum(2)
flat = d.ravel()
idx = np.argpartition(flat, -5)[-5:]
print("top AB diffs:")
for i in idx:
    y, x = divmod(int(i), w)
    print(f"  ({y},{x}) d={d[y,x]:.0f} A={A[y,x].astype(int)} B={B[y,x].astype(int)}")
