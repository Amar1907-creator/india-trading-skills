#!/usr/bin/env python3
"""Copy shared/india_data.py into every skill that has a scripts/ folder.

Run after editing shared/india_data.py:  python3 scripts/sync_shared.py
"""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "shared" / "india_data.py"

for scripts_dir in sorted(ROOT.glob("skills/*/scripts")):
    shutil.copy2(SRC, scripts_dir / "india_data.py")
    print(f"synced -> {scripts_dir.relative_to(ROOT)}")
