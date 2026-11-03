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
DUR = 81.37  # the whole film: v4's 2.55 s end card after "seen" (end card at 78.82)
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
                text = text.replace(",", "").replace(".", "")  # user: no commas or full stops in captions
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
# "But everything": the 1080p gold eyes, held still (the user asked for no pans or pushes here)
s.video("c_twn_eyes.mp4", T(21), T(23), grade="film_soft", push=None)
# "he did after Twilight" (user: the pop-out animation, calmer, behind the Twilight poster): the poster in the middle on
# black; white boxes pop out from behind it in three low-frame-rate steps, land soft then crisp and turn into Twilight
# pictures around it (one every three frames, a mild dome), while the camera slowly pulls back
s.solid(T(23), T(27), "#000000")
TWP = [  # source, centre x, centre y, w, h, tilt
    ("tw_newmoon.jpg", 600, 560, 360, 380, -8), ("tw_poster2.jpg", 1320, 560, 360, 380, 8),
    ("tw_kiss.jpg", 260, 230, 400, 225, -3), ("tw_prom.jpg", 1660, 230, 400, 225, 3),
    ("tw_cast.jpg", 260, 850, 400, 225, 3), ("tw_tree1.jpg", 1660, 850, 400, 225, -3),
]


def dome(cx, cy, f):
    nx, ny = (cx - 960) / 960, (cy - 540) / 540
    return dict(rotationY=round(30 * nx * f, 2), rotationX=round(-18 * ny * f, 2), z=round(-170 * (nx * nx + ny * ny) * f, 1))


grp_first = len(s.els)
for k, (im, cx, cy, w, h, rot) in enumerate(TWP):
    t0 = round(T(23) + 0.10 + k * 3 * F1, 3)
    box = (cx - w // 2, cy - h // 2, w, h)
    d0 = dome(cx, cy, 0.5)
    bid = s.uid("pbox")
    s.raw(f'<div id="{bid}" class="clip pbox" {s.timed(round(t0 - 4 * F1, 3), t0)} data-track-index="5" '
          f'style="left:{box[0]}px;top:{box[1]}px;width:{w}px;height:{h}px;z-index:{s.nz()}"></div>')
    s.js.append(f'tl.fromTo("#{bid}", {{ x: {round((960 - cx) * 0.8)}, y: {round((540 - cy) * 0.8)}, scale: 0.45, rotation: 0, '
                f'rotationY: 0, rotationX: 0, z: 0 }}, {{ x: 0, y: 0, scale: 1, rotation: {rot}, rotationY: {d0["rotationY"]}, '
                f'rotationX: {d0["rotationX"]}, z: {d0["z"]}, duration: {r3(3 * F1)}, ease: "steps(3)" }}, {s.at(t0 - 4 * F1)});')
    s.js.append(f'tl.set("#{bid}", {{ filter: "blur(0px)" }}, {s.at(t0 - F1)});')
    cam, mid = s.image(im, t0, T(27), grade="matte", push=None, box=box, card=True, pos="50% 0%" if h > 300 else "50% 35%",
                       vars_style="--hf-color-grading-exposure: 0.85;")
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.06, rotation: {rot}, rotationY: {d0["rotationY"]}, rotationX: {d0["rotationX"]}, '
                f'z: {d0["z"]}, transformPerspective: 1400 }}, {s.at(t0)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0.25 }}, {s.at(t0 + F1)});')
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.0 }}, {s.at(t0 + 2 * F1)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(t0 + 2 * F1)});')
# the poster itself, on top, cropped above its own title, landing in two steps
camPo, imPo = s.image("tw_poster.jpg", T(23), T(27), grade="matte", push=None, box=(640, 195, 640, 690), card=True,
                      pos="50% 0%", vars_style="--hf-color-grading-exposure: 0.8;")
s.js.append(f'tl.set("#{camPo}", {{ scale: 1.06 }}, {s.at(T(23))});')
s.js.append(f'tl.set("#{imPo}", {{ "--hf-color-grading-exposure": 0.25 }}, {s.at(T(23) + F1)});')
s.js.append(f'tl.set("#{camPo}", {{ scale: 1.0 }}, {s.at(T(23) + 2 * F1)});')
s.js.append(f'tl.set("#{imPo}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(T(23) + 2 * F1)});')
gid = s.uid("wall")
inner = "".join(s.els[grp_first:])
del s.els[grp_first:]
s.els.append(f'<div class="cam" id="{gid}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
             f'perspective:1400px;z-index:{s.nz()}">{inner}</div>')
s.js.append(f'tl.fromTo("#{gid}", {{ scale: 1.0, y: 0 }}, {{ scale: 0.95, y: -10, duration: {r3(T(27) - T(23))}, '
            f'ease: "sine.inOut" }}, {s.at(T(23))});')
s.whiteflash(T(27), 0.16)
# "proved he was never stuck": v4's year counter (full-frame stills behind the big Helvetica year), now under one smooth
# camera that pulls back and turns slightly in perspective while staying full frame (user: like the generational run)
years = [("2012", "f_belami.jpg"), ("2014", "f_rover.jpg"), ("2015", "f_queen.jpg"), ("2016", "f_lostcity.jpg"),
         ("2017", "gt_neon.jpg"), ("2018", "f_damsel.jpg"), ("2019", "lh_portrait.jpg"), ("2020", "tn_red.jpg"),
         ("2022", "bt_cowl.jpg"), ("2025", "mk_helmet.jpg"), ("2026", "f_antinous.jpg")]
durs = [0.08, 0.08, 0.08, 0.09, 0.09, 0.10, 0.11, 0.12, 0.13, 0.15, 0.18]
grp_first = len(s.els)
tcur, steps = T(27), []
for k, ((yr, im), d) in enumerate(zip(years, durs)):
    t_next = round(tcur + d, 3) if k < len(years) - 1 else T(32)
    s.image(im, tcur, t_next, grade="matte", push=(1.05, 1.0))
    steps.append((yr, round(tcur, 3)))
    tcur = t_next
yid = s.uid("yrs")
inner = "".join(s.els[grp_first:])
del s.els[grp_first:]
s.els.append(f'<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;perspective:1400px;z-index:{s.nz()}">'
             f'<div class="cam" id="{yid}" style="position:absolute;left:0;top:0;width:1920px;height:1080px">{inner}</div></div>')
s.js.append(f'tl.fromTo("#{yid}", {{ scale: 1.16, rotationY: -4, rotationX: 2 }}, {{ scale: 1.08, rotationY: 3, rotationX: -1, '
            f'duration: {r3(T(32) - T(27))}, ease: "sine.inOut" }}, {s.at(T(27))});')
s.counter(steps, T(32), 960, 600, 300)
SCENES.append(s)
sfx("whoosh-short.mp3", T(23), 0.14)
sfx("whoosh.mp3", T(27) - 0.05, 0.24)
cap([[W(21, "S", "But"), W(22, "B", "everything")]], T(23), y=820)
cap([[W(23, "S", "he"), W(24, "S", "did"), W(25, "S", "after")]], T(27), y=150)  # above the poster, off the faces
cap([[W(26, "XL", "Twilight")]], T(27), y=670)
cap([[W(27, "S", "proved")]], T(28), y=930)
cap([[W(28, "S", "he"), W(29, "S", "was"), W(30, "S", "never")]], T(31), y=930)
cap([[W(31, "S", "stuck")]], T(32), y=930)

