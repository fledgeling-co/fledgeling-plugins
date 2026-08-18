| # | assertion | original | rebuild |
|---|---|---|---|
| A1 | --regulated survives a reformatted probe | **FAIL** — printed PASS with all four disclosure checks unrun (rc 0) | **PASS** — refused, rc 1; provenanceMissing reported |
| A2 | the type floor can fail a build | **FAIL** — typeBelowFloor computed and ignored; exit 0, PASS | **PASS** — typeBelowFloor is a blocker; rc 1 |
| A3 | chart coverage carries its denominator | **FAIL** — chartsChecked never reaches the verdict | **PASS** — denominator printed beside the count |
| A4 | a declared two-bar truncated pair is judged | **FAIL** — 2-bar groups declined by judge(); printed PASS at exit 0 | **PASS** — judged and blocking; rc 1 |
| A5 | a zero denominator is not a pass | **FAIL** — PASS across 0 slides examined, exit 0 | **PASS** — refused with rc 7 and the cause named |
| A6 | every blocker carries its consequence | **FAIL** — bare count and coordinates; every consequence is in a source comment the caller never sees | **PASS** — consequence printed beneath each finding |
| A7 | the deck's own name is gated | **FAIL** — <title>Deck</title> unchecked | **PASS** — flagged as a blocker |
| A8 | drawn accent marks count | **FAIL** — text leaves only: 4 accent bars + a rule scored 0, and accentOverspent never reaches the verdict | **PASS** — drawn marks counted, reported as a warning |
| A9 | non-IFRS needs a statutory companion on its slide | **FAIL** — only deck-wide audit-qualifier presence is tested | **PASS** — flagged as a blocker (SEC Reg G / CDI 102.10, ASIC RG 230) |
| A10 | dual and inverted axes are caught | **FAIL** — no dual/inverted axis check; printed PASS at exit 0 | **PASS** — both caught and blocking; rc 1 |
| A11 | a misspelled config key is refused | **FAIL** — Object.assign accepted it; the probe ran on defaults and reported a clean deck | **PASS** — refused: unknown config key(s): regualted |
| A12 | obscura's stderr is relayed verbatim | **FAIL** — 2>/dev/null discarded it and substituted a guessed advisory (rc 4) | **PASS** — relayed under the guard |
| A13 | CONTROL: a clean deck still passes | **PASS** — passed with a real denominator | **PASS** — passed with a real denominator |
| A14 | the verdict names what was gated | **FAIL** — nothing ties the URL gated to the file delivered | **PASS** — served bytes identified in the verdict |
| A15 | a check that threw reads as unrun | **FAIL** — the note is in the JSON and never read; null read as 0 and the verdict was PASS at exit 0 | **PASS** — surfaced as NOT RUN (rc 1) |
| A16 | an empty probe result is refused | **PASS** — exit 4 with "this is NOT a pass" in the message | **PASS** — exit 4 with "this is NOT a pass" in the message |
| A17 | NO REGRESSION: pre-existing blockers still fire | **PASS** — titleWrap still blocks; rc 1 | **PASS** — titleWrap still blocks; rc 1 |

**original 3/17 · rebuild 17/17**
