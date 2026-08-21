🫥 The framing is sound — the unmeasured class is the genuinely correct insight most "remaining work" tooling lacks. Answers in order.

## Q1 — Taxonomy and gate

The five classes are right in spirit, but derive them instead of declaring them. Materialize the three-way join **brief ↔ requirement ↔ case** as an explicit artifact, and the classes fall out as *residue classes of the join plus evidence status*. That makes classification a function (disjointness for free) and makes the gate computable. Concretely: a case tracing to no requirement is (d) unnamed; a brief tracing to nothing in the registry is (a) — though see Q3 for why (a) really means "registry-silent", not "proven unbuilt".

Three corrections to the draft:

- **Split decision-work out of (c).** `contradicted` and `vacuous` don't need an instrument; they need a human ruling (stale doc vs. real regression; rewrite the requirement before it's even testable). Different fix-shape, so different class — call it (f). It routes naturally to `whats-left`'s questionnaire, since it's the one class only the developer can burn down.
- **(e) must carry the oracle rung.** An `observed` at `presence` does not retire a brief; at `effect-witness` it does. Encode a retirement threshold (rung ≥ outcome, say); below it, (e) becomes "probably done — route to `spec-validation` before retiring." Otherwise you retire intent on the weakest evidence in the ladder, which is the same silent-done failure wearing a different hat.
- **Precedence rule for overlaps.** A defect on an unnamed surface is both (b) and (d). Pick a fixed priority (evidence classes beat naming classes) so every row lands exactly once.

**The gate: total reconciliation, exit-code checked.** A script asserts (1) every input ID — brief file, requirement, case, defect — appears in **exactly one** ledger row, sets equal both directions, and (2) a status→legal-class table: `blocked|inconclusive|unoracled|carried` may only land in (c); `reported|unknown` may not support (e); rung < threshold may not support retirement. Exit nonzero on any orphan or illegal placement. This makes the central failure structurally impossible rather than reviewed-for: an unmeasured case cannot vanish, because it must land somewhere, and the only legal somewhere is (c). Note the join is the weak point — briefs don't share IDs with requirements, so that matching is the one fuzzy step. Emit the mapping with per-edge confidence and gate on the unmatched count too; a reconciliation gate over a bad join is theater.

**Denominator: yes, mandatory, and per-axis — never blended.** "This report can speak for 4/15 stated requirements (27% observed) and 20/42 designed cases (48% adjudicated — pass, fail and n/a all count as *measured*; a fail is knowledge)." Two honesty rules: fails count toward the numerator (measured ≠ passing), and the denominator is a **floor**, stated as such, because every (d) finding proves the intent space is bigger than the documents. Generate the markdown headline numbers from the ledger JSON so the prose number can't drift from the gated one.

## Q2 — Z > Y > X

**Z is the product.** The audience is one developer driving AI executors: executors consume JSON, CI consumes exit codes, the developer reads twenty lines of markdown. Everything else is a view over the ledger.

**Y second, but as a flagged action, not default output — and only for (c) and (d).** Class (a) already has briefs. The danger is a feedback loop: the skill reads the triage queue and writes into it, so an unstamped generated brief inflates next run's denominator and duplicates on re-run. Stamp frontmatter (`generated-by`, source case/requirement IDs) so re-runs update idempotently and the skill recognises its own emissions.

**X last: don't build it, route to it.** `whats-left` already owns "browsable page + human decisions." Hand it the ledger — building a second HTML surface violates your own no-duplication rule, and class (f) is literally its questionnaire input.

## Q3 — (z), with two amendments

(x) fails because registry silence is ambiguous — "no case and no requirement" cannot distinguish unbuilt from built-but-never-campaigned, and routing 200 briefs × 40 repos to `spec-validation` is not a price you'll pay, so in practice (x) means guessing. (y) as agentic code-reading is cost without strength — a name-grep hit is weak evidence, and it tempts the skill to promote grep hits toward "done", which is the exact failure the design exists to prevent.

So (z), amended: **count registry silence as disagreement** (a brief's implicit claim vs. the registry's nothing), and **cap what code evidence may do — it only ever demotes or routes, never promotes.** A producer hit on a silent brief moves it from (a) to "possibly built — route to spec-validation"; absence leaves it in (a). Done-ness stays exclusively spec-validation's verdict. One cheap addition: a deterministic ripgrep over identifiers extracted from each brief is nearly free as a *script* (it's (y)'s coverage at none of (y)'s cost) provided its output is confined to that same demote-or-route role.

## Q4 — two upgrades not in your list

1. **Key class (c) by blocker, not by case.** Your 20 blocked cases almost certainly trace to ~3 root blockers (dead OAuth, destructive sign-out, no full-disk hook). The enablement output should be per-blocker briefs, each listing the cases and requirements it unblocks: "recovering the OAuth credential unblocks 12 cases; coverage moves from 48% to ~74%." That measurement-ROI number is the actual prioritisation signal a solo developer needs, and it's computable from the join. Highest-value single change to the draft.
2. **Make the ledger persistent and diff across runs.** Asked once, "what's remaining" is a report; committed in-repo and diffed per campaign, it's a ratchet. Then the gate checks *transitions*, not snapshots: no item may leave (c) except via an evidence-bearing event (new case ID at sufficient rung, or a spec-validation verdict), and an item that disappears between runs without one exits nonzero. That kills silent-done permanently rather than per-run, and gives you a coverage trend line per repo for free.

Minor: give every ledger row a `kind ∈ product-work | evidence-work | decision-work`. It's the field executors filter on — evidence-work must never leak into a feature backlog, and the field makes that a schema fact instead of a convention.
