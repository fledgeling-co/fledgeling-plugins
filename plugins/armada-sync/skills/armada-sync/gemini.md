# armada-sync, calibrated for Gemini

Read this in one pass before *Protocol*; each override names the numbered step it lands on. Almost every
requirement this skill states is already a number — `~20 lines`, `≤8` features, `≤3` opportunities,
`1–2 sentences`, one index row, one changelog line — which is the shape this family holds best. What it
ships no instrument for is reading those numbers back, and the file it edits is ≈94,000 tokens, which
the harness will not hand you in one `Read`.

**[derived]** No route-out block, deliberately. That section's benchmark measures a model *building* —
a page, a multi-file code change, a rendered surface, a currently-passing contract — so `static-page`,
`brownfield-integration` and `visual-design` are omitted because nothing here produces one, and
`regression-sensitive`, the closest call, because the corpus measured it against a verifier and there is
none here. Override 2's snapshot diff is what would have carried it: a check, not a route.

## Epistemic status

| Tier | Used here | Source |
|---|---|---|
| `[docs]` | throughout; most of the file rests on it | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | two sessions + a 106-task corpus | Gemini runs of *other* skills; `geminify/references/evidence.md` |
| `[measured-here]` | measurements of text and files, **not of a run** | 23 Aug 2026 — `scan_skill.py` on this SKILL.md: 36 lines, **2** quota rows, **0** bound rows, 1 relative qualifier, 0 qualitative skill references, **0 emphasis tokens**, **0 modules** at three triggers and still 0 at two. `wc -l -c ~/Dev/ARMADA.md`: 1,057 lines, 375,298 bytes (≈94k tokens), 71 `### ` sections, and `~/Dev` is not a git repository |
| `[derived]` | marked where used | my reasoning from the two above |

**The tier the evidence is about.** Every measured rate here is flash-tier — `gemini-3.7-flash` across
106 benchmark tasks plus two flash sessions — and none is measured on the Pro tier or should be projected
there: on Pro these overrides stand as `[docs]`-grounded discipline while every `[measured-family]`
number is open. **[docs]** Defaults drift within the family too: "The default thinking effort is now
medium, changed from high in Gemini 3 Flash Preview".

**Unmeasured on this skill:** no Gemini run of armada-sync has been observed, so nothing below is
measured on this target, and no comparison exists between a run with this file and one without. The
bound-failure rate (58% of failing UI assertions at `medium`, 86% at `high`) is a rate on rendered-UI
assertions in one product's benchmark — a mechanism here, never a rate for prose entries. The
25,000-token `Read` ceiling behind Override 1 is one harness's limit in one session. And whether this
family writes into a neighbouring section of a 1,057-line file is unmeasured: the one recorded instance
in this manifest (Changelog, 2026-08-20 — an anchor prefix many entries share matched the wrong one) was
a Claude run, so it argues for the readback rather than saying anything about this family.

**[docs]** One self-limitation: a conditional side-file is the shape the checklist warns about — "Avoid
writing a prompt with non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt." Read this once, in order.

## What transferred intact

- **The scope statement is already a closed set** — the current entry, its index row, one changelog
  line, nothing else. **[docs]** Under **Ambiguity**: "Avoid using subjective or relative qualifiers
  that lack a concrete, measurable definition."
- **The caps are already objective**, and **[measured-family]** `evidence.md` §2.1 is why that matters:
  on the optimality bucket — tasks whose brief states a numeric bound — Gemini scored 74.7 against
  opus's 75.0, while the prose-shaped buckets produced hard zeros on 71% and 79% of decided rows.
- **Missing input is handled explicitly** — step 2 refuses to scaffold a one-project manifest, step 1
  asks rather than guesses. **[docs]** "provide instructions for handling missing data rather than
  assuming inserted data will always be present and well-formed", and step 1's fallback is Google's
  remedy for an answer landing outside the offered set: "you can rephrase the instructions as a multiple
  choice question and ask the model to choose an option". Offer the `~/Dev` children as the options.
- **The skill does not shout** — zero emphasis tokens in 36 lines, so nothing needs defusing.

## The quota ledger — two rows, both about paths

