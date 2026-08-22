#!/usr/bin/env python3
"""Fast, unprivileged read of what this Mac is currently carrying.

Every number here comes from a call that returns in milliseconds. Nothing in
this file shells out to `du`, `ioreg -l` or `powermetrics`: a governor that
takes ten seconds to decide whether you may start is a governor nobody calls.
(`ioreg -l | grep` was measured at >120s on this machine under load.)

Emits one JSON object on stdout. Read `verdict` for the summary and the
individual blocks when you need to say *why*.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
import sys
import time

DATA_VOLUME = "/System/Volumes/Data"


def _run(argv: list[str], timeout: float = 3.0) -> str:
    try:
        return subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout
        ).stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def _sysctl(name: str) -> str:
    return _run(["sysctl", "-n", name]).strip()


def _ps_snapshot() -> list[str]:
    """One `ps` pass, reused by every block that needs it.

    Measured under load average 800 on this machine, a full `ps` can take tens
    of seconds. Two passes were the reason a bounded 3-second admission request
    once took 59.4 seconds — the failure this whole design exists to avoid — so
    there is exactly one, and it is bounded.
    """
    return _run(["ps", "-Axo", "state=,command="], timeout=8.0).splitlines()


def cpu_block(rows: list[str]) -> dict:
    """Load against core count.

    macOS load average counts threads in uninterruptible sleep as well as
    runnable ones, so a machine blocked on disk reads as a machine that is
    busy. That is a real limitation and the reason `runnable` is reported
    beside it: `ps` state R is a narrower claim.
    """
    ncpu = int(_sysctl("hw.ncpu") or 8)
    perf = int(_sysctl("hw.perflevel0.logicalcpu") or 0)
    eff = int(_sysctl("hw.perflevel1.logicalcpu") or 0)

    raw = _sysctl("vm.loadavg")  # "{ 1.23 4.56 7.89 }"
    nums = re.findall(r"[\d.]+", raw)
    load1, load5, load15 = (float(n) for n in (nums + ["0", "0", "0"])[:3])

    runnable = sum(1 for line in rows if line.lstrip().startswith("R"))

    return {
        "ncpu": ncpu,
        "performance_cores": perf,
        "efficiency_cores": eff,
        "load_1m": load1,
        "load_5m": load5,
        "load_15m": load15,
        "runnable_threads": runnable,
        # Ratio against cores. 1.0 means every core has exactly one thread
        # wanting it. This machine has been observed above 50.
        "load_per_core": round(load1 / ncpu, 3) if ncpu else 0.0,
    }


def memory_block() -> dict:
    total = int(_sysctl("hw.memsize") or 0)

    # `memory_pressure` reports a free percentage directly but was measured at
    # ~2s under load, which is most of this script's runtime. vm_stat is the
    # same arithmetic from a cheaper source. "Available" counts free, inactive
    # and speculative pages the way Activity Monitor does: pages the kernel can
    # hand out without evicting anything a process is still using.
    free_pct = None
    stat = _run(["vm_stat"], timeout=3.0)
    if stat:
        page = 16384
        m = re.search(r"page size of (\d+) bytes", stat)
        if m:
            page = int(m.group(1))
        pages = {
            k.strip(): int(v.strip().rstrip("."))
            for k, v in (
                line.split(":", 1) for line in stat.splitlines() if ":" in line
            )
            if v.strip().rstrip(".").isdigit()
        }
        available = (
            pages.get("Pages free", 0)
            + pages.get("Pages inactive", 0)
            + pages.get("Pages speculative", 0)
        )
        if total and available:
            free_pct = round(100 * available * page / total)

    swap_total = swap_used = 0.0
    m = re.search(
        r"total\s*=\s*([\d.]+)M\s+used\s*=\s*([\d.]+)M", _sysctl("vm.swapusage")
    )
    if m:
        swap_total, swap_used = float(m.group(1)), float(m.group(2))

    return {
        "total_bytes": total,
        "free_pct": free_pct,
        "swap_total_mb": swap_total,
        "swap_used_mb": swap_used,
        "swap_used_pct": round(100 * swap_used / swap_total, 1) if swap_total else 0.0,
    }


def disk_block() -> dict:
    try:
        usage = shutil.disk_usage(DATA_VOLUME)
    except OSError:
        return {"free_bytes": None, "free_gib": None, "free_pct": None}
    return {
        "free_bytes": usage.free,
        "free_gib": round(usage.free / 1024**3, 1),
        "free_pct": round(100 * usage.free / usage.total, 2) if usage.total else 0.0,
    }


def workload_block(rows: list[str]) -> dict:
    """Who is on the machine, by family rather than by pid.

    Counted from one `ps` pass. The families are the ones measured to matter
    here: agent CLIs and the compilers and runtimes they start.
    """
    families = {
        "claude": re.compile(r"(^|/)claude(\s|$)"),
        "node": re.compile(r"(^|/)node(\s|$)"),
        "rustc": re.compile(r"(^|/)rustc(\s|$)"),
        "cargo": re.compile(r"(^|/)cargo(\s|$)"),
        "swift-frontend": re.compile(r"swift-frontend"),
        "xcodebuild": re.compile(r"xcodebuild"),
        "codex": re.compile(r"(^|/)codex(\s|$)"),
        "python": re.compile(r"(^|/)python3?(\s|$)"),
    }
    counts = dict.fromkeys(families, 0)
    total = 0
    for line in rows:
        total += 1
        for name, pattern in families.items():
            if pattern.search(line):
                counts[name] += 1
                break
    return {"process_total": total, "by_family": counts}


def verdict(cpu: dict, mem: dict, disk: dict) -> dict:
    """One word per axis, plus the tightest.

    Thresholds are choices, not measurements, and each is stated as one. They
    are set so that `tight` still admits work and only `critical` refuses it —
    a governor that refuses everything is indistinguishable from a broken one.
    """
    lpc = cpu["load_per_core"]
    cpu_state = (
        "critical" if lpc >= 4.0 else
        "tight" if lpc >= 2.0 else
        "busy" if lpc >= 0.8 else
        "healthy"
    )

    free_pct = mem["free_pct"]
    swap_pct = mem["swap_used_pct"]
    if free_pct is None:
        mem_state = "unknown"
    elif free_pct < 10 or swap_pct >= 90:
        mem_state = "critical"
    elif free_pct < 25 or swap_pct >= 70:
        mem_state = "tight"
    elif free_pct < 40:
        mem_state = "busy"
    else:
        mem_state = "healthy"

    # Both axes matter and the stricter wins. An absolute floor catches a small
    # volume; a percentage floor catches this one, where 72 GiB free is still
    # only 3.9% of a 1.8 TiB disk and APFS copy-on-write degrades well before
    # the bytes run out.
    gib, dpct = disk["free_gib"], disk["free_pct"]
    if gib is None or dpct is None:
        disk_state = "unknown"
    elif gib < 20 or dpct < 2:
        disk_state = "critical"
    elif gib < 60 or dpct < 5:
        disk_state = "tight"
    elif gib < 150 or dpct < 10:
        disk_state = "busy"
    else:
        disk_state = "healthy"

    order = ["healthy", "busy", "tight", "critical", "unknown"]
    states = {"cpu": cpu_state, "memory": mem_state, "disk": disk_state}
    known = [s for s in states.values() if s != "unknown"]
    overall = max(known, key=order.index) if known else "unknown"
    return {**states, "overall": overall}


CACHE = Path(os.environ.get("HARBOURMASTER_HOME",
                            str(Path.home() / ".claude/harbourmaster"))) / "pressure.json"


def cached(max_age: float) -> dict | None:
    """A recent reading, if one exists.

    Many independent sessions ask this question at once and the answer does not
    meaningfully change between them. One read serving all of them is the
    difference between the governor costing nothing and the governor being the
    load.
    """
    try:
        if time.time() - CACHE.stat().st_mtime <= max_age:
            return json.loads(CACHE.read_text())
    except (OSError, ValueError):
        pass
    return None


def collect() -> dict:
    rows = _ps_snapshot()
    cpu, mem, disk = cpu_block(rows), memory_block(), disk_block()
    return {
        "sampled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": os.uname().nodename,
        "hw_model": _sysctl("hw.model"),
        "cpu": cpu,
        "memory": mem,
        "disk": disk,
        "workload": workload_block(rows),
        "verdict": verdict(cpu, mem, disk),
    }


def main() -> int:
    max_age = 5.0
    for i, arg in enumerate(sys.argv):
        if arg == "--max-age" and i + 1 < len(sys.argv):
            max_age = float(sys.argv[i + 1])

    snapshot = cached(max_age)
    if snapshot is None:
        snapshot = collect()
        try:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            tmp = CACHE.with_suffix(".tmp")
            tmp.write_text(json.dumps(snapshot))
            tmp.replace(CACHE)
        except OSError:
            pass
    else:
        snapshot["from_cache"] = True
    json.dump(snapshot, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
