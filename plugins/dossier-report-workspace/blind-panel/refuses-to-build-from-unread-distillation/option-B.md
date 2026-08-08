# I can't build the page from this — and it isn't a scoping problem

Two things block it, and only one of them is about the warning banner.

## 1. There are no findings in what you pasted

Everything in that output is an **evidence profile**: how many sources, how many domains, how much they overlapped. That's a description of the gathering, not of the answer. There isn't a single claim, number, date, or conclusion in it.

A page built from this would have nothing on it that came from the research. I would be writing the substance myself and citing 174 URLs I've never seen as though they backed it. That's not a thin page — it's a fabricated one wearing a citation count as credibility.

## 2. Five of five reports were never opened

The banner is the merge tool telling you it produced a distillation that no one — not me, not the panel — has checked against its sources. `research_synthesise` merges deterministically: it dedupes URLs and counts domains. It doesn't read for sense. It cannot tell you that three backends contradict each other on the central question, and it will happily merge a report that failed mid-run and wrote two fluent paragraphs about why it couldn't research.

## The 7% is being read the wrong way round

"Only 7% of sources overlapped" reads like breadth. Turn it over: **about 93% of those 174 sources were seen by exactly one backend.** Almost nothing in this corpus has independent corroboration. Five researchers each went somewhere different and no two of them landed on the same page often enough to confirm each other.

That's the argument for reading the reports, not for skipping it. The one thing a five-backend panel buys you that a single run can't — seeing where they disagree — is precisely what's still unspent. And a merge that dedupes by URL can make the opposite mistake too: a claim echoed in four reports that all trace to one press release looks like consensus in a merged list and isn't. Only reading catches that.

## Also: those run IDs don't resolve

I tried. `dr_ec5f4883` returns *"No run with id."* All five are 8 characters; the stored IDs are 16 (`dr_572e265d0e726e56`). They've been truncated somewhere between the panel output and here — so as things stand I couldn't open the reports even if I stopped arguing and just did it.

## What I'd do instead — all of it free

The money is already spent (five runs, so roughly $10–30 by the usual bands). It's spent whether or not anyone reads the result. Reading is the only remaining step that's *free*, and it's the one being skipped.

1. **Get the full IDs** — `research_list` shows the recent runs; the five are near the top.
2. **Outline first, then sections** — `research_read` defaults to a table of contents with per-section token estimates. Five outlines is cheap and immediately shows whether the reports even answer the same question.
3. **Pull the sections that matter** — by index or title, under a token budget. Not the full 60k-token reports.
4. **Then `research_synthesise` becomes worth something** — the merged claim list is checkable against what I've read, and I can build the page on claims I can defend.

Worth adding once there's a draft: `research_verify_citations` dereferences every cited URL (a fabricated citation is the failure that survives to production because nobody clicks), and `research_verify_claims` tests whether the cited pages actually say what the report says they say — which is a different and stricter question.

## Say the word

Give me the full run IDs, or let me pull them from `research_list`, and I'll read all five outline-first, reconcile them, and build the page — with the disagreements surfaced rather than averaged away.

If you want to move now, I can build the page **structure** — layout, sections, evidence-profile panel, source registry — and leave the claims as marked gaps to fill after the read. That's honest. A finished-looking page over unread reports isn't, and it fails in the worst way: it looks right.
