# r05 — the rule's face

The user looked again and said C1 is "a brighter orange". That is a different fault
from the one r04 fixed: r04 corrected the bloom on the porcelain, the bounce up the
bars and the ramp direction, and all of that holds. None of it touched the face of
the rule itself.

EDIT CLASS: the rule's own vertical gradient. Three of its five stops.

## MEASURED

The rule's solid face isolated by geometry (rows where >500px run above chroma 100),
sampled over 205 columns clear of the bars and clear of both ends, at 1024:

| t down the face | C1 red | A1 red (before) | gap |
|---|---|---|---|
| 0.00 | 252 | 249 |  −3 |
| 0.20 | 254 | 239 | −15 |
| 0.33 | 252 | 230 | −22 |
| 0.46 | 252 | 220 | −32 |
| 0.59 | 254 | 208 | −46 |
| 0.65 | 253 | 203 | −50 |
| 0.85 | 207 | 176 | −32 |
| 0.98 | 202 | 147 | −55 |

**C1 holds R at 252-254 through t=0.63 and only then falls to ~202. The old face fell
away from t≈0.20 and bottomed at 147.** Face mean red 211 against C1's 240. The
coordinator's 256px band measurement — 225 against C1's 252 — is the same fact seen
through a downsample.

The cause was the lower half of the gradient: `#C43F16` at 78% and `#8C2E0F` at the
base, a dark rust. It reads as a bar in shadow rather than a lit cylinder.

## THE FIT

Same method as r04's bounce: the stops are taken from the reference rather than typed.
For each of the three lower offsets — C1's red at that depth, blue set so R−B lands on
the target band, and **C1's own G−B gap at that depth preserved**, which is what keeps
the face orange as the red rises rather than turning it red.

| stop | offset | before | after | C1 red at that depth |
|---|---|---|---|---|
| RULE_LIP  | 0.00 | `#FFE3C4` | **held** | — |
| RULE_HOT  | 0.16 | `#FF9A4E` | **held** | — |
| RULE_MID  | 0.42 | `#E85F22` | `#FC784A` | 252 |
| RULE_BODY | 0.78 | `#C43F16` | `#DB3E29` | 219 |
| RULE_DEEP | 1.00 | `#8C2E0F` | `#CA3F34` | 202 |

The lip and specular are untouched, per the brief — that part read correctly.

## RESULT

Face red now tracks C1 within a few points across the whole face, and **R−B holds
175-177 through the body** — inside the 176-180 target, so it is still a lit cylinder
with top-to-bottom form and not a flat fill:

| t | new R | C1 R | new R−B |
|---|---|---|---|
| 0.09 | 252 | 253 | +175 |
| 0.26 | 251 | 253 | +177 |
| 0.43 | 244 | 252 | +177 |
| 0.61 | 230 | 254 | +177 |
| 0.78 | 217 | 219 | +175 |
| 0.96 | 206 | 202 | +156 |

Face mean red 211 → 234 (C1: 240). At 256px, rule-band mean RGB (225,107,46) →
(232,119,81).

Gate **ACCEPT vs r04, +0.0147 net, and every one of the five sizes improved**:

| size | r04 | r05 |
|---|---|---|
| 1024 | 0.6471 | 0.6507 |
| 256  | 0.7237 | 0.7240 |
| 128  | 0.7100 | 0.7154 |
| 32   | 0.8986 | 0.9021 |
| 16   | 0.9125 | 0.9144 |

## WHAT IT COST — one gate moved, reported rather than promoted past

Self-contrast on the **master** at 32px fell 0.530 → 0.507. That size does not ship
from the master, and as delivered the movement is smaller:

| size | ships from | r04 | r05 |
|---|---|---|---|
| 1024 / 256 / 128 / 96 / 64 / 48 | icon.svg | — | **identical** |
| 32 | icon-small.svg | 0.607 | **0.603** |
| 16 | icon-small.svg | 0.618 | 0.618 |

A 0.7% drop at one size, against the gate's 6% floor. It is a real cost and it is
small; the cause is that a brighter face raises the render's p10 slightly.

## NOT TRADED, as instructed

| invariant | before | after |
|---|---|---|
| figure-ground | 15.1:1 | **15.1:1** |
| GRAPHITE_TOP/UP/MID/LOW/LIT | unchanged | **unchanged** |
| RULE_OVERHANG | 104.0 | **104.0** |
| named layers | 4 | 4 |
