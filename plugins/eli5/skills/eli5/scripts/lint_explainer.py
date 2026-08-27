#!/usr/bin/env python3
"""
lint_explainer.py -- deterministic gate for eli5 explainer artifacts.

Thirty-six checks in five families. Exits 1 on any FAIL.

    python3 lint_explainer.py artifact.html
    python3 lint_explainer.py --self-test      # prove every rule can fail
    python3 lint_explainer.py --json file.html

Every rule cites the evidence.md section it enforces. A rule that cannot fail is a finding
about the gate, not a pass -- which is what --self-test exists to prevent.

Four attributes are markers the gate reads, so staging and vendoring stay form-agnostic:

    data-pass="1|2|3"   the container for one depth pass
    data-boundary       the element stating where the analogy stops being true
    data-predict        the element asking the reader to commit a guess
    data-vendor="name"  an inlined library; excluded from containment and word counts
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import List

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

SCRIPT_TAG = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)


def strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def _split_scripts(html: str):
    """(author_js, vendor_js, vendor_attrs) -- vendor blocks carry data-vendor."""
    author, vendor, attrs = [], [], []
    for m in SCRIPT_TAG.finditer(html):
        if re.search(r"\bdata-vendor\b", m.group(1), re.I):
            vendor.append(m.group(2))
            attrs.append(m.group(1))
        else:
            author.append(m.group(2))
    return "\n".join(author), "\n".join(vendor), attrs


def author_js(html: str) -> str:
    return _split_scripts(html)[0]


def styles_of(html: str) -> str:
    return "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I))


def _strip_code(html: str) -> str:
    h = strip_comments(html)
    h = re.sub(r"<script\b[^>]*>.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style\b[^>]*>.*?</style>", " ", h, flags=re.S | re.I)
    return h


def visible_text(html: str) -> str:
    """Markup stripped, so lexicon checks do not match class names or JS identifiers."""
    h = re.sub(r"<[^>]+>", " ", _strip_code(html))
    return re.sub(r"\s+", " ", h)


# Anchors: things a reader can look at or touch. Prose is what sits between them.
ANCHOR = re.compile(
    r"<svg\b.*?</svg>|<canvas\b.*?</canvas>|<video\b.*?</video>"
    r"|<button\b.*?</button>|<select\b.*?</select>|<label\b[^>]*class=[\"']?rng.*?</label>"
    r"|<input\b[^>]*>|<img\b[^>]*>",
    re.S | re.I,
)


DEFN = re.compile(r"<dfn\b.*?</dfn>|<[a-z]+\b[^>]*\bdata-glossary\b.*?</[a-z]+>", re.S | re.I)


def _without_definitions(html: str) -> str:
    """Defining a term costs nothing against the budget, so the page defines rather than
    compresses. Compression is what turns a hard idea into an aphorism (evidence.md 4.7)."""
    return DEFN.sub(" ", html)


def prose_segments(html: str) -> List[str]:
    """Visible prose split at every visual or interactive element, in document order."""
    marked = ANCHOR.sub("\x00", _without_definitions(_strip_code(html)))
    marked = re.sub(r"<[^>]+>", " ", marked)
    return [re.sub(r"\s+", " ", s).strip() for s in marked.split("\x00")]


def prose_words(html: str) -> int:
    return sum(len(s.split()) for s in prose_segments(html))


# ---------------------------------------------------------------- family 1: containment

REMOTE = re.compile(
    r"""(?:src|href|data-src)\s*=\s*["'](?:https?:)?//(?!fonts\.googleapis\.com|fonts\.gstatic\.com)""",
    re.I,
)
REMOTE_CSS = re.compile(r"""url\(\s*["']?(?:https?:)?//(?!fonts\.gstatic\.com)""", re.I)
NETWORK_CALL = re.compile(r"\bfetch\s*\(|\bXMLHttpRequest\b|\bnew\s+WebSocket\b|\bimportScripts\s*\(")


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

    # Vendor blocks are excluded: three.js ships three fetch() calls in its loaders.
    net = NETWORK_CALL.findall(author_js(html))
    out.append(Check(
        "no-network-calls", "containment", "§1.10",
        FAIL if net else PASS,
        f"{len(net)} runtime network call(s) in author code: {sorted(set(net))}" if net
        else "no fetch/XHR/WebSocket in author code",
        len(net),
    ))

    imgs = re.findall(r"<img\b[^>]*>", h, flags=re.I)
    bad_imgs = [i for i in imgs if not re.search(r'src\s*=\s*["\']data:', i, re.I)]
    out.append(Check(
        "images-inline-only", "containment", "§1.10",
        FAIL if bad_imgs else PASS,
        f"{len(bad_imgs)} <img> without a data: URI" if bad_imgs
        else f"{len(imgs)} <img> tag(s), all inline" if imgs else "no <img> tags",
        len(bad_imgs),
    ))

    vids = re.findall(r"<video\b[^>]*>", h, flags=re.I)
    if vids:
        # A rendered clip is embedded, never linked, and the reader holds its timeline.
        # Autoplay is the transience failure evidence.md 1.8 names, with extra bandwidth.
        linked = [v for v in vids if not re.search(r'src\s*=\s*["\']data:', v, re.I)
                  and not re.search(r"<source\b", h, re.I)]
        uncontrolled = [v for v in vids if not re.search(r"\bcontrols\b", v, re.I)]
        autoplaying = [v for v in vids if re.search(r"\bautoplay\b", v, re.I)]
        problems = []
        if linked:
            problems.append(f"{len(linked)} not inlined as a data: URI")
        if uncontrolled:
            problems.append(f"{len(uncontrolled)} without controls, so the reader cannot scrub it")
        if autoplaying:
            problems.append(f"{len(autoplaying)} autoplaying")
        out.append(Check(
            "video-inline-and-scrubbable", "containment", "§1.8",
            FAIL if problems else PASS,
            "; ".join(problems) if problems
            else f"{len(vids)} clip(s), inlined, scrubbable, no autoplay",
            len(vids),
        ))
    else:
        out.append(Check("video-inline-and-scrubbable", "containment", "§1.8", SKIP, "no <video>", 0))

    _, vendor_src, vendor_attrs = _split_scripts(h)
    uses_lib = re.search(r"\bTHREE\s*\.|\bgsap\s*\.|\bScrollTrigger\b", author_js(h) + vendor_src)
    linked = [a for a in vendor_attrs if re.search(r"\bsrc\s*=", a, re.I)]
    if uses_lib or vendor_attrs:
        if linked:
            st, msg = FAIL, f"{len(linked)} data-vendor block(s) with a src attribute; inline the file instead"
        elif uses_lib and not vendor_attrs:
            st, msg = FAIL, ("author code calls THREE/gsap with no data-vendor block; a CDN "
                             "script fails silently and the page renders without its 3D or motion")
        else:
            st, msg = PASS, f"{len(vendor_attrs)} inlined vendor block(s), none linked"
        out.append(Check("vendor-inlined", "containment", "§1.10", st, msg, len(vendor_attrs)))
    else:
        out.append(Check("vendor-inlined", "containment", "§1.10", SKIP, "no library in use", 0))
    return out


