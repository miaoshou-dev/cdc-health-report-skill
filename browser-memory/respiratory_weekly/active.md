# Respiratory weekly fast path

version: 1.0.0
source_id: respiratory_weekly
parameters: year, week, latest, max_list_pages

1. Open the registered index and assert its URL and marker.
2. Parse anchors with the adapter title pattern and adjacent publication dates.
3. Match exact year/week; for latest validate all first-page records. Follow semantic pagination only when needed.
4. Open the unique HTML detail and assert the heading year, week, and report type.
5. Return the detail URL with `document_url=null`.
