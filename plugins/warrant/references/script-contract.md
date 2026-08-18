# Script contract

Every script in `scripts/` obeys this. It exists because the plugin's gates are
scripts rather than prompts, and a gate whose behaviour varies between scripts is
a gate nobody can reason about.

## Language and dependencies

Stdlib Python 3 only. No third-party imports, no network access, no model calls.
A verification tool with a dependency tree is a verification tool that stops
running, and every existing gate in the target repository holds the same line.

Two consequences worth stating because they shaped the file formats:

- **The warrant is TOML, not YAML.** `tomllib` is stdlib and read-only from
  3.11; there is no stdlib YAML parser. Shipping a hand-rolled YAML subset reader
  for the one file that gates everything else is the wrong risk to take. The
  build plan says `warrant.yaml`; the implementation is `warrant.toml`, and the
  same applies to `lanes.toml`.
- **Writing TOML is hand-rolled and deliberately narrow.** `charter_init.py`
  emits a fixed schema it fully controls. No script serialises arbitrary data to
  TOML.

## Invocation

Every script accepts:

| Flag | Behaviour |
|---|---|
| `--help` | usage, exit 0 |
| `--root PATH` | the repository under verification; defaults to `$PWD` |
| `--json` | emit one JSON object on stdout, human summary on stderr |
| `--now ISO8601` | override the clock, so tests are deterministic |
| `--selftest` | run the script's own fixtures, exit 0 only if every rule fired |

`--selftest` is not optional and it is not a smoke test. It asserts that each
rule the script implements can both pass and fail, because a rule only ever
observed passing is a rule nobody has written.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | the check ran and the thing being checked is sound |
| 1 | the script could not run: bad usage, unreadable input, internal error |
| 2 | the check ran and the thing being checked failed |
| 3 | a precondition is absent: no warrant, no ledger, no corpus |
| 4 | the check ran and a revocation fired (`ratchet.py` only) |

`_cli.py` overrides argparse's own error handler to exit 1 rather than its default 2. Without that
override a mistyped flag in a CI invocation is indistinguishable from a real gate failure, which is
the single confusion that makes a gate untrustworthy.

Exit 1 and exit 2 are different answers and callers depend on the difference: a
missing file is not a failed gate, and a harness that treats them alike either
blocks on nothing or passes on nothing. Read the exit code rather than the
output; piping a gate through `grep` reports grep's status, and that has already
turned a failure into a pass once in this marketplace.

## Output rules

**In `--json` mode, stdout carries the JSON object and nothing else.** Every
human-readable line goes to stderr. A caller parsing stdout must not have to
strip a banner.

**No bare rates.** Any percentage a script prints carries its numerator and its
denominator in the same breath. This is the `C19` rule made mechanical:
published proficiency-test failure rates differ by more than twentyfold
depending on what is counted, 1.4% of 670,489 challenges across 665
laboratories against 32.4% of lab-parameter results across three, and both are
correct. `escape_report.py` goes further and refuses to emit a rate at all,
because feedback gives a numerator with no denominator.

**A writer that has already had an external effect does not throw.** If a row is
appended, a snapshot taken or a file committed, a later failure is logged and
reported rather than raised — the effect already happened, and raising invites a
retry that does it twice.

## State layout

All under `--root`, all created on demand:

```
.warrant/
  warrant.toml            the signed warrant; the only human-signed artifact
  lanes.toml              one block per lane: role, model id, version
  suite-health.json       assay output, ratcheted
  oracle-coverage.json    oracle plane coverage per surface
  escapes.jsonl           append-only, one row per reported escape
  regression/<id>/        one directory per escape: inputs, expected verdict
  ledger.jsonl            append-only, hash-chained decision record
  reports/<date>-<kind>.json
```

`.jsonl` files are append-only. No script rewrites one; `ledger.py` appends and
`ledger_verify.py` reads.

### The producing and consuming planes key their state differently

`oracle` measures a surface, `assay` measures a test target, and authority is held
per defect class. Something has to map one onto the other, and leaving it implicit
is what produced the one integration defect in this build: two consumers read
`{"classes": {...}}` while the producer wrote `{"surfaces": [...]}`, so every class
read as having no evidence.

`rollup_classes.py` is that step. It reads the class-to-surface globs the warrant
declares and writes a `classes` block into both files:

```
oracle-coverage.json  {"surfaces": [...],            # what the producer measured
                       "classes": {"<class>": {"total","covered","coverage",
                                               "lineage_gaps","surfaces_matched",
                                               "threshold","green"}}}
suite-health.json     {"mutation": {"score","high_water",...},
                       "green": bool,                # what charter_validate reads
                       "classes": {"<class>": {"mutation_score","high_water",
                                               "measured","green"}}}
```

A class no surface matched is `green: false` rather than absent, because no
evidence is not the same answer as a pass. Run `rollup_classes.py` after `oracle`
and `assay` and before `ratchet`.

## Schemas

`schemas/*.schema.json` are the contract for anything a model produces:
`verdict.schema.json`, `escape.schema.json`. They are consumed through Structured
Outputs rather than through a prefill, which current models reject. Scripts
validate against them with a small stdlib checker in `scripts/_schema.py` rather
than a dependency.

## Shared modules

Prefixed with an underscore so they read as internal:

- `_state.py` — resolve `--root`, read the warrant, locate state files, exit 3
  when a precondition is absent.
- `_schema.py` — the stdlib subset JSON Schema validator: types, required,
  enum, minimum/maximum, items, additionalProperties.
- `_cli.py` — the common argument parser and the `--selftest` harness, so a
  new script inherits every flag above rather than re-declaring it.

A script that needs one of these imports it rather than copying it. Three
copies of a JSON reader is three places for the exit codes to drift.
