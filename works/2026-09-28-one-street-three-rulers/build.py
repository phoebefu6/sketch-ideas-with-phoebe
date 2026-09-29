"""One street, three rulers - build poster.html (render headless to full.png).

Every count on the sheet is computed from the drawn street and asserted here,
so the picture and the arithmetic cannot drift apart.
"""
from __future__ import annotations

import random
from pathlib import Path

HERE = Path(__file__).parent
rng = random.Random(20260928)

INK = "#2E3A5C"      # indigo line - structure, no data meaning
SOFT = "#8B93A8"
AMBER = "#F0A01E"    # the ONE accent: AI actually in use
PAPER = "#FAF8F3"

# ---------------------------------------------------------------- the street
# S = small shop (4 workers, 2x2 windows), T = tower (60 workers, 5x12 windows)
ORDER = "SSTSSSSTSS"
SHOP_W, SHOP_H, TOW_W, TOW_H, GAP = 66, 100, 108, 330, 14
GROUND = 640
LIT_TOWER = {2: 27, 7: 23}          # lit windows per tower
LIT_SHOP = {0: 2, 3: 1, 5: 2, 9: 1}  # bring-your-own users in unflagged shops

total_w = sum(TOW_W if c == "T" else SHOP_W for c in ORDER) + GAP * (len(ORDER) - 1)
x0 = (1000 - total_w) / 2


def jit(a: float = 1.1) -> float:
    return rng.uniform(-a, a)


def line(x1, y1, x2, y2, w=1.6, color=INK, a=1.2, op=1.0) -> str:
    """One hand stroke: slight bow + overshoot, drawn as a quadratic."""
    mx, my = (x1 + x2) / 2 + jit(a), (y1 + y2) / 2 + jit(a)
    return (f'<path d="M{x1+jit(a):.1f},{y1+jit(a):.1f} Q{mx:.1f},{my:.1f} '
            f'{x2+jit(a):.1f},{y2+jit(a):.1f}" stroke="{color}" stroke-width="{w}" '
            f'fill="none" stroke-linecap="round" opacity="{op}"/>')


def box(x, y, w, h, sw=1.6, fill="none", a=1.0, color=INK) -> str:
    out = []
    if fill != "none":
        pts = [(x + jit(a * .6), y + jit(a * .6)), (x + w + jit(a * .6), y + jit(a * .6)),
               (x + w + jit(a * .6), y + h + jit(a * .6)), (x + jit(a * .6), y + h + jit(a * .6))]
        out.append('<path d="M' + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
                   + f' Z" fill="{fill}" stroke="none"/>')
    o = 1.5  # overshoot, the hand runs past the corner
    out += [line(x - o, y, x + w + o, y, sw, color, a), line(x + w, y - o, x + w, y + h + o, sw, color, a),
            line(x + w + o, y + h, x - o, y + h, sw, color, a), line(x, y + h + o, x, y - o, sw, color, a)]
    return "".join(out)


svg: list[str] = []
workers = flagged_workers = lit = 0
firms = flagged_firms = 0
buildings = []  # (kind, flagged, n_workers, n_lit) in street order
x = x0
for i, kind in enumerate(ORDER):
    firms += 1
    if kind == "T":
        w, h, cols, rows, ww, wh, px, py, top_m = TOW_W, TOW_H, 5, 12, 12, 16, 19, 25, 20
    else:
        w, h, cols, rows, ww, wh, px, py, top_m = SHOP_W, SHOP_H, 2, 2, 17, 21, 28, 34, 20
    top = GROUND - h
    n = cols * rows
    n_lit = LIT_TOWER.get(i, 0) if kind == "T" else LIT_SHOP.get(i, 0)
    flagged = kind == "T"
    lit_idx = set(rng.sample(range(n), n_lit))
    svg.append(box(x, top, w, h, 2.0))
    if kind == "S":  # awning line + door gap, so a shop reads as a shop
        svg.append(line(x - 4, top + 8, x + w + 4, top + 8, 1.4))
    left = x + (w - (cols - 1) * px - ww) / 2
    for k in range(n):
        r, c = divmod(k, cols)
        wx, wy = left + c * px, top + top_m + r * py
        svg.append(box(wx, wy, ww, wh, 1.1, AMBER if k in lit_idx else "none", .7))
    if flagged:
        cx = x + w / 2
        svg.append(line(cx, top, cx, top - 34, 1.8))
        svg.append(f'<path d="M{cx+1:.1f},{top-34:.1f} L{cx+26:.1f},{top-27:.1f} '
                   f'L{cx+1:.1f},{top-20:.1f} Z" fill="{AMBER}" stroke="{INK}" stroke-width="1.3"/>')
        flagged_firms += 1
        flagged_workers += n
    workers += n
    lit += n_lit
    buildings.append((kind, flagged, n, n_lit, x, w, top))
    x += w + GAP

