#!/usr/bin/env python3
"""Narration check: gate a read-aloud script before it goes into a voice model.

A narrated version of a story is a prompt for a text-to-speech model, and the
things that go wrong with one are mechanical: a tag the model does not know, an
SSML break tag the v3 model ignores, a part longer than the paste box, setup
instructions leaking into the spoken text, an em dash. This script fails on
those and reports the rest as warnings, so the person pasting the parts does
not find out at render time.

Usage:
  narration_check.py NARRATION.md [--max-chars 2000] [--tags-per-100 6]
                     [--allow-tag TAG ...] [--voice-only] [--wpm-slow 140 --wpm-fast 175]
                     [--json OUT] [--quiet]
  narration_check.py --self-test

The file has the shape references/narration.md describes: any number of
sections before a heading containing "speech" (setup notes, synopsis, route),
then that heading, then one `### Part N` heading per paste-ready part.

Exit 1 on: an audio tag outside the known set (extend it with --allow-tag),
an SSML <break> tag, an em dash, a part longer than --max-chars characters,
setup vocabulary inside the speech (voice id, stability, speed, model id,
pronunciation dictionary), or no parts found.

Warnings on: a sound-effect tag (these are the least consistent in the guide;
--voice-only makes it a failure), more than --tags-per-100 tags per hundred
words in a part, three sentences in a row opening on a tag, and the estimated
duration, which is printed as a range at two reading speeds and never as one
number.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Every tag the ElevenLabs v3 guide names or uses in its sample scripts
# (docs/elevenlabs/best-practices-2026-09-05.md), plus the Enhance prompt's
# list. Anything else is a guess about the model.
VOICE_TAGS = {
    "laughs", "laughs harder", "starts laughing", "wheezing", "whispers", "whisper",
    "sighs", "exhales", "sarcastic", "curious", "excited", "crying", "snorts",
    "mischievously", "happy", "sad", "angry", "annoyed", "appalled", "thoughtful",
    "surprised", "laughing", "chuckles", "clears throat", "short pause", "long pause",
    "pause", "exhales sharply", "inhales deeply", "frustrated sigh", "happy gasp",
    "sigh", "giggles", "giggling", "dramatically", "reassuring", "professional",
    "sympathetic", "questioning", "impressed", "delighted", "amazed", "warmly",
    "nervously", "alarmed", "sheepishly", "stifling laughter", "frustrated",
    "cracking up", "desperately", "deadpan", "excitedly", "curiously",
    "laughing hysterically", "pauses", "dismissive", "cute", "with genuine belly laugh",
    "sings", "singing quickly", "woo",
}
SFX_TAGS = {"gunshot", "applause", "clapping", "explosion", "swallows", "gulps", "fart"}
ACCENT = re.compile(r"^strong .+ accent$")
SETUP_WORDS = re.compile(
    r"\b(voice id|voice_id|stability|playback speed|speed setting|model id|model_id|"
    r"eleven_v3|pronunciation dictionar\w*|creative or natural|paste)\b", re.I)
TAG_RE = re.compile(r"\[([^\[\]\n]{1,40})\]")
SENT_RE = re.compile(r"[^.!?]+[.!?]+[\"”’]?")


def split(text: str):
    """Return (setup_text, [(part_name, part_text), ...])."""
    lines = text.splitlines()
    speech_at = None
    for i, ln in enumerate(lines):
        # The speech heading ends with the word "speech"; a setup heading that
        # merely mentions the speech box ("keep these out of the speech box")
        # does not.
        if re.match(r"^#{1,3}\s", ln) and re.search(r"\bspeech\s*$", ln, re.I):
            speech_at = i
            break
    if speech_at is None:
        return text, []
    setup = "\n".join(lines[:speech_at])
    parts, cur, buf = [], None, []
    for ln in lines[speech_at + 1:]:
        m = re.match(r"^#{2,4}\s+(.+?)\s*$", ln)
        if m:
            if cur is not None:
                parts.append((cur, "\n".join(buf).strip()))
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        parts.append((cur, "\n".join(buf).strip()))
    return setup, [(n, b) for n, b in parts if b]


def check(text: str, max_chars: int, tags_per_100: float, allow: set[str],
          voice_only: bool, wpm_slow: int, wpm_fast: int) -> dict:
    fails, warns = [], []
    setup, parts = split(text)
    if not parts:
        fails.append(("no-parts", "no '### Part N' headings found after a heading containing 'speech'"))
        return {"fails": fails, "warns": warns, "parts": []}
    report = []
    total_words = 0
    for name, body in parts:
        spoken = TAG_RE.sub("", body)
        words = len(spoken.split())
        total_words += words
        chars = len(body)
        if chars > max_chars:
            fails.append(("part-too-long", f"{name}: {chars} characters, limit {max_chars}"))
        if "—" in body:
            fails.append(("em-dash", f"{name}: em dash at offset {body.index('—')}"))
        if re.search(r"<\s*break\b", body, re.I):
            fails.append(("ssml-break", f"{name}: <break> tag; Eleven v3 ignores SSML breaks"))
        m = SETUP_WORDS.search(body)
        if m:
            fails.append(("setup-in-speech", f"{name}: setup vocabulary in the spoken text: \"{m.group(0)}\""))
        tags = [t.strip().lower() for t in TAG_RE.findall(body)]
        for t in tags:
            if t in VOICE_TAGS or t in allow or ACCENT.match(t):
                continue
            if t in SFX_TAGS:
                (fails if voice_only else warns).append(("sfx-tag", f"{name}: sound-effect tag [{t}]"))
                continue
            fails.append(("unknown-tag", f"{name}: [{t}] is not in the v3 guide; add --allow-tag \"{t}\" if it is deliberate"))
        density = (len(tags) / words * 100) if words else 0
        if density > tags_per_100:
            warns.append(("tag-density", f"{name}: {len(tags)} tags in {words} words ({density:.1f} per 100)"))
        sents = SENT_RE.findall(body)
        run = 0
        for s in sents:
            if s.strip().startswith("["):
                run += 1
                if run == 3:
                    warns.append(("tag-opener-run", f"{name}: three sentences in a row open on a tag"))
                    break
            else:
                run = 0
        report.append({"part": name, "chars": chars, "words": words, "tags": len(tags)})
    slow = total_words / wpm_slow
    fast = total_words / wpm_fast
    warns.append(("duration", f"{total_words} spoken words: about {fast:.1f} to {slow:.1f} minutes "
                              f"at {wpm_fast} to {wpm_slow} words per minute, before pauses; the real length exists only once it is rendered"))
    return {"fails": fails, "warns": warns, "parts": report, "words": total_words}


GOOD = """# A story: read-aloud

