# Eval results — iteration 1

Run 2026-08-18 during the `mac-design-studio` → `mac-craft` rebuild. Two instruments:
the gate's own adversarial suite, and a blind three-family judge panel. The comparative
MC-1 A/B build was launched and had not produced artifacts when this file was written —
recorded as **not concluded** rather than omitted, because a scorecard that quietly drops
its weakest evidence is the thing this pipeline exists to prevent.

## 1 · `scripts/gate_tests.sh` — 19/19

Nineteen mocks, each built to defeat exactly one check, each asserted against the exit code
it must produce. All nineteen bite. Full listing in the script; the load-bearing rows:

| Case | Expect | Got |
|---|---|---|
| control: clean mock passes | 0 | 0 |
| contrast: 1.00:1 same-colour text | 1 | 1 |
| contrast: no text at all is unmeasured, not a pass | 2 | 2 |
| contrast: unresolvable pair is not counted as passing | 0 | 0 |
| contrast: system-hue failure gets its own message | 1 | 1 |
| contrast: disabled text is exempt, not a failure | 0 | 0 |
| metrics: declared value not built in CSS | 1 | 1 |
| metrics: kit tag disagrees with published value | 1 | 1 |
| metrics: untagged row is a defect | 1 | 1 |
| metrics: direction tag on locked chrome metric | 1 | 1 |
| metrics: empty block is unmeasured, never a pass | 2 | 2 |
| keyboard: focus-visible inside a comment does not count | 1 | 1 |
| keyboard: clickable div with no role or tabindex | 1 | 1 |

**The suite earned its cost on the day it was written by finding two defects in the gate
itself** — see `references/evidence.md`. It first reported *fourteen* broken fixtures when
the fixtures were correct: `exit 2` was masking `exit 1`, and the cascade walk was skipping
colour inheritance. The instrument was accusing the material. Fixing inheritance took the
passing fixture from **76 measured contrast pairs to 116**, a 53% undercount that nothing in
the output had disclosed.

## 2 · Blind judge panel — 3-0, one recorded failure

Two renders, blinded A/B under seed 7, mapping withheld from every judge. Judges saw
**renders only**, never source, because the candidate's mock carries a
`<!-- mac-craft:metrics -->` comment that would have named its own provenance.

Subject: `assets/fixtures/mock.html` (reproduces the predecessor's measured failure —
3.65:1 buttons, a `+` glyph at 1.00:1, 48px titlebar, no focus ring, lorem ipsum) against
`assets/fixtures/ledgerline-accounts.html` (the skill's worked example, gate-clean).

| Family | Harness | Verdict |
|---|---|---|
| Anthropic | `claude --model claude-opus-5 --effort high` | **candidate** |
| Google | `agy --model gemini-3.7-flash-high` | **candidate** |
| xAI | `grok -m grok-4.6 --effort xhigh` | **candidate** |
| OpenAI | `codex -m gpt-5.6-sol` | **FAILED — usage-limited until 2026-08-20.** Probed once, exit 1, no `-o` file written, which is the real failure signal for that CLI. Not retried. Counted as failed and excluded from the tally, so this is a **three**-judge result and is never presented as four. |

**Unanimous, 3-0.** And the finding that matters more than the tally: **all three
independently named the low-contrast/invisible-text defect as the worst thing in either
take**, unprompted as to what to look for. Anthropic: *"the selected sidebar item is
unreadable — its text disappears into the pure-cyan fill."* Google: *"near-zero contrast …
renders essential interactive labels unreadable."* xAI: *"neon cyan on cyan, the least
readable text in either take."*

That is the same defect `mock_check.py` reports as `identical=1` at 1.00:1, and the same one
the predecessor's own recorded run reported as *"100% pass rate on contrast (≥4.5:1)"*. Three
independent model families see it in a render; a prose audit did not see it in its own output.
**Gate and panel agree here — which is the case worth stating, because the ordering
gate < panel < human only earns trust when the layers are shown agreeing as well as
diverging.**

### What the panel found against the new work

xAI dissented on one sub-axis while still voting candidate:

> IDENTITY: B commits harder to one loud cyan kit, while A is a **competent but anonymous**
> stock-Mac ledger.

"Competent but anonymous" is the corpus's own named failure mode, quoted back at the
skill's own worked example by an out-of-family judge. It is correct: the fixture was built
to be gate-clean and native, not to be memorable, and it declares no signature element. The
honest reading is that **the gate can enforce correctness and cannot enforce distinctiveness**
— which is why the signature check and the essence test stay human-read rows in step 6 rather
than being folded into the script. Recorded rather than argued away.

## 3 · Harness defects found and fixed during the run

Both are the same class as the gate defects — the instrument misreporting the material —
and both are recorded because each would have produced a wrong number quietly.

1. **The tally scored a real verdict as `UNPARSED`.** xAI prefixed narration on the same
   line as its answer (`"…the prompt next.WINNER: A"`), and a line-anchored grep missed it.
   Dropping a cast vote for a formatting reason is the voting equivalent of `examined=0`.
   Fixed by unanchoring the match.
2. **Google failed for a documented environment trap, not a model reason.** `agy --print`
   auto-denies command-permission tools: empty output, exit 0, and the reason only on
   stderr. Re-run once with `--dangerously-skip-permissions` — a strategy change, not a
   blind retry — and it produced a full verdict. Had the first result been taken at face
   value, the panel would have reported two judges where three were available.

## 4 · Not concluded

**MC-1, the comparative A/B build.** Two headless Opus runs on one brief (Ledgerline, two
surfaces, light and dark) — one following `mac-design-studio`, one following `mac-craft`,
same environment note, the predecessor with no gate available. Both were still in their
reference-reading phase at 27 minutes with no artifacts on disk. One incidental observation
worth keeping: at that point the predecessor's run had accumulated **2.2 MB of transcript
across 42 shell calls** against the candidate's 880 KB across 28, which is what an
unrouted 8,325-line corpus costs a runner before it writes anything.

Grade it with `/tmp/improve-mac-craft/grade_eval.py <dir> <label>`, which scores A1–A10
mechanically off `mock_check.py --json` counters rather than off a reading.
