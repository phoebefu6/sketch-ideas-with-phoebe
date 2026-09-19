# Project Memory

Updated: 2026-09-19

## Mission

`sketch-ideas-with-phoebe` is Phoebe Fu's "Worth a Thousand Words" gallery: data and AI ideas
explained through visuals with strong concept, strong taste, and reusable prompts or source files.
This supports Phoebe's personal brand in the "Let Data Talk" domain.

## Current Operating Model

Phoebe will run this workflow in the `sketch-ideas-with-phoebe` project going forward.

- Claude is the idea kitchen: research, concept strategy, taste vocabulary, and high-level brief.
- Codex is the design studio: visual direction, creative interpretation, build, image generation,
  critique, QA, and publishing.
- Codex should challenge Claude if the brief is weak, generic, visually impossible, too literal,
  or over-constrained.

## Standing Creative Mandate (Phoebe, 2026-09-19)

Her words, after the hand-drawn iceberg landed: *"the styles are getting better and better...
now i can start to see some styles and creative designs. make it more bold and creative! i want
to try everything! so impress me every time you design, sketch or create."*

This is a standing instruction on every visual, not a note about one piece.

- **Bold is the floor, not the ceiling.** A competent, safe, legible sheet is a failure state here.
  If the direction could have been produced by any decent designer working from the same brief,
  it is not finished.
- **Try everything.** Rotate the register hard: medium, era, printing method, material, grammar.
  A style used twice in a month needs a reason. Reach for the ones not yet attempted - collage,
  risograph, engraving, papercraft, woodblock, zine, specimen plate, map, schematic, embroidery,
  typographic-only - before reaching for a familiar win.
- **The style must do argument work.** The best pieces so far are the ones where the medium's own
  rule carries the claim: style 10 allows exactly one saturated accent, so the accent was spent on
  the part of the incident that got quoted, and the argument is visible before a word is read.
  Decoration that does not carry meaning is the thing to cut.
- **Impress, every time.** Ship something she has not seen from this gallery before - a mechanism,
  a material, a structural joke, a scale reveal. One surprise per piece, minimum.
- **The two-second test still binds.** Bold is not noisy. The concept still has to land instantly;
  restraint is what makes a bold choice readable rather than busy.

## Design Principle Learned

Design is not a generated image with a headline pasted on top.

A real design has an authored system:

- one dominant visual idea;
- clear mapping from marks to meaning;
- disciplined hierarchy;
- type that belongs to the composition;
- color with a job;
- enough restraint that the idea lands in two seconds.

## Maker Routing Memory

- Posters, infographics, diagrams, cheatsheets, typographic pieces, chart-like work, exact text,
  exact labels, and data-art should be design-built in HTML/SVG and rendered.
- Image generation is reserved for raster-first illustration, painterly/comic scenes, style studies,
  or photo-like metaphor work where exact layout and text are not the core.
- Midjourney and ChatGPT image are idea/style tools, not reliable layout engines.

## Current Quality Bar

Do not ship low-quality visual work just because it exists. If it does not feel like design,
say so, diagnose it, and rebuild.

Useful self-test:

- Can the viewer understand the concept in two seconds?
- Does every visual mark have one meaning?
- Would a data/AI person respect the mechanism?
- Would an executive remember the metaphor?
- Does it avoid obvious AI-image cliches?
- Is the final artifact something Phoebe would be proud to attach to her name?

## Style Lessons

### 2026-09-19 - the medium's own rule as the argument

"The part below the line" (METR agent incident). Routed through `phoebe-design-partner` to the
`hand-drawn` pack, style 10 `情绪叙事淡彩速写`, whose discipline is loose indigo line, roughly two
thirds white paper, and exactly ONE saturated accent in the whole picture. Spending that single
accent on the small exposed tip made the argument - the loud, quoted half of the incident - visible
before any label is read. The submerged mass stays pale line work and carries the four ordinary
causes.

Built locally as seeded SVG rendered headless, not generated, after the image backend hit its
usage limit. Two upsides worth keeping: the type is real type so no label can garble, and the
geometry is reproducible from `build_handdrawn.py`. Three passes were needed - a label ran off
frame, the below-water text overflowed the ice, and the peak first read as a cartoon mountain
range. Generated or drawn, the visual still has to be read back and fixed.

Lesson: pick the style whose native constraint IS the claim, then obey it strictly. A one-accent
style makes you decide what the one thing is, and that decision is the design.

### Earlier - measure the metaphor

For "You approved the number. You inherited the shadow", the winning direction was a measured
forecast-shadow system: a crisp point estimate, a widening interval fan, a time grid, and one
accent marker showing where the business commitment actually lands.

Lesson: a familiar metaphor becomes fresh when it is measured. "Shadow" alone is cliche.
"Shadow as prediction interval on a ruled horizon" is design.

## Paths

- Real Codex repo: `/Users/phoebe.fu/Documents/Codex/sketch-ideas-with-phoebe`
- Live gallery: `https://phoebefu6.github.io/sketch-ideas-with-phoebe/`
- Claude briefs: `/Users/phoebe.fu/Documents/Codex/sketch-ideas-with-phoebe/private/briefs`
- Private previews: `/Users/phoebe.fu/Documents/Codex/sketch-ideas-with-phoebe/inbox/previews`
- Style DB: `/Users/phoebe.fu/Documents/Claude_Work/project/sketch_ideas/style_db`

## Publishing Trap Found 2026-09-19

CI on this repo regenerates the gallery data from **what is committed**. Four finished works
(retry-storm, 820-billed-turns, the-price-of-a-word, centralize-decentralize-repeat) sat built but
uncommitted for up to two weeks, and a CI "regenerate gallery" commit quietly stripped them from
`data/works.json` - the site showed 14 works while the local build had 19. Nothing errored.

Rule: a work that is finished and approved gets committed and pushed the same day. Local build
output is not publication, and an uncommitted work will be deleted from the site by the next CI
run without anyone being told.

## Publish Rule

Private preview first. Publish only after Phoebe chooses a final and explicitly says to publish,
push, or go.

Final publish must include:

- final image;
- prompt or design-built recipe;
- key concept;
- takeaway for data/AI people;
- source or inspiration only when safe.
