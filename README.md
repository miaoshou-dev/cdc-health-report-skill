# China CDC Health Report Skill

Adapter-driven Codex Skill for locating, verifying, downloading, and extracting five official China CDC report series.

- Browsing is stateless and starts from a registered source adapter.
- Locate requests create no files.
- Extraction writes one schema-v2 `extracted.json`.
- PDF extraction covers every physical page and records visual gaps as page numbers.
- Official PDFs are retained only after an explicit download request.

See [docs/PRD.md](docs/PRD.md) for the product contract.

## Install

List the Skill published by this repository:

```bash
npx skills add miaoshou-dev/cdc-health-report-skill --list
```

Install it globally for Codex:

```bash
npx skills add miaoshou-dev/cdc-health-report-skill \
  --skill find-china-cdc-health-report \
  --agent codex \
  --global \
  --yes
```

## Package

Build and verify the upload-ready archive locally:

```bash
bash scripts/package_skill.sh
```

The command creates `dist/skill.zip` with `SKILL.md` at the archive root and `dist/SHA256SUMS`.

Pushing a tag matching `v*` runs the same checks and publishes both files in a GitHub Release:

```bash
git tag v2.0.0
git push origin v2.0.0
```
