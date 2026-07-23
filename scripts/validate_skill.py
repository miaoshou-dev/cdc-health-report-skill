#!/usr/bin/env python3
"""Deterministic repository checks for the China CDC report Skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/find-china-cdc-health-report"
ERRORS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(relative: str) -> str:
    path = SKILL_ROOT / relative
    require(path.is_file(), f"missing file: {relative}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def read_repo(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing repository file: {relative}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


skill = read("SKILL.md")
frontmatter = skill.split("---", 2)[1] if skill.startswith("---") else ""
frontmatter_keys = re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE)
require(frontmatter_keys == ["name", "description"], "SKILL.md frontmatter must contain only name and description")
require("name: find-china-cdc-health-report" in frontmatter, "wrong Skill name")
require(len(skill.splitlines()) <= 500, "SKILL.md exceeds 500 lines")

openai_yaml = read("agents/openai.yaml")
for expected in (
    'display_name: "China CDC Health Reports"',
    'short_description: "Find five official China CDC report series"',
):
    require(expected in openai_yaml, f"missing openai.yaml value: {expected}")

required_refs = (
    "source-registry.md",
    "source-schema.md",
    "matching-rules.md",
    "workflow.md",
    "report-schema.md",
    "output-schema.md",
    "metric-schema.md",
    "pdf-extraction-rules.md",
    "vision-task-rules.md",
    "artifact-schema.md",
)
for name in required_refs:
    read(f"references/{name}")

source_ids = (
    "influenza_weekly",
    "respiratory_weekly",
    "covid_monthly",
    "global_infectious_risk_monthly",
    "china_public_health_risk_monthly",
)
registry = read("references/source-registry.md")
for source_id in source_ids:
    require(f"`{source_id}`" in registry, f"missing source registry entry: {source_id}")

adapter_files = sorted((SKILL_ROOT / "references/adapters").glob("*.md"))
require(len(adapter_files) == 5, f"expected 5 adapter files, found {len(adapter_files)}")
for path in adapter_files:
    content = path.read_text(encoding="utf-8")
    for field in (
        "id:",
        "index_url:",
        "allowed_path_prefix:",
        "period_type:",
        "content_mode:",
        "title_pattern:",
        "index_marker:",
        "allowed_url_patterns:",
    ):
        require(field in content, f"{path.name} missing adapter field {field}")
    require("transport_preference: browser_first" in content, f"{path.name} must be browser-first")

legacy_browser_dir = "browser" + "-memory"
require(not (ROOT / legacy_browser_dir).exists(), "legacy browser state directory still exists")
require(not (SKILL_ROOT / "references/browser-scripts.md").exists(), "legacy browser script reference still exists")
require(not (ROOT / "companion-skills").exists(), "legacy companion Skill directory still exists")

tracked_contract_files = [
    SKILL_ROOT / "SKILL.md",
    ROOT / "docs/PRD.md",
    ROOT / "docs/dev-plan.md",
    SKILL_ROOT / "references/artifact-schema.md",
    SKILL_ROOT / "references/output-schema.md",
    SKILL_ROOT / "references/pdf-extraction-rules.md",
    SKILL_ROOT / "references/vision-task-rules.md",
    SKILL_ROOT / "references/workflow.md",
]
legacy_terms = (
    "active" + ".md",
    "previous" + ".md",
    "evidence" + ".json",
    "self" + "_heal",
    "self" + "-heal",
    "bootstrap" + "_failed",
)
for path in tracked_contract_files:
    content = path.read_text(encoding="utf-8")
    for term in legacy_terms:
        require(term not in content, f"{path.relative_to(ROOT)} contains legacy term {term}")

output_schema = read("references/output-schema.md")
for expected in (
    '"schema_version": "2.0"',
    '"pages": []',
    '"content": null',
    '"vision_pages": []',
    '"requires_vision": true',
):
    require(expected in output_schema, f"output schema missing {expected}")

artifact_schema = read("references/artifact-schema.md")
require("extracted.json" in artifact_schema, "Artifact schema lacks extracted.json")
require("explicit download" in artifact_schema, "Artifact schema lacks explicit PDF download rule")

pdf_rules = read("references/pdf-extraction-rules.md")
require("every physical page" in pdf_rules, "PDF rules do not require every physical page")
require("directly within the main Skill" in pdf_rules, "PDF rules still depend on another Skill")

downloader = read("scripts/download_official_document.py")
fetcher = read("scripts/fetch_report.py")
require("ProxyHandler({})" in downloader, "downloader must ignore proxy environment")
require('OFFICIAL_HOST = "www.chinacdc.cn"' in downloader, "downloader must pin the official host")
require("TemporaryDirectory" in fetcher, "unified fetcher must clean extract-only PDF transfers")
require("def run_pipeline(" in fetcher, "unified fetcher lacks the pipeline entry point")
require("scripts/fetch_report.py" in skill, "SKILL.md does not route supported actions through the unified runner")
require("transfer verified bytes only with:" in skill.lower(), "SKILL.md must route PDF bytes through the downloader")
require("without opening a browser pdf viewer" in skill.lower(), "SKILL.md must prohibit browser PDF viewers")

tests = read_repo("tests/reference-cases.md")
for number in range(1, 51):
    require(f"TC-{number:03}" in tests, f"missing TC-{number:03}")
require("TC-049 | 无状态浏览" in tests, "TC-049 does not cover stateless browsing")
require("TC-050 | 边界安全" in tests, "TC-050 does not cover adapter boundaries")

gitignore = read_repo(".gitignore")
require(
    "/skills/find-china-cdc-health-report/artifacts/*" in gitignore,
    "runtime artifacts are not ignored",
)
require((SKILL_ROOT / "artifacts" / ".gitkeep").is_file(), "artifacts placeholder missing")

sample = ROOT / "tests/samples/P020260715815376876315.pdf"
if sample.exists():
    import hashlib

    digest = hashlib.sha256(sample.read_bytes()).hexdigest()
    require(
        digest == "9a6f23cef5ae56ff570feec73cd3b1eaedf14927a6943a2eb232d6924dc79356",
        "sample PDF hash mismatch",
    )
else:
    print("SKIP: optional frozen sample PDF is not bundled")

if ERRORS:
    for error in ERRORS:
        print(f"FAIL: {error}")
    sys.exit(1)

print("PASS: stateless v2 Skill structure valid")
