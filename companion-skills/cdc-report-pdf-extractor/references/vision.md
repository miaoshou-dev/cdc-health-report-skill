# Authorized visual processing

Use this reference only under `vision` authorization.

| Mode | Initial regions | Max total attempts/task | Confirmation | Failure behavior |
|---|---:|---:|---|---|
| `economy` | 0 | 0 | No | Return native result and task list |
| `balanced` | 3 | 2 | No | Skip excess; partial result after second failure |
| `complete` | All relevant | 2 | Confirm above 3 regions | Batch and stop failed tasks |

Default to balanced. A retry may increase resolution or widen a crop and must carry the first failure reason. Report candidate, executed, skipped, and retried task counts. Never render unrelated pages or pass the entire PDF as images.
