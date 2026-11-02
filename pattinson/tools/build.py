#!/usr/bin/env python3
"""Generate the HyperFrames compositions for the Pattinson edit (v2) from one shot/caption table.

v2 follows the reference's grammar closely (see ../reference/f1-horner-reel-breakdown.md):
mostly full-frame footage under white glow captions at the reference's sizes, about one cut
per second, paper only for punchlines and card collages, and the reference's motion kit:
inversion flashes, whip pans, exposure blowouts, snap zooms, RGB-split frames, rolling
counters, photo-to-card shrink and zoom-through, photo strobe, tile grid, text behind the
subject, a CRT glitch with a symbol and the 1-2-3 triptych.

Writes pattinson/index.html, compositions/s01..s13.html, compositions/captions.html,
compositions/grain.html and leak copies. Every timed element is plain HTML with its own id,
data-start and data-duration (seconds local to its file), so Studio can edit the output.
All times below are GLOBAL seconds; each scene converts them to local time.
"""
import html, json, os, re, shutil

ROOT = "/home/user/claude-test-2.0"
PRJ = f"{ROOT}/pattinson"
COMP = f"{PRJ}/compositions"
DUR = 74.0
LEAD = 0.07  # captions and cuts arrive 2 frames before the word

GR = json.load(open(f"{PRJ}/tools/gradings.json"))
WORDS = json.load(open(f"{PRJ}/tools/words_global.json"))


def _derive(base, adjust=None, effects=None, details=None):
    g = json.loads(GR[base])
    g["adjust"].update(adjust or {})
    g["effects"].update(effects or {})
    g["details"].update(details or {})
    return json.dumps(g, separators=(",", ":"))


# one-off looks derived from the validated base payloads (values inside the documented ranges)
GR["rgbsplit"] = _derive("matte", adjust={"exposure": 0.9, "contrast": -0.22, "saturation": -0.35},
                         effects={"chromaticAberration": 0.75, "chromaticAngle": 0.0})
GR["crt"] = _derive("glitch", effects={"digitalGlitch": 0.95, "digitalGlitchBlockAmount": 0.8,
                                       "digitalGlitchColorSplit": 0.8, "scanlines": 0.75, "tapeNoise": 1.0,
                                       "tapeDamage": 1.0, "crtCurvature": 0.4})


def T(i):
    """Appear time (global) for word index i: two frames before it is spoken."""
    return round(WORDS[i]["g_start"] - LEAD, 3)


def esc(s):
    return html.escape(s, quote=True)


def r3(x):
    return f"{x:.3f}".rstrip("0").rstrip(".") if "." in f"{x:.3f}" else f"{x}"


FONTS_CSS = """
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Regular.woff2') format('woff2'); font-weight: 400; font-style: normal; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Italic.woff2') format('woff2'); font-weight: 400; font-style: italic; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-600.woff2') format('woff2'); font-weight: 600; font-style: normal; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-700.woff2') format('woff2'); font-weight: 700; font-style: normal; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-800.woff2') format('woff2'); font-weight: 800; font-style: normal; }
"""

GLOW_REST = "0 0 12px rgba(255,255,255,0.55), 0 0 34px rgba(255,255,255,0.22), 0 3px 10px rgba(0,0,0,0.42)"
GLOW_BLOOM = "0 0 34px rgba(255,255,255,0.95), 0 0 90px rgba(255,255,255,0.55), 0 3px 10px rgba(0,0,0,0)"

# --------------------------------------------------------------------------------------------
# Scene builder
# --------------------------------------------------------------------------------------------


