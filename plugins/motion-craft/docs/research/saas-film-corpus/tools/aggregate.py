"""Aggregate every findings.json + metrics.json in the corpus into one digest.

    python3 -P aggregate.py > digest.md        (also writes corpus.json beside it)
"""
import collections
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path.home() / "Movies" / "motion-craft-corpus"
rows = []
for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name != "tools"):
    f, m = d / "findings.json", d / "measure" / "metrics.json"
    if not f.exists():
        continue
    try:
        fj = json.loads(f.read_text())
        mj = json.loads(m.read_text()) if m.exists() else {}
    except Exception:
        continue
    rows.append((d.name, fj, mj))

ok = [(i, f, m) for i, f, m in rows if f.get("status") != "failed"]
(ROOT / "corpus.json").write_text(json.dumps([{"id": i, "findings": f, "metrics": m} for i, f, m in rows], indent=1))


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x >= 0


def dist(vals, unit=""):
    v = sorted(x for x in vals if num(x))
    if not v:
        return "n=0"
    q = lambda p: v[min(len(v) - 1, int(round(p * (len(v) - 1))))]
    return f"n={len(v)} median {st.median(v):.2f}{unit} (p25 {q(.25):.2f}, p75 {q(.75):.2f}, range {v[0]:.2f}-{v[-1]:.2f})"


def by(key_fn, vals_fn, label, unit=""):
    groups = collections.defaultdict(list)
    for i, f, m in ok:
        groups[key_fn(i, f, m)].append(vals_fn(i, f, m))
    return [f"  - {label} {k}: {dist(v, unit)}" for k, v in sorted(groups.items())]


