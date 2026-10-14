#!/usr/bin/env python3
"""Search the bundled research module catalog without loading it into context."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
CATALOG = SKILL_ROOT / "references" / "catalog.json"
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)

ALIASES = {
    "论文": "paper manuscript writing publication",
    "写作": "writing manuscript",
    "润色": "polishing prose rewrite",
    "审稿": "review reviewer peer-review",
    "回复审稿": "rebuttal response reviewer",
    "返修": "revision rebuttal response",
    "投稿": "submission journal venue",
    "引用": "citation reference bibliography",
    "文献": "literature paper search lookup",
    "检索": "search lookup retrieval",
    "知网": "cnki search",
    "谷歌学术": "google scholar gs search",
    "实验": "experiment experimental design",
    "统计": "statistics statistical analysis",
    "统计分析": "statistical-analysis",
    "科研绘图": "scientific-visualization",
    "参考文献": "citation management verifier",
    "审稿回复": "nature-response paper-reviewer",
    "中文论文": "paper-skill",
    "论文工作流": "paper-workflow",
    "样本量": "statistical power sample size",
    "绘图": "figure visualization plot",
    "图表": "figure visualization chart",
    "单细胞": "single cell scanpy anndata scvi",
    "转录组": "transcriptomics rnaseq bulk-rnaseq",
    "生物信息": "bioinformatics biopython genomics",
    "化学": "chemistry rdkit medchem molecular",
    "医学": "medical clinical health",
    "材料": "materials pymatgen",
    "机器学习": "machine learning scikit-learn",
    "深度学习": "deep learning pytorch transformers",
    "时间序列": "time series forecasting aeon timesfm",
    "科研": "scientific research",
}


def tokens(text: str) -> set[str]:
    return {m.group(0).lower() for m in TOKEN_RE.finditer(text)}


def expand_query(query: str) -> str:
    additions = [english for chinese, english in ALIASES.items() if chinese in query]
    return " ".join([query, *additions])


def score(entry: dict[str, str], query: str) -> float:
    expanded = expand_query(query).lower()
    q = tokens(expanded)
    name = entry["name"].lower()
    folder = entry["folder"].lower()
    description = entry["description"].lower()
    haystack = tokens(f"{name} {folder} {description} {entry['category']}")
    value = 0.0
    if name in expanded or folder in expanded:
        value += 18.0
    platform_defaults = {
        "cnki": "cnki-search",
        "pubmed": "pm-search",
        "wos": "wos-search",
        "ieee": "ieee-search",
        "google scholar": "gs-search",
        "sciencedirect": "sd-search",
    }
    if "search" in q:
        for platform, default_name in platform_defaults.items():
            if platform in expanded and name == default_name:
                value += 16.0
    for term in q:
        if term == name or term == folder:
            value += 12.0
        elif term in name or term in folder:
            value += 5.0
        if term in haystack:
            value += 2.0
    value += len(q & haystack) / max(len(q), 1)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query")
    parser.add_argument("--list", action="store_true", help="List modules without ranking")
    parser.add_argument("--library-root", type=Path, help="Override module directory")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--category", choices=["paper", "literature", "science", "artifact"])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not args.query and not args.list:
        parser.error("provide --query or --list")
    if args.limit < 1:
        parser.error("--limit must be positive")

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = catalog["modules"]
    override = args.library_root or os.environ.get("RESEARCH_ROUTER_LIBRARY")
    library = Path(override).expanduser() if override else SKILL_ROOT / catalog["library_root"]
    library = library.resolve()
    if not library.is_dir():
        parser.error(f"module directory not found: {library}; run scripts/install.py")
    if args.category:
        entries = [entry for entry in entries if entry["category"] == args.category]
    exact = next((e for e in entries if args.query and args.query.lower() in
                  {e["name"].lower(), e["folder"].lower()}), None)
    ranked = sorted(
        ((score(entry, args.query or ""), entry) for entry in entries),
        key=lambda item: (-item[0], item[1]["name"]),
    )
    selected = [entry | {"score": round(value, 2)} for value, entry in ranked if value > 0][: args.limit]
    if exact:
        selected = [exact | {"score": 100.0}]
    if args.list:
        selected = [entry | {"score": 0.0} for entry in sorted(entries, key=lambda e: e["name"])]
    for entry in selected:
        entry["skill_path"] = str(library / entry["folder"] / "SKILL.md")
        if not Path(entry["skill_path"]).is_file():
            parser.error(f"missing module: {entry['skill_path']}; reinstall the bundle")
    if args.as_json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        for entry in selected:
            print(
                f"{entry['score']:>5}  {entry['name']:<34} "
                f"[{entry['category']}]  "
                f"{entry['skill_path']}\n"
                f"       {entry['description']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
