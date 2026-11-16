"""Per-type and per-brand tables for the motion-craft SaaS film reference.

    python3.14 -P types.py            (reads corpus.json beside tools/)
"""
import collections
import json
import statistics as st
from pathlib import Path

C = json.loads((Path.home() / "Movies/motion-craft-corpus/corpus.json").read_text())


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def med(v, nd=1):
    v = sorted(x for x in v if num(x))
    if not v:
        return "-"
    q = lambda p: v[min(len(v) - 1, int(round(p * (len(v) - 1))))]
    return f"{st.median(v):.{nd}f} ({q(.25):.{nd}f}-{q(.75):.{nd}f})"


def kind(c):
    f = c["findings"]
    vo = f["transcript"]["voiceover"]
    d = c["metrics"]["duration_s"]
    if f["format"] in ("customer-or-user-story",):
        return "customer story"
    if vo in ("on-camera-presenter", "presenter-and-vo", "narrator-vo"):
        return "narrated explainer or tutorial"
    if d <= 45:
        return "short announcement (<=45 s)"
    return "music-led feature film"


groups = collections.defaultdict(list)
for c in C:
    groups[kind(c)].append(c)
groups["ALL"] = C
print("| type | n | length s | cuts/min | median shot s | longest shot share | static 2s share | UI % runtime | LUFS |")
print("|---|---|---|---|---|---|---|---|---|")
for k, cs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    m = [c["metrics"] for c in cs]
    f = [c["findings"] for c in cs]
    print(f"| {k} | {len(cs)} | {med([x['duration_s'] for x in m], 0)} | {med([x['rhythm']['cuts_per_min'] for x in m])} | "
          f"{med([x['rhythm']['median_shot_s'] for x in m])} | {med([(x['rhythm'].get('longest_shot') or {}).get('share_of_runtime') for x in m], 2)} | "
          f"{med([(x.get('frames') or {}).get('intervals_static_share') for x in m], 2)} | {med([y['product_ui']['presence_pct_runtime'] for y in f], 0)} | "
          f"{med([(x.get('sound') or {}).get('lufs_integrated') for x in m])} |")
print()
print("brand counts:", collections.Counter(c["findings"]["brand"] for c in C))
print("bursts:", sum(1 for c in C if c["metrics"]["rhythm"]["bursts"]), "films;",
      [(c["id"], [(b["cuts"], b["mid_share"]) for b in c["metrics"]["rhythm"]["bursts"]]) for c in C if c["metrics"]["rhythm"]["bursts"]])
print("median hold s:", med([c["metrics"]["events"]["median_hold_s"] for c in C], 2))
print("longest static run s:", med([c["metrics"]["frames"]["longest_static_run_s"] for c in C], 0))
print("first cut s:", med([c["metrics"]["rhythm"]["first_cut_s"] for c in C], 1))
print("longest shot s:", med([(c["metrics"]["rhythm"].get("longest_shot") or {}).get("seconds") for c in C], 1))
print("hero share:", med([c["findings"]["structure"]["hero_moment"]["share"] for c in C], 2))
print("logo hold:", med([c["findings"]["structure"]["ending"]["logo_hold_s"] for c in C], 1))
print("title pct pooled:", med([x for c in C for x in c["findings"]["look"]["title_height_pct"]], 1))
print("words/title line:", med([c["findings"]["look"]["max_words_per_title_line"] for c in C], 0))
print("UI legible:", collections.Counter(c["findings"]["product_ui"]["legible_at_phone_width"] for c in C))
print("shown as:", collections.Counter(s for c in C for s in c["findings"]["product_ui"]["shown_as"]))
print("cursor:", collections.Counter(c["findings"]["product_ui"]["cursor"] for c in C))
print("voiceover:", collections.Counter(c["findings"]["transcript"]["voiceover"] for c in C))
print("wpm VO:", med([c["findings"]["transcript"]["words_per_minute"] for c in C if c["findings"]["transcript"]["voiceover"] != "none-music-only" and c["findings"]["transcript"]["words_per_minute"] > 0], 0))
lu = [c["metrics"]["sound"].get("lufs_integrated") for c in C]
tp = [c["metrics"]["sound"].get("true_peak_db") for c in C]
lu = [x for x in lu if num(x)]; tp = [x for x in tp if num(x)]
print(f"LUFS n={len(lu)} median {st.median(lu)}; within -15..-13: {sum(-15 <= x <= -13 for x in lu)}; quieter than -16: {sum(x < -16 for x in lu)}; range {min(lu)}..{max(lu)}")
print(f"TP n={len(tp)} median {st.median(tp)}; above -1: {sum(x > -1 for x in tp)}; above 0: {sum(x > 0 for x in tp)}")
al = [(c["metrics"]["sound"].get("cuts_on_strong_onset_share"), c["metrics"]["sound"].get("chance_share")) for c in C]
al = [(a, b) for a, b in al if num(a) and num(b)]
print(f"onset lock: n={len(al)}, >chance+0.10: {sum(a - b > 0.10 for a, b in al)}")
sil_end = 0
for c in C:
    d = c["metrics"]["duration_s"]
    sp = c["metrics"]["sound"].get("silence_spans") or []
    if any(s.get("end", 0) >= d - 0.3 and d - s.get("start", d) >= 1.0 for s in sp):
        sil_end += 1
print("films ending in >=1 s silence:", sil_end)
trans = collections.Counter(); tfilms = collections.Counter(); kinds = []
for c in C:
    ts = c["findings"]["motion"]["transitions"]
    kinds.append(len({t["type"] for t in ts}))
    for t in ts:
        trans[t["type"]] += t["count"]; tfilms[t["type"]] += 1
print("transition kinds per film:", med(kinds, 0))
print("transitions (films, count):", [(k, tfilms[k], trans[k]) for k, _ in tfilms.most_common()])
for b in ("Claude", "Harvey", "Muse"):
    cs = [c for c in C if c["findings"]["brand"] == b]
    print(b, "n", len(cs), "light share", med([c["metrics"]["frames"]["light_share"] for c in cs], 2),
          "sat", med([c["metrics"]["look"]["saturation"] for c in cs], 3), "warm", med([c["metrics"]["look"]["warmth"] for c in cs], 1),
          "cuts/min", med([c["metrics"]["rhythm"]["cuts_per_min"] for c in cs]), "logo hold", med([c["findings"]["structure"]["ending"]["logo_hold_s"] for c in cs]))
print("frame0 texts:")
for c in C:
    print(" ", c["id"], c["findings"]["brand"], "|", c["findings"]["structure"]["frame0"][:140])
print("CTA texts:")
for c in C:
    print(" ", c["id"], "|", c["findings"]["structure"]["ending"]["cta_text"])
