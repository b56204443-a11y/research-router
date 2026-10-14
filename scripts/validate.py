#!/usr/bin/env python3
"""Check release integrity, catalog paths, provenance and accidental credentials."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SECRET = re.compile(r"(?<![A-Za-z0-9_-])(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-(?:proj-)?[A-Za-z0-9_-]{32,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)")


def validate(root: Path = ROOT) -> None:
    skill = root / "skills/research-router"
    catalog = json.loads((skill / "references/catalog.json").read_text())
    if Path(catalog["library_root"]).is_absolute():
        raise ValueError("Catalog must use a portable relative module directory")
    library = (skill / catalog["library_root"]).resolve()
    modules = catalog["modules"]
    folders = [m["folder"] for m in modules]
    if len(folders) != len(set(folders)) or len(folders) != catalog["module_count"]:
        raise ValueError("Catalog count or folder uniqueness mismatch")
    if set(folders) != {p.name for p in library.iterdir() if p.is_dir()}:
        raise ValueError("Module directories do not match the catalog")
    for m in modules:
        if not re.fullmatch(r"[a-z0-9-]+", m["folder"]):
            raise ValueError(f"Invalid module folder: {m['folder']}")
        path = library / m["folder"] / "SKILL.md"
        text = path.read_text()
        if not text.startswith("---\n") or not re.search(r"(?m)^name:", text) or not re.search(r"(?m)^description:", text):
            raise ValueError(f"Invalid skill frontmatter: {path}")
        if not m.get("source_repo") or not re.fullmatch(r"[a-f0-9]{40}", m.get("source_commit", "")):
            raise ValueError(f"Missing pinned source: {m['folder']}")
    bundle = library.parent
    excluded = json.loads((bundle / "excluded-modules.json").read_text())["modules"]
    if set(folders) & {m["folder"] for m in excluded}:
        raise ValueError("An excluded module is distributed")
    provenance = json.loads((bundle / "provenance.json").read_text())
    for m in provenance["modules"]:
        base = library / m["folder"]
        expected = m["files"]
        actual = {str(p.relative_to(base)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
        if actual != expected:
            raise ValueError(f"Module snapshot differs from provenance: {m['folder']}")
    if {m["folder"] for m in provenance["modules"]} != set(folders):
        raise ValueError("Provenance coverage mismatch")
    for p in root.rglob("*"):
        if ".git" in p.parts or "__pycache__" in p.parts:
            continue
        if p.is_symlink():
            raise ValueError(f"Symlink in release: {p}")
        if not p.is_file():
            continue
        if p.name == ".env" or p.suffix in {".pem", ".key"}:
            raise ValueError(f"Potential credential file: {p}")
        if p.suffix in {".md", ".json", ".yaml", ".yml", ".toml", ".py", ".js", ".mjs", ".sh", ".txt"}:
            text = p.read_text(errors="replace")
            if re.search(r"/Users/[a-z][0-9]{5,}(?:/|\b)", text) or SECRET.search(text):
                raise ValueError(f"Personal path or credential pattern in {p}")
    for name in ["LICENSE", "NOTICE"]:
        if not (root / name).is_file():
            raise ValueError(f"Missing release notice: {name}")
    print(f"Validated {len(modules)} modules: paths, pinned sources, checksums and release exclusions.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    a = p.parse_args()
    try:
        validate(a.root.resolve())
    except (ValueError, OSError) as e:
        p.exit(1, f"Validation failed: {e}\n")
