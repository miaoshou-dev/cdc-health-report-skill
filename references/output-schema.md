# Output protocol

Schema version: `1.0`.

## Status

Use one primary status:

`success`, `invalid_query`, `ambiguous`, `not_found`, `search_budget_exceeded`, `source_unavailable`, `browser_unavailable`, `tool_environment_error`, `detail_unverified`, `bootstrap_failed`, `self_heal_failed`, `artifact_store_unavailable`, `download_failed`, `extractor_unavailable`, `extraction_partial`, `vision_budget_exceeded`, or `internal_error`.

## JSON

```json
{
  "schema_version": "1.0",
  "status": "success",
  "query": {},
  "match_method": "exact_period",
  "report": {},
  "candidates": [],
  "source": {"id": "influenza_weekly", "index_url": "https://..."},
  "artifacts": [],
  "evidence": [],
  "unresolved": [],
  "warnings": [],
  "next_actions": ["download", "extract", "vision"]
}
```

Omit neither `warnings` nor `next_actions`; use empty arrays. On non-success, keep verified partial report/candidates when safe and add a concise recovery action. Do not place approximate candidates in `report`.

## Text

State status first. On success, include report name, reporting period, issue number if present, publication date, detail/document URLs, attachments, match method, and source. Then state what was not done under the authorization boundary and offer permitted next actions. On failure, distinguish no data from technical failure and give one actionable next step.
