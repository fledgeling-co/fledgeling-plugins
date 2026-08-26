#!/usr/bin/env python3
"""Pixel analysis of REF/A/B PNGs — no external metadata."""
import json
import os
import sys

try:
    from PIL import Image
    import numpy as np
except ImportError as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)

DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ["REF-1024.png", "A-1024.png", "B-1024.png", "A-small.png", "B-small.png"]


def load_rgba(path):
    im = Image.open(path).convert("RGBA")
    return im, np.array(im, dtype=np.float64)


def luminance(rgba):
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mean_rgba(arr):
    return {
        "R": float(np.mean(arr[..., 0])),
        "G": float(np.mean(arr[..., 1])),
        "B": float(np.mean(arr[..., 2])),
        "A": float(np.mean(arr[..., 3])),
    }


def mad_per_channel(a, b):
    d = np.abs(a - b)
    out = {
        "R": float(np.mean(d[..., 0])),
        "G": float(np.mean(d[..., 1])),
        "B": float(np.mean(d[..., 2])),
        "A": float(np.mean(d[..., 3])),
    }
    la, lb = luminance(a), luminance(b)
    out["luminance"] = float(np.mean(np.abs(la - lb)))
    return out


def crop_center(arr, cx=512, cy=512, size=256):
    half = size // 2
    return arr[cy - half : cy + half, cx - half : cx + half]


def is_cream_background(rgba):
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    lum = luminance(rgba)
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    return (lum > 200) & (chroma < 25) & (np.abs(r - g) < 15)


def is_orange_core(rgba):
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    return (r > 180) & (r - g > 20) & (r - b > 40)


def is_rod_like(rgba):
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    lum = luminance(rgba)
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    cream = is_cream_background(rgba)
    orange = is_orange_core(rgba)
    grayish = (chroma < 35) & (lum > 80) & (lum < 220)
    return grayish & ~cream & ~orange


def region_mad(a, b, mask):
    if not np.any(mask):
        return None
    idx = mask
    return mad_per_channel(a[idx], b[idx])


