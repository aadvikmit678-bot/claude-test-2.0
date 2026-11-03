#!/usr/bin/env python3
"""Generate the HyperFrames compositions for the Pattinson edit (v5, new voiceover) from one shot/caption table.

v5 is built segment by segment with the user; this file holds the segments built so far and DUR is the end of
the last one. Typography: only upright Instrument Serif (with the glow) and the bold Helvetica-style sans.

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
PRJ = f"{ROOT}/pattinson-v5"
COMP = f"{PRJ}/compositions"
DUR = 23.41  # end of the segments built so far (segments 1-2: up to "the vampire kid.")
LEAD = 0.07  # captions and cuts arrive 2 frames before the word

GR = json.load(open(f"{PRJ}/tools/gradings.json"))
WORDS = json.load(open(f"{PRJ}/tools/words_v5.json"))


def _derive(base, adjust=None, effects=None, details=None, intensity=None):
    g = json.loads(GR[base])
    g["adjust"].update(adjust or {})
    g["effects"].update(effects or {})
    g["details"].update(details or {})
    if intensity is not None:
        g["intensity"] = intensity
    return json.dumps(g, separators=(",", ":"))


# one-off looks derived from the validated base payloads (values inside the documented ranges)
GR["rgbsplit"] = _derive("matte", adjust={"exposure": 0.9, "contrast": -0.22, "saturation": -0.35},
                         effects={"chromaticAberration": 0.75, "chromaticAngle": 0.0})
# the user asked for textures at 20-30 % at most: the texture effects themselves are scaled down
# (a payload's "intensity" only scales its colour grade, not the print/tape/glitch effects)
def _soften(base, scale, keys):
    g = json.loads(GR[base])
    for k in keys:
        g["effects"][k] = round(g["effects"][k] * scale, 3)
    return json.dumps(g, separators=(",", ":"))


GR["halftone_soft"] = _soften("halftone", 0.28, ["halftone"])
# first-10s v3 (user: "the screen feels more curved, like a fish-eye"): curvature alone, as lens geometry
GR["curved"] = _derive("matte", effects={"crtCurvature": 0.22})
# segment 2: halftone at half the v3 strength, and the 8mm film look with much less dust, grain and vignette
GR["halftone_faint"] = _soften("halftone", 0.15, ["halftone"])
_fs = json.loads(GR["film8mm"])
_fs["effects"]["filmArtifacts"] = 0.22
_fs["details"]["grain"] = 0.14
_fs["details"]["vignette"] = 0.18
GR["film_soft"] = json.dumps(_fs, separators=(",", ":"))
GR["vhs_soft"] = _soften("vhs", 0.55, ["chromaBleed", "tapeDamage", "tapeTracking", "scanlines", "chromaticAberration"])
GR["glitch_soft"] = _soften("glitch", 0.65, ["tapeDamage", "tapeTracking", "scanlines", "chromaticAberration",
                                             "digitalGlitch", "digitalGlitchColorSplit", "digitalGlitchLineTear",
                                             "digitalGlitchBlockAmount"])
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
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-800-Italic.woff2') format('woff2'); font-weight: 800; font-style: italic; }
"""

GLOW_REST = "0 0 12px rgba(255,255,255,0.55), 0 0 34px rgba(255,255,255,0.22), 0 3px 10px rgba(0,0,0,0.42)"
GLOW_BLOOM = "0 0 34px rgba(255,255,255,0.95), 0 0 90px rgba(255,255,255,0.55), 0 3px 10px rgba(0,0,0,0)"
# Instrument Serif glow (user's second reference, the "AI cold war" edit): a soft white halo that stays on every
# serif word; words write on after a white box flash, hero words burst in as a blown-out bloom for one frame
SERIF_REST = ("0 0 14px rgba(255,255,255,0.62), 0 0 42px rgba(255,255,255,0.30), 0 0 90px rgba(255,255,255,0.12), "
              "0 3px 10px rgba(0,0,0,0.35)")
SERIF_BLOOM = ("0 0 22px rgba(255,255,255,1), 0 0 60px rgba(255,255,255,0.95), 0 0 130px rgba(255,255,255,0.7), "
               "0 3px 10px rgba(0,0,0,0)")
SERIF_SOFT = ("0 0 18px rgba(255,255,255,0.85), 0 0 50px rgba(255,255,255,0.45), 0 0 100px rgba(255,255,255,0.18), "
              "0 3px 10px rgba(0,0,0,0.2)")
F1 = 1 / 30  # one frame

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
              pushease="none", style="", vars_style="", z=None, cam_extra="", card=False):
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
            f'<video id="{vid}" class="{"clip card" if card else "clip"}" src="assets/clips/{src}" muted playsinline '
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

    def lightstreak(self, t, frames=3, y=540, h=150):
        """Horizontal white light streak across the frame for a few frames (second reference, 10.5 s)."""
        lid = self.uid("streak")
        self.els.append(f'<div id="{lid}" class="clip streak" {self.timed(t, t + frames / 30)} data-track-index="5" '
                        f'style="top:{y - h // 2}px;height:{h}px;z-index:{self.nz()}"></div>')

    def block(self, t, frames, box, color, blend="normal", opacity=1.0):
        """A flat colour block for glitch frames (second reference: the yellow and cyan blocks on "Dario")."""
        bid = self.uid("blk")
        x, y, w, h = box
        self.els.append(f'<div id="{bid}" class="clip solid" {self.timed(t, t + frames / 30)} data-track-index="5" '
                        f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};opacity:{opacity};'
                        f'mix-blend-mode:{blend};z-index:{self.nz()}"></div>')

    def flare(self, t, frames=3, corner="tl"):
        """A soft white light flare in a corner for a few frames (second reference: the flare as "Dario" lands)."""
        fid = self.uid("flare")
        pos = {"tl": "left:-240px;top:-260px", "tr": "right:-240px;top:-260px"}[corner]
        self.els.append(f'<div id="{fid}" class="clip flare" {self.timed(t, t + frames / 30)} data-track-index="5" '
                        f'style="{pos};z-index:{self.nz()}"></div>')
        self.js.append(f'tl.fromTo("#{fid}", {{ opacity: 1 }}, {{ opacity: 0, duration: {r3(frames / 30)}, ease: "power2.in" }}, '
                       f'{self.at(t)});')

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
        fs = "normal"  # v5: upright type only
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
                glow=True, align="center", italic=False, ink=False, tick=None):
        """Rolling counter: steps = [(value, t), ...]; each value is its own timed element."""
        for k, (val, t) in enumerate(steps):
            t_next = steps[k + 1][1] if k < len(steps) - 1 else t_end
            anim = ("ink" if ink else "glow") if k == 0 else "none"
            self.text(val, t, t_next, x, y, size, family=family, weight=weight, color=color, glow=glow,
                      align=align, anim=anim, italic=italic)
            if tick:
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
  #root .streak {{ position: absolute; left: 0; width: 1920px; background: linear-gradient(180deg, rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.85) 38%, #ffffff 50%, rgba(255,255,255,0.85) 62%, rgba(255,255,255,0) 100%);
    box-shadow: 0 0 80px 30px rgba(255,255,255,0.55); }}
  #root .pbox {{ position: absolute; background: #ffffff; filter: blur(3px);
    box-shadow: 0 0 22px 4px rgba(255,255,255,0.85), 0 0 60px rgba(255,255,255,0.4); }}
  #root .flare {{ position: absolute; width: 900px; height: 760px; border-radius: 50%;
    background: radial-gradient(closest-side, rgba(255,255,255,0.95), rgba(255,255,255,0.45) 45%, rgba(255,255,255,0) 100%); }}
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
    "MI": ("Instrument Serif", 400, True, 180, "#F7F4F7", True),
    "FS": ("Instrument Serif", 400, False, 190, "#F7F4F7", True),   # full-width one-line serif
    "FSL": ("Instrument Serif", 400, False, 250, "#F7F4F7", True),
    "FSI": ("Instrument Serif", 400, True, 220, "#F7F4F7", True),
    "FN": ("Instrument Serif", 400, False, 312, "#F7F4F7", True),   # the one-line name title
    "C": ("Inter Tight", 800, False, 96, "#F7F4F7", True),  # cold-open cover words
    "CI": ("Inter Tight", 800, True, 104, "#F7F4F7", True),    # v4 cold open: bold italic sans
    "CIB": ("Inter Tight", 800, True, 150, "#F7F4F7", True),
    "CS": ("Instrument Serif", 400, True, 118, "#F7F4F7", True),
    "CB": ("Instrument Serif", 400, True, 230, "#F7F4F7", True),
}