# ground: two passes, the second faint, like a pencil going back over it
svg.append(line(40, GROUND, 960, GROUND, 2.2, INK, 1.5))
svg.append(line(46, GROUND + 3, 954, GROUND + 3, 1.0, INK, 1.8, .45))

assert (firms, flagged_firms) == (10, 2)
assert (workers, flagged_workers, lit) == (152, 120, 56)
R1 = round(100 * flagged_firms / firms)
R2 = round(100 * flagged_workers / workers)
R3 = round(100 * lit / workers)
assert (R1, R2, R3) == (20, 79, 37)


# ---------------------------------------------------------- annotations (sky)
def note(tx, ty, text, ax, ay, anchor="start") -> str:
    return (line(tx + (-6 if anchor == "end" else 6) * 0, ty + 8, ax, ay, 1.1, INK, 1.4)
            + f'<text x="{tx}" y="{ty}" class="note" text-anchor="{anchor}">{text}</text>')


t1 = buildings[2]
t2 = buildings[7]
s0 = buildings[0]
s5 = buildings[5]
flag_tip = (t1[4] + t1[5] / 2 + 24, t1[6] - 28)
svg.append(note(t1[4] + t1[5] + 30, 262, "a flag: the firm uses AI", flag_tip[0] + 4, flag_tip[1]))
svg.append(note(s5[4] - 150, 440, "a lit window: this person uses AI",
                s5[4] + 18, GROUND - SHOP_H + 26))
svg.append(note(s0[4], 468, "lit, no flag:", s0[4] + 20, GROUND - SHOP_H + 70))
svg.append(f'<text x="{s0[4]}" y="486" class="note">the owner says "no"</text>')
svg.append(f'<text x="{t2[4] - 10}" y="{t2[6] + 14}" class="note-s" text-anchor="end">60 workers</text>')
svg.append(f'<text x="{buildings[8][4]}" y="{GROUND - SHOP_H - 12}" class="note-s">4 workers</text>')
svg.append(f'<text x="500" y="{GROUND + 30}" class="caveat" text-anchor="middle">'
           f'A drawn street: {firms} firms, {workers} workers. Illustrative, not survey data.</text>')


# ------------------------------------------------------------- three rulers
def mini_firms(y) -> str:
    out = []
    for k, (kind, flagged, *_rest) in enumerate(buildings):
        bx = 372 + k * 30
        bh = 30 if kind == "T" else 16
        out.append(box(bx, y + 34 - bh, 18, bh, 1.3, "none", .6))
        if flagged:
            out.append(line(bx + 9, y + 34 - bh, bx + 9, y + 34 - bh - 12, 1.3))
            out.append(f'<path d="M{bx+9.5:.1f},{y+34-bh-12:.1f} l11,3 l-11,3 Z" fill="{AMBER}" '
                       f'stroke="{INK}" stroke-width="1"/>')
    return "".join(out)


def mini_people(y, mode) -> str:
    """152 cells, grouped building by building in street order."""
    out, k = [], 0
    cols = 38
    on = sum(n for _, f, n, *_r in buildings if f) if mode == "flag" else sum(b[3] for b in buildings)
    fill_on = INK if mode == "flag" else AMBER
    for k in range(152):
        r, c = divmod(k, cols)
        cx, cy = 372 + c * 9 + jit(.4), y + 2 + r * 9 + jit(.4)
        fill = fill_on if k < on else "none"
        out.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="6.4" height="6.4" rx="1" fill="{fill}" '
                   f'stroke="{INK}" stroke-width=".9"/>')
    k = 152
    assert k == 152
    return "".join(out)


RULERS = [
    ("Ruler 1 - count the firms", f"{flagged_firms} of {firms} fly the flag", R1, mini_firms,
     "18%", "of US firms used AI", "Census BTOS, Dec 2025"),
    ("Ruler 2 - count workers under a flag", f"{flagged_workers} of {workers} work in a flagged building",
     R2, lambda y: mini_people(y, "flag"),
     "78%", "of the US workforce is at a firm using AI", "Atlanta Fed SBU, Nov 2025"),
    ("Ruler 3 - count the lit windows", f"{lit} of {workers} use it themselves", R3,
     lambda y: mini_people(y, "lit"),
     "41%", "of US workers use genAI for work", "Real-Time Population Survey, Nov 2025"),
]
RY0, RSTEP = 722, 104
svg.append(f'<text x="56" y="{RY0 - 22}" class="kick">Same street. Three honest counts.</text>')
svg.append(f'<text x="944" y="{RY0 - 22}" class="kick" text-anchor="end">The real one, same autumn</text>')
for i, (title, sub, pct, mini, real, real_s, real_src) in enumerate(RULERS):
    y = RY0 + i * RSTEP
    svg.append(line(56, y - 8, 944, y - 8, 1.0, SOFT, .8, .8))
    svg.append(f'<text x="56" y="{y + 16}" class="r-t">{title}</text>')
    svg.append(f'<text x="56" y="{y + 36}" class="r-s">{sub}</text>')
    svg.append(f'<text x="56" y="{y + 84}" class="r-p">{pct}%</text>')
    svg.append(mini(y + 18))
    svg.append(f'<text x="944" y="{y + 52}" class="real" text-anchor="end">{real}</text>')
    svg.append(f'<text x="944" y="{y + 70}" class="real-s" text-anchor="end">{real_s}</text>')
    svg.append(f'<text x="944" y="{y + 86}" class="real-src" text-anchor="end">{real_src}</text>')
