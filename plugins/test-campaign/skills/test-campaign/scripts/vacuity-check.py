#!/usr/bin/env python3
"""Vacuity — the half of arming that mutates the specification.

Arming reverts the behaviour an assertion guards and watches the case go red.
That mutates the SYSTEM, and Ball & Kupferman (Vacuity in Testing, TAP 2008)
name it as one of a pair: mutating the system finds what the suite does not
cover, and mutating the SPECIFICATION finds what the suite never exercised at
all. A campaign with 220 armed cases had run the first direction 220 times and
the second never, and recorded "runner communication is outbound pull only via
HTTPS/WSS on TCP 443" as observed over a product with no HTTP client.

Three mechanical passes, with a name-based blind heuristic, none needing a model:

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
import hashlib
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
SCOPE_CLASSES = {"failure-sentinel", "fixture-value", "direct-output", "attributed-helper"}


def load_blind_scopes(campaign_dir: Path, raw: object) -> tuple[list[dict], list[str]]:
    """Load explicit call scopes. Invalid metadata is a finding, never an ignored scope."""
    if not raw:
        return [], []
    path = (campaign_dir / str(raw)).resolve()
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return [], [f"scope file {path} could not be read ({type(error).__name__})"]
    if not isinstance(payload, dict) or payload.get("version") != 1 or not isinstance(payload.get("scopes"), list):
        return [], [f"scope file {path} must contain version 1 and a scopes array"]
    scopes, errors, identities = [], [], set()
    for index, row in enumerate(payload["scopes"]):
        label = f"scope[{index}]"
        error_count = len(errors)
        if not isinstance(row, dict):
            errors.append(f"{label} is not an object"); continue
        required = ("file", "name", "bodySHA256", "callOffset", "callSHA256", "mutator",
                    "classification", "rationale", "references")
        missing = [key for key in required if key not in row]
        if missing:
            errors.append(f"{label} lacks {', '.join(missing)}"); continue
        if not isinstance(row["classification"], str) or row["classification"] not in SCOPE_CLASSES:
            errors.append(f"{label} has unknown classification {row['classification']!r}")
        if not all(isinstance(row[key], str) and row[key] for key in
                   ("file", "name", "bodySHA256", "callSHA256", "mutator")):
            errors.append(f"{label} has a non-string identity field")
        if not isinstance(row["callOffset"], int) or row["callOffset"] < 0:
            errors.append(f"{label} has an invalid call offset")
        if len(errors) == error_count:
            identity = (row["file"], row["name"], row["bodySHA256"], row["callOffset"])
            if identity in identities:
                errors.append(f"{label} duplicates an earlier call scope")
            identities.add(identity)
        if not isinstance(row["rationale"], str) or not row["rationale"].strip():
            errors.append(f"{label} has no rationale")
        refs = row["references"]
        if not isinstance(refs, list) or not refs:
            errors.append(f"{label} has no producer/contract reference")
        else:
            for ref in refs:
                if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
                    errors.append(f"{label} has a malformed reference"); continue
                if not all(isinstance(ref[key], str) for key in ("path", "sha256")):
                    errors.append(f"{label} has a non-string reference field"); continue
                target = (campaign_dir / ref["path"]).resolve()
                try: digest = hashlib.sha256(target.read_bytes()).hexdigest()
                except OSError:
                    errors.append(f"{label} reference {ref['path']!r} does not exist"); continue
                if digest != ref["sha256"]:
                    errors.append(f"{label} reference {ref['path']!r} has drifted")
        if len(errors) == error_count:
            scopes.append(row)
    return scopes, errors


def call_fingerprint(body: str, start: int, end: int) -> str:
    """Hash the receiver/name/open-paren spelling at one matched call occurrence."""
    left = start
    while left and (body[left - 1].isalnum() or body[left - 1] in "_.$"):
        left -= 1
    spelling = body[left:end]
    return hashlib.sha256(spelling.encode()).hexdigest()

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


# The two ways a test body starts, because keying on one of them reported a
# clean run over a corpus it could not see. `DECL_RE` is a named declaration —
# Rust `fn`, Python `def`, Go/Swift `func`, JS `function`. `SPEC_HEAD_RE` is the
# arrow-style block a JS/TS runner uses: `it('…', () => {`, `test("…", async () =>`,
# and the `.each` / `.only` / `.skip` variants.
#
# Measured 2026-08-23 on two real repositories. One monorepo's API tests held 224
# declarations the first regex could see and 2,179 arrow-style `it(` blocks it
# could not, so `blind=0` was a statement about 9% of the corpus. A second repo,
# checked independently, held 4,741 arrow-style blocks and zero declarations —
# there the false clean was total rather than partial. A tool that under-reports
# by a fraction is a quality problem; one that reports `blind=0` over 4,741
# invisible tests is answering a different question and publishing it as the
# answer to this one.
#
# The lookbehind excludes `.test(` (a regex or a method call) and `$test(`, so a
# predicate does not read as a block. The corpus is already narrowed to paths
# containing `test` or `spec`, which is what makes a bare `test(` safe to read as
# a block head.
DECL_RE = re.compile(r"^\s*(?:async\s+)?(?:fn|def|func|function)\s+(\w+)\s*\(", re.M)
SPEC_HEAD_RE = re.compile(
    r"(?<![.\w$])(?:it|test)"
    r"(?:\.(?:each|only|skip|concurrent|failing|todo|sequential|runIf|skipIf))?"
    r"\s*\(",
    re.M)


def _spec_label(src: str, pos: int) -> str:
    """The quoted name that follows a spec head, for the finding line.

    Looks only at the next 200 characters: an `it.each([...])` head carries its
    table before the name, and a label is a label rather than a key, so a miss
    costs a readable string and nothing else.
    """
    m = re.search(r"""['"`]([^'"`\n]{1,80})""", src[pos:pos + 200])
    return m.group(1) if m else "<unnamed spec>"