**[measured-here]** The scan returned two categorical rows and I bound both; neither was prose, so none
was dropped. They are one requirement stated twice, at SKILL.md:18 (*verify each path you write exists*)
and :36 (*every path is repo-relative and must exist at write time*) — and the skill says in its own
words why it is load-bearing: *a broken reference is worse than no reference*.

**[measured-family]** Why it becomes a table rather than staying a sentence: on the observed run every
enumerated requirement shipped — twelve named features, all present — while every categorical one
shipped once or not at all: *all states* → 1, *all menus* → 0, *all flows* → 0. **[derived]** Here that
is one path spot-checked out of six, and five unverified references published in a shape that reads like
verified ones. Filled below, from
`for p in …; do [ -e "$p" ] && echo "ok $p" || echo "MISS $p"; done | tee /tmp/armada-paths.txt`:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| **each path you write exists** — :18 | 5 **Read more** paths + 1 **Apps** path = **6** | 6 tested with `test -e` | `6/6 paths exist` |
| **every path is repo-relative** — :36 | the same 6 | 6 relative, 0 absolute | `6/6 repo-relative` |
| **[derived]** every parenthetical count — the `specs: <dir> (n)` shape at :33 | 1 count here | 1 from `ls` | `1/1 counts read, 0 recalled` |

**[docs]** That last row is a tool call, not a recollection: code execution "should be enabled whenever
the model needs to perform any kind of arithmetic, counting, or calculation."

## The bound ledger — moved in by hand, because the scan's vocabulary missed it

**[measured-here]** The scan returned **0** bound rows and fired no modules, `bounded-constraint`
included. That is a vocabulary gap rather than a finding: its triggers are phrase-shaped English limits
(`exactly one`, `at most`, `only one`, `maximum of`, `hard cap`) and this skill writes every cap as a
numeral or a glyph — `≤8`, `≤3`, `~20 lines`, `1–2 sentences`, *one line*. So seven move in by hand,
which is what `geminify` asks when a limit is attached to a countable property.

**[measured-family]** They earn it because this is the direction this family fails in. `evidence.md`
§2.2: 58% of failing UI assertions at `medium` and 86% at `high` stated a **bound**, against 8% for
opus — and the most-repeated one, `has exactly one soft elevation shadow`, failed on *every* instance in
its set on a run that passed 37 of its 39 other assertions. The rule was read and agreed with; a default
idiom supplied the value underneath it. **[docs]** Google treats these as a component in their own right
— "Restrictions on what the model must adhere to when generating a response, including what the model
can and can't do" — and the **Recap** component is where they go: a "Concise repeat of the key points of
the prompt, especially the constraints and response format, at the end of the prompt." Snapshot first,
because `~/Dev` is not a git repository:

```bash
cp ~/Dev/ARMADA.md /tmp/armada-before.md                        # step 4, before the first edit
diff /tmp/armada-before.md ~/Dev/ARMADA.md > /tmp/armada.diff   # step 6, before reporting
```

| Bound, and where stated | Readback | Observed | Within? |
|---|---|---|---|
| entry `~20 lines` — :18 | `awk '/^### <p> /,/^### [^<]/' ARMADA.md \| wc -l` | 9 | yes |
| **Status** `1–2 sentences` — :18, :29 | count `.` `!` `?` in the field | 2 | yes |
| **Features** `≤8` — :18, :31 | count `, ` + 1 | 8 | at cap |
| **AI/tech opportunities** `≤3` — :32 | count `;` + 1 | 3 | at cap |
| sections touched = **1** — description, :11 | hunk headers in `/tmp/armada.diff` | 1 of 71 | yes |
| index rows touched = **1** — :19 | `grep -c '^> |' /tmp/armada.diff` | 1 | yes |
| changelog lines added = **1** — :19 | added lines below `## Changelog` in the diff | 1 | yes |

**[measured-here]** Two of those are soft in the live file, which is what makes the readback worth
running: the `fledgeling-plugins` entry at `ARMADA.md:578` carries a **Status** of 155 words in **6
sentences** against the stated `1–2`, and its index row carries different prose from the entry's despite
:19 asking for the *same status phrase*. Claude runs wrote those, so they say nothing about this family
— they say the bound has no instrument behind it. **[derived]** One bound also needs a second axis to
measure anything: `~20 lines` counts markdown lines while a **Features** field can be 167 words on one
of them, so that entry is 10 lines and 594 words. Read it as *≤20 lines **and** ≤250 words*.

