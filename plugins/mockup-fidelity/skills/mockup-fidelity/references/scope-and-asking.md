# Scope, asking, and the three hard cases

Read this when honouring the mock is not simply "change the CSS" — when the element exists only as a
picture, when a whole screen needs data that isn't there, or when the mock shows something the target is
not allowed to say.

**Build the visible element; document only the behaviour it can't yet perform.** The most seductive
rationalization is *"this affordance needs a backend the app lacks, so I'll log it as a gap"* — after
which the *visible element itself* never gets built. Split the two. A card, icon, section or control the
mock shows is **always built** and wired to whatever real behaviour already exists. Only the *specific
behaviour that genuinely needs data or a service the app doesn't have* goes in the functional-gaps doc.
**"Needs a backend" is never a reason to omit a visible element; it's a reason to document one behaviour
of it.**

**Building a whole missing SCREEN that needs data — reuse a deployed real endpoint, never a mock.**
Production-code guardrails forbid stubbed content, you usually can't deploy a backend autonomously, and
the app under test points at a deployed backend, so a brand-new endpoint can't be reached to verify the
screen. Reuse an already-deployed real generation/query path with a screen-appropriate request. If reuse
forces an honest framing the mock doesn't show, **use the honest copy and record the richer endpoint as a
backend follow-up** — honest-but-real beats faithful-but-fake every time.

**Guardrail-honest divergence is a *legitimate* intentional class.** Where the mock fabricates specifics
the target's guardrails forbid (a made-up page count, "every figure traced to filings"), the target
*should* diverge to honest copy. Cite the guardrail; don't "fix" the app to reproduce the fabrication.

## Why these three are grouped

Each is a place where the honest move and the easy move diverge, and where the easy move produces a screen
that passes a visual review and fails a user. The first two are the same failure in different sizes: a
thing gets documented instead of built. The third is its mirror — a thing gets built that should not be,
because the mock asked for it.
