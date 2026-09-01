#!/usr/bin/env python3
"""A session's claims, checked against the repository and git.

signals.py reads what the session said and did. This reads what the repository
actually holds now, and pairs the two. It is the half that can say "this file was
never written" and "this commit contains no source", which no amount of transcript
reading establishes.

    crossref.py <signals.json> --repo <path> [--since ISO] [--until ISO] [--out crossref.json]

`--since` is load-bearing rather than a convenience. The audit this came from had
to separate what a session did from what a later session repaired, and got it
wrong twice — one finding cited a directory a *later* session had populated, and a
naive repo read would have cleared it. Every assertion here is made against a
window and says which.

Exit codes
    0   every claim resolved to a repo or git fact
    1   the repo is not in a state these claims can be checked against
    4   a claim whose shape could not be parsed — listed, never silently dropped
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

SCHEMA = 2

DONE_WORD = re.compile(r"\b(?:merged|verified|shipped|done|complete[d]?|closed)\b", re.I)
DURABLE = ("ARMADA.md", "ORCHESTRATOR.md", "LEDGER.md", "PRD.md", "ROADMAP.md")

# Handlers whose body cannot produce the effect their name promises.
INERT = [
    (r'Button\(\s*"[^"]*"\s*(?:,[^)]*)?\)\s*\{\s*\}', "SwiftUI button with an empty action"),
    (r'on(?:Click|Press|Tap|Submit)\s*=\s*\{\s*\(\s*\)\s*=>\s*\{\s*\}\s*\}', "handler bound to an empty arrow"),
    (r'func\s+\w+\([^)]*\)\s*\{\s*(?://[^\n]*\n\s*)?\}', "function body is empty"),
    (r'println!\([^)]*\);\s*(?:std::process::)?exit\(0\)', "subcommand that prints and exits 0"),
    (r'(?:return|=)\s*(?:format!|String::from|`)[^;\n]{0,120};?\s*//\s*TODO', "generator with a TODO and no caller"),
]

# A script that reports success unconditionally.
UNCONDITIONAL = re.compile(
    r'echo\s+["\'][^"\']*(?:correct|success|pass|ok|operating)[^"\']*["\']', re.I)


def git(repo: str, *args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, timeout=90)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as exc:
        return 1, f"{type(exc).__name__}: {exc}"


def commits(repo: str, since: str | None, until: str | None) -> list[dict]:
    args = ["log", "--format=%H%x1f%ad%x1f%an%x1f%s", "--date=iso"]
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")
    code, out = git(repo, *args)
    if code != 0:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) == 4:
            rows.append({"sha": parts[0][:12], "date": parts[1], "author": parts[2], "subject": parts[3]})
    return rows


_FILES_CACHE: dict[str, list[str]] = {}


def files_in(repo: str, sha: str) -> list[str]:
    if sha in _FILES_CACHE:
        return _FILES_CACHE[sha]
    code, out = git(repo, "show", "--stat", "--name-only", "--format=", sha)
    fs = [l.strip() for l in out.splitlines() if l.strip()] if code == 0 else []
    _FILES_CACHE[sha] = fs
    return fs


def finding(pid, title, band, confidence, remedy="", **extra):
    f = {"probe": pid, "title": title, "band": band, "confidence": confidence, "remedy": remedy}
    f.update(extra)
    return f


# ------------------------------------------------------------------- R-probes

ITEM_ID = re.compile(r"\b([A-Z]{2,6}-?\d{3,5})\b")


def r1_docs_only_commits(repo, sig, shas, out, notes):
    """An item reached a done-state and no commit anywhere carries its work.

    The naive form of this probe — "the commit that moved the row contains only
    markdown" — fires on the correct house pattern, where the ledger update is
    deliberately a separate commit from the work it records. Measured against a
    real repository it produced 13 hits, every one of them correct behaviour.

    So the question is asked over the item rather than over the commit: take the
    id out of the done-state subject, and look across all of history for any
    commit touching a non-documentation file that names it. Only an id with no
    such commit anywhere is a status that outran its work.
    """
    seen: set[str] = set()
    for c in shas:
        if not DONE_WORD.search(c["subject"]):
            continue
        for item in ITEM_ID.findall(c["subject"]):
            if item in seen:
                continue
            seen.add(item)
            code, o = git(repo, "log", "--all", "--format=%H", "--grep", item)
            if code != 0:
                continue
            carriers = []
            for sha in o.split()[:25]:
                fs = files_in(repo, sha)
                if any(not f.startswith("docs/") and not f.endswith(".md")
                       and os.path.basename(f) not in DURABLE for f in fs):
                    carriers.append(sha[:12])
                    break
            if carriers:
                continue
            out.append(finding(
                "R1", f"{item} reached a done-state and no commit in history carries its work",
                1, "observed", item=item, sha=c["sha"], subject=c["subject"][:90],
                remedy=f"git log --all --grep {item} — point the row at the work, or move it back"))



def r2_claimed_file_never_written(repo, sig, shas, out, notes):
    """A path cited as evidence that no commit anywhere in history touches.

    Checked against all of history rather than this session's window: a
    legitimate multi-commit feature writes a file in an earlier commit, and the
    narrow form false-positives on it.
    """
    seen: set[str] = set()
    for a in sig.get("assertions", []):
        for p in re.findall(r"`([\w./-]+\.(?:ts|tsx|js|mjs|py|swift|rs|go|md|json|sh))`", a["text"]):
            if p in seen or p.startswith(("http", "/tmp")):
                continue
            seen.add(p)
            if os.path.exists(os.path.join(repo, p)):
                continue
            # Reports often cite a source file by basename. If that basename is
            # tracked anywhere, it is not honest to say the file exists nowhere.
            if "/" not in p:
                code_names, tracked = git(repo, "ls-files")
                if code_names == 0 and any(os.path.basename(x) == p for x in tracked.splitlines()):
                    continue
            # A generated artefact the repo deliberately ignores is not a missing
            # file. Two `dist/goldens/*.json` paths were reported as never written
            # on a measured run, in a session whose own build printed itself
            # writing them.
            if git(repo, "check-ignore", "-q", p)[0] == 0:
                continue
            code, o = git(repo, "log", "--oneline", "--all", "--", p)
            if code == 0 and o.strip():
                continue
            out.append(finding(
                "R2", f"a cited path exists nowhere in the repo or its history: {p}",
                1 if a.get("durable") else 2, "observed", path=p, line=a["line"],
                quote=a["text"][:200],
                remedy=f"write {p}, or strike the claim that cites it"))


def r4_duplicate_captures(repo, sig, shas, out, notes):
    """Two differently-named captures that are one image."""
    import hashlib
    attributable = set(sig.get("attribution", {}).get("modified_paths", []))
    for c in shas:
        attributable.update(files_in(repo, c["sha"]))
    capture_paths = sorted(p for p in attributable
                           if p.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    digests: dict[str, list[str]] = {}
    n = 0
    for rel in capture_paths:
        fp = os.path.join(repo, rel)
        if not os.path.isfile(fp):
            continue
        try:
            with open(fp, "rb") as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
        except Exception:
            continue
        n += 1
        digests.setdefault(h, []).append(rel)
    if not n:
        notes.append("R4: no attributable capture path found; capture identity unchecked")
        return
    for h, paths in digests.items():
        if len(paths) < 2:
            continue
        stems = {re.sub(r"[-_]?\d+", "", os.path.splitext(os.path.basename(p))[0]) for p in paths}
        if len(stems) == 1 and len(paths) == 2:
            continue  # a shot and its own copy under one name is not a surface collision
        out.append(finding(
            "R4", f"{len(paths)} differently-named captures are one image ({h[:12]})",
            1, "observed", digest=h[:12], paths=paths[:8],
            remedy="re-capture each surface, or say plainly that they share one"))


def r6_isolation(repo, sig, shas, out, notes):
    """A fan-out claimed isolation that git never saw.

    Asserted on the reflog and on merged branches rather than on
    `git worktree list`: a completed fleet legitimately cleans its worktrees up,
    and counting them flags every correct run.
    """
    # The precondition is a *claim* of isolation, not the word appearing anywhere.
    # A session told to work serially in-session, that did so, was reported as
    # having claimed isolation it never claimed.
    claim = re.compile(r"\b(?:worktree|isolated branch|ai/[\w-]+|per-item branch)\b", re.I)
    if not any(claim.search(a["text"]) for a in sig.get("assertions", [])):
        return
    code, reflog = git(repo, "reflog", "--date=iso", "-n", "400")
    code2, merged = git(repo, "branch", "--all", "--merged")
    evidence = (reflog if code == 0 else "") + (merged if code2 == 0 else "")
    if re.search(r"\bai/\S+", evidence):
        return
    out.append(finding(
        "R6", "isolation is claimed and neither the reflog nor any merged branch names an ai/* branch",
        1, "strong-inference",
        remedy="git reflog | grep ai/ — or correct the ledger's worktree column"))


def r9_inert_controls(repo, sig, shas, out, notes):
    """Controls that render and do nothing, in files this window touched.

    A pointer, never a verdict: only a read decides whether an empty body is a
    stub or a deliberate no-op. Restricted to touched files so the probe reports
    this session's work rather than the repository's history.
    """
    touched: set[str] = set(sig.get("attribution", {}).get("modified_paths", []))
    hits = []
    for rel in sorted(touched):
        fp = os.path.join(repo, rel)
        if not os.path.isfile(fp) or os.path.getsize(fp) > 400_000:
            continue
        if not rel.endswith((".swift", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".kt", ".sh")):
            continue
        try:
            with open(fp, errors="replace") as fh:
                body = fh.read()
        except Exception:
            continue
        for rx, why in INERT:
            for m in re.finditer(rx, body):
                hits.append({"path": rel, "why": why,
                             "line": body[:m.start()].count("\n") + 1,
                             "quote": " ".join(m.group(0).split())[:120]})
        if rel.endswith(".sh") and UNCONDITIONAL.search(body) and "set -e" not in body \
                and not re.search(r"exit\s+[1-9]", body):
            hits.append({"path": rel, "why": "script reports success with no failing path",
                         "line": 1, "quote": "no `set -e`, no non-zero exit"})
    if not touched:
        notes.append("R9: no files attributable to this window; inert-control scan did not run")
        return
    for h in hits[:25]:
        out.append(finding(
            "R9", f"{h['why']}: {h['path']}:{h['line']}",
            2, "weak-inference", path=h["path"], line=h["line"], quote=h["quote"],
            remedy="open it and read for effect — a regex cannot tell a stub from a no-op"))


def r10_duplicate_module(repo, sig, shas, out, notes):
    """A new module nothing imports, beside an existing one everything imports."""
    touched = set(sig.get("attribution", {}).get("modified_paths", []))
    for rel in sorted(touched):
        fp = os.path.join(repo, rel)
        if not os.path.isfile(fp) or not rel.endswith((".ts", ".tsx", ".py", ".rs", ".go", ".swift")):
            continue
        # A test file is referenced only by the test runner by design. Asking
        # whether it has non-test callers is circular, and it buried the one
        # real hit in a measured run.
        if re.search(r"(?:^|/)(?:tests?|spec|__tests__)/|[.](?:test|spec)[.]|Tests?[.]swift$", rel):
            continue
        stem = os.path.splitext(os.path.basename(rel))[0]
        if len(stem) < 6:
            continue
        code, o = git(repo, "grep", "-l", stem, "--", ".")
        if code != 0:
            continue
        refs = [l for l in o.splitlines() if l.strip() and os.path.basename(l) != os.path.basename(rel)]
        nontest = [l for l in refs if "test" not in l.lower() and "spec" not in l.lower()]
        if refs and not nontest:
            out.append(finding(
                "R10", f"{rel} is referenced only by its own test — check for an existing module doing this",
                2, "strong-inference", path=rel, referenced_by=refs[:6],
                remedy=f"git grep {stem} — if a routed equivalent exists, this is a duplicate"))


def r11_weak_secret(repo, sig, shas, out, notes):
    """A credential resolved to a literal, or an env var read nowhere else.

    Handed to code-review rather than graded here. Included because a secret-scan
    that matches credential *shapes* cannot see a low-entropy literal, and one
    such literal shipped as a live auth bypass in the corpus this came from.
    """
    touched = set(sig.get("attribution", {}).get("modified_paths", []))
    rx = re.compile(
        r"(?P<name>[A-Za-z_]*(?:SECRET|TOKEN|KEY|PASSWORD|CREDENTIAL)[A-Za-z_]*)"
        r"[^\n]{0,80}?\|\|\s*['\"](?P<lit>[^'\"]{3,60})['\"]", re.I)
    for rel in sorted(touched):
        fp = os.path.join(repo, rel)
        if not os.path.isfile(fp) or os.path.getsize(fp) > 400_000:
            continue
        if not rel.endswith((".ts", ".tsx", ".js", ".mjs", ".py", ".go", ".rs", ".java", ".kt")):
            continue
        # A literal secret inside a test is how you test that a literal secret is
        # rejected. Flagging it reports the fix as the defect.
        if re.search(r"(?:^|/)(?:tests?|spec|__tests__|fixtures?)/|\.(?:test|spec)\.", rel, re.I):
            continue
        try:
            with open(fp, errors="replace") as fh:
                body = fh.read()
        except Exception:
            continue
        for m in rx.finditer(body):
            ln = body[:m.start()].count("\n") + 1
            env = re.search(r"process\.env\.([A-Z_]+)|getenv\(['\"]([A-Z_]+)", m.group(0))
            var = (env.group(1) or env.group(2)) if env else ""
            elsewhere = 0
            if var:
                c2, o2 = git(repo, "grep", "-c", var, "--", ".")
                elsewhere = sum(int(x.rsplit(":", 1)[-1]) for x in o2.splitlines()
                                if x.rsplit(":", 1)[-1].isdigit()) if c2 == 0 else 0
            out.append(finding(
                "R11", f"a credential falls back to a literal: {rel}:{ln}",
                1, "observed", path=rel, line=ln,
                quote=" ".join(m.group(0).split())[:160],
                env_var=var, env_var_occurrences=elsewhere,
                remedy="hand to code-review; if the repo owns a loader, call it"
                       + (f" — `{var}` appears {elsewhere}× in the tree" if var else "")))


R_PROBES = [
    ("R1", r1_docs_only_commits), ("R2", r2_claimed_file_never_written),
    ("R4", r4_duplicate_captures),
    ("R6", r6_isolation), ("R9", r9_inert_controls),
    ("R10", r10_duplicate_module), ("R11", r11_weak_secret),
]


def path_matches(candidate: str, scope: set[str]) -> bool:
    candidate = candidate.lstrip("./")
    return any(candidate == p or candidate.startswith(p.rstrip("/") + "/")
               or p.startswith(candidate.rstrip("/") + "/") for p in scope)


def scope_commits(repo: str, candidates: list[dict], paths: set[str]) -> list[dict]:
    if not paths:
        return []
    return [c for c in candidates if any(path_matches(p, paths) for p in files_in(repo, c["sha"]))]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("signals")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if git(a.repo, "rev-parse", "--is-inside-work-tree")[0] != 0:
        print(f"crossref: {a.repo} is not a git repository", file=sys.stderr)
        return 1
    with open(a.signals) as fh:
        sig = json.load(fh)

    candidate_shas = commits(a.repo, a.since, a.until)
    attributable_paths = set(sig.get("attribution", {}).get("paths", []))
    modified_paths = set(sig.get("attribution", {}).get("modified_paths", []))
    shas = scope_commits(a.repo, candidate_shas, modified_paths)
    out: list[dict] = []
    notes: list[str] = []
    could_not_run: list[dict] = []
    if not attributable_paths:
        could_not_run.append({
            "probe": "ATTRIBUTION",
            "error": "signals.json names no attributable paths; repository probes refuse an all-tree scan",
        })
    for pid, fn in R_PROBES:
        try:
            fn(a.repo, sig, shas, out, notes)
        except Exception as exc:
            could_not_run.append({"probe": pid, "error": f"{type(exc).__name__}: {exc}"})

    code, dirty = git(a.repo, "status", "--porcelain")
    dirty_paths = [l[3:].strip() for l in dirty.splitlines() if l.strip()] if code == 0 else []
    scoped_dirty = [p for p in dirty_paths if path_matches(p, modified_paths)]
    d = {
        "schema": SCHEMA,
        "repo": os.path.abspath(a.repo),
        "window": {"since": a.since, "until": a.until, "candidate_commits": len(candidate_shas),
                   "attributable_commits": len(shas)},
        "attribution": {"paths": sorted(attributable_paths),
                        "modified_paths": sorted(modified_paths),
                        "candidate_commits_excluded": len(candidate_shas) - len(shas)},
        "uncommitted_paths": len(scoped_dirty) if code == 0 else None,
        "findings": sorted(out, key=lambda f: (f["band"],
                                               {"observed": 0, "strong-inference": 1,
                                                "weak-inference": 2}.get(f["confidence"], 3))),
        "notes": notes,
        "probes_that_could_not_run": could_not_run,
    }

    lines = [
        f"repo         {d['repo']}",
        f"window       {a.since or '(all)'} → {a.until or 'now'} · {len(candidate_shas)} candidate commit(s)"
        f" · {len(shas)} attributable · {d['uncommitted_paths']} attributable uncommitted path(s)",
        f"scope        {len(attributable_paths)} accessed path(s) · {len(modified_paths)} modified path(s); "
        f"{len(candidate_shas) - len(shas)} unrelated commit(s) excluded",
        "",
        f"FINDINGS     {len(d['findings'])}",
    ]
    for f in d["findings"]:
        lines.append(f"  [band {f['band']}] {f['probe']:<4} {f['title']}")
        if f.get("remedy"):
            lines.append(f"            → {f['remedy']}")
    if notes:
        lines += ["", "NOT CHECKED"] + [f"  {n}" for n in notes]
    if could_not_run:
        lines += ["", "PROBES THAT COULD NOT RUN (not the same as probes that passed)"]
        lines += [f"  {p['probe']}: {p['error']}" for p in could_not_run]
    table = "\n".join(lines)

    if a.json:
        print(json.dumps(d, indent=1))
        print(table, file=sys.stderr)
    else:
        print(table)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(d, fh, indent=1)
    return 4 if could_not_run else 0


if __name__ == "__main__":
    sys.exit(main())
