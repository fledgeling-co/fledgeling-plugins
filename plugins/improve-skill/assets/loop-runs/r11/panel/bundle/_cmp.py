from PIL import Image
import numpy as np
from pathlib import Path

base = Path(__file__).resolve().parent
A = np.array(Image.open(base / "A-1024.png").convert("RGB"), dtype=np.float32)
B = np.array(Image.open(base / "B-1024.png").convert("RGB"), dtype=np.float32)
R = np.array(
    Image.open(base / "REF-1024.png").convert("RGB").resize((1024, 1024)),
    dtype=np.float32,
)
print("A-B", float(np.abs(A - B).mean()))
print("A-R", float(np.abs(A - R).mean()))
print("B-R", float(np.abs(B - R).mean()))

# top-left ground texture region (avoid subject)
tlA = A[40:280, 40:320]
tlB = B[40:280, 40:320]
tlR = R[40:280, 40:320]
print("tl std A,B,R", float(tlA.std()), float(tlB.std()), float(tlR.std()))


def grad(x):
    g = x.mean(2)
    return float(np.abs(np.diff(g, axis=1)).mean() + np.abs(np.diff(g, axis=0)).mean())


print("tl grad A,B,R", grad(tlA), grad(tlB), grad(tlR))

# high-frequency energy via local deviation from blurred
def hf(x):
    # box blur approx
    k = 5
    pad = np.pad(x, ((k, k), (k, k), (0, 0)), mode="edge")
    acc = np.zeros_like(x)
    n = 0
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            acc += pad[k + dy : k + dy + x.shape[0], k + dx : k + dx + x.shape[1]]
            n += 1
    blur = acc / n
    return float(np.abs(x - blur).mean())


print("tl hf A,B,R", hf(tlA), hf(tlB), hf(tlR))

# subject body region mid
bodyA = A[380:620, 320:700]
bodyB = B[380:620, 320:700]
bodyR = R[380:620, 320:700]
print("body std A,B,R", float(bodyA.std()), float(bodyB.std()), float(bodyR.std()))
print("body mean A", bodyA.mean(axis=(0, 1)))
print("body mean B", bodyB.mean(axis=(0, 1)))
print("body mean R", bodyR.mean(axis=(0, 1)))

# where A/B differ
d = np.abs(A.astype(np.float32) - B).mean(2)
print("diff p50,p90,p99", float(np.percentile(d, 50)), float(np.percentile(d, 90)), float(np.percentile(d, 99)))
ys, xs = np.where(d > np.percentile(d, 99))
print("top-diff y mean,x mean", float(ys.mean()), float(xs.mean()), "n", len(ys))

As = np.array(Image.open(base / "A-small.png").convert("RGB"), dtype=np.float32)
Bs = np.array(Image.open(base / "B-small.png").convert("RGB"), dtype=np.float32)
print("small A-B", float(np.abs(As - Bs).mean()), As.shape)
w = As.shape[1] // 3
print("strip mae 128/32/16", float(np.abs(As[:, :w] - Bs[:, :w]).mean()), float(np.abs(As[:, w : 2 * w] - Bs[:, w : 2 * w]).mean()), float(np.abs(As[:, 2 * w :] - Bs[:, 2 * w :]).mean()))
