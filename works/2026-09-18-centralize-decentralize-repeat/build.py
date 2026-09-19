#!/usr/bin/env python3
"""Centralize. Decentralize. Repeat. - design-built plate generator.

SV-047 Narrative Stream, FIRST outing. One unbroken ribbon on a TRUE LINEAR time axis,
1960-2026. Vertical position is the only encoded variable; thickness is constant and is
asserted equal at every sample. Every label is placed by a collision solver and every
placement is asserted, because a timeline whose labels collide is a timeline nobody reads.

Every dated event is sourced - see private/briefs/2026-09-18-centralize-decentralize-repeat.md.
"""
from pathlib import Path

# ------------------------------------------------------------------ frame + scales
W_PAGE, H_PAGE = 1000, 1250
X0, X1 = 86, 930                 # time axis, in page px
Y_MID = 560                      # the federated midline
AMP = 200                        # px for v = 1.0
RIB = 22                         # ribbon thickness, px. Constant. Carries no meaning.
YR0, YR1 = 1960, 2026
PXY = (X1 - X0) / (YR1 - YR0)

LAB_TOP, LAB_BOT = 196, 850      # labels may not leave this band
PENDING_FROM = 2022.0            # after this the swing is not yet history

def X(year): return X0 + (year - YR0) * PXY
def Y(v):    return Y_MID - v * AMP

assert abs(X(YR0) - X0) < 1e-9 and abs(X(YR1) - X1) < 1e-9
assert abs(PXY - 844 / 66) < 1e-9, PXY

# ------------------------------------------------------------------ the swing
# v = +1 one central team owns the data · -1 the domains own their own data
NODES = [
    (1960,  0.88, ["1960", "The accordion effect",
                   "Before any data team existed."]),
    (1968,  0.96, ["1960s - 70s", "The glass house",
                   "One machine. One queue."]),
    (1983, -0.80, ["1979 . 1983", "VisiCalc, Lotus 1-2-3",
                   "Analysis walks out of the",
                   "glass house onto every desk."]),
    (1992,  0.90, ["1992 . 1996", "The data warehouse",
                   "Inmon models one store;",
                   "Kimball answers with marts",
                   "per business process."]),
    (2010, -0.86, ["2006 . 2010", "Hadoop, then the lake",
                   "Keep everything, decide later."]),
    (2015,  0.82, ["2013 . 2015", "The cloud warehouse"]),
    (2019, -0.88, ["2019", "Data mesh",
                   "The domains own their data."]),
    (2024,  0.18, ["2024 . 2026", "Platform and policy",
                   "The swing is not finished."]),
]
CTRL = [(1960, 0.88), (1968, 0.96), (1983, -0.80), (1992, 0.90), (1996, 0.52),
        (2010, -0.86), (2015, 0.82), (2019, -0.88), (2024, 0.18), (2026, 0.46)]

years = [y for y, _ in CTRL]
assert years == sorted(years) and len(set(years)) == len(years)
assert len(NODES) == 8

# the acceleration claim on the sheet, computed from the dated turns, never eyeballed
FIRST_GAP = 1983 - 1968
LAST_GAP = 2019 - 2015
assert (FIRST_GAP, LAST_GAP) == (15, 4), (FIRST_GAP, LAST_GAP)

def turns(ctrl):
    """interior direction changes - how many times the default answer reversed"""
    d = [1 if b[1] > a[1] else -1 for a, b in zip(ctrl, ctrl[1:])]
    return sum(1 for a, b in zip(d, d[1:]) if a != b)
N_TURNS = turns(CTRL)
assert N_TURNS == 6, N_TURNS