STY["OS"] = ("Instrument Serif", 400, False, 150, "#F7F4F7", True)    # cold open, The Odyssey line
STY["OSB"] = ("Instrument Serif", 400, False, 230, "#F7F4F7", True)
STY["LS"] = ("Instrument Serif", 400, False, 96, "#F7F4F7", True)     # small serif in a small-big lockup
STY["FNS"] = ("Instrument Serif", 400, False, 250, "#F7F4F7", True)   # a stacked name ("Edward / Cullen.")
STY["SM"] = ("Inter Tight", 700, False, 64, "#F7F4F7", True)          # small line under a counter
STY["NUM"] = ("Inter Tight", 800, False, 300, "#F7F4F7", True)        # a big number in a lockup ("15 years")
for _k, _v in list(STY.items()):  # v5 (user): no slanted type anywhere
    STY[_k] = (_v[0], _v[1], False, _v[3], _v[4], _v[5])
# v5 (user): black words on paper are bold Helvetica (as in the F1 reference), punch words just bigger
STY["PM"] = ("Inter Tight", 800, False, 130, "#0B0B0B", False)
STY["PB"] = ("Inter Tight", 800, False, 160, "#0B0B0B", False)
STY["PXL"] = ("Inter Tight", 800, False, 200, "#0B0B0B", False)

CAPS = []  # list of dicts


def cap(lines, end, x=960, y=540, align="center", kind=None, start=None, exit=None, lh=0.92, exit_first=None):
    """lines: list of lists of (text, time, style). time = global appear time."""
    first = min(tok[1] for line in lines for tok in line)
    if start is None:
        st0 = lines[0][0][2]
        fam, _, _, size, _, glow = STY[st0]
        # a serif line word's box flashes two frames before the word, so the group starts two frames early
        start = first - 4 / 30 if (fam == "Instrument Serif" and glow and size < 200 and kind not in ("paper", "name")) else first
    CAPS.append(dict(lines=lines, start=round(start, 3), end=end, x=x, y=y,
                     align=align, kind=kind, exit=exit, lh=lh, exit_first=exit_first))


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
                fk = sum(len(l) for l in g["lines"][:li]) + wi  # word order within the group
                fam, wt, it, size, color, glow = STY[st]
                sid = f"{gid}-w{li}{wi}"
                shadow = f"text-shadow:{GLOW_REST};" if glow else ""
                if st.startswith("FS"):
                    shadow += "-webkit-text-stroke:1.4px #F7F4F7;"  # a heavier serif for the full-width titles
                if st == "FN":
                    shadow += "-webkit-text-stroke:3px #F7F4F7;"  # bold weight for the name title
                track = "-0.035em" if fam == "Inter Tight" else "-0.02em"
                if st == "SH":
                    track = "-0.01em"
                ml = "" if wi == 0 else ("margin-left:0.26em;" if fam == "Inter Tight" else "margin-left:0.2em;")
                serif_glow = fam == "Instrument Serif" and glow and g["kind"] != "paper"
                lt = round(tt - t0, 3)
                if serif_glow:
                    stroke = ""
                    if st.startswith("FS"):
                        stroke = "-webkit-text-stroke:1.4px #F7F4F7;"
                    if st == "FN":
                        stroke = "-webkit-text-stroke:3px #F7F4F7;"
                    if st == "FNS":
                        stroke = "-webkit-text-stroke:2.4px #F7F4F7;"
                    spans.append(
                        f'<span id="{sid}" class="w ws" style="{ml}font-family:\'{fam}\';font-weight:{wt};font-style:normal;'
                        f'font-size:{size}px;color:{color};letter-spacing:{track};">'
                        f'<span id="{sid}-f" class="fl"></span>'
                        f'<span id="{sid}-t" class="wt" style="opacity:0;text-shadow:{SERIF_REST};{stroke}">{esc(text)}</span></span>')
                    at = r3(t0 + lt)
                    if g["kind"] == "name":
                        # "Dario Amodei": the first word blooms in; two glitch frames (first word goes dark, a pale-
                        # yellow block where the second word lands); the second word blooms in; exit word by word
                        if fk == 1:
                            js.append(f'tl.set("#{sid}-f", {{ opacity: 1, backgroundColor: "#EFE3A0", boxShadow: "none" }}, {r3(t0 + lt - 2 * F1)});')
                            js.append(f'tl.set("#{sid}-f", {{ opacity: 0 }}, {at});')
                            first = f"{gid}-w00-t"
                            js.append(f'tl.set("#{first}", {{ color: "#0d0d0d", textShadow: "none", webkitTextStrokeColor: "#0d0d0d" }}, {r3(t0 + lt - 2 * F1)});')
                            js.append(f'tl.set("#{first}", {{ color: "#F7F4F7", textShadow: "{SERIF_REST}", webkitTextStrokeColor: "#F7F4F7" }}, {at});')
                        js.append(f'tl.set("#{sid}-t", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {at});')
                        js.append(f'tl.set("#{sid}-t", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {r3(t0 + lt + F1)});')
                        js.append(f'tl.set("#{sid}-t", {{ scale: 1.005, filter: "blur(2.5px)" }}, {r3(t0 + lt + 3 * F1)});')
                        js.append(f'tl.set("#{sid}-t", {{ scale: 1, filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {r3(t0 + lt + 4 * F1)});')
                        if fk == 0 and g.get("exit_first") is not None:
                            js.append(f'tl.set("#{sid}-t", {{ opacity: 0 }}, {r3(g["exit_first"])});')
                    elif size >= 200:
                        # hero word, stepped like the reference's "AI" / "timing": one blown-out frame, three soft-focus
                        # frames, then crisp with the lasting halo
                        js.append(f'tl.set("#{sid}-t", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {at});')
                        js.append(f'tl.set("#{sid}-t", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {r3(t0 + lt + F1)});')
                        js.append(f'tl.set("#{sid}-t", {{ scale: 1.005, filter: "blur(2.5px)" }}, {r3(t0 + lt + 3 * F1)});')
                        js.append(f'tl.set("#{sid}-t", {{ scale: 1, filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {r3(t0 + lt + 4 * F1)});')
                    else:
                        # line word: a glowing white box flashes for two frames where the word lands, then it writes on
                        b0 = max(t0, t0 + lt - 4 * F1)
                        js.append(f'tl.set("#{sid}-f", {{ opacity: 1, filter: "blur(3px)" }}, {r3(b0)});')
                        js.append(f'tl.set("#{sid}-f", {{ filter: "blur(0px)" }}, {r3(b0 + F1)});')
                        js.append(f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(max(b0 + 2 * F1, t0 + lt - F1))});')
                        js.append(f'tl.set("#{sid}-t", {{ opacity: 1, filter: "blur(8px)", textShadow: "{SERIF_BLOOM}" }}, {at});')
                        js.append(f'tl.set("#{sid}-t", {{ filter: "blur(3px)", textShadow: "{SERIF_SOFT}" }}, {r3(t0 + lt + F1)});')
                        js.append(f'tl.set("#{sid}-t", {{ filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {r3(t0 + lt + 3 * F1)});')
                    continue
                spans.append(
                    f'<span id="{sid}" class="w" style="{ml}font-family:\'{fam}\';font-weight:{wt};'
                    f'font-style:{"italic" if it else "normal"};font-size:{size}px;color:{color};'
                    f'letter-spacing:{track};{shadow}">{esc(text)}</span>')
                if g["kind"] == "paper" or st in ("PS", "PM", "PB", "PXL"):
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.14 }}, {{ opacity: 1, scale: 1, duration: 0.4, '
                              f'ease: "expo.out", immediateRender: true }}, {r3(t0 + lt)});')
                    js.append(f'tl.set("#{sid}", {{ opacity: 1 }}, {r3(t0 + lt)});')
                elif st == "SH":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.16, '
                              f'ease: "back.out(2)" }}, {r3(t0 + lt)});')
                elif g["kind"] == "streak":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0.85, scaleX: 1.9, x: -24, filter: "blur(12px)", '
                              f'textShadow: "{GLOW_BLOOM}" }}, {{ opacity: 1, scaleX: 1, x: 0, filter: "blur(0px)", '
                              f'textShadow: "{GLOW_REST}", duration: 0.1, ease: "steps(3)" }}, {r3(t0 + lt)});')
                elif g["kind"] == "name":
                    # the title glow: a bigger bloom that tracks in as it sharpens
                    dx = -90 if wi == 0 else 90  # the words glide in towards each other (transform, not tracking)
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 1.2, x: {dx}, filter: "blur(28px)", '
                              f'textShadow: "{GLOW_BLOOM}" }}, {{ opacity: 1, scale: 1, x: 0, filter: "blur(0px)", '
                              f'textShadow: "{GLOW_REST}", duration: 0.6, ease: "expo.out" }}, {r3(t0 + lt)});')
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
  #root .w {{ display: inline-block; white-space: nowrap; line-height: 0.95; position: relative; }}
  #root .w .wt {{ display: inline-block; position: relative; }}
  #root .w .fl {{ position: absolute; left: -0.03em; right: -0.03em; top: 0.22em; bottom: 0.10em; opacity: 0;
    background: #ffffff; box-shadow: 0 0 16px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.45); }}
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
        "glitch-1.mp3": 0.22, "glitch-2.mp3": 0.2, "glitch-3.mp3": 0.24, "whoosh-cinematic.mp3": 2.54,
        "tv-blip-soft.wav": 0.257}
