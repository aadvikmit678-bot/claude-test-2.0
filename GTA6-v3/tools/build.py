"""v2 builder (Tesla Roadster grammar): footage sections, one caption track, square flashes.
Writes gta6-edit/index.html and compositions/*.html from tools/edl.py.   usage: python -I -X utf8 build.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl
from edl import W, cut, N, VO_OFFSET, NEWS_DUR, TOTAL

P = edl.PROJ
os.makedirs(os.path.join(P, "compositions"), exist_ok=True)
SH = {s["id"]: s for s in edl.SHOTS}
r3 = lambda x: round(x, 3)

FONTS = """
@font-face{font-family:"InterV";src:url("assets/fonts/InterVar-latin.woff2") format("woff2");font-weight:100 900;font-style:normal;}
"""
# text-shadow stacks of one shape so GSAP can interpolate between them
SET = "0 0 22px rgba(255,255,255,0.42), 0 0 4px rgba(255,255,255,0.26), 0 2px 18px rgba(0,0,0,0.72)"
POP = "0 0 26px rgba(255,255,255,0.85), 0 0 7px rgba(255,255,255,0.85), 0 2px 16px rgba(0,0,0,0.30)"
BLOOM = "0 0 34px rgba(255,255,255,1), 0 0 10px rgba(255,255,255,1), 0 2px 16px rgba(0,0,0,0)"
INK = "0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0)"

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
.w{position:relative;display:inline-block;}
.gh{visibility:hidden;font-weight:540;}
.ik{position:absolute;left:-60%;right:-60%;top:0;bottom:0;display:flex;justify-content:center;align-items:flex-start;z-index:1;}
.tx{display:inline-block;font-weight:540;opacity:0;text-shadow:""" + SET + """;}
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


# ------------------------------------------------------------------ the Tesla word entrances (t: composition time)
def ent_js(sel, kind, t):
    t = r3(t); a = r3(t + 0.034)
    if kind == "pop":       # on its frame, a touch bright, settles in ~3 frames
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.03,filter:"blur(0.6px) brightness(1.55)",textShadow:"{POP}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SET}",duration:0.13,ease:"expo.out"}},{a});\n')
    if kind == "bloom":     # 'flying' / 'car': black weight in a white bloom, medium three frames later
        return (f'  tl.set("{sel}",{{opacity:1,fontWeight:900,scale:1.05,filter:"blur(1.2px) brightness(1.9)",textShadow:"{BLOOM}"}},{t});\n'
                f'  tl.to("{sel}",{{fontWeight:540,scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SET}",duration:0.2,ease:"expo.out"}},{a});\n')
    if kind == "scale":     # 'world' / 'using': lands large and drops into place
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.32,fontWeight:760,filter:"blur(1.4px) brightness(1.5)",textShadow:"{BLOOM}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,fontWeight:540,filter:"blur(0px) brightness(1)",textShadow:"{SET}",duration:0.18,ease:"expo.out"}},{a});\n')
    if kind == "streak":    # 'world' frame 8: a vertical smear for two frames
        return (f'  tl.set("{sel}",{{opacity:0.9,scaleY:2.8,scaleX:0.94,filter:"blur(2.2px) brightness(1.7)"}},{t});\n'
                f'  tl.to("{sel}",{{scaleY:1,scaleX:1,opacity:1,filter:"blur(0px) brightness(1)",duration:0.12,ease:"power3.out"}},{a});\n')
    if kind == "soft":      # 'So' / 'the': simply on
        return f'  tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.05,ease:"none"}},{t});\n'
    raise ValueError(kind)


SMALL = {"a", "an", "the", "to", "of", "in", "it", "on", "and", "so", "for", "at", "be", "is", "was", "if", "you", "it's",
         "he's", "i", "that", "with", "are", "from", "but", "they", "what", "just", "how", "this", "your", "that's", "all", "an"}


class Line:
    def __init__(self, words, mode="wide", end=None, y=540):
        self.words, self.mode, self.end, self.y = words, mode, end, y   # words: [(text, t, cls, kind)]


def VL(a, b, mode="wide", end=None, texts=None, kinds=None, cls=None):
    texts, kinds, cls = texts or {}, kinds or {}, cls or {}
    ws, k = [], 0
    for i in range(a, b + 1):
        txt = texts.get(i, edl.WT(i))
        bare = txt.lower().strip(",.?!")
        if i in kinds:
            kd = kinds[i]
        elif bare in SMALL:
            kd = "soft"
        else:
            kd = ("bloom", "pop", "pop", "bloom", "pop", "streak", "pop")[(i * 5 + k) % 7]
            k += 1
        ws.append((txt, W(i), cls.get(i, ""), kd))
    return Line(ws, mode, end)


def lines():
    L = [
        Line([("A", N(0), "", "soft"), ("video", N(1), "", "bloom"), ("game", N(2), "", "pop")], end=N(3) - 0.04),
        Line([("so", N(3), "", "soft"), ("popular", N(4), "", "bloom")], end=N(5) - 0.04),
        Line([("it", N(5), "", "soft"), ("could", N(6), "", "pop"), ("cost", N(7), "", "streak")], end=N(8) - 0.04),
        Line([("the", N(8), "", "soft"), ("U.S.&nbsp;economy", N(9), "sel", "sel")], mode="tight", end=N(11) - 0.12),
        Line([("Ah", NEWS_DUR + 0.04, "", "bloom"), ("shit,", NEWS_DUR + 0.56, "", "scale")], end=NEWS_DUR + 1.48),
        Line([("here", NEWS_DUR + 1.54, "", "pop"), ("we", NEWS_DUR + 1.66, "", "soft"), ("go", NEWS_DUR + 1.80, "", "pop"),
              ("again.", NEWS_DUR + 2.00, "", "bloom")], end=VO_OFFSET),
    ]
    V = [  # (a, b, opts)
        (0, 2, {}), (3, 5, {"kinds": {3: "bloom", 5: "scale"}}), (6, 9, {}), (10, 12, {"mode": "tight", "cls": {12: "card"}, "kinds": {12: "card", 11: "bloom"}}),
        (13, 15, {"end": cut(16) + 0.02}), (18, 21, {}),
        (22, 24, {"kinds": {22: "bloom"}}), (25, 26, {"mode": "tight", "kinds": {25: "scale", 26: "bloom"}}),
        (27, 30, {"kinds": {28: "scale", 29: "bloom", 30: "pop"}}), (31, 32, {}),
        (33, 37, {}), (38, 38, {"kinds": {38: "scale"}}), (39, 41, {"mode": "tight", "kinds": {40: "bloom", 41: "bloom"}}), (42, 46, {"kinds": {46: "bloom"}}),
        (47, 48, {}), (49, 54, {}), (55, 56, {"kinds": {56: "scale"}}),
        (57, 60, {}), (61, 63, {"kinds": {62: "scale"}}), (64, 68, {}), (69, 72, {"kinds": {71: "bloom", 72: "scale"}}),
        (73, 74, {"kinds": {74: "bloom"}}), (75, 78, {}), (79, 81, {"kinds": {79: "scale", 81: "scale"}}),
        (82, 85, {}), (86, 89, {}), (90, 90, {"kinds": {90: "bloom"}}),
        (91, 93, {}), (94, 96, {"mode": "tight", "kinds": {94: "scale"}}), (97, 100, {"y": 880}), (101, 103, {"mode": "tight", "y": 880}),
        (104, 106, {"kinds": {105: "bloom", 106: "bloom"}}), (107, 110, {}), (111, 114, {}), (115, 118, {}), (119, 120, {"kinds": {120: "streak"}}),
        (121, 124, {}), (125, 127, {"texts": {125: "ASPIRINE", 127: "PANZER"}, "kinds": {125: "bloom", 127: "scale"}}),
        (128, 131, {}), (132, 134, {}),
        (135, 137, {}), (138, 142, {}), (143, 147, {"kinds": {146: "bloom", 147: "pop"}}), (148, 150, {"kinds": {150: "bloom"}}),
        (151, 153, {}), (154, 158, {}), (159, 160, {"kinds": {160: "scale"}}), (161, 162, {"kinds": {162: "scale"}}),
        (163, 164, {"kinds": {164: "scale"}}), (165, 169, {"texts": {166: "owning"}, "kinds": {169: "bloom"}}),
        (170, 174, {}), (175, 180, {"kinds": {180: "bloom"}}), (181, 185, {"texts": {181: "But"}}),
        (186, 187, {"mode": "tight", "kinds": {187: "scale"}}), (188, 194, {"kinds": {194: "bloom"}}),
        (195, 198, {}), (199, 202, {}),
        (203, 207, {"y": 880}), (208, 211, {"y": 880}), (212, 212, {"kinds": {212: "bloom"}}), (213, 216, {}), (217, 221, {"kinds": {221: "bloom"}}),
        (222, 225, {}), (226, 231, {}),
        (232, 235, {"mode": "tight", "cls": {235: "card"}, "kinds": {235: "card", 234: "bloom"}}),
        (236, 240, {"kinds": {236: "bloom"}, "y": 900}), (241, 242, {"mode": "tight", "kinds": {241: "scale", 242: "bloom"}}),
        (243, 248, {}),
        (249, 253, {}), (254, 258, {"kinds": {255: "bloom", 256: "bloom"}}), (259, 260, {}), (261, 265, {}), (266, 267, {"kinds": {267: "bloom"}}),
        (268, 270, {}), (271, 274, {"kinds": {273: "bloom", 274: "bloom"}}), (275, 277, {}), (278, 281, {}),
        (282, 283, {"mode": "tight", "kinds": {282: "scale"}}), (284, 288, {"kinds": {287: "bloom"}}),
    ]
    for k, (a, b, o) in enumerate(V):
        nxt = W(V[k + 1][0]) - 0.04 if k + 1 < len(V) else 103.80
        ln = VL(a, b, mode=o.get("mode", "wide"), end=o.get("end", nxt), texts=o.get("texts"), kinds=o.get("kinds"), cls=o.get("cls"))
        ln.y = o.get("y", 540)
        L.append(ln)
    return L


def build_captions():
    body, js = [], []
    LS = lines()
    for li, L in enumerate(LS):
        lid = f"cap{li:02d}"
        t0 = r3(L.words[0][1] - 0.03)
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
                js.append(f'  tl.set("#{wid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{r3(t)});\n'
                          f'  tl.to("#{wid}",{{clipPath:"inset(0% 0% 0% 0%)",duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(t)});\n'
                          f'  tl.fromTo("#{wid}b",{{scaleX:0}},{{scaleX:1,duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(t)});\n')
            elif kd == "card":   # Tesla's white card behind 'and': a white box, the word in ink
                extra = f'<span class="cardbox" id="{wid}c"></span>'
                js.append(f'  tl.set("#{wid}c",{{opacity:1,scaleY:1.6,scaleX:1.1}},{r3(t)});\n'
                          f'  tl.to("#{wid}c",{{scaleY:1,scaleX:1,duration:0.16,ease:"expo.out"}},{r3(t + 0.034)});\n'
                          f'  tl.set("#{wid}",{{opacity:1}},{r3(t + 0.034)});\n')
            else:
                js.append(ent_js("#" + wid, kd, t))
            spans.append(f'<span class="w {cls}">{extra}<span class="gh">{txt}</span><span class="ik"><span class="tx" id="{wid}">{txt}</span></span></span>')
        body.append(f'<div id="{lid}" class="clip cl" data-start="{t0}" data-duration="{dur}" data-track-index="0" style="top:{L.y}px">'
                    f'<div class="row {L.mode}" id="{lid}r">{"".join(spans)}</div></div>')
        js.append(f'  tl.fromTo("#{lid}r",{{x:26}},{{x:-18,duration:{dur},ease:"power2.out"}},{t0});\n')
    html = comp("captions", TOTAL, "\n".join(body), "".join(js))
    open(os.path.join(P, "compositions", "captions.html"), "w", encoding="utf-8").write(html)
    return LS


# ------------------------------------------------------------------ footage sections
def vid(s, t0, z):
    st, du = r3(s["start"] - t0), r3(s["end"] - s["start"])
    return (f'<div class="shot" id="{s["id"]}-w" style="z-index:{z}">'
            f'<video id="v-{s["id"]}" class="clip" src="assets/clips/{s["id"]}.mp4" data-start="{st}" data-duration="{du}" muted playsinline></video></div>')


def push_js(s, t0):
    if not s.get("push"):
        return ""
    a, b = s["push"]
    return f'  tl.fromTo("#{s["id"]}-w",{{scale:{a}}},{{scale:{b},duration:{r3(s["end"] - s["start"])},ease:"none"}},{r3(s["start"] - t0)});\n'


SCENES = []


def section(cid, t0, t1, extra_body="", extra_js=""):
    shots = [s for s in edl.SHOTS if t0 - 1e-6 <= s["start"] < t1 - 1e-6 and not s["id"].startswith("grid") and s["id"] not in ("news", "cj")]
    body = [vid(s, t0, z) for z, s in enumerate(shots, start=1)]
    js = [push_js(s, t0) for s in shots]
    SCENES.append((cid, t0, t1, "\n".join(body) + "\n" + extra_body, "".join(js) + extra_js))


def grid_html(t0):
    g0, g1 = edl.GRID
    body, js = [], []
    for k in range(9):
        s = SH[f"grid{k}"]
        x, y = (k % 3) * 640, (k // 3) * 360
        body.append(f'<div class="cell" id="grid{k}-w" style="left:{x}px;top:{y}px;width:640px;height:360px;z-index:40">'
                    f'<video id="v-grid{k}" class="clip" src="assets/clips/grid{k}.mp4" data-start="{r3(g0 - t0)}" data-duration="{r3(g1 - g0)}" muted playsinline></video></div>'
                    f'<div class="box" id="grid{k}-f" style="left:{x}px;top:{y}px;width:640px;height:360px;z-index:41;opacity:0"></div>')
        group = {4: 0, 0: 0, 8: 0, 2: 1, 6: 1, 1: 2, 7: 2, 3: 3, 5: 3}[k]   # three cells on the cut, the rest a frame apart
        tk = r3(g0 - t0 + group * 0.034)
        js.append(f'  tl.set("#grid{k}-f",{{opacity:0.9}},{tk});\n  tl.set("#grid{k}-f",{{opacity:0}},{r3(tk + 0.034)});\n'
                  f'  tl.set("#grid{k}-w",{{opacity:1}},{tk});\n  tl.fromTo("#grid{k}-w",{{scale:1.06}},{{scale:1,duration:0.3,ease:"expo.out"}},{tk});\n'
                  f'  tl.set("#grid{k}-w",{{opacity:0}},{r3(g1 - t0)});\n')
    return "\n".join(body), "".join(js)


def build_scenes():
    # the reporter: punch into the FOX 2 banner on "a billion" and mark $1 BILLION
    zx, zy, k = 1206, 980, 2.3
    tz = N(11) - 0.17
    nb = vid(SH["news"], 0, 1) + '\n<div class="box" id="nw-hl" style="left:604px;top:652px;width:652px;height:100px;mix-blend-mode:difference;transform-origin:0 50%;opacity:0;z-index:30"></div>'
    nj = (f'  tl.fromTo("#news-w",{{x:0,y:0,scale:1,transformOrigin:"0 0"}},{{x:{r3(960 - k * zx)},y:{r3(700 - k * zy)},scale:{k},duration:0.42,ease:"power3.inOut"}},{r3(tz)});\n'
          f'  tl.set("#nw-hl",{{opacity:1,scaleX:0}},{r3(N(12) + 0.02)});\n'
          f'  tl.to("#nw-hl",{{scaleX:1,duration:0.3,ease:"power2.out"}},{r3(N(12) + 0.02)});\n'
          f'  tl.fromTo("#news-w",{{rotation:0}},{{rotation:0.5,duration:0.05,yoyo:true,repeat:3,ease:"none"}},{r3(N(13))});\n')
    SCENES.append(("news", 0.0, NEWS_DUR, nb, nj))
    SCENES.append(("cj", NEWS_DUR, VO_OFFSET, vid(SH["cj"], NEWS_DUR, 1),
                   f'  tl.fromTo("#cj-w",{{scale:1.08}},{{scale:1.0,duration:{r3(VO_OFFSET - NEWS_DUR)},ease:"power2.out"}},0);\n'))
    for cid, (t0, t1) in edl.SECTION_SPAN.items():
        if cid == "sa":
            gb, gj = grid_html(t0)
            section(cid, t0, t1, gb, gj)
        else:
            section(cid, t0, t1)
    for cid, t0, t1, body, js in SCENES:
        open(os.path.join(P, "compositions", cid + ".html"), "w", encoding="utf-8").write(comp(cid, t1 - t0, body, js))


# ------------------------------------------------------------------ fx: white flashes, Tesla's square flashes, grain
def build_fx():
    cuts = sorted({s["start"] for s in edl.SHOTS if 0.5 < s["start"] < TOTAL - 0.5 and not s["id"].startswith("grid")})
    flashes = [NEWS_DUR, cut(90), cut(91), cut(212), cut(222), cut(241), 103.85]
    body, js = [], []
    for k, t in enumerate(flashes):
        fid = f"fl{k}"
        body.append(f'<div class="clip" id="{fid}" data-start="{r3(t - 0.1)}" data-duration="0.45" style="position:absolute;inset:0;z-index:50"><div class="fl" id="{fid}i"></div></div>')
        js.append(f'  tl.fromTo("#{fid}i",{{opacity:0}},{{opacity:0.85,duration:0.1,ease:"power2.in"}},{r3(t - 0.1)});\n'
                  f'  tl.set("#{fid}i",{{opacity:1}},{r3(t)});\n'
                  f'  tl.to("#{fid}i",{{opacity:0,duration:0.3,ease:"power2.out"}},{r3(t + 0.034)});\n')
    # square flashes: the Tesla reel's two-frame rectangles at a cut (inverted slab, light card, tall bar, glass box)
    PAT = [
        [("inv", 520, 300, 980, 420)],
        [("glass", 240, 120, 760, 520), ("card", 1180, 560, 420, 300)],
        [("bar", 1090, 260, 70, 560)],
        [("glass", 430, 455, 1060, 170)],
        [("inv", 0, 0, 1920, 380), ("inv", 1320, 640, 600, 440)],
        [("card", 700, 330, 560, 420)],
        [("inv", 120, 620, 860, 300)],
        [("bar", 560, 180, 90, 720), ("glass", 900, 470, 600, 140)],
    ]
    STY = {"inv": "background:#fff;mix-blend-mode:difference;", "card": "background:rgba(236,236,232,0.92);",
           "bar": "background:rgba(255,255,255,0.95);", "glass": "background:rgba(255,255,255,0.24);"}
    sq_times = []
    for i, t in enumerate(cuts):
        if any(abs(t - f) < 0.3 for f in flashes) or i % 5 in (1, 2, 4):   # ~40% of cuts, never on a white flash
            continue
        pat = PAT[(i * 3) % len(PAT)]
        gid = f"sq{i:03d}"
        boxes = "".join(f'<div class="gb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{STY[kind]}"></div>' for kind, x, y, w, h in pat)
        body.append(f'<div class="clip" id="{gid}" data-start="{r3(t - 0.034)}" data-duration="0.067" style="position:absolute;inset:0;z-index:49">{boxes}</div>')
        sq_times.append(t)
    css = """
