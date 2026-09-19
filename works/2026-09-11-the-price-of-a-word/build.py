#!/usr/bin/env python3
"""The price of a word - design-built plate generator.

SV-052 Victorian Atlas Revival. Every geometric value is computed from the PUBLISHED
figure, never eyeballed, and asserted before the file is written.

Sources (all verified from the published PDFs - see private/briefs/2026-09-11-the-price-of-a-word.md):
  Cooper, Dimitrov & Rau (2001) J.Finance 56(6):2371-2388   -> +74%, 10-day window, n=95
  Cooper, Khorana, Osobov, Patel & Rau (2004) J.Corp.Fin    -> +64%, 60-day window, n=67
  Li, Boyuan (2025) "AI Washing", Univ. of Florida          -> ~0% (2016) -> ~20% (2024 Q2)
"""
from pathlib import Path

# ---------------------------------------------------------------- published figures
CAR_ADD, WIN_ADD, N_ADD = 74, 10, 95      # percent, days surrounding announcement, firms
CAR_DEL, WIN_DEL, N_DEL = 64, 60, 67
AI_2016, AI_2024 = 0.0, 20.0              # percent of US public firms saying "AI" on the call

# ---------------------------------------------------------------- plate I / II geometry
PLATE_W, PLATE_H = 420, 420
PAD = 24
CHART_H = 190                              # px for the 0-80 per-cent return scale
Y_MAX = 80
PX_PER_PCT = CHART_H / Y_MAX
h_add = CAR_ADD * PX_PER_PCT
h_del = CAR_DEL * PX_PER_PCT
# the whole argument is that these two are comparable, so they MUST share one scale
assert abs(h_add / h_del - CAR_ADD / CAR_DEL) < 1e-9
assert round(h_add, 2) == 175.75 and round(h_del, 2) == 152.0, (h_add, h_del)

AX_X = PAD + 40                            # x of the value axis
CHART_W = PLATE_W - PAD - AX_X - 10
AX_Y = 118 + CHART_H                       # zero baseline; 118 = bottom of the plate header
assert AX_Y + 34 < PLATE_H - 40            # x labels must clear the plate footnote

def window_block(window_days, axis_days):
    """Block spans the PUBLISHED window on a slightly wider axis. No daily path is drawn
    anywhere - only the published endpoint over its stated window."""
    px_per_day = CHART_W / (2 * axis_days)
    return (AX_X + CHART_W / 2 - (window_days / 2) * px_per_day,
            window_days * px_per_day, px_per_day)

ADD_X, ADD_W, ADD_PPD = window_block(WIN_ADD, 6)     # axis -6..+6 days
DEL_X, DEL_W, DEL_PPD = window_block(WIN_DEL, 36)    # axis -36..+36 days

# ---------------------------------------------------------------- plate III geometry
P3_W, P3_H_BOX, P3_MAX = 470, 320, 25
P3_H = 120
P3_PX = P3_H / P3_MAX
P3_AX_X, P3_AX_Y = 62, 118 + P3_H
bar2016 = max(AI_2016 * P3_PX, 3.0)        # "virtually zero" - a stub, labelled as ~0
bar2024 = AI_2024 * P3_PX
assert round(bar2024, 2) == 96.0, bar2024

def yticks(maxv, step, px_per, base_y, x0, x1):
    out = []
    v = 0
    while v <= maxv:
        y = base_y - v * px_per
        out.append(f'<line class="grid" x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}"/>')
        out.append(f'<text class="ytick" x="{x0-8:.0f}" y="{y+4:.1f}">{v}</text>')
        v += step
    return "\n  ".join(out)

def note_lines(lines, x, y_bottom, lh=15):
    out = []
    for i, ln in enumerate(lines):
        y = y_bottom - (len(lines) - 1 - i) * lh
        out.append(f'<text class="plate-note" x="{x}" y="{y:.0f}">{ln}</text>')
    return "\n  ".join(out)

