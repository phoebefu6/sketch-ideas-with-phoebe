# Visual Idea Workflow

This repo is a private-to-public pipeline for visual explanations of data and AI ideas.

## Operating Rule

Grill before execution. Each new entry starts with a short intake before prompts, images, or publishing:

- What is the data/AI concept?
- Who needs to understand it?
- What should the viewer feel or do after seeing it?
- What format fits this idea: comic, illustration, infographic, poster, carousel, card, cheatsheet, chart, ironic graph, logo, or style study?
- What part of the reference is worth learning from: layout, palette, composition, typography, texture, pacing, humor, or metaphor?
- What must stay private: source URL, screenshot, brand, person, client, or internal context?
- What must be avoided: living artist imitation, brand mimicry, exact likeness, copyrighted characters, confidential details, or text that must be perfectly typeset?

## Loop

1. Drop a wow reference into chat.
2. Extract the visual DNA: layout, palette, medium, composition, texture, type feel, pacing, and emotional effect.
3. Rewrite the content around an original data/AI concept for data people.
4. Produce two prompt tracks:
   - Midjourney for Discord/browser.
   - ChatGPT image/OpenAI image generation for this chat.
5. Generate candidates.
6. Choose one final image.
7. Publish the image, prompt, key concept, and takeaway to GitHub.

## Privacy

The public site should contain the final image, prompt, key concept, takeaway, tool, format, topics, and style notes.

Private reference material belongs in ignored folders:

- `inbox/` for dropped screenshots, URLs, rough notes, and temporary files.
- `private/` for source attribution, client-sensitive context, and rejected prompt drafts.

Use `inspired_by` in `meta.yml` only when the attribution is safe to publish.

## Publish Contract

Each work lives in one folder:

```text
works/YYYY-MM-DD-short-slug/
  full.png
  meta.yml
  idea.md
```

`full.png` may also be `full.jpg`, `full.jpeg`, or `full.webp`.

Run `python3 scripts/build.py` before publishing. The script creates `thumb.webp`, updates `data/works.js`, updates `data/works.json`, refreshes `CATALOG.md`, and rewrites the README gallery.

## Prompt Safety

Mimic style mechanics, not identity. Describe observable design choices instead of copying a living artist, brand system, exact character, exact poster, or copyrighted composition.

Good style extraction focuses on:

- composition and framing
- palette and contrast
- material and texture
- line quality and rendering medium
- rhythm, density, and visual hierarchy
- camera angle or panel structure
- mood and metaphor

Avoid:

- "in the style of [living artist]"
- exact logo or brand mimicry
- exact celebrity/person likeness
- copyrighted characters
- private company/client details
- hidden source links in public files

## Default Tools

- Midjourney: user runs the prompt through Discord/browser unless browser access is explicitly arranged.
- ChatGPT image/OpenAI image: generated in this chat with the installed `imagegen` workflow.
- GitHub: commit and push directly when the final image and metadata are ready.

## Daily Visual Intelligence

The repository includes `skills/publish-visual-intelligence/` for the automated research-to-visual pipeline.

- Run daily at 21:00 Asia/Singapore.
- Crawl the authenticated YouTube subscriptions feed and any later approved sources.
- Deduplicate and write source-backed candidates to the [Visual Intelligence Queue](https://app.notion.com/p/09116190123a4a0f8e6f847fb5847e11).
- Use a review-first gate: automation creates `New` records, but only the user may move them to `Approved`.
- Generate and publish at most one already-approved record per scheduled run.
- Never generate or publish unapproved candidates.