# ---------------- S05 paper: "in / one / role" (kept as before) ----------------
s = Scene("s05", T(32), T(35))
s.paper(T(32), T(35))
s.neg(round(T(35) - F1, 3), 1)  # the paper inverts for its last frame (the reference's cut into the split box)
SCENES.append(s)
paper_words([(32, "PS", "in"), (33, "PS", "one"), (34, "PXL", "role")], T(35), last_exit="blurout")

# ---------------- S06 "He spent the last 15 years making sure the world sees him more than just the vampire kid" ----
s = Scene("s06", T(35), T(53))
# "He spent the last 15 years" (the user's McConaughey reference at 15 s, measured frame by frame): a small white box
# flickers on black, splits into two stacked clips of his roles, grows smoothly (S-curve) into two full-width bands,
# the bands flash white for a frame as their clips change, and on "years" the halves merge into one picture
s.solid(T(35), T(41), "#000000")
SB0, CLP = 0.4204, 22.93  # a 437x227 half of a 1920x540 band: start scale and left/right clip-path inset (%)
GROW0, GROW1 = T(36), T(39)


def band(ytop, dy, items):
    bid = s.uid("band")
    inner = []
    for it in items:
        if it[0] == "white":
            wid = s.uid("bw")
            inner.append(f'<div id="{wid}" class="clip solid" {s.timed(it[1], it[2])} data-track-index="5" '
                         f'style="left:0;top:0;width:1920px;height:540px;background:#ffffff"></div>')
        elif it[0] == "img":
            _, src, t0, t1, pos = it
            iid = s.uid("bi")
            inner.append(f'<img id="{iid}" class="clip" src="assets/img/{src}" alt="" {s.timed(t0, t1)} '
                         f'data-color-grading="{esc(GR["matte"])}" data-track-index="3" '
                         f'style="position:absolute;left:0;top:0;width:1920px;height:540px;object-fit:cover;object-position:{pos}" />')
        else:
            _, src, t0, t1, ms, pos = it
            vid = s.uid("bv")
            inner.append(f'<video id="{vid}" class="clip" src="assets/clips/{src}" muted playsinline {s.timed(t0, t1)} '
                         f'data-hf-media-start-basis="local" data-media-start="{r3(ms)}" data-color-grading="{esc(GR["matte"])}" '
                         f'data-track-index="2" style="position:absolute;left:0;top:0;width:1920px;height:540px;'
                         f'object-fit:cover;object-position:{pos}"></video>')
    s.els.append(f'<div class="cam" id="{bid}" style="position:absolute;left:0;top:{ytop}px;width:1920px;height:540px;'
                 f'overflow:hidden;z-index:{s.nz()}">' + "".join(inner) + '</div>')
    s.js.append(f'tl.fromTo("#{bid}", {{ scale: {SB0}, y: {dy}, clipPath: "inset(0% {CLP}% 0% {CLP}%)" }}, '
                f'{{ scale: 1, y: 0, clipPath: "inset(0% 0% 0% 0%)", duration: {r3(GROW1 - GROW0)}, ease: "power2.inOut" }}, '
                f'{s.at(GROW0)});')


a0 = T(35)
tA, tB, tC = round(T(39) + 0.15, 3), round(T(39) + 0.30, 3), T(40)
band(0, 156.5, [
    ("white", a0, round(a0 + F1, 3)), ("white", round(a0 + 2 * F1, 3), round(a0 + 3 * F1, 3)),
    ("img", "f_devil.jpg", round(a0 + 3 * F1, 3), T(37), "50% 30%"),                    # The Devil All the Time
    ("white", T(37), round(T(37) + F1, 3)),
    ("clip", "c_lighthouse.mp4", round(T(37) + F1, 3), tA, 0.55, "50% 28%"),            # The Lighthouse
    ("white", tA, round(tA + F1, 3)),
    ("clip", "c_k15_mk17h.mp4", round(tA + F1, 3), tC, 0.0, "50% 22%"),                 # Mickey 17
    ("white", tC, round(tC + F1, 3)),
])
band(540, -156.5, [
    ("white", round(a0 + 3 * F1, 3), round(a0 + 4 * F1, 3)),
    ("clip", "c_k15_barb.mp4", round(a0 + 4 * F1, 3), round(a0 + 5 * F1, 3), 0.0, "50% 30%"),
    ("white", round(a0 + 5 * F1, 3), round(a0 + 6 * F1, 3)),
    ("clip", "c_k15_barb.mp4", round(a0 + 6 * F1, 3), T(38), 0.07, "50% 30%"),          # Waiting for the Barbarians
    ("white", T(38), round(T(38) + F1, 3)),
    ("clip", "c_k15_tenet.mp4", round(T(38) + F1, 3), tB, 0.0, "50% 22%"),               # Tenet
    ("white", tB, round(tB + F1, 3)),
    ("img", "f_damsel.jpg", round(tB + F1, 3), tC, "50% 32%"),                           # Damsel
    ("white", tC, round(tC + F1, 3)),
])
# "years": the two halves become one picture (The Drama), with the seam showing for a few frames
s.video("c_k15_drama.mp4", round(tC + F1, 3), T(41), grade="matte", push=(1.0, 1.03))
seam = s.uid("seam")
s.raw(f'<div id="{seam}" class="clip solid" {s.timed(round(tC + F1, 3), round(tC + 0.17, 3))} data-track-index="5" '
      f'style="left:0;top:538px;width:1920px;height:4px;background:#0b0b0b;z-index:{s.nz()}"></div>')
# "making sure": Venice, arriving (1080p crop from the phone original, below the watermark)
s.video("c_ven_hair.mp4", T(41), T(43), grade="matte", push=(1.0, 1.05))
s.neg(T(41), 2)
# "the world": the crowd's cameras and phones on him
s.video("c_ven_crowd.mp4", T(43), T(45), grade="matte", push=(1.06, 1.0))
# "sees him": three premiere panels wipe in left to right (the user's two clips at the sides, The Drama premiere in the
# middle); camera flashes pop on them
for k, src in enumerate(["p_frame_l.mp4", "p_carpet_b.mp4", "p_world_r.mp4"]):
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
# "the vampire kid": text behind him: the plate, "vampire" in glowing serif, then his cut-out over it, pushing in
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
s.js.append(f'tl.set("#{vt}", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {s.at(T(51))});')
s.js.append(f'tl.set("#{vt}", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {s.at(T(51) + F1)});')
s.js.append(f'tl.set("#{vt}", {{ scale: 1.005, filter: "blur(2.5px)" }}, {s.at(T(51) + 3 * F1)});')
s.js.append(f'tl.set("#{vt}", {{ scale: 1, filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {s.at(T(51) + 4 * F1)});')
SCENES.append(s)
sfx("whoosh-short.mp3", T(35), 0.10)
sfx("whoosh.mp3", GROW0, 0.18)
sfx("impact-bass-1.mp3", T(39), 0.18)
sfx("whoosh-short.mp3", T(40), 0.12)
sfx("whoosh-short.mp3", T(41), 0.14)
sfx("whoosh-short.mp3", T(43), 0.12)
sfx("whoosh-short.mp3", T(45), 0.14)
sfx("whoosh-short.mp3", T(47), 0.12)
sfx("whoosh-short.mp3", T(50), 0.12)
cap([[W(35, "SM", "He"), W(36, "SM", "spent"), W(37, "SM", "the"), W(38, "SM", "last")]], T(39), y=262)
# "15" sits on the seam while the bands run; on the merge (hidden by the white frame) "15 years" moves below his face
cap([[W(39, "NUM", "15")]], T(40), y=560)
cap([[("15", round(T(40) + F1, 3), "NUM"), W(40, "B", "years")]], T(41), y=860)
cap([[W(41, "S", "making"), W(42, "S", "sure")]], T(43), y=900)
cap([[W(43, "S", "the"), W(44, "B", "world")]], T(45), y=860)
cap([[W(45, "M", "sees"), W(46, "M", "him")]], T(47), y=560)
cap([[W(47, "S", "more"), W(48, "S", "than"), W(49, "S", "just")]], T(50), y=880)
cap([[W(50, "M", "the")]], T(53), x=150, y=190, align="left")
cap([[W(52, "M", "kid")]], T(53), x=1790, y=940, align="right")

