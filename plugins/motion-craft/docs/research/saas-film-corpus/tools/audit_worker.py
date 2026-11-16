"""Count what a headless worker actually did, from its stream-json transcripts.

    python3 -P audit_worker.py <video-dir>
"""
import json
import sys
from pathlib import Path

d = Path(sys.argv[1])
reads = {"frames": set(), "sheets": set(), "strips": set(), "crops": set(), "other": set()}
skills, mcp, bash = [], 0, {"prep": 0, "ink": 0, "crop": 0, "whisper": 0}
tools = {}
cost = 0.0
models = set()
final = None
for name in ("worker.jsonl", "worker.repair.jsonl"):
    p = d / name
    if not p.exists():
        continue
    for line in p.read_text(errors="replace").splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "result":
            cost += float(ev.get("total_cost_usd") or 0)
            models |= set((ev.get("modelUsage") or {}).keys())
            final = ev.get("result")
        msg = ev.get("message") or {}
        if ev.get("type") == "assistant" and msg.get("model"):
            models.add(msg["model"])
        for c in msg.get("content") or []:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            n = c.get("name", "")
            tools[n] = tools.get(n, 0) + 1
            inp = c.get("input") or {}
            if n == "Read":
                fp = str(inp.get("file_path", ""))
                for k in ("frames", "sheets", "strips", "crops"):
                    if f"/{k}/" in fp:
                        reads[k].add(Path(fp).name)
                        break
                else:
                    reads["other"].add(Path(fp).name)
            elif n == "Skill":
                skills.append(inp.get("skill") or inp.get("command") or json.dumps(inp)[:60])
            elif "youtube_transcript" in n:
                mcp += 1
            elif n == "Bash":
                cmd = str(inp.get("command", ""))
                bash["prep"] += "prep.sh" in cmd
                bash["ink"] += "measure ink" in cmd
                bash["crop"] += "crop.py" in cmd
                bash["whisper"] += "mlx_whisper" in cmd

expected = []
try:
    expected = json.loads((d / "measure" / "metrics.json").read_text()).get("frames_to_open", [])
except Exception:
    pass
missing = sorted(set(expected) - reads["frames"])
summary = {
    "models": sorted(models), "cost_usd": round(cost, 3),
    "be_my_witness_invoked": any("be-my-witness" in s for s in skills),
    "transcript_mcp_calls": mcp, "prep_runs": bash["prep"], "ink_runs": bash["ink"], "crop_runs": bash["crop"],
    "frames_read": len(reads["frames"]), "frames_expected": len(expected), "frames_missing": len(missing),
    "sheets_read": len(reads["sheets"]), "strips_read": len(reads["strips"]), "crops_read": len(reads["crops"]),
}
print(json.dumps({"summary": summary, "tools": tools, "skills": skills, "frames_missing": missing[:80],
                  "final": (final or "")[:300]}, indent=1))
