"""Common CLI surface for every warrant script.

Every script inherits --help, --root, --json, --now and --selftest from here
rather than re-declaring them, so the flags and the exit codes cannot drift
between scripts. See references/script-contract.md.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import typing
import json
import os
import sys
from typing import Any, Callable, Sequence

OK = 0            # the check ran and the thing checked is sound
ERROR = 1         # the script could not run
FAILED = 2        # the check ran and the thing checked failed
MISSING = 3       # a precondition is absent
REVOKED = 4       # a revocation fired (ratchet.py only)


class _Parser(argparse.ArgumentParser):
    """Argparse exits 2 on a usage error, and this contract reserves 2 for
    'the check ran and the thing checked failed'. Left alone, a mistyped flag in
    a CI invocation is indistinguishable from a real gate failure, which is the
    one confusion that makes a gate untrustworthy. Usage errors exit 1."""

    def error(self, message: str) -> "typing.NoReturn":   # type: ignore[name-defined]
        self.print_usage(sys.stderr)
        print(f"{self.prog}: usage error: {message}", file=sys.stderr)
        raise SystemExit(ERROR)


def parser(description: str) -> argparse.ArgumentParser:
    p = _Parser(description=description)
    p.add_argument("--root", default=os.environ.get("WARRANT_ROOT", os.getcwd()),
                   help="repository under verification (default: $PWD)")
    p.add_argument("--json", action="store_true",
                   help="emit one JSON object on stdout; human output on stderr")
    p.add_argument("--now", default=os.environ.get("WARRANT_NOW"),
                   help="ISO 8601 instant, overriding the clock so tests are deterministic")
    p.add_argument("--selftest", action="store_true",
                   help="run this script's own fixtures; exit 0 only if every rule fired")
    return p


def now(args: argparse.Namespace) -> _dt.datetime:
    if getattr(args, "now", None):
        return _dt.datetime.fromisoformat(args.now.replace("Z", "+00:00"))
    return _dt.datetime.now(_dt.timezone.utc)


def say(args: argparse.Namespace, *parts: object) -> None:
    """Human output. Goes to stderr under --json so stdout stays parseable."""
    stream = sys.stderr if getattr(args, "json", False) else sys.stdout
    print(*parts, file=stream)


def emit(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    """The machine result. Only ever written under --json, only ever to stdout."""
    if getattr(args, "json", False):
        json.dump(payload, sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write("\n")


def rate(numerator: int, denominator: int, label: str) -> str:
    """A percentage never travels without its population.

    C19: published proficiency-test failure rates differ more than twentyfold
    by denominator, and both figures were correct. A bare percentage is the
    shape that error arrives in.
    """
    if denominator <= 0:
        return f"{numerator} {label} (no denominator; no rate is meaningful)"
    pct = 100.0 * numerator / denominator
    return f"{pct:.1f}% ({numerator} of {denominator} {label})"


def run(main: Callable[[argparse.Namespace], int],
        selftest: Callable[[], list[tuple[str, bool]]] | None,
        args: argparse.Namespace) -> int:
    """Dispatch to --selftest or to main, and turn an unexpected raise into exit 1."""
    if args.selftest:
        if selftest is None:
            print("no selftest defined for this script", file=sys.stderr)
            return ERROR
        results = selftest()
        width = max(len(name) for name, _ in results) if results else 0
        failed = 0
        for name, passed in results:
            print(f"  {'ok  ' if passed else 'FAIL'}  {name:<{width}}", file=sys.stderr)
            failed += 0 if passed else 1
        print(f"{len(results)} case(s), {failed} failure(s)", file=sys.stderr)
        return OK if failed == 0 else FAILED
    try:
        return main(args)
    except SystemExit:
        raise
    except FileNotFoundError as exc:
        print(f"precondition absent: {exc}", file=sys.stderr)
        return MISSING
    except Exception as exc:                                  # noqa: BLE001
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return ERROR


def entry(description: str,
          main: Callable[[argparse.Namespace], int],
          selftest: Callable[[], list[tuple[str, bool]]] | None = None,
          extra: Callable[[argparse.ArgumentParser], None] | None = None,
          argv: Sequence[str] | None = None) -> int:
    p = parser(description)
    if extra:
        extra(p)
    return run(main, selftest, p.parse_args(argv))
