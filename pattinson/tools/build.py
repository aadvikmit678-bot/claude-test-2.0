#!/usr/bin/env python3
"""Generate the HyperFrames compositions for the Pattinson edit from one shot/caption table.

Writes pattinson/index.html, compositions/s01..s13.html, compositions/captions.html,
compositions/grain.html and leak copies. Every timed element is plain HTML with its own id,
data-start and data-duration (seconds local to its file), so Studio can edit the output.
All times below are GLOBAL seconds; each scene converts them to local time.
"""
import html, json, os, re, shutil

ROOT = "/home/user/claude-test-2.0"
PRJ = f"{ROOT}/pattinson"
WORK = f"{ROOT}/pattinson-work"
COMP = f"{PRJ}/compositions"
DUR = 74.0
LEAD = 0.07  # captions and cuts arrive 2 frames before the word

GR = json.load(open(f"{WORK}/build/gradings.json"))
WORDS = json.load(open(f"{WORK}/words_global.json"))


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
                           f'duration: {r3(round(t1 - t0, 3))}, ease: "{pushease}" }}, {r3(self.L(t0))});')
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
                f'{{ scale: 1, y: 0, rotation: {rot}, opacity: 1, duration: 0.26, ease: "expo.out" }}, {r3(self.L(t0))});')
            if push and d > 0.3:
                self.js.append(f'tl.to("#{cam}", {{ scale: {push[1] - 0.01}, duration: {r3(d - 0.26)}, ease: "none" }}, '
                               f'{r3(self.L(t0) + 0.26)});')
        elif push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]}, rotation: {rot} }}, {{ scale: {push[1]}, rotation: {rot}, '
                           f'duration: {r3(d)}, ease: "none" }}, {r3(self.L(t0))});')
        return cam, im

    def paper(self, t0, t1):
        pid = self.uid("paper")
        self.els.append(f'<img id="{pid}" class="clip paper" src="assets/tex/paper.png" alt="" '
                        f'{self.timed(t0, t1)} data-track-index="1" style="z-index:{self.nz()}" />')

    def solid(self, t0, t1, color="#000"):
        sid = self.uid("solid")
        self.els.append(f'<div id="{sid}" class="clip solid" {self.timed(t0, t1)} data-track-index="4" '
                        f'style="background:{color};z-index:{self.nz()}"></div>')

    def neg(self, t, frames=3):
        nid = self.uid("neg")
        self.els.append(f'<div id="{nid}" class="clip neg" {self.timed(t, t + frames / 30)} data-track-index="5" '
                        f'style="z-index:{self.nz()}"></div>')

    def whiteflash(self, t, d=0.2, peak=0.95):
        fid = self.uid("wf")
        self.els.append(f'<div id="{fid}" class="clip flashw" {self.timed(t - 0.06, t + d)} data-track-index="5" '
                        f'style="z-index:{self.nz()}"></div>')
        self.js.append(f'tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: {peak}, duration: 0.06, ease: "power4.in" }}, {r3(self.L(t - 0.06))});')
        self.js.append(f'tl.to("#{fid}", {{ opacity: 0, duration: {r3(d - 0.01)}, ease: "power2.out" }}, {r3(self.L(t))});')

    def silhouette(self, src, t, frames=2):
        sid = self.uid("sil")
        self.els.append(f'<img id="{sid}" class="clip" src="assets/img/{src}" alt="" {self.timed(t, t + frames / 30)} '
                        f'data-track-index="5" style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
                        f'object-fit:cover;z-index:{self.nz()}" />')

    def numeral(self, ch, t0, t1, x=960, y=540, size=560, z=None):
        self.uses_text = True
        wid, nid = self.uid("numw"), self.uid("num")
        z = z or self.nz()
        self.els.append(
            f'<div id="{wid}" class="clip numwrap" {self.timed(t0, t1)} data-track-index="6" '
            f'style="z-index:{z};left:{x - 400}px;top:{y - 400}px;width:800px;height:800px">'
            f'<span id="{nid}" class="num" style="font-size:{size}px">{ch}</span></div>')
        self.js.append(f'tl.fromTo("#{nid}", {{ opacity: 0, scale: 1.12, filter: "blur(18px)" }}, '
                       f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }}, {r3(self.L(t0))});')

    def text(self, txt, t0, t1, x, y, size, family="Inter Tight", weight=800, color="#F7F4F7",
             glow=True, align="center", style="", anim="glow", z=None, italic=False):
        """A free graphic text element (counters, panel labels in scenes)."""
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
                           f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {r3(self.L(t0))});')
        return sid

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
                           f'ease: "expo.out" }}, {r3(self.L(t0))});')

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
# --------------------------------------------------------------------------------------------
STY = {
    # key: (family, weight, italic, size, color, glow)
    "S": ("Inter Tight", 700, False, 54, "#F7F4F7", True),
    "M": ("Inter Tight", 800, False, 92, "#F7F4F7", True),
    "B": ("Instrument Serif", 400, False, 180, "#F7F4F7", True),
    "BI": ("Instrument Serif", 400, True, 180, "#F7F4F7", True),
    "XL": ("Instrument Serif", 400, False, 270, "#F7F4F7", True),
    "XLI": ("Instrument Serif", 400, True, 270, "#F7F4F7", True),
    "PS": ("Inter Tight", 700, False, 70, "#0B0B0B", False),
    "PB": ("Instrument Serif", 400, True, 170, "#0B0B0B", False),
    "PXL": ("Instrument Serif", 400, True, 230, "#0B0B0B", False),
    "R": ("Inter Tight", 600, False, 38, "#F7F4F7", True),
    "SH": ("Archivo Black", 400, False, 150, "#1C59F7", False),
    "T": ("Instrument Serif", 400, False, 66, "#F7F4F7", True),
    "TI": ("Instrument Serif", 400, True, 58, "#F7F4F7", True),
    "Y": ("Inter Tight", 700, False, 32, "#F7F4F7", True),
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
                if g["kind"] == "paper" or st in ("PS", "PB", "PXL"):
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
SFX = []  # (name, picture_time, volume, media_start)

PEAK = {"whoosh.mp3": 0.16, "whoosh-short.mp3": 0.16, "impact-bass-1.mp3": 0.04, "impact-bass-2.mp3": 2.06,
        "pop.mp3": 0.12, "click.mp3": 0.06, "click-soft.mp3": 0.06, "key-press.mp3": 0.06, "sparkle.mp3": 0.08,
        "glitch-1.mp3": 0.22, "glitch-3.mp3": 0.24, "whoosh-cinematic.mp3": 2.54}
SFXDUR = {"whoosh.mp3": 0.57, "whoosh-short.mp3": 0.57, "impact-bass-1.mp3": 2.12, "impact-bass-2.mp3": 2.59,
          "pop.mp3": 0.72, "click.mp3": 0.37, "click-soft.mp3": 0.37, "key-press.mp3": 0.4, "sparkle.mp3": 1.8,
          "glitch-1.mp3": 2.64, "glitch-3.mp3": 3.1, "whoosh-cinematic.mp3": 5.54}


def sfx(name, t, vol=0.35, ms=0.0, dur=None):
    SFX.append((name, t, vol, ms, dur))


# ---------------- S01 cold open ----------------
s = Scene("s01", 0.0, 5.40)
s.video("c_start_clean.mp4", 0.0, 3.10, ms=0.0, grade="matte", push=(1.0, 1.04))
s.video("c_start_clean.mp4", 3.10, 5.40, ms=3.10, grade="matte", push=(1.03, 1.10))
s.neg(3.10, 3)
SCENES.append(s)
sfx("whoosh-short.mp3", 3.10, 0.28)
# cover captions (burned ones are inpainted underneath)
cap([[("somebody", 0.13, "C")]], 0.53, y=546)
cap([[("get these", 0.53, "C")]], 1.03, y=546)
cap([[("beggars", 1.03, "CB")]], 1.33, y=556)
cap([[("out of here?", 1.33, "C")]], 2.10, y=546)
cap([[("somebody", 3.23, "C"), ("get", 3.47, "C"), ("these", 3.63, "C")]], 3.90, y=548)
cap([[("beggars", 3.90, "CB")]], 4.27, y=560)
cap([[("out", 4.27, "C"), ("of", 4.43, "C"), ("here!", 4.60, "C")]], 5.05, y=548)

# ---------------- S02 thesis ----------------
s = Scene("s02", 5.40, T(13))
s.image("hero.jpg", 5.40, T(2), grade="pixel", push=(1.0, 1.06), vars_style="--hf-color-grading-pixelate: 0.9;")
hero_img = f"{s.sid}-i2"
s.js.append(f'tl.to("#{hero_img}", {{ "--hf-color-grading-pixelate": 0, duration: 0.55, ease: "power2.out" }}, 0);')
s.paper(T(2), T(6))
s.image("slate.jpg", T(2), T(6), grade="matte", box=(1150, 95, 620, 890), card=True, rot=-1.5, drop=True)
s.video("c_run.mp4", T(6), T(7), ms=0.0, grade="matte", push=(1.18, 1.0), pushease="expo.out")
s.whiteflash(T(6), 0.18)
s.solid(T(7), T(8) - 0.0, "#050505")
s.video("c_kimmel_laugh.mp4", T(8), T(9), ms=0.0, grade="matte", push=(1.0, 1.05))
s.silhouette("kimmel-sil.png", T(8), 2)
s.paper(T(9), T(13))
SCENES.append(s)
sfx("impact-bass-1.mp3", 5.40, 0.42)
sfx("whoosh-short.mp3", T(2), 0.26)
sfx("whoosh.mp3", T(6), 0.32)
sfx("pop.mp3", T(8), 0.18)
sfx("click-soft.mp3", T(9), 0.30)
cap([[W(0, "B", "Robert")], [W(1, "B", "Pattinson")]], T(2), x=150, y=640, align="left", lh=0.82)
cap([[W(2, "PS", "is"), W(3, "PS", "having"), W(4, "PS", "a")], [W(5, "PB", "generational")]], T(6), x=150, y=560, align="left", kind="paper", lh=1.0)
cap([[W(6, "XLI", "run,")]], T(7), y=560)
cap([[W(7, "S", "and")]], T(8), y=545)
cap([[W(8, "BI", "honestly,")]], T(9), x=1820, y=760, align="right")
cap([[W(9, "PS", "nobody")]], T(10), kind="paper")
cap([[W(10, "PS", "saw")]], T(11), kind="paper")
cap([[W(11, "PS", "it")]], T(12), kind="paper")
cap([[W(12, "PXL", "coming.")]], T(13), kind="paper", exit="blurout")

# ---------------- S03 edward ----------------
s = Scene("s03", T(13), T(21))
s.paper(T(13), T(16))
s.image("tw_cast.jpg", T(13) + 0.02, T(16), grade="halftone", box=(170, 170, 900, 506), card=True, rot=-4, drop=True)
s.image("tw_poster.jpg", T(14), T(16), grade="halftone", box=(1180, 120, 520, 780), card=True, rot=3, drop=True)
s.image("tw_trio.jpg", T(15), T(16), grade="halftone", box=(520, 430, 900, 506), card=True, rot=-1, drop=True)
s.video("c_bio.mp4", T(16), T(19), ms=0.0, grade="film8mm", push=(1.0, 1.04))
s.video("c_edward_cu.mp4", T(19), T(21), ms=0.0, grade="film8mm", push=(1.0, 1.06))
SCENES.append(s)
for i in (13, 14, 15):
    sfx("pop.mp3", T(i) + 0.02, 0.20)
sfx("sparkle.mp3", T(19), 0.30)
cap([[W(13, "M", "to")]], T(14))
cap([[W(14, "M", "some")]], T(15))
cap([[W(15, "M", "people,")]], T(16))
cap([[W(16, "S", "he'll")], [W(17, "BI", "always"), W(18, "S", "be")]], T(19), x=180, y=520, align="left")
cap([[W(19, "B", "Edward")], [W(20, "B", "Cullen.")]], T(21), x=150, y=600, align="left", lh=0.82)

# ---------------- S04 turn ----------------
s = Scene("s04", T(21), T(35))
s.video("c_sparkle.mp4", T(21), T(26), ms=0.0, grade="film8mm", push=(1.0, 1.06))
s.neg(T(21), 3)
s.paper(T(26), T(27))
s.image("tw_prom.jpg", T(26), T(27), grade="halftone", box=(380, 150, 1160, 652), card=True, rot=1.5, drop=True)
years = [("2012", "f_belami.jpg"), ("2014", "f_rover.jpg"), ("2015", "f_queen.jpg"), ("2016", "f_lostcity.jpg"),
         ("2017", "gt_neon.jpg"), ("2018", "f_damsel.jpg"), ("2019", "lh_portrait.jpg"), ("2020", "tn_red.jpg"),
         ("2022", "bt_cowl.jpg"), ("2025", "mk_helmet.jpg"), ("2026", "f_antinous.jpg")]
durs = [0.08, 0.08, 0.08, 0.09, 0.09, 0.10, 0.11, 0.12, 0.13, 0.15, 0.18]
tcur = T(27)
c_end = T(32)
for k, ((yr, im), d) in enumerate(zip(years, durs)):
    t_next = tcur + d if k < len(years) - 1 else c_end
    s.image(im, tcur, t_next, grade="matte", push=(1.04, 1.0))
    s.text(yr, tcur, t_next, 960, 640, 300, family="Inter Tight", weight=800, anim="glow" if k == 0 else "none")
    sfx("key-press.mp3", tcur, 0.22)
    tcur = t_next
s.paper(T(32), T(35))
SCENES.append(s)
sfx("whoosh-short.mp3", T(21), 0.26)
sfx("whoosh.mp3", T(27) - 0.05, 0.30)
sfx("click-soft.mp3", T(32), 0.30)
cap([[W(21, "S", "but")]], T(22))
cap([[W(22, "BI", "everything")]], T(23), y=560)
cap([[W(23, "S", "he"), W(24, "S", "did"), W(25, "S", "after")]], T(26))
cap([[W(26, "B", "Twilight")]], T(27), y=560)
cap([[W(27, "S", "proved")]], T(28), y=880)
cap([[W(28, "S", "he"), W(29, "S", "was"), W(30, "S", "never")]], T(31), y=880)
cap([[W(31, "S", "stuck")]], T(32), y=880)
cap([[W(32, "PS", "with"), W(33, "PS", "one")]], T(34), kind="paper")
cap([[W(34, "PXL", "role.")]], T(35), kind="paper", exit="blurout")

# ---------------- S05 film run (5 panels) ----------------
s = Scene("s05", T(35), T(44), ground="#0b0b0b")
s.paper(T(35), T(44))
panels = [("p_goodtime.mp4", 35, 2.85), ("p_lighthouse.mp4", 37, 1.95), ("p_tenet.mp4", 39, 1.65),
          ("p_batman.mp4", 40, 1.10), ("p_mickey.mp4", 42, 1.05)]
for k, (src, wi, clen) in enumerate(panels):
    t0 = T(wi)
    d = T(44) - t0
    rate = round(min(1.0, clen / d), 3)
    grade = "matte_bw" if "lighthouse" in src else "matte"
    cam, vid = s.video(src, t0, T(44), ms=0.0, rate=rate, grade=grade, push=None,
                       box=(k * 384, 0, 384, 1080), cam_extra="clip-path:inset(0% 100% 0% 0%);")
    s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
                f'duration: 0.22, ease: "expo.out" }}, {r3(s.L(t0))});')
    sfx("whoosh-short.mp3" if k % 2 == 0 else "whoosh.mp3", t0, 0.22)