def bbox_from_mask(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return {
        "x0": int(xs.min()),
        "y0": int(ys.min()),
        "x1": int(xs.max()),
        "y1": int(ys.max()),
        "width": int(xs.max() - xs.min() + 1),
        "height": int(ys.max() - ys.min() + 1),
    }


def ssim_luminance(a, b):
    """Simple SSIM on luminance (global, single scale)."""
    la = luminance(a).astype(np.float64)
    lb = luminance(b).astype(np.float64)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mu_a, mu_b = la.mean(), lb.mean()
    var_a, var_b = la.var(), lb.var()
    cov = np.mean((la - mu_a) * (lb - mu_b))
    num = (2 * mu_a * mu_b + c1) * (2 * cov + c2)
    den = (mu_a**2 + mu_b**2 + c1) * (var_a + var_b + c2)
    return float(num / den) if den else 0.0


def pearson_luminance(a, b):
    la = luminance(a).ravel()
    lb = luminance(b).ravel()
    if la.std() == 0 or lb.std() == 0:
        return float("nan")
    return float(np.corrcoef(la, lb)[0, 1])


def to_json(obj):
    if isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_json(v) for v in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def sample_rgb(arr, x, y, name):
    h, w = arr.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        return {"point": name, "x": int(x), "y": int(y), "error": "out of bounds"}
    px = arr[y, x]
    return {
        "point": name,
        "x": int(x),
        "y": int(y),
        "R": float(px[0]),
        "G": float(px[1]),
        "B": float(px[2]),
        "A": float(px[3]),
        "lum": float(luminance(px.reshape(1, 1, 4))[0, 0]),
    }


def rod_interior_variance(arr):
    """Variance of luminance along rod-like pixels."""
    mask = is_rod_like(arr)
    if not np.any(mask):
        return None
    lum = luminance(arr)[mask]
    return float(np.var(lum))


def grid_showthrough(arr, radius=8):
    """Compare rod luminance to mean of nearby cream background."""
    h, w = arr.shape[:2]
    rod = is_rod_like(arr)
    cream = is_cream_background(arr)
    diffs = []
    ys, xs = np.where(rod)
    step = max(1, len(xs) // 500)
    for y, x in zip(ys[::step], xs[::step]):
        y0, y1 = max(0, y - radius), min(h, y + radius + 1)
        x0, x1 = max(0, x - radius), min(w, x + radius + 1)
        patch_cream = cream[y0:y1, x0:x1]
        if not np.any(patch_cream):
            continue
        bg_lum = luminance(arr[y0:y1, x0:x1])[patch_cream].mean()
        rod_lum = luminance(arr[y, x])
        diffs.append(rod_lum - bg_lum)
    if not diffs:
        return None
    return {
        "mean_rod_minus_bg_luminance": float(np.mean(diffs)),
        "std": float(np.std(diffs)),
        "samples": len(diffs),
    }


def find_overlap_point(ref, a, b):
    """Find rod-over-orange: orange under gray rod."""
    orange = is_orange_core(ref)
    rod = is_rod_like(ref)
    overlap = orange & rod
    if not np.any(overlap):
        # relax: orange near rod (dilate rod by checking neighbors)
        ys, xs = np.where(rod)
        h, w = ref.shape[:2]
        candidates = []
        for y, x in zip(ys[::50], xs[::50]):
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and is_orange_core(ref[ny:ny+1, nx:nx+1])[0, 0]:
                        candidates.append((nx, ny))
        if candidates:
            x, y = candidates[len(candidates) // 2]
            return x, y, "near_overlap"
        return None
    ys, xs = np.where(overlap)
    mid = len(xs) // 2
    return int(xs[mid]), int(ys[mid]), "direct_overlap"


def analyze_small_strip(path, label):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    arr = np.array(im, dtype=np.float64)
    # tiles at 0, 144, 288 for 128-wide tiles with 16px gap
    tile_positions = [0, 144, 288]
    tiles = []
    for i, x0 in enumerate(tile_positions):
        if x0 + 128 > w:
            continue
        tile = arr[:, x0 : x0 + 128]
        tiles.append({"index": i, "x0": x0, "width": tile.shape[1]})

    def metrics_on_region(region, scale_name):
        cream = is_cream_background(region)
        orange = is_orange_core(region)
        rod = is_rod_like(region)
        lum = luminance(region)
        out = {"scale": scale_name}
        if np.any(cream):
            out["cream_mean_lum"] = float(lum[cream].mean())
        if np.any(orange):
            out["orange_mean_lum"] = float(lum[orange].mean())
            out["orange_count"] = int(orange.sum())
        if np.any(rod):
            out["rod_mean_lum"] = float(lum[rod].mean())
            out["rod_count"] = int(rod.sum())
        if np.any(cream) and np.any(orange):
            out["orange_vs_cream_contrast"] = float(lum[orange].mean() - lum[cream].mean())
        if np.any(cream) and np.any(rod):
            out["rod_vs_cream_contrast"] = float(lum[rod].mean() - lum[cream].mean())
        return out

    # Full strip = 16x scale (tile 0 area magnified?) — user says 128px + NN magnified 32 and 16
    # Strip layout: 3 tiles of 128 with 16 gap => width 416
    # tile 0 = 16x?, tile 1 = 32x?, tile 2 = 128 native? Or positions indicate scales
    # User: "strips of 128px + nearest-neighbor magnified 32 and 16"
    # Likely: tile at 0 = 16x magnified (from 128/16=8? or 128 at 16x = 8px source?)
    # Actually: 128px tile magnified to show at 16x and 32x scales — three tiles compare scales
    result = {"file": label, "size": [w, h], "tiles": tiles}
    scale_names = ["128_native", "32x_magnified", "16x_magnified"]
    for i, x0 in enumerate(tile_positions):
        if x0 + 128 > w:
            continue
        tile = arr[:, x0 : x0 + 128]
        result[scale_names[i] if i < 3 else f"tile_{i}"] = metrics_on_region(
            tile, scale_names[i] if i < 3 else f"tile_{i}"
        )
    return result


def main():
    report = {}

    # 1. File metadata
    report["file_info"] = {}
    images = {}
    for fn in FILES:
        path = os.path.join(DIR, fn)
        im = Image.open(path)
        report["file_info"][fn] = {
            "bytes": os.path.getsize(path),
            "dimensions": list(im.size),
            "mode": im.mode,
        }
        if fn.endswith("-1024.png"):
            images[fn.split("-")[0]] = load_rgba(path)[1]

    ref, a, b = images["REF"], images["A"], images["B"]

    # 2. Mean RGBA 1024
    report["mean_rgba_1024"] = {
        "REF": mean_rgba(ref),
        "A": mean_rgba(a),
        "B": mean_rgba(b),
    }

    # 3. MAD vs REF
    report["mad_vs_ref"] = {}
    for name, img in [("A", a), ("B", b)]:
        entry = {"full_image": mad_per_channel(img, ref)}
        entry["center_crop_256"] = mad_per_channel(crop_center(img), crop_center(ref))
        rod_mask = is_rod_like(ref)
        bg_mask = is_cream_background(ref)
        entry["rod_region"] = region_mad(img, ref, rod_mask)
        entry["background_region"] = region_mad(img, ref, bg_mask)
        report["mad_vs_ref"][name] = entry

    # 4. A vs B difference mask
    diff = np.abs(a - b)
    diff_mask = np.any(diff[..., :3] > 8, axis=-1)
    frac = float(diff_mask.mean())
    bbox = bbox_from_mask(diff_mask)
    if np.any(diff_mask):
        mean_a_diff = mean_rgba(a[diff_mask])
        mean_b_diff = mean_rgba(b[diff_mask])
    else:
        mean_a_diff = mean_b_diff = None
    report["a_vs_b"] = {
        "threshold": 8,
        "fraction_differing_pixels": frac,
        "differing_pixel_count": int(diff_mask.sum()),
        "total_pixels": int(diff_mask.size),
        "bounding_box": bbox,
        "mean_color_in_diff_regions": {"A": mean_a_diff, "B": mean_b_diff},
        "pixel_identical_except_regions": frac < 0.01,
    }

    # 5. Key point samples
    points = [
        (512, 512, "center"),
        (400, 250, "rod_400_250"),
        (700, 350, "rod_700_350"),
        (300, 700, "rod_300_700"),
        (100, 100, "background_100_100"),
    ]
    overlap = find_overlap_point(ref, a, b)
    if overlap:
        ox, oy, otype = overlap
        points.append((ox, oy, f"rod_triangle_overlap_{otype}"))

    report["key_points"] = {}
    for x, y, pname in points:
        report["key_points"][pname] = {
            "REF": sample_rgb(ref, x, y, pname),
            "A": sample_rgb(a, x, y, pname),
            "B": sample_rgb(b, x, y, pname),
        }

    # 6. Per-image rod/orange/grid metrics
    report["image_metrics_1024"] = {}
    for name, img in [("REF", ref), ("A", a), ("B", b)]:
        lum = luminance(img)
        rod = is_rod_like(img)
        orange = is_orange_core(img)
        m = {}
        if np.any(rod):
            m["rod_mean_luminance"] = float(lum[rod].mean())
            m["rod_pixel_count"] = int(rod.sum())
        if np.any(orange):
            m["orange_core_mean_luminance"] = float(lum[orange].mean())
            m["orange_core_pixel_count"] = int(orange.sum())
        m["rod_interior_luminance_variance"] = rod_interior_variance(img)
        m["grid_showthrough"] = grid_showthrough(img)
        report["image_metrics_1024"][name] = m

    # 7. SSIM and correlation
    report["similarity_vs_ref"] = {}
    for name, img in [("A", a), ("B", b)]:
        report["similarity_vs_ref"][name] = {
            "ssim_luminance": ssim_luminance(img, ref),
            "pearson_luminance": pearson_luminance(img, ref),
        }

    # 8. Small strips
    report["small_strips"] = {
        "A-small": analyze_small_strip(os.path.join(DIR, "A-small.png"), "A-small"),
        "B-small": analyze_small_strip(os.path.join(DIR, "B-small.png"), "B-small"),
    }

    print(json.dumps(to_json(report), indent=2))


if __name__ == "__main__":
    main()
