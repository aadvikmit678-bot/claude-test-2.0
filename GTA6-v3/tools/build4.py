"""v4 builder, part 1 (to "... sitting in front of the family computer,"): v2's cut with the user's notes.
Writes gta6-edit/index.html and compositions/*.html from tools/edl4.py.   usage: python -I -X utf8 tools/build4.py

Type: v2's, exactly (Inter variable, 76 px, weight 540, v2's glow and word entrances: soft, pop, bloom, scale, streak;
the white card behind "19th", the blue box on "U.S. economy"). Captions do not slide. Black type on the light cards.
No sound effects, no textures (v2's grain and vignette only). Square flashes before most cuts (reference 7's
white / grey / white rectangles on consecutive frames).
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
fr = lambda t: round(round(t * 30) / 30, 4)

# ------------------------------------------------------------------ v2's type
FONTS = """
@font-face{font-family:"InterV";src:url("assets/fonts/InterVar-latin.woff2") format("woff2");font-weight:100 900;font-style:normal;}
"""
SET = "0 0 22px rgba(255,255,255,0.42), 0 0 4px rgba(255,255,255,0.26), 0 2px 18px rgba(0,0,0,0.72)"
POP = "0 0 26px rgba(255,255,255,0.85), 0 0 7px rgba(255,255,255,0.85), 0 2px 16px rgba(0,0,0,0.30)"
BLOOM = "0 0 34px rgba(255,255,255,1), 0 0 10px rgba(255,255,255,1), 0 2px 16px rgba(0,0,0,0)"
INK = "0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0)"
HALO = "0 0 2px rgba(255,255,255,1), 0 0 7px rgba(255,255,255,1), 0 0 16px rgba(255,255,255,0.9)"   # black type over the logo

CSS = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;}
.shot{position:absolute;inset:0;overflow:hidden;}
.shot video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.cell{position:absolute;overflow:hidden;opacity:0;}
.cell video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.box{position:absolute;background:#fff;}
.cl{position:absolute;left:0;right:0;height:300px;margin-top:-150px;display:flex;align-items:center;justify-content:center;pointer-events:none;}
.row{display:flex;align-items:baseline;justify-content:center;white-space:nowrap;font-family:"InterV",sans-serif;font-size:76px;line-height:1.2;letter-spacing:-0.03em;color:#F2F2F0;}
.row.wide{column-gap:1.1em;} .row.tight{column-gap:0.26em;}
.row.side{font-size:64px;}
.row.ink{color:#141414;}
.w{position:relative;display:inline-block;}
.gh{visibility:hidden;font-weight:540;}
.ik{position:absolute;left:-60%;right:-60%;top:0;bottom:0;display:flex;justify-content:center;align-items:flex-start;z-index:1;}
.tx{display:inline-block;font-weight:540;opacity:0;text-shadow:""" + SET + """;}
.row.ink .tx{text-shadow:""" + INK + """;}
.row.ink.halo .tx{text-shadow:""" + HALO + """;}
.w.card .tx{color:#141414;text-shadow:""" + INK + """;}
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


def ent_js(sel, kind, t, rest=SET, pop=POP, bloom=BLOOM):
    """v2's word entrances"""
    t = r3(t); a = r3(t + 0.034)
    if kind == "pop":
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.03,filter:"blur(0.6px) brightness(1.55)",textShadow:"{pop}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{rest}",duration:0.13,ease:"expo.out"}},{a});\n')
    if kind == "bloom":
        return (f'  tl.set("{sel}",{{opacity:1,fontWeight:900,scale:1.05,filter:"blur(1.2px) brightness(1.9)",textShadow:"{bloom}"}},{t});\n'
                f'  tl.to("{sel}",{{fontWeight:540,scale:1,filter:"blur(0px) brightness(1)",textShadow:"{rest}",duration:0.2,ease:"expo.out"}},{a});\n')
    if kind == "scale":
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.32,fontWeight:760,filter:"blur(1.4px) brightness(1.5)",textShadow:"{bloom}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,fontWeight:540,filter:"blur(0px) brightness(1)",textShadow:"{rest}",duration:0.18,ease:"expo.out"}},{a});\n')
    if kind == "streak":
        return (f'  tl.set("{sel}",{{opacity:0.9,scaleY:2.8,scaleX:0.94,filter:"blur(2.2px) brightness(1.7)"}},{t});\n'
                f'  tl.to("{sel}",{{scaleY:1,scaleX:1,opacity:1,filter:"blur(0px) brightness(1)",duration:0.12,ease:"power3.out"}},{a});\n')
    if kind == "soft":
        return f'  tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.05,ease:"none"}},{t});\n'
    raise ValueError(kind)