# Swift is lexed separately: a following declaration is not a body's closing brace.
class SwiftScanError(ValueError):
    def __init__(self, position: int, reason: str):
        self.position, self.reason = position, reason
        super().__init__(reason)


class SwiftLexicalMask:
    """Keep offsets/newlines and executable interpolation; erase only literal/comment text.

    This is a bounded lexer, not a compiler. Ambiguous slash/regex forms and malformed
    delimiters fail the file's measurement rather than manufacturing executable text.
    """
    def __init__(self, source: str):
        self.source = source
        self.output = list(source)
        self.escaped_identifiers: set[int] = set()

    def erase(self, start: int, end: int) -> None:
        for i in range(start, end):
            if self.output[i] not in "\r\n":
                self.output[i] = " "

    def code(self, i: int = 0, interpolation: bool = False, depth: int = 0) -> int:
        if depth > 128:
            raise SwiftScanError(i, "interpolation nesting exceeds the supported limit (128)")
        s, parens = self.source, 0
        while i < len(s):
            if s.startswith("//", i):
                end = s.find("\n", i)
                end = len(s) if end < 0 else end
                self.erase(i, end); i = end; continue
            if s.startswith("/*", i):
                start, nesting = i, 1
                i += 2
                while i < len(s) and nesting:
                    if s.startswith("/*", i): nesting += 1; i += 2
                    elif s.startswith("*/", i): nesting -= 1; i += 2
                    else: i += 1
                if nesting:
                    raise SwiftScanError(start, "unterminated block comment")
                self.erase(start, i); continue
            if s.startswith("*/", i):
                raise SwiftScanError(i, "unmatched block-comment terminator")
            if s[i] == '`':
                end = s.find('`', i + 1)
                if end < 0 or not re.fullmatch(r"[^\W\d]\w*", s[i + 1:end], re.UNICODE):
                    raise SwiftScanError(i, "unsupported or unterminated escaped identifier")
                self.escaped_identifiers.add(i + 1)
                self.erase(i, i + 1); self.erase(end, end + 1)
                i = end + 1; continue
            hashes = 0
            if s[i] == '#':
                while i + hashes < len(s) and s[i + hashes] == '#': hashes += 1
                if s.startswith('/', i + hashes):
                    raise SwiftScanError(i, "Swift regex literal is not measured")
            if s.startswith('"', i + hashes):
                i = self.string(i, hashes, depth); continue
            if s[i] == '/':
                # Ordinary arithmetic is distinguishable after a simple operand. Other slash
                # fixity (including regex) needs Swift's expression grammar: refuse to guess.
                prefix = ''.join(self.output[:i]).rstrip()
                before = re.search(r"([\w]+|[)\]}])$", prefix)
                after = s[i + 1:].lstrip()
                word = before.group(1) if before else ''
                if (not before or word in {'return', 'throw', 'try', 'await', 'case', 'in', 'yield'}
                        or not re.match(r"(?:[\w(]|[+-]\s*[\w(]|=\s*[\w(])", after)):
                    raise SwiftScanError(i, "ambiguous slash/operator or bare regex is not measured")
            if s[i] == "'":
                raise SwiftScanError(i, "single-quoted literal is not supported Swift syntax")
            if interpolation:
                if s[i] == '(': parens += 1
                elif s[i] == ')':
                    if not parens: return i + 1
                    parens -= 1
            i += 1
        if interpolation:
            raise SwiftScanError(i, "unterminated string interpolation")
        return i

    def string(self, start: int, hashes: int, depth: int) -> int:
        s = self.source
        quote = start + hashes
        width = 3 if s.startswith('"""', quote) else 1
        close = '"' * width + '#' * hashes
        escape = '\\' + '#' * hashes
        i = quote + width
        self.erase(start, i)
        while i < len(s):
            if s.startswith(close, i):
                self.erase(i, i + len(close)); return i + len(close)
            if s.startswith(escape, i):
                following = i + len(escape)
                if following >= len(s): break
                if s[following] == '(':
                    self.erase(i, following)
                    i = self.code(following + 1, interpolation=True, depth=depth + 1)
                    continue
                if width == 1 and s[following] in '\r\n':
                    raise SwiftScanError(i, "newline in single-line string")
                self.erase(i, following + 1); i = following + 1; continue
            if width == 1 and s[i] in '\r\n':
                raise SwiftScanError(i, "newline in single-line string")
            self.erase(i, i + 1); i += 1
        raise SwiftScanError(start, "unterminated string literal")


