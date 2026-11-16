"""Validate one findings.json against the corpus contract.

    python3 -P validate_findings.py <path/to/findings.json>
Exit 0 and print OK when valid; exit 1 and print one error per line otherwise.
"""
import json
import sys

S, N, I = "str", "num", "int"

TRANSITIONS = ["hard-cut", "match-cut", "push-or-slide", "zoom-through", "whip-pan", "mask-or-wipe",
               "morph-or-shared-element", "cross-dissolve", "fade-through-colour", "continuous-camera-move",
               "ui-state-change", "other"]

SPEC = {
    "id": S, "title": S, "brand": S, "duration_s": N,
    "status": ("enum", ["ok", "partial", "failed"]),
    "format": ("enum", ["launch-film", "feature-explainer", "product-demo-walkthrough", "customer-or-user-story",
                        "tutorial", "brand-manifesto", "short-announcement", "partnership-sting", "other"]),
    "format_note": (S, 30),
    "one_thing": (S, 30),
    "transcript": {
        "source": ("enum", ["human-captions", "auto-captions", "local-whisper", "none"]),
        "voiceover": ("enum", ["narrator-vo", "on-camera-presenter", "presenter-and-vo", "customer-testimonial", "none-music-only"]),
        "words_total": I, "words_per_minute": N,
        "voice_style": (S, 25), "script_shape": (S, 40),
    },
    "structure": {
        "frame0": (S, 40), "first_3s": (S, 40),
        "beats": ("list", 3, 20, {"start_s": N, "end_s": N,
                                  "role": ("enum", ["hook", "problem", "setup", "reveal", "demo", "proof", "turn",
                                                    "payoff", "cta", "logo", "other"]),
                                  "what": (S, 25)}),
        "hero_moment": {"t_s": N, "share": N, "what": (S, 30)},
        "ending": {"cta_text": (S, 20), "logo_hold_s": N, "what": (S, 30)},
    },
    "rhythm": {"route": ("enum", ["continuous", "montage", "hybrid"]), "hard_cuts": I, "cuts_per_min": N,
               "median_shot_s": N, "how_change_is_paced": (S, 50)},
    "look": {
        "ground": (S, 30), "palette": ("list", 1, 8, S), "accent_use": (S, 30), "type": (S, 40),
        "title_height_pct": ("list", 2, 2, N),
        "title_measurements": ("list", 0, 8, {"t_s": N, "text": (S, 15), "line_height_px": N,
                                              "frame_height_px": N, "pct": N}),
        "max_words_per_title_line": I,
        "density": ("enum", ["sparse", "medium", "dense"]), "depth": (S, 30),
    },
    "product_ui": {
        "presence_pct_runtime": N,
        "shown_as": ("list", 1, 4, ("enum", ["real-ui-capture", "redrawn-simplified-ui", "floating-ui-cards",
                                             "device-mockup", "abstract-illustration", "live-action", "none"])),
        "cursor": ("enum", ["none", "real", "stylised", "labelled-cursors"]),
        "camera_on_ui": (S, 40), "legible_at_phone_width": ("enum", ["yes", "partly", "no"]), "notes": (S, 60),
    },
    "motion": {
        "text_entry": (S, 40), "ui_motion": (S, 50), "camera": (S, 40), "eases": (S, 40),
        "transitions": ("list", 1, 12, {"type": ("enum", TRANSITIONS), "count": I, "example_t_s": N, "cause": (S, 20)}),
        "strips_read": ("list", 3, 12, S),
    },
    "copy": {
        "on_screen_lines": ("list", 0, 30, {"t_s": N, "text": (S, 25), "words": I, "hold_s": N}),
        "holds_vs_reading_rule": (S, 40),
    },
    "sound": {"music": (S, 40), "sfx": (S, 40), "vo_music_balance": (S, 30), "energy_arc": (S, 40), "sync_to_picture": (S, 40)},
    "good": ("list", 3, 8, {"observation": (S, 40), "evidence": (S, 20)}),
    "weak": ("list", 0, 5, {"observation": (S, 40), "evidence": (S, 20)}),
    "rule_candidates": ("list", 3, 8, {"rule": (S, 35), "evidence": (S, 25),
                                       "relation": ("enum", ["confirms", "contradicts", "extends", "new"]),
                                       "skill_rule": (S, 20)}),
    "frames_opened": I, "crops_made": I,
    "unchecked": ("list", 0, 6, (S, 25)),
}

errors = []


def words(s):
    return len(str(s).split())


def check(val, spec, path):
    if isinstance(spec, dict):
        if not isinstance(val, dict):
            errors.append(f"{path}: expected object")
            return
        for k, sub in spec.items():
            if k not in val:
                errors.append(f"{path}.{k}: missing")
            else:
                check(val[k], sub, f"{path}.{k}")
        return
    if spec == S:
        if not isinstance(val, str) or not val.strip():
            errors.append(f"{path}: expected non-empty string")
        return
    if spec == N:
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            errors.append(f"{path}: expected number (use -1 when it could not be measured)")
        return
    if spec == I:
        if isinstance(val, bool) or not isinstance(val, int):
            errors.append(f"{path}: expected integer")
        return
    kind = spec[0]
    if kind == S:
        if not isinstance(val, str) or not val.strip():
            errors.append(f"{path}: expected non-empty string")
        elif words(val) > spec[1]:
            errors.append(f"{path}: {words(val)} words, limit {spec[1]}")
        return
    if kind == "enum":
        if val not in spec[1]:
            errors.append(f"{path}: {val!r} not one of {spec[1]}")
        return
    if kind == "list":
        _, lo, hi, item = spec
        if not isinstance(val, list):
            errors.append(f"{path}: expected list")
            return
        if not lo <= len(val) <= hi:
            errors.append(f"{path}: {len(val)} items, allowed {lo}-{hi}")
        for i, v in enumerate(val):
            check(v, item, f"{path}[{i}]")


try:
    data = json.load(open(sys.argv[1]))
except Exception as e:
    print(f"cannot parse {sys.argv[1]}: {e}")
    sys.exit(1)
if isinstance(data, dict) and data.get("status") == "failed":
    check(data, {k: SPEC[k] for k in ("id", "title", "brand", "duration_s", "status")}, "$")
    check(data.get("unchecked"), ("list", 1, 6, (S, 25)), "$.unchecked")
else:
    check(data, SPEC, "$")
    try:
        D = float(data["duration_s"])
        h = data["structure"]["hero_moment"]
        if D > 0 and h["t_s"] >= 0 and h["share"] >= 0 and abs(h["share"] - h["t_s"] / D) > 0.05:
            errors.append(f"$.structure.hero_moment.share: {h['share']} but t_s / duration_s = {h['t_s'] / D:.3f}; share means t_s divided by duration_s")
        for i, b in enumerate(data["structure"]["beats"]):
            if b["end_s"] > D + 1 or (b["start_s"] >= 0 and b["end_s"] >= 0 and b["end_s"] < b["start_s"]):
                errors.append(f"$.structure.beats[{i}]: start {b['start_s']} end {b['end_s']} outside 0-{D}")
    except Exception:
        pass
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