## Override 1 — the manifest will not fit in one Read (steps 2 and 3)

**[measured-here]** `~/Dev/ARMADA.md` is ≈94k tokens; a plain `Read` of it returns `File content exceeds
maximum allowed tokens (25000)` and returns nothing at all. **[measured-family]** `evidence.md` §1.2.3:
on the session that hit this exact ceiling the model retried `Read` **four consecutive times** with minor
parameter tweaks before pivoting to a Python split. **[docs]** The rule it broke is published: "On
*other* errors, you must change your strategy or arguments, not repeat the same failed call." A capacity
ceiling pivots on attempt **1**, not attempt 2 — so never read the manifest whole; address the two
regions you may touch and nothing else:

```bash
grep -n '^### <project>' ~/Dev/ARMADA.md      # the entry's start line
grep -n '^| \[<project>\]' ~/Dev/ARMADA.md    # its index row
sed -n '<start>,<end>p' ~/Dev/ARMADA.md       # the entry, and only the entry
tail -20 ~/Dev/ARMADA.md                      # the changelog tail, for the line shape
```

Two attempts per tool otherwise, then change approach; a permanent error — `command not found`, no git
repo, no commits since the stamp — gets one, and the answer is a report line rather than a third attempt.
**[docs]** Step 3's *gather the delta cheaply* has a vendor form worth borrowing verbatim: "You have a
limited action budget of <n> tool calls. Use them efficiently."

## Override 2 — verification is asked for, and this reverses the house style (steps 4–6)

**[docs]** "Include specific verification steps in either the system instructions or your prompts
directly", and from the agentic template, "Review your output against the user's task". **[derived]**
Skills here are written for a model that over-verifies, so verification scaffolding is stripped on
purpose; inheriting that removal is the defect, because this skill ships **no gate at all** — no
`scripts/`, no exit code, nothing that reads the entry after it is written. The snapshot diff is the only
instrument, so it gets run, not described.

**[measured-family]** What fills the vacuum is well-formed and false: a run's own review asserted a
browser engine that had failed all four invocation attempts and never ran, and *100% pass rate on
contrast* from a probe never executed — measured afterwards at 3.65:1 on every primary button. Step 6's
report is where that lands here, so ship it filled:

```
ARMADA SYNC — fledgeling-plugins
  paths     6/6 exist, 6/6 repo-relative                    (/tmp/armada-paths.txt)
  counts    1/1 read from ls, 0 recalled
  bounds    7/7 within: 9 lines / 213 words, Status 2 sentences, Features 8, opps 3
  diff      1 entry section, 1 index row, 1 changelog line, 0 other sections (3 hunks)
  stamp     2026-08-23, from `date +%F`
```

A denominator of zero is a gate that never ran, never a pass: `paths verified` with no count beside it is
not a result. Where a readback could not run — no snapshot taken, no git history to take a delta from —
name the axis the entry is unchecked on rather than dropping the line.

## Override 3 — four passes, and the index row is copied from the entry (steps 4–5)

Step 4 asks for six edits in one rewrite — stamp, **Status**, **Features**, **Read more**, **AI/tech
opportunities**, shape — and step 5 adds two more locations. **[docs]** Under **Too many tasks**: "it is
likely trying to accomplish too much. Break the requests into separate prompts." The remedy is the chain:
"make each step a prompt and chain the prompts together in a sequence", where "the output of one prompt
in the sequence becomes the input of the next prompt."

1. **Delta** — `git -C ~/Dev/<project> log --oneline --since=<stamp>` plus the session, written down as
   a short list of facts before any prose is composed.
2. **Entry** — rewrite the section from that list and the current entry, nothing else.
3. **Index row** — derived *from the entry written in pass 2*. SKILL.md:19 asks for the *same status
   phrase, same date*, so this is a copy rather than a second composition; composing it independently
   is how the two drift, and **[measured-here]** they have drifted on the live row.
4. **Changelog** — one line, appended, in the shape the file's own tail already uses.

**[derived]** Passes 2 and 3 are the one genuine artifact dependency here: the index row has a required
upstream and nothing checks it. Override 2's diff is what makes it observable.

## Override 4 — the date and the counts are read, not recalled (steps 4–5)