SMALL = {"a", "an", "the", "to", "of", "in", "it", "on", "and", "so", "for", "at", "be", "is", "was", "if", "you", "it's",
         "he's", "i", "that", "with", "are", "from", "but", "they", "what", "just", "how", "this", "your", "that's", "all"}


class Line:
    def __init__(self, words, mode="wide", end=None, y=540, ink=False, halo=False, size=""):
        self.words, self.mode, self.end, self.y, self.ink, self.halo, self.size = words, mode, end, y, ink, halo, size


def kind_for(i, k, txt, kinds):
    if i in kinds:
        return kinds[i], k
    if txt.lower().strip(",.?!") in SMALL:
        return "soft", k
    return ("bloom", "pop", "pop", "bloom", "pop", "streak", "pop")[(i * 5 + k) % 7], k + 1


def VL(idx, mode="wide", end=None, texts=None, kinds=None, cls=None, shift=0.0, **kw):
    """v2's caption line from VO word indices (times shifted by -shift for scene-local lines)"""
    texts, kinds, cls = texts or {}, kinds or {}, cls or {}
    ws, k = [], 0
    for i in idx:
        if not has(i):
            continue
        txt = texts.get(i, WT(i))
        kd, k = kind_for(i, k, txt, kinds)
        ws.append((txt, r3(W(i) - shift), cls.get(i, ""), kd))
    return Line(ws, mode, None if end is None else r3(end - shift), **kw)


def line_html(L, lid, js):
    t0 = r3(L.words[0][1] - 0.03)
    last = L.words[-1][1]
    t1 = r3(min(L.end, last + 1.3)) if L.end else r3(last + 0.8)
    dur = r3(max(0.2, t1 - t0))
    rest = HALO if L.halo else (INK if L.ink else SET)
    pop = INK if L.ink else POP
    bloom = INK if L.ink else BLOOM
    spans = []
    for wi, (txt, t, cls, kd) in enumerate(L.words):
        wid = f"{lid}w{wi}"
        extra = ""
        if kd == "sel":
            extra = f'<span class="selbox" id="{wid}b"></span>'
            n = len(txt.replace("&nbsp;", " "))
            js.append(f'  tl.set("#{wid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{r3(t)});\n'
                      f'  tl.to("#{wid}",{{clipPath:"inset(0% 0% 0% 0%)",duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(t)});\n'
                      f'  tl.fromTo("#{wid}b",{{scaleX:0}},{{scaleX:1,duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(t)});\n')
        elif kd == "card":
            extra = f'<span class="cardbox" id="{wid}c"></span>'
            js.append(f'  tl.set("#{wid}c",{{opacity:1,scaleY:1.6,scaleX:1.1}},{r3(t)});\n'
                      f'  tl.to("#{wid}c",{{scaleY:1,scaleX:1,duration:0.16,ease:"expo.out"}},{r3(t + 0.034)});\n'
                      f'  tl.set("#{wid}",{{opacity:1}},{r3(t + 0.034)});\n')
        else:
            js.append(ent_js("#" + wid, kd, t, rest, pop, bloom))
        spans.append(f'<span class="w {cls}">{extra}<span class="gh">{txt}</span><span class="ik"><span class="tx" id="{wid}">{txt}</span></span></span>')
    cls_row = " ".join(x for x in ("row", L.mode, "ink" if L.ink else "", "halo" if L.halo else "", L.size) if x)
    return (f'<div id="{lid}" class="clip cl" data-start="{t0}" data-duration="{dur}" data-track-index="0" style="top:{L.y}px">'
            f'<div class="{cls_row}" id="{lid}r">{"".join(spans)}</div></div>')


def NL(words, mode="wide", end=None):
    return Line([(txt, r3(t), "", kd) for txt, t, kd in words], mode, end)