def swift_body_spans(source: str) -> dict:
    """Return lexical function bodies and explicit measurement failures, never next-decl slices.

    Every named body is a candidate, not necessarily a runnable test. Called-helper exclusions
    remain heuristic; @Test and test* names are explicit entry points and cannot be excluded.
    Nested named declarations are erased from parents, without resolving helper calls.
    """
    lexer = SwiftLexicalMask(source)
    result: dict = {"masked": "", "blocks": [], "diagnostics": [], "bodyless": 0}
    try:
        lexer.code()
        masked = ''.join(lexer.output)
        result['masked'] = masked
        pairs, stack = {}, []
        for i, ch in enumerate(masked):
            if ch in '([{': stack.append((ch, i))
            elif ch in ')]}':
                if not stack or stack[-1][0] != {')': '(', ']': '[', '}': '{'}[ch]:
                    raise SwiftScanError(i, "unmatched or mismatched delimiter")
                _, start = stack.pop(); pairs[start] = i
        if stack:
            raise SwiftScanError(stack[-1][1], "unterminated delimiter")

        def skip_space(i: int) -> int:
            while i < len(masked) and masked[i].isspace(): i += 1
            return i

        # Attributes can contain parentheses/default closures. Associate @Test only with the
        # declaration that follows its balanced attribute/modifier sequence, not a previous test.
        test_entries = set()
        declaration_prefixes = {}
        modifier = re.compile(r"(?:private|fileprivate|internal|public|open|package|static|class|final|"
                              r"override|mutating|nonmutating|nonisolated|isolated|distributed|"
                              r"borrowing|consuming|optional|dynamic)\b")
        for annotation in re.finditer(r"@[\w.]+", masked):
            is_test = annotation.group(0) in {'@Test', '@Testing.Test'}
            i = skip_space(annotation.end())
            if i < len(masked) and masked[i] == '(': i = pairs[i] + 1
            while True:
                i = skip_space(i)
                attr = re.match(r"@[\w.]+", masked[i:])
                mod = modifier.match(masked, i)
                if attr: i += attr.end()
                elif mod: i = mod.end()
                else: break
                i = skip_space(i)
                if i < len(masked) and masked[i] == '(': i = pairs[i] + 1
            if re.match(r"(?:func|struct|class|enum|actor|protocol|extension)\b", masked[i:]):
                declaration_prefixes[i] = min(annotation.start(), declaration_prefixes.get(i, i))
                if is_test: test_entries.add(i)

        # A protocol requirement has no executable body; distinguish that supported absence
        # from a malformed bodyless test declaration. Named type ranges also mask local types.
        types = []
        for match in re.finditer(r"\b(struct|class|enum|actor|protocol|extension)\s+[^\W\d]\w*", masked):
            i = match.end()
            while i < len(masked) and masked[i] not in '{};':
                if masked[i] in '([': i = pairs[i]
                i += 1
            if i < len(masked) and masked[i] == '{':
                types.append((match.start(), i, pairs[i], match.group(1)))

        declarations = []
        for match in re.finditer(r"\bfunc\b", masked):
            if match.start() in lexer.escaped_identifiers: continue
            i = skip_space(match.end())
            name_match = re.match(r"(?:[^\W\d]\w*|[=+*/%<>!&|^~?.-]+)", masked[i:])
            if not name_match:
                raise SwiftScanError(i, "function name is not supported")
            name = name_match.group(0)
            i = skip_space(i + name_match.end())
            if i < len(masked) and masked[i] == '<':
                opening, angle = i, 1; i += 1
                while i < len(masked) and angle:
                    if masked[i] == '<': angle += 1
                    elif masked[i] == '>' and masked[i - 1] != '-': angle -= 1
                    i += 1
                if angle: raise SwiftScanError(opening, "unterminated generic signature")
                i = skip_space(i)
            if i >= len(masked) or masked[i] != '(':
                raise SwiftScanError(i, "function parameter clause is not supported")
            i = pairs[i] + 1
            while i < len(masked):
                i = skip_space(i)
                if i >= len(masked) or masked[i] in '{};': break
                if re.compile(r"\b(?:func|var|let|init|subscript|struct|class|enum|actor|protocol)\b").match(masked, i): break
                if masked[i] in '([': i = pairs[i] + 1
                else: i += 1
            if i >= len(masked) or masked[i] != '{':
                if any(a < match.start() < end and kind == 'protocol' for a, _, end, kind in types):
                    result['bodyless'] += 1; continue
                raise SwiftScanError(match.start(), "function declaration has no measurable body")
            declarations.append({"name": name, "start": match.start(), "bodyStart": i + 1,
                                 "end": pairs[i], "line": source.count('\n', 0, match.start()) + 1,
                                 "testEntry": match.start() in test_entries or name.startswith('test')})
        for block in declarations:
            body = list(masked[block['bodyStart']:block['end']])
            nested = [(declaration_prefixes.get(child['start'], child['start']), child['end'] + 1) for child in declarations
                      if block['bodyStart'] <= child['start'] < block['end']]
            nested += [(declaration_prefixes.get(a, a), end + 1) for a, _, end, _ in types if block['bodyStart'] <= a < block['end']]
            for start, end in nested:
                for i in range(start - block['bodyStart'], end - block['bodyStart']):
                    if body[i] not in '\r\n': body[i] = ' '
            block['body'] = ''.join(body)
        result['blocks'] = declarations
    except (SwiftScanError, RecursionError) as error:
        pos = error.position if isinstance(error, SwiftScanError) else 0
        reason = error.reason if isinstance(error, SwiftScanError) else "lexer nesting limit exceeded"
        result['diagnostics'] = [{"line": source.count('\n', 0, pos) + 1, "reason": reason}]
        result['blocks'] = []
    return result


