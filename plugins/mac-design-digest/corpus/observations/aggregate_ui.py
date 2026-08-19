#!/usr/bin/env python3
"""Aggregate every observations/*-ui.json into machine + human readable rollups.
Run from the observations/ directory. Author: Mac Design Archivist synthesis pass.
"""
import json, glob, collections, re, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

NATIVE_LINEAGES = {"native", "swiftui-native", "swiftui"}

# ---------- normalizers ----------

def norm_law(head_raw, full):
    """Map a psychology entry to a canonical law name."""
    h = full.lower()
    if h.startswith("aesthetic") or "aesthetic-usability" in h or "aesthetic usability" in h:
        return "Aesthetic-usability effect"
    if "jakob" in h:
        return "Jakob's Law (familiarity)"
    if "hick" in h:
        return "Hick's Law (choice cost)"
    if "von restorff" in h or "isolation effect" in h:
        return "Von Restorff effect (isolation/salience)"
    if "fitts" in h:
        return "Fitts's Law (target size/distance)"
    if "miller" in h or "cowan" in h or "chunk" in h:
        return "Miller/Cowan chunking (working memory)"
    if "recognition over recall" in h or ("recognition" in h and "recall" in h):
        return "Recognition over recall"
    if "serial" in h or "peak" in h and "end" in h:
        return "Serial-position / Peak-end"
    if "peak" in h and "end" in h:
        return "Peak-end rule"
    if "fluency" in h or "processing fluency" in h:
        return "Processing fluency"
    if "tesler" in h:
        return "Tesler's Law (conservation of complexity)"
    if "progressive disclosure" in h:
        return "Progressive disclosure"
    if "zeigarnik" in h or "goal-gradient" in h or "goal gradient" in h or ("goal" in h and "gradient" in h):
        return "Zeigarnik / Goal-gradient"
    if "fogg" in h or "b=map" in h or "b = map" in h:
        return "Fogg behaviour model (B=MAP)"
    if "information scent" in h or "scent" in h:
        return "Information scent"
    if "hierarchy via de" in h or ("hierarchy" in h and "de-emphasis" in h) or "refactoring ui" in h:
        return "Hierarchy via de-emphasis (Refactoring UI)"
    if "pragnanz" in h or "gestalt" in h or "proximity" in h or "figure-ground" in h or "figure/ground" in h or "common region" in h or "closure" in h:
        return "Gestalt principles (proximity/figure-ground)"
    if "signal detection" in h or "signal-detection" in h:
        return "Von Restorff effect (isolation/salience)"
    if "forgiveness" in h or "undo" in h:
        return "Forgiveness / reversibility"
    if "doherty" in h:
        return "Doherty threshold (responsiveness)"
    if "occam" in h:
        return "Occam's razor / minimalism"
    if "first" in h and "impression" in h:
        return "First-impression / 50ms appeal"
    if "selective attention" in h or "pre-attentive" in h or "preattentive" in h or "peripheral" in h:
        return "Pre-attentive / peripheral-vision capture"
    if "demonstrate" in h and "describe" in h:
        return "Demonstrate-don't-describe / description-experience gap"
    if "description-experience" in h or "description experience" in h:
        return "Demonstrate-don't-describe / description-experience gap"
    if "loss" in h and ("aversion" in h or "framing" in h or "frame" in h):
        return "Loss aversion / emotional framing"
    if "colour-never-alone" in h or "color-never-alone" in h or "color-as-sole" in h or "colour-as-sole" in h or ("color" in h and "alone" in h):
        return "Colour-never-alone (redundant coding)"
    if "picture superiority" in h:
        return "Picture superiority"
    if "spatial memory" in h or "method of loci" in h or "automaticity" in h:
        return "Spatial memory / automaticity"
    if "social proof" in h or "social facilitation" in h or "co-presence" in h or "cialdini" in h:
        return "Social proof / Cialdini persuasion"
    if "choice overload" in h or "choice-overload" in h:
        return "Choice-overload calibration"
    if "data-ink" in h or "data ink" in h:
        return "Data-ink minimalism (Tufte)"
    if "natural mapping" in h:
        return "Natural mapping"
    # fallback: cleaned head
    head = re.split(r'\s*[—:(]|\s-\s', full, maxsplit=1)[0].strip()
    return head[:48] if head else "(unparsed)"


