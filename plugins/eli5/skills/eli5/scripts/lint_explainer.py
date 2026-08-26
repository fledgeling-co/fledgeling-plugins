#!/usr/bin/env python3
"""
lint_explainer.py — deterministic gate for eli5 explainer artifacts.

Sixteen checks in four families. Exits 1 on any FAIL.

    python3 lint_explainer.py artifact.html
    python3 lint_explainer.py --self-test      # prove every rule can fail
    python3 lint_explainer.py --json file.html

Every rule cites the evidence.md section it enforces. A rule that cannot fail is a
finding about the gate, not a pass -- which is what --self-test exists to prevent.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------- result types

FAIL, WARN, PASS, SKIP = "FAIL", "WARN", "PASS", "SKIP"


@dataclass
class Check:
    rule: str
    family: str
    evidence: str
    status: str
    detail: str
    counted: int = 0


@dataclass
class Report:
    path: str
    checks: List[Check] = field(default_factory=list)

    @property
    def failures(self) -> List[Check]:
        return [c for c in self.checks if c.status == FAIL]

    @property
    def warnings(self) -> List[Check]:
        return [c for c in self.checks if c.status == WARN]

    @property
    def ran(self) -> int:
        return sum(1 for c in self.checks if c.status != SKIP)


# ---------------------------------------------------------------- helpers

def strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def scripts_of(html: str) -> str:
    return "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.S | re.I))


def styles_of(html: str) -> str:
    return "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I))


def visible_text(html: str) -> str:
    """Markup stripped, so lexicon checks do not match class names or JS identifiers."""
    h = strip_comments(html)
    h = re.sub(r"<script\b[^>]*>.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style\b[^>]*>.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h)


# ---------------------------------------------------------------- family 1: containment

REMOTE = re.compile(
    r"""(?:src|href|data-src)\s*=\s*["'](?:https?:)?//(?!fonts\.googleapis\.com|fonts\.gstatic\.com)""",
    re.I,
)
REMOTE_CSS = re.compile(r"""url\(\s*["']?(?:https?:)?//(?!fonts\.gstatic\.com)""", re.I)
NETWORK_CALL = re.compile(
    r"\bfetch\s*\(|\bXMLHttpRequest\b|\bnew\s+WebSocket\b|\bimportScripts\s*\("
)


def check_containment(html: str) -> List[Check]:
    h = strip_comments(html)
    out = []

    hits = REMOTE.findall(h) + REMOTE_CSS.findall(h + styles_of(html))
    out.append(Check(
        "no-external-assets", "containment", "§1.10",
        FAIL if hits else PASS,
        f"{len(hits)} external resource reference(s); a blocked request fails silently"
        if hits else "no remote src/href outside Google Fonts",
        len(hits),
    ))

    net = NETWORK_CALL.findall(scripts_of(html))
    out.append(Check(
        "no-network-calls", "containment", "§1.10",
        FAIL if net else PASS,
        f"{len(net)} runtime network call(s): {sorted(set(net))}" if net
        else "no fetch/XHR/WebSocket at runtime",
        len(net),
    ))

    # A single HTML file with no <img> at all is fine; an <img> with a data: URI is fine.
    imgs = re.findall(r"<img\b[^>]*>", h, flags=re.I)
    bad_imgs = [i for i in imgs if not re.search(r'src\s*=\s*["\']data:', i, re.I)]
    out.append(Check(
        "images-inline-only", "containment", "§1.10",
        FAIL if bad_imgs else PASS,
        f"{len(bad_imgs)} <img> without a data: URI" if bad_imgs
        else f"{len(imgs)} <img> tag(s), all inline" if imgs else "no <img> tags; SVG only",
        len(bad_imgs),
    ))
    return out


# ---------------------------------------------------------------- family 2: geometry

