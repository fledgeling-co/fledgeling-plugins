"""Deterministic metrics for one video folder, from the measure/*.json files.

    python3 -I analyze.py <video-dir>   > measure/metrics.json
"""
import json
import re
import statistics as st
import sys
from pathlib import Path

d = Path(sys.argv[1])
m = d / "measure"


def load(name):
    p = m / name
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


cuts = load("cuts.json") or {}
events = load("events.json") or {}
audio = (load("audio.json") or {}).get("items", [{}])[0]
look = load("look.json") or {}
scan = (load("frames-scan.json") or {}).get("frames", [])
info = {}
try:
    info = json.loads((d / "video.info.json").read_text())
except Exception:
    pass

dur = float(cuts.get("end") or audio.get("duration") or info.get("duration") or 0)
cut_t = [c["t"] for c in cuts.get("cuts", [])]
shots = [s["seconds"] for s in cuts.get("shots", [])]
out = {"id": d.name, "title": info.get("title"), "uploader": info.get("uploader"),
       "duration_s": round(dur, 2), "fps": cuts.get("fps")}

# --- rhythm -------------------------------------------------------------
r = {"hard_cuts": len(cut_t),
     "cuts_per_min": round(len(cut_t) / dur * 60, 2) if dur else None,
     "cut_times_s": [round(t, 2) for t in cut_t],
     "median_shot_s": round(st.median(shots), 2) if shots else None,
     "mean_shot_s": round(st.mean(shots), 2) if shots else None,
     "shots_over_10s": sum(1 for s in shots if s > 10),
     "first_cut_s": round(cut_t[0], 2) if cut_t else None,
     "not_cuts": [{"t": round(n.get("t", 0), 2), "kind": n.get("kind") or n.get("why")} for n in cuts.get("not_cuts", [])]}
if cuts.get("shots"):
    longest = max(cuts["shots"], key=lambda s: s["seconds"])
    r["longest_shot"] = {"start": round(longest["start"], 2), "end": round(longest["end"], 2),
                         "seconds": longest["seconds"], "share_of_runtime": round(longest["seconds"] / dur, 3) if dur else None}
# bursts: maximal spans where a 5 s window holds >= 5 cuts
bursts = []
for i, t in enumerate(cut_t):
    j = i
    while j + 1 < len(cut_t) and cut_t[j + 1] - t <= 5.0:
        j += 1
    if j - i + 1 >= 5:
        s, e = t, cut_t[j]
        if bursts and s <= bursts[-1][1]:
            bursts[-1][1] = e
        else:
            bursts.append([s, e])
r["bursts"] = [{"start_s": round(s, 2), "end_s": round(e, 2),
                "cuts": sum(1 for t in cut_t if s <= t <= e),
                "mid_share": round(((s + e) / 2) / dur, 3) if dur else None} for s, e in bursts]
out["rhythm"] = r

# --- on-screen events ----------------------------------------------------
holds = [h["seconds"] for h in events.get("holds", [])]
out["events"] = {"counts": events.get("counts"),
                 "holds_over_1s": sum(1 for h in holds if h >= 1),
                 "median_hold_s": round(st.median(holds), 2) if holds else None,
                 "longest_hold_s": max(holds) if holds else None,
                 "windows": len(events.get("windows", []))}

# --- sampled frames (every 2 s) ------------------------------------------
if scan:
    diffs = [f["diffFromPrev"] for f in scan if f.get("diffFromPrev") is not None]
    static = [f for f in scan if f.get("diffFromPrev") is not None and f["diffFromPrev"] < 0.02]
    run = best = 0
    best_end = None
    for f in scan:
        if f.get("diffFromPrev") is not None and f["diffFromPrev"] < 0.02:
            run += 2
            if run > best:
                best, best_end = run, f["t"]
        else:
            run = 0
    lum = [f["meanLuminance"] for f in scan]
    out["frames"] = {
        "count": len(scan),
        "not_evidence_frames": [f["frame"] for f in scan if f.get("isEvidence") is False],
        "dark_share": round(sum(1 for x in lum if x < 0.35) / len(lum), 3),
        "light_share": round(sum(1 for x in lum if x > 0.7) / len(lum), 3),
        "median_contentful_cells": round(st.median(f["contentfulCells"] for f in scan), 3),
        "intervals_new_composition_share": round(sum(1 for x in diffs if x >= 0.25) / len(diffs), 3) if diffs else None,
        "intervals_static_share": round(len(static) / len(diffs), 3) if diffs else None,
        "longest_static_run_s": best, "longest_static_run_ends_at_s": best_end,
        "frame0": {k: scan[0].get(k) for k in ("meanLuminance", "contentfulCells", "blankCells", "isEvidence")},
    }
    # deterministic list of frames the analyst must open at full resolution
    n = len(scan)
    if n <= 60:
        pick = list(range(n))
    else:
        pick = {0, n - 1}
        pick |= {i for i, f in enumerate(scan) if (f.get("diffFromPrev") or 0) >= 0.25}
        pick |= set(range(0, n, 3))
        pick = sorted(pick)
        if len(pick) > 70:
            keep = {0, n - 1} | {i for i in pick if (scan[i].get("diffFromPrev") or 0) >= 0.25}
            rest = [i for i in pick if i not in keep]
            step = max(1, len(rest) // max(1, 70 - len(keep)))
            pick = sorted(keep | set(rest[::step]))[:70]
    out["frames_to_open"] = [scan[i]["frame"] for i in pick]

# --- sound ----------------------------------------------------------------
snd = {}
if audio:
    snd["kind"] = audio.get("kind", {}).get("value")
    lo = audio.get("loudness", {})
    snd["lufs_integrated"] = lo.get("lufsIntegrated")
    snd["lufs_short_term_max"] = lo.get("lufsShortTermMax")
    snd["true_peak_db"] = lo.get("truePeakDb")
    snd["bpm"] = (audio.get("bpm") or {}).get("value")
    b = audio.get("beats") or {}
    snd["beats"] = {"count": len(b.get("times", [])), "confidence": b.get("confidence"), "reason": b.get("reason")}
    snd["silence_spans"] = audio.get("silence")
    snd["sections"] = (audio.get("sections") or {}).get("spans")
    snd["describe_tags"] = [(t["label"], t["score"]) for t in (audio.get("describe") or {}).get("tags", [])[:8]]
eb = (m / "ebur128.txt")
if eb.exists():
    txt = eb.read_text()
    lra = re.search(r"LRA:\s+(-?[\d.]+)", txt)
    snd["lra_lu"] = float(lra.group(1)) if lra else None
strong = (events.get("sound") or {}).get("strong_onsets") or []
if strong and cut_t and dur:
    tol = 0.12
    hit = sum(1 for t in cut_t if any(abs(t - o) <= tol for o in strong))
    # chance a random instant lies within tol of some strong onset
    covered = 0.0
    last = -1e9
    for o in sorted(strong):
        lo_, hi_ = max(o - tol, last), o + tol
        if hi_ > lo_:
            covered += hi_ - lo_
        last = max(last, hi_)
    snd["cuts_on_strong_onset_share"] = round(hit / len(cut_t), 3)
    snd["chance_share"] = round(min(1.0, covered / dur), 3)
    snd["strong_onsets_per_min"] = round(len(strong) / dur * 60, 1)
out["sound"] = snd
out["look"] = {k: look.get(k) for k in ("luma", "contrast", "saturation", "bw_share", "warmth")}
print(json.dumps(out, indent=1))