# ------------------------------------------------------------------ centreline
def catmull(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t +
                  (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                  (-p0 + 3 * p1 - 3 * p2 + p3) * t3)

def centreline(ctrl, steps=90):
    pts = []
    n = len(ctrl)
    for i in range(n - 1):
        p0 = ctrl[max(i - 1, 0)]
        p1, p2 = ctrl[i], ctrl[i + 1]
        p3 = ctrl[min(i + 2, n - 1)]
        last = steps if i == n - 2 else steps - 1
        for s in range(last + 1):
            t = s / steps
            yr = catmull(p0[0], p1[0], p2[0], p3[0], t)
            v = catmull(p0[1], p1[1], p2[1], p3[1], t)
            pts.append((yr, max(-1.0, min(1.0, v))))
    return pts

LINE = centreline(CTRL)
assert abs(LINE[0][0] - YR0) < 1e-6 and abs(LINE[-1][0] - YR1) < 1e-6
assert all(b[0] >= a[0] - 1e-9 for a, b in zip(LINE, LINE[1:])), "time must not run backwards"

PX = [(X(yr), Y(v)) for yr, v in LINE]

def band(x_from, x_to):
    """ribbon top and bottom over an x range - used to keep labels off the band"""
    ys = [y for x, y in PX if x_from - 2 <= x <= x_to + 2]
    if not ys:
        ys = [min(PX, key=lambda p: min(abs(p[0] - x_from), abs(p[0] - x_to)))[1]]
    return min(ys) - RIB / 2, max(ys) + RIB / 2

def ribbon(pts):
    top = " ".join(f"{x:.2f},{y - RIB/2:.2f}" for x, y in pts)
    bot = " ".join(f"{x:.2f},{y + RIB/2:.2f}" for x, y in reversed(pts))
    return top + " " + bot

# thickness is a claim on the sheet, so it is checked, not trusted
thick = {round((y + RIB / 2) - (y - RIB / 2), 9) for _, y in PX}
assert thick == {float(RIB)}, thick

SOLID = [p for p, (yr, _) in zip(PX, LINE) if yr <= PENDING_FROM]
PEND = [p for p, (yr, _) in zip(PX, LINE) if yr >= PENDING_FROM]
assert len(SOLID) > 100 and len(PEND) > 5

# ------------------------------------------------------------------ label solver
CW_YEAR, CW_NAME, CW_BODY = 6.35, 7.15, 5.85     # px per char, measured off the rendered faces
PAD_X, LH_YEAR, LH_NAME, LH_BODY = 11, 15, 18, 15.5

def label_box(lines):
    w = max(len(lines[0]) * CW_YEAR, len(lines[1]) * CW_NAME,
            *[len(l) * CW_BODY for l in lines[2:]]) + PAD_X
    h = LH_YEAR + LH_NAME + LH_BODY * len(lines[2:]) + 12
    assert w <= 190, f"label line too long for the box: {lines[1]} ({w:.0f}px)"
    return w, h

def overlap(a, b, m=8):
    return not (a[0] + a[2] + m <= b[0] or b[0] + b[2] + m <= a[0] or
                a[1] + a[3] + m <= b[1] or b[1] + b[3] + m <= a[1])

FED = (X0, Y_MID - 26, 116, 24)      # the FEDERATED midline stamp
placed = [(FED[0], FED[1], FED[2], FED[3], "reserved", 0, 0, ["", "FEDERATED"])]

def crowding(yr):
    return sum(1 for o, _, _ in NODES if o != yr and abs(X(o) - X(yr)) < 130)

# most-constrained first: crowded nodes have fewest slots, and within a cluster the most extreme
# node has least room on its own side, so both must choose before their neighbours
for yr, v, lines in sorted(NODES, key=lambda n: (-crowding(n[0]), -abs(n[1]))):
    nx, ny = X(yr), Y(v)
    w, h = label_box(lines)

    def clamp(x):
        return max(X0, min(x, X1 - w))

    best = None
    for gap in (18, 54, 90, 126, 162, 198):
        for lx in (clamp(nx + 12), clamp(nx - 12 - w)):
            for side in ("above", "below"):
                top_b, bot_b = band(lx, lx + w)
                if side == "above":
                    edge = ny - RIB / 2
                    by = min(top_b, edge) - gap - h   # never crosses the band OR its own node
                    if by < LAB_TOP:
                        continue
                else:
                    edge = ny + RIB / 2
                    by = max(bot_b, edge) + gap
                    if by + h > LAB_BOT:
                        continue
                cand = (lx, by, w, h)
                if any(overlap(cand, (q[0], q[1], q[2], q[3])) for q in placed):
                    continue
                # a label belongs to its node: pick the feasible slot nearest to it
                score = abs(by + h / 2 - ny) + 0.6 * abs(lx + w / 2 - nx)
                if best is None or score < best[0]:
                    best = (score, lx, by, w, h, side, nx, edge, lines)
    if best is None:
        for q in placed:
            print(f"  placed {q[7][1]:<32} x={q[0]:.0f}-{q[0]+q[2]:.0f} y={q[1]:.0f}-{q[1]+q[3]:.0f}")
        raise SystemExit(f"no collision-free slot for {yr} {lines[1]} "
                         f"(node x={nx:.0f} y={ny:.0f} box {w:.0f}x{h:.0f})")
    placed.append(best[1:])

placed.sort(key=lambda q: q[5])          # draw order follows time, not placement order

placed = [q for q in placed if q[4] != "reserved"]
assert len(placed) == len(NODES), (len(placed), len(NODES))
for i, a in enumerate(placed):
    assert LAB_TOP <= a[1] and a[1] + a[3] <= LAB_BOT, f"{a[7][1]} leaves the plate"
    assert X0 - 1 <= a[0] and a[0] + a[2] <= X1 + 1, f"{a[7][1]} leaves the frame"
    for b in placed[i + 1:]:
        assert not overlap((a[0], a[1], a[2], a[3]), (b[0], b[1], b[2], b[3])), \
            f"labels collide: {a[7][1]} / {b[7][1]}"

def label_svg(p):
    lx, by, w, h, side, nx, edge, lines = p
    ty = by + h if side == "above" else by          # the edge the leader meets
    body = "".join(
        f'<text class="l-body" x="{lx}" y="{by + 12 + LH_YEAR + LH_NAME + i*LH_BODY:.1f}">{t}</text>'
        for i, t in enumerate(lines[2:]))
    return f'''  <g class="lab">
    <polyline class="lead" points="{nx:.1f},{edge:.1f} {nx:.1f},{ty:.1f} {lx if lx>nx else lx+w:.1f},{ty:.1f}"/>
    <circle class="dot" cx="{nx:.1f}" cy="{edge:.1f}" r="3"/>
    <text class="l-year" x="{lx}" y="{by + 12:.1f}">{lines[0]}</text>
    <text class="l-name" x="{lx}" y="{by + 12 + LH_YEAR + 3:.1f}">{lines[1]}</text>
    {body}
  </g>'''

# ------------------------------------------------------------------ axis furniture
decades = "".join(
    f'<line class="tick" x1="{X(d):.1f}" y1="876" x2="{X(d):.1f}" y2="884"/>'
    f'<text class="xtick" x="{X(d):.1f}" y="900">{d}</text>'
    for d in range(1960, 2030, 10))

rails = "".join(
    f'<line class="rail" x1="{X0}" y1="{Y(s):.1f}" x2="{X1}" y2="{Y(s):.1f}"/>' for s in (1, -1))

AXT = (f'<text class="ax-t c" transform="translate(957,{Y(0.55):.0f}) rotate(-90)">'
       f'OWNED BY ONE CENTRAL TEAM</text>'
       f'<text class="ax-t d" transform="translate(957,{Y(-0.55):.0f}) rotate(-90)">'
       f'OWNED BY EACH DOMAIN</text>')

PLATE = f'''<svg id="plate" width="{W_PAGE}" height="720" viewBox="0 196 {W_PAGE} 720">
  <defs>
    <clipPath id="upper"><rect x="0" y="0" width="{W_PAGE}" height="{Y_MID}"/></clipPath>
    <clipPath id="lower"><rect x="0" y="{Y_MID}" width="{W_PAGE}" height="{916 - Y_MID}"/></clipPath>
  </defs>
  <rect class="wash" x="{X0}" y="{Y_MID}" width="{X1-X0}" height="{Y(-1)-Y_MID:.0f}"/>
  {rails}
  <line class="mid" x1="{X0}" y1="{Y_MID}" x2="{X1}" y2="{Y_MID}"/>
  {AXT}
  <text class="mid-t" x="{X0}" y="{Y_MID-9}">FEDERATED</text>
  <line class="now" x1="{X(2024):.1f}" y1="{Y(1)-14:.0f}" x2="{X(2024):.1f}" y2="{Y(-1)+14:.0f}"/>


  <polygon class="rib c" points="{ribbon(SOLID)}" clip-path="url(#upper)"/>
  <polygon class="rib d" points="{ribbon(SOLID)}" clip-path="url(#lower)"/>
  <polygon class="rib c pend" points="{ribbon(PEND)}" clip-path="url(#upper)"/>
  <polygon class="rib d pend" points="{ribbon(PEND)}" clip-path="url(#lower)"/>
  <polygon class="pend-edge" points="{ribbon(PEND)}"/>

  <line class="axis" x1="{X0}" y1="876" x2="{X1}" y2="876"/>
  {decades}
{chr(10).join(label_svg(p) for p in placed)}
</svg>'''

# ------------------------------------------------------------------ page
HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Centralize. Decentralize. Repeat.</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ===== SV-047 Narrative Stream - FIRST outing, design-built =====
   core_locked: single_continuous_stream / annotations_inside_the_flow /
   one_saturated_accent_per_category / muted_editorial_ground.
   MARK MEANING (one mark, one meaning):
     x           = time, true linear scale, 1960-2026, no compression anywhere
     y           = where ownership of the data sits
     the ribbon  = the industry's default answer, one unbroken band
     ribbon hue  = which half of the axis the band is in; it changes at the midline, nowhere else
     thickness   = CONSTANT. Carries no meaning. Asserted equal at every sample in build.py
     dashed end  = after Aug 2024 the swing is not yet history. No arrowhead: nothing predicts.
   All structure - rails, ticks, leaders, axis - is warm grey and carries no data meaning. */
:root{{
  --paper:#fbf6f0;
  --wash:#f6e9e5;
  --ink:#241f1c;
  --ink-soft:#7d7069;
  --hair:#ded2c8;
  --central:#0f5f5c;
  --domain:#bf3a68;
  --display:"Fraunces","Iowan Old Style",Georgia,"Times New Roman",serif;
  --text:"Inter","Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
  --mono:"IBM Plex Mono","SF Mono",Menlo,Consolas,monospace;
}}
@page{{size:1000px 1250px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1000px}}
body{{width:1000px;height:1250px;overflow:hidden;position:relative;background:var(--paper);
  color:var(--ink);font:15px/1.45 var(--text);-webkit-font-smoothing:antialiased}}

.spec{{position:absolute;top:34px;font:500 10px/1 var(--mono);letter-spacing:2.2px;
  text-transform:uppercase;color:var(--ink-soft)}}
.spec.l{{left:56px}} .spec.r{{right:56px;text-align:right}}

header{{position:absolute;left:56px;top:62px;width:888px}}
h1{{font:700 54px/1.03 var(--display);letter-spacing:-1px}}
h1 .c{{color:var(--central)}} h1 .d{{color:var(--domain)}}
.deck{{margin-top:11px;font:400 16.5px/1.45 var(--text);color:#453e39;max-width:790px}}
.hr{{margin-top:13px;border-top:1.5px solid var(--ink);width:888px}}

#plate{{position:absolute;left:0;top:196px}}
.wash{{fill:var(--wash)}}
.rail{{stroke:var(--hair);stroke-width:1}}
.mid{{stroke:var(--ink-soft);stroke-width:1;stroke-dasharray:2 5;opacity:.7}}
.axis{{stroke:var(--ink);stroke-width:1}}
.tick{{stroke:var(--ink-soft);stroke-width:1}}
.xtick{{fill:var(--ink-soft);font:500 11px var(--mono);text-anchor:middle;letter-spacing:.4px}}
.ax-t{{font:600 10.5px var(--text);letter-spacing:2.5px;text-anchor:middle}}
.ax-t.c{{fill:var(--central)}} .ax-t.d{{fill:var(--domain)}}
.mid-t{{fill:var(--ink-soft);font:500 10px var(--mono);letter-spacing:2.4px}}

.rib{{stroke:none}}
.rib.c{{fill:var(--central)}}
.rib.d{{fill:var(--domain)}}
.rib.pend{{opacity:.55}}
.pend-edge{{fill:none;stroke:var(--ink-soft);stroke-width:1.1;stroke-dasharray:5 4}}
.pend-t{{fill:var(--ink-soft);font:400 10px var(--mono);letter-spacing:1.5px;text-anchor:end}}
.now{{stroke:var(--ink-soft);stroke-width:1;stroke-dasharray:3 4}}

.lead{{fill:none;stroke:var(--ink-soft);stroke-width:.9}}
.dot{{fill:var(--paper);stroke:var(--ink);stroke-width:1.4}}
.l-year{{fill:var(--ink-soft);font:500 11px var(--mono);letter-spacing:1.1px}}
.l-name{{fill:var(--ink);font:600 14px var(--text)}}
.l-body{{fill:#5d544e;font:400 12.5px var(--text)}}

.bracket{{position:absolute;left:56px;top:944px;width:888px}}
.bracket .q{{font:400 15.5px/1.48 var(--display);font-style:italic;color:#453e39}}
.bracket .q b{{font-style:normal;font-weight:400}}
.cite{{margin-top:6px;font:500 10.5px var(--mono);letter-spacing:1.1px;color:var(--ink-soft);
  text-transform:uppercase}}

.take{{position:absolute;left:56px;top:1028px;width:888px;border-top:1.5px solid var(--ink);
  padding-top:14px;display:flex;gap:30px;align-items:flex-start}}
.take .t{{font:700 27px/1.14 var(--display);width:396px;letter-spacing:-.4px}}
.take .s{{font:400 13.2px/1.55 var(--text);color:#564e49;width:462px;padding-top:4px}}

.src{{position:absolute;left:56px;top:1188px;width:888px;font:400 9.2px/1.3 var(--mono);
  color:var(--ink-soft);letter-spacing:.1px}}
</style>
</head>
<body>
<div class="spec l">Worth a Thousand Words</div>
<div class="spec r">The data-team pendulum &middot; 1960&ndash;2026</div>

<header>
  <h1><span class="c">Centralize.</span> <span class="d">Decentralize.</span> Repeat.</h1>
  <div class="deck">Sixty-six years of one swing, drawn on a true time axis. Every turn below is a
  dated, sourced event &mdash; and the shape they make was described in 1960, before the first
  data team existed.</div>
  <div class="hr"></div>
</header>

{PLATE}

<div class="bracket">
  <div class="q">&ldquo;<b>Top management decides that things have gotten out of hand</b>&rdquo; &mdash; and tightens
  up. Then the tightened thing cannot be run centrally, so it is loosened again. McGregor called it the
  accordion effect, and he was writing about factories.</div>
  <div class="cite">Douglas McGregor, The Human Side of Enterprise, McGraw-Hill, 1960</div>
</div>

<div class="take">
  <div class="t">You are not choosing an architecture. You are standing on a phase.</div>
  <div class="s">The default answer has reversed six times since 1960, and the turns keep getting
  closer &mdash; {FIRST_GAP} years from the glass house to the spreadsheet, {LAST_GAP} from the cloud
  warehouse to the data mesh. So the question with leverage is not which side is right. It is: which
  half of the swing was I hired into, and what did the last one break?</div>
</div>

<div class="src">
  McGregor, The Human Side of Enterprise, 1960 &middot; Computerworld, "Swinging Toward Centralization" (centralised EDP "glass house")
  &middot; VisiCalc 1979; Lotus 1-2-3 introduced January 1983 &middot; Inmon, Building the Data Warehouse, 1992 &middot;
  Kimball, The Data Warehouse Toolkit, 1996 &middot; Apache Hadoop 0.1.0, April 2006 &middot; James Dixon,
  "Pentaho, Hadoop, and Data Lakes", 14 Oct 2010 &middot; Amazon Redshift GA 15 Feb 2013; Snowflake cloud data
  warehouse GA June 2015 &middot; Zhamak Dehghani, "How to Move Beyond a Monolithic Data Lake to a Distributed
  Data Mesh", martinfowler.com, 20 May 2019 &middot; EU AI Act in force 1 Aug 2024, GPAI obligations from 2 Aug 2025
  &middot; Thoughtworks, "The state of data mesh in 2026", 16 Jan 2026. Vertical position is an editorial reading of
  each event; every date is as published.
</div>
</body>
</html>'''

out = Path(__file__).with_name("poster.html")
out.write_text(HTML, encoding="utf-8")
print(f"wrote {out}")
print(f"  {len(LINE)} centreline samples | ribbon {RIB}px constant | "
      f"{len(placed)} labels placed, 0 collisions | px/year {PXY:.4f}")
for p in placed:
    print(f"    {p[7][0]:<12} {p[7][1]:<30} {p[4]:<5} box=({p[0]:.0f},{p[1]:.0f},{p[2]:.0f},{p[3]:.0f})")
