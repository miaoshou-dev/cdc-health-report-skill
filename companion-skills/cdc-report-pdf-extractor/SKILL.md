---
name: cdc-report-pdf-extractor
description: Extract every physical page of an already-located and authorized official China CDC PDF into one extracted.json file. Preserve native text and tables, record only page numbers that require visual interpretation, and process those pages only with explicit vision authorization. Do not locate reports, download other issues, compare periods, or persist evidence, screenshots, crops, page maps, or visual-task files.
---

# CDC Report PDF Extractor

## Accept one bounded handoff

Require an absolute local PDF path, normalized report metadata, one absolute `extracted.json` output path, and authorization `extract` or `vision`. The verified source URL and SHA-256 are optional provenance.

Reject non-PDF input, paths outside the supplied task or Artifact roots, authorization below `extract`, and requests to expand the supplied report or target.

## Extract every page natively

Use the bundled PDF runtime. Prefer `pdfinfo`, `pdftotext`, `pypdf`, and `pdfplumber`; do not install packages without approval.

Process every physical page in ascending order, including covers, empty pages, and image pages. For each page write:

```json
{
  "page": 1,
  "text": "",
  "tables": [],
  "visuals": [],
  "requires_vision": false
}
```

- Preserve readable native text without guessing missing characters.
- Reconstruct native tables from characters and vector borders where practical.
- Preserve table titles, headers, rows, footnotes, units, and original strings.
- Attach concise warnings for garbled text, uncertain order, or inconsistent values.
- Do not build or persist a separate page map, bbox evidence, or extraction ledger.

Set `requires_vision=true` only when visually encoded content on that page is relevant and cannot be read natively. Set top-level `vision_pages` to the unique ascending list of those page numbers. Do not create richer unresolved tasks.

## Run authorized vision

Without `vision` authorization, stop after native extraction. With authorization, inspect only target-relevant pages already in `vision_pages`, using the smallest useful temporary render.

Write visual results into that page's `visuals`. Preserve titles, axes, units, legends, labels, and table structure. Mark estimated chart values with `approximate=true`. When a page is fully resolved, set `requires_vision=false`; otherwise keep it in `vision_pages` and add a concise warning.

Never save screenshots, crops, OCR files, or visual-task records. Remove temporary renders after success or failure.

## Persist one file

Atomically write one schema-version `2.0` `extracted.json` containing `report`, `pages`, `content=null`, `vision_pages`, and `warnings`. Return status, output path, page count, vision page numbers, and warnings.