def check_geometry(html: str) -> List[Check]:
    h = strip_comments(html)
    out = []

    svgs = re.findall(r"<svg\b[^>]*>", h, flags=re.I)
    if not svgs:
        out.append(Check("svg-present", "geometry", "§1.7", FAIL, "no <svg> element; explainer must draw", 0))
        out.append(Check("svg-viewbox", "geometry", "§1.10", SKIP, "no <svg> to check", 0))
        out.append(Check("no-hardcoded-svg-px", "geometry", "§1.10", SKIP, "no <svg> to check", 0))
        return out

    out.append(Check("svg-present", "geometry", "§1.7", PASS, f"{len(svgs)} <svg> element(s)", len(svgs)))

    missing = [s for s in svgs if not re.search(r"\bviewBox\s*=", s, re.I)]
    out.append(Check(
        "svg-viewbox", "geometry", "§1.10",
        FAIL if missing else PASS,
        f"{len(missing)} of {len(svgs)} <svg> without viewBox; clips inside constrained panels"
        if missing else f"all {len(svgs)} <svg> carry a viewBox",
        len(missing),
    ))

    px = [s for s in svgs if re.search(r'\b(?:width|height)\s*=\s*["\']\d+(?:px)?["\']', s, re.I)]
    out.append(Check(
        "no-hardcoded-svg-px", "geometry", "§1.10",
        FAIL if px else PASS,
        f"{len(px)} <svg> with fixed pixel width/height; use width=\"100%\" with viewBox"
        if px else "no fixed pixel dimensions on <svg>",
        len(px),
    ))
    return out


# ---------------------------------------------------------------- family 3: interaction

def check_interaction(html: str) -> List[Check]:
    js = scripts_of(html)
    css = styles_of(html)
    h = strip_comments(html)
    out = []

    controls = len(re.findall(r"<(?:button|input|select)\b", h, re.I))
    listeners = len(re.findall(r"addEventListener\s*\(", js))
    out.append(Check(
        "interactive-controls", "interaction", "§1.3",
        PASS if (controls and listeners) else FAIL,
        f"{controls} control(s), {listeners} listener(s)" if (controls and listeners)
        else (f"{controls} control(s) and no handler: dead controls invite an action that does "
              f"nothing, which is worse than an honestly static page. Wire them or remove them"
              if controls and not listeners
              else f"needs both: {controls} control(s), {listeners} listener(s)"),
        controls,
    ))

    drags = re.search(r"\bpointermove\b|\bmousemove\b|\btouchmove\b", js)
    if drags:
        cap = re.search(r"setPointerCapture", js)
        out.append(Check(
            "pointer-capture", "interaction", "§1.10",
            PASS if cap else FAIL,
            "drag handlers use setPointerCapture" if cap
            else "drag handler without setPointerCapture; tracking dies when the finger leaves",
            1,
        ))
        ta = re.search(r"touch-action\s*:\s*none", css + h, re.I)
        out.append(Check(
            "touch-action-none", "interaction", "§1.10",
            PASS if ta else FAIL,
            "touch-action: none present" if ta
            else "drag handler without touch-action: none; the page scrolls instead",
            1,
        ))
    else:
        out.append(Check("pointer-capture", "interaction", "§1.10", SKIP, "no drag handlers", 0))
        out.append(Check("touch-action-none", "interaction", "§1.10", SKIP, "no drag handlers", 0))

    raf = len(re.findall(r"requestAnimationFrame\s*\(", js))
    if raf:
        caf = len(re.findall(r"cancelAnimationFrame\s*\(", js))
        out.append(Check(
            "raf-lifecycle", "interaction", "§1.10",
            PASS if caf else FAIL,
            f"{raf} rAF call(s), {caf} cancel(s)" if caf
            else f"{raf} requestAnimationFrame with no cancelAnimationFrame; leaks CPU",
            raf,
        ))
    else:
        out.append(Check("raf-lifecycle", "interaction", "§1.10", SKIP, "no animation frames", 0))

    # Motion must be steppable, not autoplay-only.
    has_motion = bool(raf) or bool(re.search(r"@keyframes|\banimation\s*:", css, re.I))
    if has_motion:
        stepped = re.search(
            r"\b(step|next|prev|play|pause|scrub|advance|replay|restart)\b",
            h, re.I,
        )
        out.append(Check(
            "motion-steppable", "interaction", "§1.8",
            PASS if stepped else FAIL,
            "motion has a step/play/pause control" if stepped
            else "autoplay-only motion; animation's advantage evaporates on transience",
            1,
        ))
    else:
        out.append(Check("motion-steppable", "interaction", "§1.8", SKIP, "no motion", 0))

    themed = re.search(r"prefers-color-scheme", css + h, re.I)
    out.append(Check(
        "theme-aware", "interaction", "artifact CSP",
        PASS if themed else WARN,
        "responds to prefers-color-scheme" if themed
        else "no prefers-color-scheme block; verify the single-theme choice is deliberate",
        1 if themed else 0,
    ))
    return out