CLUSTER_RULES = [
    # (normalized name, [keyword substrings]) — first match wins, order = priority
    ("brand / non-native / marketing-register (do-not-seed-canon)", [
        "brand-only", "do-not-cluster", "do not cluster", "do not conflate", "not conflate",
        "not a macos", "not a native", "marketing", "insufficient evidence", "insufficient for a ui",
        "not-yet-clusterable", "no macos ui", "not a ui", "brand cluster", "brand family",
        "brand register", "brand surface", "non-native", "unresolved-brand", "brand-poster",
        "gradient-marketing", "web brand", "brand aesthetic", "brand-crystalline", "brand-drenched",
        "n/a for app ui", "if a brand corpus", "web/marketing", "productivity-web-crisp", "command-driven-web",
    ]),
    ("notch / dynamic-island utility", [
        "notch", "dynamic-island", "dynamic island", "live-activity", "live activity", "island",
    ]),
    ("developer / terminal-dark tool", [
        "terminal", "ide", "developer-dark", "developer dark", "cosmic-console", "neon-instrument",
        "ai-chat", "ai chat", "acid-terminal", "instrument-dark", "developer productivity", "console",
    ]),
    ("warm-editorial / writing & reading", [
        "editorial", "writing", "reader", "-paper", " paper", "drafting", "mono-canvas", "notes)",
        "quiet-dark-notes", "monochrome-workspace",
    ]),
    ("gallery / content-forward", [
        "gallery", "content-mosaic", "content-forward", "media-dark", "media", "mosaic",
    ]),
    ("glass / translucent utility", [
        "glass", "translucent", "vibrancy", "liquid-glass", "liquid glass", "ambient",
    ]),
    ("warm consumer utility", [
        "warm-consumer", "warm consumer", "warm-charcoal", "warm-glass", "warm creator", "warm-dark",
        "wellness", "calm-nudge", "consumer-glossy", "friendly-dark", "friendly-paper", "playful",
        "warm-accent", "warm-brand", "warm-terminal",
    ]),
    ("menu-bar utility", [
        "menu-bar", "menubar", "menu bar", "popover", "launcher", "system-deferential", "graphite-menubar",
    ]),
    ("native-system-idiom utility", [
        "native-settings", "system-default", "system-settings", "native-utility", "native-faithful",
        "native workspace", "spatial-canvas", "native-pro", "native-minimal", "system-vibrancy",
        "system-adjacent", "achromatic-utility", "config pane", "file-rules",
    ]),
    ("electric / accent-dark utility", [
        "electric-dark", "electric", "achromatic", "black-control", "dark-hud", "hud",
    ]),
]

def norm_cluster(hint):
    h = (hint or "").lower()
    for name, kws in CLUSTER_RULES:
        for kw in kws:
            if kw in h:
                return name
    return "unclustered / other"


def norm_token_group(name):
    """Group value list by exact token name (already structured prefix/name)."""
    return name.strip()


# ---------- aggregation ----------

files = sorted(f for f in glob.glob('*-ui.json') if not os.path.basename(f).startswith('_'))
apps = []
for f in files:
    with open(f) as fh:
        apps.append(json.load(fh))

lineage_dist = collections.Counter()
lineage_conf = collections.defaultdict(lambda: collections.Counter())
era_dist = collections.Counter()
rubric_scores = []
native_scores = []
rubric_by_lineage = collections.defaultdict(list)
token_freq = collections.defaultdict(lambda: {"count": 0, "apps": [], "values": []})
pattern_freq = collections.defaultdict(lambda: {"count": 0, "apps": []})
defect_freq = collections.defaultdict(lambda: {"count": 0, "apps": []})
signature_moves = []  # {slug, move}
cluster_groups = collections.defaultdict(lambda: {
    "members": [], "adjectives": collections.Counter(), "directions": [],
    "peers": collections.Counter(), "raw_hints": collections.Counter(), "native_members": []})
law_freq = collections.defaultdict(lambda: {"count": 0, "apps": []})
mode_dist = collections.Counter()
surface_type_dist = collections.Counter()

marketing_only = []   # no scorable UI surface
real_ui = []          # >=1 scorable UI surface

def defect_key(d):
    """Anti-pattern name = text before first em-dash / open paren."""
    k = re.split(r'\s*[—(]|\s-\s', d, maxsplit=1)[0].strip()
    return k[:70] if k else d[:70]

