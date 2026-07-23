# COVID monthly fast path

version: 1.0.0
source_id: covid_monthly
parameters: year, month, latest, max_list_pages

1. Open the registered index and assert its URL and marker.
2. Parse anchors with the adapter title pattern and adjacent publication dates.
3. Match exact year/month; for latest validate all first-page records. Follow semantic pagination only when needed.
4. Open the unique HTML detail and assert the heading year, month, and report type.
5. Return the detail URL with `document_url=null`; extract from HTML only when authorized.
