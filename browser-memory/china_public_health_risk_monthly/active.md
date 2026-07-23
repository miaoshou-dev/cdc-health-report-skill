# China public-health risk monthly fast path

version: 1.0.0
source_id: china_public_health_risk_monthly
parameters: year, month, latest, max_list_pages

1. Open the registered index and assert its URL and marker.
2. Parse direct PDF anchors with the adapter title pattern and adjacent publication dates.
3. Match exact year/month; for latest validate all first-page records. Follow semantic pagination only when needed.
4. Assert the unique PDF URL is allowed and return it with `detail_url=null`.
5. Use the index URL as Referer if download is authorized.