# ---------------------------------------------------------------- plate builder
def plate(num, title, sub, hatch, bx, bw, bh, stamp, axis_days, ppd, notes):
    top = AX_Y - bh
    xt = []
    for d in [-axis_days, -axis_days // 2, 0, axis_days // 2, axis_days]:
        x = AX_X + CHART_W / 2 + d * ppd
        xt.append(f'<line class="tick" x1="{x:.1f}" y1="{AX_Y}" x2="{x:.1f}" y2="{AX_Y+5}"/>')
        xt.append(f'<text class="xtick" x="{x:.1f}" y="{AX_Y+19}">{f"{d:+d}" if d else "0"}</text>')
    zx = AX_X + CHART_W / 2
    px, pw, ph = bx + bw / 2 - 45, 90, 40                 # the label patch on the hatch
    return f'''
<svg class="plate" width="{PLATE_W}" height="{PLATE_H}" viewBox="0 0 {PLATE_W} {PLATE_H}">
  <rect class="plate-bg" x="0.5" y="0.5" width="{PLATE_W-1}" height="{PLATE_H-1}"/>
  <rect class="plate-rule-outer" x="3.5" y="3.5" width="{PLATE_W-7}" height="{PLATE_H-7}"/>
  <rect class="plate-rule-inner" x="8.5" y="8.5" width="{PLATE_W-17}" height="{PLATE_H-17}"/>
  <text class="plate-no" x="{PAD}" y="{PAD+16}">Plate {num}</text>
  <line class="hair" x1="{PAD}" y1="{PAD+25}" x2="{PLATE_W-PAD}" y2="{PAD+25}"/>
  <text class="plate-title" x="{PAD}" y="{PAD+51}">{title}</text>
  <text class="plate-sub" x="{PAD}" y="{PAD+71}">{sub}</text>
  <text class="axname" x="{PAD}" y="{AX_Y-CHART_H-9}">per cent</text>

  {yticks(Y_MAX, 20, PX_PER_PCT, AX_Y, AX_X, PLATE_W-PAD)}
  <line class="axis" x1="{AX_X}" y1="{AX_Y-CHART_H-4}" x2="{AX_X}" y2="{AX_Y}"/>
  <line class="axis" x1="{AX_X}" y1="{AX_Y}" x2="{PLATE_W-PAD}" y2="{AX_Y}"/>
  {''.join(xt)}
  <text class="xname" x="{AX_X + CHART_W/2:.0f}" y="{AX_Y+34}">days surrounding the announcement</text>

  <rect x="{bx:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="url(#{hatch})"/>
  <line class="edge" x1="{bx:.1f}" y1="{top:.1f}" x2="{bx:.1f}" y2="{AX_Y}"/>
  <line class="edge" x1="{bx+bw:.1f}" y1="{top:.1f}" x2="{bx+bw:.1f}" y2="{AX_Y}"/>
  <line class="edge-open" x1="{bx:.1f}" y1="{top:.1f}" x2="{bx+bw:.1f}" y2="{top:.1f}"/>
  <line class="day0" x1="{zx:.1f}" y1="{AX_Y-CHART_H-4}" x2="{zx:.1f}" y2="{AX_Y}"/>
  <text class="day0lab" x="{zx:.1f}" y="{AX_Y-CHART_H-9}">the name changes</text>

  <rect class="patch" x="{px:.1f}" y="{top+14:.1f}" width="{pw}" height="{ph}"/>
  <text class="stamp" x="{px+pw/2:.1f}" y="{top+44:.1f}">{stamp}</text>
  {note_lines(notes, PAD, PLATE_H-PAD-8)}
</svg>'''

P1 = plate("I", "Addition of &ldquo;.com&rdquo; to the name",
           f"{N_ADD} firms &middot; June 1998 &ndash; July 1999 &middot; published {WIN_ADD}-day window", "hatchR",
           ADD_X, ADD_W, h_add, f"+{CAR_ADD}%", 6, ADD_PPD,
           ["The effect was similar across all four involvement categories &mdash;",
            "including firms whose core business was not internet-related."])

P2 = plate("II", "Deletion of &ldquo;.com&rdquo; from the name",
           f"{N_DEL} firms &middot; after the mid-2000 crash &middot; published {WIN_DEL}-day window", "hatchL",
           DEL_X, DEL_W, h_del, f"+{CAR_DEL}%", 36, DEL_PPD,
           ["Same register of firms, opposite action. Mind the day scale:",
            "this window is six times wider than Plate I&rsquo;s."])

# ---------------------------------------------------------------- plate III
p3_cols = ""
for i, (yr, lab, h) in enumerate([("2016 Q1", "~0", bar2016), ("2024 Q2", "~20", bar2024)]):
    cx = 112 + i * 184
    p3_cols += f'''
  <rect x="{cx}" y="{P3_AX_Y-h:.1f}" width="100" height="{h:.1f}" fill="url(#hatchV)"/>
  <rect class="edge3" x="{cx}" y="{P3_AX_Y-h:.1f}" width="100" height="{h:.1f}"/>
  <text class="stamp3" x="{cx+50}" y="{P3_AX_Y-h-12:.1f}">{lab}%</text>
  <text class="xtick" x="{cx+50}" y="{P3_AX_Y+19}">{yr}</text>'''

P3 = f'''
<svg class="plate3" width="{P3_W}" height="{P3_H_BOX}" viewBox="0 0 {P3_W} {P3_H_BOX}">
  <rect class="plate-bg" x="0.5" y="0.5" width="{P3_W-1}" height="{P3_H_BOX-1}"/>
  <rect class="plate-rule-outer" x="3.5" y="3.5" width="{P3_W-7}" height="{P3_H_BOX-7}"/>
  <rect class="plate-rule-inner" x="8.5" y="8.5" width="{P3_W-17}" height="{P3_H_BOX-17}"/>
  <text class="plate-no" x="{PAD}" y="{PAD+16}">Plate III</text>
  <line class="hair" x1="{PAD}" y1="{PAD+25}" x2="{P3_W-PAD}" y2="{PAD+25}"/>
  <text class="plate-title" x="{PAD}" y="{PAD+51}">Mention of &ldquo;AI&rdquo; on the earnings call</text>
  <text class="plate-sub" x="{PAD}" y="{PAD+71}">Share of U.S. public firms &middot; 2016 Q1 &ndash; 2024 Q2</text>
  <text class="axname" x="{PAD}" y="{P3_AX_Y-P3_H-9}">per cent</text>
  {yticks(P3_MAX, 5, P3_PX, P3_AX_Y, P3_AX_X, P3_W-PAD)}
  <line class="axis" x1="{P3_AX_X}" y1="{P3_AX_Y-P3_H-4}" x2="{P3_AX_X}" y2="{P3_AX_Y}"/>
  <line class="axis" x1="{P3_AX_X}" y1="{P3_AX_Y}" x2="{P3_W-PAD}" y2="{P3_AX_Y}"/>
  {p3_cols}
  {note_lines(["Two published endpoints, drawn as two quarters.",
               "No path between them is reproduced here."], PAD, P3_H_BOX-PAD-8)}
</svg>'''

SW = ('<svg class="sw" width="26" height="16" viewBox="0 0 26 16">'
      '<rect width="26" height="16" fill="url(#{p})"/>'
      '<rect x=".5" y=".5" width="25" height="15" fill="none" stroke="{s}" stroke-width="1"/></svg>')

# ---------------------------------------------------------------- page
HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The price of a word</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
/* ===== SV-052 Victorian Atlas Revival - FIRST outing, design-built =====
   core_locked: engraved hatching fills / aged paper ground / serif smallcaps labels /
   ornamental rules and plate furniture. Two muted plate colours, no flat modern colour block.
   COLOUR MEANING (one fill, one meaning, stated in the legend on the sheet):
     madder = a PUBLISHED cumulative abnormal return
     indigo = a count of the word being said. Not a payment.
   Everything structural - rules, ticks, borders, hatch geometry - is iron-gall ink and
   carries no data meaning. Bodoni Moda wears the era; EB Garamond carries the data.
   The top edge of every block is DASHED: it is a published endpoint, not a path. */
:root{{
  --paper:#f2e8d5;
  --paper-plate:#f8f1e1;
  --ink:#332f28;
  --ink-soft:#7d7466;
  --hair:#bcb09a;
  --madder:#a63324;
  --indigo:#3d5568;
  --display:"Bodoni Moda","Didot","Bodoni MT",Georgia,serif;
  --text:"EB Garamond","Iowan Old Style",Georgia,"Times New Roman",serif;
}}
@page{{size:1000px 1250px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1000px}}
body{{width:1000px;height:1250px;overflow:hidden;position:relative;background:var(--paper);
  color:var(--ink);font:15px/1.42 var(--text);font-variant-numeric:oldstyle-nums;
  -webkit-font-smoothing:antialiased}}
#grain{{position:absolute;inset:0;opacity:.075;pointer-events:none;mix-blend-mode:multiply}}
#vign{{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 80% 70% at 50% 44%,rgba(0,0,0,0) 56%,rgba(96,74,40,.15) 100%)}}

.spec{{position:absolute;top:36px;font:500 10px/1 var(--text);letter-spacing:2.4px;
  text-transform:uppercase;color:var(--ink-soft)}}
.spec.l{{left:56px}} .spec.r{{right:56px;text-align:right}}

.cartouche{{position:absolute;left:56px;top:62px;width:888px;text-align:center}}
.orn{{display:block;margin:0 auto}}
h1{{font:700 57px/1 var(--display);letter-spacing:1.5px;text-transform:uppercase;margin:7px 0 0}}
.deck{{margin-top:10px;font:500 11px/1 var(--text);letter-spacing:3.4px;text-transform:uppercase;
  color:var(--ink-soft)}}
.thesis{{margin-top:11px;font:italic 400 17px/1.4 var(--text)}}
.dbl{{margin-top:12px;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);height:4px}}