SCENES.append(s)
titles = [("Good Time", "2017", 35, 192, None), ("The Lighthouse", "2019", 37, 576, 38),
          ("Tenet", "2020", 39, 960, None), ("The Batman", "2022", 40, 1344, 41), ("Mickey 17", "2025", 42, 1728, 43)]
for name, yr, wi, cx, wi2 in titles:
    cap([[(yr, T(wi), "Y")], [(name, T(wi), "T")]], T(44), x=cx, y=930, lh=1.15)

# ---------------- S06 swing ----------------
s = Scene("s06", T(44), T(57))
roles = ["gt_red.jpg", "lh_soot.jpg", "tn_desert.jpg", "bt_red.jpg", "mk_two.jpg", "f_king.jpg", "f_devil.jpg",
         "f_rover.jpg", "f_queen.jpg", "f_damsel.jpg", "pt_overhead.jpg", "dune_scy2.jpg", "gt_purple.jpg",
         "lh_duo.jpg", "f_heron.jpg", "f_dali.jpg"]
s.grid(roles[:4], 2, 2, T(44), T(46))
s.grid(roles[:9], 3, 3, T(46), T(48))
s.grid(roles, 4, 4, T(48), T(50))
s.video("c_soot.mp4", T(50), T(51), grade="matte_bw", push=(1.04, 1.0))
s.neg(T(50), 3)
s.video("c_connie.mp4", T(51), T(52), grade="matte", push=(1.0, 1.05))
cam, vid = s.video("c_king.mp4", T(52), T(53), grade="matte", push=None)
s.js.append(f'tl.fromTo("#{cam}", {{ x: 520, scale: 1.08 }}, {{ x: 0, scale: 1.0, duration: 0.2, ease: "power3.out" }}, {r3(s.L(T(52)))});')
s.paper(T(53), T(57))
SCENES.append(s)
for i in (44, 46, 48):
    sfx("pop.mp3", T(i), 0.18)
