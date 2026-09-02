# Where does your data live?

## Key Concept

Data infrastructure vocabulary is a geography lesson nobody draws: lake, warehouse, mart,
lakehouse, mesh. Five architectures that get compared in feature tables - rows of "schema
on read" vs "schema on write" - when their own names already encode the real differences:
what each one stores, how structured it is, and who owns it.

The tension: these words are used daily by people who could not place them on a map, and
vendor decks profit from the fog. Taken literally, the metaphors are honest. A lake really
is where everything lands raw. A mart really is a small shop serving one neighborhood. A
lakehouse really is a house standing in the water.

## Explanation

One hand-drawn town, five locations, and the spatial relationships do the teaching:

- **DATA LAKE** - a pond with mismatched raw objects afloat: a file, a photo, a scroll,
  a music note. Nothing shelved, nothing labeled. Store first, decide later.
- **DATA WAREHOUSE** - the big central building with identical boxes in ordered rows.
  Structure is the product; everything inside was cleaned to earn its shelf.
- **DATA MART** - the corner shop *beside* the warehouse, deliberately smaller. A mart
  is a subset with a customer: one team's curated slice.
- **DATA LAKEHOUSE** - the house on stilts standing in the lake itself, tidy shelves
  visible through the window. The adjacency IS the definition: warehouse comfort built
  directly on raw lake storage.
- **DATA MESH** - the only "architecture" that is not a building. Four garden plots,
  each with its own well and its own gardener, connected by pipes. Ownership is drawn,
  not captioned: in the first four a central team owns the water; in the mesh, every
  domain does - and the pipes are the contracts.

The closing question the visual plants: not "which one is best" but "who owns the water
quality" - the actual axis the five architectures disagree on.

## Recipe

- **Pipeline**: baoyu-infographic - isometric-map layout x craft-handmade style, blended
  with traits extracted from Phoebe's pasted hand-drawn reference (macaron pastels, wobble
  outlines, doodle stars, casual lettering). Backend codex-imagegen. Prompts preserved in
  `prompts/`.
- **Iteration lesson banked**: the backend emits 3:2 regardless of the requested 4:3, so
  the LinkedIn 1.35:1 centre-crop trims the SIDES - v1's left-edge labels got clipped
  ("store" became "tore"). v2 wrote the safe-area instruction for a side-crop: every label
  at least 12% of the width inboard. Verify the crop, not the master.
- **Hybrid enrichment**: after Phoebe's "too short of words" note, the shipped full.png became
  raster hero + hand-set HTML explainer panel (`poster.html`, headless Chrome) - six cards with
  what-it-is / best-at / where-it-goes-wrong per architecture. Words that must be exact are never
  left to diffusion; the maker-routing hard rule applied mid-work.
- **Taste rule applied**: "when a concept is named after an object, build the object"
  (banked on IK-15) - here scaled from one metaphor to a whole vocabulary sharing one
  scene, so the differences between terms become visible as geography.