.plates{{position:absolute;left:56px;top:222px;width:888px;display:flex;gap:48px}}

.bracket{{position:absolute;left:56px;top:656px;width:888px;text-align:center}}
.bracket .rule{{border-top:1px solid var(--hair);margin:0 150px}}
.bracket .line{{margin-top:11px;font:700 27px/1.14 var(--display)}}
.bracket .sub{{margin-top:7px;font:italic 400 15px/1.4 var(--text);color:var(--ink-soft)}}

.lower{{position:absolute;left:56px;top:736px;width:888px;display:flex;gap:34px;align-items:flex-start}}
.findings{{width:384px;padding-top:4px}}
.findings h3{{font:600 10.5px/1 var(--text);letter-spacing:2.6px;text-transform:uppercase;
  color:var(--ink-soft);padding-bottom:7px;border-bottom:1px solid var(--hair)}}
.findings li{{list-style:none;margin-top:10px;padding-left:16px;position:relative;
  font:400 14.4px/1.36 var(--text)}}
.findings li:before{{content:"\\2014";position:absolute;left:0;color:var(--hair)}}
.findings .refuse{{margin-top:13px;padding:9px 11px;border:1px solid var(--hair);
  font:italic 400 12.8px/1.35 var(--text);color:var(--ink-soft)}}

