#!/usr/bin/env python3
"""Video tools for a generated hero clip. Needs ffmpeg and ffprobe on PATH.

    python3 clip_tools.py report  clip.mp4
    python3 clip_tools.py reverse clip.mp4 out.mp4
    python3 clip_tools.py joins   clip.mp4 [--ratio 2.5]
    python3 clip_tools.py grade   clip.mp4 out.mp4 --bg "#F4F1EA" [--tolerance 6]
    python3 clip_tools.py seam    clip.mp4 [--ratio 2.5]
    python3 clip_tools.py loop    clip.mp4 out.mp4
    python3 clip_tools.py xfade   a.mp4 b.mp4 out.mp4 [--seconds 0.4]
    python3 clip_tools.py flashes clip.mp4 [--loops 2]
    python3 clip_tools.py variants clip.mp4 outdir/ [--desktop-crf 23 --phone-width 720 --phone-crf 28 --av1]

report    duration, resolution, frame rate, size and whether an audio track is present.
reverse   play a clip backwards. To show things settling into an arrangement, generate the
          settled still, animate it coming apart, and reverse the result.
joins     measure the mean frame-to-frame difference through the whole clip and flag any jump more
          than --ratio times the median of its neighbours. A skip at a join, where one clip ended
          still moving and the next started from rest, measured 1.41 against 0.4-0.5 either side.
          Exit 1 when a jump is found. Sampled frames on a contact sheet cannot show this.
grade     lift the clip's darkest backdrop to the page's background colour, clamp at it, and report
          the share of sampled pixels that now match the page exactly, so the video has no visible
          frame. The source run matched 88%, the rest being the subject and its shadow.
seam      measure the wraparound of a looping clip: the difference from the last frame back to the
          first, against the median difference inside the clip. Exit 1 when the seam is a jump.
          Identical endpoint pictures can still loop badly (a model rushing back to its first pose),
          so watch the loop as well; this catches the jump, not the acceleration.
loop      drop the final frame when it repeats the first, which first-and-last-frame conditioning
          produces, so the loop does not hold one frame twice at the seam.
xfade     join two clips with a short crossfade after normalising frame rate, size and pixel format,
          which FFmpeg's xfade requires. A dissolve can ghost over motion that does not match, so
          run joins on the result and look at the join.
flashes   a proxy for WCAG 2.3.1 (no more than three flashes in any one second): counts opposing
          swings in mean luminance over 20 of 255 within each one-second window, across the loop
          seam as well. Exit 1 above three. It is not a certified flash analysis (that measures area
          and red flashes too); a clip that flags here needs regenerating, and one that passes still
          needs watching.
variants  write the web files: a desktop H.264 MP4, a smaller phone MP4, a WebM (VP9), the first
          frame as the poster and the last frame as the resting still, all without audio, with
          faststart so playback can begin before the file finishes loading. --av1 adds an AV1 file
          to list first; keep the H.264 file last as the fallback every browser plays. CRF is a
          quality setting, not a size: read the megabytes it reports against the budget.
"""
import argparse
import json
import os
import statistics
import subprocess
import sys

W, H = 64, 36  # thumbnail size for frame differences: enough to see motion, cheap to compare


