#!/usr/bin/env python3
"""Roll the per-round score.json files up into fidelity-runs/rounds.json."""
import json
import pathlib

ASSETS = pathlib.Path(__file__).resolve().parent
RUNS = ASSETS / "fidelity-runs"

LABELS = {
    "r00": ("baseline", "first draft: three separated cards, flat material", "baseline"),
    "r01": ("coarse structure",
            "cards overlap into a real stack; geometry fitted to the reference's edge map",
            "REJECT vs r00"),
    "r02": ("material",
            "vertical wall ramp, measured occlusion line under every card, stronger lit "
            "top arris, gel and ink dark ends resampled", "REJECT vs r00"),
    "r03": ("detail", "card proportions fitted to the reference's bands",
            "REJECT (16px contrast floor vs r02)"),
    "r04": ("small-size repair", "deeper, wider cast shadows",
            "REJECT (16px contrast floor vs r02)"),
    "r05": ("material (accent)",
            "flat gel body, rim-not-core highlight, recessed well ring, warm bloom removed; "
            "back-plane rims masked by the drawn card", "REJECT (16px contrast floor vs r02)"),
    "r06": ("small-size repair", "one pooled shadow under the whole stack",
            "ACCEPT vs r00, the last accepted state"),
    "r07": ("detail", "real vertical wall ramp plus a separate lateral lean", "ACCEPT"),
    "r08": ("material", "gel body deepened to the reference's own median L", "ACCEPT"),
    "r09": ("material", "margin ink deepened for the small-size read", "ACCEPT"),
    "r10": ("small-size repair",
            "the extrusion wall carries the small-size read: taller, ramping into real "
            "occlusion, held near the reference's own wall values",
            "REJECT vs r09 on the composite; kept - see r11"),
    "r11": ("small-size repair",
            "value hierarchy: the two options still in the stack are clay in shade, the "
            "drawn card is porcelain in the light",
            "REJECT on the composite, ACCEPTED on the rubric - deliberate divergence"),
    "r12": ("detail",
            "shaded-card ramp deepened until its face clears 3:1 against the tile; drawn "
            "card lightened until the bead clears 3:1 against it",
            "REJECT on the composite, ships"),
}

rows = []
for r in sorted(LABELS):
    d = json.load(open(RUNS / r / "score.json"))
    s = d.get("sizes", d)
    cls, note, gate = LABELS[r]
    rows.append({
        "round": r, "edit_class": cls, "note": note, "gate": gate,
        "composite": {k: round(s[k]["composite"], 4) for k in ("1024", "256", "128", "32", "16")},
        "self_contrast_16": round(s["16"]["self_contrast"], 4),
    })

(RUNS / "rounds.json").write_text(json.dumps({
    "fixture": "clarify",
    "reference": "icon-engineC-4c230c-2-masked.png",
    "metric_tier": "numpy (no torch on this host: luminance + ssim + edges only)",
    "accepted_baseline": "r00",
    "ships": "r12",
    "rounds": rows,
}, indent=2) + "\n")
for r in rows:
    print(r["round"], r["composite"], "|", r["gate"])