svg.append(line(56, RY0 + 3 * RSTEP - 8, 944, RY0 + 3 * RSTEP - 8, 1.0, SOFT, .8, .8))

HTML = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>One street, three rulers</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --paper:{PAPER}; --ink:{INK}; --soft:{SOFT}; --amber:{AMBER};
  --display:"Fraunces","Iowan Old Style",Georgia,"Times New Roman",serif;
  --text:"Inter","Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
  --mono:"IBM Plex Mono","SF Mono",Menlo,Consolas,monospace;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1000px;height:1250px;overflow:hidden}}
body{{background:var(--paper);color:var(--ink);font:15px/1.45 var(--text);-webkit-font-smoothing:antialiased}}
svg{{position:absolute;left:0;top:0}}
.spec{{position:absolute;top:34px;font:500 10px/1 var(--mono);letter-spacing:2.2px;text-transform:uppercase;color:var(--soft)}}
.spec.l{{left:56px}} .spec.r{{right:56px}}
header{{position:absolute;left:56px;top:68px;width:888px}}
h1{{font:700 66px/1 var(--display);letter-spacing:-1.5px}}
.deck{{margin-top:14px;font:400 17px/1.45 var(--text);color:#4A5270;max-width:800px}}
text.note{{fill:var(--ink);font:italic 400 15px var(--display)}}
text.note-s{{fill:var(--soft);font:500 10.5px var(--mono);letter-spacing:.5px}}
text.caveat{{fill:var(--soft);font:500 11px var(--mono);letter-spacing:.4px}}
text.kick{{fill:var(--ink);font:600 12px var(--text);letter-spacing:1.6px;text-transform:uppercase}}
text.r-t{{fill:var(--ink);font:600 15px var(--text)}}
text.r-s{{fill:#5B6380;font:400 13px var(--text)}}
text.r-p{{fill:var(--ink);font:700 40px var(--display);letter-spacing:-1px}}
text.real{{fill:var(--ink);font:700 40px var(--display);letter-spacing:-1px}}
text.real-s{{fill:#4A5270;font:400 12.5px var(--text)}}
text.real-src{{fill:var(--soft);font:500 10.5px var(--mono);letter-spacing:.3px}}
footer{{position:absolute;left:56px;top:1064px;width:888px}}
.take{{font:700 27px/1.2 var(--display);letter-spacing:-.4px}}
.why{{margin-top:10px;font:400 13.5px/1.5 var(--text);color:#4A5270;max-width:880px}}
.src{{margin-top:12px;font:500 9.5px/1.5 var(--mono);color:var(--soft);letter-spacing:.2px}}
</style></head><body>
<div class="spec l">Worth a thousand words - applied AI</div>
<div class="spec r">AI adoption rate, decoded</div>
<header>
  <h1>18% or 78%?</h1>
  <p class="deck">Both are the US AI adoption rate, measured the same autumn. Nobody is wrong.
  They counted different things on the same street.</p>
</header>
<svg width="1000" height="1250" viewBox="0 0 1000 1250" xmlns="http://www.w3.org/2000/svg">
{''.join(svg)}
</svg>
<footer>
  <div class="take">An adoption rate without its unit is not a number yet.
  Say per firm, per worker, or per worker-at-a-firm - then the date.</div>
  <p class="why">Why the rulers split: big firms adopt first (37% of firms with 250+ employees
  vs under 20% of the smallest, Census, May 2026), and big firms hold most of the workers.</p>
  <p class="src">SOURCES: J. S. Allen, "Monitoring AI Adoption in the U.S. Economy", FEDS Notes, Federal Reserve Board, 3 Apr 2026
  (BTOS 18% of firms, Dec 2025; RPS 41% of workforce, Nov 2025; SBU 78% of labor force, employment-weighted, Nov 2025).
  US Census Bureau, "Large Firms With at Least 20 Employees Biggest AI Users", May 2026.</p>
</footer>
</body></html>
"""
assert HTML.isascii(), "all-ASCII body so it cannot mojibake"
(HERE / "poster.html").write_text(HTML)
print("ok", firms, workers, flagged_workers, lit, R1, R2, R3)
