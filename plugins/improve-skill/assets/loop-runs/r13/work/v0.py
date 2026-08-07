"""Where the residual actually lives, and viewing crops for the eye.

Prints |candidate - reference| pooled over a 8x8 grid of 128px cells and over the
named regions, so the round starts from the artefact rather than from the last
round's mandate. Then writes 2x-zoom crops of the worst cells, side by side.
"""
import sys, pathlib, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")

W = 1024
g = np.load("g1024.npy"); h = np.load("h1024.npy")
rough = np.load("rough.npy"); trued = np.load("trued.npy"); block = np.load("block.npy")
d = np.abs(g - h)

print("residual |ours - ref|, 128px cells (mean x100)")
print("      " + "".join(f"{x:6d}" for x in range(0, W, 128)))
for y0 in range(0, W, 128):
    row = "".join(f"{100*d[y0:y0+128, x0:x0+128].mean():6.1f}" for x0 in range(0, W, 128))
    print(f"{y0:5d} {row}")

print()
for name, m in (("un-planed", rough), ("trued", trued), ("block+curl", block)):
    print(f"{name:12s} mean {d[m].mean():.4f}  p90 {np.quantile(d[m], .9):.4f}  "
          f"ours {g[m].mean():.4f} ref {h[m].mean():.4f}")

# contrast budget check: p90-p10 spread of the whole tile at the two small sizes is
# what the floor is on, but the tile-level spread is a fair proxy for an edit's sign.
for nm, im in (("ours", g), ("ref ", h)):
    print(f"{nm} whole-tile p90-p10 {np.quantile(im, .9) - np.quantile(im, .1):.4f}")


def png(path, arr):
    import zlib, struct
    a = np.clip(arr * 255, 0, 255).astype(np.uint8)
    if a.ndim == 2:
        a = np.stack([a] * 3, -1)
    raw = b"".join(b"\x00" + a[i].tobytes() for i in range(a.shape[0]))
    def chunk(t, b):
        c = t + b
        return struct.pack(">I", len(b)) + c + struct.pack(">I", zlib.crc32(c))
    hdr = struct.pack(">IIBBBBB", a.shape[1], a.shape[0], 8, 2, 0, 0, 0)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", hdr) +
                           chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def crop2x(name, x0, y0, n=180):
    pair = []
    for im in (h, g):
        p = im[y0:y0+n, x0:x0+n]
        pair.append(np.repeat(np.repeat(p, 2, 0), 2, 1))
    out = np.ones((2*n, 4*n + 8))
    out[:, :2*n] = pair[0]; out[:, 2*n+8:] = pair[1]
    png(f"v-{name}.png", out)


if __name__ == "__main__":
    for nm, (x0, y0) in {"band-left": (30, 540), "band-mid": (150, 420),
                         "band-low": (120, 700), "trued": (660, 620),
                         "above": (280, 90)}.items():
        crop2x(nm, x0, y0)
    png("v-residual.png", np.clip(d * 3.0, 0, 1))
    print("wrote crops (left = reference, right = ours)")
