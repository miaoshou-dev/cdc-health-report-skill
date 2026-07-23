#!/usr/bin/env python3
"""Deterministic repository checks for the China CDC report skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing file: {relative}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


skill = read("SKILL.md")
lines = skill.splitlines()
frontmatter = skill.split("---", 2)[1] if skill.startswith("---") else ""
frontmatter_keys = re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE)

require(frontmatter_keys == ["name", "description"], "SKILL.md frontmatter must contain only name and description")
require("name: find-china-cdc-health-report" in frontmatter, "wrong skill name")
require(len(lines) <= 500, f"SKILL.md exceeds 500 lines: {len(lines)}")
require(100 <= len(lines), f"SKILL.md is unexpectedly thin: {len(lines)} lines")

openai_yaml = read("agents/openai.yaml")
for expected in (
    'display_name: "China CDC Health Reports"',
    'short_description: "Find five official China CDC report series"',
    'default_prompt: "Use $find-china-cdc-health-report to locate and process the requested official China CDC report."',
):
    require(expected in openai_yaml, f"missing openai.yaml value: {expected}")

required_refs = (
    "source-registry.md", "source-schema.md", "matching-rules.md", "browser-scripts.md",
    "workflow.md", "report-schema.md", "output-schema.md", "metric-schema.md",
    "pdf-extraction-rules.md", "vision-task-rules.md", "artifact-schema.md", "test-cases.md",
)
for name in required_refs:
    read(f"references/{name}")

registry = read("references/source-registry.md")
source_ids = (
    "influenza_weekly", "respiratory_weekly", "covid_monthly",
    "global_infectious_risk_monthly", "china_public_health_risk_monthly",
)
for source_id in source_ids:
    require(f"`{source_id}`" in registry, f"missing source registry entry: {source_id}")
adapter_files = sorted((ROOT / "references/adapters").glob("*.md"))
require(len(adapter_files) == 5, f"expected 5 adapter files, found {len(adapter_files)}")
for path in adapter_files:
    content = path.read_text(encoding="utf-8")
    require("transport_preference: browser_first" in content, f"{path.name} must be browser-first")
require("ordinary HTTP as page-access fallback" in skill, "SKILL.md lacks browser-first page-access fallback rule")
downloader = read("scripts/download_official_document.py")
require("ProxyHandler({})" in downloader, "downloader must explicitly ignore proxy environment")
require("OFFICIAL_HOST = \"www.chinacdc.cn\"" in downloader, "downloader must pin the official host")
require("transfer bytes only with:" in skill, "SKILL.md must route all document bytes through the downloader")
require("without opening a browser PDF viewer" in skill, "SKILL.md must prohibit browser PDF downloads")

memory_files = sorted((ROOT / "browser-memory").glob("*/*.md"))
require(bool(memory_files), "no browser memory files")
for source_id in source_ids:
    require((ROOT / "browser-memory" / source_id / "active.md").is_file(), f"missing active memory: {source_id}")
    require((ROOT / "browser-memory" / source_id / "previous.md").is_file(), f"missing previous memory: {source_id}")
for path in memory_files:
    content = path.read_text(encoding="utf-8")
    forbidden = {
        "transient element ref": r"@e\d+",
        "cookie assignment": r"(?i)\bset-cookie\s*:",
        "authorization header": r"(?i)\bauthorization\s*:",
        "screen coordinate": r"(?i)\b(?:x|y)\s*=\s*\d+",
    }
    for label, pattern in forbidden.items():
        require(not re.search(pattern, content), f"{path.relative_to(ROOT)} contains {label}")

tests = read("references/test-cases.md")
require("pending_freeze" not in "\n".join(line for line in tests.splitlines() if line.startswith("| TC-")), "test table still has pending_freeze")
fast_frozen = sum(
    1 for line in tests.splitlines()
    if line.startswith("| TC-") and "| yes | frozen |" in line
)
require(fast_frozen >= 20, f"only {fast_frozen} frozen fast-path cases")
for number in range(1, 51):
    require(f"TC-{number:03}" in tests, f"missing TC-{number:03}")

gitignore = read(".gitignore")
require("artifacts/*" in gitignore, "runtime artifacts are not ignored")
require((ROOT / "artifacts" / ".gitkeep").is_file(), "artifacts placeholder missing")

sample = ROOT / "references/samples/P020260715815376876315.pdf"
if sample.exists():
    import hashlib

    digest = hashlib.sha256(sample.read_bytes()).hexdigest()
    require(digest == "9a6f23cef5ae56ff570feec73cd3b1eaedf14927a6943a2eb232d6924dc79356", "sample PDF hash mismatch")
else:
    print("SKIP: optional frozen sample PDF is not bundled")

if ERRORS:
    for error in ERRORS:
        print(f"FAIL: {error}")
    sys.exit(1)

print(f"PASS: skill structure valid; {fast_frozen} frozen fast-path cases")
