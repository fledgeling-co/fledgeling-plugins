# 1.3.0 gate review — grok-4.6 at xhigh

`grok -m grok-4.6 --effort xhigh -p` · 16 Aug 2026 · adversarial review of the gate rewrite.
Prompt: the current gates, the proposed change, the documented 4-0 eval loss, the 93-95% over-asking datum; flaws requested, not agreement.

I'll read the current `clarify` skill, its eval notes, and the composition rules so the verdict is grounded in what it already measures.The 4-0 eval and the linter are the load-bearing evidence; reading those next.The 4-0 loss is the near-synonym eval. I'll pull its prompt and the evidence on option-count so the verdict names the actual missing third.**(d) makes the 4-0 worse. (a)+(b) do not neutralize it.**

The 4-0 was not a missing fact a panel would fetch. The skill already had a Gaps rule; three fixes, including that rule, did not move four families in either A/B order. The loss was compositional: synonym-collapse plus brevity produced a tidy binary (one file vs split) and never reached expand/contract. A hard cap of two writes that collapse into the spec.

The winning baseline had three shapes on one axis *and* a second question with four diagnostic categories. Two slots cannot hold a three-way taxonomy even if a panel names the third. Splitting into two questions pays the interruption the skill exists to avoid; evidence.md already flags that sequential short lists can cost more than one longer one.

“Name the rejected option in the preamble” is the documented invisible-gap failure. A named-but-unclickable third cannot be chosen. If the agent is wrong to reject it — which is what the judges found — the user never learns the set was incomplete.

(a) does not invent taxonomies. The packet is “question + evidence → verdict.” Frame “one file vs split” and the panel answers that frame. (b) then takes the conventional recommendation and never asks. That is a worse 4-0: expand/contract reaches nobody.

**(b) collapses to never-ask, including on both carve-outs.**

The loop is closed: refer until you can recommend; if you can recommend, take it; the panel exists so you become sure. A literal Opus escalates until it has a reason, then treats certainty as a ticket past the user. It can always invent a reason on a taste question (“I’d pick this because the rest of the app does”).

Carve-out (i) loses to recency: (b) is the new terminal gate. Both eval arms already ask before a production drop, so the novel instruction is the one that fires. Carve-out (ii) loses because “can you name a recommendation” is the wrong predicate — you almost always can.

The sentence that prevents it: **Take it without asking only when the axis is yours (craft, convention, reversible). Certainty is not a ticket past their axis or past an unrecoverable action.** Bind “take it” to gate 3, not to confidence.

**The invariant is not clean enough to lint.**

“Mark ⇒ destructive” is the enforceable direction. “Destructive ⇒ mark” is where it breaks: you cannot classify destructive from payload text.

Unseen false-positive class: **user-axis questions that mention a destructive verb as context or as one pole of a risk/scope choice.** “How aggressive should cleanup be — delete the flags this week, or quarantine them?” Keyword `delete` demands a mark; the axis is theirs, so the mark is the bug. Same for `publish` / `send` / `spend` if carve-out (i) includes outward-facing and costly. False negative: “Apply 0007?” with no drop/delete token.

The current gold payloads (offline support, backpressure) are marked and reversible. The invariant would fail them, which is consistent with (b) only if you accept never asking those.

**Refuse as written**

- **(d)** exactly-two. Keep 2–4. Require a third slot when you can name a third distinct shape. Nobody has measured 2 vs 3 vs 4 in this setting; moving the least-supported number toward the one robust loss is the wrong experiment.
- **(a)** mandatory for *any* technical fork. That is a tax, an egress leak, and a category error: most surviving questions are technical *forks* with a user *axis*. Literal Opus will refer everything that still has a library name in it. Dossier-as-escalation is the wrong ladder — Dossier is for the world, not for residual uncertainty. Keep referral for high-leverage architecture and for split panels, which you already have.
- **(b)** unless rewritten to the gate-3 test above. As written it eats the carve-outs. The 93–95% problem is already solved by gates 1–3.
- Preamble-as-option-slot. A live rejected option needs a clickable slot.

Ship the *intent* of (c): no Recommended on user-axis questions (already the rule); Recommended only on unrecoverable-action questions, on the safe path. Tighten “outward-facing / costly” to actions that cannot be undone (delete data, force-push, production mutate, send to a person, spend money). Drafts and reversible publishes stay unmarked user-axis.
