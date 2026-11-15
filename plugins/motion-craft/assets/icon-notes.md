# Icon notes — `motion-craft`

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying gel objects, beside `design-craft` and `ux-craft` in the marketplace lineup. Concept chosen by the owner on 2026-11-15 from three: onion-skin ghosts, over an ease-out ribbon and a playhead on a track.

## The idea

**Onion-skin ghosts.** One gel capsule shown at three moments of a single move, the way an animator's onion skin, or motion-craft's own contact sheet, shows a film: successive frames laid over each other. The two earlier frames are frosted ghosts, fainter the older they are; the frame it lands on is the only solid thing in the tile, poured vermilion gel lit from inside.

The signature move is the **spacing**: the gap between frames shrinks as the capsule arrives (`GAP_1` 12.5° against `GAP_2` 8.5° of arc), an ease-out drawn in space, the long-tailed arrival the skill's craft rules put on every entrance.

## How it was made

- Engine A, `build_icon.py` → `icon.svg`, is the shipped master; every value is a named constant.
- Engine B, Arrow 2 (`icon-engineB-arrow-431b80.svg`), and Engine C, a GPT Image raster referenced on apple-06, apple-12 and apple-28 (`icon-engineC-82b1d4.png`), were the alternates. The raster won the material read; its frosted ghosts, shared orientation along the path, broader specular band and warm ground bloom were carried into the master as parameter edits over four renders.
- `audit.html` scores the three takes (11, 8 and 9 of 12) and passes `audit_sheet.py check`.

## Known liabilities

The measured fidelity loop was not run, so the master's distance from the raster's material is judged by eye. The landed capsule's gloss is flatter than the raster's, the ghosts' frost is opaque rather than truly translucent, and at 16 px the trail reads as a grey smear rather than two frames.