SFXDUR = {"whoosh.mp3": 0.57, "whoosh-short.mp3": 0.57, "impact-bass-1.mp3": 2.12, "impact-bass-2.mp3": 2.59,
          "pop.mp3": 0.72, "click.mp3": 0.37, "click-soft.mp3": 0.37, "key-press.mp3": 0.4, "sparkle.mp3": 1.8,
          "glitch-1.mp3": 2.64, "glitch-2.mp3": 3.5, "glitch-3.mp3": 3.1, "whoosh-cinematic.mp3": 5.54,
          "tv-blip-soft.wav": 0.5}


def sfx(name, t, vol=0.35, ms=0.0, dur=None):
    SFX.append((name, t, vol, ms, dur))


# ==================================================================================================
# SEGMENT 1 (0 - 10.85): cold open, then "Robert Pattinson is on a generational run, and honestly,
# nobody saw it coming."
# ==================================================================================================

# ---------------- S01 cold open: Venice "beggars" -> The Odyssey line ----------------
s = Scene("s01", 0.0, 5.40)
camA, vA = s.video("c_start_clean.mp4", 0.0, 1.53, ms=0.0, push=None)
# snap zoom on the shouted "beggars" (reference: snap zoom into the name tag in the cold open)
s.scale_keys(camA, [(0.0, 1.0, 1.03, 0.98, "none"), (0.98, 1.03, 1.12, 0.14, "expo.out"), (1.12, 1.12, 1.15, 0.41, "none")])
s.video("c_start_clean.mp4", 1.53, 3.10, ms=1.53, push=(1.0, 1.04))
camC, vC = s.video("c_start_clean.mp4", 3.10, 5.40, ms=3.10, push=None)
s.scale_keys(camC, [(3.10, 1.0, 1.03, 0.73, "none"), (3.83, 1.03, 1.12, 0.14, "expo.out"), (3.97, 1.12, 1.16, 1.43, "none")])
s.neg(3.10, 3)
SCENES.append(s)
sfx("whoosh-short.mp3", 0.98, 0.16)
sfx("whoosh-short.mp3", 3.10, 0.28)
sfx("whoosh-short.mp3", 3.83, 0.14)
# v5 (user): the reference's word-by-word glow captions ("and / he'll be / the / first / to / tell / you"): each
# word blooms in centred about two frames before it is spoken and replaces the last. Venice in the bold
# Helvetica-style sans; the Odyssey line in upright Instrument Serif with glow, written word by word.
# Word onsets measured from the dialogue audio; captions sit over the inpainted caption band.
# first-10s v2 (user): "Somebody get these" builds word by word on one line exactly like "out of here!" does;
# "beggars" lands on its own in between (the punch word, as in the Odyssey line)
cap([[("Somebody", 0.05, "S"), ("get", 0.41, "S"), ("these", 0.53, "S")]], 0.93, y=548)
cap([[("beggars", 0.93, "S")]], 1.25, y=548)
cap([[("out", 1.25, "S"), ("of", 1.39, "S"), ("here!", 1.49, "S")]], 2.30, y=548)
# The Odyssey line writes on like the user's second reference: a glowing white box flashes two frames where each
# word lands, then the word blooms in and keeps a soft halo; "beggars" bursts in as a hero word
cap([[("Somebody", 3.20, "OS"), ("get", 3.37, "OS"), ("these", 3.53, "OS")]], 3.77, y=575, start=3.10)
cap([[("beggars", 3.77, "OSB")]], 4.183, y=580)
cap([[("out", 4.29, "OS"), ("of", 4.43, "OS"), ("here.", 4.59, "OS")]], 5.05, y=575, start=4.183)

