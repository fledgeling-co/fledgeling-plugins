#!/usr/bin/env python3
"""design-lint: deterministic checks for design-craft HTML artifacts.

The mechanically-checkable subset of the design-craft review rules (SKILL.md
ch. 6-12, ai-slop-check.md, accessibility-audit.md, typesetting.md), so a build
loop catches them per round without spending a model critique. Stdlib only;
runs anywhere the skill is seeded (Claude Code, CI, a headless sandbox).

    python3 design-lint.py file.html [more.html ...]
    python3 design-lint.py --selftest          # prove every rule can fire
    python3 design-lint.py --json file.html

Exit codes
    0  clean, or warnings only
    1  any critical or major finding
    2  usage error
    3  --selftest found a rule that cannot fire

Two channels, and the split is load-bearing:
  * critical/major go to STDOUT and gate the build.
  * minor goes to STDERR. Anything on stderr is a warning to read, never a
    reason to stop — so a build loop can pipe it away and still be honest.

**A rule gates when it names a mechanism; it warns when it names a fashion.**
Legibility, breakage, and a standards floor are gating (contrast, a removed
focus ring, an unread token, a resource the CSP will block). A taste cue is a
warning, however well-evidenced the taste — the research is clear that no
individual visual cue reliably identifies AI authorship to a human, so a hard
gate on a font name would encode a claim the evidence does not support and
would fire on a brand that genuinely uses that font. `references/evidence.md`
records which is which and why.

Contrast is **tri-state**, never binary: PASS, FAIL, or UNMEASURABLE. A ground
that is a gradient, an image, or undeclared is reported as unmeasurable rather
than skipped, because an unmeasured pair and a passing pair serialise
identically otherwise — which is the exact mechanism by which axe-core's
"incomplete" results ship inaccessible gradients on pipelines that halt only on
`violations`.

Every finding names three things: what is in the file, what the downstream
consumer will SILENTLY do about it, and the fix. That is a function signature
here rather than a convention (`add()` requires `consequence` and `fix`), so a
new rule cannot ship without one.

A clean run prints its own "not checked" line. This gate is downstream of the
findings that motivated it: it can prove a defect someone has already met has
not come back, and it is structurally incapable of finding the one nobody has
met yet. `0 findings` means "no known defect is present", never "verified" —
and the summary says so in its own output so the distinction survives being
pasted into a report.

**Stated substrate limitation.** Markup checks run through Python's stdlib HTML
parser; CSS checks run on a small rule-block parser in this file, not on a real
CSS AST. Every reviewed source recommends a full AST (PostCSS/Stylelint) over
text heuristics, and that recommendation is right — the constraint here is that
this script must run with zero dependencies anywhere the skill is seeded,
including a headless sandbox with no npm. The mitigations are in the file:
comments are blanked before matching, declarations are read per rule block
rather than free-text, non-source paths are excluded before checking, every
rule is proved to fire by `--selftest`, and a clean fixture is asserted to
produce nothing. Where a check would need the cascade or real specificity, it
is not written — see the "deliberately NOT checked" block at the end.

Path classification: files under `docs/`, `references/`, `fixtures/`,
`examples/`, `node_modules/`, `dist/` and `vendor/`, and any `.md`, are skipped
unless named explicitly on the command line. Classifying the source is a more
reliable fix for "the gate fires on its own documentation" than ever-more-exact
patterns.

Suppression: `lint-ok: <check> - <reason>` in an HTML or CSS comment on the
same line or within two lines above. The reason is required; a bare
`lint-ok: pure-bw` is ignored and reported, because a suppression nobody
justified is a rule nobody applied. `lint-ok-file: <check> - <reason>`
suppresses the check for the whole file. A suppression records that an
instance is genuinely correct — it is not a way to clear a finding you
disagree with, and a run that suppresses its way to zero has not passed.
"""

import json
import math
import re
import sys
from html.parser import HTMLParser


# ---------------------------------------------------------------------------
# Markup: a real parser, not a regex
# ---------------------------------------------------------------------------

# Every reviewed source says the same thing: a string search cannot reproduce
# DOM construction, implicit nodes, error recovery, or element context. The
# stdlib parser is what makes that available here without a dependency.

NON_SOURCE = ("/docs/", "/references/", "/fixtures/", "/examples/",
              "/node_modules/", "/dist/", "/vendor/", "/reports/", "/__pycache__/")