## Setup notes (keep these out of the speech box)

Model Eleven v3, stability Creative or Natural. Paste one part per generation.

## The speech

### Part 1

[thoughtful] Four small creatures wake in the ash. [short pause] One of them counts things.

[whispers] Get ahead of it.

### Part 2

[reassuring] But every world has an ember. That's the job. [sighs] So they split up.
"""

BAD = """# A story: read-aloud

## The speech

### Part 1

[grinning] Four small creatures wake in the ash — one of them counts things. <break time="1s" /> Set stability to Creative.
"""


def self_test() -> int:
    cases = []
    r = check(GOOD, 2000, 6, set(), False, 140, 175)
    cases.append(("a well-formed narration passes", not r["fails"]))
    kinds = {k for k, _ in check(BAD, 2000, 6, set(), False, 140, 175)["fails"]}
    cases.append(("an unknown tag fails", "unknown-tag" in kinds))
    cases.append(("an em dash fails", "em-dash" in kinds))
    cases.append(("an SSML break fails", "ssml-break" in kinds))
    cases.append(("setup vocabulary in the speech fails", "setup-in-speech" in kinds))
    r = check(GOOD.replace("[thoughtful]", "[thoughtful] " + "word " * 900), 2000, 6, set(), False, 140, 175)
    cases.append(("a part over the character limit fails", any(k == "part-too-long" for k, _ in r["fails"])))
    r = check(GOOD.replace("[sighs]", "[gunshot]"), 2000, 6, set(), False, 140, 175)
    cases.append(("a sound-effect tag warns by default", any(k == "sfx-tag" for k, _ in r["warns"]) and not r["fails"]))
    r = check(GOOD.replace("[sighs]", "[gunshot]"), 2000, 6, set(), True, 140, 175)
    cases.append(("a sound-effect tag fails under --voice-only", any(k == "sfx-tag" for k, _ in r["fails"])))
    r = check(GOOD.replace("[sighs]", "[wistful]"), 2000, 6, {"wistful"}, False, 140, 175)
    cases.append(("an allowed tag passes", not r["fails"]))
    r = check("# x\n\nno speech heading here\n", 2000, 6, set(), False, 140, 175)
    cases.append(("a file with no parts fails", any(k == "no-parts" for k, _ in r["fails"])))
    ok = True
    for name, passed in cases:
        print(f"  {'pass' if passed else 'FAIL'}  {name}")
        ok = ok and passed
    print("\nall self-tests passed" if ok else "\nself-test failures")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--max-chars", type=int, default=2000)
    ap.add_argument("--tags-per-100", type=float, default=6)
    ap.add_argument("--allow-tag", action="append", default=[])
    ap.add_argument("--voice-only", action="store_true")
    ap.add_argument("--wpm-slow", type=int, default=140)
    ap.add_argument("--wpm-fast", type=int, default=175)
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.file:
        ap.error("a narration file or --self-test")
    text = open(a.file, encoding="utf-8").read()
    r = check(text, a.max_chars, a.tags_per_100, {t.lower() for t in a.allow_tag},
              a.voice_only, a.wpm_slow, a.wpm_fast)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(r, f, indent=2)
    print(f"{a.file}: {len(r['parts'])} part(s), {r.get('words', 0)} spoken words, "
          f"{len(r['fails'])} fail(s), {len([w for w in r['warns'] if w[0] != 'duration'])} warning(s)")
    for k, msg in r["fails"]:
        print(f"  FAIL  {k:<18} {msg}")
    if not a.quiet:
        for k, msg in r["warns"]:
            print(f"  warn  {k:<18} {msg}")
        for p in r["parts"]:
            print(f"  part  {p['part']:<10} {p['chars']:>5} chars {p['words']:>4} words {p['tags']:>2} tags")
    return 1 if r["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
