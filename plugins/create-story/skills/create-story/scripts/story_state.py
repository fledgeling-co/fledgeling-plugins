#!/usr/bin/env python3
"""Story state ledger: validate, diff and check the Chain of States.

The state file is the machine-readable answer to "where is everyone, what are
they holding, what do they want, what is still open" at the moment a scene
ends. The next scene is drafted from it rather than from the prose, which is
what keeps paragraph N conditioned on paragraph N-1 instead of on a diffuse
impression of the whole book (references/evidence.md, E1, E4, E5).

Commands:
  story_state.py validate STATE.json
  story_state.py validate-beats BEATS.json
  story_state.py diff BEFORE.json AFTER.json
  story_state.py check-exit --beats BEATS.json --beat ID --state EXIT.json
  story_state.py previous --beats BEATS.json --beat ID --state-dir DIR
  story_state.py --self-test

Exit 0 on success, 1 on any failure. Every failure names the field.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STATE_REQUIRED = {
    "scene": str, "time": str, "location": str, "characters": dict,
    "items": dict, "open_threads": list, "last_paragraph": str,
}
CHARACTER_REQUIRED = {"position": str, "holding": list, "wants": str, "feels": str}
ITEM_REQUIRED = {"where": str, "status": str}
BEAT_REQUIRED = {
    "id": str, "pov": str, "location": str, "present": list, "goal": str,
    "change": str, "function": str, "exit": dict, "words": dict,
}
EXIT_REQUIRED = {"unresolved": list, "tension": str, "last_image": str}
TENSION = {"higher", "same", "lower"}


def _load(p: Path):
    try:
        return json.loads(Path(p).read_text())
    except json.JSONDecodeError as e:
        raise SystemExit(f"{p}: not valid JSON ({e})")


def validate_state(s: dict, label: str = "state") -> list[str]:
    errs = []
    for k, t in STATE_REQUIRED.items():
        if k not in s:
            errs.append(f"{label}: missing field '{k}'")
        elif not isinstance(s[k], t):
            errs.append(f"{label}: field '{k}' should be {t.__name__}")
    for name, c in (s.get("characters") or {}).items():
        if not isinstance(c, dict):
            errs.append(f"{label}: characters.{name} should be an object")
            continue
        for k, t in CHARACTER_REQUIRED.items():
            if k not in c:
                errs.append(f"{label}: characters.{name} missing '{k}'")
            elif not isinstance(c[k], t):
                errs.append(f"{label}: characters.{name}.{k} should be {t.__name__}")
    for name, it in (s.get("items") or {}).items():
        if not isinstance(it, dict):
            errs.append(f"{label}: items.{name} should be an object")
            continue
        for k, t in ITEM_REQUIRED.items():
            if k not in it:
                errs.append(f"{label}: items.{name} missing '{k}'")
    if isinstance(s.get("open_threads"), list) and not s["open_threads"]:
        errs.append(f"{label}: open_threads is empty; a scene that resolves everything has no "
                    "next scene (mark at least one thread, or the story's end thread)")
    if isinstance(s.get("last_paragraph"), str) and len(s["last_paragraph"].split()) < 5:
        errs.append(f"{label}: last_paragraph should be the verbatim final paragraph (5+ words)")
    return errs


def validate_beats(b) -> list[str]:
    errs = []
    scenes = b.get("scenes") if isinstance(b, dict) else b
    if not isinstance(scenes, list) or not scenes:
        return ["beats: expected {\"scenes\": [...]} with at least one scene"]
    ids = set()
    for i, sc in enumerate(scenes):
        lab = f"scenes[{i}]" + (f" ({sc.get('id')})" if isinstance(sc, dict) and sc.get("id") else "")
        if not isinstance(sc, dict):
            errs.append(f"{lab}: should be an object")
            continue
        for k, t in BEAT_REQUIRED.items():
            if k not in sc:
                errs.append(f"{lab}: missing '{k}'")
            elif not isinstance(sc[k], t):
                errs.append(f"{lab}: '{k}' should be {t.__name__}")
        if sc.get("id") in ids:
            errs.append(f"{lab}: duplicate id")
        ids.add(sc.get("id"))
        ex = sc.get("exit") or {}
        for k, t in EXIT_REQUIRED.items():
            if k not in ex:
                errs.append(f"{lab}: exit missing '{k}'")
        if ex.get("tension") not in TENSION:
            errs.append(f"{lab}: exit.tension should be one of {sorted(TENSION)}")
        w = sc.get("words") or {}
        if not (isinstance(w.get("min"), int) and isinstance(w.get("max"), int) and 0 < w["min"] < w["max"]):
            errs.append(f"{lab}: words needs integer min < max")
        elif w["max"] > 1600:
            errs.append(f"{lab}: words.max {w['max']} exceeds 1600, the ceiling one drafting pass holds")
        if sc.get("pov") and sc.get("present") and sc["pov"] not in sc["present"]:
            errs.append(f"{lab}: pov character '{sc['pov']}' is not in present")
    return errs


def diff_states(a: dict, b: dict) -> dict:
    out = {"moved": [], "holding": [], "feels": [], "items": [], "resolved": [], "opened": [],
           "left": [], "arrived": []}
    ca, cb = a.get("characters", {}), b.get("characters", {})
    for n in sorted(set(ca) | set(cb)):
        if n not in cb:
            out["left"].append(n)
            continue
        if n not in ca:
            out["arrived"].append(n)
            continue
        if ca[n].get("position") != cb[n].get("position"):
            out["moved"].append(f"{n}: {ca[n].get('position')} -> {cb[n].get('position')}")
        if sorted(ca[n].get("holding", [])) != sorted(cb[n].get("holding", [])):
            out["holding"].append(f"{n}: {ca[n].get('holding')} -> {cb[n].get('holding')}")
        if ca[n].get("feels") != cb[n].get("feels"):
            out["feels"].append(f"{n}: {ca[n].get('feels')} -> {cb[n].get('feels')}")
    ia, ib = a.get("items", {}), b.get("items", {})
    for n in sorted(set(ia) | set(ib)):
        if ia.get(n) != ib.get(n):
            out["items"].append(f"{n}: {ia.get(n)} -> {ib.get(n)}")
    ta, tb = set(a.get("open_threads", [])), set(b.get("open_threads", []))
    out["resolved"] = sorted(ta - tb)
    out["opened"] = sorted(tb - ta)
    return out


def check_exit(beat: dict, state: dict) -> list[str]:
    errs = []
    ex = beat.get("exit", {})
    open_threads = set(state.get("open_threads", []))
    for th in ex.get("unresolved", []):
        if th not in open_threads:
            errs.append(f"premature resolution: beat says '{th}' stays unresolved, exit state "
                        "does not list it in open_threads")
    present = set(beat.get("present", []))
    chars = set(state.get("characters", {}))
    for n in present - chars:
        errs.append(f"character '{n}' is present in the beat but has no exit state")
    if state.get("scene") != beat.get("id"):
        errs.append(f"state.scene is {state.get('scene')!r}, beat id is {beat.get('id')!r}")
    li = (ex.get("last_image") or "").lower()
    lp = (state.get("last_paragraph") or "").lower()
    if li and lp:
        words = [w for w in li.replace(",", " ").split() if len(w) > 3]
        if words and not any(w in lp for w in words):
            errs.append("last_paragraph shares no word with beat.exit.last_image "
                        f"({ex.get('last_image')!r}); the scene may not end where the beat asked")
    return errs


def previous_state(beats, beat_id: str, state_dir: Path) -> Path | None:
    scenes = beats.get("scenes") if isinstance(beats, dict) else beats
    ids = [s.get("id") for s in scenes]
    if beat_id not in ids:
        raise SystemExit(f"beat {beat_id!r} not in beats")
    i = ids.index(beat_id)
    beat = scenes[i]
    if beat.get("follows"):
        cand = state_dir / f"{beat['follows']}.json"
        return cand if cand.exists() else None
    for j in range(i - 1, -1, -1):
        cand = state_dir / f"{ids[j]}.json"
        if cand.exists():
            return cand
    return None


SAMPLE_BEAT = {
    "id": "L1-hold-01", "title": "The beacon", "pov": "Bisk", "person": "third", "tense": "past",
    "location": "evac platform", "present": ["Bisk"], "time": "night", "goal": "hold the platform",
    "change": "the train leaves without her", "function": "dread settling into resolve",
    "exit": {"unresolved": ["the infected have not reached the platform"], "tension": "higher",
             "last_image": "first click from the dark"},
    "words": {"min": 400, "max": 900},
}
SAMPLE_STATE = {
    "scene": "L1-hold-01", "time": "night, after the last train", "location": "evac platform",
    "characters": {"Bisk": {"position": "back against the beacon post", "holding": [],
                            "wants": "to hold until dawn", "feels": "steady, cold",
                            "knows": ["the train is gone"]}},
    "items": {"beacon": {"where": "platform", "status": "lit"}},
    "open_threads": ["the infected have not reached the platform"],
    "promises": [],
    "last_paragraph": "The train went. She heard it before she felt it, then nothing but the beacon "
                      "and the tunnel and the first click from the dark.",
}


def self_test() -> int:
    ok = True
    ok &= _t("a well-formed state validates", validate_state(SAMPLE_STATE) == [])
    bad = json.loads(json.dumps(SAMPLE_STATE)); del bad["characters"]["Bisk"]["holding"]
    ok &= _t("a character without holding fails", any("holding" in e for e in validate_state(bad)))
    bad = json.loads(json.dumps(SAMPLE_STATE)); bad["open_threads"] = []
    ok &= _t("empty open_threads fails", any("open_threads" in e for e in validate_state(bad)))
    ok &= _t("a well-formed beat sheet validates", validate_beats({"scenes": [SAMPLE_BEAT]}) == [])
    bb = json.loads(json.dumps(SAMPLE_BEAT)); bb["words"]["max"] = 5000
    ok &= _t("a 5000-word beat fails the ceiling", any("1600" in e for e in validate_beats({"scenes": [bb]})))
    bb = json.loads(json.dumps(SAMPLE_BEAT)); bb["exit"]["tension"] = "resolved"
    ok &= _t("an unknown tension word fails", any("tension" in e for e in validate_beats({"scenes": [bb]})))
    ok &= _t("a matching exit passes check-exit", check_exit(SAMPLE_BEAT, SAMPLE_STATE) == [])
    st = json.loads(json.dumps(SAMPLE_STATE)); st["open_threads"] = ["a new thread"]
    ok &= _t("resolving a thread the beat kept open fails", any("premature" in e for e in check_exit(SAMPLE_BEAT, st)))
    st = json.loads(json.dumps(SAMPLE_STATE)); st["last_paragraph"] = "She smiled and slept well that night."
    ok &= _t("ending away from the beat's last image fails", any("last_image" in e for e in check_exit(SAMPLE_BEAT, st)))
    after = json.loads(json.dumps(SAMPLE_STATE)); after["characters"]["Bisk"]["position"] = "in the tunnel"
    after["open_threads"].append("who spoke from the speaker")
    d = diff_states(SAMPLE_STATE, after)
    ok &= _t("diff reports a move and an opened thread", d["moved"] and d["opened"] == ["who spoke from the speaker"])
    print(f"\n{'all' if ok else 'NOT all'} self-tests passed")
    return 0 if ok else 1


def _t(label: str, cond) -> bool:
    print(f"  {'pass' if cond else 'FAIL'}  {label}")
    return bool(cond)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", choices=["validate", "validate-beats", "diff", "check-exit", "previous"])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--beats", type=Path)
    ap.add_argument("--beat")
    ap.add_argument("--state", type=Path)
    ap.add_argument("--state-dir", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.command == "validate":
        errs = []
        for p in a.paths:
            errs += validate_state(_load(Path(p)), p)
        _report(errs, f"{len(a.paths)} state file(s) valid")
        return 1 if errs else 0
    if a.command == "validate-beats":
        errs = []
        for p in a.paths:
            errs += validate_beats(_load(Path(p)))
        _report(errs, "beat sheet valid")
        return 1 if errs else 0
    if a.command == "diff":
        if len(a.paths) != 2:
            ap.error("diff needs BEFORE.json AFTER.json")
        d = diff_states(_load(Path(a.paths[0])), _load(Path(a.paths[1])))
        for k, v in d.items():
            if v:
                print(f"{k}:")
                for line in v:
                    print(f"  {line}")
        return 0
    if a.command == "check-exit":
        if not (a.beats and a.beat and a.state):
            ap.error("check-exit needs --beats --beat --state")
        beats = _load(a.beats)
        scenes = beats.get("scenes") if isinstance(beats, dict) else beats
        beat = next((s for s in scenes if s.get("id") == a.beat), None)
        if not beat:
            raise SystemExit(f"beat {a.beat!r} not found")
        state = _load(a.state)
        errs = validate_state(state, str(a.state)) + check_exit(beat, state)
        _report(errs, f"exit state for {a.beat} matches its beat")
        return 1 if errs else 0
    if a.command == "previous":
        if not (a.beats and a.beat and a.state_dir):
            ap.error("previous needs --beats --beat --state-dir")
        p = previous_state(_load(a.beats), a.beat, a.state_dir)
        print(p if p else "")
        return 0
    ap.print_help()
    return 1


def _report(errs: list[str], ok_msg: str) -> None:
    if errs:
        for e in errs:
            print(f"  FAIL  {e}")
        print(f"{len(errs)} problem(s)")
    else:
        print(f"  ok    {ok_msg}")


if __name__ == "__main__":
    sys.exit(main())
