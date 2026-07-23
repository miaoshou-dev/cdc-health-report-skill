# Parameterized browser script contract

## Parameters

Every source script declares only applicable fields from:

```text
report_type, year, week, month, issue_number, publish_date,
reference_date, latest, max_list_pages
```

Default `max_list_pages=8` for one report. Validate all values before substitution.

## Stable operations

Use semantic operations such as:

- Open the registered index URL.
- Confirm final host and index marker.
- Read report anchors whose text matches the anchored title pattern.
- Follow `下一页`, `尾页`, or numeric pagination relations.
- Open an exact candidate by its verified canonical URL.
- Find attachments by semantic label, extension, and official URL.

Do not save `@eN`, XPath tied to incidental layout, CSS class hashes, screen coordinates, cookies, authentication, profiles, complete snapshots, or full reasoning.

Execute index/detail operations through a unique isolated agent-browser session first. Use ordinary HTTP for index/detail recovery only after recording the failed browser step and assertion. Do not run browser and HTTP page-access paths speculatively in parallel.

For an authorized document download, use agent-browser only to verify the detail page, attachment label, allowed official `document_url`, and report identity. Close the session after capturing the verified URL and Referer. Invoke `scripts/download_official_document.py` for all document-byte transfer. Never open the Chrome PDF viewer, click its Download control, return a PDF through `eval`/Base64/screenshots/tool messages, or assemble an equivalent curl command ad hoc.

## Assertions

Require:

1. final host is `www.chinacdc.cn`;
2. every URL matches the adapter boundary;
3. index marker or exact report title is present;
4. title-derived period/issue equals the query;
5. candidate cardinality has the expected value;
6. carrier routing matches `content_mode`;
7. HTML+PDF results include a verified official PDF.

## Bootstrap input/output

Input: adapter, normalized query, current page's minimum relevant link/pagination structure. Output: a candidate `active.md` following this contract. Write only after all deterministic security and success checks pass.

## Recovery input/output

Input only: query parameters, current script, failed step, failed assertion, minimum relevant snapshot. Output: candidate script plus the assertion evidence. Preserve old active as the sole previous version before atomic replacement. Leave memory unchanged on failure.
