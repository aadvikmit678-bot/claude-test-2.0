"""v4 builder, part 1 (to "Freedom."): v2's cut with the user's notes. Writes gta6-edit/index.html and compositions/*.html
from tools/edl4.py.   usage: python -I -X utf8 tools/build4.py

Type: the Tesla Roadster reel (reel1 / "reference 7"): a Helvetica Neue Medium look (TeX Gyre Heros, thickened to medium),
words on the spoken word in their final places, the line drifting left at a constant speed, entrances snapped frame by
frame (plain, scale pop, two-frame weight flash, light streak), black type on the light cards. No sound effects.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl4 as E
from edl4 import W, WT, cut, N, VO_OFFSET, NEWS_DUR, TOTAL, has

P = E.PROJ
os.makedirs(os.path.join(P, "compositions"), exist_ok=True)
SH = {s["id"]: s for s in E.SHOTS}
F = 1 / 30
r3 = lambda x: round(x, 3)
fr = lambda t: round(round(t * 30) / 30, 4)              # snap to a frame

FONTS = """
@font-face{font-family:"Heros";src:url("assets/fonts/TeXGyreHeros-Regular.otf") format("opentype");font-weight:400;font-style:normal;}
@font-face{font-family:"Heros";src:url("assets/fonts/TeXGyreHeros-Bold.otf") format("opentype");font-weight:700;font-style:normal;}
"""
MED = "0.024em"                     # Heros Regular + this stroke = the reel's medium weight
HEAVY_STROKE = "0.075em"            # Heros Bold + this = the reel's heavy flash frame
SET = "0 0 22px rgba(255,255,255,0.40), 0 0 5px rgba(255,255,255,0.28), 0 2px 16px rgba(0,0,0,0.70)"
BLOOM = "0 0 30px rgba(255,255,255,0.95), 0 0 9px rgba(255,255,255,0.9), 0 2px 16px rgba(0,0,0,0)"
NONE3 = "0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0)"
HALO = "0 0 2px rgba(255,255,255,1), 0 0 7px rgba(255,255,255,1), 0 0 16px rgba(255,255,255,0.9)"   # black type over the logo

CSS = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;}
.shot{position:absolute;inset:0;overflow:hidden;}
.shot video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.cell{position:absolute;overflow:hidden;opacity:0;}
.cell video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.box{position:absolute;background:#fff;}
.cl{position:absolute;left:0;right:0;height:300px;margin-top:-150px;display:flex;align-items:center;justify-content:center;pointer-events:none;}
.row{display:flex;align-items:baseline;justify-content:center;white-space:nowrap;font-family:"Heros",sans-serif;font-size:64px;line-height:1.2;letter-spacing:-0.012em;color:#F4F4F2;}
.row.big{font-size:74px;} .row.r7{font-size:68px;}
.row.wide{column-gap:1.22em;} .row.tight{column-gap:0.27em;} .row.spread{column-gap:3.1em;}
.row.ink{color:#151515;}
.w{position:relative;display:inline-block;}
.gh{visibility:hidden;font-weight:400;}
.ik{position:absolute;left:-60%;right:-60%;top:0;bottom:0;display:flex;justify-content:center;align-items:flex-start;z-index:1;}
.tx{display:inline-block;font-weight:400;-webkit-text-stroke:""" + MED + """ currentColor;opacity:0;text-shadow:""" + SET + """;}
.row.ink .tx{text-shadow:""" + NONE3 + """;}
.row.ink.halo .tx{text-shadow:""" + HALO + """;}
.w.card .tx{color:#141414;text-shadow:""" + NONE3 + """;}
.cardbox{position:absolute;left:-0.28em;right:-0.28em;top:0.02em;bottom:-0.06em;background:#F4F4F2;z-index:0;opacity:0;}
.selbox{position:absolute;left:-0.08em;right:-0.08em;top:0.12em;bottom:0.02em;background:rgba(48,96,255,0.88);z-index:0;transform-origin:0 50%;}
"""


def comp(cid, dur, body, js, extra_css=""):
    return f"""<template>
<style>{CSS}{extra_css}</style>
<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{r3(dur)}">
{body}
</div>
<script>
(function(){{
  const tl = gsap.timeline({{ paused: true }});
{js}
  window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
"""