for d in apps:
    slug = d["slug"]
    lin = d.get("lineage", "unknown")
    conf = d.get("lineage_confidence", "?")
    lineage_dist[lin] += 1
    lineage_conf[lin][conf] += 1
    era_dist[d.get("era", "unknown")] += 1

    max_rubric = 0
    for s in d.get("surfaces", []):
        rs = s.get("rubric_score", 0) or 0
        ns = s.get("native_audit_score", 0) or 0
        mode_dist[s.get("mode", "?").split()[0] if s.get("mode") else "?"] += 1
        st = s.get("surface_type", "")
        # coarse surface-type bucket
        stl = st.lower()
        if "marketing" in stl or "og social" in stl or "opengraph" in stl:
            surface_type_dist["marketing-composite"] += 1
        elif "icon" in stl and "surface" not in stl.split("icon")[0][-12:]:
            surface_type_dist["app-icon"] += 1
        elif "settings" in stl or "preferences" in stl:
            surface_type_dist["settings"] += 1
        elif "empty" in stl:
            surface_type_dist["empty-state"] += 1
        elif "onboard" in stl:
            surface_type_dist["onboarding"] += 1
        elif "sidebar" in stl or "three-pane" in stl or "split" in stl:
            surface_type_dist["main-window (sidebar/split)"] += 1
        elif "menu-bar" in stl or "menubar" in stl or "popover" in stl or "notch" in stl:
            surface_type_dist["menu-bar / notch popover"] += 1
        else:
            surface_type_dist["other/main-window"] += 1
        if rs > 0:
            rubric_scores.append(rs)
            rubric_by_lineage[lin].append(rs)
        if ns > 0:
            native_scores.append(ns)
        max_rubric = max(max_rubric, rs)

    if max_rubric == 0:
        marketing_only.append(slug)
    else:
        real_ui.append(slug)

    seen_tokens = set()
    for t in d.get("tokens", []):
        tn = norm_token_group(t.get("token", "?"))
        rec = token_freq[tn]
        if slug not in seen_tokens:
            pass
        rec["count"] += 1
        if slug not in rec["apps"]:
            rec["apps"].append(slug)
        rec["values"].append({"app": slug, "value": t.get("value", ""), "quality": t.get("quality", "?")})

    for p in d.get("patterns", []):
        pn = p.get("pattern", "?").strip().lower()
        pattern_freq[pn]["count"] += 1
        if slug not in pattern_freq[pn]["apps"]:
            pattern_freq[pn]["apps"].append(slug)

    for de in d.get("defects", []):
        k = defect_key(de)
        defect_freq[k]["count"] += 1
        if slug not in defect_freq[k]["apps"]:
            defect_freq[k]["apps"].append(slug)

    for m in d.get("signature_moves", []):
        signature_moves.append({"slug": slug, "move": m})

    a = d.get("aesthetic", {})
    hint = a.get("cluster_hint", "")
    cn = norm_cluster(hint)
    g = cluster_groups[cn]
    g["members"].append(slug)
    g["raw_hints"][hint] += 1
    for adj in a.get("adjectives", []):
        g["adjectives"][adj] += 1
    if a.get("direction"):
        g["directions"].append({"app": slug, "direction": a["direction"]})
    for pr in a.get("peers", []):
        g["peers"][pr] += 1
    if lin in NATIVE_LINEAGES:
        g["native_members"].append(slug)

    seen_laws = set()
    for p in d.get("psychology", []):
        head = re.split(r'\s*[—:(]', p, maxsplit=1)[0].strip()[:45]
        law = norm_law(head, p)
        if law in seen_laws:
            continue
        seen_laws.add(law)
        law_freq[law]["count"] += 1
        law_freq[law]["apps"].append(slug)

native_slugs = [d["slug"] for d in apps if d.get("lineage") in NATIVE_LINEAGES]

def scoredist(vals):
    if not vals:
        return {"n": 0}
    c = collections.Counter(vals)
    return {
        "n": len(vals), "min": min(vals), "max": max(vals),
        "mean": round(statistics.mean(vals), 2), "median": statistics.median(vals),
        "histogram": dict(sorted(c.items())),
    }

# order helpers
def order_freq(dd):
    return dict(sorted(dd.items(), key=lambda kv: (-kv[1]["count"], kv[0])))