# ==================================================================================================
# SEGMENT 3 (23.41 - 37.68): "Good Time, The Lighthouse, Tenet, The Batman, and Mickey 17. Every one of them was a
# weird, bold swing nobody expected from him. And while the internet kept making Twilight jokes," + spider monkey
# (v4's scenes ported, with the new text animation, as the user asked)
# ==================================================================================================

# ---------------- S07 the film run: one full-frame film per title, year above, title centred (v4) ----------------
s = Scene("s07", T(53), T(63))
s.video("c_goodtime.mp4", T(53), T(55), grade="matte", push=(1.0, 1.05))
s.neg(T(53), 2)
camL, vL = s.video("c_lighthouse.mp4", T(55), T(57), grade="matte_bw", push=(1.05, 1.0),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camL, vL, T(55), dx=1)
camT1, vT1 = s.video("c_tenet_a.mp4", T(57), T(57) + 0.38, grade="matte", push=(1.0, 1.04),
                     vars_style="--hf-color-grading-exposure: 0.9;")
s.blow_in(vT1, T(57), 0.2)
s.video("c_tenet_b.mp4", T(57) + 0.38, T(58), grade="matte", push=(1.0, 1.07))
s.video("c_batroof.mp4", T(58), T(60), rate=0.75, grade="matte", push=(1.0, 1.05))
s.neg(T(58), 2)
camM, vM = s.video("c_mickey.mp4", T(60), T(63), grade="matte", push=(1.0, 1.05),
                   vars_style="--hf-color-grading-blur: 0.85;")
s.whip_in(camM, vM, T(60), dx=-1)
# "Mickey 17": the year above, the title centred, the number rolls 1 -> 17 and lands on the spoken "17"
s.text("2025", T(61), T(63), 960, 400, 56, family="Inter Tight", weight=700)
mk = s.text("Mickey", T(61), T(63), 1010, 620, 230, family="Instrument Serif", weight=400, align="right", anim="none")
s.js.append(f'tl.set("#{mk}", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {s.at(T(61))});')
s.js.append(f'tl.set("#{mk}", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {s.at(T(61) + F1)});')
s.js.append(f'tl.set("#{mk}", {{ scale: 1.005, filter: "blur(2.5px)" }}, {s.at(T(61) + 3 * F1)});')
s.js.append(f'tl.set("#{mk}", {{ scale: 1, filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {s.at(T(61) + 4 * F1)});')
roll = ["1", "2", "4", "7", "10", "13", "15", "16", "17"]
rt = [T(61) + 0.06, T(61) + 0.12, T(61) + 0.18, T(61) + 0.25, T(61) + 0.32, T(61) + 0.40, T(61) + 0.48, T(61) + 0.56, T(62)]
s.counter([(v, round(t, 3)) for v, t in zip(roll, rt)], T(63), 1060, 620, 230, family="Instrument Serif", weight=400,
          align="left")
SCENES.append(s)
sfx("impact-bass-1.mp3", T(53), 0.20)
sfx("whoosh.mp3", T(55) - 0.04, 0.28)
sfx("whoosh-short.mp3", T(57), 0.20)
sfx("impact-bass-1.mp3", T(58), 0.22)
sfx("whoosh.mp3", T(60) - 0.04, 0.28)
# the year sits clearly above each title (as on the v4 Mickey 17 frame the user marked as perfect)
for (yr, wi, wj, st, ty, t1) in [("2017", 53, 54, "B", 560, T(55)), ("2019", 55, 56, "B", 560, T(57)),
                                  ("2020", 57, None, "XL", 560, T(58)), ("2022", 58, 59, "B", 560, T(60))]:
    cap([[(yr, T(wi), "Y")]], t1, y=ty - (215 if st == "XL" else 170))
    cap([[W(wi, st)] + ([W(wj, st)] if wj is not None else [])], t1, y=ty)
cap([[W(60, "S", "and")]], T(61), y=560)

# ---------------- S08 "Every one of them was a weird bold swing nobody expected from him" ----------------
s = Scene("s08", T(63), T(76))
# the five films over the Mickey 17 shot (v4), with the entrance and exit of the General Catalyst founders wall (24-25 s):
# each panel pops in left to right on a word with one blown-out frame, then settles; on the way out the panels flash
# white one by one, left to right, and each reveals the next shot ("weird") through its slot
SWEEP = round(T(68) - 0.05, 3)
s.video("c_mickey.mp4", T(63), SWEEP, ms=round(T(63) - T(60), 3), grade="matte", push=(1.05, 1.1),
        vars_style="--hf-color-grading-exposure: -0.5;")
s.video("c_soot.mp4", SWEEP, T(70), grade="matte_bw", push=(1.04, 1.0))
panels = [("p_goodtime.mp4", T(63)), ("p_lighthouse.mp4", T(64)), ("p_tenet.mp4", T(65)), ("p_batman.mp4", T(66)),
          ("p_mickey.mp4", T(67))]
for k, (src, t0) in enumerate(panels):
    t_out = round(SWEEP + k * 2 * F1, 3)
    grade = "matte_bw" if "lighthouse" in src else "matte"
    cam, vid = s.video(src, t0, round(t_out + F1, 3), grade=grade, push=None, box=(k * 384, 0, 384, 1080),
                       vars_style="--hf-color-grading-exposure: 1.2;")
    s.js.append(f'tl.set("#{vid}", {{ "--hf-color-grading-exposure": 0.4 }}, {s.at(t0 + F1)});')
    s.js.append(f'tl.set("#{vid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(t0 + 2 * F1)});')
    s.block(t0, 1, (k * 384, 0, 384, 1080), "#ffffff", opacity=0.45)
    s.block(t_out, 1, (k * 384, 0, 384, 1080), "#ffffff", opacity=0.9)
    sfx("whoosh-short.mp3", t0, 0.10)