.legend{{position:absolute;left:56px;top:1068px;width:888px;display:flex;gap:24px;
  border-top:1px solid var(--ink);padding-top:10px}}
.key{{display:flex;gap:9px;align-items:flex-start;width:280px}}
.key svg.sw{{flex:none;margin-top:3px}}
.key p{{font:400 12.4px/1.32 var(--text)}}
.key b{{font-weight:600}}

.takeaway{{position:absolute;left:56px;top:1126px;width:888px;text-align:center}}
.takeaway .t{{font:700 24px/1.2 var(--display)}}
.src{{position:absolute;left:56px;bottom:26px;width:888px;text-align:center;
  font:400 10.4px/1.5 var(--text);color:var(--ink-soft)}}

svg text{{font-family:var(--text);fill:var(--ink);font-variant-numeric:oldstyle-nums}}
.plate-bg{{fill:var(--paper-plate)}}
.plate-rule-outer{{fill:none;stroke:var(--ink);stroke-width:1.6}}
.plate-rule-inner{{fill:none;stroke:var(--hair);stroke-width:.8}}
.plate-no{{font-size:10.5px;letter-spacing:2.8px;text-transform:uppercase;fill:var(--ink-soft)}}
.plate-title{{font-family:var(--display);font-size:20px;font-weight:400}}
.plate-sub{{font-size:12.4px;fill:var(--ink-soft);font-style:italic}}
.plate-note{{font-size:11.2px;fill:var(--ink-soft);font-style:italic}}
.hair{{stroke:var(--hair);stroke-width:.8}}
.grid{{stroke:var(--hair);stroke-width:.6;stroke-dasharray:2 4}}
.axis{{stroke:var(--ink);stroke-width:1.2}}
.tick{{stroke:var(--ink);stroke-width:1}}
.ytick{{font-size:11px;text-anchor:end;fill:var(--ink-soft)}}
.xtick{{font-size:11px;text-anchor:middle;fill:var(--ink-soft)}}
.xname{{font-size:9.6px;letter-spacing:1.8px;text-transform:uppercase;fill:var(--ink-soft);text-anchor:middle}}
.axname{{font-size:9.6px;letter-spacing:1.8px;text-transform:uppercase;fill:var(--ink-soft)}}
.edge{{stroke:var(--madder);stroke-width:1.2}}
.edge-open{{stroke:var(--madder);stroke-width:1.6;stroke-dasharray:5 4}}
.edge3{{fill:none;stroke:var(--indigo);stroke-width:1.2}}
.day0{{stroke:var(--ink);stroke-width:1;stroke-dasharray:3 3}}
.day0lab{{font-size:9.6px;letter-spacing:1.6px;text-transform:uppercase;fill:var(--ink-soft);text-anchor:middle}}
.patch{{fill:var(--paper-plate);stroke:var(--ink);stroke-width:.9}}
.stamp{{font-family:var(--display);font-size:29px;font-weight:700;fill:var(--madder);text-anchor:middle}}
.stamp3{{font-family:var(--display);font-size:21px;font-weight:700;fill:var(--indigo);text-anchor:middle}}
</style>
</head>
<body>
<svg id="grain" width="1000" height="1250"><filter id="f"><feTurbulence type="fractalNoise"
  baseFrequency="0.85" numOctaves="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>
  </filter><rect width="1000" height="1250" filter="url(#f)"/></svg>

