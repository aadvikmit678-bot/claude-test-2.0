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
.jn{font-family:"InterSB",sans-serif;font-weight:600;font-size:62px;letter-spacing:-0.05em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 10px rgba(255,255,255,0.40),0 0 28px rgba(255,255,255,0.18);}
.jn.ink{color:#141414;text-shadow:none;}
.jn.heavy{text-shadow:0 0 10px rgba(255,255,255,0.45),0 0 28px rgba(255,255,255,0.2);}
.ser{font-family:"ISerif",serif;font-weight:400;line-height:1;color:#FBF8EC;white-space:nowrap;letter-spacing:0.005em;}
.por{font-family:"ISerif",serif;font-style:italic;font-weight:400;line-height:1;color:#fff;white-space:nowrap;word-spacing:0.38em;}
.por span{display:inline-block;opacity:0;}
.pl{font-family:"Heros",sans-serif;font-weight:700;font-size:94px;line-height:1.02;letter-spacing:-0.015em;color:#EDEDEA;
 text-shadow:0 0 12px rgba(255,255,255,0.35),0 0 30px rgba(255,255,255,0.14);}
.pl span{display:inline-block;opacity:0;}
.dline{display:flex;align-items:baseline;justify-content:center;font-family:"ISerif",serif;font-weight:400;line-height:1;
 color:#fff;white-space:nowrap;}
.dw{position:relative;display:inline-block;}
.dfl{position:absolute;left:-0.04em;right:-0.04em;top:0.34em;bottom:0.12em;opacity:0;background:#fff;
 box-shadow:0 0 16px rgba(255,255,255,0.9),0 0 44px rgba(255,255,255,0.45);}
.dwt{position:relative;display:inline-block;opacity:0;}
.isnt{display:flex;align-items:baseline;gap:0.11em;font-family:"LGothic",sans-serif;font-weight:400;line-height:1;color:#fff;
 white-space:nowrap;}
.isnt span{display:inline-block;transform-origin:50% 55%;}
.lock{position:absolute;display:flex;align-items:center;white-space:nowrap;pointer-events:none;}
.gt{font-family:"InterD",sans-serif;font-weight:700;letter-spacing:-0.035em;line-height:1;color:#fff;white-space:nowrap;
 text-shadow:0 0 14px rgba(255,255,255,0.55),0 0 40px rgba(255,255,255,0.28),0 0 90px rgba(255,255,255,0.12);}
.wht2{position:absolute;inset:0;background:#f4f4f0;opacity:0;}
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


def s_open():
    """0 to "you touch.": the wall of Finks, ON EARTH, the name mosaic, the red scene, the world, the hook."""
    sc = Scene("s_open", 0.0, B["touch"][1])
    L = lambda k: T[k] - 0.03
    # ---- "This is the most powerful man": the Nvidia reel's wall build with nine rooms of Fink; "powerful" and "man"
    # in the Dario serif on their words (the old cut's "powerful" / "people"); the wall ends on "IT ISN'T"'s lead-in
    a0, a1 = B["wall"]
    n = round((a1 - a0) * 60)
    sc.video("v9_wall.mp4", a0, a1, z=1)
    serif(sc, "powerful", L("powerful"), F(T["man"] + FR), 200, y=540, z=30)
    serif(sc, "man", F(T["man"] + FR), a0 + (n - 8) * FR, 200, y=540, z=30)   # (after the wall's first negative)
    # ---- "on Earth.": reel DdB8's "IT ISN'T" card, as before
    isnt_card(sc, B["earth"][0], B["earth"][1], "ON", "EARTH", T["earth"] + 0.02)
    # ---- "Larry Fink, the CEO of BlackRock.": the Hemant video's name mosaic (prep_v9 r_mosaic). The name in the
    # serif with its bloom over the middle, then the title in the grotesque, word by word; on "BlackRock" every tile
    # flips to BlackRock's own buildings
    b0, b1 = B["name"]
    sc.video("v9_mosaic.mp4", b0, b1, z=1)
    t_title = L("the2")
    dario_line(sc, [("Larry", L("larry"), 230, True), ("Fink", L("fink"), 230, True)], F(L("larry") - 2 * F25 - FR),
               F(t_title - FR), y=545, z=30, italic=False, gap=0.2)
    # ("BlackRock" is not written: the tower's own lit sign says it, in the middle of the frame)
    grot_line(sc, [("the", L("the2")), ("CEO", L("ceo")), ("of", L("of0"))], t_title, F(L("blackrock")), y=545, size=124)
    # ---- "The most evil": the red horned scene, as before (re-timed); then "company in the world." on the Earth at
    # night, "world" big in the serif (the Dario video's EARTH)
    sc.video("v6_evil.mp4", *B["evil"], z=1)
    c0, c1 = B["company"]
    sc.video("v9_earth.mp4", c0, c1, z=1)
    dim(sc, c0, c1, k=0.18)
    lockup(sc, [("company", c0, 96, False), ("in", L("in"), 96, False), ("the", L("the5"), 96, False)], c0, c1,
           960, 378, z=30)
    serif(sc, "world", L("world"), c1, 360, y=610, z=30)
    # ---- "A $15 trillion dollar": the headline flipbook, the figure on one spot (no caption: the pages say it)
    sc.video("v9_articles.mp4", *B["money"], z=1)
    # ---- "cartel of weaponized capital that owns a piece of everything": as the user approved it (Nov 23)
    sc.video("r_cartel4.mp4", *B["cartel"], z=1)
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
    ends = starts[1:] + [F(T["touch"] - 0.03)]          # "everything" until the fingers meet: the burst lands clean
    for p, a, b in zip(phrases, starts, ends):
        dario_line(sc, p, a, b, y=540, z=30)
    sc.video("r_touch3.mp4", *B["touch"], z=1)         # cut on "everything": the fingers meet on "touch"
    sc.write()
    return sc


# ---- "A company that's never made a single physical product,"
MADE_CSS = """
.card{position:absolute;overflow:hidden;border-radius:6px;}
.card video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.frame{position:absolute;border:2px solid rgba(255,255,255,0.92);border-radius:6px;box-shadow:0 0 22px rgba(255,255,255,0.4),inset 0 0 22px rgba(255,255,255,0.14);}
.wht{position:absolute;inset:0;background:#f6f6f4;opacity:0;}
"""


def s_made():
    """The Hemant / Dario lockup: a card in the middle with things being made (boards, a press, an assembly line),
    the words either side of it in the serif; on "product" the card flashes white and is gone -- an empty frame."""
    a0, a1 = B["made"]
    sc = Scene("s_made", a0, a1, css=MADE_CSS)
    L = lambda k: T[k] - 0.03
    X, Y, CW, CH = 610, 343, 700, 394
    t_out = F(L("product"))
    fid, cid, wid, vid = sc.uid("fr"), sc.uid("cd"), sc.uid("wh"), sc.uid("v")
    sc.div(t_out, a1, f'<div id="{fid}" class="frame" style="left:{X}px;top:{Y}px;width:{CW}px;height:{CH}px;"></div>', z=4)
    sc.add(f'<div id="{cid}" class="card" style="left:{X}px;top:{Y}px;width:{CW}px;height:{CH}px;z-index:5;">'
           f'<video id="{vid}" class="clip" src="assets/clips/v9_factory.mp4" {sc.timed(a0, t_out)} '
           f'data-media-start="0.0000" data-track-index="1" muted playsinline></video>'
           f'<div id="{wid}" class="wht"></div></div>')
    sc.js.append(f'tl.fromTo("#{cid}",{{scale:0.94}},{{scale:1,duration:0.32,ease:"power3.out"}},0);')
    sc.js.append(f'tl.set("#{wid}",{{opacity:1}},0);tl.set("#{wid}",{{opacity:0}},{r4(2 * FR)});')
    sc.js.append(f'tl.set("#{wid}",{{opacity:1}},{sc.at(t_out)});tl.set("#{wid}",{{opacity:0}},{sc.at(t_out + 2 * FR)});')
    SM, BG = 70, 124
    lockup(sc, [("A", L("a3"), SM, False), ("company", L("company2"), SM, False), ("that’s", L("thats"), SM, False)],
           a0, a1, 575, 478, align="right", z=30)
    lockup(sc, [("never", L("never"), BG, True), ("made", L("made"), BG, True)], F(L("never") - 2 * F25 - FR), a1,
           575, 590, align="right", z=30, gap=0.2)
    lockup(sc, [("a", L("a4"), SM, False), ("single", L("single"), SM, False), ("physical", L("physical"), SM, False)],
           F(L("a4") - 2 * F25 - FR), a1, 1345, 478, align="left", z=30)
    lockup(sc, [("product", L("product"), BG, True)], F(L("product") - 2 * F25 - FR), a1, 1345, 590, align="left", z=30)
    sc.write()
    return sc


# ---- "yet it's one of the top shareholders in almost every major US company."
SHARE_CSS = """
.lc{position:absolute;width:238px;height:150px;border-radius:9px;background:#0e0e0e;border:1px solid rgba(255,255,255,0.2);opacity:0;}
.lc img{position:absolute;left:83px;top:24px;width:72px;height:72px;}
.lc span{position:absolute;left:0;right:0;top:112px;text-align:center;font-family:"InterSB",sans-serif;font-size:19px;letter-spacing:0.1em;color:#a8a8a8;line-height:1;}
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


def s_share():
    """The Hemant video's cards (white cards popping in, then their pictures) with the companies' marks: "top
    shareholders" in the serif in the middle, and from "one of the" to "major US company" a card for one company after
    another fills the frame around it, slowly at first and faster and faster."""
    a0, a1 = B["share"]
    sc = Scene("s_share", a0, a1, css=SHARE_CSS)
    L = lambda k: T[k] - 0.03
    lockup(sc, [("top", L("top"), 104, False), ("shareholders", L("shareholders"), 214, True)],
           F(L("top") - 2 * F25 - FR), a1, 960, 545, z=30, gap=0.22)
    rows, cols = [100, 270, 810, 980], [180 + 260 * k for k in range(7)]
    t0, t1 = L("one"), L("company3")
    N = len(SHARE_ORDER)
    cards = []
    for j, slot in enumerate(SHARE_ORDER):
        slug, tick = LOGOS[slot]
        r, c = divmod(slot, 7)
        cid, wid = sc.uid("lc"), sc.uid("lw")
        cards.append(f'<div id="{cid}" class="lc" style="left:{cols[c] - 119}px;top:{rows[r] - 75}px;">'
                     f'<img src="assets/logos/{slug}.svg" alt="" /><span>{tick}</span><div id="{wid}" class="lw"></div></div>')
        t = t0 + (t1 - t0) * (j / (N - 1)) ** 0.62     # a card every ~19 frames at first, every 3 by "company"
        sc.js.append(f'tl.set("#{cid}",{{opacity:1}},{sc.at(t)});tl.set("#{wid}",{{opacity:0}},{sc.at(t + 2 * FR)});')
    sc.div(a0, a1, "".join(cards), z=6)
    sc.write()
    return sc


# ---- "It holds more of Nvidia than Jensen Huang, more of Microsoft than Bill Gates, and more of Apple than Steve
# Jobs ever did."
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
.lab{position:absolute;left:1040px;font-family:"InterSB",sans-serif;font-weight:600;font-size:46px;letter-spacing:-0.03em;color:#141414;line-height:1;white-space:nowrap;}
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
    """Think School's "Founders vs Blackrock" page as a motion graphic (the user: "the TV, MacBook and the bar ... a
    much better motion graphic"): the page's own grey; the product big on the left, rising in on the company's name;
    the founder switching on on its screen on his name (the Elon reel's old-TV device: Gates in green on the MS-DOS
    monitor, Jobs in black and white on the Macintosh; Jensen on a card over the graphics card); on the right two
    bars on one scale -- BlackRock's and the founder's -- their figures rolling up in the serif, and how many times
    more BlackRock holds landing after the founder's bar has stopped."""
    a0, a1 = B["stake"]
    sc = Scene("s_stake", a0, a1, bg=PAGE, css=STAKE_CSS)
    L = lambda k: T[k] - 0.03
    cuts_ = [a0, F(T["more2"] - TM.LEAD), F(T["and"] - TM.LEAD), a1]
    CX, CY = 505, 520
    # the fixed parts of the right column
    na, fa = sc.uid("na"), sc.uid("fa")
    static = (f'<div class="k" style="top:82px;">SHARE OF THE COMPANY</div>'
              f'<div class="lab" style="top:356px;">BlackRock</div>'
              f'<div id="{na}" class="num" style="top:300px;">0.00%</div>'
              f'<div class="trk" style="top:470px;"><div id="{fa}" class="fill" style="background:#141414;"></div></div>'
              f'<div class="trk" style="top:734px;"></div>'
              f'<div class="src">Source · Investopedia · Yahoo Finance</div>')
    sc.div(a0, a1, static, z=4)
    sc.js.append(f'tl.set("#{fa}",{{scaleX:0}},0);')
    prev = 0.0
    for k, fd in enumerate(FOUNDERS):
        s0, s1 = cuts_[k], cuts_[k + 1]
        t_co, t_f = L(fd["w_co"]), L(fd["w_f"])
        t_b = F(T[fd["w_l"]] + 0.20)                      # the multiple lands after the founder's bar has stopped
        pr = STAKE[fd["key"]]
        px, py = CX - pr["w"] // 2, CY - pr["h"] // 2
        # BlackRock's bar and figure: up from nothing on "holds more of", then moving to each company's figure
        t_a = L("holds") if k == 0 else s0
        d_a = 0.5 if k == 0 else 0.34
        sc.js.append(f'tl.to("#{fa}",{{scaleX:{fd["br"] / FULL:.4f},duration:{d_a},ease:"power3.out"}},{sc.at(t_a)});')
        count(sc, na, prev, fd["br"], t_a, d_a, f'{fd["br"]:.2f}%')
        prev = fd["br"]
        # the product, rising in on the company's name
        pw = sc.uid("pw")
        t_p = L("more1") if k == 0 else s0                # in on "more of", so the page is never half empty
        sc.add(f'<div id="{pw}" class="pw" style="left:{px}px;top:{py}px;width:{pr["w"]}px;height:{pr["h"]}px;z-index:3;">'
               f'<img id="{pw}-img" class="clip" src="assets/img/v9_{fd["key"]}.png" alt="" {sc.timed(t_p, s1)} data-track-index="2" /></div>')
        sc.js.append(f'tl.fromTo("#{pw}",{{y:34,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"power3.out"}},{sc.at(t_p)});')
        # the founder on its screen, switched on on his name
        sw, wh, vid = sc.uid("sw"), sc.uid("wh"), sc.uid("v")
        if "screen" in pr:
            sx, sy, ww, hh = pr["screen"]
            box, cls = f"left:{px + sx}px;top:{py + sy}px;width:{ww}px;height:{hh}px;border-radius:16px;", "scr"
        else:
            box, cls = "left:560px;top:92px;width:400px;height:300px;", "scr jcard"
        sc.add(f'<div id="{sw}" class="{cls}" style="{box}z-index:5;">'
               f'<video id="{vid}" class="clip" src="assets/clips/{fd["vid"]}" {sc.timed(t_f, s1)} data-media-start="0.0000" '
               f'data-track-index="1" muted playsinline></video><div id="{wh}" class="wht2"></div></div>')
        sc.js.append(f'tl.set("#{sw}",{{opacity:1}},{sc.at(t_f)});tl.set("#{sw}",{{opacity:0}},{sc.at(s1)});')
        sc.js.append(f'tl.set("#{wh}",{{opacity:1}},{sc.at(t_f)});tl.set("#{wh}",{{opacity:0}},{sc.at(t_f + 2 * FR)});')
        # the right column for this company: its name, the founder's label, figure and bar, and the multiple
        co, lb, nb, fb, bd = sc.uid("co"), sc.uid("lb"), sc.uid("nb"), sc.uid("fb"), sc.uid("bd")
        dyn = (f'<div id="{co}" class="co">{fd["co"]}</div>'
               f'<div id="{lb}" class="lab" style="top:620px;opacity:0;">{fd["who"]}</div>'
               f'<div id="{nb}" class="num" style="top:564px;opacity:0;color:{fd["color"]};">0.00%</div>'
               f'<div class="trk" style="top:734px;background:transparent;"><div id="{fb}" class="fill" style="background:{fd["color"]};"></div></div>'
               f'<div id="{bd}" class="bdg">{fd["mult"]}</div>')
        sc.div(s0, s1, dyn, z=5)
        sc.js.append(f'tl.set("#{fb}",{{scaleX:0}},0);')
        sc.js.append(f'tl.set("#{co}",{{opacity:1}},{sc.at(t_co)});')
        sc.js.append(f'tl.set("#{lb}",{{opacity:1}},{sc.at(t_f)});tl.set("#{nb}",{{opacity:1}},{sc.at(t_f)});')
        sc.js.append(f'tl.to("#{fb}",{{scaleX:{fd["fo"] / FULL:.4f},duration:0.4,ease:"power3.out"}},{sc.at(t_f)});')
        count(sc, nb, 0.0, fd["fo"], t_f, 0.4, fd["fo_s"])
        sc.js.append(f'tl.fromTo("#{bd}",{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.2,ease:"power2.out"}},{sc.at(t_b)});')
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
        y, cls = {"ink": (972, "jn ink"), "heavy": (540, "jn heavy"), "low": (705, "jn")}.get(kind, (540, "jn"))
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
    scenes = [s_open(), s_made(), s_share(), s_stake(), s_rogan(), s_rest2(), s_caps()]
    index(scenes)
    print("wrote", len(scenes), "scenes; total", TM.TOTAL)