# ---------------------------------------------------------------- family 2: geometry

def check_geometry(html: str) -> List[Check]:
    h = strip_comments(html)
    out = []

    svg_blocks = re.findall(r"<svg\b[^>]*>(.*?)</svg>", h, flags=re.S | re.I)
    svgs = [s for s in re.findall(r"<svg\b[^>]*>", h, flags=re.I)]
    drawn = [b for b in svg_blocks if re.search(r"<(?:rect|circle|path|line|polygon|polyline|text|g|ellipse|use)\b", b, re.I)]
    canvases = re.findall(r"<canvas\b[^>]*>", h, flags=re.I)
    data_imgs = re.findall(r'<img\b[^>]*src\s*=\s*["\']data:', h, flags=re.I)
    videos = re.findall(r"<video\b[^>]*>", h, flags=re.I)
    scenes = len(drawn) + len(canvases) + len(data_imgs) + len(videos)

    out.append(Check(
        "visual-scenes", "geometry", "§1.7",
        PASS if scenes >= 3 else FAIL,
        f"{scenes} visual scene(s): {len(drawn)} drawn svg, {len(canvases)} canvas, "
        f"{len(data_imgs)} inline image, {len(videos)} clip"
        + ("" if scenes >= 3 else "; an explainer with fewer than 3 is a document with a picture in it"),
        scenes,
    ))

    if not svgs:
        out.append(Check("svg-viewbox", "geometry", "§1.10", SKIP, "no <svg> to check", 0))
        out.append(Check("no-hardcoded-svg-px", "geometry", "§1.10", SKIP, "no <svg> to check", 0))
    else:
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
            f'{len(px)} <svg> with fixed pixel width/height; use width="100%" with viewBox'
            if px else "no fixed pixel dimensions on <svg>",
            len(px),
        ))

    # Reach. Four artifacts in a row drew with SVG and CSS alone and passed everything,
    # because every library rule was written as a bar to clear rather than a default.
    # An explainer may still be SVG-only; it has to say so on purpose.
    surfaces = []
    if re.search(r"<canvas\b", h, re.I):
        surfaces.append("canvas")
    if re.search(r"\bTHREE\s*\.", h):
        surfaces.append("three.js")
    if re.search(r"\bgsap\s*\.|\bScrollTrigger\b", h):
        surfaces.append("gsap")
    if re.search(r"<video\b", h, re.I):
        surfaces.append("clip")
    if re.search(r'<img\b[^>]*src\s*=\s*["\']data:', h, re.I):
        surfaces.append("image")
    declared = re.search(r"<!--\s*surface\s*:", html, re.I)
    if surfaces:
        st, msg = PASS, f"draws with {', '.join(surfaces)} beyond SVG and CSS"
    elif declared:
        st, msg = PASS, "SVG and CSS only, declared deliberately in a `surface:` comment"
    else:
        st, msg = FAIL, ("SVG and CSS only. Reach for the surface the mechanism wants -- canvas "
                         "past ~500 elements, three.js where a flat view loses the invariant or "
                         "for a second lens, gsap to orchestrate a state change, a clip for what "
                         "cannot be computed live. To keep it SVG-only, say why in a "
                         "`<!-- surface: ... -->` comment")
    out.append(Check("surface-reach", "geometry", "§1.2 / §1.7", st, msg, len(surfaces)))

    if canvases:
        unlabelled = [c for c in canvases if not re.search(r"\baria-label(?:ledby)?\s*=", c, re.I)]
        out.append(Check(
            "canvas-labelled", "geometry", "a11y floor",
            FAIL if unlabelled else PASS,
            f"{len(unlabelled)} <canvas> with no aria-label; its content is invisible to "
            "assistive technology" if unlabelled else f"all {len(canvases)} <canvas> labelled",
            len(unlabelled),
        ))
    else:
        out.append(Check("canvas-labelled", "geometry", "a11y floor", SKIP, "no <canvas>", 0))
    return out


