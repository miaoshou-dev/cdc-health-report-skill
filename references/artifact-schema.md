# Artifact store

Write only after `download` or higher authorization.

```text
artifacts/<report-id>/
├── source.<ext>
├── extracted.json
└── evidence.json
```

Only create files authorized by the action. `download` creates `source.<ext>` only. Use an absolute Artifact root. If absent, resolve `<skill-root>/artifacts`. Do not use an application data directory as fallback.

Download filename before placement: weekly `{report_type}_{year}_W{week:02}_{issue|NA}_{sha256_8}.{ext}`; monthly `{report_type}_{year}_M{month:02}_NA_{sha256_8}.{ext}`. Use ASCII. Verify size > 0, type/magic, extension, final official URL, and SHA-256. Reuse identical content. If a different file collides, append `_2`, `_3`, and so on; never overwrite.

Use agent-browser to verify the report identity, attachment label, official `document_url`, and detail-page Referer, then close the session without opening the PDF viewer. Run every authorized document transfer with `scripts/download_official_document.py`. Do not transfer document bytes through browser download controls, `eval`, Base64 chunks, model context, screenshots, or ad hoc curl commands.

Supply the script with the verified document URL, verified detail-page Referer, adapter `allowed_path_prefix`, absolute report Artifact directory, report type, year, exactly one week/month, and issue when applicable. The script ignores proxy environment variables, supplies a stable browser User-Agent and Referer, applies a bounded timeout and size limit, requires the official HTTPS host/path plus PDF content type and magic, computes SHA-256, reuses identical files, and adds a numeric suffix on content collision. Consume its JSON stdout.

Persist JSON atomically and include `schema_version`, source URL, SHA-256, creation natural datetime with timezone, authorization level, and tool/method provenance. Treat existing `artifacts/` as protected during install/upgrade. Tell users they may delete a report directory to clean its saved data.