s.video("c_connie.mp4", T(70), T(71), grade="matte", push=(1.0, 1.06))
camK, vK = s.video("c_king.mp4", T(71), T(72), grade="matte", push=None, vars_style="--hf-color-grading-blur: 0.9;")
s.js.append(f'tl.fromTo("#{camK}", {{ x: 560, scale: 1.1 }}, {{ x: 0, scale: 1.0, duration: 0.2, ease: "power3.out" }}, {s.at(T(71))});')
s.js.append(f'tl.to("#{vK}", {{ "--hf-color-grading-blur": 0, duration: 0.24, ease: "power2.out" }}, {s.at(T(71))});')
s.paper(T(72), T(76))
SCENES.append(s)
sfx("whoosh.mp3", SWEEP, 0.20)
sfx("whoosh.mp3", T(71) - 0.04, 0.34)
cap([[W(63, "M", "every"), W(64, "M", "one")]], T(65), y=540)
cap([[W(65, "M", "of"), W(66, "M", "them")]], T(67), y=540)
cap([[W(67, "S", "was"), W(68, "S", "a")]], T(69), y=540)
cap([[W(69, "XL", "weird")]], T(70), x=1780, y=700, align="right")
cap([[W(70, "XL", "bold")]], T(71), x=160, y=640, align="left")
cap([[W(71, "XL", "swing")]], T(72), y=600)
paper_words([(72, "PS", "nobody"), (73, "PXL", "expected"), (74, "PS", "from"), (75, "PS", "him")], T(76), last_exit="blurout")

# ---------------- S09 "And while the internet kept making Twilight jokes" + "spider monkey" (v4) ----------------
s = Scene("s09", T(76), 37.68)
s.video("c_tw_stare.mp4", T(76), T(78), grade="film_soft", push=(1.0, 1.05))
s.video("c_tw_glitch.mp4", T(78), T(80), grade="glitch_soft", push=(1.0, 1.04))
s.video("c_tw_battle.mp4", T(80), T(82), grade="halftone_faint", push=(1.05, 1.0))
s.video("c_sparkle2.mp4", T(82), 35.33, grade="halftone_faint", push=(1.0, 1.06))
s.neg(T(82), 2)
s.video("c_spider.mp4", 35.33, 37.68, ms=0.10, grade="film_soft", push=(1.0, 1.05))
SCENES.append(s)
sfx("whoosh-short.mp3", T(76), 0.16)
sfx("tv-blip-soft.wav", T(78), 0.24)
sfx("whoosh-short.mp3", T(80), 0.16)
sfx("whoosh-short.mp3", T(82), 0.20)
cap([[W(76, "FS", "and"), W(77, "FS", "while"), W(78, "FS", "the"), W(79, "FS", "internet")]], T(80), y=540)
cap([[W(80, "FSL", "kept"), W(81, "FSL", "making")]], T(82), y=540)
cap([[W(82, "FSL", "Twilight"), W(83, "FSL", "jokes")]], 35.33, y=540)
cap([[("you better hold on tight", 35.43, "R")]], 36.53, y=150)
cap([[("spider", 36.53, "FSI"), ("monkey", 36.71, "FSI")]], 37.68, y=880)

# ---------------- S10 "he was quietly working with the best directors alive, until one day he became Batman" ----------
# v4's beat with the user's changes: a new "quietly" shot, Nolan at the IMAX camera for the whole directors line
# (no director strobe), and the user's second Batman edit (6-7 s) behind "he became Batman" under v4's reveal
s = Scene("s10", T(84), T(99))
s.video("c_quiet.mp4", T(84), T(87), grade="matte_bw", push=(1.0, 1.05))   # The Lighthouse, by the lamp
s.neg(T(84), 2)
s.video("c_lh_work.mp4", T(87), T(88), grade="matte_bw", push=(1.0, 1.04))
# one shot for "with the best directors alive": the camera itself pulls back ~23 %, so no push; it whips in from
# the left and is scaled up while it slides, so the frame stays covered (scale >= 1 + 2x/1920)
camN, vN = s.video("c_nolan_imax.mp4", T(88), T(93), grade="matte", push=None,
                   vars_style="--hf-color-grading-blur: 0.85;")
s.js.append(f'tl.fromTo("#{camN}", {{ x: -220, scale: 1.24 }}, {{ x: 0, scale: 1.0, duration: 0.22, ease: "power3.out" }}, '
            f'{s.at(T(88))});')
s.js.append(f'tl.to("#{vN}", {{ "--hf-color-grading-blur": 0, duration: 0.28, ease: "power2.out" }}, {s.at(T(88))});')
s.video("c_backhead.mp4", T(93), T(96), grade="matte", push=(1.0, 1.04))
# "he became": the user's clip, 6-7 s, ten flashes at two frames each; "Batman": the cowl close-up that follows,
# with v4's reveal (negative, settle from 106 %, the two impacts)
s.video("c_bat2_strobe.mp4", T(96), T(98), grade="matte", push=(1.0, 1.08))
s.video("c_bat2_cowl.mp4", T(98), T(99), grade="matte", push=(1.06, 1.0), pushease="power2.out")
s.neg(T(98), 3)
SCENES.append(s)
sfx("whoosh-short.mp3", T(84) - 0.02, 0.22)
sfx("whoosh.mp3", T(88) - 0.04, 0.28)
sfx("impact-bass-2.mp3", T(98), 0.42)
sfx("impact-bass-1.mp3", T(98), 0.50)
# captions keep off the faces: "quietly" over the dark half of the lamp shot, the directors line over Nolan's coat
cap([[W(84, "S", "he"), W(85, "S", "was")], [W(86, "B", "quietly")]], T(87), x=150, y=540, align="left", lh=0.95)
cap([[W(87, "M", "working")]], T(88), y=560)
cap([[W(88, "S", "with"), W(89, "S", "the"), W(90, "S", "best")], [W(91, "B", "directors")]], T(92), x=110, y=470,
    align="left", lh=0.95)
cap([[W(92, "XL", "alive")]], T(93), x=110, y=470, align="left")
cap([[W(93, "S", "until")]], T(94), y=800)
cap([[W(94, "S", "one"), W(95, "S", "day")]], T(96), y=800)
cap([[W(96, "S", "he"), W(97, "S", "became")]], T(98), x=1780, y=560, align="right")
cap([[W(98, "XL", "Batman")]], T(99), y=905)

# ---------------- S11 "He doesn't play characters, he becomes them. He picks roles that scare the shit out of others, the
# ones everyone else runs from." The user's Batman makeup test, shot by shot, animated from the references: Legora's
# ease back into a centred frame, the Dario serif glow and corner flare, the Hemant Taneja white silhouette, F1's sans
s = Scene("s11", T(99), T(122))
# "He doesn't play characters": the clean face (slowed, before the spray bottle comes in) eases back from full frame
# into a centred frame (Legora: power4.out over 0.9 s), lifted so the line sits under it
camF, vF = s.video("c_r_face.mp4", T(99), T(103), rate=round(1.22 / (T(103) - T(99)), 3), grade="matte", push=None,
                   cam_extra="box-shadow: 0 40px 120px rgba(0,0,0,0.7);")
s.js.append(f'tl.fromTo("#{camF}", {{ scale: 1.0, y: 0 }}, {{ scale: 0.62, y: -84, duration: 0.9, ease: "power4.out" }}, '
            f'{s.at(T(99) + 0.12)});')
s.js.append(f'tl.to("#{camF}", {{ scale: 0.6, duration: {r3(T(103) - T(99) - 1.02)}, ease: "none" }}, {s.at(T(99) + 1.02)});')
s.whiteflash(T(99), 0.2, 0.85)
# "he becomes them": the eye black running, full frame again; his white silhouette for two frames on "becomes"
s.video("c_r_tears.mp4", T(103), T(106), grade="matte", push=(1.0, 1.06))
s.neg(T(103), 2)
s.silhouette("r_tears_sil.png", T(104), frames=2)
s.flare(T(105), frames=3, corner="tr")
# "He picks roles": alone in the studio, arriving from the right (scaled while it slides, so the frame stays covered)
camW, vW = s.video("c_r_wide.mp4", T(106), T(109), grade="matte", push=None, vars_style="--hf-color-grading-blur: 0.85;")
s.js.append(f'tl.fromTo("#{camW}", {{ x: 220, scale: 1.24 }}, {{ x: 0, scale: 1.02, duration: 0.22, ease: "power3.out" }}, '
            f'{s.at(T(106))});')