sfx("whoosh-short.mp3", T(50), 0.24)
sfx("whoosh.mp3", T(52) - 0.04, 0.40)
sfx("click-soft.mp3", T(53), 0.30)
cap([[W(44, "M", "every"), W(45, "M", "one")]], T(46))
cap([[W(46, "M", "of"), W(47, "M", "them")]], T(48))
cap([[W(48, "M", "was"), W(49, "M", "a")]], T(50))
cap([[W(50, "XLI", "weird,")]], T(51), x=1780, y=700, align="right")
cap([[W(51, "XL", "bold")]], T(52), x=160, y=640, align="left")
cap([[W(52, "XLI", "swing")]], T(53), y=600)
cap([[W(53, "PS", "nobody")]], T(54), kind="paper")
cap([[W(54, "PXL", "expected")]], T(55), kind="paper")
cap([[W(55, "PS", "from"), W(56, "PS", "him.")]], T(57), kind="paper")

# ---------------- S07 jokes + spider monkey ----------------
s = Scene("s07", T(57), 32.60)
s.paper(T(57), T(63))
s.image("tw_tree1.jpg", T(57) + 0.02, T(63), grade="halftone", box=(130, 150, 860, 484), card=True, rot=-3, drop=True)
s.image("tw_tree2.jpg", T(59), T(63), grade="halftone", box=(960, 110, 820, 461), card=True, rot=2.5, drop=True)
s.image("tw_kiss.jpg", T(61), T(63), grade="halftone", box=(560, 500, 820, 461), card=True, rot=-1, drop=True)
s.video("c_sparkle2.mp4", T(63), 30.30, grade="halftone", push=(1.0, 1.06))
s.video("c_spider.mp4", 30.30, 32.60, ms=0.10, grade="film8mm", push=(1.0, 1.05))
SCENES.append(s)
for i in (57, 59, 61):
    sfx("pop.mp3", T(i) + 0.02, 0.18)
