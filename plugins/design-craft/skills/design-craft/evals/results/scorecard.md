# design-craft lint gate — structural evals, original vs rebuild

**original 9/25 · rebuild 23/25**  
Artifact checks, not scores. Both versions run the same fixtures with the same
invocations. A19-A22 are regression guards over what the original already did;
A23-A25 are cost assertions the ORIGINAL passes and the rebuild deliberately
does not — each one is a trade named in evidence.md rather than an oversight.

| # | assertion | original | rebuild |
|---|---|---|---|
| A1 | 13px brand orange on paper (#E65400 on #FDFCFA, 3.66:1) is reported | FAIL | PASS |
| A2 | a contrast failure gates at critical | FAIL | PASS |
| A3 | a failing pair written in oklch() is resolved and reported | FAIL | PASS |
| A4 | text on a gradient is reported UNMEASURABLE rather than skipped | FAIL | PASS |
| A5 | the documented phone-bezel snippet passes (exit 0) | FAIL | PASS |
| A6 | the documented tweak-panel snippet passes (exit 0) | PASS | PASS |
| A7 | a Google Fonts <link> is not condemned as a blocker (it is the one origin the artifact CSP permits) | FAIL | PASS |
| A8 | an <img> with no width/height attributes is caught even when its style string contains the words | FAIL | PASS |
| A9 | the external resource is reported at its own line, not at the first // in the file | FAIL | PASS |
| A10 | a suppression with no reason does not silence its check | PASS | PASS |
| A11 | a resting opacity:0 on a page with reveal keyframes is reported (prints and captures blank) | FAIL | PASS |
| A12 | a token defined and never referenced is reported | FAIL | PASS |
| A13 | outline:none with no replacement is reported | FAIL | PASS |
| A14 | an HTML deliverable with no <title> is reported | FAIL | PASS |
| A15 | index.html is reported as naming the format, not the design | FAIL | PASS |
| A16 | gating findings go to stdout and warnings do not (fail/warn split) | FAIL | PASS |
| A17 | the run prints its own not-checked line, so a clean result cannot be read as verified | FAIL | PASS |
| A18 | every finding names the downstream consequence, not just the rule | FAIL | PASS |
| A19 | all 14 checks the original carried still fire on the regression fixture | PASS | PASS |
| A20 | a file full of defects exits non-zero | PASS | PASS |
| A21 | a contrast failure alone is enough to fail the build | PASS | PASS |
| A22 | the gate does not lint a file under references/ as source | PASS | PASS |
| A23 | a file whose ONLY defects are aesthetic cues (pure b/w, Inter, the border-left card, Tailwind indigo) fails the build | PASS | FAIL |
| A24 | a hero with text over a gradient produces no finding at all | PASS | FAIL |
| A25 | a specimen file publishing tokens for downstream consumers passes (exit 0) | PASS | PASS |

## Where the original wins or draws

- **A23** — a file whose ONLY defects are aesthetic cues (pure b/w, Inter, the border-left card, Tailwind indigo) fails the build
- **A24** — a hero with text over a gradient produces no finding at all

Drawn (both pass) — these are the regression guards doing their job:

- **A6** — the documented tweak-panel snippet passes (exit 0)
- **A10** — a suppression with no reason does not silence its check
- **A19** — all 14 checks the original carried still fire on the regression fixture
- **A20** — a file full of defects exits non-zero
- **A21** — a contrast failure alone is enough to fail the build
- **A22** — the gate does not lint a file under references/ as source
- **A25** — a specimen file publishing tokens for downstream consumers passes (exit 0)
