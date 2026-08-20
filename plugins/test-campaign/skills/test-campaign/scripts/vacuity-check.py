#!/usr/bin/env python3
"""Vacuity — the half of arming that mutates the specification.

Arming reverts the behaviour an assertion guards and watches the case go red.
That mutates the SYSTEM, and Ball & Kupferman (Vacuity in Testing, TAP 2008)
name it as one of a pair: mutating the system finds what the suite does not
cover, and mutating the SPECIFICATION finds what the suite never exercised at
all. A campaign with 220 armed cases had run the first direction 220 times and
the second never, and recorded "runner communication is outbound pull only via
HTTPS/WSS on TCP 443" as observed over a product with no HTTP client.

Three passes, all exact, none needing a model:

  unclassed   a requirement whose text names an effect outside the process and
              carries no `effect` field. Deliberately over-flags: it prompts the
              census rather than deciding it.
  uncensused  a requirement declaring an external effect class and recording no
              `provider` — nothing in production source that could perform it.
  blind       a test that calls a mutating verb and never reads again, so it can
              only be asserting the call's own return value.

Plus the control, which is this skill's own arming rule turned on this gate:

  --seed-strengthen   strengthen a requirement's declared constraint to one the
                      registry cannot satisfy, and require the gate to go red.
                      A strengthened constraint that still passes proves the
                      gate reads nothing.

The witness obligation and the unbacked-effect blocker live in campaign.py,
where the rest of the case-level rules are. This script is the requirement-level
and test-tree half. references/effect-boundary.md.

  python3 vacuity-check.py <dir> --gate
  python3 vacuity-check.py <dir> --tests crates --gate
  python3 vacuity-check.py <dir> --seed-strengthen REQ-001
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EFFECT_CLASSES = ("subprocess", "outbound-socket", "inbound-socket", "packet-filter",
                  "multicast", "filesystem-write", "device", "ipc", "none")
EXTERNAL = tuple(e for e in EFFECT_CLASSES if e != "none")

# Words that mean the product acts outside its own memory. Matched against a
# requirement's title and description. This over-flags on purpose: a false
# positive costs one `"effect": "none"` and a false negative costs the campaign
# its central claim, so the error runs toward asking.
VOCAB: dict[str, tuple[str, ...]] = {
    "subprocess":      ("spawn", "subprocess", "child process", "launch", "boot ",
                        "execute", "invoke ", "docker", "wsl", "tart", "hypervisor",
                        "vm ", "guest", "container", "microvm"),
    "outbound-socket": ("https", "http ", "wss", "outbound", "connect to", "upload",
                        "download", "webhook", "poll", "api call", "fetch", "tls",
                        "port 443", "remote"),
    "inbound-socket":  ("listen", "inbound", "bind", "accepts connections", "serve"),
    "packet-filter":   ("pfctl", "nftables", "iptables", "packet filter", "firewall",
                        "quarantine", "drop packets", "rfc1918", "egress filter"),
    "multicast":       ("mdns", "bonjour", "multicast", "broadcast", "discovery",
                        "announce", "_tcp.local"),
    "filesystem-write": ("keychain", "credential locker", "credential store",
                         "persist", "written to disk", "survives a restart"),
    "device":          ("usb", "camera", "microphone", "gpu", "smartcard", "hardware key"),
    "ipc":             ("daemon", "helper process", "rpc", "unix socket", "named pipe"),
}

# For the blind-mutation pass. The project declares its own vocabulary in
# campaign.json under `blindVocabulary: {mutators: [...], readers: [...]}`; these
# are the fallback for a Rust/RPC shape and nothing else.
#
# Getting this wrong is not a quiet degradation, it is a louder result. Measured
# on a real campaign: the defaults missed four reader verbs the project actually
# uses (`activity_feed`, `job_record`, `github_identity`, `run_audit`), and the
# pass reported 26 blind tests out of 35 mutating ones. With the project's own
# vocabulary the same tree reports 13. A wrong vocabulary produces MORE findings,
# so it reads as a thorough pass rather than a misconfigured one — which is why
# the effective lists and where they came from are printed on every run.
DEFAULT_MUTATORS = ("stop_all", "stop_runner", "restart", "clear_", "cancel_",
                    "set_", "delete_", "create_", "confirm_")
DEFAULT_READERS = ("list_", "get_", "read_", "fetch_", "sample_", "count_", "load_")


def load(d: Path, name: str, default):
    p = d / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else default


def requirements(d: Path) -> list[dict]:
    inv = load(d, "inventory", {})
    return inv.get("requirement", []) if isinstance(inv, dict) else []


def text_of(r: dict) -> str:
    return f"{r.get('title', '')} {r.get('description', '')} {r.get('text', '')}".lower()


def suspected(r: dict) -> list[str]:
    """Which external effect classes this requirement's own words name."""
    t = text_of(r)
    return sorted({cls for cls, words in VOCAB.items() if any(w in t for w in words)})