# ---------------------------------------------------------------- family 3: interaction

# `animation: none` in a prefers-reduced-motion reset is the absence of motion, not motion.
MOTION_DECL = re.compile(r"@keyframes|\b(?:animation|transition)\s*:\s*(?!none\b)", re.I)


def interaction_kinds(html: str) -> List[str]:
    h = strip_comments(html)
    js = author_js(h)
    kinds = []
    if re.search(r'<input\b[^>]*type\s*=\s*["\']range', h, re.I):
        kinds.append("slider")
    if re.search(r"\bpointermove\b|\bmousemove\b|\btouchmove\b", js):
        kinds.append("drag")
    if len(re.findall(r"<button\b", h, re.I)) >= 2 and re.search(r"['\"]click['\"]", js):
        kinds.append("step")
    if re.search(r'<select\b|<input\b[^>]*type\s*=\s*["\'](?:checkbox|radio)', h, re.I):
        kinds.append("pick")
    if re.search(r"\bScrollTrigger\b|['\"]scroll['\"]|\bIntersectionObserver\b|\bwheel\b", js):
        kinds.append("scroll")
    if re.search(r"OrbitControls|\bTHREE\s*\.", js + _split_scripts(h)[1]):
        kinds.append("orbit")
    if re.search(r"['\"]key(?:down|up|press)['\"]", js):
        kinds.append("keyboard")
    return kinds


def check_interaction(html: str) -> List[Check]:
    h = strip_comments(html)
    js = author_js(h)
    css = styles_of(html)
    out = []

    controls = len(re.findall(r"<(?:button|input|select)\b", h, re.I))
    listeners = len(re.findall(r"addEventListener\s*\(", js))
    if controls and not listeners:
        st, msg = FAIL, (f"{controls} control(s) and no handler in author code: dead controls invite "
                         f"an action that does nothing, which is worse than an honestly static page")
    elif controls < 3 or not listeners:
        st, msg = FAIL, f"{controls} control(s), {listeners} listener(s); an explainer is operated, so 3 wired controls is the floor"
    else:
        st, msg = PASS, f"{controls} control(s), {listeners} listener(s)"
    out.append(Check("interactive-controls", "interaction", "§1.3", st, msg, controls))

    kinds = interaction_kinds(h)
    out.append(Check(
        "interaction-variety", "interaction", "§1.3",
        PASS if len(kinds) >= 2 else FAIL,
        f"{len(kinds)} interaction kind(s): {kinds}"
        + ("" if len(kinds) >= 2 else "; one mode of interaction across a whole page reads as one widget"),
        len(kinds),
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
            f"{raf} rAF call(s), {caf} cancel(s) in author code" if caf
            else f"{raf} requestAnimationFrame with no cancelAnimationFrame; leaks CPU",
            raf,
        ))
    else:
        out.append(Check("raf-lifecycle", "interaction", "§1.10", SKIP, "no animation frames in author code", 0))

    has_motion = bool(raf) or bool(MOTION_DECL.search(css)) \
        or bool(re.search(r"\bgsap\s*\.|\bScrollTrigger\b", js))
    if has_motion:
        # Read the controls, not the prose: "each step moves one packet" in a paragraph is
        # not a step control, and searching the whole page let that pass.
        controls_markup = " ".join(
            re.findall(r"<button\b[^>]*>.*?</button>|<input\b[^>]*>|<select\b[^>]*>.*?</select>",
                       h, flags=re.S | re.I)
        )
        # Scroll position is the reader's clock, so ScrollTrigger paces motion without a play button.
        stepped = re.search(r"\b(step|next|prev|play|pause|scrub|advance|replay|restart)\b",
                            controls_markup, re.I) \
            or re.search(r"\bScrollTrigger\b", js)
        out.append(Check(
            "motion-steppable", "interaction", "§1.8",
            PASS if stepped else FAIL,
            "motion is reader-paced (control or scroll position)" if stepped
            else "autoplay-only motion; animation's advantage evaporates on transience",
            1,
        ))
        reduced = re.search(r"prefers-reduced-motion", css + h + js, re.I)
        out.append(Check(
            "reduced-motion", "interaction", "a11y floor",
            PASS if reduced else FAIL,
            "prefers-reduced-motion path present" if reduced
            else "motion with no prefers-reduced-motion path; land each state statically and keep the controls",
            1,
        ))
    else:
        out.append(Check("motion-steppable", "interaction", "§1.8", SKIP, "no motion", 0))
        out.append(Check("reduced-motion", "interaction", "a11y floor", SKIP, "no motion", 0))

    # Signalling costs g = 0.46-0.53 when a state change goes unmarked (evidence.md 1.7).
    # Three artifacts shipped 4 static SVGs, 12 controls and no motion of any kind.
    if controls >= 3 and listeners:
        marked = bool(MOTION_DECL.search(css)) \
            or bool(re.search(r"\bgsap\s*\.|requestAnimationFrame\s*\(", js))
        out.append(Check(
            "state-change-signalled", "interaction", "§1.7",
            PASS if marked else WARN,
            "state changes carry a transition, animation or frame loop" if marked
            else f"{controls} controls change state with nothing marking the change; "
                 f"an unsignalled transition costs g=0.46-0.53",
            1 if marked else 0,
        ))
    else:
        out.append(Check("state-change-signalled", "interaction", "§1.7", SKIP, "no wired controls", 0))

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
    r"|stops (?:being true|carrying weight)",
    re.I,
)