# ---------------- S02 "Robert Pattinson is on a generational run, and honestly, nobody saw it coming." ----------------
s = Scene("s02", 5.40, T(13))
# a 3x3 box grid builds on black under the one-line glowing name: each box is pure white for one frame, then plays
# a clip; centre first, then corners, then edges, a new box every two frames; it ends on a white flash
DARK = "--hf-color-grading-exposure: -0.55;"
s.solid(5.40, T(2), "#000000")
grid_order = [(1, 1), (0, 0), (2, 2), (0, 2), (2, 0), (0, 1), (2, 1), (1, 0), (1, 2)]
grid_clips = [("c_carpet_bg.mp4", 0.5), ("c_goodtime.mp4", 0.05), ("c_hansen.mp4", 0.2), ("c_kimmel_laugh2.mp4", 0.0),
              ("c_lighthouse.mp4", 0.1), ("c_scytale.mp4", 1.0), ("c_batroof.mp4", 0.0), ("c_mickey.mp4", 0.3),
              ("c_antinous_feast.mp4", 0.2)]
for k, ((row, col), (clip, ms)) in enumerate(zip(grid_order, grid_clips)):
    t0 = round(5.40 + k * 2 / 30, 3)
    box = (col * 640, row * 360, 640, 360)
    cam, vid = s.video(clip, t0, T(2), ms=ms, grade="matte", push=None, box=box, vars_style=DARK)
    s.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.08 }}, {{ scale: 1.0, duration: 0.3, ease: "expo.out" }}, {s.at(t0)});')
    fl = s.uid("box")
    s.raw(f'<div id="{fl}" class="clip solid" {s.timed(t0, t0 + 1 / 30)} data-track-index="5" '
          f'style="left:{box[0]}px;top:{box[1]}px;width:640px;height:360px;background:#ffffff;z-index:{s.nz()}"></div>')
# the name lands like "Dario Amodei" in the second reference: a corner flare as "Robert" blooms in, two glitch
# frames (the word goes dark, a cyan patch over his face, a pale-yellow block where "Pattinson" lands), then
# "Pattinson"; "Robert" leaves first; a horizontal light streak wipes into the next beat
s.flare(5.40, frames=3, corner="tl")
s.block(round(T(1) - 2 / 30, 3), 2, (800, 400, 330, 300), "#63E6E2", blend="difference")
s.lightstreak(round(T(2) - 2 / 30, 3), frames=3)
# "is on a generational run" (first-10s v3, the user's notes + the Hemant Taneja wall measured frame by frame):
#  - the shot eases back from full frame to a centred window (Legora: power4.out, ~0.9 s)
#  - the cut-outs and four role clips pop out from behind the window in low-frame-rate steps, land as white
#    boxes and turn into pictures; the role tiles are PLAYING VIDEO and one blows out for a frame, like the
#    Hemant Taneja wall, so the wall is never still
#  - the wall sits on a gentle dome (outer edges fall away, like a fish-eye); the dome deepens and the window
#    bends into a curved screen while the whole wall keeps slowly pulling back, then the accelerating pan out
#    carries into the run cut
FR = 0.66
PICS = [  # source, centre x, centre y, w, h, tilt, video media-start, video rate
    ("slate_drama.jpg", 300, 190, 460, 142, -4, None, None),
    ("c_tenet_b.mp4", 1745, 545, 300, 190, 3, 0.0, 0.45),
    ("slate_prime.jpg", 300, 895, 460, 142, 3, None, None),
    ("c_mickey.mp4", 760, 105, 300, 170, -2, 0.3, 1.0),
    ("slate_odyssey.jpg", 1620, 200, 460, 142, 4, None, None),
    ("c_cowl.mp4", 175, 560, 300, 190, -3, 0.0, 1.0),
    ("slate_dune.jpg", 1625, 885, 460, 142, -4, None, None),
    ("c_lighthouse.mp4", 1190, 980, 280, 170, 2, 0.1, 1.0),
]
PIC_T0 = round(T(3) + 3 * F1, 3)            # the first picture lands ~0.2 s after the shot starts easing back
INV = round(PIC_T0 + 8 * 2 * F1 + 0.10, 3)  # the wall inverts for two frames once all eight are in
PAN = 0.30                                  # the accelerating pan out, ending on the cut into "run,"
CURVE_T0, CURVE_T1 = round(T(5) - 0.08, 3), round(T(6) - PAN, 3)  # the dome deepens / the wall pulls back here


def dome(cx, cy, f):
    """Placement on a convex dome: outer edges recede (rotateY>0 recedes the right edge, rotateX>0 the top)."""
    nx, ny = (cx - 960) / 960, (cy - 540) / 540
    return dict(rotationY=round(30 * nx * f, 2), rotationX=round(-18 * ny * f, 2), z=round(-170 * (nx * nx + ny * ny) * f, 1))


