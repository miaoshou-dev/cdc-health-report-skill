# China CDC Health Report Skill

Adapter-driven Codex Skill for locating, verifying, downloading, and extracting five official China CDC report series.

- Browsing is stateless and starts from a registered source adapter.
- Locate requests create no files.
- Extraction writes one schema-v2 `extracted.json`.
- PDF extraction covers every physical page and records visual gaps as page numbers.
- Official PDFs are retained only after an explicit download request.

See [docs/PRD.md](docs/PRD.md) for the product contract.