# ------------------------------------------------------------------ captions (VO and CJ; the news lines live in the news scene)
def build_captions():
    body, js = [], []
    L = [NL([("Ah", NEWS_DUR + 0.04, "bloom"), ("shit,", NEWS_DUR + 0.56, "scale")], end=NEWS_DUR + 1.48),
         NL([("here", NEWS_DUR + 1.54, "pop"), ("we", NEWS_DUR + 1.66, "soft"), ("go", NEWS_DUR + 1.80, "pop"),
             ("again.", NEWS_DUR + 2.00, "bloom")], end=VO_OFFSET)]
    V = [
        ([0, 1, 2], {}), ([3, 4, 5], {"kinds": {3: "bloom", 5: "scale"}}), ([6, 7, 8, 9], {}),
        ([10, 11, 12], {"mode": "tight", "cls": {12: "card"}, "kinds": {12: "card", 11: "bloom"}}),
        ([13, 14, 15], {"end": cut(16) + 0.02}), ([18, 19, 20, 21], {"end": E.R7["t0"] - 0.02}),
        ([55, 57, 58, 59, 60], {"texts": {57: "why"}, "kinds": {57: "scale"}}),
        ([61, 62, 63], {"kinds": {62: "scale"}}), ([64, 65, 66, 67, 68], {}),
        ([69, 70, 71, 72], {"kinds": {71: "bloom", 72: "scale"}}),
        ([73, 74], {"kinds": {74: "bloom"}}), ([75, 76, 77, 78], {}), ([79, 80, 81], {"kinds": {79: "scale", 81: "scale"}}),
        ([82, 83, 84, 85], {}), ([86, 87, 88, 89], {"end": cut(90)}),
        ([91, 92, 93], {"end": cut(94)}),
        ([94, 95, 96], {"mode": "tight", "kinds": {94: "scale"}, "end": E.TCARD - 3 * F}),
        ([104, 105, 106], {"kinds": {105: "bloom", 106: "bloom"}}), ([107, 108, 109, 110], {}), ([111, 112, 113, 114], {}),
        ([115, 116, 117, 118], {}), ([119, 120], {"kinds": {120: "streak"}, "end": TOTAL}),
    ]
    for k, (idx, o) in enumerate(V):
        nxt = W(V[k + 1][0][0]) - 0.04 if k + 1 < len(V) else TOTAL
        L.append(VL(idx, mode=o.get("mode", "wide"), end=o.get("end", nxt), texts=o.get("texts"), kinds=o.get("kinds"),
                    cls=o.get("cls")))
    for li, ln in enumerate(L):
        body.append(line_html(ln, f"cap{li:02d}", js))
    open(os.path.join(P, "compositions", "captions.html"), "w", encoding="utf-8").write(comp("captions", TOTAL, "\n".join(body), "".join(js)))
    return L


# ------------------------------------------------------------------ footage
def vid(s, t0, z, cls="shot", dur=None):
    st, du = r3(s["start"] - t0), r3(dur if dur is not None else s["end"] - s["start"])
    return (f'<div class="{cls}" id="{s["id"]}-w" style="z-index:{z}">'
            f'<video id="v-{s["id"]}" class="clip" src="assets/clips/{s["id"]}.mp4" data-start="{st}" data-duration="{du}" muted playsinline></video></div>')


def push_js(s, t0):
    if not s.get("push"):
        return ""
    a, b = s["push"]
    return f'  tl.fromTo("#{s["id"]}-w",{{scale:{a}}},{{scale:{b},duration:{r3(s["end"] - s["start"])},ease:"none"}},{r3(s["start"] - t0)});\n'


SCENES = []
SKIP = ("grid", "r7t", "news", "cj", "nmoney", "bd")


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


