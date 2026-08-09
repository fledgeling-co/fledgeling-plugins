# Evidence

Every number in SKILL.md, where it came from, and how far it should be
trusted. Built from a five-backend research panel (Claude Code, Codex CLI,
Perplexity Sonar, Gemini Deep Research, OpenAI gpt-5.6) run on one brief in
August 2026. Full reports in `docs/deep-research/`.

Read this before changing a threshold. Several of the numbers here are
deliberately conservative authoring defaults rather than measured optima, and
the file says which are which — a rule swapped without knowing which kind it
was is how a skill drifts away from its evidence.

## How the panel behaved, and one warning about it

Four of the five backends converged closely: ask on divergence, batch, cap at
three, 2-4 options, recommend only with a reason, keep it short and plain.

**The Gemini report is the outlier and should be discounted.** It sources the
exponential cost-of-change curve to `reworkcost.com`, the "25-minute recovery"
figure to `usecarly.com`, and a batching claim to `lifetips.alibaba.com` — SEO
aggregators, not primary literature. It asserts a "9-12 option neurobiological
sweet spot" that three other members refute with a 63-condition meta-analysis.
It is retained in the corpus because discarding a member silently would
misrepresent the panel, and because it surfaced one finding nothing else did
(ASPI, below) which was then verified first-hand.

Citation check on the strongest member: **zero fabricated citations** out of 62;
85% confirmed to exist, the rest blocked by publisher bot-walls rather than
missing.

## The gate

**The divergence test.** ClarifyGPT generates candidate solutions from an
ambiguous request and asks only when they disagree. Human-in-the-loop, this
lifted GPT-4 Pass@1 from 70.96% to 80.80% on MBPP-sanitized (+13.87% relative,
p = 3.2e-05), and +16.83% on MBPP-ET. *Mu et al., FSE 2024 / PACMSE,*
<https://dl.acm.org/doi/full/10.1145/3660810>

This is the strongest single result behind any rule in the skill, and it is why
gate step 2 asks you to sketch both readings rather than to judge whether the
request "feels vague".

**Restraint is measurable, and correct restraint looks like nothing.** Ask or
Assume partitions tasks by whether the agent asked. On the 344 tasks where it
asked, it scored 65.99% against a no-information baseline of 44.48% — the
information was worth having. On the 156 where it declined, it scored 76.92%
against the baseline's 77.56% — there was genuinely nothing to learn. *Edwards
& Schuster, arXiv:2603.26233, March 2026*

**Encouragement backfires.** Told plainly to ask when unsure, Llama 3.1 70B
asked on 93-95% of *fully specified* SWE-bench issues. *Vijayvargiya et al.,
Ambig-SWE, ICLR 2026, arXiv:2502.13069.* The opposite failure is just as
measured: across 1,000 AmbigQA items and ten models, internal recognition of
ambiguity ran 60-80% while outward asking was ≤5%. *Su & Cardie,
arXiv:2605.25284, May 2026*

Both numbers point the same way: an instruction to ask more does not produce
better asking. That is why the gate is a set of tests and why this skill's
description leads with restraint despite being a skill about asking.

**Do not justify any of this with the cost-of-change curve.** The delayed-issue
effect was tested across 171 projects (2006-2014) and not found; the authors
conclude it "is not a constant across all projects". *Menzies, Nichols, Shull
et al., Empirical Software Engineering 22:1903-1935, 2017.* The Standish CHAOS
figures rest on a one-sided estimation definition. *Eveleens & Verhoef, IEEE
Software 27(1), 2010.* One panel member leaned on both; it was wrong to.

## Batching and timing

**Cap of three.** The systems with the best outcome-per-question ratio asked
1.39-3.06 questions per task. The highest-volume asker (6.02/task) was the one
model that got *worse* when given the information it had asked for. *Suri et
al., Findings of ACL 2026; Ambig-SWE.* Fragmented asking is scored as its own
failure: two models tied on premises resolved (0.643 vs 0.640) but scored 0.365
vs 0.456 on efficiency-adjusted recall, purely on turns-to-clarify. *Li, Wu &
Chang, ClarEval, arXiv:2603.00187*