class Markup(HTMLParser):
    """Collect the tags the markup-shaped checks need, with real line numbers."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []        # (name, {attr: value}, line)
        self.classes = set()  # every class token actually applied
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        self.tags.append((tag.lower(), d, self.getpos()[0]))
        self.classes.update(d.get("class", "").split())
        if tag.lower() == "title":
            self._in_title, self.title = True, ""

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and self.title is not None:
            self.title += data


def parse_markup(html):
    m = Markup()
    try:
        m.feed(html)
        m.close()
    except Exception:
        # A parse that throws is a finding about the file, not a reason to skip
        # every markup check: whatever was collected before the throw stands.
        pass
    return m

# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

SEVERITIES = ("critical", "major", "minor")


class Report:
    def __init__(self):
        self.findings = []          # dicts
        self.seen = set()
        self.suppressed = []        # (path, check, reason)
        self.bad_suppressions = []  # (path, line, raw)

    def add(self, sev, path, line, check, detail, consequence, fix):
        """Record a finding. `consequence` is what the downstream consumer does
        about it silently; `fix` is the concrete move. Both are required."""
        assert sev in SEVERITIES, sev
        assert consequence and fix, f"{check}: every finding names its consequence and its fix"
        key = (path, line, check)
        if key in self.seen:
            return
        self.seen.add(key)
        self.findings.append({
            "severity": sev, "file": path, "line": line, "check": check,
            "detail": detail, "consequence": consequence, "fix": fix,
        })

    def count(self, sev):
        return sum(1 for f in self.findings if f["severity"] == sev)


R = Report()

# ---------------------------------------------------------------------------
# Colour: parsing, oklch, WCAG
# ---------------------------------------------------------------------------


def _srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin_to_srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklch_to_rgb(L, C, h_deg):
    """OKLCh -> sRGB 0..1. Implemented because SKILL.md ch. 6 tells you to build
    palettes in oklch(); a contrast gate blind to oklch is blind to exactly the
    code this skill asks for."""
    h = math.radians(h_deg)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return (_lin_to_srgb(r), _lin_to_srgb(g), _lin_to_srgb(bb))


NAMED = {
    "white": (1.0, 1.0, 1.0), "black": (0.0, 0.0, 0.0),
    "transparent": None, "currentcolor": None, "inherit": None,
    "initial": None, "unset": None, "none": None,
}


def parse_color(value):
    """-> (r, g, b, alpha) in 0..1, or None when the value is not a resolvable
    flat colour (a gradient, an image, a keyword, a colour function this does
    not implement). None is 'unknown', never 'fine'."""
    if value is None:
        return None
    v = value.strip().rstrip(";").strip().lower()
    if not v:
        return None
    if v in NAMED:
        rgb = NAMED[v]
        return None if rgb is None else (*rgb, 1.0)

    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (r, g, b, a)

    m = re.fullmatch(r"rgba?\(([^)]*)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        if len(parts) < 3:
            return None
        try:
            ch = []
            for p in parts[:3]:
                ch.append(float(p[:-1]) / 100 if p.endswith("%") else float(p) / 255)
            a = 1.0
            if len(parts) > 3:
                a = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])
            return (*ch, a)
        except ValueError:
            return None

    m = re.fullmatch(r"oklch\(([^)]*)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        if len(parts) < 3:
            return None
        try:
            L = float(parts[0][:-1]) / 100 if parts[0].endswith("%") else float(parts[0])
            C = float(parts[1])
            hs = parts[2]
            for unit in ("deg", "grad", "rad", "turn"):
                if hs.endswith(unit):
                    hs = hs[: -len(unit)]
                    break
            h = float(hs)
            a = 1.0
            if len(parts) > 3:
                a = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])
            return (*oklch_to_rgb(L, C, h), a)
        except ValueError:
            return None

    m = re.fullmatch(r"hsla?\(([^)]*)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        if len(parts) < 3:
            return None
        try:
            hh = float(re.sub(r"deg$", "", parts[0])) / 360.0
            s = float(parts[1].rstrip("%")) / 100
            ll = float(parts[2].rstrip("%")) / 100
            a = 1.0
            if len(parts) > 3:
                a = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])

            def hue(p, q, t):
                t %= 1.0
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p
            if s == 0:
                return (ll, ll, ll, a)
            q = ll * (1 + s) if ll < 0.5 else ll + s - ll * s
            p = 2 * ll - q
            return (hue(p, q, hh + 1 / 3), hue(p, q, hh), hue(p, q, hh - 1 / 3), a)
        except ValueError:
            return None
    return None


def luminance(rgb):
    r, g, b = (_srgb_to_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def composite(fg, bg, extra_alpha=1.0):
    """Flatten a translucent foreground onto an opaque ground. `opacity` on the
    rule multiplies the colour's own alpha — the property that moves a computed
    ratio without moving any colour token, which is why a token-map audit is
    structurally blind to it."""
    a = fg[3] * extra_alpha
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))


# ---------------------------------------------------------------------------
# Source handling
# ---------------------------------------------------------------------------


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def collect_suppressions(raw, path):
    """Read `lint-ok:` / `lint-ok-file:` out of comments BEFORE they are blanked.
    Returns (per_line {check: set(lines)}, file_wide set(checks))."""
    per_line, file_wide = {}, set()
    pat = re.compile(r"lint-ok(-file)?\s*:\s*([a-z0-9-]+)\s*(?:[-\u2014:]\s*(.*?))?(?=-->|\*/|\n|$)", re.I)
    for m in pat.finditer(raw):
        whole, check, reason = m.group(1), m.group(2).lower(), (m.group(3) or "").strip()
        ln = lineno(raw, m.start())
        if len(reason) < 4:
            R.bad_suppressions.append((path, ln, m.group(0).strip()))
            continue
        R.suppressed.append((path, check, reason))
        if whole:
            file_wide.add(check)
        else:
            per_line.setdefault(check, set()).update({ln, ln + 1, ln + 2, ln + 3})
    return per_line, file_wide


def strip_comments(html):
    """Blank HTML, CSS block and JS line comments, keeping offsets stable.

    The original blanked `<!-- -->` and slash-star only, so `external-resource`
    reported the line of the first `//` in the file — usually a JS comment —
    rather than the resource. JS line comments are blanked here, and every
    finding carries its own match position regardless."""
    html = re.sub(r"<!--.*?-->", blank, html, flags=re.S)
    html = re.sub(r"/\*.*?\*/", blank, html, flags=re.S)
    # `//` line comments, but never inside a URL (`https://`) or a string.
    html = re.sub(r"(?<![:\"'\\])//[^\n]*", blank, html)
    return html


def text_nodes(html):
    """Visible text nodes only (crude): drop script/style, then tags."""
    no_code = re.sub(r"<(script|style)\b.*?</\1>", blank, html, flags=re.S | re.I)
    out = []
    for m in re.finditer(r">([^<>]+)<", no_code):
        t = m.group(1).strip()
        if t:
            out.append((lineno(no_code, m.start(1)), t))
    return out


RULE_RE = re.compile(r"([^{}@/]+?)\{([^{}]*)\}", re.S)


def rule_blocks(html):
    """(selector, body, offset) for every flat CSS rule. Nested at-rules are
    handled because the inner blocks match on their own; the selector text then
    excludes the at-rule line, which is why media-scoped findings report the
    inner selector."""
    out = []
    for m in RULE_RE.finditer(html):
        sel = m.group(1).strip().splitlines()[-1].strip() if m.group(1).strip() else ""
        out.append((sel, m.group(2), m.start()))
    return out


def decls(body):
    d = {}
    for part in body.split(";"):
        if ":" not in part:
            continue
        k, _, v = part.partition(":")
        k = k.strip().lower()
        if k and not k.startswith("--"):
            d[k] = v.strip()
    return d


def resolve(value, tokens, depth=0):
    """Follow var(--x) chains to a literal. Honours the fallback form."""
    if value is None or depth > 8:
        return value
    m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]*))?\)", value)
    if not m:
        return value
    name, fallback = m.group(1), m.group(2)
    repl = tokens.get(name)
    if repl is None:
        repl = fallback
    if repl is None:
        return None
    return resolve(value[: m.start()] + repl.strip() + value[m.end():], tokens, depth + 1)


def px(value):
    if not value:
        return None
    m = re.search(r"(-?[\d.]+)\s*(px|rem|em|pt)?", value)
    if not m:
        return None
    try:
        n = float(m.group(1))
    except ValueError:
        return None
    unit = m.group(2) or "px"
    return {"px": n, "rem": n * 16, "em": n * 16, "pt": n * 4 / 3}[unit]


# ---------------------------------------------------------------------------
# Constant sets
# ---------------------------------------------------------------------------

DEFAULT_FONTS = ("Inter", "Roboto", "Arial", "Space Grotesk", "Fraunces",
                 "Instrument Serif", "Playfair Display")

TAILWIND_INDIGO = {"#6366f1", "#4f46e5", "#4338ca", "#3730a3",
                   "#8b5cf6", "#7c3aed", "#a855f7"}

CREAM_TOKEN_NAMES = ("--paper", "--cream", "--sand", "--bone", "--linen",
                     "--parchment", "--ivory", "--wheat")

GENERIC_TITLES = {
    "design", "designs", "canvas", "design canvas", "new design", "untitled",
    "untitled document", "mockup", "mock", "mock-up", "prototype", "page",
    "index", "demo", "test", "output", "artifact", "app", "document",
    "html", "example", "sample", "preview", "wireframe", "draft",
}
GENERIC_FILENAMES = {
    "index.html", "page.html", "design.html", "designs.html", "canvas.html",
    "mockup.html", "mock.html", "prototype.html", "output.html", "test.html",
    "untitled.html", "demo.html", "main.html", "app.html", "example.html",
    "your-file-name.html", "draft.html", "wireframe.html", "final.html",
}

# Origins the published-artifact CSP permits. Everything else is blocked there
# with no error: the page ships without the resource and nothing warns.
# See references/delivery-surfaces.md for the full policy.
CSP_ALLOWED_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------


def check_file(path):
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError as e:
        R.add("critical", path, 0, "unreadable", str(e),
              "nothing downstream of this ran, and an empty finding list reads as clean",
              "check the path")
        return

    per_line_sup, file_sup = collect_suppressions(raw, path)
    html = strip_comments(raw)
    dom = parse_markup(html)
    has_markup = any(t[0] in ("html", "body", "div", "section", "main", "button")
                     for t in dom.tags)

    def add(sev, line, check, detail, consequence, fix):
        if check in file_sup or line in per_line_sup.get(check, ()):
            return
        R.add(sev, path, line, check, detail, consequence, fix)

    tokens = {}
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;{}]+)", html):
        tokens.setdefault(m.group(1), m.group(2).strip())

    blocks = rule_blocks(html)

    # --- the deliverable's name is content -----------------------------------
    base = path.rsplit("/", 1)[-1].lower()
    if has_markup:
        title_line = next((ln for n, _, ln in dom.tags if n == "title"), 1)
        if dom.title is None:
            add("major", 1, "missing-title",
                "no <title> in an HTML deliverable",
                "every surface that lists this file — a browser tab, an artifact gallery, "
                "a bookmark, a shared link — shows the URL or the filename instead, "
                "permanently and to everyone",
                "title it the way the user would name the design themselves")
        elif dom.title.strip().lower() in GENERIC_TITLES:
            add("major", title_line, "generic-title",
                f'<title>{dom.title.strip()}</title> names the '
                "format or nothing, not the content",
                "the title is the design's name everywhere it is listed, and nobody renames "
                "it later — the placeholder is what the user lives with",
                "retitle from what the user actually asked for")
        if base in GENERIC_FILENAMES:
            add("minor", 1, "generic-filename",
                f"{base} names the format, not the design",
                "the filename is the first and most durable thing the user sees; two runs on "
                "one brief produce index.html and interaction-mock.html and neither says what "
                "it is",
                "name the file from the content (kebab-case), never after the tool or the format")

    # --- content -------------------------------------------------------------
    for m in re.finditer(r"lorem\s+ipsum|\bdolor\s+sit\s+amet\b", html, re.I):
        add("critical", lineno(html, m.start()), "placeholder-text",
            "lorem ipsum in the deliverable",
            "a reviewer reads greeked copy as 'not finished yet' and stops reading the design; "
            "in a wireframe it also hides the real length of the string the layout has to hold",
            "real content, or the honest placeholder recipe (SKILL.md ch. 6) with a label "
            "naming what goes there")

    # --- colour --------------------------------------------------------------
    for m in re.finditer(r"(?:color|background(?:-color)?)\s*:\s*(#fff(?:fff)?|#000(?:000)?)\b",
                         html, re.I):
        add("minor", lineno(html, m.start()), "pure-bw",
            f"{m.group(1)} as a text or surface colour",
            "pure-on-pure reads harsh and unfinished on every display, and it is the "
            "cheapest tell that no palette decision was made. Warns rather than gates: 21:1 is perfectly legible, so this is a taste claim",
            "tone it (e.g. #FAFAFA / #1A1A1A), or suppress with "
            "`lint-ok: pure-bw - <why black is correct here>` when the black is real "
            "(a device bezel, a scrim, print ink)")

    for m in re.finditer(r"linear-gradient\([^)]*\)", html, re.I):
        stops = len(re.findall(r"#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(|oklch\(", m.group(0), re.I))
        if stops >= 3:
            add("minor", lineno(html, m.start()), "gradient-stops",
                f"{stops}-stop gradient",
                "three or more stops is the rainbow-hero signature; it reads as decoration "
                "applied to a surface no one designed",
                "flat colour, or two stops of low contrast in one hue family")

    for m in re.finditer(r"var\(\s*(--[\w-]+)", html):
        name = m.group(1)
        if name not in tokens and not re.search(
                r"var\(\s*" + re.escape(name) + r"\s*,", html):
            add("critical", lineno(html, m.start()), "unresolved-var",
                f"var({name}) has no definition and no fallback",
                "the property resolves to nothing — the element renders with the inherited or "
                "initial value, which is usually plausible enough to survive every look",
                "define the token, or give the var() a fallback")

    # A token nothing reads is a real and measured defect — but only in a file
    # that is USING its own token layer. A design-system specimen publishes a
    # layer for downstream consumers, and most of its tokens are legitimately
    # unread here. Found by this skill's own eval A25 as a false positive on
    # exactly that shape, so the check is scoped by read ratio rather than
    # dropped: below the threshold it declares that it did not apply, because a
    # rule that quietly stopped firing is indistinguishable from a clean file.
    if has_markup and tokens:
        unread = [n for n in tokens
                  if not re.search(r"var\(\s*" + re.escape(n) + r"\b", html)]
        read_ratio = 1 - len(unread) / len(tokens)
        if read_ratio >= 0.6:
            for name in unread:
                add("major", lineno(html, html.find(name)), "unread-token",
                    f"{name} is defined and never referenced "
                    f"({len(unread)} of {len(tokens)} tokens unread)",
                    "a token nothing reads is not applied: the theme carries it, the markup "
                    "shows it, and every element it was meant to paint keeps the raw value "
                    "(measured: a 72px company name at 2.14:1 under a primaryOnDark nobody read)",
                    "write the rule that reads it, or delete the token")
        else:
            add("minor", 1, "unread-token-not-applied",
                f"only {read_ratio:.0%} of this file's {len(tokens)} tokens are read here, "
                "so the unread-token check did not run",
                "the file reads as a token layer published for other files rather than an "
                "artifact using its own tokens, and firing on every unread token there would "
                "be noise — but that also means a genuinely orphaned token is NOT being "
                "caught in this file",
                "if this is a self-contained artifact rather than a specimen, the low read "
                "ratio is itself the finding: grep var(--token) for each one")

    for hexv in TAILWIND_INDIGO:
        for m in re.finditer(re.escape(hexv), html, re.I):
            add("minor", lineno(html, m.start()), "tailwind-indigo",
                f"{hexv} — the default Tailwind indigo family",
                "indigo is the textbook AI accent: the palette reads as untouched framework "
                "default even when everything around it was chosen",
                "replace with the committed accent from the direction contract")
            break

    for tk in CREAM_TOKEN_NAMES:
        if tk in tokens:
            add("minor", lineno(html, html.find(tk)), "cream-token-name",
                f"{tk} — a warm-neutral token name",
                "the token names are tells in themselves: the warm-editorial default arrives "
                "named, and the name is what keeps it after the hex is changed",
                "name the token by its role (--surface, --ground) and check the value is not "
                "in the OKLCH L 0.84-0.97 / C<0.06 / H 40-100 cream band unless the brief "
                "pinned it")

    if has_markup:
        outside = re.sub(r":root\s*\{[^{}]*\}", blank, html)
        raw_hex = {h.lower() for h in re.findall(r"#[0-9a-f]{6}\b", outside)}
        if len(raw_hex) > 12:
            add("major", 1, "hex-sprawl",
                f"{len(raw_hex)} distinct raw hex literals outside :root",
                "the token block exists, so the system looks real while the surface is painted "
                "inline — a rebrand then edits one layer and misses the page "
                "(measured: 45 raw hex against 11 declared tokens)",
                "move them into :root and reference by var()")

    # --- contrast: PASS / FAIL / UNMEASURABLE, never a silent skip ----------
    # WCAG 2.x is the gate (4.5:1 body, 3:1 large and non-text), inclusive with
    # no rounding. APCA is deliberately not used: it was removed from the
    # WCAG 3.0 working draft and the draft still records its contrast algorithm
    # as undetermined, so gating on it would gate on a non-standard.
    # Low-contrast text is the most common automatically-detectable
    # accessibility error on the web — WebAIM's 2026 million-page scan found it
    # on 83.9% of home pages — which is why this is the one check that fails at
    # critical.
    page_bg, page_bg_declared = (1.0, 1.0, 1.0, 1.0), False
    for sel, body, off in blocks:
        if re.search(r"(^|,)\s*(body|html|:root)\s*$", sel, re.I):
            d = decls(body)
            for prop in ("background-color", "background"):
                if prop in d:
                    c = parse_color(resolve(d[prop], tokens))
                    if c and c[3] > 0.95:
                        page_bg, page_bg_declared = c, True

    for sel, body, off in blocks:
        d = decls(body)
        if "color" not in d:
            continue
        fg = parse_color(resolve(d["color"], tokens))
        if fg is None:
            continue
        bg_src = None
        for prop in ("background-color", "background"):
            if prop in d:
                bg_src = parse_color(resolve(d[prop], tokens))
                break
        opaque_own_bg = bool(bg_src and bg_src[3] > 0.95)
        complex_bg = any(k in body.lower() for k in
                         ("gradient(", "url(", "background-image", "backdrop-filter",
                          "mix-blend-mode"))

        # A ground this file cannot resolve is UNMEASURABLE, not clean. Two
        # cases: a gradient/image/blend backdrop, and a rule that declares no
        # ground on a page that declares none either.
        if not opaque_own_bg and (complex_bg or not page_bg_declared):
            why = ("its backdrop is a gradient, image or blend layer"
                   if complex_bg else
                   "neither the rule nor body/:root declares an opaque ground")
            add("major", lineno(html, off), "contrast-unmeasurable",
                f"`{sel}` sets a text colour and {why}",
                "no ratio can be computed from source, and an unmeasured pair and a "
                "passing pair look identical in a findings list — this is exactly how a "
                "checker's 'incomplete' result ships inaccessible text on a pipeline that "
                "halts only on outright violations",
                "put the text on a declared opaque backing surface and re-run, or sample "
                "the rendered pixels with the pixel-median fallback in "
                "accessibility-audit.md checklist 1 — it gives you the worst-case region "
                "WCAG G18 asks for, and it is also what adjudicates a ratio this gate "
                "DID report when the cascade overrode the declared ground. Never treat "
                "an unmeasurable as a pass")
            continue

        bg = bg_src if opaque_own_bg else page_bg
        try:
            op = float(d.get("opacity", "1"))
        except ValueError:
            op = 1.0
        flat_fg = composite(fg, bg, op)
        ratio = contrast_ratio(flat_fg, bg[:3])

        size = px(resolve(d.get("font-size"), tokens))
        weight = d.get("font-weight", "")
        bold = weight in ("bold", "bolder") or (weight.isdigit() and int(weight) >= 700)
        large = size is not None and (size >= 24 or (size >= 18.66 and bold))
        floor = 3.0 if large else 4.5
        if size is None and re.search(r"\b(h1|h2|display|hero|title)\b", sel, re.I):
            floor = 3.0   # unsized heading selector: judged at the large-text floor
            large = True
        if ratio + 1e-9 < floor:
            note = f"{ratio:.2f}:1 against its ground, floor {floor}:1"
            if op != 1.0:
                note += f" (composited through opacity: {op})"
            add("critical", lineno(html, off), "contrast",
                f"`{sel}` measures {note}",
                "nothing in the render says so — a model reads the pair as fine and only the "
                "arithmetic disagrees, which is how a surface ships claiming 100% pass with "
                "every primary button at 3.65:1",
                "lift the text colour, or derive a second token for this role rather than "
                "changing the brand value (accessibility-audit.md checklist 1). "
                "Thresholds are inclusive with no rounding: 4.499:1 fails. This ratio is "
                "computed from the ground the CSS DECLARES — when you believe it is wrong, "
                "adjudicate it with the pixel-median fallback rather than scoping the rule: "
                "a fabricated failure costs as much as a fabricated pass")

    # --- the default-card tell ----------------------------------------------
    for sel, body, off in blocks:
        if re.search(r"border-left\s*:\s*[2-9]px\s+solid", body) and "border-radius" in body:
            add("minor", lineno(html, off), "default-card",
                "border-radius + a border-left accent as the card style",
                "the combination is so overused it reads 'default SaaS template' before a "
                "reader has looked at anything you chose",
                "shadow, a thin all-around border, or background contrast; keep the left "
                "border only where it carries real semantic emphasis")
        blur = [int(x) for x in re.findall(r"box-shadow\s*:[^;]*?(\d+)px\s+rgba?", body)]
        if re.search(r"border\s*:\s*1px\s+solid", body) and any(b >= 16 for b in blur):
            add("minor", lineno(html, off), "ghost-card",
                "a 1px border and a wide soft shadow on the same element",
                "two elevation languages stacked read as softness applied rather than depth "
                "designed, and the effect compounds on every card on the page",
                "pick one per card: border, or a defined shadow at <=8px blur, or a "
                "background shift")
        for m in re.finditer(r"border-radius\s*:\s*(\d+)px", body):
            if int(m.group(1)) >= 24 and not re.search(r"\b(pill|tag|chip|badge|avatar)\b", sel, re.I):
                add("minor", lineno(html, off), "over-rounding",
                    f"border-radius: {m.group(1)}px on `{sel}`",
                    "over-rounding reads as generic-friendly; cards top out at 12-16px and "
                    "full-pill belongs to tags and buttons",
                    "12-16px on cards and sections, 9999px only on pills")

    # --- typography ---------------------------------------------------------
    for m in re.finditer(r"font-family\s*:\s*['\"]?(" + "|".join(DEFAULT_FONTS) + r")\b", html, re.I):
        add("minor", lineno(html, m.start()), "default-font",
            f"{m.group(1)} as the leading family",
            "these are the faces this model reaches for unprompted — Space Grotesk "
            "especially when *asked* to be distinctive — so their presence is evidence of "
            "gravity rather than of choice. Warns rather than gates: no evidence supports treating a font name as proof of AI authorship, and a brand that genuinely uses this face is correct to keep it",
            "a face the direction can defend in one sentence; keep this one only if the "
            "brand specifies it")

    for sel, body, off in blocks:
        if re.search(r"text-transform\s*:\s*uppercase", body) and "letter-spacing" not in body:
            add("major", lineno(html, off), "untracked-caps",
                f"uppercase without letter-spacing on `{sel}`",
                "the counters collide at caps sizes, so the label reads cramped and amateur — "
                "untracked caps and untracked display are the two most reliable typographic "
                "AI tells",
                "letter-spacing: 0.06-0.1em on all-caps labels")

    for m in re.finditer(r"letter-spacing\s*:\s*(-0?\.\d+)em", html):
        if float(m.group(1)) < -0.04:
            add("major", lineno(html, m.start()), "over-tight-tracking",
                f"{m.group(1)}em is below the -0.04em floor",
                "letters touch, which reads cramped rather than designed, and it survives "
                "every screenshot because the words are still readable",
                "-0.02 to -0.03em on display type, with -0.04em as the hard floor")

    for ln, t in text_nodes(html):
        if "..." in t:
            add("minor", ln, "three-dots",
                "'...' in visible text",
                "three periods render with the wrong spacing and can break across a line where "
                "the real character cannot",
                "the ellipsis character")

    # --- layout / engineering -----------------------------------------------
    for m in re.finditer(r":\s*100vh\b", html):
        add("major", lineno(html, m.start()), "100vh",
            "100vh",
            "on a mobile browser 100vh is the viewport WITHOUT the chrome, so the section "
            "overflows by the toolbar's height and the page gains a scroll nobody designed",
            "min-height: 100dvh, which is the viewport the user actually has")

    for m in re.finditer(r"z-index\s*:\s*(\d{3,})", html):
        if int(m.group(1)) >= 999:
            add("minor", lineno(html, m.start()), "zindex-arms-race",
                f"z-index: {m.group(1)}",
                "the next thing that needs to sit above it gets 10000, and the page's stacking "
                "order stops being expressible",
                "a tokenized scale (--z-dropdown: 100 ... --z-toast: 500) and "
                "isolation: isolate on components that layer internally")

    for name, attrs, ln in dom.tags:
        if name != "img":
            continue
        has_w, has_h = "width" in attrs, "height" in attrs
        style_v = attrs.get("style", "").lower()
        if not (has_w and has_h):
            add("major", ln, "unsized-img",
                "img with no width and height attributes",
                "the browser reserves no box, so everything below it jumps when the image "
                "decodes — and the jump is invisible in a screenshot taken after load",
                "add both attributes AND `height: auto` in the style: an <img> carrying a "
                "height attribute and a CSS aspect-ratio has two definite dimensions, so "
                "aspect-ratio is ignored and the photo over-crops (SKILL.md ch. 15)")
        elif has_h and "aspect-ratio" in html and "height:auto" not in style_v.replace(" ", ""):
            add("minor", ln, "img-two-dimensions",
                "img with a height attribute on a page that uses aspect-ratio",
                "two definite dimensions make the browser ignore aspect-ratio, and the photo "
                "renders at its natural height in a distorted, over-cropped box",
                "height: auto in the style, so the attribute only seeds the intrinsic ratio")

    for name, attrs, ln in dom.tags:
        if name != "div" or "onclick" not in attrs:
            continue
        add("major", ln, "div-as-button",
            "div with onclick",
            "the control is unreachable by keyboard and invisible to assistive tech; the page "
            "looks and clicks fine, so nothing in a visual review finds it",
            "a real <button> (keyboard, focus, semantics for free)")

    for name, attrs, ln in dom.tags:
        if name != "svg":
            continue
        if not ({"width", "height"} & set(attrs)) and "viewbox" in attrs and "style" not in attrs:
            add("major", ln, "svg-unsized",
                "inline <svg> with no width, height or style",
                "it fills whatever box it is dropped into — a validation icon rendered as a "
                "250px black disc under every field while every DOM assertion about that form "
                "passed",
                "explicit dimensions and a colour on every inline SVG; 'it inherits' is only "
                "true of the ones that do")

    # --- interaction states and focus ---------------------------------------
    for sel, body, off in blocks:
        if re.search(r"outline\s*:\s*(none|0)\b", body):
            has_repl = re.search(r"outline\s*:\s*[^;]*\b\d", body) or "box-shadow" in body
            if not has_repl:
                add("critical", lineno(html, off), "focus-ring-removed",
                    f"`{sel}` removes the outline with no replacement",
                    "a keyboard user loses their position entirely; it is a triple WCAG "
                    "violation (1.4.11, 2.4.7, 2.4.13) and it looks tidier, so it survives "
                    "every visual review",
                    ":focus-visible { outline: 2px solid var(--primary); outline-offset: 2px }")
        if re.search(r"transition\s*:\s*all\b", body):
            add("major", lineno(html, off), "transition-all",
                f"transition: all on `{sel}`",
                "it animates every property the element ever gains, including layout ones — it "
                "works until the day something else changes and then janks for reasons nobody "
                "can locate",
                "name the properties: transition: background .2s ease, transform .2s ease")

    interactive = any(n in ("button", "input", "select", "textarea") or
                      (n == "a" and "href" in a) for n, a, _ in dom.tags)
    if interactive and has_markup:
        if ":focus-visible" not in html and ":focus" not in html:
            add("major", 1, "no-focus-state",
                "interactive elements and no :focus-visible rule anywhere",
                "absence is invisible in a screenshot — the surface photographs perfectly and "
                "cannot be operated from a keyboard (measured: 0 :focus-visible, 0 :active, "
                "0 :disabled on a five-surface artifact)",
                "one :focus-visible rule covering every interactive element")
        if ":hover" not in html:
            add("minor", 1, "no-hover-state",
                "interactive elements and no :hover rule",
                "a button without hover reads as a label, and the page feels dead rather than "
                "broken, so nobody files it",
                "hover on every interactive element")

    for m in re.finditer(r"(?<!user-)\:invalid\b", html):
        add("minor", lineno(html, m.start()), "invalid-not-user-invalid",
            ":invalid rather than :user-invalid",
            ":invalid matches required-but-empty fields on page load, so the form shows red "
            "borders before the user has touched anything — the loudest 'validation added "
            "without testing' tell",
            ":user-invalid, which matches only after a blur with bad input or a submit")

    # --- what the capture engine and the CSP will silently do ----------------
    # Mirroring the downstream consumer's real limits is the highest-transfer
    # sub-pattern available to this gate: Obscura executes no CSS animation and
    # loads no web font, and a published artifact's CSP blocks every origin but
    # its own bar Google Fonts. Each is a source-checkable defect.
    for sel, body, off in blocks:
        d = decls(body)
        resting_hidden = (
            d.get("opacity", "").strip() in ("0", "0.0", "0%")
            or d.get("visibility", "").strip() == "hidden"
            or re.search(r"transform\s*:\s*scale\(0\)", body)
        )
        if resting_hidden and re.search(r"@keyframes|\.(seen|visible|in-view|revealed|is-visible)\b", html):
            add("major", lineno(html, off), "reveal-blank",
                f"`{sel}` is invisible at rest on a page with reveal animations",
                "kill the animation and the content is GONE: it prints blank, it exports blank "
                "to PDF, it captures blank in a headless renderer that runs no animations, and "
                "it stays blank in a background tab — all four look exactly like a layout bug",
                "invert the states — the resting style IS the final style, and the 'from' state "
                "lives only inside @keyframes (make-a-doc.md Phase 3)")

    for m in re.finditer(r'(?:href|src)\s*=\s*["\'](?:https?:)?//([^/"\']+)([^"\']*)', html, re.I):
        host, rest = m.group(1).lower(), m.group(2)
        ln = lineno(html, m.start())
        tag_start = html.rfind("<", 0, m.start())
        tag = html[tag_start:m.start()].lower()
        if any(host.endswith(h) for h in CSP_ALLOWED_HOSTS):
            continue          # the one carve-out a published artifact's CSP permits
        pinned = "integrity=" in html[tag_start:html.find(">", m.start()) + 1].lower()
        if pinned:
            add("minor", ln, "external-resource-pinned",
                f"pinned external request to {host}",
                "fine on a served page; inside a published artifact the CSP blocks it with no "
                "error, so the script never runs and the page ships motionless or blank",
                "keep it for local/served delivery; inline it before publishing as an artifact "
                "(references/delivery-surfaces.md)")
        else:
            add("major", ln, "external-resource",
                f"unpinned external request to {host}",
                "offline, behind a strict CSP, and inside a sandboxed artifact the request "
                "simply does not happen — the page opens in a different typeface, or with the "
                "library missing, and nothing in the console of the machine that built it "
                "ever said so",
                "inline it (base64 / a data: URI), or pin it with an integrity hash for "
                "served-only delivery. Google Fonts via <link> is the sole exception a "
                "published artifact permits")

    for m in re.finditer(r"@font-face\s*\{([^{}]*)\}", html, re.S):
        src = re.search(r"src\s*:\s*([^;]+)", m.group(1))
        if src and "data:" not in src.group(1) and "url(" in src.group(1):
            add("minor", lineno(html, m.start()), "font-face-remote",
                "@font-face pointing at a URL rather than a data: URI",
                "web fonts do not load in the sanctioned capture engine, so type fidelity is "
                "unmeasurable rather than verified — and a published artifact blocks any font "
                "host but Google's",
                "embed the face as a data: URI, or use Google Fonts via <link>")

    # --- a variant nothing selects, and a stylesheet that documents it -------
    if has_markup:
        css_classes = set()
        for sel, _, _ in blocks:
            css_classes.update(re.findall(r"\.([A-Za-z][\w-]*)", sel))
        used_names = set(dom.classes)
        js_strings = set(re.findall(r"['\"]([A-Za-z][\w-]*)['\"]", html))
        for cls in sorted(css_classes):
            if cls in used_names or cls in js_strings:
                continue
            base_names = [cls.split("--")[0], cls.rsplit("-", 1)[0]]
            if "--" in cls and any(b in used_names for b in base_names if b):
                add("major", lineno(html, html.find("." + cls)), "unapplied-variant",
                    f".{cls} is defined and never applied, while its base class is used",
                    "every instance renders the base variant, so the state the stylesheet "
                    "documents is one the renderer cannot reach — measured as thirteen rows "
                    "rendering a dated layout with nothing to put in the date cell",
                    "wire up the selector that applies it, or delete the rule")
            else:
                add("minor", lineno(html, html.find("." + cls)), "unused-class",
                    f".{cls} is defined and never applied",
                    "dead CSS is invisible, and it is indistinguishable from a rule whose "
                    "producer was lost in a refactor",
                    "apply it or delete it")

    # --- emoji as decoration -------------------------------------------------
    emoji = re.compile("[\U0001F300-\U0001FAFF\U00002728\U00002705\U0001F680"
                       "\U0001F4C8-\U0001F4CA\U00002B50\U0001F525\U0001F4A1]")
    hits = [(ln, t) for ln, t in text_nodes(html) if emoji.search(t)]
    if hits:
        ln, t = hits[0]
        add("minor", ln, "decorative-emoji",
            f'{len(hits)} text node(s) contain emoji (first: "{t[:40]}")',
            "emoji carry another vendor's illustration style into your palette, and they "
            "render differently on every platform the design will actually be opened on",
            "only where the brand uses them or the emoji is functional; otherwise a real "
            "icon from one library at one stroke weight")

    # --- verification output leaked into copy --------------------------------
    leak = re.compile(r"constant ratio|scale factor\s*[:=]|zero-?based\s*[:=]\s*true|"
                      r"gate (?:passed|clean)|preflight|contrast (?:pass|verified)|"
                      r"wcag (?:pass|compliant)\b", re.I)
    for ln, t in text_nodes(html):
        if leak.search(t):
            add("major", ln, "leaked-verification",
                f'"{t[:52]}" in visible copy',
                "verification arithmetic printed where provenance belongs tells the reader you "
                "were satisfying a checker; it also reads as a claim the artifact cannot "
                "support",
                "show the source, the as-at date and what the axis does — never your proof of "
                "compliance")
            break

    # --- deliberately NOT checked here --------------------------------------
    # Kept as comments because a rule that cannot fire honestly is worse than an
    # absent one: silence from a broken rule and silence from a clean file
    # serialise identically. Each names where the measurement DOES belong.
    #
    # 1. Hue families. The highest-value single measurement available (measured:
    #    1 family in a designed artifact against 3 in its generic twin) and not
    #    honest from source: a well-tokenised file writes `color: var(--success)`
    #    and the hex appears once, in :root, whether the token paints forty chips
    #    or none — so a static count under-reports on precisely the code most
    #    worth reviewing. Count it in the RENDER, via getComputedStyle.
    #
    # 2. Accent marks per surface. A filled bar, a rule, a progress track and a
    #    dot each read as an accent object to the eye and as nothing to a
    #    selector scan, so an automated count under-reports by exactly the amount
    #    that matters. Count marks in the capture.
    #
    # 3. The section list (ai-slop-check.md ss17). Two blind judges named it as
    #    the first thing separating two builds, ahead of every visual difference —
    #    and it is a judgement about whether the outline came from the material or
    #    from the brief. No regex reaches that.
    #
    # 4. Contrast against a gradient, an image, or an ancestor's ground. The pairs
    #    above are the ones DECLARED TOGETHER. A colour whose ground arrives
    #    through the cascade, from a background-image, or from an inline style on
    #    a parent is skipped rather than measured against the page ground — a
    #    number computed against the wrong ground is worse than no number.
    #
    # 5. Whether an override actually won. An override at equal specificity placed
    #    earlier in the file loses to source order silently, and the file then
    #    contains a correct-looking, greppable rule that does nothing. Only the
    #    computed value on the node distinguishes them.


# ---------------------------------------------------------------------------
# Self-test: prove every rule can fire
# ---------------------------------------------------------------------------

FIXTURES = {
    "placeholder-text": "<title>Ledger review</title><p>Lorem ipsum dolor sit</p>",
    "pure-bw": "<title>Ledger review</title><style>body{background:#FFFFFF;color:#000000}</style>",
    "gradient-stops": "<title>Ledger review</title><style>.h{background:linear-gradient(90deg,#f0f,#0ff,#ff0)}</style>",
    "unresolved-var": "<title>Ledger review</title><style>.a{color:var(--nope)}</style>",
    "unread-token": ("<title>Ledger review</title><div></div><style>:root{--ink:#1A1A1A;"
                     "--ground:#FAFAFA;--ghost:#123456}body{background:var(--ground);"
                     "color:var(--ink)}</style>"),
    "unread-token-not-applied": ("<title>Ledger review</title><div></div><style>:root{"
                                 "--a:#111;--b:#222;--c:#333;--d:#444;--e:#555;--f:#666}"
                                 "body{background:#FAFAFA;color:var(--a)}</style>"),
    "tailwind-indigo": "<title>Ledger review</title><style>.a{border-color:#6366F1}</style>",
    "cream-token-name": "<title>Ledger review</title><style>:root{--paper:#F4F1EA}.a{background:var(--paper)}</style>",
    "hex-sprawl": "<title>Ledger review</title><div></div><style>" + "".join(
        f".c{i}{{border-color:#{i:02x}{i:02x}{i + 32:02x}}}" for i in range(14)) + "</style>",
    "contrast": "<title>Ledger review</title><style>.m{color:#9AA3AF;background:#FFFEFC;font-size:14px}</style>",
    "contrast-unmeasurable": "<title>Ledger review</title><style>body{background:#FFFEFC}.h{color:#fefefe;background:linear-gradient(90deg,#333,#eee)}</style>",
    "default-card": "<title>Ledger review</title><style>.c{border-radius:12px;border-left:4px solid #333}</style>",
    "ghost-card": "<title>Ledger review</title><style>.c{border:1px solid #ddd;box-shadow:0 8px 24px rgba(0,0,0,.1)}</style>",
    "over-rounding": "<title>Ledger review</title><style>.card{border-radius:28px}</style>",
    "default-font": "<title>Ledger review</title><style>body{font-family:'Space Grotesk',sans-serif}</style>",
    "untracked-caps": "<title>Ledger review</title><style>.l{text-transform:uppercase;font-size:12px}</style>",
    "over-tight-tracking": "<title>Ledger review</title><style>h1{letter-spacing:-0.06em}</style>",
    "three-dots": "<title>Ledger review</title><p>Saving...</p>",
    "100vh": "<title>Ledger review</title><style>.hero{min-height:100vh}</style>",
    "zindex-arms-race": "<title>Ledger review</title><style>.p{z-index:9999}</style>",
    "unsized-img": '<title>Ledger review</title><img src="a.png" style="max-width:100%;height:auto">',
    "img-two-dimensions": '<title>Ledger review</title><style>.s{aspect-ratio:3/2}</style><img src="a.png" width="800" height="600">',
    "div-as-button": '<title>Ledger review</title><div onclick="go()">Next</div>',
    "svg-unsized": '<title>Ledger review</title><svg viewBox="0 0 24 24"><path d="M0 0h24"/></svg>',
    "focus-ring-removed": "<title>Ledger review</title><style>.b:focus{outline:none}</style>",
    "transition-all": "<title>Ledger review</title><style>.b{transition:all .2s ease}</style>",
    "no-focus-state": "<title>Ledger review</title><div><button>Go</button></div>",
    "no-hover-state": "<title>Ledger review</title><div><button>Go</button></div><style>.b:focus-visible{outline:2px solid #333}</style>",
    "invalid-not-user-invalid": "<title>Ledger review</title><style>input:invalid{border-color:#c00}</style>",
    "reveal-blank": "<title>Ledger review</title><style>.row{opacity:0}@keyframes fadeUp{to{opacity:1}}</style>",
    "external-resource": '<title>Ledger review</title><script src="https://cdn.example.com/x.js"></script>',
    "external-resource-pinned": '<title>Ledger review</title><script src="https://cdn.example.com/x.js" integrity="sha384-aaa" crossorigin="anonymous"></script>',
    "font-face-remote": "<title>Ledger review</title><style>@font-face{font-family:X;src:url(https://f.example.com/x.woff2)}</style>",
    "unapplied-variant": '<title>Ledger review</title><div class="idx">r</div><style>.idx{color:#333}.idx--undated{color:#555}</style>',
    "unused-class": '<title>Ledger review</title><div>r</div><style>.orphan{color:#333}</style>',
    "decorative-emoji": "<title>Ledger review</title><h2>\U0001F680 Get started</h2>",
    "leaked-verification": "<title>Ledger review</title><p>Constant ratio 1.1765%</p>",
    "missing-title": "<div>no title here</div>",
    "generic-title": "<title>Untitled</title><div>x</div>",
    "generic-filename": "<title>Ledger review</title><div>x</div>",
}

# Rules whose fixture is named rather than written: they need a filename, not a body.
FILENAME_FIXTURES = {"generic-filename": "index.html"}


def selftest():
    """Run each rule against a fixture built to trip it, and assert it fires.

    A rule only ever observed passing is a rule you have not written. This is the
    mechanical form of that: it caught nothing on the day it was added and it is
    the check that stops a regex from silently collapsing (a widow rule shipped as
    /S+/g, matched runs of the letter S, found nothing on any page ever, and its
    silence was reported as a pass)."""
    import os
    import tempfile
    failures, missing_fields = [], []
    tmp = tempfile.mkdtemp(prefix="design-lint-selftest-")
    for check, body in FIXTURES.items():
        name = FILENAME_FIXTURES.get(check, f"{check}-fixture.html")
        p = os.path.join(tmp, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
        global R
        R = Report()
        check_file(p)
        fired = [f for f in R.findings if f["check"] == check]
        if not fired:
            failures.append((check, [f["check"] for f in R.findings]))
            continue
        f = fired[0]
        if len(f["consequence"]) < 20 or len(f["fix"]) < 10:
            missing_fields.append(check)

    # A suppression comment with a reason must silence its check; without a
    # reason it must not.
    p = os.path.join(tmp, "suppressed.html")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("<title>Ledger review</title>\n"
                 "<!-- lint-ok: pure-bw - phone bezel, the real device is black -->\n"
                 "<style>.bezel{background:#000}</style>\n")
    R = Report()
    check_file(p)
    if any(f["check"] == "pure-bw" for f in R.findings):
        failures.append(("suppression-honoured", ["pure-bw still fired"]))
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("<title>Ledger review</title>\n"
                 "<!-- lint-ok: pure-bw -->\n"
                 "<style>.bezel{background:#000}</style>\n")
    R = Report()
    check_file(p)
    if not any(f["check"] == "pure-bw" for f in R.findings):
        failures.append(("suppression-needs-reason", ["an unjustified lint-ok silenced the rule"]))

    # A clean file must produce nothing: a gate that fires on correct code trains
    # the runner to overrule it, and after that no finding counts.
    p = os.path.join(tmp, "ledger-review.html")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(CLEAN_FIXTURE)
    R = Report()
    check_file(p)
    false_positives = [(f["check"], f["line"]) for f in R.findings]

    print(f"selftest: {len(FIXTURES)} rules, {len(FIXTURES) - len(failures)} fired")
    for check, got in failures:
        print(f"  DID NOT FIRE  {check}   (got: {sorted(set(got)) or 'nothing'})")
    for check in missing_fields:
        print(f"  THIN MESSAGE  {check}   (a finding must name its consequence and its fix)")
    if false_positives:
        print(f"  FALSE POSITIVE on the clean fixture: {false_positives}")
    ok = not failures and not missing_fields and not false_positives
    print("selftest: PASS" if ok else "selftest: FAIL")
    return 0 if ok else 3


CLEAN_FIXTURE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Northwind freight ledger</title>
<style>
  :root { --ink:#1A1A1A; --ground:#FAF8F5; --accent:#8C3B1E; --z-toast:500; }
  body { background: var(--ground); color: var(--ink); font-family: "Tiempos Text", Georgia, serif; }
  .eyebrow { text-transform: uppercase; letter-spacing: 0.08em; font-size: 12px; color: var(--ink); }
  .cta { background: var(--accent); color: var(--ground); font-size: 16px; transition: background .2s ease; }
  .cta:hover { background: var(--ink); }
  .cta:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .toast { z-index: var(--z-toast); }
  .row { opacity: 1; }
</style></head>
<body>
  <p class="eyebrow">Freight</p>
  <button class="cta">Book a lane</button>
  <div class="toast" hidden>Saved</div>
  <div class="row">47.2% of lanes cleared</div>
  <img src="dock.png" width="1200" height="800" style="max-width:100%;height:auto" alt="Loading dock at dawn">
</body></html>
"""


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

