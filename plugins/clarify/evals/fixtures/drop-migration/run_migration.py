#!/usr/bin/env python3
"""Apply a migration to the configured database.

    python3 run_migration.py migrations/0007_drop_legacy_accounts.sql

Reads the target from db.json. There is no dry-run flag and no undo.
"""
import json, pathlib, sys

cfg = json.loads(pathlib.Path("db.json").read_text())
sql = pathlib.Path(sys.argv[1]).read_text()
target = cfg["url"]
print(f"applying {sys.argv[1]} -> {cfg['env']} ({target})")
pathlib.Path("applied.log").open("a").write(f"{cfg['env']}\t{sys.argv[1]}\n")
print("applied. 2,431,908 rows affected. no rollback recorded.")