Held loosely: three of the four converging reports say explicitly that three is
a conservative operational rule, not an empirical optimum. **No controlled study
compares 1 vs 2 vs 3 vs 4 clarification questions in a coding agent.** That
experiment does not exist and would settle the number.

**What an interruption actually costs.** Only 10% of programming sessions resume
work in under a minute after an interruption, and only 7% resume with no
navigation first. *Parnin & Rugaber, Software Quality Journal 19:5-34, 2011 —
10,000 sessions, 86 programmers, plus 414 surveyed.* This is the figure the
batching rule rests on, and it is first-party observational data rather than the
widely-quoted "23 minutes" that traces back to blog posts.

Related and often misread: interrupted tasks in a controlled office study were
completed *faster*, not slower — people compensate, "but at the price of more
stress, higher frustration, time pressure and effort". *Mark, Gudith & Klocke,
CHI 2008.* Speed is the wrong outcome to measure here.

**Timing and the ignored third.** In a within-subjects study of proactive AI
help to programmers (N=18, 1,004 logged episodes, 398 proactivity instances):
53.3% led to effective engagement, 12.1% were disruptions, 34.7% were ignored.
Sub-task boundaries were the only timing heuristic that worked; inferring
availability from idleness **failed outright**, because idleness often signalled
high load — thinking, not waiting. *Pu et al., CHI 2025, DOI
10.1145/3706598.3713357*

That failed heuristic is why the skill says never to read silence as
availability, and the 34.7% is why an unanswered question needs a fallback.

## Options and ordering

**2-4 options, aim for 3.** Two panel members independently landed on "2-4,
default 3".

**The usual reason for this is wrong.** Choice overload pools to a mean effect
size of virtually zero across 63 conditions from 50 experiments (N = 5,036),
with no sufficient conditions identified for reliable overload. *Scheibehenne,
Greifeneder & Todd, JCR 37(3), 2010.* A later meta-analysis (99 observations,
N = 7,202) recovers the effect under four moderators — complexity, task
difficulty, preference uncertainty, decision goal. *Chernev, Böckenholt &
Goodman, JCP 25(2), 2015 (see the 2016 corrigendum).*

Both camps agree overload appears where preferences are *unformed*. An engineer
answering a fork about their own project has formed preferences, so overload is
a weak argument here. The real reasons to cap are reading cost and primacy bias,
which grows with list length and has been observed at lists as short as seven.

**Reaction time is not the constraint.** RT = a + b·log₂(N) at roughly 140
ms/bit: about 160 ms for one alternative, 600 ms for eight. *Proctor &
Schneider, QJEP 2018.* Note the trap that follows from it — three sequential
5-option steps can cost more than one 15-option step, so splitting a question to
shorten each list can lose more than it saves.

## The recommendation

This is where the panel actually disagreed, and the disagreement changed the
skill.

- One member: lead with a marked recommendation, placed first.
- Another: **do not** lead with one on a preference-sensitive decision; state it
  after neutral options and label it as advice.
- A third resolved it: recommend first **when repository evidence or explicit
  constraints make it superior**; use neutral ordering and no recommendation
  when eliciting a subjective preference.

SKILL.md takes the third position, because it explains the other two rather than
splitting them.

**The asymmetry that justifies it.** In a controlled e-prescribing experiment,
correct decision support cut omission errors by 38.3-46.6%; *incorrect* support
raised them by 24.5-33.3% and produced commission-error rates of 51.7-65.8%.
*Lyell et al., 2017.* Meanwhile the upside is capped: measured weight-of-advice
is 0.20-0.30 in the classic review (*Bonaccio & Dalal, OBHDP 101(2), 2006*) and
0.39 [0.37, 0.42] in a 2024 meta-analysis (*Bailey et al.*) — people move only
20-40% toward advice, and discount it harder when unsolicited.