def pass_blind(root: Path, mutators: tuple[str, ...], readers: tuple[str, ...],
               scopes: list[dict] | None = None) -> dict:
    """After the last mutating call in a test body, does any reader appear?

    Name-based and deliberately generous: a reader called for an unrelated
    reason still counts, so the error runs toward reporting fewer blind tests
    than there are. A candidate with a mutator name and no later reader name
    needs source review: it may assert only the return value, or the name may
    describe a fixture factory/failure sentinel rather than a product mutation.
    """
    files = [f for f in root.rglob("*")
             if f.is_file() and f.suffix in {".rs", ".py", ".ts", ".js", ".go", ".swift", ".cs"}
             and ("test" in str(f).lower() or "spec" in str(f).lower())]
    examined = mutating = reread = 0
    decl_blocks = spec_blocks = 0
    findings: list[str] = []
    not_measured: list[str] = []
    swift_files = swift_measured = swift_entries = swift_helpers = swift_bodyless = 0
    scopes = scopes or []
    scope_uses = {id(row): 0 for row in scopes}
    scope_errors: list[str] = []
    scoped_counts = {name: 0 for name in sorted(SCOPE_CLASSES)}
    scoped_only_bodies = 0
    scope_identities = [(row.get("file"), row.get("name"), row.get("bodySHA256"),
                         row.get("callOffset")) for row in scopes]
    if len(scope_identities) != len(set(scope_identities)):
        scope_errors.append("duplicate call scope identities were supplied")
    # Which declared verbs appear anywhere in this corpus at all. A vocabulary
    # for another language half-matches — the generic verbs hit, the project's
    # own never do — and half-matching is what made 32 findings against a foreign
    # tree indistinguishable from 32 real ones. Recorded per run, not per test.
    seen_verbs: set[str] = set()
    for f in files:
        is_swift = f.suffix == ".swift"
        swift_files += int(is_swift)
        try:
            src = f.read_text(encoding="utf-8", errors="strict" if is_swift else "replace")
        except (OSError, UnicodeError) as error:
            if is_swift:
                not_measured.append(f"{f}:1 — Swift source could not be read ({type(error).__name__})")
            continue
        original_src = src
        swift = swift_body_spans(src) if is_swift else None
        if swift is not None:
            if swift["diagnostics"]:
                not_measured.extend(f"{f}:{d['line']} — {d['reason']}" for d in swift["diagnostics"])
                continue
            swift_measured += 1
            swift_bodyless += swift["bodyless"]
            src = swift["masked"]
        for v in mutators:
            if v not in seen_verbs and re.search(
                    r"(?<![A-Za-z0-9_])" + re.escape(v) + r"\w*\s*\(", src):
                seen_verbs.add(v)
        if swift is not None:
            decls = [(block["start"], block["name"], "decl") for block in swift["blocks"]]
            specs = []
            swift_entries += sum(block["testEntry"] for block in swift["blocks"])
        else:
            decls = [(m.start(), m.group(1), "decl") for m in DECL_RE.finditer(src)]
            specs = [(m.start(), _spec_label(src, m.end()), "spec")
                     for m in SPEC_HEAD_RE.finditer(src)]
        starts = sorted(decls + specs)
        decl_blocks += len(decls)
        spec_blocks += len(specs)
        # A function another function in the same file calls is a fixture helper,
        # not a test. Counting one inflates `examined` and can report it blind:
        # a helper that seeds a log and returns it mutates and never reads, which
        # is correct — its callers do the reading. Measured: one such helper was
        # reported as a blind test while every one of its four callers asserted on
        # what it built. Excluding them only ever removes findings, which is the
        # direction this pass is already committed to erring in.
        #
        # Only declarations can be helpers. An arrow-style `it(` block is never
        # called by name, so it has nothing to be excluded by.
        helpers = {n for _, n, k in starts if k == "decl"
                   and len(re.findall(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"\s*\(", src)) > 1}
        if swift is not None:
            helpers -= {block["name"] for block in swift["blocks"] if block["testEntry"]}
            swift_helpers += sum(block["name"] in helpers for block in swift["blocks"])
        for i, (pos, name, kind) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else len(src)
            body = swift["blocks"][i]["body"] if swift is not None else src[pos:end]
            source_body = (original_src[swift["blocks"][i]["bodyStart"]:swift["blocks"][i]["end"]]
                           if swift is not None else body)
            rel = f.relative_to(root).as_posix()
            body_digest = hashlib.sha256(source_body.encode()).hexdigest()
            body_scopes = [row for row in scopes if row.get("file") == rel and
                           row.get("name") == name and row.get("bodySHA256") == body_digest]
            if kind == "decl" and name in helpers and not any(
                    row.get("classification") == "attributed-helper" for row in body_scopes):
                continue
            examined += 1
            calls = []
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
                    calls.append((m.start(), m.end(), v))
            if calls:
                mutating += 1
            ignored: set[tuple[int, int, str]] = set()
            for row in body_scopes:
                matches = [call for call in calls if call[0] == row.get("callOffset") and
                           call[2] == row.get("mutator") and
                           call_fingerprint(source_body, call[0], call[1]) == row.get("callSHA256")]
                if len(matches) != 1:
                    scope_errors.append(f"{rel}:{name} scope does not bind exactly one current call")
                    continue
                ignored.add(matches[0]); scope_uses[id(row)] += 1
                scoped_counts[row["classification"]] += 1
            calls = [call for call in calls if call not in ignored]
            last_call = max(calls, default=None, key=lambda call: call[0])
            last, which = (-1, None) if last_call is None else (last_call[0], last_call[2])
            if last < 0:
                scoped_only_bodies += bool(ignored)
                continue
            tail = body[last:]
            if any(re.search(re.escape(rd) + r"\w*", tail) for rd in readers):
                reread += 1
            else:
                location = f"{f}:{swift['blocks'][i]['line']}" if swift is not None else str(f)
                findings.append(f"{name} — last mutator '{which}', no read after it "
                                f"({location})")
    for row in scopes:
        if scope_uses[id(row)] != 1:
            scope_errors.append(f"{row.get('file')}:{row.get('name')} scope matched "
                                f"{scope_uses[id(row)]} bodies/calls, expected exactly one")
    return {"files": len(files), "examined": examined, "mutating": mutating,
            "reread": reread, "findings": findings, "seenVerbs": seen_verbs,
            "declBlocks": decl_blocks, "specBlocks": spec_blocks,
            "notMeasured": not_measured, "swiftFiles": swift_files,
            "swiftMeasuredFiles": swift_measured, "swiftTestEntries": swift_entries,
            "swiftExcludedHelpers": swift_helpers, "swiftBodylessRequirements": swift_bodyless,
            "scopeFindings": scope_errors, "scopedCounts": scoped_counts,
            "scopeRecords": len(scopes), "scopedOnlyBodies": scoped_only_bodies}


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
    blind_scopes, scope_load_findings = load_blind_scopes(d, campaign.get("blindScopeFile"))
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
                res = pass_blind(root, muts, rds, blind_scopes)
                if res["swiftFiles"]:
                    print(f"  Swift: files={res['swiftFiles']} measured-files={res['swiftMeasuredFiles']} "
                          f"unmeasured-files={len(res['notMeasured'])} "
                          f"explicit-test-entries={res['swiftTestEntries']} "
                          f"called-helpers-excluded={res['swiftExcludedHelpers']} "
                          f"bodyless-protocol-requirements={res['swiftBodylessRequirements']}")
                    if res["scopeRecords"]:
                        counts = ", ".join(f"{key}={value}" for key, value in
                                           sorted(res["scopedCounts"].items()))
                        print(f"  Swift scopes: records={res['scopeRecords']} · "
                              f"scoped-only-bodies={res['scopedOnlyBodies']} · {counts}")
                    print("  Swift discovery: uncalled named functions remain candidates, not proven test entries; "
                          "nested declarations supply no parent calls. Helper effects and reader independence "
                          "are not resolved.")
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
                    print(f"  blocks: declaration-style {res['declBlocks']} · "
                          f"arrow-style it/test {res['specBlocks']}")
                    print(f"  vocabulary: {source} — {len(muts)} mutator(s), {len(rds)} reader(s)")
                    print(f"  readers: {', '.join(rds)}")
                    for line in blind_findings[:20]:
                        print(f"  · {line}")
                # Missing measurements are independent of vocabulary fit and cannot be erased by
                # clean findings from other files (or by a vocabulary warning).
                for diagnostic in res["notMeasured"]:
                    print(f"blind:      NOT MEASURED — {diagnostic}")
                blind_findings.extend(res["notMeasured"])
                for diagnostic in scope_load_findings + res["scopeFindings"]:
                    print(f"blind:      INVALID SCOPE — {diagnostic}")
                blind_findings.extend(scope_load_findings)
                blind_findings.extend(res["scopeFindings"])
                if not res["examined"]:
                    print(f"blind:      NOT MEASURED — {res['files']} file(s) scanned and "
                          "0 test blocks recognised; an empty measured population cannot clear.")
                    blind_findings.append(f"the blind pass recognised 0 test blocks in {res['files']} "
                                          f"file(s) under {root} — a result over an empty population")

    findings = len(unclassed) + len(uncensused) + len(blind_findings)
    print(f"\nvacuity: requirements={total} external={declared} findings={findings}")
    if args.gate and findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
