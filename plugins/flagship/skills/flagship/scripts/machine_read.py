#!/usr/bin/env python3
"""The honest machine read, in one call.

Three axes, each with a measured reason it cannot be read the obvious way:

  berths   -- counts registered governor-run claims, NOT load. Measured in_use=0 while
              five Opus runners were live, because workflow-inner agents never register.
              Reported alongside load per core so it cannot be mistaken for capacity.
  thermal  -- held_for_sec describes only the CURRENT state and dwell_required_sec is 60,
              so one quiet minute flips the verdict on an unchanged machine. Sampled
              repeatedly; the pessimistic reading wins.
  disk     -- `df -h /` on APFS reads the read-only SYSTEM volume (~5% used) while the data
              volume sits at 87%. Wrong by an order of magnitude in the reassuring
              direction. Read from harbourmaster's pressure.py, never from `/`.

Exit 0 always: this reports, it does not gate. Read `advice` and act on it.
"""
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path

HM_CANDIDATES = [
    Path.home() / "Dev/fledgeling-plugins/plugins/harbourmaster/skills/harbourmaster/scripts",
]


def find_hm(explicit=None):
    if explicit:
        p = Path(explicit)
        return p if (p / "berths.py").exists() else None
    for p in HM_CANDIDATES:
        if (p / "berths.py").exists():
            return p
    # installed plugin cache, newest version last
    cache = Path.home() / ".claude/plugins/cache"
    found = sorted(cache.glob("*/harbourmaster/*/skills/harbourmaster/scripts"))
    return found[-1] if found else None


def run_json(script, timeout=30):
    try:
        r = subprocess.run([sys.executable, str(script)], capture_output=True,
                           text=True, timeout=timeout)
        return json.loads(r.stdout) if r.stdout.strip() else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hm", help="harbourmaster scripts dir; auto-detected otherwise")
    ap.add_argument("--thermal-samples", type=int, default=3,
                    help="thermal reads (default 3 -- one is not evidence)")
    ap.add_argument("--thermal-interval", type=float, default=20.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    hm = find_hm(a.hm)
    out = {"harbourmaster": str(hm) if hm else None, "advice": []}

    if not hm:
        out["advice"].append(
            "harbourmaster not found -- do NOT invent a slot count; run unwrapped and say so once")
        print(json.dumps(out, indent=2))
        return 0

    berths = run_json(hm / "berths.py")
    pressure = run_json(hm / "pressure.py")

    # Thermal: sample repeatedly, keep the pessimistic verdict.
    samples = []
    for i in range(max(1, a.thermal_samples)):
        t = run_json(hm / "thermal.py", timeout=90)
        if t:
            samples.append({"verdict": t.get("verdict"),
                            "held_for_sec": t.get("held_for_sec"),
                            "reason": t.get("reason")})
        if i + 1 < a.thermal_samples:
            time.sleep(a.thermal_interval)

    verdicts = [s["verdict"] for s in samples]
    if "limited" in verdicts:
        thermal_verdict = "limited"
    elif verdicts and all(v == "not_limited" for v in verdicts):
        thermal_verdict = "not_limited"
    else:
        thermal_verdict = verdicts[0] if verdicts else "unobservable"

    out["thermal"] = {"verdict_pessimistic": thermal_verdict, "samples": samples,
                      "flipped": len(set(verdicts)) > 1}

    if berths:
        out["berths"] = {k: berths.get(k) for k in
                         ("capacity", "ceiling", "in_use", "available", "degraded", "hard_gate")}
        out["berths"]["MEANS"] = "registered governor-run claims, NOT machine load"
    if pressure:
        out["load_per_core"] = pressure.get("cpu", {}).get("load_per_core")
        out["disk"] = pressure.get("disk")
        out["memory_free_pct"] = pressure.get("memory", {}).get("free_pct")
        out["verdicts"] = {k: pressure.get(k) for k in ("verdict", "verdicts") if pressure.get(k)}

    # The token: ship-armada's policy (3 projects) intersected with measured berths.
    avail = (berths or {}).get("available")
    if isinstance(avail, int):
        token = max(1, min(3, avail))
        if thermal_verdict == "limited":
            token = 1
            out["advice"].append(
                "thermal limited -- issuing ONE heavy slot regardless of berth count")
        elif out["thermal"]["flipped"]:
            token = max(1, token - 1)
            out["advice"].append(
                "thermal flipped across samples -- a clamp is near; issuing one fewer than the cap")
        out["heavy_slot_token"] = token
        out["token_basis"] = "min(ship-armada 3 concurrent projects, harbourmaster available berths)"

    if (berths or {}).get("hard_gate"):
        out["advice"].append(
            f"HARD GATE: {berths['hard_gate']} -- stop scheduling; disk goes to mac-doctor, not here")

    d = out.get("disk") or {}
    if isinstance(d.get("free_pct"), (int, float)) and d["free_pct"] < 15:
        out["advice"].append(
            f"disk at {d['free_pct']}% free ({d.get('free_gib')} GiB) -- relatively tightest axis; "
            "APFS degrades before the bytes run out. NEVER read this with `df -h /`.")

    out["advice"].append("say which number you used and whether it was measured")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
