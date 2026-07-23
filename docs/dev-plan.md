# China CDC Health Report Skill v2 Development Plan

## 1. Runtime contract

- Refactor the main Skill to start every browse from the selected adapter.
- Remove all persisted browser-state and route-learning behavior.
- Keep the five adapters as the only source-specific navigation configuration.
- Preserve browser-first access, scoped HTTP fallback, exact title matching, and carrier verification.

Exit condition: all five sources can be located without reading or writing browser state.

## 2. Artifact and extraction contract

- Keep the secure PDF downloader for explicit downloads.
- Use a task-temporary output directory for extract-only PDF transfers and clean it in all exit paths.
- Persist extraction only to `artifacts/<report-id>/extracted.json`.
- Implement schema v2 for PDF pages and HTML content.
- Simplify the companion extractor to process every PDF page and derive `vision_pages`.

Exit condition: locate writes nothing; extract writes one JSON; download may additionally retain one verified PDF.

## 3. Visual processing

- Treat `vision_pages` as the complete visual-work queue.
- Require explicit vision authorization.
- Process only target-relevant queued pages.
- Write results into the matching page's `visuals`.
- Recompute `requires_vision` and `vision_pages`.
- Remove every render and crop.

Exit condition: visual processing creates no second artifact and failed pages remain discoverable.

## 4. Documentation and validation

- Align the PRD, workflow, schemas, extraction rules, and regression cases with v2.
- Remove legacy browser-state files and references.
- Update structural validation to enforce five adapters, schema v2, one parsing artifact, downloader safety, and absence of legacy concepts.
- Retain the frozen report identities and matching regression matrix.

Exit condition: repository-wide searches find no legacy memory, route-learning, or separate evidence contract in tracked runtime/design files.

## 5. Tests

1. Run deterministic repository validation.
2. Run downloader unit tests.
3. Validate all five adapter declarations.
4. Validate the frozen 19-page PDF output shape when the optional sample exists.
5. Test `vision_pages` ordering, uniqueness, and page consistency.
6. Test HTML output shape.
7. Test Artifact counts for locate, extract, download, and combined actions.
8. Test temporary cleanup on success and failure.

Release requires every check to pass and no unreviewed runtime Artifact to remain.