s.solid(T(2), T(6), "#000000")
grp_first = len(s.els)
pic_els = []
for k, (src, cx, cy, w, h, rot, ms, rate) in enumerate(PICS):  # made first, so they sit behind the centre window
    t0 = round(PIC_T0 + k * 2 * F1, 3)               # one picture every two frames
    box = (cx - w // 2, cy - h // 2, w, h)
    d0, d1 = dome(cx, cy, 0.55), dome(cx, cy, 1.0)
    # the white box pops out from behind the window in three low-frame-rate steps, lands soft then crisp
    bid = s.uid("pbox")
    s.raw(f'<div id="{bid}" class="clip pbox" {s.timed(round(t0 - 4 * F1, 3), t0)} data-track-index="5" '
          f'style="left:{box[0]}px;top:{box[1]}px;width:{w}px;height:{h}px;z-index:{s.nz()}"></div>')
    s.js.append(f'tl.fromTo("#{bid}", {{ x: {round((960 - cx) * 0.8)}, y: {round((540 - cy) * 0.8)}, scale: 0.45, rotation: 0, '
                f'rotationY: 0, rotationX: 0, z: 0 }}, {{ x: 0, y: 0, scale: 1, rotation: {rot}, rotationY: {d0["rotationY"]}, '
                f'rotationX: {d0["rotationX"]}, z: {d0["z"]}, duration: {r3(3 * F1)}, ease: "steps(3)" }}, {s.at(t0 - 4 * F1)});')
    s.js.append(f'tl.set("#{bid}", {{ filter: "blur(0px)" }}, {s.at(t0 - F1)});')
    if src.endswith(".mp4"):
        cam, mid = s.video(src, t0, T(6), ms=ms, rate=rate if rate != 1.0 else None, grade="matte", push=None, box=box,
                           card=True, vars_style="--hf-color-grading-exposure: 0.85;")
    else:
        cam, mid = s.image(src, t0, T(6), grade="matte", push=None, box=box, card=True, pos="50% 35%",
                           vars_style="--hf-color-grading-blur: 0; --hf-color-grading-exposure: 0.85;")
    # lands overexposed and a touch big on the dome, settles in two steps
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.06, rotation: {rot}, rotationY: {d0["rotationY"]}, rotationX: {d0["rotationX"]}, '
                f'z: {d0["z"]} }}, {s.at(t0)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0.25 }}, {s.at(t0 + F1)});')
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.0 }}, {s.at(t0 + 2 * F1)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(t0 + 2 * F1)});')
    # the dome deepens and the picture drifts outward as the camera pulls back (parallax: the outer ones move most)
    nx, ny = (cx - 960) / 960, (cy - 540) / 540
    c0 = round(max(CURVE_T0, t0 + 2 * F1), 3)  # a picture that lands late starts deepening on landing
    s.js.append(f'tl.to("#{cam}", {{ rotationY: {d1["rotationY"]}, rotationX: {d1["rotationX"]}, z: {d1["z"]}, '
                f'x: {round(46 * nx)}, y: {round(30 * ny)}, duration: {r3(CURVE_T1 - c0)}, ease: "sine.inOut" }}, '
                f'{s.at(c0)});')
    pic_els.append((cam, mid, cx, cy, t0, src.endswith(".mp4")))
for k, (cam, mid, cx, cy, t0, isvid) in enumerate(pic_els):
    if k in (0, 4, 6):  # a still blinks out for a frame now and then (the reference's flicker)
        s.js.append(f'tl.set("#{mid}", {{ opacity: 0 }}, {s.at(t0 + 0.30)});')
        s.js.append(f'tl.set("#{mid}", {{ opacity: 1 }}, {s.at(t0 + 0.30 + F1)});')
    if not isvid:  # the stills fall out of focus behind the window after the inversion; the video tiles stay sharp
        s.js.append(f'tl.to("#{mid}", {{ "--hf-color-grading-blur": 0.32, duration: 0.24, ease: "power2.out" }}, {s.at(INV + 2 * F1)});')
# one video tile blows out for two frames, like the cyan wash on the Hemant Taneja wall
bl_cam, bl_mid = pic_els[1][0], pic_els[1][1]
s.js.append(f'tl.set("#{bl_mid}", {{ "--hf-color-grading-exposure": 1.5 }}, {s.at(INV + 0.30)});')
s.js.append(f'tl.set("#{bl_mid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(INV + 0.30 + 2 * F1)});')
# the centre window: the flat shot, and the same shot through the curved-screen treatment fading in over it
camG, vG = s.video("c_genbg.mp4", T(2), T(6), grade="matte", push=None,
                   cam_extra="box-shadow: 0 40px 120px rgba(0,0,0,0.7);")
