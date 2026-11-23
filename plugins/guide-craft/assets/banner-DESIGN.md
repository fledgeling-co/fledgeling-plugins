# guide-craft Banner Design Spec (`design-craft:design-craft`)

Visitor mode: **Read** (marketplace README hero banner, viewed at 900px desktop README width and 400px phone width, authored at 1600x520 and rendered at 3200x1040 @2x).

## Constants derived from `build_icon.py`

| Icon constant (`build_icon.py`) | Value | Banner mapping |
|---|---|---|
| `GROUND_HI` / `GROUND_MID` / `GROUND_LO` | `#FDFCF9` / `#F3EFE7` / `#E7E1D5` | Porcelain ground ramp along `x1=310,y1=0 -> x2=640,y2=1024` (`162deg`) |
| `VIGNETTE` | `#C4B899` (`0.24`, `40% 28%`) | Matching subtle corner cushion vignette |
| `LIGHT_DX, LIGHT_DY` | `-0.62, -0.78` | Shadow offset vector `(+0.62, +0.78)`: `16px 20px` soft, `5px 6px` near in `AO` (`#4A3B2C`) |
| `COVER_HI` / `COVER_MID` / `COVER_LO` | `#6B645E` / `#4A4541` / `#302D2A` | Primary wordmark ink (`#25211E`, >13:1 on porcelain), dark slate surface plate |
| `PAGE_HI` / `PAGE_MID` / `PAGE_LO` | `#FFFBF3` / `#F0E3D0` / `#D4BFA4` | Right-side frosted readout cards and hairline dividers |
| `TAB_MID` / `TAB_LO` | `#EC6A31` / `#C44D1B` | Fill accent only (single season tab pip and active rule); body/mono accent lifted to `#A63812` (5.7:1 AA on `#F3EFE7`) |

## Typography (linked Google Fonts, zero local-only faces)

- **Wordmark:** `Saira Condensed` 700 (`94px`, `-0.015em` tracking, `#25211E`) — subject-mined from tactical field manuals and MW4's own typography, distinct from warned AI defaults.
- **Essence line:** `IBM Plex Sans` 400/500 (`26px`, line-height `1.38`, `#564D43` / `#25211E`, contrast >= 7.2:1).
- **Readout labels:** `IBM Plex Mono` 500 (`15px`, `+0.06em` uppercase tracking, `#564D43` and lifted `#A63812`).

## Composition

Three balanced zones inside `1600x520` with zero overflow:
1. **Left (`x=104..392`):** Real `icon.png` asset (not redrawn) resting over a soft warm porcelain-compatible shadow along `(+0.62, +0.78)`.
2. **Centre (`x=452..1060`):** `guide-craft` wordmark plus one plain essence sentence naming what it delivers (`One dataset, three surfaces, and verified provenance behind every pick.`) with zero em dashes.
3. **Right (`x=1100..1504`):** Three stacked frosted-ivory readout cards (`WEB GUIDE`, `IOS APP`, `VOICE GUIDE`) bridged by one slate `DATASET` spine rail on the left and flagged by one vermilion `SEASON` tab pill at top right, echoing the folio icon's geometry without crowding at 400px downscale.