.fl{position:absolute;inset:0;background:#fff;opacity:0;}
.gb{position:absolute;}
.grain{position:absolute;left:-200px;top:-200px;width:2320px;height:1480px;background:url("assets/tex/grain.png");opacity:0.07;mix-blend-mode:overlay;}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.42) 100%);}
"""
    body.append('<div class="vig" id="fx-vig"></div><div class="grain" id="fx-grain"></div>')
    js.append(f'  tl.fromTo("#fx-grain",{{x:0,y:0}},{{x:-180,y:-140,duration:{TOTAL},ease:"steps({int(TOTAL * 15)})"}},0);\n')
    open(os.path.join(P, "compositions", "fx.html"), "w", encoding="utf-8").write(comp("fx", TOTAL, "\n".join(body), "".join(js), css))
    return flashes, sq_times


def build_root(flashes, sq_times):
    hosts = []
    for k, (cid, t0, t1, *_r) in enumerate(SCENES):
        hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{r3(t0)}" '
                     f'data-duration="{r3(t1 - t0)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:{k + 1}"></div>')
    hosts.append(f'      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:90;pointer-events:none"></div>')
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:80;pointer-events:none"></div>')
    aud = [f'      <audio id="a-news" src="assets/audio/news_line.wav" data-start="0" data-duration="{NEWS_DUR}" data-track-index="5" data-volume="1"></audio>',
           f'      <audio id="a-cj" src="assets/audio/cj_line.wav" data-start="{NEWS_DUR}" data-duration="{r3(VO_OFFSET - NEWS_DUR + 0.2)}" data-track-index="6" data-volume="1"></audio>',
           f'      <audio id="a-vo" src="assets/audio/vo.wav" data-start="{VO_OFFSET}" data-duration="96.44" data-track-index="7" data-volume="1"></audio>']
    sfx = [("impact-bass-1.mp3", t - 0.02, 0.75) for t in flashes]
    sfx += [(("glitch-1.mp3", "glitch-2.mp3", "glitch-3.mp3")[k % 3], t - 0.05, 0.32) for k, t in enumerate(sq_times) if k % 3 == 0]
    sfx += [("riser.mp3", cut(90) - 1.2, 0.3), ("whoosh-cinematic.mp3", cut(91) - 0.25, 0.45), ("riser.mp3", 103.85 - 1.3, 0.3)]
    for k, (f, t, v) in enumerate(sorted(sfx, key=lambda x: x[1])):
        aud.append(f'      <audio id="sfx{k:02d}" src="assets/sfx/{f}" data-start="{r3(max(0, t))}" data-track-index="{8 + k}" data-volume="{v}"></audio>')
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
    return len(sfx)


if __name__ == "__main__":
    LS = build_captions()
    build_scenes()
    fl, sq = build_fx()
    n_sfx = build_root(fl, sq)
    # stale v1 scene files
    keep = {c[0] for c in SCENES} | {"captions", "fx"}
    for f in os.listdir(os.path.join(P, "compositions")):
        if f.endswith(".html") and f[:-5] not in keep:
            os.remove(os.path.join(P, "compositions", f))
    print(f"captions {len(LS)} lines | scenes {len(SCENES)} | square flashes {len(sq)} | white flashes {len(fl)} | sfx {n_sfx}")
