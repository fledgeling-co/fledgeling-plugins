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
              `provider`, or naming one that resolves to nothing — no such path
              under the source root, no such symbol in production source.
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

Both roots this script reads belong in `campaign.json`, beside the vocabulary
that has to agree with them: `sourceRoot` for the census, `testRoot` for the
blind pass. A flag overrides a declared root; it is not the only place a root
can live, because a root that lives only on a command line drifts from the
vocabulary silently and the drift reads as a thorough pass.

  python3 vacuity-check.py <dir> --gate
  python3 vacuity-check.py <dir> --tests crates --source crates --gate
  python3 vacuity-check.py <dir> --seed-strengthen REQ-001
"""
from __future__ import annotations

import argparse
import json
import os
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

# ── what a provider has to resolve to ───────────────────────────────────────
#
# A `provider` is a claim that something in PRODUCTION code can perform the
# effect. Until 0.9.5 the census read the field's presence and never its
# referent: `isolation/macos.rs:88 spawn_guest` cleared whether or not that file
# or that symbol existed anywhere, so a census could report every external-effect
# requirement as provided while some of them named nothing. That is the same
# vacuity the script exists to find, one level up.
PRODUCTION_SUFFIXES = {".rs", ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".go",
                       ".swift", ".kt", ".java", ".cs", ".rb", ".c", ".cc", ".cpp",
                       ".h", ".hpp", ".m", ".mm", ".php", ".scala", ".ex", ".exs"}
PATHY_SUFFIXES = PRODUCTION_SUFFIXES | {".json", ".toml", ".lock", ".yaml", ".yml",
                                        ".xml", ".plist", ".md", ".sh", ".sql", ".proto"}
SKIP_DIRS = {"node_modules", "target", "dist", "build", "out", "vendor", "Pods",
             "venv", "__pycache__", "DerivedData", "coverage"}
# Production means what ships. A provider found only in the test tree is the
# product's test double naming itself as the thing it stands in for.
TEST_MARKERS = ("test", "spec", "fixture", "mock", "e2e", "bench")


class SourceIndex:
    """Every path under the declared root, and the production source among them."""

    def __init__(self, root: Path, origin: str = ""):
        self.root = root
        self.origin = origin
        self.paths: set[str] = set()
        self.production: list[Path] = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [x for x in dirnames
                           if x not in SKIP_DIRS and not x.startswith(".")]
            # Directories too: a provider may name a module (`crates/core/src/tui`)
            # rather than a single file, and refusing that would push authors to
            # name an arbitrary file inside it.
            try:
                d = Path(dirpath).relative_to(root).as_posix().lower()
                if d and d != ".":
                    self.paths.add(d)
            except ValueError:
                pass
            for fn in filenames:
                f = Path(dirpath) / fn
                try:
                    rel = f.relative_to(root).as_posix().lower()
                except ValueError:
                    continue
                self.paths.add(rel)
                if (f.suffix.lower() in PRODUCTION_SUFFIXES
                        and not any(m in rel for m in TEST_MARKERS)):
                    self.production.append(f)
        self._texts: list[str] | None = None

    def has_path(self, cand: str) -> bool:
        c = cand.strip().strip("./").lower()
        return bool(c) and any(p == c or p.endswith("/" + c) for p in self.paths)

    def has_symbol(self, sym: str) -> bool:
        # Two characters is a substring, not a symbol; matching one would resolve
        # every provider ever written and the pass would be back where it started.
        if len(sym) < 3:
            return False
        if self._texts is None:
            self._texts = []
            for f in self.production:
                try:
                    if f.stat().st_size <= 2_000_000:
                        self._texts.append(f.read_text(errors="replace"))
                except OSError:
                    continue
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(sym) + r"(?![A-Za-z0-9_])")
        return any(pat.search(t) for t in self._texts)


def provider_targets(provider: str) -> tuple[list[str], list[str]]:
    """Split a provider string into the paths and the symbols it claims.

    `isolation/macos.rs:88 spawn_guest` claims one of each. A line number is not
    part of either, and a token that is neither a path nor a symbol is neither.

    **Only the claim counts, never the description after it.** Providers are
    written `<claim> — <what it does>`, and the prose half is English. Before
    this split, every word of it was offered to `has_symbol`, so a provider
    resolved on whichever of its own adjectives happened to appear somewhere in
    production source. Measured on a real campaign: `totally/made/up/path.swift
    — the window server is another process` resolved, via the symbol `the`; so
    did a file that does not exist, via `file`. Nine of nine providers reported
    resolved and the pass was reading stopwords. A census that resolves anything
    with a description is the dead predicate this file exists to find, one level
    in.
    """
    claim = re.split(r"\s+[—–]\s+|\s+-\s+", str(provider).strip(), maxsplit=1)[0]
    paths: list[str] = []
    syms: list[str] = []
    for raw in re.split(r"[\s,;]+", claim):
        tok = raw.strip("()[]{}<>'\"`,")
        if not tok:
            continue
        head = tok.split(":")[0]
        if "/" in head or Path(head).suffix.lower() in PATHY_SUFFIXES:
            paths.append(head)
        else:
            sym = tok.split(":")[0]
            syms.append(sym)
            if "." in sym:
                syms.append(sym.split(".")[-1])
    return paths, syms


def resolve_provider(provider: str, index: SourceIndex) -> tuple[bool, str]:
    paths, syms = provider_targets(provider)
    for c in paths:
        if index.has_path(c):
            return True, f"path {c}"
    for sym in syms:
        if index.has_symbol(sym):
            return True, f"symbol {sym}"
    parts = []
    if paths:
        parts.append("no file at " + " or ".join(repr(c) for c in paths))
    if syms:
        parts.append("no production source contains " + " or ".join(repr(s) for s in syms))
    if not parts:
        parts.append("it names neither a path nor a symbol")
    return False, f"{'; '.join(parts)} under {index.root}"


def find_root(d: Path, raw: str) -> Path | None:
    """Resolve a declared or passed root. Campaign dir first, then its ancestors,
    then the working directory — a campaign living in `docs/test-campaign` names
    its roots relative to the repo, not to itself."""
    p = Path(raw).expanduser()
    if p.is_absolute():
        return p.resolve() if p.exists() else None
    for base in [d, *list(d.parents)[:3], Path.cwd()]:
        if (base / raw).exists():
            return (base / raw).resolve()
    return None


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


def pass_uncensused(reqs: list[dict], index: "SourceIndex | None" = None
                    ) -> tuple[int, list[str], int, int]:
    """Declared effects, and whether each one's provider resolves to anything.

    Returns (declared, findings, named, resolved) — the denominator matters as
    much as the findings, because "every external effect has a provider" was
    true of a registry where several providers named a file that did not exist.
    """
    declared = [r for r in reqs if r.get("effect") in EXTERNAL]
    findings: list[str] = []
    named = resolved = 0
    for r in declared:
        prov = str(r.get("provider") or "").strip()
        if not prov:
            findings.append(f"{r['id']} declares a {r['effect']} effect and records no "
                            f"`provider` — nothing in production source is named as able "
                            f"to perform it")
            continue
        named += 1
        if index is None:
            continue
        ok, why = resolve_provider(prov, index)
        if ok:
            resolved += 1
        else:
            findings.append(f"{r['id']} declares a {r['effect']} effect and names provider "
                            f"{prov!r}, which resolves to nothing — {why}. A provider that "
                            f"resolves to nothing is the census result of no provider at all.")
    return len(declared), findings, named, resolved


def pass_blind(root: Path, mutators: tuple[str, ...], readers: tuple[str, ...]) -> dict:
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
    # Which declared verbs appear anywhere in this corpus at all. A vocabulary
    # for another language half-matches — the generic verbs hit, the project's
    # own never do — and half-matching is what made 32 findings against a foreign
    # tree indistinguishable from 32 real ones. Recorded per run, not per test.
    seen_verbs: set[str] = set()
    for f in files:
        try:
            src = f.read_text(errors="replace")
        except OSError:
            continue
        for v in mutators:
            if v not in seen_verbs and re.search(
                    r"(?<![A-Za-z0-9_])" + re.escape(v) + r"\w*\s*\(", src):
                seen_verbs.add(v)
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
    return {"files": len(files), "examined": examined, "mutating": mutating,
            "reread": reread, "findings": findings, "seenVerbs": seen_verbs}


# ── the control ─────────────────────────────────────────────────────────────

def seed_strengthen(d: Path, req_id: str, index: "SourceIndex | None" = None) -> int:
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

    before = _census_clear(d, index)
    try:
        hit["effect"] = "packet-filter" if hit.get("effect") != "packet-filter" else "subprocess"
        hit["evidence"] = "observed"
        hit.pop("provider", None)
        inv_path.write_text(json.dumps(inv, indent=2) + "\n")
        after = _census_clear(d, index)
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


def _census_clear(d: Path, index: "SourceIndex | None" = None) -> bool:
    reqs = requirements(d)
    _, unclassed = pass_unclassed(reqs)
    _, uncensused, _, _ = pass_uncensused(reqs, index)
    return not (unclassed or uncensused)


# ── entry ───────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--tests", help="Root to scan for the blind-mutation pass, e.g. 'crates'. "
                                    "OVERRIDES campaign.json `testRoot`; it does not replace it "
                                    "as the place the root lives.")
    ap.add_argument("--source", help="Root of production source, for resolving each declared "
                                     "`provider`. OVERRIDES campaign.json `sourceRoot`.")
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
    campaign = load(d, "campaign", {})

    # The census root. A provider is only a claim until something resolves it,
    # and resolving it needs to know where production source is. A flag overrides
    # the declaration; neither is invented when both are absent, because guessing
    # a root is how the blind pass came to report 32 findings about a tree that
    # was not the campaign's.
    index = None
    src_origin = ""
    raw_source = args.source or campaign.get("sourceRoot") or ""
    if raw_source:
        src_origin = "--source" if args.source else "campaign.json sourceRoot"
        src_root = find_root(d, str(raw_source))
        if src_root is None:
            print(f"providers:  NOT RESOLVED — {raw_source!r} ({src_origin}) does not exist. "
                  f"A root that is not there resolves nothing, and nothing resolved is not "
                  f"nothing to resolve.")
        else:
            index = SourceIndex(src_root, src_origin)

    if args.seed_strengthen:
        return seed_strengthen(d, args.seed_strengthen, index)

    reqs = requirements(d)
    if not reqs:
        print("No requirements in the registry. A vacuity check over nothing is clean "
              "for the same reason an empty campaign is: there is nothing to read.")
        return 1 if args.gate else 0

    total, unclassed = pass_unclassed(reqs)
    declared, uncensused, named, resolved = pass_uncensused(reqs, index)

    print(f"unclassed:  examined={total} findings={len(unclassed)}")
    for line in unclassed[:20]:
        print(f"  · {line}")
    print(f"uncensused: examined={declared} findings={len(uncensused)}")
    for line in uncensused[:20]:
        print(f"  · {line}")
    if declared:
        if index is None:
            print(f"  providers: {named} of {declared} named, 0 resolved — NOT CHECKED. "
                  f"Declare `sourceRoot` in campaign.json or pass --source <root>; until "
                  f"one of them says where production source is, a provider is a string "
                  f"nobody read.")
        else:
            print(f"  providers: {named} of {declared} named, {resolved} resolved under "
                  f"{index.root} ({index.origin}, {len(index.production)} production file(s))")

    blind_findings: list[str] = []
    # The corpus root belongs beside the vocabulary that has to agree with it.
    # Measured: a campaign whose vocabulary was one language, pointed by hand at
    # another language's test tree, produced 32 findings identical in shape and
    # confidence to genuine ones; the same command over its own corpus returned 0.
    # Nothing warned, because the vocabulary half-matched.
    declared_root = campaign.get("testRoot") or (campaign.get("blindVocabulary") or {}).get("testRoot")
    raw_tests = args.tests or declared_root or ""
    tests_origin = "--tests" if args.tests else "campaign.json testRoot"
    if args.tests and declared_root and str(declared_root) != str(args.tests):
        print(f"blind:      --tests {args.tests!r} overrides campaign.json testRoot "
              f"({declared_root!r}). The declared root is what the vocabulary was written "
              f"for; an override is a different corpus.")
    if not raw_tests:
        print("blind:      NOT RUN — no corpus. Declare `testRoot` in campaign.json beside "
              "`blindVocabulary`, or pass --tests <root>. This is the cheapest of the three "
              "and needs no privilege.")
    else:
        root = find_root(d, str(raw_tests))
        if root is None:
            print(f"blind:      SKIPPED — {raw_tests} ({tests_origin}) does not exist. A pass "
                  f"that could not run is not a pass that found nothing.")
        else:
            vocab = campaign.get("blindVocabulary") or {}
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
                res = pass_blind(root, muts, rds)
                # The corroboration. Only the verbs the project (or the operator)
                # CLAIMED are evidence about fit: the defaults are a grab-bag and
                # some of them match every language. Fewer than a quarter of the
                # claimed verbs appearing anywhere in the corpus means the corpus
                # is not the one the vocabulary describes, and a number produced
                # over the wrong tree is worse than no number.
                claimed = tuple(dict.fromkeys(declared_m + tuple(args.mutator)))
                seen = [v for v in claimed if v in res["seenVerbs"]]
                misfit = bool(claimed) and res["files"] > 0 and len(seen) * 4 < len(claimed)
                if misfit:
                    print(f"blind:      VOCABULARY DOES NOT FIT — {len(seen)} of {len(claimed)} "
                          f"declared mutator(s) appear anywhere under {root} "
                          f"({tests_origin}, {res['files']} file(s) scanned).")
                    print(f"  claimed: {', '.join(claimed)}")
                    print("  A vocabulary written for one language, run over another language's "
                          "tree, produces findings identical in shape and confidence to genuine "
                          "ones — 32 of them, where the same command over its own corpus "
                          "returned 0. Declare `testRoot` in campaign.json beside "
                          "`blindVocabulary` so the corpus and the vocabulary cannot drift.")
                    blind_findings = [f"the blind vocabulary does not fit {root}: "
                                      f"{len(seen)} of {len(claimed)} declared mutator(s) "
                                      f"appear anywhere under it"]
                else:
                    blind_findings = res["findings"]
                    print(f"blind:      examined={res['examined']} mutating={res['mutating']} "
                          f"re-read-after={res['reread']} blind={len(blind_findings)}")
                    print(f"  corpus: {root} ({tests_origin}, {res['files']} file(s))")
                    print(f"  vocabulary: {source} — {len(muts)} mutator(s), {len(rds)} reader(s)")
                    print(f"  readers: {', '.join(rds)}")
                    for line in blind_findings[:20]:
                        print(f"  · {line}")

    findings = len(unclassed) + len(uncensused) + len(blind_findings)
    print(f"\nvacuity: requirements={total} external={declared} findings={findings}")
    if args.gate and findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
