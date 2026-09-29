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

The sheet draws that street. Eight small shops with four people each, two towers with sixty each:
ten firms, 152 workers. Only the towers fly the flag. Some windows are lit - that person uses AI -
most of them in the towers, a few in shops whose owner would tell a survey "no".

- **Count the firms:** 2 of 10 fly the flag. 20 per cent.
- **Count workers under a flag:** 120 of 152 work in a flagged building. 79 per cent.
- **Count the lit windows:** 56 of 152 use it themselves. 37 per cent.

The drawn street is illustrative, but the order is not: the real figures land 18, 78, 41 for the
same reason. Big firms adopt first - 37 per cent of US firms with 250+ employees used AI in May
2026, against under 20 per cent of the smallest (Census) - and big firms hold most of the workers.
So a firm-weighted rate is small, an employment-weighted rate is large, and individual use sits in
between, pulled up by people using their own tools where the company says it does not.

The practical rule for any dashboard: an adoption rate without its unit is not a number yet. Say
per firm, per worker, or per worker-at-a-firm - then the date.

## Recipe

- **Maker:** design-built. `build.py` draws the street and computes every ruler from it, with
  asserts, then writes `poster.html`; headless Chrome renders 2000x2500.
- **Style:** ink sketch, one accent. Indigo line, warm paper, seeded wobble. Amber is the only
  saturated colour and means one thing - AI in use - as a roof flag (firm) or a lit window (person).
- **Why it works as a picture:** the weighting argument is abstract in words and obvious in a
  drawing. Two tall buildings are two firms and 120 people at once.

Sources: J. S. Allen, "Monitoring AI Adoption in the U.S. Economy", FEDS Notes, Federal Reserve
Board, 3 April 2026. US Census Bureau, "Large Firms With at Least 20 Employees Biggest AI Users",
May 2026.
