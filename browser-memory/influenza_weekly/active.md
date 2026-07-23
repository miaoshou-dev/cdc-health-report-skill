# Influenza weekly parameterized path

version: 1.0.0
source_id: influenza_weekly
parameters: year, week, issue_number, latest, max_list_pages

1. Open `https://www.chinacdc.cn/jksj/jksj04_14249/`.
2. Assert the final URL is allowed and visible content contains `流感监测周报`.
3. Read official report anchors whose normalized text matches the registered influenza title pattern; parse title year, week, and issue, plus adjacent publication date.
4. Match the requested exact year+week or issue. For latest, inspect all valid first-page records and apply the latest-order anomaly checks.
5. When no exact match exists on the current page, follow the semantic `下一页` link, track visited canonical page URLs, and stop at `max_list_pages`.
6. Open the unique exact candidate and assert its heading reproduces report type, year, week, and issue.
7. Find every official attachment labeled as a file or ending in a supported document extension.
8. Require at least one allowed official PDF; return the HTML detail URL, PDF URL, normalized metadata, source page, and match method.

success_assertions:
- final host equals `www.chinacdc.cn`
- every navigated URL matches the registered allowed patterns
- candidate cardinality equals one for a successful exact query
- title fields equal the normalized query
- detail heading agrees with list title
- at least one allowed PDF attachment exists
