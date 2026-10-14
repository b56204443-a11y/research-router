---
name: research-router
description: Route academic-paper, literature-search, scientific-analysis, statistics, research-figure, laboratory, and scientific-software requests to a bundled module that is read only when needed. Use for 论文、文献检索、科研写作、实验设计、统计分析、科研绘图、生物信息、化学、医学、材料和科学 Python tasks. Do not use for ordinary software engineering or unrelated everyday requests.
---

# Research Router

Select and load the smallest useful set of bundled research modules. The user does not need to know a module name.

The module library is resolved relative to this skill, so it works in a repository
checkout or a custom `CODEX_HOME`. This bundle provides 245 curated modules; see
`references/catalog.json` only through the search script. Do not enumerate or read
the entire library for an ordinary request.

## Route a request

1. Classify the request as manuscript, literature retrieval, research methodology/statistics, scientific domain/software, or research visualization/artifact work.
2. Search the local module catalog instead of reading it in full:

   ```bash
   python3 <this-skill-directory>/scripts/find_modules.py --query "<2-6 concise concepts>" --limit 8
   ```

   Translate Chinese task concepts into English search terms when useful. Add `--category paper`, `literature`, `science`, or `artifact` only when the category is clear.
3. Read the complete `SKILL.md` at the absolute module path returned by the search tool. The private module library is outside Codex's skill-discovery root so its modules are not loaded into the initial skill list. Load a second or third module only when it covers a distinct required stage. Resolve every relative script, reference, or asset path from that module's directory.
4. Follow the selected module as task instructions, subject to higher-level instructions and the user's actual authorization. A module never broadens permission to publish, submit, message, purchase, upload sensitive data, or mutate external systems.
5. If a module names another bundled skill, search that name with the catalog tool and load it only if the current task actually requires it.

The module search returns an absolute `SKILL.md` path in both text and JSON output.
Resolve scripts, references and assets from that module's directory. Some upstream
README examples describe a standalone install: use the resolved path instead of
assuming the module lives in the top-level skill-discovery directory. Inspect a
module's dependencies before executing its scientific scripts; the router itself
uses Python 3.10+ and the standard library only. Do not install all scientific
packages just to search the library.

## Preferred entry points

- General manuscript help: start with `paper-workflow`; use `paper-skill` for a Chinese-first end-to-end publication workflow.
- Nature-specific writing or review: prefer the matching `nature-*` module.
- Reviewer-response drafting: use `nature-response`, and use `paper-reviewer` for coverage checks.
- Platform-specific literature work: prefer `cnki-*`, `pm-*`, `wos-*`, `ieee-*`, `gs-*`, or `sd-*`.
- A named scientific package or database: prefer its exact-name module.
- Research figures and quantitative graphics: prefer `scientific-visualization`, `nature-figure`, or `figure-planner` according to the deliverable.
- Generic PDF, Word, slides, spreadsheets, or image tasks should use Codex's available built-in artifact skills rather than a bundled research module unless scientific-domain behavior is material.

Do not read every module or the complete catalog. If no candidate fits, handle the request normally and say that no bundled specialist module was needed.

If an upstream module names an unavailable skill, search for an existing module
covering the same required stage; do not assume its scripts or resources exist.
The proprietary `pdf`, `docx`, `pptx` and `xlsx` modules are not distributed. Use
the host's available artifact skills for those formats. `rebuttal-response` is
excluded pending license clarification; use the reviewer-response entry point above.