sfx("whoosh-short.mp3", T(63), 0.24)
sfx("pop.mp3", 31.55, 0.30)
cap([[W(57, "PS", "and"), W(58, "PS", "while")]], T(59), kind="paper", y=990)
cap([[W(59, "PS", "the"), W(60, "PS", "internet")]], T(61), kind="paper", y=990)
cap([[W(61, "PS", "kept"), W(62, "PS", "making")]], T(63), kind="paper", y=990)
cap([[W(63, "S", "Twilight")], [W(64, "BI", "jokes,")]], 30.30, x=1800, y=760, align="right")
cap([[("you better hold on tight,", 30.40, "R")]], 31.50, y=150)
cap([[("SPIDER", 31.50, "SH")], [("MONKEY", 31.68, "SH")]], 32.60, y=620, lh=0.86)

# ---------------- S08 directors + batman ----------------
s = Scene("s08", 32.60, 38.90)
s.paper(32.60, T(69))
s.image("bw2.jpg", 32.60, T(69), grade="matte", box=(640, 60, 640, 960), card=True, rot=-1.5, drop=True)
s.paper(T(69), T(73))
s.image("nolan.jpg", T(69), T(73), grade="matte", box=(560, 90, 800, 900), card=True, rot=1.5, drop=True)
dirs = [("gt_neon.jpg", "Safdie"), ("lh_duo.jpg", "Eggers"), ("tn_walk.jpg", "Nolan"), ("bt_signal.jpg", "Reeves"),
        ("mk_two.jpg", "Bong"), ("dune_scy2.jpg", "Villeneuve")]