def ffprobe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def report(path):
    info = ffprobe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    if v is None:
        raise SystemExit(f"{path}: no video stream")
    num, den = (v.get("avg_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    r = {
        "path": path,
        "seconds": round(float(info["format"].get("duration", 0)), 3),
        "width": v["width"],
        "height": v["height"],
        "fps": round(fps, 3),
        "codec": v["codec_name"],
        "megabytes": round(int(info["format"].get("size", 0)) / 1e6, 2),
        "audio": any(s["codec_type"] == "audio" for s in info["streams"]),
    }
    return r


def frames_gray(path):
    """Yield each frame as bytes of a W x H greyscale thumbnail."""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = W * H
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield buf
    p.wait()


def diffs(path):
    prev, out = None, []
    for f in frames_gray(path):
        if prev is not None:
            out.append(sum(abs(a - b) for a, b in zip(f, prev)) / len(f))
        prev = f
    return out


def joins(path, ratio=2.5, window=6):
    d = diffs(path)
    if len(d) < 3:
        return {"frames": len(d) + 1, "jumps": []}
    fps = report(path)["fps"] or 24
    jumps = []
    for i, x in enumerate(d):
        neigh = d[max(0, i - window):i] + d[i + 1:i + 1 + window]
        med = statistics.median(neigh) if neigh else 0
        if med > 0 and x > ratio * med and x > 1.0:
            jumps.append({"frame": i + 1, "seconds": round((i + 1) / fps, 3), "difference": round(x, 2),
                          "neighbours": round(med, 2)})
    return {"frames": len(d) + 1, "median": round(statistics.median(d), 2), "jumps": jumps}


def seam(path, ratio=2.5):
    frames = list(frames_gray(path))
    if len(frames) < 4:
        raise SystemExit(f"{path}: too few frames to judge a loop")
    d = [sum(abs(a - b) for a, b in zip(f, g)) / len(f) for g, f in zip(frames, frames[1:])]
    wrap = sum(abs(a - b) for a, b in zip(frames[0], frames[-1])) / len(frames[0])
    med = statistics.median(d)
    return {"frames": len(frames), "median": round(med, 2), "seam": round(wrap, 2),
            "duplicateEndpoint": wrap < 0.05,
            "jump": bool(med > 0 and wrap > ratio * med and wrap > 1.0)}


def loop(src, dst):
    """Drop the last frame if it repeats the first (first == last conditioning), so the seam is clean."""
    info = seam(src)
    n = info["frames"] - (1 if info["duplicateEndpoint"] else 0)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"select='lt(n,{n})',setpts=N/FRAME_RATE/TB",
                    "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
    return {"out": dst, "droppedDuplicate": info["duplicateEndpoint"], "frames": n}


def xfade(a, b, dst, seconds=0.4):
    ra, rb = report(a), report(b)
    fps = ra["fps"] or 24
    norm = f"fps={fps},scale={ra['width']}:{ra['height']},format=yuv420p,settb=AVTB"
    offset = max(0.0, ra["seconds"] - seconds)
    fc = (f"[0:v]{norm}[a];[1:v]{norm}[b];"
          f"[a][b]xfade=transition=fade:duration={seconds}:offset={offset:.3f}[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-i", b, "-filter_complex", fc, "-map", "[v]", "-an",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
    return {"out": dst, "seconds": round(ra["seconds"] + rb["seconds"] - seconds, 3), "joinAt": round(offset, 3)}


def flashes(path, loops=2, swing=20.0):
    means = [sum(f) / len(f) for f in frames_gray(path)] * max(1, loops)
    fps = report(path)["fps"] or 24
    events, direction, anchor = [], 0, means[0] if means else 0
    for i, m in enumerate(means):
        if m - anchor >= swing and direction <= 0:
            events.append(i); direction, anchor = 1, m
        elif anchor - m >= swing and direction >= 0:
            events.append(i); direction, anchor = -1, m
        elif (direction > 0 and m > anchor) or (direction < 0 and m < anchor):
            anchor = m
    # A flash is a pair of opposing changes; count pairs inside each one-second window.
    win = max(1, int(round(fps)))
    worst = 0
    for i in range(len(events)):
        inside = sum(1 for e in events[i:] if e - events[i] < win)
        worst = max(worst, inside // 2)
    return {"fps": fps, "transitions": len(events), "worstFlashesPerSecond": worst, "fails": worst > 3}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def grade(src, dst, bg, tolerance=6):
    r, g, b = hex_rgb(bg)
    # Find the darkest backdrop level from a few frames' border pixels, then map it to the page colour
    # and clamp at it, so the backdrop reads as the page and nothing below it can show.
    probe = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", "scale=160:-2,format=rgb24", "-frames:v", "1",
                            "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    width = 160
    height = len(probe) // (width * 3)
    border = []
    for y in range(height):
        for x in (0, 1, width - 2, width - 1):
            i = (y * width + x) * 3
            border.append(probe[i:i + 3])
    darkest = min(border, key=lambda p: sum(p))
    exprs = []
    for chan, target, src_level in zip("rgb", (r, g, b), darkest):
        lo = max(src_level, 1)
        exprs.append(f"{chan}='clip(val*{target}/{lo},{target},255)'")
    vf = "format=rgb24,lutrgb=" + ":".join(exprs) + ",format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-crf", "18",
                    "-preset", "slow", "-movflags", "+faststart", dst], check=True)
    sample = subprocess.run(["ffmpeg", "-v", "error", "-i", dst, "-vf", "fps=2,scale=160:-2,format=rgb24",
                             "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    px = [sample[i:i + 3] for i in range(0, len(sample) - 2, 3)]
    match = sum(1 for p in px if abs(p[0] - r) <= tolerance and abs(p[1] - g) <= tolerance and abs(p[2] - b) <= tolerance)
    return {"out": dst, "background": bg, "matchingShare": round(match / max(1, len(px)), 3)}


# Provisional budgets: Codex's panel member offered phone <= 1 MB and desktop <= 3 MB as conservative
# experimental limits, not measured browser limits (docs/deep-research). They are warnings to read,
# not a pass mark; the page's LCP on the target devices is the real test.
BUDGET_MB = {"phone": 1.0, "desktop": 3.0}


def variants(src, outdir, desktop_crf=23, phone_width=720, phone_crf=28, av1=False):
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0]
    paths = {
        "desktop": os.path.join(outdir, f"{stem}.mp4"),
        "phone": os.path.join(outdir, f"{stem}-phone.mp4"),
        "webm": os.path.join(outdir, f"{stem}.webm"),
        "poster": os.path.join(outdir, f"{stem}-poster.jpg"),
        "rest": os.path.join(outdir, f"{stem}-rest.jpg"),
    }
    env = {**os.environ, "SVT_LOG": "1"}  # SVT-AV1 logs to stderr on its own; keep errors only
    run = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True, env=env)
    run("-i", src, "-an", "-c:v", "libx264", "-crf", str(desktop_crf), "-preset", "slow", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", paths["desktop"])
    run("-i", src, "-an", "-vf", f"scale='min({phone_width},iw)':-2", "-c:v", "libx264", "-crf", str(phone_crf), "-preset", "slow",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", paths["phone"])
    run("-i", src, "-an", "-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0", "-row-mt", "1", paths["webm"])
    run("-i", src, "-frames:v", "1", "-q:v", "3", paths["poster"])
    run("-sseof", "-0.1", "-i", src, "-frames:v", "1", "-q:v", "3", paths["rest"])
    if av1:
        paths["av1"] = os.path.join(outdir, f"{stem}-av1.mp4")
        run("-i", src, "-an", "-c:v", "libsvtav1", "-crf", "35", "-preset", "6", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", paths["av1"])
    out = {k: {"path": v, "megabytes": round(os.path.getsize(v) / 1e6, 2)} for k, v in paths.items()}
    for k, cap in BUDGET_MB.items():
        if out[k]["megabytes"] > cap:
            out[k]["warn"] = f"over the provisional {cap:g} MB budget: shorten or simplify the clip before raising it"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("report"); p.add_argument("clip")
    p = sub.add_parser("reverse"); p.add_argument("clip"); p.add_argument("out")
    p = sub.add_parser("joins"); p.add_argument("clip"); p.add_argument("--ratio", type=float, default=2.5)
    p = sub.add_parser("seam"); p.add_argument("clip"); p.add_argument("--ratio", type=float, default=2.5)
    p = sub.add_parser("loop"); p.add_argument("clip"); p.add_argument("out")
    p = sub.add_parser("xfade"); p.add_argument("a"); p.add_argument("b"); p.add_argument("out")
    p.add_argument("--seconds", type=float, default=0.4)
    p = sub.add_parser("flashes"); p.add_argument("clip"); p.add_argument("--loops", type=int, default=2)
    p = sub.add_parser("grade"); p.add_argument("clip"); p.add_argument("out"); p.add_argument("--bg", required=True)
    p.add_argument("--tolerance", type=int, default=6)
    p = sub.add_parser("variants"); p.add_argument("clip"); p.add_argument("outdir")
    p.add_argument("--desktop-crf", type=int, default=23); p.add_argument("--phone-width", type=int, default=720)
    p.add_argument("--phone-crf", type=int, default=28); p.add_argument("--av1", action="store_true")
    a = ap.parse_args()
    if a.cmd == "report":
        print(json.dumps(report(a.clip), indent=2))
    elif a.cmd == "reverse":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.clip, "-vf", "reverse", "-an", "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", a.out], check=True)
        print(json.dumps(report(a.out), indent=2))
    elif a.cmd == "joins":
        r = joins(a.clip, a.ratio)
        print(json.dumps(r, indent=2))
        return 1 if r["jumps"] else 0
    elif a.cmd == "seam":
        r = seam(a.clip, a.ratio)
        print(json.dumps(r, indent=2))
        return 1 if r["jump"] else 0
    elif a.cmd == "loop":
        print(json.dumps(loop(a.clip, a.out), indent=2))
    elif a.cmd == "xfade":
        print(json.dumps(xfade(a.a, a.b, a.out, a.seconds), indent=2))
    elif a.cmd == "flashes":
        r = flashes(a.clip, a.loops)
        print(json.dumps(r, indent=2))
        return 1 if r["fails"] else 0
    elif a.cmd == "grade":
        print(json.dumps(grade(a.clip, a.out, a.bg, a.tolerance), indent=2))
    elif a.cmd == "variants":
        print(json.dumps(variants(a.clip, a.outdir, a.desktop_crf, a.phone_width, a.phone_crf, a.av1), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