PREDICT = re.compile(
    r"\b(?:predict|your guess|guess(?: first| which| what| who)?|"
    r"what do you think (?:will )?happen|before you (?:look|reveal|run)|"
    r"commit(?: to)? (?:a|your) (?:guess|answer)|which do you think)\b",
    re.I,
)

BABY_TALK = re.compile(
    r"\bgrown[- ]ups?\b"
    r"|\bmagic (?:rule|word|trick|box|number|sauce|thing|part)\b"
    r"|\b(?:goes ding|puts? (?:its|their|his|her) hand up|gets? the crown|"
    r"waves? hello|says? hello to|has a (?:little )?nap|wakes? up sleepy)\b"
    r"|\b(?:magic fairy|fairies|mommy|mummy|daddy|tummy|boo[- ]boo|kiddy|"
    r"little friend|tiny helper|magical (?:little )?(?:creature|elf|gnome|wizard)|"
    r"like a big hug|silly little|"
    r"imagine a (?:little|tiny) (?:monster|creature|man|elf))\b",
    re.I,
)

# Phrases lifted verbatim from the first version's worked examples. All three sample
# artifacts reproduced them word for word, which is what a shared template looks like.
BOILERPLATE = [
    "the bridge, and the row it is for",
    "where this analogy breaks",
    "the second lens",
    "commit to a guess before the reveal",
    "skip ahead to tier",
    "tier 1",
    "tier 2",
    "tier 3",
    "the turn",
    "the real thing",
    "what this leaves out",
    "what it leaves out",
]



DFN = re.compile(r"<dfn\b([^>]*)>(.*?)</dfn>", re.S | re.I)


def check_defined_terms(html: str, text: str) -> Check:
    """The failure the baby-talk rule cannot see: a page pitched so far from a five-year-old
    that nobody outside the project can read it. One recorded artifact passed every other
    check at 200 words while using cards, rung, class, oracle, assay, charter, denominator,
    closures and escapes, none of them defined (evidence.md 4.7).

    Readability metrics do not separate the two cases -- measured, that artifact and a
    readable one both ran a mean sentence of 8 words and about 60% short sentences. What
    separates them is whether the page defines its own vocabulary, so that is what is checked.
    """
    body = _strip_code(html)
    found = list(DFN.finditer(body))
    if not found:
        return Check(
            "defines-its-terms", "pedagogy", "§1.11", FAIL,
            "no <dfn> in the page. Mark each term specific to this topic where it is first "
            "used and define it there; definitions are free against the prose budget",
            0,
        )

    used_early = []
    for m in found:
        attr, inner = m.group(1), m.group(2)
        term = re.search(r'data-term\s*=\s*["\']([^"\']+)', attr)
        term = term.group(1) if term else re.sub(r"<[^>]+>", "", inner)
        term = re.split(r"[:\u2014\u2013,.]", term.strip())[0].strip()
        if len(term) < 3:
            continue
        before = re.sub(r"<[^>]+>", " ", body[: m.start()])
        if re.search(r"\b" + re.escape(term) + r"\b", before, re.I):
            used_early.append(term)

    n = len(found)
    if used_early:
        return Check(
            "defines-its-terms", "pedagogy", "§1.11", FAIL,
            f"{len(used_early)} term(s) used before being defined: {sorted(set(used_early))}; "
            f"define at first use, not after the reader has already met the word",
            n,
        )
    if n < 3:
        return Check(
            "defines-its-terms", "pedagogy", "§1.11", WARN,
            f"{n} defined term(s); most hard topics carry at least 3 words the reader does not "
            f"already own, and an undefined one is where the page stops being readable",
            n,
        )
    return Check("defines-its-terms", "pedagogy", "§1.11", PASS, f"{n} term(s) defined at first use", n)



# Slogan shapes, from agent-voice's ai-writing-signs.md 1.7 ("the epigram used in place of
# a plain statement") and 2.3 (negative parallelism). Run over ALL visible text including
# <svg> labels: exempting diagram text from the WORD BUDGET must not exempt it from the
# register, and one measured artifact kept its densest slogans there where nothing looked.
SLOGAN = {
    "appositive contrast": re.compile(r"\b[a-z]{4,}, not (?:a |an |the )?[a-z]{3,}", re.I),
    "not-just parallel": re.compile(
        r"(?i)\b(?:it'?s not just|isn'?t just|not only .{3,60} but also|not (?:the|a|an) \w+, but)"),
    "abstract copula": re.compile(
        r"(?i)\b\w+ (?:is|are) (?:a |an )?(?:different|one-way|external|another|the same)\b"),
}