d_t0, d_t1 = T(73), T(74)
step = round((d_t1 - d_t0) / len(dirs), 3)
for k, (im, name) in enumerate(dirs):
    a = round(d_t0 + k * step, 3)
    b = round(d_t0 + (k + 1) * step, 3) if k < len(dirs) - 1 else d_t1
    s.image(im, a, b, grade="matte", push=(1.06, 1.0))
    s.text(name, a, b, 960, 860, 46, family="Inter Tight", weight=700, anim="none")
    sfx("key-press.mp3", a, 0.2)
s.video("c_backhead.mp4", T(74), T(77), grade="matte", push=(1.0, 1.04))
s.video("c_cowl.mp4", T(77), T(79), grade="matte", push=(1.0, 1.08))
s.video("c_gotham.mp4", T(79), 38.90, grade="matte", push=(1.06, 1.0), pushease="power2.out")
s.neg(T(79), 3)
SCENES.append(s)
sfx("whoosh-short.mp3", 32.58, 0.24)
sfx("pop.mp3", T(69), 0.18)
sfx("impact-bass-2.mp3", T(79), 0.42)
sfx("impact-bass-1.mp3", T(79), 0.50)
cap([[W(65, "S", "he"), W(66, "S", "was")]], T(67))
cap([[W(67, "BI", "quietly")]], T(68), y=560)
cap([[W(68, "M", "working")]], T(69))
cap([[W(69, "S", "with"), W(70, "S", "the"), W(71, "S", "best")], [W(72, "B", "directors")]], T(73), y=560)
cap([[W(73, "XLI", "alive,")]], T(74), y=520)
cap([[W(74, "S", "until")]], T(75), y=800)
cap([[W(75, "S", "one"), W(76, "S", "day,")]], T(77), y=800)
cap([[W(77, "S", "he"), W(78, "S", "became")]], T(79), x=1780, y=560, align="right")
cap([[W(79, "XL", "Batman.")]], 38.90, y=800)

# ---------------- S09 respect, this year, triptych ----------------
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
s.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {r3(T(83) - 38.90)}, ease: "none" }}, 0);')
s.js.append(f'tl.fromTo("#{cam}-vampire", {{ opacity: 0, scale: 1.12, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
            f'{{ opacity: 1, scale: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.26, ease: "expo.out" }}, {r3(s.L(T(81)))});')
