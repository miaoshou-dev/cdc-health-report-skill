# China CDC Health Report Skill PRD

Version: 2.0

## 1. Purpose

Provide a Codex Skill that locates, verifies, optionally downloads, and extracts five registered official China CDC report series:

1. China influenza weekly reports;
2. acute respiratory infectious-disease sentinel weekly reports;
3. national COVID-19 monthly updates;
4. global infectious-disease event risk assessments;
5. China key-infectious-disease/public-health-emergency risk assessments.

The Skill is not a medical-advice, prediction, web-search, or third-party-report tool.

## 2. Product principles

- Official sources only: `https://www.chinacdc.cn/`.
- Adapter-driven: each source declares its entry URL, title grammar, period, carrier, markers, and URL boundary.
- Stateless browsing: no browser execution path, page state, candidate, snapshot, or learned route is persisted.
- Native-first extraction: text and native tables precede visual interpretation.
- One parsing artifact: extraction produces only `extracted.json`.
- Explicit source retention: save a source PDF only when the user explicitly asks to download it.
- Minimum authorization: locate by default; reading authorizes native extraction; vision requires explicit intent.

## 3. Supported actions

### Locate

Return verified report metadata and official URLs. Do not write files.

### Download

For PDF-capable sources, save the verified official PDF only after an explicit download request. Use the repository downloader; never use browser PDF controls or an ad hoc transfer.

### Extract

- HTML: persist main text, DOM tables, figure titles, and image URLs in `extracted.json`.
- PDF: obtain the verified PDF temporarily unless download was requested, parse every physical page, and persist `extracted.json`.
- Do not save raw HTML, page snapshots, source PDF during extract-only work, or any separate evidence output.

### Vision

Vision is an extension of PDF extraction. Process only user-relevant pages already listed in `vision_pages`, update the same `extracted.json`, and remove temporary renders.

## 4. Source model

`references/source-registry.md` maps aliases to exactly one adapter. Each adapter contains:

- stable source ID and display name;
- official index URL and allowed path prefix;
- weekly or monthly period type;
- `html`, `pdf`, or `html_with_pdf` carrier;
- anchored title pattern;
- semantic pagination declaration;
- supported selectors;
- index marker and allowed URL patterns.

Adapters contain no report content, runtime history, browser trace, extraction output, or authorization state.

## 5. Browser behavior

For every query:

1. open a fresh isolated agent-browser session;
2. start from the selected adapter's `index_url`;
3. verify host, allowed path, and index marker;
4. parse titles and publication dates;
5. follow semantic pagination, tracking task-local visited URLs;
6. identify one exact report;
7. verify its detail page or direct document carrier;
8. close the session.

Use ordinary HTTP only after a recorded browser page-access failure and apply identical URL and content checks. Never expand an adapter's permission boundary or persist a recovered route.

## 6. Matching behavior

- Validate weeks, months, issues, dates, and conflicting selectors before browsing.
- Derive reporting period and issue from the official title.
- Keep publication date distinct from reporting period.
- Require exact period, issue, or publication-date matches.
- For `latest`, inspect every valid first-page record.
- Search at most eight list pages for one query.
- Do not report `not_found` for a technical failure.

## 7. Artifact model

The only valid report-directory files are:

```text
artifacts/<report-id>/
├── extracted.json
└── <verified-source-name>.pdf   # explicit download only
```

`locate` creates no directory. `extract` writes only `extracted.json`. `download` may write only the official PDF. A combined request may produce both.

PDFs used for extract-only work and all visual renders live in a task-temporary directory and are deleted after success or failure.

## 8. Extraction schema

`extracted.json` uses schema version `2.0` and contains:

```json
{
  "schema_version": "2.0",
  "report": {},
  "pages": [],
  "content": null,
  "vision_pages": [],
  "warnings": []
}
```

### PDF

`pages` contains exactly one ascending record per physical page:

```json
{
  "page": 1,
  "text": "",
  "tables": [],
  "visuals": [],
  "requires_vision": true
}
```

`vision_pages` is the unique ascending set of page numbers whose `requires_vision` is true. It replaces all richer unresolved-task and evidence models.

### HTML

`pages=[]`, `vision_pages=[]`, and:

```json
{
  "content": {
    "text": "",
    "tables": [],
    "images": [{"title": "", "url": ""}]
  }
}
```

## 9. Failure statuses

Use:

`success`, `invalid_query`, `ambiguous`, `not_found`, `search_budget_exceeded`, `source_unavailable`, `browser_unavailable`, `tool_environment_error`, `detail_unverified`, `artifact_store_unavailable`, `download_failed`, `extractor_unavailable`, `extraction_partial`, `vision_budget_exceeded`, or `internal_error`.

Page-structure failures map to source or detail verification failures. There are no browser-learning or route-update statuses.

## 10. Acceptance criteria

- All five registered sources remain locatable through their adapters.
- Locate creates no file.
- Extract creates only `extracted.json`.
- Explicit download retains a verified PDF.
- Extract-only PDF work deletes the temporary source.
- PDF extraction emits one ordered record per physical page.
- Native-unreadable relevant pages are represented only by `requires_vision` and `vision_pages`.
- Vision updates the same file and leaves no rendered intermediates.
- HTML extraction retains parsed content but no raw page data.
- No browser state or execution trace is persisted.
- Repository validation rejects legacy memory, separate evidence outputs, and old route-learning rules.