<svg width="0" height="0" style="position:absolute"><defs>
  <pattern id="hatchR" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="7" height="7" fill="#f8f1e1"/><line x1="0" y1="0" x2="0" y2="7" stroke="#a63324" stroke-width="1.15"/>
  </pattern>
  <pattern id="hatchL" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
    <rect width="7" height="7" fill="#f8f1e1"/><line x1="0" y1="0" x2="0" y2="7" stroke="#a63324" stroke-width="1.15"/>
  </pattern>
  <pattern id="hatchV" width="7" height="7" patternUnits="userSpaceOnUse">
    <rect width="7" height="7" fill="#f8f1e1"/><line x1="0" y1="0" x2="0" y2="7" stroke="#3d5568" stroke-width="1.15"/>
  </pattern>
</defs></svg>

<div class="spec l">Worth a Thousand Words &middot; Chart No. 01</div>
<div class="spec r">Plates I&ndash;III &middot; 1998&ndash;2024</div>

<div class="cartouche">
  <svg class="orn" width="188" height="11" viewBox="0 0 188 11"><g stroke="#bcb09a" fill="none"
    stroke-width="1"><line x1="0" y1="5.5" x2="76" y2="5.5"/><line x1="112" y1="5.5" x2="188" y2="5.5"/>
    <path d="M86 5.5 L94 1 L102 5.5 L94 10 Z"/></g><circle cx="94" cy="5.5" r="1.4" fill="#bcb09a"/></svg>
  <h1>The Price of a Word</h1>
  <div class="deck">What the market paid for a name it could not verify</div>
  <div class="thesis">Three measured plates on one question: is the market pricing the business, or the word?</div>
  <div class="dbl"></div>