s.paper(T(83), T(86))
s.video("c_fans.mp4", T(83), T(86), grade="halftone", box=(560, 40, 800, 874), cam_extra="", style="", push=(1.0, 1.04))
s.paper(T(86), T(93))
s.video("c_carpet.mp4", T(86), T(93), grade="matte", box=(650, 40, 620, 872), push=(1.0, 1.04))
s.paper(T(93), T(95))
s.image("solo01.jpg", T(93), T(95), grade="matte", box=(170, 120, 520, 780), card=True, rot=-3, drop=True)
s.image("solo04.jpg", T(93) + 0.18, T(95), grade="matte", box=(1230, 160, 520, 780), card=True, rot=3, drop=True)
s.image("solo06.jpg", T(94), T(95), grade="matte", box=(700, 200, 520, 780), card=True, rot=-1, drop=True)
s.paper(T(95), T(98))
# triptych build (44.85 -> 45.85)
tri = [("t_odyssey.mp4", "1", 44.85, 4.0), ("t_prime.mp4", "2", 45.02, 2.5), ("t_dune.mp4", "3", 45.19, 0.95)]
for k, (src, num, t0, clen) in enumerate(tri):
    d = T(98) - t0
    cam2, vid = s.video(src, t0, T(98), ms=0.0, rate=round(min(1, clen / d), 3), grade="matte", push=None,
                        box=(k * 640, 0, 640, 1080), cam_extra="clip-path:inset(0% 100% 0% 0%);")
    s.js.append(f'tl.fromTo("#{cam2}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
                f'duration: 0.24, ease: "expo.out" }}, {r3(s.L(t0))});')
    s.numeral(num, t0 + 0.06, T(98), x=k * 640 + 320, y=560, size=520)
    sfx("whoosh-short.mp3", t0, 0.22)
SCENES.append(s)
sfx("whoosh-short.mp3", 38.88, 0.22)
sfx("pop.mp3", T(83), 0.18)
for tt in (T(86) + 0.1, T(86) + 0.45, T(90)):
    sfx("click.mp3", tt, 0.22)
sfx("pop.mp3", T(93), 0.18)
sfx("pop.mp3", T(93) + 0.18, 0.16)
sfx("pop.mp3", T(94), 0.18)
sfx("click-soft.mp3", T(95), 0.30)
cap([[W(80, "M", "the")]], T(81), x=170, y=200, align="left")
cap([[W(82, "M", "kid")]], T(83), x=1760, y=930, align="right")
cap([[W(83, "M", "everyone")]], T(84))
cap([[W(84, "BI", "laughed"), W(85, "S", "at")]], T(86), y=560)
cap([[W(86, "S", "is"), W(87, "S", "now"), W(88, "S", "one"), W(89, "S", "of"), W(90, "S", "the"), W(91, "S", "most")],
     [W(92, "B", "respected")]], T(93), y=560)
cap([[W(93, "S", "actors"), (" in", T(93) + 0.18, "S")], [W(94, "B", "Hollywood.")]], T(95), y=560)
cap([[W(95, "PS", "and")]], T(96), kind="paper")
cap([[W(96, "PB", "this"), W(97, "PB", "year?")]], 44.85, kind="paper")

# ---------------- S10 chapter 1: The Odyssey ----------------
s = Scene("s10", T(98), T(113))
# panels 2 and 3 slide off to the right while panel 1 opens to full frame
for k, (src, clen) in enumerate([("t_prime.mp4", 2.5), ("t_dune.mp4", 0.95)], start=1):
    cam2, vid = s.video(src, T(98), T(98) + 0.4, ms=0.8, grade="matte", push=None, box=(k * 640, 0, 640, 1080))
    s.js.append(f'tl.fromTo("#{cam2}", {{ x: 0 }}, {{ x: 1300, duration: 0.34, ease: "power3.in" }}, 0);')
cam, vid = s.video("c_antinous_fire.mp4", T(98), T(101), ms=0.0, grade="matte", push=None,
                   cam_extra="clip-path:inset(0% 66.67% 0% 0%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 66.67% 0% 0%)", scale: 1.0 }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'scale: 1.0, duration: 0.36, ease: "power3.inOut" }}, 0);')