# ------------------------------------------------------------------ the reel's word entrances, snapped by frame
def ent_js(sel, kind, t, ink=False, halo=False):
    t = r3(fr(t)); a, b = r3(t + F), r3(t + 2 * F)
    rest = HALO if halo else (NONE3 if ink else SET)
    bloom = NONE3 if ink else BLOOM
    if kind == "plain":
        return f'  tl.set("{sel}",{{opacity:1}},{t});\n'
    if kind == "pop":        # frame 1 at 1.5x and brighter, frame 2 in place
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.5,filter:"blur(0px) brightness(1.6)"}},{t});\n'
                f'  tl.set("{sel}",{{scale:1,filter:"blur(0px) brightness(1)"}},{a});\n')
    if kind == "weight":     # two heavy frames in a bloom, the second smeared sideways, then medium
        return (f'  tl.set("{sel}",{{opacity:1,fontWeight:700,WebkitTextStrokeWidth:"{HEAVY_STROKE}",textShadow:"{bloom}",filter:"blur(0px) brightness(1.15)"}},{t});\n'
                f'  tl.set("{sel}",{{scaleX:1.06,filter:"blur(1.6px) brightness(1.1)"}},{a});\n'
                f'  tl.set("{sel}",{{fontWeight:400,WebkitTextStrokeWidth:"{MED}",textShadow:"{rest}",scaleX:1,filter:"blur(0px) brightness(1)"}},{b});\n')
    if kind == "streak":     # vertical light streaks for two frames, then the clean word
        return (f'  tl.set("{sel}",{{opacity:0.9,scaleY:2.6,scaleX:0.95,filter:"blur(2.2px) brightness(1.8)"}},{t});\n'
                f'  tl.set("{sel}",{{scaleY:1.6,filter:"blur(1px) brightness(1.3)"}},{a});\n'
                f'  tl.set("{sel}",{{scaleY:1,scaleX:1,opacity:1,filter:"blur(0px) brightness(1)"}},{b});\n')
    raise ValueError(kind)


SMALL = {"a", "an", "the", "to", "of", "in", "it", "on", "and", "so", "for", "at", "be", "is", "was", "if", "you", "it's",
         "he's", "i", "that", "with", "are", "from", "but", "they", "what", "just", "how", "this", "your", "that's", "all"}


class Line:
    def __init__(self, words, mode="wide", end=None, y=540, ink=False, size=""):
        self.words, self.mode, self.end, self.y, self.ink, self.size = words, mode, end, y, ink, size


def VLW(idx, mode="wide", end=None, texts=None, kinds=None, cls=None, y=540):
    texts, kinds, cls = texts or {}, kinds or {}, cls or {}
    ws, k = [], 0
    for i in idx:
        if not has(i):
            continue
        txt = texts.get(i, WT(i))
        bare = txt.lower().strip(",.?!")
        if i in kinds:
            kd = kinds[i]
        elif bare in SMALL:
            kd = "plain"
        else:
            kd = ("weight", "pop", "pop", "weight", "pop", "streak", "pop")[(i * 5 + k) % 7]
            k += 1
        ws.append((txt, W(i), cls.get(i, ""), kd))
    return Line(ws, mode, end, y)


def line_html(L, lid, js, drift=44):
    """one caption line: the words laid out in their final places; each enters on its word; the row drifts left"""
    t0 = r3(fr(L.words[0][1]) - F)
    last = L.words[-1][1]
    t1 = r3(min(L.end, last + 1.3)) if L.end else r3(last + 0.8)
    dur = r3(max(0.2, t1 - t0))
    spans = []
    for wi, (txt, t, cls, kd) in enumerate(L.words):
        wid = f"{lid}w{wi}"
        extra = ""
        if kd == "sel":
            extra = f'<span class="selbox" id="{wid}b"></span>'
            n = len(txt.replace("&nbsp;", " "))
            js.append(f'  tl.set("#{wid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{r3(fr(t))});\n'
                      f'  tl.to("#{wid}",{{clipPath:"inset(0% 0% 0% 0%)",duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(fr(t))});\n'
                      f'  tl.fromTo("#{wid}b",{{scaleX:0}},{{scaleX:1,duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(fr(t))});\n')
        elif kd == "card":
            extra = f'<span class="cardbox" id="{wid}c"></span>'
            js.append(f'  tl.set("#{wid}c",{{opacity:1,scaleY:1.6,scaleX:1.1}},{r3(fr(t))});\n'
                      f'  tl.to("#{wid}c",{{scaleY:1,scaleX:1,duration:0.16,ease:"expo.out"}},{r3(fr(t) + F)});\n'
                      f'  tl.set("#{wid}",{{opacity:1}},{r3(fr(t) + F)});\n')
        else:
            js.append(ent_js("#" + wid, kd, t, L.ink, getattr(L, "halo", False)))
        spans.append(f'<span class="w {cls}">{extra}<span class="gh">{txt}</span><span class="ik"><span class="tx" id="{wid}">{txt}</span></span></span>')
    cls_row = " ".join(x for x in ("row", L.mode, "ink" if L.ink else "", "halo" if getattr(L, "halo", False) else "", L.size) if x)
    html = (f'<div id="{lid}" class="clip cl" data-start="{t0}" data-duration="{dur}" data-track-index="0" style="top:{L.y}px">'
            f'<div class="{cls_row}" id="{lid}r">{"".join(spans)}</div></div>')
    js.append(f'  tl.fromTo("#{lid}r",{{x:{r3(drift * dur / 2)}}},{{x:{r3(-drift * dur / 2)},duration:{dur},ease:"none"}},{t0});\n')
    return html


