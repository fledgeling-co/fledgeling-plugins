<!-- The prompt both lanes were given, verbatim, so a re-run is comparable. -->

You are reviewing a mature, evidence-driven UI test-campaign methodology for BLIND SPOTS.
Answer as a testing-research specialist. Be specific and cite real techniques, tools and
papers where you can. Do not restate what is already covered.

CONTEXT — what the methodology already does.

Ten phases: ground in the project; read requirements from PRD/specs/mocks into a
requirement inventory (classes: affordance, behaviour, honesty-guardrail, deferred,
vacuous); build a coverage model over surface x state x viewport x theme x role x locale
x data-shape x modality x execution-plane x oracle with declared t-way sampling;
enumerate surfaces, navigation destinations, per-surface controls, flows and components;
ground selectors against the running app; write cases; run, stabilise and ARM each
assertion (revert the behaviour, watch the case go red, restore); build oracles for cases
nothing could settle; sweep; measure the build against its design of record on structure,
resolved style, vocabulary and quantised geometry; publish an evidence page.

Oracle rungs, weakest first: touch, presence, structural, structural-visual, outcome,
metamorphic, effect-witness, raster-visual, interactive-glass. Only the last five count as
"effect" rungs. A critical flow proved only by presence fails the gate.

Sweeps: A state matrix, B fault injection, C interaction integrity (enumerate and actuate
every control, content-hash change detection, write-refusal firewall), D keyboard + axe,
E data-shape stress, F security surface, G multi-user/realtime, H refusal honesty,
I metamorphic relations, J freshness/provenance, K desktop shell and window invariants,
L live process and IPC chaos, M reality boundary and vacuity (effect census, provider
resolution, blind-mutation grep, specification strengthening).

Mechanised gates already in place: every sweep prints a denominator; a lane claiming the
app was running and drawn must name the built artifact and what witnessed it attaching to
a display server; every published screenshot must name what the capture channel was
pointed at, with a seeded swap test proving the tie-check can fail; a requirement claiming
an effect outside the process must name an independent recorder and a non-zero count;
armed and unarmed passes counted apart; "unchecked is failed" scoring with a ratchet; a
closed-world reconciliation partitioning every brief and registry entity into exactly one
of eight classes with an exit code.

Known measured failures already defended against: covering a subset and reporting it as
the whole; proving a surface rendered and calling it proof the product works; testing the
parts on paper and reporting it as the product on glass; publishing a picture of one thing
under the name of another; verifying a guarantee over a capability that never runs; and
most recently, an application that rendered correctly while six navigation destinations
opened one placeholder view and every button ran an empty closure, under a campaign
reporting 32/32 cases passing and armed.

THE QUESTION.

What classes of user-visible defect would STILL escape this, and what specific method
would catch each? I am most interested in:

1. Defect classes reachable only by driving a real multi-step user journey end to end
   (state accumulated across steps, back/forward and deep-link re-entry, resume after
   interruption, partial-completion recovery, cross-surface data consistency).
2. Where an LLM or vision model genuinely outperforms a deterministic check as a UI
   oracle, and where the published evidence says it does not — with the measured
   false-positive/false-negative rates if you know them.
3. Methods absent from the list above entirely. Consider at least: differential/A-B
   testing against a previous build, record-replay of real user sessions, chaos and
   soak/endurance testing of a UI, concurrency and race detection in a UI, accessibility
   beyond a rule engine, internationalisation and pseudo-localisation, time and timezone
   and clock manipulation, offline/reconnect state machines, permission and capability
   revocation mid-session, memory/leak/perf regression as a correctness signal, telemetry
   and analytics correctness, and anything else you consider a real omission.
4. The single highest-yield thing to add, and why, with its cost.

Rank your findings by expected defect yield per unit of effort. For each, name the
detection mechanism concretely enough to implement. Where you are uncertain or the
evidence is thin, say so rather than asserting.
