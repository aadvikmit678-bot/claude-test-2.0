#!/usr/bin/env python3
"""Writes the HyperFrames project: index.html (scene hosts + the mix) and compositions/s_*.html.

Every time comes from tools/timing.py (60 fps grid). Scene times in the HTML are relative to the scene's start.
Run: python3 tools/build.py
"""
import html as _html
import json
import subprocess
import os

import timing as TM

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMP = f"{ROOT}/compositions"
CLIPS = f"{ROOT}/assets/clips"
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
@font-face{font-family:"HerosR";src:url("assets/fonts/TeXGyreHeros-Regular.otf") format("opentype");font-weight:400;font-style:normal;}
@font-face{font-family:"Bodoni";src:url("assets/fonts/BodoniModa-96-600.ttf") format("truetype");font-weight:600;font-style:normal;}
"""
# the Dario video's Instrument Serif glow (the user: "exactly like the Dario video ... with that white glow")
SERIF_REST = "0 0 14px rgba(255,255,255,0.62),0 0 42px rgba(255,255,255,0.30),0 0 90px rgba(255,255,255,0.12)"
SERIF_SOFT = "0 0 18px rgba(255,255,255,0.85),0 0 50px rgba(255,255,255,0.45),0 0 100px rgba(255,255,255,0.18)"
SERIF_BLOOM = "0 0 22px rgba(255,255,255,1),0 0 60px rgba(255,255,255,0.95),0 0 130px rgba(255,255,255,0.7)"
# the Porsche reel's small italic line: a tight halo and a wide faint one; a faint dark lift over bright pictures
POR_GLOW = "0 0 6px rgba(255,255,255,0.55),0 0 22px rgba(255,255,255,0.32),0 0 48px rgba(255,255,255,0.16)"
# over white pictures (the user's ending video, the S&P logo wall): the same type with a dark halo
POR_HEAVY = POR_GLOW                       # (no dark halo any more: the white shots are toned down under the type instead)

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:#000;}
.full{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.layer{position:absolute;inset:0;}
.cap{position:absolute;left:0;right:0;display:flex;justify-content:center;align-items:center;white-space:nowrap;pointer-events:none;}
.nv{font-family:"InterD",sans-serif;font-weight:800;letter-spacing:-0.02em;color:#fff;text-transform:uppercase;}
.hv{font-family:"Heros",sans-serif;font-weight:700;letter-spacing:-0.012em;color:#EEF0F0;text-transform:uppercase;line-height:1;white-space:nowrap;}
.flash{position:absolute;inset:0;background:#fff;opacity:0;}
.jn{font-family:"HerosR",sans-serif;font-weight:400;font-size:60px;letter-spacing:-0.015em;line-height:1;color:#fff;white-space:nowrap;
 -webkit-text-stroke:0.022em currentColor;text-shadow:0 0 10px rgba(255,255,255,0.36),0 0 26px rgba(255,255,255,0.16);}
.jn.ink{color:#141414;text-shadow:none;}
.jn.heavy{text-shadow:0 0 10px rgba(255,255,255,0.45),0 0 28px rgba(255,255,255,0.2);}
.ser{font-family:"ISerif",serif;font-weight:400;line-height:1;color:#FBF8EC;white-space:nowrap;letter-spacing:0.005em;}
.por{font-family:"ISerif",serif;font-style:italic;font-weight:400;line-height:1;color:#fff;white-space:nowrap;word-spacing:0.38em;}
.por span{display:inline-block;opacity:0;}
.pl{font-family:"Heros",sans-serif;font-weight:700;font-size:94px;line-height:1.02;letter-spacing:-0.015em;color:#EDEDEA;
 text-shadow:0 0 12px rgba(255,255,255,0.35),0 0 30px rgba(255,255,255,0.14);}
.pl span{display:inline-block;opacity:0;}
.dline{display:flex;align-items:baseline;justify-content:center;font-family:"ISerif",serif;font-weight:400;line-height:1;
 color:#fff;white-space:nowrap;letter-spacing:-0.04em;}
.dw{position:relative;display:inline-block;}
.dfl{position:absolute;left:-0.04em;right:-0.04em;top:0.34em;bottom:0.12em;opacity:0;background:#fff;
 box-shadow:0 0 16px rgba(255,255,255,0.9),0 0 44px rgba(255,255,255,0.45);}
.dwt{position:relative;display:inline-block;opacity:0;}
.isnt{display:flex;align-items:baseline;gap:0.11em;font-family:"LGothic",sans-serif;font-weight:400;line-height:1;color:#fff;
 white-space:nowrap;}
.isnt span{display:inline-block;transform-origin:50% 55%;}
.lock{position:absolute;display:flex;align-items:center;white-space:nowrap;pointer-events:none;}
.gt{font-family:"Heros",sans-serif;font-weight:700;letter-spacing:-0.04em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 14px rgba(255,255,255,0.55),0 0 40px rgba(255,255,255,0.28),0 0 90px rgba(255,255,255,0.12);}
.wht2{position:absolute;inset:0;background:#f4f4f0;opacity:0;}
.bigh{font-family:"Heros",sans-serif;font-weight:700;letter-spacing:-0.045em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 16px rgba(255,255,255,0.32);}
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


SHADOW = "text-shadow:0 0 10px rgba(255,255,255,0.40),0 0 28px rgba(255,255,255,0.18);"
# over the ending video (it strobes pure white / black, then bright sand): the same white caption, a heavier halo
SHADOW_HEAVY = SHADOW


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


# Dario's words (the Dimon edit's recipe, read from the Dario reel at 25 fps; the user, Nov 22: "our Dario Amodei style,
# how it comes with that flash"): a word's place lights up as a glowing white bar for two Dario frames, then a small word
# comes in dim and soft for a frame and sits in its white glow, a big word comes in blown out and a little large and is
# crisp four frames later. White glow only, never a dark shadow.
F25 = 0.04


def dario_word_js(sc, wid, t, hero, t_min, rest):
    b0 = max(t_min, t - 2 * F25)
    if t - b0 > 0.015:
        sc.js.append(f'tl.set("#{wid}f",{{opacity:1,filter:"blur({3 if hero else 0}px)"}},{sc.at(b0)});')
        sc.js.append(f'tl.set("#{wid}f",{{opacity:0}},{sc.at(t)});')
    if hero:
        sc.js.append(f'tl.set("#{wid}",{{opacity:1,scale:1.04,filter:"blur(14px)",textShadow:"{SERIF_BLOOM}"}},{sc.at(t)});')
        sc.js.append(f'tl.set("#{wid}",{{scale:1.015,filter:"blur(5px)",textShadow:"{SERIF_SOFT}"}},{sc.at(t + FR)});')
        sc.js.append(f'tl.set("#{wid}",{{scale:1.005,filter:"blur(2.5px)"}},{sc.at(t + 3 * FR)});')
        sc.js.append(f'tl.set("#{wid}",{{scale:1,filter:"blur(0px)",textShadow:"{rest}"}},{sc.at(t + 4 * FR)});')
    else:
        sc.js.append(f'tl.set("#{wid}",{{opacity:0.5,filter:"blur(1.5px)",textShadow:"{SERIF_SOFT}"}},{sc.at(t)});')
        sc.js.append(f'tl.set("#{wid}",{{opacity:1,filter:"blur(0px)",textShadow:"{rest}"}},{sc.at(t + F25)});')


def dario_line(sc, words, a, b, y=540, z=60, italic=True, gap=0.26):
    """words: [(text, onset, size px, hero?)] laid out whole and centred, each word coming in on its onset in its place."""
    spans = []
    for text, t, size, hero in words:
        wid = sc.uid("dw")
        rest = BIG_REST if hero else SERIF_REST
        spans.append(f'<span class="dw" style="font-size:{size}px;margin:0 {gap / 2:.3f}em;"><span id="{wid}f" class="dfl"></span>'
                     f'<span id="{wid}" class="dwt" style="text-shadow:{rest};transform-origin:50% 60%;">'
                     f'{_html.escape(text, quote=False)}</span></span>')
        dario_word_js(sc, wid, t, hero, a, rest)
    st = "font-style:italic;" if italic else ""
    sc.div(a, b, f'<div class="dline" style="{st}">{"".join(spans)}</div>', z=z, cls="cap", style=f"top:{y}px;height:0;")


def dim(sc, a, b, k=0.5, z=5):
    """bright footage brought down under the white type (a black layer at k), so the glow reads without a dark halo"""
    sc.div(a, b, f'<div style="position:absolute;inset:0;background:rgba(0,0,0,{k});"></div>', z=z, cls="layer")


# Reel DdB8's "IT ISN'T" (the user, Nov 22: ON EARTH and IN 1988 "exactly like that"), read frame by frame at 24 fps:
# the shot before goes negative for one frame, two frames of cyan (the red's own negative), then the red card; the
# first word lands in its final place one reel frame 1.25x large, the second joins on its syllable; League Gothic,
# white, the caps ~15 % of the height, the phrase centred, nothing moves after.


def isnt_card(sc, a, b, w1, w2, t2, y=548, size=205, z=30, extra=""):
    """(the lead-in -- one reel frame negative, two cyan -- is in the shot before: r_tiles3 for ON EARTH, the montage's
    fx_out "neg" on "So,"'s shot for IN 1988)"""
    sc.img("red_bg_user.jpg", a, b, z=z - 1)
    i1, i2 = sc.uid("iw"), sc.uid("iw")
    inner = (f'<div class="isnt" style="font-size:{size}px;"><span id="{i1}">'
             f'{_html.escape(w1, quote=False)}</span><span id="{i2}" style="opacity:0;position:relative;">'
             f'{_html.escape(w2, quote=False)}{extra}</span></div>')
    sc.div(a, b, inner, z=z, cls="cap", style=f"top:{y}px;height:0;")
    sc.js.append(f'tl.set("#{i1}",{{scale:1.25}},{sc.at(a)});')             # one reel frame large
    sc.js.append(f'tl.set("#{i1}",{{scale:1}},{sc.at(a + 3 * FR)});')
    sc.js.append(f'tl.set("#{i2}",{{opacity:1}},{sc.at(t2)});')
    return i1, i2


# ------------------------------------------------------------------ v9: the new opening
def lockup(sc, words, a, b, x, y, align="center", z=60, italic=False, gap=0.26, color=None):
    """Dario's words on one line: `align` "left" starts the line at x, "right" ends it at x, "center" centres it on x.
    words: [(text, onset, size px, hero?)], each in on its onset in its own place."""
    spans = []
    for text, t, size, hero in words:
        wid = sc.uid("lw")
        rest = BIG_REST if hero else SERIF_REST
        spans.append(f'<span class="dw" style="font-size:{size}px;margin:0 {gap / 2:.3f}em;"><span id="{wid}f" class="dfl"></span>'
                     f'<span id="{wid}" class="dwt" style="text-shadow:{rest};transform-origin:50% 60%;">'
                     f'{_html.escape(text, quote=False)}</span></span>')
        dario_word_js(sc, wid, t, hero, a, rest)
    st = "font-style:italic;" if italic else ""
    if align == "left":
        box = f"left:{x}px;right:0;justify-content:flex-start;"
    elif align == "right":
        box = f"left:0;right:{1920 - x}px;justify-content:flex-end;"
    else:
        box = (f"left:{2 * x - 1920}px;right:0;" if x >= 960 else f"left:0;right:{1920 - 2 * x}px;") + "justify-content:center;"
    sc.div(a, b, f'<div class="dline" style="{st}">{"".join(spans)}</div>', z=z, cls="lock",
           style=f"top:{y}px;height:0;{box}")


def grot_line(sc, words, a, b, y=540, size=96, z=60):
    """The Hemant video's title line ("CEO of General Catalyst"): the bold grotesque, laid out whole and centred, each
    word cut in on its onset in its own place."""
    spans = []
    for text, t in words:
        wid = sc.uid("gw")
        spans.append(f'<span id="{wid}" style="opacity:0;display:inline-block;">{_html.escape(text, quote=False)}</span>')
        sc.js.append(f'tl.set("#{wid}",{{opacity:1}},{sc.at(t)});')
    sc.div(a, b, f'<div class="gt" style="font-size:{size}px;">{" ".join(spans)}</div>', z=z, cls="cap",
           style=f"top:{y}px;height:0;")



# ============================================================================== v10 (Nov 24, evening)
# The Kalanick reel's serif (DdbK-PAT7O6, read frame by frame at 10 fps): Instrument Serif set tight, a soft white
# halo; a word lands as one reel frame (6 of ours) of blur and bloom, then is crisp.
REEL = 6 * FR
K_REST = "0 0 4px rgba(255,255,255,0.40),0 0 14px rgba(255,255,255,0.20),0 0 34px rgba(255,255,255,0.10)"
K_HERO = "0 0 6px rgba(255,255,255,0.50),0 0 20px rgba(255,255,255,0.26),0 0 50px rgba(255,255,255,0.12)"
K_BLOOM = ("0 0 10px rgba(255,255,255,1),0 0 34px rgba(255,255,255,0.95),0 0 80px rgba(255,255,255,0.75),"
           "0 0 160px rgba(255,255,255,0.45)")
FINK_IN = F(T["powerful"] - TM.LEAD)


def kflash(sc, wid, t, rest=K_REST, blur=6):
    sc.js.append(f'tl.set("#{wid}",{{opacity:1,filter:"blur({blur}px)",textShadow:"{K_BLOOM}"}},{sc.at(t)});')
    sc.js.append(f'tl.set("#{wid}",{{filter:"blur(0px)",textShadow:"{rest}"}},{sc.at(t + REEL)});')


def kline(sc, words, a, b, y, size, rest=K_REST, ls=-0.045, gap=0.12, color="#f4efe6", z=60, flash=True):
    """a Kalanick line: laid out whole and centred, each word landing on its onset in its own place"""
    spans = []
    for text, t in words:
        wid = sc.uid("kw")
        spans.append(f'<span id="{wid}" style="display:inline-block;opacity:0;margin:0 {gap}em;">'
                     f'{_html.escape(text, quote=False)}</span>')
        if flash:
            kflash(sc, wid, t, rest)
        else:
            sc.js.append(f'tl.set("#{wid}",{{opacity:1}},{sc.at(t)});')
    did = sc.div(a, b, f'<div style="display:flex;justify-content:center;align-items:baseline;font-family:\'ISerif\',serif;'
                       f'font-size:{size}px;letter-spacing:{ls}em;line-height:1;color:{color};white-space:nowrap;'
                       f'text-shadow:{rest};">{"".join(spans)}</div>', z=z, cls="cap", style=f"top:{y}px;height:0;")
    return did


# ---- "This is the most powerful man on Earth." (0 to the name mosaic)
FIRST_CSS = """
.ff{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:960px 540px;}
.pl{position:absolute;left:-140px;top:-79px;width:2200px;height:1238px;}
.bgv{position:absolute;left:-144px;top:-81px;width:2208px;height:1242px;object-fit:fill;}
"""


def s_first():
    """v15: the wall (reel DgHoW0vhPvb, now covering the whole frame and bent inward) with "This is the most"; Fink's
    photo arrives as the reel's Chainsmokers do -- one reel frame as a white silhouette, then the photo, in front of the
    soft wall, "powerful man on Earth." behind his head; one subtle push all the way (the user: no zoom in and out);
    on "Earth" a white flash over his cut-out and the background turns to BlackRock's building; a straight cut out."""
    a0, a1 = B["first"]
    sc = Scene("s_first", a0, a1, css=FIRST_CSS)
    sc.video("v15_wall.mp4", a0, FINK_IN, z=1)
    kline(sc, [("This", F(T["this"] - 0.03)), ("is", F(T["is"] - 0.03)), ("the", F(T["the1"] - 0.03)),
               ("most", F(T["most1"] - 0.03))], F(T["this"] - 0.03), FINK_IN, 540, 150, K_HERO, z=30)
    t_e = F(T["earth"] - 0.03)
    ff, pa, pb, cut, line, wf = sc.uid("ff"), sc.uid("pa"), sc.uid("pb"), sc.uid("ct"), sc.uid("kl"), sc.uid("wf")
    spans, words = [], [("powerful", FINK_IN), ("man", F(T["man"] - 0.03)), ("on", F(T["on"] - 0.03)), ("Earth.", t_e)]
    for text, t in words:
        wid = sc.uid("fw")
        spans.append(f'<span id="{wid}" style="display:inline-block;opacity:0;margin:0 0.12em;">{text}</span>')
        kflash(sc, wid, t, K_HERO, blur=7)
    inner = (f'<img id="{pa}" class="clip pl" src="assets/img/v15_bg_wall.jpg" alt="" {sc.timed(FINK_IN, t_e)} '
             f'data-track-index="2" style="z-index:1;" />'
             f'<img id="{pb}" class="clip pl" src="assets/img/v12_bg_b.jpg" alt="" {sc.timed(t_e, a1)} '
             f'data-track-index="2" style="z-index:1;" />'
             f'<div id="{line}" data-layout-allow-overlap style="position:absolute;left:0;right:0;top:96px;display:flex;justify-content:center;'
             f'align-items:baseline;font-family:\'ISerif\',serif;font-size:170px;letter-spacing:-0.045em;line-height:1;'
             f'color:#f4efe6;white-space:nowrap;z-index:2;text-shadow:{K_HERO};">{"".join(spans)}</div>'
             f'<img id="{cut}" class="pl" src="assets/img/v10_fink_cut.png" alt="" style="z-index:3;" />'
             f'<img id="{wf}" class="pl" src="assets/img/v15_fink_white.png" alt="" style="z-index:4;opacity:0;" />')
    sc.add(f'<div id="{ff}" class="clip ff" {sc.timed(FINK_IN, a1)} data-track-index="3" style="z-index:5;">{inner}</div>')
    # one subtle push, start to end
    sc.js.append(f'tl.fromTo("#{ff}",{{scale:1.0}},{{scale:1.045,duration:{r4(a1 - FINK_IN)},ease:"none"}},{sc.at(FINK_IN)});')
    # the arrival: one reel frame as a white silhouette (the reel's Chainsmokers), then the photo
    sc.js.append(f'tl.set("#{wf}",{{opacity:1}},{sc.at(FINK_IN)});tl.set("#{wf}",{{opacity:0}},{sc.at(FINK_IN + 5 * FR)});')
    # "Earth": the flash over his cut-out, out over 0.2 s, as the background changes
    sc.js.append(f'tl.set("#{wf}",{{opacity:1}},{sc.at(t_e)});')
    sc.js.append(f'tl.to("#{wf}",{{opacity:0,duration:0.2,ease:"power1.out"}},{sc.at(t_e + 2 * FR)});')
    sc.write()
    return sc


# ---- "Larry Fink, the CEO of BlackRock" (the v9 name mosaic, re-timed)
def s_name():
    b0, b1 = B["name"]
    sc = Scene("s_name", b0, b1)
    L = lambda k: T[k] - 0.03
    sc.video("v9_mosaic.mp4", b0, b1, z=1)
    t_title = L("the2")
    dario_line(sc, [("Larry", L("larry"), 230, True), ("Fink", L("fink"), 230, True)], F(L("larry") - 2 * F25 - FR),
               F(t_title - FR), y=545, z=30, italic=False, gap=0.2)
    grot_line(sc, [("the", L("the2")), ("CEO", L("ceo")), ("of", L("of0"))], t_title, F(L("blackrock")), y=545, size=124)
    sc.write()
    return sc


# ---- "or how people call it, the most evil company ever built. A $15 trillion dollar cartel of weaponized capital
# that owns a piece of everything you touch."
HOOK_CSS = """
.sw{position:absolute;font-family:"Heros",sans-serif;font-weight:700;font-size:78px;letter-spacing:-0.03em;color:#fff;
 line-height:1;white-space:nowrap;opacity:0;text-shadow:0 0 8px rgba(255,255,255,0.55),0 0 24px rgba(255,255,255,0.28);}
.noise{position:absolute;left:0;right:0;top:540px;height:0;display:flex;justify-content:center;align-items:center;}
.noise span{display:inline-block;font-family:"Bodoni",serif;font-weight:600;font-size:777px;line-height:1;color:#ff1414;
 transform-origin:50% 50%;text-shadow:0 0 18px rgba(255,0,0,0.65),0 0 60px rgba(255,20,20,0.5),0 0 140px rgba(255,40,40,0.35);}
.rglow{position:absolute;inset:0;mix-blend-mode:screen;
 background:radial-gradient(ellipse 30% 48% at 50% 50%,rgba(255,60,70,0.60),rgba(255,40,50,0.22) 55%,rgba(255,0,0,0) 80%);}
"""


def s_hook():
    a0, a1 = B["evil"][0], B["touch"][1]
    sc = Scene("s_hook", a0, a1, css=HOOK_CSS)
    L = lambda k: T[k] - 0.03
    # the red scene, as v6 had it (prep_v10 r_evil)
    sc.video("v10_evil.mp4", *B["evil"], z=1)
    # "company ever": reel DgHoW0vhPvb's "But behind ... all that": a black-and-white crowd in a haze, the words at the
    # sides in the bold sans, each in on its word
    c0, t_b, c1 = B["built"][0], F(T["built"] - TM.LEAD), B["built"][1]
    sc.video("v15_company.mp4", c0, t_b, z=1)
    for word, key, x in (("company", "company", 0.22), ("ever", "ever0", 0.47)):
        wid = sc.uid("sw")
        sc.div(c0, t_b, f'<div id="{wid}" class="sw" style="left:{x * 1920:.0f}px;top:502px;transform:translate(-50%,-50%);">'
                        f'{word}</div>', z=30)
        sc.js.append(f'tl.fromTo("#{wid}",{{opacity:0,filter:"blur(5px)"}},{{opacity:1,filter:"blur(0px)",duration:{r4(3 * FR)},'
                     f'ease:"none"}},{sc.at(L(key))});')
    # "built.": its NOISE: BlackRock's letters on its tower in black and white, a red light behind the word, the word
    # in a tall red Bodoni -- two of its frames stretched wide, then condensed
    sc.video("v10_built.mp4", t_b, c1, z=1)
    sc.div(t_b, c1, "", z=5, cls="layer rglow")
    nid = sc.uid("nz")
    sc.div(t_b, c1, f'<div class="noise"><span id="{nid}">BUILT</span></div>', z=30, cls="layer")
    sc.js.append(f'tl.set("#{nid}",{{scaleX:0.95}},{sc.at(t_b)});')
    sc.js.append(f'tl.set("#{nid}",{{scaleX:0.28}},{sc.at(t_b + 4 * FR)});')
    # "A $15 trillion dollar": the headline cutouts (no highlight, the oval focus), straight into the cartel's faces
    sc.video("v9_cutouts.mp4", *B["money"], z=1)
    sc.video("v10_cartel.mp4", *B["cartel"], z=1)
    sc.video("r_weap.mp4", *B["weap"], z=1)
    dim(sc, *B["weap"], k=0.45)
    sc.video("v6_owns.mp4", *B["logos"], z=1)
    dim(sc, *B["logos"], k=0.5)
    SM, HE, BIG = 100, 175, 225
    phrases = [
        [("cartel", L("cartel"), BIG, True)],
        [("of", L("of1"), SM, False), ("weaponized", L("weapon"), HE, True), ("capital", L("capital"), HE, True)],
        [("that", L("that"), SM, False), ("owns", L("owns"), HE, True)],
        [("a", L("a2"), SM, False), ("piece", L("piece"), HE, True), ("of", L("of2"), SM, False)],
        [("everything", L("everything"), BIG, True)],
    ]
    starts = [F(p[0][1] - 2 * F25 - FR) for p in phrases]
    starts[0] = max(starts[0], B["cartel"][0])
    ends = starts[1:] + [F(T["touch"] - 0.03)]
    for p, a, b in zip(phrases, starts, ends):
        dario_line(sc, p, a, b, y=540, z=30, italic=False)
    sc.video("r_touch3.mp4", *B["touch"], z=1)
    sc.write()
    return sc


# ---- "A company that's never made a single physical product,"
MADE_CSS = """
.paper{position:absolute;inset:0;background:url("assets/img/paper_light.png") center/cover no-repeat;}
.card{position:absolute;overflow:hidden;border-radius:6px;box-shadow:0 26px 70px rgba(0,0,0,0.55),0 0 140px rgba(0,0,0,0.30);}
.card video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.ink{position:absolute;top:540px;height:0;display:flex;align-items:center;white-space:nowrap;font-family:"ISerif",serif;
 font-size:88px;letter-spacing:-0.03em;line-height:1;color:#0b0b0b;}
.ink span{display:inline-block;opacity:0;margin:0 0.12em;}
.whitep{position:absolute;inset:0;background:linear-gradient(to bottom,#dcdcdc 0%,#fbfbfb 16%,#fdfdfd 50%,#fbfbfb 84%,#dcdcdc 100%);}
.turn{position:absolute;left:0;right:0;top:390px;height:300px;}
.turn .tl{display:flex;align-items:baseline;white-space:nowrap;font-family:"ISerif",serif;font-size:225px;letter-spacing:-0.055em;
 line-height:1;color:#111;transform-origin:50% 50%;}
.turn .tl span{display:inline-block;opacity:0;margin:0 0.11em;}
.tl2{position:relative;width:1920px;height:300px;transform-origin:960px 150px;}
.tline{position:absolute;left:0;right:0;top:0;height:300px;display:flex;justify-content:center;align-items:center;white-space:nowrap;
 font-family:"ISerif",serif;font-size:225px;letter-spacing:-0.055em;word-spacing:0.08em;line-height:1;color:#111;}
.slam{position:absolute;left:40px;top:540px;height:0;display:flex;align-items:center;white-space:nowrap;font-family:"ISerif",serif;
 font-size:1460px;letter-spacing:-0.055em;line-height:1;color:#111;}
"""


def s_made():
    """The user (Nov 24): this frame, on the Pattinson video's paper with the dark light behind the card, the words
    black, "A company that's" left of the card and "never made" right of it at one size, the card's footage fast and only
    while that is said; then "a single physical product" as the Kalanick reel's "turning a crazy idea" (13.2-14.4 s):
    one frame of the line's start enormous, then the line building word by word on white while it grows, then sinking
    out of the frame into the next shot."""
    a0, a1 = B["made"]
    sc = Scene("s_made", a0, a1, css=MADE_CSS)
    L = lambda k: T[k] - 0.03
    t_k = F(T["a4"] - TM.LEAD)
    sc.div(a0, t_k, "", z=1, cls="layer paper")
    X, Y, CW, CH = 650, 366, 620, 349
    cid, vid = sc.uid("cd"), sc.uid("v")
    sc.add(f'<div id="{cid}" class="card" style="left:{X}px;top:{Y}px;width:{CW}px;height:{CH}px;z-index:5;">'
           f'<video id="{vid}" class="clip" src="assets/clips/v10_factory.mp4" {sc.timed(a0, t_k)} '
           f'data-media-start="0.0000" data-track-index="1" muted playsinline></video></div>')
    sc.js.append(f'tl.fromTo("#{cid}",{{scale:0.96}},{{scale:1,duration:0.32,ease:"power3.out"}},0);')
    sc.js.append(f'tl.set("#{cid}",{{opacity:0}},{sc.at(t_k)});')
    for words, x, side in (([("A", "a3"), ("company", "company2"), ("that’s", "thats")], 612, "right"),
                           ([("never", "never"), ("made", "made")], 1308, "left")):
        spans = []
        for w, k in words:
            wid = sc.uid("iw")
            spans.append(f'<span id="{wid}">{w}</span>')
            sc.js.append(f'tl.fromTo("#{wid}",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",'
                         f'duration:{r4(REEL)},ease:"none"}},{sc.at(L(k))});')
        box = f"left:0;right:{1920 - x}px;justify-content:flex-end;" if side == "right" else f"left:{x}px;right:0;justify-content:flex-start;"
        sc.div(a0, t_k, f'<div class="ink" style="{box}">{"".join(spans)}</div>', z=10, cls="layer")
    # "a single physical product": the Kalanick reel's "turning a crazy idea" (13.3-14.3 s, measured frame by frame):
    # the words come one by one, the line always centred, and the whole line grows smoothly as it builds (0.63 -> 1.0,
    # fast first, then slower), then sinks out of the frame (v15: no giant first frame -- the user)
    sc.div(t_k, a1, "", z=1, cls="layer whitep")
    tl_id = sc.uid("tl")
    ws = [("a", max(L("a4"), t_k)), ("single", L("single")), ("physical", L("physical")), ("product", L("product"))]
    t_x = F(a1 - 12 * FR)
    states = []
    for k in range(len(ws)):
        s0 = F(ws[k][1])
        s1 = F(ws[k + 1][1]) if k + 1 < len(ws) else a1
        text = " ".join(w for w, _ in ws[:k + 1])
        states.append(f'<div class="clip tline" {sc.timed(s0, s1)} data-track-index="3">{text}</div>')
    sc.add(f'<div class="turn" style="z-index:10;"><div id="{tl_id}" class="tl2">{"".join(states)}</div></div>')
    t_in = F(ws[0][1])
    sc.js.append(f'tl.fromTo("#{tl_id}",{{scale:0.63}},{{scale:1.0,duration:{r4(F(ws[-1][1]) + 0.15 - t_in)},ease:"power2.out"}},{sc.at(t_in)});')
    sc.js.append(f'tl.to("#{tl_id}",{{scale:1.03,duration:{r4(max(FR, t_x - F(ws[-1][1]) - 0.15))},ease:"none"}},{sc.at(F(ws[-1][1]) + 0.15)});')
    sc.js.append(f'tl.to("#{tl_id}",{{y:40,duration:{r4(6 * FR)},ease:"power1.in"}},{sc.at(t_x)});')
    sc.js.append(f'tl.to("#{tl_id}",{{y:300,duration:{r4(6 * FR)},ease:"power2.in"}},{sc.at(t_x + 6 * FR)});')
    sc.write()
    return sc


# ---- "yet it's one of the top shareholders in almost every major" (the cards done by "major"), then "U.S. company."
SHARE_CSS = """
.lc{position:absolute;width:238px;height:150px;border-radius:9px;background:#0e0e0e;border:1px solid rgba(255,255,255,0.2);opacity:0;}
.lc img{position:absolute;left:83px;top:24px;width:72px;height:72px;}
.lc span{position:absolute;left:0;right:0;top:112px;text-align:center;font-family:"Heros",sans-serif;font-weight:700;font-size:19px;letter-spacing:0.08em;color:#a8a8a8;line-height:1;}
.lw{position:absolute;inset:0;border-radius:8px;background:#f6f6f4;}
"""
LOGOS = [("apple", "AAPL"), ("microsoft", "MSFT"), ("nvidia", "NVDA"), ("amazon", "AMZN"), ("google", "GOOGL"),
         ("meta", "META"), ("tesla", "TSLA"), ("netflix", "NFLX"), ("visa", "V"), ("mastercard", "MA"),
         ("target", "TGT"), ("paypal", "PYPL"), ("pepsi", "PEP"), ("mcdonalds", "MCD"), ("nike", "NKE"),
         ("starbucks", "SBUX"), ("intel", "INTC"), ("amd", "AMD"), ("ibm", "IBM"), ("oracle", "ORCL"),
         ("adobe", "ADBE"), ("chase", "JPM"), ("bankofamerica", "BAC"), ("boeing", "BA"), ("ford", "F"),
         ("fedex", "FDX"), ("ups", "UPS"), ("uber", "UBER")]
# the order the cards arrive in (a fixed scatter over the 4 x 7 slots, nothing random at render time)
SHARE_ORDER = [10, 24, 3, 17, 6, 21, 13, 0, 27, 8, 19, 5, 15, 22, 11, 2, 25, 9, 18, 26, 1, 14, 20, 7, 23, 4, 16, 12]

SHARE_CSS += """
.mid{position:absolute;left:0;right:0;top:540px;height:0;display:flex;justify-content:center;align-items:center;}
.big{font-family:"Heros",sans-serif;font-weight:700;font-size:250px;letter-spacing:-0.045em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 14px rgba(255,255,255,0.45),0 0 40px rgba(255,255,255,0.22);}
"""


def s_share():
    """The Hemant video's cards with the companies' marks round "top shareholders" (the serif, in the middle), one card
    after another, faster and faster, all in by "major" (the user); "in almost every" in the middle in the caption sans,
    "major" big in the sans, then the cut to the flag (s_us)."""
    a0, a1 = B["share"][0], F(T["us"] - TM.LEAD)
    sc = Scene("s_share", a0, a1, css=SHARE_CSS)
    L = lambda k: T[k] - 0.03
    t_in2 = F(L("in2"))
    lockup(sc, [("top", L("top"), 172, True), ("shareholders", L("shareholders"), 172, True)],
           F(L("top") - 2 * F25 - FR), t_in2, 960, 545, z=30, gap=0.22)
    # "in almost every": the caption line, building word by word in the middle
    ws = [("in", L("in2")), ("almost", L("almost")), ("every", L("every")), ("major", L("major"))]
    for k in range(len(ws)):                     # (v15: "major" in the caption type too -- the user)
        s0 = F(ws[k][1])
        s1 = F(ws[k + 1][1]) if k + 1 < len(ws) else a1
        text = " ".join(w for w, _ in ws[:k + 1])
        sc.div(s0, s1, f'<div class="jn">{text}</div>', z=30, cls="cap", style="top:540px;height:0;")
    rows, cols = [100, 270, 810, 980], [180 + 260 * k for k in range(7)]
    t0, t1 = L("one"), F(L("major") - 4 * FR)
    N = len(SHARE_ORDER)
    cards = []
    for j, slot in enumerate(SHARE_ORDER):
        slug, tick = LOGOS[slot]
        r, c = divmod(slot, 7)
        cid, wid = sc.uid("lc"), sc.uid("lw")
        tid = sc.uid("tk")
        cards.append(f'<div id="{cid}" class="lc" style="left:{cols[c] - 119}px;top:{rows[r] - 75}px;">'
                     f'<img src="assets/logos/{slug}.svg" alt="" /><span id="{tid}" style="opacity:0;">{tick}</span><div id="{wid}" class="lw"></div></div>')
        t = t0 + (t1 - t0) * (j / (N - 1)) ** 0.62
        sc.js.append(f'tl.set("#{cid}",{{opacity:1}},{sc.at(t)});tl.set("#{wid}",{{opacity:0}},{sc.at(t + 2 * FR)});'
                     f'tl.set("#{tid}",{{opacity:1}},{sc.at(t + 2 * FR)});')
    sc.div(a0, a1, "".join(cards), z=6)
    sc.write()
    return sc


def s_us():
    """"U.S. company.": the Kalanick reel's "global company" on the Earth (16.7-17.5 s): a cut to the picture (the
    user's flag), the words small in the middle in the serif, blooming in, coloured squares jumping about; then a cut to
    a closer framing, the words staying (prep_v10 r_flag)."""
    a0, a1 = F(T["us"] - TM.LEAD), B["share"][1]
    sc = Scene("s_us", a0, a1)
    sc.video("v10_flag.mp4", a0, a1, z=1)
    kline(sc, [("U.S.", F(T["us"] - 0.03)), ("company", F(T["company3"] - 0.03))], a0, a1, 560, 108, K_HERO, z=30)
    sc.write()
    return sc


# ---- "It holds more of Nvidia than Jensen Huang ...": the v9 page (the user: "the format is correct"), without its
# label, the company's name, the "× more" badge, the source line and the founder's card; on each founder's name the
# earlier versions' full-frame clip of him (prep_v10 r_founders: v3_r1_jensen / gates / jobs)
STAKE = json.load(open(f"{ROOT}/tools/words/stake.json"))
PAGE = "rgb(%d,%d,%d)" % tuple(STAKE["page"])
STAKE_CSS = """
.pw{position:absolute;}
.pw img{position:absolute;left:0;top:0;width:100%;height:100%;}
.scr{position:absolute;overflow:hidden;opacity:0;background:#0b0b0b;}
.scr video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.jcard{border-radius:14px;border:4px solid #141414;box-shadow:0 18px 40px rgba(0,0,0,0.28);}
.k{position:absolute;left:1040px;font-family:"InterSB",sans-serif;font-weight:600;color:#5c5c5c;font-size:26px;letter-spacing:0.12em;line-height:1;white-space:nowrap;}
.co{position:absolute;left:1036px;top:112px;font-family:"InterD",sans-serif;font-weight:800;font-size:124px;letter-spacing:-0.035em;color:#121212;line-height:1;white-space:nowrap;opacity:0;}
.lab{position:absolute;left:1040px;font-family:"HerosR",sans-serif;font-weight:400;font-size:48px;letter-spacing:-0.02em;color:#141414;line-height:1;white-space:nowrap;-webkit-text-stroke:0.022em currentColor;}
.num{position:absolute;right:90px;font-family:"ISerif",serif;font-size:150px;letter-spacing:-0.01em;color:#141414;line-height:1;white-space:nowrap;font-variant-numeric:tabular-nums lining-nums;}
.trk{position:absolute;left:1040px;width:790px;height:26px;background:#c6c6c4;border-radius:3px;overflow:hidden;}
.fill{position:absolute;left:0;top:0;width:790px;height:26px;transform-origin:0 50%;}
.bdg{position:absolute;right:90px;top:826px;font-family:"InterD",sans-serif;font-weight:800;font-size:58px;letter-spacing:-0.03em;color:#f4f4f2;background:#141414;border-radius:12px;padding:12px 26px 14px;line-height:1;white-space:nowrap;opacity:0;}
.src{position:absolute;left:96px;top:1022px;font-family:"InterSB",sans-serif;font-size:21px;letter-spacing:0.04em;color:#5c5c5c;line-height:1;white-space:nowrap;}
"""
# Think School's page ("Founders vs Blackrock", source: Investopedia, Yahoo Finance): the founder's stake and BlackRock's
FOUNDERS = [
    dict(key="gpu", co="Nvidia", who="Jensen Huang", vid="v9_jensen.mp4", color="#4a8600", br=8.02, fo=3.7, fo_s="3.7%",
         w_co="nvidia", w_f="jensen", w_l="huang", mult="2.2× more"),
    dict(key="pc", co="Microsoft", who="Bill Gates", vid="v9_gates.mp4", color="#c8431a", br=8.18, fo=1.34, fo_s="1.34%",
         w_co="microsoft", w_f="bill", w_l="gates", mult="6.1× more"),
    dict(key="mac", co="Apple", who="Steve Jobs", vid="v9_jobs.mp4", color="#1676c8", br=7.97, fo=0.24, fo_s="0.24%",
         w_co="apple", w_f="steve", w_l="jobs", mult="33× more"),
]
FULL = 10.0          # the bars' full width stands for 10 % of the company


def count(sc, eid, v0, v1, t0, dur, final):
    """A figure rolling from v0 to v1 (a set every second frame, an ease-out), landing on the page's own figure."""
    n = max(2, round(dur * 60))
    for f in range(0, n, 2):
        u = f / n
        v = v0 + (v1 - v0) * (1 - (1 - u) ** 3)
        sc.js.append(f'tl.set("#{eid}",{{textContent:"{v:.2f}%"}},{sc.at(t0 + f * FR)});')
    sc.js.append(f'tl.set("#{eid}",{{textContent:"{final}"}},{sc.at(t0 + n * FR)});')




def s_stake():
    """The v9 page without its label, the company's name, the "x more" badge and the source line (the user): the
    product, BlackRock's share (its bar and figure) and, on the company's name, the founder's (his name, figure and
    bar, in his company's colour) -- then on the founder's name the earlier versions' clip of him. Each company's page
    is its own element, ending where the founder's clip starts."""
    a0, a1 = B["stake"]
    sc = Scene("s_stake", a0, a1, bg=PAGE, css=STAKE_CSS)
    L = lambda k: T[k] - 0.03
    LD = lambda k: F(T[k] - TM.LEAD)
    cuts_ = [a0, LD("more2"), LD("and"), a1]
    CX, CY = 505, 520
    prev = 0.0
    for k, fd in enumerate(FOUNDERS):
        s0, s1 = cuts_[k], cuts_[k + 1]
        t_co, t_f = L(fd["w_co"]), LD(fd["w_f"])
        pr = STAKE[fd["key"]]
        px, py = CX - pr["w"] // 2, CY - pr["h"] // 2
        t_a = L("holds") if k == 0 else s0
        d_a = 0.5 if k == 0 else 0.34
        na, fa, lb, nb, fb, pw = (sc.uid(x) for x in ("na", "fa", "lb", "nb", "fb", "pw"))
        page = (f'<div class="lab" style="top:356px;">BlackRock</div>'
                f'<div id="{na}" class="num" style="top:300px;">{prev:.2f}%</div>'
                f'<div class="trk" style="top:470px;"><div id="{fa}" class="fill" style="background:#141414;"></div></div>'
                f'<div class="trk" style="top:734px;"><div id="{fb}" class="fill" style="background:{fd["color"]};"></div></div>'
                f'<div id="{lb}" class="lab" style="top:620px;opacity:0;">{fd["who"]}</div>'
                f'<div id="{nb}" class="num" style="top:564px;opacity:0;color:{fd["color"]};">0.00%</div>'
                f'<div id="{pw}" class="pw" style="left:{px}px;top:{py}px;width:{pr["w"]}px;height:{pr["h"]}px;">'
                f'<img src="assets/img/v9_{fd["key"]}.png" alt="" /></div>')
        sc.div(s0, t_f, page, z=4)
        sc.js.append(f'tl.set("#{fa}",{{scaleX:{prev / FULL:.4f}}},{sc.at(s0)});tl.set("#{fb}",{{scaleX:0}},{sc.at(s0)});')
        sc.js.append(f'tl.to("#{fa}",{{scaleX:{fd["br"] / FULL:.4f},duration:{d_a},ease:"power3.out"}},{sc.at(t_a)});')
        count(sc, na, prev, fd["br"], t_a, d_a, f'{fd["br"]:.2f}%')
        prev = fd["br"]
        t_p = L("more1") if k == 0 else s0
        sc.js.append(f'tl.fromTo("#{pw}",{{y:34,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"power3.out"}},{sc.at(t_p)});')
        sc.js.append(f'tl.set("#{lb}",{{opacity:1}},{sc.at(t_co)});tl.set("#{nb}",{{opacity:1}},{sc.at(t_co)});')
        sc.js.append(f'tl.to("#{fb}",{{scaleX:{fd["fo"] / FULL:.4f},duration:0.3,ease:"power3.out"}},{sc.at(t_co)});')
        count(sc, nb, 0.0, fd["fo"], t_co, 0.3, fd["fo_s"])
        clip = {"gpu": "v3_r1_jensen.mp4", "pc": "v3_r1_gates.mp4", "mac": "v3_r1_jobs.mp4"}[fd["key"]]
        sc.video(clip, t_f, s1, z=20)
    sc.write()
    return sc


# ------------------------------------------------------------------ Rogan: Elon's question, then Rogan's silent second
def s_rogan():
    a, b = B["rogan"][0], B["react"][1]
    sc = Scene("s_rogan", a, b)
    sc.video("v5_rogan.mp4", *B["rogan"], z=1)             # Elon, through "company?" and his short silent pause
    if B["react"][1] - B["react"][0] > FR / 2:
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
    sc.div(a, b, f'<div id="{stack}" style="position:absolute;left:118px;top:300px;text-align:left;">{"".join(rows)}</div>',
           z=40, cls="layer")
    for sid, t in sets:
        sc.js.append(f'tl.fromTo("#{sid}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",'
                     f'duration:0.22,ease:"power2.out"}},{sc.at(t)});')
    sc.js.append(f'tl.to("#{stack}",{{opacity:0,filter:"blur(10px)",duration:0.2,ease:"power1.in"}},{sc.at(b - 0.2)});')
    sc.flash(b - FR, peak=1.0, up=4 * FR, down=FR, z=90)     # the flash into "Back in the 1980s" (no pause)
    sc.write()
    return sc


# ------------------------------------------------------------------ rest2: "Back in the 1980s" to the end
def s_rest2():
    sc = Scene("s_rest2", *B["rest2"])
    sc.video("v6_rest2.mp4", *B["rest2"], z=1)         # prep_v5: the shots, cut on the words (shotlist.REST2_V6)
    sc.flash(B["rest2"][0], peak=1.0, up=0, down=0.22, z=90)  # out of the Rogan flash
    for a, b, kind, words, text in CAP.porsche_phrases():
        if kind != "card":
            continue
        # "in 1988": exactly like reel DdB8's "IT ISN'T" (the user, Nov 22), as ON EARTH; then on "1988" the Tesla
        # reel's boxes snap round the year (outlines, one filled wipe, a wide frame), one every two frames
        t8 = words[1][1]
        boxes = [(-0.10, -0.10, 0.10, 0.02, 0, 2, "o"), (-0.26, -0.26, -0.04, -0.10, 2, 4, "o"),
                 (-0.05, -0.05, 0.16, 0.08, 4, 6, "f"), (-1.45, -0.95, -0.55, -0.55, 6, 8, "o"),
                 (-0.16, -0.16, 0.04, -0.03, 8, 10, "o")]
        extra, sets = "", []
        for k, (l, r, t, btm, f0, f1, kind) in enumerate(boxes):
            bid = sc.uid("bx")
            look = "background:#fff;" if kind == "f" else "border:0.03em solid #fff;"
            extra += (f'<span id="{bid}" style="position:absolute;left:{l}em;right:{r}em;top:{t}em;bottom:{btm}em;'
                      f'{look}opacity:0;display:block;transform:none;"></span>')
            sets.append((bid, t8 + f0 * FR, t8 + f1 * FR))
        isnt_card(sc, a, b, words[0][0], words[1][0], t8, z=6, extra=extra)   # ("So,"'s shot ends negative)
        for bid, s0, s1 in sets:
            sc.js.append(f'tl.set("#{bid}",{{opacity:1}},{sc.at(s0)});tl.set("#{bid}",{{opacity:0}},{sc.at(s1)});')
    sc.write()
    return sc



# ---- "but one bad bet cost him $100 million loss." (v15)
BET_CSS = """
.hb{position:absolute;left:1000px;top:190px;font-family:"ISerif",serif;font-size:196px;letter-spacing:-0.05em;line-height:0.84;
 color:#f6f1e8;white-space:nowrap;}
.hb span{display:inline-block;opacity:0;margin-right:0.16em;}
"""
RI = lambda i: TM.R(TM.ALIGN["rest"][i]["start"])        # a rest-recording word's film time, by its index


def s_bet():
    """The Kalanick reel's "he's coming back hungrier." (9.0-9.7 s): through one reel frame of the next shot smeared
    in black and white to the shot -- the user's money clip, dark and warm with a red light at the right, textured --
    and the two lines at the right in the serif with its white glow, each word landing with the reel's bloom; then
    the $100 million counter (prep_v10 r_count: the Kalanick year roll, 19.2-20.8 s)."""
    a0 = F(TM.RT("but1") - TM.LEAD)
    t_c = F(TM.RT("cost") - TM.LEAD)
    a1 = F(RI(50) - TM.LEAD)
    sc = Scene("s_bet", a0, a1, css=BET_CSS)
    sc.video("v15_bet.mp4", a0, t_c, z=1)
    sc.video("v14_count.mp4", t_c, a1, z=1)
    glow = "0 0 8px rgba(255,255,255,0.62),0 0 26px rgba(255,255,255,0.34),0 0 72px rgba(255,255,255,0.18)"
    lines = []
    for row in ([("but", RI(41)), ("one", RI(42))], [("bad", RI(43)), ("bet", RI(44))]):
        spans = []
        for w, t in row:
            wid = sc.uid("hw")
            spans.append(f'<span id="{wid}">{w}</span>')
            kflash(sc, wid, F(max(t - 0.03, a0 + 6 * FR)), glow, blur=7)
        lines.append("".join(spans))
    sc.div(a0, t_c, f'<div class="hb" style="text-shadow:{glow};">{"<br>".join(lines)}</div>', z=30, cls="layer")
    sc.write()
    return sc


# ---- "So, in 1988, he co-founded BlackRock and built a system with one job -- calculating risk. He called it
# Aladdin." (v15): the Anthropic reel's 10-20 s, device by device, over v6_rest2's shots (this scene sits above it)
RISK_CSS = """
.yr{position:absolute;left:40px;top:250px;width:1000px;height:300px;display:flex;align-items:center;justify-content:center;
 font-family:"Heros",sans-serif;font-weight:700;font-size:330px;letter-spacing:-0.045em;line-height:1;color:#fff;
 text-shadow:0 0 18px rgba(0,0,0,0.25);}
.page{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;}
.logo{font-family:"Heros",sans-serif;font-weight:700;font-size:250px;letter-spacing:-0.035em;line-height:1;white-space:nowrap;}
.wp{position:absolute;inset:0;background:#fbfbfa;}
.it{position:absolute;left:0;right:0;top:540px;height:0;display:flex;justify-content:center;align-items:center;white-space:nowrap;
 font-family:"ISerif",serif;font-size:120px;letter-spacing:-0.045em;line-height:1;color:#111;}
.it span{display:inline-block;opacity:0;margin:0 0.11em;}
.bigb{font-family:"Heros",sans-serif;font-weight:700;letter-spacing:-0.045em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 16px rgba(255,255,255,0.35);}
.ybox{display:inline-block;background:#f2c200;color:#fff;font-family:"HerosR",sans-serif;font-size:56px;letter-spacing:-0.015em;
 -webkit-text-stroke:0.022em currentColor;padding:8px 18px 12px;line-height:1;white-space:nowrap;}
.sil{position:absolute;left:0;top:0;width:1920px;height:1080px;}
"""


def s_risk():
    a0, a1 = F(TM.RT("so") - TM.LEAD), F(TM.RT("when") - TM.LEAD)
    sc = Scene("s_risk", a0, a1, bg="transparent", css=RISK_CSS)
    Lr = lambda i: F(RI(i) - 0.03)

    def build(words, t_end, y=540, cls="jn", z=40):
        """the reel's small caption: the phrase building word by word in the middle"""
        for k in range(len(words)):
            s0 = words[k][1]
            s1 = words[k + 1][1] if k + 1 < len(words) else t_end
            text = " ".join(w for w, _ in words[:k + 1])       # (each entry one word)
            sc.div(s0, s1, f'<div class="{cls}">{text}</div>', z=z, cls="cap", style=f"top:{y}px;height:0;")

    # "So," -- the reel's "And": the small caption on the shot (v6_rest2's old board)
    t88 = Lr(77)
    build([("So", Lr(75))], t88)
    # "in 1988," -- the reel's "2018" (12.82-13.57): a white silhouette frame, the number scrambling for two reel
    # frames, then the year (prep_v10 r_r88: Fink seated at the Economic Club)
    t_he = Lr(78)
    sc.video("v15_r88.mp4", t88, t_he, z=1)
    yid = sc.uid("yr")
    sc.div(t88, t_he, f'<div id="{yid}" class="yr">1907</div>', z=30, cls="layer")
    sc.js.append(f'tl.set("#{yid}",{{textContent:"2996"}},{sc.at(t88 + 5 * FR)});')
    sc.js.append(f'tl.set("#{yid}",{{textContent:"1988"}},{sc.at(t88 + 10 * FR)});')
    # "he co-founded" -- the reel's "Elon left"
    t_br = Lr(80)
    build([("he", t_he), ("co-founded", Lr(79))], t_br)
    # the reel's one-frame negative (11.32 s), on the shot before the page
    sc.img("v15_neg_br.jpg", F(t_br - 5 * FR), t_br, z=15)
    # "BlackRock" -- the reel's ANTHROP\\C: one reel frame of the other page, then the brand's own
    t_and = Lr(81)
    sc.div(t_br, F(t_br + 5 * FR), '<div class="page" style="background:#fbfbfa;"><div class="logo" style="color:#111;">BlackRock</div></div>',
           z=20, cls="layer")
    sc.div(F(t_br + 5 * FR), t_and, '<div class="page" style="background:#0b0b0b;"><div class="logo" style="color:#fff;">BlackRock</div></div>',
           z=20, cls="layer")
    # "and built a system" -- the reel's "walked out to start": a white page, the italic serif building word by word
    t_with = Lr(85)
    sc.div(t_and, t_with, "", z=20, cls="layer wp")
    spans = []
    for w, i in (("and", 81), ("built", 82), ("a", 83), ("system", 84)):
        wid = sc.uid("iw")
        spans.append(f'<span id="{wid}">{w}</span>')
        tw = max(Lr(i), t_and)                       # (v15: the Kalanick serif, upright; one reel frame soft, then crisp)
        sc.js.append(f'tl.set("#{wid}",{{opacity:1,filter:"blur(5px)"}},{sc.at(tw)});tl.set("#{wid}",{{filter:"blur(0px)"}},{sc.at(tw + REEL)});')
    sc.div(t_and, t_with, f'<div class="it">{"".join(spans)}</div>', z=22, cls="layer")
    # "with one job" -- the reel's "just had the" (the data centre, the glass brain); "calculating" on the chalkboard
    t_calc, t_risk = Lr(88), Lr(89)
    sc.video("v15_job.mp4", Lr(86), t_calc, z=1)       # (the ring of screens, not the brain shot's burned-in text)
    build([("with", t_with), ("one", Lr(86)), ("job", Lr(87))], t_calc)
    build([("calculating", t_calc)], t_risk)
    sc.img("v15_neg_risk.jpg", F(t_risk - 5 * FR), t_risk, z=15)
    # "risk." -- the reel's "biggest": big, bold, lowercase, on the next shot
    t_hc = F(RI(90) - TM.LEAD)
    sc.div(t_risk, t_hc, '<div class="bigb" style="font-size:300px;">risk.</div>', z=30, cls="cap", style="top:540px;height:0;")
    # "He called it" -- the reel's "Now elon's": the man's white silhouette for two reel frames, the yellow label
    t_al = Lr(93)
    sc.add(f'<img id="{sc.uid("sl")}" class="clip sil" src="assets/img/v15_called_white.png" alt="" {sc.timed(t_hc, F(t_hc + 10 * FR))} '
           f'data-track-index="2" style="z-index:25;" />')
    for k, (txt, t) in enumerate((("He", max(Lr(90), t_hc)), ("He called", Lr(91)), ("He called it", Lr(92)))):
        nxt = (Lr(91), Lr(92), t_al)[k]
        sc.div(t, nxt, f'<div class="ybox">{txt}</div>', z=40, cls="cap", style="top:600px;height:0;")
    # "Aladdin." -- the reel's "SPACE X": the name big in bold capitals over the genie, landing with a bloom
    aid = sc.uid("al")
    sc.div(t_al, a1, f'<div id="{aid}" class="bigb" style="font-size:250px;opacity:0;">ALADDIN</div>', z=30, cls="cap",
           style="top:540px;height:0;")
    kflash(sc, aid, t_al, "0 0 16px rgba(255,255,255,0.35)", blur=8)
    sc.write()
    return sc


# ------------------------------------------------------------------ s_caps: every caption, on its word
import captions as CAP

SL_white = ("a2", "has")                    # rest-recording keys: the ending video's span


HELV_LINES = {"the U.S. government", "called", "the one guy", "Today,", "every time", "you buy the", "your money",
              "ends up in"}


def hl_line(sc, words, t_end, y=545):
    """the Anthropic reel's small caption: the line builds word by word, re-centring each time"""
    for k in range(len(words)):
        s0 = words[k][1]
        s1 = words[k + 1][1] if k + 1 < len(words) else t_end
        if s1 - s0 < FR:
            continue
        text = " ".join(w for w, _ in words[:k + 1])
        sc.div(s0, s1, f'<div class="jn">{_html.escape(text, quote=False)}</div>', z=60, cls="cap", style=f"top:{y}px;height:0;")


def s_caps():
    sc = Scene("s_caps", 0.0, TM.TOTAL, bg="transparent")
    # 1. the Jensen reel's line (and the serif key words) to "...ever did."
    for a, b, ws, kind in CAP.jensen_phrases():
        if kind == "emph":
            serif(sc, " ".join(w for w, _, _ in ws), a, b, 150, y=540)
            continue
        y, cls = {"ink": (972, "jn ink"), "heavy": (540, "jn heavy"), "low": (705, "jn")}.get(kind, (540, "jn"))
        for k in range(len(ws)):                       # the phrase builds word by word, re-centring as it grows
            s0 = ws[k][1]
            s1 = ws[k + 1][1] if k + 1 < len(ws) else b
            if s1 - s0 < FR:
                continue
            text = " ".join(w for w, _, _ in ws[:k + 1])
            sc.div(s0, s1, f'<div class="{cls}">{text}</div>', z=60, cls="cap", style=f"top:{y}px;height:0;")
    # 3. from "Back in the 1980s" (v15, the user: the type of the whole video): mostly the Kalanick reel's serif --
    # upright, tight, its soft white glow, the line laid out and centred, each word landing in its place with one reel
    # frame of bloom; some lines in the Anthropic reel's Helvetica, building word by word and re-centring; the figures
    # big in its bold Helvetica (its "2015" / "2018"); never two fonts in one line
    for a, b, kind, words, text in CAP.porsche_phrases():
        if kind in ("skip", "card"):
            continue
        if kind == "big":
            size = {"2008": 330, "3x": 420}.get(text, 240)
            sc.div(a, b, f'<div class="bigh" style="font-size:{size}px;">{_html.escape(text, quote=False)}</div>', z=60, cls="cap",
                   style="top:540px;height:0;")
            continue
        if kind == "type":
            hl_line(sc, [(w, t) for w, t in words], b)
            continue
        if text in HELV_LINES:
            hl_line(sc, words, b)
            continue
        size, rest = (150, K_HERO) if kind == "word" else (84, K_REST)
        kline(sc, words, a, b, 545, size, rest, z=60)
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
    scenes = [s_first(), s_name(), s_hook(), s_made(), s_share(), s_us(), s_stake(), s_rogan(), s_rest2(), s_bet(), s_risk(),
              s_caps()]
    index(scenes)
    print("wrote", len(scenes), "scenes; total", TM.TOTAL)
