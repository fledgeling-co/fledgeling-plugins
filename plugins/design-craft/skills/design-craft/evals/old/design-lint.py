#!/usr/bin/env python3
"""design-lint: deterministic anti-slop checks for design-craft HTML artifacts.

The mechanically-checkable subset of the design-craft review rules (SKILL.md
ch. 6-11, ai-slop-check.md, typesetting.md), so a build loop can catch them
per round without spending a model critique. Stdlib only; runs anywhere the
skill is seeded (Claude Code, CI, a headless sandbox).

Usage:
    python3 design-lint.py file.html [more.html ...]

Exit codes: 0 clean (or minor only) · 1 any critical/major finding.
Findings are heuristics on source text: a "major" is a strong slop signal to
fix or consciously overrule (e.g. the brand genuinely uses Inter), not a law.
"""

import re
import sys

FINDINGS = []  # (severity, file, line, check, detail)
_SEEN = set()


def add(sev, path, line, check, detail):
    key = (path, line, check)
    if key in _SEEN:
        return
    _SEEN.add(key)
    FINDINGS.append((sev, path, line, check, detail))


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def strip_comments(html):
    """Blank out HTML and CSS/JS comments so we don't lint commented-out code
    (keep offsets stable by replacing with spaces)."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    html = re.sub(r"<!--.*?-->", blank, html, flags=re.S)
    html = re.sub(r"/\*.*?\*/", blank, html, flags=re.S)
    return html


def text_content(html):
    """Visible text nodes only (crude): drop script/style, then tags.
    Returns list of (line, text)."""
    no_code = re.sub(r"<(script|style)\b.*?</\1>", lambda m: re.sub(r"[^\n]", " ", m.group(0)), html, flags=re.S | re.I)
    out = []
    for m in re.finditer(r">([^<>]+)<", no_code):
        t = m.group(1).strip()
        if t:
            out.append((lineno(no_code, m.start(1)), t))
    return out


def check_file(path):
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError as e:
        add("critical", path, 0, "unreadable", str(e))
        return
    html = strip_comments(raw)

    # --- content ------------------------------------------------------------
    for m in re.finditer(r"lorem\s+ipsum|\bdolor\s+sit\s+amet\b", html, re.I):
        add("critical", path, lineno(html, m.start()), "placeholder-text",
            "lorem ipsum present — replace with real or honestly-placeheld content")

    # --- colour -------------------------------------------------------------
    for m in re.finditer(r"(?:color|background(?:-color)?)\s*:\s*(#fff(?:fff)?|#000(?:000)?)\b", html, re.I):
        add("major", path, lineno(html, m.start()), "pure-bw",
            f"{m.group(1)} — tone whites/blacks (e.g. #FAFAFA / #1A1A1A), never pure")

    for m in re.finditer(r"linear-gradient\([^)]*\)", html, re.I):
        stops = len(re.findall(r"#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(|oklch\(", m.group(0), re.I))
        if stops >= 3:
            add("major", path, lineno(html, m.start()), "gradient-stops",
                f"{stops}-stop gradient — default to flat colour; max two stops, low contrast, same hue family")

    # unresolved custom properties: var(--x) with no --x: definition anywhere in file
    defined = set(re.findall(r"--([\w-]+)\s*:", html))
    for m in re.finditer(r"var\(\s*--([\w-]+)", html):
        name = m.group(1)
        if name not in defined and not re.search(r"var\(\s*--" + re.escape(name) + r"\s*,", html):
            add("critical", path, lineno(html, m.start()), "unresolved-var",
                f"var(--{name}) has no definition and no fallback — it silently resolves to nothing")

    # --- the default-card tell ----------------------------------------------
    for m in re.finditer(r"\{[^{}]*\}", html, re.S):
        block = m.group(0)
        if re.search(r"border-left\s*:\s*[2-9]px\s+solid", block) and "border-radius" in block:
            add("major", path, lineno(html, m.start()), "default-card",
                "border-radius + border-left accent card — the default-SaaS-template tell; "
                "use shadow, a thin all-around border, or background contrast")

    # --- typography ---------------------------------------------------------
    for m in re.finditer(r"font-family\s*:\s*['\"]?(Inter|Roboto|Arial|Space Grotesk)\b", html):
        add("major", path, lineno(html, m.start()), "default-font",
            f"{m.group(1)} as the leading family — a silent default unless the brand genuinely uses it")

    for m in re.finditer(r"\{[^{}]*text-transform\s*:\s*uppercase[^{}]*\}", html, re.S):
        if "letter-spacing" not in m.group(0):
            add("major", path, lineno(html, m.start()), "untracked-caps",
                "uppercase without letter-spacing — ALL-CAPS labels need 0.06-0.1em tracking")

    for m in re.finditer(r"letter-spacing\s*:\s*(-0?\.\d+)em", html):
        if float(m.group(1)) < -0.04:
            add("major", path, lineno(html, m.start()), "over-tight-tracking",
                f"{m.group(1)}em — below the -0.04em floor; letters touch (cramped, not designed)")

    for ln, t in text_content(html):
        if "..." in t:
            add("minor", path, ln, "three-dots",
                "'...' in visible text — use the real ellipsis character")

    # --- layout / engineering ----------------------------------------------
    for m in re.finditer(r":\s*100vh\b", html):
        add("minor", path, lineno(html, m.start()), "100vh",
            "100vh overflows under mobile browser chrome — use 100dvh")

    for m in re.finditer(r"z-index\s*:\s*(\d{3,})", html):
        if int(m.group(1)) >= 999:
            add("minor", path, lineno(html, m.start()), "zindex-arms-race",
                f"z-index: {m.group(1)} — tokenize the scale (--z-dropdown: 100 … --z-toast: 500)")

    for m in re.finditer(r"<img\b[^>]*>", html, re.I):
        tag = m.group(0)
        if "width" not in tag or "height" not in tag:
            add("minor", path, lineno(html, m.start()), "unsized-img",
                "img without explicit width+height — causes layout shift")

    for m in re.finditer(r"<div\b[^>]*\bonclick\s*=", html, re.I):
        add("major", path, lineno(html, m.start()), "div-as-button",
            "div with onclick — use a real <button> (keyboard, focus, semantics for free)")

    # --- emoji as decoration --------------------------------------------------
    emoji = re.compile("[\U0001F300-\U0001FAFF\U00002728\U00002705\U0001F680\U0001F4C8-\U0001F4CA\U00002B50\U0001F525\U0001F4A1]")
    hits = [(ln, t) for ln, t in text_content(html) if emoji.search(t)]
    if hits:
        ln, t = hits[0]
        add("major", path, ln, "decorative-emoji",
            f"{len(hits)} text node(s) contain emoji (first: \"{t[:40]}…\") — only when the brand "
            "uses them or the emoji is functional; no emoji beats performative emoji")

    # --- self-containment ------------------------------------------------------
    # A page that <link>s a webfont or a CDN script opens in a different typeface
    # offline, behind a strict CSP and inside a sandboxed portal — three of the
    # places a shipped artifact is most often actually read. Measured: one deck
    # carried 3 such requests and its comparison carried 0.
    ext = re.findall(r'(?:href|src)\s*=\s*["\'](https?:)?//[^"\']+', html, re.I)
    if ext:
        add("major", path, lineno(html, html.lower().find("//")), "external-resource",
            f"{len(ext)} external resource request(s) — inline fonts and assets as base64 "
            "so the artifact renders identically offline and under CSP")

    # --- verification output leaked into copy ----------------------------------
    # A surface built to satisfy a checker starts printing the checker's working
    # where the disclosure belongs. Measured: "Constant ratio 1.1765%" beside the
    # legitimate axis note on three slides of one investor deck.
    leak = re.compile(r"constant ratio|scale factor\s*[:=]|zero-?based\s*[:=]\s*true|"
                      r"gate (?:passed|clean)|preflight", re.I)
    for ln, t in text_content(html):
        if leak.search(t):
            add("major", path, ln, "leaked-verification",
                f'"{t[:52]}" — verification arithmetic is not provenance; show the reader '
                "the source, the as-at date and what the axis does, never your proof of compliance")
            break

    # --- hue budget: deliberately NOT checked here -----------------------------
    # Counting hue families is one of the highest-value measurements available
    # (measured: 1 family in a designed artifact against 3 in its generic twin),
    # but it cannot be done honestly from source. A well-tokenised file writes
    # `color: var(--success)` and the hex appears exactly once, in :root, whether
    # that token is used on forty chips or never — so a static count under-reports
    # on precisely the code most worth reviewing, and a rule that cannot fire is
    # indistinguishable from a clean file. Count hue families in the RENDER:
    # `deck-craft/scripts/deck-preflight.js` reports `hueFamilies`, and the same
    # walk works on any page via getComputedStyle.


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    for path in argv[1:]:
        check_file(path)
    order = {"critical": 0, "major": 1, "minor": 2}
    FINDINGS.sort(key=lambda f: (order[f[0]], f[1], f[2]))
    for sev, path, line, check, detail in FINDINGS:
        print(f"{sev.upper():8} {path}:{line}  [{check}]  {detail}")
    crit = sum(1 for f in FINDINGS if f[0] == "critical")
    major = sum(1 for f in FINDINGS if f[0] == "major")
    minor = sum(1 for f in FINDINGS if f[0] == "minor")
    print(f"\ndesign-lint: {crit} critical, {major} major, {minor} minor")
    return 1 if (crit or major) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
