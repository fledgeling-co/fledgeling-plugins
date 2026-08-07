#!/usr/bin/env python3
"""loop_runner.py — headless driver for the icon fidelity loop.

Runs the whole loop without a Claude session attached: start it with nohup,
close the terminal, come back to committed rounds and a review queue.

    python3 loop_runner.py --config docs/loop.config.json            # run
    python3 loop_runner.py --config ... --dry-run                    # plan only
    touch docs/LOOP-STOP                                             # stop after the current round

Per round it: builds an Opus brief from live state, runs it through
`claude -p` with a whitelisted toolset (no git, no rm, no network), runs the
structure gate, scores against the reference, applies the Pareto gate,
optionally runs the blind judge panel, commits accepted rounds, appends to
the ledger, and writes a review sheet for the human.

Two things it deliberately does NOT do, because they are judgment calls:
  - It never decides that the 12-point rubric beat the gate. When the gate
    and the panel disagree, the round is committed as PROVISIONAL and an
    entry is written to the review queue for a human to settle.
  - It never pushes. Commits are local until someone pushes them.

Safety: the implement agent runs with an explicit tool whitelist that has no
git, no rm, and no network. The "subagents never run git" rule is enforced by
the harness rather than by asking the model nicely.
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

EDIT_CLASSES = ["material", "detail", "small-size repair", "coarse structure"]

# No git, no rm, no curl. The agent can build, render, score and read.
ALLOWED_TOOLS = ",".join([
    "Read", "Write", "Edit", "Glob", "Grep",
    "Bash(python3:*)", "Bash(rsvg-convert:*)", "Bash(sips:*)",
    "Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)", "Bash(cp:*)",
])

BRIEF = """<context>
You are running one round of a measured icon-fidelity loop. A hand-authored SVG
icon is being iterated toward a diffusion-raster reference until its material
quality matches. Each round makes ONE class of edit, scores the result at five
sizes against the reference, and a Pareto gate accepts or rejects it.

This is round {round_id} on this fixture. The round's edit class is {edit_class}.

Why the loop exists: hand-authored masters reliably win composition and
small-size legibility but lose material richness (volumetric shading, lighting,
translucency, contact shadows) to the rasters. Closing that gap is the work.
</context>

<fixture>
Working directory: {assets_dir}

- `{build}` — the generator. Geometry and material are named constants here; it
  emits `{icon}`. Every edit goes through this script; never hand-edit the SVG.
- `{icon}` — the current master (generated).
- `{reference}` — THE REFERENCE this round scores against.
- `{notes}` — the decision log across prior rounds. Read its tail first.
- `{baseline_dir}/` — the baseline this round is measured against: `score.json`,
  `residual-1024.png` (bright = disagreement), `edges-candidate.png`,
  `edges-reference.png`, `candidate-1024.png`, `reference-1024.png`.
{extra_files}
{hazards}</fixture>

<baseline_numbers>
Current master vs the reference:

{score_table}

The shape of these numbers is the brief. Where small sizes score well above
large ones, composition has converged and material has not, and the gain has to
come from 1024 and 256.
</baseline_numbers>

<prior_learnings>
Confirmed, measured findings. Apply what fits this round's edit class:

{learnings}

The full recipe table is at {skill_dir}/references/material-recipes.md. Read it.
</prior_learnings>

{human}<task>
Make ONE class of edit: {edit_class}. {class_scope}