**[docs]** "Your knowledge cutoff date is January 2025", and Google's clause for time-sensitive work is
blunt about the consequence: "Remember it is 2026 this year." **[measured-family]** The informative
failure on the observed run was not a guess but Windows 10's published accent colour written onto a
Windows 11 app. **[derived]** The `updated:` stamp is that hazard here, because the template shows
`YYYY-MM-DD` and step 5 shows a stale example date — so the stamp comes from `date +%F` and the changelog
line reuses that string, `specs: <dir> (n)` takes `n` from `ls <dir>/*.md | wc -l`, and **Apps** rows
come from `ls apps/`.

**[measured-family]** The same rule covers documents the prompt names. `evidence.md` §1.2.4: asked a
question naming three skills, the run answered from memory without loading any, then inverted the error
and launched a skill when an answer was wanted. Read-then-answer is two ordered steps and neither
substitutes for the other: when `ship-armada` hands over a stale entry, or a prompt names `README.md`,
`CLAUDE.md` or an `ORCHESTRATOR.md`, load them and *then* write **Status**.

## One worked example, before the set

**[docs]** "We recommend to always include few-shot examples in your prompts", and "you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand." The
**Entry template** is a structure specification with slot descriptions rather than an instance —
**[docs]** half of what the checklist asks: "Avoid leaving the model to guess the structure of the
output; instead, use a clear, explicit instruction to specify the format and show the output structure
in your few-shot examples." Fill one instance to full fidelity first:

```markdown
### fledgeling-plugins · skill-plugin · updated: 2026-08-23

**What:** Fledgeling's public Claude Code plugin marketplace, authored by Luke. 44 plugins, each with an icon set, banner and README; `site/` indexes the repo at build time.
**Status:** Actively developed. `defer` v1.0.0 merged and pushed at `d73997f`; seven branches remain unmerged.
**Stack:** Markdown skills plus Python and Node harnesses; `site/` is Next.js 16, React 19 and TypeScript on Vercel.
**Apps:** `site` — skills.fledgeling.app, the searchable directory (Vercel project `fledgeling-skills`, root `site`).
**Features:** defer 1.0.0, agent-voice 0.1.1, armada-sync 1.0.0, email-digest 1.7.0, code-review 1.2.0, recover-claude-code 1.0.0, should-compact 0.3.0, site/
**AI/tech opportunities:** Two marketplace entries carry no `category` and the catalogue gate does not fail on it; eight unmerged branches carry finished work; the skills pointing at `defer` name it bare across two marketplaces.
**Read more:** `README.md` · `CLAUDE.md` · `plugins/defer/README.md` · `site/scripts/build-catalogue.mjs` · `.claude-plugin/marketplace.json` (44 entries)
```

Receipt: 9 lines · 213 words · **Status** 2 sentences · **Features** 8 · opportunities 3 · 5/5 paths
exist. **[docs]** "Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats" — every field keeps template order, and one with nothing true to say is
omitted rather than padded.

## `thinking_level`, and the modules not written

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as multi-step planning,
verified code generation, or advanced function calling scenarios", and Gemini 3.7 Flash defaults to
`MEDIUM`. **[derived]** This skill is none of those — a bounded read-and-edit over two regions of one
file — so the default is correct, and **[docs]** raising it works against step 3's own cheapness rule:
"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering the
level can reduce tool calls." **[measured-family]** It is no remedy for anything above either: paired
across the 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7 points.
**[docs]** Brevity is the resting state — "By default, Gemini 3 models provide direct and efficient
answers" — which suits step 6's one-or-two-sentence report, so trim its preamble and never the receipt.

**[measured-here]** The scan fired no modules, at three triggers and at two, and the skill earns that: it
renders nothing (`visual`), ships no probe or exit code (`gate`), enumerates no unhappy paths beyond the
two already handled (`states`), cites no vendor design values (`platform-values`), spawns nothing
(`delegation`) and ingests nothing it did not author (`injection`). Two near misses sit in the core
instead: `bounded-constraint`, moved in by hand above, and `count-contract`, whose `(n)` counts fold into
the quota ledger. `authorship` is worth naming: the entry is prose a reader acts on, but the skill's own
rule covers it — *prose states facts, not aspirations* — and this file's grounding is Override 4's.
