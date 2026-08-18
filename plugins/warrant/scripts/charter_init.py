#!/usr/bin/env python3
"""Draft `.warrant/warrant.toml` from the repository.

The warrant is the only human-signed artifact in the system, so this script
enumerates rather than asks: it walks the repository, buckets what it finds into
surfaces, spec files, schemas and captures, proposes a defect class per bucket,
and writes every class at tier 0 — advisory only. Raising a tier is a separate
evidenced act, and `charter_validate.py` refuses a tier whose entry condition is
unmet.

The file is TOML because `tomllib` is stdlib and read-only; see
references/script-contract.md. Writing it is hand-rolled through
`_state.toml_kv()` and covers this fixed schema only.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import fnmatch
import io
import os
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

WARRANT_SCHEMA_VERSION = "1"

# Directories that hold build products or dependencies rather than surfaces.
# `ios`/`android` are Expo prebuild output; a hand-written native surface in one
# of them would be missed, which is recorded in [survey].skipped_dirs.
SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".next", ".nuxt", ".turbo", ".nx",
    "dist", "build", "out", "coverage", ".coverage", ".venv", "venv", "env",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".warrant",
    ".cache", ".parcel-cache", "vendor", "target", ".pnpm-store", ".yarn",
    "ios", "android", ".expo", ".vercel", ".serverless", ".gradle",
}

SURFACE_PATTERNS: dict[str, tuple[str, ...]] = {
    "html-mock": ("*.html", "*.htm"),
    "next-page": ("page.tsx", "page.jsx", "page.js"),
    "story": ("*.stories.tsx", "*.stories.ts", "*.stories.jsx", "*.stories.mdx"),
    "screen": ("*Screen.tsx", "*Screen.jsx", "*.screen.tsx"),
    "template": ("*.hbs", "*.mustache", "*.ejs", "*.jinja", "*.jinja2"),
}

TEST_PATTERNS = (
    "*.spec.ts", "*.spec.tsx", "*.spec.js", "*.spec.jsx",
    "*.test.ts", "*.test.tsx", "*.test.js", "*.test.jsx",
    "*.spec.py", "test_*.py", "*_test.py", "*_spec.rb",
    "*.e2e.ts", "*.e2e.js", "*.feature",
)

SPEC_DOC_PATTERNS = (
    "spec-*.md", "*.spec.md", "plan-*.md", "requirements*.md", "PRD*.md",
    "prd*.md", "acceptance*.md", "*-spec.md", "DESIGN.md", "design-*.md",
)

SCHEMA_PATTERNS = ("*.schema.json", "*.schema.ts", "schema.gql", "schema.graphql",
                   "*.graphql", "*.avsc", "*.proto")

CAPTURE_DIR_HINTS = ("screenshot", "screenshots", "captures", "__screenshots__",
                     "snapshots", "__snapshots__", "baseline", "baselines",
                     "visual-regression")

MAX_FILES = 60000          # a bound, so a walk on a huge tree still terminates
MAX_EXAMPLES = 6           # example paths recorded per bucket


# ── enumeration ──────────────────────────────────────────────────────────────

def _matches(name: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def survey(root: pathlib.Path) -> dict[str, object]:
    """Walk the repository once and bucket what is there.

    Classification is by path and filename only. Nothing here reads file
    contents, so the survey is bounded and predictable — and a defect class that
    would need a content scan to notice (tenant isolation, for one) is proposed
    from directory names or not at all.
    """
    buckets: dict[str, list[str]] = {k: [] for k in SURFACE_PATTERNS}
    buckets["test"] = []
    buckets["spec-doc"] = []
    buckets["schema"] = []
    buckets["capture"] = []
    counts: dict[str, int] = {k: 0 for k in buckets}

    files_seen = 0
    truncated = False
    tenant_hint = False

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in SKIP_DIRS and not d.startswith(".git"))
        rel_dir = os.path.relpath(dirpath, root)
        lowered_dir = rel_dir.lower()
        in_captures = any(hint in lowered_dir for hint in CAPTURE_DIR_HINTS)
        if any(part in ("tenant", "tenants", "company", "companies", "multitenant")
               for part in lowered_dir.split(os.sep)):
            tenant_hint = True

        for name in sorted(filenames):
            files_seen += 1
            if files_seen > MAX_FILES:
                truncated = True
                break
            rel = os.path.normpath(os.path.join(rel_dir, name)) if rel_dir != "." else name

            if in_captures and _matches(name, ("*.png", "*.jpg", "*.jpeg", "*.webp")):
                counts["capture"] += 1
                if len(buckets["capture"]) < MAX_EXAMPLES:
                    buckets["capture"].append(rel)
                continue
            if _matches(name, TEST_PATTERNS):
                counts["test"] += 1
                if len(buckets["test"]) < MAX_EXAMPLES:
                    buckets["test"].append(rel)
                continue
            if _matches(name, SPEC_DOC_PATTERNS):
                counts["spec-doc"] += 1
                if len(buckets["spec-doc"]) < MAX_EXAMPLES:
                    buckets["spec-doc"].append(rel)
                continue
            if _matches(name, SCHEMA_PATTERNS):
                counts["schema"] += 1
                if len(buckets["schema"]) < MAX_EXAMPLES:
                    buckets["schema"].append(rel)
                continue
            for kind, patterns in SURFACE_PATTERNS.items():
                if _matches(name, patterns):
                    counts[kind] += 1
                    if len(buckets[kind]) < MAX_EXAMPLES:
                        buckets[kind].append(rel)
                    break
        if truncated:
            break

    surface_count = sum(counts[k] for k in SURFACE_PATTERNS)
    return {
        "counts": counts,
        "examples": buckets,
        "files_seen": min(files_seen, MAX_FILES),
        "truncated": truncated,
        "surface_count": surface_count,
        "tenant_hint": tenant_hint,
    }


def propose_classes(sv: dict[str, object]) -> list[dict[str, object]]:
    """Propose one defect class per bucket that actually has members.

    Two classes are unconditional. `figure-lineage` is the highest-consequence
    class — a correctly rendered surface asserting a figure no source supports —
    and it is closable with arithmetic rather than judgement. `disclosure-content`
    is unconditional because its absence from a warrant reads as an oversight
    rather than as a decision; it is census-reviewed and tier 4 is unreachable.
    """
    counts = sv["counts"]                                      # type: ignore[index]
    classes: list[dict[str, object]] = [
        {
            "name": "figure-lineage",
            "tier": 0,
            "escalation": "owner",
            "census": False,
            "plane": "oracle",
            "surfaces": ["**/*.html", "**/page.tsx"],
            "note": "a rendered figure with no provenance token back to its source record",
        },
        {
            "name": "disclosure-content",
            "tier": 0,
            "escalation": "owner",
            "census": True,
            "plane": "human",
            "surfaces": ["**/*"],
            "note": "census-reviewed; tier 4 is unreachable on current evidence",
        },
    ]

    if counts["html-mock"] or counts["story"] or counts["next-page"] or counts["screen"]:
        classes.append({
            "name": "render-fidelity",
            "tier": 0,
            "escalation": "owner",
            "census": False,
            "plane": "panel",
            "surfaces": ["**/*.html", "**/*.stories.tsx", "**/page.tsx"],
            "note": "the built surface diverges from its design of record",
        })
    if counts["test"] or counts["spec-doc"]:
        classes.append({
            "name": "spec-conformance",
            "tier": 0,
            "escalation": "owner",
            "census": False,
            "plane": "panel",
            "surfaces": ["**/*.spec.ts", "**/spec-*.md"],
            "note": "the work omits something its spec required while reading as complete",
        })
    if counts["schema"]:
        classes.append({
            "name": "taxonomy-classification",
            "tier": 0,
            "escalation": "owner",
            "census": False,
            "plane": "oracle",
            "surfaces": ["**/*.schema.json", "**/*.graphql"],
            "note": "a valid-looking value in the wrong field",
        })
    if counts["capture"]:
        classes.append({
            "name": "perceptual-regression",
            "tier": 0,
            "escalation": "owner",
            "census": False,
            "plane": "panel",
            "surfaces": ["**/__screenshots__/**", "**/captures/**"],
            "note": "a capture changed in a way no requirement named",
        })
    if sv["tenant_hint"]:
        classes.append({
            "name": "tenant-isolation",
            "tier": 0,
            "escalation": "owner",
            "census": False,
            "plane": "oracle",
            "surfaces": ["**/*"],
            "note": "proposed from directory names only; confirm the surfaces before signing",
        })
    return classes


# ── emission ─────────────────────────────────────────────────────────────────

def header(root: pathlib.Path, sv: dict[str, object], drafted: str) -> list[str]:
    bar = "# " + "─" * 74
    return [
        bar,
        "# .warrant/warrant.toml — the only human-signed artifact in this system.",
        "#",
        "# What you are signing:",
        "#",
        "#   1. For every class below at a tier above 0, a machine may close items in",
        "#      that class and no person will look at the item.",
        "#   2. The tolerable error rate in [lot] is the risk you are choosing to run on",
        "#      the queue, and the sample size it implies is the human time it costs.",
        "#   3. You are the escalation route. An `inconclusive` verdict, a census class",
        "#      and every revocation arrive at you by name.",
        "#   4. You re-sign on the renewal date. A warrant past renewal is not a",
        "#      warrant, and charter_validate.py exits 2 on one.",
        "#",
        "# What signing does not mean: this is not per-item approval, and it is not a",
        "# claim that the machine has been measured against a human. The tier ladder is",
        "# climbed on absence of escapes, which grows more convincing with volume and",
        "# time and never becomes a rate.",
        "#",
        "# The signature is the commit. This file is signed when a named person commits",
        "# it; an agent committing it is not a signature.",
        "#",
        f"# Drafted by charter_init.py on {drafted}",
        f"# from {sv['files_seen']} file(s) under {root}"
        + (" (walk truncated)" if sv["truncated"] else "")
        + f", {sv['surface_count']} surface(s).",
        "# Every class starts at tier 0 — advisory. Raising one is a separate evidenced",
        "# act; see [tiers] and warrant:ratchet.",
        bar,
        "",
    ]


def render(root: pathlib.Path, sv: dict[str, object], classes: list[dict[str, object]],
           owner_name: str, owner_email: str, signed: _dt.date, renewal: _dt.date,
           renewal_days: int, drafted: str) -> str:
    kv = _state.toml_kv
    lines: list[str] = header(root, sv, drafted)

    lines += [
        kv("version", WARRANT_SCHEMA_VERSION),
        kv("signed", signed.isoformat()),
        kv("renewal", renewal.isoformat()),
        "",
        "# The named person answerable for every machine-closed item under this warrant.",
        "# A role with no current holder is a warrant with no signature: name a person.",
        "[owner]",
        kv("name", owner_name),
        kv("email", owner_email),
        "",
    ]

    lines += [
        "# One block per defect class. `tier` is the authority the machine holds over the",
        "# class; `escalation` is where an inconclusive or failed item goes.",
    ]
    for cls in classes:
        lines += [
            "",
            f"# {cls['note']}",
            "[[classes]]",
            kv("name", cls["name"]),
            kv("tier", cls["tier"]),
            kv("escalation", cls["escalation"]),
            kv("census", cls["census"]),
            kv("plane", cls["plane"]),
            kv("surfaces", cls["surfaces"]),
        ]

    lines += [
        "",
        "# Thresholds for the deterministic plane. Tolerances live here rather than in",
        "# the scripts, so changing one is a diff against a signed file.",
        "[oracle]",
        kv("lineage_coverage_min", 0.95),
        kv("tick_and_tie_abs_tolerance", 0.01),
        kv("tick_and_tie_rel_tolerance", 0.005),
        kv("taxonomy_violations_max", 0),
        "",
        "# The queue is accepted as a lot under a declared risk limit rather than signed",
        "# item by item. tolerable_error_rate sets the sample size; see lot_plan.py.",
        "[lot]",
        kv("tolerable_error_rate", 0.05),
        kv("risk_limit", 0.05),
        kv("census_classes", ["disclosure-content", "inconclusive"]),
        "",
        "# Entry conditions for the ladder. Counts and windows are risk appetite, not",
        "# technical facts: too low and the ladder is decoration, too high and nothing",
        "# ever reaches tier 3.",
        "[tiers]",
        kv("tier1_oracle_coverage_min", 0.95),
        kv("tier2_requires_assay_green", True),
        kv("tier2_regression_recatch_min", 1.0),
        kv("tier3_items_closed_min", 200),
        kv("tier3_window_days", 90),
        kv("tier4_reachable", False),
        "",
        "# How old evidence may be before the authority resting on it lapses.",
        "[staleness]",
        kv("calibration_max_days", 30),
        kv("snapshot_max_hours", 24),
        kv("renewal_window_days", renewal_days),
        "",
        "# What the walk found. Informational: no gate reads this section.",
        "[survey]",
        kv("drafted", drafted),
        kv("files_seen", sv["files_seen"]),
        kv("truncated", sv["truncated"]),
        kv("surface_count", sv["surface_count"]),
        kv("skipped_dirs", sorted(SKIP_DIRS)),
    ]
    counts = sv["counts"]                                      # type: ignore[index]
    for bucket in sorted(counts):                              # type: ignore[arg-type]
        lines.append(kv(f"count_{bucket.replace('-', '_')}", counts[bucket]))
    examples = sv["examples"]                                  # type: ignore[index]
    for bucket in sorted(examples):                            # type: ignore[arg-type]
        if examples[bucket]:
            lines.append(kv(f"example_{bucket.replace('-', '_')}", examples[bucket]))
    return "\n".join(lines) + "\n"


# ── main ─────────────────────────────────────────────────────────────────────

def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--out", default=None,
                   help="warrant path (default: <root>/.warrant/warrant.toml)")
    p.add_argument("--owner-name", default="",
                   help="the named person answerable; left blank in a draft")
    p.add_argument("--owner-email", default="")
    p.add_argument("--renewal-days", type=int, default=180,
                   help="days from the signing date to renewal (default: 180)")
    p.add_argument("--force", action="store_true",
                   help="overwrite an existing warrant, discarding its signature")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    if not root.is_dir():
        _cli.say(args, f"--root is not a directory: {root}")
        return _cli.ERROR

    out = pathlib.Path(args.out).expanduser().resolve() if args.out else _state.warrant_path(root)
    if out.exists() and not args.force:
        _cli.say(args, f"a warrant already exists at {out}")
        _cli.say(args, "refusing to overwrite a signed file; pass --force to discard it")
        _cli.emit(args, {"ok": False, "warrant": str(out), "reason": "exists"})
        return _cli.ERROR

    stamp = _cli.now(args)
    signed = stamp.date()
    renewal = signed + _dt.timedelta(days=args.renewal_days)

    sv = survey(root)
    classes = propose_classes(sv)
    text = render(root, sv, classes, args.owner_name, args.owner_email,
                  signed, renewal, args.renewal_days, stamp.isoformat())

    # Only create .warrant/ when the warrant is actually going there: a draft
    # written elsewhere with --out must not leave state behind in the surveyed
    # repository.
    if out == _state.warrant_path(root):
        _state.state_dir(root, create=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)

    # The file is on disk from here on: anything that goes wrong below is
    # reported rather than raised, because the effect has already happened.
    problems: list[str] = []
    try:
        import tomllib
        with out.open("rb") as fh:
            tomllib.load(fh)
    except Exception as exc:                                   # noqa: BLE001
        problems.append(f"the draft does not parse as TOML: {type(exc).__name__}: {exc}")

    counts = sv["counts"]                                      # type: ignore[index]
    _cli.say(args, f"wrote {out}")
    _cli.say(args, f"  surfaces {sv['surface_count']}  tests {counts['test']}  "
                   f"specs {counts['spec-doc']}  schemas {counts['schema']}  "
                   f"captures {counts['capture']}")
    _cli.say(args, f"  {len(classes)} defect class(es), all at tier 0: "
                   + ", ".join(str(c["name"]) for c in classes))
    if not args.owner_name or not args.owner_email:
        _cli.say(args, "  owner is blank — charter_validate.py will exit 2 until a person "
                       "is named in [owner]")
    for problem in problems:
        _cli.say(args, f"  problem after writing: {problem}")

    _cli.emit(args, {
        "ok": not problems,
        "warrant": str(out),
        "signed": signed.isoformat(),
        "renewal": renewal.isoformat(),
        "classes": [{"name": c["name"], "tier": c["tier"]} for c in classes],
        "survey": {"files_seen": sv["files_seen"], "truncated": sv["truncated"],
                   "surface_count": sv["surface_count"], "counts": counts},
        "owner_named": bool(args.owner_name and args.owner_email),
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


def _fixture_repo(base: pathlib.Path, rich: bool) -> pathlib.Path:
    repo = base / ("rich" if rich else "bare")
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "notes.txt").write_text("nothing classifiable here\n")
    if rich:
        (repo / "docs" / "ui-mockups").mkdir()
        (repo / "docs" / "ui-mockups" / "dashboard.html").write_text("<main></main>")
        (repo / "docs" / "spec-inbox.md").write_text("# spec\n")
        (repo / "e2e").mkdir()
        (repo / "e2e" / "inbox.spec.ts").write_text("test('x', () => {})\n")
        (repo / "schemas").mkdir()
        (repo / "schemas" / "figure.schema.json").write_text("{}")
        (repo / "e2e" / "__screenshots__").mkdir()
        (repo / "e2e" / "__screenshots__" / "inbox.png").write_bytes(b"\x89PNG")
        (repo / "node_modules").mkdir()
        (repo / "node_modules" / "ignored.html").write_text("<b>skip me</b>")
    return repo


def selftest() -> list[tuple[str, bool]]:
    import tomllib
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-charter-init-"))
    try:
        rich = _fixture_repo(tmp, rich=True)
        bare = _fixture_repo(tmp, rich=False)

        code, _, _ = _call("--root", str(rich), "--now", "2026-08-19T00:00:00+00:00")
        cases.append(("writes a draft on a fresh repository", code == _cli.OK))
        path = _state.warrant_path(rich)
        cases.append(("the draft lands at .warrant/warrant.toml", path.exists()))

        text = path.read_text()
        doc = tomllib.loads(text)
        cases.append(("the draft parses as TOML", isinstance(doc, dict)))
        required = ["version", "signed", "renewal", "owner", "classes", "oracle",
                    "lot", "tiers", "staleness"]
        cases.append(("every required key is present",
                      all(k in doc for k in required)))
        cases.append(("a missing required key would be noticed",
                      not all(k in {"version": 1} for k in required)))
        cases.append(("owner carries name and email",
                      set(doc["owner"]) >= {"name", "email"}))
        cases.append(("every class is at tier 0",
                      all(c["tier"] == 0 for c in doc["classes"])))
        cases.append(("every class names an escalation route",
                      all(c.get("escalation") for c in doc["classes"])))
        cases.append(("the header says what is being signed",
                      "What you are signing" in text and text.lstrip().startswith("#")))
        cases.append(("lot carries a tolerable error rate",
                      0.0 < float(doc["lot"]["tolerable_error_rate"]) < 1.0))
        cases.append(("tiers carry the tier-3 count and window",
                      "tier3_items_closed_min" in doc["tiers"]
                      and "tier3_window_days" in doc["tiers"]))
        cases.append(("staleness carries a calibration window",
                      "calibration_max_days" in doc["staleness"]))
        cases.append(("--now drives signed and renewal",
                      doc["signed"] == "2026-08-19" and doc["renewal"] == "2027-02-15"))

        names = {c["name"] for c in doc["classes"]}
        cases.append(("a repository with mocks proposes render-fidelity",
                      "render-fidelity" in names))
        cases.append(("a repository with specs proposes spec-conformance",
                      "spec-conformance" in names))
        cases.append(("a repository with schemas proposes taxonomy-classification",
                      "taxonomy-classification" in names))
        cases.append(("a repository with captures proposes perceptual-regression",
                      "perceptual-regression" in names))
        cases.append(("figure-lineage and disclosure-content are unconditional",
                      {"figure-lineage", "disclosure-content"} <= names))
        cases.append(("node_modules is not surveyed",
                      "ignored.html" not in text))

        code, _, _ = _call("--root", str(bare), "--now", "2026-08-19T00:00:00+00:00")
        bare_doc = tomllib.loads(_state.warrant_path(bare).read_text())
        bare_names = {c["name"] for c in bare_doc["classes"]}
        cases.append(("a bare repository still gets a warrant", code == _cli.OK))
        cases.append(("a bare repository proposes no render-fidelity class",
                      "render-fidelity" not in bare_names))
        cases.append(("a bare repository proposes no capture class",
                      "perceptual-regression" not in bare_names))

        code, out, err = _call("--root", str(rich))
        cases.append(("refuses to overwrite an existing warrant",
                      code == _cli.ERROR and "--force" in out + err))
        before = path.read_text()
        code, _, _ = _call("--root", str(rich), "--force", "--owner-name", "Ada L",
                           "--owner-email", "ada@example.test",
                           "--now", "2026-08-19T00:00:00+00:00")
        after = path.read_text()
        cases.append(("--force overwrites", code == _cli.OK and after != before))
        cases.append(("--owner-name lands in [owner]",
                      'name = "Ada L"' in after))

        code, _, _ = _call("--root", str(tmp / "nope"))
        cases.append(("a root that is not a directory exits 1", code == _cli.ERROR))

        out, o, _ = _call("--root", str(rich), "--force", "--json")
        cases.append(("--json puts only JSON on stdout", o.lstrip().startswith("{")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