# ── the three passes ────────────────────────────────────────────────────────

def pass_unclassed(reqs: list[dict]) -> tuple[int, list[str]]:
    findings = []
    for r in reqs:
        if r.get("effect"):
            continue
        if r.get("class") == "deferred":
            continue
        hits = suspected(r)
        if hits:
            findings.append(f"{r['id']} names {'/'.join(hits)} and declares no `effect` "
                            f"— run the census, or record \"effect\": \"none\"")
    return len(reqs), findings


def pass_uncensused(reqs: list[dict]) -> tuple[int, list[str]]:
    declared = [r for r in reqs if r.get("effect") in EXTERNAL]
    findings = [
        f"{r['id']} declares a {r['effect']} effect and records no `provider` — "
        f"nothing in production source is named as able to perform it"
        for r in declared if not r.get("provider")
    ]
    return len(declared), findings


def pass_blind(root: Path, mutators: tuple[str, ...], readers: tuple[str, ...]
               ) -> tuple[int, int, int, list[str]]:
    """After the last mutating call in a test body, does any reader appear?

    Name-based and deliberately generous: a reader called for an unrelated
    reason still counts, so the error runs toward reporting fewer blind tests
    than there are. A test that mutates and never reads again can only be
    asserting the call's own return value, which is the shape that let a daemon
    verb report success while changing nothing.
    """
    fn_re = re.compile(r"^\s*(?:async\s+)?(?:fn|def|func|function)\s+(\w+)\s*\(", re.M)
    files = [f for f in root.rglob("*")
             if f.is_file() and f.suffix in {".rs", ".py", ".ts", ".js", ".go", ".swift", ".cs"}
             and ("test" in str(f).lower() or "spec" in str(f).lower())]
    examined = mutating = reread = 0
    findings: list[str] = []
    for f in files:
        try:
            src = f.read_text(errors="replace")
        except OSError:
            continue
        starts = [(m.start(), m.group(1)) for m in fn_re.finditer(src)]
        # A function another function in the same file calls is a fixture helper,
        # not a test. Counting one inflates `examined` and can report it blind:
        # a helper that seeds a log and returns it mutates and never reads, which
        # is correct — its callers do the reading. Measured: one such helper was
        # reported as a blind test while every one of its four callers asserted on
        # what it built. Excluding them only ever removes findings, which is the
        # direction this pass is already committed to erring in.
        helpers = {n for _, n in starts
                   if len(re.findall(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"\s*\(", src)) > 1}
        for i, (pos, name) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else len(src)
            body = src[pos:end]
            if name in helpers:
                continue
            examined += 1
            last, which = -1, None
            for v in mutators:
                # `(?<![A-Za-z0-9_])` is load-bearing. Without it a verb that is a
                # substring of a longer identifier fires: `record` matched inside
                # `job_record(` and reported a test with no mutating call in it as
                # blind, and `set_` would match `offset_`. The lookbehind still
                # allows a method call, because `.` and whitespace are not word
                # characters. The reader side is deliberately left loose — a false
                # reader match suppresses a finding, which is the safe direction,
                # while a false mutator match manufactures one.
                for m in re.finditer(r"(?<![A-Za-z0-9_])" + re.escape(v) + r"\w*\s*\(", body):
                    if m.start() > last:
                        last, which = m.start(), v
            if last < 0:
                continue
            mutating += 1
            tail = body[last:]
            if any(re.search(re.escape(rd) + r"\w*", tail) for rd in readers):
                reread += 1
            else:
                findings.append(f"{name} — last mutator '{which}', no read after it "
                                f"({f})")
    return examined, mutating, reread, findings


# ── the control ─────────────────────────────────────────────────────────────

def seed_strengthen(d: Path, req_id: str) -> int:
    """Strengthen one requirement's constraint and require the gate to go red.

    Registry-level, and exact: take a requirement that currently clears the
    census, replace its declared effect class with one no case witnesses, and
    re-run. A gate that still clears is reading nothing, and every verdict it
    has issued is worthless. Restores the registry either way.

    The specification-level version of the same control is a manual step and it
    is the more valuable one: rewrite the requirement's constraint to something
    strictly harder to satisfy ("TCP 443" to "TCP 1", "at most two guests" to
    "at most zero"), re-run the project's own suite, and require a red. See
    references/effect-boundary.md §6.
    """
    inv_path = d / "inventory.json"
    original = inv_path.read_text()
    inv = json.loads(original)
    hit = next((r for r in inv.get("requirement", []) if r["id"] == req_id), None)
    if hit is None:
        sys.exit(f"No requirement {req_id}.")

    before = _census_clear(d)
    try:
        hit["effect"] = "packet-filter" if hit.get("effect") != "packet-filter" else "subprocess"
        hit["evidence"] = "observed"
        hit.pop("provider", None)
        inv_path.write_text(json.dumps(inv, indent=2) + "\n")
        after = _census_clear(d)
    finally:
        inv_path.write_text(original)

    print(f"seed-strengthen {req_id}: before={'clear' if before else 'red'} "
          f"after={'clear' if after else 'red'}")
    if after:
        print("FAIL — the strengthened requirement still clears the census, so the "
              "census reads nothing and every verdict it has issued is worthless.")
        return 1
    print("The gate bites: strengthening the constraint turned it red, and the "
          "registry was restored byte-for-byte.")
    return 0


