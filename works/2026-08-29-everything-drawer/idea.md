# The everything drawer

## Key Concept

People argue about whether "the model knows things," "remembers them," "wants things" - and
the argument stays stuck because nobody opens the drawer. So open it: an LLM's entire
contents, laid out in full, is billions of numerical weights and the wiring between them.
That is the complete inventory. No facts database. No memory of your last conversation. No
intent. The three things everyone assumes are in there were never fitted - and the system
works anyway, which is the genuinely strange part worth sitting with.

## Explanation

The piece borrows the reverence of a museum flat-lay - the entire contents of one immense
specimen drawer photographed overhead, every object sharp, half knolled into rows and half
collapsed into piles. Watch-part weights stand in for the model's weights ("billions of
small numbers - this is all there is"), softened punch cards for training traces
("compressed impressions of the text it read - never the text itself"), copper wire for
connections ("meaning lives in the wiring, not in any single part"), paper tape for output
("one token at a time").

The argument is carried by what is NOT there. Three rectangles are taped off on the drawer
felt, empty, each stamped in the piece's only red: **FACTS DATABASE - never fitted. MEMORY
OF YOUR LAST VISIT - never fitted. INTENT - never fitted.** This is the wall's
composed-absence move (an omission looks like a mistake; a measured absence reads as
evidence): the voids were reserved at generation time, taped like museum lots awaiting
specimens that never existed.

Why it matters practically: every one of the three voids is a product decision someone bolts
on later - retrieval for facts, session state for memory, guardrails and objectives for
intent. Knowing they are add-ons, not innards, is the difference between evaluating a model
and evaluating a system.

Terminal line, set like a collection label: **there is no mind in the drawer. It works anyway.**

## Recipe

HYBRID. Hero: codex image_gen, portrait 3:4, first attempt - full prompt in
`prompts/01-hero-drawer.md`. The load-bearing instruction is the three taped empty
rectangles "large enough to hold something that is not there," plus the corner-to-corner
no-empty-background rule and the individually-refused lettering list. The drawer rail with
brass handles was requested as a plain top strip - it became the natural mount for the
title plate.

Type layer: museum register - aged-paper specimen tags (Archivo Narrow headings, pinned with
a drawn grommet), a brass-gradient title plate on the rail, IBM Plex Mono small print, and
stamped red `#A63A2B` NEVER FITTED chips inside the voids. Hand-authored HTML
(`poster.html`), rendered headless Chrome at 1086x1448 @2x. Two registration rounds - the
first void's label needed one nudge down into its tape.
