# What was removed from this directory, and why

The fidelity loop ran three rounds (r00, r01, r02) and wrote a reference,
candidate and residual raster at 1024 for each, plus the blind panel's image
bundle. That was **30 image files, about 14MB**.

Every sibling plugin in this marketplace ships 5-8MB of assets in total and none
ships a loop trajectory; `create-mac-icon` ships one 15MB example because it owns
the loop and the example is its documentation. Carrying a second copy here buys
nothing and costs every clone of this repository.

**Kept: all 15 text records** — each round's brief, its `score.json`, its gate
output, the blind panel's map, its verdicts and `RUN-NOTE.md`. Those are the
evidence that the loop ran and what it scored, which is the part anybody would
audit. The rasters were intermediate states of an image that is in this directory
at its final form.

Removed deliberately on 2026-08-27, recorded here rather than done silently.
