# Why this panel directory is incomplete

Written by the commission agent, not by `judge_panel.py`. There is no
`panel.json` here because the run was stopped before it could write one, and a
missing tally is a fact worth stating rather than an absence to be filled in by
hand.

What ran:

- **`claude` (opus, high) — completed, both orders.** `verdict-claude.json`.
  It picked the same slot letter in both passes, which after unblinding means it
  preferred opposite takes; the protocol records a swap flip as a tie, so all
  four dimensions resolve to `tie`. It is also the same family as the author of
  the master, so it is excluded from the majority regardless.
- **`cursor` (grok-4.6, xhigh) — failed.** It read the bundle, wrote its own
  `analyze_pixels.py`, produced `analysis_output.json`, and then stopped without
  emitting a verdict; the first pass ran into the harness's 900-second cap. The
  swapped pass began behaving the same way and was stopped rather than retried
  into the ground. Its measurements survive in `bundle/analysis_output.json` and
  separate the two takes by under one luminance unit in every region it sampled
  — full image, centre crop, rod region and background — which is consistent
  with the tie the other judge recorded.
- **`openai` (gpt-5.6-sol) — not asked.** Warden, the secrets broker, was not
  running, so there was no key to be had without reading one out of a config
  file, which is the thing Warden exists to stop.

Net: no decisive judge. Under the loop's own ordering — gate below panel below
the rubric and a human — that hands the shipping decision back to the 12-point
rubric and to looking at the renders, which is what `../../../audit.html`
records. It is not evidence that the shipped take is better than the pre-loop
one; it is the absence of that evidence, and the sheet says so.
