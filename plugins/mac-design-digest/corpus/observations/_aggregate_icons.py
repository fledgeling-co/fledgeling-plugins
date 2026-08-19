#!/usr/bin/env python3
"""Aggregate every observations/*-icon.json into corpus-level icon statistics.

Written for the Mac Design Archivist. Measurement honesty: this script only
counts and groups what the per-icon observers already recorded. Hue bucketing is
derived (marked 'derived' in output); no new taste claims are minted here.
Candidate style families are keyword-signature groupings of the observers'
rhymes_hint / devices / adjectives text — they are (candidate/recurring), NOT
promoted canon (canon needs >=3 independent NATIVE-lineage apps; icon
observations carry no lineage field, so nativeCount is reported as 0).
"""
import json, glob, re, colorsys, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(HERE, "*-icon.json")))

icons = []
for f in files:
    with open(f) as fh:
        icons.append(json.load(fh))

N = len(icons)

# ---------------------------------------------------------------- era
era_dist = Counter(d.get("era", "MISSING") for d in icons)

# ---------------------------------------------------------------- rubric score
score_dist = Counter(d.get("rubric_score", "MISSING") for d in icons)
scores_num = [d["rubric_score"] for d in icons if isinstance(d.get("rubric_score"), (int, float))]
score_stats = {
    "min": min(scores_num), "max": max(scores_num),
    "mean": round(sum(scores_num) / len(scores_num), 2),
    "median": sorted(scores_num)[len(scores_num) // 2],
    "n": len(scores_num),
}

# ---------------------------------------------------------------- failures / soft_passes by check #
check_re = re.compile(r"#(\d+)")
fail_by_check = Counter()
fail_members = defaultdict(list)
soft_by_check = Counter()
for d in icons:
    for fl in d.get("failures", []):
        m = check_re.search(fl)
        if m:
            n = int(m.group(1))
            fail_by_check[n] += 1
            fail_members[n].append(d["slug"])
        else:
            fail_by_check[-1] += 1
            fail_members[-1].append(d["slug"])
    for sp in d.get("soft_passes", []):
        m = check_re.search(sp)
        if m:
            soft_by_check[int(m.group(1))] += 1

total_failures = sum(len(d.get("failures", [])) for d in icons)
icons_with_failures = sum(1 for d in icons if d.get("failures"))
clean_icons = [d["slug"] for d in icons if not d.get("failures")]

# ---------------------------------------------------------------- palette / hue families
hex_re = re.compile(r"#([0-9A-Fa-f]{6})")

def hue_family(hx):
    r = int(hx[0:2], 16) / 255.0
    g = int(hx[2:4], 16) / 255.0
    b = int(hx[4:6], 16) / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.12:  # achromatic axis
        if v < 0.18: return "black/near-black"
        if v > 0.85: return "white/near-white"
        return "grey/silver"
    deg = h * 360
    if deg < 15 or deg >= 345: return "red"
    if deg < 40: return "orange"
    if deg < 65: return "yellow"
    if deg < 90: return "chartreuse/lime"
    if deg < 160: return "green"
    if deg < 195: return "cyan/teal"
    if deg < 240: return "blue"
    if deg < 275: return "indigo/violet"
    if deg < 320: return "magenta/purple"
    return "pink/rose"

bg_hue = Counter(); glyph_hue = Counter(); accent_hue = Counter(); all_hue = Counter()
for d in icons:
    pal = d.get("palette", {})
    for hx in hex_re.findall(str(pal.get("background", ""))):
        fam = hue_family(hx); bg_hue[fam] += 1; all_hue[fam] += 1
    glyphs = pal.get("glyph", [])
    if isinstance(glyphs, str): glyphs = [glyphs]
    for gv in glyphs:
        for hx in hex_re.findall(str(gv)):
            fam = hue_family(hx); glyph_hue[fam] += 1; all_hue[fam] += 1
    acc = pal.get("accent", "")
    for hx in hex_re.findall(str(acc)):
        fam = hue_family(hx); accent_hue[fam] += 1; all_hue[fam] += 1

# accent present vs none
accent_none = sum(1 for d in icons if str(d.get("palette", {}).get("accent", "")).strip().lower() in ("none", "", "none (monochromatic)"))

# background field: ramp vs flat vs scene vs glass (from composition.background_type, normalised)
def norm_bg(bt):
    bt = (bt or "").lower()
    if bt.startswith("ramp"): return "ramp"
    if bt.startswith("flat"): return "flat"
    if "none" in bt or "transparent" in bt: return "none/transparent"
    if "scene" in bt: return "scene"
    if "glass" in bt: return "glass-layers"
    return bt or "unknown"

# ---------------------------------------------------------------- composition cross-tabs
bt_c = Counter(); gt_c = Counter(); od_c = Counter()
combo_c = Counter()
combo_members = defaultdict(list)
bt_x_gt = Counter()
for d in icons:
    c = d.get("composition", {})
    bt = norm_bg(c.get("background_type"))
    gt = (c.get("glyph_type") or "unknown").lower()
    od = (c.get("overlay_device") or "unknown").lower()
    bt_c[bt] += 1; gt_c[gt] += 1; od_c[od] += 1
    bt_x_gt[(bt, gt)] += 1
    key = f"{bt} | {gt} | {od}"
    combo_c[key] += 1
    combo_members[key].append(d["slug"])

# ---------------------------------------------------------------- light model
def light_bucket(lm):
    s = (lm or "").lower()
    if "flat" in s or "null" in s:
        return "flat/null"
    has_top = "top-down" in s or "top down" in s
    has_glass = "specular" in s or "refract" in s or "glass" in s or "sheen" in s or "gloss" in s or "bloom" in s
    has_emis = "emissive" in s or "glow" in s or "self-lit" in s or "luminous" in s or "self-illum" in s
    if has_emis:
        return "emissive/self-lit"
    if has_top and has_glass:
        return "top-down soft + specular/glass"
    if has_top:
        return "top-down soft"
    if has_glass:
        return "specular/glass (no explicit top-down)"
    return "other/unclassified"

light_dist = Counter(light_bucket(d.get("light_model")) for d in icons)

# ---------------------------------------------------------------- devices: slug -> devices
device_map = {d["slug"]: d.get("devices", []) for d in icons}
# device-motif keyword frequency (coarse)
device_kw = Counter()
DEV_KWS = {
    "double-read/pun glyph": ["double-read", "double reading", "pun", "doubl"],
    "subject-mined literal object": ["subject-mined", "literal", "front-facing"],
    "monogram/letterform fusion": ["monogram", "letterform", "numeral", "initial", "wordmark"],
    "mascot/face personification": ["mascot", "face", "eyes", "creature", "character", "personif"],
    "diagonal-tool overlay": ["diagonal", "tool overlay"],
    "concentric/radial motif": ["concentric", "radial", "ring", "aperture", "dial"],
    "negative-space cut": ["negative-space", "negative space", "knockout", "knocked out", "cut from"],
    "glass/refraction material": ["specular", "refraction", "glass", "translucent", "frosted"],
    "device/hardware portrait": ["laptop", "keycap", "keyboard", "notch", "display", "screen", "hardware", "bezel"],
    "emissive glow focal": ["emissive", "glow", "luminous", "self-lit", "bloom"],
}
for d in icons:
    blob = " ".join(d.get("devices", [])).lower()
    for label, kws in DEV_KWS.items():
        if any(k in blob for k in kws):
            device_kw[label] += 1

# ---------------------------------------------------------------- adjectives
adj_freq = Counter()
for d in icons:
    for a in d.get("adjectives", []):
        adj_freq[a.strip().lower()] += 1

# ---------------------------------------------------------------- candidate style families (keyword signatures over rhymes_hint + devices + adjectives)
# Each family = (label, [keyword substrings]). An icon joins if any keyword matches its combined text.
# These are CANDIDATE/RECURRING groupings, not canon.
FAMILIES = [
    ("flat-monochrome-logomark (Vercel/Linear register)",
     ["monochrome logo-mark", "monochrome brand-mark", "vercel", "linear-register", "linear-monogram",
      "web logo as app icon", "logo-as-app-icon", "logo-on-near-black", "monogram-on-flat", "flat monochrome brand",
      "achromatic dev", "flat single-letter brand", "reductive monochrome", "brand logo poured", "monochrome letterform"]),
    ("dark-field emissive-object (glow-on-black)",
     ["emissive-orb", "single-luminous-object", "luminous object", "glow on near-black", "glowing on near-black",
      "glowing gradient blob", "emissive form on void", "emissive focal", "glow-on-black", "luminous-emblem",
      "spotlight one glassy luminous", "glowing brand mark", "neon-glyph-on-void", "self light source"]),
    ("charcoal-squircle single-white-glyph (dark mono-minimal utility)",
     ["charcoal squircle", "near-black charcoal", "white glyph centred on", "white symbol family",
      "single white glyph", "white glyph on a near-black", "dark minimalist utility tile", "black squircle + single",
      "dark-field monochrome line-glyph", "silver/white geometric mark", "mono-minimal-dark", "charcoal-squircle + single white"]),
    ("Liquid-Glass frosted-glass-glyph/object",
     ["frosted-glass", "liquid-glass", "liquid glass", "clear-glass", "glass wedge", "glass-wedge", "glass blob",
      "glass over an emissive", "extruded glass", "glass rod", "translucent glass", "frosted-slab", "dark-glass monogram"]),
    ("Big-Sur single-object-on-gradient-squircle utility",
     ["single-object utility", "single system-object", "single nameable object", "object-at-an-angle", "object on a saturated gradient",
      "object staged over a saturated gradient", "single-object-on-field", "object-on-gradient", "big sur object",
      "menu-bar power-utility", "front-facing squircle", "single-object-", "object-metaphor big sur", "warm-gradient single-object"]),
    ("Big-Sur diagonal-tool / cleaner-maintenance",
     ["diagonal-tool", "diagonal tool", "cleanmymac", "cleaner/maintenance", "broom", "sparkles on a saturated",
      "maintenance mark", "content-on-a-surface", "device being serviced"]),
    ("skeuomorphic / photoreal literal-object",
     ["skeuomorphic", "photoreal", "photo-real", "photographic material", "chrome 3d emblem", "metallic-on-black",
      "polished-metal", "instrument-gauge", "tachometer", "hardware-render", "literal real-world object",
      "aqua glass-button", "web-2.0 gel", "gloss", "diegetic-monogram", "app-as-appliance", "rendered-object"]),
    ("3D-render / claymorphism (Blender/Spline)",
     ["claymorph", "blender", "spline", "3d-render", "3d clay", "clay/plastic", "puffy object", "soft-render",
      "matte-clay", "3d-object", "rendered-3d-object", "3d glass/chrome/liquid-metal", "molten-glass", "candy/clay-render",
      "soft-3d object", "3d-rendered", "iconscout", "icons8"]),
    ("mascot / character / creature",
     ["mascot", "creature", "character", "cartoon", "animal-mascot", "emoji-face", "sticker", "personified", "pixar-render",
      "friendly-face", "friendly bot", "cute creature", "sprite"]),
    ("scene / diorama / app-UI-as-icon",
     ["scene-diorama", "scene / diorama", "app-ui-as-icon", "app-UI-as-icon", "window-motif", "mini-desktop",
      "illustrated-scene", "landscape-vignette", "full-bleed scene", "photo-hero", "scene ico", "diorama"]),
    ("device-portrait / notch / framed-screen utility",
     ["notch", "menu-bar utility icons that depict", "device-portrait", "depict the mac hardware", "framed-screen",
      "framed-window", "device bezel", "notchnook", "boring-boring", "screen inside a device", "phone/display inside a device",
      "framed-tile", "literal-ui-depiction", "ui-mimic"]),
    ("monogram editorial / serif-initial",
     ["serif init", "editorial single-glyph monogram", "fashion-house serif", "bodoni", "didot", "letterpress",
      "hand-lettered monogram", "museum placard", "editorial/luxury single-glyph"]),
    ("spectrum-gradient organic brand-blob (Arc/Raycast/Siri-orb)",
     ["spectrum-gradient", "spectral orb", "siri-orb", "siri orb", "arc browser", "raycast-class gradient", "organic shape poure",
      "mesh-gradient", "oil-slick", "iridescent-gradient", "aurora", "holographic"]),
    ("AI violet->blue gradient glass-blob dev/agent",
     ["violet->blue", "violet-blue", "violet/blue", "indigo->royal", "periwinkle->royal", "ai/agent app icon", "ai-assistant",
      "glowing-glass-card", "gradient glass blob", "glass blobs on a light", "ai-app icon family", "electric purple->blue"]),
    ("data-viz / ring-chart emblem",
     ["data-viz", "disk-usage", "disk analyser", "ring-chart", "segmented-ring", "daisydisk", "grandperspective",
      "renders its own output as the mark", "chart/meter", "stats tool", "monitor"]),
    ("single-glyph-on-single-hue gradient (monochromatic tint)",
     ["single-glyph-on-single-hue", "single-hue gradient", "monochromatic single-hue", "single white glyph on a vertical",
      "monogram-on-gradient-squircle", "sf-symbol glyph on a", "glyph-on-indigo-gradient", "blue->indigo gradient squircle",
      "saturated-gradient squircle + white line-glyph", "vertical-blue ramp"]),
    ("flat two-tone / geometric-glyph indie utility",
     ["flat two-tone", "two-tone geometric", "flat vector face", "braun/rams", "max-bill", "functionalist",
      "flat monochrome utility mark", "notation-mark glyph", "typographic", "flat glyph-on-solid-tile", "recoloured-system-symbol",
      "flat single-glyph-on-solid", "flat single-object glyph"]),
]

fam_members = defaultdict(list)
icon_fam = defaultdict(list)
for d in icons:
    blob = (d.get("rhymes_hint", "") + " || " + " ".join(d.get("devices", [])) + " || " + " ".join(d.get("adjectives", []))).lower()
    for label, kws in FAMILIES:
        if any(k.lower() in blob for k in kws):
            fam_members[label].append(d["slug"])
            icon_fam[d["slug"]].append(label)

unassigned = sorted(s for s in device_map if s not in icon_fam)
multi = {s: fams for s, fams in icon_fam.items() if len(fams) > 1}

fam_ranked = sorted(((lab, sorted(set(m))) for lab, m in fam_members.items()),
                    key=lambda x: -len(x[1]))
candidate_families = [(lab, m) for lab, m in fam_ranked if len(m) >= 2]

# ---------------------------------------------------------------- assemble JSON
agg = {
    "meta": {
        "n_icons": N,
        "source_glob": "observations/*-icon.json",
        "note": "Icon observations carry no framework-lineage field; nativeCount=0. "
                "Hue families are DERIVED by HSV bucketing of observer-recorded hex. "
                "Candidate style families are keyword-signature groupings of observer text "
                "(rhymes_hint+devices+adjectives) — (candidate/recurring), not promoted canon.",
    },
    "era_distribution": dict(era_dist.most_common()),
    "rubric_score": {"distribution": {str(k): v for k, v in sorted(score_dist.items(), key=lambda x: (isinstance(x[0], str), x[0]))},
                     "stats": score_stats},
    "failures": {
        "total_failure_lines": total_failures,
        "icons_with_at_least_one_failure": icons_with_failures,
        "icons_clean_no_failures": len(clean_icons),
        "by_check_number": {str(k): v for k, v in sorted(fail_by_check.items(), key=lambda x: -x[1])},
        "by_check_number_members": {str(k): sorted(set(v)) for k, v in sorted(fail_members.items(), key=lambda x: -len(x[1]))},
        "soft_pass_by_check_number": {str(k): v for k, v in sorted(soft_by_check.items(), key=lambda x: -x[1])},
        "clean_icon_members": sorted(clean_icons),
    },
    "palette": {
        "background_field_type": dict(bt_c.most_common()),
        "accent_none_count": accent_none,
        "hue_families_derived": {
            "background_hexes": dict(bg_hue.most_common()),
            "glyph_hexes": dict(glyph_hue.most_common()),
            "accent_hexes": dict(accent_hue.most_common()),
            "all_hexes_combined": dict(all_hue.most_common()),
        },
    },
    "composition": {
        "background_type_marginal": dict(bt_c.most_common()),
        "glyph_type_marginal": dict(gt_c.most_common()),
        "overlay_device_marginal": dict(od_c.most_common()),
        "background_x_glyph": {f"{a} x {b}": v for (a, b), v in bt_x_gt.most_common()},
        "background_x_glyph_x_overlay_top": {k: v for k, v in combo_c.most_common(25)},
        "background_x_glyph_x_overlay_members": {k: sorted(v) for k, v in combo_members.items() if len(v) >= 2},
    },
    "light_model_distribution": dict(light_dist.most_common()),
    "device_motif_keyword_frequency": dict(device_kw.most_common()),
    "device_map": {s: device_map[s] for s in sorted(device_map)},
    "adjective_frequency": dict(adj_freq.most_common()),
    "candidate_icon_style_families": [
        {"family": lab, "n": len(m), "members": m} for lab, m in candidate_families
    ],
    "family_assignment": {
        "icons_assigned": len(icon_fam),
        "icons_unassigned": unassigned,
        "icons_in_multiple_families": {s: sorted(f) for s, f in sorted(multi.items())},
    },
}

with open(os.path.join(HERE, "_aggregate-icon.json"), "w") as fh:
    json.dump(agg, fh, indent=2)

# ---------------------------------------------------------------- markdown
def bar(n, total, width=30):
    filled = int(round(width * n / total)) if total else 0
    return "#" * filled + "." * (width - filled)

md = []
md.append("# Icon corpus aggregate")
md.append("")
md.append(f"_{N} icon observations aggregated from `observations/*-icon.json`._  ")
md.append("Icons carry no framework-lineage field, so **nativeCount = 0** and no rule here is "
          "promoted to macOS canon. Hue families are **derived** (HSV bucketing of observer hex). "
          "Style families are **candidate/recurring** keyword groupings of observer text, not canon "
          "(canon needs >=3 independent NATIVE-lineage apps).")
md.append("")

md.append("## Era distribution")
md.append("")
md.append("| era | n | share |")
md.append("|---|---|---|")
for k, v in era_dist.most_common():
    md.append(f"| {k} | {v} | {v/N:.0%} |")
md.append("")

md.append("## Rubric score distribution")
md.append("")
md.append(f"min {score_stats['min']} / median {score_stats['median']} / mean {score_stats['mean']} / max {score_stats['max']} (n={score_stats['n']})")
md.append("")
md.append("| score | n | bar |")
md.append("|---|---|---|")
for k in sorted(score_dist, key=lambda x: (isinstance(x, str), x)):
    v = score_dist[k]
    md.append(f"| {k} | {v} | {bar(v, N)} |")
md.append("")

md.append("## Failure frequency by rubric check")
md.append("")
md.append(f"{total_failures} failure lines across {icons_with_failures}/{N} icons; "
          f"{len(clean_icons)} icons ship clean (no failures).")
md.append("")
md.append("| check | failures | members |")
md.append("|---|---|---|")
for k, v in sorted(fail_by_check.items(), key=lambda x: -x[1]):
    label = f"#{k}" if k != -1 else "(no #)"
    mem = ", ".join(sorted(set(fail_members[k]))[:12])
    if len(set(fail_members[k])) > 12:
        mem += f" (+{len(set(fail_members[k]))-12})"
    md.append(f"| {label} | {v} | {mem} |")
md.append("")
md.append("### Soft-pass (near-miss) frequency by check")
md.append("")
md.append("| check | soft passes |")
md.append("|---|---|")
for k, v in sorted(soft_by_check.items(), key=lambda x: -x[1]):
    md.append(f"| #{k} | {v} |")
md.append("")

md.append("## Palette")
md.append("")
md.append("### Background field type")
md.append("")
md.append("| type | n |")
md.append("|---|---|")
for k, v in bt_c.most_common():
    md.append(f"| {k} | {v} |")
md.append("")
md.append(f"Accent recorded as none/monochromatic: **{accent_none}/{N}**.")
md.append("")
md.append("### Dominant hue families (derived, HSV bucketing of hex)")
md.append("")
md.append("| hue family | background | glyph | accent | all |")
md.append("|---|---|---|---|---|")
allfams = sorted(all_hue, key=lambda x: -all_hue[x])
for fam in allfams:
    md.append(f"| {fam} | {bg_hue.get(fam,0)} | {glyph_hue.get(fam,0)} | {accent_hue.get(fam,0)} | {all_hue.get(fam,0)} |")
md.append("")

md.append("## Composition")
md.append("")
md.append("### Marginals")
md.append("")
md.append("**background_type**: " + ", ".join(f"{k} {v}" for k, v in bt_c.most_common()))
md.append("")
md.append("**glyph_type**: " + ", ".join(f"{k} {v}" for k, v in gt_c.most_common()))
md.append("")
md.append("**overlay_device**: " + ", ".join(f"{k} {v}" for k, v in od_c.most_common()))
md.append("")
md.append("### background_type x glyph_type")
md.append("")
md.append("| background | glyph | n |")
md.append("|---|---|---|")
for (a, b), v in bt_x_gt.most_common():
    md.append(f"| {a} | {b} | {v} |")
md.append("")
md.append("### Top background x glyph x overlay combinations")
md.append("")
md.append("| background \\| glyph \\| overlay | n |")
md.append("|---|---|")
for k, v in combo_c.most_common(20):
    md.append(f"| {k} | {v} |")
md.append("")

md.append("## Light model distribution")
md.append("")
md.append("| model | n |")
md.append("|---|---|")
for k, v in light_dist.most_common():
    md.append(f"| {k} | {v} |")
md.append("")

md.append("## Device-motif keyword frequency")
md.append("")
md.append("| motif | n |")
md.append("|---|---|")
for k, v in device_kw.most_common():
    md.append(f"| {k} | {v} |")
md.append("")

md.append("## Adjective frequency")
md.append("")
md.append("| adjective | n |")
md.append("|---|---|")
for k, v in adj_freq.most_common():
    md.append(f"| {k} | {v} |")
md.append("")

md.append("## Candidate icon style families (>=2 members, keyword-signature grouping)")
md.append("")
md.append("_Overlap is expected and recorded — icons can belong to several families. "
          "These are (candidate/recurring), promotable only with lineage evidence the icon layer lacks._")
md.append("")
md.append("| family | n | members |")
md.append("|---|---|---|")
for lab, m in candidate_families:
    md.append(f"| {lab} | {len(m)} | {', '.join(m)} |")
md.append("")
md.append(f"Icons assigned to >=1 family: **{len(icon_fam)}/{N}**. "
          f"Unassigned (idiosyncratic / thin signal): {', '.join(unassigned) if unassigned else 'none'}.")
md.append("")

md.append("## Device map (slug -> devices)")
md.append("")
for s in sorted(device_map):
    devs = device_map[s]
    md.append(f"- **{s}**: " + ("; ".join(devs) if devs else "(none recorded)"))
md.append("")

with open(os.path.join(HERE, "_aggregate-icon.md"), "w") as fh:
    fh.write("\n".join(md))

# ---------------------------------------------------------------- console summary
print(f"icons={N}")
print("era:", dict(era_dist.most_common()))
print("score stats:", score_stats)
print("fail by check (top):", dict(sorted(fail_by_check.items(), key=lambda x:-x[1])[:6]))
print("bg field:", dict(bt_c.most_common()))
print("glyph type:", dict(gt_c.most_common()))
print("overlay:", dict(od_c.most_common()))
print("light:", dict(light_dist.most_common()))
print("candidate families >=2:", [(l, len(m)) for l, m in candidate_families])
print("unassigned:", unassigned)
