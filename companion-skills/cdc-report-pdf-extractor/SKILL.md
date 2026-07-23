---
name: cdc-report-pdf-extractor
description: Deterministically inspect and extract targeted text, native tables, evidence, and unresolved visual gaps from an already-located and authorized official China CDC PDF. Use only when the parent workflow supplies a local PDF, target questions or fields, report period, output paths, and `extract` or `vision` authorization. Do not locate reports, fetch other issues, compare periods, or perform OCR/chart vision without explicit `vision` authorization.
---

# CDC Report PDF Extractor

## Accept a bounded handoff

Require:

- absolute local PDF path;
- verified source URL and SHA-256 when available;
- report type and reporting period;
- specific target questions, metrics, tables, or sections;
- absolute output paths for evidence and extracted results;
- authorization level: `extract` or `vision`;
- vision budget when authorized.

Reject missing or non-PDF input, paths outside the provided task/Artifact roots, and authorization below `extract`. Do not locate a report, download another issue, read user Downloads, expand targets, or compare periods.

## Load the environment

Prefer Codex's bundled document/PDF runtime. Use available tools appropriate to the target: `pdfinfo` for metadata, `pdftotext` for searchable text, `pypdf` for page inspection, and `pdfplumber` for characters, coordinates, vector lines, and native tables. Do not install a system package without separate user approval. If a minimal isolated Python package is needed under `extract`, announce its name, location, and purpose first.

## Diagnose before extracting

Build a page map containing page number, useful text character count/quality, images, vector lines, candidate tables/charts, likely scan status, and relevance to the targets. Do not send the whole PDF to model context. Do not render all pages by default.

Treat covers and decorative image pages as irrelevant unless explicitly targeted. For the frozen influenza sample, expect 19 pages, usable native text on pages 2–18, mostly-image pages 1 and 19, native-first tables on pages 4 and 13, and image-based line charts.

## Extract native text

- Select target-relevant pages using native search and the page map.
- Preserve page, original text, blocks, reading order, bbox when available, and extraction method.
- Keep original strings beside parsed values.
- Record omissions, garbled text, or uncertain reading order as warnings; never repair text by guessing.

## Extract native tables

- Prefer character coordinates and vector borders over visual recognition.
- Preserve headers, row/column order, merged-cell interpretation, footnotes, raw strings, parsed values, units, denominators, counts, and percentages.
- Validate row and column totals, percentage ranges/totals where meaningful, header/period/unit agreement, and internal consistency.
- Keep values with failed checks and attach warnings; do not silently correct them.

## Identify visual gaps

Create an unresolved item only when native extraction cannot answer a target. Include `id`, `type`, `page`, `image` or bbox if known, `reason`, `requires_vision=true`, `relevance_tags`, `estimated_cost`, and `expected_output`.

Under `extract`, stop after writing native evidence and unresolved items. Return `extraction_partial` when relevant gaps remain and ask the parent workflow to obtain vision authorization. Merely identifying a gap is not authorization to render or inspect it visually.

## Run authorized vision

Under `vision`, read `references/vision.md`. Select only relevant, unresolved, nondecorative regions. Render the smallest useful crop. Preserve OCR reading order and table structure. For charts, identify title, axes, units, legend, series, annotations, and labeled values. Mark unlabeled-curve digitization as `approximate=true` with confidence and error notes.

Keep visual evidence separate from native evidence. If they conflict, retain both with provenance. Never overwrite native results. Follow the supplied budget; default `balanced` if absent. Do not retry more than the reference allows.

## Persist atomically

Write `evidence.json` and `extracted.json` only to supplied absolute output paths, using temporary siblings and atomic replacement. Include `schema_version=1.0`, request targets, report identity, source hash, tool/method provenance, native evidence, visual evidence, unresolved items, validations, and warnings.

Every important evidence item includes page, human-readable location, original text/header, parsed value, unit, method, `approximate`, confidence when relevant, and period/header/unit validation.

Return a concise status, written paths, answered targets, unresolved targets, warnings, and vision usage. Delete task-temporary renders after persistence unless the parent explicitly authorizes retaining them as evidence.