s.js.append(f'tl.to("#{camW}", {{ scale: 1.06, duration: {r3(T(109) - T(106) - 0.22)}, ease: "none" }}, {s.at(T(106) + 0.22)});')
s.js.append(f'tl.to("#{vW}", {{ "--hf-color-grading-blur": 0, duration: 0.28, ease: "power2.out" }}, {s.at(T(106))});')
# "that scare the shit out of others": the low angle creeping in; "scare" hits with a negative and a channel split
s.video("c_r_low.mp4", T(109), T(116), grade="matte", push=(1.0, 1.1))
s.neg(T(110), 2)
s.rgbsplit("c_r_low.mp4", round(T(110) + 2 * F1, 3), ms=round(T(110) + 2 * F1 - T(109), 3), frames=2)
# "the ones everyone else runs from": the red room pulling back, then the monitors
s.video("c_r_red.mp4", T(116), T(120), grade="matte", push=(1.06, 1.0))
s.video("c_r_mon.mp4", T(120), T(122), grade="matte", push=(1.0, 1.05))
s.neg(T(120), 2)
SCENES.append(s)
sfx("whoosh.mp3", T(99) - 0.02, 0.24)
sfx("whoosh-short.mp3", T(103), 0.16)
sfx("tv-blip-soft.wav", T(104), 0.18)
sfx("whoosh-short.mp3", T(106) - 0.02, 0.18)
sfx("impact-bass-1.mp3", T(110), 0.30)
sfx("whoosh-short.mp3", T(116), 0.14)
sfx("whoosh-short.mp3", T(120), 0.14)
cap([[W(99, "S", "He"), W(100, "S", "doesn't"), W(101, "S", "play"), W(102, "B", "characters")]], T(103), y=905)
cap([[W(103, "S", "he"), W(104, "S", "becomes")], [W(105, "XL", "them")]], T(106), x=96, y=400, align="left", lh=0.95)
cap([[W(106, "S", "He"), W(107, "S", "picks")], [W(108, "B", "roles")]], T(109), x=1820, y=540, align="right", lh=0.95)
cap([[W(109, "S", "that")], [W(110, "B", "scare")]], T(111), x=96, y=430, align="left", lh=0.95)
cap([[W(111, "S", "the"), W(112, "S", "shit"), W(113, "S", "out"), W(114, "S", "of")], [W(115, "B", "others")]], T(116),
    x=1820, y=250, align="right", lh=0.95)
cap([[W(116, "S", "the"), W(117, "S", "ones")], [W(118, "B", "everyone"), W(119, "B", "else")]], T(120), y=860, lh=0.95)
cap([[W(120, "M", "runs"), W(121, "M", "from")]], T(122), y=880)

# ---------------- S12 "And in 2026, we saw him do it all." (v4's "and this year?" paper, then the 1-2-3 triptych) ------
s = Scene("s12", T(122), T(131))
s.paper(T(122), T(125))
tri = [("t_odyssey.mp4", "1", T(125), 4.0), ("t_prime.mp4", "2", T(126), 2.5), ("t_dune.mp4", "3", T(127), 0.95)]
for k, (src, num, t0, clen) in enumerate(tri):
    d = T(131) - t0
    cam2, vid = s.video(src, t0, T(131), ms=0.0, rate=round(min(1, clen / d), 3), grade="matte", push=None,
                        box=(k * 640, 0, 640, 1080), cam_extra="clip-path:inset(0% 100% 0% 0%);")
    s.js.append(f'tl.fromTo("#{cam2}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
                f'duration: 0.24, ease: "expo.out" }}, {s.at(t0)});')
    s.numeral(num, round(t0 + 0.06, 3), T(131), x=k * 640 + 320, y=560, size=520)
    sfx("whoosh-short.mp3", t0, 0.20)
SCENES.append(s)
sfx("whoosh-short.mp3", T(122), 0.12)
paper_words([(122, "PS", "and"), (123, "PS", "in"), (124, "PXL", "2026")], T(125))
cap([[W(125, "S", "we"), W(126, "S", "saw"), W(127, "S", "him"), W(128, "M", "do"), W(129, "M", "it"), W(130, "M", "all")]],
    T(131), y=930)

# ---------------- S13 chapter 1: The Odyssey (v4, on the new words; "one of the story's central antagonists" is gone) ----
s = Scene("s13", T(131), T(139))
for k, (src, clen) in enumerate([("t_prime.mp4", 2.5), ("t_dune.mp4", 0.95)], start=1):
    cam2, vid = s.video(src, T(131), round(T(131) + 0.4, 3), ms=round(min(0.8, clen - 0.42), 2), grade="matte", push=None,
                        box=(k * 640, 0, 640, 1080))
    s.js.append(f'tl.fromTo("#{cam2}", {{ x: 0 }}, {{ x: 1300, duration: 0.34, ease: "power3.in" }}, 0);')
cam, vid = s.video("c_antinous_fire.mp4", T(131), T(133), ms=0.0, grade="matte", push=None,
                   cam_extra="clip-path:inset(0% 66.67% 0% 0%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 66.67% 0% 0%)", scale: 1.0 }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'scale: 1.0, duration: 0.36, ease: "power3.inOut" }}, 0);')
s.js.append(f'tl.to("#{cam}", {{ scale: 1.05, duration: {r3(T(133) - T(131) - 0.36)}, ease: "none" }}, 0.36);')
s.numeral("1", T(131), T(133), x=1500, y=470, size=600)
s.video("c_antinous_feast.mp4", T(133), T(135), grade="matte", push=(1.0, 1.06))
s.neg(T(133), 2)
camNo, imNo = s.image("nolan.jpg", round(T(133) + 0.04, 3), T(135), grade="matte", push=None, box=(1210, 150, 520, 620),
                      card=True)
s.js.append(f'tl.fromTo("#{camNo}", {{ scale: 0.35, opacity: 0, rotation: -6 }}, {{ scale: 1, opacity: 1, rotation: 3, '
            f'duration: 0.34, ease: "back.out(1.7)" }}, {s.at(T(133) + 0.04)});')
s.js.append(f'tl.to("#{camNo}", {{ scale: 1.04, duration: {r3(T(135) - T(133) - 0.38)}, ease: "none" }}, {s.at(T(133) + 0.38)});')
s.video("c_antinous_arch.mp4", T(135), T(137), grade="matte", push=(1.0, 1.07))
s.video("c_antinous_fire.mp4", T(137), T(139), ms=1.2, grade="matte", push=(1.0, 1.05))
s.neg(T(137), 2)
SCENES.append(s)
sfx("whoosh.mp3", T(131), 0.30)
sfx("whoosh-short.mp3", T(133), 0.16)
sfx("whoosh-short.mp3", T(135), 0.18)
sfx("whoosh-short.mp3", T(137), 0.18)
sfx("impact-bass-1.mp3", T(138), 0.22)
cap([[W(131, "S", "walked"), W(132, "S", "into")]], T(133), x=1500, y=900)
cap([[W(133, "S", "Christopher")], [W(134, "B", "Nolan's")]], T(135), x=140, y=620, align="left", lh=0.92)
cap([[W(135, "FSL", "The"), W(136, "FSL", "Odyssey")]], T(137), y=540)
cap([[W(137, "S", "as")], [W(138, "B", "Antinous")]], T(139), x=150, y=640, align="left")