Start by finding where the gap actually is, from the artifacts rather than from
assumption: open the residual map, the two edge maps, and the candidate and
reference at 1024. Crop and zoom into the regions the residual says are worst,
and sample actual pixel values out of both images wherever a relationship
matters (face luminances, each material's darkest pixel and its hue there, the
ground's local values beside each object). The reference is ground truth for
material relationships, and reading numbers off it beats reasoning about what it
probably looks like.

Run the instrument as you go:

    cd {assets_dir}
    python3 {skill_dir}/scripts/fidelity.py structure --candidate {icon}{envelope_flags}
    python3 {skill_dir}/scripts/fidelity.py score --candidate {icon} --reference {reference} --outdir {round_dir} --label "{round_id} {edit_class}"
    python3 {skill_dir}/scripts/fidelity.py gate --candidate {round_dir}/score.json --baseline {baseline_dir}/score.json

The gate is the round's verdict, and the harness applies it. If it REJECTs,
LEAVE your candidate in place and report the rejection with its numbers; the
harness reverts from its own snapshot. Do not revert the files yourself: the
harness re-scores independently after you finish, and a reverted file makes it
score the baseline instead of your work, losing the round's real numbers. A
rejected round is a real result; the next round takes a different class. Do not
keep editing to chase an ACCEPT.

{extra_checks}
The 12-point rubric holds authority over the gate. The reference itself can fail
checks the master passes, so converging on it can drag the master below the
rubric floor. If a change raises the composite while breaking figure-ground, the
16px read, or the single light model, that change loses. Say so when it happens;
that disagreement is worth more than the point.

Make the material physically right and let the score follow. Tuning constants
against the composite without a physical reason is how this loop breaks, and the
score is a proxy for a judgment a human will make on the render.
</task>

<constraints>
- Edit `{build}` only. Regenerate the SVG and its PNG renders from it.
- You have no git tools and no network; do not attempt either.
- Do not delegate to subagents. This is a single track; spawn none.
- Deliver what was asked, at the scope intended: one {edit_class} round on this
  fixture. Make routine judgment calls yourself. If the brief looks mistaken or
  a better approach exists, say so in a sentence and carry on with the round as
  asked rather than quietly widening or transforming it.
- Append a round entry to `{notes}`: what you measured off the reference, what
  changed and why, the before/after table, what it cost. Cover the substance
  without padding it.
</constraints>

<reporting>
Your final message is a plain report of about 200 words: the gate verdict with
the five before/after composites, what you changed and the measurement that
motivated it, whether the rubric score moved, and any construction confirmed
well enough to be reusable (named precisely enough that another icon could
apply it).
</reporting>"""

CLASS_SCOPE = {
    "material": "In scope: gradient stops and ramps, per-face shading separation, opacity, blur radii, highlight and shadow shapes, contact shadows, ambient occlusion, rim light. Out of scope: silhouette, footprint, object scale, composition.",
    "detail": "In scope: micro-geometry, texture accents, local control points, small ornament that survives at 128px. Out of scope: the overall silhouette, palette, and light model.",
    "small-size repair": "In scope: simplifying or strengthening features that alias or smear at 32 and 16px, and only those. Out of scope: anything that changes the 1024 read beyond tolerance.",
    "coarse structure": "In scope: silhouette, centring, object scale, attitude, major colour fields. Out of scope: fine material work and micro-detail.",
}

DEFAULT_LEARNINGS = """1. Check the dark end's hue, not only the ramp's endpoints. A lit or translucent
   material must keep its SATURATION in shadow, not just its luminance; a shadow
   that desaturates reads opaque. Invisible to a range check, obvious to a
   darkest-pixel check.
2. Measure the reference's actual values rather than assuming them. Assumed
   relationships ("the highlight is lighter than its surroundings") have cost
   this loop three failed attempts where the reference had no such relationship.
3. Fade material where no boundary lives, never across one. Copying a
   reference's fade wholesale once dropped a master's figure-ground to 1.02:1.
4. Contact shadows are the highest ratio-of-effect-to-bytes layer.
5. Attitude is a taper, not a lifted copy; keep lifts affine so materials follow
   the geometry for free."""


def sh(cmd, cwd=None, timeout=None, check=False):
    return subprocess.run(cmd, cwd=cwd, timeout=timeout, check=check,
                          capture_output=True, text=True, shell=isinstance(cmd, str))


def score_table(score_path: pathlib.Path) -> str:
    if not score_path.exists():
        return "(no baseline yet)"
    d = json.loads(score_path.read_text())
    rows = ["| size | composite | lum_delta | ssim | edge_f1 |", "|---:|---:|---:|---:|---:|"]
    for size in ("1024", "256", "128", "32", "16"):
        m = d["sizes"][size]
        rows.append(f"| {size} | {m['composite']:.4f} | {m['lum_delta']:.4f} | {m['ssim']:.4f} | {m['edge_f1']:.4f} |")
    rows.append(f"\nMetric tier: {d.get('tier', 'unknown')}.")
    return "\n".join(rows)


def composite_1024(score_path: pathlib.Path):
    if not score_path.exists():
        return None
    return json.loads(score_path.read_text())["sizes"]["1024"]["composite"]


class Runner:
    def __init__(self, cfg_path: pathlib.Path, args):
        self.cfg = json.loads(cfg_path.read_text())
        self.repo = pathlib.Path(self.cfg["repo"])
        self.skill = (self.repo / self.cfg["skill"]).resolve()
        self.ledger = self.repo / self.cfg["ledger"]
        self.queue = self.repo / self.cfg.get("review_queue", "docs/loop-review-queue.md")
        self.stopfile = self.repo / self.cfg.get("stop_file", "docs/LOOP-STOP")
        self.args = args
        self.state_path = self.repo / self.cfg.get("state", "docs/loop-state.json")
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {
            "iteration": 0, "fixture_index": 0, "cost_usd": 0.0, "fixtures": {}}

    # ---------------------------------------------------------------- helpers
    def fstate(self, name):
        return self.state["fixtures"].setdefault(
            name, {"round": 0, "class_index": 0, "accepted": 0, "rejects_in_row": 0,
                   "gains": [], "panel_nonwins": 0, "converged": False})

    def save(self):
        self.state_path.write_text(json.dumps(self.state, indent=2))

    def log(self, msg):
        stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"[{stamp}] {msg}", flush=True)

    def ledger_line(self, fixture, edit_class, gate, panel, skill_change):
        with self.ledger.open("a") as f:
            f.write(f"| {self.state['iteration']} | {fixture} | {edit_class} | {gate} | {panel} | {skill_change} |\n")

    def review_entry(self, title, body):
        if not self.queue.exists():
            self.queue.write_text("# Loop review queue\n\nRounds the runner could not settle on its own. Each needs a human look.\n\n")
        with self.queue.open("a") as f:
            f.write(f"\n## {title}\n\n{body}\n")

    # ----------------------------------------------------------------- round
    def build_brief(self, fx, edit_class, round_id, round_dir, baseline_dir):
        assets = self.repo / fx["dir"]
        envelope = ""
        if fx.get("max_paths"):
            envelope = f" --max-paths {fx['max_paths']} --max-bytes {fx['max_bytes']}"
        extra_checks = ""
        if fx.get("extra_checks"):
            lines = "\n".join(f"    {c}" for c in fx["extra_checks"])
            extra_checks = (f"This fixture carries an extra invariant. Run it and keep it satisfied:\n\n{lines}\n\n"
                            f"{fx.get('extra_checks_note', '')}\n\n")
        extra_files = ""
        for name, desc in fx.get("extra_files", {}).items():
            extra_files += f"- `{name}` — {desc}\n"
        # Reading a large generated master thrashes autocompact and kills the round.
        # Measured: improve-skill's icon.svg is 307KB, about 88k tokens, and the agent
        # re-read it after each rebuild until the context refilled three times over.
        big = []
        for f in sorted(assets.glob("*")):
            if f.is_file() and f.stat().st_size > 60_000 and f.suffix in (".svg", ".html", ".json"):
                big.append(f"`{f.name}` ({f.stat().st_size // 1024}KB)")
        hazards = ""
        if big:
            hazards = ("\nDo not read these files; they are generated output, they are large "
                       "enough to exhaust the context window, and nothing in this round needs "
                       "their text: " + ", ".join(big) + ". Judge the artwork from its PNG "
                       "renders and edit the build script. If you must confirm a fragment, "
                       "grep it or read a bounded byte range.\n")
        human = ""
        feedback = sorted((assets / "loop-runs").glob("r*/review-feedback.json"),
                          key=lambda f: f.stat().st_mtime, reverse=True)
        if feedback:
            try:
                fb = json.loads(feedback[0].read_text())
                a = fb.get("answers") or {}
                notes = (a.get("notes") or "").strip()
                defects = ", ".join(a.get("defects") or [])
                if notes or defects:
                    human = ("<human_verdict>\nA human reviewed a previous round of this icon "
                             f"against the reference and said:\n\n  \"{notes}\"\n")
                    if defects:
                        human += f"\nDefects they ticked: {defects}.\n"
                    human += ("\nThis outranks the metrics. A human comparing the render to the "
                              "reference sees things no similarity score measures, and this is the "
                              "only judgment here made by someone who knows what the icon is for. "
                              "If what they describe falls inside this round's edit class, it is "
                              "the round's job. If it does not, leave it for the round that owns "
                              "it and say so; do not widen the round to chase it.\n"
                              "</human_verdict>\n\n")
            except Exception:
                pass
        return BRIEF.format(
            round_id=round_id, edit_class=edit_class,
            class_scope=CLASS_SCOPE.get(edit_class, ""),
            assets_dir=assets, build=fx["build"], icon=fx["icon"],
            reference=fx["reference"], notes=fx.get("notes", "icon-notes.md"),
            baseline_dir=baseline_dir, round_dir=round_dir,
            score_table=score_table(pathlib.Path(baseline_dir) / "score.json"),
            learnings=self.cfg.get("learnings", DEFAULT_LEARNINGS),
            skill_dir=self.skill, envelope_flags=envelope,
            extra_checks=extra_checks, extra_files=extra_files, hazards=hazards,
            human=human)

    def run_implement(self, brief_path, assets):
        # Hand the agent the brief's PATH, not its text. Passing ~7KB of brief as the
        # -p argument fails instantly and deterministically with "Prompt is too long"
        # (measured: same bytes, same cwd, same flags; a one-line suffix flips it to
        # success, so it is not length). Reading it from disk sidesteps that entirely
        # and costs one Read.
        prompt = (f"Read {brief_path} and carry out the round it describes, in full. "
                  f"It is your complete brief; follow it exactly.")
        cmd = ["claude", "-p", prompt, "--model", self.cfg.get("model", "opus"),
               "--allowedTools", ALLOWED_TOOLS,
               "--permission-mode", "acceptEdits",
               # Load ZERO MCP servers. This machine configures 13 of them, and their
               # tool definitions alone (higgsfield and dossier are enormous) fill a
               # large fraction of the window before the agent reads anything. A round
               # that made 6 tool calls totalling ~10k tokens still died reporting the
               # context refilling three times over. The implement agent needs none of
               # them: it edits a build script and runs a scorer.
               "--strict-mcp-config",
               "--add-dir", str(self.repo)]
        if self.cfg.get("effort"):
            cmd += ["--effort", self.cfg["effort"]]
        # Run from OUTSIDE the marketplace repo. Started with cwd inside it, every
        # brief fails instantly with "Prompt is too long" while the same bytes
        # succeed from elsewhere (measured: identical 200-byte prefix, ok from /tmp,
        # ~, and ~/Dev; fails from the repo root and below). The repo is a plugin
        # marketplace, so a session opened inside it loads far more context than the
        # brief itself. --add-dir keeps write access to the fixture; the brief uses
        # absolute paths and cds itself.
        t0 = time.time()
        self.log(f"  brief {brief_path}, cwd {self.cfg.get('agent_cwd') or self.repo.parent}, effort {self.cfg.get('effort')}")
        # CLAUDE_CODE_DISABLE_1M_CONTEXT is set to the string "0" in this shell, and a
        # non-empty string is truthy, so inheriting it caps the child at the small
        # window. Drop it and the other session-scoped vars so the child starts clean.
        env = {k: v for k, v in os.environ.items()
               if k not in ("CLAUDE_CODE_DISABLE_1M_CONTEXT", "CLAUDE_CODE_SESSION_ID",
                            "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_EFFORT")}
        r = subprocess.run(cmd, cwd=str(self.cfg.get("agent_cwd") or self.repo.parent),
                           capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL,  # else the CLI waits 3s for stdin
                           timeout=self.cfg.get("round_timeout_s", 2700))
        self.log(f"  implement finished in {time.time()-t0:.0f}s (exit {r.returncode})")
        if r.returncode != 0:
            head = ((r.stdout or "") + (r.stderr or "")).strip()[:200]
            self.log(f"  implement FAILED: {head}")
        return r

    def run_panel(self, fx, round_dir, candidate, baseline_svg, label):
        cmd = ["python3", str(self.skill / "scripts/judge_panel.py"),
               "--candidate", str(candidate), "--baseline", str(baseline_svg),
               "--reference", str(self.repo / fx["dir"] / fx["reference"]),
               "--outdir", str(round_dir / "panel"), "--label", label]
        if self.cfg.get("panel_env_file"):
            cmd += ["--env-file", self.cfg["panel_env_file"]]
        if self.cfg.get("judges"):
            cmd += ["--judges", self.cfg["judges"]]
        r = sh(cmd, timeout=self.cfg.get("panel_timeout_s", 1800))
        pj = round_dir / "panel" / "panel.json"
        if not pj.exists():
            self.log(f"  panel produced no verdict (exit {r.returncode})")
            return None
        panel = json.loads(pj.read_text())
        # exact cost from the sol leg's usage, at published rates
        for fam in ("openai",):
            vp = round_dir / "panel" / f"verdict-{fam}.json"
            if vp.exists():
                u = (json.loads(vp.read_text()).get("meta") or {}).get("usage") or {}
                it, ot = u.get("input_tokens", 0), u.get("output_tokens", 0)
                rate_in = self.cfg.get("sol_rate_in_per_mtok", 1.25)
                rate_out = self.cfg.get("sol_rate_out_per_mtok", 10.0)
                self.state["cost_usd"] += it / 1e6 * rate_in + ot / 1e6 * rate_out
        return panel

    def one_round(self):
        fixtures = self.cfg["fixtures"]
        while self.state["fixture_index"] < len(fixtures) and \
                self.fstate(fixtures[self.state["fixture_index"]]["name"])["converged"]:
            self.state["fixture_index"] += 1
        if self.state["fixture_index"] >= len(fixtures):
            self.log("queue exhausted: every fixture converged")
            return False

        fx = fixtures[self.state["fixture_index"]]
        st = self.fstate(fx["name"])
        assets = self.repo / fx["dir"]
        st["round"] += 1
        self.state["iteration"] += 1
        round_id = f"r{st['round']:02d}"
        round_dir = assets / "loop-runs" / round_id
        round_dir.mkdir(parents=True, exist_ok=True)
        baseline_dir = assets / "loop-runs" / (st.get("baseline_dir") or "r00-baseline")
        edit_class = EDIT_CLASSES[st["class_index"] % len(EDIT_CLASSES)]
        self.log(f"iteration {self.state['iteration']}: {fx['name']} {round_id} [{edit_class}]")

        if not (baseline_dir / "score.json").exists():
            sh(["python3", str(self.skill / "scripts/fidelity.py"), "score",
                "--candidate", fx["icon"], "--reference", fx["reference"],
                "--outdir", str(baseline_dir), "--label", "baseline"], cwd=str(assets))

        # snapshot for revert
        bak = round_dir / "_before"
        bak.mkdir(exist_ok=True)
        for f in (fx["build"], fx["icon"]):
            if (assets / f).exists():
                shutil.copy2(assets / f, bak / f)

        brief = self.build_brief(fx, edit_class, round_id, round_dir, baseline_dir)
        (round_dir / "brief.md").write_text(brief)
        if self.args.dry_run:
            self.log("  dry run: brief written, nothing executed")
            return False

        r = self.run_implement(round_dir / "brief.md", assets)
        (round_dir / "implement.log").write_text((r.stdout or "") + "\n---STDERR---\n" + (r.stderr or ""))
        if r.returncode != 0:
            # A harness failure is not a rejected edit. Counting it as one would burn
            # the fixture's edit-class rotation and could converge it on nothing.
            self.log("  harness failure, not an edit rejection; recording and stopping")
            self.ledger_line(fx["name"], edit_class, "HARNESS-FAIL", "n/a",
                             "implement agent could not run")
            self.review_entry(f"{fx['name']} {round_id}: implement agent failed to run",
                              f"`claude -p` exited {r.returncode}. First 200 chars of its output:\n\n"
                              f"    {((r.stdout or '') + (r.stderr or '')).strip()[:200]}\n\n"
                              f"The loop stopped rather than spending iterations on a broken harness.")
            st["round"] -= 1
            self.state["iteration"] -= 1
            self.save()
            return False

        # score + gate, run by the harness rather than trusted from the agent
        sh(["python3", str(self.skill / "scripts/fidelity.py"), "score",
            "--candidate", fx["icon"], "--reference", fx["reference"],
            "--outdir", str(round_dir), "--label", f"{round_id} {edit_class}"], cwd=str(assets))
        g = sh(["python3", str(self.skill / "scripts/fidelity.py"), "gate",
                "--candidate", str(round_dir / "score.json"),
                "--baseline", str(baseline_dir / "score.json")], cwd=str(assets))
        gate_ok = g.returncode == 0
        (round_dir / "gate.txt").write_text(g.stdout or "")
        self.log(f"  gate: {'ACCEPT' if gate_ok else 'REJECT'}")

        panel_verdict = "n/a"
        provisional = False
        if gate_ok and self.cfg.get("panel_every", 1) and \
                st["accepted"] % self.cfg.get("panel_every", 1) == 0:
            last = assets / "loop-runs" / "last-accepted" / fx["icon"]
            if last.exists():
                panel = self.run_panel(fx, round_dir, assets / fx["icon"], last, round_id)
                if panel:
                    panel_verdict = panel["tally"]["overall"]["winner"]
                    if panel_verdict == "baseline":
                        st["panel_nonwins"] += 1
                        provisional = True
                    elif panel_verdict == "no-majority":
                        st["panel_nonwins"] += 1
                    else:
                        st["panel_nonwins"] = 0

        if gate_ok:
            st["accepted"] += 1
            st["rejects_in_row"] = 0
            gain = (composite_1024(round_dir / "score.json") or 0) - (composite_1024(baseline_dir / "score.json") or 0)
            st["gains"].append(round(gain, 5))
            snap = assets / "loop-runs" / "last-accepted"
            snap.mkdir(exist_ok=True)
            for f in (fx["build"], fx["icon"]):
                if (assets / f).exists():
                    shutil.copy2(assets / f, snap / f)
            st["baseline_dir"] = round_id  # next round measures against this one
            tag = "PROVISIONAL " if provisional else ""
            # scoped add: never sweep up unrelated work happening elsewhere in the repo
            sh(["git", "add", str(assets), str(self.ledger), str(self.state_path)], cwd=str(self.repo))
            if self.queue.exists():
                sh(["git", "add", str(self.queue)], cwd=str(self.repo))
            sh(["git", "commit", "-q", "-m",
                f"Loop {fx['name']} {round_id}: {tag}{edit_class}, gate ACCEPT (1024 {gain:+.4f}), panel {panel_verdict}\n\n"
                f"Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"], cwd=str(self.repo))
            if provisional:
                self.review_entry(
                    f"{fx['name']} {round_id}: gate and panel disagree",
                    f"The Pareto gate ACCEPTed (1024 composite {gain:+.4f}) but the blind panel "
                    f"preferred the previous take. The runner committed it as PROVISIONAL and did "
                    f"not settle the rubric question.\n\n"
                    f"Review sheet: `{round_dir}/review.html`\nPanel: `{round_dir}/panel/panel.json`\n"
                    f"Revert with: `git revert` the round's commit, or keep it and note why.")
        else:
            st["rejects_in_row"] += 1
            st["class_index"] += 1  # next round takes a different class
            for f in (fx["build"], fx["icon"]):
                if (bak / f).exists():
                    shutil.copy2(bak / f, assets / f)
            sh(["git", "checkout", "--", str(assets)], cwd=str(self.repo))

        # human review sheet, written for later rather than served
        last = assets / "loop-runs" / "last-accepted" / fx["icon"]
        if last.exists():
            sh(["python3", str(self.skill / "scripts/review_sheet.py"),
                "--candidate", str(assets / fx["icon"]), "--baseline", str(last),
                "--reference", str(assets / fx["reference"]),
                "--outdir", str(round_dir), "--label", f"{fx['name']} {round_id}",
                "--no-serve"])

        # convergence
        recent = st["gains"][-3:]
        if len(recent) == 3 and all(abs(x) < self.cfg.get("converge_gain", 0.005) for x in recent):
            st["converged"] = True
            self.log(f"  {fx['name']} converged: three rounds under the gain floor")
        # Panel non-wins normally converge a fixture: the judges have stopped
        # preferring new rounds. But an open human-named defect outranks that. The
        # reviewer of r01 called the shaving curl and the left side's lighting wrong
        # while the panel was calling rounds a tie, so converging on the panel alone
        # would abandon a fixture with known defects. While human notes are on file,
        # both signals must agree; the gain floor still bounds the fixture either way.
        has_open_human_notes = bool(list((assets / "loop-runs").glob("r*/review-feedback.json")))
        if st["panel_nonwins"] >= 2:
            if has_open_human_notes and not st["converged"]:
                self.log(f"  {fx['name']}: panel would converge, but human notes are open; "
                         f"continuing until the gain floor decides")
            else:
                st["converged"] = True
                self.log(f"  {fx['name']} converged: panel stopped preferring new rounds")
        if st["rejects_in_row"] >= len(EDIT_CLASSES):
            st["converged"] = True
            self.log(f"  {fx['name']} converged: every edit class rejected in turn")

        self.ledger_line(fx["name"], edit_class,
                         "ACCEPT" if gate_ok else "REJECT", panel_verdict,
                         "PROVISIONAL, queued for review" if provisional else "")
        self.save()
        return True

    def run(self):
        consecutive_errors = 0
        import datetime as _dt
        _src = pathlib.Path(__file__)
        self.log(f"runner source {_src.name} modified "
                 f"{_dt.datetime.fromtimestamp(_src.stat().st_mtime):%H:%M:%S} — a long-running "
                 f"process keeps the version it started with; restart it after editing.")
        self.log(f"loop runner: {len(self.cfg['fixtures'])} fixtures, "
                 f"budget {self.cfg.get('max_iterations', 100)} iterations, "
                 f"cost cap ${self.cfg.get('cost_cap_usd', 15)}")
        while self.state["iteration"] < self.cfg.get("max_iterations", 100):
            if self.stopfile.exists():
                self.log(f"stop file present ({self.stopfile}); stopping cleanly")
                break
            if self.state["cost_usd"] >= self.cfg.get("cost_cap_usd", 15.0):
                self.log(f"cost cap reached (${self.state['cost_usd']:.2f}); stopping")
                self.review_entry("Cost cap reached",
                                  f"Panel spend hit ${self.state['cost_usd']:.2f}. Raise `cost_cap_usd` in the config to continue.")
                break
            try:
                if not self.one_round():
                    break
            except subprocess.TimeoutExpired:
                self.log("  round timed out; recording and moving on")
                self.ledger_line("(timeout)", "-", "TIMEOUT", "-", "")
                self.fstate(self.cfg["fixtures"][self.state["fixture_index"]]["name"])["rejects_in_row"] += 1
                self.save()
            except Exception as e:  # a bad round must not kill an overnight run
                self.log(f"  round error: {e}")
                self.ledger_line("(error)", "-", "ERROR", "-", str(e)[:120])
                self.save()
                consecutive_errors += 1
                # Without this, a bug that throws every round spends the entire
                # iteration budget in about one second. It did exactly that once.
                if consecutive_errors >= 3:
                    self.log("  three consecutive errors; stopping rather than burning the budget")
                    self.review_entry("Loop stopped: three consecutive round errors",
                                      f"Last error: {e}\n\nThe runner halted instead of spending "
                                      f"the remaining iteration budget on a broken round.")
                    break
                time.sleep(10)
                continue
            consecutive_errors = 0
        self.log(f"done: {self.state['iteration']} iterations, panel spend ${self.state['cost_usd']:.2f}")
        self.log(f"review queue: {self.queue}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--dry-run", action="store_true", help="write the next round's brief and stop")
    args = ap.parse_args()
    Runner(pathlib.Path(args.config), args).run()


if __name__ == "__main__":
    main()