def _census_clear(d: Path) -> bool:
    reqs = requirements(d)
    _, unclassed = pass_unclassed(reqs)
    _, uncensused = pass_uncensused(reqs)
    return not (unclassed or uncensused)


# ── entry ───────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--tests", help="Root to scan for the blind-mutation pass, e.g. 'crates'.")
    ap.add_argument("--mutator", action="append", default=[],
                    help="A verb that changes state. Repeatable; ADDS to the campaign's "
                         "vocabulary and the defaults.")
    ap.add_argument("--reader", action="append", default=[],
                    help="A verb that reads state. Repeatable; ADDS to the campaign's "
                         "vocabulary and the defaults.")
    ap.add_argument("--only", action="store_true",
                    help="Use only the verbs passed on the command line, ignoring the "
                         "campaign's vocabulary and the defaults.")
    ap.add_argument("--gate", action="store_true",
                    help="Exit 1 when any pass finds something.")
    ap.add_argument("--seed-strengthen", metavar="REQ-ID",
                    help="Prove the census can fail, then restore the registry.")
    args = ap.parse_args()
    d = Path(args.dir).resolve()

    if args.seed_strengthen:
        return seed_strengthen(d, args.seed_strengthen)

    reqs = requirements(d)
    if not reqs:
        print("No requirements in the registry. A vacuity check over nothing is clean "
              "for the same reason an empty campaign is: there is nothing to read.")
        return 1 if args.gate else 0

    total, unclassed = pass_unclassed(reqs)
    declared, uncensused = pass_uncensused(reqs)

    print(f"unclassed:  examined={total} findings={len(unclassed)}")
    for line in unclassed[:20]:
        print(f"  · {line}")
    print(f"uncensused: examined={declared} findings={len(uncensused)}")
    for line in uncensused[:20]:
        print(f"  · {line}")

    blind_findings: list[str] = []
    if args.tests:
        root = Path(args.tests)
        if not root.is_absolute():
            root = Path.cwd() / root
        if not root.exists():
            print(f"blind:      SKIPPED — {root} does not exist. A pass that could not "
                  f"run is not a pass that found nothing.")
        else:
            vocab = load(d, "campaign", {}).get("blindVocabulary") or {}
            declared_m = tuple(vocab.get("mutators") or ())
            declared_r = tuple(vocab.get("readers") or ())
            # A default that does not fit the project manufactures findings and
            # there was no way to say so: the campaign could add a verb, never
            # replace one. Measured here — the generic `create_` matched the pure
            # function `create_pairing_response`, and two crypto tests with no
            # state to re-read were reported blind. `only` lets a project own the
            # whole vocabulary; it must then declare both lists, because an empty
            # one matches nothing and returns clean.
            if args.only or vocab.get("only"):
                muts = tuple(args.mutator) or declared_m
                rds = tuple(args.reader) or declared_r
                source = ("command line only (--only)" if args.only
                          else "campaign.blindVocabulary only — defaults not applied")
            else:
                muts = tuple(dict.fromkeys(DEFAULT_MUTATORS + declared_m + tuple(args.mutator)))
                rds = tuple(dict.fromkeys(DEFAULT_READERS + declared_r + tuple(args.reader)))
                source = ("defaults + campaign.blindVocabulary" if (declared_m or declared_r)
                          else "defaults only — campaign.json declares no blindVocabulary")
                if args.mutator or args.reader:
                    source += " + command line"
            if not muts or not rds:
                print("blind:      NOT RUN — an empty mutator or reader list matches nothing, "
                      "and a pass that matches nothing returns clean.")
                muts = rds = ()
            if muts and rds:
                examined, mutating, reread, blind_findings = pass_blind(root, muts, rds)
                print(f"blind:      examined={examined} mutating={mutating} "
                      f"re-read-after={reread} blind={len(blind_findings)}")
                print(f"  vocabulary: {source} — {len(muts)} mutator(s), {len(rds)} reader(s)")
                print(f"  readers: {', '.join(rds)}")
            for line in blind_findings[:20]:
                print(f"  · {line}")
    else:
        print("blind:      NOT RUN — pass --tests <root> to scan the test tree. "
              "This is the cheapest of the three and needs no privilege.")

    findings = len(unclassed) + len(uncensused) + len(blind_findings)
    print(f"\nvacuity: requirements={total} external={declared} findings={findings}")
    if args.gate and findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
