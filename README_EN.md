# Research Router

[中文](README.md) · [Modules](docs/MODULES.md) · [Licensing](docs/LICENSING.md)

A lightweight Codex skill that searches and loads research modules on demand:
manuscripts, literature retrieval, statistics, scientific figures and scientific software.
Only the router enters skill discovery. The **245** curated modules remain in a separate library.

## Install

Requires Codex and Python 3.10+. Installation and search use the standard library only.

```bash
git clone https://github.com/b56204443-a11y/research-router.git
cd research-router
python3 scripts/install.py
```

On Windows use `py -3` if needed. Download ZIP also works; run the installer from the extracted repository.
Start a new Codex chat and ask: `Use $research-router to plan the statistical analysis for this study.`

`CODEX_HOME` is respected; the default is `~/.codex`. Use `--codex-home PATH` for a custom destination
and `--dry-run` to preview it. Existing installations require `--replace`, which creates a backup.

```bash
git pull --ff-only
python3 scripts/install.py --replace
python3 scripts/uninstall.py
```

Uninstallation moves a managed installation to a recoverable backup, leaving other skills untouched.
Use the same `--codex-home` for installation, updates and uninstallation.

## Inspect

```bash
python3 skills/research-router/scripts/find_modules.py --query "scanpy" --json
python3 skills/research-router/scripts/find_modules.py --list --category literature
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Search uses local keyword ranking with common Chinese task aliases; it is not an online semantic search.
Results include absolute `skill_path` values. Override the library using `--library-root` or `RESEARCH_ROUTER_LIBRARY`.

Scientific dependencies are installed only when a selected module needs them. Model weights,
databases, papers and a complete scientific Python environment are not distributed. External services
may require network access, subscriptions or the user's credentials. Host tools determine execution capabilities.

Installation and routing are tested; external APIs and algorithms in all 245 modules are not independently validated.
Eleven modules are withheld due to restrictive or unresolved licensing labels or upstream notices.
See [the exclusions](skill-libraries/research-router/excluded-modules.json).

This is a curated third-party bundle, not a claim that the modules were authored here.
Original routing and release tooling is MIT-licensed. Modules retain their upstream and component-specific terms,
including Apache-2.0. Pinned origins, licenses, notices and snapshot hashes travel with the installed library.
See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute.
