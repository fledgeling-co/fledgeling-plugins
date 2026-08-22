#!/usr/bin/env python3
"""Decide whether macOS is holding this chip back, and if it is, ask for more.

## Why this is an inference and not a reading

Checked on Mac16,5 (M4 Max, macOS 26.6) on 2026-08-22, and independently by the
zephyr project on 2026-08-05 and 2026-08-08:

- `pmset -g therm` prints "No thermal warning level has been recorded / No
  performance warning level has been recorded / No CPU power status has been
  recorded". That is the registry keys being ABSENT, not a clean bill of health.
- `IOPMCopyCPUPowerStatus` returns `kIOReturnNotFound`; `ioreg -n IOPMrootDomain`
  carries none of `CPU_Speed_Limit`, `CPU_Available_CPUs`, `CPU_Scheduler_Limit`.
- `ProcessInfo.thermalState` reported `.nominal` across 240 samples while the
  die peaked at 106.92 and 111.25 °C.
- There are no thermal `sysctl`s.

So on this chassis every reported signal is silent, and any check built on one
returns "not throttling" forever. Frequency and package power need
`powermetrics`, which needs root. Without that grant this module reports
`unobservable` and changes nothing, which is the honest answer rather than a
convenient one.

## The statistic, and why it is the maximum

zephyr first looked for a DECLINE in clock as temperature rose, found none up to
115 °C, and concluded nothing was throttling. That was wrong, and the correction
is the whole basis of this file: **a limiter clamps, it does not slope.** The
capture had been inside the limited regime the entire time. Median frequency
against itself is flat either way; what separates the two is the per-window
MAXIMUM against the hardware's own ladder. M4 Max P-cores top out at 4512 MHz,
and across 925 samples spanning 87.67-115.42 °C that capture never once exceeded
4104 MHz and never touched the top two states.

This module therefore asks: over the dwell window, while the machine had work
outstanding, did the P-cluster ever reach the top of its ladder? A machine that
never does, while busy, is being held.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HOME = Path(os.environ.get("HARBOURMASTER_HOME", Path.home() / ".claude/harbourmaster"))
STATE = HOME / "thermal-state.json"

# Every value here is a choice, stated as one, and set to fail toward silence.
# A false "throttling" claim raises the machine's power draw and heat for no
# reason, which is worse than saying nothing.
DWELL_SECONDS = 60.0        # the user's stated bar: throttling for over a minute
CLEAR_SECONDS = 180.0       # hysteresis before standing down; longer than dwell
                            # on purpose, so a borderline machine cannot flap
UTILISATION_FLOOR = 0.60    # below this there is no work being held back
LADDER_FRACTION = 0.93      # 'near the top' means at or above this share of it
NEAR_TOP_FLOOR = 0.02       # a busy cluster spending under 2% of its active
                            # time in its top states is being held there
MIN_SAMPLES = 6


def powermetrics_available() -> tuple[bool, str]:
    """Can we read frequency at all? Never prompts for a password."""
    probe = subprocess.run(
        ["sudo", "-n", "powermetrics", "-n", "1", "-i", "200",
         "--samplers", "cpu_power"],
        capture_output=True, text=True, timeout=25,
    )
    if probe.returncode == 0 and probe.stdout.strip():
        return True, "readable"
    err = (probe.stderr or "").strip().splitlines()
    reason = err[-1] if err else "no output"
    if "password" in reason.lower() or "sudo:" in reason:
        reason = ("powermetrics needs root and no passwordless rule is installed "
                  "— run scripts/install.sh --thermal-read")
    return False, reason


CLUSTER_RE = re.compile(
    r"^(?P<name>[EP]\d*)-Cluster HW active residency:\s+(?P<busy>[\d.]+)%"
    r"(?:\s*\((?P<ladder>[^)]*)\))?"
)
LADDER_RE = re.compile(r"(\d+)\s*MHz:\s*([\d.]+)%")


def parse_clusters(text: str) -> list[dict]:
    """Per-cluster residency, with the hardware's own frequency ladder.

    `powermetrics` prints the whole P-state table inline, so the ladder top is
    READ rather than learned or hard-coded — which matters because it is
    per-SKU, and a constant would be wrong on any other Mac.

    Clusters are parsed separately because they clamp separately. Measured on
    this machine on 2026-08-22 in a single sample: P0 held 13% residency at the
    4512 MHz top while P1 held 0% at both top states and 59% at 3888 MHz. A
    machine-level average, or a peak taken across both, reports that machine as
    healthy.
    """
    out = []
    for line in text.splitlines():
        m = CLUSTER_RE.match(line.strip())
        if not m or not m.group("ladder"):
            continue
        states = [(float(f), float(r)) for f, r in LADDER_RE.findall(m.group("ladder"))]
        if not states:
            continue
        top = max(f for f, _ in states)
        # Share of active time spent at or near the top of the ladder. This is
        # the statistic, not peak frequency: a cluster can touch a high state
        # for a fraction of a percent and still be clamped for all of the time
        # that mattered.
        near_top = sum(r for f, r in states if f >= top * LADDER_FRACTION)
        out.append({
            "cluster": m.group("name"),
            "busy": float(m.group("busy")) / 100.0,
            "ladder_top_mhz": top,
            "near_top_residency": near_top / 100.0,
            "states": len(states),
        })
    return out


def sample(duration: float, interval_ms: int = 1000) -> list[list[dict]]:
    """Collect per-cluster residency over `duration` seconds."""
    count = max(MIN_SAMPLES, int(duration * 1000 / interval_ms))
    proc = subprocess.run(
        ["sudo", "-n", "powermetrics", "-n", str(count), "-i", str(interval_ms),
         "--samplers", "cpu_power"],
        capture_output=True, text=True, timeout=duration + 90,
    )
    if proc.returncode != 0:
        return []
    frames, current = [], []
    for line in proc.stdout.splitlines():
        parsed = parse_clusters(line)
        if parsed:
            name = parsed[0]["cluster"]
            if current and any(c["cluster"] == name for c in current):
                frames.append(current)
                current = []
            current.extend(parsed)
    if current:
        frames.append(current)
    return frames


def verdict_for(frames: list[list[dict]]) -> dict:
    """One verdict per P-cluster, folded into one for the machine.

    E-cores are excluded: they are meant to run low and a clamp there is the
    scheduler working, not heat.
    """
    per: dict[str, dict] = {}
    for frame in frames:
        for entry in frame:
            if not entry["cluster"].startswith("P"):
                continue
            acc = per.setdefault(entry["cluster"], {
                "busy": [], "near_top": [], "ladder_top_mhz": entry["ladder_top_mhz"]})
            acc["busy"].append(entry["busy"])
            acc["near_top"].append(entry["near_top_residency"])

    clusters = []
    for name, acc in sorted(per.items()):
        busy = sum(acc["busy"]) / len(acc["busy"])
        near = sum(acc["near_top"]) / len(acc["near_top"])
        if busy < UTILISATION_FLOOR:
            state = "idle"
        elif near <= NEAR_TOP_FLOOR:
            state = "limited"
        else:
            state = "not_limited"
        clusters.append({
            "cluster": name, "busy": round(busy, 3),
            "near_top_residency": round(near, 4),
            "ladder_top_mhz": acc["ladder_top_mhz"], "state": state,
        })

    states = {c["state"] for c in clusters}
    if not clusters:
        overall = "unknown"
    elif "limited" in states:
        overall = "limited"
    elif states == {"idle"}:
        overall = "idle"
    else:
        overall = "not_limited"
    return {"overall": overall, "clusters": clusters}


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save_state(state: dict) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(STATE)


def current_power_mode() -> dict:
    """`pmset -g custom` reports per power source; the wrong branch lies."""
    out = subprocess.run(["pmset", "-g", "custom"], capture_output=True,
                         text=True, timeout=10).stdout
    modes, section = {}, None
    for line in out.splitlines():
        if line.startswith("Battery Power"):
            section = "battery"
        elif line.startswith("AC Power"):
            section = "ac"
        elif section:
            m = re.search(r"powermode\s+(\d+)", line)
            if m:
                modes[section] = int(m.group(1))
    return modes


def set_power_mode(value: int, source: str = "ac") -> tuple[bool, str]:
    """0 Automatic, 2 High Power. Only ever the charger branch.

    High Power on battery would trade the user's remaining charge for clock
    they did not ask for, so this refuses to touch that branch at all.
    """
    if value not in (0, 2):
        return False, f"refusing unknown powermode {value}"
    if source != "ac":
        return False, "only the AC branch is ever written"
    proc = subprocess.run(["sudo", "-n", "pmset", "-c", "powermode", str(value)],
                          capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        return False, (proc.stderr or "pmset refused").strip().splitlines()[-1]
    return True, f"powermode set to {value} on AC"


def evaluate(duration: float) -> dict:
    ok, why = powermetrics_available()
    state = load_state()
    now = time.time()

    if not ok:
        return {
            "verdict": "unobservable", "reason": why,
            "action": "none",
            "note": "Every OS-reported thermal signal is silent on this chassis "
                    "(see this file's header), so without powermetrics there is "
                    "nothing to read. Not a claim that the machine is cool.",
        }

    frames = sample(duration)
    if len(frames) < MIN_SAMPLES:
        return {"verdict": "unknown",
                "reason": f"only {len(frames)} usable frames from powermetrics",
                "action": "none"}

    assessment = verdict_for(frames)
    verdict = assessment["overall"]
    limited = [c for c in assessment["clusters"] if c["state"] == "limited"]
    if limited:
        worst = min(limited, key=lambda c: c["near_top_residency"])
        reason = (f"{worst['cluster']} busy at {worst['busy']:.0%} but spent "
                  f"{worst['near_top_residency']:.1%} of active time at or near "
                  f"its {worst['ladder_top_mhz']:.0f} MHz ladder top")
    elif verdict == "idle":
        reason = f"no P-cluster above the {UTILISATION_FLOOR:.0%} busy floor"
    else:
        reason = "every busy P-cluster is reaching the top of its ladder"

    # Dwell: how long has this verdict held without interruption? A verdict that
    # changes resets the clock, so a machine flickering between states never
    # accumulates a dwell and nothing is done to it.
    if state.get("verdict") == verdict:
        since = state.get("since", now)
    else:
        since = now
    state.update({"verdict": verdict, "since": since, "checked_at": now,
                  "clusters": assessment["clusters"]})

    held_for = now - since
    modes = current_power_mode()
    action, detail = "none", ""

    if verdict == "limited" and held_for >= DWELL_SECONDS:
        if modes.get("ac") == 2:
            action, detail = "none", "already in High Power on AC"
        else:
            done, detail = set_power_mode(2)
            action = "raised_to_high_power" if done else "failed"
            state["raised_by_us"] = done
    elif verdict in ("not_limited", "idle") and held_for >= CLEAR_SECONDS:
        # Only stand down what we raised. A High Power setting the user chose
        # is theirs, and quietly reverting it would be the tool overruling them.
        if state.get("raised_by_us") and modes.get("ac") == 2:
            done, detail = set_power_mode(0)
            action = "returned_to_automatic" if done else "failed"
            if done:
                state["raised_by_us"] = False

    save_state(state)
    return {"verdict": verdict, "reason": reason, "held_for_sec": round(held_for),
            "dwell_required_sec": DWELL_SECONDS, "frames": len(frames),
            "clusters": assessment["clusters"], "power_mode": modes,
            "action": action, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--check", action="store_true",
                        help="report whether the lane is readable, and stop")
    args = parser.parse_args()

    if args.check:
        ok, why = powermetrics_available()
        json.dump({"readable": ok, "reason": why,
                   "power_mode": current_power_mode()}, sys.stdout, indent=2)
        print()
        return 0

    json.dump(evaluate(args.duration), sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