# ------------------------------------------------------------------ the news: zoom onto "U.S. economy", cut to the money on "a billion"
def news_scene():
    js = []
    tm = E.NEWS_TM
    lines = [
        NL([("A", N(0), "soft"), ("video", N(1), "bloom"), ("game", N(2), "pop")], end=N(3) - 0.04),
        NL([("so", N(3), "soft"), ("popular", N(4), "bloom")], end=N(5) - 0.04),
        NL([("it", N(5), "soft"), ("could", N(6), "pop"), ("cost", N(7), "streak")], end=N(8) - 0.04),
        NL([("the", N(8), "soft"), ("U.S.&nbsp;economy", N(9), "sel")], mode="tight", end=N(11) - 0.12),
    ]
    caps = "".join(line_html(L, f"ncap{k}", js) for k, L in enumerate(lines))
    money = NL([("a", N(11), "soft"), ("billion", N(12), "bloom"), ("dollars", N(13), "pop")], end=NEWS_DUR - 0.02)
    mcap = line_html(money, "ncapm", js)
    body = (f'<div class="nz" id="nz">{vid(SH["news"], 0, 1, dur=tm)}</div>'
            f'<div class="nbm" id="nbm"><div class="nz" id="nzb">{vid(SH["newsblur"], 0, 1, dur=tm)}</div></div>'
            f'<div class="nz" id="nzc" style="z-index:60">{caps}</div>'
            f'{vid(SH["nmoney"], 0, 70)}<div style="position:absolute;inset:0;z-index:75">{mcap}</div>')
    cx, cy, s1 = 1015, 548, 1.13
    t1 = r3(N(9))
    z1 = f'x:{r3(cx * (1 - s1))},y:{r3(cy * (1 - s1))},scale:{s1}'
    js.append(f'  tl.set("#nz,#nzb,#nzc",{{x:0,y:0,scale:1,transformOrigin:"0 0"}},0);\n'
              f'  tl.to("#nz,#nzb,#nzc",{{{z1},duration:{r3(tm - t1)},ease:"power2.in"}},{t1});\n'
              f'  tl.fromTo("#nbm",{{opacity:0}},{{opacity:0.45,duration:{r3(tm - t1)},ease:"power2.in"}},{t1});\n'
              f'  tl.set("#nbm",{{opacity:0}},{r3(tm)});\n')
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
    lt = lambda t: r3(t - t0)
    js, body = [], []
    body.append('<div class="r7bg" id="r7bg"></div>')
    order = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
    tiles = []
    for k, (c, r) in enumerate(order):
        tk = r3(k * 0.0834)
        tiles.append(f'<div class="r7tile" id="r7t{k}-w" style="left:{c * 640}px;top:{r * 360}px">'
                     f'<video id="v-r7t{k}" class="clip" src="assets/clips/r7t{k}.mp4" data-start="0" data-duration="{r3(tw - t0)}" muted playsinline></video>'
                     f'<div class="inv" id="r7t{k}-i"></div></div>')
        js.append(f'  tl.set("#r7t{k}-w",{{opacity:1}},{L(t0 + tk)});\n  tl.set("#r7t{k}-i",{{opacity:1}},{L(t0 + tk)});\n'
                  f'  tl.set("#r7t{k}-i",{{opacity:0}},{r3(L(t0 + tk) + F)});\n')
    body.append(f'<div class="r7g" id="r7g">{"".join(tiles)}</div>')
    js.append(f'  tl.set("#r7g",{{scale:1,transformOrigin:"50% 50%"}},0);\n  tl.set("#r7g",{{scale:1.5}},{L(tz)});\n')
    # "GTA VI" on the plain card
    p1 = Line([("GTA", lt(W(22)), "", "bloom"), ("VI", lt(W(23)), "", "bloom")], "tight", end=lt(tz), ink=True)
    body.append(line_html(p1, "r7a", js))
    # the zoom: a square flash the frame before, the logo rising into the middle of the card, one dimmed frame
    body.append('<div class="r7sq" id="r7sq1" style="left:166px;top:68px;width:640px;height:677px;background:#fff;mix-blend-mode:difference"></div>'
                '<div class="r7sq" id="r7sq2" style="left:615px;top:350px;width:190px;height:395px;background:rgba(72,72,72,0.92)"></div>')
    js.append(f'  tl.set("#r7sq1,#r7sq2",{{opacity:1}},{r3(L(tz) - F)});\n  tl.set("#r7sq1,#r7sq2",{{opacity:0}},{L(tz)});\n')
    body.append('<img id="r7logo" class="r7logo" src="assets/img/gta6_logo.png" alt="GTA VI logo" />')
    js.append(f'  tl.set("#r7logo",{{opacity:1,y:26}},{L(tz)});\n  tl.to("#r7logo",{{y:0,duration:{r3(3 * F)},ease:"power2.out"}},{L(tz)});\n')
    body.append('<div class="r7sq" id="r7dim" style="left:480px;top:270px;width:960px;height:540px;background:rgba(38,38,38,0.58)"></div>')
    js.append(f'  tl.set("#r7dim",{{opacity:1}},{r3(L(tz) + F)});\n  tl.set("#r7dim",{{opacity:0}},{r3(L(tz) + 2 * F)});\n')

    # "GTA" and "VI" slide apart to either side of the logo
    def flank(lid, word, xc, x_from):
        ln = Line([(word, lt(tz), "", "soft")], "tight", end=lt(W(24) - 0.02), ink=True)
        html = line_html(ln, lid, js).replace('style="top:540px"', f'style="top:540px;left:{xc - 960}px;right:{960 - xc}px"')
        js.append(f'  tl.fromTo("#{lid}",{{x:{x_from - xc}}},{{x:0,duration:{r3(6 * F)},ease:"expo.out"}},{L(tz)});\n')
        return html
    body.append(flank("r7fl", "GTA", 628, 900))
    body.append(flank("r7fr", "VI", 1292, 1036))
    # "took 13 years to make." -- a normal caption, centred, on top of everything
    cap = Line([("took", lt(W(24)), "", "soft"), ("13", lt(W(25)), "", "scale"), ("years", lt(W(26)), "", "pop"),
                ("to", lt(W(31)), "", "soft"), ("make.", lt(W(32)), "", "bloom")], "wide", end=lt(tw), ink=True, halo=True)
    body.append(line_html(cap, "r7p", js).replace('style="top:540px"', 'style="top:540px;z-index:40"'))
    body.append('<div class="r7sq" id="r7neg" style="left:0;top:0;width:1920px;height:1080px;background:#fff;mix-blend-mode:difference;z-index:70"></div>')
    jn = L(W(24)) + 2 * F
    js.append(f'  tl.set("#r7neg",{{opacity:1}},{r3(jn)});\n  tl.set("#r7neg",{{opacity:0}},{r3(jn + F)});\n')
    js.append(f'  tl.set("#r7logo,#r7g",{{opacity:0}},{L(tw)});\n')
    # the white card: the bars start to close right after "And yet" (the reel's per-frame curve), "moved on." in the band
    wbody = ['<div class="r7wbg"></div>']
    run = Line([(("yet," if i == 48 else WT(i)), lt(W(i)), "", "soft") for i in range(47, 53)], "wide", end=lt(W(53) - 0.01), ink=True)
    wbody.append(line_html(run, "r7b", js))
    emph = Line([("moved", lt(W(53)), "", "bloom"), ("on.", lt(W(54)), "", "bloom")], "tight", end=lt(t1), ink=True)
    wbody.append(line_html(emph, "r7c", js))
    wbody.append('<div class="bar top" id="r7bt"></div><div class="bar bot" id="r7bb"></div>')
    tb0 = W(48) + 0.16
    vmax = max(BAR[i + 1] - BAR[i] for i in range(len(BAR) - 1))
    js.append('  tl.set("#r7bt",{y:0},0);\n  tl.set("#r7bb",{y:0},0);\n')
    for i in range(len(BAR) - 1):
        ta = r3(tb0 + i / 23.976 - t0)
        v = (BAR[i + 1] - BAR[i]) / vmax
        bow, blur, y = r3(18 + 104 * v), r3(1.6 + 2.6 * v), r3(BAR[i + 1] * 1.5)
        js.append(f'  tl.to("#r7bt",{{y:{y},borderBottomLeftRadius:"2500px {bow}px",borderBottomRightRadius:"2500px {bow}px",filter:"blur({blur}px)",duration:{r3(1 / 23.976)},ease:"none"}},{ta});\n'
                  f'  tl.to("#r7bb",{{y:{-y},borderTopLeftRadius:"2500px {bow}px",borderTopRightRadius:"2500px {bow}px",filter:"blur({blur}px)",duration:{r3(1 / 23.976)},ease:"none"}},{ta});\n')
    specks = [(312, 410, 3, 2), (1508, 620, 2, 2), (874, 731, 2, 7), (1260, 388, 3, 3), (540, 690, 2, 2), (1702, 452, 5, 1),
              (1066, 575, 2, 2), (402, 520, 2, 5)]
    for k, (x, y, w, h) in enumerate(specks):
        wbody.append(f'<div class="speck" id="sp{k}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>')
        for j in range(0, int((t1 - tw) * 15)):
            on = (j * 7 + k * 3) % 5 < 2
            js.append(f'  tl.set("#sp{k}",{{opacity:{0.55 if on else 0},x:{((j * 37 + k * 53) % 41) - 20},y:{((j * 29 + k * 17) % 31) - 15}}},{r3(L(tw) + j * 2 * F)});\n')
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