def check_plain_statements(html: str) -> Check:
    """An epigram states a conclusion and shows no mechanism. One per page is a flourish; a
    page of them explains nothing, and it is what a word budget produces when it meets a hard
    idea. Measured over two artifacts of comparable length: 5 distinct shapes in the one a
    reader called cryptic, 1 in the one they did not (evidence.md 4.8, n=2)."""
    text = re.sub(r"<[^>]+>", " ", DEFN.sub(" ", _strip_code(html)))
    text = re.sub(r"\s+", " ", text)
    hits = sorted({m.group(0).strip() for pat in SLOGAN.values() for m in pat.finditer(text)})
    n = len(hits)
    if n >= 4:
        st, msg = FAIL, (f"{n} slogan-shaped lines: {hits}. Each states a conclusion and shows no "
                         f"mechanism; say what happens instead")
    elif n >= 2:
        st, msg = WARN, f"{n} slogan-shaped lines: {hits}; roughly one landing line per page"
    else:
        st, msg = PASS, f"{n} slogan-shaped line(s)"
    return Check("plain-statements", "pedagogy", "ai-signs 1.7", st, msg, n)



# Placeholder nouns. "Something runs, looks at what came back, and reports" names nothing a
# reader can hold, and it was the opening sentence of a shipped artifact.
VAGUE_NOUN = re.compile(
    r"\b(?:something|someone|somebody|anything|stuff|a thing|the thing|things|"
    r"what came back|some kind of|one of those|any one of those)\b", re.I)

# Words too common to tell you what a page is about.
TITLE_STOP = set(
    "the a an and or of to in on it its this that these those is are was were be been for "
    "with from at by as if then than so but not no you your we our they them their there "
    "here what which who how when why all any some each every one two three four five more "
    "most other another same still says say said do does did make makes made use used using "
    "get gets got see look looks still".split())


def check_names_things(html: str) -> List[Check]:
    body = _strip_code(html)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", _without_definitions(body)))
    out = []

    hits = sorted({m.group(0).lower() for m in VAGUE_NOUN.finditer(text)})
    if len(hits) >= 4:
        st, msg = FAIL, (f"{len(hits)} placeholder nouns: {hits}. Name the thing -- a reader cannot "
                         f"hold \"something\" or \"what came back\"")
    elif len(hits) >= 2:
        st, msg = WARN, f"{len(hits)} placeholder nouns: {hits}"
    else:
        st, msg = PASS, f"{len(hits)} placeholder noun(s)"
    out.append(Check("names-things", "pedagogy", "ai-signs 1.7", st, msg, len(hits)))

    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", body, re.S | re.I)
    if not m:
        out.append(Check("title-names-its-subject", "pedagogy", "ai-signs 1.7", SKIP, "no <h1>", 0))
        return out
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    whole = visible_text(html).lower()
    anchored = [w for w in re.findall(r"[a-z']{4,}", title.lower())
                if w not in TITLE_STOP
                and len(re.findall(r"\b" + re.escape(w) + r"\w*", whole)) >= 3]
    out.append(Check(
        "title-names-its-subject", "pedagogy", "ai-signs 1.7",
        PASS if anchored else FAIL,
        f"title anchored by {anchored}" if anchored else
        f"title {title!r} names nothing the page goes on to discuss; a heading whose subject is a "
        f"bare pronoun is a riddle the body has to decode",
        len(anchored),
    ))
    return out