NOT_CHECKED = (
    "hue families and accent-mark counts (render only) - the section list, whose "
    "provenance is a judgement - contrast against a gradient, an image, or a ground "
    "that arrives through the cascade (reported as contrast-unmeasurable, never as a "
    "pass) - whether an override actually won - a pseudo-element's own styles - "
    "anything that only exists mid-animation"
)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if "--selftest" in flags:
        return selftest()
    if not args:
        print(__doc__)
        return 2

    # Classify the source before checking it. A gate that lints its own
    # documentation, fixtures or vendored files trains the runner to overrule
    # it, and after that no finding counts. Path classification is a more
    # reliable fix for that than ever-more-exact patterns.
    checked, skipped = [], []
    for path in args:
        norm = "/" + path.replace("\\", "/").lstrip("./")
        if "--include-all" not in flags and (
                norm.endswith(".md") or any(seg in norm for seg in NON_SOURCE)):
            skipped.append(path)
        else:
            checked.append(path)
    for path in checked:
        check_file(path)
    if skipped and "--json" not in flags:
        print(f"design-lint: skipped {len(skipped)} non-source path(s) "
              f"({', '.join(skipped[:4])}{', …' if len(skipped) > 4 else ''}) "
              "— documentation, fixtures and vendored files are not linted as source. "
              "Use --include-all to override.", file=sys.stderr)
    if not checked:
        print("design-lint: nothing to check (every path was classified non-source).")
        return 0

    order = {"critical": 0, "major": 1, "minor": 2}
    R.findings.sort(key=lambda f: (order[f["severity"]], f["file"], f["line"]))

    if "--json" in flags:
        print(json.dumps({
            "findings": R.findings,
            "suppressed": [{"file": f, "check": c, "reason": r} for f, c, r in R.suppressed],
            "not_checked": NOT_CHECKED,
            "summary": {s: R.count(s) for s in SEVERITIES},
        }, indent=2))
        return 1 if (R.count("critical") or R.count("major")) else 0

    for f in R.findings:
        line = (f"{f['severity'].upper():8} {f['file']}:{f['line']}  [{f['check']}]  "
                f"{f['detail']}\n         -> {f['consequence']}\n         fix: {f['fix']}")
        print(line) if f["severity"] != "minor" else print(line, file=sys.stderr)

    for path, ln, rawtxt in R.bad_suppressions:
        print(f"MINOR    {path}:{ln}  [suppression-without-reason]  {rawtxt}\n"
              "         -> the check ran anyway; a suppression nobody justified is a rule "
              "nobody applied\n         fix: `lint-ok: <check> - <why this instance is correct>`",
              file=sys.stderr)

    crit, major, minor = (R.count(s) for s in SEVERITIES)
    print(f"\ndesign-lint: {crit} critical, {major} major, {minor} minor"
          + (f", {len(R.suppressed)} suppressed" if R.suppressed else ""))
    print(f"not checked: {NOT_CHECKED}")
    print("A clean run means no known defect is present. It never means verified.")
    return 1 if (crit or major) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
