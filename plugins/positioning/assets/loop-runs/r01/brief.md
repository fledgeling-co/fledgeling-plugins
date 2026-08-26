# r01 — edit class: material

One class, the battens' glass. Four parameter changes in `build_icon.py`:

- `TRANSMIT` — the chart's graticule redrawn a second time clipped to the
  battens, so the ground survives the object. An object at 0.8 opacity over a
  smooth ground still hides it; translucency needs something to see through.
- `FROST` — a frosted catch on both long edges, the shaded one narrower and
  cooler, replacing the single lit-edge rim.
- `CORE_LIGHT_*` — a broad low-opacity band well inside the lit edge: the body
  transmitting, rather than a specular sitting on the surface.
- the cross-section stops re-laid so the face is even from 14% to 70% with the
  fall confined to the last fifth — a flat batten rather than a turned dowel.

Two composition changes rode along: the arris cut to the lit pocket edge only,
and the bloom widened.

Result: composite up at all five sizes, net +0.0313. Gate REJECT on the
legibility floor — 32px self-contrast −6.3%, 16px −13.6%. The reference's
battens are lighter than the master's, so converging its material also
converged its figure-ground. This is the documented conflict, not a bug.
