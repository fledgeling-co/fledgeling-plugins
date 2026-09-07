# Environment doctor

Load this file when `visualization:visualization` receives a request for diagnostics,
health checks, or import/export troubleshooting. For example, invoke the skill
with arguments `doctor --strict --json`. These are instructions interpreted by
the skill; no separate doctor command or diagnostic executable is bundled.

The result is a read-only readiness report for the installed Visualization skill.
Resolve `<skill-dir>` as the parent of this reference's `references/` directory
(the directory containing `SKILL.md`), not from the user's project working directory. Resolve
`<plugin-root>` two levels above it only when checking plugin metadata.

## Inputs

- `--strict`: warnings make the overall result `FAIL`; keep individual check
  statuses and counts unchanged.
- `--json`: append a JSON report to the human summary.
- A source HTML, Mermaid or draw.io path: include the relevant source check.

These arguments do not authorize dependency installation or file repair.

## Readiness checks

Run the relevant checks and report each as `pass`, `warn`, or `fail`:

1. **Python runtime.** Resolve `python3`, then `python`, and record the actual
   interpreter path and version. The bundled Python tools require Python 3.10+.
   A missing or older runtime fails Python-based import and verification readiness.
2. **Installed files.** Verify `<skill-dir>/SKILL.md`, the requested workflow's
   reference, and the bundled scripts it uses. Core checks are
   `scripts/self_check.py`, `scripts/verify-geometry.py`, and
   `scripts/validate_palette.py`; imports use `scripts/drawio_extract.py` and
   `scripts/mermaid_extract.py`; animated output uses `scripts/verify-motion.py`
   and `assets/template-motion.html`. For a particular chart, resolve its checker
   from SKILL.md's verification table and require that exact file. Missing required
   files fail that workflow. Do not require predecessor repository scripts such
   as a documentation-sync checker or a plugin-packaging checker.
3. **Script readiness.** Check `--help` for the two import extractors and
   `self_check.py` with the resolved Python interpreter. Capture stderr and exit
   status; file presence alone is not an executable pass. With a source HTML path,
   run `self_check.py` and applicable geometry/type checkers against that file;
   with no source, report artifact verification as not run. Do not fabricate a
   successful import or visual assessment from the help checks.
4. **PNG export environment.** Follow `export.md`. For its Python recipe, check
   `import playwright.sync_api` in the same interpreter, then attempt a headless
   Chromium launch and close on a blank page. A package import or
   `playwright install --help` does not prove a browser is installed or launchable.
   Missing dependencies or failed launch are warnings for PNG export; SVG export
   remains available. If another supported browser tool can capture the required
   local SVG element, record that tested route instead. Do not claim launch or
   capture success without performing it.
5. **Paths and profiles.** Quote absolute paths in commands. If a project marker
   exists, validate it and its selected profile per `profiles.md`, without creating
   or rewriting either. Missing selected profiles and invalid markers are warnings
   with the exact recovery action. A missing installed `SKILL.md` is an installation
   failure; changing into a maintainer checkout is not the remedy.

## Optional plugin packaging check

When `<plugin-root>/.claude-plugin/plugin.json` exists, parse it and confirm its
name is `visualization`, that `skills/visualization/SKILL.md` is the resolved entry
point, and that the entry point links to `references/doctor.md`, `export.md`,
`onboarding.md`, `profiles.md`, `import-drawio.md`, and `import-mermaid.md`.
Report malformed metadata or broken local routing as failures. In a standalone
skill installation, report plugin metadata as not applicable; it is not a failure.

This package exposes the single `visualization:visualization` skill. Do not
require `commands/`, `prompts/`, predecessor CI files, or unbundled maintainer
scripts. If asked for broader repository checks, discover this checkout's actual
validation commands before running them and identify those results separately.

## Output contract

Print `Doctor summary: <PASS|WARN|FAIL> (<pass_count> pass, <warn_count> warn,
<fail_count> fail)`, followed by one evidence-bearing line per check. Overall
status is `FAIL` when any check fails, otherwise `WARN` when any warns, otherwise
`PASS`; strict mode promotes overall `WARN` to `FAIL`.

Use a short `Next actions` list only for warnings or failures. For the Python
export route, a missing package/browser remediation is
`"<python-path>" -m pip install playwright` followed by
`"<python-path>" -m playwright install chromium`; these are suggestions,
not commands to run during diagnostics. Preserve the user's existing environment
and dependency-management convention.

With `--json`, append an object with `status`, `counts`, `checks` (each containing
`name`, `status`, `message`, and optional `fix`), and `timestamp`. Mark skipped
checks explicitly as `not run` or `not applicable` outside the pass/warn/fail
counts. Record unexpected stderr and continue independent checks. End with the
specific action needed to resolve each remaining failure; re-enter through
`visualization:visualization` with arguments `doctor --strict` when ready.