def NL(words, mode="wide", end=None):     # a news / CJ line from explicit (text, time, kind)
    return Line([(txt, t, "sel" if kd == "sel" else "", kd) for txt, t, kd in words], mode, end)


# ------------------------------------------------------------------ captions (the VO; the news lines live in the news scene)
def build_captions():
    body, js = [], []
    L = [
        NL([("Ah", NEWS_DUR + 0.04, "weight"), ("shit,", NEWS_DUR + 0.56, "pop")], end=NEWS_DUR + 1.48),
        NL([("here", NEWS_DUR + 1.54, "pop"), ("we", NEWS_DUR + 1.66, "plain"), ("go", NEWS_DUR + 1.80, "pop"),
            ("again.", NEWS_DUR + 2.00, "weight")], end=VO_OFFSET),
    ]
    V = [
        ([0, 1, 2], {}), ([3, 4, 5], {"kinds": {3: "weight", 5: "pop"}}), ([6, 7, 8, 9], {}),
        ([10, 11, 12], {"mode": "tight", "cls": {12: "card"}, "kinds": {12: "card", 11: "weight"}}),
        ([13, 14, 15], {"end": cut(16) + 0.02}), ([18, 19, 20, 21], {"end": E.R7["t0"] - 0.02}),
        ([55, 57, 58, 59, 60], {"texts": {57: "why"}, "kinds": {57: "weight"}}),
        ([61, 62, 63], {"mode": "tight", "kinds": {62: "weight"}}), ([64, 65, 66, 67, 68], {}),
        ([69, 70, 71, 72], {"kinds": {71: "weight", 72: "pop"}}),
        ([73, 74], {"kinds": {74: "weight"}}), ([75, 76, 77, 78], {}), ([79, 80, 81], {"kinds": {79: "pop", 81: "pop"}}),
        ([82, 83, 84, 85], {}), ([86, 87, 88, 89], {"end": cut(90)}),
    ]
    for k, (idx, o) in enumerate(V):
        nxt = W(V[k + 1][0][0]) - 0.04 if k + 1 < len(V) else cut(90)
        L.append(VLW(idx, mode=o.get("mode", "wide"), end=o.get("end", nxt), texts=o.get("texts"), kinds=o.get("kinds"),
                     cls=o.get("cls")))
    for li, ln in enumerate(L):
        body.append(line_html(ln, f"cap{li:02d}", js))
    open(os.path.join(P, "compositions", "captions.html"), "w", encoding="utf-8").write(comp("captions", TOTAL, "\n".join(body), "".join(js)))
    return L


# ------------------------------------------------------------------ footage
def vid(s, t0, z, cls="shot"):
    st, du = r3(s["start"] - t0), r3(s["end"] - s["start"])
    return (f'<div class="{cls}" id="{s["id"]}-w" style="z-index:{z}">'
            f'<video id="v-{s["id"]}" class="clip" src="assets/clips/{s["id"]}.mp4" data-start="{st}" data-duration="{du}" muted playsinline></video></div>')


def push_js(s, t0):
    if not s.get("push"):
        return ""
    a, b = s["push"]
    return f'  tl.fromTo("#{s["id"]}-w",{{scale:{a}}},{{scale:{b},duration:{r3(s["end"] - s["start"])},ease:"none"}},{r3(s["start"] - t0)});\n'


SCENES = []
SKIP = ("grid", "r7t", "news", "cj")


def section(cid, extra_body="", extra_js="", extra_css=""):
    t0, t1 = E.SPAN[cid]
    shots = [s for s in E.SHOTS if t0 - 1e-6 <= s["start"] < t1 - 1e-6 and not s["id"].startswith(SKIP)]
    body = [vid(s, t0, z) for z, s in enumerate(shots, start=1)]
    js = [push_js(s, t0) for s in shots]
    SCENES.append((cid, t0, t1, "\n".join(body) + "\n" + extra_body, "".join(js) + extra_js, extra_css))