# ------------------------------------------------------------------ "freedom": big, white, glowing, centred (v2's type)
def freedom_title(t0):
    t = r3(W(90) - t0)
    body = '<div class="hero" id="fh"><div class="hw" id="fhw"><span class="ht" id="fht">freedom</span></div></div>'
    glow = "0 0 46px rgba(255,255,255,0.75), 0 0 14px rgba(255,255,255,0.7), 0 4px 30px rgba(0,0,0,0.55)"
    js = (f'  tl.set("#fhw",{{opacity:0}},0);\n'
          f'  tl.set("#fhw",{{opacity:1,scale:1.05}},{t});\n'
          f'  tl.set("#fht",{{fontWeight:900,filter:"blur(1.2px) brightness(1.9)",textShadow:"{BLOOM}"}},{t});\n'
          f'  tl.to("#fht",{{fontWeight:540,filter:"blur(0px) brightness(1)",textShadow:"{glow}",duration:0.2,ease:"expo.out"}},{r3(t + 0.034)});\n'
          f'  tl.to("#fhw",{{scale:1,duration:0.2,ease:"expo.out"}},{r3(t + 0.034)});\n')
    css = """
.hero{position:absolute;left:0;right:0;top:300px;height:400px;display:flex;align-items:center;justify-content:center;z-index:50;}
.hw{position:relative;font-family:"InterV",sans-serif;font-size:240px;letter-spacing:-0.04em;line-height:1;}
.ht{position:relative;display:block;color:#fff;font-weight:540;}
"""
    return body, js, css