</div>

<div class="plates">{P1}{P2}</div>

<div class="bracket">
  <div class="rule"></div>
  <div class="line">The same word. Opposite actions. Both paid.</div>
  <div class="sub">Adding &ldquo;.com&rdquo; was worth {CAR_ADD} per cent. Deleting it was worth {CAR_DEL} per cent. The word was the asset in both directions.</div>
</div>

<div class="lower">
  {P3}
  <div class="findings">
    <h3>The same instrument, a new word</h3>
    <ul>
      <li><b>Walk</b> &mdash; AI expertise measured from employee resumes &mdash; predicts later AI patent quantity and quality.</li>
      <li><b>Talk</b> &mdash; investment claims made on the earnings call &mdash; does not. Within a firm, past talk does not forecast future walk.</li>
      <li>The market <b>rewards talk in the short run and discounts it in the long run</b>. Walk earns large, persistent gains only over longer horizons.</li>
    </ul>
    <div class="refuse">Plate III carries no madder. The 2016&ndash;2024 study reports direction, not a published abnormal return, so no return is stamped here. The receipts for this word are not in yet.</div>
  </div>
</div>

<div class="legend">
  <div class="key">{SW.format(p="hatchR", s="#a63324")}
    <p><b>Madder.</b> A published cumulative abnormal return. Stamped twice on this sheet and nowhere else.</p></div>
  <div class="key">{SW.format(p="hatchV", s="#3d5568")}
    <p><b>Indigo.</b> A count of the word being said. Not a payment.</p></div>
  <div class="key" style="width:264px">{SW.format(p="hatchL", s="#a63324")}
    <p><b>Hatch leans with the change:</b> right for a word added, left for a word removed.</p></div>
</div>

<div class="takeaway"><div class="t">The market has never required the thing. It prices the sentence.</div></div>

<div class="src">
  Plate I: Cooper, Dimitrov &amp; Rau, &ldquo;A Rose.com by Any Other Name&rdquo;, <i>Journal of Finance</i> 56(6), 2001, 2371&ndash;2388. &nbsp;
  Plate II: Cooper, Khorana, Osobov, Patel &amp; Rau, &ldquo;Valuation effects of name changes in the dot.com decline&rdquo;, <i>Journal of Corporate Finance</i>, 2004.<br>
  Plate III: B. Li, &ldquo;AI Washing&rdquo;, University of Florida working paper, August 2025. &nbsp; Figures are quoted as published; a dashed top edge marks an endpoint, never a path. Nothing here is investment advice, and no company is named.
</div>
<div id="vign"></div>
</body>
</html>'''

out = Path(__file__).with_name("poster.html")
out.write_text(HTML, encoding="utf-8")
print(f"wrote {out} | add {h_add:.1f}px={CAR_ADD}% del {h_del:.1f}px={CAR_DEL}% "
      f"ai {bar2024:.1f}px={AI_2024}% | scale {PX_PER_PCT:.4f}px/pct")
