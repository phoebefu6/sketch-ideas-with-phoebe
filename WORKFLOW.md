# Visual Idea Workflow

This repo is the private-to-public pipeline for Phoebe Fu's visual explanations of data and AI
ideas. The goal is not just to make images. The goal is to build taste, sharpen ideas, and publish
visuals that make data people and executives say: "I have seen this problem at work."

## Operating Model

Phoebe now runs this work from the `sketch-ideas-with-phoebe` project.

Role split:

- Claude owns research, concept strategy, taste education, and high-level briefs.
- Codex owns visual direction, medium, layout, palette, typography, composition, image generation,
  design-build, critique, QA, publishing, and the final visual call.

Claude briefs should spark, not specify. Codex may reject, repair, or upgrade a brief if it does
not make visual sense.

## Intake

Grill before execution. Each new entry starts with a short intake or a Claude handoff brief:

- What is the data/AI concept?
- Who needs to understand it?
- What misunderstanding, decision, or tension should the visual expose?
- What should the viewer feel or do after seeing it?
- What format fits: comic, illustration, infographic, poster, carousel, card, cheatsheet, chart,
  ironic graph, map, matrix, zine, typographic, or style study?
- What part of any reference is worth learning from: layout, palette, composition, typography,
  texture, pacing, humor, metaphor, or material?
- What must stay private?
- What must be avoided?

## Maker Routing

Choose the maker by what the artifact is.

| Artifact type | Maker | Tool |
|---|---|---|
| Poster, infographic, diagram, cheatsheet, typographic, chart, matrix, data-art, exact text or layout | Design-build | HTML/CSS/SVG, rendered with Chrome |
| Rich illustration, painterly scene, comic, character, photo-like metaphor, style study | Image generation | Midjourney, ChatGPT image, Nano Banana |
| Ornate generative data-art | Code | SVG, D3, p5, or canvas |

Hard rule: if exact labels, hierarchy, grids, axes, or readable typography matter, do not rely on
text-to-image as the final artifact.

## Taste Loop

Every strong piece should teach Phoebe one reusable taste distinction.

Use `phoebe-design-partner` and the mandatory `impeccable` references before visual work. A final
artifact must pass the design gate:

- one dominant visual idea;
- clear mapping from mark to meaning;
- strong hierarchy;
- purposeful palette;
- typography integrated into the composition;
- no generic AI visual cliches;
- no pasted-on headline pretending to be design.

If the work is not a design, say so and rebuild.

## Working Loop

1. Read the brief, reference, or concept.
2. Extract the concept mechanism and decision tension.
3. Choose the maker route.
4. Create private previews in `inbox/previews/YYYY-MM-DD-slug/`.
5. Build 1-5 distinct directions when exploration is needed.
6. Render, inspect, and run the taste gate.
7. Phoebe chooses the final.
8. Publish only after explicit approval.

## Privacy

Private reference material belongs in ignored folders:

- `inbox/` for dropped screenshots, rough notes, temporary files, and private previews.
- `private/` for source attribution, client-sensitive context, and rejected prompt drafts.

Use `inspired_by` in `meta.yml` only when the attribution is safe to publish.

## Publish Contract

Each public work lives in one folder:

```text
works/YYYY-MM-DD-short-slug/
  full.png
  meta.yml
  idea.md
  sheet.html   # optional source for design-built work
```

Run before publishing:

- render and visually inspect the final image;
- `node /Users/phoebe.fu/.claude/skills/impeccable/scripts/detect.mjs --json <html-or-dir>`;
- check for placeholders, unfinished notes, typos, clipping, and em dashes;
- `python3 scripts/build.py`;
- `python3 scripts/qa_pages.py`;
- `git diff --check`.

Standalone HTML pages must be flexible on screen and precise only for export. Keep `html` and
`body` scrollable on screen. Fixed poster dimensions belong inside a stage/sheet wrapper, not by
locking the viewport with `overflow: hidden`.

## Prompt Safety

Mimic style mechanics, not identity. Describe observable design choices instead of copying a living
artist, brand system, exact character, exact poster, or copyrighted composition.

For visual idea-sparking, browse [Midlibrary Art Styles](https://midlibrary.io/art-styles) to expand
the vocabulary of possible art directions. Use it to identify mechanics like medium, era,
composition, texture, palette, lighting, printing method, and mood. Do not copy an exact artist,
brand, copyrighted composition, or living-artist identity.

## Default Tools

- Design-build: Codex authors HTML/CSS/SVG and renders with Chrome.
- Midjourney: Phoebe or Codex uses Discord/browser for raster-first style or illustration work.
- ChatGPT image/OpenAI image: use the installed `imagegen` workflow for raster-first work.
- GitHub: commit and push directly only after Phoebe approves the final.

## Daily Visual Intelligence

The repository includes `skills/publish-visual-intelligence/` for source-backed candidate ingestion
and approved publishing.

- Run daily at 21:00 Asia/Singapore.
- Create reviewable candidates first.
- Never generate or publish unapproved candidates.
- Run the QA specialist gate before publishing.