# ------------------------------------------------------------------ "10 years old, sitting in front of the family computer,"
def tv_scene():
    """the kid at the TV (Vice City on the screen) full screen with "10 years old,"; then reference 1's move: a bright
    frame, two negative frames, the picture as a card with a glowing border, a white card, and the picture in the card
    with the words written in glow either side of it"""
    t0, t1 = E.TV
    dur = r3(t1 - t0)
    tc = r3(fr(E.TCARD) - t0)
    js = []
    cw, ch, cx, cy = 520, 860, 700, 110                        # the card
    iw, ih = 1670, 940                                         # the picture inside it, 0.87x
    body = [f'<div class="tvf" id="tvf"><video id="v-tvf" class="clip" src="assets/clips/tv10.mp4" data-start="0" data-duration="{dur}" muted playsinline></video></div>',
            '<div class="tvglow" id="tvg"></div><div class="tvinv" id="tvi"></div><div class="tvbg" id="tvb"></div>',
            f'<div class="tvc" id="tvc" style="left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px">'
            f'<video id="v-tvc" class="clip" src="assets/clips/tv10.mp4" data-start="0" data-duration="{dur}" muted playsinline style="left:{(cw - iw) // 2 - 40}px;top:{(ch - ih) // 2 + 30}px;width:{iw}px;height:{ih}px"></video>'
            '<div class="tvw" id="tvw"></div></div>']
    a = lambda n: r3(tc + n * F)
    body.append(f'<div class="tvsq" id="tvsq" style="left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px"></div>')
    js.append(f'  tl.set("#tvg",{{opacity:0.62}},{a(-6)});\n'
              f'  tl.set("#tvi",{{opacity:1}},{a(-5)});\n  tl.set("#tvg",{{opacity:0.32}},{a(-5)});\n'
              f'  tl.set("#tvi,#tvg,#tvf",{{opacity:0}},{a(-3)});\n  tl.set("#tvb",{{opacity:1}},{a(-3)});\n'
              f'  tl.set("#tvsq",{{opacity:1,scale:0.1}},{a(-3)});\n  tl.set("#tvsq",{{scale:0.45}},{a(-2)});\n  tl.set("#tvsq",{{opacity:0}},{a(-1)});\n'
              f'  tl.set("#tvc",{{opacity:1,boxShadow:"0 0 0 5px rgba(255,255,255,1), 0 0 60px rgba(255,255,255,0.95)"}},{a(-1)});\n'
              f'  tl.set("#tvw",{{opacity:1}},{a(-1)});\n  tl.set("#tvw",{{opacity:0}},{a(0)});\n'
              f'  tl.to("#tvc",{{boxShadow:"0 0 0 3px rgba(255,255,255,0.85), 0 0 34px rgba(255,255,255,0.45)",duration:0.25,ease:"power2.out"}},{a(0)});\n'
              f'  tl.fromTo("#tvc",{{scale:1}},{{scale:0.965,duration:{r3(dur - tc)},ease:"none"}},{a(0)});\n')
    left = VL([97, 98, 99, 100], mode="tight", end=t1, shift=t0, size="side")
    right = VL([101, 102, 103], mode="tight", end=t1, shift=t0, size="side")
    for L in (left, right):
        L.words[0] = (L.words[0][0], max(L.words[0][1], tc), L.words[0][2], L.words[0][3])
    lh = line_html(left, "tvl", js).replace('style="top:540px"', f'style="top:540px;left:0;right:{1920 - cx + 34}px;justify-content:flex-end;z-index:20"')
    rh = line_html(right, "tvr", js).replace('style="top:540px"', f'style="top:540px;left:{cx + cw + 34}px;right:0;justify-content:flex-start;z-index:20"')
    body += [lh, rh]
    css = """
.tvf{position:absolute;inset:0;}
.tvf video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.tvglow{position:absolute;inset:0;opacity:0;background:radial-gradient(ellipse 60% 60% at 50% 45%, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.55) 55%, rgba(255,255,255,0.2) 100%);z-index:5;}
.tvinv{position:absolute;inset:0;opacity:0;background:#fff;mix-blend-mode:difference;z-index:4;}
.tvbg{position:absolute;inset:0;opacity:0;background:radial-gradient(ellipse 55% 60% at 50% 50%, #151515 0%, #050505 70%, #000 100%);z-index:6;}
.tvc{position:absolute;overflow:hidden;opacity:0;z-index:7;}
.tvc video{position:absolute;object-fit:cover;}
.tvw{position:absolute;inset:0;background:#fff;opacity:0;}
.tvsq{position:absolute;background:#fff;opacity:0;z-index:8;transform-origin:50% 50%;box-shadow:0 0 50px rgba(255,255,255,0.95);}
"""
    SCENES.append(("tv", t0, t1, "\n".join(body), "".join(js), css))


