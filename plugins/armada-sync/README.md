# armada-sync

Keeps `~/Dev/ARMADA.md` — the portfolio manifest of every active project in `~/Dev` — truthful after work happens in any single project.

One job, done surgically: rewrite the current project's entry (status, features, key-file references, `updated:` stamp), refresh its index row, and append one changelog line. Never touches other entries; never rebuilds the manifest (that's `ship-armada`'s survey).

Every project's `CLAUDE.md` carries a short "Portfolio manifest" section pointing at this skill, so the manifest stays fresh even when an agent works on a project without the `ship-armada` orchestrator running.