s.js.append(f'tl.to("#{cam}", {{ scale: 1.05, duration: {r3(T(101) - T(98) - 0.36)}, ease: "none" }}, 0.36);')
s.numeral("1", T(98), T(101), x=1500, y=470, size=600)
s.paper(T(101), T(103))
s.image("nolan.jpg", T(101), T(103), grade="matte", box=(560, 90, 800, 900), card=True, rot=-1.5, drop=True)
s.paper(T(103), T(105))
s.image("od_poster.jpg", T(103), T(105), grade="matte", box=(640, 20, 640, 960), card=True, rot=1, drop=True)
s.video("c_antinous_feast.mp4", T(105), T(107), grade="matte", push=(1.0, 1.05))
s.video("c_antinous_arch.mp4", T(107), T(107) + 0.95, grade="matte", push=(1.0, 1.06))
s.video("c_antinous_fire.mp4", T(107) + 0.95, T(113), ms=2.6, grade="matte", push=(1.04, 1.0))
s.neg(T(107) + 0.95, 3)
SCENES.append(s)
sfx("whoosh.mp3", T(98), 0.32)
sfx("pop.mp3", T(101), 0.18)
sfx("pop.mp3", T(103), 0.18)
sfx("whoosh-short.mp3", T(105), 0.22)
sfx("whoosh-short.mp3", T(107) + 0.95, 0.24)
cap([[W(98, "S", "he"), W(99, "S", "walked"), W(100, "S", "into")]], T(101), x=1500, y=900)
cap([[W(101, "S", "Christopher")], [W(102, "B", "Nolan's")]], T(103), y=560)
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
s.video("c_prime_title.mp4", T(115), T(117), grade="vhs", push=(1.0, 1.04))
s.video("c_hansen.mp4", T(117), T(122), ms=0.6, grade="vhs", push=(1.0, 1.05))
s.video("c_schedule.mp4", T(122), T(123), grade="vhs", push=(1.0, 1.05))
s.video("c_stinghouse.mp4", T(123), T(128), grade="vhs", push=(1.0, 1.04))
s.video("c_chat.mp4", T(128), T(129), grade="glitch", push=(1.0, 1.06))
s.video("c_hiddencam.mp4", T(129), T(130), grade="glitch", push=(1.0, 1.06))
s.video("c_strobeface.mp4", T(130), 57.80, grade="vhs", push=(1.0, 1.06))
s.image("pt_pink.jpg", 57.80, 59.90, grade="vhs", push=(1.0, 1.07))
SCENES.append(s)
sfx("whoosh.mp3", T(113), 0.30)
sfx("glitch-1.mp3", T(115), 0.30)
sfx("glitch-3.mp3", T(122), 0.35)
sfx("glitch-1.mp3", T(128), 0.32)
sfx("click.mp3", T(129), 0.26)
sfx("glitch-3.mp3", 57.80, 0.35)
cap([[W(113, "S", "then"), W(114, "S", "came")]], T(115), x=1500, y=900)
cap([[W(117, "S", "with"), W(118, "S", "Pattinson")]], T(119), x=1780, y=840, align="right")
cap([[W(119, "S", "playing"), W(120, "S", "a")]], T(121), x=1780, y=840, align="right")
cap([[W(121, "BI", "television")]], T(122), x=1780, y=800, align="right")
cap([[W(122, "B", "journalist")]], T(123), y=880)
cap([[W(123, "S", "at"), W(124, "S", "the"), W(125, "S", "center"), W(126, "S", "of")]], T(127), y=880)
cap([[W(127, "BI", "controversial")]], T(128), y=860)
cap([[W(128, "XL", "predator")]], T(129), y=860)
cap([[W(129, "M", "sting")]], T(130), y=560)
cap([[W(130, "BI", "operations.")]], 57.80, y=860)
cap([[("…don't you have a seat right there?", 57.92, "R")]], 59.90, y=160)

