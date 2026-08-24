#!/usr/bin/env python3
"""How many weight units this Mac can carry right now, and which are taken.

A berth is one weight unit. A job declares how many it needs; the ceiling is
what the machine can carry; the difference is what is available.

The registry IS the lock table. There is no separate record of who holds what,
no TTL and no reaper, because every one of those needs a process to notice a
death and act on it. A POSIX advisory lock held on an open file descriptor is
released by the kernel when the holding process exits for ANY reason —
including SIGKILL, a panic, or the user closing the terminal. Reading the
registry means trying each lock: the ones that refuse are held, right now, by a
process that is alive, right now.

The `.meta` sidecars are hints for humans and are never trusted on their own.
A meta file beside an unlocked slot is the residue of a finished job.
"""
from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
from pathlib import Path

HOME = Path(os.environ.get("HARBOURMASTER_HOME", Path.home() / ".claude/harbourmaster"))
BERTHS = HOME / "berths"

# The top of the band the machine is aimed at. 0.80 of core count, so a fully
# admitted machine sits at the upper end of 60-80% and leaves the spikes room.
CEILING_FRACTION = 0.80

# What each pressure state does to the ceiling. `critical` does not go to zero:
# a governor that admits nothing is indistinguishable from a broken one, and
# the machine would never drain because draining requires work to finish.
PRESSURE_MULTIPLIER = {
    "healthy": 1.00,
    "busy": 0.85,
    "tight": 0.50,
    "critical": 0.25,
    # A read we could not take degrades to the SAME multiplier as the worst
    # state, never to the middle. Measured bug: `unknown` at 0.50 was more
    # permissive than the machine's true `critical` 0.25, so a pressure read
    # that timed out under load RAISED the ceiling from 3 to 6 and admitted
    # work the governor had just decided to refuse. Not knowing is a reason to
    # be careful, not a reason to average.
    "unknown": 0.25,
}

# Below these, nothing is admitted whatever the berth count says. Both are
# states where starting more work makes the machine worse rather than slower.
HARD_GATES = (
    ("disk", lambda s: s["disk"]["free_gib"] is not None and s["disk"]["free_gib"] < 20,
     "disk below 20 GiB free — new work will fail on write, not merely run slowly"),
    ("swap", lambda s: s["memory"]["swap_used_pct"] >= 90,
     "swap above 90% — the machine is paging, and more concurrency deepens it"),
)


# Degrading to "unknown" costs half the ceiling. Waiting costs the caller its
# whole tool call, and a governor that hangs is worse than one that guesses low.
UNKNOWN = {
    "sampled_at": "unavailable", "cpu": {"ncpu": os.cpu_count() or 8,
    "load_per_core": None}, "memory": {"swap_used_pct": 0.0},
    "disk": {"free_gib": None, "free_pct": None},
    "verdict": {"cpu": "unknown", "memory": "unknown", "disk": "unknown",
                "overall": "unknown"},
}


def snapshot(max_age: float = 5.0, timeout: float = 8.0) -> dict:
    """Current pressure, bounded. Never blocks a caller past `timeout`."""
    try:
        out = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("pressure.py")),
             "--max-age", str(max_age)],
            capture_output=True, text=True, timeout=timeout,
        )
        return json.loads(out.stdout)
    except (subprocess.TimeoutExpired, ValueError, OSError):
        degraded = dict(UNKNOWN)
        degraded["degraded"] = True
        return degraded


def capacity(snap: dict) -> int:
    """Total berths this machine has when nothing is wrong."""
    return max(1, int(snap["cpu"]["ncpu"] * CEILING_FRACTION))


def ceiling(snap: dict) -> int:
    """Berths admissible right now, after pressure."""
    mult = PRESSURE_MULTIPLIER.get(snap["verdict"]["overall"], 0.5)
    return max(1, int(capacity(snap) * mult))


def held() -> list[dict]:
    """Which berths are occupied, proved by the lock rather than by a record."""
    BERTHS.mkdir(parents=True, exist_ok=True)
    occupied = []
    for index in range(64):
        slot = BERTHS / f"slot_{index:02d}.lock"
        if not slot.exists():
            continue
        fd = os.open(slot, os.O_RDWR | os.O_CREAT)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(fd, fcntl.LOCK_UN)  # free — the meta beside it is residue
        except OSError:
            meta_path = slot.with_suffix(".meta")
            meta = {}
            try:
                meta = json.loads(meta_path.read_text())
            except (OSError, ValueError):
                pass
            # A berth is held by whoever holds the DESCRIPTOR, and every
            # descendant inherits it. So the lock outliving the process that
            # took it is not a bug — an orphaned build child still burns CPU
            # and should still hold its berth. It is worth surfacing, because
            # a berth held by an orphan nobody is waiting on is the one way
            # this can leak.
            claimant = meta.get("pid")
            alive = None
            if isinstance(claimant, int):
                try:
                    os.kill(claimant, 0)
                    alive = True
                except ProcessLookupError:
                    alive = False
                except PermissionError:
                    alive = True
            occupied.append({"slot": index, "claimant_alive": alive, **meta})
        finally:
            os.close(fd)
    return occupied


