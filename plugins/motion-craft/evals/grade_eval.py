#!/usr/bin/env python3
"""Check motion-craft's [script] eval assertions against a run's outputs folder.

    python3 grade_eval.py <eval-id 1|2> <run>/outputs  [--json out.json]

Prints one line per assertion (PASS/FAIL with evidence) and writes grading-script.json beside the
outputs folder in skill-creator's expectations shape: [{"text", "passed", "evidence"}].
Needs ffmpeg and ffprobe on the PATH. Exit 0 when every check ran, whatever the verdicts; exit 2
when the outputs folder or the MP4 is missing.
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

DESIGN_CRAFT_ICONS = [
    Path("/Volumes/LLMs/Dev/fledgeling-plugins/plugins/design-craft/assets") / n
    for n in ("icon.png", "icon-256.png", "icon.svg")
]
SOURCE_SUFFIXES = {".html", ".js", ".mjs", ".jsx", ".tsx", ".ts", ".svg", ".css", ".json", ".md", ".py"}
SKIP_DIRS = {"node_modules", "vendor", "frames", ".hyperframes", "out", "renders", ".git"}
COMPOSITION_SUFFIXES = {".html", ".js", ".mjs", ".jsx", ".tsx", ".ts", ".svg"}
BANNED = ["seamless", "unlock", "supercharge", "game-changer", "revolutionize", "effortless"]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(mp4):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
               "-of", "json", str(mp4)]).stdout
    d = json.loads(out or "{}")
    streams = d.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    return float(d.get("format", {}).get("duration", 0)), v.get("width"), v.get("height"), \
        any(s.get("codec_type") == "audio" for s in streams)


def gray(mp4, t, w=96, h=54):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(mp4), "-frames:v", "1",
                          "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    return list(raw)


def files(root, suffixes):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in suffixes and not (set(p.relative_to(root).parts) & SKIP_DIRS):
            yield p


def text_of(root, suffixes):
    out = []
    for p in files(root, suffixes):
        try:
            if p.stat().st_size < 2_000_000:
                out.append((p, p.read_text(errors="ignore")))
        except OSError:
            pass
    return out


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def main(argv):
    if len(argv) < 3:
        sys.exit("usage: grade_eval.py <1|2> <run>/outputs [--json out.json]")
    eval_id, outputs = argv[1], Path(argv[2])
    mp4 = outputs / "film.mp4"
    if not mp4.is_file():
        print(f"FAIL no film.mp4 in {outputs}")
        sys.exit(2)
    project = outputs / "project"
    res = []

    def add(text, passed, evidence):
        res.append({"text": text, "passed": bool(passed), "evidence": evidence})

    dur, w, h, has_audio = probe(mp4)
    if eval_id == "1":
        add("An MP4 exists in outputs, 15-30 s long, 1920x1080", 15 <= dur <= 30 and (w, h) == (1920, 1080),
            f"ffprobe: {dur:.2f} s, {w}x{h}")
        add("The MP4 has an audio stream", has_audio, f"audio stream present: {has_audio}")
    else:
        add("An MP4 exists in outputs, 10-20 s long, 1080x1920", 10 <= dur <= 20 and (w, h) == (1080, 1920),
            f"ffprobe: {dur:.2f} s, {w}x{h}")

    f0 = gray(mp4, 0)
    rng = (max(f0) - min(f0)) if f0 else 0
    add("Frame 0 is not a flat field: its luma range (YMAX-YMIN) is at least 40", rng >= 40,
        f"frame 0 luma range {rng} (96x54 grey thumbnail)")
    f3 = gray(mp4, 3.0)
    diff = sum(abs(a - b) for a, b in zip(f0, f3)) / len(f0) if f0 and f3 and len(f0) == len(f3) else 0
    add("The picture changes within the first 3 s: mean absolute difference between the frames at 0.0 s and 3.0 s is at least 2.0",
        diff >= 2.0, f"mean abs luma difference 0 s vs 3 s: {diff:.2f}")

    comp = text_of(project, COMPOSITION_SUFFIXES) if project.is_dir() else []
    if eval_id == "1":
        icon_hashes = {md5(p): p.name for p in DESIGN_CRAFT_ICONS if p.is_file()}
        copies = [str(p.relative_to(outputs)) for p in project.rglob("*")
                  if p.is_file() and p.suffix.lower() in {".png", ".svg"} and p.stat().st_size < 5_000_000
                  and md5(p) in icon_hashes] if project.is_dir() else []
        refs = [str(p.relative_to(outputs)) for p, t in comp if re.search(r"design-craft/assets/icon(-256)?\.(png|svg)", t)]
        add("The plugin's real icon file is used (byte-identical copy in the project, or a path reference)",
            bool(copies or refs), f"copies: {copies[:3]}; references: {refs[:3]}")
        hits = [(str(p.relative_to(outputs)), wd) for p, t in comp for wd in BANNED if re.search(rf"\b{wd}\b", t, re.I)]
        add("No banned hype word appears in any composition source file", not hits, f"hits: {hits[:5]}")
    else:
        alltext = "\n".join(t for _, t in text_of(project, SOURCE_SUFFIXES)) if project.is_dir() else ""
        found = [s for s in ("7145", "7,145", "1187", "1,187", "119%") if s in alltext]
        add("At least one headline figure computed from the CSV (7145, 1187, 119%) appears in the composition source",
            bool(found), f"found: {found}")
        # The "no contradicting number" check was dropped after iteration 1; see dropped_assertions in evals.json.

    for r in res:
        print(("PASS " if r["passed"] else "FAIL ") + r["text"] + " — " + r["evidence"])
    out = outputs.parent / "grading-script.json"
    out.write_text(json.dumps({"expectations": res}, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv)
