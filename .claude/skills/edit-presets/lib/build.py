"""Trimmed from blackrock-open/tools/build.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import html as _html

import json

import subprocess

import os

import timing as TM

# edit-presets: where the code reads and writes. Default: this repo's BlackRock project. For a new edit set
# PRESET_ROOT (the HyperFrames project: assets/clips, assets/img, assets/fonts, compositions), PRESET_SRC (its
# source media, the old blackrock-src) and PRESET_REPO (the repo, for dimon-src).
REPO = os.environ.get("PRESET_REPO") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
ROOT = os.environ.get("PRESET_ROOT") or os.path.join(REPO, "blackrock-open")

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
@font-face{font-family:"HerosR";src:url("assets/fonts/TeXGyreHeros-Regular.otf") format("opentype");font-weight:400;font-style:normal;}
@font-face{font-family:"Bodoni";src:url("assets/fonts/BodoniModa-96-600.ttf") format("truetype");font-weight:600;font-style:normal;}
@font-face{font-family:"Michroma";src:url("assets/fonts/Michroma-latin.woff2") format("woff2");font-weight:400;font-style:normal;}
"""

# the Dario video's Instrument Serif glow (the user: "exactly like the Dario video ... with that white glow")
SERIF_REST = "0 0 14px rgba(255,255,255,0.62),0 0 42px rgba(255,255,255,0.30),0 0 90px rgba(255,255,255,0.12)"

SERIF_SOFT = "0 0 18px rgba(255,255,255,0.85),0 0 50px rgba(255,255,255,0.45),0 0 100px rgba(255,255,255,0.18)"

SERIF_BLOOM = "0 0 22px rgba(255,255,255,1),0 0 60px rgba(255,255,255,0.95),0 0 130px rgba(255,255,255,0.7)"

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

# ------------------------------------------------------------------ type devices
BIG_REST = "0 0 20px rgba(255,255,255,0.75),0 0 60px rgba(255,255,255,0.40),0 0 130px rgba(255,255,255,0.16)"

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

ISF_PATH = f"{ROOT}/assets/fonts/InstrumentSerif-Regular.woff2"

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
# the Chainsmokers' rise (reel DgHoW0vhPvb n30-n49 at 30 fps): the states' times after the cut, and the share of the
# rise (324 px = 0.30 of the frame) still to go
RISE = 324

RISE_T = [0.0, 0.1, 0.1667, 0.2333, 0.3333, 0.4, 0.4667, 0.5667, 0.6333]

RISE_R = [1.0, 0.6, 0.413, 0.273, 0.173, 0.097, 0.043, 0.01, 0.0]

