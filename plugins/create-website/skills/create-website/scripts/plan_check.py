#!/usr/bin/env python3
"""Check a website's plan before anything is built: site-plan.json.

    python3 plan_check.py site-plan.json          # exit 0 clean, 1 on any error
    python3 plan_check.py --example               # print a complete example plan

The plan is where the steps that instruction-only skills skip become checkable: the trawl run that
widened the idea space, a shipped reference for every section, a motion line for every section with
its reduced-motion behaviour, and the four questions a generated video hero has to settle before
the first billed clip. Each of those, left to prose, has a recorded history of being skipped or
answered after the money was spent (references/evidence.md).

ERROR fails the run. WARN is a prompt to read the line and decide.
"""
import json
import sys

EXAMPLE = {
    "site": {
        "subject": "A ceramics studio's site: classes, the shop, and the maker's story",
        "audience": "Locals booking a class on a phone; buyers browsing pieces",
        "visitorMode": "Persuade",
        "pages": ["home", "classes", "shop", "about"],
    },
    "trawl": {
        "tier": "--any",
        "packet": ".create-website/trawl-packet.md",
        "pick": "Kiln log: the page as a firing record, glaze tests as the grid",
        "took": ["glaze test tiles as the section rhythm"],
        "left": ["a named studio's hand-drawn wordmark style"],
    },
    "sections": [
        {
            "id": "hero",
            "job": "Say what the studio makes and get a visitor to book a class",
            "mobbin": {
                "query": "craft studio landing hero with booking button",
                "opened": 4,
                "gold": "web section 7f2c (pottery studio hero)",
                "took": ["one product photo bleeding off the right edge", "a single filled button"],
                "left": ["the reference's serif wordmark"],
            },
            "motion": {
                "entrance": "headline lines rise 12px and fade, 60ms stagger",
                "scroll": "none",
                "hover": "button lifts 2px",
                "signature": "a bowl turns on the wheel (video hero), plays once and holds",
                "reducedMotion": "resting frame shown as a still; text appears without movement",
            },
            "media": {"kind": "video"},
        },
        {
            "id": "classes",
            "job": "Show the three class types with times and prices",
            "mobbin": {"query": "class schedule cards with price and book button", "opened": 3,
                       "gold": "web section 1a9d", "took": ["price in the card corner"], "left": []},
            "motion": {"entrance": "cards fade in as the row enters", "scroll": "none", "hover": "none",
                       "signature": None, "reducedMotion": "cards present with no fade"},
            "media": {"kind": "image"},
        },
    ],
    "hero": {
        "kind": "video",
        "plainFallback": "the resting frame as a still image",
        "playback": "once",
        "settled": {
            "replacesOrBuilds": "replaces the current photo hero",
            "placementAndEdges": "right two-thirds of the hero; the wheel stays centred, nothing enters or leaves",
            "restingFrame": "the finished bowl, wheel stopped, at the clip's last frame",
            "beats": [
                {"what": "clay centred, wheel spinning", "seconds": 2.0},
                {"what": "hands draw the wall up", "seconds": 3.0},
                {"what": "hold on the finished bowl", "seconds": 1.5},
            ],
            "runtimeSeconds": 6.5,
        },
    },
    "effects": [
        {"name": "image grows slightly on hover", "previewedAs": "local page", "iterations": 1,
         "plainOffered": True}
    ],
    "spendLedger": ".create-website/spend.json",
}

SIGNATURE_LIMIT = 2


class Report:
    def __init__(self):
        self.errors, self.warns = [], []

    def error(self, msg):
        self.errors.append(f"ERROR {msg}")

    def warn(self, msg):
        self.warns.append(f"WARN  {msg}")


def _text(v):
    return isinstance(v, str) and v.strip() != ""


