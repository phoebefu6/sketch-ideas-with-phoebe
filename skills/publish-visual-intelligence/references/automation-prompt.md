# Scheduled job prompt

Use `$publish-visual-intelligence` from `skills/publish-visual-intelligence/SKILL.md` to run the daily review-first visual intelligence pipeline for this repository.

1. Read the skill and all references it requires.
2. Query the Notion Sourcebase at `collection://4c4b2ddc-0ada-45eb-88af-a59b255e18d1` and scan each row once using its supported authenticated surface.
3. Use each row's `Latest Scan Date` as the lower bound, with a 48-hour fallback window. For video feeds inspect at most 30 items.
4. Deduplicate each item against the Notion Visual Intelligence Queue using `Source Fingerprint`.
5. Create at most 10 strong, source-backed candidates with `Status = New`. Never approve them.
6. Query the queue for `Status = Approved`. If present, process at most the highest-scoring one using the approved-generation workflow.
7. Never generate or publish a `New` or `Triaged` item.
8. Validate repository output using `WORKFLOW.md`, `taxonomy.yml`, `scripts/build.py`, JSON validation, thumbnail inspection, and `git diff --check`.
9. Commit and push only validated, approved output. Update the Notion record to `Published` with its GitHub URL.
10. Return a compact summary: discovered, deduplicated, created, approved processed, published, skipped, errors, and direct Notion links.

Update a source row's `Latest Scan Date` only after its scan succeeds. If a source is signed out or unavailable, do not guess its content; report the block and leave its scan date unchanged.