Small upside, large downside, and the downside lands hardest exactly when you
are confidently wrong. Hence: the reason carries the recommendation, not the
label.

**Defaults are strong, which is the risk not the benefit.** A default-effects
meta-analysis of 58 studies (n = 73,675) puts the pooled effect at d = 0.68,
95% CI [0.53, 0.83]. Opt-out versus opt-in roughly doubled consent, ~42% → ~82%
(*Johnson & Goldstein, Science 302, 2003*), and their proposed mechanism is that
people read a default as an implicit recommendation. Marking an option is
therefore not a neutral act.

Held loosely: the broader nudge literature does not survive bias correction
intact. Pooled d = 0.43 with a significant Egger's test, dropping 22.5% under
moderate-bias adjustment (*Mertens et al., PNAS 119(1), 2022*); a robust
Bayesian re-analysis of the same data found **no evidence** for an overall
nudging effect (*Maier et al., PNAS 119(31), 2022*). Do not design as though
"(Recommended)" moves choices by a known amount.

## Wording

**≤20 words for the question stem, 25 hard cap.** Payne's 1951 rule; Johnson &
Morgan (2016) relax it to 25. Reliability declines with word count across 426
exactly-replicated questions in six panel surveys (*Alwin & Beattie,
Sociological Methodology 46(1), 2016*).

Held loosely, and honestly: a competing review finds question length **not**
consistently associated with respondent behaviour, noting length is confounded
with complexity and that longer questions can give more time to think (*JSSAM
7(2):275, 2019*). The resolution most authors reach is that **words are a proxy
for complexity, and complexity is the real driver**. The cap is a usable
heuristic, not a law. No primary source reproducing Payne's original phrasing
was located; the 20-word figure travels entirely through secondary literature.

**What plain language actually buys.** Less than people assume. Rewrites move
readability scores reliably, but measured comprehension gains run 0-14
percentage points and are frequently null in adequately powered RCTs — a
150-parent randomised consent trial found 55.7% vs 46.2%, p = 0.303. Changing
the *process* rather than the words moved comprehension 45.2% → 73.1%
(+27.9 points, p < 0.001) in a cluster RCT.

So the honest claim for the wording rules is **speed and willingness to answer,
not accuracy**. Where the underlying concept is hard, shortening the sentence
will not fix it — restructure the question instead. This is also why the skill
puts as much weight on the gate and on batching as on phrasing.

**Seven linguistic features raise cognitive burden** — low-frequency words,
left-embedded syntax, vague relative terms — with at least six materially
affecting clarity (*Lenzner, Kaczmirek & Lenzner, Applied Cognitive Psychology
24, 2010*); less comprehensible questions produce worse break-off, more
non-substantive and more neutral answers (*Lenzner, Field Methods 24(4), 2012*).
The linter's jargon checks target this class directly.

**Double-barrelled questions** changed item meaning in six of eight tested items
in one experiment, and difficult wording raised skips from 4.3% to 10.5% in a
randomised survey experiment. Worth noting the contrary detail: response
latencies for double-barrelled items were equal or *shorter*, which is read as
respondents answering one half and ignoring the other — the damage is silent.

## The note

**The specific design — an optional free-text note attached to a chosen option —
has not been tested by anyone.** Two panel members say so explicitly. What
exists is adjacent evidence pointing in three directions:

- Closed lists miss real categories that pretesting does not catch (*Schuman &
  Presser*), which argues for an escape hatch.
- A standalone "don't know" *substitute* for choosing fails: across nine
  experiments in three household surveys, omitting no-opinion options did not
  compromise data quality, and the option attracted the least motivated
  respondents (*Krosnick et al., POQ 66(3), 2002*).
- Mandatory or prominent open-ended prompts raise break-off and answer-changing
  (*Hadler, Sociological Methods & Research, 2025*), and carry far higher
  non-response — Pew measures 12-17% for open prompts against 1-2% for closed
  questions on the same panel.

