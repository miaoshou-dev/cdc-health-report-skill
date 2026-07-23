# PDF deterministic extraction contract

This reference defines the handoff to the separately installed `cdc-report-pdf-extractor` Skill. `extract` authorization allows native inspection and extraction; only `vision` allows OCR or image/chart interpretation.

## Native-first sequence

1. Inspect per-page text presence/character quality, images, vector lines, table/chart candidates, and scan/cover status.
2. Prefer `pdfinfo`, `pdftotext`, `pypdf`, and `pdfplumber` available in the bundled runtime.
3. Extract text with page, blocks, reading order, bbox, original string, and method.
4. Reconstruct character/vector tables programmatically; retain raw and parsed values, units, counts, percentages, headers, and footnotes.
5. Validate row/column totals, percentage bounds/totals where meaningful, period, header, and unit.
6. Emit an `unresolved` item only when native evidence cannot answer a relevant target.
7. Do not render or OCR merely because a page contains an image.

## Evidence

```json
{
  "schema_version": "1.0",
  "request": {"targets": [], "period": null},
  "native_evidence": [{
    "page": 1, "location": "table_or_bbox", "original_text": "",
    "value": null, "unit": null, "method": "native_text",
    "approximate": false,
    "validation": {"period_match": true, "header_match": true, "unit_match": true}
  }],
  "unresolved": [],
  "warnings": []
}
```

An unresolved item includes `id`, `type`, `page`, optional image/bbox, `reason`, `requires_vision`, `relevance_tags`, `estimated_cost`, and `expected_output`. Identification does not authorize execution.

The frozen `P020260715815376876315.pdf` baseline has 19 pages; pages 2–18 have usable text, pages 1 and 19 are primarily images, tables on pages 4 and 13 are native-first candidates, and line charts are primarily images.