vGc, vGw = s.uid("v"), s.uid("cvw")
s.els[-1] = s.els[-1].replace(
    "</div>",
    f'<div id="{vGw}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:0">'
    f'<video id="{vGc}" class="clip" src="assets/clips/c_genbg.mp4" muted playsinline {s.timed(CURVE_T0, T(6))} '
    f'data-hf-media-start-basis="local" data-media-start="{r3(round(CURVE_T0 - T(2), 3))}" '
    f'data-color-grading="{esc(GR["curved"])}" data-track-index="2" '
    f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover"></video></div></div>', 1)
s.js.append(f'tl.to("#{vGw}", {{ opacity: 1, duration: 0.3, ease: "sine.inOut" }}, {s.at(CURVE_T0)});')
# Legora's ease back: 100 % -> 66 % over 0.9 s, power4.out, drifting 20 px left; then it keeps receding and
# leans back a little (it goes farther in perspective) until the pan
s.js.append(f'tl.fromTo("#{camG}", {{ scale: 1.0, x: 0 }}, {{ scale: {FR}, x: -20, duration: 0.9, ease: "power4.out" }}, {s.at(T(2))});')
s.js.append(f'tl.to("#{camG}", {{ scale: {FR - 0.035}, duration: {r3(T(6) - T(2) - 0.9)}, ease: "none" }}, {s.at(T(2) + 0.9)});')
s.js.append(f'tl.fromTo("#{camG}", {{ rotationY: 0, rotationX: 0 }}, {{ rotationY: -6, rotationX: 3, duration: {r3(CURVE_T1 - CURVE_T0)}, '
            f'ease: "sine.inOut" }}, {s.at(CURVE_T0)});')
# everything made since grp_first moves as one wall, under one perspective (so the dome reads as one curved space)
gid = s.uid("wall")
inner = "".join(s.els[grp_first:])
del s.els[grp_first:]
s.els.append(f'<div class="cam" id="{gid}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
             f'perspective:1400px;perspective-origin:50% 50%;z-index:{s.nz()}">{inner}</div>')
# the wall's camera: drift up and a ~2 deg turn as the pictures land; a continuous slow pull-back from then on;
# then the accelerating pan left into the cut
s.js.append(f'tl.fromTo("#{gid}", {{ y: 0, rotation: 0 }}, {{ y: -16, rotation: -2, duration: 0.3, ease: "power2.out" }}, {s.at(PIC_T0)});')
s.js.append(f'tl.fromTo("#{gid}", {{ scale: 1.0 }}, {{ scale: 0.86, duration: {r3(T(6) - PIC_T0)}, ease: "sine.inOut", '
            f'immediateRender: false }}, {s.at(PIC_T0)});')
s.js.append(f'tl.fromTo("#{gid}", {{ x: 0 }}, {{ x: -230, duration: {PAN}, ease: "power2.in", immediateRender: false }}, {s.at(T(6) - PAN)});')
s.neg(INV, 2)  # the wall inverts for two frames
# "run,": the fast stretch of the user's Batman cut; it arrives still moving left and decelerates (pan continuity);
# x and scale ease together, so the frame stays covered while it slides (needs scale >= 1 + 2x/1920)
camR, vR = s.video("c_run2.mp4", T(6), T(8), grade="matte", push=None, rate=round(1.0 / (T(8) - T(6)), 3))
s.js.append(f'tl.fromTo("#{camR}", {{ x: 220, scale: 1.26 }}, {{ x: 0, scale: 1.03, duration: 0.34, ease: "power2.out" }}, {s.at(T(6))});')
s.js.append(f'tl.to("#{camR}", {{ scale: 1.05, duration: {r3(T(8) - T(6) - 0.34)}, ease: "none" }}, {s.at(T(6) + 0.34)});')
# "and honestly," (user: keep the full-frame talk-show video and the white silhouette; reference: General Catalyst
# opening): his first frame as a glowing white silhouette over the darkened frame, flickering back to the real frame
# for single frames, with glitch boxes; then the clip plays
KS = T(8)
KP = round(KS + 0.42, 3)  # the video starts moving here
s.image("kim2_f0.jpg", KS, KP, grade="matte", push=(1.0, 1.015), vars_style="--hf-color-grading-exposure: -0.95;")
sil_segments = [(KS, round(KS + 0.14, 3)), (round(KS + 0.175, 3), round(KS + 0.34, 3)), (round(KS + 0.375, 3), KP)]
for a, b in sil_segments:
    sid_ = s.uid("ksil")
    s.raw(f'<img id="{sid_}" class="clip" src="assets/img/kim2_sil.png" alt="" {s.timed(a, b)} data-track-index="4" '
          f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:0.94;z-index:{s.nz()}" />')
# glitch: a band of the real frame cut through the silhouette, plus small white bars
gl = s.uid("kgl")
s.raw(f'<img id="{gl}" class="clip" src="assets/img/kim2_f0.jpg" alt="" {s.timed(round(KS + 0.25, 3), round(KS + 0.317, 3))} '
      f'data-color-grading="{esc(GR["matte"])}" data-track-index="5" '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;'
      f'clip-path:inset(46% 30% 42% 22%);z-index:{s.nz()}" />')
s.block(round(KS + 0.25, 3), 2, (1270, 300, 46, 210), "#ffffff")
s.block(round(KS + 0.283, 3), 1, (1330, 470, 70, 14), "#ffffff")
s.block(round(KS + 0.36, 3), 2, (1180, 420, 36, 160), "#ffffff")
s.video("c_kimmel_laugh2.mp4", KP, T(9), grade="matte", push=(1.0, 1.04))
s.paper(T(9), T(13))
SCENES.append(s)
sfx("impact-bass-1.mp3", 5.40, 0.36)
sfx("whoosh-short.mp3", 5.40, 0.12)
sfx("whoosh-short.mp3", T(2), 0.14)
sfx("whoosh-short.mp3", T(4), 0.14)
sfx("whoosh.mp3", round(T(6) - 0.30, 3), 0.24)
sfx("whoosh-short.mp3", KS, 0.12)
sfx("impact-bass-1.mp3", T(6), 0.20)
cap([[("Robert", 5.40, "FN"), W(1, "FN", "Pattinson")]], T(2), y=560, kind="name", exit_first=round(T(2) - 0.17, 3))
cap([[W(2, "S", "is"), W(3, "S", "on"), W(4, "S", "a")]], T(6), y=380)
cap([[W(5, "FSL", "generational"), W(6, "FSL", "run,")]], T(7), y=610)
# the reference's lockup: a small serif word, then a big one on the same baseline, beside the silhouette
# first-10s v2 (user): "Honestly" with a capital H and no comma, moved left off his face: a small-over-big
# stack (the reference's lockup) that ends well before his head
cap([[W(7, "LS", "and")], [W(8, "B", "Honestly")]], T(9), x=70, y=300, align="left", lh=0.9)
paper_words([(9, "PS", "nobody"), (10, "PS", "saw"), (11, "PS", "it"), (12, "PXL", "coming.")], T(13), last_exit="blurout")


# ==================================================================================================
# SEGMENT 2 (10.85 - 23.41): "To some people, he'll always be Edward Cullen. But everything he did after
# Twilight proved he was never stuck in one role. He spent the last 15 years making sure the world sees him
# more than just the vampire kid."  (v4's Edward scene ported; the user's 1080p Twilight footage where sharper)
# ==================================================================================================

# ---------------- S03 "To some people, he'll always be Edward Cullen." ----------------
s = Scene("s03", T(13), T(21))
# "To some people,": v4's three shots, the halftone fainter (user note); the words build on one line across the cuts
s.video("c_tw_lab.mp4", T(13), T(14), grade="halftone_faint", push=(1.0, 1.04))
s.video("c_tw_wed.mp4", T(14), T(15), grade="halftone_faint", push=(1.05, 1.0))
s.video("c_fans_full.mp4", T(15), T(16), grade="halftone_faint", push=(1.0, 1.05))
# "he'll always be": Edward turns to camera in the school hallway (1080p)
s.video("c_twn_hall.mp4", T(16), T(19), grade="film_soft", push=(1.0, 1.04))
# "Edward Cullen.": the warm close-up; the name lands like "Dario Amodei": a corner flare as "Edward" blooms,
# two glitch frames (the word goes dark, a cyan patch, a pale-yellow block where "Cullen." lands), "Cullen." blooms,
# "Edward" leaves first, then a horizontal light streak wipes into the next line
s.video("c_twn_warm.mp4", T(19), T(21), grade="film_soft", push=(1.0, 1.05))
s.neg(T(19), 2)
s.flare(T(19), frames=3, corner="tl")
s.block(round(T(20) - 2 * F1, 3), 2, (1180, 250, 430, 400), "#63E6E2", blend="difference")
s.lightstreak(round(T(21) - 2 * F1, 3), frames=3)
SCENES.append(s)
sfx("whoosh-short.mp3", T(13), 0.12)
sfx("whoosh-short.mp3", T(16), 0.12)
sfx("impact-bass-1.mp3", T(19), 0.22)
sfx("whoosh-short.mp3", T(19), 0.12)
cap([[W(13, "M", "To"), W(14, "M", "some"), W(15, "M", "people,")]], T(16), y=560)
cap([[W(16, "S", "he'll")], [W(17, "B", "always"), W(18, "S", "be")]], T(19), x=1820, y=540, align="right", lh=0.95)
cap([[W(19, "FNS", "Edward")], [W(20, "FNS", "Cullen.")]], T(21), x=100, y=560, align="left", lh=0.84, kind="name",
    exit_first=round(T(21) - 0.17, 3))

# ---------------- S04 "But everything he did after Twilight proved he was never stuck" ----------------
s = Scene("s04", T(21), T(32))
# "But everything": the gold eyes, close (1080p)
s.video("c_twn_eyes.mp4", T(21), T(23), grade="film_soft", push=(1.0, 1.06))
# "he did after": a whip into Edward striding past the car
camW, vW = s.video("c_twn_walk.mp4", T(23), T(26), grade="film_soft", push=(1.05, 1.0),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camW, vW, T(23), dx=1)
# "Twilight": the poster as a sharp card on black (it is only 1000 px wide), pushing in, then it burns to white
s.solid(T(26), T(27), "#000000")
camP, vP = s.image("tw_poster.jpg", T(26), T(27), grade="matte", push=None, box=(560, 110, 800, 860), card=True,
                   pos="50% 0%", vars_style="--hf-color-grading-exposure: 0;")  # cropped above the poster's own title
s.js.append(f'tl.fromTo("#{camP}", {{ scale: 0.9 }}, {{ scale: 1.05, duration: {r3(T(27) - T(26))}, ease: "power1.out" }}, {s.at(T(26))});')
s.blow_out(vP, T(27), 0.24, 1.8)
s.whiteflash(T(27), 0.16)
s.lightstreak(round(T(27) - 2 * F1, 3), frames=2)
# "proved he was never stuck" (improved year counter, the Hemant Taneja wall): the years roll in bold Helvetica in a
# black band; each year's film pops out from behind the number in three low-frame-rate steps, lands as a white box
# and turns into the picture (role clips play), filling a 5x3 wall; the wall keeps pushing in; 2026 lands on
# "stuck" with The Odyssey and Dune and a white flash
s.solid(T(27), T(32), "#000000")
YEARS = [("2012", "f_belami.jpg", None, None), ("2014", "c_rover.mp4", 0.0, 0.75), ("2015", "f_queen.jpg", None, None),
         ("2016", "f_lostcity.jpg", None, None), ("2017", "c_connie.mp4", 0.1, None), ("2018", "f_damsel.jpg", None, None),
         ("2019", "c_lighthouse.mp4", 0.1, None), ("2020", "tn_red.jpg", None, None), ("2022", "c_cowl.mp4", 0.0, None),
         ("2025", "c_mickey.mp4", 0.4, None), ("2026", "c_antinous_fire.mp4", 0.6, None)]
EXTRA_2026 = ("c_scytale.mp4", 0.8, None)
STEP_D = [0.06, 0.06, 0.07, 0.07, 0.08, 0.09, 0.10, 0.12, 0.14, 0.17]  # sums to T(31) - T(27): 2026 lands on "stuck"
FILL = [(0, 2), (2, 2), (1, 0), (1, 4), (0, 0), (2, 4), (0, 4), (2, 0), (0, 1), (2, 3), (0, 3), (2, 1)]
CW, CH, GAP = 384, 360, 5
times = [T(27)]
for d in STEP_D:
    times.append(round(times[-1] + d, 3))
times[-1] = T(31)
tiles = [(yr, src, ms, rate, times[k]) for k, (yr, src, ms, rate) in enumerate(YEARS)]
tiles.append(("2026", EXTRA_2026[0], EXTRA_2026[1], EXTRA_2026[2], round(T(31) + 2 * F1, 3)))
grp_first = len(s.els)
for k, (yr, src, ms, rate, t0) in enumerate(tiles):
    r_, c_ = FILL[k]
    box = (c_ * CW + GAP, r_ * CH + GAP, CW - 2 * GAP, CH - 2 * GAP)
    cx, cy = c_ * CW + CW // 2, r_ * CH + CH // 2
    bid = s.uid("pbox")
    s.raw(f'<div id="{bid}" class="clip pbox" {s.timed(round(t0 - 4 * F1, 3), t0)} data-track-index="5" '
          f'style="left:{box[0]}px;top:{box[1]}px;width:{box[2]}px;height:{box[3]}px;z-index:{s.nz()}"></div>')
    s.js.append(f'tl.fromTo("#{bid}", {{ x: {round((960 - cx) * 0.85)}, y: {round((540 - cy) * 0.85)}, scale: 0.4 }}, '
                f'{{ x: 0, y: 0, scale: 1, duration: {r3(3 * F1)}, ease: "steps(3)" }}, {s.at(t0 - 4 * F1)});')
    s.js.append(f'tl.set("#{bid}", {{ filter: "blur(0px)" }}, {s.at(t0 - F1)});')
    if src.endswith(".mp4"):
        cam, mid = s.video(src, t0, T(32), ms=ms or 0.0, rate=rate, grade="matte", push=None, box=box,
                           vars_style="--hf-color-grading-exposure: 0.85;")
    else:
        cam, mid = s.image(src, t0, T(32), grade="matte", push=None, box=box, pos="50% 35%",
                           vars_style="--hf-color-grading-exposure: 0.85;")
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.06 }}, {s.at(t0)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0.25 }}, {s.at(t0 + F1)});')
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.0 }}, {s.at(t0 + 2 * F1)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(t0 + 2 * F1)});')
gid = s.uid("wall")
inner = "".join(s.els[grp_first:])
del s.els[grp_first:]
s.els.append(f'<div class="cam" id="{gid}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{s.nz()}">{inner}</div>')
s.js.append(f'tl.fromTo("#{gid}", {{ scale: 1.0 }}, {{ scale: 1.045, duration: {r3(T(32) - T(27))}, ease: "sine.inOut" }}, {s.at(T(27))});')
s.counter([(yr, t) for (yr, src, ms, rate, t) in tiles[:-1]], T(32), 960, 560, 260)
s.whiteflash(T(31), 0.18, 0.85)
SCENES.append(s)
sfx("whoosh-short.mp3", T(21), 0.18)
sfx("whoosh.mp3", T(23) - 0.04, 0.26)
sfx("whoosh-short.mp3", T(26), 0.14)
sfx("whoosh.mp3", T(27) - 0.05, 0.24)
sfx("impact-bass-1.mp3", T(31), 0.26)
cap([[W(21, "S", "But"), W(22, "B", "everything")]], T(23), y=820)
cap([[W(23, "S", "he"), W(24, "S", "did"), W(25, "S", "after")]], T(26), x=110, y=540, align="left")
cap([[W(26, "XL", "Twilight")]], T(27), y=600)
cap([[W(27, "SM", "proved"), W(28, "SM", "he"), W(29, "SM", "was"), W(30, "SM", "never"), W(31, "SM", "stuck")]],
    T(32), y=672)

