#!/usr/bin/env python3
"""
scan_source.py — greppable anti-patterns in source.

Everything here is deterministic and needs no render. It catches the class of
defect that is invisible at rest in a screenshot but obvious in the stylesheet:
motion that will not be interruptible, content whose visibility is gated on a
transition, focus rings removed without replacement.

Findings carry a tier so the reviewer knows what each is allowed to do:
  1  gate     — deterministic, blocking
  2  finding  — judged, needs evidence
  3  prompt   — attention only, never gates

Usage:
    python scan_source.py src/
    python scan_source.py src/ --json findings.json
    python scan_source.py src/ --tier 1
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

EXTENSIONS = {".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx",
              ".vue", ".svelte", ".astro", ".html"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", "out",
             "coverage", "vendor", ".venv", "__pycache__"}
MAX_BYTES = 2_000_000


@dataclass
class Rule:
    id: str
    tier: int
    pattern: str
    message: str
    fix: str
    why: str
    exts: tuple[str, ...] = ()


RULES: list[Rule] = [
    # ---- Tier 1: motion gates -------------------------------------------
    Rule("transition-all", 1,
         r"transition\s*:\s*all\b",
         "`transition: all` animates every property, including ones you did not intend",
         "Name the properties: `transition-property: transform, opacity`",
         "Unnamed transitions animate layout properties on any future style change, and cost frames"),

    Rule("will-change-all", 1,
         r"will-change\s*:\s*all\b",
         "`will-change: all` promotes everything and defeats the optimisation",
         "`will-change` only on `transform`, `opacity`, `filter` — and remove it after",
         "Blanket promotion costs memory and stops the compositor making useful decisions"),

    Rule("scale-zero-entrance", 1,
         r"scale\(\s*0\s*\)|scale3d\(\s*0\s*,\s*0",
         "Entrance from `scale(0)` — objects do not materialise from a point",
         "Start at `scale(0.9)`–`scale(0.97)` plus `opacity: 0`",
         "A zero-scale entrance reads as a glitch rather than an arrival"),

    Rule("ease-in-on-ui", 1,
         r"transition[^;{]*\bease-in\b(?!-out)",
         "`ease-in` on UI delays the exact moment the user is watching",
         "`ease-out` for entering and exiting; `ease-in-out` for moving on screen",
         "The slow start lands precisely where attention is highest"),

    Rule("animating-layout-props", 1,
         r"transition-property\s*:[^;]*\b(width|height|top|left|right|bottom|margin|padding)\b",
         "Animating a layout property forces reflow every frame",
         "Animate `transform` and `opacity`. For height, the `grid-template-rows: 0fr → 1fr` trick",
         "Layout properties cannot run on the compositor, so they drop frames under load"),

    Rule("outline-none", 1,
         r"outline\s*:\s*(none|0)\b",
         "`outline: none` — check for a replacement focus indicator nearby",
         "`:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }`",
         "Removing the ring without replacing it fails 1.4.11, 2.4.7 and 2.4.13 at once"),

    Rule("hidden-until-animated", 1,
         r"^\s*\.[\w-]+\s*\{[^}]*opacity\s*:\s*0\s*;[^}]*\}",
         "Element hidden at rest — if the reveal is class-triggered, it ships blank",
         "Invert: resting style is the final style; the `from` state lives only in `@keyframes`",
         "Transitions pause in hidden tabs and headless renderers, so gated content is missing from prints, prerenders and screenshots"),

    Rule("transform-origin-center-popover", 3,
         r"transform-origin\s*:\s*center",
         "`transform-origin: center` — wrong for anything anchored to a trigger",
         "Set the origin to the trigger side. Radix and Base UI expose a variable for this",
         "A popover that grows from its own centre reads as unanchored from the control that opened it"),

    # ---- Tier 1: accessibility ------------------------------------------
    Rule("positive-tabindex", 1,
         r'tabindex\s*=\s*["\']?[1-9]',
         "Positive `tabindex` distorts the natural tab order",
         "Use `tabindex=\"0\"` or fix the DOM order",
         "Positive values create a separate tab sequence that almost never matches the visual order"),

    Rule("div-button", 1,
         r'<div[^>]*\brole\s*=\s*["\']button["\']',
         "`role=\"button\"` on a div — check for the keyboard handlers",
         "Use `<button>`, or bind Enter and Space explicitly",
         "The role announces a button; without key handlers nothing happens when a keyboard user presses it"),

    Rule("user-scalable-no", 1,
         r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1\b",
         "Zoom disabled in the viewport meta",
         "Remove `user-scalable=no` and any `maximum-scale=1`",
         "Blocking zoom fails 1.4.4 and is hostile to anyone who needs to enlarge text"),

    Rule("placeholder-as-label", 2,
         r"<input(?![^>]*aria-label)(?![^>]*aria-labelledby)[^>]*placeholder=",
         "Input with a placeholder and no visible label or aria-label",
         "Add a visible `<label for>`. Placeholders are format examples only",
         "Placeholder text disappears the moment the user types, taking the field's meaning with it"),

    Rule("type-number-for-codes", 2,
         r'type\s*=\s*["\']number["\']',
         "`type=\"number\"` — wrong for ZIPs, OTPs and card numbers",
         "`type=\"text\" inputmode=\"numeric\" pattern=\"[0-9]*\"`",
         "It adds spinners, strips leading zeros and applies locale decimal handling"),

    Rule("invalid-pseudo", 2,
         r":invalid\b(?!-)",
         "`:invalid` matches required-but-empty fields on page load",
         "`:user-invalid`, which only matches after the user has interacted",
         "Red borders before anyone typed is the loudest 'validation added without testing' tell"),

    # ---- Tier 1: layout / robustness -------------------------------------
    Rule("vh-unit-fullheight", 1,
         r"(height|min-height)\s*:\s*100vh\b",
         "`100vh` overflows under mobile browser chrome",
         "`100dvh`, or `min-height: 100dvh`",
         "`vh` ignores the dynamic toolbar, so the last 60-100px sit below the fold on mobile"),

    Rule("img-height-attr-with-aspect", 2,
         r"aspect-ratio\s*:",
         "CSS `aspect-ratio` present — check no `<img>` in that slot also carries a `height` attribute",
         "Set `height: auto` in the style so the attribute only seeds the intrinsic ratio",
         "Two definite dimensions means `aspect-ratio` is ignored and the photo silently over-crops"),

    Rule("z-index-arms-race", 2,
         r"z-index\s*:\s*(9{3,}|[1-9]\d{3,})",
         "Ad-hoc high z-index",
         "Tokenise the scale: `--z-dropdown: 100` … `--z-toast: 500`, plus `isolation: isolate` on layered components",
         "An arms race means the stacking order is accidental, and the next component will need 10000"),

    # ---- Tier 2: text and i18n -------------------------------------------
    Rule("fixed-width-button", 2,
         r"\.(btn|button)[^{]*\{[^}]*\bwidth\s*:\s*\d+px",
         "Fixed-width button — German and Finnish expand 35-50%",
         "Intrinsic sizing with padding, or `min-width`",
         "A fixed button width truncates the first time the label is translated"),

    Rule("nowrap-without-ellipsis", 2,
         r"white-space\s*:\s*nowrap(?![^}]*text-overflow)",
         "`nowrap` without an ellipsis safeguard",
         "Add `overflow: hidden; text-overflow: ellipsis`, or allow wrapping",
         "Long real content escapes its container instead of truncating visibly"),

    Rule("justified-body-text", 2,
         r"text-align\s*:\s*justify",
         "Justified text creates rivers on the web",
         "`text-align: start` with a ragged edge",
         "Without hyphenation and proper H&J, justification produces uneven word spacing"),

    Rule("string-concat-plural", 2,
         r'["\'][^"\']*\s\+\s*\w+\s*\+\s*["\']\s*(item|message|result|file|day)s?',
         "String concatenation for a plural — breaks in most languages",
         "ICU plural formats, or `Intl.PluralRules`",
         "Plural rules differ per language; concatenation bakes English grammar into the layout"),

    # ---- Tier 2: imitation material --------------------------------------
    Rule("stacked-inset-bevel", 2,
         r"box-shadow\s*:[^;]*\binset\b[^;]*,[^;]*\binset\b",
         "Stacked inset shadows — the signature of a faked bevel or embossed edge",
         "Use a real asset for the material, or an honestly flat surface with one elevation language",
         "Real elevation says this sits above that; a bevel claims the surface is made of something, and that claim needs an asset to be true"),

    Rule("letterpress-text-shadow", 2,
         r"text-shadow\s*:\s*0\s+(-?1|-?2)px\s+0(px)?\s+",
         "Hard-offset zero-blur `text-shadow` — the faux-letterpress / engraved-text effect",
         "Drop it, or set the type on a real textured asset",
         "The effect imitates ink pressed into paper on a surface with no paper; it reads as machine-made and costs contrast"),

    # ---- Tier 3: prompts, never gates ------------------------------------
    Rule("lorem-ipsum", 3,
         r"\blorem\s+ipsum\b",
         "Lorem ipsum in a surface under review",
         "Real content, or an honest placeholder that names the asset and its dimensions",
         "Placeholder copy hides both layout and comprehension problems"),

    Rule("pure-black-on-white", 3,
         r"#000000|#000\b|rgb\(0,\s*0,\s*0\)",
         "Pure black — worth checking it isn't paired with pure white",
         "Subtly toned near-black, e.g. `#1A1A1A`",
         "Pure black on pure white is harsh and reads as unfinished, though it is not a WCAG failure"),

    Rule("default-font-stack", 3,
         r"font-family\s*:\s*(Inter|Roboto|Arial|Space Grotesk)\b",
         "A commonly-defaulted typeface — check whether it was chosen or inherited",
         "Keep it if the brand specifies it; otherwise a face you can defend in one sentence",
         "A font arrived at before there was a reason is a default, not a decision"),

    Rule("fabricated-stat", 3,
         r"\b(10,?000\+|99\.9%|100%\s+(secure|uptime|satisfaction))",
         "Round-number statistic — check it is real and falsifiable",
         "A specific verifiable figure, or remove it",
         "Unfalsifiable social proof spends the trust the rest of the surface earned"),

    Rule("emoji-in-ui-string", 3,
         r'[">]\s*[\U0001F300-\U0001FAFF✀-➿]\s',
         "Emoji in a UI string — check the brand actually uses them",
         "A real icon from an established set, or improve the typographic hierarchy",
         "Emoji render differently per platform and rarely carry the meaning they're standing in for"),
]


def iter_files(root: Path):
    """Yield scannable files under root, or root itself if it is a file.

    A single-file argument must work: passing one and silently getting zero hits
    is the exact 'coverage is silent' failure this script exists to catch.
    """
    if root.is_file():
        if root.suffix in EXTENSIONS:
            yield root
        else:
            print(f"note: {root.suffix or 'no extension'} is not a scanned type "
                  f"({', '.join(sorted(EXTENSIONS))})", file=sys.stderr)
        return

    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in EXTENSIONS:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            if p.stat().st_size > MAX_BYTES:
                continue
        except OSError:
            continue
        yield p


def scan(root: Path, tier_filter: int | None) -> list[dict]:
    findings = []
    rules = [r for r in RULES if tier_filter is None or r.tier == tier_filter]
    compiled = [(r, re.compile(r.pattern, re.IGNORECASE | re.MULTILINE)) for r in rules]

    for path in iter_files(root):
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        for rule, rx in compiled:
            if rule.exts and path.suffix not in rule.exts:
                continue
            for m in rx.finditer(text):
                line_no = text[: m.start()].count("\n") + 1
                snippet = lines[line_no - 1].strip() if line_no <= len(lines) else ""
                findings.append({
                    "rule": rule.id,
                    "tier": rule.tier,
                    "file": str(path),
                    "line": line_no,
                    "snippet": snippet[:160],
                    "message": rule.message,
                    "fix": rule.fix,
                    "why": rule.why,
                })
    return findings


def main():
    ap = argparse.ArgumentParser(description="Greppable design anti-patterns in source.")
    ap.add_argument("path", help="Source directory or file")
    ap.add_argument("--json", help="Write findings to this path")
    ap.add_argument("--tier", type=int, choices=[1, 2, 3], help="Only this tier")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        sys.exit(f"No such path: {root}")

    findings = scan(root, args.tier)

    scanned = len(list(iter_files(root)))
    if scanned == 0:
        print(f"No scannable files found under {root}.", file=sys.stderr)
        print("Nothing was checked — this is not a clean result.", file=sys.stderr)
        sys.exit(2)

    if args.json:
        Path(args.json).write_text(json.dumps(findings, indent=2))
        print(f"Wrote {len(findings)} findings to {args.json}")

    by_tier: dict[int, list[dict]] = {1: [], 2: [], 3: []}
    for f in findings:
        by_tier[f["tier"]].append(f)

    labels = {1: "TIER 1 — gates (deterministic, blocking)",
              2: "TIER 2 — findings (judged, need evidence)",
              3: "TIER 3 — prompts (attention only, never gate)"}

    for tier in (1, 2, 3):
        items = by_tier[tier]
        if not items:
            continue
        print(f"\n{labels[tier]}")
        grouped: dict[str, list[dict]] = {}
        for f in items:
            grouped.setdefault(f["rule"], []).append(f)
        for rule_id, hits in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
            first = hits[0]
            print(f"\n  {rule_id} — {len(hits)} hit(s)")
            print(f"    {first['message']}")
            print(f"    Fix: {first['fix']}")
            print(f"    Why: {first['why']}")
            for h in hits[:5]:
                print(f"      {h['file']}:{h['line']}  {h['snippet'][:90]}")
            if len(hits) > 5:
                print(f"      … and {len(hits) - 5} more")

    print(f"\n{len(by_tier[1])} gate hits · {len(by_tier[2])} findings · {len(by_tier[3])} prompts")
    if not findings:
        print("No pattern matched. That means no *known* defect is present — it does")
        print("not mean the surface is clean. A rule matching nothing passes silently.")


if __name__ == "__main__":
    main()
