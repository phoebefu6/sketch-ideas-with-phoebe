# The price of a word

## Key concept

Three plates from a statistical atlas that does not exist.

**Plate I.** Between June 1998 and July 1999, 95 publicly traded firms added ".com" to their
names. Cumulative abnormal return: **about 74 per cent** over the 10 days surrounding the
announcement. The paper sorts those firms into four categories by how much business they actually
did on the internet - pure internet, prior involvement, refocused, and core business not
internet-related - and finds the announcement-day effect **similar across all four**. In the
authors' words, a mere association with the internet was enough.

**Plate II.** After the mid-2000 crash, 67 firms **removed** ".com" from their names. Cumulative
abnormal return: **about 64 per cent** over the 60 days surrounding the announcement.

Same word. Opposite actions. Both paid.

That pair is the whole argument, and it is not an anecdote - it is a Journal of Finance result
and its Journal of Corporate Finance sequel. If adding a word is worth 74 and deleting the same
word is worth 64, then the word was the asset, in both directions. The market was not pricing a
business it could inspect. It was pricing a sentence.

**Plate III.** The instrument is running again on a new word. The share of US public firms saying
"AI" on the quarterly earnings call went from roughly zero in 2016 to about 20 per cent by mid-2024.

## Explanation

**The measure that separates the claim from the capability.** The 2025 working paper that supplies
Plate III does something better than counting mentions. It builds two measures for the same firms:
**AI talk** - forward-looking in-house AI investment claims, pulled from earnings-call transcripts
and classified with an LLM - and **AI walk** - AI-related workforce expertise, measured from
employee resumes. Then it checks which one is real:

- **Walk predicts subsequent AI patent quantity and quality. Talk does not.**
- Within a firm, **past talk does not forecast future walk.** Saying it this quarter is not the
  early sign of doing it next year.
- **The market rewards talk in the short run and discounts it in the long run**, while walk earns
  large, persistent valuation gains only over longer horizons.
- Firms with strong managerial incentives are more likely to raise talk without raising walk.

So the honest version of the 1999 question is not "is this a bubble". It is: **is your roadmap
buying talk or buying walk?** Both are paid. Only one of them is still paid in five years, and
only one of them shows up in what your team can actually build.

**What this piece refuses to claim.** Plate III carries no madder, because madder means a
*published* cumulative abnormal return and no such figure exists for the AI era in this source -
the study reports direction, not a stamped number. Inventing one would have made a better poster
and a worse argument. For the same reason, no plate draws a path between published points: the
dot-com plates show a block spanning the stated window with a **dashed** top edge, and Plate III is
two quarters, not a curve. Nothing here is investment advice, and no company is named - the claim
is about the pricing of language, not about anyone's honesty.

## Recipe

**DESIGN-BUILT**, not generated. Hand-authored HTML with inline SVG, geometry computed in
`build.py`, rendered with headless Chrome at 1000x1250 CSS px and `--force-device-scale-factor=2`
(2000x2500, 4:5). Fully reproducible: `python3 build.py` then the Chrome screenshot line.

- **Style:** SV-052 Victorian Atlas Revival, **first outing** - engraved hatching fills, aged paper
  ground, serif smallcaps labels, ornamental plate furniture. The period costume is the rhetorical
  move: the same numbers set as a 19th-century atlas plate say *we have a filing system for this*,
  so the claim arrives pre-aged instead of sounding like an opinion about the present.
- **Colour, one fill one meaning:** madder = a published cumulative abnormal return (used twice on
  the sheet and nowhere else); indigo = a count of the word being said, not a payment. Every rule,
  tick, border and hatch line is iron-gall ink and means nothing on its own. The legend on the
  sheet states this, because a reader should be able to tell which colour is money without being
  told in a caption.
- **Hatch direction is data:** it leans right where a word was added and left where a word was
  removed, so the two plates mirror each other and still both rise.
- **Type:** Bodoni Moda wears the era and does nothing else; EB Garamond with oldstyle figures
  carries every label, value, note and source. One face for the costume, a quieter one for the
  data - otherwise the costume eats the numbers.
- **Geometry is asserted, not eyeballed.** `build.py` derives both block heights from one
  pixels-per-percentage-point scale and asserts that their ratio equals 74/64 before writing the
  file. When two bars exist to be compared, the comparison has to be true in code.

## Sources

- Michael J. Cooper, Orlin Dimitrov and P. Raghavendra Rau, "A Rose.com by Any Other Name",
  *The Journal of Finance* 56(6), December 2001, 2371-2388.
- Michael J. Cooper, Ajay Khorana, Igor Osobov, Ajay Patel and P. Raghavendra Rau, "Managerial
  actions in response to a market downturn: valuation effects of name changes in the dot.com
  decline", *Journal of Corporate Finance*, 2004.
- Boyuan Li, "AI Washing", University of Florida working paper, August 2025.