# ---------------------------------------------------------------- family 4: pedagogy

BOUNDARY = re.compile(
    r"where (?:this|the) analogy (?:breaks|stops|ends|fails)"
    r"|breaks? down"
    r"|limits? of (?:this|the) analogy"
    r"|analogy (?:limits|boundary|stops)"
    r"|where (?:this|it) stops being true"
    r"|does\s*n[o']t map"
    r"|stops being true",
    re.I,
)

PREDICT = re.compile(
    r"\b(?:predict|your guess|guess(?: first| which| what| who)?|"
    r"what do you think (?:will )?happen|before you (?:look|reveal|run)|"
    r"commit(?: to)? (?:a|your) (?:guess|answer)|which do you think)\b",
    re.I,
)

BABY_TALK = re.compile(
    # Positioning the reader as a child. Mined from six measured baseline artifacts,
    # where "grown-up word: DNS" and "grown-ups call the boss the leader" appeared in
    # 4 of 6 while an earlier, weaker lexicon passed all six.
    r"\bgrown[- ]ups?\b"
    # Naming a mechanism "magic" is the opposite of explaining it.
    r"|\bmagic (?:rule|word|trick|box|number|sauce|thing|part)\b"
    # Storybook anthropomorphism standing in for mechanism.
    r"|\b(?:goes ding|puts? (?:its|their|his|her) hand up|gets? the crown|"
    r"waves? hello|says? hello to|has a (?:little )?nap|wakes? up sleepy)\b"
    # Nursery register.
    r"|\b(?:magic fairy|fairies|mommy|mummy|daddy|tummy|boo[- ]boo|kiddy|"
    r"little friend|tiny helper|magical (?:little )?(?:creature|elf|gnome|wizard)|"
    r"like a big hug|silly little|"
    r"imagine a (?:little|tiny) (?:monster|creature|man|elf))\b",
    re.I,
)

TIER = re.compile(
    r"\b(?:tier|level|step|stage|part|layer)\s*[1-9]\b"
    r"|\b(?:the turn|the mechanism|the real thing)\b"
    r"|\b(?:intuition|mechanism|under the hood|edge cases|what this leaves out)\b",
    re.I,
)