brand = lambda i, f, m: f.get("brand", "?")
fmt = lambda i, f, m: f.get("format", "?")
dur = lambda i, f, m: m.get("duration_s")
out = [f"# Corpus digest: {len(rows)} findings, {len(ok)} usable, {len(rows) - len(ok)} failed", ""]
out.append("## Mix")
out.append("- brands: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("brand") for _, f, _ in ok).most_common()))
out.append("- formats: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("format") for _, f, _ in ok).most_common()))
out.append("- voiceover: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("transcript", {}).get("voiceover") for _, f, _ in ok).most_common()))
out.append("- duration: " + dist([dur(*r) for r in ok], " s"))
out += by(brand, dur, "duration", " s")

out += ["", "## Rhythm (measured)"]
R = lambda k: (lambda i, f, m: (m.get("rhythm") or {}).get(k))
for k, u in (("cuts_per_min", ""), ("median_shot_s", " s"), ("first_cut_s", " s")):
    out.append(f"- {k}: " + dist([R(k)(*r) for r in ok], u))
    out += by(brand, R(k), k, u)
    out += by(fmt, R(k), k, u)
ls = [((m.get("rhythm") or {}).get("longest_shot") or {}).get("share_of_runtime") for _, _, m in ok]
out.append("- longest unbroken shot as share of runtime: " + dist(ls))
nb = [len((m.get("rhythm") or {}).get("bursts") or []) for _, _, m in ok]
out.append(f"- films with at least one burst (>=5 cuts in 5 s): {sum(1 for x in nb if x)}/{len(nb)}")
mids = [b["mid_share"] for _, _, m in ok for b in (m.get("rhythm") or {}).get("bursts") or []]
out.append("- burst midpoints as share of runtime: " + dist(mids))
out.append("- route (analyst): " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("rhythm", {}).get("route") for _, f, _ in ok).most_common()))
F = lambda k: (lambda i, f, m: (m.get("frames") or {}).get(k))
out.append("- share of 2 s intervals that are a new composition: " + dist([F("intervals_new_composition_share")(*r) for r in ok]))
out.append("- share of 2 s intervals with <2 % pixel change: " + dist([F("intervals_static_share")(*r) for r in ok]))
out.append("- longest static run: " + dist([F("longest_static_run_s")(*r) for r in ok], " s"))
out.append("- dark-frame share: " + dist([F("dark_share")(*r) for r in ok]) + "; light-frame share: " + dist([F("light_share")(*r) for r in ok]))
out += by(brand, F("light_share"), "light-frame share")

out += ["", "## Structure (analyst)"]
hero = [f.get("structure", {}).get("hero_moment", {}).get("share") for _, f, _ in ok]
out.append("- hero moment as share of runtime: " + dist(hero))
out.append("- logo hold at end: " + dist([f.get("structure", {}).get("ending", {}).get("logo_hold_s") for _, f, _ in ok], " s"))
roles = collections.Counter(b.get("role") for _, f, _ in ok for b in f.get("structure", {}).get("beats", []))
out.append("- beat roles used: " + ", ".join(f"{k} {v}" for k, v in roles.most_common()))
first = collections.Counter((f.get("structure", {}).get("beats") or [{}])[0].get("role") for _, f, _ in ok)
out.append("- first beat role: " + ", ".join(f"{k} {v}" for k, v in first.most_common()))
share = collections.defaultdict(list)
for _, f, m in ok:
    D = m.get("duration_s") or f.get("duration_s")
    for b in f.get("structure", {}).get("beats", []):
        if num(b.get("start_s")) and num(b.get("end_s")) and D:
            share[b.get("role")].append((b["end_s"] - b["start_s"]) / D)
for k, v in sorted(share.items(), key=lambda kv: -len(kv[1])):
    out.append(f"  - share of runtime per {k} beat: {dist(v)}")
out.append("- frame 0 (analyst text):")
for i, f, _ in ok:
    out.append(f"  - {i} [{f.get('brand')}]: {f.get('structure', {}).get('frame0')}")

out += ["", "## Look and type"]
th = [x for _, f, _ in ok for x in (f.get("look", {}).get("title_height_pct") or [])]
out.append("- title height % of frame (min and max per film pooled): " + dist(th))
out.append("- max words per title line: " + dist([f.get("look", {}).get("max_words_per_title_line") for _, f, _ in ok]))
out.append("- density: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("look", {}).get("density") for _, f, _ in ok).most_common()))
out += by(brand, lambda i, f, m: (m.get("look") or {}).get("saturation"), "saturation")
out += by(brand, lambda i, f, m: (m.get("look") or {}).get("warmth"), "warmth")

out += ["", "## Product UI"]
out.append("- UI presence % of runtime: " + dist([f.get("product_ui", {}).get("presence_pct_runtime") for _, f, _ in ok]))
out += by(brand, lambda i, f, m: f.get("product_ui", {}).get("presence_pct_runtime"), "UI presence %")
out.append("- shown as: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(s for _, f, _ in ok for s in f.get("product_ui", {}).get("shown_as", [])).most_common()))
out.append("- cursor: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("product_ui", {}).get("cursor") for _, f, _ in ok).most_common()))
out.append("- legible at phone width: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f.get("product_ui", {}).get("legible_at_phone_width") for _, f, _ in ok).most_common()))

out += ["", "## Transitions"]
tc = collections.Counter()
tf = collections.Counter()
kinds = []
for _, f, _ in ok:
    ts = f.get("motion", {}).get("transitions", [])
    kinds.append(len({t.get("type") for t in ts}))
    for t in ts:
        tc[t.get("type")] += t.get("count") or 0
        tf[t.get("type")] += 1
out.append("- kinds per film: " + dist(kinds))
out.append("- films using each type (total count): " + ", ".join(f"{k} {tf[k]} ({tc[k]})" for k, _ in tf.most_common()))

out += ["", "## Sound (measured)"]
S = lambda k: (lambda i, f, m: (m.get("sound") or {}).get(k))
for k, u, neg in (("lufs_integrated", " LUFS", True), ("true_peak_db", " dBTP", True), ("lra_lu", " LU", False), ("strong_onsets_per_min", "", False)):
    vals = [S(k)(*r) for r in ok]
    if neg:
        vals = [-v if isinstance(v, (int, float)) else None for v in vals]
    out.append(f"- {k}{' (negated, so 14 means -14)' if neg else ''}: " + dist(vals, u))
out += by(brand, lambda i, f, m: -((m.get("sound") or {}).get("lufs_integrated") or 1), "LUFS (negated)")
al = [(S("cuts_on_strong_onset_share")(*r), S("chance_share")(*r)) for r in ok]
al = [(a, c) for a, c in al if num(a) and num(c)]
out.append(f"- cuts on a strong onset: median {st.median(a for a, _ in al):.2f} vs chance median {st.median(c for _, c in al):.2f}; films >0.10 above chance: {sum(1 for a, c in al if a - c > 0.10)}/{len(al)}" if al else "- cut/onset alignment: n=0")
out.append("- sound kind: " + ", ".join(f"{k} {v}" for k, v in collections.Counter((m.get("sound") or {}).get("kind") for _, _, m in ok).most_common()))
out.append("- words per minute (VO films): " + dist([f.get("transcript", {}).get("words_per_minute") for _, f, _ in ok if f.get("transcript", {}).get("voiceover") != "none-music-only"]))

out += ["", "## Rule candidates by skill rule and relation"]
rc = collections.defaultdict(list)
for i, f, _ in ok:
    for r in f.get("rule_candidates", []):
        rc[(r.get("skill_rule", "none")[:12], r.get("relation"))].append(f"{r.get('rule')} [{i}: {r.get('evidence')}]")
for (k, rel), v in sorted(rc.items(), key=lambda kv: (kv[0][0], kv[0][1] or "")):
    out.append(f"### {k} / {rel} ({len(v)})")
    out += [f"- {x}" for x in v]
print("\n".join(out))