# ---------------- S12 chapter 3: Dune ----------------
s = Scene("s12", 59.90, T(140))
cam, vid = s.video("c_scytale.mp4", 59.90, T(133), ms=0.0, grade="matte", push=None,
                   cam_extra="clip-path:inset(0% 0% 0% 66.67%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 0% 0% 66.67%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.36, ease: "power3.inOut" }}, 0);')
s.numeral("3", 59.90, T(133), x=1500, y=470, size=600)
s.video("c_scytale.mp4", T(133), T(138), ms=1.2, grade="matte", push=(1.0, 1.05))
s.image("dune_scy.jpg", T(138), T(140), grade="matte", push=(1.0, 1.05), pos="50% 30%")
s.neg(T(139), 3)
SCENES.append(s)
sfx("whoosh.mp3", 59.90, 0.30)
sfx("impact-bass-1.mp3", T(139), 0.45)
cap([[W(131, "S", "and"), W(132, "S", "now")]], T(133), x=1500, y=900)
cap([[W(133, "S", "he's"), W(134, "S", "closing"), W(135, "S", "out")]], T(136), y=880)
cap([[W(136, "S", "the"), W(137, "S", "year")]], T(138), y=880)
cap([[W(138, "S", "with")], [W(139, "XL", "Dune.")]], T(140), x=1800, y=640, align="right")

# ---------------- S13 payoff + end card ----------------
s = Scene("s13", T(140), DUR)
strobe = ["solo02.jpg", "gt_purple.jpg", "f_cedric.jpg", "tn_desert.jpg", "bt_bruce.jpg", "mk_portal.jpg",
          "pt_smile.jpg", "f_scytale.jpg", "f_devil.jpg", "lh_portrait.jpg"]
st0, st1 = T(140), T(144)
stp = round((st1 - st0) / len(strobe), 3)
for k, im in enumerate(strobe):
    a = round(st0 + k * stp, 3)
    b = round(st0 + (k + 1) * stp, 3) if k < len(strobe) - 1 else st1
    s.image(im, a, b, grade="matte", push=(1.05, 1.0))
    sfx("key-press.mp3", a, 0.18)
tiles = ["f_edward_cu.jpg", "gt_neon.jpg", "lh_soot.jpg", "tn_red.jpg", "bt_cowl.jpg", "mk_helmet.jpg", "f_hansen.jpg",
         "f_scytale.jpg", "f_king.jpg", "f_devil.jpg", "f_rover.jpg", "f_queen.jpg", "f_damsel.jpg", "f_dali.jpg",
         "f_bruce.jpg", "f_drama.jpg"]
s.grid(tiles, 4, 4, T(144), T(147))
s.grid(tiles[:9], 3, 3, T(147), T(149))
s.grid(tiles[:4], 2, 2, T(149), T(151))
# "one box": paper with a single framed square
s.paper(T(151), T(157))
s.image("f_edward_cu.jpg", T(151), T(157), grade="film8mm", box=(660, 240, 600, 600), card=True, rot=0, drop=True,
        push=(1.0, 1.04))
s.whiteflash(T(157), 0.22, 0.9)
cam, vid = s.video("h_edward.mp4", T(157), T(158), grade="film8mm", push=None, box=(0, 0, 960, 1080))
cam, vid = s.video("h_batman.mp4", T(157), T(158), grade="matte", push=None, box=(960, 0, 960, 1080))
s.paper(T(158), DUR)
SCENES.append(s)
for i in (144, 147, 149):
    sfx("pop.mp3", T(i), 0.18)
sfx("impact-bass-1.mp3", T(152), 0.28)
sfx("whoosh-cinematic.mp3", T(156), 0.30)
sfx("whoosh-short.mp3", T(157), 0.26)
sfx("click-soft.mp3", T(158), 0.30)
sfx("impact-bass-1.mp3", 71.95, 0.30)
cap([[W(140, "B", "Pattinson")]], T(141), y=560)
cap([[W(141, "S", "keeps"), W(142, "S", "choosing")]], T(143), y=880)
cap([[W(143, "XLI", "roles")]], T(144), y=560)
cap([[W(144, "M", "that"), W(145, "M", "stop"), W(146, "M", "anyone")]], T(147), y=560)
cap([[W(147, "M", "from"), W(148, "M", "putting"), W(149, "M", "him")]], T(150), y=560)
cap([[W(150, "PS", "in"), W(151, "PS", "one")]], T(152), kind="paper", y=950)
cap([[W(152, "PB", "box,")]], T(153), kind="paper", y=950)
cap([[W(153, "PS", "and"), W(154, "PS", "that")]], T(155), kind="paper", y=950)
cap([[W(155, "PS", "post")]], T(156), kind="paper", y=950)
cap([[W(156, "XL", "Twilight")]], T(157), y=560)
cap([[W(157, "XLI", "reinvention")]], T(158), y=560)
cap([[W(158, "PS", "might"), W(159, "PS", "be")]], T(160), kind="paper")
cap([[W(160, "PS", "one"), W(161, "PS", "of"), W(162, "PS", "the")]], T(163), kind="paper")
cap([[W(163, "PXL", "best")]], T(164), kind="paper")
cap([[W(164, "PS", "we've"), W(165, "PS", "ever")]], T(166), kind="paper")
cap([[W(166, "PXL", "seen.")]], 71.95, kind="paper", exit="blurout")
cap([[("Robert", 72.05, "PB")], [("Pattinson", 72.20, "PB")]], DUR, kind="paper", lh=0.84)
cap([[("2008 — 2026", 72.55, "PS")]], DUR, kind="paper", y=860)

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
        auds.append(f'<audio id="sfx{k:02d}" class="clip" src="assets/audio/sfx/{name}" data-start="{r3(start)}" '
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
    # grain: the registry component's markup inside a scene template, at 6 % opacity
    g = open(f"{COMP}/components/grain-overlay.html").read()
    m = re.search(r'url\("(data:image/svg\+xml[^"]+)"\)', g)
    data_url = m.group(1) if m else ""
    frames = int(DUR * 30)
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