def build_scenes():
    news_scene()
    SCENES.append(("cj", NEWS_DUR, E.T_BD, vid(SH["cj"], NEWS_DUR, 1, dur=E.T_BD - NEWS_DUR),
                   f'  tl.fromTo("#cj-w",{{scale:1.08}},{{scale:1.0,duration:{r3(E.T_BD - NEWS_DUR)},ease:"power2.out"}},0);\n', ""))
    # "here we go again. That's exactly how" -- the beat-drop clip (the user's reference), until "millions"
    SCENES.append(("bd", E.T_BD, E.SPAN["sa"][0], vid(SH["bd"], E.T_BD, 1), "", ""))
    gb, gj = grid_html(E.SPAN["sa"][0])
    section("sa", gb, gj)
    r7_scene()
    section("se")
    section("sf")
    section("sg")
    hb, hj, hc = freedom_title(E.SPAN["sh"][0])
    section("sh", hb, hj, hc)
    section("si")
    tv_scene()
    section("sj")
    for cid, a, b, body, js, css in SCENES:
        open(os.path.join(P, "compositions", cid + ".html"), "w", encoding="utf-8").write(comp(cid, b - a, body, js, css))


# ------------------------------------------------------------------ fx: white flashes, square flashes before the cuts, grain, vignette
SEQ = [   # one list of boxes per frame, the last frame just before the cut (reference 7: white, grey, white)
    [[("white", 590, 120, 760, 430)], [("grey", 1450, 30, 260, 640)], [("white", 330, 380, 700, 300)]],
    [[("inv", 520, 300, 980, 420)], [("glass", 240, 120, 760, 520), ("card", 1180, 560, 420, 300)]],
    [[("bar", 1090, 260, 70, 560)], [("grey", 430, 455, 1060, 170)], [("inv", 1120, 120, 620, 380)]],
    [[("inv", 0, 0, 1920, 380), ("inv", 1320, 640, 600, 440)], [("card", 700, 330, 560, 420)]],
    [[("white", 120, 620, 860, 300)], [("bar", 560, 180, 90, 720), ("grey", 900, 470, 600, 140)]],
    [[("grey", 1280, 160, 420, 560)], [("white", 260, 260, 640, 380)], [("glass", 800, 600, 900, 300)]],
]
STY = {"inv": "background:#fff;mix-blend-mode:difference;", "card": "background:rgba(236,236,232,0.92);",
       "bar": "background:rgba(255,255,255,0.95);", "glass": "background:rgba(255,255,255,0.24);",
       "grey": "background:rgba(128,128,128,0.78);", "white": "background:rgba(250,250,248,0.96);"}


