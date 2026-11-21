#!/usr/bin/env python3
"""Writes the HyperFrames project: index.html (scene hosts + the mix) and compositions/s_*.html.

Every time comes from tools/timing.py (60 fps grid). Scene times in the HTML are relative to the scene's start.
Run: python3 tools/build.py
"""
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
"""

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:#000;}
.full{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
.layer{position:absolute;inset:0;}
.cap{position:absolute;left:0;right:0;display:flex;justify-content:center;align-items:center;white-space:nowrap;pointer-events:none;}
.nv{font-family:"InterD",sans-serif;font-weight:800;letter-spacing:-0.02em;color:#fff;text-transform:uppercase;}
.hv{font-family:"Heros",sans-serif;font-weight:700;letter-spacing:-0.012em;color:#EEF0F0;text-transform:uppercase;line-height:1;white-space:nowrap;}
.flash{position:absolute;inset:0;background:#fff;opacity:0;}
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


# ------------------------------------------------------------------ s_quote: the panel line
def s_quote():
    sc = Scene("s_quote", *B["quote"])
    L = TM.LINE
    cut1, cut2 = L[8][1], L[14][1]                     # "with", "financial"
    sc.video("p_wide.mp4", 0.0, cut1, z=1)             # no zooms (the user)
    sc.video("p_over.mp4", cut1, cut2, z=1)
    # "of financial talent and skill as you've been able to put together here": four panelists talking (muted),
    # a white flash into each one
    cuts_ = [cut2, L[16][1], L[19][1], L[23][1], B["quote"][1]]
    for k, name in enumerate(["ob_fink", "ob_schw", "ob_dalio", "ob_motsepe"]):
        sc.video(f"v3_{name}.mp4", cuts_[k], cuts_[k + 1], z=1)
        sc.flash(cuts_[k], peak=1.0, up=2 * FR, down=0.16, z=30)
    sc.add('<div class="layer" style="z-index:20;background:linear-gradient(to bottom,rgba(0,0,0,0) 55%,rgba(0,0,0,0.55) 100%)"></div>')
    items = []
    for i0, i1 in [(0, 3), (3, 6), (6, 8), (8, 11), (11, 13), (13, 16), (16, 18), (18, 22), (22, 26)]:
        items.append((" ".join(w for w, _ in L[i0:i1]).replace("'", "’"), L[i0][1]))
    chunks(sc, items, B["quote"][1] - 2 * FR, blend=None)
    sc.write()
    return sc


# ------------------------------------------------------------------ s_hook: from "These" to the puppet
def s_hook():
    sc = Scene("s_hook", B["tiles"][0], B["puppet"][1])
    t0 = B["tiles"][0]
    n = round((B["tiles"][1] - t0) * 60)
    sc.video("r_tiles3.mp4", *B["tiles"], z=1)
    caption(sc, "These are the most", T["these"], T["powerful"], blend=None)
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
    # a $60 trillion dollar: the article flipbook (its "$60 trillion" is the text)
    sc.video("r_articles.mp4", *B["money"], z=1)
    sc.video("r_cartel3.mp4", *B["cartel"], z=1)     # the user's cartel video as it is: table flash, then the faces
    # weaponized capital: on its word, gone again, no bounce
    sc.video("r_weap.mp4", *B["weap"], z=1)
    cap = T["capital"]
    for word, a, b in (("WEAPONIZED", B["weap"][0], B["weap"][0] + 0.35), ("CAPITAL", cap, min(cap + 0.42, B["weap"][1] - 2 * FR))):
        sc.div(a, b, f'<div style="font-family:\'LGothic\',sans-serif;font-size:430px;line-height:1;color:#fff;letter-spacing:0.01em;">{word}</div>',
               z=30, cls="cap", style="top:545px;height:0;mix-blend-mode:difference;")
    # that owns a piece of everything you touch
    sc.video("r_logos.mp4", *B["logos"], z=1)
    chunks(sc, [("That owns", T["that"]), ("A piece of", T["piece"]), ("Everything", T["everything"])], B["logos"][1])
    sc.video("r_touch3.mp4", *B["touch"], z=1)
    caption(sc, "Everything", B["touch"][0], T["you"], blend=None)
    chunks(sc, [("You", T["you"]), ("You touch.", T["touch"])], B["touch"][1] - 2 * FR, blend=None)
    sc.video("v3_puppet.mp4", *B["puppet"], z=1)        # the explainer's puppet, then "That's Jamie Dimon"
    sc.write()
    return sc


# ------------------------------------------------------------------ plain cuts
def cuts(sc, shots, z=1):
    for src, a, b in shots:
        sc.video(src, a, b, z=z)


def split(a, b, n):
    return [(F(a + (b - a) * k / n), F(a + (b - a) * (k + 1) / n)) for k in range(n)]


# ------------------------------------------------------------------ the intros (pre-rendered from the references)
def s_dimon():
    sc = Scene("s_dimon", B["dimon"][0], B["jpm"][1])
    sc.video("r_dimon3.mp4", *B["dimon"], z=1)         # the reference edit's "if intelligence is automated"
    sc.video("r_jpm.mp4", *B["jpm"], z=1)              # the reel's "the man behind OpenAI"
    sc.write()
    return sc


def s_solomon():
    sc = Scene("s_solomon", B["solomon"][0], B["ceo"][1])
    sc.video("r_solomon3.mp4", *B["solomon"], z=1)     # the reference edit's "AI"
    a, b = B["dj"]
    m = F((a + b) / 2)
    sc.video("v3_dj_a.mp4", a, m, z=1)
    sc.video("v3_dj_b.mp4", m, b, z=1)
    sc.video("r_ceo.mp4", *B["ceo"], z=1)              # the reel's OpenAI device, with the Goldman Sachs video
    sc.write()
    return sc


def s_search():
    sc = Scene("s_search", B["orbit"][0], B["thisguy"][1])
    sc.video("r_orbit3.mp4", *B["orbit"], z=1)          # the table circling, people lighting up at random
    sc.video("r_spot.mp4", *B["thisguy"], z=1)          # "is this guy": the spotlight reel's 3rd second on Fink
    caption(sc, "Amongst them", T["amongst"], T["is"], blend=None, shadow=True)
    caption(sc, "Is this guy", T["is"], B["thisguy"][1] - 2 * FR, blend=None, shadow=True)
    sc.write()
    return sc


# ------------------------------------------------------------------ s_fink: the man who runs ... BlackRock.
BOX_FACE = (1332, 396)   # Fink's face centre in v2_fink_box (Haar, mean over the shot; it moves < 2 px a step)
BOX = 400                # the square, a little wider than his face (345 px)
# the VC reel's box: cut in at 88.5 % of its size, then held 2 frames at 25 fps per step (12.5 steps a second)
BOX_STEPS = [(0.0, 0.885, 0.40), (0.08, 0.945, 0.43), (0.16, 0.980, 0.46), (0.24, 0.995, 0.475), (0.32, 1.0, 0.48)]


def s_fink():
    sc = Scene("s_fink", B["walk"][0], B["brand"][1])
    sc.video("v2_fink_stage.mp4", *B["walk"], z=1)
    sc.video("v2_fink_box.mp4", *B["box"], z=1)
    caption(sc, "The man who runs", T["the3"], T["most"], blend=None, shadow=True)
    # the red square: appears on "most" while the shot plays (not on the cut), settles in steps, stays put
    rb = sc.uid("rb")
    bx, by = BOX_FACE[0] - BOX // 2, BOX_FACE[1] - BOX // 2 - 10
    hs = "".join(f'<div style="position:absolute;left:{x - 7}px;top:{y - 7}px;width:14px;height:14px;background:#0b0b0b;"></div>'
                 for x, y in ((0, 0), (BOX, 0), (0, BOX), (BOX, BOX)))
    w1, w2, fill = sc.uid("t"), sc.uid("t"), sc.uid("f")
    box = (f'<div id="{rb}" style="position:absolute;left:{bx}px;top:{by}px;width:{BOX}px;height:{BOX}px;'
           f'transform-origin:50% 50%;">'
           f'<div id="{fill}" style="position:absolute;inset:0;background:rgba(222,30,44,{BOX_STEPS[0][2]});'
           f'border:2px solid rgba(36,6,8,0.9);"></div>' + hs +
           f'<div style="position:absolute;left:0;right:0;top:22px;display:flex;justify-content:center;gap:0.24em;'
           f'font-family:\'ISerif\',serif;font-size:50px;line-height:1;color:#fff;letter-spacing:0.005em;">'
           f'<span id="{w1}">most</span><span id="{w2}" style="opacity:0">evil</span></div></div>')
    sc.div(T["most"], B["box"][1], box, z=12, did=f"{rb}w")
    sc.js.append(f'tl.set("#{rb}",{{scale:{BOX_STEPS[0][1]}}},0);')
    for dt, k, al in BOX_STEPS[1:]:
        sc.js.append(f'tl.set("#{rb}",{{scale:{k}}},{sc.at(T["most"] + dt)});')
        sc.js.append(f'tl.set("#{fill}",{{backgroundColor:"rgba(222,30,44,{al})"}},{sc.at(T["most"] + dt)});')
    sc.js.append(f'tl.set("#{w2}",{{opacity:1}},{sc.at(T["evil"])});')
    # company in the world: BlackRock itself, in plain cuts; "BlackRock.": its letters
    # the source edit cuts every 16 frames, so the letters and the flags get their whole shots (0.45 s, 0.5 s)
    c0, c1 = B["company"]
    k1, k2 = F(c0 + 0.45), F(c0 + 0.95)
    cuts(sc, [("v2_br_letters.mp4", c0, k1), ("v2_br_bldg.mp4", k1, k2), ("v2_br_doors.mp4", k2, c1),
              ("v2_br_sign.mp4", *B["brand"])])
    caption(sc, "Company in the world", T["company"], B["company"][1], blend=None, shadow=True)
    caption(sc, "BlackRock.", T["blackrock"], B["brand"][1] - 2 * FR, blend=None, shadow=True)
    sc.write()
    return sc


# ------------------------------------------------------------------ the rest of the script
import shotlist as SL

CARD_RED = "url(assets/img/red_bg_user.jpg) center/cover"


def rest_time(x):
    return TM.RT(x) if isinstance(x, str) else F((TM.REST1_AT if x < TM.REST_SPLIT else TM.REST2_AT) + x)


def rest_part(sc, shots, part, caps):
    a0, a1 = B[part]
    starts = [a0 if k in ("rest1", "rest2") else TM.RT(k) for k, *_ in shots]
    for (key, name, src, t0, extra, fc), a, b in zip(shots, starts, starts[1:] + [a1]):
        if src == "card":
            color, word = extra
            bg = CARD_RED if color == "red" else color
            inner = (f'<div style="position:absolute;inset:0;background:{bg};"></div>'
                     f'<div class="cap" style="top:540px;height:0;"><div style="font-family:\'LGothic\',sans-serif;'
                     f'font-size:300px;line-height:1;color:#fff;letter-spacing:0.01em;">{word}</div></div>')
            sc.div(a, b, inner, z=1)
            if name == "card_jobs":                    # "ever did." under the name
                sc.div(TM.RT("ever"), b, '<div style="font-family:\'LGothic\',sans-serif;font-size:120px;line-height:1;color:#fff;">EVER DID.</div>',
                       z=2, cls="cap", style="top:800px;height:0;")
        elif src == "clip":
            sc.video(f"{name}.mp4", a, b, z=1)
        else:
            sc.video(f"v3_{name}.mp4", a, b, z=1)
    for key, text, until in SL.HERO:
        t = TM.RT(key)
        if a0 <= t < a1:
            sc.div(t, TM.RT(until) - 2 * FR, f'<div style="font-family:\'LGothic\',sans-serif;font-size:300px;line-height:1;color:#fff;'
                   f'letter-spacing:0.01em;text-shadow:0 0 40px rgba(0,0,0,0.45),0 0 12px rgba(0,0,0,0.35);">{text}</div>',
                   z=30, cls="cap", style="top:520px;height:0;")
    for i, (text, t, *opt) in enumerate(caps):
        if text is None:
            continue
        a = rest_time(t)
        b = rest_time(caps[i + 1][1]) if i + 1 < len(caps) else a1 - 2 * FR
        ink = "ink" in opt                             # dark, over Think School's light grey page
        heavy = TM.RT("a2") <= a < TM.RT("has")        # over the user's ending video
        caption(sc, text, a, min(b, a1 - 2 * FR), blend=None, shadow=("heavy" if heavy else not ink),
                color="#151515" if ink else None)


def s_rest1():
    sc = Scene("s_rest1", *B["rest1"])
    rest_part(sc, SL.REST1, "rest1", SL.CAPS1)
    sc.write()
    return sc


def s_rest2():
    sc = Scene("s_rest2", *B["rest2"])
    rest_part(sc, SL.REST2, "rest2", SL.CAPS2)
    sc.write()
    return sc


# ------------------------------------------------------------------ s_rogan: Elon's question, after "...than Steve Jobs ever did.", and a 1 s pause
ROGAN_CAPS = [("Do you think", 0.00), ("BlackRock’s", 0.67), ("a bad company?", 1.41)]   # s from his first word


def s_rogan():
    a, b = B["rogan"][0], B["pause"][1]
    sc = Scene("s_rogan", a, b)
    sc.video("rogan2.mp4", a, b, z=1)                  # its burned-in subtitle removed; held 1 s after the question
    items = [(text, F(a + dt)) for text, dt in ROGAN_CAPS]
    chunks(sc, items, b - 2 * FR, blend=None, shadow=True)
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
    scenes = [s_quote(), s_hook(), s_dimon(), s_solomon(), s_search(), s_fink(), s_rest1(), s_rogan(), s_rest2()]
    index(scenes)
    print("wrote", len(scenes), "scenes; total", TM.TOTAL)
