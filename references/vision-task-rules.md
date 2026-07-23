# Visual processing rules

Run a visual task only when all are true: `vision` is authorized; the region is relevant to the user's question; native extraction cannot answer it; it is not decorative; and budget remains.

## Task behavior

- OCR preserves reading order and uncertainty; never fill missing text.
- Image-table extraction preserves row/column structure, headers, footnotes, raw strings, and validation totals.
- Chart extraction identifies title, chart type, axes, units, legend, series, labeled values, and source location.
- Unlabeled curves produce only approximate values with confidence and error notes.
- Send the smallest useful crop, not the whole PDF or unrelated pages.
- Keep visual results alongside native evidence and mark conflicts; never overwrite native evidence.

## Sole budget table

| Mode | Initial regions | Maximum total attempts per task | Confirmation | Failure |
|---|---:|---:|---|---|
| `economy` | 0 | 0 | No | Return native result and skipped tasks |
| `balanced` | 3 | 2 | No | Skip excess; return partial after second failure |
| `complete` | All relevant | 2 | Confirm if more than 3 regions | Batch; do not loop failures |

Default to `balanced`. A retry may raise render detail or widen the crop and must include the first failure reason. Report candidate count, executed count, skipped reasons, retry count, budget mode, and whether the result is partial.