def build_fx():
    skip = [(E.R7["t0"] - 0.05, E.R7["t1"] + 0.05), (E.SPAN["sg"][0] + 0.05, E.SPAN["sg"][1] - 0.05), (E.TV[0] + 0.05, E.TV[1] - 0.05)]
    cuts = sorted({s["start"] for s in E.SHOTS if 0.5 < s["start"] < TOTAL - 0.3 and not s["id"].startswith(("grid", "r7t"))}
                  | {E.R7["t0"], E.TV[0]})
    flashes = [NEWS_DUR, cut(90)]
    body, js = [], []
    for k, t in enumerate(flashes):
        fid = f"fl{k}"
        body.append(f'<div class="clip" id="{fid}" data-start="{r3(t - 0.1)}" data-duration="0.45" style="position:absolute;inset:0;z-index:50"><div class="fl" id="{fid}i"></div></div>')
        js.append(f'  tl.fromTo("#{fid}i",{{opacity:0}},{{opacity:0.85,duration:0.1,ease:"power2.in"}},{r3(t - 0.1)});\n'
                  f'  tl.set("#{fid}i",{{opacity:1}},{r3(t)});\n'
                  f'  tl.to("#{fid}i",{{opacity:0,duration:0.3,ease:"power2.out"}},{r3(t + 0.034)});\n')
    n = 0
    for i, t in enumerate(cuts):
        if any(a <= t <= b for a, b in skip) or any(abs(t - f) < 0.3 for f in flashes) or i % 4 == 3:
            continue
        seq = SEQ[(i * 5) % len(SEQ)]
        tc = fr(t)
        for j, frame in enumerate(seq):
            ts = r3(tc - (len(seq) - j) * F)
            boxes = "".join(f'<div class="gb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{STY[kind]}"></div>' for kind, x, y, w, h in frame)
            body.append(f'<div class="clip" id="sq{i:03d}{j}" data-start="{ts}" data-duration="{r3(F)}" style="position:absolute;inset:0;z-index:49">{boxes}</div>')
        n += 1
    css = """
.fl{position:absolute;inset:0;background:#fff;opacity:0;}
.gb{position:absolute;}
.grain{position:absolute;left:-200px;top:-200px;width:2320px;height:1480px;background:url("assets/tex/grain.png");opacity:0.07;mix-blend-mode:overlay;}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.42) 100%);}
"""
    body.append('<div class="vig" id="fx-vig"></div><div class="grain" id="fx-grain"></div>')
    js.append(f'  tl.fromTo("#fx-grain",{{x:0,y:0}},{{x:-180,y:-140,duration:{TOTAL},ease:"steps({int(TOTAL * 15)})"}},0);\n')
    open(os.path.join(P, "compositions", "fx.html"), "w", encoding="utf-8").write(comp("fx", TOTAL, "\n".join(body), "".join(js), css))
    return flashes, n


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
    print(f"v4: {TOTAL} s | captions {len(LS)} lines | scenes {len(SCENES)} | square-flash runs {sq} | white flashes {len(fl)} | no sfx, no textures")