The design threads these: a note *beside* a committed choice is not an escape
*from* choosing, and leaving it optional means it costs nothing to those with
nothing to add. Its most defensible value is as a **detector of a bad option
set** — if notes keep arriving, the options were wrong.

Treat this section as reasoning, not evidence. It is the weakest-supported part
of the skill and the part most worth measuring later.

## The security rule

**Asking makes you more vulnerable, and it is a large effect.** The ASPI
benchmark runs 728 task-attack scenarios twice under matched conditions — once
with a fully specified instruction, once where the agent must request and
incorporate user input before acting. Attack success rose from 1.8% → 34.0%
(o3) and 2.2% → 35.7% (Gemini-3-Flash), consistently across ten frontier models.
The authors' conclusion is that evaluating security at execution time
"systematically underestimates the attack surface of interactive agents".
*arXiv:2605.17324, May 2026; code at github.com/scaleapi/aspi*

Only one panel member surfaced this, and that member is the one with the
weakest sourcing overall — so it was verified first-hand against the paper
before being made a rule. It is the reason SKILL.md treats a note as data about
the decision rather than as instructions.

## What is not supported

**Decision fatigue, as a depletable-resource mechanism, is not.** Ego depletion
failed a 23-laboratory preregistered replication (N = 2,141, d = 0.04). The
flagship parole-board field result is confounded by non-random case ordering.
The skill never argues from decision fatigue, and neither should anything built
on it — interruption cost and order bias are both better measured and sufficient.

## The description, and why it is still unproven

The `description` field is the whole triggering mechanism, and it is the one part of this skill
with no measurement behind it. A trigger-optimisation run over twenty queries returned 0% recall
on both the shipped description and a full rewrite, identical to the digit — which says the run
was not measuring the description rather than that the description fails. `EVALS.md` has the
detail.

The rewrite is kept here rather than shipped, because swapping one unmeasured description for
another is not an improvement, only a change. It is worth trying if real use shows the skill
under-triggering, since it leads with trigger conditions instead of with what the skill does,
which is the shape skill-creator and Anthropic's own guidance both recommend:

> Use when a decision, assumption, or ambiguity needs the user's input before work proceeds.
> Triggers: they ask what you need from them, tell you to check with them first, say not to just
> pick one, want a say in an approach, or want unknowns surfaced before code is written; a
> request or spec is vague enough that different readings produce different work; you're about to
> build on an unverified assumption; a fork has several defensible answers involving taste, scope,
> cost, or risk; or an action is destructive or irreversible. Also covers gathering everything you
> need in one batch before a big task starts. First hunts the answer in the conversation, repo,
> and prior work, drops questions whose answer wouldn't change anything, then asks one clickable
> AskUserQuestion with a reasoned recommendation and reads any note the user attaches. Skip for
> routine calls you should just make, and for explaining something the user asked you to clarify.

The last clause is the useful part either way: *"skip for explaining something the user asked you
to clarify"* separates this skill from the commonest near-miss, someone asking Claude to clarify a
regex or an error message. That distinction is worth keeping whichever description ends up
shipping.

## Gaps worth measuring

1. **Option count in this exact setting.** Nobody has varied 2 / 3 / 4 / 6
   options on matched forks in a real agent. The 2-4 rule is an inference from
   order bias and reading cost, not a measurement.
2. **The note, as an A/B.** How often it is used, and how often its content
   reveals a category the options missed.
3. **Batch size.** No controlled comparison of 1 / 2 / 3 questions in a coding
   agent exists.
4. **Every agent benchmark cited here uses a simulated user**, and at least two
   of the papers flag that simulated users are unnaturally cooperative. Every
   measured benefit of asking is therefore an upper bound. A real person answers
   late, partially, or not at all.

One transfer caveat worth carrying: the survey and decision-science findings
were mostly generated on lay respondents with low motivation, answering about
topics they did not choose. An engineer answering about their own project has
high ability and high motivation, so the satisficing-derived rules bind *less*
here — while the interruption-derived rules bind *more*, because that same
person has valuable work to get back to.
