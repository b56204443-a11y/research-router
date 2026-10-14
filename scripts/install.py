#!/usr/bin/env python3
"""Install only the router into discovery; keep its modules in a private library."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def install(home: Path, replace: bool = False, dry_run: bool = False) -> None:
    home = home.expanduser().resolve()
    sources = [ROOT / "skills/research-router", ROOT / "skill-libraries/research-router"]
    targets = [home / "skills/research-router", home / "skill-libraries/research-router"]
    if home == ROOT or ROOT in home.parents or home in ROOT.parents:
        raise ValueError("Installation home must be separate from this source checkout")
    for source in sources:
        if not source.is_dir():
            raise ValueError(f"Missing source directory: {source}")
    for target in targets:
        if target.is_symlink():
            raise ValueError(f"Refusing to replace a symlink: {target}")
        if target.exists() and not replace:
            raise ValueError(f"Already exists: {target}. Use --replace to back it up and replace it")
        print(f"Install -> {target}")
    if dry_run:
        return
    from validate import validate
    validate(ROOT)
    home.mkdir(parents=True, exist_ok=True)
    backup = None
    if any(t.exists() for t in targets):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup = home / "research-router-backups" / stamp
        backup.mkdir(parents=True)
    installed, saved = [], []
    with tempfile.TemporaryDirectory(prefix=".research-router-", dir=home) as temp:
        staging = Path(temp)
        for i, source in enumerate(sources):
            shutil.copytree(source, staging / str(i), ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        for name in ["LICENSE", "NOTICE"]:
            shutil.copy2(ROOT / name, staging / "1" / name)
        marker = {"schema_version": 1, "managed_by": "research-router", "module_count":
                  json.loads((sources[0] / "references/catalog.json").read_text())["module_count"]}
        (staging / "1" / "installation.json").write_text(json.dumps(marker, indent=2) + "\n")
        try:
            for i, target in enumerate(targets):
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    saved_path = backup / str(i)
                    target.rename(saved_path)
                    saved.append((target, saved_path))
                (staging / str(i)).rename(target)
                installed.append(target)
        except Exception:
            for target in reversed(installed):
                shutil.rmtree(target)
            for target, saved_path in reversed(saved):
                saved_path.rename(target)
            raise
    print("Installed. Start a new Codex chat and invoke $research-router.")
    if backup:
        print(f"Previous installation backed up at: {backup}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")))
    p.add_argument("--replace", action="store_true", help="Back up the existing router and library before replacement")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    try:
        install(a.codex_home, a.replace, a.dry_run)
    except (ValueError, OSError) as e:
        p.exit(1, f"Install failed: {e}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
