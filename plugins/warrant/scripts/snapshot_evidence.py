#!/usr/bin/env python3
"""Take a content-addressed, read-only snapshot of the evidence before judging.

Every artifact a verdict rests on is reachable by the thing being judged. Frontier
coding agents modify tests, overwrite timers and monkey-patch evaluators to return
success; 30.4% of RE-Bench runs exhibited reward hacking and on some tasks every
successful run did. So the diff, the test files and the captures are copied to
`.warrant/snapshots/<digest>/files/` and set read-only BEFORE any lane runs, and
the verdict records the digest. A verdict whose digest does not match is void —
`lane_run.py` enforces that with `verify()` below.

The digest is sha256 over `sha256(content)  relpath` lines, sorted by path, so it
is reproducible from the files alone: same contents at the same paths, same
digest, on any machine and in any flag order. Paths must therefore resolve under
`--root`; an absolute path from outside the tree would put a machine-specific
string into the digest, so it exits 1 instead.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import pathlib
import shutil
import stat
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

MANIFEST = "manifest.json"
FILES_DIR = "files"
READ_ONLY = 0o444

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".warrant", "dist", "build",
             ".next", ".venv", ".pytest_cache", ".mypy_cache"}


def sha256_file(path: pathlib.Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def digest_of(entries: list[dict[str, object]]) -> str:
    """sha256 over `<file digest>  <relpath>` lines, sorted by path."""
    h = hashlib.sha256()
    for entry in sorted(entries, key=lambda e: str(e["path"])):
        h.update(f"{entry['sha256']}  {entry['path']}\n".encode())
    return h.hexdigest()


def _collect(root: pathlib.Path, targets: list[tuple[str, str]],
             notes: list[str]) -> list[dict[str, object]]:
    """Expand each --diff/--tests/--captures/--include target into file entries."""
    seen: dict[str, dict[str, object]] = {}
    for role, raw in targets:
        target = pathlib.Path(raw).expanduser()
        if not target.is_absolute():
            target = root / target
        target = target.resolve()
        try:
            rel_check = target.relative_to(root)
        except ValueError:
            raise ValueError(
                f"{raw} resolves outside --root ({target}); the digest is over "
                "repository-relative paths, so an outside path would make it "
                "machine-specific. Copy the file under the root first")
        if not target.exists():
            raise FileNotFoundError(f"{role} target does not exist: {target}")
        del rel_check

        candidates: list[pathlib.Path] = []
        if target.is_dir():
            for dirpath, dirnames, filenames in os.walk(target):
                dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
                for name in sorted(filenames):
                    candidates.append(pathlib.Path(dirpath) / name)
        else:
            candidates.append(target)

        for path in candidates:
            if path.is_symlink():
                notes.append(f"skipped symlink {path.relative_to(root)}: a link can "
                             "point outside the snapshot")
                continue
            if not path.is_file():
                continue
            rel = str(path.relative_to(root))
            sha, size = sha256_file(path)
            if rel in seen:
                if seen[rel]["sha256"] != sha:
                    notes.append(f"{rel} changed while the snapshot was being taken")
                continue
            seen[rel] = {"path": rel, "role": role, "sha256": sha, "bytes": size}
    return list(seen.values())


def _write_snapshot(root: pathlib.Path, digest: str, entries: list[dict[str, object]],
                    taken_at: str, notes: list[str]) -> tuple[pathlib.Path, list[str]]:
    """Copy the evidence in and set it read-only. Returns (dir, problems).

    Problems after the first copy are returned rather than raised: the effect has
    already happened, and raising invites a retry that does it twice.
    """
    snap = _state.state_dir(root, create=True) / "snapshots" / digest
    problems: list[str] = []
    dest_root = snap / FILES_DIR
    dest_root.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        src = root / str(entry["path"])
        dst = dest_root / str(entry["path"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            if dst.exists():
                dst.chmod(0o644)                # a re-snapshot has to be able to overwrite
            shutil.copy2(src, dst)
            dst.chmod(READ_ONLY)
        except OSError as exc:
            problems.append(f"{entry['path']}: {type(exc).__name__}: {exc}")

    manifest = {
        "schema": "warrant.snapshot/1",
        "digest": digest,
        "taken_at": taken_at,
        "root": str(root),
        "files": sorted(entries, key=lambda e: str(e["path"])),
        "file_count": len(entries),
        "total_bytes": sum(int(e["bytes"]) for e in entries),
        "notes": notes,
    }
    path = snap / MANIFEST
    try:
        if path.exists():
            path.chmod(0o644)
        path.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
        path.chmod(READ_ONLY)
    except OSError as exc:
        problems.append(f"{MANIFEST}: {type(exc).__name__}: {exc}")
    return snap, problems


def verify(root: str | pathlib.Path, digest: str) -> tuple[bool, list[str]]:
    """Re-derive a snapshot's digest from the files on disk.

    `lane_run.py` calls this before it will accept a verdict, so a snapshot that
    has been edited since it was taken cannot authorise anything.
    """
    root = pathlib.Path(root).expanduser().resolve()
    snap = _state.state_dir(root) / "snapshots" / digest
    manifest_path = snap / MANIFEST
    if not manifest_path.exists():
        return False, [f"no snapshot at {snap}"]
    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        return False, [f"{MANIFEST} is unreadable: {exc}"]

    problems: list[str] = []
    entries: list[dict[str, object]] = []
    for entry in manifest.get("files", []):
        rel = str(entry.get("path"))
        path = snap / FILES_DIR / rel
        if not path.is_file():
            problems.append(f"{rel} is missing from the snapshot")
            continue
        sha, size = sha256_file(path)
        if sha != entry.get("sha256"):
            problems.append(f"{rel} was modified after the snapshot was taken")
        entries.append({"path": rel, "sha256": sha, "bytes": size})
    recomputed = digest_of(entries)
    if recomputed != digest:
        problems.append(f"the snapshot re-derives as {recomputed}, not {digest}")
    if manifest.get("digest") != digest:
        problems.append(f"{MANIFEST} claims digest {manifest.get('digest')}")
    return not problems, problems


# ── main ─────────────────────────────────────────────────────────────────────

def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--diff", action="append", default=[], metavar="PATH",
                   help="the diff under judgement (file)")
    p.add_argument("--tests", action="append", default=[], metavar="PATH",
                   help="test file or directory (repeatable)")
    p.add_argument("--captures", action="append", default=[], metavar="PATH",
                   help="capture file or directory (repeatable)")
    p.add_argument("--include", action="append", default=[], metavar="PATH",
                   help="any other evidence the verdict rests on (repeatable)")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    targets = ([("diff", p) for p in args.diff]
               + [("tests", p) for p in args.tests]
               + [("captures", p) for p in args.captures]
               + [("other", p) for p in args.include])
    if not targets:
        _cli.say(args, "nothing to snapshot: pass --diff, --tests, --captures or --include")
        _cli.emit(args, {"ok": False, "reason": "no-targets", "digest": None})
        return _cli.MISSING

    notes: list[str] = []
    try:
        entries = _collect(root, targets, notes)
    except ValueError as exc:
        _cli.say(args, str(exc))
        _cli.emit(args, {"ok": False, "reason": "outside-root", "digest": None,
                         "detail": str(exc)})
        return _cli.ERROR

    if not entries:
        _cli.say(args, "the targets contain no files to snapshot")
        _cli.emit(args, {"ok": False, "reason": "no-files", "digest": None,
                         "notes": notes})
        return _cli.MISSING

    digest = digest_of(entries)
    snap = _state.state_dir(root) / "snapshots" / digest
    already = (snap / MANIFEST).exists()
    if already:
        ok, problems = verify(root, digest)
        if ok:
            _cli.say(args, f"already snapshotted: {snap}")
            for note in notes:
                _cli.say(args, f"  note: {note}")
            _cli.say(args, digest)
            _cli.emit(args, {"ok": True, "digest": digest, "snapshot": str(snap),
                             "file_count": len(entries), "reused": True,
                             "notes": notes, "problems": []})
            return _cli.OK
        notes.append("an existing snapshot at this digest did not verify "
                     f"({'; '.join(problems)}); it was rewritten")

    taken_at = _cli.now(args).isoformat()
    snap, problems = _write_snapshot(root, digest, entries, taken_at, notes)

    by_role: dict[str, int] = {}
    for entry in entries:
        by_role[str(entry["role"])] = by_role.get(str(entry["role"]), 0) + 1
    _cli.say(args, f"snapshot {snap}")
    _cli.say(args, "  " + ", ".join(f"{n} {role}" for role, n in sorted(by_role.items()))
                   + f", {sum(int(e['bytes']) for e in entries)} byte(s), read-only")
    for note in notes:
        _cli.say(args, f"  note: {note}")
    for problem in problems:
        _cli.say(args, f"  problem after copying: {problem}")
    _cli.say(args, digest)

    _cli.emit(args, {
        "ok": not problems,
        "digest": digest,
        "snapshot": str(snap),
        "taken_at": taken_at,
        "file_count": len(entries),
        "total_bytes": sum(int(e["bytes"]) for e in entries),
        "roles": by_role,
        "reused": False,
        "notes": notes,
        "problems": problems,
    })
    return _cli.OK


# ── selftest ─────────────────────────────────────────────────────────────────

def _call(*argv: str) -> tuple[int, str, str]:
    p = _cli.parser("selftest")
    extra(p)
    parsed = p.parse_args(list(argv))
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _cli.run(main, None, parsed)
    return code, out.getvalue(), err.getvalue()


def _repo(base: pathlib.Path, name: str, figure: str = "12.4") -> pathlib.Path:
    root = base / name
    (root / "e2e").mkdir(parents=True)
    (root / "captures").mkdir(parents=True)
    (root / "work.diff").write_text("--- a/x\n+++ b/x\n+one line\n")
    (root / "e2e" / "inbox.spec.ts").write_text(f"expect(total).toBe({figure})\n")
    (root / "e2e" / "helpers.ts").write_text("export const noop = () => {};\n")
    (root / "captures" / "inbox.txt").write_text("rendered total 12.4\n")
    return root


def _digest_from(out: str) -> str:
    return out.strip().splitlines()[-1].strip()


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-snapshot-"))
    try:
        a = _repo(tmp, "a")
        code, out, _ = _call("--root", str(a), "--diff", "work.diff",
                             "--tests", "e2e", "--captures", "captures",
                             "--now", "2026-08-19T00:00:00+00:00")
        cases.append(("takes a snapshot", code == _cli.OK))
        digest = _digest_from(out)
        cases.append(("prints a sha256 digest",
                      len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)))
        snap = _state.state_dir(a) / "snapshots" / digest
        cases.append(("the snapshot lands under .warrant/snapshots/<digest>",
                      (snap / MANIFEST).exists()))
        copied = snap / FILES_DIR / "e2e" / "inbox.spec.ts"
        cases.append(("evidence is copied in", copied.exists()))
        cases.append(("copied evidence is read-only",
                      not copied.stat().st_mode & stat.S_IWUSR))
        cases.append(("the manifest is read-only",
                      not (snap / MANIFEST).stat().st_mode & stat.S_IWUSR))
        cases.append(("the manifest records every file",
                      json.loads((snap / MANIFEST).read_text())["file_count"] == 4))

        # Reproducible: same contents at the same paths, same digest.
        b = _repo(tmp, "b")
        code, out_b, _ = _call("--root", str(b), "--diff", "work.diff",
                               "--tests", "e2e", "--captures", "captures")
        cases.append(("the digest is reproducible across roots",
                      _digest_from(out_b) == digest))
        code, out_order, _ = _call("--root", str(b), "--captures", "captures",
                                   "--tests", "e2e/helpers.ts", "--tests",
                                   "e2e/inbox.spec.ts", "--diff", "work.diff")
        cases.append(("the digest does not depend on flag order",
                      _digest_from(out_order) == digest))

        c = _repo(tmp, "c", figure="99.9")
        code, out_c, _ = _call("--root", str(c), "--diff", "work.diff",
                               "--tests", "e2e", "--captures", "captures")
        cases.append(("changed content changes the digest",
                      _digest_from(out_c) != digest))

        d = _repo(tmp, "d")
        (d / "e2e" / "inbox.spec.ts").rename(d / "e2e" / "renamed.spec.ts")
        code, out_d, _ = _call("--root", str(d), "--diff", "work.diff",
                               "--tests", "e2e", "--captures", "captures")
        cases.append(("a renamed file changes the digest",
                      _digest_from(out_d) != digest))

        ok, problems = verify(a, digest)
        cases.append(("a fresh snapshot verifies", ok and not problems))

        # The property the whole plane rests on: an edited snapshot cannot verify.
        tampered = snap / FILES_DIR / "e2e" / "inbox.spec.ts"
        tampered.chmod(0o644)
        tampered.write_text("expect(total).toBe(99.9)\n")
        ok, problems = verify(a, digest)
        cases.append(("a tampered snapshot fails verification", not ok))
        cases.append(("verification names the tampered file",
                      any("inbox.spec.ts" in p for p in problems)))
        tampered.write_text("expect(total).toBe(12.4)\n")
        tampered.chmod(READ_ONLY)
        ok, _ = verify(a, digest)
        cases.append(("restoring the byte restores verification", ok))

        removed = snap / FILES_DIR / "captures" / "inbox.txt"
        removed.chmod(0o644)
        removed.unlink()
        ok, problems = verify(a, digest)
        cases.append(("a missing snapshot file fails verification",
                      not ok and any("missing" in p for p in problems)))

        ok, problems = verify(a, "0" * 64)
        cases.append(("verifying an unknown digest fails",
                      not ok and any("no snapshot" in p for p in problems)))

        e = _repo(tmp, "e")
        code, out_e, _ = _call("--root", str(e), "--diff", "work.diff",
                               "--tests", "e2e", "--captures", "captures")
        code2, out2, _ = _call("--root", str(e), "--diff", "work.diff",
                               "--tests", "e2e", "--captures", "captures")
        cases.append(("re-snapshotting the same evidence is idempotent",
                      code2 == _cli.OK and "already snapshotted" in out2
                      and _digest_from(out2) == _digest_from(out_e)))

        outside = tmp / "outside.txt"
        outside.write_text("evidence from nowhere\n")
        code, out_o, _ = _call("--root", str(e), "--include", str(outside))
        cases.append(("a path outside --root exits 1",
                      code == _cli.ERROR and "outside --root" in out_o))

        code, out_n, _ = _call("--root", str(e))
        cases.append(("no targets exits 3", code == _cli.MISSING))
        (e / "hollow").mkdir()
        code, out_h, _ = _call("--root", str(e), "--include", "hollow")
        cases.append(("a target with no files exits 3", code == _cli.MISSING))
        code, out_m, _ = _call("--root", str(e), "--include", "nope.txt")
        cases.append(("a target that does not exist exits 3", code == _cli.MISSING))

        f = _repo(tmp, "f")
        os.symlink(f / "work.diff", f / "e2e" / "linked.diff")
        code, out_f, _ = _call("--root", str(f), "--tests", "e2e")
        cases.append(("a symlink is skipped and reported",
                      code == _cli.OK and "skipped symlink" in out_f))

        code, o, err = _call("--root", str(a), "--diff", "work.diff", "--json")
        cases.append(("--json puts only JSON on stdout",
                      o.lstrip().startswith("{") and "digest" in json.loads(o)))
        cases.append(("--json keeps the human summary on stderr", "snapshot" in err))
    finally:
        for path in tmp.rglob("*"):
            with contextlib.suppress(OSError):
                path.chmod(0o755)
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