def grid_html(t0):
    g0, g1 = E.GRID
    body, js = [], []
    for k in range(9):
        x, y = (k % 3) * 640, (k // 3) * 360
        body.append(f'<div class="cell" id="grid{k}-w" style="left:{x}px;top:{y}px;width:640px;height:360px;z-index:40">'
                    f'<video id="v-grid{k}" class="clip" src="assets/clips/grid{k}.mp4" data-start="{r3(g0 - t0)}" data-duration="{r3(g1 - g0)}" muted playsinline></video></div>'
                    f'<div class="box" id="grid{k}-f" style="left:{x}px;top:{y}px;width:640px;height:360px;z-index:41;opacity:0"></div>')
        group = {4: 0, 0: 0, 8: 0, 2: 1, 6: 1, 1: 2, 7: 2, 3: 3, 5: 3}[k]
        tk = r3(g0 - t0 + group * 0.034)
        js.append(f'  tl.set("#grid{k}-f",{{opacity:0.9}},{tk});\n  tl.set("#grid{k}-f",{{opacity:0}},{r3(tk + 0.034)});\n'
                  f'  tl.set("#grid{k}-w",{{opacity:1}},{tk});\n  tl.fromTo("#grid{k}-w",{{scale:1.06}},{{scale:1,duration:0.3,ease:"expo.out"}},{tk});\n'
                  f'  tl.set("#grid{k}-w",{{opacity:0}},{r3(g1 - t0)});\n')
    return "\n".join(body), "".join(js)


# ------------------------------------------------------------------ the news: "U.S. economy" zoom, punch, corner blur
def news_scene():
    js = []
    lines = [
        NL([("A", N(0), "plain"), ("video", N(1), "weight"), ("game", N(2), "pop")], end=N(3) - 0.04),
        NL([("so", N(3), "plain"), ("popular", N(4), "weight")], end=N(5) - 0.04),
        NL([("it", N(5), "plain"), ("could", N(6), "pop"), ("cost", N(7), "streak")], end=N(8) - 0.04),
        NL([("the", N(8), "plain"), ("U.S.&nbsp;economy", N(9), "sel")], mode="tight", end=N(11) - 0.12),
    ]
    caps = "".join(line_html(L, f"ncap{k}", js) for k, L in enumerate(lines))
    s = SH["news"]
    body = (f'<div class="nz" id="nz">{vid(s, 0, 1)}'
            f'<div class="box" id="nw-hl" style="left:604px;top:652px;width:652px;height:100px;mix-blend-mode:difference;transform-origin:0 50%;opacity:0;z-index:30"></div></div>'
            f'<div class="nbm" id="nbm"><div class="nz" id="nzb">{vid(SH["newsblur"], 0, 1)}</div></div>'
            f'<div class="nz" id="nzc" style="z-index:60">{caps}</div>')
    # zoom 1: from "U.S. economy" onto the highlight, slowly speeding up; zoom 2: the punch into the FOX banner, faster still
    cx, cy, s1 = 1015, 548, 1.13
    t1, tz = r3(N(9)), r3(N(11) - 0.17)
    zx, zy, k = 1206, 980, 2.3
    z1 = f'x:{r3(cx * (1 - s1))},y:{r3(cy * (1 - s1))},scale:{s1}'
    z2 = f'x:{r3(960 - k * zx)},y:{r3(700 - k * zy)},scale:{k}'
    js.append(f'  tl.set("#nz,#nzb,#nzc",{{x:0,y:0,scale:1,transformOrigin:"0 0"}},0);\n'
              f'  tl.to("#nz,#nzb,#nzc",{{{z1},duration:{r3(tz - t1)},ease:"power2.in"}},{t1});\n'
              f'  tl.to("#nz,#nzb,#nzc",{{{z2},duration:0.4,ease:"power3.in"}},{tz});\n'
              f'  tl.fromTo("#nbm",{{opacity:0}},{{opacity:0.42,duration:{r3(tz - t1)},ease:"power2.in"}},{t1});\n'
              f'  tl.to("#nbm",{{opacity:0.85,duration:0.4,ease:"power2.in"}},{tz});\n'
              f'  tl.to("#nbm",{{opacity:0,duration:0.35,ease:"power2.out"}},{r3(tz + 0.42)});\n'
              f'  tl.set("#nw-hl",{{opacity:1,scaleX:0}},{r3(N(12) + 0.02)});\n'
              f'  tl.to("#nw-hl",{{scaleX:1,duration:0.3,ease:"power2.out"}},{r3(N(12) + 0.02)});\n'
              f'  tl.fromTo("#nz",{{rotation:0}},{{rotation:0.5,duration:0.05,yoyo:true,repeat:3,ease:"none"}},{r3(N(13))});\n')
    css = """
.nz{position:absolute;inset:0;}
.nbm{position:absolute;inset:0;z-index:20;opacity:0;-webkit-mask-image:radial-gradient(ellipse 60% 62% at 50% 50%, rgba(0,0,0,0) 38%, rgba(0,0,0,0.55) 68%, #000 100%);mask-image:radial-gradient(ellipse 60% 62% at 50% 50%, rgba(0,0,0,0) 38%, rgba(0,0,0,0.55) 68%, #000 100%);}
"""
    SCENES.append(("news", 0.0, NEWS_DUR, body, "".join(js), css))


# ------------------------------------------------------------------ reference 7: the logo card and the white card
BAR = [3, 8, 16, 24, 35, 47, 61, 77, 95, 116, 135, 155, 173, 191, 206, 218, 229, 237, 244, 250, 254, 258, 260, 262, 263]


def r7_scene():
    R = E.R7
    t0, t1, tz, tw = R["t0"], R["t1"], R["tz"], R["tw"]
    L = lambda t: r3(fr(t) - t0)
    js, body = [], []
    body.append('<div class="r7bg" id="r7bg"></div>')
    order = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
    tiles = []
    for k, (c, r) in enumerate(order):
        tk = r3(k * 0.0834)
        x, y = c * 640, r * 360
        tiles.append(f'<div class="r7tile" id="r7t{k}-w" style="left:{x}px;top:{y}px">'
                     f'<video id="v-r7t{k}" class="clip" src="assets/clips/r7t{k}.mp4" data-start="0" data-duration="{r3(tw - t0)}" muted playsinline></video>'
                     f'<div class="inv" id="r7t{k}-i"></div></div>')
        js.append(f'  tl.set("#r7t{k}-w",{{opacity:1}},{L(t0 + tk)});\n  tl.set("#r7t{k}-i",{{opacity:1}},{L(t0 + tk)});\n'
                  f'  tl.set("#r7t{k}-i",{{opacity:0}},{r3(L(t0 + tk) + F)});\n')
    body.append(f'<div class="r7g" id="r7g">{"".join(tiles)}</div>')
    js.append(f'  tl.set("#r7g",{{scale:1,transformOrigin:"50% 50%"}},0);\n  tl.set("#r7g",{{scale:1.5}},{L(tz)});\n')
    # phase 1: "GTA VI" on the grey card, each word a heavy flash on its word
    lt = lambda t: r3(t - t0)                  # scene-local time
    p1 = Line([("GTA", lt(W(22)), "", "weight"), ("VI", lt(W(23)), "", "weight")], "tight", end=lt(tz), ink=True, size="r7")
    body.append(line_html(p1, "r7a", js, drift=26))
    # the zoom: a square flash the frame before, the logo rising into the card, one dimmed frame
    zf = L(tz) - F
    body.append('<div class="r7sq" id="r7sq1" style="left:166px;top:68px;width:640px;height:677px;background:#fff;mix-blend-mode:difference"></div>'
                '<div class="r7sq" id="r7sq2" style="left:615px;top:350px;width:190px;height:395px;background:rgba(72,72,72,0.92)"></div>')
    js.append(f'  tl.set("#r7sq1,#r7sq2",{{opacity:1}},{r3(zf)});\n  tl.set("#r7sq1,#r7sq2",{{opacity:0}},{L(tz)});\n')
    body.append('<img id="r7logo" class="r7logo" src="assets/img/gta6_logo.png" alt="GTA VI logo" />')
    js.append(f'  tl.set("#r7logo",{{opacity:1,y:26}},{L(tz)});\n  tl.to("#r7logo",{{y:0,duration:{r3(3 * F)},ease:"power2.out"}},{L(tz)});\n')
    body.append('<div class="r7sq" id="r7dim" style="left:480px;top:270px;width:960px;height:540px;background:rgba(38,38,38,0.58)"></div>')
    js.append(f'  tl.set("#r7dim",{{opacity:1}},{r3(L(tz) + F)});\n  tl.set("#r7dim",{{opacity:0}},{r3(L(tz) + 2 * F)});\n')
    # phase 2: words spread across the frame on their words: "GTA | logo | VI", then "took" on the left tile,
    # "13 years" and "to make." either side of the logo
    def slot(lid, words, xc, end, kinds=None):
        ln = Line([(txt, lt(t), "", (kinds or {}).get(txt, "plain")) for txt, t in words], "tight", end=lt(end), ink=True, size="r7")
        html = line_html(ln, lid, js, drift=18)
        return html.replace('style="top:540px"', f'style="top:540px;left:{xc - 960}px;right:{960 - xc}px"')
    # the logo sits in the middle of the card; "GTA" and "VI" slide apart from the centred pair to either side of it
    def flank(lid, word, xc):
        return slot(lid, [(word, tz)], xc, W(24) - 0.02)
    body.append(flank("r7fl", "GTA", 628))
    body.append(flank("r7fr", "VI", 1292))
    js.append(f'  tl.fromTo("#r7fl",{{x:{910 - 628}}},{{x:0,duration:{r3(6 * F)},ease:"expo.out"}},{L(tz)});\n'
              f'  tl.fromTo("#r7fr",{{x:{1028 - 1292}}},{{x:0,duration:{r3(6 * F)},ease:"expo.out"}},{L(tz)});\n')
    # "took 13 years to make." -- a normal caption line, centred, on top of every layer (Tesla style, black on the
    # light card), each word on its word, drifting slowly left
    cap = Line([("took", lt(W(24)), "", "plain"), ("13", lt(W(25)), "", "weight"), ("years", lt(W(26)), "", "pop"),
                ("to", lt(W(31)), "", "plain"), ("make.", lt(W(32)), "", "weight")], "wide", end=lt(tw), ink=True)
    cap.halo = True
    body.append(line_html(cap, "r7p", js, drift=44).replace('style="top:540px"', 'style="top:540px;z-index:40"'))
    body.append('<div class="r7sq" id="r7neg" style="left:0;top:0;width:1920px;height:1080px;background:#fff;mix-blend-mode:difference;z-index:70"></div>')
    jn = L(W(24)) + 2 * F
    js.append(f'  tl.set("#r7neg",{{opacity:1}},{r3(jn)});\n  tl.set("#r7neg",{{opacity:0}},{r3(jn + F)});\n')
    js.append(f'  tl.set("#r7logo,#r7g",{{opacity:0}},{L(tw)});\n')
    # phase 3: the white card. "And yet, nobody seems to have" word by word, then "moved on." in a heavy flash while
    # two curved black bars close in (the reel's per-frame curve, 24 fps, its fastest frame on "moved")
    wbody = ['<div class="r7wbg"></div>']
    run = Line([(("yet," if i == 48 else WT(i)), lt(W(i)), "", "plain") for i in range(47, 53)], "wide", end=lt(W(53) - 0.01), ink=True)
    wbody.append(line_html(run, "r7b", js, drift=45))
    emph = Line([("moved", lt(W(53)), "", "weight"), ("on.", lt(W(54)), "", "weight")], "tight", end=lt(t1), ink=True, size="big")
    wbody.append(line_html(emph, "r7c", js, drift=20))
    wbody.append('<div class="bar top" id="r7bt"></div><div class="bar bot" id="r7bb"></div>')
    tb0 = W(53) - 10 / 23.976
    vmax = max(BAR[i + 1] - BAR[i] for i in range(len(BAR) - 1))
    js.append(f'  tl.set("#r7bt",{{y:0}},0);\n  tl.set("#r7bb",{{y:0}},0);\n')
    for i in range(len(BAR) - 1):
        ta = r3(tb0 + i / 23.976 - t0)
        v = (BAR[i + 1] - BAR[i]) / vmax
        bow = r3(18 + 104 * v)            # elliptical edge: ~7.6 px sag at full speed, ~1.4 px at rest
        blur = r3(1.6 + 2.6 * v)
        y = r3(BAR[i + 1] * 1.5)
        js.append(f'  tl.to("#r7bt",{{y:{y},borderBottomLeftRadius:"2500px {bow}px",borderBottomRightRadius:"2500px {bow}px",filter:"blur({blur}px)",duration:{r3(1 / 23.976)},ease:"none"}},{ta});\n'
                  f'  tl.to("#r7bb",{{y:{-y},borderTopLeftRadius:"2500px {bow}px",borderTopRightRadius:"2500px {bow}px",filter:"blur({blur}px)",duration:{r3(1 / 23.976)},ease:"none"}},{ta});\n')
    # film dust on the card: a few specks that move every second frame
    specks = [(312, 410, 3, 2), (1508, 620, 2, 2), (874, 731, 2, 7), (1260, 388, 3, 3), (540, 690, 2, 2), (1702, 452, 5, 1),
              (1066, 575, 2, 2), (402, 520, 2, 5)]
    for k, (x, y, w, h) in enumerate(specks):
        wbody.append(f'<div class="speck" id="sp{k}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>')
        for j in range(0, int((t1 - tw) * 15)):
            on = (j * 7 + k * 3) % 5 < 2
            js.append(f'  tl.set("#sp{k}",{{opacity:{0.55 if on else 0},x:{((j * 37 + k * 53) % 41) - 20},y:{((j * 29 + k * 17) % 31) - 15}}},{r3(L(tw) + j * 2 * F)});\n')
    # square flashes before the cut: the inverting slab, the translucent bar, the translucent grey slab
    wbody.append('<div class="r7sq" id="r7f1" style="left:0;top:300px;width:665px;height:480px;background:#fff;mix-blend-mode:difference"></div>'
                 '<div class="r7sq" id="r7f2" style="left:1080px;top:225px;width:240px;height:630px;background:rgba(128,128,128,0.78)"></div>'
                 '<div class="r7sq" id="r7f3" style="left:185px;top:285px;width:875px;height:540px;background:#8a8a8a;mix-blend-mode:difference;opacity:0"></div>')
    for k, back in ((1, 6), (2, 5), (3, 4)):
        tt = r3(fr(t1) - t0 - back / 23.976)
        js.append(f'  tl.set("#r7f{k}",{{opacity:{0.92 if k == 3 else 1}}},{tt});\n  tl.set("#r7f{k}",{{opacity:0}},{r3(tt + F)});\n')
    body.append(f'<div class="r7w" id="r7w">{"".join(wbody)}</div>')
    js.append(f'  tl.set("#r7w",{{opacity:1}},{L(tw)});\n')
    css = """
.r7bg{position:absolute;inset:0;background:radial-gradient(ellipse 70% 70% at 50% 46%, #e4e4e2 0%, #d6d6d4 50%, #bdbdbb 100%);}
.r7g{position:absolute;inset:0;}
.r7tile{position:absolute;width:640px;height:360px;overflow:hidden;opacity:0;}
.r7tile video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.inv{position:absolute;inset:0;background:#fff;mix-blend-mode:difference;opacity:0;}
.r7logo{position:absolute;left:776px;top:395px;width:368px;height:280px;object-fit:contain;opacity:0;z-index:10;}
.r7sq{position:absolute;opacity:0;z-index:60;}
.r7w{position:absolute;inset:0;opacity:0;z-index:80;overflow:hidden;}
.r7wbg{position:absolute;inset:0;background:radial-gradient(ellipse 68% 75% at 50% 50%, #ececea 0%, #dededc 45%, #c6c6c4 100%);}
.bar{position:absolute;left:-1540px;width:5000px;height:1100px;background:#030303;z-index:50;}
.bar.top{top:-1100px;border-bottom-left-radius:2500px 18px;border-bottom-right-radius:2500px 18px;}
.bar.bot{top:1080px;border-top-left-radius:2500px 18px;border-top-right-radius:2500px 18px;}
.speck{position:absolute;background:#2a2a2a;border-radius:1px;opacity:0;z-index:5;}
"""
    SCENES.append(("r7", t0, t1, "\n".join(body), "".join(js), css))


# ------------------------------------------------------------------ "freedom." in big type: glow + difference
def freedom_title(t0):
    t = W(90) - t0
    body = '<div class="hero" id="fh"><div class="hw" id="fhw"><span class="ht" id="fht">freedom</span></div></div>'
    a, b = r3(fr(t)), r3(fr(t) + F)
    glow = "0 0 46px rgba(255,255,255,0.75), 0 0 14px rgba(255,255,255,0.7), 0 4px 30px rgba(0,0,0,0.55)"
    js = (f'  tl.set("#fhw",{{opacity:0,scale:1.32}},0);\n'
          f'  tl.set("#fhw",{{opacity:1}},{a});\n'
          f'  tl.set("#fht",{{WebkitTextStrokeWidth:"0.05em",textShadow:"{BLOOM}",filter:"brightness(1.25)"}},{a});\n'
          f'  tl.set("#fhw",{{scale:1.14,filter:"blur(1.6px)"}},{b});\n'
          f'  tl.set("#fht",{{WebkitTextStrokeWidth:"0.014em",textShadow:"{glow}",filter:"brightness(1)"}},{r3(b + F)});\n'
          f'  tl.fromTo("#fhw",{{scale:1.1,filter:"blur(0px)"}},{{scale:1.0,duration:0.7,ease:"expo.out"}},{r3(b + F)});\n'
          f'  tl.to("#fhw",{{scale:0.965,duration:{r3(TOTAL - t0 - b - 0.75)},ease:"none"}},{r3(b + 0.75)});\n')
    css = """
.hero{position:absolute;left:0;right:0;top:300px;height:400px;display:flex;align-items:center;justify-content:center;z-index:50;}
.hw{position:relative;font-family:"Heros",sans-serif;font-size:250px;letter-spacing:-0.045em;line-height:1;}
.ht{position:relative;display:block;color:#fff;font-weight:700;-webkit-text-stroke:0.014em #fff;}
"""
    return body, js, css


def build_scenes():
    news_scene()
    SCENES.append(("cj", NEWS_DUR, VO_OFFSET, vid(SH["cj"], NEWS_DUR, 1),
                   f'  tl.fromTo("#cj-w",{{scale:1.08}},{{scale:1.0,duration:{r3(VO_OFFSET - NEWS_DUR)},ease:"power2.out"}},0);\n', ""))
    t0 = E.SPAN["sa"][0]
    gb, gj = grid_html(t0)
    section("sa", gb, gj)
    r7_scene()
    section("se")
    section("sf")
    section("sg")
    hb, hj, hc = freedom_title(E.SPAN["sh"][0])
    section("sh", hb, hj, hc)
    for cid, a, b, body, js, css in SCENES:
        open(os.path.join(P, "compositions", cid + ".html"), "w", encoding="utf-8").write(comp(cid, b - a, body, js, css))


# ------------------------------------------------------------------ fx: white flashes, the reel's square flashes, textures
def build_fx():
    skip = [(E.R7["t0"] - 0.05, E.R7["t1"] + 0.05), (E.SPAN["sg"][0] - 0.05, E.SPAN["sg"][1] - 0.05)]
    cuts = sorted({s["start"] for s in E.SHOTS if 0.5 < s["start"] < TOTAL - 0.5 and not s["id"].startswith(("grid", "r7t"))})
    flashes = [NEWS_DUR, cut(90)]
    body, js = [], []
    for k, t in enumerate(flashes):
        fid = f"fl{k}"
        body.append(f'<div class="clip" id="{fid}" data-start="{r3(t - 0.1)}" data-duration="0.45" style="position:absolute;inset:0;z-index:50"><div class="fl" id="{fid}i"></div></div>')
        js.append(f'  tl.fromTo("#{fid}i",{{opacity:0}},{{opacity:0.85,duration:0.1,ease:"power2.in"}},{r3(t - 0.1)});\n'
                  f'  tl.set("#{fid}i",{{opacity:1}},{r3(t)});\n'
                  f'  tl.to("#{fid}i",{{opacity:0,duration:0.3,ease:"power2.out"}},{r3(t + 0.034)});\n')
    PAT = [
        [("inv", 520, 300, 980, 420)],
        [("glass", 240, 120, 760, 520), ("card", 1180, 560, 420, 300)],
        [("bar", 1090, 260, 70, 560)],
        [("grey", 430, 455, 1060, 170)],
        [("inv", 0, 0, 1920, 380), ("inv", 1320, 640, 600, 440)],
        [("card", 700, 330, 560, 420)],
        [("inv", 120, 620, 860, 300)],
        [("bar", 560, 180, 90, 720), ("grey", 900, 470, 600, 140)],
    ]
    STY = {"inv": "background:#fff;mix-blend-mode:difference;", "card": "background:rgba(236,236,232,0.92);",
           "bar": "background:rgba(255,255,255,0.95);", "glass": "background:rgba(255,255,255,0.24);",
           "grey": "background:rgba(128,128,128,0.75);"}
    sq = 0
    for i, t in enumerate(cuts):
        if any(a <= t <= b for a, b in skip) or any(abs(t - f) < 0.3 for f in flashes) or i % 5 in (1, 2, 4):
            continue
        pat = PAT[(i * 3) % len(PAT)]
        boxes = "".join(f'<div class="gb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{STY[kind]}"></div>' for kind, x, y, w, h in pat)
        body.append(f'<div class="clip" id="sq{i:03d}" data-start="{r3(t - 0.034)}" data-duration="0.067" style="position:absolute;inset:0;z-index:49">{boxes}</div>')
        sq += 1
    css = """
.fl{position:absolute;inset:0;background:#fff;opacity:0;}
.gb{position:absolute;}
.grain{position:absolute;left:-200px;top:-200px;width:2320px;height:1480px;background:url("assets/tex/grain.png");opacity:0.07;mix-blend-mode:overlay;}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.42) 100%);}
.tex{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover;}
"""
    body.append('<div class="vig" id="fx-vig"></div><div class="grain" id="fx-grain"></div>'
                '<img class="tex" id="tx1" src="assets/tex/ht_grunge.jpg" alt="" style="mix-blend-mode:overlay;opacity:0.08" />'
                '<img class="tex" id="tx2" src="assets/tex/ht_paper.jpg" alt="" style="mix-blend-mode:soft-light;opacity:0.05" />'
                '<img class="tex" id="tx3" src="assets/tex/ht_dots.jpg" alt="" style="mix-blend-mode:overlay;opacity:0.12" />')
    js.append(f'  tl.fromTo("#fx-grain",{{x:0,y:0}},{{x:-180,y:-140,duration:{TOTAL},ease:"steps({int(TOTAL * 15)})"}},0);\n')
    open(os.path.join(P, "compositions", "fx.html"), "w", encoding="utf-8").write(comp("fx", TOTAL, "\n".join(body), "".join(js), css))
    return flashes, sq


def build_root():
    hosts = []
    for k, (cid, t0, t1, *_r) in enumerate(SCENES):
        hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{r3(t0)}" '
                     f'data-duration="{r3(t1 - t0)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:{k + 1}"></div>')
    hosts.append(f'      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:90;pointer-events:none"></div>')
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:80;pointer-events:none"></div>')
    aud = [f'      <audio id="a-news" src="assets/audio/news_line.wav" data-start="0" data-duration="{NEWS_DUR}" data-track-index="5" data-volume="1"></audio>',
           f'      <audio id="a-cj" src="assets/audio/cj_line.wav" data-start="{NEWS_DUR}" data-duration="{r3(VO_OFFSET - NEWS_DUR + 0.2)}" data-track-index="6" data-volume="1"></audio>',
           f'      <audio id="a-vo" src="assets/audio/vo4.wav" data-start="{VO_OFFSET}" data-duration="{E.VO_DUR}" data-track-index="7" data-volume="1"></audio>']
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="bg" style="position:absolute;inset:0;background:#000"></div>
{chr(10).join(hosts)}
{chr(10).join(aud)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(P, "index.html"), "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    LS = build_captions()
    build_scenes()
    fl, sq = build_fx()
    build_root()
    keep = {c[0] for c in SCENES} | {"captions", "fx"}
    for f in os.listdir(os.path.join(P, "compositions")):
        if f.endswith(".html") and f[:-5] not in keep:
            os.remove(os.path.join(P, "compositions", f))
    print(f"v4: {TOTAL} s | captions {len(LS)} lines | scenes {len(SCENES)} | square flashes {sq} | white flashes {len(fl)} | no sfx")