class Scene:
    def __init__(self, sid, start, end, ground="#0b0b0b"):
        self.sid, self.start, self.end = sid, start, end
        self.ground = ground
        self.els, self.js = [], []
        self.n, self.z = 0, 1
        self.uses_text = False

    @property
    def dur(self):
        return round(self.end - self.start, 3)

    def L(self, t):
        return round(t - self.start, 3)

    def at(self, t):
        return r3(self.L(t))

    def uid(self, p):
        self.n += 1
        return f"{self.sid}-{p}{self.n}"

    def nz(self):
        self.z += 1
        return self.z

    def timed(self, t0, t1):
        t0 = max(t0, self.start)
        t1 = min(t1, self.end)
        return f'data-start="{r3(self.L(t0))}" data-duration="{r3(round(t1 - t0, 3))}"'

    # ---- media -----------------------------------------------------------------------------
    def video(self, src, t0, t1, ms=0.0, rate=None, grade="matte", push=(1.0, 1.05), box=None,
              pushease="none", style="", vars_style="", z=None, cam_extra=""):
        cam, vid = self.uid("cam"), self.uid("v")
        z = z or self.nz()
        grading = f' data-color-grading="{esc(GR[grade])}"' if grade else ""
        rate_attr = f' data-playback-rate="{rate}"' if rate else ""
        if box:  # x, y, w, h
            x, y, w, h = box
            vstyle = f"position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:cover;{vars_style}"
            camstyle = f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{cam_extra}"
        else:
            vstyle = f"position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;{vars_style}"
            camstyle = f"position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{z};{cam_extra}"
        self.els.append(
            f'<div class="cam" id="{cam}" style="{camstyle}">'
            f'<video id="{vid}" class="clip" src="assets/clips/{src}" muted playsinline '
            f'{self.timed(t0, t1)} data-hf-media-start-basis="local" data-media-start="{r3(ms)}"{rate_attr}{grading} '
            f'data-track-index="2" style="{vstyle}{style}"></video></div>')
        if push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, '
                           f'duration: {r3(round(t1 - t0, 3))}, ease: "{pushease}" }}, {self.at(t0)});')
        return cam, vid

    def image(self, src, t0, t1, grade="matte", push=(1.0, 1.05), box=None, fit="cover",
              vars_style="", z=None, pos="center", card=False, rot=0.0, drop=False):
        cam, im = self.uid("cam"), self.uid("i")
        z = z or self.nz()
        grading = f' data-color-grading="{esc(GR[grade])}"' if grade else ""
        if box:
            x, y, w, h = box
            camstyle = f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};"
            istyle = (f"position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:{fit};"
                      f"object-position:{pos};{vars_style}")
        else:
            camstyle = f"position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{z};"
            istyle = (f"position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:{fit};"
                      f"object-position:{pos};{vars_style}")
        cls = "clip card" if card else "clip"
        self.els.append(
            f'<div class="cam" id="{cam}" style="{camstyle}">'
            f'<img id="{im}" class="{cls}" src="assets/img/{src}" alt="" {self.timed(t0, t1)}'
            f'{grading} data-track-index="3" style="{istyle}" /></div>')
        d = round(t1 - t0, 3)
        if drop:
            self.js.append(
                f'tl.fromTo("#{cam}", {{ scale: 1.24, y: -34, rotation: {rot - 3}, opacity: 0 }}, '
                f'{{ scale: 1, y: 0, rotation: {rot}, opacity: 1, duration: 0.26, ease: "expo.out" }}, {self.at(t0)});')
            if push and d > 0.3:
                self.js.append(f'tl.to("#{cam}", {{ scale: {push[1] - 0.01}, duration: {r3(d - 0.26)}, ease: "none" }}, '
                               f'{self.at(t0 + 0.26)});')
        elif push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]}, rotation: {rot} }}, {{ scale: {push[1]}, rotation: {rot}, '
                           f'duration: {r3(d)}, ease: "none" }}, {self.at(t0)});')
        return cam, im

    def paper(self, t0, t1):
        pid = self.uid("paper")
        self.els.append(f'<img id="{pid}" class="clip paper" src="assets/tex/paper.png" alt="" '
                        f'{self.timed(t0, t1)} data-track-index="1" style="z-index:{self.nz()}" />')

    def solid(self, t0, t1, color="#000"):
        sid = self.uid("solid")
        self.els.append(f'<div id="{sid}" class="clip solid" {self.timed(t0, t1)} data-track-index="4" '
                        f'style="background:{color};z-index:{self.nz()}"></div>')

    def neg(self, t, frames=2):
        nid = self.uid("neg")
        self.els.append(f'<div id="{nid}" class="clip neg" {self.timed(t, t + frames / 30)} data-track-index="5" '
                        f'style="z-index:{self.nz()}"></div>')

    def whiteflash(self, t, d=0.2, peak=0.95):
        fid = self.uid("wf")
        self.els.append(f'<div id="{fid}" class="clip flashw" {self.timed(t - 0.06, t + d)} data-track-index="5" '
                        f'style="z-index:{self.nz()}"></div>')
        self.js.append(f'tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: {peak}, duration: 0.06, ease: "power4.in" }}, {self.at(t - 0.06)});')
        self.js.append(f'tl.to("#{fid}", {{ opacity: 0, duration: {r3(d - 0.01)}, ease: "power2.out" }}, {self.at(t)});')

    def silhouette(self, src, t, frames=2):
        sid = self.uid("sil")
        self.els.append(f'<img id="{sid}" class="clip" src="assets/img/{src}" alt="" {self.timed(t, t + frames / 30)} '
                        f'data-track-index="5" style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
                        f'object-fit:cover;z-index:{self.nz()}" />')

    def rgbsplit(self, src, t, ms=0.0, frames=2, pos="center"):
        """1-2 bleached frames with channel separation laid over the incoming shot (reference 6.63 s)."""
        if src.endswith(".jpg") or src.endswith(".png"):
            return self.image(src, t, t + frames / 30, grade="rgbsplit", push=None, pos=pos)
        return self.video(src, t, t + frames / 30, ms=ms, grade="rgbsplit", push=None)

    # ---- transitions -----------------------------------------------------------------------
    def whip_in(self, cam, vid, t, dx=1, dist=340, d=0.2):
        """Whip-pan arrival: the shot slides in fast while its blur clears (needs blur var inline)."""
        self.js.append(f'tl.fromTo("#{cam}", {{ x: {dist * dx} }}, {{ x: 0, duration: {d}, ease: "power3.out" }}, {self.at(t)});')
        self.js.append(f'tl.to("#{vid}", {{ "--hf-color-grading-blur": 0, duration: {r3(d + 0.06)}, ease: "power2.out" }}, {self.at(t)});')

    def blow_in(self, vid, t, d=0.32):
        """Exposure blowout settling back to normal (needs exposure var inline)."""
        self.js.append(f'tl.to("#{vid}", {{ "--hf-color-grading-exposure": 0, duration: {d}, ease: "power2.out" }}, {self.at(t)});')

    def blow_out(self, vid, t, d=0.18, peak=1.7):
        """Outgoing shot burns to white just before the cut (needs exposure var 0 inline)."""
        self.js.append(f'tl.to("#{vid}", {{ "--hf-color-grading-exposure": {peak}, duration: {d}, ease: "power3.in" }}, {self.at(t - d)});')

    def scale_keys(self, cam, keys):
        """Sequential scale tweens on one camera: keys = [(t, from, to, dur, ease), ...]."""
        for k, (t, a, b, d, e) in enumerate(keys):
            ir = "" if k == 0 else ", immediateRender: false"
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {a} }}, {{ scale: {b}, duration: {r3(d)}, ease: "{e}"{ir} }}, {self.at(t)});')

    def numeral(self, ch, t0, t1, x=960, y=540, size=560, z=None):
        self.uses_text = True
        wid, nid = self.uid("numw"), self.uid("num")
        z = z or self.nz()
        self.els.append(
            f'<div id="{wid}" class="clip numwrap" {self.timed(t0, t1)} data-track-index="6" '
            f'style="z-index:{z};left:{x - 400}px;top:{y - 400}px;width:800px;height:800px">'
            f'<span id="{nid}" class="num" style="font-size:{size}px">{ch}</span></div>')
        self.js.append(f'tl.fromTo("#{nid}", {{ opacity: 0, scale: 1.12, filter: "blur(18px)" }}, '
                       f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }}, {self.at(t0)});')

    def text(self, txt, t0, t1, x, y, size, family="Inter Tight", weight=800, color="#F7F4F7",
             glow=True, align="center", style="", anim="glow", z=None, italic=False):
        """A free graphic text element (counters, lockups that live inside a scene)."""
        self.uses_text = True
        wid, sid = self.uid("txw"), self.uid("tx")
        z = z or self.nz()
        shadow = f"text-shadow:{GLOW_REST};" if glow else ""
        fs = "italic" if italic else "normal"
        if align == "center":
            box, acls = f"left:{x - 900}px;width:1800px;text-align:center;", ""
        elif align == "left":
            box, acls = f"left:{x}px;width:1600px;text-align:left;", " al"
        else:
            box, acls = f"left:{x - 1600}px;width:1600px;text-align:right;", " ar"
        self.els.append(
            f'<div id="{wid}" class="clip txw{acls}" {self.timed(t0, t1)} data-track-index="6" '
            f'style="z-index:{z};top:{y - size}px;height:{int(size * 1.6)}px;{box}">'
            f'<span id="{sid}" class="tx" style="font-family:\'{family}\';font-weight:{weight};font-style:{fs};'
            f'font-size:{size}px;color:{color};{shadow}{style}">{esc(txt)}</span></div>')
        if anim == "glow":
            self.js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.1, filter: "blur(14px)" }}, '
                           f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {self.at(t0)});')
        elif anim == "ink":
            self.js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.14 }}, {{ opacity: 1, scale: 1, duration: 0.4, '
                           f'ease: "expo.out" }}, {self.at(t0)});')
            self.js.append(f'tl.set("#{sid}", {{ opacity: 1 }}, {self.at(t0)});')
        return sid

    def counter(self, steps, t_end, x, y, size, family="Inter Tight", weight=800, color="#F7F4F7",
                glow=True, align="center", italic=False, ink=False, tick=0.2):
        """Rolling counter: steps = [(value, t), ...]; each value is its own timed element."""
        for k, (val, t) in enumerate(steps):
            t_next = steps[k + 1][1] if k < len(steps) - 1 else t_end
            anim = ("ink" if ink else "glow") if k == 0 else "none"
            self.text(val, t, t_next, x, y, size, family=family, weight=weight, color=color, glow=glow,
                      align=align, anim=anim, italic=italic)
            sfx("key-press.mp3", t, tick)

    def grid(self, imgs, cols, rows, t0, t1, gap=6, z=None, push=(1.0, 1.04)):
        gid, cam = self.uid("grid"), self.uid("cam")
        z = z or self.nz()
        cw, ch = 1920 / cols, 1080 / rows
        cells = "".join(
            f'<img id="{gid}-c{k}" class="clip" src="assets/img/{im}" alt="" {self.timed(t0, t1)} data-track-index="3" '
            f'style="position:absolute;left:{c * cw + gap / 2:.1f}px;'
            f'top:{r * ch + gap / 2:.1f}px;width:{cw - gap:.1f}px;height:{ch - gap:.1f}px;object-fit:cover" />'
            for k, im in enumerate(imgs[: cols * rows]) for r, c in [divmod(k, cols)])
        self.els.append(f'<div class="cam" id="{cam}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{z}">'
                        f'<div id="{gid}" class="clip gridbox" {self.timed(t0, t1)} data-track-index="3">{cells}</div></div>')
        if push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.12 }}, {{ scale: {push[1]}, duration: {r3(round(t1 - t0, 3))}, '
                           f'ease: "expo.out" }}, {self.at(t0)});')

    def raw(self, el):
        self.els.append(el)

    def write(self):
        css = f"""
  {FONTS_CSS if self.uses_text else ''}
  #root {{ position: absolute; inset: 0; overflow: hidden; background: {self.ground}; }}
  #root .cam {{ position: absolute; transform-origin: 50% 50%; }}
  #root .paper {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; }}
  #root .solid {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .neg {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #ffffff; mix-blend-mode: difference; }}
  #root .flashw {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #ffffff; opacity: 0; }}
  #root .card {{ box-sizing: border-box; border: 9px solid #F4EFEB; box-shadow: 0 22px 48px rgba(0,0,0,0.30), 0 3px 8px rgba(0,0,0,0.18); }}
  #root .numwrap {{ position: absolute; display: flex; align-items: center; justify-content: center; }}
  #root .num {{ font-family: 'Instrument Serif'; font-weight: 400; line-height: 1; display: inline-block;
    background: linear-gradient(180deg, #F7F4F7 38%, rgba(247,244,247,0.0) 92%); -webkit-background-clip: text;
    background-clip: text; color: transparent; letter-spacing: -0.02em; }}
  #root .txw {{ position: absolute; display: flex; align-items: center; justify-content: center; }}
  #root .txw.al {{ justify-content: flex-start; }}
  #root .txw.ar {{ justify-content: flex-end; }}
  #root .tx {{ display: inline-block; white-space: nowrap; line-height: 1; letter-spacing: -0.03em; }}
  #root .gridbox {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #0b0b0b; }}
  #root .rule {{ position: absolute; height: 6px; background: #0B0B0B; transform-origin: 50% 50%; }}
  #root .rec {{ position: absolute; display: flex; align-items: center; gap: 22px; font-family: 'Inter Tight'; font-weight: 800;
    font-size: 64px; letter-spacing: 0.04em; color: #FF2A3D; text-shadow: 0 0 18px rgba(255,42,61,0.8); }}
  #root .rec i {{ display: block; width: 46px; height: 46px; border-radius: 50%; background: #FF2A3D; box-shadow: 0 0 24px rgba(255,42,61,0.9); }}
"""
        body = "\n    ".join(self.els)
        js = "\n    ".join(self.js)
        out = f"""<template>
  <style>{css}  </style>
  <div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080">
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(self.dur)} }}, 0);
    {js}
    window.__timelines["{self.sid}"] = tl;
  </script>
</template>
"""
        open(f"{COMP}/{self.sid}.html", "w").write(out)


# --------------------------------------------------------------------------------------------
# Captions (one composition, global times)
# Sizes follow the reference measured at 1080p: everyday words about 100-115 px, emphasis
# words 200-300 px, black paper words about 100 px with a bigger punch word.
# --------------------------------------------------------------------------------------------
STY = {
    # key: (family, weight, italic, size, color, glow)
    "S": ("Inter Tight", 700, False, 100, "#F7F4F7", True),
    "M": ("Inter Tight", 800, False, 132, "#F7F4F7", True),
    "B": ("Instrument Serif", 400, False, 210, "#F7F4F7", True),
    "BI": ("Instrument Serif", 400, True, 210, "#F7F4F7", True),
    "XL": ("Instrument Serif", 400, False, 290, "#F7F4F7", True),
    "XLI": ("Instrument Serif", 400, True, 290, "#F7F4F7", True),
    "PS": ("Inter Tight", 700, False, 100, "#0B0B0B", False),
    "PM": ("Instrument Serif", 400, True, 160, "#0B0B0B", False),
    "PB": ("Instrument Serif", 400, True, 200, "#0B0B0B", False),
    "PXL": ("Instrument Serif", 400, True, 250, "#0B0B0B", False),
    "R": ("Inter Tight", 600, False, 46, "#F7F4F7", True),
    "SH": ("Archivo Black", 400, False, 150, "#1C59F7", False),
    "Y": ("Inter Tight", 700, False, 56, "#F7F4F7", True),
    "C": ("Inter Tight", 800, False, 96, "#F7F4F7", True),  # cold-open cover words
    "CB": ("Instrument Serif", 400, True, 230, "#F7F4F7", True),
}

CAPS = []  # list of dicts


def cap(lines, end, x=960, y=540, align="center", kind=None, start=None, exit=None, lh=0.92):
    """lines: list of lists of (text, time, style). time = global appear time."""
    first = min(tok[1] for line in lines for tok in line)
    CAPS.append(dict(lines=lines, start=start if start is not None else first, end=end, x=x, y=y,
                     align=align, kind=kind, exit=exit, lh=lh))


def W(i, style, text=None):
    return (text if text is not None else WORDS[i]["text"], T(i), style)


def paper_words(items, end, y=540, last_exit=None):
    """Black words on paper, one at a time, each replacing the last (reference paper beats)."""
    for k, (i, st, txt) in enumerate(items):
        t_next = T(items[k + 1][0]) if k < len(items) - 1 else end
        cap([[W(i, st, txt)]], t_next, y=y, kind="paper", exit=last_exit if k == len(items) - 1 else None)


def build_captions():
    els, js = [], []
    for gi, g in enumerate(CAPS):
        gid = f"cg{gi:03d}"
        t0, t1 = round(g["start"], 3), round(g["end"], 3)
        x, y, align = g["x"], g["y"], g["align"]
        if align == "center":
            box = f"left:{x - 960}px;width:1920px;align-items:center;"
        elif align == "left":
            box = f"left:{x}px;width:1700px;align-items:flex-start;"
        else:
            box = f"left:{x - 1700}px;width:1700px;align-items:flex-end;"
        lines_html = []
        for li, line in enumerate(g["lines"]):
            spans = []
            for wi, (text, tt, st) in enumerate(line):
                fam, wt, it, size, color, glow = STY[st]
                sid = f"{gid}-w{li}{wi}"
                shadow = f"text-shadow:{GLOW_REST};" if glow else ""
                track = "-0.035em" if fam == "Inter Tight" else "-0.02em"
                if st == "SH":
                    track = "-0.01em"
                ml = "" if wi == 0 else ("margin-left:0.26em;" if fam == "Inter Tight" else "margin-left:0.2em;")
                spans.append(
                    f'<span id="{sid}" class="w" style="{ml}font-family:\'{fam}\';font-weight:{wt};'
                    f'font-style:{"italic" if it else "normal"};font-size:{size}px;color:{color};'
                    f'letter-spacing:{track};{shadow}">{esc(text)}</span>')
                lt = round(tt - t0, 3)
                if g["kind"] == "paper" or st in ("PS", "PM", "PB", "PXL"):
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.14 }}, {{ opacity: 1, scale: 1, duration: 0.4, '
                              f'ease: "expo.out", immediateRender: true }}, {r3(t0 + lt)});')
                    js.append(f'tl.set("#{sid}", {{ opacity: 1 }}, {r3(t0 + lt)});')
                elif st == "SH":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.16, '
                              f'ease: "back.out(2)" }}, {r3(t0 + lt)});')
                elif st == "R":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", '
                              f'duration: 0.16, ease: "power3.out" }}, {r3(t0 + lt)});')
                else:
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.12, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
                              f'{{ opacity: 1, scale: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.24, '
                              f'ease: "expo.out" }}, {r3(t0 + lt)});')
            gap = "0.18em"
            lines_html.append(f'<div class="ln" style="gap:{gap};line-height:{g["lh"]}">' + "".join(spans) + "</div>")
        els.append(
            f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(round(t1 - t0, 3))}" '
            f'data-track-index="1" data-layout-allow-overflow data-layout-allow-overlap '
            f'style="top:{y - 540}px;{box}">' + "".join(lines_html) + "</div>")
        if g["exit"] == "blurout":
            js.append(f'tl.to("#{gid} .w", {{ opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }}, '
                      f'{r3(t1 - 0.2)});')
    css = f"""
  {FONTS_CSS}
  #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; }}
  #root .cg {{ position: absolute; height: 1080px; display: flex; flex-direction: column; justify-content: center; }}
  #root .ln {{ display: flex; flex-direction: row; align-items: baseline; white-space: nowrap; }}
  #root .w {{ display: inline-block; white-space: nowrap; line-height: 0.95; }}
"""
    out = f"""<template>
  <style>{css}  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">
    {chr(10).join('    ' + e for e in els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(DUR)} }}, 0);
    {chr(10).join('    ' + j for j in js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
    open(f"{COMP}/captions.html", "w").write(out)


# --------------------------------------------------------------------------------------------
# THE EDIT
# --------------------------------------------------------------------------------------------
SCENES = []
SFX = []  # (name, picture_time, volume, media_start, duration)

PEAK = {"whoosh.mp3": 0.16, "whoosh-short.mp3": 0.16, "impact-bass-1.mp3": 0.04, "impact-bass-2.mp3": 2.06,
        "pop.mp3": 0.12, "click.mp3": 0.06, "click-soft.mp3": 0.06, "key-press.mp3": 0.06, "sparkle.mp3": 0.08,
        "glitch-1.mp3": 0.22, "glitch-2.mp3": 0.2, "glitch-3.mp3": 0.24, "whoosh-cinematic.mp3": 2.54}
SFXDUR = {"whoosh.mp3": 0.57, "whoosh-short.mp3": 0.57, "impact-bass-1.mp3": 2.12, "impact-bass-2.mp3": 2.59,
          "pop.mp3": 0.72, "click.mp3": 0.37, "click-soft.mp3": 0.37, "key-press.mp3": 0.4, "sparkle.mp3": 1.8,
          "glitch-1.mp3": 2.64, "glitch-2.mp3": 3.5, "glitch-3.mp3": 3.1, "whoosh-cinematic.mp3": 5.54}


def sfx(name, t, vol=0.35, ms=0.0, dur=None):
    SFX.append((name, t, vol, ms, dur))


# ---------------- S01 cold open: Venice "beggars" -> The Odyssey line ----------------
s = Scene("s01", 0.0, 5.40)
camA, vA = s.video("c_start_clean.mp4", 0.0, 1.53, ms=0.0, push=None)
# snap zoom on the shouted "BEGGARS" (reference: snap zoom into the name tag in the cold open)
s.scale_keys(camA, [(0.0, 1.0, 1.03, 0.98, "none"), (0.98, 1.03, 1.12, 0.14, "expo.out"), (1.12, 1.12, 1.15, 0.41, "none")])
s.video("c_start_clean.mp4", 1.53, 3.10, ms=1.53, push=(1.0, 1.04))
camC, vC = s.video("c_start_clean.mp4", 3.10, 5.40, ms=3.10, push=None)
s.scale_keys(camC, [(3.10, 1.0, 1.03, 0.73, "none"), (3.83, 1.03, 1.12, 0.14, "expo.out"), (3.97, 1.12, 1.16, 1.43, "none")])
s.neg(3.10, 3)
SCENES.append(s)
sfx("whoosh-short.mp3", 0.98, 0.16)
sfx("whoosh-short.mp3", 3.10, 0.28)
sfx("whoosh-short.mp3", 3.83, 0.14)
# cover captions (the burned ones are inpainted underneath)
cap([[("somebody", 0.13, "C")]], 0.53, y=546)
cap([[("get these", 0.53, "C")]], 1.03, y=546)
cap([[("beggars", 1.03, "CB")]], 1.33, y=556)
cap([[("out of here?", 1.33, "C")]], 2.10, y=546)
cap([[("somebody", 3.23, "C"), ("get", 3.47, "C"), ("these", 3.63, "C")]], 3.90, y=548)
cap([[("beggars", 3.90, "CB")]], 4.27, y=560)
cap([[("out", 4.27, "C"), ("of", 4.43, "C"), ("here!", 4.60, "C")]], 5.05, y=548)

# ---------------- S02 thesis ----------------
s = Scene("s02", 5.40, T(13))
camH, vH = s.image("hero.jpg", 5.40, T(2), grade="pixel", push=(1.0, 1.05), vars_style="--hf-color-grading-pixelate: 0.9;")
s.js.append(f'tl.to("#{vH}", {{ "--hf-color-grading-pixelate": 0, duration: 0.55, ease: "power2.out" }}, 0);')
s.paper(T(2), T(6))
# the hero photo shrinks into a card on the paper, then two more cards drop in per word
CX, CY, CW, CH = 1010, 250, 800, 450
cam1, im1 = s.image("hero.jpg", T(2), T(6), grade="pixel", push=None, box=(CX, CY, CW, CH), card=True,
                    vars_style="--hf-color-grading-pixelate: 0;")
dx0, dy0 = round(960 - (CX + CW / 2)), round(540 - (CY + CH / 2))
s.js.append(f'tl.fromTo("#{cam1}", {{ x: {dx0}, y: {dy0}, scale: 2.5, rotation: 0 }}, {{ x: 0, y: 0, scale: 1, rotation: -2, '
            f'duration: 0.36, ease: "expo.out" }}, {s.at(T(2))});')
s.js.append(f'tl.to("#{cam1}", {{ scale: 1.035, duration: {r3(T(6) - T(2) - 0.36)}, ease: "none" }}, {s.at(T(2) + 0.36)});')
s.image("bw1.jpg", T(3), T(6), grade="matte", box=(1440, 70, 380, 500), card=True, rot=5, drop=True, push=(1.0, 1.03))
s.image("slate.jpg", T(5), T(6), grade="matte", box=(1270, 330, 440, 550), card=True, rot=-3, drop=True, push=(1.0, 1.03))
camR, vR = s.video("c_run.mp4", T(6), T(7), grade="matte", push=(1.18, 1.0), pushease="expo.out",
                   vars_style="--hf-color-grading-exposure: 1.2;")
s.blow_in(vR, T(6), 0.3)
s.whiteflash(T(6), 0.18)
s.solid(T(7), T(8), "#050505")
s.video("c_kimmel_laugh.mp4", T(8), T(9), grade="matte", push=(1.0, 1.05))
s.silhouette("kimmel-sil.png", T(8), 2)
s.paper(T(9), T(13))
SCENES.append(s)
sfx("impact-bass-1.mp3", 5.40, 0.42)
sfx("whoosh-short.mp3", T(2), 0.24)
sfx("pop.mp3", T(3) + 0.02, 0.18)
sfx("pop.mp3", T(5) + 0.02, 0.20)
sfx("whoosh.mp3", T(6), 0.32)
sfx("pop.mp3", T(8), 0.18)
sfx("click-soft.mp3", T(9), 0.30)
cap([[W(0, "B", "Robert")], [W(1, "B", "Pattinson")]], T(2), x=140, y=660, align="left", lh=0.82)
cap([[W(2, "PS", "is"), W(3, "PS", "having"), W(4, "PS", "a")], [W(5, "PM", "generational")]], T(6), x=110, y=560,
    align="left", kind="paper", lh=1.05)
cap([[W(6, "XLI", "run,")]], T(7), y=560)
cap([[W(7, "S", "and")]], T(8), y=545)
cap([[W(8, "BI", "honestly,")]], T(9), x=1820, y=760, align="right")
paper_words([(9, "PS", "nobody"), (10, "PS", "saw"), (11, "PS", "it"), (12, "PXL", "coming.")], T(13), last_exit="blurout")

# ---------------- S03 "to some people, he'll always be Edward Cullen" ----------------
s = Scene("s03", T(13), T(21))
s.video("c_tw_lab.mp4", T(13), T(14), grade="halftone", push=(1.0, 1.04))
s.video("c_tw_wed.mp4", T(14), T(15), grade="halftone", push=(1.05, 1.0))
s.video("c_fans_full.mp4", T(15), T(16), grade="halftone", push=(1.0, 1.05))
s.video("c_bio.mp4", T(16), T(19), grade="film8mm", push=(1.0, 1.04))
s.video("c_edward_cu.mp4", T(19), T(21), grade="film8mm", push=(1.0, 1.06))
s.neg(T(19), 2)
SCENES.append(s)
for i in (13, 14, 15):
    sfx("click.mp3", T(i), 0.18)
sfx("sparkle.mp3", T(19), 0.30)
cap([[W(13, "M", "to")]], T(14), y=560)
cap([[W(14, "M", "some")]], T(15), y=560)
cap([[W(15, "M", "people,")]], T(16), y=560)
cap([[W(16, "S", "he'll")], [W(17, "BI", "always"), W(18, "S", "be")]], T(19), x=170, y=540, align="left", lh=0.95)
cap([[W(19, "B", "Edward")], [W(20, "B", "Cullen.")]], T(21), x=140, y=600, align="left", lh=0.82)

# ---------------- S04 "but everything he did after Twilight proved..." ----------------
s = Scene("s04", T(21), T(35))
s.video("c_sparkle.mp4", T(21), T(23), grade="film8mm", push=(1.0, 1.05))
s.neg(T(21), 2)
camW1, vW1 = s.video("c_tw_van.mp4", T(23), T(26), grade="film8mm", push=(1.05, 1.0),
                     vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camW1, vW1, T(23), dx=1)
camP, vP = s.image("tw_poster.jpg", T(26), T(27), grade="halftone", push=(1.0, 1.08), pos="50% 20%",
                   vars_style="--hf-color-grading-exposure: 0;")
s.blow_out(vP, T(27), 0.24, 1.8)
s.whiteflash(T(27), 0.16)
years = [("2012", "f_belami.jpg"), ("2014", "f_rover.jpg"), ("2015", "f_queen.jpg"), ("2016", "f_lostcity.jpg"),
         ("2017", "gt_neon.jpg"), ("2018", "f_damsel.jpg"), ("2019", "lh_portrait.jpg"), ("2020", "tn_red.jpg"),
         ("2022", "bt_cowl.jpg"), ("2025", "mk_helmet.jpg"), ("2026", "f_antinous.jpg")]
durs = [0.08, 0.08, 0.08, 0.09, 0.09, 0.10, 0.11, 0.12, 0.13, 0.15, 0.18]
tcur, steps = T(27), []
for k, ((yr, im), d) in enumerate(zip(years, durs)):
    t_next = tcur + d if k < len(years) - 1 else T(32)
    s.image(im, tcur, t_next, grade="matte", push=(1.05, 1.0))
    steps.append((yr, round(tcur, 3)))
    tcur = t_next
s.counter(steps, T(32), 960, 600, 300)
s.paper(T(32), T(35))
SCENES.append(s)
sfx("whoosh-short.mp3", T(21), 0.24)
sfx("whoosh.mp3", T(23) - 0.04, 0.30)
sfx("whoosh.mp3", T(27) - 0.05, 0.30)
sfx("click-soft.mp3", T(32), 0.30)
cap([[W(21, "S", "but")]], T(22), y=560)
cap([[W(22, "BI", "everything")]], T(23), y=560)
cap([[W(23, "S", "he"), W(24, "S", "did"), W(25, "S", "after")]], T(26), y=560)
cap([[W(26, "XL", "Twilight")]], T(27), y=620)
cap([[W(27, "S", "proved")]], T(28), y=930)
cap([[W(28, "S", "he"), W(29, "S", "was"), W(30, "S", "never")]], T(31), y=930)
cap([[W(31, "S", "stuck")]], T(32), y=930)
paper_words([(32, "PS", "with"), (33, "PS", "one"), (34, "PXL", "role.")], T(35), last_exit="blurout")

# ---------------- S05 the film run: one full-frame film per title ----------------
s = Scene("s05", T(35), T(44))
s.video("c_goodtime.mp4", T(35), T(37), grade="matte", push=(1.0, 1.05))
s.neg(T(35), 2)
camL, vL = s.video("c_lighthouse.mp4", T(37), T(39), grade="matte_bw", push=(1.05, 1.0),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camL, vL, T(37), dx=1)
camT1, vT1 = s.video("c_tenet_a.mp4", T(39), T(39) + 0.38, grade="matte", push=(1.0, 1.04),
                     vars_style="--hf-color-grading-exposure: 0.9;")
s.blow_in(vT1, T(39), 0.2)
s.video("c_tenet_b.mp4", T(39) + 0.38, T(40), grade="matte", push=(1.0, 1.07))
s.video("c_batroof.mp4", T(40), T(42), rate=0.75, grade="matte", push=(1.0, 1.05))
s.neg(T(40), 2)
camM, vM = s.video("c_mickey.mp4", T(42), T(44), grade="matte", push=(1.0, 1.05),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camM, vM, T(42), dx=-1)
# "Mickey 17": the number rolls 1 -> 17 and lands on the spoken "17" (reference counters)
s.text("2025", T(42), T(44), 960, 330, 56, family="Inter Tight", weight=700)
s.text("Mickey", T(42), T(44), 1010, 640, 230, family="Instrument Serif", weight=400, align="right")
roll = ["1", "2", "4", "7", "10", "13", "15", "16", "17"]
rt = [T(42) + 0.10, T(42) + 0.16, T(42) + 0.22, T(42) + 0.28, T(42) + 0.35, T(42) + 0.42, T(42) + 0.50, T(42) + 0.57, T(43)]
s.counter([(v, round(t, 3)) for v, t in zip(roll, rt)], T(44), 1060, 640, 230, family="Instrument Serif", weight=400,
          align="left", tick=0.14)
SCENES.append(s)
sfx("impact-bass-1.mp3", T(35), 0.22)
sfx("whoosh.mp3", T(37) - 0.04, 0.30)
sfx("whoosh-short.mp3", T(39), 0.22)
sfx("impact-bass-1.mp3", T(40), 0.24)
sfx("whoosh.mp3", T(42) - 0.04, 0.30)
cap([[("2017", T(35), "Y")], [W(35, "B", "Good"), W(36, "B", "Time.")]], T(37), y=820, lh=1.0)
cap([[("2019", T(37), "Y")], [W(37, "B", "The"), W(38, "B", "Lighthouse,")]], T(39), y=820, lh=1.0)
cap([[("2020", T(39), "Y")], [W(39, "XL", "Tenet,")]], T(40), y=760, lh=1.0)
cap([[("2022", T(40), "Y")], [W(40, "B", "The"), W(41, "B", "Batman,")]], T(42), y=820, lh=1.0)

# ---------------- S06 "every one of them was a weird, bold swing..." ----------------
s = Scene("s06", T(44), T(57))
s.paper(T(44), T(50))
panels = [("p_goodtime.mp4", T(44)), ("p_lighthouse.mp4", T(44) + 0.14), ("p_tenet.mp4", T(45)),
          ("p_batman.mp4", T(46)), ("p_mickey.mp4", T(47))]
for k, (src, t0) in enumerate(panels):
    grade = "matte_bw" if "lighthouse" in src else "matte"
    cam, vid = s.video(src, t0, T(50), grade=grade, push=None, box=(k * 384, 0, 384, 1080),
                       cam_extra="clip-path:inset(0% 100% 0% 0%);")
    s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
                f'duration: 0.2, ease: "expo.out" }}, {s.at(t0)});')
    sfx("whoosh-short.mp3" if k % 2 == 0 else "whoosh.mp3", t0, 0.16)
s.video("c_soot.mp4", T(50), T(51), grade="matte_bw", push=(1.04, 1.0))
s.neg(T(50), 2)
s.video("c_connie.mp4", T(51), T(52), grade="matte", push=(1.0, 1.06))
camK, vK = s.video("c_king.mp4", T(52), T(53), grade="matte", push=None, vars_style="--hf-color-grading-blur: 0.9;")
s.js.append(f'tl.fromTo("#{camK}", {{ x: 560, scale: 1.1 }}, {{ x: 0, scale: 1.0, duration: 0.2, ease: "power3.out" }}, {s.at(T(52))});')
s.js.append(f'tl.to("#{vK}", {{ "--hf-color-grading-blur": 0, duration: 0.24, ease: "power2.out" }}, {s.at(T(52))});')
s.paper(T(53), T(57))
SCENES.append(s)
sfx("whoosh-short.mp3", T(50), 0.24)
sfx("whoosh.mp3", T(52) - 0.04, 0.40)
sfx("click-soft.mp3", T(53), 0.30)
cap([[W(44, "M", "every"), W(45, "M", "one")]], T(46), y=540)
cap([[W(46, "M", "of"), W(47, "M", "them")]], T(48), y=540)
cap([[W(48, "S", "was"), W(49, "S", "a")]], T(50), y=540)
cap([[W(50, "XLI", "weird,")]], T(51), x=1780, y=700, align="right")
cap([[W(51, "XL", "bold")]], T(52), x=160, y=640, align="left")
cap([[W(52, "XLI", "swing")]], T(53), y=600)
paper_words([(53, "PS", "nobody"), (54, "PXL", "expected"), (55, "PS", "from"), (56, "PS", "him.")], T(57),
            last_exit="blurout")

# ---------------- S07 internet jokes + "spider monkey" ----------------
s = Scene("s07", T(57), 32.60)
s.video("c_tw_stare.mp4", T(57), T(59), grade="film8mm", push=(1.0, 1.05))
s.video("c_tw_glitch.mp4", T(59), T(61), grade="glitch", push=(1.0, 1.04))
s.video("c_tw_battle.mp4", T(61), T(63), grade="halftone", push=(1.05, 1.0))
s.video("c_sparkle2.mp4", T(63), 30.30, grade="halftone", push=(1.0, 1.06))
s.neg(T(63), 2)
s.video("c_spider.mp4", 30.30, 32.60, ms=0.10, grade="film8mm", push=(1.0, 1.05))
SCENES.append(s)
sfx("whoosh-short.mp3", T(57), 0.20)
sfx("glitch-1.mp3", T(59), 0.26)
sfx("whoosh-short.mp3", T(61), 0.20)
sfx("whoosh-short.mp3", T(63), 0.24)
sfx("pop.mp3", 31.55, 0.30)
cap([[W(57, "S", "and"), W(58, "S", "while")]], T(59), y=560)
cap([[W(59, "S", "the"), W(60, "M", "internet")]], T(61), y=560)
cap([[W(61, "S", "kept"), W(62, "S", "making")]], T(63), y=560)
cap([[W(63, "S", "Twilight")], [W(64, "BI", "jokes,")]], 30.30, x=1800, y=760, align="right")
cap([[("you better hold on tight,", 30.40, "R")]], 31.50, y=150)
cap([[("SPIDER", 31.50, "SH")], [("MONKEY", 31.68, "SH")]], 32.60, y=620, lh=0.86)

# ---------------- S08 directors + Batman ----------------
s = Scene("s08", 32.60, 38.90)
s.video("c_rover.mp4", 32.60, T(68), grade="matte", push=(1.0, 1.05))
s.neg(32.60, 2)
s.video("c_lh_work.mp4", T(68), T(69), grade="matte_bw", push=(1.0, 1.04))
camN, vN = s.video("c_nolan_set.mp4", T(69), T(73), grade="matte", push=(1.0, 1.05),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camN, vN, T(69), dx=-1)
dirs = [("gt_neon.jpg", "Safdie"), ("lh_duo.jpg", "Eggers"), ("tn_walk.jpg", "Nolan"), ("bt_signal.jpg", "Reeves"),
        ("mk_two.jpg", "Bong"), ("dune_scy2.jpg", "Villeneuve")]
d_t0, d_t1 = T(73), T(74)
step = round((d_t1 - d_t0) / len(dirs), 3)
for k, (im, name) in enumerate(dirs):
    a = round(d_t0 + k * step, 3)
    b = round(d_t0 + (k + 1) * step, 3) if k < len(dirs) - 1 else d_t1
    s.image(im, a, b, grade="matte", push=(1.06, 1.0))
    s.text(name, a, b, 960, 880, 64, family="Inter Tight", weight=700, anim="none")
    sfx("key-press.mp3", a, 0.2)
s.video("c_backhead.mp4", T(74), T(77), grade="matte", push=(1.0, 1.04))
s.video("c_cowl.mp4", T(77), T(79), grade="matte", push=(1.0, 1.08))
s.neg(T(77), 2)
camG, vG = s.video("c_gotham.mp4", T(79), 38.90, grade="matte", push=None)
s.scale_keys(camG, [(T(79), 1.2, 1.0, 0.3, "expo.out"), (T(79) + 0.3, 1.0, 1.04, round(38.90 - T(79) - 0.3, 3), "none")])
s.neg(T(79), 3)
SCENES.append(s)
sfx("whoosh-short.mp3", 32.58, 0.24)
sfx("whoosh.mp3", T(69) - 0.04, 0.30)
sfx("whoosh-short.mp3", T(77), 0.22)
sfx("impact-bass-2.mp3", T(79), 0.42)
sfx("impact-bass-1.mp3", T(79), 0.50)
cap([[W(65, "S", "he"), W(66, "S", "was")], [W(67, "BI", "quietly")]], T(68), y=560, lh=0.95)
cap([[W(68, "M", "working")]], T(69), y=560)
cap([[W(69, "S", "with"), W(70, "S", "the"), W(71, "S", "best")], [W(72, "B", "directors")]], T(73), y=560, lh=0.95)
cap([[W(73, "XLI", "alive,")]], T(74), y=520)
cap([[W(74, "S", "until")]], T(75), y=560)
cap([[W(75, "S", "one"), W(76, "S", "day,")]], T(77), y=560)
cap([[W(77, "S", "he"), W(78, "S", "became")]], T(79), x=1780, y=560, align="right")
cap([[W(79, "XL", "Batman.")]], 38.90, y=800)

# ---------------- S09 the vampire kid -> respected -> "and this year?" -> triptych ----------------
s = Scene("s09", 38.90, T(98))
cam = s.uid("cam")
z = s.nz()
s.uses_text = True
s.raw(f'<div class="cam" id="{cam}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{z}">'
      f'<img id="{cam}-plate" class="clip" src="assets/img/f_edward_cu.jpg" alt="" {s.timed(38.90, T(83))} '
      f'data-color-grading="{esc(GR["film8mm"])}" data-track-index="3" '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />'
      f'<div id="{cam}-vw" class="clip txw al" {s.timed(T(81), T(83))} data-track-index="6" '
      f'style="left:250px;width:1600px;top:170px;height:420px;text-align:left">'
      f'<span id="{cam}-vampire" class="tx" style="font-family:\'Instrument Serif\';font-style:italic;font-size:300px;'
      f'color:#F7F4F7;text-shadow:{GLOW_REST}">vampire</span></div>'
      f'<img id="{cam}-cut" class="clip" src="assets/img/f_edward_cu-cut.png" alt="" {s.timed(38.90, T(83))} '
      f'data-color-grading="{esc(GR["film8mm"])}" data-track-index="4" data-layout-allow-occlusion '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />'
      f'</div>')
s.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {r3(T(83) - 38.90)}, ease: "none" }}, 0);')
s.js.append(f'tl.fromTo("#{cam}-vampire", {{ opacity: 0, scale: 1.12, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
            f'{{ opacity: 1, scale: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.26, ease: "expo.out" }}, {s.at(T(81))});')
s.video("c_fans2.mp4", T(83), T(84), grade="halftone", push=(1.0, 1.05))
s.video("c_tw_party.mp4", T(84), T(86), grade="halftone", push=(1.05, 1.0))
s.neg(T(84), 2)
# photo strobe, one portrait every 5 frames (reference 15.43 s "why Oracle put their name")
strobe = ["solo01.jpg", "solo03.jpg", "solo05.jpg", "solo06.jpg", "solo02.jpg", "solo07.jpg"]
st0, st1 = T(86), T(92)
stp = round((st1 - st0) / len(strobe), 3)
for k, im in enumerate(strobe):
    a = round(st0 + k * stp, 3)
    b = round(st0 + (k + 1) * stp, 3) if k < len(strobe) - 1 else st1
    s.image(im, a, b, grade="matte", push=(1.05, 1.0), pos="50% 48%")
    sfx("key-press.mp3", a, 0.18)
camS, vS = s.image("solo08.jpg", T(92), T(93), grade="matte", push=(1.0, 1.05), pos="50% 35%",
                   vars_style="--hf-color-grading-exposure: 1.1;")
s.blow_in(vS, T(92), 0.28)
s.video("c_venice.mp4", T(93), T(94), grade="matte", push=(1.0, 1.05))
s.video("c_frame_cu.mp4", T(94), T(95), grade="matte", push=(1.0, 1.06))
s.neg(T(94), 2)
s.paper(T(95), T(98))
# triptych build (44.85 -> 45.85): three panels wipe in left to right with giant numerals
tri = [("t_odyssey.mp4", "1", 44.85, 4.0), ("t_prime.mp4", "2", 45.02, 2.5), ("t_dune.mp4", "3", 45.19, 0.95)]
for k, (src, num, t0, clen) in enumerate(tri):
    d = T(98) - t0
    cam2, vid = s.video(src, t0, T(98), ms=0.0, rate=round(min(1, clen / d), 3), grade="matte", push=None,
                        box=(k * 640, 0, 640, 1080), cam_extra="clip-path:inset(0% 100% 0% 0%);")
    s.js.append(f'tl.fromTo("#{cam2}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
                f'duration: 0.24, ease: "expo.out" }}, {s.at(t0)});')
    s.numeral(num, t0 + 0.06, T(98), x=k * 640 + 320, y=560, size=520)
    sfx("whoosh-short.mp3", t0, 0.22)
SCENES.append(s)
sfx("whoosh-short.mp3", 38.88, 0.22)
sfx("click.mp3", T(83), 0.20)
sfx("whoosh-short.mp3", T(84), 0.20)
sfx("whoosh.mp3", T(92) - 0.04, 0.26)
sfx("whoosh-short.mp3", T(93), 0.18)
sfx("whoosh-short.mp3", T(94), 0.18)
sfx("click-soft.mp3", T(95), 0.30)
cap([[W(80, "M", "the")]], T(81), x=170, y=200, align="left")
cap([[W(82, "M", "kid")]], T(83), x=1760, y=930, align="right")
cap([[W(83, "M", "everyone")]], T(84), y=560)
cap([[W(84, "BI", "laughed"), W(85, "S", "at")]], T(86), y=560)
cap([[W(86, "S", "is"), W(87, "S", "now"), W(88, "S", "one"), W(89, "S", "of"), W(90, "S", "the"), W(91, "S", "most")]],
    T(92), y=880)
cap([[W(92, "B", "respected")]], T(93), y=860)
cap([[W(93, "S", "actors"), (" in", T(93) + 0.18, "S")]], T(94), y=560)
cap([[W(94, "B", "Hollywood.")]], T(95), y=840)
paper_words([(95, "PS", "and"), (96, "PB", "this year?")], 44.85)

# ---------------- S10 chapter 1: The Odyssey ----------------
s = Scene("s10", T(98), T(113))
for k, (src, clen) in enumerate([("t_prime.mp4", 2.5), ("t_dune.mp4", 0.95)], start=1):
    cam2, vid = s.video(src, T(98), T(98) + 0.4, ms=0.8, grade="matte", push=None, box=(k * 640, 0, 640, 1080))
    s.js.append(f'tl.fromTo("#{cam2}", {{ x: 0 }}, {{ x: 1300, duration: 0.34, ease: "power3.in" }}, 0);')
cam, vid = s.video("c_antinous_fire.mp4", T(98), T(101), ms=0.0, grade="matte", push=None,
                   cam_extra="clip-path:inset(0% 66.67% 0% 0%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 66.67% 0% 0%)", scale: 1.0 }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'scale: 1.0, duration: 0.36, ease: "power3.inOut" }}, 0);')
s.js.append(f'tl.to("#{cam}", {{ scale: 1.05, duration: {r3(T(101) - T(98) - 0.36)}, ease: "none" }}, 0.36);')
s.numeral("1", T(98), T(101), x=1500, y=470, size=600)
# Nolan and the poster drop onto the paper as a two-card collage
s.paper(T(101), T(105))
s.image("nolan.jpg", T(101), T(105), grade="matte", box=(330, 120, 640, 760), card=True, rot=-3, drop=True)
s.image("od_poster.jpg", T(103), T(105), grade="matte", box=(1010, 90, 600, 900), card=True, rot=2.5, drop=True)
s.video("c_antinous_feast.mp4", T(105), T(107), grade="matte", push=(1.0, 1.05))
s.neg(T(105), 2)
s.video("c_antinous_arch.mp4", T(107), T(111), grade="matte", push=(1.0, 1.06))
s.video("c_antinous_glasses.mp4", T(111), T(112), grade="matte", push=(1.06, 1.0))
s.video("c_antinous_fire.mp4", T(112), T(113), ms=2.6, grade="matte", push=(1.04, 1.0))
s.neg(T(112), 3)
SCENES.append(s)
sfx("whoosh.mp3", T(98), 0.32)
sfx("pop.mp3", T(101), 0.18)
sfx("pop.mp3", T(103), 0.20)
sfx("whoosh-short.mp3", T(105), 0.22)
sfx("whoosh-short.mp3", T(111), 0.20)
sfx("impact-bass-1.mp3", T(112), 0.24)
cap([[W(98, "S", "he"), W(99, "S", "walked"), W(100, "S", "into")]], T(101), x=1500, y=900)
cap([[W(101, "S", "Christopher")], [W(102, "B", "Nolan's")]], T(103), x=650, y=880, lh=0.92)
cap([[W(103, "S", "The"), W(104, "B", "Odyssey")]], T(105), x=1310, y=900, lh=0.92)
cap([[W(105, "S", "as")], [W(106, "BI", "Antinous,")]], T(107), x=150, y=640, align="left")
cap([[W(107, "S", "one"), W(108, "S", "of"), W(109, "S", "the"), W(110, "S", "story's")]], T(111), y=880)
cap([[W(111, "M", "central")]], T(112), y=880)
cap([[W(112, "BI", "antagonists.")]], T(113), y=800)

# ---------------- S11 chapter 2: Primetime ----------------
s = Scene("s11", T(113), 59.90)
cam, vid = s.video("c_hansen.mp4", T(113), T(115), ms=0.0, grade="vhs", push=None,
                   cam_extra="clip-path:inset(0% 33.33% 0% 33.33%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 33.33% 0% 33.33%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.36, ease: "power3.inOut" }}, 0);')
s.numeral("2", T(113), T(115), x=1500, y=470, size=600)
s.video("c_prime_title.mp4", T(115), T(117), grade="vhs", push=(1.0, 1.05))
s.neg(T(115), 2)
s.video("c_hansen_cu.mp4", T(117), T(119), grade="vhs", push=(1.0, 1.05))
s.video("c_hansen.mp4", T(119), T(122), ms=0.9, grade="vhs", push=(1.05, 1.0))
s.video("c_schedule.mp4", T(122), T(123), grade="vhs", push=(1.0, 1.05))
s.video("c_stinghouse.mp4", T(123), T(127), grade="vhs", push=(1.0, 1.04))
s.video("c_pt_worried.mp4", T(127), T(128), grade="vhs", push=(1.0, 1.06))
s.video("c_chat.mp4", T(128), T(129), grade="glitch", push=(1.0, 1.06))
s.neg(T(128), 2)
s.video("c_hiddencam.mp4", T(129), T(130), grade="glitch", push=(1.0, 1.06))
# CRT static with a red REC glyph for 4 frames (reference 25.27 s: static + pink "$")
s.video("c_hiddencam.mp4", T(129), T(129) + 4 / 30, grade="crt", push=None)
rid = s.uid("rec")
s.raw(f'<div id="{rid}" class="clip rec" {s.timed(T(129), T(130))} data-track-index="6" '
      f'style="left:120px;top:96px;z-index:{s.nz()}"><i></i><span>REC</span></div>')
s.uses_text = True
s.video("c_strobeface.mp4", T(130), 57.80, grade="vhs", push=(1.0, 1.06))
# the real "...why don't you have a seat right there?" moment, in sync with the sting audio
s.video("c_seat1.mp4", 57.80, 59.28, grade="vhs", push=(1.0, 1.05))
s.video("c_seat2.mp4", 59.28, 59.90, grade="vhs", push=(1.04, 1.0))
SCENES.append(s)
sfx("whoosh.mp3", T(113), 0.30)
sfx("glitch-1.mp3", T(115), 0.30)
sfx("whoosh-short.mp3", T(117), 0.18)
sfx("glitch-3.mp3", T(122), 0.30)
sfx("glitch-1.mp3", T(128), 0.32)
sfx("glitch-2.mp3", T(129), 0.26)
sfx("click.mp3", T(130), 0.22)
sfx("glitch-3.mp3", 57.80, 0.28)
cap([[W(113, "S", "then"), W(114, "S", "came")]], T(115), x=1500, y=900)
cap([[W(117, "S", "with"), W(118, "S", "Pattinson")]], T(119), x=1800, y=860, align="right")
cap([[W(119, "S", "playing"), W(120, "S", "a")]], T(121), x=1800, y=860, align="right")
cap([[W(121, "BI", "television")]], T(122), x=1800, y=830, align="right")
cap([[W(122, "B", "journalist")]], T(123), y=880)
cap([[W(123, "S", "at"), W(124, "S", "the"), W(125, "S", "center"), W(126, "S", "of")]], T(127), y=880)
cap([[W(127, "BI", "controversial")]], T(128), y=860)
cap([[W(128, "XL", "predator")]], T(129), y=860)
cap([[W(129, "M", "sting")]], T(130), y=560)
cap([[W(130, "BI", "operations.")]], 57.80, y=860)
cap([[("…why don't you have a seat right there?", 57.92, "R")]], 59.90, y=150)

# ---------------- S12 chapter 3: Dune ----------------
s = Scene("s12", 59.90, T(140))
cam, vid = s.video("c_scytale.mp4", 59.90, T(133), ms=0.0, grade="matte", push=None,
                   cam_extra="clip-path:inset(0% 0% 0% 66.67%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 0% 0% 66.67%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.36, ease: "power3.inOut" }}, 0);')
s.numeral("3", 59.90, T(133), x=1500, y=470, size=600)
camY, vY = s.video("c_scytale.mp4", T(133), T(136), ms=1.0, grade="matte", push=(1.05, 1.0),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camY, vY, T(133), dx=1)
s.video("c_scytale.mp4", T(136), T(138), ms=2.2, grade="matte", push=(1.0, 1.05))
s.neg(T(136), 2)
camD, vD = s.image("dune_poster.jpg", T(138), T(140), grade="matte", push=None, pos="50% 38%")
s.scale_keys(camD, [(T(138), 1.0, 1.03, round(T(139) - T(138), 3), "none"),
                    (T(139), 1.03, 1.16, 0.14, "expo.out"), (T(139) + 0.14, 1.16, 1.2, round(T(140) - T(139) - 0.14, 3), "none")])
s.neg(T(139), 3)
SCENES.append(s)
sfx("whoosh.mp3", 59.90, 0.30)
sfx("whoosh.mp3", T(133) - 0.04, 0.26)
sfx("whoosh-short.mp3", T(136), 0.18)
sfx("impact-bass-1.mp3", T(139), 0.45)
cap([[W(131, "S", "and"), W(132, "S", "now")]], T(133), x=1500, y=900)
cap([[W(133, "S", "he's"), W(134, "S", "closing"), W(135, "S", "out")]], T(136), y=880)
cap([[W(136, "S", "the"), W(137, "S", "year")]], T(138), y=880)
cap([[W(138, "S", "with")], [W(139, "XL", "Dune.")]], T(140), x=1800, y=700, align="right")

# ---------------- S13 payoff + end card ----------------
s = Scene("s13", T(140), DUR)
camP1, vP1 = s.image("solo04.jpg", T(140), T(141), grade="matte", push=(1.0, 1.06), pos="50% 52%",
                     vars_style="--hf-color-grading-exposure: 1.0;")
s.blow_in(vP1, T(140), 0.3)
s.rgbsplit("solo04.jpg", T(140), frames=2, pos="50% 52%")
# role-switch montage from the source (King -> Mickey 17 -> Devil All the Time -> Good Time)
s.video("c_roles.mp4", T(141), T(144), grade="matte", push=(1.0, 1.04))
tiles = ["f_edward_cu.jpg", "gt_neon.jpg", "lh_soot.jpg", "tn_red.jpg", "bt_cowl.jpg", "mk_helmet.jpg", "f_hansen.jpg",
         "f_scytale.jpg", "f_king.jpg", "f_devil.jpg", "f_rover.jpg", "f_queen.jpg", "f_damsel.jpg", "f_dali.jpg",
         "f_bruce.jpg", "f_drama.jpg"]
s.grid(tiles, 4, 4, T(144), T(147))
s.neg(T(144), 2)
s.grid(tiles[:9], 3, 3, T(147), T(149))
s.grid(tiles[:4], 2, 2, T(149), T(151))
# "one box": a single framed square on paper, which then zooms through to full frame
s.paper(T(151), T(153) + 0.3)
camB, imB = s.image("f_edward_cu.jpg", T(151), T(153) + 0.3, grade="film8mm", box=(660, 240, 600, 600), card=True,
                    rot=0, drop=True, push=None)
s.js.append(f'tl.to("#{camB}", {{ scale: 1.03, duration: {r3(T(153) - T(151) - 0.26)}, ease: "none" }}, {s.at(T(151) + 0.26)});')
s.js.append(f'tl.to("#{camB}", {{ scale: 3.4, duration: 0.3, ease: "power3.in" }}, {s.at(T(153))});')
camE, vE = s.video("c_sparkle.mp4", T(153) + 0.3, T(157), ms=0.2, grade="film8mm", push=(1.06, 1.12),
                   vars_style="--hf-color-grading-exposure: 0;")
s.blow_out(vE, T(157), 0.5, 1.9)
s.whiteflash(T(157), 0.22, 0.9)
cam, vid = s.video("h_edward.mp4", T(157), T(158), grade="film8mm", push=None, box=(0, 0, 960, 1080))
camBt, vBt = s.video("h_batman.mp4", T(157), T(158), grade="matte", push=None, box=(960, 0, 960, 1080))
s.js.append(f'tl.fromTo("#{camBt}", {{ x: 960 }}, {{ x: 0, duration: 0.28, ease: "expo.out" }}, {s.at(T(157) + 0.06)});')
s.paper(T(158), DUR)
# end card: the name, a rule that draws out from the centre and a year counter (logo-build analog)
s.text("Robert", 71.45, DUR, 960, 470, 190, family="Instrument Serif", weight=400, color="#0B0B0B", glow=False,
       anim="ink", italic=True)
s.text("Pattinson", 71.55, DUR, 960, 640, 190, family="Instrument Serif", weight=400, color="#0B0B0B", glow=False,
       anim="ink", italic=True)
rule = s.uid("rule")
s.raw(f'<div id="{rule}" class="clip rule" {s.timed(71.70, DUR)} data-track-index="6" '
      f'style="left:660px;top:742px;width:600px;z-index:{s.nz()}"></div>')
s.js.append(f'tl.fromTo("#{rule}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "expo.out" }}, {s.at(71.70)});')
yrs = ["2008", "2011", "2014", "2017", "2019", "2022", "2024", "2025", "2026"]
ytm = [71.58, 71.61, 71.64, 71.68, 71.72, 71.77, 71.83, 71.90, 71.98]
s.counter([(v, t) for v, t in zip(yrs, ytm)], DUR, 960, 850, 64, family="Inter Tight", weight=700, color="#0B0B0B",
          glow=False, ink=True, tick=0.10)
SCENES.append(s)
sfx("impact-bass-1.mp3", T(140), 0.30)
sfx("whoosh-short.mp3", T(141), 0.20)
for i in (144, 147, 149):
    sfx("pop.mp3", T(i), 0.18)
sfx("pop.mp3", T(151), 0.20)
sfx("whoosh.mp3", T(153), 0.28)
sfx("whoosh-cinematic.mp3", T(156), 0.30)
sfx("whoosh-short.mp3", T(157), 0.26)
sfx("click-soft.mp3", T(158), 0.30)
sfx("impact-bass-1.mp3", 71.45, 0.30)
cap([[W(140, "B", "Pattinson")]], T(141), y=900)
cap([[W(141, "S", "keeps"), W(142, "S", "choosing")]], T(143), y=880)
cap([[W(143, "XLI", "roles")]], T(144), y=600)
cap([[W(144, "M", "that"), W(145, "M", "stop"), W(146, "M", "anyone")]], T(147), y=560)
cap([[W(147, "M", "from"), W(148, "M", "putting"), W(149, "M", "him")]], T(150), y=560)
cap([[W(150, "PS", "in"), W(151, "PS", "one")]], T(152), kind="paper", y=960)
cap([[W(152, "PB", "box,")]], T(153), kind="paper", y=960)
cap([[W(153, "S", "and"), W(154, "S", "that")]], T(155), y=560)
cap([[W(155, "S", "post")]], T(156), y=560)
cap([[W(156, "XL", "Twilight")]], T(157), y=580)
cap([[W(157, "XLI", "reinvention")]], T(158), y=580)
paper_words([(158, "PS", "might"), (159, "PS", "be"), (160, "PS", "one"), (161, "PS", "of"), (162, "PS", "the"),
             (163, "PXL", "best"), (164, "PS", "we've"), (165, "PS", "ever"), (166, "PXL", "seen.")], 71.45,
            last_exit="blurout")

# --------------------------------------------------------------------------------------------
# write everything
# --------------------------------------------------------------------------------------------


def write_root():
    hosts = []
    for k, sc in enumerate(SCENES):
        hosts.append(
            f'<div id="{sc.sid}" class="clip" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" '
            f'data-start="{r3(sc.start)}" data-duration="{r3(sc.dur)}" data-track-index="1" data-track-kind="graphics" '
            f'data-width="1920" data-height="1080" style="z-index:{10 + k}"></div>')
    hosts.append(
        f'<div id="leak1" class="clip" data-composition-id="leak1" data-composition-src="compositions/leak1.html" '
        f'data-start="{r3(T(26) + 0.30)}" data-duration="0.80" data-track-index="2" data-track-kind="graphics" '
        f'data-width="1920" data-height="1080" style="z-index:80"></div>')
    hosts.append(
        f'<div id="leak2" class="clip" data-composition-id="leak2" data-composition-src="compositions/leak2.html" '
        f'data-start="{r3(T(155) + 0.10)}" data-duration="1.30" data-track-index="2" data-track-kind="graphics" '
        f'data-width="1920" data-height="1080" style="z-index:80"></div>')
    hosts.append(
        f'<div id="grain" class="clip" data-composition-id="grain" data-composition-src="compositions/grain.html" '
        f'data-start="0" data-duration="{r3(DUR)}" data-track-index="3" data-track-kind="graphics" '
        f'data-width="1920" data-height="1080" style="z-index:90"></div>')
    hosts.append(
        f'<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
        f'data-start="0" data-duration="{r3(DUR)}" data-track-index="4" data-track-kind="captions" '
        f'data-width="1920" data-height="1080" style="z-index:100"></div>')
    auds = []
    vo = [("vo-a", 5.40, 24.90, 0.00), ("vo-b", 32.60, 5.40, 24.90), ("vo-c", 38.90, 5.95, 30.30),
          ("vo-d", 45.85, 11.95, 36.25), ("vo-e", 59.90, 11.52, 48.20)]
    for aid, st, d, ms in vo:
        auds.append(f'<audio id="{aid}" class="clip" src="assets/audio/vo.wav" data-start="{r3(st)}" data-duration="{r3(d)}" '
                    f'data-media-start="{r3(ms)}" data-volume="1" data-track-index="10"></audio>')
    for aid, src, st, d in [("sting-beggars", "sting-beggars.wav", 0.0, 5.50), ("sting-spider", "sting-spider.wav", 30.30, 2.35),
                            ("sting-seat", "sting-seat.wav", 57.80, 2.15)]:
        auds.append(f'<audio id="{aid}" class="clip" src="assets/audio/{src}" data-start="{r3(st)}" data-duration="{r3(d)}" '
                    f'data-volume="1" data-fade-out="0.12" data-track-index="11"></audio>')
    lanes = []  # end time per lane
    for k, (name, t, vol, ms, dur) in enumerate(sorted(SFX, key=lambda x: x[1])):
        start = max(0.0, round(t + 1 / 30 - PEAK.get(name, 0.05), 3))
        d = dur or SFXDUR.get(name, 1.0)
        if start + d > DUR:
            d = round(DUR - start, 3)
        lane = next((i for i, e in enumerate(lanes) if e <= start), None)
        if lane is None:
            lanes.append(0.0); lane = len(lanes) - 1
        lanes[lane] = start + d
        auds.append(f'<audio id="sfx{k:03d}" class="clip" src="assets/audio/sfx/{name}" data-start="{r3(start)}" '
                    f'data-duration="{r3(d)}" data-media-start="{r3(ms)}" data-volume="{vol}" data-track-index="{20 + lane}"></audio>')
    page = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0b0b0b; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; background: #0b0b0b; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r3(DUR)}" data-width="1920" data-height="1080">
      <div id="bg"></div>
      {chr(10).join('      ' + h for h in hosts)}
      {chr(10).join('      ' + a for a in auds)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.to({{}}, {{ duration: {r3(DUR)} }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(f"{PRJ}/index.html", "w").write(page)


def write_aux():
    # light-leak copies with their own composition ids; GSAP from the local vendor copy
    src = open(f"{COMP}/organic-light-leak-overlay.html").read()
    src = src.replace("https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js", "vendor/gsap.min.js")
    for lid in ("leak1", "leak2"):
        open(f"{COMP}/{lid}.html", "w").write(
            src.replace('id="organic-light-leak-overlay"', f'id="{lid}"')
               .replace('data-composition-id="organic-light-leak-overlay"', f'data-composition-id="{lid}"'))
    # grain: the registry component's markup inside a scene template, at 7 % opacity
    g = open(f"{COMP}/components/grain-overlay.html").read()
    m = re.search(r'url\("(data:image/svg\+xml[^"]+)"\)', g)
    data_url = m.group(1) if m else ""
    # deterministic grain: a stepped GSAP position jitter (12 fps), no CSS animation
    jit = []
    offs = [(-5, -5), (-10, 5), (5, -10), (-5, 15), (-10, 5), (15, 0), (0, 10), (-15, 0), (10, 5), (0, 0)]
    t = 0.0
    k = 0
    while t < DUR:
        dx, dy = offs[k % len(offs)]
        jit.append(f'tl.set("#grain-tex", {{ xPercent: {dx}, yPercent: {dy} }}, {t:.3f});')
        t = round(t + 1 / 12, 3)
        k += 1
    grain = f"""<template>
  <style>
  #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
  #grain-tex {{ position: absolute; left: -50%; top: -50%; width: 200%; height: 200%; opacity: 0.07;
    background-image: url("{data_url}"); mix-blend-mode: overlay; }}
  </style>
  <div id="root" data-composition-id="grain" data-width="1920" data-height="1080">
    <div id="grain-box" class="clip" data-start="0" data-duration="{r3(DUR)}" data-track-index="1" data-layout-ignore
      style="position:absolute;left:0;top:0;width:1920px;height:1080px"><div id="grain-tex"></div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(DUR)} }}, 0);
    {chr(10).join('    ' + j for j in jit)}
    window.__timelines["grain"] = tl;
  </script>
</template>
"""
    open(f"{COMP}/grain.html", "w").write(grain)


if __name__ == "__main__":
    os.makedirs(f"{PRJ}/vendor", exist_ok=True)
    shutil.copy(f"{ROOT}/vendor/gsap.min.js", f"{PRJ}/vendor/gsap.min.js")
    for sc in SCENES:
        sc.write()
    build_captions()
    write_aux()
    write_root()
    print("scenes:", [(sc.sid, round(sc.start, 2), round(sc.end, 2)) for sc in SCENES])
    print("captions:", len(CAPS), "sfx:", len(SFX))
