# ADR-004 — no backpressure at the ingest boundary

Status: accepted, 2026-04-11

We accept lossy ingest rather than propagating backpressure to callers, because the
upstream emitters are fire-and-forget and cannot handle a rejection. The queue is sized
to absorb a 30-second burst at the *expected* peak of 1,200 events/s.

Open: we have never measured what the real ceiling is. The 1,200 figure is the product
forecast from 2025, not a measurement.