# ---------------- S14 chapter 2: Primetime (v4) with the TV texture (VHS lines plus a CRT screen, user) --------------
GR["tv"] = _derive("vhs_soft", effects={"crtCurvature": 0.2})
s = Scene("s14", T(139), 66.70)
cam, vid = s.video("c_hansen.mp4", T(139), T(141), ms=0.0, grade="tv", push=None,
                   cam_extra="clip-path:inset(0% 33.33% 0% 33.33%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 33.33% 0% 33.33%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.36, ease: "power3.inOut" }}, 0);')
s.numeral("2", T(139), T(141), x=1500, y=470, size=600)
s.video("c_prime_title.mp4", T(141), T(142), grade="tv", push=(1.0, 1.05))
s.neg(T(141), 2)
s.video("c_hansen_cu.mp4", T(142), T(144), grade="tv", push=(1.0, 1.05))
s.video("c_hansen.mp4", T(144), T(147), ms=0.9, grade="tv", push=(1.05, 1.0))
s.video("c_schedule.mp4", T(147), T(148), grade="tv", push=(1.0, 1.05))
s.video("c_stinghouse.mp4", T(148), T(152), grade="tv", push=(1.0, 1.04))
s.video("c_pt_worried.mp4", T(152), T(153), grade="tv", push=(1.0, 1.06), rate=0.9)
s.video("c_chat.mp4", T(153), T(154), grade="glitch_soft", push=(1.0, 1.06))
s.neg(T(153), 2)
s.video("c_hiddencam.mp4", T(154), T(155), grade="glitch_soft", push=(1.0, 1.06))
s.video("c_hiddencam.mp4", T(154), round(T(154) + 4 / 30, 3), grade="crt", push=None)
rid = s.uid("rec")
s.raw(f'<div id="{rid}" class="clip rec" {s.timed(T(154), T(155))} data-track-index="6" '
      f'style="left:120px;top:96px;z-index:{s.nz()}"><i></i><span>REC</span></div>')
s.uses_text = True
s.video("c_strobeface.mp4", T(155), 64.55, grade="tv", push=(1.0, 1.06))
# the real "...why don't you have a seat right there?" moment, in sync with the sting audio; reframed (user) so his
# body shows -- the film's own subtitle carries the line, so ours is gone
s.video("c_seat1.mp4", 64.55, 66.02, grade="tv", push=(1.0, 1.04))
s.video("c_seat2.mp4", 66.02, 66.70, grade="tv", push=(1.04, 1.0))
SCENES.append(s)
sfx("whoosh.mp3", T(139), 0.26)
sfx("tv-blip-soft.wav", T(141), 0.30)
sfx("whoosh-short.mp3", T(142), 0.14)
sfx("whoosh-short.mp3", T(147), 0.12)
sfx("whoosh-short.mp3", T(153), 0.10)
sfx("tv-blip-soft.wav", T(154), 0.24)
cap([[W(139, "S", "then"), W(140, "S", "came")]], T(141), x=1500, y=900)
cap([[W(142, "S", "with"), W(143, "S", "Pattinson")]], T(144), x=1800, y=860, align="right")
cap([[W(144, "S", "playing"), W(145, "S", "a")]], T(146), x=1800, y=860, align="right")
cap([[W(146, "B", "television")]], T(147), x=1800, y=830, align="right")
cap([[W(147, "B", "journalist")]], T(148), y=880)
cap([[W(148, "S", "at"), W(149, "S", "the"), W(150, "S", "center"), W(151, "S", "of")]], T(152), y=880)
cap([[W(152, "B", "controversial")]], T(153), y=860)
cap([[W(153, "XL", "predator")]], T(154), y=860)
cap([[W(154, "M", "sting")]], T(155), y=560)
cap([[W(155, "B", "operations")]], 64.55, y=860)

# ---------------- S15 chapter 3: Dune (v4), the poster beat rebuilt as a Hemant Taneja wall (user) ------------------
s = Scene("s15", 66.70, T(167))
cam, vid = s.video("c_scytale.mp4", 66.70, T(158), ms=0.0, grade="matte", push=None,
                   cam_extra="clip-path:inset(0% 0% 0% 66.67%);")
s.js.append(f'tl.fromTo("#{cam}", {{ clipPath: "inset(0% 0% 0% 66.67%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.36, ease: "power3.inOut" }}, 0);')
s.numeral("3", 66.70, T(158), x=1500, y=470, size=600)
camY, vY = s.video("c_scytale.mp4", T(158), T(161), ms=1.0, grade="matte", push=None,
                   vars_style="--hf-color-grading-blur: 0.85;")
s.js.append(f'tl.fromTo("#{camY}", {{ x: 220, scale: 1.26 }}, {{ x: 0, scale: 1.05, duration: 0.22, ease: "power3.out" }}, '
            f'{s.at(T(158))});')
s.js.append(f'tl.to("#{camY}", {{ scale: 1.0, duration: {r3(T(161) - T(158) - 0.22)}, ease: "none" }}, {s.at(T(158) + 0.22)});')
s.js.append(f'tl.to("#{vY}", {{ "--hf-color-grading-blur": 0, duration: 0.28, ease: "power2.out" }}, {s.at(T(158))});')
s.video("c_scytale.mp4", T(161), T(163), ms=2.2, grade="matte", push=(1.0, 1.05))
s.neg(T(161), 2)
# "with Dune Part Three": the poster lands as a centred card on black (a white box first, one blown-out frame), then the
# Dune pictures pop out from behind it two frames apart, white boxes stepping out at a low frame rate, on a gentle dome;
# the wall keeps pulling back, a video tile blows out on "Part", the wall inverts on "Three", then pans out into the cut
DW, DW1, DT0 = T(163), T(167), T(164)
PST = (730, 110, 460, 690)
DTILES = [  # source, centre x, centre y, w, h, tilt, video media-start
    ("dune_scy.jpg", 400, 300, 280, 350, -4, None),
    ("c_scytale.mp4", 1540, 260, 380, 214, 3, 0.4),
    ("f_scytale.jpg", 380, 690, 380, 214, 3, None),
    ("dune_scy2.jpg", 1560, 650, 380, 214, -3, None),
    ("t_dune.mp4", 140, 470, 180, 304, -2, 0.0),
    ("f_kimmel_scytale.jpg", 1785, 455, 240, 135, 4, None),
]


def ddome(cx, cy, f):
    nx, ny = (cx - 960) / 960, (cy - 540) / 540
    return dict(rotationY=round(26 * nx * f, 2), rotationX=round(-16 * ny * f, 2), z=round(-150 * (nx * nx + ny * ny) * f, 1))


grp_first = len(s.els)
dt_els = []
for k, (src, cx, cy, w, h, rot, ms) in enumerate(DTILES):  # made first, so they sit behind the poster
    t0 = round(DT0 + k * 2 * F1, 3)
    box = (cx - w // 2, cy - h // 2, w, h)
    d0, d1 = ddome(cx, cy, 0.6), ddome(cx, cy, 1.0)
    bid = s.uid("pbox")
    s.raw(f'<div id="{bid}" class="clip pbox" {s.timed(round(t0 - 4 * F1, 3), t0)} data-track-index="5" '
          f'style="left:{box[0]}px;top:{box[1]}px;width:{w}px;height:{h}px;z-index:{s.nz()}"></div>')
    s.js.append(f'tl.fromTo("#{bid}", {{ x: {round((960 - cx) * 0.8)}, y: {round((455 - cy) * 0.8)}, scale: 0.45, rotation: 0, '
                f'rotationY: 0, rotationX: 0, z: 0 }}, {{ x: 0, y: 0, scale: 1, rotation: {rot}, rotationY: {d0["rotationY"]}, '
                f'rotationX: {d0["rotationX"]}, z: {d0["z"]}, duration: {r3(3 * F1)}, ease: "steps(3)" }}, {s.at(t0 - 4 * F1)});')
    s.js.append(f'tl.set("#{bid}", {{ filter: "blur(0px)" }}, {s.at(t0 - F1)});')
    if src.endswith(".mp4"):
        rate = round(min(1.0, (0.95 - ms) / (DW1 - t0)), 3) if src == "t_dune.mp4" else None  # the short Dune panel slows
        cam, mid = s.video(src, t0, DW1, ms=ms, rate=rate, grade="matte", push=None, box=box, card=True,
                           vars_style="--hf-color-grading-exposure: 0.85;")
    else:
        cam, mid = s.image(src, t0, DW1, grade="matte", push=None, box=box, card=True, pos="50% 35%",
                           vars_style="--hf-color-grading-blur: 0; --hf-color-grading-exposure: 0.85;")
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.06, rotation: {rot}, rotationY: {d0["rotationY"]}, rotationX: {d0["rotationX"]}, '
                f'z: {d0["z"]} }}, {s.at(t0)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0.25 }}, {s.at(t0 + F1)});')
    s.js.append(f'tl.set("#{cam}", {{ scale: 1.0 }}, {s.at(t0 + 2 * F1)});')
    s.js.append(f'tl.set("#{mid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(t0 + 2 * F1)});')
    nx, ny = (cx - 960) / 960, (cy - 540) / 540
    s.js.append(f'tl.to("#{cam}", {{ rotationY: {d1["rotationY"]}, rotationX: {d1["rotationX"]}, z: {d1["z"]}, '
                f'x: {round(40 * nx)}, y: {round(26 * ny)}, duration: {r3(DW1 - t0 - 2 * F1)}, ease: "sine.inOut" }}, '
                f'{s.at(t0 + 2 * F1)});')
    dt_els.append((cam, mid, src.endswith(".mp4")))
pbid = s.uid("pbox")
s.raw(f'<div id="{pbid}" class="clip pbox" {s.timed(round(DW - 2 * F1, 3), DW)} data-track-index="5" '
      f'style="left:{PST[0]}px;top:{PST[1]}px;width:{PST[2]}px;height:{PST[3]}px;z-index:{s.nz()}"></div>')
s.js.append(f'tl.set("#{pbid}", {{ filter: "blur(0px)" }}, {s.at(DW - F1)});')
camP, imP = s.image("dune_poster.jpg", DW, DW1, grade="matte", push=None, box=PST, card=True, pos="50% 40%",
                    vars_style="--hf-color-grading-blur: 0; --hf-color-grading-exposure: 0.85;")
s.js.append(f'tl.set("#{camP}", {{ scale: 1.06 }}, {s.at(DW)});')
s.js.append(f'tl.set("#{imP}", {{ "--hf-color-grading-exposure": 0.25 }}, {s.at(DW + F1)});')
s.js.append(f'tl.set("#{camP}", {{ scale: 1.0 }}, {s.at(DW + 2 * F1)});')
s.js.append(f'tl.set("#{imP}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(DW + 2 * F1)});')
gid = s.uid("wall")
inner = "".join(s.els[grp_first:])
del s.els[grp_first:]
s.els.append(f'<div class="cam" id="{gid}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
             f'perspective:1400px;perspective-origin:50% 45%;z-index:{s.nz()}">{inner}</div>')
s.js.append(f'tl.fromTo("#{gid}", {{ y: 0, rotation: 0 }}, {{ y: -14, rotation: -1.5, duration: 0.3, ease: "power2.out" }}, '
            f'{s.at(DT0)});')
s.js.append(f'tl.fromTo("#{gid}", {{ scale: 1.0 }}, {{ scale: 0.9, duration: {r3(DW1 - DW)}, ease: "sine.inOut", '
            f'immediateRender: false }}, {s.at(DW)});')
s.js.append(f'tl.fromTo("#{gid}", {{ x: 0 }}, {{ x: -230, duration: 0.3, ease: "power2.in", immediateRender: false }}, '
            f'{s.at(DW1 - 0.3)});')
s.neg(DT0, 3)  # v4's hit on "Dune"
bl_mid = dt_els[1][1]  # the Scytale video tile blows out for two frames on "Part"
s.js.append(f'tl.set("#{bl_mid}", {{ "--hf-color-grading-exposure": 1.5 }}, {s.at(T(165))});')
s.js.append(f'tl.set("#{bl_mid}", {{ "--hf-color-grading-exposure": 0 }}, {s.at(T(165) + 2 * F1)});')
s.neg(T(166), 2)  # the wall inverts on "Three"; the stills fall out of focus behind the poster
for cam, mid, isvid in dt_els:
    if not isvid:
        s.js.append(f'tl.to("#{mid}", {{ "--hf-color-grading-blur": 0.32, duration: 0.24, ease: "power2.out" }}, '
                    f'{s.at(T(166) + 2 * F1)});')
SCENES.append(s)
sfx("whoosh.mp3", 66.70, 0.28)
sfx("whoosh.mp3", T(158) - 0.04, 0.24)
sfx("whoosh-short.mp3", T(161), 0.16)
sfx("whoosh-short.mp3", DW, 0.14)
sfx("impact-bass-1.mp3", DT0, 0.42)
sfx("tv-blip-soft.wav", T(166), 0.16)
cap([[W(156, "S", "and"), W(157, "S", "now")]], T(158), x=1500, y=900)
cap([[W(158, "S", "he's"), W(159, "S", "closing"), W(160, "S", "out")]], T(161), y=880)
cap([[W(161, "S", "the"), W(162, "S", "year")]], T(163), y=880)
cap([[W(163, "S", "with"), W(164, "XL", "Dune"), W(165, "S", "Part"), W(166, "S", "Three")]], T(167), y=905)

# ---------------- S16 payoff + end card (v4, on the new words) ----------------
END = round(WORDS[192]["g_start"] + 0.63, 3)  # v4: the end card lands 0.63 s after "seen" starts
s = Scene("s16", T(167), DUR)
camP1, vP1 = s.video("c_venice.mp4", T(167), T(168), rate=0.75, grade="matte", push=(1.0, 1.06),
                     vars_style="--hf-color-grading-exposure: 1.0;")
s.blow_in(vP1, T(167), 0.3)
s.rgbsplit("c_venice.mp4", T(167), frames=2)
s.video("c_roles.mp4", T(168), T(171), grade="matte", push=(1.0, 1.04))
tiles = ["f_edward_cu.jpg", "gt_neon.jpg", "lh_soot.jpg", "tn_red.jpg", "bt_cowl.jpg", "mk_helmet.jpg", "f_hansen.jpg",
         "f_scytale.jpg", "f_king.jpg", "f_devil.jpg", "f_rover.jpg", "f_queen.jpg", "f_damsel.jpg", "f_dali.jpg",
         "f_bruce.jpg", "f_drama.jpg"]
s.grid(tiles, 4, 4, T(171), T(174))
s.neg(T(171), 2)
s.grid(tiles[:9], 3, 3, T(174), T(176))
s.grid(tiles[:4], 2, 2, T(176), T(178))
# "one box": Edward, playing inside a single framed square on paper, which then zooms through to full frame
s.paper(T(178), round(T(180) + 0.3, 3))
camB, vB = s.video("c_edward_cu.mp4", T(178), round(T(180) + 0.3, 3), grade="film_soft", push=None,
                   box=(660, 240, 600, 600), card=True)
s.js.append(f'tl.fromTo("#{camB}", {{ scale: 1.24, y: -34, rotation: -3, opacity: 0 }}, {{ scale: 1, y: 0, rotation: 0, '
            f'opacity: 1, duration: 0.26, ease: "expo.out" }}, {s.at(T(178))});')
s.js.append(f'tl.to("#{camB}", {{ scale: 1.03, duration: {r3(T(180) - T(178) - 0.26)}, ease: "none" }}, {s.at(T(178) + 0.26)});')
s.js.append(f'tl.to("#{camB}", {{ scale: 3.4, duration: 0.3, ease: "power3.in" }}, {s.at(T(180))});')
camE, vE = s.video("c_sparkle.mp4", round(T(180) + 0.3, 3), T(183), ms=0.2, grade="film_soft", push=(1.06, 1.12),
                   vars_style="--hf-color-grading-exposure: 0;")
s.blow_out(vE, T(183), 0.5, 1.9)
s.whiteflash(T(183), 0.22, 0.9)
cam, vid = s.video("h_edward.mp4", T(183), T(184), grade="film_soft", push=None, box=(0, 0, 960, 1080))
camBt, vBt = s.video("h_batman.mp4", T(183), T(184), grade="matte", push=None, box=(960, 0, 960, 1080))
s.js.append(f'tl.fromTo("#{camBt}", {{ x: 960 }}, {{ x: 0, duration: 0.28, ease: "expo.out" }}, {s.at(T(183) + 0.06)});')
s.paper(T(184), DUR)
# end card: the name in bold sans on paper (v5: paper words are bold Helvetica), a rule drawing out, a year counter
s.text("Robert", END, DUR, 960, 470, 170, family="Inter Tight", weight=800, color="#0B0B0B", glow=False, anim="ink",
       style="letter-spacing:-0.035em;")
s.text("Pattinson", round(END + 0.10, 3), DUR, 960, 640, 170, family="Inter Tight", weight=800, color="#0B0B0B",
       glow=False, anim="ink", style="letter-spacing:-0.035em;")
rule = s.uid("rule")
s.raw(f'<div id="{rule}" class="clip rule" {s.timed(round(END + 0.25, 3), DUR)} data-track-index="6" '
      f'style="left:660px;top:742px;width:600px;z-index:{s.nz()}"></div>')
s.js.append(f'tl.fromTo("#{rule}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "expo.out" }}, {s.at(END + 0.25)});')
yrs = ["2008", "2011", "2014", "2017", "2019", "2022", "2024", "2025", "2026"]
ytm = [round(END + d, 3) for d in (0.13, 0.16, 0.19, 0.23, 0.27, 0.32, 0.38, 0.45, 0.53)]
s.counter([(v, t) for v, t in zip(yrs, ytm)], DUR, 960, 850, 64, family="Inter Tight", weight=700, color="#0B0B0B",
          glow=False, ink=True)
SCENES.append(s)
TW = round(T(182) + 0.32, 3)  # "post-Twilight" is one token in the new transcript: "Twilight" lands 0.32 s after "post"
sfx("impact-bass-1.mp3", T(167), 0.28)
sfx("whoosh-short.mp3", T(168), 0.18)
sfx("whoosh-short.mp3", T(171), 0.16)
sfx("whoosh.mp3", T(180), 0.26)
sfx("whoosh-cinematic.mp3", TW, 0.28)
sfx("whoosh-short.mp3", T(183), 0.24)
sfx("impact-bass-1.mp3", END, 0.28)
cap([[W(167, "B", "Pattinson")]], T(168), y=900)
cap([[W(168, "S", "keeps"), W(169, "S", "choosing")]], T(170), y=880)
cap([[W(170, "XL", "roles")]], T(171), y=600)
cap([[W(171, "M", "that"), W(172, "M", "stop"), W(173, "M", "anyone")]], T(174), y=560)
cap([[W(174, "M", "from"), W(175, "M", "putting"), W(176, "M", "him")]], T(177), y=560)
cap([[W(177, "PS", "in"), W(178, "PS", "one")]], T(179), kind="paper", y=960)
cap([[W(179, "PB", "box")]], T(180), kind="paper", y=960)
cap([[W(180, "S", "and"), W(181, "S", "that")]], T(182), y=560)
cap([[("post", T(182), "S")]], TW, y=560)
cap([[("Twilight", TW, "XL")]], T(183), y=580)
cap([[W(183, "XL", "reinvention")]], T(184), y=580)
paper_words([(184, "PS", "might"), (185, "PS", "be"), (186, "PS", "one"), (187, "PS", "of"), (188, "PS", "the"),
             (189, "PXL", "best"), (190, "PS", "we've"), (191, "PS", "ever"), (192, "PXL", "seen")], END,
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
    for lid, t0, d in (("leak2", T(182) + 0.10, 1.30),):
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
    for aid, src, st, d, vol, lane in [("a-run", "a_run.wav", T(6), 0.641, 0.55, 12),
                                       ("a-kimmel", "a_kimmel.wav", T(8), 0.90, 0.5, 13)]:
        if st >= DUR:
            continue
        auds.append(f'<audio id="{aid}" class="clip" src="assets/audio/{src}" data-start="{r3(st)}" data-duration="{r3(d)}" '
                    f'data-volume="{vol}" data-fade-out="0.06" data-track-index="{lane}"></audio>')
    lanes = []  # end time per lane
    for k, (name, t, vol, ms, dur) in enumerate(sorted(SFX, key=lambda x: x[1])):
        start = max(0.0, round(t + 1 / 30 - PEAK.get(name, 0.05), 3))
        d = dur or SFXDUR.get(name, 1.0)
        fade = ""
        if start + d > DUR:  # cut by the end of the built part: fade it rather than stop it dead
            d = round(DUR - start, 3)
            fade = ' data-fade-out="0.25"'
        if d <= 0:
            continue
        lane = next((i for i, e in enumerate(lanes) if e <= start), None)
        if lane is None:
            lanes.append(0.0); lane = len(lanes) - 1
        lanes[lane] = start + d
        auds.append(f'<audio id="sfx{k:03d}" class="clip" src="assets/audio/sfx/{name}" data-start="{r3(start)}" '
                    f'data-duration="{r3(d)}" data-media-start="{r3(ms)}" data-volume="{vol}"{fade} data-track-index="{20 + lane}"></audio>')
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