def check_pedagogy(html: str) -> List[Check]:
    text = visible_text(html)
    h = strip_comments(html)
    out = []

    b = BOUNDARY.search(text)
    marked = re.search(r"\bdata-boundary\b", h, re.I)
    out.append(Check(
        "boundary-card", "pedagogy", "§1.1",
        PASS if (b or marked) else FAIL,
        (f"analogy boundary stated: {b.group(0)!r}" if b else "boundary marked with data-boundary")
        if (b or marked) else
        "no statement of where the analogy stops; unbounded analogy installs misconceptions",
        1 if (b or marked) else 0,
    ))

    if b or marked:
        # Measure against markup with scripts and styles removed: a 690 KB inlined
        # library in the denominator puts every position at 1% and the rule stops firing.
        body = _strip_code(html)
        pos = (b.start() / max(len(text), 1)) if b else \
            (body.lower().find("data-boundary") / max(len(body), 1))
        out.append(Check(
            "boundary-reachable", "pedagogy", "§1.6",
            PASS if pos <= 0.80 else FAIL,
            f"boundary appears at {pos:.0%} through the artifact"
            + ("" if pos <= 0.80 else "; buried at the end, a caveat nobody reaches"),
            int(pos * 100),
        ))
    else:
        out.append(Check("boundary-reachable", "pedagogy", "§1.6", SKIP, "no boundary to locate", 0))

    p = PREDICT.search(text) or re.search(r"\bdata-predict\b", h, re.I)
    out.append(Check(
        "predict-observe-explain", "pedagogy", "§1.3",
        PASS if p else FAIL,
        "prediction beat present" if p
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

    out.append(check_defined_terms(html, text))
    out.append(check_plain_statements(html))
    out += check_names_things(html)

    passes = set(re.findall(r'data-pass\s*=\s*["\']?([1-9])', h, re.I))
    n = len(passes)
    if n >= 3:
        st, msg = PASS, f"{n} depth passes marked: {sorted(passes)}"
    elif n:
        st, msg = FAIL, (f"{n} depth pass(es) marked; three passes stage intuition -> mechanism -> "
                         f"the real thing, and the form decides how they are presented")
    else:
        st, msg = FAIL, ('no data-pass="1|2|3" markers; mark each depth pass on its container so '
                         "staging is checkable whatever the form")
    out.append(Check("disclosure-tiers", "pedagogy", "§1.6", st, msg, n))

    skip = re.search(r"\b(?:skip(?: ahead| to| the)?|jump to|straight to|go (?:to|straight))\b", text, re.I) \
        or re.search(r"\bdata-skip\b", h, re.I)
    out.append(Check(
        "skip-ahead", "pedagogy", "§1.5",
        PASS if skip else WARN,
        "route past the first pass present" if skip
        else "no skip control; scaffolding that lifts novices impedes experts (d<0)",
        1 if skip else 0,
    ))

    emoji = re.findall("[\U0001F300-\U0001FAFF☀-➿]", text)
    out.append(Check(
        "coherence-no-emoji-diagrams", "pedagogy", "§1.7",
        WARN if len(emoji) > 12 else PASS,
        f"{len(emoji)} emoji in visible text; seductive detail costs d=0.65-0.86"
        if len(emoji) > 12 else f"{len(emoji)} emoji, within budget",
        len(emoji),
    ))
    return out


# ---------------------------------------------------------------- family 5: composition

BLOCK = re.compile(r"<(p|li|h1|h2|h3|h4|figcaption|blockquote)\b[^>]*>(.*?)</\1>", re.S | re.I)


def prose_blocks(html: str) -> List[int]:
    """Word count of each visible text block, largest last."""
    body = _without_definitions(_strip_code(html))
    counts = []
    for _, inner in BLOCK.findall(body):
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", inner)).strip()
        if txt:
            counts.append(len(txt.split()))
    return sorted(counts)


def check_composition(html: str) -> List[Check]:
    h = strip_comments(html)
    segs = prose_segments(html)
    words = sum(len(s.split()) for s in segs)
    out = []

    if words > 350:
        st, msg = FAIL, (f"{words} words of prose outside the diagrams; the budget is 350. Words "
                         f"inside <svg> cost nothing and satisfy spatial contiguity, so move a "
                         f"sentence of explanation onto the thing it explains")
    elif words > 300:
        # 300 rather than 250: plain language measurably costs more words than the compressed
        # register it replaces, and this should warn on padding rather than on clarity.
        st, msg = WARN, f"{words} words of prose; under 300 keeps the artifact something you operate"
    else:
        st, msg = PASS, f"{words} words of prose outside the diagrams"
    out.append(Check("prose-budget", "composition", "§1.6", st, msg, words))

    # Total can be inside budget while one wall of text still reads as a document. Measured
    # on a page that passed at 367 words: the three blocks a reader called wordy ran 73, 48
    # and 38, against captions of 14-22 that nobody objected to.
    blocks = prose_blocks(html)
    biggest = blocks[-1] if blocks else 0
    if biggest > 50:
        st, msg = FAIL, (f"longest text block is {biggest} words; the budget is 50. Split it, cut it, "
                         f"or annotate the diagram with it")
    elif biggest > 35:
        st, msg = WARN, f"longest text block is {biggest} words; under 35 reads as a caption rather than a passage"
    else:
        st, msg = PASS, f"longest text block is {biggest} words"
    out.append(Check("prose-block", "composition", "§1.7", st, msg, biggest))

    runs = [len(s.split()) for s in segs]
    longest = max(runs) if runs else 0
    if longest > 120:
        st, msg = FAIL, (f"longest unbroken prose run is {longest} words; the budget is 120 between "
                         f"one thing to look at or touch and the next")
    elif longest > 80:
        st, msg = WARN, f"longest unbroken prose run is {longest} words; under 80 keeps the page operable"
    else:
        st, msg = PASS, f"longest unbroken prose run is {longest} words"
    out.append(Check("prose-run", "composition", "§1.7", st, msg, longest))

    opening = runs[0] if runs else 0
    if opening > 90:
        st, msg = FAIL, f"{opening} words before the reader can look at or touch anything; the budget is 90"
    elif opening > 60:
        st, msg = WARN, f"{opening} words of opening prose; the first pass lands faster under 60"
    else:
        st, msg = PASS, f"{opening} words before the first visual or control"
    out.append(Check("opening-budget", "composition", "§1.6", st, msg, opening))

    text = visible_text(html).lower()
    hits = sorted({p for p in BOILERPLATE if p in text})
    if len(hits) >= 3:
        st, msg = FAIL, (f"{len(hits)} phrases copied from the skill's worked examples: {hits}. "
                         f"Headings come from the topic's own vocabulary")
    elif len(hits) == 2:
        st, msg = WARN, f"2 template phrases: {hits}"
    else:
        st, msg = PASS, f"{len(hits)} template phrase(s)"
    out.append(Check("no-template-boilerplate", "composition", "forms.md", st, msg, len(hits)))

    drawn = len(re.findall(r"<svg\b[^>]*>(?=.*?<(?:rect|circle|path|line|polygon|polyline|text|g|ellipse|use)\b)", h, re.S | re.I))
    scenes = drawn + len(re.findall(r"<canvas\b", h, re.I)) + len(re.findall(r'<img\b[^>]*src\s*=\s*["\']data:', h, re.I))
    density = words // max(scenes, 1)
    out.append(Check(
        "visual-density", "composition", "§1.7",
        WARN if density > 110 else PASS,
        f"{density} words of prose per visual scene"
        + ("; past 110 the diagrams are illustrating an essay rather than carrying it" if density > 110 else ""),
        density,
    ))
    return out


# ---------------------------------------------------------------- driver

def lint(html: str, path: str = "<string>") -> Report:
    r = Report(path)
    r.checks += check_containment(html)
    r.checks += check_geometry(html)
    r.checks += check_interaction(html)
    r.checks += check_pedagogy(html)
    r.checks += check_composition(html)
    return r


FAMILIES = ("containment", "geometry", "interaction", "pedagogy", "composition")


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
    for fam in FAMILIES:
        lines.append(f"\n  {fam}")
        for c in [x for x in r.checks if x.family == fam]:
            lines.append(f"    {icon[c.status]}  {c.rule:<28} {c.evidence:<12} {c.detail}")
    lines.append(f"\n  {r.ran} check(s) ran, {len(r.failures)} failed, {len(r.warnings)} warned")
    if r.ran == 0:
        lines.append("  NOTE: zero checks ran. A gate with no checked count is not a pass.")
    return "\n".join(lines)


# ---------------------------------------------------------------- self-test

GOOD = """<!doctype html><html><head><style>
:root{--bg:#fff}@media (prefers-color-scheme: dark){:root{--bg:#111}}
@media (prefers-reduced-motion: reduce){*{animation:none}}
.stage{touch-action:none}
.pulse{animation:p .3s}
</style></head><body>
<section data-pass="1">
<p><dfn>Constriction</dfn>: the narrow part of the pipe. <dfn>Head</dfn>: how hard the water is pushed. <dfn>Rate</dfn>: how much passes a point each second. Pressure drives flow through a constriction.</p>
<svg viewBox="0 0 960 540" width="100%"><rect x="60" y="72" width="240" height="80"/><text x="180" y="120">inlet</text></svg>
<p data-predict>Guess which node wins before you run it.</p>
<button id="step">Step</button><button id="back">Prev</button><input type="range" id="v">
<p data-boundary>Where this analogy breaks: cut a pipe and water sprays out; break a wire and current stops.</p>
</section>
<section data-pass="2">
<svg viewBox="0 0 960 540" width="100%"><circle cx="480" cy="270" r="60"/><text x="480" y="300">node</text></svg>
<p>Each step moves one packet and marks the edge it crossed.</p>
<canvas id="field" aria-label="diffusion field, 64 by 64 cells"></canvas>
</section>
<section data-pass="3">
<p>Production systems batch these, and the batch boundary is where the model above stops predicting well. Jump to this section for the numbers.</p>
</section>
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
    ("vendor-inlined", GOOD.replace("function draw(){", "function draw(){THREE.Scene();")),
    ("visual-scenes", GOOD.replace('<canvas id="field" aria-label="diffusion field, 64 by 64 cells"></canvas>', "")
                          .replace('<svg viewBox="0 0 960 540" width="100%"><circle cx="480" cy="270" r="60"/><text x="480" y="300">node</text></svg>', "")),
    ("svg-viewbox", GOOD.replace('viewBox="0 0 960 540" ', "", 1)),
    ("no-hardcoded-svg-px", GOOD.replace('width="100%"', 'width="960" height="540"', 1)),
    ("canvas-labelled", GOOD.replace(' aria-label="diffusion field, 64 by 64 cells"', "")),
    ("interactive-controls", GOOD.replace('<button id="back">Prev</button>', "").replace('<input type="range" id="v">', "")),
    ("interaction-variety", GOOD.replace('<input type="range" id="v">', "")
                                .replace("s.addEventListener('pointerdown',e=>{s.setPointerCapture(e.pointerId)});", "")
                                .replace("s.addEventListener('pointermove',()=>{});", "")
                                .replace("const s=document.getElementById('v');", "")),
    ("pointer-capture", GOOD.replace("s.setPointerCapture(e.pointerId)", "0")),
    ("touch-action-none", GOOD.replace(".stage{touch-action:none}", "")),
    ("raf-lifecycle", GOOD.replace("cancelAnimationFrame(h)", "0")),
    ("motion-steppable", GOOD.replace('<button id="step">Step</button>', '<button id="go">Go</button>')
                             .replace('<button id="back">Prev</button>', '<button id="two">Two</button>')
                             .replace("getElementById('step')", "getElementById('go')")),
    ("reduced-motion", GOOD.replace("@media (prefers-reduced-motion: reduce){*{animation:none}}", "")),
    ("theme-aware", GOOD.replace("@media (prefers-color-scheme: dark){:root{--bg:#111}}", "")),
    ("surface-reach", GOOD.replace('<canvas id="field" aria-label="diffusion field, 64 by 64 cells"></canvas>', "")),
    ("video-inline-and-scrubbable", GOOD.replace("<canvas", '<video src="clip.mp4" autoplay></video><canvas')),
    ("state-change-signalled", GOOD.replace(".pulse{animation:p .3s}", "")
                                   .replace("h=requestAnimationFrame(draw)", "draw()")
                                   .replace("function draw(){cancelAnimationFrame(h)}", "function draw(){h=0}")),
    ("boundary-card", GOOD.replace("Where this analogy breaks: cut", "More detail: cut")
                          .replace("<p data-boundary>", "<p>")),
    ("boundary-reachable",
     GOOD.replace("Jump to this section for the numbers.", "Jump to this section for the numbers. " + "detail " * 60)
         .replace('<p data-boundary>Where this analogy breaks: cut a pipe and water sprays out; break a wire and current stops.</p>', "")
         .replace("</section>\n<script>", "<p data-boundary>Where this analogy breaks: cut a pipe and water sprays out; break a wire and current stops.</p></section>\n<script>")),
    ("predict-observe-explain", GOOD.replace("Guess which node wins before you run it.", "It runs.")
                                    .replace("<p data-predict>", "<p>")),
    ("register", GOOD.replace("Pressure drives", "Grown-ups call this the magic rule; pressure drives")),
    ("defines-its-terms", GOOD.replace("<dfn>", "<span>").replace("</dfn>", "</span>")),
    ("names-things", GOOD.replace("Pressure drives flow through a constriction.",
                                  "Something drives anything through the thing, and stuff moves.")),
    ("title-names-its-subject", GOOD.replace("<body>", "<body><h1>It still says all is well</h1>")),
    ("plain-statements", GOOD.replace("Pressure drives flow through a constriction.",
                                      "Pressure is a different axis. Flow is external. "
                                      "Wide, not narrow. Resistance is another thing.")),
    ("disclosure-tiers", GOOD.replace('data-pass="2"', "id=b").replace('data-pass="3"', "id=c")),
    ("skip-ahead", GOOD.replace("Jump to this section for the numbers.", "These are the numbers.")),
    ("coherence-no-emoji-diagrams", GOOD.replace("<p>Each step moves", "<p>" + "🔥" * 13 + " Each step moves")),
    ("prose-budget", GOOD.replace("<p>Each step moves one packet and marks the edge it crossed.</p>",
                                  "".join(f"<p>{'packet ' * 40}</p>" for _ in range(10)))),
    ("prose-block", GOOD.replace("<p>Each step moves one packet and marks the edge it crossed.</p>",
                                 "<p>" + "packet " * 51 + "</p>")),
    ("prose-run", GOOD.replace("<p>Each step moves one packet and marks the edge it crossed.</p>",
                               "".join(f"<p>{'packet ' * 42}</p>" for _ in range(3)))),
    ("opening-budget", GOOD.replace("<p><dfn>Constriction</dfn>: the narrow part of the pipe. <dfn>Head</dfn>: how hard the water is pushed. <dfn>Rate</dfn>: how much passes a point each second. Pressure drives flow through a constriction.</p>",
                                    "".join(f"<p>{'pressure ' * 31}</p>" for _ in range(3)))),
    ("no-template-boilerplate", GOOD.replace("<p>Each step moves one packet and marks the edge it crossed.</p>",
                                             "<p>The turn. The second lens. Tier 3.</p>")),
    ("visual-density", GOOD.replace("<p>Each step moves one packet and marks the edge it crossed.</p>",
                                    "".join(f"<p>{'packet ' * 34}</p>" for _ in range(11)))),
]


def self_test() -> int:
    base = lint(GOOD, "<good>")
    bad = [c for c in base.checks if c.status in (FAIL, WARN)]
    print(f"baseline GOOD fixture: {base.ran} ran, {len(base.failures)} failed, {len(base.warnings)} warned")
    for c in bad:
        print(f"  {c.status}  {c.rule}: {c.detail}")

    rules = {c.rule for c in base.checks}
    covered, misses = set(), []
    for rule, html in FIXTURES:
        r = lint(html, f"<fixture:{rule}>")
        got = {c.rule for c in r.checks if c.status in (FAIL, WARN)}
        if rule in got:
            covered.add(rule)
        else:
            misses.append((rule, sorted(got)))

    uncovered = sorted(rules - covered)
    print(f"\n{len(covered)} of {len(rules)} rules proved able to fail")
    for rule, got in misses:
        print(f"  FIXTURE DID NOT TRIP  {rule}  (tripped: {got})")
    for rule in uncovered:
        if rule not in dict(FIXTURES):
            print(f"  NO FIXTURE            {rule}")

    ok = not bad and not misses and not uncovered
    print("\nself-test", "passed" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------- entry

def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic gate for eli5 explainer artifacts.")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.path:
        ap.error("give a file path, or --self-test")

    html = open(args.path, encoding="utf-8", errors="replace").read()
    r = lint(html, args.path)
    print(render(r, args.json))
    return 1 if r.failures else 0


if __name__ == "__main__":
    sys.exit(main())