# ---------------- S05 paper: "in / one / role." (kept as before) ----------------
s = Scene("s05", T(32), T(35))
s.paper(T(32), T(35))
SCENES.append(s)
paper_words([(32, "PS", "in"), (33, "PS", "one"), (34, "PXL", "role.")], T(35), last_exit="blurout")

# ---------------- S06 "He spent the last 15 years making sure the world sees him more than just the vampire kid." ----
s = Scene("s06", T(35), T(53))
# "He spent the last 15 years" (Legora: "and their first office was", a small centred photo on black with the words
# placed around it): his portraits strobe and accelerate inside a fixed frame, hitting "15" with a flash; the frame
# then holds on him between "15" and "years", so no word sits on his face
s.solid(T(35), T(41), "#000000")
FB = (500, 230, 920, 620)
STROBE = [("solo01.jpg", 0.22), ("solo02.jpg", 0.18), ("solo03.jpg", 0.15), ("solo05.jpg", 0.13), ("solo06.jpg", 0.12),
          ("solo07.jpg", 0.12), ("hero.jpg", 0.12)]
grp_first = len(s.els)
tcur = T(35)
for im, d in STROBE:
    t_next = round(tcur + d, 3)
    s.image(im, tcur, t_next, grade="matte", push=(1.06, 1.0), box=(0, 0, FB[2], FB[3]),
            pos="50% 42%" if im != "hero.jpg" else "50% 35%")
    tcur = t_next
camF, imF = s.image("solo04.jpg", T(39), T(41), grade="matte", push=(1.0, 1.07), box=(0, 0, FB[2], FB[3]), pos="50% 42%",
                    vars_style="--hf-color-grading-exposure: 1.1;")
