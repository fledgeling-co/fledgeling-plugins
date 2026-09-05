#!/usr/bin/env python3
"""Context pack: assemble everything the drafter is allowed to see, and nothing else.

The drafter of scene N receives four things: the bible sections that apply to
this scene, the entry state (the previous scene's exit state), the beat card,
and the last two paragraphs of the previous scene. It does not receive the
rest of the manuscript. That restriction is the sliding window the research
found holds paragraph-level continuity where a flat context dump loses it
(references/evidence.md, E1, E2, E5), and doing it with a script rather than
by hand means the window cannot quietly widen.

Usage:
  context_pack.py --root story/ --beat ID [--tail 2] [--voice-file PATH] [--out PATH]

Reads   ROOT/bible.md, ROOT/beats.json, ROOT/state/<prev>.json, ROOT/scenes/<prev>.md
Writes  ROOT/packs/<ID>.md (or --out) and prints the path.

Bible selection: the sections included are `## Voice`, `## World`, `## Excluded`,
any `## <Name>` whose name is in the beat's `present` or `also_present` list, and
any heading named in the beat's `bible_sections` list. Everything else in the
bible stays out of the pack.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALWAYS = {"voice", "world", "style", "rules", "excluded"}


def sections(md: str) -> list[tuple[str, str]]:
    """Split markdown on ## headings; returns (heading, body) pairs."""
    out = []
    cur, buf = None, []
    for line in md.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if cur is not None:
                out.append((cur, "\n".join(buf).strip()))
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out.append((cur, "\n".join(buf).strip()))
    return out


def pick_sections(bible: str, beat: dict) -> list[tuple[str, str]]:
    wanted_names = {n.lower() for n in beat.get("present", []) + beat.get("also_present", [])}
    wanted_extra = {n.lower() for n in beat.get("bible_sections", [])}
    picked = []
    for h, body in sections(bible):
        key = h.lower().strip()
        first = key.split()[0] if key else ""
        if first in ALWAYS or key in wanted_extra or first in wanted_names or key in wanted_names:
            picked.append((h, body))
    return picked


def last_paragraphs(text: str, n: int) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()
             and not re.match(r"^(\*\s*\*\s*\*|#{1,6}\s|---+)", p.strip())]
    return paras[-n:] if paras else []


def find_previous(beats: list[dict], beat: dict, root: Path) -> tuple[Path | None, Path | None]:
    ids = [b["id"] for b in beats]
    if beat.get("follows"):
        pid = beat["follows"]
    else:
        i = ids.index(beat["id"])
        pid = None
        for j in range(i - 1, -1, -1):
            if (root / "state" / f"{ids[j]}.json").exists():
                pid = ids[j]
                break
    if not pid:
        return None, None
    return root / "state" / f"{pid}.json", root / "scenes" / f"{pid}.md"


def build(root: Path, beat_id: str, tail: int, voice_file: Path | None) -> str:
    bible_p, beats_p = root / "bible.md", root / "beats.json"
    if not bible_p.exists() or not beats_p.exists():
        raise SystemExit(f"need {bible_p} and {beats_p}")
    beats_doc = json.loads(beats_p.read_text())
    beats = beats_doc.get("scenes") if isinstance(beats_doc, dict) else beats_doc
    beat = next((b for b in beats if b.get("id") == beat_id), None)
    if not beat:
        raise SystemExit(f"beat {beat_id!r} not in {beats_p}")
    bible = bible_p.read_text()
    picked = pick_sections(bible, beat)
    state_p, scene_p = find_previous(beats, beat, root)
    entry_state = beat.get("entry_state")
    if entry_state is None and state_p:
        entry_state = json.loads(state_p.read_text())
    tail_paras = last_paragraphs(scene_p.read_text(), tail) if scene_p and scene_p.exists() else []
    words = beat.get("words", {"min": 400, "max": 1000})
    person = beat.get("person", "third")
    tense = beat.get("tense", "past")

    parts = [f"<scene_pack id=\"{beat_id}\">"]
    parts.append("<bible>")
    for h, body in picked:
        parts.append(f"<section name=\"{h}\">\n{body}\n</section>")
    parts.append("</bible>")
    if voice_file and voice_file.exists():
        parts.append(f"<voice source=\"{voice_file}\">\n{voice_file.read_text().strip()}\n</voice>")
    parts.append("<entry_state>")
    parts.append(json.dumps(entry_state, indent=2) if entry_state else
                 "null  (this is the first scene; the beat card's location, time and present list are the entry state)")
    parts.append("</entry_state>")
    parts.append("<beat>\n" + json.dumps(beat, indent=2) + "\n</beat>")
    parts.append("<previous_paragraphs>")
    if tail_paras:
        parts.extend(tail_paras)
    else:
        parts.append("(none: this scene opens the story or follows a scene not yet drafted)")
    parts.append("</previous_paragraphs>")
    task = f"""<task>
Write scene {beat_id} as {words['min']} to {words['max']} words of {person}-person, {tense}-tense prose in the voice above. The point of view is {beat.get('pov')}.

The scene starts from the entry state and the previous paragraphs, and ends on the beat's last_image with these threads still open: {json.dumps(beat.get('exit', {}).get('unresolved', []))}. Tension at the end is {beat.get('exit', {}).get('tension', 'higher')} than at the start.

Each paragraph after the first takes something from the paragraph before it: an object, a gesture, a line of dialogue, a question, a place. A paragraph that could be lifted out and read alone is the failure this pack exists to prevent, because the reader experiences it as the story losing its thread. When the scene needs a real jump in time or place, put a line containing only * * * before it.

Write plain, literal sentences; when a literal phrase is available, use it rather than a metaphor. Vary sentence length so that short sentences land where something changes. Use no em dashes. Resolve nothing the beat keeps open, and let the characters stay in the feeling the state gives them until the beat's change moves them.

Return only the prose, in a fenced block, then one line: EXIT_STATE_FOLLOWS, then the exit state as JSON in the same shape as the entry state (scene, time, location, characters, items, open_threads, promises, last_paragraph).
</task>"""
    parts.append(task)
    parts.append("</scene_pack>")
    return "\n".join(parts) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path("story"))
    ap.add_argument("--beat", required=True)
    ap.add_argument("--tail", type=int, default=2)
    ap.add_argument("--voice-file", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    text = build(a.root, a.beat, a.tail, a.voice_file)
    out = a.out or (a.root / "packs" / f"{a.beat}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    n_words = len(text.split())
    print(f"{out} ({n_words} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