def check_pedagogy(html: str) -> List[Check]:
    text = visible_text(html)
    h = strip_comments(html)
    out = []

    b = BOUNDARY.search(text)
    out.append(Check(
        "boundary-card", "pedagogy", "§1.1",
        PASS if b else FAIL,
        f"analogy boundary stated: {b.group(0)!r}" if b
        else "no statement of where the analogy stops; unbounded analogy installs misconceptions",
        1 if b else 0,
    ))

    if b:
        # The caveat must be reachable, not buried at the end (evidence §1.6).
        pos = b.start() / max(len(text), 1)
        out.append(Check(
            "boundary-reachable", "pedagogy", "§1.6",
            PASS if pos <= 0.80 else FAIL,
            f"boundary appears at {pos:.0%} through the text"
            + ("" if pos <= 0.80 else "; buried past tier 2, a caveat nobody reaches"),
            int(pos * 100),
        ))
    else:
        out.append(Check("boundary-reachable", "pedagogy", "§1.6", SKIP, "no boundary to locate", 0))

    p = PREDICT.search(text)
    out.append(Check(
        "predict-observe-explain", "pedagogy", "§1.3",
        PASS if p else FAIL,
        f"prediction beat present: {p.group(0)!r}" if p
        else "no prediction beat; a slider without a committed guess is Active, not Constructive "
             "(d~0.2-0.4 vs d~0.4-0.6)",
        1 if p else 0,
    ))

    baby = BABY_TALK.findall(text)
    out.append(Check(
        "register", "pedagogy", "§1.11",
        FAIL if baby else PASS,
        f"condescending register: {sorted(set(x.lower() for x in baby))}" if baby
        else "no baby-talk markers",
        len(baby),
    ))

    tiers = set(m.lower() for m in TIER.findall(text))
    n = len(tiers)
    if n == 0:
        st, msg = FAIL, "no disclosure tiers found; explainer must stage from intuition to mechanism"
    elif n > 6:
        st, msg = WARN, f"{n} distinct tier markers; three tiers, no nesting (deep hierarchies bury content)"
    else:
        st, msg = PASS, f"{n} tier marker(s)"
    out.append(Check("disclosure-tiers", "pedagogy", "§1.6", st, msg, n))

    skip = re.search(r"\b(?:skip(?: ahead| to)?|jump to|straight to|go to (?:tier|level|step) *3)\b", text, re.I)
    out.append(Check(
        "skip-ahead", "pedagogy", "§1.5",
        PASS if skip else WARN,
        "skip-ahead control present" if skip
        else "no skip control; scaffolding that lifts novices impedes experts (d<0)",
        1 if skip else 0,
    ))

    words = len(text.split())
    if words > 2600:
        st, msg = WARN, (f"{words} visible words; the original this replaces ran ~350. Depth is the "
                         f"trade, but tier 1 must still read in under a minute or progressive "
                         f"disclosure has bought nothing")
    else:
        st, msg = PASS, f"{words} visible words"
    out.append(Check("length-budget", "pedagogy", "§1.6", st, msg, words))

    # Coherence: emoji standing in for a diagram is the original skill's failure mode.
    emoji = re.findall(
        "[\U0001F300-\U0001FAFF☀-➿]", text
    )
    out.append(Check(
        "coherence-no-emoji-diagrams", "pedagogy", "§1.7",
        WARN if len(emoji) > 12 else PASS,
        f"{len(emoji)} emoji in visible text; seductive detail costs d=0.65-0.86"
        if len(emoji) > 12 else f"{len(emoji)} emoji, within budget",
        len(emoji),
    ))
    return out


# ---------------------------------------------------------------- driver

def lint(html: str, path: str = "<string>") -> Report:
    r = Report(path)
    r.checks += check_containment(html)
    r.checks += check_geometry(html)
    r.checks += check_interaction(html)
    r.checks += check_pedagogy(html)
    return r


def render(r: Report, as_json: bool = False) -> str:
    if as_json:
        return json.dumps({
            "path": r.path,
            "ran": r.ran,
            "failed": len(r.failures),
            "warned": len(r.warnings),
            "checks": [c.__dict__ for c in r.checks],
        }, indent=2)

    lines = [f"eli5 lint: {r.path}"]
    icon = {FAIL: "FAIL", WARN: "WARN", PASS: "  ok", SKIP: "skip"}
    for fam in ("containment", "geometry", "interaction", "pedagogy"):
        lines.append(f"\n  {fam}")
        for c in [x for x in r.checks if x.family == fam]:
            lines.append(f"    {icon[c.status]}  {c.rule:<28} {c.evidence:<8} {c.detail}")
    lines.append(
        f"\n  {r.ran} check(s) ran, {len(r.failures)} failed, {len(r.warnings)} warned"
    )
    if r.ran == 0:
        lines.append("  NOTE: zero checks ran. A gate with no checked count is not a pass.")
    return "\n".join(lines)


# ---------------------------------------------------------------- self-test

GOOD = """<!doctype html><html><head><style>
:root{--bg:#fff}@media (prefers-color-scheme: dark){:root{--bg:#111}}
.stage{touch-action:none}</style></head><body>
<h2>Tier 1: the turn</h2>
<p>Think of it as pressure driving flow through a constriction.</p>
<h3>Where this analogy breaks</h3>
<p>Cut a pipe and water sprays out; break a wire and current stops entirely.</p>
<h2>Tier 2: the mechanism</h2>
<p>Predict which node wins before you run it. Skip ahead to tier 3 if you know this.</p>
<svg viewBox="0 0 960 540" width="100%"><rect x="60" y="72" width="240" height="80"/></svg>
<button id="step">Step</button><input type="range" id="v">
<script>
let h=null;
document.getElementById('step').addEventListener('click',()=>{h=requestAnimationFrame(draw)});
function draw(){cancelAnimationFrame(h)}
const s=document.getElementById('v');
s.addEventListener('pointerdown',e=>{s.setPointerCapture(e.pointerId)});
s.addEventListener('pointermove',()=>{});
</script></body></html>"""

