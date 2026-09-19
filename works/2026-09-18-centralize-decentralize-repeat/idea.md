# Centralize. Decentralize. Repeat.

## Key concept

Every few years the data organisation answers the same question again. Who owns the data - one
central team, or the domains that produce it? The answer flips, everyone treats the flip as an
architecture decision, and the flip flips back.

This work draws sixty-six years of that question on one honest axis. Time runs left to right on a
true linear scale, 1960 to 2026, with no compression anywhere. Vertical position is the only thing
encoded: the top rail is "one central team owns the data", the bottom rail is "every domain owns
its own data". The ribbon is the industry's default answer, and it is never interrupted.

Eight dated events, every one of them verifiable:

- **1960** - Douglas McGregor describes the cycle in *The Human Side of Enterprise* and calls it
  the accordion effect. A big move toward decentralisation happens; the consequences take their
  toll; top management decides things have gotten out of hand and tightens up; the tightened thing
  cannot be run centrally, so it loosens again. He was writing about factories, a decade before
  anybody had a data team.
- **1960s-70s** - the glass house. One data processing department, one machine, one queue.
- **1979, then January 1983** - VisiCalc, then Lotus 1-2-3 at 495 dollars, the IBM PC's first
  killer app. Analysis walks out of the glass house and onto every desk. Nobody calls it a
  decentralisation programme; it is one.
- **1992** - Inmon publishes *Building the Data Warehouse*: one modelled enterprise store.
  **1996** - Kimball answers with *The Data Warehouse Toolkit*: marts per business process. The
  first wobble inside the centralised half.
- **April 2006** Hadoop 0.1.0; **14 October 2010** James Dixon names the data lake. Schema-on-read:
  keep everything, decide later, and let teams bring their own tools.
- **15 February 2013** Redshift GA; **June 2015** Snowflake ships its cloud data warehouse. It all
  comes back into one store, because the one store is finally cheap and elastic.
- **20 May 2019** - Zhamak Dehghani publishes the data mesh argument. The domains own their own
  data products.
- **1 August 2024** the EU AI Act enters into force, with obligations for general-purpose AI
  providers applying from 2 August 2025; by January 2026 Thoughtworks describes the settled answer
  as a central platform handling tenancy so that the value-creating components can stay
  decentralised. Governance recentralises. Ownership does not follow it back.

## Explanation

**Why the shape is the point.** Every one of those events is common knowledge in this field. Nobody
is surprised by any single one of them. The surprise is only available when they share one axis,
because then the eye does something no sentence can: it sees a wave. And then it sees the second
thing, which is that the wave is speeding up. Fifteen years pass between the glass house and the
spreadsheet. Four pass between the cloud warehouse and the data mesh.

**What the swing is actually made of.** The cycle is not stupidity. Each turn is a correct local
response to the real cost of the previous one. Centralisation buys consistency, one definition of
revenue, one place to enforce policy - and it buys a queue, and a team that does not know the
business. Decentralisation buys speed and context - and it buys eleven definitions of revenue and
a quality incident nobody is staffed to answer. Both failure modes are real. Neither is solved by
swinging; each is solved by paying for the thing the current half is bad at, deliberately, while
you are in it.

**What is different about the current turn.** For the first time the two things are separating.
The platform is recentralising - storage, compute, identity, lineage, policy - while ownership of
the data products stays with the domains. That is why the ribbon's last stretch climbs back toward
the middle rather than the top rail, and why it is drawn pale and dashed rather than solid. It is
not history yet, and this sheet does not predict where it lands. There is no arrowhead on it.

**The honest limits of this drawing.** The dates are as published; the vertical position of each
event is an editorial reading, which the sheet says in its own source line. Nobody has measured
"how centralised was the median data organisation in 1987", and any curve claiming to is lying.
What the shape can honestly carry is the sequence, the direction of each turn, and the spacing
between them - and that is enough for the argument.

## Recipe

DESIGN-BUILT. `build.py` holds the nine control points, interpolates a Catmull-Rom centreline into
811 samples, offsets it into a constant-thickness ribbon, splits the ribbon into an upper and a
lower clip so the hue changes exactly at the midline, and places all eight annotations with a
collision solver. Before it writes a single byte it asserts that time never runs backwards, that
the ribbon is exactly 22px thick at every sample, that no two label boxes overlap, that no label
crosses the ribbon in its own x-range, and that the two spacing numbers quoted in the takeaway
(15 years and 4) are the actual differences between the plotted turns. Rendered with headless
Chrome at 2000x2500.

Style: **SV-047 Narrative Stream**, first outing - one continuous stream, annotations inside the
flow, one saturated accent per category, muted editorial ground, and no legend anywhere.
