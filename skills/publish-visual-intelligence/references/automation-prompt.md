# Scheduled job prompt

Use `$publish-visual-intelligence` from `skills/publish-visual-intelligence/SKILL.md` to run the daily review-first visual intelligence pipeline for this repository.

1. Read the skill and all references it requires.
2. Open the signed-in YouTube subscriptions feed at `https://www.youtube.com/feed/subscriptions` using the supported browser surface.
3. Inspect at most 30 items from the previous successful run, with a 48-hour fallback window.
4. Deduplicate each item against the Notion Visual Intelligence Queue using `Source Fingerprint`.
5. Create at most 10 strong, source-backed candidates with `Status = New`. Never approve them.
6. Query the queue for `Status = Approved`. If present, process at most the highest-scoring one using the approved-generation workflow.
7. Never generate or publish a `New` or `Triaged` item.
8. Validate repository output using `WORKFLOW.md`, `taxonomy.yml`, `scripts/build.py`, JSON validation, thumbnail inspection, and `git diff --check`.
9. Commit and push only validated, approved output. Update the Notion record to `Published` with its GitHub URL.
10. Return a compact summary: discovered, deduplicated, created, approved processed, published, skipped, errors, and direct Notion links.

If YouTube is signed out, do not guess the feed. Report the authentication block and leave repository and Notion publication state unchanged.