token_out = {}
for tn, rec in sorted(token_freq.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
    token_out[tn] = {"app_count": len(rec["apps"]), "apps": rec["apps"], "values": rec["values"]}

cluster_out = {}
for cn, g in sorted(cluster_groups.items(), key=lambda kv: -len(kv[1]["members"])):
    cluster_out[cn] = {
        "member_count": len(g["members"]),
        "members": g["members"],
        "native_member_count": len(g["native_members"]),
        "native_members": g["native_members"],
        "top_adjectives": g["adjectives"].most_common(12),
        "top_peers": g["peers"].most_common(12),
        "raw_hints": dict(g["raw_hints"]),
        "directions": g["directions"],
    }

aggregate = {
    "meta": {
        "total_apps": len(apps),
        "total_surfaces": sum(len(d.get("surfaces", [])) for d in apps),
        "generated_by": "aggregate_ui.py (Mac Design Archivist synthesis)",
        "canon_rule": ">=3 independent NATIVE-lineage apps, no contradiction = canon; native lineages = " + ", ".join(sorted(NATIVE_LINEAGES)),
    },
    "lineage_distribution": {
        "counts": dict(lineage_dist.most_common()),
        "by_confidence": {k: dict(v) for k, v in lineage_conf.items()},
        "native_lineage_count": len(native_slugs),
        "native_slugs": native_slugs,
    },
    "era_distribution": dict(era_dist.most_common()),
    "rubric_score_distribution": scoredist(rubric_scores),
    "native_audit_score_distribution": scoredist(native_scores),
    "rubric_by_lineage": {k: scoredist(v) for k, v in sorted(rubric_by_lineage.items())},
    "mode_distribution": dict(mode_dist.most_common()),
    "surface_type_distribution": dict(surface_type_dist.most_common()),
    "token_frequency": token_out,
    "pattern_frequency": order_freq(pattern_freq),
    "defect_frequency": order_freq(defect_freq),
    "signature_moves": signature_moves,
    "cluster_hint_groups": cluster_out,
    "psychology_law_frequency": order_freq(law_freq),
    "evidence_class": {
        "marketing_only_no_scorable_ui": {"count": len(marketing_only), "slugs": sorted(marketing_only)},
        "real_ui_evidence": {"count": len(real_ui), "slugs": sorted(real_ui)},
    },
}

with open("_aggregate-ui.json", "w") as f:
    json.dump(aggregate, f, indent=2)

# ---------- human-readable markdown ----------
def pct(n, d):
    return f"{100*n/d:.0f}%" if d else "0%"

L = []
L.append("# UI Observation Aggregate — Mac Design Archivist synthesis")
L.append("")
L.append(f"Aggregated from **{len(apps)} apps** / **{aggregate['meta']['total_surfaces']} surfaces** "
         f"(`observations/*-ui.json`). Machine-readable twin: `_aggregate-ui.json`.")
L.append("")
L.append("Canon gate: a rule is canon only with >=3 independent **native-lineage** apps and no contradiction. "
         "Native lineage here = `native` (+ `swiftui-native` if present). "
         "`web-electron` / `catalyst` / `ios-on-mac` feed the tells-and-corrections record, never macOS canon.")
L.append("")

L.append("## Lineage distribution")
L.append("")
L.append("| lineage | apps | share | confidence (high/med/low) |")
L.append("|---|---|---|---|")
for lin, n in lineage_dist.most_common():
    c = lineage_conf[lin]
    L.append(f"| {lin} | {n} | {pct(n,len(apps))} | {c.get('high',0)}/{c.get('med',0)}/{c.get('low',0)} |")
L.append("")
L.append(f"**Native-lineage apps: {len(native_slugs)} of {len(apps)} ({pct(len(native_slugs),len(apps))})** — the canon-eligible pool.")
L.append("")

L.append("## Era distribution")
L.append("")
L.append("| era | apps |")
L.append("|---|---|")
for e, n in era_dist.most_common():
    L.append(f"| {e} | {n} |")
L.append("")

L.append("## Rubric & native-audit score distributions")
L.append("")
rd, nd = aggregate["rubric_score_distribution"], aggregate["native_audit_score_distribution"]
L.append(f"- **Rubric (14-pt), scorable surfaces only (n={rd.get('n',0)})**: "
         f"min {rd.get('min')}, median {rd.get('median')}, mean {rd.get('mean')}, max {rd.get('max')}.")
L.append(f"- **Native-audit (10-pt), n={nd.get('n',0)}**: "
         f"min {nd.get('min')}, median {nd.get('median')}, mean {nd.get('mean')}, max {nd.get('max')}.")
L.append("")
L.append("Rubric histogram (score: count): " + ", ".join(f"{k}:{v}" for k, v in rd.get("histogram", {}).items()))
L.append("")
L.append("Native-audit histogram (score: count): " + ", ".join(f"{k}:{v}" for k, v in nd.get("histogram", {}).items()))
L.append("")
L.append("Rubric mean by lineage (scorable surfaces): " +
         ", ".join(f"{k} {v['mean']} (n={v['n']})" for k, v in aggregate["rubric_by_lineage"].items() if v.get('n')))
L.append("")

L.append("## Evidence class — real UI vs marketing/brand-only")
L.append("")
L.append(f"- **Real-UI evidence (>=1 scorable surface): {len(real_ui)} apps.**")
L.append(f"- **Marketing/brand-only (no scorable UI surface): {len(marketing_only)} apps** — brand-evidence-only, "
         "treat tokens as brand/icon evidence, never UI canon:")
L.append("  " + ", ".join(sorted(marketing_only)))
L.append("")

L.append("## Mode & surface-type coverage")
L.append("")
L.append("Mode (per surface): " + ", ".join(f"{k} {v}" for k, v in mode_dist.most_common()))
L.append("")
L.append("Surface types: " + ", ".join(f"{k} {v}" for k, v in surface_type_dist.most_common()))
L.append("")

L.append("## Pattern frequency (apps evidencing)")
L.append("")
L.append("| pattern | apps |")
L.append("|---|---|")
for k, v in aggregate["pattern_frequency"].items():
    L.append(f"| {k} | {v['count']} |")
L.append("")

L.append("## Token frequency (top 30 by app coverage)")
L.append("")
L.append("| token | apps |")
L.append("|---|---|")
for tn, rec in list(token_out.items())[:30]:
    L.append(f"| `{tn}` | {rec['app_count']} |")
L.append("")
L.append("Full per-token value lists (every member) live in `_aggregate-ui.json` -> `token_frequency`.")
L.append("")

L.append("## Defect frequency (anti-pattern -> apps)")
L.append("")
L.append("| anti-pattern (name) | apps |")
L.append("|---|---|")
for k, v in list(aggregate["defect_frequency"].items())[:30]:
    L.append(f"| {k} | {v['count']} |")
L.append("")

L.append("## Aesthetic cluster-hint groups (normalised)")
L.append("")
L.append("Raw `cluster_hint` strings are near-unique free text; grouped by keyword theme. "
         "`native` = members with native lineage (the canon-eligible subset of each cluster).")
L.append("")
L.append("| normalised cluster | members | native | top adjectives |")
L.append("|---|---|---|---|")
for cn, g in cluster_out.items():
    adjs = ", ".join(a for a, _ in g["top_adjectives"][:5])
    L.append(f"| {cn} | {g['member_count']} | {g['native_member_count']} | {adjs} |")
L.append("")
for cn, g in cluster_out.items():
    if g["member_count"] < 2:
        continue
    L.append(f"### {cn}  ({g['member_count']} members, {g['native_member_count']} native)")
    L.append("")
    L.append("- **Members:** " + ", ".join(g["members"]))
    if g["native_members"]:
        L.append("- **Native (canon-eligible):** " + ", ".join(g["native_members"]))
    L.append("- **Adjectives:** " + ", ".join(f"{a}({n})" for a, n in g["top_adjectives"][:8]))
    L.append("- **Peer references:** " + ", ".join(f"{p}({n})" for p, n in g["top_peers"][:8]))
    L.append("")

L.append("## Psychology-law frequency")
L.append("")
L.append("| law / heuristic | apps |")
L.append("|---|---|")
for k, v in aggregate["psychology_law_frequency"].items():
    if v["count"] >= 2:
        L.append(f"| {k} | {v['count']} |")
L.append("")
L.append("(single-app laws omitted here; full list in JSON.)")
L.append("")

L.append("## Signature moves (app -> move)")
L.append("")
L.append(f"{len(signature_moves)} recorded signature moves across the corpus; full list in "
         "`_aggregate-ui.json` -> `signature_moves`. A sample:")
L.append("")
for sm in signature_moves[:20]:
    move = sm["move"] if len(sm["move"]) < 160 else sm["move"][:157] + "..."
    L.append(f"- **{sm['slug']}** — {move}")
L.append("")

with open("_aggregate-ui.md", "w") as f:
    f.write("\n".join(L))

print("WROTE _aggregate-ui.json + _aggregate-ui.md")
print("apps:", len(apps), "native:", len(native_slugs), "marketing-only:", len(marketing_only))
print("clusters>=2:", [k for k, v in cluster_out.items() if v["member_count"] >= 2])