def hard_gate(snap: dict) -> tuple[str, str] | None:
    for name, test, reason in HARD_GATES:
        try:
            if test(snap):
                return name, reason
        except (KeyError, TypeError):
            continue
    return None


def report() -> dict:
    snap = snapshot()
    occupied = held()
    # One held slot is one unit. `weight` in the meta is what the job ASKED
    # for and is informational; a weight-3 job holds three slots, so summing
    # the field would count it three times over.
    used = len(occupied)
    orphaned = [o for o in occupied if o.get("claimant_alive") is False]

    # `occupants` is one row PER SLOT, and each row repeats its job's declared
    # `weight`. That is honest and it is a footgun, because the obvious thing a
    # consumer reaches for — `sum(o["weight"] for o in occupants)` — counts a
    # weight-8 job eight times. Measured 2026-08-23: 10 rows, 2 distinct pids,
    # and that sum returned **68 against a capacity of 12**. Not subtly wrong;
    # 5.7x the machine, with nothing in the output to say so.
    #
    # The comment above warned about it and the JSON did not, which is the whole
    # defect: a caveat a consumer cannot see is not a caveat. So `claims` is the
    # deduplicated view — one row per distinct claim, carrying how many slots it
    # actually holds — and summing `slots` over it equals `in_use` by
    # construction. Reach for `claims` to size or attribute a hold; `occupants`
    # stays per-slot for anything that needs the slot indices.
    claims: list[dict] = []
    for o in occupied:
        key = (o.get("pid"), o.get("project"), o.get("label"), o.get("started_at"))
        for c in claims:
            if c["_key"] == key:
                c["slots"] += 1
                break
        else:
            claims.append({
                "_key": key,
                "pid": o.get("pid"),
                "project": o.get("project"),
                "label": o.get("label"),
                "command": o.get("command"),
                "declared_weight": o.get("weight"),
                "qos": o.get("qos"),
                "started_at": o.get("started_at"),
                "claimant_alive": o.get("claimant_alive"),
                "slots": 1,
            })
    for c in claims:
        del c["_key"]
    top = ceiling(snap)
    gate = hard_gate(snap)
    return {
        "sampled_at": snap["sampled_at"],
        "pressure": snap["verdict"],
        "load_per_core": snap["cpu"]["load_per_core"],
        "capacity": capacity(snap),
        "ceiling": top,
        "in_use": used,
        "available": 0 if gate else max(0, top - used),
        "degraded": snap.get("degraded", False),
        "hard_gate": {"axis": gate[0], "reason": gate[1]} if gate else None,
        "occupants": occupied,
        # One row per distinct claim. `sum(c["slots"] for c in claims)` ==
        # `in_use`; summing `occupants[*].weight` does not, and is the trap.
        # `declared_weight` is what the job asked for, repeated here once
        # rather than once per slot.
        "claims": claims,
        "distinct_claims": len(claims),
        # Berths whose original process is gone but whose lock a descendant
        # still holds. Normal during a build; a standing count here with an
        # idle machine means something was left behind.
        "held_by_descendants": len(orphaned),
    }


def main() -> int:
    # Unknown arguments exit 2 and name themselves, for the same measured
    # reason as pressure.py: a generated brief invented a `claim` subcommand,
    # and this script read the board and exited 0 — nothing held, nothing
    # recorded, success reported. Claims are governor-run's; this only reads.
    unknown = [a for a in sys.argv[1:] if a != "--quiet"]
    if unknown:
        sys.stderr.write(f"berths.py: unknown argument {unknown[0]!r}\n")
        sys.stderr.write(
            "No subcommands, and --quiet is the only flag: this script reads "
            "the board and takes nothing. Berths are claimed through "
            "governor-run.\n")
        return 2
    data = report()
    if "--quiet" in sys.argv:
        print(data["available"])
    else:
        json.dump(data, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
