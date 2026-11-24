#!/usr/bin/env python3
"""Find single-frame pops and dead stretches in a rendered film.

    python3 pop_scan.py out/draft.mp4 [--json] [--ratio 3] [--still 4] [--ignore 12.0-13.5,20-21]

A pop is one frame that jumps out of place: its difference from the previous frame
is at least --ratio times the difference on both sides of it (the method in the
prompts behind two of the most-liked films on prompt-motion.com: "scan for
single-frame pops, frame-difference spikes 3x their neighbours"). A hard cut is also
a spike, and so is each character of a typed line and each step of animation held on
twos, so read each pop against the timeline: a pop on a planned cut, a keystroke or a
held pose is fine (pass those spans to --ignore), a pop anywhere else is a frame shown
before its tween starts, two texts swapping, or a flood that changes half the frame at
once.

A dead stretch is a run of frames with almost no change, reported when it lasts at
least --still seconds (the skill's ceiling outside a planned stop is 4 s).

Standard library only; needs ffmpeg on PATH. Frames are measured at 160 px wide in
grey, so the numbers are relative, not absolute.
"""
import argparse
import json
import re
import subprocess
import sys


def frame_diffs(path):
    """Mean absolute luma difference between each frame and the one before it."""
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", path,
        "-vf", "scale=160:-2,format=gray,tblend=all_mode=difference,signalstats,"
               "metadata=print:key=lavfi.signalstats.YAVG:file=-",
        "-an", "-f", "null", "-",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("ffmpeg failed: " + out.stderr.strip().splitlines()[-1])
    times, vals = [], []
    t = None
    for line in out.stdout.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m:
            t = float(m.group(1))
            continue
        m = re.search(r"YAVG=([0-9.]+(?:[eE][-+]?[0-9]+)?)", line)  # ffmpeg prints tiny values as 6.9e-05
        if m and t is not None:
            times.append(t)
            vals.append(float(m.group(1)))
    return times, vals


def parse_ignore(spec):
    spans = []
    for part in filter(None, (spec or "").split(",")):
        a, b = part.split("-")
        spans.append((float(a), float(b)))
    return spans


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("--ratio", type=float, default=3.0, help="spike over both neighbours (default 3)")
    ap.add_argument("--floor", type=float, default=1.0, help="ignore spikes smaller than this mean difference")
    ap.add_argument("--still", type=float, default=4.0, help="report still runs of at least this many seconds")
    ap.add_argument("--still-level", type=float, default=0.15, help="difference under this counts as still")
    ap.add_argument("--ignore", help="time spans to skip, e.g. 12.0-13.5,20-21 (planned bursts)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    times, d = frame_diffs(a.video)
    if len(d) < 3:
        sys.exit("too few frames to scan")
    skip = parse_ignore(a.ignore)
    ignored = lambda t: any(x <= t <= y for x, y in skip)

    pops = []
    for i in range(1, len(d) - 1):
        v, before, after = d[i], d[i - 1], d[i + 1]
        if v >= a.floor and v >= a.ratio * max(before, 1e-3) and v >= a.ratio * max(after, 1e-3) and not ignored(times[i]):
            pops.append({"t": round(times[i], 3), "frame": i, "diff": round(v, 2),
                         "ratio": round(v / max(before, after, 1e-3), 1)})

    stills, start = [], None
    for i, v in enumerate(d + [99.0]):
        if v < a.still_level and start is None:
            start = i
        elif v >= a.still_level and start is not None:
            t0, t1 = times[start], times[min(i, len(times) - 1)]
            if t1 - t0 >= a.still:
                stills.append({"from": round(t0, 2), "to": round(t1, 2), "seconds": round(t1 - t0, 2)})
            start = None

    result = {"video": a.video, "frames": len(d) + 1, "duration": round(times[-1], 2),
              "pops": pops, "still_runs": stills}
    if a.json:
        print(json.dumps(result, indent=1))
        return
    print(f"{a.video}: {result['frames']} frames, {result['duration']} s")
    print(f"pops (>= {a.ratio}x both neighbours): {len(pops)}")
    for p in pops:
        print(f"  t={p['t']:.3f}s frame {p['frame']}  diff {p['diff']}  {p['ratio']}x")
    print(f"still runs >= {a.still}s: {len(stills)}")
    for s in stills:
        print(f"  {s['from']:.2f}-{s['to']:.2f}s ({s['seconds']} s)")


if __name__ == "__main__":
    main()
