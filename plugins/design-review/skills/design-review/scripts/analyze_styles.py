#!/usr/bin/env python3
"""
analyze_styles.py — systematisation metrics from a computed-style dump.

Measures whether design decisions were *specified* or *defaulted*. That question
survives the argument about whether "AI slop" names a real property of artifacts,
because a surface whose values are ungrouped and undeclared is measurably less
systematic than one whose values trace to tokens — regardless of taste.

Reports counts, implicit scales, outliers and near-misses. It does not decide
severity; it produces the evidence a reviewer reasons over.

Usage:
    python analyze_styles.py <probes-dir-or-file> [--tokens tokens.css] [--json out.json]

    # a whole run
    python analyze_styles.py review-work/probes/

    # one viewport, with token adherence
    python analyze_styles.py review-work/probes/1280x900.json --tokens src/tokens.css
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# A value within ~5% of an existing token reads as "almost right, therefore
# wrong" — colour perception is non-linear, so a near-miss registers as more
# wrong than an obviously different value, which at least might be deliberate.
NEAR_MISS_PCT = 0.05

# Healthy ranges. These are review prompts, not pass/fail gates: a surface can
# exceed them deliberately, and the finding is the absence of a reason.
HEALTHY = {
    "font_sizes": (4, 8),
    "font_weights": (1, 3),
    "colors": (3, 12),
    "radii": (1, 3),
    "shadows": (1, 4),
    "durations": (1, 5),
    "max_widths": (1, 3),
}


def px(value: str) -> float | None:
    if not value:
        return None
    m = re.match(r"^(-?[\d.]+)px$", value.strip())
    return float(m.group(1)) if m else None


def norm_color(value: str) -> str | None:
    """Normalise to rgb()/rgba() with integer channels, dropping fully transparent."""
    if not value:
        return None
    v = value.strip().lower()
    if v in ("transparent", "none", "currentcolor"):
        return None
    m = re.match(r"rgba?\(([^)]+)\)", v)
    if not m:
        return None
    parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
    try:
        nums = [float(p) for p in parts[:4]]
    except ValueError:
        return None
    if len(nums) >= 4 and nums[3] == 0:
        return None
    r, g, b = (int(round(n)) for n in nums[:3])
    if len(nums) >= 4 and nums[3] < 1:
        return f"rgba({r}, {g}, {b}, {nums[3]:g})"
    return f"rgb({r}, {g}, {b})"


def rgb_tuple(c: str) -> tuple[int, int, int] | None:
    m = re.match(r"rgba?\((\d+), (\d+), (\d+)", c)
    return tuple(int(m.group(i)) for i in (1, 2, 3)) if m else None


def color_distance(a: str, b: str) -> float | None:
    """Rough perceptual distance, 0-1. Weighted channels beat plain euclidean."""
    ta, tb = rgb_tuple(a), rgb_tuple(b)
    if not ta or not tb:
        return None
    rmean = (ta[0] + tb[0]) / 2
    dr, dg, db = (ta[i] - tb[i] for i in range(3))
    d = ((2 + rmean / 256) * dr * dr + 4 * dg * dg + (2 + (255 - rmean) / 256) * db * db) ** 0.5
    return d / 765.0


def split_spacing(value: str) -> list[float]:
    out = []
    for part in (value or "").split():
        v = px(part)
        if v is not None and v != 0:
            out.append(v)
    return out


def infer_scale(values: list[float]) -> dict:
    """Detect a 4px or 8px base, and name the values that sit off it.

    A half-step of the base (4 on an 8px scale) is a legitimate scale member,
    not drift — most systems carry one. Counting it as an outlier makes the tool
    cry wolf on well-built surfaces, which is worse than missing a real one.
    """
    if not values:
        return {"base": None, "on_scale": [], "off_scale": []}
    uniq = sorted(set(values))
    for base in (8, 4):
        half = base / 2

        def on_base(v: float) -> bool:
            for step in (base, half):
                if abs(v % step) < 0.51 or abs(step - (v % step)) < 0.51:
                    return True
            return False

        on = [v for v in uniq if on_base(v)]
        if len(on) / len(uniq) >= 0.7:
            return {
                "base": base,
                "coverage": round(len(on) / len(uniq), 2),
                "on_scale": on,
                "off_scale": [v for v in uniq if v not in on],
            }
    return {"base": None, "coverage": 0.0, "on_scale": [], "off_scale": uniq}


def find_near_misses(values: list[float], tol: float = NEAR_MISS_PCT) -> list[dict]:
    """Numeric values close enough to each other to read as a mistake."""
    uniq = sorted(set(values))
    out = []
    for i, a in enumerate(uniq):
        for b in uniq[i + 1:]:
            if a == 0:
                continue
            delta = abs(b - a) / a
            if 0 < delta <= tol:
                out.append({"a": a, "b": b, "delta_pct": round(delta * 100, 1)})
    return out


def find_color_near_misses(colors: list[str], tol: float = 0.04) -> list[dict]:
    """Colours close enough to read as a mistake rather than a decision.

    Near-white and near-black surfaces are excluded: a page background of
    #FFFFFF beside a card surface of #F6F7F9 is a deliberate two-step, and
    flagging it would fire on almost every well-built surface. The finding this
    check exists for is two brand colours a digit apart.
    """
    def is_extreme(c: str) -> bool:
        t = rgb_tuple(c)
        if not t:
            return False
        return min(t) > 235 or max(t) < 24

    candidates = [c for c in sorted(set(colors)) if not is_extreme(c)]
    out = []
    for i, a in enumerate(candidates):
        for b in candidates[i + 1:]:
            d = color_distance(a, b)
            if d is not None and 0 < d <= tol:
                out.append({"a": a, "b": b, "distance": round(d, 4)})
    return sorted(out, key=lambda x: x["distance"])[:40]


def parse_tokens(path: Path) -> dict[str, str]:
    """Pull custom properties from a CSS file, or values from a DTCG/design.md JSON."""
    text = path.read_text(errors="replace")
    tokens: dict[str, str] = {}

    if path.suffix == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return tokens

        def walk(node, prefix=""):
            if isinstance(node, dict):
                if "$value" in node:          # DTCG
                    tokens[prefix] = str(node["$value"])
                    return
                if "value" in node and not isinstance(node["value"], (dict, list)):
                    tokens[prefix] = str(node["value"])
                    return
                for k, v in node.items():
                    if k.startswith("$"):
                        continue
                    walk(v, f"{prefix}.{k}" if prefix else k)

        walk(data)
        return tokens

    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", text):
        tokens[m.group(1)] = m.group(2).strip()
    return tokens


def analyze(nodes: list[dict], tokens: dict[str, str] | None) -> dict:
    font_sizes, weights, line_heights, tracking = [], [], [], []
    colors, bgs, radii, shadows, durations, max_widths, z_indexes = [], [], [], [], [], [], []
    spacing: list[float] = []
    families: Counter = Counter()
    caps_untracked, transition_all, pointer_missing = [], [], []
    tabular_candidates = []

    # Where each metric's values came from, so a zero can be told apart from a
    # channel the engine would not answer. `dumpStyles()` tags every value it
    # recovers with a `*_src` of `computed`, `computed-longhand`, `declared` or
    # `unreadable`; this counts them per metric.
    #
    # The failure this prevents: five metrics here used to read computed
    # properties that return `""` or `0px` on the review engine whatever the CSS
    # said, so `radii.count: 0` and `shadows.distinct_count: 0` reported a
    # perfectly tokenised surface on a page carrying two radii and a shadow.
    # A rule matching nothing passes silently; a metric measuring nothing does too.
    prov = {}

    def note_src(metric, node, key):
        src = node.get(key + "_src")
        if src is None:
            return
        bag = prov.setdefault(metric, Counter())
        bag[src] += 1

    for n in nodes:
        fs = px(n.get("fontSize", ""))
        if fs:
            font_sizes.append(fs)
        if n.get("fontWeight"):
            weights.append(n["fontWeight"])
        if n.get("fontFamily"):
            families[n["fontFamily"].split(",")[0].strip().strip('"\'')] += 1

        lh = px(n.get("lineHeight", ""))
        if lh and fs:
            line_heights.append(round(lh / fs, 3))

        ls = n.get("letterSpacing", "normal")
        note_src("uppercase_untracked", n, "textTransform")
        if n.get("textTransform") == "uppercase" and n.get("hasText"):
            # ALL CAPS needs +0.06 to +0.1em. Untracked caps is one of the two
            # most reliable typographic tells.
            lsv = px(ls) if ls != "normal" else 0.0
            if fs and (lsv is None or lsv / fs < 0.04):
                caps_untracked.append({"selector": n["selector"], "letterSpacing": ls,
                                       "fontSize": n.get("fontSize"),
                                       "source": n.get("textTransform_src")})
        if ls and ls != "normal":
            v = px(ls)
            if v is not None and fs:
                tracking.append(round(v / fs, 4))

        c = norm_color(n.get("color", ""))
        if c and n.get("hasText"):
            colors.append(c)
        b = norm_color(n.get("backgroundColor", ""))
        if b:
            bgs.append(b)

        note_src("radii", n, "borderRadius")
        for r in (n.get("borderRadius") or "").split():
            v = px(r)
            if v:
                radii.append(v)

        note_src("shadows", n, "boxShadow")
        sh = n.get("boxShadow", "none")
        if sh and sh != "none":
            shadows.append(re.sub(r"\s+", " ", sh.strip())[:120])

        for prop in ("margin", "padding"):
            spacing.extend(split_spacing(n.get(prop, "")))
        note_src("gap", n, "gap")
        g = n.get("gap")
        if g and g != "normal":
            spacing.extend(split_spacing(g))

        note_src("durations", n, "transitionDuration")
        td = n.get("transitionDuration", "")
        active_durations = [p.strip() for p in (td or "").split(",")
                            if p.strip() and p.strip() not in ("0s", "0ms")]
        durations.extend(active_durations)

        # `transitionProperty` computes to `all` on every element that has no
        # transition at all, so the property alone proves nothing. Only count it
        # where a non-zero duration means a transition will actually run.
        note_src("transition_all", n, "transitionProperty")
        tp = n.get("transitionProperty", "")
        if tp and "all" in [p.strip() for p in tp.split(",")] and active_durations:
            transition_all.append(n["selector"])

        mw = px(n.get("maxWidth", ""))
        if mw:
            max_widths.append(mw)

        zi = n.get("zIndex", "auto")
        if zi and zi != "auto":
            z_indexes.append(zi)

        if n.get("cursor") == "default" and n.get("tag") in ("div", "li", "article", "section"):
            pointer_missing.append(n["selector"])

        # Changing numbers want tabular figures so digits don't shift as they tick.
        if n.get("hasText") and n.get("fontVariantNumeric") in ("normal", ""):
            tabular_candidates.append(n["selector"])

    def measurability(metric):
        """How this metric's population was obtained, as a reportable state.

        Three outcomes, and the middle one is the whole point:

        - `measured` — every value came from the engine's own computed cascade.
        - `declared` — some or all values came from the stylesheet because the
          computed channel is unreadable here. The count is real, but it is a
          count of what the CSS asked for rather than of what the cascade
          resolved. Weaker, and labelled.
        - `unmeasurable` — no value could be obtained at all. A count of 0 in
          this state means nothing was measured, NOT that the surface is clean,
          and a consumer that prints `0 distinct radii` from it is reporting a
          perfectly tokenised surface on no evidence.
        """
        bag = prov.get(metric)
        if not bag:
            return {"state": "measured", "sources": {}}
        total = sum(bag.values())
        unreadable = bag.get("unreadable", 0)
        declared_n = bag.get("declared", 0)
        if unreadable == total:
            return {"state": "unmeasurable", "sources": dict(bag),
                    "note": "This engine answers neither the computed property nor a "
                            "declaration for it. A zero here is the absence of a "
                            "measurement, not the absence of the thing."}
        if declared_n or unreadable:
            return {"state": "declared", "sources": dict(bag),
                    "note": f"{declared_n} of {total} values came from the stylesheet "
                            f"because the computed channel is unreadable on this engine"
                            + (f"; {unreadable} could not be obtained at all" if unreadable else "")
                            + ". Counts reflect declared intent, not the resolved cascade."}
        return {"state": "measured", "sources": dict(bag)}

    result = {
        "node_count": len(nodes),
        # Per-metric provenance, so no consumer has to guess which zeros are real.
        "measurability": {m: measurability(m) for m in
                          ("uppercase_untracked", "radii", "shadows", "gap",
                           "durations", "transition_all")},
        "typography": {
            "font_families": families.most_common(10),
            "font_sizes": {
                "distinct": sorted(set(font_sizes)),
                "count": len(set(font_sizes)),
                "healthy": HEALTHY["font_sizes"],
                "near_misses": find_near_misses(font_sizes),
                "scale": infer_scale(font_sizes),
            },
            "font_weights": {"distinct": sorted(set(weights)), "count": len(set(weights)),
                             "healthy": HEALTHY["font_weights"]},
            "line_height_ratios": sorted(set(line_heights))[:20],
            "tracking_em": sorted(set(tracking))[:20],
            "uppercase_untracked": caps_untracked[:30],
        },
        "color": {
            "text_colors": {"distinct": sorted(set(colors)), "count": len(set(colors))},
            "background_colors": {"distinct": sorted(set(bgs)), "count": len(set(bgs))},
            "total_distinct": len(set(colors) | set(bgs)),
            "healthy": HEALTHY["colors"],
            "near_misses": find_color_near_misses(list(set(colors) | set(bgs))),
        },
        "spacing": {
            "distinct_count": len(set(spacing)),
            "scale": infer_scale(spacing),
            "near_misses": find_near_misses(spacing)[:40],
        },
        "shape": {
            "radii": {"distinct": sorted(set(radii)), "count": len(set(radii)), "healthy": HEALTHY["radii"]},
            "shadows": {"distinct_count": len(set(shadows)), "sample": sorted(set(shadows))[:8],
                        "healthy": HEALTHY["shadows"]},
            "max_widths": {"distinct": sorted(set(max_widths)), "count": len(set(max_widths)),
                           "healthy": HEALTHY["max_widths"]},
            "z_indexes": {"distinct": sorted(set(z_indexes), key=lambda z: (len(z), z)),
                          "count": len(set(z_indexes)),
                          "ad_hoc": [z for z in set(z_indexes) if z.isdigit() and int(z) >= 999]},
        },
        "motion": {
            "durations": {"distinct": sorted(set(durations)), "count": len(set(durations)),
                          "healthy": HEALTHY["durations"]},
            "transition_all": transition_all[:30],
        },
        "hints": {
            "clickable_looking_without_pointer": pointer_missing[:20],
            "text_without_tabular_nums": len(tabular_candidates),
        },
    }

    if tokens:
        token_values = {v.strip() for v in tokens.values()}
        token_px = {px(v) for v in token_values if px(v) is not None}
        token_colors = {norm_color(v) for v in token_values}
        token_colors.discard(None)

        used_colors = set(colors) | set(bgs)
        off_token_colors = sorted(used_colors - token_colors)
        near_token = []
        for c in off_token_colors:
            for tc in token_colors:
                d = color_distance(c, tc)
                if d is not None and d <= 0.04:
                    near_token.append({"used": c, "near_token_value": tc, "distance": round(d, 4)})
                    break

        off_token_spacing = sorted({s for s in spacing if s not in token_px})
        result["tokens"] = {
            "token_count": len(tokens),
            "colors_not_in_tokens": off_token_colors[:40],
            "colors_near_a_token": near_token[:40],  # snap these; they read as mistakes
            "spacing_not_in_tokens": off_token_spacing[:40],
            "note": "Values near a token are a MORE severe finding than values clearly different from every token.",
        }

    return result


def analyze_label_value_pairs(pairs: list[dict]) -> dict:
    """Grade label/value pairs the probe found.

    Three outcomes, and the middle one is the interesting case:
      inverted  — label renders larger than the value. A defect.
      flat      — neither outranks the other. The pair reads as one blob.
      weak      — value outranks by ONE vector only. Survives today, collapses
                  the moment that vector is normalised.

    Hierarchy wants at least two vectors moving together (craft-visual.md §1),
    so a value that leads on weight alone is a real if minor finding — and it
    is the one an eye misses, because on screen it does look bolder.
    """
    inverted, flat, weak, no_tabular = [], [], [], []
    for p in pairs:
        lab, val = p["label"], p["value"]
        bigger = val["fontSize"] > lab["fontSize"]
        heavier = val["fontWeight"] > lab["fontWeight"]
        if lab["fontSize"] > val["fontSize"]:
            inverted.append(p)
        elif not bigger and not heavier:
            flat.append(p)
        elif bigger != heavier:          # exactly one vector
            weak.append({**p, "vector": "size" if bigger else "weight"})
        if not val["tabularNums"]:
            no_tabular.append(p)
    return {
        "count": len(pairs),
        "inverted": inverted[:20],
        "flat": flat[:20],
        "weak_single_vector": weak[:20],
        "missing_tabular_nums": no_tabular[:20],
    }


def summarize(a: dict) -> list[str]:
    lines = []
    # Measurability first, because it decides which of the lines below mean
    # anything. A metric reported `unmeasurable` and then summarised as a count
    # is the exact failure this block exists to stop: the summary is the only
    # part of this output most reviewers read.
    m = a.get("measurability") or {}
    dark = [k for k, v in m.items() if v.get("state") == "unmeasurable"]
    declared = [k for k, v in m.items() if v.get("state") == "declared"]
    if dark:
        lines.append(f"! UNMEASURABLE on this engine: {', '.join(sorted(dark))} — "
                     f"a zero for these is the absence of a measurement, not a clean "
                     f"surface. Do not report them as counts.")
    if declared:
        lines.append(f"~ {', '.join(sorted(declared))} recovered from the stylesheet "
                     f"rather than the computed cascade — counts reflect declared "
                     f"intent. Say 'declared' when quoting them.")

    # The distinct-value counts themselves, printed unconditionally.
    #
    # `systematisation.md` tells a reviewer to "count distinct type sizes, spacing
    # values, colours, radii, shadows and durations" and names this script as the
    # instrument. It only ever printed the values that BREACHED a healthy range,
    # so a reviewer following the reference had to recompute the counts by hand
    # from the probe JSON — which is what happened on a real run. A count inside a
    # healthy range is still the measurement the reference asked for, and printing
    # it is also what makes the denominator visible: `radii 2` and a silent line
    # are different claims.
    t0 = a["typography"]
    sh0, mo0, co0, sp0 = a["shape"], a["motion"], a["color"], a["spacing"]

    def band(n, healthy):
        lo, hi = healthy
        return "" if lo <= n <= hi else f" (healthy {lo}-{hi})"

    counts = [
        f"type sizes {t0['font_sizes']['count']}{band(t0['font_sizes']['count'], t0['font_sizes']['healthy'])}",
        f"weights {t0['font_weights']['count']}{band(t0['font_weights']['count'], t0['font_weights']['healthy'])}",
        f"colours {co0['total_distinct']}{band(co0['total_distinct'], co0['healthy'])}",
        f"spacing {sp0['distinct_count']}",
        f"radii {sh0['radii']['count']}{band(sh0['radii']['count'], sh0['radii']['healthy'])}",
        f"shadows {sh0['shadows']['distinct_count']}{band(sh0['shadows']['distinct_count'], sh0['shadows']['healthy'])}",
        f"durations {mo0['durations']['count']}{band(mo0['durations']['count'], mo0['durations']['healthy'])}",
        f"max-widths {sh0['max_widths']['count']}{band(sh0['max_widths']['count'], sh0['max_widths']['healthy'])}",
        f"z-indexes {sh0['z_indexes']['count']}",
    ]
    # A metric measured off a dead channel must not appear here as a number.
    for metric, label in (("radii", "radii"), ("shadows", "shadows"), ("durations", "durations")):
        if (m.get(metric) or {}).get("state") == "unmeasurable":
            counts = [c for c in counts if not c.startswith(label + " ")]
            counts.append(f"{label} UNMEASURABLE")
    lines.append("distinct values — " + " · ".join(counts))

    t = a["typography"]
    fs = t["font_sizes"]
    lo, hi = fs["healthy"]
    if fs["count"] > hi:
        lines.append(f"{fs['count']} distinct font sizes (healthy {lo}-{hi}) — check for an implicit scale and outliers")
    if fs["near_misses"]:
        lines.append(f"{len(fs['near_misses'])} font-size near-misses, e.g. {fs['near_misses'][0]['a']}px vs {fs['near_misses'][0]['b']}px")
    if t["font_weights"]["count"] > 4:
        lines.append(f"{t['font_weights']['count']} font weights — three (read/emphasize/announce) usually does the work")
    if t["uppercase_untracked"]:
        lines.append(f"{len(t['uppercase_untracked'])} uppercase runs without tracking — needs +0.06 to +0.1em")

    sp = a["spacing"]["scale"]
    if sp["base"]:
        if sp["off_scale"]:
            lines.append(f"spacing base {sp['base']}px ({sp['coverage']:.0%} coverage); off-scale: {sp['off_scale'][:8]}")
    else:
        lines.append("no consistent 4px or 8px spacing base detected — values look ad-hoc")

    c = a["color"]
    if c["total_distinct"] > c["healthy"][1]:
        lines.append(f"{c['total_distinct']} distinct colours (healthy {c['healthy'][0]}-{c['healthy'][1]})")
    if c["near_misses"]:
        n = c["near_misses"][0]
        lines.append(f"{len(c['near_misses'])} colour near-misses, e.g. {n['a']} vs {n['b']} — snap to one token")

    sh = a["shape"]
    if sh["radii"]["count"] > 3:
        lines.append(f"{sh['radii']['count']} border-radius values — a 4th is drift, not a scale")
    if sh["max_widths"]["count"] > 3:
        lines.append(f"{sh['max_widths']['count']} content max-widths — rails shifting between sections read as incoherent")
    if sh["z_indexes"]["ad_hoc"]:
        lines.append(f"ad-hoc z-index values {sh['z_indexes']['ad_hoc']} — tokenise the scale")

    if a["motion"]["transition_all"]:
        lines.append(f"{len(a['motion']['transition_all'])} elements using `transition: all` — name the properties")
    if a["motion"]["durations"]["count"] > 5:
        lines.append(f"{a['motion']['durations']['count']} distinct transition durations — mixed timings read as unintentional")

    tok = a.get("tokens")
    if tok:
        if tok["colors_near_a_token"]:
            lines.append(f"{len(tok['colors_near_a_token'])} colours sit near a token but don't match it — highest-severity drift")
        if tok["colors_not_in_tokens"]:
            lines.append(f"{len(tok['colors_not_in_tokens'])} colours trace to no token")
        if tok["spacing_not_in_tokens"]:
            lines.append(f"{len(tok['spacing_not_in_tokens'])} spacing values trace to no token")

    lv = a.get("label_value_pairs")
    if lv and lv["count"]:
        if lv["inverted"]:
            lines.append(f"{len(lv['inverted'])} label/value pairs INVERTED — label renders larger than the value")
        if lv["flat"]:
            lines.append(f"{len(lv['flat'])} label/value pairs flat — neither outranks the other")
        if lv["weak_single_vector"]:
            v = ", ".join(sorted({p["vector"] for p in lv["weak_single_vector"]}))
            lines.append(f"{len(lv['weak_single_vector'])} label/value pairs lead on {v} alone — collapses if that vector is normalised")
        if lv["missing_tabular_nums"]:
            lines.append(f"{len(lv['missing_tabular_nums'])} numeric values without tabular-nums — digits will shift as they change")

    return lines


def main():
    ap = argparse.ArgumentParser(description="Systematisation metrics from a probe dump.")
    ap.add_argument("input", help="probes/ directory or a single probe JSON file")
    ap.add_argument("--tokens", help="tokens.css, DTCG .json, or design.md front matter")
    ap.add_argument("--json", help="write full analysis to this path")
    args = ap.parse_args()

    path = Path(args.input)
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    if not files:
        sys.exit(f"No probe JSON found at {path}")

    tokens = parse_tokens(Path(args.tokens)) if args.tokens else None
    if args.tokens and not tokens:
        print(f"note: no tokens parsed from {args.tokens}", file=sys.stderr)

    everything = {}
    empty = []
    for f in files:
        data = json.loads(f.read_text())
        nodes = data.get("styles", [])
        if not nodes:
            # `styles: null` is what run_probes writes when dumpStyles did not
            # run. Counting that file as "no outliers" is the silent-coverage
            # failure scan_source.py already exits non-zero over.
            empty.append(f.name)
            continue
        result = analyze(nodes, tokens)
        pairs = (data.get("semantics") or {}).get("labelValuePairs") or []
        if pairs:
            result["label_value_pairs"] = analyze_label_value_pairs(pairs)
        everything[f.stem] = result

    if args.json:
        Path(args.json).write_text(json.dumps(everything, indent=2))
        print(f"Wrote {args.json}")

    for viewport, a in everything.items():
        print(f"\n=== {viewport} ({a['node_count']} visible nodes) ===")
        obs = summarize(a)
        if obs:
            for line in obs:
                print(f"  · {line}")
        else:
            print("  · no systematisation outliers detected")

    print("\nThese are observations, not findings. A surface may exceed a healthy")
    print("range deliberately — the finding is an outlier with no reason behind it.")

    if empty:
        print(f"\n! {len(empty)} probe file(s) carried no style dump: {', '.join(empty)}",
              file=sys.stderr)
        print("  dumpStyles did not run for those viewports. Nothing was analysed for",
              file=sys.stderr)
        print("  them — this is not a clean result.", file=sys.stderr)
    if not everything:
        # Zero analysed and exit 0 is a gate that never ran reporting success.
        sys.exit("Nothing was analysed — this is not a clean result.")


if __name__ == "__main__":
    main()
