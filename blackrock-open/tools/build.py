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
    inner = (f'<div class="isnt" style="font-size:{size}px;"><span id="{i1}" style="transform:scale(1.25);">'
             f'{_html.escape(w1, quote=False)}</span><span id="{i2}" style="opacity:0;position:relative;">'
             f'{_html.escape(w2, quote=False)}{extra}</span></div>')
    sc.div(a, b, inner, z=z, cls="cap", style=f"top:{y}px;height:0;")
    sc.js.append(f'tl.set("#{i1}",{{scale:1}},{sc.at(a + 3 * FR)});')      # one reel frame large
    sc.js.append(f'tl.set("#{i2}",{{opacity:1}},{sc.at(t2)});')
    return i1, i2


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


# ------------------------------------------------------------------ s_hook: from "These" to "you touch"
def s_hook():
    sc = Scene("s_hook", B["tiles"][0], B["touch"][1])
    t0 = B["tiles"][0]
    n = round((B["tiles"][1] - t0) * 60)
    # the tiles end on "IT ISN'T"'s lead-in already (prep_v3 r_tiles3): the strobe, one reel frame negative, two cyan
    sc.video("r_tiles3.mp4", *B["tiles"], z=1)
    # "powerful" / "people": a different effect (the user, Nov 22) -- the Dario video's Instrument Serif with its white
    # glow, in on the word blurred and blooming, sharp four frames later
    for word, a, b in (("powerful", T["powerful"], T["people"]), ("people", T["people"], t0 + (n - 8) * FR)):
        serif(sc, word, a - 0.03, b, 200, y=540, z=30)
    # ON EARTH: reel DdB8's "IT ISN'T" -- the tiles go negative for a frame, cyan for two, then the user's red, ON
    # landing large for a frame in its place and EARTH joining on its word
    isnt_card(sc, B["earth"][0], B["earth"][1], "ON", "EARTH", T["earth"] + 0.02)
    # "a $60 trillion dollar cartel of weaponized capital that owns a piece of everything you touch." -- all of it
    # written, in the Porsche reel's italic ("$100 million loss.") with Dario's entrance: each word's glowing bar, then
    # the word (the big ones blown out, then crisp). The bright pages under it are brought down so the white reads.
    sc.video("r_articles.mp4", *B["money"], z=1)
    dim(sc, *B["money"], k=0.5)
    sc.video("r_cartel4.mp4", *B["cartel"], z=1)
    sc.video("r_weap.mp4", *B["weap"], z=1)
    dim(sc, *B["weap"], k=0.45)
    sc.video("v6_owns.mp4", *B["logos"], z=1)
    dim(sc, *B["logos"], k=0.5)
    L = lambda k: T[k] - 0.03
    SM, HE, BIG = 100, 175, 225
    phrases = [
        [("a", L("a"), SM, False), ("$60", L("sixty"), HE, True), ("trillion", L("trillion"), HE, True)],
        [("cartel", L("cartel"), BIG, True)],
        [("of", L("of1"), SM, False), ("weaponized", L("weapon"), HE, True), ("capital", L("capital"), HE, True)],
        [("that", L("that"), SM, False), ("owns", L("owns"), HE, True)],
        [("a", L("a2"), SM, False), ("piece", L("piece"), HE, True), ("of", L("of2"), SM, False)],
        [("everything", L("everything"), BIG, True)],
        [("you", L("you"), SM, False), ("touch.", L("touch"), HE, True)],
    ]
    starts = [F(p[0][1] - 2 * F25 - FR) for p in phrases]
    ends = starts[1:] + [B["touch"][1]]
    for k, (p, a, b) in enumerate(zip(phrases, starts, ends)):
        # "you touch." sits low, clear of the burst where the fingers meet
        dario_line(sc, p, a, b, y=860 if k == len(phrases) - 1 else 540, z=30)
    sc.video("r_touch3.mp4", *B["touch"], z=1)         # cut on "everything": the fingers meet on "touch"
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
    """"Amongst them is this guy": the spotlight reel (DeJRKmqTPdg) -- "Amongst them" in the captions' line (the user,
    Nov 22: like "a part-time DJ"), then the face flash, the room going dark and the punch-in on Fink, the small italic
    words under his face."""
    sc = Scene("s_search", B["orbit"][0], B["thisguy"][1])
    sc.video("r_orbit4.mp4", *B["orbit"], z=1)
    sc.video("r_spot4.mp4", *B["thisguy"], z=1)
    por_phrase(sc, [("is", T["is"] - 0.03), ("this", T["this"] - 0.03), ("guy", T["guy2"] - 0.03)],
               T["is"] - 0.03, B["thisguy"][1], size=78, y=745, spacing="0.3em")
    sc.write()
    return sc


# ------------------------------------------------------------------ s_fink: the man who runs ... BlackRock.
def s_fink():
    sc = Scene("s_fink", B["evil"][0], B["brand"][1])
    # "the man who runs the most evil": the reference's "terrible boss" scene (prep_v6 r_evil) -- red, Fink rising,
    # the horns, MOST / EVIL behind him (the user, Nov 22: the red part only)
    sc.video("v6_evil.mp4", *B["evil"], z=1)
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
    t15, t_in = TM.RT("15") - 0.03, TM.R(TM.ALIGN["rest"][TM.RW_IDX["trillion"] + 1]["start"]) - 0.03
    dario_line(sc, [("$15 trillion", t15, 220, True)], F(t15 - 2 * F25 - FR), F(t_in - FR), y=540, z=60, italic=False)
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
        y, cls = {"ink": (900, "jn ink"), "heavy": (540, "jn heavy")}.get(kind, (540, "jn"))
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
