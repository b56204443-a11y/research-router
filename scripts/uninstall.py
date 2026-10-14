#!/usr/bin/env python3
"""Uninstall a managed bundle by moving it to a recoverable backup."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys


def uninstall(home: Path, dry_run: bool = False) -> None:
    home = home.expanduser().resolve()
    router = home / "skills/research-router"
    library = home / "skill-libraries/research-router"
    if router.is_symlink() or library.is_symlink():
        raise ValueError("Refusing to move a symlink installation")
    marker = library / "installation.json"
    if not marker.is_file() or json.loads(marker.read_text(encoding="utf-8")).get("managed_by") != "research-router":
        raise ValueError("No installation managed by this installer was found")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup = home / "research-router-backups" / ("uninstall-" + stamp)
    print(f"Move managed installation to {backup}")
    if dry_run:
        return
    backup.mkdir(parents=True)
    moved = []
    try:
        for name, path in [("router", router), ("library", library)]:
            if path.exists():
                path.rename(backup / name)
                moved.append((path, backup / name))
    except Exception:
        for path, saved in reversed(moved):
            saved.rename(path)
        raise
    print("Uninstalled; other skills are unchanged. The backup can be restored manually.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")))
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    try:
        uninstall(a.codex_home, a.dry_run)
    except (ValueError, OSError) as e:
        p.exit(1, f"Uninstall failed: {e}\n")
