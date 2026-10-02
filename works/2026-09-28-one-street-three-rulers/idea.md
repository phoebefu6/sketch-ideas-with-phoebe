# 18% or 78%? One street, three rulers.

## Key concept

"What share of the economy has adopted AI?" has at least three honest answers, and in late 2025
they were 18, 41 and 78 per cent - in the same country, in the same few weeks. A Federal Reserve
note from April 2026 lays them side by side:

| ruler | what is counted | US figure | source |
|---|---|---|---|
| firms | share of firms that used AI | 18% | Census BTOS, Dec 2025 |
| workers, own use | share of workers using genAI for work | 41% | Real-Time Population Survey, Nov 2025 |
| workers, by roof | share of the workforce at a firm that has adopted AI | 78% | Atlanta Fed Survey of Business Uncertainty, Nov 2025 |

Nobody is wrong. They counted different things on the same street.

## Explanation

The picture paints that street. Two office towers fly the flag - the firms that use AI - and
their windows are full of people at screens. Around them, small shops: a baker, a barber, a
bookseller, a florist, a bike mechanic, a tailor, a toymaker, all working by hand. One cafe owner
sits at a laptop, and her shop flies no flag.

Three surveyors measure the same street:

- **Count the firms** - a clicker on each door. Most doors are small shops, so the rate is small:
  18 per cent of US firms.
- **Count everyone under a flag** - a tape round the two towers, taking in every desk inside
  whether that person uses AI or not: 78 per cent of the US workforce works at an adopting firm.
- **Count who uses it** - a ladder and a lantern, window by window, including the cafe: 41 per
  cent of US workers use genAI for work.

The order is not an accident. Big firms adopt first - 37 per cent of US firms with 250+ employees
used AI in May 2026, against under 20 per cent of the smallest (Census) - and big firms hold most
of the workers. So a firm-weighted rate is small, an employment-weighted rate is large, and
individual use sits in between, pulled up by people using their own tools where the company
says it does not.

The practical rule for any dashboard: an adoption rate without its unit is not a number yet. Say
per firm, per worker, or per worker-at-a-firm - then the date.

## Recipe

- **Maker:** raster, GPT Image through codex-cli, 2:3. Four variants. The first two put a laptop
  in nearly every shop, which blurred the argument; the third fixed that but carried almost no
  information; the fourth builds the facts into the street - a shop sign and a tower plaque for
  WHY the rates split, and a source line on each surveyor's signpost.
- **Style:** storybook high street - watercolour and gouache, ink outlines, autumn blue hour,
  lettering on the banner, a hanging shop sign, a brass plaque, a cafe chalkboard, the three
  signposts and the scroll - every fact in the scene, no paragraph block.
- **Why it works as a picture:** the weighting argument is abstract in words and obvious in a
  place. Two towers are two firms and most of the people at once, and the surveyor with the tape
  is visibly measuring something different from the one with the clicker.

Sources: J. S. Allen, "Monitoring AI Adoption in the U.S. Economy", FEDS Notes, Federal Reserve
Board, 3 April 2026. US Census Bureau, "Large Firms With at Least 20 Employees Biggest AI Users",
May 2026.
