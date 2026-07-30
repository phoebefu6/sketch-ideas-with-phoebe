# Sketch Ideas With Phoebe - Codex Instructions

This repo is the live gallery and build system for Phoebe Fu's visual explainers in the
"Let Data Talk" domain. Treat it as the durable home for the project.

## Start Here

- Read `PROJECT_MEMORY.md`, `WORKFLOW.md`, and `CATALOG.md` before making or publishing a work.
- Check `~/phoebe-skill-vault/INDEX.md` and use matching skills before acting.
- For visual work, use `phoebe-design-partner` and its mandatory `impeccable` taste gate.
- For gallery mechanics, use `sketch-engine`.

## Role Split

- Claude owns research, concept strategy, taste education, and high-level briefs.
- Codex owns visual direction, medium, layout, palette, typography, image generation, design-build,
  critique, QA, publishing, and the final call on whether a concept is visually strong enough.
- Claude briefs should not over-constrain art direction. Codex may reject or improve a weak brief.

## Maker Routing

- Use design-build HTML/SVG for posters, infographics, diagrams, cheatsheets, data-art,
  typography, exact text, exact layout, charts, and anything that needs precision.
- Use image generation only for raster-first illustration, painterly scenes, style studies,
  character/comic art, or photo-like metaphor work where exact text/layout is not the core.
- If a visual has exact words, labels, axes, grids, or hierarchy, do not rely on Midjourney or
  ChatGPT image generation as the final artifact.

## Design Bar

- Design is not image plus headline. Every finished piece needs an authored system:
  composition, hierarchy, typography, color roles, and one clear metaphor.
- Build multiple truly different routes when Phoebe asks for options. Vary metaphor, structure,
  palette, type, and medium, not just colors.
- Avoid generic AI tells: glowing robots, neural blobs, purple-blue gradients, dashboard chrome,
  stock-photo metaphors, pasted labels, and fake precision with no conceptual encoding.
- Teach taste as you go. Name what makes a design good or bad so Phoebe's eye improves.

## Private Previews

- Use `inbox/previews/YYYY-MM-DD-slug/` for temporary source files and rendered previews.
- `inbox/` is private and gitignored. Do not publish reference images, rejected routes, or private
  prompt drafts.

## Publish Contract

Publish only after Phoebe explicitly says to publish, push, or go with a selected final.

Each public work lives in:

```text
works/YYYY-MM-DD-short-slug/
  full.png
  meta.yml
  idea.md
  sheet.html   # optional editable source for design-built works
```

Before push:

- Render and inspect the final image.
- Run the impeccable detector on HTML/SVG artifacts.
- Check for placeholders, unfinished notes, clipping, typos, and em dashes.
- Run `python3 scripts/build.py`.
- Run `python3 scripts/qa_pages.py`.
- Confirm standalone subpages scroll naturally on desktop and mobile.
- Run `git diff --check`.

## Voice And Copy

- Warm practitioner, direct, specific.
- Hyphens only. Do not use em dashes.
- Publicly use "Phoebe Fu" only.
- Never guess private URLs, handles, clients, or source details.
