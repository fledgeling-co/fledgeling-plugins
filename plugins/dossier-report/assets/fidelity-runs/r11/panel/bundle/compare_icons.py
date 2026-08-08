#!/usr/bin/env python3
"""Compare REF vs A vs B icon images."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent


def load_rgba(name: str) -> np.ndarray:
    path = BASE / name
    img = Image.open(path).convert("RGBA")
    return np.array(img, dtype=np.float64)


def composite_on_white(rgba: np.ndarray) -> np.ndarray:
    alpha = rgba[:, :, 3:4] / 255.0
    rgb = rgba[:, :, :3]
    return rgb * alpha + 255.0 * (1.0 - alpha)


def align_sizes(ref: np.ndarray, other: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if ref.shape == other.shape:
        return ref, other
    h = min(ref.shape[0], other.shape[0])
    w = min(ref.shape[1], other.shape[1])
    return ref[:h, :w], other[:h, :w]


def metrics(ref: np.ndarray, other: np.ndarray) -> dict:
    ref, other = align_sizes(ref, other)
    diff = other - ref
    mae = float(np.mean(np.abs(diff)))
    rmse = float(np.sqrt(np.mean(diff**2)))
    return {"mae": mae, "rmse": rmse, "shape": list(ref.shape)}


def region_masks(rgba: np.ndarray) -> dict[str, np.ndarray]:
    """Heuristic region segmentation from REF colors."""
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]

    opaque = alpha > 128
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    # Orange fold: high R, moderate G, low B
    orange = opaque & (r > 140) & (g > 60) & (g < 200) & (b < 120) & (r > g)

    # White body: bright neutral, not orange
    white = opaque & ~orange & (r > 200) & (g > 200) & (b > 200)

    # Spine/edge: mid-tones at boundaries / thickness cues
    gray = opaque & ~orange & ~white & (np.abs(r - g) < 25) & (np.abs(g - b) < 25)

    return {"orange_fold": orange, "white_body": white, "spine_edge": gray, "opaque": opaque}


def region_metrics(ref: np.ndarray, other: np.ndarray, mask: np.ndarray) -> dict | None:
    if mask.sum() < 100:
        return None
    ref, other = align_sizes(ref, other)
    mask = mask[: ref.shape[0], : ref.shape[1]]
    ref_px = ref[mask]
    other_px = other[mask]
    diff = other_px - ref_px
    return {
        "pixels": int(mask.sum()),
        "mae": float(np.mean(np.abs(diff))),
        "rmse": float(np.sqrt(np.mean(diff**2))),
        "mean_ref_rgb": [float(x) for x in ref_px.mean(axis=0)],
        "mean_other_rgb": [float(x) for x in other_px.mean(axis=0)],
    }


def compare_pair(ref_name: str, other_name: str, masks: dict) -> dict:
    ref_rgba = load_rgba(ref_name)
    other_rgba = load_rgba(other_name)
    ref = composite_on_white(ref_rgba)
    other = composite_on_white(other_rgba)

    out = {
        "pair": f"{other_name} vs {ref_name}",
        "global": metrics(ref, other),
        "regions": {},
    }
    for region, mask in masks.items():
        if region == "opaque":
            continue
        rm = region_metrics(ref, other, mask)
        if rm:
            out["regions"][region] = rm
    return out


def small_strip_analysis() -> dict:
    a = load_rgba("A-small.png")
    b = load_rgba("B-small.png")
    a_rgb = composite_on_white(a)
    b_rgb = composite_on_white(b)

    h = min(a_rgb.shape[0], b_rgb.shape[0])
    w = min(a_rgb.shape[1], b_rgb.shape[1])
    a_rgb = a_rgb[:h, :w]
    b_rgb = b_rgb[:h, :w]

    diff = b_rgb - a_rgb
    absdiff = np.abs(diff)

    return {
        "A_small_shape": list(a.shape),
        "B_small_shape": list(b.shape),
        "aligned_shape": [h, w, 3],
        "A_vs_B_mae": float(np.mean(absdiff)),
        "A_vs_B_rmse": float(np.sqrt(np.mean(diff**2))),
        "max_channel_delta": {
            "R": float(absdiff[:, :, 0].max()),
            "G": float(absdiff[:, :, 1].max()),
            "B": float(absdiff[:, :, 2].max()),
        },
        "mean_delta_rgb": [float(x) for x in diff.mean(axis=(0, 1))],
        "pixels_over_10": int((absdiff > 10).sum()),
        "pixels_over_25": int((absdiff > 25).sum()),
    }


def main() -> None:
    ref_rgba = load_rgba("REF-1024.png")
    masks = region_masks(ref_rgba)

    result = {
        "sizes": {
            "REF": list(ref_rgba.shape),
            "A": list(load_rgba("A-1024.png").shape),
            "B": list(load_rgba("B-1024.png").shape),
        },
        "A_vs_REF": compare_pair("REF-1024.png", "A-1024.png", masks),
        "B_vs_REF": compare_pair("REF-1024.png", "B-1024.png", masks),
        "small_strip": small_strip_analysis(),
        "mask_pixel_counts": {k: int(v.sum()) for k, v in masks.items()},
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
