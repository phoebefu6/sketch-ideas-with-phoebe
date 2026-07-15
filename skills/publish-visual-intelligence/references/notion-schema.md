# Notion contract

## Destination

- Database: [Visual Intelligence Queue](https://app.notion.com/p/09116190123a4a0f8e6f847fb5847e11)
- Data source: `collection://52f37cd9-efcd-4b8d-80d3-c7c28031e04f`
- Parent: [sketch-ideas-with-phoebe](https://app.notion.com/p/39ef64f699d980c992c5fa39b5d329df)
- Related Content Ideas: `collection://08fe8f44-9d6a-41c8-a26b-8e02da695faf`
- Related Content Calendar: `collection://ebfe7fbc-0323-4204-818c-42be3260ade1`

Always fetch the database before writes because its schema may evolve.

## Required fields for new candidates

- `Idea`: concise source-specific title
- `Status`: `New`
- `Captured At`: current date/time
- `Source Published At`: source timestamp when available
- `Source Type`
- `Source Channel`
- `Source URL`
- `Source Fingerprint`
- `Topics`
- `Summary`
- `Key Insight`
- `Evidence`
- `Visual Thesis`
- `Visual Format`
- `Visual Direction`
- `Rank Score`: 0–100
- `Confidence`: 0–100

## Publishing fields

- `Generation Prompt`
- `Repository Slug`
- `GitHub URL`
- `Last Error`

Use `Generated Asset` only when an upload or attachment ID is available. Never invent attachment IDs.

## Deduplication

Query by exact `Source Fingerprint` before creating a page. If exact matching is unavailable, query the source URL and verify manually. Do not create a second record for the same video, article, podcast episode, or paper.

## Status ownership

- Automation may create `New`, move `Generating` to `Published`, or set `Error`.
- The user owns the transition to `Approved`.
- Automation must never set `Approved`.