s.blow_in(imF, T(39), 0.3)
frm = s.uid("frame")
inner = "".join(s.els[grp_first:])
del s.els[grp_first:]
s.els.append(f'<div class="cam" id="{frm}" style="position:absolute;left:{FB[0]}px;top:{FB[1]}px;width:{FB[2]}px;'
             f'height:{FB[3]}px;overflow:hidden;box-sizing:border-box;border:5px solid #F4EFEB;'
             f'box-shadow:0 30px 80px rgba(0,0,0,0.6);z-index:{s.nz()}">{inner}</div>')
s.js.append(f'tl.fromTo("#{frm}", {{ scale: 0.94 }}, {{ scale: 1.0, duration: {r3(T(41) - T(35))}, ease: "sine.out" }}, {s.at(T(35))});')
s.whiteflash(T(39), 0.14, 0.7)
# "making sure": Venice, arriving (1080p crop from the phone original, below the watermark)
s.video("c_ven_hair.mp4", T(41), T(43), grade="matte", push=(1.0, 1.05))
s.neg(T(41), 2)
# "the world": the crowd's cameras and phones on him
s.video("c_ven_crowd.mp4", T(43), T(45), grade="matte", push=(1.06, 1.0))
# "sees him": three premiere panels at native size wipe in left to right; camera flashes pop on them
for k, src in enumerate(["p_carpet_a.mp4", "p_carpet_b.mp4", "p_carpet_c.mp4"]):
    t0 = round(T(45) + k * 2 * F1, 3)
    cam, vid = s.video(src, t0, T(47), grade="matte", push=None, box=(k * 640, 0, 640, 1080),
                       cam_extra="clip-path:inset(0% 100% 0% 0%);")
    s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
                f'duration: 0.16, ease: "expo.out" }}, {s.at(t0)});')
for t, k, fr in [(T(45) + 0.12, 1, 1), (T(45) + 0.20, 0, 2), (T(46), 2, 2), (T(46) + 0.10, 1, 1), (T(46) + 0.15, 0, 1)]:
    s.block(round(t, 3), fr, (k * 640, 0, 640, 1080), "#ffffff", opacity=0.85)
# "more than just": back to Edward, in the forest (1080p)
s.video("c_twn_forest.mp4", T(47), T(50), grade="film_soft", push=(1.0, 1.05))
s.neg(T(47), 2)
# "the vampire kid.": text behind him: the plate, "vampire" in glowing serif, then his cut-out over it, all pushing in
cam = s.uid("cam")
z = s.nz()
s.uses_text = True
vw, vt = f"{cam}-vw", f"{cam}-vampire"
s.raw(f'<div class="cam" id="{cam}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{z}">'
      f'<img id="{cam}-plate" class="clip" src="assets/img/f_twn_vamp.jpg" alt="" {s.timed(T(50), T(53))} '
      f'data-color-grading="{esc(GR["film_soft"])}" data-track-index="3" '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />'
      f'<div id="{vw}" class="clip txw al" {s.timed(T(51), T(53))} data-track-index="6" '
      f'style="left:230px;width:1600px;top:120px;height:440px;text-align:left">'
      f'<span id="{vt}" class="tx" style="font-family:\'Instrument Serif\';font-size:330px;color:#F7F4F7;opacity:0;'
      f'text-shadow:{SERIF_REST}">vampire</span></div>'
      f'<img id="{cam}-cut" class="clip" src="assets/img/f_twn_vamp-cut.png" alt="" {s.timed(T(50), T(53))} '
      f'data-color-grading="{esc(GR["film_soft"])}" data-track-index="4" data-layout-allow-occlusion '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />'
      f'</div>')
s.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.07, duration: {r3(T(53) - T(50))}, ease: "none" }}, {s.at(T(50))});')
# the serif hero settle, measured on the reference: one blown-out frame, three soft frames, then crisp
s.js.append(f'tl.set("#{vt}", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {s.at(T(51))});')
s.js.append(f'tl.set("#{vt}", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {s.at(T(51) + F1)});')
s.js.append(f'tl.set("#{vt}", {{ scale: 1.005, filter: "blur(2.5px)" }}, {s.at(T(51) + 3 * F1)});')
s.js.append(f'tl.set("#{vt}", {{ scale: 1, filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {s.at(T(51) + 4 * F1)});')
SCENES.append(s)
sfx("whoosh-short.mp3", T(35), 0.14)
sfx("impact-bass-1.mp3", T(39), 0.24)
sfx("whoosh-short.mp3", T(41), 0.14)
sfx("whoosh-short.mp3", T(43), 0.12)
sfx("whoosh-short.mp3", T(45), 0.14)
sfx("whoosh-short.mp3", T(47), 0.12)
sfx("whoosh-short.mp3", T(50), 0.12)
cap([[W(35, "S", "He")]], T(39), x=455, y=540, align="right")
cap([[W(36, "S", "spent")]], T(39), x=1465, y=540, align="left")
cap([[W(37, "S", "the"), W(38, "S", "last")]], T(39), y=955)
cap([[W(39, "NUM", "15")]], T(41), x=465, y=600, align="right")
cap([[W(40, "B", "years")]], T(41), x=1460, y=600, align="left")
cap([[W(41, "S", "making"), W(42, "S", "sure")]], T(43), y=900)
cap([[W(43, "S", "the"), W(44, "B", "world")]], T(45), y=860)
cap([[W(45, "M", "sees"), W(46, "M", "him")]], T(47), y=560)
cap([[W(47, "S", "more"), W(48, "S", "than"), W(49, "S", "just")]], T(50), y=880)
cap([[W(50, "M", "the")]], T(53), x=150, y=190, align="left")
cap([[W(52, "M", "kid.")]], T(53), x=1790, y=940, align="right")


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
    for lid, t0, d in (("leak1", T(26) + 0.05, 0.75), ("leak2", T(182) + 0.10, 1.30)):
        if t0 + d <= DUR:
            hosts.append(
                f'<div id="{lid}" class="clip" data-composition-id="{lid}" data-composition-src="compositions/{lid}.html" '
                f'data-start="{r3(t0)}" data-duration="{r3(d)}" data-track-index="2" data-track-kind="graphics" '
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
    # the new voiceover in three parts, split around the two dialogue stings
    vo = [("vo-a", 5.40, 29.93, 0.00), ("vo-b", 37.68, 26.87, 29.93), ("vo-c", 66.70, 12.03, 56.80)]
    for aid, st, d, ms in vo:
        if st >= DUR:
            continue
        d = min(d, round(DUR - st, 3))
        auds.append(f'<audio id="{aid}" class="clip" src="assets/audio/vo2.wav" data-start="{r3(st)}" data-duration="{r3(d)}" '
                    f'data-media-start="{r3(ms)}" data-volume="1" data-fade-out="0.06" data-track-index="10"></audio>')
    for aid, src, st, d in [("sting-beggars", "sting-beggars.wav", 0.0, 5.50), ("sting-spider", "sting-spider.wav", 35.33, 2.35),
                            ("sting-seat", "sting-seat.wav", 64.55, 2.15)]:
        if st >= DUR:
            continue
        d = min(d, round(DUR - st, 3))
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