def check(plan):
    r = Report()
    site = plan.get("site") or {}
    if not _text(site.get("subject")):
        r.error("site.subject is missing: name the one concrete subject the site is about")
    if site.get("visitorMode") not in {"Persuade", "Operate", "Read", "Experience"}:
        r.error("site.visitorMode must be Persuade, Operate, Read or Experience")

    trawl = plan.get("trawl")
    if not isinstance(trawl, dict):
        r.error("no trawl block: run trawl:trawl for the site's world and record the pick, or record why it was skipped")
    elif _text(trawl.get("skipped")):
        r.warn(f"trawl skipped: {trawl['skipped']}")
    else:
        if trawl.get("tier") not in {"--any", "--standard"}:
            r.error("trawl.tier must be --any or --standard")
        if not _text(trawl.get("pick")):
            r.error("trawl.pick is missing: record which world was taken")
        if not isinstance(trawl.get("left"), list):
            r.error("trawl.left is missing: record what was declined, even if nothing")

    sections = plan.get("sections") or []
    if not sections:
        r.error("no sections: list every section with its job before building")
    golds, signatures = [], 0
    for i, s in enumerate(sections):
        sid = s.get("id") or f"#{i + 1}"
        if not _text(s.get("job")):
            r.error(f"section {sid}: no job. One sentence: what this section is for")
        m = s.get("mobbin")
        if not isinstance(m, dict):
            r.error(f"section {sid}: no mobbin block. Search for a shipped reference, or record why none applies")
        elif _text(m.get("none")):
            r.warn(f"section {sid}: no reference ({m['none']})")
        else:
            if not _text(m.get("query")) or not _text(m.get("gold")):
                r.error(f"section {sid}: mobbin needs the query and the gold you chose")
            if not isinstance(m.get("opened"), int) or m["opened"] < 1:
                r.error(f"section {sid}: mobbin.opened must count the results you actually looked at")
            if not m.get("took"):
                r.error(f"section {sid}: mobbin.took is empty. A reference you took nothing from was not used")
            golds.append((sid, m.get("gold")))
        mo = s.get("motion")
        if not isinstance(mo, dict):
            r.error(f"section {sid}: no motion block. Every section states its entrance, scroll and reduced-motion behaviour")
        else:
            for k in ("entrance", "reducedMotion"):
                if not _text(mo.get(k)):
                    r.error(f"section {sid}: motion.{k} is missing")
            if _text(mo.get("signature")):
                signatures += 1
    for (a, ga), (b, gb) in zip(golds, golds[1:]):
        if ga and ga == gb:
            r.warn(f"sections {a} and {b} share one reference: adjacent sections in one layout family read as repetition")
    if signatures > SIGNATURE_LIMIT:
        r.warn(f"{signatures} signature moments: more than {SIGNATURE_LIMIT} compete with each other. Keep the rest as quiet entrances")

    hero = plan.get("hero") or {}
    kind = hero.get("kind")
    if kind not in {"image", "video", "3d", "plain"}:
        r.error("hero.kind must be image, video, 3d or plain")
    if kind in {"video", "3d"} and not _text(hero.get("plainFallback")):
        r.error(f"hero.plainFallback is missing: a {kind} hero needs the still it shows under reduced motion, without WebGL, or when play() is refused")
    if kind == "3d":
        t = hero.get("threeD") or {}
        if t.get("source") not in {"three-scene", "generated-image", "mesh-generator", "css-depth"}:
            r.error("hero.threeD.source must be three-scene, generated-image, mesh-generator or css-depth: decide where the 3D comes from before building")
        if not _text(t.get("why")):
            r.error("hero.threeD.why is missing: say what a real-time scene shows that a still, CSS depth or scroll depth cannot")
        if t.get("source") == "mesh-generator" and not _text(t.get("tool")):
            r.error("hero.threeD.tool is missing: name the mesh generator the run actually found; none was connected when this skill was written")
    if kind == "video":
        if hero.get("playback") not in {"once", "loop"}:
            r.error("hero.playback must be once (play and hold on the resting frame) or loop")
        elif hero["playback"] == "loop":
            r.warn("a looping hero runs past five seconds: the page needs a visible pause control (WCAG 2.2.2, Level A)")
        st = hero.get("settled") or {}
        for k, label in (("replacesOrBuilds", "whether it replaces the current hero or builds on it"),
                         ("placementAndEdges", "where it sits and which edge things enter and leave by"),
                         ("restingFrame", "what the page shows when the clip ends")):
            if not _text(st.get(k)):
                r.error(f"hero.settled.{k} is missing: settle {label} before generating anything")
        beats, runtime = st.get("beats"), st.get("runtimeSeconds")
        if not beats or not isinstance(runtime, (int, float)):
            r.error("hero.settled needs beats (each with seconds) and runtimeSeconds")
        else:
            total = sum(float(b.get("seconds", 0)) for b in beats)
            if abs(total - float(runtime)) > 0.5:
                r.error(f"hero beats add up to {total:.1f}s against a runtime of {runtime}s: fit the length in the beats, never by speeding the clip")
            if not any("hold" in str(b.get("what", "")).lower() or "pause" in str(b.get("what", "")).lower() for b in beats):
                r.warn("no beat is a hold or a pause: a pause that is not in the prompt will not be in the clip")

    for e in plan.get("effects") or []:
        name = e.get("name", "an effect")
        if e.get("previewedAs") not in {"still", "recording", "local page"}:
            r.error(f"effect '{name}': previewedAs must be still, recording or local page. Show it cheaply before building it in")
        if isinstance(e.get("iterations"), int) and e["iterations"] > 2 and not e.get("plainOffered"):
            r.error(f"effect '{name}': {e['iterations']} iterations and the plain version not offered again. Offer it after two")
    return r


def main():
    if "--example" in sys.argv:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    r = check(plan)
    for line in r.errors + r.warns:
        print(line)
    print(f"RESULT: {len(r.errors)} error(s), {len(r.warns)} warning(s)")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
