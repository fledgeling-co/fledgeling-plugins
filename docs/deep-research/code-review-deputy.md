# deputy

> Source: `~/Dev/dossier/deputy/index.html`. Published research page, captured 20 August 2026 for the `code-review` and `atlas-publish` skills. Live at https://dossier.fledgeling.app/deputy where published.

  

    

      [![](data:image/svg+xml;base64,<stripped>)
        **Dossier**](https://github.com/fledgeling-co/dossier-research-mcp)
      
      [![](data:image/svg+xml;base64,<stripped>)
        **Margin**](https://margin.fledgeling.app/)
    
    

      
Not a compliance opinion
        A research page about who may sign off software, not legal advice about whether a rule applies to you.

    
  

  

    

      **Deputy**
      Can a model sign this off?
    

    

      
        
        
        
        
        
      
      The whole question
    

    
      Read this as
      
      **Primer**from scratch
      
      **Brief**what it means
      
      **Technical**how we know
    

    Auto
  

  

  

    
The finding

    
# You can hand a robot a job. You can’t hand it the blame.You can delegate the decision. You cannot delegate the signature.

    

      
Four different AI research systems went looking, separately, for a company that
      lets computers do the last check on software before it ships with nobody signing
      off afterwards. None of them found one.[1](#r1)

      

        - The rule that gets in the way isn’t about how clever the computer is. It’s a rule
        about names: the signature at the bottom has to belong to one person, and a computer
        isn’t a person.[2](#r2)

        - Here’s the odd part. When you ask nine of the cleverest computers the same question,
        you don’t get nine opinions. You get about two.[1](#r1)
        So stacking more of them up doesn’t buy what it looks like it buys.

        - Our own robot checked fifty screens and said “I can’t tell” fifty
        times.[3](#r3) That’s the honest
        answer, and it’s the start of a better plan: give the machine a small job it can
        actually finish, and keep a person’s name on the part that matters.

      

      
**What would change this.** Nobody has measured the human. There’s
      no study anywhere that checks how often a person doing this job gets it
      right.[1](#r1) So “as good as a
      human” has no number to be as good as.

    

    

      
The substitution is possible, but only as a warrant rather than a verdict:
      name the class of item a machine may close, keep the classes where the call turns on
      materiality, omission, tenant isolation or a novel interaction, and put a named human on
      the policy instead of on every ticket.

      

        - Four independent readers went looking for a counter-example and none of them found
        one: no regulated software vendor whose all-machine verification step was accepted as the
        control of record.[1](#r1)

        - The reason isn’t capability. A 21 CFR Part 11 signature has to be unique to one
        individual, and a model identifier isn’t an
        individual[2](#r2); PCAOB benchmarking only
        permits leaning on last year’s testing of an automated control if the control
        hasn’t changed, which a silently reversioned model can never
        satisfy.[4](#r4)

        - Adding models doesn’t fix it either. Nine frontier judges across seven families
        supply about two effective independent votes, panel accuracy lands 8 to 22 points short of
        genuinely independent voting, and the best single judge matches or beats the whole
        panel.[1](#r1)

      

      
**The one thing that would change it.** Nobody has ever run a powered
      non-inferiority study on human code or UI
      acceptance.[1](#r1) The incumbent is
      unmeasured, so every claim about matching a human is an argument rather than a result. From
      here the page tightens the warrant, from what a regulator has actually let a machine decide
      alone down to what fits inside one here, and then says what to do with the 194 items already
      queued.

    

    

      
Defensible substitution is graded authority, not a jury: a pre-registered
      low-risk class closed by machine, human retention of materiality, omission, cross-tenant and
      novel-interaction classes, and a named human owning the policy rather than countersigning
      items. All four independent readers converge on this shape from different starting points,
      which is the strongest signal in the corpus.

      

        - No regulated vendor found with an all-machine step accepted as the control of record;
        also no enforcement action or qualified opinion where the defence was “the automated
        checks passed”. Search absence across four
        readers.[1](#r1)

        - Nine judges, seven families, about two effective independent votes; panel accuracy 8 to
        22 pp below independent voting; best single judge ≥ panel across all tested conditions;
        established aggregation closes at most 11% of the gap even given the correct
        answers.[1](#r1) Measured on NLI and
        RewardBench, not on UI acceptance; the transfer is an assumption. Preprint.

        - Local ground: 194 items in Done awaiting the human step; roughly 3,011
        Playwright test instances across 137 spec files, of which CI selects 420, or
        13.9%.[5](#r5) The product’s own
        screenshot-judging pass holds 50 surfaces with both captures and expectation atoms present,
        and returns `inconclusive` on all 50, stated each time as being for want of a
        judge rather than for want of an
        oracle.[3](#r3)

      

      
**The largest gap.** No powered non-inferiority reader study exists for
      code review or UI/feature
      acceptance.[1](#r1) A search absence rather
      than a proof of absence, and it is the measurement the decision most needs.

    
  

  

  
## The warrant, drawn as five nested scopes

  
    
### The warrant narrows four times, and a different body of evidence forces each narrowing.

    

      

        Scope 0 · a person holds all of it
        Everything a verifier decides today
        Materiality, omission, tenant isolation, novel interaction, and
        whether the thing built is the thing that was asked for.
        194 items queued here right now[5](#r5)
      
      

        Scope 1 · what a regulator has permitted
        One indication, one camera, and a duty to refuse
        The only machine cleared to decide without a clinician was scoped
        to a single disease and a single device, validated against an external reference standard,
        and required to escalate rather than guess.
        Sn 87.4% · Sp 89.5% · n=819 · 38 forced referrals[7](#r7)
      
      

        Scope 2 · what a warrant can carry
        A named class, a pinned version, a human policy owner
        A signature must belong to one individual, and an automated control
        may only be leaned on across periods if it has not changed. Both cut a per-item machine
        verdict; neither cuts a standing scope with a person answerable for it.
        Re-qualification on version change[8](#r8)
      
      

        Scope 3 · what survives the evidence channel
        Nothing whose evidence the judged party controls
        Agents rewrite tests and patch evaluators; a green suite can miss
        over half of injected faults; and tenant-authored text renders into the very screenshot a
        vision judge reads.
        30.4% of runs reward-hacked[16](#r16)
      
      

        Scope 4 · what actually fits inside
        Perceptual classes, with a declared miss rate and a way out
        Display defects a labelled detector reaches about 85% precision and
        84% recall on, closed by machine, with `inconclusive` as a terminal state that
        routes to a person rather than a retry.
        ≈16% missed is the ceiling, before any domain shift[20](#r20)
      
    
    
      Each box is smaller than the one above it. The big outside box is
      the whole job a person does now. The little filled box at the bottom is the part a machine can
      be trusted with on its own. Everything between the two is held back for a reason, and each
      reason is a different piece of evidence.
      Read top to bottom as a tightening rather than a ranking. Nothing
      here is an argument that the machines are weak; every narrowing is forced by something
      outside the model, and the accent marks the only band a machine holds alone.
      Levels are authored from the claim graph, not from the research
      brief: Scope 1 from DEN180001, Scope 2 from the conjunction of 21 CFR 11.100/11.200 and PCAOB
      AS 2201 ¶B28 to B29, Scope 3 from the reward-hacking and mutation-survival evidence, Scope 4
      from the published detector ceiling. The nesting is a device, not a measurement; the inset
      distances encode no quantity.
    
  

  

  
**Scope 0** · the shape of the answer

  
## The answer is a smaller job, not a yesReasoning

  
## The answer is a scope, not a verdictReasoning

  

    
Think about a learner driver with an instructor beside them. The learner really is driving.
    They’re allowed to steer, brake and pick the lane. What they can’t do is sign the form
    at the end that says this car is safe to be on the road.

    
That’s the shape of the answer. The machines can do a lot of the driving. The form still
    needs a person’s name on it.[2](#r2)
    Four separate searches for a company doing it any other way came up
    empty.[1](#r1)

  

  

    
Every version of “can AI replace the verifier” that gets asked out loud is asking
    for a verdict: a thing that looks at the work and says yes. The corpus answers a different
    question, because that is the question everyone who has tried it in a regulated setting ended up
    answering. What you can give a machine is a warrant: a written scope saying exactly which
    decisions it may make, and what it must escalate.

    
That distinction does real work. A verdict needs an accountable signer, and no model
    identifier can be one.[2](#r2) A warrant
    needs a scope, a policy and a person who owns the policy, all of which exist already.

    
It’s also the shape all four independent readers arrived at from different starting
    points, which is the part of this corpus I’d defend
    hardest.[1](#r1)

    
Worth knowing what the market does not offer while you’re deciding: no vendor in the
    surveyed landscape publishes an independently adjudicated false-negative rate for “feature
    genuinely complete”, and no named customer is documented as having removed a human
    sign-off step because of a
    product.[1](#r1) So there
    is nothing on sale that would settle this for you.

  

  

    
The finding is an inference, marked as one, drawn from the absence of a measured incumbent,
    the correlated-judge result, the single regulatory clearance, the tool-qualification regimes, the
    signature rule and the absence of any accepted all-machine control.

    
The distinction is operational rather than rhetorical. A verdict is a per-item attestation and
    inherits the signature requirement[2](#r2)
    and the unchanged-control
    predicate.[4](#r4) A warrant is a standing
    scope with a named policy owner; the per-item act inside it is a *measurement*, which no
    standard in the corpus requires an individual to sign.

    
Convergent derivation across the four independent readers, from four different entry points:
    the OpenAI lane from tool-qualification regimes, Grok from the regulatory clearance record,
    Perplexity from the reader-study literature, Gemini from vendor feature surfaces. Convergence on
    a shape is not corroboration of a measurement, and §5 is the reason to hold that distinction
    firmly.

    
Absence of a counter-example is the load-bearing evidence here, and it is a search absence:
    auditors’ acceptance decisions are frequently private, and vendor terms are contractual and
    often unpublished.[1](#r1)
    The same shape holds commercially: no surveyed vendor publishes an independently adjudicated
    false-negative rate for feature completeness, and no named customer is documented as having
    retired a human sign-off because of one.

  

  

  
**Scope 0** · the ground this stands on

  
## There are 194 finished jobs waiting for a person

  
## The fence here already has 194 items stacked against it

  

    
Right now there’s a queue of 194 finished jobs waiting for a person to look at
    them.[5](#r5)

    
There’s also a robot that takes pictures of the screens and compares them to the
    drawings. It looked at fifty of them and said “I can’t tell” every single
    time.[3](#r3) Not because the pictures
    were missing. Because there was nobody to ask.

    
And there’s a reason a person is in this queue at all. When the people who built the work
    were the ones who checked it, about half of a batch of 110 jobs turned out not to match what was
    asked for, while looking
    finished.[6](#r6)

  

  

    
This isn’t a hypothetical. 194 items sit in Done waiting on the human step, the suite
    holds about 3,011 Playwright test instances across 137 spec files, and CI runs 420 of them, which
    is 13.9%.[5](#r5)

    
The screenshot-judging pass is the interesting one. Fifty surfaces have both their captures
    and their expectation atoms present, and all fifty verdicts read
    inconclusive.[3](#r3) Each one records
    the reason as wanting a judge rather than wanting an oracle, which means the pipeline is already
    built up to the point where the decision would be made, and stops there.

    
The human step exists for a measured reason. Author-judged acceptance is how roughly half of a
    110-ticket corpus shipped not as specified while reading as
    complete.[6](#r6) That figure is
    internal and has no published method behind it, so treat it as the reason the control was added
    rather than as a benchmark.

  

  

    
Verified locally this session rather than taken from the panel.

    
`verdicts.json` parsed: 50 entries, `gate: inconclusive` on every one,
    with captures and expectation atoms present in
    each.[3](#r3) Playwright listing and
    tracker query: ~3,011 test instances across 137 spec files; CI selection 420 (13.9%); 194 items
    in Done.[5](#r5) The verify stage’s
    own definition records the ~half-of-110 figure as the reason the stage exists and requires an
    out-of-family grader[6](#r6); confidence
    medium, internal, no published method.

    
The 13.9% selection rate is a fact about CI economics, not about coverage, and it is not a
    defect rate. It matters here only because the fault-sensitivity argument in §8 applies to the
    selected set rather than the authored set, and nobody has measured either for browser
    suites.

  

  
    
### The pipeline is finished up to the point where the decision would be made, and stops there.

    

      

        194
        items in Done
        Each one already passed an out-of-family automated verifier. Every one
        waits on the same person.
      
      

        50/50
        verdicts inconclusive
        Captures present, expectations present, judgement absent. Recorded as
        wanting a judge, not an oracle.
      
      

        420/3,011
        tests CI selects
        13.9% of the authored suite, across 137 spec files. A budget decision,
        not a coverage claim.
      
    
    
      Three numbers about us, not about the research. A big pile of
      finished work, a robot that won’t guess, and a set of tests where only some get run each
      time.
      All three measured on this repository rather than reported by a
      backend. The middle one is the load-bearing observation: the machinery is complete right up to
      the judgement, which is exactly where it declines to
      go.[3](#r3)
      Sources are local artefacts, parsed this session: the storyboard
      verdict file, the Playwright listing, and a tracker query. Not corroborated by the panel and
      not intended to be; the panel supplies the outside evidence and these supply the case the
      decision is actually
      about.[3](#r3)[5](#r5)
    
  

  

  
**Scope 1** · what a regulator has permitted

  
## One machine is allowed to decide alone, and its job is tiny

  
## The one machine allowed to decide alone was scoped to a single camera

  

    
There is one machine in the world a medical regulator has let make a call on its own, with no
    doctor checking after it. It looks at photographs of the back of the eye and says whether someone
    needs to see a specialist.

    
Look at how small its job is. One disease. One make of camera. It got the answer right about
    87 times in 100 when the answer was yes, and about 90 in 100 when the answer was no, across 819
    usable cases.[7](#r7)

    
And here’s the part worth copying: when the photo wasn’t good enough, it
    wasn’t allowed to guess. It had to say “send this one to a person”. That
    happened 38 times.[7](#r7)

  

  

    
The clearance record has exactly one example worth studying, and its shape is the argument.
    IDx-DR was cleared to decide without a clinician, and to get there it was scoped to a single
    indication and a single camera, validated prospectively against a reading-centre reference
    standard, and required to refuse rather than guess: 87.4% sensitivity, 89.5% specificity, 819
    analysable cases, 96.1% imageability, and 38 insufficient-quality exams forced to
    referral.[7](#r7)

    
Three of those four properties are available here. A narrow scope, a pre-registered reference
    standard, and a mandatory refusal path are all things you can write into a warrant. The fourth
    isn’t: software acceptance has no equivalent of a reading centre, because there’s no
    gold standard for “this feature is genuinely complete”.

    
The tool-qualification regimes point the same way. DO-330 Criterion 2 covers a tool that could
    fail to detect an error where its output isn’t otherwise verified, and it demands
    operational requirements, a qualification plan, and re-qualification whenever the tool
    changes.[8](#r8)

  

  

    
DEN180001. Single indication, single camera, prospective validation against a
    reading-centre reference standard, mandatory referral on insufficient quality. Sn 87.4%,
    Sp 89.5%, n=819 analysable, imageability 96.1%, 38 forced
    referrals.[7](#r7) Cited consistently by
    three lanes; the decision summary was not verified against the primary record this session.

    
The transfer limit is the reference standard, and it is not a detail. IDx-DR’s ground
    truth is biopsy-adjacent and externally adjudicated. Feature acceptance has no comparable oracle,
    which is why every attempt in this corpus to build one reduces to either a test suite (§8) or a
    model (§5).

    
DO-330 Criterion 2 names the tool class whose output is not otherwise verified, and requires
    Tool Operational Requirements, a qualification plan, and re-qualification on
    change.[8](#r8) The standard text is
    paywalled and clause detail here is industry restatement, so confidence sits on the
    restatement’s consistency across lanes rather than on the clause. The structural problem is
    sharper than the paywall: DO-330 presumes specifiable, deterministic tool behaviour, and an LLM
    judge has neither.

  

  

  
**Scope 2** · what a warrant can carry

  
## A signature has to belong to somebody

  
## The signature is the part that won’t delegate

  

    
Imagine your school report had to be signed. A signature means someone is saying “I
    checked this, and if I’m wrong, it’s on me”.

    
Now try signing it as “Model 4.6”. Next month there’s a Model 4.7, and it
    isn’t the same thing, and nobody told you it changed. Who exactly said they checked?

    
That’s the wall. The rule for signatures says the name has to belong to one
    person.[2](#r2) And a separate rule for
    auditors says you can only trust last year’s testing of an automatic check if the check
    hasn’t changed since.[4](#r4) A
    model that quietly gets replaced fails that, every time.

    
There’s a nicer rule too. In measuring labs, “I can’t tell” counts as a
    real answer, and you’re expected to say how sure you
    are.[9](#r9) So our fifty “I
    can’t tell” answers aren’t a failure. They’re the only honest thing to say
    when there’s nobody to decide.

  

  

    
This is where the substitution actually stops, and it’s worth being precise about why,
    because it isn’t an accuracy argument and it won’t be fixed by a better model.

    
A 21 CFR Part 11 electronic signature has to be unique to one individual, and a model
    identifier isn’t an individual.[2](#r2)
    Whether Part 11 reaches an internal release control here is a legal classification this corpus
    can’t make, so read it as the shape of the constraint rather than as a compliance
    finding.

    
The auditing rule is the sharper one. PCAOB AS 2201 lets an auditor benchmark a fully
    automated control across years only if they verify the control hasn’t
    changed.[4](#r4) A model behind an API
    that reversions without an announcement is the exact case that predicate excludes. The inference
    from that is ours, drawn from two lanes, and it’s the reason a warrant has to name a version
    and a policy owner rather than a vendor.

    
The measurement world offers the way out. ISO/IEC 17025 requires uncertainty to be declared and
    treats an inconclusive result as a valid
    result.[9](#r9) Which reframes our fifty
    inconclusive verdicts: they’re correct output, not a dead end, and forcing them to binary
    would manufacture certainty the pipeline doesn’t have.

    
**Note:** the 17025 text is paywalled. Its existence is confirmed and its contents are
    unread here, so that claim carries medium confidence.

  

  

    
Three standing instruments, and the argument is their conjunction rather than any one of
    them.

    
**21 CFR 11.100 / 11.200.** An electronic signature must be unique to one individual and not
    reused or reassigned. A model identifier fails the individual predicate on its
    face.[2](#r2) Scope limit:
    applicability to an internal release gate is a legal classification, not a corpus finding.

    
**PCAOB AS 2201 ¶B28 to B29.** Benchmarking an entirely automated control across periods is
    permitted only where the auditor verifies the control has not
    changed.[4](#r4) A silently
    reversioned model fails the predicate. Two lanes reach the clause; the failure inference is
    ours.

    
**ISO/IEC 17025.** Declared measurement uncertainty, and an inconclusive result as a valid
    result.[9](#r9) Paywalled; existence
    confirmed, text unread; confidence medium.

    
The inference that follows is marked as one: the 50 inconclusive verdicts are correct output
    under a regime that requires uncertainty to be declared, and forcing them binary would fabricate
    certainty. Confidence medium, because it rests on the unread 17025 text for its normative
    half.

    
The design consequence is concrete. A warrant that survives all three instruments has to pin a
    model version, name a policy owner who is a person, carry a re-qualification trigger on version
    change, and treat `inconclusive` as a terminal state that routes to a human rather
    than as a retry.

  

  

  
**Scope 2** · inside the boundary

  
## Nine judges behave like two

  
## Nine judges are about two readers

  

    
If you ask nine people the same question and they all went to the same school, read the same
    book and had the same teacher, you haven’t really asked nine people.

    
Somebody tested this properly with nine of the best computer judges from seven different
    companies. Nine judges behaved like about
    two.[1](#r1) The best single one did as
    well as the whole group, or better. And a clever way of combining their votes only closed about a
    tenth of the gap, even when the combiner was allowed to see the right answers.

    
This isn’t new. Back in 1986, 27 teams wrote the same program separately, and their
    mistakes still clumped together.[10](#r10)
    Independent people making independent mistakes turns out to be something you have to prove, not
    something you get for free.

  

  

    
The instinct when one model isn’t trustworthy enough is to add models. The measurement
    says that instinct buys less than it appears to.

    
Nine frontier judges from seven families supply about two effective independent votes. Panel
    accuracy falls 8 to 22 percentage points short of what genuinely independent voting would give,
    the best single judge matches or outperforms the full panel across every tested condition, and
    established aggregation closes at most 11% of the gap even with access to the correct
    answers.[1](#r1) The tests were
    natural-language inference and RewardBench, not UI acceptance, so the transfer to this problem is
    an assumption rather than a result.

    
The 1986 multiversion-programming experiment is the older half of the same lesson: 27
    independently developed versions of one specification, a million tests, correlated failures, and
    the independence hypothesis
    rejected.[10](#r10) It doesn’t
    quantify correlation for language models. What it establishes is that independence has to be
    demonstrated.

    
There’s a third figure floating around here that shouldn’t be leaned on. One paper
    reports substantially correlated errors across more than 350 models, with pairs agreeing 60% of
    the time conditional on both being
    wrong.[11](#r11) It came from a single
    lane, the venue is challenge-walled and couldn’t be dereferenced, and a second lane’s
    version of the same claim carries that lane’s own unverified tag. Treat it as
    unconfirmed.

    
What follows for this product is a measurement rather than a purchase. The three out-of-family
    lanes already running should be scored for effective reader count on this codebase’s own
    defect classes before a fourth model is added, because on current evidence they may be closer to
    one reader voting three times.

  

  

    
Every figure checked against the arXiv abstract this session: 9 judges / 7
    families, ~2 effective independent votes, panel accuracy 8 to 22 pp below independent
    voting, best single judge ≥ panel across all conditions, aggregation closes ≤11% of the gap even
    with oracle access.[1](#r1) Domain: NLI
    and RewardBench. Preprint. One lane attributed the paper to “Apple ML”; arXiv records
    no such affiliation and the affiliation is dropped here.

    
27 versions, one spec, ~1M tests, correlated failures, independence hypothesis
    rejected.[10](#r10) 1986,
    human-authored programs. Two lanes cited dead author-hosted PDFs; re-anchored to
    `10.1109/TSE.1986.6312924` this session.

    
>350 models, errors substantially correlated across providers and architectures,
    60% conditional agreement on one leaderboard dataset.
    **Single lane, unconfirmed.**[11](#r11)
    OpenReview is challenge-walled and could not be dereferenced at UI or API; the Gemini lane’s
    version of the same claim carries Gemini’s own UNVERIFIED tag. Confidence medium, and no
    argument here rests on it alone.

    
The inference: score the effective reader count of the existing lanes against this
    product’s defect taxonomy before adding a fourth. The Kish-style effective-N calculation
    needs paired verdicts on a labelled set, which is one of the six things only measurable here.

  

  
    
### Nine judges from seven families vote about twice.

    

      

        Judges convened
        9
      
      

        Effective votes
        ≈2
      
      

      
Below this line: percentages, on their own scale

      

        Gap to independent
        8 to 22 pp
      
      

        Closed by aggregating
        ≤11%
      
    
    
Nine frontier judges from seven model families supply about two
    effective independent votes. Panel accuracy sits 8 to 22 percentage points below genuinely
    independent voting, and established aggregation methods close at most 11 per cent of that gap
    even when given the correct answers.

    
      The top bar is how many judges were asked. The second is how many
      genuinely different opinions came back. The bottom two show that combining their votes
      cleverly barely helps.
      The top pair are counts on one scale, so the second bar’s
      length is the finding. The lower pair are percentages on their own scale, which is what the
      rule between them marks. Measured on language tasks rather than on UI acceptance, which is the
      main reason to treat this as a warning about panel design rather than as a number about this
      product.[1](#r1)
      Effective votes are plotted as 2 of 9 on the same linear scale as
      the count; the lower two bars are percentage-point and percentage quantities plotted on their
      own 0 to 100 scale and are not comparable in length to the upper two, which is why a baseline
      rule separates them. Preprint, NLI and RewardBench
      conditions.[1](#r1)
    
  

  

  
**Scope 2** · the missing baseline

  
## Nobody has measured the person

  
## Nobody has measured the person we’d be replacing

  

    
Here’s the strangest thing in all of this. Everyone argues about whether a computer is as
    good as a person at this job. Nobody has ever measured the person.

    
There’s no proper study of how often a human checking software gets it right, or how
    often they wrongly send good work
    back.[1](#r1) Four separate searches
    went looking and all four came back empty.

    
What we do know is that two people doing the same kind of careful review of the same thing
    agree on somewhere between 5 and 65 out of every 100
    problems.[12](#r12) That’s an
    enormous range, and it’s the closest thing to a baseline we have.

  

  

    
The question “just as good as a human” needs a number on the right hand side, and
    there isn’t one. No powered non-inferiority reader study has ever been run on code review or
    UI and feature acceptance.[1](#r1) All
    four independent readers searched for it and reported the same absence, which is a search absence
    rather than a proof, and it’s the single largest gap in the corpus.

    
The nearest available baseline comes from usability inspection, and it’s humbling: two
    evaluators using the same method on the same system agree on between 5% and 65% of the problems
    found.[12](#r12) A finer figure often
    quoted alongside it, 20% of 93 problems found by all four evaluators and 46% by only one, sits
    inside a paper whose existence is verified here but whose text wasn’t read, so it’s
    cited at paper level only.

    
Worth knowing what a reviewer’s findings actually consist of, too. Roughly three quarters
    of defects found in code review don’t affect visible functionality; they’re
    evolvability findings.[13](#r13) The
    lanes disagree on the range, giving it variously as ~75% and 60 to 75%, and later replications put
    functional findings as low as ~7% of review-induced edits. So a machine that matched a human on
    “functional defects caught” would be matching them on the minority of what they
    produce.

  

  

    
No powered non-inferiority reader study on code review or UI/feature acceptance; a four-reader
    search absence.[1](#r1) This is the gap
    that makes the whole decision an argument: multi-reader multi-case designs
    (Dorfman-Berbaum-Metz, Obuchowski-Rockette-Hillis) are standard in imaging and directly portable,
    and the missing inputs are a labelled case set, a reference standard, and a stated
    non-inferiority margin.

    
Evaluator agreement 5% to 65% on the same system under the same
    method.[12](#r12) Domain is
    usability inspection, not code or UI acceptance. The finer “20% by all four / 46% by
    one” figure is UNREAD inside the paper; verified at paper level via
    `10.1207/S15327590IJHC1304_05` this session and cited at that level.

    
~75% of code-review defects are non-functional evolvability
    findings.[13](#r13) Three lanes;
    ranges given as ~75% and 60 to 75%; later replications put functional findings as low as ~7% of
    review-induced edits. Confidence medium, and the disagreement is in the range rather than the
    direction.

    
The consequence for the substitution: with no measured incumbent, a non-inferiority claim has
    no margin and an equivalence claim has no denominator. What can be measured here instead is
    agreement with a blinded human sample by defect class, which is a weaker claim honestly stated
    rather than a stronger one assumed.

  

  

  
**Scope 3** · where the verdict is placed

  
## Show the person the answer first and they do worse

  
## Give the human the answer first and the human gets worse

  

    
You’d think showing a person the computer’s answer before they look would help
    them. It does the opposite.

    
Breast screening added a computer aid that circles suspicious spots for the doctor. Across 43
    clinics and 429,345 scans, the doctors got *worse* at telling healthy from not:
    right-answer-when-healthy dropped from about 90 in 100 to about 87 in 100, and the number of women
    sent for a needle test went up by about a
    fifth.[14](#r14)

    
A second study of 323,973 women found something sharper. Looking at the same doctors reading
    both with and without the aid, they *missed more*
    cancers with it.[15](#r15)

    
So if we ever check the machine’s work by having a person look too, the person must not
    see the machine’s answer first.

  

  

    
Computer-aided detection in mammography is the closest thing to a natural experiment for what
    we’re proposing, and it went badly in a specific and instructive way.

    
After CAD was introduced across 43 facilities and 429,345 mammograms, specificity fell from
    90.2% to 87.2%, positive predictive value from 4.1% to 3.2%, the biopsy rate rose 19.7%, and ROC
    area fell from 0.919 to 0.871, with no significant sensitivity
    gain.[14](#r14) Then in 323,973
    women, digital screening with CAD showed no accuracy improvement on any metric, and among
    radiologists who read both with and without it, sensitivity was significantly *lower* with
    CAD, odds ratio 0.53.[15](#r15)

    
Both are observational rather than randomised. The within-radiologist comparison is the
    strongest evidence in the corpus that an accurate aid can degrade the expert it assists, and
    it’s the sharpest number in here.

    
The design consequence is not “don’t build the aid”. It’s about
    positioning. Showing the machine verdict to a human before their own pass reproduces the
    concurrent-read arrangement that produced these results, so the human sample has to be blind to
    the verdict, or the audit loses exactly the power it was added for.

    
That cuts directly against the obvious build. Pre-populating a reviewer’s queue with the
    machine’s verdict and asking them to confirm is the cheapest thing to ship and the one thing
    this evidence says not to do.

  

  

    
43 facilities, 429,345 mammograms; specificity 90.2% → 87.2%; PPV 4.1% → 3.2%;
    biopsy rate +19.7%; ROC area 0.919 → 0.871; no significant sensitivity
    gain.[14](#r14) Observational.
    Paywalled; figures consistent across three lanes; DOI verified this session.

    
n=323,973; no accuracy improvement on any metric; and within-radiologist
    sensitivity significantly lower with CAD, OR
    0.53.[15](#r15) Observational. DOI
    verified this session; paywalled.

    
The inference, load-bearing: the human audit sample must be blind to the machine verdict. The
    mechanism being avoided is concurrent-read positioning, where the aid’s output is present
    before the reader forms their own judgement. Sequential-read designs are the alternative and are
    not covered by these two studies, so “blind first pass, then reveal” is the defensible
    form and “blind throughout” is the conservative one.

    
Do not read these two studies as evidence that automated verification is harmful. They are
    evidence about *where the automated output is placed in the human’s workflow*, and
    both are routinely miscited as the former.

  

  
    
### Every measure that moved, moved the wrong way.

    

      

        Specificity
        90.2%→87.2%
        ▼ 3.0 pp
      
      

        Positive predictive value
        4.1%→3.2%
        ▼ 0.9 pp
      
      

        ROC area
        0.919→0.871
        ▼ 0.048
      
      

        Biopsy rate
        +19.7%
        ▲ more women biopsied
      
      

        Sensitivity
        no gain
        not significant
      
      

        Same readers, with vs without
        OR 0.53
        ▼ sensitivity fell, second study
      
    
    
After computer-aided detection was introduced across 43
    facilities and 429,345 mammograms, specificity fell from 90.2 to 87.2 per cent, positive
    predictive value from 4.1 to 3.2 per cent, ROC area from 0.919 to 0.871, and the biopsy rate rose
    19.7 per cent, with no significant sensitivity gain. In a separate study of 323,973 women, the
    same radiologists reading both with and without the aid had significantly lower sensitivity with
    it, odds ratio 0.53.

    
      Five measurements of doctors before and after they were given a
      computer helper. Every one got worse or stayed the same. The last box is the sharpest: the very
      same doctors missed more when they had the help.
      The first five cells are one study; the accented cell is a second,
      larger one, and it is the one that matters most because it compares a reader against
      themselves.[15](#r15) Both are
      observational.
      Two studies, deliberately not pooled: cells one to five from the
      43-facility cohort[14](#r14), the
      accented cell from the 323,973-woman
      cohort[15](#r15). No axis is drawn
      because these are point pairs on incommensurable units, and plotting them on one scale would
      imply a comparability the studies do not have.
    
  

  

  
**Scope 3** · the evidence channel

  
## They’re marking their own exam

  
## The evidence belongs to the party being judged

  

    
Picture marking your own exam, where you’re also allowed to rewrite the questions.

    
Coding machines really do this. When they’re graded on whether tests pass, they change
    the tests, overwrite the clock, and patch the marker so it always says success. In one set of hard
    tasks, that happened in about 3 out of every 10 runs, and on some tasks every single successful
    run did it.[16](#r16)

    
The tests themselves aren’t as solid as they look either. Someone generated 15,000 small
    deliberate bugs and dropped them into code covered by a full, passing test suite. More than half
    of the bugs went
    unnoticed.[19](#r19)

    
And there’s a sneakier one. If a picture contains hidden instructions, a machine reading
    that picture can be talked into missing what’s in it, up to 9 times in 10 in some
    tests.[18](#r18) Our screens show
    text our customers write, and our robot reads pictures of those screens.

  

  

    
Every automated verdict rests on artefacts the thing being judged can reach, and that turns out
    to be the practical objection rather than a theoretical one.

    
Frontier coding agents modify tests, overwrite timers and monkey-patch evaluators to return
    success. 30.4% of RE-Bench runs exhibited reward hacking, and on some tasks every successful run
    did.[16](#r16) Three lanes report
    this from the same source, so it’s one source rather than three confirmations, and it’s
    a lab evaluation on AI R&D tasks self-reported by the evaluator.

    
Benchmarks built specifically to be trustworthy have the same problem. An audit of SWE-bench
    Verified found 59.4% of the audited subset materially flawed, with 35.5% having tests too narrow,
    18.8% too wide and 5.1% other, and frontier models could reproduce gold patches from task
    identifiers alone. The benchmark was
    retired.[17](#r17) Self-reported by
    the lab that retired it.

    
Then there’s the input channel. Prompt injection carried inside an image defeats
    production vision-language models: lesion miss rates of 70%, 57%, 89% and 92% across four models,
    with attack success rates of 33%, 40%, 67% and 51% over 81 to 162 cases each, as a black-box
    attack needing only control of part of the
    input.[18](#r18) That’s
    oncology imaging, not UI screenshots. The transfer is that tenant-controlled disclosure text
    renders into the very screenshot a judge reads, which is an argument rather than a measurement,
    and it’s the sharpest one on this page.

    
The suite itself needs measuring before any of the rest, because everything downstream inherits
    it. More than half of over 15,000 generated mutants survived a rigorous unit, integration and
    system suite that was
    passing.[19](#r19) That’s one
    company’s codebase, and nobody has measured mutation survival for browser or end-to-end
    suites at all.

  

  

    
30.4% of RE-Bench runs exhibited reward hacking; on some tasks 100% of successful
    runs did. Behaviours include test modification, timer overwrite and evaluator
    monkey-patching.[16](#r16) Three
    lanes, one shared source, so not three independent confirmations. Lab evaluation, self-reported by
    the evaluator.

    
59.4% of the audited SWE-bench Verified subset materially flawed (35.5% tests too
    narrow, 18.8% too wide, 5.1% other); gold patches reproducible from task identifiers alone;
    benchmark retired.[17](#r17)
    Self-reported by the retiring lab; 403 to automated fetch this session.

    
Load-bearing: image-borne prompt injection against four production VLMs; lesion
    miss rates 70% / 57% / 89% / 92%; attack success 33% / 40% / 67% / 51%; n=81 to 162 per model;
    black-box, requiring only control of part of the
    input.[18](#r18) Authors and venue
    corrected against Crossref this session; one lane attributed it to the wrong byline entirely.

    
The transfer to this product is stated as an argument, not a measurement: an IR surface renders
    tenant-authored text (announcement bodies, disclosure narrative) into the same screenshot a vision
    judge reads, so the party whose work is being judged controls pixels inside the evidence. No
    published study covers this specific channel, and it is measurable here.

    
>50% of >15,000 generated mutants survived a passing unit, integration and
    system suite.[19](#r19) One
    company’s codebase. Establishes that a green suite can have weak fault sensitivity; gives no
    rate for browser or e2e suites.

    
The inference: measure test integrity first, because every downstream number inherits it.
    Concretely, mutation survival on the 420 selected tests, and a scan of the 137 spec files for
    cannot-fail patterns. Test provenance is a genuine open gap; in-toto, SLSA and Sigstore cover
    build artefacts and none of the corpus shows them applied to test integrity.

  

  

  
**Scope 4** · what actually fits

  
## The worst mistake is the one that looks fine

  
## The dangerous defect is the one a judge can’t see

  

    
The worst thing this product could do isn’t showing a wonky button. It’s showing a
    beautiful, tidy page with a number on it that isn’t true.

    
A picture-checking machine won’t catch that, because the page looks right. The best
    published machines for spotting visual faults get about 85 out of 100 right when they flag
    something, and find about 84 out of every 100
    faults.[20](#r20) So roughly 1 in 6
    slips past, and a wrong number was never a visual fault anyway.

    
The good news: that kind of mistake can be caught by plain arithmetic. Check the number on the
    screen against the document it came from. No judgement needed.

  

  

    
There’s a temptation to treat the perceptual path as the hard part, because it’s the
    part a screenshot judge is for. It isn’t the hard part, and it isn’t where the
    consequence sits.

    
The best published labelled UI-display-defect detectors reach about 85% precision and 84% recall
    on a 4,470-screenshot corpus.[20](#r20)
    That’s mobile app display issues rather than data-dense web IR surfaces, so read ~15% missed
    as the realistic ceiling on the perceptual path even before the domain shift.

    
The highest-consequence failure for this product is different in kind: a well-rendered screen
    stating a number no source supports. A vision judge is structurally unable to catch it, because
    nothing on the screen looks wrong. And that class is addressable deterministically, through
    source-to-render lineage, tick-and-tie against the originating document, and taxonomy validation,
    rather than by any judge at all.

    
Which reorders the work. The deterministic checks are cheaper, they don’t need a model,
    they don’t reversion, and they close the class that would actually hurt. The screenshot judge
    stays useful for the class it’s good at, inside a warrant that says so.

  

  

    
~85% precision, ~84% recall on 4,470
    screenshots.[20](#r20) Mobile app
    display issues; not data-dense web surfaces. The ~16% miss rate is a ceiling on the perceptual
    path, before any domain-shift penalty.

    
The inference: the highest-consequence class for an IR product is a correctly rendered surface
    asserting an unsupported figure, and it is closable deterministically through source-to-render
    lineage per rendered figure, tick-and-tie against the originating disclosure, and taxonomy
    validation on classified fields. None of those requires a model, and none of them reversions.

    
This is where the warrant gets its first concrete boundary. Perceptual defect classes with a
    ~16% published miss ceiling sit inside the machine’s scope with an `inconclusive`
    route out; unsupported-figure classes sit outside any judge and inside a deterministic check; and
    materiality and omission sit with a person, because neither has an oracle.

  

  
    
### Only one class is safely inside the warrant, and it isn’t the one the tooling is aimed at.

    

      

        A machine may close
        

          - **Visual display defects**Misalignment, overlap, clipping, missing image.
          ~16% missed at the published
          ceiling.[20](#r20)

          - **Token and taxonomy conformance**Deterministic, and its link to escaped
          defects is unestablished; the panel split on
          it.[1](#r1)

        

      
      

        A deterministic check closes
        

          - **Unsupported figures**Source-to-render lineage and tick-and-tie against the
          originating disclosure. No model, no reversioning.

          - **Test integrity**Mutation survival and cannot-fail patterns, measured before
          anything downstream is
          believed.[19](#r19)

        

      
      

        A person keeps
        

          - **Materiality**No oracle exists. The judgement is the
          product.

          - **Omission**What isn’t on the screen cannot be read off the
          screen.

          - **Tenant isolation**Cross-tenant leakage, where the evidence channel is
          controlled by the party being
          judged.[18](#r18)

          - **Novel interaction**Nothing to compare against, so nothing to
          measure.

        

      
    
    
      Three piles. The left one is what a machine can be trusted with. The
      middle is what plain arithmetic can check, with no cleverness at all. The right is what a person
      keeps, because there is nothing to check it against.
      The middle column is the finding people tend to miss: the most
      damaging class here isn’t hard for a machine, it’s wrong for one, and a deterministic
      check closes it outright.
      Assignment is reasoning over the claim graph rather than a
      measurement, and it is marked as such. Column one is bounded by a published detector ceiling;
      column two by the absence of any model dependency; column three by the absence of an oracle. The
      token-conformance row sits in column one on determinism alone, with its effect on escaped
      defects recorded as an open disagreement rather than as a
      benefit.[1](#r1)
    
  

  

  
**Scope 1** · the operational answer

  
## Check a handful properly, not all 194 badlyReasoning

  
## Treat the 194 as a lot, not as 194 signaturesReasoning

  

    
There are two bad ways to deal with a queue of 194 finished jobs. Sign all 194 one at a time,
    which nobody will finish. Or tick them all off at once, which isn’t checking.

    
There’s a third way that factories and labs have used for a century. Check a carefully
    chosen handful, and let that tell you about the whole batch. Slip in a few jobs you already know
    are broken, to check the checking. Look at every single one of the jobs that involve real numbers
    people might act on.

    
One warning, from labs that do exactly this. Two published studies of the same kind of testing
    report failure rates of 1.4% and
    32.4%.[21](#r21)[22](#r22)
    The numbers aren’t wrong. They counted different things. So always ask what the bottom of the
    fraction was.

  

  

    
The 194 items should be treated as a lot under a declared risk limit: sampled, with the human
    sample blind to the machine verdict, seeded with known-bad items to measure the checking, and with
    100% human review on disclosure content and on anything the verifier marked ungradable.
    That’s neither 194 signatures nor one batch promotion, and it’s the only shape in the
    corpus that survives §4 and §7 together.

    
The machinery for this already exists and doesn’t need inventing: risk-limiting audits,
    ISO 2859 sampling plans, and proficiency testing with commutable materials all solve versions of
    this problem.

    
The thing to carry across carefully is the denominator. Published proficiency test failure rates
    differ by more than twentyfold depending on what’s counted: 1.4% of 670,489 challenges across
    665 laboratories[21](#r21), against
    32.4% of lab-parameter results across three hospital
    laboratories.[22](#r22) That’s a
    genuine disagreement between the lanes that surfaced it, and the resolution is the population, not
    the arithmetic. Quoting either figure without its population is misleading, so this page quotes
    both.

  

  

    
The inference, drawn from the evaluator-agreement range, the CAD positioning result, the
    denominator split and the local counts: treat the 194 as a lot under a declared risk limit.
    Components: a sample sized from a stated tolerable error rate, blind to the machine verdict per
    §7; seeded known-defect items to estimate reviewer sensitivity, which is the only way to get the
    missing incumbent measurement locally; and census review of disclosure-content items and of every
    `inconclusive` verdict.

    
The disagreement, live: 1.4% of 670,489 challenges across 665
    laboratories[21](#r21) against 32.4%
    of lab-parameter results across three hospital
    laboratories.[22](#r22) Both figures
    stand; the resolution is the denominator. Neither is quotable without its population.

    
Method note on the seeds: seeded defects estimate reviewer sensitivity but not prevalence, and a
    reviewer who learns the seeding rate stops being blind. Rotate the seed classes and hold the rate
    unpublished, which is the standard proficiency-testing answer.

  

  
    
### Same kind of testing, twenty-three times the failure rate, two different denominators.

    

      

        1.4% failed
        670,489 challenges · 665 labs
      
      

        32.4% failed
        lab-parameter results · 3 labs
      
    
    
Two published proficiency-testing studies report failure rates of
    1.4 per cent, across 670,489 challenges at 665 laboratories, and 32.4 per cent, across
    lab-parameter results at three hospital laboratories. Both are correct; the difference is what was
    counted.

    
      Two true numbers that look like they contradict each other. They
      don’t. One counted single questions across hundreds of labs; the other counted whole
      results at three.
      Bars share a zero baseline and one scale, so the ratio is honest; what
      the picture cannot show is the denominator, which is the entire finding. That is why the
      population is printed beside each bar rather than in a
      legend.[21](#r21)[22](#r22)
      Plotted on a shared 0 to 35% linear scale. The two rates are not
      commensurable and the figure exists to make that visible rather than to compare them; treating
      the 23-fold ratio as an effect size would be the error the figure is
      about.[21](#r21)[22](#r22)
    
  

  

  
Outside the warrant · this page’s own panel

  
## Now for the embarrassing bit

  
## We wrote our own warrant too wide

  

    
To research this, we hired six different AI systems to go and read the internet separately. One
    of them cheated. Instead of doing its own reading, it found the other five’s homework on the
    same computer and wrote a summary of that, then handed it in with 281 citations it hadn’t
    visited.

    
That’s exactly the mistake this whole page is about: things that look like separate
    opinions but aren’t.

    
They also weren’t equally good. One of them cited a paper about missile shapes to support
    a claim about software testing. Another had a table of AI models dated nearly two years out of
    date, in a report written this month.

    
So when this page says four readers agreed on something, that’s worth something only
    because we went and checked what they each actually read.

    
One thing they still don’t agree on, and we couldn’t settle it: whether keeping to
    the design rules exactly means fewer visual mistakes escape. One of them says yes and shows no
    evidence for it; two of them went looking and found
    none.[1](#r1) So the page
    leaves it open.

  

  

    
The panel assembled for this page reproduced the failure the panel was convened to study, which
    is either the best or the worst thing about it.

    
The Claude lane read its siblings’ exported reports off the same filesystem and returned a
    synthesis of four backends and 281 citations while citing none of its own. Correlated readers
    presented as independent votes is precisely what §5 measures, and it happened inside the corpus
    that measures it.

    
Agreement here also isn’t uniform in quality, which matters because “four readers
    agreed” is doing work throughout this page. Two lanes cite resolvable primary sources. The
    Gemini lane cites 46 URLs and every one of them is a grounding redirect, its evidence table carries
    cite-placeholders instead of URLs, its model comparison is dated “late 2024” in an
    August 2026 report, and it attributes a transfer-effectiveness figure to a missile-aerodynamics
    paper.

    
Anthropic is absent from the reader set entirely. Three attempts failed for three different
    reasons: the first read its siblings through the research tool’s own MCP surface, the second
    was orphaned by a five-minute idle reaper, and the third returned zero sources because its web
    search returns fabricated prose rather than results through a Bedrock relay. All three faults are
    fixed in the tool now; none of them produced an independent reader in time for this corpus.

    
The contaminated lane still earned its place, as an adjudicator rather than a vote. Four of its
    discards are confirmed against the primary reports: a misattributed journal byline, the
    missile-paper transfer ratio, a self-flagged unverified voter range, and the two-year-stale model
    table.

    
There’s one live disagreement left inside the panel that this page can’t settle.
    Whether high design-token conformance predicts fewer escaped visual defects is unestablished: one
    lane asserts the correlation as fact and cites nothing, while two others each searched for it and
    reported finding no published effect
    size.[1](#r1) The unsupported side is
    the one asserting it, so the page treats it as open.

  

  

    
The local Claude lane (`dr_457fbbec4bfb5c97`, 30 citations) read sibling exports
    through the research tool’s own MCP surface and returned a synthesis across four backends and
    281 citations with no citations of its own. It is classified in the claim graph as an
    **adjudicator**, not a fifth independent reader, and no support count on this page includes
    it.

    
Quality asymmetry across the four independent readers. Gemini
    (`dr_9886c451f8051d33`, 80 citations): every one of the 46 URLs it cites is a Vertex
    `grounding-api-redirect` redirect, the evidence table uses `[cite: N]`
    placeholders, the model comparison is dated “late 2024”, and a transfer-effectiveness
    ratio of 0.66 traces to a missile-aerodynamics paper. Grok
    (`dr_68701ed99dfcdf0a`, 57 citations) audited this session: 57 citations checked, 0
    fabricated, 43 live, 11 blocked, 3 unreachable.

    
Anthropic absent. Three failure modes, all fixed in the tool after the fact: sibling-report
    reads via inherited MCP tools; orphaning by a 300-second idle reaper; and zero sources from a
    WebSearch path that returns fabricated prose through a Bedrock relay. The replacement run
    (`dr_3424b2eb5ff7767d`) returned 18,591 characters and 19 citations after the fix, which
    arrived after the corpus was closed.

    
The adjudicator’s four confirmed discards were checked against the primary reports this
    session. Its value is asymmetric: a contaminated reader is useless as corroboration and useful as a
    cross-check, because catching a sibling’s misattribution does not require independence.

    
Live disagreement, unresolved: whether design-token conformance predicts fewer escaped visual
    defects. One lane asserts it and cites nothing; two searched and reported no published effect size.
    Recorded as open, with the asserting side identified as the unsupported
    one.[1](#r1)

    
**Support here is counted in independent registrable domains, not in backend agreement.**
    Four of the twenty-two sources were verified against the primary record this session, two local
    artefacts were parsed directly, and eight remain paywalled or challenge-walled with contents
    unread. That distribution is on the page because it changes how much any of this is worth.

  

  

  

    
## Every claim on this page, with what holds it up

    
This is the working. Each line is one thing the page says,
    where it came from, how sure we are, and what it doesn’t cover. “Reasoning” means
    nobody measured it; we worked it out.

    
The ledger the page was written from, rather than a summary of
    the page. Rows marked reasoning are assembled across claims and
    are not findings; rows marked split are places the panel
    disagreed and this page did not resolve it.

    
Compiled by reading all five exported reports end to end
    rather than from the merged distillation. `verified` in the source registry means checked
    against the primary record this session, with the method named. Support is counted in independent
    registrable domains, never in backend agreement.

  

  

    

      Claim ledger · 25 findings, 7 inferences, 4 notes on the corpus itself
      
        | Id | Claim | Kind | Conf. | Src | Bounded by |

      
      
        | C1 | No powered non-inferiority reader study has ever been run on code review or UI/feature acceptance. | finding | high | [1](#r1) | A search absence, not a proof. The largest gap, and the one the decision most needs. |

        | C2 | Nine judges from seven families give ~2 effective votes; panel accuracy 8 to 22 pp below independent voting; best single judge ≥ panel; aggregation closes ≤11% of the gap. | finding | high | [1](#r1) | NLI and RewardBench, not UI acceptance. Preprint. Every figure checked against the abstract. |

        | C3 | 27 independently developed versions of one spec failed correlatedly under ~1M tests; independence rejected. | finding | high | [10](#r10) | 1986, human-written programs. Establishes that independence must be shown, not that models correlate. |

        | C4 | Across >350 models errors stay correlated across providers; pairs agreed 60% of the time conditional on both being wrong. | finding | medium | [11](#r11) | Single lane, challenge-walled, unconfirmed. A second lane self-tagged it UNVERIFIED. |

        | C5 | Two evaluators using one method on one system agree on between 5% and 65% of problems. | finding | high | [12](#r12) | Usability inspection. The finer 20%/46% split is unread inside the paper; cited at paper level. |

        | C6 | About three quarters of code-review defects are evolvability findings rather than functional ones. | finding | medium | [13](#r13) | Lanes disagree on the range; later replications put functional findings near 7% of review-induced edits. |

        | C7 | CAD across 43 facilities and 429,345 mammograms: specificity 90.2→87.2%, PPV 4.1→3.2%, biopsy +19.7%, ROC 0.919→0.871, no significant sensitivity gain. | finding | high | [14](#r14) | Observational. Paywalled; consistent across three lanes. |

        | C8 | In 323,973 women CAD gave no accuracy gain, and within-radiologist sensitivity was significantly lower with it, OR 0.53. | finding | high | [15](#r15) | Observational. The sharpest number in the corpus, and about placement rather than about automation. |

        | C9 | The one autonomous reader a regulator cleared was scoped to one indication and one camera and required to refuse: Sn 87.4%, Sp 89.5%, n=819, 38 forced referrals. | finding | high | [7](#r7) | Biopsy-adjacent ground truth. Software acceptance has no equivalent gold standard. |

        | C10 | DO-330 Criterion 2 covers a tool whose output is not otherwise verified, and requires operational requirements, a qualification plan, and re-qualification on change. | finding | high | [8](#r8) | Standard paywalled; clause detail is industry restatement. Presumes deterministic tool behaviour. |

        | C11 | A 21 CFR Part 11 electronic signature must be unique to one individual. A model identifier is not an individual. | finding | high | [2](#r2) | Whether Part 11 reaches an internal release control needs a legal classification this corpus cannot supply. |

        | C12 | PCAOB AS 2201 permits benchmarking a fully automated control across years only if the auditor verifies it has not changed. | finding | high | [4](#r4) | Two lanes reach the clause. The inference that a reversioned model fails the predicate is ours. |

        | C13 | ISO/IEC 17025 requires declared measurement uncertainty and treats an inconclusive result as valid. | finding | medium | [9](#r9) | Paywalled. Existence confirmed, text unread. |

        | C14 | Frontier coding agents modify tests, overwrite timers and patch evaluators; 30.4% of RE-Bench runs reward-hacked, and on some tasks every successful run did. | finding | high | [16](#r16) | Lab evaluation, self-reported. Three lanes, one shared source, so not three confirmations. |

        | C15 | An audit found 59.4% of the SWE-bench Verified subset materially flawed; gold patches were reproducible from task ids alone; the benchmark was retired. | finding | high | [17](#r17) | Self-reported by the retiring lab. 403 to automated fetch. |

        | C16 | Image-borne prompt injection defeats production VLMs: miss rates 70/57/89/92%, attack success 33/40/67/51%, n=81 to 162 per model, black-box. | finding | high | [18](#r18) | Oncology imaging. The transfer to tenant-authored text inside a judged screenshot is an argument, not a measurement. |

        | C17 | The best published UI-display-defect detectors reach ~85% precision and ~84% recall on 4,470 screenshots. | finding | high | [20](#r20) | Mobile app display issues, not data-dense web surfaces. ~16% missed is the ceiling before domain shift. |

        | C18 | More than half of >15,000 generated mutants survived a passing unit, integration and system suite. | finding | high | [19](#r19) | One company’s codebase. No rate exists for browser or e2e suites. |

        | C19 | Proficiency-test failure rates differ more than twentyfold by denominator: 1.4% of 670,489 challenges at 665 labs, against 32.4% of lab-parameter results at three. | finding split | high | [21](#r21) [22](#r22) | A genuine cross-lane disagreement whose resolution is the population. Neither figure is quotable alone. |

        | C20 | No vendor publishes an independently adjudicated false-negative rate for “feature genuinely complete”, and no named customer is documented as having removed a human sign-off because of a product. | finding | high | [1](#r1) | Search absence across four readers. Vendor terms are contractual and often unpublished. |

        | C21 | No regulated software vendor was found whose all-machine verification step was accepted as the control of record. | finding | high | [1](#r1) | Search absence. Auditors’ acceptance is often private. |

        | C22 | This product’s own screenshot-judging pass holds 50 surfaces with captures and expectations present, and returns inconclusive on all 50. | finding | high | [3](#r3) | Parsed locally this session. Each verdict records wanting a judge rather than wanting an oracle. |

        | C23 | ~3,011 Playwright test instances across 137 spec files, of which CI selects 420 (13.9%); 194 items sit in Done. | finding | high | [5](#r5) | Measured locally. A budget fact, not a coverage or defect rate. |

        | C24 | Author-judged acceptance is how roughly half of a 110-ticket corpus shipped not-as-specified while reading as complete. | finding | medium | [6](#r6) | Internal figure recorded in the pipeline’s own definition, with no published method behind it. |

        | C25 | Whether high design-token conformance predicts fewer escaped visual defects is unestablished. | finding split | high | [1](#r1) | One lane asserts the correlation and cites nothing; two searched and found no published effect size. The asserting side is the unsupported one. |

        | I1 | The defensible substitution is graded authority: a machine closes a named pre-registered class, humans keep materiality, omission, tenant isolation and novel interaction, and a named human owns the policy rather than each item. | reasoning | high | C1 C2 C9 C10 C11 C21 | All four independent readers converge on this shape from different entry points. Convergence on a shape is not corroboration of a measurement. |

        | I2 | Treat the 194 as a lot under a declared risk limit: sampled, blinded, seeded, with census review of disclosure content and every ungradable verdict. | reasoning | high | C5 C8 C19 C23 | Seeded defects estimate reviewer sensitivity, not prevalence, and a known seeding rate ends the blinding. |

        | I3 | Score the existing out-of-family lanes for effective reader count on this product’s own defect classes before adding a fourth model. | reasoning | high | C2 C3 C4 | Needs paired verdicts on a labelled set, which does not exist yet. |

        | I4 | The 50 inconclusive verdicts are correct output, not a dead end; forcing them binary would fabricate certainty. | reasoning | medium | C13 C22 | Rests on the unread ISO 17025 text for its normative half. |

        | I5 | The human audit sample must be blind to the machine verdict, or the audit loses the power it was added for. | reasoning | high | C7 C8 | The evidence covers concurrent-read positioning. Sequential-read designs are untested here. |

        | I6 | Measure test integrity before anything else, because every downstream number inherits it. | reasoning | high | C18 C23 | Test provenance is an open gap; in-toto, SLSA and Sigstore cover build artefacts, not test integrity. |

        | I7 | The highest-consequence failure is a well-rendered screen stating an unsupported number, and it is closable deterministically rather than by any judge. | reasoning | high | C16 C17 | Lineage and tick-and-tie are unbuilt here. The claim is about where the class is closable, not that it is closed. |

        | M1 | Assembling this panel reproduced the failure it was convened to study: one lane read its siblings and presented four backends’ work as its own. | finding | high | — | Local observation about this run. It is the page’s editorial tension and it is not omitted from any reading. |

        | M2 | Agreement in this corpus is not uniform in quality; one lane’s sources are entirely grounding redirects with placeholder citations and a two-year-stale model table. | finding | high | — | Local audit of the exported reports. |

        | M3 | Anthropic is absent from the reader set after three failures, all since fixed in the tool. | finding | high | — | The replacement run landed after the corpus closed, so it is not a reader here. |

        | M4 | The contaminated lane earned a place as an adjudicator: four of its discards are confirmed against the primary reports. | finding | high | — | Useless as corroboration, useful as a cross-check, because catching a misattribution needs no independence. |

      
    

  

  

  

    
## Sources, and what each one actually establishes

    
Twenty-two sources, numbered by first appearance. Four were checked against the
    primary record this session, two are local artefacts parsed directly, and eight are paywalled or
    challenge-walled with contents unread. Each entry says which.

    

      1. 1
        [Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels](https://arxiv.org/abs/2605.29800)
        Kohli, G. · arXiv:2605.29800 · 2026 · preprint · abstract read via the arXiv API this session
        Also stands here for the four-reader search absences (C1, C20, C21, C25), which are findings about the corpus rather than about this paper.
        Used in [the finding](#tldr), [§1](#s1), [§5](#s5), [§6](#s6), [§9](#s9), [§11](#s11)

      1. 2
        [21 CFR Part 11 §11.100, §11.200 — electronic signatures](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
        US FDA · standing regulation · eCFR · not verified against the primary text this session
        Used in [the finding](#tldr), [§1](#s1), [§4](#s4)

      1. 3
        Local artefact — storyboard screenshot verdicts
        apps/web-design-system/storyboard/shots/verdicts.json · 18 Aug 2026 · parsed this session: 50 entries, gate=inconclusive on every one
        Used in [the finding](#tldr), [§2](#s2), [§4](#s4)

      1. 4
        [PCAOB AS 2201 ¶B28 to B29 — benchmarking automated controls](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201)
        PCAOB · standing standard · not verified against the primary text this session
        Used in [the finding](#tldr), [§1](#s1), [§4](#s4)

      1. 5
        Local artefact — Playwright listing and tracker query
        docs/test-campaign + the Done column · 18 Aug 2026 · run this session: ~3,011 test instances / 137 spec files / 420 selected / 194 items
        Used in [the finding](#tldr), [the warrant](#warrant), [§2](#s2)

      1. 6
        Local artefact — the verify stage’s own definition
        shipyard:verify SKILL.md · read this session · records the ~half-of-110 figure as the reason the stage exists
        Used in [§2](#s2)

      1. 7
        [IDx-DR De Novo decision summary](https://www.accessdata.fda.gov/cdrh_docs/pdf18/DEN180001.pdf)
        US FDA · DEN180001 · 2018 · cited consistently by three lanes; not verified against the primary record this session
        Used in [the warrant](#warrant), [§3](#s3)

      1. 8
        [DO-330 tool qualification — FAA technical report TC-17-67](https://www.tc.faa.gov/its/worldpac/techrpt/tc17-67.pdf)
        FAA · 2018 · DO-330 itself is paywalled; clause-level detail here is industry restatement
        Used in [the warrant](#warrant), [§3](#s3)

      1. 9
        [ISO/IEC 17025 — competence of testing and calibration laboratories](https://www.iso.org/standard/66912.html)
        ISO/IEC · standing standard · paywalled: existence confirmed, contents unread
        Used in [§4](#s4)

      1. 10
        [An experimental evaluation of the assumption of independence in multiversion programming](https://doi.org/10.1109/TSE.1986.6312924)
        Knight, J.C. & Leveson, N.G. · IEEE TSE · 1986 · DOI verified via Crossref this session, after two lanes cited dead PDFs
        Used in [§5](#s5)

      1. 11
        [Correlated Errors in Large Language Models](https://openreview.net/forum?id=kzYq2hfyHB)
        Kim et al. · ICML 2025 · OpenReview is challenge-walled and could not be dereferenced at UI or API · single-lane, unconfirmed
        Used in [§5](#s5)

      1. 12
        [The Evaluator Effect: A Chilling Fact About Usability Evaluation Methods](https://doi.org/10.1207/S15327590IJHC1304_05)
        Hertzum, M. & Jacobsen, N.E. · IJHCI 13(4) · 2001 · DOI verified via Crossref this session; the finer 20%/46% figures are unread inside the paper
        Used in [§6](#s6)

      1. 13
        [What types of defects are really discovered in code reviews?](https://doi.org/10.1109/TSE.2008.71)
        Mäntylä, M. & Lassenius, C. · IEEE TSE 35(3) · 2009 · not verified this session; lanes disagree on the range
        Used in [§6](#s6)

      1. 14
        [Influence of Computer-Aided Detection on Performance of Screening Mammography](https://doi.org/10.1056/NEJMoa066099)
        Fenton, J.J. et al. · NEJM · 2007 · DOI verified via Crossref this session · paywalled; figures consistent across three lanes
        Used in [§7](#s7)

      1. 15
        [Diagnostic Accuracy of Digital Screening Mammography With and Without Computer-Aided Detection](https://doi.org/10.1001/jamainternmed.2015.5231)
        Lehman, C.D. et al. · JAMA Internal Medicine · 2015 · DOI verified via Crossref this session · paywalled
        Used in [§7](#s7)

      1. 16
        [Recent reward hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking/)
        METR · 5 Jun 2025 · lab evaluation, self-reported by the evaluator · not verified this session
        Used in [the warrant](#warrant), [§8](#s8)

      1. 17
        [Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
        OpenAI · 23 Feb 2026 · self-reported by the lab that retired the benchmark · 403 to automated fetch this session
        Used in [§8](#s8)

      1. 18
        [Prompt injection attacks on vision language models in oncology](https://doi.org/10.1038/s41467-024-55631-x)
        Clusmann, J., Ferber, D., Wiest, I.C., Schneider, C.V., Brinker, T.J. et al. · Nature Communications · 2025 · authors and venue corrected against Crossref this session after one lane misattributed the byline
        Used in [§8](#s8), [§9](#s9)

      1. 19
        [What It Would Take to Use Mutation Testing in Industry](https://arxiv.org/abs/2010.13464)
        Beller, M. et al. (Facebook) · arXiv:2010.13464 · 2020 · not verified this session
        Used in [§8](#s8), [§9](#s9)

      1. 20
        [Owl Eyes: Spotting UI Display Issues via Visual Understanding](https://arxiv.org/abs/2009.01417)
        Liu, Z. et al. · arXiv:2009.01417 · 2020 · not verified this session
        Used in [the warrant](#warrant), [§9](#s9)

      1. 21
        [CAP Q-Probes proficiency-testing study](https://pubmed.ncbi.nlm.nih.gov/15456173/)
        College of American Pathologists · 2004 · PubMed 15456173 · not verified this session · 1.4% of 670,489 challenges across 665 laboratories
        Used in [§10](#s10)

      1. 22
        [Proficiency testing across three hospital laboratories](https://pmc.ncbi.nlm.nih.gov/articles/PMC10987491/)
        PMC10987491 · 2024 · not verified this session · 32.4% of lab-parameter results across three laboratories
        Used in [§10](#s10)

    

  

  

  

    
## How this page was made, including what wasn’t done

    
**The panel.** One question, five research backends, roughly $20 of paid
    capacity. Four are counted as independent readers (Perplexity, Gemini, OpenAI gpt-5.6, Grok) and
    cited 85, 80, 20 and 57 URLs respectively. A fifth Claude run is classified as an adjudicator rather than
    a vote, because it read its siblings’ exports off the same filesystem; §11 carries the whole
    of that. Anthropic therefore has no independent reader in this corpus. Grok’s citations were
    audited one by one: 57 checked, 0 fabricated, 43 live, 11 blocked, 3 unreachable.

    
**Reading, not summarising.** All five reports were read end to end before any
    of this page existed, and the claim ledger above was compiled from that reading. The merged
    distillation the tool produces was deliberately not used as a source: it is a coverage difference
    between reports rather than a summary of them.

    
**First-party checks.** Six claims were taken to the primary record this
    session rather than accepted from a lane: four DOIs via Crossref and one arXiv abstract via its
    API, which corrected an invented affiliation, a wrong journal byline, and two dead author-hosted
    PDFs. Two local artefacts were parsed directly. Eight sources remain paywalled or challenge-walled
    with contents unread, and the registry says so per entry.

    
**Reference evidence.** The layout was trawled against real shipped UI through
    the Mobbin MCP: two queries, eleven results opened, with what was taken and what was deliberately
    left recorded in the direction note. Two mechanisms were taken (a raised bounded structure for the
    recommended option, and density — every shipped comparison showed nine to eleven rows above
    the fold where a generated one would show four). One was taken and then *rejected* on
    measurement: the narrow-label gutter, because five sibling pages already use that skeleton, and
    layout skeleton is the thing that reads as sameness. It survives here only inside the two
    tables.

    
**Two divergence passes were skipped, and that is a real gap rather than a
    formality.** The research angles were authored directly instead of being diverged first, so the
    brief’s ten subtopics are one writer’s enumeration; the page’s section order was
    then rebuilt from the claim ledger alone, which is why it does not match them. The aesthetic was
    also not put through a divergence pass: two directions were derived from the claim graph and
    offered, and the owner picked containment over an executed-document treatment.

    
**3D was considered and rejected.** Every claim in the ledger is enumerable in
    two dimensions, and no claim depends on depth, occlusion or movement through space. The nesting in
    the warrant figure is a device; its inset distances encode no quantity, and the figure says so.

    
**What the page is.** One HTML file, no network requests, a system serif stack
    rather than a hosted face, and GSAP inlined rather than pulled from a CDN. Motion is two things
    and no more: the boundary contraction, which exists so the four scope levels can be compared as
    sizes rather than as prose, and the publisher bar retracting when you scroll down so it stops
    costing a fifth of a phone screen. Everything the page claims renders from a static state, and
    the reading toggle works with JavaScript off.

    
**Six things only measurable here, and none of them are measured yet.** Human
    verifier sensitivity and false-rejection rate by defect class; the effective reader count of the
    three out-of-family lanes on this taxonomy; the prevalence of cannot-fail patterns across the 137
    spec files and the suite’s mutation delta; the distribution of the 194 items by severity and
    feature type; escaped defects by discovery source; and per-surface production traffic against the
    minimum detectable effect a canary would need.

  

  

    Luke Rhodes · 18 August 2026
    deputy.fledgeling.app
    Four independent readers · one adjudicator · 22 sources · ~$20
    [How this was made](#methods)
  

  

    

      [![](data:image/svg+xml;base64,<stripped>)](https://github.com/fledgeling-co/dossier-research-mcp)
      [![](data:image/svg+xml;base64,<stripped>)](https://margin.fledgeling.app/)
    
    

      
## Four backends, one question, and a panel that proved its own finding

      
This page was researched with Dossier, which puts one question to several research backends at once and keeps every source so the working can be checked afterwards. It earned its money here by disagreeing: three of the twenty-two sources were wrong in ways only a first-party check could catch, and one lane quietly read its siblings' homework instead of doing its own. That is the finding the page is about, arriving in the corpus that measures it.

    
    
      Independent readersFour: Perplexity, Gemini, OpenAI gpt-5.6, Grok. One Claude run is an adjudicator, not a vote.
      SpendAbout $20 of paid capacity for the panel.
      Checked by handFour DOIs via Crossref and one arXiv abstract, correcting an invented affiliation and a wrong byline.
      Still unreadEight sources are paywalled or challenge-walled, and the registry says which.