STEP12 = 5                                  # frames per 12 fps state

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
    sc.video("v16_wall.mp4", a0, FINK_IN, z=1)          # (v16: its false colour shows the first state of the rise)
    kline(sc, [("This", F(T["this"] - 0.03)), ("is", F(T["is"] - 0.03)), ("the", F(T["the1"] - 0.03)),
               ("most", F(T["most1"] - 0.03))], F(T["this"] - 0.03), FINK_IN, 540, 150, K_HERO, z=30)
    t_e = F(T["earth"] - 0.03)
    ff, pa, pb, cut, line, wf = sc.uid("ff"), sc.uid("pa"), sc.uid("pb"), sc.uid("ct"), sc.uid("kl"), sc.uid("wf")
    spans, words = [], [("Powerful", FINK_IN), ("man", F(T["man"] - 0.03)), ("on", F(T["on"] - 0.03)), ("Earth", t_e)]  # (v17)
    for text, t in words:
        wid = sc.uid("fw")
        spans.append(f'<span id="{wid}" style="display:inline-block;opacity:0;margin:0 0.12em;">{text}</span>')
        kflash(sc, wid, t, K_HERO, blur=7)
    inner = (f'<img id="{pa}" class="clip pl" src="assets/img/v17_bg_wall.jpg" alt="" {sc.timed(FINK_IN, t_e)} '
             f'data-track-index="2" style="z-index:1;" />'
             f'<img id="{pb}" class="clip pl" src="assets/img/v17_bg_b.jpg" alt="" {sc.timed(t_e, a1)} '
             f'data-track-index="2" style="z-index:1;" />'
             f'<div id="{line}" data-layout-allow-overlap style="position:absolute;left:0;right:0;top:96px;display:flex;justify-content:center;'
             f'align-items:baseline;font-family:\'ISerif\',serif;font-size:170px;letter-spacing:-0.045em;line-height:1;'
             f'color:#f4efe6;white-space:nowrap;z-index:2;text-shadow:{K_HERO};">{"".join(spans)}</div>'
             f'<img id="{cut}" class="pl" src="assets/img/v10_fink_cut.png" alt="" style="z-index:3;transform-origin:1040px 879px;" />'
             f'<img id="{wf}" class="pl" src="assets/img/v15_fink_white.png" alt="" style="z-index:4;opacity:0;transform-origin:1040px 879px;" />')
    sc.add(f'<div id="{ff}" class="clip ff" {sc.timed(FINK_IN, a1)} data-track-index="3" style="z-index:5;">{inner}</div>')
    # v16 (the user: "how the Chainsmokers image came from the bottom ... at that speed ... the texture"): the reel's
    # 1.0-1.7 s measured frame by frame -- the duo rises 0.30 of the frame in 0.63 s on 12 fps states, easing out; the
    # wall behind them zoomed in and soft, settling 1.08 -> 1.04 -> 1.0 in two of those states; a screen-door mesh over
    # the frame. Then one subtle push.
    # v17 (the user: after coming up his picture "just becomes still ... makes the video less animated"; the reel's duo
    # are footage and never stop): the rise as the reel's, then he keeps moving -- on up slowly and a touch closer, on the
    # same 12 fps states -- and the wall behind settles (1.08 -> 1.04 -> 1.0, soft to sharp), then drifts gently the
    # other way; the subtle push over all of it. No texture over the frame any more (the user).
    span = a1 - FINK_IN
    t_rise = RISE_T[-1]

    def fink_state(u):
        if u < t_rise - 1e-6:
            k = max(i for i, tt in enumerate(RISE_T) if tt <= u + 1e-6)
            y = RISE * RISE_R[k]
        else:
            v = (u - t_rise) / (span - t_rise)
            y = -24 * (1 - (1 - v) ** 2)
        return y, 1.0 + 0.035 * (u / span)

    def bg_state(u):
        if u < 6 * FR - 1e-6:
            return 1.08, 9, 0.0
        if u < 14 * FR - 1e-6:
            return 1.04, 3, 0.0
        v = (u - 14 * FR) / (span - 14 * FR)
        return 1.0 + 0.03 * v, 0, 18 * v

    times = {F(FINK_IN + t) for t in RISE_T} | {F(FINK_IN + 6 * FR), F(FINK_IN + 14 * FR)}
    t = F(FINK_IN + t_rise)
    while t < a1 - 1e-6:
        times.add(t)
        t = F(t + STEP12 * FR)
    for tt in sorted(times):
        if tt >= a1:
            continue
        u = tt - FINK_IN
        y, s = fink_state(u)
        bs, bl, by = bg_state(u)
        sc.js.append(f'tl.set("#{cut}",{{y:{y:.1f},scale:{s:.4f}}},{sc.at(tt)});tl.set("#{wf}",{{y:{y:.1f},scale:{s:.4f}}},{sc.at(tt)});')
        sc.js.append(f'tl.set("#{pa}",{{scale:{bs:.4f},y:{by:.1f},filter:"blur({bl}px)"}},{sc.at(tt)});'
                     f'tl.set("#{pb}",{{scale:{bs:.4f},y:{by:.1f},filter:"blur({bl}px)"}},{sc.at(tt)});')
    t_up = F(FINK_IN + t_rise)
    sc.js.append(f'tl.fromTo("#{ff}",{{scale:1.0}},{{scale:1.03,duration:{r4(a1 - t_up)},ease:"none"}},{sc.at(t_up)});')
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
    sc.video("v16_touch.mp4", *B["touch"], z=1)       # (v16: at its own speed, on into the next shots)
    sc.write()
    return sc

RI = lambda i: TM.R(TM.ALIGN["rest"][i]["start"])        # a rest-recording word's film time, by its index

# ---- v16: "When the 2008 crisis hit, the U.S. government called the one guy"
def s_crisis():
    """"When the 2008": the Chainsmokers reel's date frame (28.17 s); "crisis hit,": reel DelkyjLP4p_'s grid (27.0 s);
    "the U.S. government called the one guy": the earlier shots with its datamosh at the cuts (prep_v16 date, grid,
    gov). The captions are s_caps'."""
    LV = lambda i: F(RI(i) - TM.LEAD)
    d0, g0, g1, v1 = LV(94), LV(97), LV(99), F(RI(106))
    sc = Scene("s_crisis", d0, v1)
    sc.video("v17_date.mp4", d0, g0, z=1)
    sc.video("v17_grid.mp4", g0, g1, z=1)
    sc.video("v16_gov.mp4", g1, v1, z=1)
    sc.write()
    return sc

