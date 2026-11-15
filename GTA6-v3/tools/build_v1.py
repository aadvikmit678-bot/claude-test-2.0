"""Write gta6-edit/index.html and compositions/*.html from tools/edl.py.
usage: python -I -X utf8 build.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl
from edl import W, WE, cut, N, C, VO_OFFSET, NEWS_DUR, TOTAL

P = edl.PROJ
os.makedirs(os.path.join(P, "compositions"), exist_ok=True)
SH = {s["id"]: s for s in edl.SHOTS}
r3 = lambda x: round(x, 3)

# ------------------------------------------------------------------ shared style
FONTS = """
@font-face{font-family:"InterV";src:url("assets/fonts/InterVar-latin.woff2") format("woff2");font-weight:100 900;font-style:normal;}
@font-face{font-family:"Instrument Serif";src:url("assets/fonts/InstrumentSerif-Regular.woff2") format("woff2");font-weight:400;font-style:normal;}
@font-face{font-family:"Instrument Serif";src:url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2");font-weight:400;font-style:italic;}
@font-face{font-family:"Heros";src:url("assets/fonts/TeXGyreHeros-Bold.woff2") format("woff2");font-weight:700;font-style:normal;}
@font-face{font-family:"Gochi Hand";src:url("assets/fonts/GochiHand-latin.woff2") format("woff2");font-weight:400;font-style:normal;}
"""
# text-shadow stacks share one shape so GSAP can interpolate between them
SET = "0 0 16px rgba(255,255,255,0.26), 0 0 3px rgba(255,255,255,0.16), 0 2px 18px rgba(0,0,0,0.55)"
BLOOM = "0 0 30px rgba(255,255,255,0.95), 0 0 9px rgba(255,255,255,0.95), 0 2px 18px rgba(0,0,0,0)"
SGLOW = "0 0 28px rgba(255,255,255,0.42), 0 0 6px rgba(255,255,255,0.30), 0 2px 18px rgba(0,0,0,0.55)"
FLASH = "0 0 70px rgba(255,255,255,1), 0 0 20px rgba(255,255,255,1), 0 2px 18px rgba(0,0,0,0)"
INK = "0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0), 0 1px 0px rgba(0,0,0,0.10)"
INKB = "0 0 14px rgba(0,0,0,0.35), 0 0 4px rgba(0,0,0,0.35), 0 1px 0px rgba(0,0,0,0)"
RED = "0 0 30px rgba(255,64,96,0.60), 0 0 8px rgba(255,64,96,0.45), 0 2px 18px rgba(0,0,0,0.55)"

CSS = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;}
.shot{position:absolute;inset:0;overflow:hidden;}
.shot video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.full{position:absolute;inset:0;}
.cl{position:absolute;left:0;right:0;height:300px;margin-top:-150px;display:flex;align-items:center;justify-content:center;pointer-events:none;}
.row{display:flex;align-items:baseline;justify-content:center;white-space:nowrap;font-family:"InterV",sans-serif;font-size:64px;line-height:1.18;letter-spacing:-0.02em;color:#F4F4F1;}
.row.wide{column-gap:0.62em;} .row.tight{column-gap:0.26em;}
.row.ink{color:#151515;}
.w{position:relative;display:inline-block;}
.gh{visibility:hidden;font-weight:500;}
.ik{position:absolute;left:-60%;right:-60%;top:0;bottom:0;display:flex;justify-content:center;align-items:flex-start;}
.tx{display:inline-block;font-weight:500;opacity:0;text-shadow:""" + SET + """;}
.row.ink .tx{text-shadow:""" + INK + """;}
.w.serif .gh,.w.serif .tx{font-family:"Instrument Serif",serif;font-weight:400;font-size:1.85em;letter-spacing:-0.01em;line-height:1;}
.w.serifi .gh,.w.serifi .tx{font-family:"Instrument Serif",serif;font-style:italic;font-weight:400;font-size:1.85em;letter-spacing:-0.01em;line-height:1;}
.w.big .gh,.w.big .tx{font-size:2.7em;}
.w.bold .gh,.w.bold .tx{font-family:"Heros",sans-serif;font-weight:700;font-size:1.6em;letter-spacing:-0.03em;line-height:1;}
.w.hand .gh,.w.hand .tx{font-family:"Gochi Hand",cursive;font-weight:400;font-size:1.9em;letter-spacing:0.02em;line-height:1;}
.w.red .tx{color:#FF4060;}
.box{position:absolute;background:#fff;}
.card{position:absolute;overflow:hidden;opacity:0;box-shadow:0 30px 70px rgba(0,0,0,0.55),0 0 0 2px rgba(255,255,255,0.10);}
.card video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.paper{position:absolute;inset:0;background:#ecebe7 url("assets/tex/paper_light.png") center/cover;}
.grunge{position:absolute;inset:0;background:#09090b url("assets/tex/ht_grunge.jpg") center/cover;}
.kick{position:absolute;left:0;right:0;text-align:center;font-family:"InterV",sans-serif;font-weight:500;font-size:28px;letter-spacing:0.42em;color:#F4F4F1;opacity:0;text-shadow:""" + SET + """;}
.hb{position:absolute;font-family:"Heros",sans-serif;font-weight:700;color:#F4F4F1;white-space:nowrap;letter-spacing:-0.03em;line-height:1;}
.strike{position:absolute;height:14px;background:#E8202A;border-radius:7px;transform-origin:0 50%;opacity:0.92;}
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


# ------------------------------------------------------------------ word tweens (t is composition-local)
def ent_js(sel, kind, t, ink=False):
    t = r3(t); a = r3(t + 0.034)
    if kind == "bloom":
        if ink:
            return (f'  tl.set("{sel}",{{opacity:1,fontWeight:900,scale:1.04,filter:"blur(1.4px)",textShadow:"{INKB}"}},{t});\n'
                    f'  tl.to("{sel}",{{fontWeight:500,scale:1,filter:"blur(0px)",textShadow:"{INK}",duration:0.22,ease:"expo.out"}},{a});\n')
        return (f'  tl.set("{sel}",{{opacity:1,fontWeight:900,scale:1.05,filter:"blur(1.2px) brightness(1.9)",textShadow:"{BLOOM}"}},{t});\n'
                f'  tl.to("{sel}",{{fontWeight:500,scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SET}",duration:0.22,ease:"expo.out"}},{a});\n')
    if kind == "scale":
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.34,fontWeight:760,filter:"blur(1.5px) brightness(1.5)",textShadow:"{BLOOM}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,fontWeight:500,filter:"blur(0px) brightness(1)",textShadow:"{INK if ink else SET}",duration:0.2,ease:"expo.out"}},{a});\n')
    if kind == "streak":
        return (f'  tl.set("{sel}",{{opacity:0.9,scaleY:2.8,scaleX:0.94,filter:"blur(2.2px) brightness(1.7)"}},{t});\n'
                f'  tl.to("{sel}",{{scaleY:1,scaleX:1,opacity:1,filter:"blur(0px) brightness(1)",duration:0.13,ease:"power3.out"}},{a});\n')
    if kind == "soft":
        return f'  tl.fromTo("{sel}",{{opacity:0,fontWeight:720}},{{opacity:1,fontWeight:500,duration:0.11,ease:"power2.out"}},{t});\n'
    if kind == "flash":   # Dario/Dimon hero entrance: whole on its frame, blown out, crisp in its glow 4-5 frames later
        glow = INK if ink else SGLOW
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.1,filter:"blur(3px) brightness(2.8)",textShadow:"{INKB if ink else FLASH}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{glow}",duration:0.2,ease:"power3.out"}},{r3(t + 0.05)});\n')
    if kind == "flashred":
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.12,filter:"blur(3px) brightness(2.6)",textShadow:"{FLASH}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{RED}",duration:0.22,ease:"power3.out"}},{r3(t + 0.05)});\n')
    raise ValueError(kind)


SMALL = {"a", "an", "the", "to", "of", "in", "it", "on", "and", "so", "for", "at", "be", "is", "was", "if", "you", "it's", "he's", "i"}


def default_ent(text, k):
    t = text.lower().strip(",.?!")
    if t in SMALL:
        return "soft"
    return "streak" if k % 5 == 3 else "bloom"


# ------------------------------------------------------------------ caption lines
class Line:
    def __init__(self, words, y=540, mode="wide", ink=False, end=None, exit="blur", start=None):
        self.words = words          # [(text, t_abs, cls, ent)]
        self.y, self.mode, self.ink, self.end, self.exit, self.start = y, mode, ink, end, exit, start


def VL(a, b, y=540, mode="wide", ink=False, end=None, exit="blur", st=None, en=None, start=None, texts=None):
    """Caption from VO words a..b. st: {idx: css class}, en: {idx: entrance}."""
    st, en = st or {}, en or {}
    ws, k = [], 0
    for i in range(a, b + 1):
        txt = (texts or {}).get(i, edl.WT(i))
        cls = st.get(i, "")
        e = en.get(i) or ("flash" if cls and cls not in ("red",) else default_ent(txt, k))
        if "red" in cls:
            e = en.get(i, "flashred")
        ws.append((txt, W(i), cls, e)); k += 1
    return Line(ws, y, mode, ink, end, exit, start)


LINES = [
    # cold open: the reporter (news-local word times) -------------------------------------------
    Line([("A", N(0), "", "soft"), ("video", N(1), "", "bloom"), ("game", N(2), "", "bloom")], end=N(3) - 0.05),
    Line([("so", N(3), "", "soft"), ("popular", N(4), "serifi", "flash")], mode="tight", end=N(5) - 0.04),
    Line([("it", N(5), "", "soft"), ("could", N(6), "", "bloom"), ("cost", N(7), "", "streak")], end=N(8) - 0.04),
    Line([("the", N(8), "", "soft"), ("U.S.&nbsp;economy", N(9), "sel", "sel")], mode="tight", end=N(11) - 0.08),
    # CJ --------------------------------------------------------------------------------------------
    Line([("Ah", NEWS_DUR + 0.02, "", "bloom"), ("shit,", NEWS_DUR + 0.56, "", "scale")], y=835, end=NEWS_DUR + 1.50),
    Line([("here", NEWS_DUR + 1.54, "", "bloom"), ("we", NEWS_DUR + 1.66, "", "soft"), ("go", NEWS_DUR + 1.80, "", "bloom"),
          ("again.", NEWS_DUR + 2.00, "serifi", "flash")], y=835, mode="wide", end=VO_OFFSET),
    # A -----------------------------------------------------------------------------------------------
    VL(0, 2, end=cut(3)),
    VL(3, 5, st={3: "serifi"}, mode="tight", end=cut(6)),
    VL(6, 9, end=cut(11)),
    VL(10, 12, st={11: "serif", 12: "serif"}, mode="tight", end=cut(13), exit="cut"),
    VL(13, 15, end=W(16) - 0.02),
    VL(18, 21, end=cut(22)),
    # B ------------------------------------------------------------------------------------------------
    VL(22, 24, mode="wide", end=cut(25), texts={22: "GTA", 23: "6"}),
    VL(25, 26, st={25: "bold", 26: "serifi"}, mode="tight", end=cut(27)),
    VL(31, 32, end=cut(33)),
    # C (on the 2025 card: top) -------------------------------------------------------------------------
    VL(33, 37, y=150, end=cut(38)),
    VL(42, 45, y=880, end=cut(46)),
    # D
    VL(47, 48, end=cut(49)),
    VL(49, 54, end=cut(55)),
    # E
    VL(55, 56, st={56: "serifi big"}, mode="tight", end=cut(57)),
    # F
    VL(57, 60, end=cut(61)),
    VL(61, 63, st={62: "bold"}, mode="tight", end=cut(64)),
    VL(64, 68, end=cut(69)),
    VL(69, 72, end=cut(73)),
    # G
    VL(73, 74, end=cut(75)),
    VL(75, 78, end=cut(79)),
    VL(79, 81, end=cut(82)),
    # H
    VL(82, 85, end=cut(86)),
    VL(86, 89, end=cut(90)),
    VL(90, 90, st={90: "serifi big"}, end=cut(91) + 0.12, exit="cut"),
    # I
    VL(94, 96, mode="tight", end=cut(97), st={94: "bold"}),
    VL(97, 100, y=985, end=cut(101)),
    VL(101, 103, y=985, end=cut(104)),
    VL(104, 106, st={105: "serif", 106: "serif"}, y=985, end=cut(107)),
    VL(107, 110, y=985, end=cut(111)),
    VL(111, 114, y=985, end=cut(115)),
    VL(115, 118, end=cut(119)),
    VL(119, 120, end=cut(121)),
    # J (notebook: ink, top band) ------------------------------------------------------------------------
    VL(121, 124, y=190, ink=True, end=cut(127)),
    VL(128, 131, y=190, ink=True, end=cut(132)),
    VL(132, 134, y=190, ink=True, end=cut(135)),
    # K
    VL(135, 137, end=cut(138)),
    VL(138, 142, end=cut(143)),
    VL(143, 147, st={146: "serifi", 147: "serifi"}, mode="wide", end=cut(148)),
    VL(148, 150, st={150: "serifi"}, end=cut(151)),
    # L
    VL(151, 153, end=cut(154)),
    VL(154, 158, st={156: "serifi"}, end=cut(159)),
    VL(159, 160, en={160: "scale"}, end=cut(161)),
    VL(161, 162, en={162: "scale"}, end=cut(163)),
    VL(163, 164, en={164: "scale"}, end=cut(165)),
    VL(165, 169, st={168: "serifi", 169: "serifi"}, texts={166: "owning"}, end=cut(170)),
    # M (paper card: ink) ----------------------------------------------------------------------------------
    VL(170, 174, ink=True, end=cut(175)),
    VL(175, 180, ink=True, st={179: "serifi", 180: "serifi"}, end=cut(181) - 0.18, exit="cut"),
    VL(181, 185, end=cut(186), texts={181: "But"}),
    VL(186, 187, st={187: "serifi big red"}, mode="tight", end=cut(188)),
    VL(188, 191, end=cut(192)),
    VL(192, 194, st={193: "serifi", 194: "serifi"}, mode="tight", end=cut(195)),
    VL(195, 198, end=cut(199)),
    VL(199, 202, end=cut(203)),
    # N
    VL(203, 207, end=cut(208)),
    VL(208, 211, end=cut(212)),
    VL(212, 212, st={212: "serifi big"}, end=cut(213)),
    VL(213, 216, end=cut(217)),
    VL(217, 221, st={221: "serifi"}, end=cut(222)),
    VL(222, 225, end=cut(226)),
    VL(226, 231, end=cut(232)),
    # O
    VL(232, 235, st={234: "serif", 235: "serif"}, mode="tight", end=cut(236), exit="cut"),
    VL(236, 240, y=880, end=cut(241)),
    VL(241, 242, st={241: "serif", 242: "serif"}, y=870, mode="tight", end=cut(243)),
    VL(243, 248, y=880, end=cut(249)),
    # P
    VL(249, 253, end=cut(254)),
    VL(254, 258, st={255: "serifi", 256: "serifi"}, end=cut(259)),
    VL(259, 260, end=cut(261)),
    VL(261, 265, end=cut(266)),
    VL(266, 267, st={267: "serifi"}, end=cut(268)),
    # Q
    VL(268, 270, end=cut(271)),
    VL(271, 274, st={273: "serif", 274: "serif"}, y=985, end=cut(275)),
    VL(275, 277, end=cut(278)),
    VL(278, 281, end=cut(282)),
    VL(282, 283, st={282: "bold", 283: "serifi"}, mode="tight", end=cut(284)),
    VL(284, 288, st={287: "serifi"}, end=103.80),
]


def build_captions():
    body, js = [], []
    for li, L in enumerate(LINES):
        lid = f"cap{li:02d}"
        t0 = r3(L.start if L.start is not None else L.words[0][1] - 0.04)
        t1 = r3(L.end if L.end is not None else L.words[-1][1] + 0.6)
        dur = r3(max(0.2, t1 - t0))
        spans = []
        for wi, (txt, t, cls, e) in enumerate(L.words):
            wid = f"{lid}w{wi}"
            c = cls.replace("sel", "").strip()
            spans.append(f'<span class="w {c}"><span class="gh">{txt}</span><span class="ik"><span class="tx" id="{wid}">{txt}</span></span>'
                         + (f'<span class="selbox" id="{wid}b"></span>' if "sel" in cls else "") + '</span>')
            if e == "sel":   # Tesla's SpaceX: a blue text-selection box typing the word in, letter by letter
                n = max(3, len(txt.replace("&nbsp;", " ")))
                js.append(f'  tl.set("#{wid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{r3(t)});\n'
                          f'  tl.to("#{wid}",{{clipPath:"inset(0% 0% 0% 0%)",duration:{r3(n * 0.055)},ease:"steps({n})"}},{r3(t)});\n'
                          f'  tl.fromTo("#{wid}b",{{scaleX:0}},{{scaleX:1,duration:{r3(n * 0.055)},ease:"steps({n})"}},{r3(t)});\n')
            else:
                js.append(ent_js("#" + wid, e, t, L.ink))
        mode = L.mode + (" ink" if L.ink else "")
        body.append(f'<div id="{lid}" class="clip cl" data-start="{t0}" data-duration="{dur}" data-track-index="0" style="top:{L.y}px">'
                    f'<div class="row {mode}" id="{lid}r">{"".join(spans)}</div></div>')
        js.append(f'  tl.fromTo("#{lid}r",{{x:24}},{{x:-16,duration:{dur},ease:"power2.out"}},{t0});\n')
        if L.exit == "blur" and dur > 0.5:
            js.append(f'  tl.to("#{lid}r",{{opacity:0,filter:"blur(8px)",duration:0.13,ease:"power2.in"}},{r3(t1 - 0.13)});\n')
    extra = """
#cap{position:absolute;inset:0;}
.selbox{position:absolute;left:-0.08em;right:-0.08em;top:0.12em;bottom:0.02em;background:rgba(48,96,255,0.88);z-index:0;transform-origin:0 50%;}
.w .ik{z-index:1;}
"""
    html = comp("captions", TOTAL, '<div id="cap">\n' + "\n".join(body) + "\n</div>", "".join(js), extra)
    open(os.path.join(P, "compositions", "captions.html"), "w", encoding="utf-8").write(html)
    return len(LINES)


# ------------------------------------------------------------------ scenes
def vid(s, t0, z, wrap_css="", card=None):
    """A shot as an untimed wrapper (moves) around its timed <video>; times local to the scene."""
    st, du = r3(s["start"] - t0), r3(s["end"] - s["start"])
    if card:
        x, y, w, h = card
        return (f'<div class="card" id="{s["id"]}-w" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{wrap_css}">'
                f'<video id="v-{s["id"]}" class="clip" src="assets/clips/{s["id"]}.mp4" data-start="{st}" data-duration="{du}" muted playsinline></video></div>')
    return (f'<div class="shot" id="{s["id"]}-w" style="z-index:{z};{wrap_css}">'
            f'<video id="v-{s["id"]}" class="clip" src="assets/clips/{s["id"]}.mp4" data-start="{st}" data-duration="{du}" muted playsinline></video></div>')


def push_js(s, t0):
    if not s.get("push"):
        return ""
    a, b = s["push"]
    return f'  tl.fromTo("#{s["id"]}-w",{{scale:{a}}},{{scale:{b},duration:{r3(s["end"] - s["start"])},ease:"none"}},{r3(s["start"] - t0)});\n'


def pop_js(sel, boxsel, t, sc=1.04):
    """A card after a white box (the user's 'kpop'): two frames of white, then the card settles."""
    t = r3(t)
    return (f'  tl.set("{boxsel}",{{opacity:1}},{t});\n'
            f'  tl.set("{boxsel}",{{opacity:0}},{r3(t + 0.067)});\n'
            f'  tl.set("{sel}",{{opacity:1}},{r3(t + 0.067)});\n'
            f'  tl.fromTo("{sel}",{{scale:{sc}}},{{scale:1,duration:0.35,ease:"expo.out"}},{r3(t + 0.067)});\n')


def year_flicker_js(boxsel, t):
    """1998-style: after the year has landed, its first two digits go black in a white box: on, off, on, off."""
    out = ""
    for k, f in enumerate((6, 8, 10, 11)):
        out += f'  tl.set("{boxsel}",{{opacity:{1 if k % 2 == 0 else 0}}},{r3(t + f / 60)});\n'
    return out


SCENES = []   # (cid, start, end, body_html, js, css)


def scene(cid, t0, t1, ids, extra_body="", extra_js="", css="", cards=None, wraps=None):
    cards, wraps = cards or {}, wraps or {}
    body, js = [], []
    for z, i in enumerate(ids, start=1):
        s = SH[i]
        body.append(vid(s, t0, z, wraps.get(i, ""), cards.get(i)))
        js.append(push_js(s, t0))
    SCENES.append((cid, t0, t1, "\n".join(body) + "\n" + extra_body, "".join(js) + extra_js, css))


def L(t, t0): return r3(t - t0)


# ---- s00 news ----------------------------------------------------------------------------------------
def s_news():
    t0, t1 = 0.0, NEWS_DUR
    # $1 BILLION in the FOX 2 banner sits at (1206, 980) in the frame: bring it to (960, 700) at 2.3x
    zx, zy, k = 1206, 980, 2.3
    body = f"""
<div class="hb" id="nw-count" style="left:0;right:0;top:290px;text-align:center;font-size:150px;opacity:0;z-index:30;font-variant-numeric:tabular-nums;">$0</div>
<div class="box" id="nw-hl" style="left:604px;top:652px;width:652px;height:100px;mix-blend-mode:difference;transform-origin:0 50%;opacity:0;z-index:30"></div>
"""
    tz = N(11) - 0.17          # just before "a billion"
    js = f"""  tl.fromTo("#news-w",{{x:0,y:0,scale:1,transformOrigin:"0 0"}},{{x:{r3(960 - k * zx)},y:{r3(700 - k * zy)},scale:{k},duration:0.42,ease:"power3.inOut"}},{r3(tz)});
  tl.set("#nw-hl",{{opacity:1,scaleX:0}},{r3(N(12) + 0.02)});
  tl.to("#nw-hl",{{scaleX:1,duration:0.3,ease:"power2.out"}},{r3(N(12) + 0.02)});
  const cnt = {{v:0}};
  tl.set("#nw-count",{{opacity:1,filter:"blur(2px) brightness(2.2)",textShadow:"{FLASH}"}},{r3(N(12))});
  tl.to("#nw-count",{{filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.25,ease:"power3.out"}},{r3(N(12) + 0.05)});
  tl.to(cnt,{{v:1000000000,duration:{r3(N(13) - N(12))},ease:"expo.out",onUpdate:()=>{{document.getElementById("nw-count").textContent="$"+Math.round(cnt.v).toLocaleString("en-US");}}}},{r3(N(12))});
  tl.set("#nw-count",{{scale:1.14,filter:"blur(2px) brightness(2.6)",textShadow:"{FLASH}"}},{r3(N(13))});
  tl.to("#nw-count",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.22,ease:"power3.out"}},{r3(N(13) + 0.05)});
  tl.fromTo("#news-w",{{rotation:0}},{{rotation:0.6,duration:0.05,yoyo:true,repeat:3,ease:"none"}},{r3(N(13))});
  tl.to("#news-w",{{filter:"brightness(1.8)",duration:0.12,ease:"power2.in"}},{r3(t1 - 0.12)});
"""
    scene("news", t0, t1, ["news"], body, js)


def s_cj():
    t0, t1 = NEWS_DUR, VO_OFFSET
    scene("cj", t0, t1, ["cj"], "", f'  tl.fromTo("#cj-w",{{scale:1.08}},{{scale:1.0,duration:{r3(t1 - t0)},ease:"power2.out"}},0);\n')


# ---- A ------------------------------------------------------------------------------------------------
def s_a():
    t0, t1 = VO_OFFSET, cut(22)
    xs = [84, 680, 1276]
    cards = {i: (x, 42, 560, 996) for i, x in zip(("a1a", "a1b", "a1c"), xs)}
    body = '<div class="grunge" style="z-index:0;filter:brightness(0.35)"></div>\n'
    body += "".join(f'<div class="box" id="a-pb{k}" style="left:{x}px;top:42px;width:560px;height:996px;z-index:20;opacity:0"></div>\n' for k, x in enumerate(xs))
    js = "".join(pop_js(f"#{i}-w", f"#a-pb{k}", L(SH[i]["start"], t0)) for k, i in enumerate(("a1a", "a1b", "a1c")))
    # the date: a small 2026 over November 19th
    body += '<div class="kick" id="a-kick" style="top:392px;z-index:25">2026</div>\n'
    js += f'  tl.fromTo("#a-kick",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.25,ease:"power2.out"}},{L(W(11) + 0.2, t0)});\n'
    js += f'  tl.to("#a-kick",{{opacity:0,duration:0.1}},{L(cut(13) - 0.1, t0)});\n'
    scene("sa", t0, t1, ["a1a", "a1b", "a1c", "a2", "a3", "a4", "a5", "a6"], body, js, cards=cards)


def s_b():
    t0, t1 = cut(22), cut(33)
    body = (f'<div class="hb" id="b-count" style="left:0;right:0;top:420px;text-align:center;font-size:132px;opacity:0;z-index:30;font-variant-numeric:tabular-nums;">$0</div>\n'
            f'<div class="box" id="b-yb" style="left:0;top:0;width:10px;height:10px;opacity:0;z-index:40"></div>\n')
    a, b = W(28), W(30)
    js = f"""  const c2 = {{v:0}};
  tl.set("#b-count",{{opacity:1,filter:"blur(2px) brightness(2.4)",textShadow:"{FLASH}"}},{L(a, t0)});
  tl.to("#b-count",{{filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.22,ease:"power3.out"}},{L(a + 0.05, t0)});
  tl.to(c2,{{v:2000000000,duration:{r3(b - a)},ease:"expo.out",onUpdate:()=>{{document.getElementById("b-count").textContent="$"+Math.round(c2.v).toLocaleString("en-US");}}}},{L(a, t0)});
  tl.set("#b-count",{{scale:1.12,filter:"blur(2px) brightness(2.6)",textShadow:"{FLASH}"}},{L(b, t0)});
  tl.to("#b-count",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.22,ease:"power3.out"}},{L(b + 0.05, t0)});
  tl.to("#b-count",{{opacity:0,filter:"blur(10px)",duration:0.14,ease:"power2.in"}},{L(cut(31) - 0.14, t0)});
"""
    scene("sb", t0, t1, ["b1", "b2", "b3", "b4", "b5"], body, js)


def s_c():
    """2025 struck out on Trailer 1's own end card, May 2026 struck on paper, then Rockstar's November card."""
    t0, t1 = cut(33), cut(47)
    k, fx, fy = 2.6, 964, 952          # COMING 2025 on the card, pulled to the centre
    p_on, p_off = L(cut(39), t0), L(cut(45), t0)
    body = f"""
<div class="strike" id="c-st1" style="left:1186px;top:553px;width:600px;z-index:30;opacity:0;transform:rotate(-3deg)"></div>
<div class="paper clip" id="c-paper" data-start="{p_on}" data-duration="{r3(p_off - p_on)}" style="z-index:20"></div>
<div class="clip" id="c-may" data-start="{p_on}" data-duration="{r3(p_off - p_on)}" style="position:absolute;inset:0;z-index:21">
  <div id="c-mayrow" style="position:absolute;left:0;right:0;top:400px;display:flex;justify-content:center;align-items:baseline;column-gap:56px;color:#141414;">
    <span id="c-may1" style="font-family:'Instrument Serif',serif;font-style:italic;font-size:210px;line-height:1;opacity:0;">May</span>
    <span id="c-may2" style="position:relative;font-family:'Heros',sans-serif;font-weight:700;font-size:190px;letter-spacing:-0.04em;line-height:1;opacity:0;">2026<span id="c-yb" style="position:absolute;left:-6px;top:4px;width:0.55em;height:0.9em;background:#141414;mix-blend-mode:difference;opacity:0"></span></span>
  </div>
  <div class="strike" id="c-st2" style="left:430px;top:500px;width:1060px;opacity:0;transform:rotate(2deg)"></div>
</div>
"""
    js = f"""  tl.fromTo("#c1-w",{{x:0,y:0,scale:1,transformOrigin:"0 0"}},{{x:{r3(960 - k * fx)},y:{r3(560 - k * fy)},scale:{k},duration:0.38,ease:"power3.inOut"}},{L(cut(38) - 0.12, t0)});
  tl.set("#c-st1",{{opacity:0.95,scaleX:0}},{L(W(38) + 0.42, t0)});
  tl.to("#c-st1",{{scaleX:1,duration:0.22,ease:"power2.out"}},{L(W(38) + 0.42, t0)});
  tl.set("#c-st1",{{opacity:0}},{p_on});
{ent_js('#c-may1', 'flash', L(W(40), t0), ink=True)}{ent_js('#c-may2', 'flash', L(W(41), t0), ink=True)}{year_flicker_js('#c-yb', L(W(41), t0))}  tl.set("#c-st2",{{opacity:0.95,scaleX:0}},{L(W(43), t0)});
  tl.to("#c-st2",{{scaleX:1,duration:0.26,ease:"power2.out"}},{L(W(43), t0)});
  tl.fromTo("#c3-w",{{scale:1.0}},{{scale:1.12,duration:0.5,ease:"expo.out"}},{L(cut(46), t0)});
"""
    scene("sc", t0, t1, ["c1", "c3"], body, js)


def s_simple(cid, t0, t1, ids, extra_body="", extra_js="", **kw):
    scene(cid, t0, t1, ids, extra_body, extra_js, **kw)


def s_f():
    t0, t1 = cut(57), cut(73)
    cards = {"f1": (380, 42, 560, 996), "f2": (980, 42, 560, 996)}
    body = ('<div class="grunge" style="z-index:0;filter:brightness(0.3)"></div>\n'
            '<div class="box" id="f-pb0" style="left:380px;top:42px;width:560px;height:996px;z-index:20;opacity:0"></div>\n'
            '<div class="box" id="f-pb1" style="left:980px;top:42px;width:560px;height:996px;z-index:20;opacity:0"></div>\n')
    js = pop_js("#f1-w", "#f-pb0", 0.0) + pop_js("#f2-w", "#f-pb1", L(SH["f2"]["start"], t0))
    scene("sf", t0, t1, ["f1", "f2", "f3", "f3b", "f4", "f4b"], body, js, cards=cards)


# ---- I: rewind to 2002, the family computer --------------------------------------------------------
CRT_CSS = """
.crt-room{position:absolute;inset:0;background:radial-gradient(ellipse 60% 55% at 50% 48%, #1d2440 0%, #0a0b10 55%, #050506 100%);}
.crt{position:absolute;left:300px;top:60px;width:1320px;height:1000px;border-radius:46px;
  background:linear-gradient(160deg,#e3dac4 0%,#cfc5ab 45%,#b3a98f 100%);
  box-shadow:inset 0 3px 0 rgba(255,255,255,0.6), inset 0 -10px 24px rgba(0,0,0,0.25), 0 40px 90px rgba(0,0,0,0.7);}
.crt-in{position:absolute;left:96px;top:70px;width:1128px;height:846px;border-radius:30px;background:#111;
  box-shadow:inset 0 0 0 10px #8f8770, inset 0 0 0 14px #2a2823;}
.crt-scr{position:absolute;left:24px;top:22px;width:1080px;height:802px;border-radius:44px / 36px;overflow:hidden;background:#000;}
.crt-scr video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.crt-lines{position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0px, rgba(0,0,0,0.22) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 4px);mix-blend-mode:multiply;}
.crt-glass{position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 40% 30%, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0) 60%), radial-gradient(ellipse 100% 100% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%);}
.crt-led{position:absolute;right:120px;bottom:30px;width:16px;height:16px;border-radius:50%;background:#7dff6a;box-shadow:0 0 12px #7dff6a;}
.crt-badge{position:absolute;left:96px;bottom:24px;font-family:"InterV",sans-serif;font-weight:700;font-size:22px;letter-spacing:0.3em;color:#8a826c;}
.xp{position:absolute;right:56px;bottom:40px;width:390px;height:560px;background:#ece9d8;border:2px solid #0831d9;border-radius:8px 8px 3px 3px;box-shadow:4px 6px 16px rgba(0,0,0,0.5);font-family:Tahoma,"InterV",sans-serif;font-size:20px;color:#000;opacity:0;}
.xp-bar{height:40px;background:linear-gradient(180deg,#0a5ce8 0%,#3c8bf7 18%,#0548d6 60%,#0a46c9 100%);border-radius:6px 6px 0 0;color:#fff;font-weight:700;font-size:20px;line-height:40px;padding-left:12px;text-shadow:1px 1px 0 #00125c;}
.xp-x{position:absolute;right:6px;top:6px;width:28px;height:28px;border-radius:3px;background:linear-gradient(180deg,#e9805f,#c0391b);border:1px solid #fff;}
.xp-lab{position:absolute;left:0;right:0;top:58px;text-align:center;font-weight:700;}
.xp-track{position:absolute;left:186px;top:118px;width:10px;height:310px;background:#fff;border:1px solid #888;border-radius:2px;box-shadow:inset 1px 1px 0 #999;}
.xp-ticks{position:absolute;left:220px;top:118px;width:18px;height:310px;background:repeating-linear-gradient(180deg,#666 0,#666 2px,transparent 2px,transparent 31px);}
.xp-thumb{position:absolute;left:164px;top:110px;width:54px;height:26px;background:linear-gradient(180deg,#fff,#d6d3c4);border:1px solid #6b6b6b;border-radius:3px;box-shadow:0 1px 0 #999;}
.xp-mute{position:absolute;left:120px;top:466px;display:flex;align-items:center;gap:8px;}
.xp-box{width:22px;height:22px;background:#fff;border:1px solid #1c5180;position:relative;}
.xp-tick{position:absolute;left:2px;top:-6px;font-size:24px;font-weight:700;color:#21a121;opacity:0;}
.vhs{position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 1px, rgba(0,0,0,0.0) 1px, rgba(0,0,0,0.0) 3px);}
.vhs-band{position:absolute;left:0;right:0;height:120px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,0.35),rgba(255,255,255,0));mix-blend-mode:screen;}
.osd{position:absolute;left:120px;top:96px;font-family:"InterV",sans-serif;font-weight:700;font-size:54px;color:#fff;letter-spacing:0.06em;text-shadow:3px 3px 0 #000;}
"""


def crt(prefix, vids_html, with_xp=False):
    xp = ""
    if with_xp:
        xp = f"""<div class="xp" id="{prefix}-xp"><div class="xp-bar">Volume Control<span class="xp-x"></span></div>
<div class="xp-lab">Volume Control</div><div class="xp-track"></div><div class="xp-ticks"></div>
<div class="xp-thumb" id="{prefix}-thumb"></div>
<div class="xp-mute"><span class="xp-box"><span class="xp-tick" id="{prefix}-tick">&#10004;</span></span><span>Mute all</span></div></div>"""
    return f"""<div class="crt-room"></div>
<div class="crt" id="{prefix}-crt"><div class="crt-in"><div class="crt-scr">{vids_html}<div class="crt-lines"></div>{xp}<div class="crt-glass"></div></div></div>
<div class="crt-badge">PENTIUM 4</div><div class="crt-led"></div></div>"""


def scr_vid(i, t0):
    s = SH[i]
    return f'<video id="v-{i}" class="clip" src="assets/clips/{i}.mp4" data-start="{L(s["start"], t0)}" data-duration="{r3(s["end"] - s["start"])}" muted playsinline></video>'


def s_i():
    t0, t1 = cut(91) + 0.12, cut(121)
    c_on, c_off = L(cut(97), t0), L(cut(115), t0)
    body = (vid(SH["i0"], t0, 1) + "\n" +
            f'<div class="clip full" id="i-vhs" data-start="0" data-duration="{L(cut(94), t0)}" style="z-index:5"><div class="vhs"></div>'
            f'<div class="vhs-band" id="i-band" style="top:-140px"></div><div class="osd">&#9664;&#9664; REW</div></div>\n'
            f'<div class="clip full" id="i-yr" data-start="0" data-duration="{L(cut(94), t0)}" style="z-index:6">'
            f'<div class="hb" id="i-year" style="left:0;right:0;top:420px;text-align:center;font-size:230px;opacity:0;">'
            f'<span style="position:relative">2002<span id="i-yb" style="position:absolute;left:-0.04em;top:0.02em;width:1.14em;height:0.96em;background:#fff;mix-blend-mode:difference;opacity:0"></span></span></div></div>\n'
            + vid(SH["i1"], t0, 2) + "\n" +
            f'<div class="full" id="i-crtw" style="z-index:4;opacity:0">'
            + crt("i", scr_vid("i3", t0) + scr_vid("i3b", t0) + scr_vid("i4", t0), with_xp=True) + "</div>\n" + vid(SH["i5"], t0, 5) + "\n" + vid(SH["i5b"], t0, 6))
    yt = 0.20
    js = f"""  tl.fromTo("#i-band",{{y:0}},{{y:1300,duration:{L(cut(94), t0)},ease:"none"}},0);
  tl.set("#i-year",{{opacity:1,scale:1.1,filter:"blur(3px) brightness(2.6)",textShadow:"{FLASH}"}},{yt});
  tl.to("#i-year",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.2,ease:"power3.out"}},{r3(yt + 0.05)});
{year_flicker_js('#i-yb', yt)}  tl.set("#i-crtw",{{opacity:1}},{c_on});
  tl.set("#i-crtw",{{opacity:0}},{c_off});
  tl.fromTo("#i-crt",{{scale:1.0}},{{scale:1.045,duration:{r3(c_off - c_on)},ease:"none"}},{c_on});
  tl.fromTo("#i-xp",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.22,ease:"expo.out"}},{L(W(109) - 0.05, t0)});
  tl.fromTo("#i-thumb",{{y:0}},{{y:300,duration:{r3(W(114) - W(110))},ease:"power2.inOut"}},{L(W(110), t0)});
  tl.set("#i-tick",{{opacity:1}},{L(W(114) + 0.05, t0)});
"""
    SCENES.append(("si", t0, t1, body, js, CRT_CSS))


# ---- J: the notebook ------------------------------------------------------------------------------------
NB_CSS = """
.nb{position:absolute;left:-60px;top:-60px;width:2040px;height:1200px;background:#f6f3ea;}
.nb-tex{position:absolute;inset:0;background:url("assets/tex/ht_paper.jpg") center/cover;mix-blend-mode:multiply;opacity:0.55;}
.nb-lines{position:absolute;inset:0;background:repeating-linear-gradient(180deg, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 61px, rgba(70,120,190,0.55) 61px, rgba(70,120,190,0.55) 63px);}
.nb-margin{position:absolute;top:0;bottom:0;left:330px;width:3px;background:rgba(220,60,70,0.75);}
.nb-hole{position:absolute;left:120px;width:44px;height:44px;border-radius:50%;background:#0b0b0b;box-shadow:inset 0 3px 6px rgba(0,0,0,0.6);}
.hand{position:absolute;font-family:"Gochi Hand",cursive;color:#1f2f7a;white-space:nowrap;line-height:1;}
"""


def s_j():
    t0, t1 = cut(121), cut(135)
    holes = "".join(f'<div class="nb-hole" style="top:{y}px"></div>' for y in (220, 520, 820))
    page = f'<div class="nb" id="j-nb"><div class="nb-tex"></div><div class="nb-lines"></div><div class="nb-margin"></div>{holes}</div>'
    tw1, tw2 = W(125), W(127)
    body = f"""<div class="full" id="j-page" style="z-index:1">{page}
<div class="hand" id="j-h1" style="left:520px;top:420px;font-size:150px;transform:rotate(-4deg);clip-path:inset(0% 100% 0% 0%)">ASPIRINE</div>
<div class="hand" id="j-h2" style="left:610px;top:640px;font-size:150px;transform:rotate(-2deg);clip-path:inset(0% 100% 0% 0%)">PANZER</div>
<svg id="j-ul" style="position:absolute;left:600px;top:800px;width:640px;height:60px;overflow:visible" viewBox="0 0 640 60"><path id="j-ulp" d="M8 30 C 160 52, 380 8, 630 34" stroke="#1f2f7a" stroke-width="9" fill="none" stroke-linecap="round" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"/></svg>
<svg id="j-star" style="position:absolute;left:1360px;top:380px;width:150px;height:150px;overflow:visible" viewBox="0 0 100 100"><path id="j-starp" d="M50 6 L61 38 L95 38 L67 58 L78 92 L50 71 L22 92 L33 58 L5 38 L39 38 Z" stroke="#1f2f7a" stroke-width="5" fill="none" stroke-linejoin="round" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"/></svg>
</div>
{vid(SH['j2'], t0, 5)}
<div class="clip full" id="j-tank" data-start="{L(SH['j2']['start'], t0)}" data-duration="{r3(SH['j2']['end'] - SH['j2']['start'])}" style="z-index:6">
<div class="hand" id="j-tk" style="left:0;right:0;top:330px;text-align:center;font-size:260px;color:#fff;opacity:0">PANZER</div></div>
"""
    js = f"""  tl.fromTo("#j-nb",{{scale:1.0,rotation:-1.2}},{{scale:1.06,rotation:-0.4,duration:{r3(t1 - t0)},ease:"none"}},0);
  tl.to("#j-h1",{{clipPath:"inset(0% 0% 0% 0%)",duration:0.5,ease:"steps(8)"}},{L(tw1, t0)});
  tl.set("#j-h2",{{clipPath:"inset(0% 0% 0% 0%)"}},{L(SH['j2']['end'], t0)});
  tl.set("#j-tk",{{opacity:1,scale:1.12,filter:"blur(3px) brightness(2.4)",textShadow:"{FLASH}"}},{L(tw2, t0)});
  tl.to("#j-tk",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.2,ease:"power3.out"}},{L(tw2 + 0.05, t0)});
  tl.to("#j-ulp",{{strokeDashoffset:0,duration:0.35,ease:"power2.inOut"}},{L(SH['j2']['end'] + 0.25, t0)});
  tl.to("#j-starp",{{strokeDashoffset:0,duration:0.45,ease:"power1.inOut"}},{L(SH['j2']['end'] + 0.75, t0)});
"""
    SCENES.append(("sj", t0, t1, body, js, NB_CSS))


# ---- M: every other game asks you to be the hero (paper card that squeezes to a band) -----------------
def s_m():
    t0, t1 = cut(170), cut(203)
    sq = L(cut(181) - 0.20, t0)
    body = f'<div class="paper" id="m-paper" style="z-index:30"></div>\n'
    js = f"""  tl.fromTo("#m-paper",{{scale:1.0}},{{scale:1.035,duration:{sq},ease:"none"}},0);
  tl.to("#m-paper",{{clipPath:"inset(46% 0% 46% 0%)",duration:0.18,ease:"power3.in"}},{sq});
  tl.set("#m-paper",{{opacity:0}},{L(cut(181), t0)});
"""
    scene("sm", t0, t1, ["m2", "m2b", "m3", "m4", "m5", "m5b", "m5c"], body, js)


def build_scenes():
    s_news(); s_cj(); s_a(); s_b(); s_c()
    s_simple("sd", cut(47), cut(55), ["d1", "d2"])
    s_simple("se", cut(55), cut(57), ["e1", "e2"])
    s_f()
    s_simple("sg", cut(73), cut(82), ["g1", "g1b", "g2", "g3"])
    s_simple("sh", cut(82), cut(91) + 0.12, ["h1", "h1b", "h2"])
    s_i(); s_j()
    s_simple("sk", cut(135), cut(151), ["k1", "k1b", "k2", "k2b", "k3a", "k3b"])
    s_simple("sl", cut(151), cut(170), ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "l7b"])
    s_m()
    s_simple("sn", cut(203), cut(232), ["n1", "n2", "n3", "n4", "n4b", "n5", "n5b"])
    s_simple("so", cut(232), cut(249), ["o1", "o2", "o3", "o4", "o4b"])
    s_simple("sp", cut(249), cut(268), ["p1", "p1b", "p2", "p3", "p4"])
    q_body = ""
    t0q = cut(268)
    q_crt = f'<div class="full" id="q-crtw" style="z-index:2;opacity:0">' + crt("q", scr_vid("q2", t0q)) + "</div>"
    ids = ["q1", "q3", "q4", "q4b", "q5", "q6", "q7"]
    body, js = [], []
    for z, i in enumerate(ids, start=3):
        body.append(vid(SH[i], t0q, z)); js.append(push_js(SH[i], t0q))
    js.append(f'  tl.to("#q7-w",{{opacity:0,duration:0.45,ease:"power1.in"}},{L(TOTAL - 0.45, t0q)});\n')
    SCENES.append(("sq", t0q, TOTAL, vid(SH["q1"], t0q, 1) + "\n" + q_crt + "\n" + "\n".join(body[1:]), "".join(js), CRT_CSS))

    for cid, t0, t1, body, js, css in SCENES:
        html = comp(cid, t1 - t0, body, js, css)
        open(os.path.join(P, "compositions", cid + ".html"), "w", encoding="utf-8").write(html)
    return SCENES


# ------------------------------------------------------------------ global fx: flashes, glitch blocks, grain
FLASHES = [NEWS_DUR, cut(90), cut(212) + 0.0, cut(222), cut(91) + 0.12]   # white bloom cuts
GLITCH = [cut(38) - 0.12, cut(46), cut(55), cut(186) + 0.11, cut(232), cut(268)]


def build_fx():
    body, js = [], []
    for k, t in enumerate(FLASHES):
        fid = f"fl{k}"
        body.append(f'<div class="clip" id="{fid}" data-start="{r3(t - 0.12)}" data-duration="0.5" style="position:absolute;inset:0;z-index:50"><div class="fl" id="{fid}i"></div></div>')
        js.append(f'  tl.fromTo("#{fid}i",{{opacity:0}},{{opacity:0.9,duration:0.12,ease:"power2.in"}},{r3(t - 0.12)});\n'
                  f'  tl.set("#{fid}i",{{opacity:1}},{r3(t)});\n'
                  f'  tl.to("#{fid}i",{{opacity:0,duration:0.32,ease:"power2.out"}},{r3(t + 0.04)});\n')
    rects = [(120, 160, 760, 300), (980, 520, 640, 220), (300, 700, 1100, 140), (1300, 120, 420, 520)]
    for k, t in enumerate(GLITCH):
        gid = f"gl{k}"
        boxes = "".join(f'<div class="gb" id="{gid}b{j}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'
                        for j, (x, y, w, h) in enumerate(rects[k % 2::2] if k % 3 else rects[:3]))
        body.append(f'<div class="clip" id="{gid}" data-start="{r3(t - 0.034)}" data-duration="0.12" style="position:absolute;inset:0;z-index:49">{boxes}</div>')
    css = """
.fl{position:absolute;inset:0;background:#fff;opacity:0;}
.gb{position:absolute;background:#fff;mix-blend-mode:difference;}
.grain{position:absolute;left:-200px;top:-200px;width:2320px;height:1480px;background:url("assets/tex/grain.png");opacity:0.07;mix-blend-mode:overlay;}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.38) 100%);}
"""
    body.append('<div class="vig" id="fx-vig"></div><div class="grain" id="fx-grain"></div>')
    js.append(f'  tl.fromTo("#fx-grain",{{x:0,y:0}},{{x:-180,y:-140,duration:{TOTAL},ease:"steps({int(TOTAL * 15)})"}},0);\n')
    open(os.path.join(P, "compositions", "fx.html"), "w", encoding="utf-8").write(comp("fx", TOTAL, "\n".join(body), "".join(js), css))


# ------------------------------------------------------------------ audio + root
SFX = [  # (file, t, volume)
    ("impact-bass-1.mp3", NEWS_DUR - 0.02, 0.9), ("riser.mp3", N(12) - 0.9, 0.35),
    ("pop.mp3", VO_OFFSET + 0.06, 0.5), ("pop.mp3", VO_OFFSET + 0.36, 0.5), ("pop.mp3", VO_OFFSET + 0.69, 0.5),
    ("glitch-1.mp3", cut(38) - 0.15, 0.55), ("glitch-2.mp3", cut(46) - 0.04, 0.5), ("glitch-3.mp3", cut(55) - 0.04, 0.5),
    ("impact-bass-2.mp3", W(30) - 0.02, 0.7), ("whoosh-cinematic.mp3", cut(90) - 0.35, 0.6),
    ("whoosh-short.mp3", cut(91) + 0.1, 0.6), ("click-soft.mp3", W(110) - 0.02, 0.6), ("click-soft.mp3", W(114) + 0.04, 0.6),
    ("key-press.mp3", W(125) + 0.05, 0.5), ("impact-bass-1.mp3", W(127) - 0.02, 0.6),
    ("glitch-1.mp3", cut(186) + 0.08, 0.5), ("impact-bass-2.mp3", W(187) - 0.02, 0.6),
    ("whoosh.mp3", cut(222) - 0.25, 0.5), ("glitch-2.mp3", cut(232) - 0.04, 0.45), ("riser.mp3", W(287) - 1.4, 0.3),
]


def build_root(scenes):
    hosts = []
    for k, (cid, t0, t1, *_r) in enumerate(scenes):
        hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{r3(t0)}" '
                     f'data-duration="{r3(t1 - t0)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:{k + 1}"></div>')
    hosts.append(f'      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:90;pointer-events:none"></div>')
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:80;pointer-events:none"></div>')
    aud = [f'      <audio id="a-news" src="assets/audio/news_line.wav" data-start="0" data-duration="{NEWS_DUR}" data-track-index="5" data-volume="1"></audio>',
           f'      <audio id="a-cj" src="assets/audio/cj_line.wav" data-start="{NEWS_DUR}" data-duration="{r3(VO_OFFSET - NEWS_DUR + 0.2)}" data-track-index="6" data-volume="1"></audio>',
           f'      <audio id="a-vo" src="assets/audio/vo.wav" data-start="{VO_OFFSET}" data-duration="96.44" data-track-index="7" data-volume="1"></audio>']
    for k, (f, t, v) in enumerate(SFX):
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


if __name__ == "__main__":
    n = build_captions()
    sc = build_scenes()
    build_fx()
    build_root(sc)
    print(f"captions: {n} lines; scenes: {len(sc)}; total {TOTAL}s")
    for cid, t0, t1, *_r in sc:
        print(f"  {cid:8s} {t0:7.2f} -> {t1:7.2f}")
