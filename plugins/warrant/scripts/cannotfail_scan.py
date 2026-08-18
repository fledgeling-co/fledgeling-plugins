#!/usr/bin/env python3
"""Find the assertions that cannot fail, which is how a suite passes blind.

A suite's green is only worth what its assertions can detect, and several common
shapes can detect nothing at all: an expect with no matcher, a matcher handed
the value it was given, two constants compared with each other, a catch that
swallows the failure it caught, an assertion inside a callback nobody awaits, a
skipped or todo test, a soft assertion whose result is never read, and a spec
file with no assertions in it.

This reports rather than gates. The count is a trend, and a first run that
returns a bad number is a success -- a first run that returns no number is not.
So it exits 0 with the count and leaves the judgement to the ratchet.

Detection reads the file with strings and comments masked, so an expect inside a
comment is not a finding, and then reads the argument text back out of the
original, because two different string literals must not compare equal. The
unawaited-callback rule is a heuristic and says so in its detail line: a callback
registered on an event handler and never awaited is reported, while callbacks the
test runner owns (test, it, describe, the hooks) and callbacks reached through
await, return or .then are not.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402
# The masker lives in mutate.py; both planes need the same idea of what counts as
# code, and a second copy is a second place for the two to disagree.
from mutate import MASKED, mask_noncode                            # noqa: E402

DEFAULT_GLOBS = ("*.spec.ts", "*.spec.tsx", "*.spec.js", "*.spec.jsx",
                 "*.test.ts", "*.test.tsx", "*.test.js", "*.test.jsx")
SKIP_DIRS = frozenset((".git", "node_modules", ".next", "dist", "build", "coverage",
                       ".warrant", "__pycache__"))

_RUNNER = re.compile(r"^(test|it|describe|suite|context|"
                     r"before|after|beforeEach|afterEach|beforeAll|afterAll)(\.\w+)*$")
_KEYWORD_BLOCK = re.compile(r"\b(if|for|while|switch|with)\s*\([^{;]*\)\s*$")
_KEYWORD_BARE = re.compile(r"\b(try|else|do|finally)\s*$")
_CATCH_BLOCK = re.compile(r"\bcatch\s*(\([^)]*\))?\s*$")
_ARROW = re.compile(r"=>\s*$")
_FUNCTION_BLOCK = re.compile(r"\bfunction\b[^{;]*\)\s*$")
_NAMED_FUNCTION = re.compile(r"\bfunction\s+[A-Za-z_$][\w$]*\s*\(")
_METHOD_BLOCK = re.compile(r"[\w$]\s*\([^{;]*\)\s*$")
_AWAITED = re.compile(r"\b(await|return|yield)\b|\.then\s*\(")
_CALLEES = re.compile(r"(?<![\w$.])([A-Za-z_$][\w$.]*)\s*\(")
_SKIPPED = re.compile(r"\b(?:(test|it|describe|suite)\s*\.\s*(skip|todo|fixme)|"
                      r"(xit|xtest|xdescribe))\s*\(")
_SOFT_READ = re.compile(r"test\s*\.\s*info\s*\(\s*\)\s*\.\s*errors")
_LITERAL = (r"(?:'[^']*'|\"[^\"]*\"|`[^`]*`|-?\d+(?:\.\d+)?|true|false|null|undefined|"
            r"\[\s*\]|\{\s*\})")
_CONSTANT = re.compile(rf"^\s*{_LITERAL}(?:\s*[-+*/]\s*{_LITERAL})*\s*$")
_CONSOLE_ONLY = re.compile(r"^(?:\s*console\s*\.\s*\w+\s*\([^;]*\)\s*;?\s*)+$")


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _snippet(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    return text[start:len(text) if end < 0 else end].strip()[:140]


def _balanced(mask: str, open_at: int) -> int:
    """Offset just past the parenthesis group starting at open_at, or -1."""
    depth = 0
    for i in range(open_at, len(mask)):
        if mask[i] == "(":
            depth += 1
        elif mask[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    return -1


def _head_of(flat: str, window_start: int, brace_at: int) -> str:
    """The text that introduces the block at brace_at, within its parent block.

    Scoped to the parent rather than to the file: the head has to be found by
    local paren counting, and one unmatched parenthesis anywhere -- a regex
    literal is enough -- would otherwise desynchronise every head after it. A
    window bounded by the enclosing brace keeps the damage to one block.
    """
    window = flat[window_start:brace_at]
    depth, last = 0, 0
    for index, char in enumerate(window):
        if char in "([":
            depth += 1
        elif char in ")]":
            depth = max(0, depth - 1)
        elif char == ";" and depth == 0:
            last = index + 1
    return window[last:]


def blocks(mask: str) -> list[dict[str, Any]]:
    """Every brace region, classified by the text that introduces it.

    Braces are paired on their own, without trying to decide first whether each
    one opens a block or an object: the pairing is what has to be right, and the
    classification is then a bounded question about one region's head. A callback
    the runner owns (test, it, describe, the hooks) or one reached through await,
    return or .then does not need an await of its own.
    """
    flat = mask.replace(MASKED, " ")          # length-preserving, so offsets hold
    pairs: list[tuple[int, int, int]] = []    # (start, end, parent_start)
    stack: list[int] = []
    for i, char in enumerate(flat):
        if char == "{":
            stack.append(i)
        elif char == "}" and stack:
            start = stack.pop()
            pairs.append((start, i, stack[-1] if stack else -1))
    for start in stack:                        # unbalanced: assume it runs to the end
        pairs.append((start, len(flat), -1))

    frames: list[dict[str, Any]] = []
    by_start: dict[int, dict[str, Any]] = {}
    for start, end, parent in sorted(pairs):
        head = _head_of(flat, parent + 1 if parent >= 0 else 0, start).rstrip()
        # A callback held in an object property is introduced by the call that
        # takes the object, so the head has to reach through an object-literal
        # parent -- otherwise `await run(page, { apply: async () => {` looks
        # unawaited. The parent is always classified first, being earlier.
        parent_frame = by_start.get(parent)
        if parent_frame is not None and parent_frame["kind"] == "object":
            head = (parent_frame["head_full"] + " " + head).strip()
        if _CATCH_BLOCK.search(head):
            kind = "catch"
        elif _KEYWORD_BLOCK.search(head) or _KEYWORD_BARE.search(head):
            kind = "plain"
        elif _ARROW.search(head):
            # An arrow assigned to a name is a helper, awaited at its call sites,
            # not a callback handed to something that may never await it.
            stem = head[:head.rfind("=>")]
            kind = "function" if re.search(r"(?<![=!<>])=(?!=)", stem) else "callback"
        elif _FUNCTION_BLOCK.search(head):
            kind = "function" if _NAMED_FUNCTION.search(head) else "callback"
        elif _METHOD_BLOCK.search(head):
            kind = "function"
        else:
            kind = "object"
        callees = [name for name in _CALLEES.findall(head) if name != "async"]
        frame = {
            "kind": kind,
            "start": start,
            "end": end,
            "head": " ".join(head.split())[:140],
            "head_full": head,
            # Any runner call in the head is enough: a multi-line test(...) puts
            # its callee several arguments before the callback it registers.
            "runner": any(_RUNNER.match(name) for name in callees),
            "awaited": bool(_AWAITED.search(head)),
        }
        frames.append(frame)
        by_start[start] = frame
    return frames


def _enclosing_callback(frames: list[dict[str, Any]], offset: int) -> dict[str, Any] | None:
    inner = [f for f in frames
             if f["kind"] in ("callback", "function") and f["start"] < offset < f["end"]]
    if not inner:
        return None
    return max(inner, key=lambda f: f["start"])


def scan_text(text: str, label: str, ext: str = ".ts") -> list[dict[str, Any]]:
    """Every finding in one spec file, in file order."""
    mask = mask_noncode(text, ext)
    frames = blocks(mask)
    findings: list[dict[str, Any]] = []

    def add(pattern: str, offset: int, detail: str) -> None:
        findings.append({"file": label, "line": _line_of(text, offset), "pattern": pattern,
                         "detail": detail, "snippet": _snippet(text, offset)})

    soft_offsets: list[int] = []
    expect_calls = 0

    for match in re.finditer(r"(?<![\w$.])expect\s*(\.\s*soft\s*)?\(", mask):
        soft = match.group(1) is not None
        open_at = mask.index("(", match.end() - 1)
        close = _balanced(mask, open_at)
        if close < 0:
            continue
        expect_calls += 1
        actual = text[open_at + 1:close - 1]
        if soft:
            soft_offsets.append(match.start())

        rest = mask[close:]
        stripped = rest.lstrip()
        if not stripped.startswith("."):
            add("expect_without_matcher", match.start(),
                "expect() with no matcher call: the value is computed and then dropped")
            continue

        # Walk the chain (.not, .resolves, .rejects) to the first called member.
        cursor = close + (len(rest) - len(stripped))
        matcher = None
        while True:
            chain = re.match(r"\.\s*([A-Za-z_$][\w$]*)\s*", mask[cursor:])
            if not chain:
                break
            after = cursor + chain.end()
            if after < len(mask) and mask[after] == "(":
                matcher = chain.group(1)
                matcher_close = _balanced(mask, after)
                expected = text[after + 1:matcher_close - 1] if matcher_close > 0 else ""
                break
            cursor = after
        if matcher is None:
            continue

        left, right = actual.strip(), expected.strip()
        if _CONSTANT.match(left) and _CONSTANT.match(right):
            add("constant_comparison", match.start(),
                f"{left} compared with {right}: both sides are constants, so the "
                f"assertion holds whatever the code does")
        elif re.sub(r"\s+", "", left) == re.sub(r"\s+", "", right) and left:
            add("self_comparison", match.start(),
                f"expect({left}).{matcher}({right}): the expected value is the actual value")

        enclosing = _enclosing_callback(frames, match.start())
        if enclosing and enclosing["kind"] == "callback" \
                and not enclosing["runner"] and not enclosing["awaited"]:
            add("assertion_in_unawaited_callback", match.start(),
                f"assertion inside a callback nothing awaits ({enclosing['head']}); "
                f"a failure here may be raised after the test has already passed "
                f"(heuristic: await, return, .then or a runner callback would clear it)")

    for frame in frames:
        if frame["kind"] != "catch":
            continue
        body = mask[frame["start"] + 1:frame["end"]].replace(MASKED, " ")
        if not body.strip():
            add("empty_catch", frame["start"],
                "catch block with an empty body: the failure it caught is discarded")
        elif _CONSOLE_ONLY.match(body):
            add("empty_catch", frame["start"],
                "catch block that only logs: the failure it caught is discarded")

    for match in _SKIPPED.finditer(mask):
        add("skipped_test", match.start(),
            f"{match.group(0).strip()[:40]} never runs, so nothing it asserts is checked")

    if soft_offsets and not _SOFT_READ.search(mask):
        for offset in soft_offsets:
            add("discarded_soft_assertion", offset,
                "expect.soft() records a failure without failing the test, and this file "
                "never reads test.info().errors, so the result is discarded")

    if expect_calls == 0:
        findings.append({"file": label, "line": 1, "pattern": "no_expect_in_spec",
                         "detail": "spec file with no expect() calls at all",
                         "snippet": _snippet(text, 0)})

    findings.sort(key=lambda f: (f["line"], f["pattern"]))
    return findings


def scan_files(paths: list[pathlib.Path], root: pathlib.Path | None = None) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for path in paths:
        try:
            label = str(path.relative_to(root)) if root else str(path)
        except ValueError:
            label = str(path)
        findings.extend(scan_text(path.read_text(errors="replace"), label, path.suffix))
    by_pattern: dict[str, int] = {}
    for finding in findings:
        by_pattern[finding["pattern"]] = by_pattern.get(finding["pattern"], 0) + 1
    dirty = {f["file"] for f in findings}
    return {
        "files": len(paths),
        "clean_files": len(paths) - len(dirty),
        "findings": findings,
        "count": len(findings),
        "by_pattern": dict(sorted(by_pattern.items())),
    }


def spec_files(target: pathlib.Path, globs: tuple[str, ...]) -> list[pathlib.Path]:
    if not target.exists():
        raise _state.Absent(str(target))
    if target.is_file():
        return [target]
    found: set[pathlib.Path] = set()
    for pattern in globs:
        found.update(p for p in target.rglob(pattern)
                     if p.is_file() and not (SKIP_DIRS & set(p.parts)))
    return sorted(found)


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    target = pathlib.Path(args.input).expanduser().resolve() if args.input else root
    globs = tuple(g.strip() for g in args.glob.split(",") if g.strip())
    paths = spec_files(target, globs)
    if not paths:
        _cli.say(args, f"no spec files matching {args.glob} under {target}")
        return _cli.MISSING

    result = scan_files(paths, root if target.is_dir() else None)
    result["input"] = str(target)
    result["generated_at"] = _cli.now(args).isoformat()

    _cli.say(args, f"{result['count']} finding(s) across {result['files']} spec file(s)")
    _cli.say(args, "files with nothing found: "
                   + _cli.rate(result["clean_files"], result["files"], "spec files"))
    for pattern, count in result["by_pattern"].items():
        _cli.say(args, f"  {pattern}: {count}")
    for finding in result["findings"]:
        _cli.say(args, f"  {finding['file']}:{finding['line']} {finding['pattern']} "
                       f"-- {finding['detail']}")
    _cli.emit(args, result)
    return _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--input", help="spec file or directory of them (default: --root)")
    p.add_argument("--glob", default=",".join(DEFAULT_GLOBS),
                   help="comma-separated filename patterns for spec discovery")


def selftest() -> list[tuple[str, bool]]:
    """Each pattern observed firing on the dirty fixture and silent on the clean one."""
    import contextlib
    import io

    cases: list[tuple[str, bool]] = []
    fx = (pathlib.Path(__file__).resolve().parent.parent
          / "evals" / "fixtures" / "oracle-assay" / "cannotfail")

    dirty = scan_text((fx / "dirty.spec.ts").read_text(), "dirty.spec.ts", ".ts")
    clean = scan_text((fx / "clean.spec.ts").read_text(), "clean.spec.ts", ".ts")
    empty = scan_text((fx / "empty.spec.ts").read_text(), "empty.spec.ts", ".ts")
    dirty_patterns = {f["pattern"] for f in dirty}
    clean_patterns = {f["pattern"] for f in clean}

    for pattern in ("expect_without_matcher", "self_comparison", "constant_comparison",
                    "empty_catch", "assertion_in_unawaited_callback", "skipped_test",
                    "discarded_soft_assertion"):
        cases.append((f"{pattern} fires on the dirty spec", pattern in dirty_patterns))
        cases.append((f"{pattern} stays silent on the clean spec",
                      pattern not in clean_patterns))

    cases.append(("the clean spec produces no findings at all", clean == []))
    cases.append(("no_expect_in_spec fires on a spec with no assertions",
                  {f["pattern"] for f in empty} == {"no_expect_in_spec"}))
    cases.append(("no_expect_in_spec stays silent where assertions exist",
                  "no_expect_in_spec" not in clean_patterns
                  and "no_expect_in_spec" not in dirty_patterns))

    by_pattern = {f["pattern"]: f for f in dirty}
    cases.append(("a finding names its line",
                  by_pattern["expect_without_matcher"]["line"] == 6))
    cases.append(("the self comparison is the one with matching sides",
                  "expect(total).toBe(total)" in by_pattern["self_comparison"]["detail"]))
    cases.append(("both constant comparisons are found",
                  sum(1 for f in dirty if f["pattern"] == "constant_comparison") == 2))
    cases.append(("two skipped declarations are found",
                  sum(1 for f in dirty if f["pattern"] == "skipped_test") == 2))
    cases.append(("the unawaited finding names the callback it found",
                  "page.on" in by_pattern["assertion_in_unawaited_callback"]["detail"]))
    cases.append(("the unawaited rule declares itself a heuristic",
                  "heuristic" in by_pattern["assertion_in_unawaited_callback"]["detail"]))

    # Near misses that must not fire, and the same shape mutated until it does.
    cases.append(("two different string literals do not read as a self comparison",
                  scan_text("expect('a').toBe('b');", "t.ts") == []
                  or all(f["pattern"] != "self_comparison"
                         for f in scan_text("expect('a').toBe('b');", "t.ts"))))
    cases.append(("a chained matcher still resolves",
                  any(f["pattern"] == "self_comparison"
                      for f in scan_text("expect(x).not.toBe(x);", "t.ts"))))
    cases.append(("an expect inside a comment is not a finding",
                  scan_text("// expect(x);\nexpect(a).toBe(1);\n", "t.ts") == []))
    cases.append(("a catch that only logs is a finding",
                  any(f["pattern"] == "empty_catch"
                      for f in scan_text("try { go(); } catch (e) { console.log(e); }\n"
                                         "expect(a).toBe(1);", "t.ts"))))
    cases.append(("a catch that rethrows is not",
                  all(f["pattern"] != "empty_catch"
                      for f in scan_text("try { go(); } catch (e) { throw e; }\n"
                                         "expect(a).toBe(1);", "t.ts"))))
    cases.append(("a runner callback is not reported as unawaited",
                  all(f["pattern"] != "assertion_in_unawaited_callback"
                      for f in scan_text("test('x', async ({ page }) => { "
                                         "expect(await page.title()).toBe('y'); });", "t.ts"))))
    cases.append(("an awaited callback is not reported as unawaited",
                  all(f["pattern"] != "assertion_in_unawaited_callback"
                      for f in scan_text("await Promise.all(xs.map(async (x) => { "
                                         "expect(x).toBe(1); }));", "t.ts"))))
    cases.append(("expect.soft with an errors check is not reported",
                  all(f["pattern"] != "discarded_soft_assertion"
                      for f in scan_text("expect.soft(a).toBe(1);\n"
                                         "expect(test.info().errors).toHaveLength(0);", "t.ts"))))

    def run(argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = _cli.entry("selftest", main, None, _extra, argv)
        return rc, out.getvalue(), err.getvalue()

    rc, out, err = run(["--root", str(fx), "--input", str(fx), "--json"])
    import json
    payload = json.loads(out)
    cases.append(("a directory of specs is scanned", payload["files"] == 3))
    cases.append(("a dirty suite still exits 0, because this reports", rc == _cli.OK))
    cases.append(("the count travels with its population",
                  "of 3 spec files" in err))
    cases.append(("clean_files counts only the untouched ones", payload["clean_files"] == 1))

    rc, _, _ = run(["--root", str(fx), "--input", str(fx / "clean.spec.ts"), "--json"])
    cases.append(("a clean spec exits 0 with nothing found", rc == _cli.OK))
    rc, _, _ = run(["--root", str(fx), "--input", str(fx / "nope.spec.ts"), "--json"])
    cases.append(("an absent input exits 3", rc == _cli.MISSING))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
