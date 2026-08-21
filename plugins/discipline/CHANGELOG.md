# discipline changelog

## 4.2.0 - 2026-08-21

- New section on the output-to-input ratio, the spend signal that catches an agent reciting an artifact it should be saving. A working run writes back about what it was sent; the failing class wrote back 33.8 times as much.
- The measured cost of leaving it unwatched: 813,649 output tokens on runs that produced nothing, 22% of window output, 414 million cache reads, and 74 of 135 runs producing no artifact.
- Three follow-ons ordered by cost: watch the ratio rather than the total, count the runs that produced nothing, and judge success from the artifact rather than the narration.
- evidence.md records every figure with its tier, and states that the 5x threshold is a judgement from one distribution and that nobody has measured whether watching it shortens a diagnosis.

