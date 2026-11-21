#!/usr/bin/env python3
"""Writes the HyperFrames project: index.html (scene hosts + the mix) and compositions/s_*.html.

Every time comes from tools/timing.py (60 fps grid). Scene times in the HTML are relative to the scene's start.
Run: python3 tools/build.py
"""
import html as _html
import json
import os

import timing as TM

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMP = f"{ROOT}/compositions"
T, B, F = TM.T, TM.B, TM.F
FR = 1 / 60

FONTS = """
@font-face{font-family:"ISerif";src:url("assets/fonts/InstrumentSerif-Regular.woff2") format("woff2");font-weight:400;font-style:normal;}
@font-face{font-family:"ISerif";src:url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2");font-weight:400;font-style:italic;}
@font-face{font-family:"InterD";src:url("assets/fonts/InterDisplay-Medium.otf") format("opentype");font-weight:500;font-style:normal;}
@font-face{font-family:"InterD";src:url("assets/fonts/InterDisplay-Bold.otf") format("opentype");font-weight:700;font-style:normal;}
@font-face{font-family:"InterD";src:url("assets/fonts/InterDisplay-ExtraBold.otf") format("opentype");font-weight:800;font-style:normal;}
@font-face{font-family:"LGothic";src:url("assets/fonts/LeagueGothic-latin.woff2") format("woff2");font-weight:400;font-style:normal;}
@font-face{font-family:"Heros";src:url("assets/fonts/TeXGyreHeros-Bold.otf") format("opentype");font-weight:700;font-style:normal;}
@font-face{font-family:"InterSB";src:url("assets/fonts/InterDisplay-SemiBold.otf") format("opentype");font-weight:600;font-style:normal;}
"""
# the Dario video's Instrument Serif glow (the user: "exactly like the Dario video ... with that white glow")
SERIF_REST = "0 0 14px rgba(255,255,255,0.62),0 0 42px rgba(255,255,255,0.30),0 0 90px rgba(255,255,255,0.12)"
SERIF_SOFT = "0 0 18px rgba(255,255,255,0.85),0 0 50px rgba(255,255,255,0.45),0 0 100px rgba(255,255,255,0.18)"
SERIF_BLOOM = "0 0 22px rgba(255,255,255,1),0 0 60px rgba(255,255,255,0.95),0 0 130px rgba(255,255,255,0.7)"
# the Porsche reel's small italic line: a tight halo and a wide faint one; a faint dark lift over bright pictures
POR_GLOW = "0 0 6px rgba(255,255,255,0.50),0 0 30px rgba(255,255,255,0.20),0 2px 16px rgba(0,0,0,0.42)"
# over white pictures (the user's ending video, the S&P logo wall): the same type with a dark halo
POR_HEAVY = "0 0 10px rgba(0,0,0,0.85),0 0 26px rgba(0,0,0,0.65),0 0 60px rgba(0,0,0,0.35),0 2px 6px rgba(0,0,0,0.7)"

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:#000;}
.full{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.layer{position:absolute;inset:0;}
.cap{position:absolute;left:0;right:0;display:flex;justify-content:center;align-items:center;white-space:nowrap;pointer-events:none;}
.nv{font-family:"InterD",sans-serif;font-weight:800;letter-spacing:-0.02em;color:#fff;text-transform:uppercase;}
.hv{font-family:"Heros",sans-serif;font-weight:700;letter-spacing:-0.012em;color:#EEF0F0;text-transform:uppercase;line-height:1;white-space:nowrap;}
.flash{position:absolute;inset:0;background:#fff;opacity:0;}
.jn{font-family:"InterSB",sans-serif;font-weight:600;font-size:62px;letter-spacing:-0.05em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 18px rgba(0,0,0,0.45),0 2px 6px rgba(0,0,0,0.35);}
.jn.ink{color:#141414;text-shadow:none;}
.ser{font-family:"ISerif",serif;font-weight:400;line-height:1;color:#FBF8EC;white-space:nowrap;letter-spacing:0.005em;}
.por{font-family:"ISerif",serif;font-style:italic;font-weight:400;line-height:1;color:#fff;white-space:nowrap;word-spacing:0.38em;}
.por span{display:inline-block;opacity:0;}
.pl{font-family:"Heros",sans-serif;font-weight:700;font-size:94px;line-height:1.02;letter-spacing:-0.015em;color:#EDEDEA;
 text-shadow:0 0 14px rgba(0,0,0,0.35);}
.pl span{display:inline-block;opacity:0;}
"""


def r4(x):
    return f"{x:.4f}"


class Scene:
    def __init__(self, sid, t0, t1, bg="#000", css=""):
        self.sid, self.t0, self.t1 = sid, F(t0), F(t1)
        self.bg, self.css = bg, css
        self.els, self.js, self.n = [], [], 0

    @property
    def dur(self):
        return round(self.t1 - self.t0, 4)

    def rel(self, t):
        return round(max(0.0, min(self.dur, F(t) - self.t0)), 4)

    def timed(self, a, b):
        a, b = self.rel(a), self.rel(b)
        return f'data-start="{r4(a)}" data-duration="{r4(max(FR, b - a))}"'

    def uid(self, p):
        self.n += 1
        return f"{self.sid}-{p}{self.n}"

    def add(self, html, js=()):
        self.els.append(html)
        self.js.extend(js)

    def at(self, t):
        return r4(self.rel(t))

    def video(self, src, a, b, media=0.0, z=1, style="", cls="full", vid=None):
        vid = vid or self.uid("v")
        self.add(f'<video id="{vid}" class="clip {cls}" src="assets/clips/{src}" {self.timed(a, b)} '
                 f'data-media-start="{r4(media)}" data-track-index="1" muted playsinline '
                 f'style="z-index:{z};{style}"></video>')
        return vid

    def img(self, src, a, b, z=1, style="", cls="full", iid=None):
        iid = iid or self.uid("i")
        self.add(f'<img id="{iid}" class="clip {cls}" src="assets/img/{src}" alt="" {self.timed(a, b)} '
                 f'data-track-index="2" style="z-index:{z};{style}" />')
        return iid

    def div(self, a, b, inner, z=5, style="", cls="layer", did=None):
        did = did or self.uid("d")
        self.add(f'<div id="{did}" class="clip {cls}" {self.timed(a, b)} data-track-index="3" '
                 f'style="z-index:{z};{style}">{inner}</div>')
        return did

    def flash(self, a, peak=1.0, up=0.0, down=0.15, z=90, color="#fff"):
        """A white flash peaking at a (ramping up for `up` seconds before it), fading over `down`."""
        fid = self.uid("fl")
        s, e = a - up, a + down
        self.add(f'<div id="{fid}" class="clip flash" {self.timed(s, e)} data-track-index="4" '
                 f'style="z-index:{z};background:{color}"></div>')
        if up > 0:
            self.js.append(f'tl.fromTo("#{fid}",{{opacity:0}},{{opacity:{peak},duration:{r4(up)},ease:"power2.in"}},{self.at(s)});')
        else:
            self.js.append(f'tl.set("#{fid}",{{opacity:{peak}}},{self.at(a)});')
        self.js.append(f'tl.to("#{fid}",{{opacity:0,duration:{r4(down)},ease:"power2.out"}},{self.at(a)});')
        return fid

    def html(self):
        js = "\n  ".join(self.js)
        return f"""<template>
<style>
{FONTS}
{BASE_CSS}
#root{{background:{self.bg};}}
{self.css}
</style>
<div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080" data-duration="{r4(self.dur)}">
{chr(10).join(self.els)}
</div>
<script>
(function(){{
  const tl = gsap.timeline({{ paused: true }});
  tl.set({{}}, {{}}, {r4(self.dur)});
  {js}
  window.__timelines["{self.sid}"] = tl;
}})();
</script>
</template>
"""

    def write(self):
        with open(f"{COMP}/{self.sid}.html", "w") as f:
            f.write(self.html())


# ------------------------------------------------------------------ shared devices
# ------------------------------------------------------------------ shared devices
def B_dur(a, b):
    return max(FR, F(b) - F(a))


CAP_Y, CAP_SIZE = 900, 64   # the Jensen Huang reel's caption: white bold Helvetica caps, ~83 % down, in at once


SHADOW = "text-shadow:0 0 18px rgba(0,0,0,0.45),0 2px 6px rgba(0,0,0,0.35);"
# over the ending video (it strobes pure white / black, then bright sand): the same white caption, a heavier halo
SHADOW_HEAVY = "text-shadow:0 0 30px rgba(0,0,0,0.8),0 0 12px rgba(0,0,0,0.72),0 2px 5px rgba(0,0,0,0.6);"


def caption(sc, text, a, b, y=CAP_Y, size=CAP_SIZE, blend="difference", z=40, shadow=False, color=None):
    """The captions that were small italic labels, now as the Nvidia reel's caption (the user: the Jensen video's
    caption font). Difference blend over the people, so they read on the dark suits and the white shirts alike.
    `color` only for the dark "ink" captions over Think School's light grey page (same font, size and place)."""
    st = f"top:{y}px;height:0;" + (f"mix-blend-mode:{blend};" if blend else "")
    sh = SHADOW_HEAVY if shadow == "heavy" else (SHADOW if shadow else "")
    col = f"color:{color};" if color else ""
    return sc.div(a, b, f'<div class="hv" style="font-size:{size}px;{sh}{col}">{text}</div>', z=z, cls="cap", style=st)


def chunks(sc, items, end, **kw):
    """[(text, t)]: each caption chunk shows from its time to the next one's (the last to `end`)."""
    for i, (text, t) in enumerate(items):
        b = items[i + 1][1] if i + 1 < len(items) else end
        caption(sc, text, t, b, **kw)


# ------------------------------------------------------------------ type devices
BIG_REST = "0 0 20px rgba(255,255,255,0.75),0 0 60px rgba(255,255,255,0.40),0 0 130px rgba(255,255,255,0.16)"


def dhero(sc, eid, a, rest=SERIF_REST):
    """The Dario entrance: in blurred and blooming at 1.04, sharp and at rest four frames later."""
    sc.js.append(f'tl.set("#{eid}",{{scale:1.04,filter:"blur(14px)",textShadow:"{SERIF_BLOOM}"}},{sc.at(a)});')
    sc.js.append(f'tl.set("#{eid}",{{scale:1.015,filter:"blur(5px)",textShadow:"{SERIF_SOFT}"}},{sc.at(a + FR)});')
    sc.js.append(f'tl.set("#{eid}",{{scale:1.005,filter:"blur(2.5px)"}},{sc.at(a + 3 * FR)});')
    sc.js.append(f'tl.set("#{eid}",{{scale:1,filter:"blur(0px)",textShadow:"{rest}"}},{sc.at(a + 4 * FR)});')


def serif(sc, text, a, b, size, y=540, z=60, italic=False, rest=SERIF_REST):
    eid = sc.uid("sr")
    st = "font-style:italic;" if italic else ""
    sc.div(a, b, f'<div id="{eid}" class="ser" style="font-size:{size}px;{st}text-shadow:{rest};transform-origin:50% 55%;">'
                 f'{text}</div>', z=z, cls="cap", style=f"top:{y}px;height:0;")
    dhero(sc, eid, a, rest)
    return eid


def por_phrase(sc, words, a, b, size=96, y=540, z=60, fade=0.28, blur=6, spacing=None, glow=None):
    """The Porsche reel's line: laid out whole and centred first, each word fading in from a soft blur in its place."""
    spans, ids = [], []
    for w, t in words:
        sid = sc.uid("pw")
        ids.append((sid, t))
        spans.append(f'<span id="{sid}">{_html.escape(w, quote=False)}</span>')
    ws = f"word-spacing:{spacing};" if spacing else ""
    sc.div(a, b, f'<div class="por" style="font-size:{size}px;{ws}text-shadow:{glow or POR_GLOW};">{" ".join(spans)}</div>',
           z=z, cls="cap", style=f"top:{y}px;height:0;")
    for sid, t in ids:
        sc.js.append(f'tl.fromTo("#{sid}",{{opacity:0,filter:"blur({blur}px)"}},{{opacity:1,filter:"blur(0px)",'
                     f'duration:{fade},ease:"power1.out"}},{sc.at(t)});')


def type_phrase(sc, words, a, b, size=150, y=540, z=60, step=0.07, glow=None):
    """The Porsche reel's "4,500 people": the letters come in left to right, each from a soft blur."""
    spans, sets = [], []
    for wi, (w, t) in enumerate(words):
        for ci, ch in enumerate(w):
            sid = sc.uid("ty")
            spans.append(f'<span id="{sid}">{_html.escape(ch, quote=False)}</span>')
            sets.append((sid, t + ci * step))
        if wi < len(words) - 1:
            spans.append(" ")
    sc.div(a, b, f'<div class="por" style="font-size:{size}px;word-spacing:0.12em;text-shadow:{glow or POR_GLOW};">{"".join(spans)}</div>',
           z=z, cls="cap", style=f"top:{y}px;height:0;")
    for sid, t in sets:
        sc.js.append(f'tl.fromTo("#{sid}",{{opacity:0,filter:"blur(4px)"}},{{opacity:1,filter:"blur(0px)",duration:0.16,'
                     f'ease:"power1.out"}},{sc.at(t)});')


def big_words(sc, text, a, b, z=30, y=545, size=330):
    """League Gothic, centred, in difference over the picture (WEAPONIZED's treatment, the user's CARTEL)."""
    sc.div(a, b, f'<div style="font-family:\'LGothic\',sans-serif;font-size:{size}px;line-height:0.9;color:#fff;'
                 f'letter-spacing:0.01em;text-align:center;">{text}</div>',
           z=z, cls="cap", style=f"top:{y}px;height:0;mix-blend-mode:difference;")


# ------------------------------------------------------------------ s_quote: the panel line
def s_quote():
    sc = Scene("s_quote", *B["quote"])
    L = TM.LINE
    cut1, cut2 = L[8][1], L[14][1]                     # "with", "financial"
    sc.video("p_wide.mp4", 0.0, cut1, z=1)             # no zooms (the user)
    sc.video("p_over.mp4", cut1, cut2, z=1)
    # from "financial talent": Fink, Schwarzman, then Jamie Dimon (3rd) and Ray Dalio (4th) -- the user, Nov 21
    cuts_ = [cut2, L[16][1], L[19][1], L[23][1], B["quote"][1]]
    for k, clip in enumerate(["v3_ob_fink", "v3_ob_schw", "v4_ob_dimon", "v4_ob_dalio"]):
        sc.video(f"{clip}.mp4", cuts_[k], cuts_[k + 1], z=1)
        sc.flash(cuts_[k], peak=1.0, up=2 * FR, down=0.16, z=30)
    sc.write()
    return sc


# ------------------------------------------------------------------ s_hook: from "These" to the puppet
def s_hook():
    sc = Scene("s_hook", B["tiles"][0], B["puppet"][1])
    t0 = B["tiles"][0]
    n = round((B["tiles"][1] - t0) * 60)
    sc.video("r_tiles3.mp4", *B["tiles"], z=1)
    for word, a, b in (("Powerful", T["powerful"], T["people"]), ("People", T["people"], t0 + (n - 5) * FR)):
        wid = sc.uid("pw")
        sc.div(a, b, f'<div id="{wid}" class="nv" style="font-size:118px;text-shadow:0 0 22px rgba(0,0,0,0.45);">{word}</div>', z=30, cls="cap",
               style="top:540px;height:0;")
        for fa, fb in ((n - 21, n - 18), (n - 8, n - 5)):   # black while the tiles go negative
            ta, tb = t0 + fa * FR, t0 + fb * FR
            if a <= ta < b:
                sc.js.append(f'tl.set("#{wid}",{{color:"#000"}},{sc.at(ta)});tl.set("#{wid}",{{color:"#fff"}},{sc.at(tb)});')
    # ON EARTH on the user's plain red
    sc.img("red_bg_user.jpg", *B["earth"], z=1)
    on, ea = sc.uid("on"), sc.uid("ea")
    inner = (f'<div style="display:flex;gap:0.2em;font-family:\'LGothic\',sans-serif;font-size:330px;color:#fff;'
             f'letter-spacing:0.01em;line-height:1;"><span id="{on}">ON</span><span id="{ea}" style="opacity:0">EARTH</span></div>')
    sc.div(*B["earth"], inner, z=30, cls="cap", style="top:545px;height:0;")
    sc.js.append(f'tl.set("#{ea}",{{opacity:1}},{sc.at(T["earth"])});')
    # "a $60 trillion dollar": the article flipbook (its "$60 trillion" is the text), as long as the line lets it run
    sc.video("r_articles.mp4", *B["money"], z=1)
    # "cartel": the user's cartel video -- its table flash, a split second later the faces; CARTEL at the centre in
    # difference, on its word (the user: "like WEAPONIZED is written")
    sc.video("r_cartel4.mp4", *B["cartel"], z=1)
    big_words(sc, "CARTEL", T["cartel"], B["cartel"][1] - FR)
    # "weaponized capital": nothing written at the cut; WEAPONIZED on its word, then CAPITAL under it, smaller,
    # centred, in difference, no bounce (the user)
    sc.video("r_weap.mp4", *B["weap"], z=1)
    wid, cid = sc.uid("wz"), sc.uid("cp")
    stack = (f'<div style="font-family:\'LGothic\',sans-serif;font-size:250px;line-height:0.88;color:#fff;letter-spacing:0.01em;'
             f'text-align:center;"><div id="{wid}" style="opacity:0">WEAPONIZED</div><div id="{cid}" style="opacity:0">CAPITAL</div></div>')
    sc.div(T["weapon"], B["weap"][1] - FR, stack, z=30, cls="cap", style="top:545px;height:0;mix-blend-mode:difference;")
    sc.js.append(f'tl.set("#{wid}",{{opacity:1}},{sc.at(T["weapon"])});tl.set("#{cid}",{{opacity:1}},{sc.at(T["capital"])});')
    sc.video("r_logos.mp4", *B["logos"], z=1)          # that owns a piece of
    sc.video("r_touch3.mp4", *B["touch"], z=1)         # everything you touch
    sc.video("v3_puppet.mp4", *B["puppet"], z=1)
    sc.write()
    return sc


# ------------------------------------------------------------------ plain cuts
def cuts(sc, shots, z=1):
    for src, a, b in shots:
        sc.video(src, a, b, z=z)


# ------------------------------------------------------------------ the intros
def s_dimon():
    sc = Scene("s_dimon", B["dimon"][0], B["jpm"][1])
    sc.video("v5_dimon.mp4", *B["dimon"], z=1)         # refff's band in the ON EARTH red, the name in the white glow
    sc.video("r_jpm.mp4", *B["jpm"], z=1)              # the reel's "the man behind OpenAI"
    sc.write()
    return sc


def s_solomon():
    sc = Scene("s_solomon", B["solomon"][0], B["ceo"][1])
    sc.video("v5_solomon.mp4", *B["solomon"], z=1)     # the same device; "a part-time DJ" is the captions' line
    a, b = B["dj"]
    m = F((a + b) / 2)
    sc.video("v4_dj_a.mp4", a, m, z=1)
    sc.video("v4_dj_b.mp4", m, b, z=1)
    sc.video("r_ceo4.mp4", *B["ceo"], z=1)             # exactly the JPMorgan device, no shot repeated
    sc.write()
    return sc


def s_search():
    """"Amongst them is this guy": the spotlight reel (DeJRKmqTPdg) -- the big glowing serif words over the group,
    then the face flash, the room going dark and the punch-in on Fink, the small italic words under his face."""
    sc = Scene("s_search", B["orbit"][0], B["thisguy"][1])
    sc.video("r_orbit4.mp4", *B["orbit"], z=1)
    sc.video("r_spot4.mp4", *B["thisguy"], z=1)
    serif(sc, "Amongst them", T["amongst"] - 0.03, B["orbit"][1], 150, y=540)
    por_phrase(sc, [("is", T["is"] - 0.03), ("this", T["this"] - 0.03), ("guy", T["guy2"] - 0.03)],
               T["is"] - 0.03, B["thisguy"][1], size=78, y=745, spacing="0.3em")
    sc.write()
    return sc


# ------------------------------------------------------------------ s_fink: the man who runs ... BlackRock.
def s_fink():
    sc = Scene("s_fink", B["walk"][0], B["brand"][1])
    # "the man who runs the most evil": reel DeHkRtts3bI's opening -- a Fink picture every 4 frames, out of
    # perspective, blurred on the cuts (the user's new photos first); no red box
    sc.video("r_finkflip.mp4", B["walk"][0], B["box"][1], z=1)
    c0, c1 = B["company"]
    k1, k2 = F(c0 + 0.45), F(c0 + 0.95)
    cuts(sc, [("v2_br_letters.mp4", c0, k1), ("v2_br_bldg.mp4", k1, k2), ("v2_br_doors.mp4", k2, c1),
              ("v2_br_sign.mp4", *B["brand"])])
    sc.write()
    return sc


# ------------------------------------------------------------------ rest1: "A company that manages ... ever did."
import shotlist as SL


def s_rest1():
    sc = Scene("s_rest1", *B["rest1"])
    a0, a1 = B["rest1"]
    starts = [a0 if k == "rest1" else TM.RTX(k) for k, *_ in SL.REST1]
    for (key, name, src, t0, extra, fc), a, b in zip(SL.REST1, starts, starts[1:] + [a1]):
        sc.video(f"v3_{name}.mp4", a, b, z=1)
    # "$15 trillion": the Dario serif glow over the user's montage (not League Gothic, the user)
    serif(sc, "$15 trillion", TM.RT("15") - 0.03, TM.RT("assets") - 0.03, 210, y=540)
    sc.write()
    return sc


# ------------------------------------------------------------------ Rogan: Elon's question, then Rogan's silent second
def s_rogan():
    a, b = B["rogan"][0], B["react"][1]
    sc = Scene("s_rogan", a, b)
    sc.video("v5_rogan.mp4", *B["rogan"], z=1)
    sc.video("v5_react.mp4", *B["react"], z=1)
    # the Palmer Luckey reel's captions: lowercase bold Helvetica stacked beside him, each word blurring in
    rows, sets = [], []
    for line in CAP.palmer_lines():
        spans = []
        for w, t in line:
            sid = sc.uid("pl")
            spans.append(f'<span id="{sid}">{w}</span>')
            sets.append((sid, t))
        rows.append('<div class="pl">' + " ".join(spans) + "</div>")
    stack = sc.uid("st")
    sc.div(a, B["react"][0] + 0.62, f'<div id="{stack}" style="position:absolute;left:118px;top:300px;text-align:left;">{"".join(rows)}</div>',
           z=40, cls="layer")
    for sid, t in sets:
        sc.js.append(f'tl.fromTo("#{sid}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",'
                     f'duration:0.22,ease:"power2.out"}},{sc.at(t)});')
    sc.js.append(f'tl.to("#{stack}",{{opacity:0,filter:"blur(10px)",duration:0.28,ease:"power1.in"}},{sc.at(B["react"][0] + 0.32)});')
    sc.write()
    return sc


# ------------------------------------------------------------------ rest2: "Back in the 1980s" to the end
def s_rest2():
    sc = Scene("s_rest2", *B["rest2"])
    sc.video("v5_rest2.mp4", *B["rest2"], z=1)         # prep_v5: 72 shots, cut on the words (shotlist.REST2_V5)
    for a, b, kind, words, text in CAP.porsche_phrases():
        if kind != "card":
            continue
        # "in 1988": exactly the ON EARTH card (the user) -- the user's red, IN, then 1988 on its word
        in_, yr = sc.uid("in"), sc.uid("yr")
        sc.img("red_bg_user.jpg", a, b, z=5)
        inner = (f'<div style="display:flex;gap:0.2em;font-family:\'LGothic\',sans-serif;font-size:330px;color:#fff;'
                 f'letter-spacing:0.01em;line-height:1;"><span id="{in_}">{words[0][0]}</span>'
                 f'<span id="{yr}" style="opacity:0">{words[1][0]}</span></div>')
        sc.div(a, b, inner, z=6, cls="cap", style="top:545px;height:0;")
        sc.js.append(f'tl.set("#{yr}",{{opacity:1}},{sc.at(words[1][1])});')
    sc.write()
    return sc


# ------------------------------------------------------------------ s_caps: every caption, on its word
import captions as CAP

SL_white = ("a2", "has")                    # rest-recording keys: the ending video's span


def s_caps():
    sc = Scene("s_caps", 0.0, TM.TOTAL, bg="transparent")
    # 1. the Jensen reel's line (and the serif key words) to "...ever did."
    for a, b, ws, kind in CAP.jensen_phrases():
        if kind == "emph":
            serif(sc, " ".join(w for w, _, _ in ws), a, b, 150, y=540)
            continue
        y, cls = (900, "jn ink") if kind == "ink" else (540, "jn")
        for k in range(len(ws)):                       # the phrase builds word by word, re-centring as it grows
            s0 = ws[k][1]
            s1 = ws[k + 1][1] if k + 1 < len(ws) else b
            if s1 - s0 < FR:
                continue
            text = " ".join(w for w, _, _ in ws[:k + 1])
            sc.div(s0, s1, f'<div class="{cls}">{text}</div>', z=60, cls="cap", style=f"top:{y}px;height:0;")
    # 3. the Porsche reel's type from "Back in the 1980s"
    white = [(TM.RTX(SL_white[0]), TM.RTX(SL_white[1]))]          # the ending video (white frames) to "has"
    for a, b, kind, words, text in CAP.porsche_phrases():
        glow = POR_HEAVY if any(w0 - 0.05 <= a < w1 for w0, w1 in white) else None
        if kind == "por":
            por_phrase(sc, words, a, b, glow=glow)
        elif kind == "word":
            por_phrase(sc, words, a, b, size=150, glow=glow)
        elif kind == "type":
            type_phrase(sc, words, a, b, glow=POR_HEAVY)
        elif kind == "big":
            size = {"2008": 470, "3x": 560}.get(text, 200)
            serif(sc, text, a, b, size, y=545, italic=True, rest=BIG_REST)
    sc.write()
    return sc


def index(scenes):
    hosts = []
    for z, sc in enumerate(scenes, start=1):
        hosts.append(f'<div id="h-{sc.sid}" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" '
                     f'data-start="{r4(sc.t0)}" data-duration="{r4(sc.dur)}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:{z}"></div>')
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
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r4(TM.TOTAL)}" data-width="1920" data-height="1080">
      <div id="bg" style="position:absolute;inset:0;background:#000"></div>
      {chr(10).join('      ' + h for h in hosts).strip()}
      <audio id="a-mix" src="assets/audio/mix.wav" data-start="0" data-duration="{r4(TM.TOTAL)}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(f"{ROOT}/index.html", "w").write(html)


if __name__ == "__main__":
    os.makedirs(COMP, exist_ok=True)
    scenes = [s_quote(), s_hook(), s_dimon(), s_solomon(), s_search(), s_fink(), s_rest1(), s_rogan(), s_rest2(),
              s_caps()]
    index(scenes)
    print("wrote", len(scenes), "scenes; total", TM.TOTAL)
