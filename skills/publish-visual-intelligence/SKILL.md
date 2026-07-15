---
name: publish-visual-intelligence
description: Crawl configured data and AI sources, extract source-backed insights, route ideas into visual formats, populate the Notion Visual Intelligence Queue, and publish approved visuals to the sketch-ideas-with-phoebe gallery. Use for daily source monitoring, YouTube talk analysis, visual candidate triage, cheatsheets, mind maps, infographics, charts, comics, posters, carousels, cards, ironic graphs, illustrations, logos, style studies, and the repository publishing workflow.
---

# Publish Visual Intelligence

Turn trusted source material into reviewable visual ideas and publish only approved work.

## Read first

- Read `references/sources.md` before crawling.
- Read `references/notion-schema.md` before querying or writing Notion.
- Read `references/format-routing.md` before selecting a visual format.
- Read the repository `WORKFLOW.md`, `taxonomy.yml`, and `templates/` before publishing.

## Choose a mode

### Daily ingest

Use for scheduled runs.

1. Open each configured source using its supported authenticated surface.
2. Collect items published since the previous successful run, with a 48-hour fallback window.
3. Canonicalize each URL with `scripts/source_fingerprint.py`.
4. Query Notion for the fingerprint. Skip existing records.
5. Extract title, channel, publication time, summary, key topics, evidence, and the strongest visual thesis.
6. Score the candidate:
   - data/AI relevance: 0–30
   - visual potential: 0–25
   - evidence quality: 0–20
   - novelty against the gallery: 0–15
   - freshness: 0–10
7. Route the candidate using `references/format-routing.md`.
8. Create a Notion record with `Status = New`.
9. Never generate an image, create repository files, commit, or push a `New` or `Triaged` item.
10. Report counts for discovered, deduplicated, created, skipped, and errored items.

### Approved generation and publish

Use manually or during a scheduled run after ingestion.

1. Query records with `Status = Approved`, highest `Rank Score` first.
2. Process at most one approved record per scheduled run.
3. Re-open the source and verify every material claim. Record timestamps or links in `Evidence`.
4. Set `Status = Generating`.
5. Generate the selected format:
   - use code-native SVG/HTML/PlantUML for deterministic charts, mind maps, and diagrams when appropriate;
   - use the image-generation workflow for illustrated or raster-first formats;
   - preserve exact source-backed wording and minimize text inside generated images.
6. Inspect the final visual for legibility, factual accuracy, spelling, copyright risk, confidential details, and unsupported likenesses.
7. If validation fails, set `Status = Error`, write `Last Error`, and do not publish.
8. If validation passes, create the repository work folder using the publish contract below.
9. Run `python3 scripts/build.py`, validate generated JSON, inspect the thumbnail, and run `git diff --check`.
10. Commit only the scoped work and generated gallery files, then push according to repository policy.
11. Set `Status = Published`; populate `Repository Slug`, `GitHub URL`, and the final prompt.

## Review-first policy

Treat `Approved` as the only authorization to generate and publish. Do not infer approval from a high score, a previous approval, a scheduled run, or a visually promising source.

Status flow:

`New → Triaged → Approved → Generating → Published`

Use `Skipped` for intentional rejection and `Error` for operational failures. Do not silently move an item into `Approved`.

## Source integrity

- Keep facts traceable to the source URL.
- Prefer primary sources, complete talks, official transcripts, papers, and first-party data.
- Separate the speaker's claim from the workflow's inference.
- Do not quote more source text than needed.
- Deduplicate by fingerprint before semantic comparison.
- When authentication is missing, stop that source, preserve other in-scope work, and report the sign-in requirement.

## Repository publish contract

Create exactly:

```text
works/YYYY-MM-DD-short-slug/
  full.png
  meta.yml
  idea.md
```

Allow the repository build to create `thumb.webp` and generated catalog files. Store the public source URL in `inspired_by` only when safe. Include the final OpenAI prompt and a reusable Midjourney prompt track in `idea.md`.

## Automation behavior

For the 21:00 Asia/Singapore daily run:

1. Run Daily ingest.
2. Process at most one already-approved record.
3. Leave all new candidates awaiting review.
4. Never publish solely because the automation ran.
5. Return a compact run summary with direct Notion links and any authentication or validation failures.
