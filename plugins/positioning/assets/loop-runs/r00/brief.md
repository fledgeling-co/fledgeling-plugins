# r00 — baseline

The pre-loop Engine A master: geometry settled (three bearings at 22 / 66 / -40
screen degrees, errors +84 / -124 / -96 px from the fix at (496, 486)), material
still the first draft — near-opaque battens with a single cross-section ramp, a
radial ember shard, a bright arris on all three pocket edges.

Reference: `../reference.png`, the c1 raster masked to the family squircle so
both sides carry the same outer shape. The reference's composition is not the
master's, so the composite is bounded well below 1 whatever the material does.
It is read for direction of travel, not level.

Metric tier: numpy. torch and lpips are not installed here, so LPIPS never ran
and nothing measured material at 256 or 1024. Every gate below was taken with
`--allow-degraded-tier` and covers structure and small-size legibility only.

1024 composite 0.5173 · 16px self-contrast 0.452 (reference 0.465).