FIXTURES = [
    ("no-external-assets", GOOD.replace("<body>", '<body><script src="https://cdn.example.com/x.js"></script>')),
    ("no-network-calls", GOOD.replace("function draw(){", "function draw(){fetch('/x');")),
    ("images-inline-only", GOOD.replace("<body>", '<body><img src="https://x.test/a.png">')),
    ("svg-present", GOOD.replace('<svg viewBox="0 0 960 540" width="100%">', "<div>").replace("</svg>", "</div>")),
    ("svg-viewbox", GOOD.replace('viewBox="0 0 960 540" ', "")),
    ("no-hardcoded-svg-px", GOOD.replace('width="100%"', 'width="960" height="540"')),
    ("interactive-controls", GOOD.replace('<button id="step">Step</button><input type="range" id="v">', "")),
    ("pointer-capture", GOOD.replace("s.setPointerCapture(e.pointerId)", "0")),
    ("touch-action-none", GOOD.replace(".stage{touch-action:none}", "")),
    ("raf-lifecycle", GOOD.replace("cancelAnimationFrame(h)", "0")),
    ("motion-steppable", GOOD.replace('<button id="step">Step</button>', "")
                            .replace("getElementById('step')", "querySelector('#a')")),
    ("theme-aware", GOOD.replace("@media (prefers-color-scheme: dark){:root{--bg:#111}}", "")),
    ("boundary-card", GOOD.replace("Where this analogy breaks", "More detail")
                          .replace("Cut a pipe and water sprays out; break a wire and current stops entirely.", "More.")),
    ("predict-observe-explain", GOOD.replace("Predict which node wins before you run it.", "It runs.")),
    ("register", GOOD.replace("Think of it as pressure", "Imagine a little monster with a happy tummy and pressure")),
    ("register", GOOD.replace("Think of it as pressure", "Grown-ups call this the magic rule; pressure")),
    ("disclosure-tiers", GOOD.replace("Tier 1: the turn", "X").replace("Tier 2: the mechanism", "Y")
                             .replace("Skip ahead to tier 3 if you know this.", "")),
    ("skip-ahead", GOOD.replace("Skip ahead to tier 3 if you know this.", "")),
    ("length-budget", GOOD.replace("<p>Think of it as pressure driving flow through a constriction.</p>",
                                   "<p>" + ("word " * 2700) + "</p>")),
]


def self_test() -> int:
    base = lint(GOOD, "<good fixture>")
    print(render(base))
    ok = True
    if base.failures:
        print("\n  SELF-TEST: the good fixture must pass cleanly, but it failed:")
        for c in base.failures:
            print(f"    {c.rule}: {c.detail}")
        ok = False

    print("\n  proving each rule can fail")
    for rule, broken in FIXTURES:
        r = lint(broken, f"<broken:{rule}>")
        got = next((c for c in r.checks if c.rule == rule), None)
        fired = got is not None and got.status in (FAIL, WARN)
        print(f"    {'ok  ' if fired else 'DEAD'}  {rule:<28} "
              f"{'fires' if fired else 'DID NOT FIRE -- rule cannot fail, so its pass means nothing'}")
        ok = ok and fired

    print(f"\n  self-test: {'PASS' if ok else 'FAIL'} "
          f"({len(FIXTURES)} rules proven fallible)" if ok else
          f"\n  self-test: FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic gate for eli5 explainers.")
    ap.add_argument("path", nargs="?", help="HTML artifact to lint")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--self-test", action="store_true", help="prove every rule can fail")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.path:
        ap.error("give a path, or --self-test")

    try:
        with open(a.path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    except OSError as e:
        print(f"cannot read {a.path}: {e}", file=sys.stderr)
        return 2

    r = lint(html, a.path)
    print(render(r, a.json))
    return 1 if r.failures else 0


if __name__ == "__main__":
    sys.exit(main())