def white_hit(sc, t, z=90, peak=0.82):
    """the Kalanick reel's flashes ("Following years of controversy", 22.3 / 22.9 s): one reel frame of the next shot
    blown out to white"""
    sc.div(t, F(t + REEL), "", z=z, cls="layer", style=f"background:#fff;opacity:{peak};")

MONEY_CSS = """
.mcap{position:absolute;left:0;right:0;top:905px;height:0;display:flex;justify-content:center;align-items:center;white-space:nowrap;
 font-family:"ISerif",serif;font-size:80px;letter-spacing:-0.035em;line-height:1;color:#222;}
.lbox{position:absolute;top:0;width:0;height:104px;margin-top:-52px;background:rgba(58,58,58,0.92);overflow:hidden;}
.lbox .lt{position:absolute;left:28px;top:0;height:104px;display:block;line-height:104px;font-family:"ISerif",serif;font-size:72px;
 letter-spacing:-0.035em;color:#fff;white-space:pre;}
.lbox .lt span{opacity:0;}
"""

def s_money():
    """"He came out of that crisis with 3x the money." (v16, the user: the Kalanick reel's money graphics): its 39.4-44 s
    on white (prep_v16 money) -- the small dark line at the bottom building word by word (its "He's betting billions"),
    then its grey label rising with the first stacks to the middle (its "And with $1.7 billion"); a flash into "Today,"."""
    LV = lambda i: F(RI(i) - TM.LEAD)
    h0, s0, e0 = LV(119), LV(125), F(RI(130))
    sc = Scene("s_money", h0, F(e0 + REEL), bg="transparent", css=MONEY_CSS)
    sc.video("v17_money.mp4", h0, e0, z=1)
    ws = [("He", LV(119)), ("came", LV(120)), ("out", LV(121)), ("of", LV(122)), ("that", LV(123)), ("crisis", LV(124))]
    for k in range(len(ws)):
        a = max(ws[k][1], h0)
        b = ws[k + 1][1] if k + 1 < len(ws) else s0
        if b - a < FR:
            continue
        sc.div(a, b, f'<div class="mcap">{" ".join(w for w, _ in ws[:k + 1])}</div>', z=30, cls="layer")
    # "with 3x the money" (v17, the user: bigger; the box should not come in whole first -- it grows with the words,
    # left to right): each word turns on at its onset and the box opens over it (0.2 s, eased), the line ending centred
    from PIL import ImageFont
    fnt = ImageFont.truetype(ISF_PATH, 72)
    trk = -0.035 * 72
    wlen = lambda txt: sum(fnt.getlength(ch) + trk for ch in txt)
    words = [("with", LV(125)), ("3x", LV(126)), ("the", LV(128)), ("money", LV(129))]
    pad = 28
    widths = [wlen(" ".join(w for w, _ in words[:k + 1])) + 2 * pad for k in range(len(words))]
    left = 960 - widths[-1] / 2
    bid = sc.uid("lb")
    spans = []
    for k, (w, t) in enumerate(words):
        sid = sc.uid("lw")
        spans.append(f'<span id="{sid}">{w}</span>' + (" " if k < len(words) - 1 else ""))
        sc.js.append(f'tl.set("#{sid}",{{opacity:1}},{sc.at(max(t, s0))});')
    sc.div(s0, e0, f'<div id="{bid}" class="lbox" style="left:{left:.1f}px;"><div class="lt">{"".join(spans)}</div></div>',
           z=30, cls="layer")
    t = s0
    while t < e0 - 1e-6:
        w = 0.0
        for k, (_, tw) in enumerate(words):
            u = min(1.0, max(0.0, (t - max(tw, s0)) / 0.2))
            w += ((widths[k] - (widths[k - 1] if k else 0.0)) * (1 - (1 - u) ** 3))
        sc.js.append(f'tl.set("#{bid}",{{width:{w:.1f}}},{sc.at(t)});')
        t = F(t + FR)
    for k, y in enumerate((1000, 905, 800, 700, 620, 575, 560)):
        sc.js.append(f'tl.set("#{bid}",{{y:{y}}},{sc.at(F(s0 + k * 5 * FR))});')
    white_hit(sc, e0)
    sc.write()
    return sc
