#!/usr/bin/env python3
"""Generate the HyperFrames compositions for the Jamie Dimon / JPMorgan Chase edit.

Style reference: the user's Larry Fink reel (dimon/reference/FINK_REEL_REFERENCE.md), measured frame by frame:
 - one bold grotesque (Inter Tight 700/800), no serif; small centred captions whose words cut on at the frame
   they are spoken, hero lockups (one big word with small context words tucked against it), white-bar
   write-ons on black, giant typed words on black that brighten grey -> white with jump reframes, a name that
   decodes letter by letter over a pale echo, a quote panel for the outside voice
 - a new picture every 1-3 words (median shot ~0.45 s), literal noun-to-picture mapping, mostly static shots
 - negative (inverted) flashes as the signature cut, white/grey flash frames, HUD wireframes, light rays,
   glitch and halftone frames, a window zoom-out, a card settle, a 2x2 grid assembly, a logo sting
 - dark contrasty grade with vignette; the user's own halftone and old-TV (RGB phosphor) textures over
   everything at low opacity

Opens on Dimon's own words (the user's pick from the interview): "We bank some of these companies in 30
countries. We bank countries. We bank the World Bank, the IMF. We bank the United States government. You have
to be big." Then the user's voiceover ("jamie dimon audio 2.0").

Writes dimon/index.html and compositions/*.html. All times below are GLOBAL seconds; each scene converts them
to local time. Every timed element is plain HTML with its own id, data-start and data-duration.
"""
import html, json, math, os, random, re, subprocess

ROOT = "/home/user/claude-test-2.0"
PRJ = f"{ROOT}/dimon"
COMP = f"{PRJ}/compositions"
F1 = 1 / 30
LEAD = 0.07          # captions and cuts land two frames before the word
SB_END = 9.15        # the opening soundbite (sync sound) ends here
OFF = 9.15           # the voiceover starts here
DUR = 87.0           # voiceover ends at 84.20, then the logo sting

GR = json.load(open(f"{PRJ}/tools/gradings.json"))


def _derive(base, adjust=None, effects=None, details=None, intensity=None):
    g = json.loads(GR[base])
    g["adjust"].update(adjust or {})
    g["effects"].update(effects or {})
    g["details"].update(details or {})
    if intensity is not None:
        g["intensity"] = intensity
    return json.dumps(g, separators=(",", ":"))


# the reference's look: dark, contrasty, desaturated, heavy vignette, light grain
GR["doc"] = _derive("matte", adjust={"contrast": 0.08, "highlights": -0.1, "shadows": -0.08, "blacks": -0.05,
                                     "saturation": -0.18},
                    details={"vignette": 0.34, "vignetteMidpoint": 0.46, "vignetteFeather": 0.7, "grain": 0.12})
GR["doc_bw"] = _derive("matte_bw", adjust={"contrast": 0.1, "saturation": -1.0},
                       details={"vignette": 0.36, "vignetteMidpoint": 0.45, "grain": 0.16})
GR["doc_warm"] = _derive("doc", adjust={"temperature": 0.2, "saturation": -0.12})
GR["gold"] = _derive("doc", adjust={"temperature": 0.34, "tint": 0.04, "saturation": 0.06, "highlights": 0.04})
# old TV screen (the user's request, at reduced strength): soft scanlines, a little curvature and bleed
GR["tv"] = _derive("vhs", effects={"tapeDamage": 0.15, "tapeTracking": 0.12, "chromaBleed": 0.25, "digitalGlitch": 0.0,
                                   "digitalGlitchLineTear": 0.0, "scanlines": 0.32, "crtCurvature": 0.12,
                                   "chromaticAberration": 0.14},
                   details={"vignette": 0.3, "vignetteMidpoint": 0.5, "grain": 0.14})
GR["glitch2"] = _derive("glitch", effects={"digitalGlitch": 0.9, "digitalGlitchColorSplit": 0.85,
                                           "digitalGlitchBlockAmount": 0.7, "chromaticAberration": 0.7})
GR["half"] = _derive("halftone", effects={"halftone": 1.0, "halftoneSize": 0.42})


def esc(s):
    return html.escape(s, quote=True)


def r3(x):
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def clip_dur(name):
    p = f"{PRJ}/assets/clips/{name}"
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


CLIPDUR = {f: clip_dur(f) for f in os.listdir(f"{PRJ}/assets/clips") if f.endswith(".mp4")}

# ---------------------------------------------------------------------------------------------------------------
# words: the voiceover (parakeet word times, fixed against the script) and the soundbite
# ---------------------------------------------------------------------------------------------------------------


def _vo_words():
    raw = [(w["text"], float(w["start"])) for w in json.load(open(f"{PRJ}/tools/words_vo_raw.json"))]
    out, k = [], 0
    while k < len(raw):
        t, s = raw[k]
        if t == "two" and raw[k + 1][0] == "thousand":
            out.append(("2008", s)); k += 3; continue
        if t == "J" and raw[k + 1][0] == "P":
            out.append(("JP", s)); k += 2; continue
        fix = {"Diamond,": "Dimon", "Weil": "Weill", "Turn": "turned", "ten": "$10"}
        out.append((fix.get(t, t), s))
        if t == "lends":
            out.append(("to", 13.52))  # parakeet drops "to" between "lends" and "countries"
        k += 1
    return out


def norm(s):
    return re.sub(r"[^a-z0-9$]", "", s.lower())


class Cursor:
    """Consumes the words in script order; take("a b=B c=") checks each word and returns (shown, edit time)."""

    def __init__(self, items, base):
        self.items, self.base, self.k = items, base, 0

    def take(self, phrase):
        out = []
        for tok in phrase.split():
            shown = tok
            if "=" in tok:
                tok, shown = tok.split("=", 1)
            text, t = self.items[self.k]
            assert norm(text) == norm(tok), f"expected {tok!r}, got {text!r} at word {self.k}"
            self.k += 1
            if shown:
                out.append((shown.replace("_", " "), round(self.base + t - LEAD, 3)))
        return out


VO = Cursor(_vo_words(), OFF)
SB = Cursor([(w["text"], float(w["start"])) for w in json.load(open(f"{PRJ}/tools/words_sb_raw.json"))], 0.0)

# ---------------------------------------------------------------------------------------------------------------
# type
# ---------------------------------------------------------------------------------------------------------------
FONTS_CSS = """
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-600.woff2') format('woff2'); font-weight: 600; font-style: normal; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-700.woff2') format('woff2'); font-weight: 700; font-style: normal; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-800.woff2') format('woff2'); font-weight: 800; font-style: normal; }
"""
HALO_S = "0 0 10px rgba(255,255,255,0.30), 0 2px 12px rgba(0,0,0,0.60)"
HALO_B = "0 0 22px rgba(255,255,255,0.34), 0 0 64px rgba(255,255,255,0.14), 0 6px 26px rgba(0,0,0,0.50)"
GLOW_TYPED = "0 0 26px rgba(255,255,255,0.55), 0 0 80px rgba(255,255,255,0.22)"

# ---------------------------------------------------------------------------------------------------------------
# scene builder
# ---------------------------------------------------------------------------------------------------------------


class Scene:
    def __init__(self, sid, start, end, ground="#050505"):
        self.sid, self.start, self.end, self.ground = sid, round(start, 3), round(end, 3), ground
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
        t0 = max(round(t0, 3), self.start)
        t1 = min(round(t1, 3), self.end)
        return f'data-start="{r3(self.L(t0))}" data-duration="{r3(round(t1 - t0, 3))}"'

    # ---- media -------------------------------------------------------------------------------------------------
    def video(self, src, t0, t1, ms=0.0, rate=None, grade="doc", push=(1.0, 1.04), box=None, pushease="none",
              vars_style="", z=None, cam_extra="", fit=True, opacity=None, blend=None):
        name = src if src.endswith(".mp4") else f"{src}.mp4"
        slot = round(t1 - t0, 3)
        if name[:2] in ("r_", "s_"):
            # a baked speed ramp / stutter clip: its timing is designed for this slot, never re-timed
            fit = False
            if CLIPDUR[name] - ms < slot - 0.02:
                print(f"WARNING {name}: {CLIPDUR[name] - ms:.2f}s of ramp for a {slot:.2f}s slot")
        if rate is None and fit:
            avail = CLIPDUR[name] - ms - 0.04
            if slot > avail:
                rate = round(max(0.3, avail / slot), 3)
        cam, vid = self.uid("cam"), self.uid("v")
        z = z or self.nz()
        grading = f' data-color-grading="{esc(GR[grade])}"' if grade else ""
        rate_attr = f' data-playback-rate="{rate}"' if rate else ""
        x, y, w, h = box or (0, 0, 1920, 1080)
        extra = (f"opacity:{opacity};" if opacity is not None else "") + (f"mix-blend-mode:{blend};" if blend else "")
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{extra}{cam_extra}">'
            f'<video id="{vid}" class="clip" src="assets/clips/{name}" muted playsinline {self.timed(t0, t1)} '
            f'data-hf-media-start-basis="local" data-media-start="{r3(ms)}"{rate_attr}{grading} data-track-index="2" '
            f'style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:cover;{vars_style}"></video></div>')
        if push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {r3(slot)}, '
                           f'ease: "{pushease}" }}, {self.at(t0)});')
        return cam, vid

    def image(self, src, t0, t1, grade="doc", push=(1.0, 1.05), box=None, fit="cover", pos="center", z=None,
              vars_style="", cam_extra="", cls="clip"):
        cam, im = self.uid("cam"), self.uid("i")
        z = z or self.nz()
        grading = f' data-color-grading="{esc(GR[grade])}"' if grade else ""
        x, y, w, h = box or (0, 0, 1920, 1080)
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{cam_extra}">'
            f'<img id="{im}" class="{cls}" src="assets/img/{src}" alt="" {self.timed(t0, t1)}{grading} data-track-index="3" '
            f'style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:{fit};object-position:{pos};'
            f'{vars_style}" /></div>')
        if push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {r3(t1 - t0)}, '
                           f'ease: "none" }}, {self.at(t0)});')
        return cam, im

    # ---- camera speed ramps (keyframed: fast-then-slow, slow-then-fast) ------------------------------------------
    def ramp_push(self, cam, t0, t1, s0=1.0, s1=1.22, x1=0, y1=0, fast=5, share=0.82):
        """Fast-then-slow push: `share` of the move lands in `fast` frames (power3.out), the rest drifts."""
        d = t1 - t0
        tf = min(fast * F1, d * 0.5)
        sm = s0 + (s1 - s0) * share
        self.js.append(f'tl.fromTo("#{cam}", {{ scale: {s0}, x: 0, y: 0 }}, {{ scale: {sm:.4f}, x: {x1 * share:.0f}, '
                       f'y: {y1 * share:.0f}, duration: {r3(tf)}, ease: "power3.out", immediateRender: false }}, {self.at(t0)});')
        self.js.append(f'tl.to("#{cam}", {{ scale: {s1}, x: {x1}, y: {y1}, duration: {r3(d - tf)}, ease: "sine.out" }}, '
                       f'{self.at(t0 + tf)});')

    def ramp_into(self, cam, t0, t1, s0=1.0, s1=1.42, drift=0.035, fast=0.17, rot=0):
        """Slow-then-fast: a slow drift that accelerates (expo.in) into the cut."""
        d = t1 - t0
        fast = min(fast, d * 0.45)
        self.js.append(f'tl.fromTo("#{cam}", {{ scale: {s0}, rotation: 0 }}, {{ scale: {s0 + drift}, duration: {r3(d - fast)}, '
                       f'ease: "sine.inOut", immediateRender: false }}, {self.at(t0)});')
        self.js.append(f'tl.to("#{cam}", {{ scale: {s1}, rotation: {rot}, duration: {r3(fast)}, ease: "expo.in" }}, '
                       f'{self.at(t1 - fast)});')

    def ramp_land(self, cam, t0, t1, s0=1.5, s1=1.0, rot=0, fast=0.32, x0=0):
        """The far side of a zoom-through: arrives fast from a big scale, decelerates (expo.out), then drifts."""
        d = t1 - t0
        fast = min(fast, d)
        self.js.append(f'tl.fromTo("#{cam}", {{ scale: {s0}, rotation: {rot}, x: {x0} }}, {{ scale: {s1 + 0.012}, rotation: 0, '
                       f'x: 0, duration: {r3(fast)}, ease: "expo.out", immediateRender: false }}, {self.at(t0)});')
        if d > fast + 0.02:
            self.js.append(f'tl.to("#{cam}", {{ scale: {s1 + 0.035}, duration: {r3(d - fast)}, ease: "none" }}, '
                           f'{self.at(t0 + fast)});')

    def style_strobe(self, src, t0, t1, frames=2, seed=4):
        """One picture in six looks, 2 frames each (the reference's walking-man strobe)."""
        looks = [("doc", None), ("half", None), ("doc_bw", ("#6a1fd0", "lighten", "#ff8a1e", "multiply")),
                 ("doc_bw", None), ("pixel", ("#1238d8", "lighten", "#ff2a3a", "multiply")),
                 ("doc_bw", ("#ffffff", "difference", "#ff2bd6", "multiply"))]
        step = round(frames * F1, 3)
        t, k = t0, 0
        while t < t1 - 0.01:
            b = min(round(t + step, 3), t1)
            grade, tint = looks[k % len(looks)]
            self.image(src, t, b, grade=grade, push=None)
            if tint:
                for col, mode in ((tint[0], tint[1]), (tint[2], tint[3])):
                    oid = self.uid("tint")
                    self.els.append(f'<div id="{oid}" class="clip solid" {self.timed(t, b)} data-track-index="5" '
                                    f'style="background:{col};mix-blend-mode:{mode};z-index:{self.nz()}"></div>')
            t, k = b, k + 1

    def dust(self, t0, t1, box, seed=9, n=240):
        """A picture breaking into white dust that blows outward and thins into the starfield."""
        rnd = random.Random(seed)
        did = self.uid("dust")
        x, y, w, h = box
        cx, cy = x + w / 2, y + h / 2
        dots = []
        for k in range(n):
            px, py = rnd.uniform(x, x + w), rnd.uniform(y, y + h)
            r = rnd.choice([1.0, 1.4, 1.8, 2.2, 3.0])
            dots.append(f'<circle id="{did}-p{k}" cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="#ffffff" opacity="0" />')
            ang = math.atan2(py - cy, px - cx) + rnd.uniform(-0.5, 0.5)
            dist = rnd.uniform(160, 900)
            dl = rnd.uniform(0, 0.16)
            fin = rnd.uniform(0.0, 0.55)
            self.js.append(f'tl.fromTo("#{did}-p{k}", {{ x: 0, y: 0, opacity: 0 }}, {{ x: {math.cos(ang) * dist:.0f}, '
                           f'y: {math.sin(ang) * dist:.0f}, opacity: 1, duration: 0.05, ease: "none" }}, {self.at(t0 + dl)});')
            self.js.append(f'tl.to("#{did}-p{k}", {{ x: {math.cos(ang) * dist * 1.25:.0f}, y: {math.sin(ang) * dist * 1.25:.0f}, '
                           f'opacity: {fin:.2f}, duration: {r3(t1 - t0 - dl - 0.05)}, ease: "expo.out" }}, {self.at(t0 + dl + 0.05)});')
        self.els.append(f'<svg id="{did}" class="clip" {self.timed(t0, t1)} data-track-index="6" viewBox="0 0 1920 1080" '
                        f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible;z-index:{self.nz()}">'
                        f'{"".join(dots)}</svg>')

    # ---- more of the reference's motion graphics ---------------------------------------------------------------
    def godrays(self, t0, t1, cx, cy, rgb="255,200,110", opacity=0.45, blend="screen"):
        """Slow-turning tinted light rays over the picture (the reference's light bursts)."""
        gid = self.uid("god")
        self.els.append(f'<div id="{gid}" class="clip rays" {self.timed(t0, t1)} data-track-index="6" data-layout-ignore '
                        f'style="left:{cx - 1400}px;top:{cy - 1400}px;z-index:{self.nz() + 60};mix-blend-mode:{blend};'
                        f'background:repeating-conic-gradient(from 0deg, rgba({rgb},0.9) 0deg 4deg, rgba({rgb},0) 4deg 15deg)"></div>')
        self.js.append(f'tl.fromTo("#{gid}", {{ scale: 0.86, rotation: -6, opacity: 0 }}, {{ scale: 1.0, rotation: 0, opacity: {opacity}, '
                       f'duration: 0.16, ease: "power2.out", immediateRender: false }}, {self.at(t0)});')
        self.js.append(f'tl.to("#{gid}", {{ scale: 1.08, rotation: 9, duration: {r3(t1 - t0 - 0.16)}, ease: "none" }}, {self.at(t0 + 0.16)});')

    def collage(self, t0, t_zoom, t1, stills, seed=13, ground="#F3F2EE", grade="doc_bw", cy=430):
        """The reference's collage on white: the centre card flips to a new picture every 2 frames, then the
        camera pulls out (expo.out) to the whole wall of cards."""
        rnd = random.Random(seed)
        outer, wall = self.uid("colw"), self.uid("wall")
        cw, ch, px, py, S0 = 360, 240, 400, 345, 2.5
        cards, n = [], 0
        gr = f' data-color-grading="{esc(GR[grade])}"' if grade else ""

        def img(src, a, b):
            return (f'<img id="{self.uid("ci")}" class="clip" src="assets/img/{src}" alt="" data-start="{self.at(a)}" data-duration="{r3(round(b - a, 3))}"'
                    f'{gr} data-track-index="3" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover" />')
        for r in (-1, 0, 1):
            for c in (-2, -1, 0, 1, 2):
                centre = (r, c) == (0, 0)
                x = 960 + c * px - cw / 2 + (0 if centre else rnd.randint(-18, 18))
                y = cy + r * py - ch / 2 + (0 if centre else rnd.randint(-14, 14))
                cid = self.uid("cc")
                if centre:
                    inner, t, k = [], t0, 0
                    while t < t_zoom - 0.01:
                        b = min(round(t + 2 * F1, 3), t_zoom)
                        inner.append(img(stills[k % len(stills)], t, b))
                        self.js.append(f'tl.set("#{cid}", {{ rotation: {rnd.uniform(-3.5, 3.5):.1f} }}, {self.at(t)});')
                        t, k = b, k + 1
                    inner.append(img(stills[k % len(stills)], t_zoom, t1))
                    self.js.append(f'tl.set("#{cid}", {{ rotation: 0 }}, {self.at(t_zoom)});')
                    rot = ""
                else:
                    inner = [img(stills[(n * 3 + 1) % len(stills)], t0 + (n % 8) * 0.004, t1)]
                    rot = f"transform:rotate({rnd.uniform(-5, 5):.1f}deg);"
                cards.append(f'<div id="{cid}" class="ccard" style="left:{x:.0f}px;top:{y:.0f}px;width:{cw}px;height:{ch}px;{rot}'
                             f'z-index:{30 if centre else 1}">{"".join(inner)}</div>')
                n += 1
        self.els.append(f'<div id="{outer}" class="clip" {self.timed(t0, t1)} data-track-index="4" '
                        f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:{ground};z-index:{self.nz()}">'
                        f'<div class="cam" id="{wall}" style="left:0;top:0;width:1920px;height:1080px;transform-origin:960px {cy}px">'
                        f'{"".join(cards)}</div></div>')
        self.js.append(f'tl.set("#{wall}", {{ scale: {S0} }}, {self.at(t0)});')
        self.js.append(f'tl.fromTo("#{wall}", {{ scale: {S0} }}, {{ scale: 1.0, duration: 0.42, ease: "expo.out", immediateRender: false }}, '
                       f'{self.at(t_zoom)});')
        if t1 - t_zoom > 0.44:
            self.js.append(f'tl.to("#{wall}", {{ scale: 0.965, duration: {r3(t1 - t_zoom - 0.42)}, ease: "none" }}, {self.at(t_zoom + 0.42)});')

    def flipcal(self, t0, t1, pages, step=1.45, box=(1090, 285, 440, 500)):
        """A desk calendar flipping a page a month (the reference's flip-calendar for "in a single quarter")."""
        x, y, w, h = box
        outer = self.uid("cal")
        parts = []
        for k, (mon, yr) in enumerate(pages):
            ta = round(t0 + round(k * step) * F1, 3)
            pid = f"{outer}-p{k}"
            parts.append(f'<div id="{pid}" class="clip calpage" data-start="{self.at(ta)}" data-duration="{r3(round(t1 - ta, 3))}" '
                         f'data-track-index="5" data-layout-ignore style="z-index:{k + 2}"><div class="calband">{yr}</div><div class="calmon">{mon}</div></div>')
            if k:
                self.js.append(f'tl.fromTo("#{pid}", {{ rotationX: 82 }}, {{ rotationX: 0, duration: {r3(1.4 * F1)}, ease: "power2.in", '
                               f'immediateRender: false }}, {self.at(ta)});')
        rings = "".join(f'<i class="calring" style="left:{rx:.0f}px"></i>' for rx in (w * 0.24, w * 0.76 - 22))
        self.els.append(f'<div id="{outer}" class="clip" {self.timed(t0, t1)} data-track-index="5" '
                        f'style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;perspective:900px;z-index:{self.nz()}">'
                        f'<div class="calback"></div>{"".join(parts)}{rings}</div>')
        self.js.append(f'tl.fromTo("#{outer}", {{ scale: 1.12, rotation: -3 }}, {{ scale: 1.0, rotation: 0, duration: 0.3, ease: "expo.out", '
                       f'immediateRender: false }}, {self.at(t0)});')

    def linechart(self, t0, t1, keys, seed=5, box=(250, 160, 1420, 600)):
        """A line chart drawing itself with a moving cursor (the reference's growth chart). keys: [(t, 0..1)];
        the fall is drawn red, the climb white."""
        rnd = random.Random(seed)
        x0, y0, W, H = box
        cid = self.uid("chart")
        tk = [t for t, _ in keys]
        N = max(8, int((tk[-1] - tk[0]) * 40))
        pts = []
        for i in range(N + 1):
            t = tk[0] + (tk[-1] - tk[0]) * i / N
            for j in range(len(keys) - 1):
                if keys[j][0] <= t <= keys[j + 1][0] + 1e-9:
                    f = (t - keys[j][0]) / max(1e-6, keys[j + 1][0] - keys[j][0])
                    v = keys[j][1] + (keys[j + 1][1] - keys[j][1]) * f
                    break
            if 0 < i < N:
                v += rnd.uniform(-0.018, 0.018)
            pts.append((round(t, 4), x0 + W * i / N, y0 + H * (1 - v)))
        imin = max(range(len(pts)), key=lambda i: pts[i][2])
        grid = "".join(f'<line x1="{x0}" y1="{y0 + H * k / 5:.0f}" x2="{x0 + W}" y2="{y0 + H * k / 5:.0f}" />' for k in range(6))
        grid += "".join(f'<line x1="{x0 + W * k / 10:.0f}" y1="{y0}" x2="{x0 + W * k / 10:.0f}" y2="{y0 + H}" />' for k in range(11))
        paths = []
        for pi, seg in enumerate((pts[:imin + 1], pts[imin:])):
            d = "M" + " L".join(f"{x:.1f},{y:.1f}" for _, x, y in seg)
            L = sum(math.hypot(seg[i + 1][1] - seg[i][1], seg[i + 1][2] - seg[i][2]) for i in range(len(seg) - 1))
            pid = f"{cid}-l{pi}"
            col = "#ff3b3b" if pi == 0 else "#ffffff"
            paths.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round" '
                         f'stroke-linecap="round" stroke-dasharray="{L:.1f}" stroke-dashoffset="{L:.1f}" />')
            acc = 0.0
            for i in range(len(seg) - 1):
                acc += math.hypot(seg[i + 1][1] - seg[i][1], seg[i + 1][2] - seg[i][2])
                self.js.append(f'tl.to("#{pid}", {{ attr: {{ "stroke-dashoffset": {L - acc:.1f} }}, duration: {r3(seg[i + 1][0] - seg[i][0])}, '
                               f'ease: "none" }}, {self.at(seg[i][0])});')
        cur, cl = f"{cid}-cur", f"{cid}-cl"
        for i in range(len(pts) - 1):
            dt = r3(pts[i + 1][0] - pts[i][0])
            self.js.append(f'tl.to("#{cur}", {{ attr: {{ cx: {pts[i + 1][1]:.1f}, cy: {pts[i + 1][2]:.1f} }}, duration: {dt}, ease: "none" }}, {self.at(pts[i][0])});')
            self.js.append(f'tl.to("#{cl}", {{ attr: {{ x1: {pts[i + 1][1]:.1f}, x2: {pts[i + 1][1]:.1f}, y1: {pts[i + 1][2]:.1f} }}, duration: {dt}, '
                           f'ease: "none" }}, {self.at(pts[i][0])});')
        _, sx, sy = pts[0]
        self.els.append(
            f'<svg id="{cid}" class="clip chart" {self.timed(t0, t1)} data-track-index="5" data-layout-ignore viewBox="0 0 1920 1080" '
            f'style="z-index:{self.nz()}"><g class="grid">{grid}</g>'
            f'<line id="{cl}" x1="{sx:.1f}" y1="{sy:.1f}" x2="{sx:.1f}" y2="{y0 + H}" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="6 8" />'
            f'<g class="glow">{"".join(paths)}</g>'
            f'<circle id="{cur}" cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="#ffffff" class="glow" /></svg>')

    def screens3d(self, t0, t_fall, t1, items, grade="doc"):
        """Floating screens in a dark 3D space with the camera drifting through them (the reference's gallery of
        floating screens); on t_fall they drop out of frame one after another, accelerating."""
        stage = self.uid("stage")
        layout = [(0, -10, 0, 0, 760, 428), (-650, -250, -420, 28, 560, 315), (660, -215, -380, -26, 560, 315),
                  (-610, 300, -300, 22, 520, 292), (640, 305, -330, -24, 520, 292)]
        scr = []
        gr = lambda g: f' data-color-grading="{esc(GR[g])}"' if g else ""
        for k, ((dx, dy, dz, ry, w, h), src) in enumerate(zip(layout, items)):
            sid = f"{stage}-s{k}"
            if src.endswith(".mp4"):
                avail = CLIPDUR[src] - 0.04
                rate = round(max(0.3, avail / (t1 - t0)), 3) if t1 - t0 > avail else None
                media = (f'<video id="{sid}v" class="clip" src="assets/clips/{src}" muted playsinline {self.timed(t0, t1)} '
                         f'data-hf-media-start-basis="local" data-media-start="0"{f" data-playback-rate=" + chr(34) + str(rate) + chr(34) if rate else ""}'
                         f'{gr("tv")} data-track-index="2" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover"></video>')
            else:
                media = (f'<img id="{sid}i" class="clip" src="assets/img/{src}" alt="" {self.timed(t0, t1)}{gr(grade)} data-track-index="3" '
                         f'style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover" />')
            frame = f'<div id="{sid}f" class="clip scrframe" {self.timed(t0, t1)} data-track-index="4"></div>'
            scr.append(f'<div id="{sid}" class="scr" style="left:{960 - w / 2:.0f}px;top:{540 - h / 2:.0f}px;width:{w}px;height:{h}px">'
                       f'{media}{frame}</div>')
            self.js.append(f'tl.fromTo("#{sid}", {{ x: {dx}, y: {dy}, z: {dz - 260}, rotationY: {ry} }}, {{ z: {dz + 110}, rotationY: {ry * 0.75:.1f}, '
                           f'duration: {r3(t_fall - t0)}, ease: "sine.inOut", immediateRender: false }}, {self.at(t0)});')
            self.js.append(f'tl.to("#{sid}", {{ y: {dy + 1350}, rotationX: -48, rotation: {(1 if k % 2 else -1) * 13}, '
                           f'duration: 0.5, ease: "power2.in" }}, {self.at(t_fall + k * 2 * F1)});')
        self.els.append(f'<div id="{stage}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;perspective:1200px;'
                        f'perspective-origin:50% 45%;transform-style:preserve-3d;z-index:{self.nz()}">{"".join(scr)}</div>')

    def split3(self, items, t_end):
        """Three vertical panels slide in one after another, alternating up and down (the reference's split panels)."""
        for k, (src, t, ms, grade) in enumerate(items):
            cam, _ = self.video(src, t, t_end, ms=ms, grade=grade, push=None, box=(k * 640, 0, 640, 1080), cam_extra="overflow:hidden;")
            dy = -1080 if k % 2 == 0 else 1080
            self.js.append(f'tl.fromTo("#{cam}", {{ y: {dy} }}, {{ y: 0, duration: 0.24, ease: "expo.out", immediateRender: false }}, {self.at(t)});')
            if k:
                seam = self.uid("seam")
                self.els.append(f'<div id="{seam}" class="clip solid" {self.timed(t, t_end)} data-track-index="5" '
                                f'style="left:{k * 640 - 2}px;width:4px;background:#ffffff;z-index:{self.nz()}"></div>')

    def ring_beat(self, t0, t1, src, cx=960, cy=430, r=250, color="#1A6FD1", grade="doc"):
        """A ring filling around a circular portrait while the camera pushes in 19 % (the reference's donut charts
        around the subject's eye)."""
        grp, vid, svg = self.uid("ringg"), self.uid("v"), self.uid("ring")
        avail = CLIPDUR[src] - 0.04
        rate = round(max(0.3, avail / (t1 - t0)), 3) if t1 - t0 > avail else None
        C = 2 * math.pi * r
        ticks = "".join(
            f'<line x1="{cx + (r + 34) * math.cos(a):.1f}" y1="{cy + (r + 34) * math.sin(a):.1f}" '
            f'x2="{cx + (r + (50 if k % 5 == 0 else 42)) * math.cos(a):.1f}" y2="{cy + (r + (50 if k % 5 == 0 else 42)) * math.sin(a):.1f}" />'
            for k, a in ((k, 2 * math.pi * k / 60 - math.pi / 2) for k in range(60)))
        arc, dotg = f"{svg}-arc", f"{svg}-dot"
        self.els.append(
            f'<div class="cam" id="{grp}" style="left:0;top:0;width:1920px;height:1080px;transform-origin:{cx}px {cy}px;z-index:{self.nz()}">'
            f'<div style="position:absolute;left:{cx - r + 20}px;top:{cy - r + 20}px;width:{2 * r - 40}px;height:{2 * r - 40}px;'
            f'border-radius:50%;overflow:hidden">'
            f'<video id="{vid}" class="clip" src="assets/clips/{src}" muted playsinline {self.timed(t0, t1)} data-hf-media-start-basis="local" '
            f'data-media-start="0"{f" data-playback-rate=" + chr(34) + str(rate) + chr(34) if rate else ""} data-color-grading="{esc(GR[grade])}" '
            f'data-track-index="2" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover"></video></div>'
            f'<svg id="{svg}" class="clip ring" {self.timed(t0, t1)} data-track-index="5" data-layout-ignore viewBox="0 0 1920 1080">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity="0.16" stroke-width="30" />'
            f'<circle id="{arc}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="30" stroke-dasharray="{C:.1f}" '
            f'stroke-dashoffset="{C:.1f}" transform="rotate(-90 {cx} {cy})" class="glow" />'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 24}" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2" />'
            f'<g stroke="#ffffff" stroke-opacity="0.5" stroke-width="2">{ticks}</g>'
            f'<g id="{dotg}"><circle cx="{cx}" cy="{cy - r}" r="13" fill="#ffffff" class="glow" /></g></svg></div>')
        d = r3(t1 - t0 - 0.1)
        self.js.append(f'tl.fromTo("#{grp}", {{ scale: 0.94 }}, {{ scale: 1.19, duration: {r3(t1 - t0)}, ease: "power1.inOut", immediateRender: false }}, {self.at(t0)});')
        self.js.append(f'tl.to("#{arc}", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: {d}, ease: "power2.inOut" }}, {self.at(t0)});')
        self.js.append(f'tl.fromTo("#{dotg}", {{ rotation: 0 }}, {{ rotation: 360, svgOrigin: "{cx} {cy}", duration: {d}, ease: "power2.inOut", '
                       f'immediateRender: false }}, {self.at(t0)});')

    def solid(self, t0, t1, color="#000", z=None):
        sid = self.uid("solid")
        self.els.append(f'<div id="{sid}" class="clip solid" {self.timed(t0, t1)} data-track-index="4" '
                        f'style="background:{color};z-index:{z or self.nz()}"></div>')
        return sid

    def raw(self, el):
        self.els.append(el)

    # ---- the reference's transitions -------------------------------------------------------------------------
    def neg(self, t, frames=2):
        """Inverted frames (the reference's signature cut), on the global invert layer above everything."""
        t0 = max(round(t, 3), self.start)
        t1 = min(round(t + frames * F1, 3), self.end)
        if t1 > t0:
            NEGS.append((t0, t1))

    def flash(self, t, frames=1, color="#ffffff"):
        """Flat flash frames (white or grey)."""
        fid = self.uid("fl")
        self.els.append(f'<div id="{fid}" class="clip solid" {self.timed(t, t + frames * F1)} data-track-index="5" '
                        f'style="background:{color};z-index:{self.nz()}"></div>')

    def whiteflash(self, t, d=0.2, peak=0.95):
        fid = self.uid("wf")
        self.els.append(f'<div id="{fid}" class="clip flashw" {self.timed(t - 0.06, t + d)} data-track-index="5" '
                        f'style="z-index:{self.nz()}"></div>')
        self.js.append(f'tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: {peak}, duration: 0.06, ease: "power4.in" }}, {self.at(t - 0.06)});')
        self.js.append(f'tl.to("#{fid}", {{ opacity: 0, duration: {r3(d - 0.01)}, ease: "power2.out" }}, {self.at(t)});')

    def fx_frames(self, src, t, frames, grade, ms=0.0, image=False, box=None):
        """A few frames of the same picture through a stronger treatment (glitch or halftone hits)."""
        if image:
            return self.image(src, t, t + frames * F1, grade=grade, push=None, box=box)
        return self.video(src, t, t + frames * F1, ms=ms, grade=grade, push=None, box=box, fit=False)

    def hud(self, t0, t1, seed=1, opacity=0.8):
        """HUD wireframes: thin squares, connecting lines, triangles and tiny hex labels, re-laid every 2 frames."""
        rnd = random.Random(seed)
        hid = self.uid("hud")
        groups, js = [], []
        nfr = max(1, int(round((t1 - t0) / (2 * F1))))
        for k in range(nfr):
            parts, pts = [], []
            for _ in range(rnd.randint(3, 6)):
                s = rnd.choice([40, 56, 72, 96, 130, 170])
                x, y = rnd.randint(40, 1880 - s), rnd.randint(40, 1040 - s)
                pts.append((x + s / 2, y + s / 2))
                parts.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" />')
                if rnd.random() < 0.5:
                    parts.append(f'<text x="{x}" y="{y - 6}">{rnd.randint(100, 999)}.{rnd.randint(100, 999)}.{rnd.choice("ABCDEF")}{rnd.choice("ABCDEF")}{rnd.choice("ABCDEF")}</text>')
            for a, b in zip(pts, pts[1:]):
                parts.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" />')
            if rnd.random() < 0.6:
                x, y = rnd.randint(100, 1800), rnd.randint(100, 980)
                parts.append(f'<polygon points="{x},{y} {x + 46},{y + 70} {x - 40},{y + 64}" />')
            gid = f"{hid}-g{k}"
            groups.append(f'<g id="{gid}" style="opacity:0">{"".join(parts)}</g>')
            tk = t0 + k * 2 * F1
            self.js.append(f'tl.set("#{gid}", {{ opacity: 1 }}, {self.at(tk)});')
            self.js.append(f'tl.set("#{gid}", {{ opacity: 0 }}, {self.at(tk + 2 * F1)});')
        self.els.append(
            f'<svg id="{hid}" class="clip hud" {self.timed(t0, t1)} data-track-index="6" data-layout-ignore viewBox="0 0 1920 1080" '
            f'style="z-index:{self.nz()};opacity:{opacity}">{"".join(groups)}</svg>')

    def stars(self, t0, t1, seed=3, n=170):
        """A drifting starfield with a few bokeh stars and twinkles (the reference's space behind the seal)."""
        rnd = random.Random(seed)
        sid = self.uid("stars")
        dots = []
        for k in range(n):
            x, y = rnd.uniform(0, 1920), rnd.uniform(0, 1080)
            r = rnd.choice([0.8, 1.0, 1.2, 1.5, 1.8, 2.4]) if rnd.random() < 0.92 else rnd.uniform(5, 11)
            col = rnd.choice(["#ffffff", "#ffffff", "#ffffff", "#dfe9ff", "#ffd9d9", "#d9fff4"])
            op = rnd.uniform(0.35, 1.0) if r < 4 else rnd.uniform(0.18, 0.4)
            dots.append(f'<circle id="{sid}-d{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="{op:.2f}" />')
            if r < 4 and rnd.random() < 0.15:
                tt = rnd.uniform(t0, t1 - 0.1)
                self.js.append(f'tl.set("#{sid}-d{k}", {{ opacity: 0.08 }}, {self.at(tt)});')
                self.js.append(f'tl.set("#{sid}-d{k}", {{ opacity: {op:.2f} }}, {self.at(tt + 2 * F1)});')
        cam = self.uid("cam")
        self.els.append(f'<div class="cam" id="{cam}" style="left:0;top:0;width:1920px;height:1080px;z-index:{self.nz()}">'
                        f'<svg id="{sid}" class="clip" {self.timed(t0, t1)} data-track-index="4" viewBox="0 0 1920 1080" '
                        f'style="position:absolute;left:0;top:0;width:1920px;height:1080px">{"".join(dots)}</svg></div>')
        self.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {r3(t1 - t0)}, ease: "none" }}, {self.at(t0)});')

    def glint(self, t, x, y, size=180, d=0.3):
        """A four-point light glint that grows and fades."""
        gid = self.uid("glint")
        self.els.append(f'<div id="{gid}" class="clip glint" {self.timed(t, t + d)} data-track-index="6" '
                        f'style="left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px;width:{size}px;height:{size}px;z-index:{self.nz()}"></div>')
        self.js.append(f'tl.fromTo("#{gid}", {{ scale: 0.2, rotation: 0, opacity: 0 }}, {{ scale: 1.0, rotation: 30, opacity: 1, '
                       f'duration: {r3(d * 0.55)}, ease: "power2.out" }}, {self.at(t)});')
        self.js.append(f'tl.to("#{gid}", {{ scale: 0.6, opacity: 0, duration: {r3(d * 0.45)}, ease: "power2.in" }}, {self.at(t + d * 0.55)});')

    def rays(self, t0, t1, cx=960, cy=540):
        """Light rays bursting from a point until they fill the frame white."""
        rid = self.uid("rays")
        self.els.append(f'<div id="{rid}" class="clip rays" {self.timed(t0, t1)} data-track-index="6" '
                        f'style="left:{cx - 1400}px;top:{cy - 1400}px;z-index:{self.nz()}"></div>')
        d = round(t1 - t0, 3)
        self.js.append(f'tl.fromTo("#{rid}", {{ scale: 0.12, rotation: -8, opacity: 0.2 }}, {{ scale: 1.6, rotation: 16, opacity: 1, '
                       f'duration: {r3(d)}, ease: "power2.in" }}, {self.at(t0)});')

    def strobe(self, items, t0, t1, frames=3, grade="doc"):
        """Pictures swapping every few frames (the reference's photo flips)."""
        step = round(frames * F1, 3)
        k, t = 0, t0
        while t < t1 - 0.01:
            b = min(round(t + step, 3), t1)
            src = items[k % len(items)]
            if src.endswith(".mp4"):
                self.video(src, t, b, grade=grade, push=None)
            else:
                self.image(src, t, b, grade=grade, push=None)
            t, k = b, k + 1

    def grid2(self, tiles, t1, grade="doc"):
        """A 2x2 grid assembling tile by tile, each landing on a one-frame white flash."""
        boxes = [(0, 0), (960, 0), (0, 540), (960, 540)]
        for (src, t), (x, y) in zip(tiles, boxes):
            self.image(src, t, t1, grade=grade, push=(1.06, 1.0), box=(x + 3, y + 3, 954, 534))
            fid = self.uid("tf")
            self.els.append(f'<div id="{fid}" class="clip solid" {self.timed(t, t + F1)} data-track-index="5" '
                            f'style="left:{x}px;top:{y}px;width:960px;height:540px;background:#fff;z-index:{self.nz()}"></div>')

    def faceboxes(self, t0, t1, boxes):
        """Face-detection boxes over a film shot (the reference's Wolf of Wall Street frames)."""
        for k, (x, y, w, h, color, label) in enumerate(boxes):
            bid = self.uid("fbox")
            lab = f'<i style="background:{color}">{label}</i>' if label else ""
            self.els.append(f'<div id="{bid}" class="clip fbox" {self.timed(t0 + k * F1, t1)} data-track-index="6" data-layout-ignore '
                            f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-color:{color};z-index:{self.nz()}">{lab}</div>')
            for j in range(int((t1 - t0) / (4 * F1))):  # boxes re-fit every 4 frames, like a detector
                tt = t0 + (j + 1) * 4 * F1
                dx, dy = ((-1) ** j) * (3 + j % 3), ((-1) ** (j + k)) * (2 + j % 2)
                self.js.append(f'tl.set("#{bid}", {{ x: {dx}, y: {dy} }}, {self.at(tt)});')

    def write(self):
        css = f"""
  {FONTS_CSS if self.uses_text else ''}
  #root {{ position: absolute; inset: 0; overflow: hidden; background: {self.ground}; }}
  #root .cam {{ position: absolute; transform-origin: 50% 50%; }}
  #root .solid {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .neg {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #ffffff; mix-blend-mode: difference; }}
  #root .flashw {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #ffffff; opacity: 0; }}
  #root .hud {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; fill: none; stroke: #ffffff; stroke-width: 1.4; }}
  #root .hud text {{ fill: #ffffff; stroke: none; font-family: 'Inter Tight', sans-serif; font-weight: 600; font-size: 11px; letter-spacing: 0.06em; }}
  #root .glint {{ position: absolute; background:
      linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.95) 50%, rgba(255,255,255,0) 100%) center / 100% 4px no-repeat,
      linear-gradient(0deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.95) 50%, rgba(255,255,255,0) 100%) center / 4px 100% no-repeat,
      radial-gradient(closest-side, rgba(255,255,255,0.9), rgba(255,255,255,0) 70%) center / 26% 26% no-repeat; }}
  #root .rays {{ position: absolute; width: 2800px; height: 2800px; border-radius: 50%;
    background: repeating-conic-gradient(from 0deg, rgba(255,255,255,0.95) 0deg 5deg, rgba(255,255,255,0) 5deg 16deg);
    -webkit-mask-image: radial-gradient(closest-side, #000 0%, #000 30%, rgba(0,0,0,0) 100%);
    mask-image: radial-gradient(closest-side, #000 0%, #000 30%, rgba(0,0,0,0) 100%); }}
  #root .fbox {{ position: absolute; border: 2px solid; box-sizing: border-box; }}
  #root .fbox i {{ position: absolute; left: -2px; top: -22px; padding: 2px 6px; font: 600 13px 'Inter Tight', sans-serif;
    font-style: normal; color: #ffffff; letter-spacing: 0.02em; }}
  #root .card {{ position: absolute; box-shadow: 0 30px 70px rgba(0,0,0,0.28), 0 4px 12px rgba(0,0,0,0.18); overflow: hidden; }}
  #root .wcard {{ position: absolute; background: #ffffff; box-shadow: 0 0 60px rgba(255,255,255,0.55), 0 0 140px rgba(255,255,255,0.25); }}
  #root .tx {{ position: absolute; white-space: nowrap; font-family: 'Inter Tight', sans-serif; line-height: 1; }}
  #root .wipebar {{ position: absolute; top: 0; width: 70px; height: 1080px; background: #ffffff;
    box-shadow: 0 0 40px 18px rgba(255,255,255,0.7); }}
  #root .ccard {{ position: absolute; background: #ffffff; border: 7px solid #ffffff; box-sizing: border-box; overflow: hidden;
    box-shadow: 0 12px 30px rgba(0,0,0,0.22), 0 2px 6px rgba(0,0,0,0.12); }}
  #root .calback {{ position: absolute; left: 10px; top: 14px; width: 100%; height: 100%; border-radius: 14px; background: #bdbdbd;
    box-shadow: 0 24px 60px rgba(0,0,0,0.55); }}
  #root .calpage {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: 14px; overflow: hidden; background: #f4f2ee;
    transform-origin: 50% 0%; box-shadow: 0 3px 0 #d4d2ce; font-family: 'Inter Tight', sans-serif; }}
  #root .calband {{ height: 118px; background: #c8102e; color: #ffffff; font-weight: 800; font-size: 62px; letter-spacing: 0.02em;
    display: flex; align-items: center; justify-content: center; }}
  #root .calmon {{ height: calc(100% - 118px); display: flex; align-items: center; justify-content: center; color: #111111;
    font-weight: 800; font-size: 178px; letter-spacing: -0.04em; }}
  #root .calring {{ position: absolute; top: -20px; width: 22px; height: 46px; border-radius: 11px; z-index: 60;
    background: linear-gradient(90deg, #8b8b8b, #e9e9e9 50%, #7b7b7b); }}
  #root .chart {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .chart .grid line {{ stroke: #ffffff; stroke-opacity: 0.1; stroke-width: 1.5; }}
  #root .glow {{ filter: drop-shadow(0 0 10px rgba(255,255,255,0.55)); }}
  #root .scr {{ position: absolute; background: #000000; overflow: hidden; }}
  #root .scrframe {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; box-sizing: border-box;
    border: 2px solid rgba(255,255,255,0.92); box-shadow: inset 0 0 40px rgba(0,0,0,0.5), 0 0 40px rgba(255,255,255,0.22); }}
  #root .ring {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }}
  #root .streak {{ position: absolute; height: 3px; width: 520px; border-radius: 2px;
    background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.95)); box-shadow: 0 0 14px rgba(255,255,255,0.8); }}
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


# ---------------------------------------------------------------------------------------------------------------
# captions: one composition, global times
# ---------------------------------------------------------------------------------------------------------------
CAPS = []
NEGS = []


def Wr(words, size=56, weight=700):
    return dict(kind="w", words=words, size=size, weight=weight)


def SWAP(values, size=200, weight=800, chrome=False):
    return dict(kind="swap", values=values, size=size, weight=weight, chrome=chrome)


def COUNT(a, b, t0, t1, size=230):
    n = b - a + 1
    vals = [(str(a + k), round(t0 + (t1 - t0) * k / (n - 1), 3)) for k in range(n)]
    return SWAP(vals, size=size)


def CUT(word, t_cut, size=190):
    return dict(kind="cut", words=[word], t_cut=t_cut, size=size, weight=800)


def line(words, end, y=540, size=56):
    CAPS.append(dict(kind="lock", rows=[Wr(words, size)], end=end, x=None, y=y, align="center", tone="lt"))


def lock(rows, end, x=None, y=540, align="center", tone="lt"):
    CAPS.append(dict(kind="lock", rows=rows, end=end, x=x, y=y, align=align, tone=tone))


def bars(words, end, y=540, size=72):
    CAPS.append(dict(kind="bars", words=words, end=end, y=y, size=size))


def typed(words, end, y=560, size=320, mode="follow", pre=None, cadence=1):
    CAPS.append(dict(kind="typed", words=words, end=end, y=y, size=size, mode=mode, pre=pre, cadence=cadence))


def quote(lines, end, x=150, y=500, size=46):
    CAPS.append(dict(kind="quote", lines=lines, end=end, x=x, y=y, size=size))


ADV = dict(zip("abcdefghijklmnopqrstuvwxyz", [.55, .58, .52, .58, .55, .33, .58, .58, .25, .25, .53, .25, .86, .58, .57,
                                               .58, .58, .38, .50, .36, .58, .53, .78, .52, .53, .50]))


def adv(ch):
    if ch.isdigit():
        return 0.57
    if ch == " ":
        return 0.25
    if ch in "$":
        return 0.57
    if ch in ",.":
        return 0.27
    if ch.isupper():
        return {"I": 0.27, "T": 0.58, "W": 0.92, "M": 0.84}.get(ch, 0.66)
    return ADV.get(ch, 0.55)


def build_captions():
    els, js = [], []
    first_t = {}

    def word_span(sid, text, tone, ml):
        return f'<span id="{sid}" class="w {tone}" style="{ml}">{esc(text)}</span>'

    for gi, g in enumerate(CAPS):
        gid = f"cg{gi:03d}"
        k = g["kind"]
        if k == "lock":
            t0 = min(min(t for _, t in r.get("words", []) or [(0, 9e9)]) if r["kind"] != "swap" else r["values"][0][1]
                     for r in g["rows"])
            t1 = g["end"]
            if g["align"] == "center":
                box = "left:0;width:1920px;align-items:center;"
            elif g["align"] == "left":
                box = f"left:{g['x']}px;width:1800px;align-items:flex-start;"
            else:
                box = f"left:{g['x'] - 1800}px;width:1800px;align-items:flex-end;"
            rows_html = []
            n_rows = len(g["rows"])
            for ri, r in enumerate(g["rows"]):
                big = r["size"] >= 120
                tone = g["tone"] + (" big" if big else "")
                track = "-0.045em" if big else "-0.02em"
                lh = 0.88 if big else 1.0
                tuck = ""
                if n_rows > 1:
                    if not big and ri < n_rows - 1 and g["rows"][ri + 1]["size"] >= 120:
                        tuck = "margin-bottom:-0.06em;"
                    if not big and ri > 0 and g["rows"][ri - 1]["size"] >= 120:
                        tuck = "margin-top:0.02em;"
                style = (f'font-size:{r["size"]}px;font-weight:{r["weight"]};letter-spacing:{track};line-height:{lh};{tuck}')
                rid = f"{gid}-r{ri}"
                if r["kind"] == "w":
                    spans = []
                    for wi, (text, t) in enumerate(r["words"]):
                        sid = f"{rid}w{wi}"
                        spans.append(word_span(sid, text, tone, "" if wi == 0 else "margin-left:0.24em;"))
                        js.append(f'tl.set("#{sid}", {{ opacity: 1 }}, {r3(t)});')
                    rows_html.append(f'<div class="row" id="{rid}" style="{style}">{"".join(spans)}</div>')
                elif r["kind"] == "swap":
                    longest = max((v for v, _ in r["values"]), key=len)
                    cls = tone + (" chrome" if r.get("chrome") else "")
                    parts = [f'<span class="w spacer" style="opacity:0">{esc(longest)}</span>']
                    vals = r["values"]
                    for vi, (text, t) in enumerate(vals):
                        sid = f"{rid}v{vi}"
                        parts.append(f'<span id="{sid}" class="w {cls} swapv">{esc(text)}</span>')
                        js.append(f'tl.set("#{sid}", {{ opacity: 1 }}, {r3(t)});')
                        if vi < len(vals) - 1:
                            js.append(f'tl.set("#{sid}", {{ opacity: 0 }}, {r3(vals[vi + 1][1])});')
                    pos = "left:0;" if g["align"] != "right" else "right:0;"
                    rows_html.append(f'<div class="row swap" id="{rid}" style="{style}--pos:{pos}">{"".join(parts)}</div>')
                elif r["kind"] == "cut":
                    text, t = r["words"][0]
                    top, bot = f"{rid}top", f"{rid}bot"
                    rows_html.append(
                        f'<div class="row cutw" id="{rid}" style="{style}">'
                        f'<span class="w spacer" style="opacity:0">{esc(text)}</span>'
                        f'<span id="{top}" class="w {tone} half top">{esc(text)}</span>'
                        f'<span id="{bot}" class="w {tone} half bot">{esc(text)}</span>'
                        f'<i id="{rid}line" class="cutline"></i></div>')
                    js.append(f'tl.set("#{top}", {{ opacity: 1 }}, {r3(t)});')
                    js.append(f'tl.set("#{bot}", {{ opacity: 1 }}, {r3(t)});')
                    js.append(f'tl.to("#{top}", {{ x: -46, y: -6, duration: 0.14, ease: "power3.out" }}, {r3(r["t_cut"])});')
                    js.append(f'tl.to("#{bot}", {{ x: 46, y: 6, duration: 0.14, ease: "power3.out" }}, {r3(r["t_cut"])});')
                    js.append(f'tl.set("#{rid}line", {{ opacity: 1 }}, {r3(r["t_cut"])});')
                    js.append(f'tl.set("#{rid}line", {{ opacity: 0 }}, {r3(r["t_cut"] + 2 * F1)});')
            els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(round(t1 - t0, 3))}" '
                       f'data-track-index="1" data-layout-allow-overflow data-layout-allow-overlap '
                       f'style="top:{g["y"] - 540}px;{box}">{"".join(rows_html)}</div>')
        elif k == "bars":
            words = g["words"]
            t0 = round(words[0][1] - 3 * F1, 3)
            t1 = g["end"]
            spans = []
            for wi, (text, t) in enumerate(words):
                sid = f"{gid}w{wi}"
                ml = "" if wi == 0 else "margin-left:0.26em;"
                spans.append(f'<span class="bw" style="{ml}"><i class="bb" id="{sid}b"></i><b class="bt" id="{sid}t">{esc(text)}</b></span>')
                js.append(f'tl.set("#{sid}b", {{ opacity: 1 }}, {r3(t - 3 * F1)});')
                js.append(f'tl.set("#{sid}b", {{ opacity: 0 }}, {r3(t)});')
                js.append(f'tl.set("#{sid}t", {{ opacity: 1 }}, {r3(t)});')
            sw = f"{gid}sw"
            js.append(f'tl.fromTo("#{sw}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {r3(3 * F1)}, ease: "steps(3)" }}, {r3(t1 - 4 * F1)});')
            for wi in range(len(words)):
                js.append(f'tl.set("#{gid}w{wi}t", {{ opacity: 0 }}, {r3(t1 - F1)});')
            els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(round(t1 - t0, 3))}" '
                       f'data-track-index="1" data-layout-allow-overflow data-layout-allow-overlap '
                       f'style="top:{g["y"] - 540}px;left:0;width:1920px;align-items:center;">'
                       f'<div class="row bars" style="font-size:{g["size"]}px;font-weight:700;letter-spacing:-0.02em">'
                       f'{"".join(spans)}<i class="sweep" id="{sw}"></i></div></div>')
        elif k == "typed":
            size, words = g["size"], g["words"]
            chars = []  # (char, t)
            for wi, (text, t) in enumerate(words):
                if wi:
                    chars.append((" ", t))
                for ci, ch in enumerate(text):
                    chars.append((ch, round(t + ci * g["cadence"] * F1, 3)))
            t0 = round(min(t for _, t in chars) - F1, 3)
            if g["pre"]:
                t0 = min(t0, round(g["pre"][1] - F1, 3))
            t1 = g["end"]
            widths = [adv(c) * size * 0.96 for c, _ in chars]
            total = sum(widths)
            tw = f"{gid}tw"
            spans = []
            for ci, (ch, t) in enumerate(chars):
                sid = f"{gid}c{ci}"
                spans.append(f'<span id="{sid}" class="ch">{"&nbsp;" if ch == " " else esc(ch)}</span>')
                if ch != " ":
                    js.append(f'tl.set("#{sid}", {{ opacity: 1 }}, {r3(t)});')
                    js.append(f'tl.set("#{sid}", {{ color: "#a9a9a9" }}, {r3(t + F1)});')
                    js.append(f'tl.set("#{sid}", {{ color: "#f4f2ee" }}, {r3(t + 2 * F1)});')
            # reframing: "follow" keeps the newest letter inside the right of the frame, jumping like the reference;
            # "center" re-centres the typed part on every letter
            x_left = 960 - total / 2
            last_shift = None
            for ci, (ch, t) in enumerate(chars):
                typed_w = sum(widths[:ci + 1])
                if g["mode"] == "center":
                    shift = (960 - typed_w / 2) - x_left
                else:
                    start_x = 0.30 * 1920
                    shift = start_x - x_left + min(0, 0.86 * 1920 - (start_x + typed_w))
                if last_shift is None or abs(shift - last_shift) > 90 or ci == len(chars) - 1:
                    js.append(f'tl.set("#{tw}", {{ x: {shift:.0f} }}, {r3(t)});')
                    last_shift = shift
            pre_html = ""
            if g["pre"]:
                ptext, pt, psize = g["pre"]
                pid = f"{gid}pre"
                pre_html = f'<div id="{pid}" class="tpre" style="font-size:{psize}px">{esc(ptext)}</div>'
                js.append(f'tl.set("#{pid}", {{ opacity: 1 }}, {r3(pt)});')
                # when the big word starts, the small word jumps up and grows (the reference's "By 2007")
                js.append(f'tl.set("#{pid}", {{ y: -{size * 0.62:.0f}, scale: 1.7 }}, {r3(chars[0][1])});')
            els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(round(t1 - t0, 3))}" '
                       f'data-track-index="1" data-layout-allow-overflow data-layout-allow-overlap '
                       f'style="top:{g["y"] - 540}px;left:0;width:1920px;align-items:center;">{pre_html}'
                       f'<div class="typedrow"><div id="{tw}" class="tw" style="font-size:{size}px;width:{total + 40:.0f}px">'
                       f'{"".join(spans)}</div></div></div>')
        elif k == "quote":
            t0 = round(min(t for ln in g["lines"] for _, t in ln) - 4 * F1, 3)
            t1 = g["end"]
            rows = []
            for li, ln in enumerate(g["lines"]):
                spans = []
                for wi, (text, t) in enumerate(ln):
                    sid = f"{gid}l{li}w{wi}"
                    ml = "" if wi == 0 else "margin-left:0.26em;"
                    spans.append(f'<span class="qw" style="{ml}"><i class="qb" id="{sid}b"></i><b class="qt" id="{sid}t">{esc(text)}</b></span>')
                    js.append(f'tl.set("#{sid}b", {{ opacity: 0.6 }}, {r3(t - 3 * F1)});')
                    for j, (ob, ot) in enumerate(((0.42, 0.35), (0.22, 0.7), (0, 1))):
                        js.append(f'tl.set("#{sid}b", {{ opacity: {ob} }}, {r3(t + j * F1)});')
                        js.append(f'tl.set("#{sid}t", {{ opacity: {ot} }}, {r3(t + j * F1)});')
                rows.append(f'<div class="row qrow" style="font-size:{g["size"]}px">{"".join(spans)}</div>')
            els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(round(t1 - t0, 3))}" '
                       f'data-track-index="1" data-layout-allow-overflow data-layout-allow-overlap '
                       f'style="top:{g["y"] - 540}px;left:{g["x"]}px;width:1000px;align-items:flex-start;">'
                       f'<div class="qm">&ldquo;</div>{"".join(rows)}<div class="qm qm2">&rdquo;</div></div>')
    css = f"""
  {FONTS_CSS}
  #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; font-family: 'Inter Tight', sans-serif; }}
  #root .cg {{ position: absolute; height: 1080px; display: flex; flex-direction: column; justify-content: center; }}
  #root .row {{ display: flex; flex-direction: row; align-items: baseline; white-space: nowrap; position: relative; }}
  #root .w {{ display: inline-block; white-space: nowrap; position: relative; opacity: 0; }}
  #root .lt {{ color: #F6F3EE; text-shadow: {HALO_S}; }}
  #root .lt.big {{ text-shadow: {HALO_B}; }}
  #root .dk {{ color: #111111; }}
  #root .chrome {{ background: linear-gradient(180deg, #ffffff 0%, #f3f6f8 38%, #9fb6c6 52%, #e9f2f6 64%, #ffffff 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent; text-shadow: none;
    filter: drop-shadow(0 0 18px rgba(170,230,255,0.35)); }}
  #root .swap {{ position: relative; }}
  #root .swapv {{ position: absolute; top: 0; left: 0; }}
  #root .cutw .half {{ position: absolute; left: 0; top: 0; }}
  #root .cutw .top {{ clip-path: inset(0 0 52% 0); }}
  #root .cutw .bot {{ clip-path: inset(48% 0 0 0); }}
  #root .cutline {{ position: absolute; left: -4%; width: 108%; top: 50%; height: 4px; background: #ffffff; opacity: 0;
    box-shadow: 0 0 18px 4px rgba(255,255,255,0.8); }}
  #root .bars {{ color: #F6F3EE; }}
  #root .bw {{ position: relative; display: inline-block; }}
  #root .bb {{ position: absolute; left: -0.05em; right: -0.05em; top: 0.16em; bottom: 0.02em; background: #ffffff; opacity: 0; }}
  #root .bt {{ opacity: 0; font-weight: 700; }}
  #root .sweep {{ position: absolute; left: -0.08em; right: -0.08em; top: 0.16em; bottom: 0.02em; background: #ffffff; transform-origin: 0% 50%; }}
  #root .typedrow {{ position: relative; width: 1920px; display: flex; justify-content: center; }}
  #root .tw {{ display: flex; flex-direction: row; white-space: nowrap; font-weight: 800; letter-spacing: -0.04em; line-height: 1;
    text-shadow: {GLOW_TYPED}; }}
  #root .ch {{ display: inline-block; opacity: 0; color: #5c5c5c; }}
  #root .tpre {{ font-weight: 700; color: #F6F3EE; opacity: 0; text-shadow: {HALO_S}; transform-origin: 50% 50%; margin-bottom: 10px; }}
  #root .qm {{ font-size: 170px; font-weight: 800; color: #ffffff; line-height: 0.6; height: 0.62em; text-shadow: {HALO_S}; }}
  #root .qm2 {{ align-self: flex-end; margin-right: 60px; margin-top: 20px; }}
  #root .qrow {{ font-weight: 700; color: #F6F3EE; line-height: 1.12; letter-spacing: -0.015em; text-shadow: {HALO_S}; }}
  #root .qw {{ position: relative; display: inline-block; }}
  #root .qb {{ position: absolute; left: -0.06em; right: -0.06em; top: 0.12em; bottom: 0.06em; background: rgba(255,255,255,0.85);
    box-shadow: 0 0 14px rgba(255,255,255,0.55); opacity: 0; }}
  #root .qt {{ opacity: 0; font-weight: 700; }}
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


# ---------------------------------------------------------------------------------------------------------------
# sound
# ---------------------------------------------------------------------------------------------------------------
SFX = []
PEAK = {"whoosh.mp3": 0.165, "whoosh-short.mp3": 0.165, "impact-bass-1.mp3": 0.04, "impact-bass-2.mp3": 2.066,
        "pop.mp3": 0.122, "click.mp3": 0.075, "click-soft.mp3": 0.075, "key-press.mp3": 0.08, "sparkle.mp3": 0.03,
        "glitch-1.mp3": 0.818, "glitch-3.mp3": 0.293, "whoosh-cinematic.mp3": 2.55, "tv-blip-soft.wav": 0.262,
        "riser.mp3": 3.037, "typing.mp3": 0.05}
SFXDUR = {"whoosh.mp3": 0.57, "whoosh-short.mp3": 0.57, "impact-bass-1.mp3": 2.11, "impact-bass-2.mp3": 2.59,
          "pop.mp3": 0.72, "click.mp3": 0.36, "click-soft.mp3": 0.36, "key-press.mp3": 0.43, "sparkle.mp3": 1.8,
          "glitch-1.mp3": 2.63, "glitch-3.mp3": 3.09, "whoosh-cinematic.mp3": 5.54, "tv-blip-soft.wav": 0.5,
          "riser.mp3": 3.1, "typing.mp3": 0.9}


def sfx(name, t, vol=0.2, dur=None):
    SFX.append((name, t, vol, dur))


SCENES = []

# ===============================================================================================================
# THE EDIT
# ===============================================================================================================
# ---- S01 the cold open: Dimon's own words (sync), as the reference's quote panel and literal pictures -------------
q1 = SB.take("We bank some of these companies in thirty=30 countries")
q2 = SB.take("We bank countries")
q3 = SB.take("We bank the World Bank")
q4 = SB.take("the IMF")
q5 = SB.take("we=We bank the United States government")
q6 = SB.take("You have to be big")
T_CTRY, T_WB, T_IMF, T_GOV = q2[0][1], q3[0][1], q4[0][1], q5[0][1]
T_TWO = 7.95  # the source cuts to its wide two-shot here (sb_two starts at this frame)

s = Scene("s01", 0.0, SB_END)
s.video("sb_cu.mp4", 0.0, T_CTRY, grade="doc", push=(1.0, 1.035))
# the reference's ghost portrait behind the quote, with a glint on the eye
s.image("ghost_bw.jpg", 0.0, T_CTRY, grade="doc_bw", push=(1.04, 1.0), box=(60, 150, 640, 780),
        cam_extra="opacity:0.17;mix-blend-mode:screen;")
s.glint(1.15, 395, 455, size=170, d=0.32)
s.hud(0.0, 0.47, seed=11, opacity=0.75)
# "We bank countries": Dimon with heads of government, three frames each
s.neg(T_CTRY, 2)
s.strobe(["lead_japan1.jpg", "lead_macri.jpg", "lead_reeves1.jpg", "lead_japan2.jpg", "dimon_davos.jpg",
          "lead_reeves2.jpg", "lead_japan3.jpg", "dimon_mcdermott.jpg"], T_CTRY, T_WB, frames=3)
# "We bank the World Bank"
s.neg(T_WB, 2)
s.image("wb_2.jpg", T_WB, q3[4][1], grade="doc", push=(1.0, 1.05))
camWB1, _ = s.image("wb_1.jpg", q3[4][1], T_IMF + 4 * F1, grade="doc", push=(1.04, 1.0))
s.js.append(f'tl.to("#{camWB1}", {{ opacity: 0, duration: {r3(4 * F1)}, ease: "steps(4)" }}, {s.at(T_IMF)});')
s.dust(T_IMF - F1, T_TWO - 3 * F1, (420, 180, 1080, 720), seed=9, n=260)
# "the IMF": white bars on black (the scene's black ground)
# "We bank the United States government": the presidential seal holding the government, on a starfield
s.stars(T_IMF, T_TWO, seed=5)
SEAL = (700, 520, 300)  # centre x, y, radius
cx, cy, R = SEAL
seal_cam = s.uid("seal")
hole = s.uid("hole")
gov = ["gov_capitol.jpg", "gov_wh1.jpg", "gov_treasury.jpg", "gov_fed.jpg", "gov_wh2.jpg", "gov_gallatin.jpg",
       "gov_fed_old.jpg"]
imgs, t, k = [], T_GOV, 0
T_SEAL_FULL = q5[5][1]
while t < T_SEAL_FULL - 0.01:
    b = min(round(t + 3 * F1, 3), T_SEAL_FULL)
    iid = s.uid("gi")
    imgs.append(f'<img id="{iid}" class="clip" src="assets/img/{gov[k % len(gov)]}" alt="" {s.timed(t, b)} '
                f'data-color-grading="{esc(GR["doc"])}" data-track-index="3" '
                f'style="position:absolute;left:0;top:0;width:{2 * R}px;height:{2 * R}px;object-fit:cover" />')
    t, k = b, k + 1
ring = s.uid("ring")
full = s.uid("full")
s.raw(f'<div class="cam" id="{seal_cam}" style="left:{cx - R}px;top:{cy - R}px;width:{2 * R}px;height:{2 * R}px;z-index:{s.nz()}">'
      f'<div id="{hole}" style="position:absolute;left:0;top:0;width:{2 * R}px;height:{2 * R}px;border-radius:50%;overflow:hidden">{"".join(imgs)}</div>'
      f'<img id="{ring}" class="clip" src="assets/img/seal.png" alt="" {s.timed(T_GOV, T_SEAL_FULL)} data-track-index="4" '
      f'style="position:absolute;left:0;top:0;width:{2 * R}px;height:{2 * R}px;'
      f'-webkit-mask-image:radial-gradient(circle closest-side, rgba(0,0,0,0) 0 74.5%, #000 75.5%);mask-image:radial-gradient(circle closest-side, rgba(0,0,0,0) 0 74.5%, #000 75.5%)" />'
      f'<img id="{full}" class="clip" src="assets/img/seal.png" alt="" {s.timed(T_SEAL_FULL, T_TWO)} data-track-index="4" '
      f'style="position:absolute;left:0;top:0;width:{2 * R}px;height:{2 * R}px" /></div>')
s.js.append(f'tl.fromTo("#{seal_cam}", {{ scale: 0.55, rotation: -4 }}, {{ scale: 1.0, rotation: 0, duration: 0.5, ease: "power3.out" }}, {s.at(T_GOV)});')
s.js.append(f'tl.to("#{seal_cam}", {{ scale: 1.08, duration: {r3(T_TWO - T_GOV - 0.5)}, ease: "none" }}, {s.at(T_GOV + 0.5)});')
s.hud(T_GOV, T_GOV + 0.4, seed=12, opacity=0.6)
s.glint(T_SEAL_FULL + 0.12, cx, cy, size=420, d=0.34)
s.rays(T_SEAL_FULL + 0.36, T_TWO - F1 * 3, cx=cx, cy=cy)
s.flash(T_TWO - 3 * F1, 3, "#ffffff")
# "You have to be big": the source's own two-shot, with a hard punch-in on "big"
camT, vT = s.video("sb_two.mp4", T_TWO, SB_END, grade="doc", push=None)
T_BIG = q6[4][1]
s.ramp_push(camT, T_BIG, SB_END, s0=1.0, s1=1.6, x1=-532, y1=108, fast=3, share=0.9)
SCENES.append(s)
sfx("tv-blip-soft.wav", 0.0, 0.18)
sfx("whoosh-short.mp3", T_CTRY, 0.16)
sfx("impact-bass-1.mp3", q2[2][1], 0.2)
sfx("whoosh-short.mp3", T_WB, 0.13)
sfx("key-press.mp3", q4[0][1], 0.22)
sfx("sparkle.mp3", T_IMF, 0.1)
sfx("key-press.mp3", q4[1][1], 0.22)
sfx("whoosh.mp3", T_GOV, 0.15)
sfx("riser.mp3", T_TWO - 3 * F1, 0.1)
sfx("impact-bass-2.mp3", T_BIG, 0.4)
sfx("impact-bass-1.mp3", T_BIG, 0.28)
quote([q1[:5], q1[5:]], T_CTRY, x=150, y=520, size=46)
lock([Wr(q2[:2], 56), Wr(q2[2:], 200, 800)], T_WB)
lock([Wr(q3[:3], 56), Wr(q3[3:], 170, 800)], T_IMF)
bars(q4, T_GOV, size=120)
lock([Wr(q5[:3], 52), Wr(q5[3:5], 96, 800), Wr(q5[5:], 96, 800)], T_TWO - 3 * F1, x=1120, y=520, align="left")
lock([Wr(q6[:4], 56), Wr(q6[4:], 330, 800)], SB_END, x=150, y=540, align="left")

# ---- S02 "This is the most influential man in America right now. He's basically the CEO of Wall Street." ---------
h1 = VO.take("This is the most influential")
h2 = VO.take("man in America")
h3 = VO.take("right now")
h4 = VO.take("He's basically")
h5 = VO.take("the CEO of Wall Street")
T_MAN, T_NOW, T_HES, T_CEO = h2[0][1], h3[0][1], h4[0][1], h5[0][1]
s = Scene("s02", SB_END, VO.items[VO.k][1] + OFF - LEAD)
T0 = SB_END
# Dimon with the same presidential seal composited behind him (the reference's "This man is")
comp = s.uid("comp")
bgi, sli, cti = s.uid("i"), s.uid("i"), s.uid("i")
s.raw(f'<div class="cam" id="{comp}" style="left:0;top:0;width:1920px;height:1080px;z-index:{s.nz()}">'
      f'<img id="{bgi}" class="clip" src="assets/img/dimon_gesture.jpg" alt="" {s.timed(T0, T_NOW)} data-color-grading="{esc(GR["doc_warm"])}" '
      f'data-track-index="3" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />'
      f'<img id="{sli}" class="clip" src="assets/img/seal.png" alt="" {s.timed(T0, T_NOW)} data-track-index="3" '
      f'style="position:absolute;left:420px;top:150px;width:860px;height:860px" />'
      f'<img id="{cti}" class="clip" src="assets/img/dimon_gesture-cut.png" alt="" {s.timed(T0, T_NOW)} data-color-grading="{esc(GR["doc_warm"])}" '
      f'data-track-index="3" data-layout-allow-occlusion style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" /></div>')
s.js.append(f'tl.fromTo("#{comp}", {{ scale: 1.0, x: 0, y: 0 }}, {{ scale: 1.03, duration: {r3(T_MAN - T0)}, ease: "none" }}, 0);')
s.ramp_push(comp, T_MAN, T_NOW, s0=1.03, s1=1.47, x1=-310, y1=245, fast=4, share=0.88)
s.neg(T0, 2)
s.neg(T0 + 3 * F1, 1)
s.video("c_dimon_window.mp4", T_NOW, T_HES, push=(1.0, 1.04))
s.neg(T_NOW, 1)
camWS, _ = s.video("c_wallst_sign.mp4", T_HES, T_CEO, push=None)
s.ramp_into(camWS, T_HES, T_CEO, s1=1.45)
T_OF = h5[2][1]
camNJ, _ = s.video("c_nyse_jpm.mp4", T_CEO, T_OF, push=None)
s.ramp_land(camNJ, T_CEO, T_OF, s0=1.55)
s.video("c_nyse_flag.mp4", T_OF, s.end, push=(1.0, 1.05))
SCENES.append(s)
sfx("glitch-3.mp3", T0, 0.12)
sfx("impact-bass-1.mp3", h1[4][1], 0.22)
sfx("whoosh-short.mp3", T_MAN, 0.18)
sfx("whoosh-short.mp3", T_NOW, 0.1)
sfx("whoosh-short.mp3", T_HES, 0.1)
sfx("whoosh-short.mp3", T_CEO, 0.12)
sfx("impact-bass-1.mp3", h5[1][1], 0.2)
sfx("whoosh-short.mp3", T_OF, 0.1)
lock([Wr(h1[:1], 64), Wr(h1[1:4], 64), Wr(h1[4:], 150, 800)], T_MAN, x=130, y=330, align="left")
line(h2, T_NOW)
line(h3, T_HES)
line(h4, T_CEO)
lock([Wr(h5[:1], 56), Wr(h5[1:2], 210, 800), Wr(h5[2:], 56)], s.end)

# ---- S03 "A guy who got fired in 1998 by his own mentor over a bonus and a family grudge." ----------------------
f1 = VO.take("A guy who got")
f2 = VO.take("fired")
f3 = VO.take("in 1998")
f4 = VO.take("by his own mentor")
f5 = VO.take("over a bonus")
f6 = VO.take("and a family grudge")
s = Scene("s03", f1[0][1], VO.items[VO.k][1] + OFF - LEAD)
camYD, _ = s.video("c_young_dimon.mp4", f1[0][1], f2[0][1], push=None)
s.ramp_into(camYD, f1[0][1], f2[0][1], s1=1.38, fast=0.15)
s.video("c_young_dimon.mp4", f2[0][1], f3[0][1], ms=0.7, grade="glitch2", push=(1.12, 1.16), fit=False)
s.neg(f2[0][1], 2)
s.video("c_citigroup98.mp4", f3[0][1], f4[0][1], push=(1.0, 1.05))
s.video("c_weill_old.mp4", f4[0][1], f4[3][1], push=(1.0, 1.04))
s.video("c_dimon_weill_bw.mp4", f4[3][1], f5[0][1], grade="doc_bw", push=(1.04, 1.0))
camCS, _ = s.video("c_cash.mp4", f5[0][1], f6[0][1], push=None)
s.ramp_push(camCS, f5[2][1], f6[0][1], s0=1.0, s1=1.2, fast=4)
s.fx_frames("c_cash.mp4", f5[0][1], 1, "half")
s.video("c_jessica.mp4", f6[0][1], f6[2][1], push=(1.0, 1.04))
s.video("c_weill_daughter.mp4", f6[2][1], s.end, push=(1.0, 1.06))
SCENES.append(s)
sfx("whoosh-short.mp3", f1[0][1], 0.1)
sfx("glitch-1.mp3", f2[0][1], 0.16)
sfx("impact-bass-1.mp3", f2[0][1], 0.26)
sfx("whoosh-short.mp3", f3[0][1], 0.12)
sfx("impact-bass-1.mp3", f3[1][1], 0.15)
sfx("whoosh-short.mp3", f4[0][1], 0.1)
sfx("whoosh-short.mp3", f4[3][1], 0.1)
sfx("whoosh-short.mp3", f5[0][1], 0.1)
sfx("whoosh-short.mp3", f6[0][1], 0.1)
sfx("impact-bass-1.mp3", f6[3][1], 0.16)
line(f1, f2[0][1])
lock([Wr(f2, 230, 800)], f3[0][1])
lock([Wr(f3[:1], 56), Wr(f3[1:], 230, 800)], f4[0][1])
line(f4, f5[0][1])
lock([Wr(f5[:2], 56), Wr(f5[2:], 200, 800)], f6[0][1])
lock([Wr(f6[:3], 56), Wr(f6[3:], 210, 800)], s.end)

# ---- S04 "Now runs a bank that lends to countries, World Bank, and even the US government." ----------------------
n1 = VO.take("Now runs a bank")
n2 = VO.take("that lends to countries")
n3 = VO.take("World Bank")
n4 = VO.take("and even the")
n5 = VO.take("US government")
s = Scene("s04", n1[0][1], VO.items[VO.k][1] + OFF - LEAD)
camJG, _ = s.video("c_jpm_gold.mp4", n1[0][1], n2[0][1], push=None)
s.ramp_land(camJG, n1[0][1], n2[0][1], s0=1.4)
s.neg(n1[0][1], 2)
s.grid2([("lead_reeves1.jpg", n2[0][1]), ("lead_japan1.jpg", n2[1][1]), ("lead_macri.jpg", n2[2][1]),
         ("lead_japan3.jpg", n2[3][1])], n3[0][1])
s.image("wb_3.jpg", n3[0][1], n4[0][1], push=(1.0, 1.06))
s.image("gov_capitol.jpg", n4[0][1], n5[0][1], push=(1.0, 1.05))
s.video("c_dc_aerial.mp4", n5[0][1], s.end, push=(1.0, 1.06))
s.neg(s.end - 4 * F1, 2)
SCENES.append(s)
sfx("whoosh-short.mp3", n1[0][1], 0.12)
for _, t in n2:
    sfx("pop.mp3", t, 0.1)
sfx("whoosh-short.mp3", n3[0][1], 0.1)
sfx("whoosh-short.mp3", n4[0][1], 0.1)
sfx("whoosh.mp3", n5[0][1], 0.14)
line(n1, n2[0][1])
line(n2, n3[0][1])
line(n3, n4[0][1])
lock([Wr(n4, 56), Wr(n5, 124, 800)], s.end)

# ---- S05 "Meet Jamie Dimon, the golden boy of Wall Street." ------------------------------------------------------
m1 = VO.take("Meet Jamie Dimon")
m2 = VO.take("the golden boy")
m3 = VO.take("of Wall Street")
s = Scene("s05", m1[0][1] - 2 * F1, VO.items[VO.k][1] + OFF - LEAD, ground="#F3F2EE")
s.uses_text = True
T_MEET, T_GB = m1[0][1], m2[0][1]
# the name card on white (the reference's red card, here in JPMorgan Chase blue with Chase octagons)
CARD = (560, 250, 800, 500)
x, y, w, h = CARD
card = s.uid("card")
octs = []
rnd = random.Random(21)
for k in range(9):
    sz = rnd.choice([110, 140, 170, 210, 250])
    ox, oy = rnd.randint(-60, w - 60), rnd.randint(-60, h - 60)
    octs.append(f'<svg class="oct" viewBox="0 0 56 56" style="left:{ox}px;top:{oy}px;width:{sz}px;height:{sz}px;'
                f'transform:rotate({rnd.randint(-30, 30)}deg);opacity:{rnd.uniform(0.18, 0.42):.2f}"><use href="#chase-oct"/></svg>')
cardbg = s.uid("cardbg")
s.raw(f'<svg width="0" height="0" style="position:absolute"><defs><g id="chase-oct">'
      f'<path d="M19,0 L37,0 L56,19 L56,37 L37,56 L19,56 L0,37 L0,19 Z M19,19 L19,37 L37,37 L37,19 Z" fill="#ffffff" fill-rule="evenodd"/>'
      f'</g></defs></svg>')
s.raw(f'<div class="cam card" id="{card}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{s.nz() + 20}">'
      f'<div id="{cardbg}" class="clip" {s.timed(T_MEET, T_GB)} data-track-index="3" '
      f'style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;background:linear-gradient(140deg,#0B4EA2 0%,#1468C8 55%,#0A3F86 100%)">'
      f'{"".join(octs)}'
      f'<img class="cutimg" src="assets/img/dimon_card-cut.png" alt="" style="position:absolute;left:{(w - 410) // 2}px;bottom:0;height:{h - 18}px" />'
      f'</div></div>')
s.js.append(f'tl.fromTo("#{card}", {{ scale: 1.75, y: -40 }}, {{ scale: 1.0, y: 0, duration: 0.36, ease: "power3.out" }}, {s.at(T_MEET)});')
s.js.append(f'tl.to("#{card}", {{ scale: 0.97, duration: {r3(T_GB - T_MEET - 0.36)}, ease: "none" }}, {s.at(T_MEET + 0.36)});')
# "Meet" above the card's top-left; the name decodes under it, over a giant pale echo of itself
meet = s.uid("tx")
s.raw(f'<div id="{meet}" class="clip tx" {s.timed(T_MEET, T_GB)} data-track-index="6" '
      f'style="left:{x}px;top:{y - 58}px;font-size:44px;font-weight:700;color:#111;z-index:{s.nz() + 20}">Meet</div>')
echo = s.uid("echo")
s.raw(f'<div id="{echo}" class="clip tx" {s.timed(m1[1][1], T_GB)} data-track-index="4" '
      f'style="left:0;top:395px;width:1920px;text-align:center;font-size:300px;font-weight:800;letter-spacing:-0.04em;'
      f'color:rgba(0,0,0,0);-webkit-text-stroke:2px rgba(20,20,20,0.10);z-index:{s.nz()}">Jamie Dimon</div>')
s.js.append(f'tl.fromTo("#{echo}", {{ scale: 1.06 }}, {{ scale: 1.0, duration: 0.7, ease: "power2.out" }}, {s.at(m1[1][1])});')
name = s.uid("name")
letters = []
rnd = random.Random(7)
for wi, (word, tw) in enumerate(m1[1:]):
    order = list(range(len(word)))
    rnd.shuffle(order)
    for ci, ch in enumerate(word):
        lid = f"{name}l{wi}{ci}"
        letters.append(f'<span id="{lid}" style="opacity:0;color:#d9d9d9">{esc(ch)}</span>')
        tt = tw + order.index(ci) * F1
        s.js.append(f'tl.set("#{lid}", {{ opacity: 1 }}, {s.at(tt)});')
        s.js.append(f'tl.set("#{lid}", {{ color: "#8f8f8f" }}, {s.at(tt + 2 * F1)});')
        s.js.append(f'tl.set("#{lid}", {{ color: "#111111" }}, {s.at(tt + 4 * F1)});')
    if wi == 0:
        letters.append('<span>&nbsp;</span>')
s.raw(f'<div id="{name}" class="clip tx" {s.timed(m1[1][1], T_GB)} data-track-index="6" '
      f'style="left:{x}px;top:{y + h + 26}px;width:{w}px;text-align:right;font-size:74px;font-weight:800;letter-spacing:-0.03em;'
      f'z-index:{s.nz() + 20}">{"".join(letters)}</div>')
camG, vG = s.video("c_young_window.mp4", T_GB, m3[0][1], grade="gold", push=None, z=s.nz() + 40)
s.ramp_into(camG, T_GB, m3[0][1], s1=1.4)
s.godrays(T_GB, m3[0][1], cx=1420, cy=80, rgb="255,196,96", opacity=0.42)
camW, vW = s.video("c_wolf_mic.mp4", m3[0][1], s.end, grade="doc", push=(1.0, 1.03), z=s.nz() + 40)
s.faceboxes(m3[0][1], s.end, [(560, 40, 470, 560, "#B23CFF", "person"), (1400, 300, 360, 520, "#B23CFF", "person"),
                              (650, 640, 170, 300, "#2DE38A", "tie")])
SCENES.append(s)
sfx("tv-blip-soft.wav", s.start, 0.16)
sfx("sparkle.mp3", m1[1][1], 0.12)
sfx("whoosh-short.mp3", T_GB, 0.12)
sfx("tv-blip-soft.wav", m3[0][1], 0.13)
lock([Wr(m2[:1], 56), Wr(m2[1:], 180, 800)], m3[0][1])
line(m3, s.end)

# ---- S06 "The guy everyone said was next in line to run the biggest financial company in the world." -----------
e1 = VO.take("the guy everyone said")
e2 = VO.take("was next in line")
e3 = VO.take("to run the biggest")
e4 = VO.take("financial company")
e5 = VO.take("in the world")
s = Scene("s06", e1[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.video("c_cameras.mp4", e1[0][1], e2[2][1] + 0.26, push=(1.0, 1.05))
s.neg(e1[0][1], 1)
# "was next in line": three panels slide in one after another (the reference's split panels)
s.split3([("c_heir.mp4", e2[0][1], 0.0, "doc"), ("c_weill_dimon_pair.mp4", e2[1][1], 1.0, "doc"),
          ("c_dimon_weill_bw.mp4", e2[2][1], 0.0, "doc_bw")], e3[0][1])
camCI, _ = s.video("c_citi_sign.mp4", e3[0][1], e4[0][1], push=None)
s.ramp_into(camCI, e3[0][1], e4[0][1], s1=1.45)
camCC, _ = s.video("c_citi_crowd.mp4", e4[0][1], e5[0][1], push=None)
s.ramp_land(camCC, e4[0][1], e5[0][1], s0=1.5)
s.video("c_citi_aerial.mp4", e5[0][1], s.end, push=(1.0, 1.05))
SCENES.append(s)
for t in (e1[0][1], e3[0][1], e5[0][1]):
    sfx("whoosh-short.mp3", t, 0.1)
for _, t in e2[:3]:
    sfx("whoosh-short.mp3", t, 0.09)
sfx("whoosh.mp3", e4[0][1] - 0.12, 0.16)
sfx("impact-bass-1.mp3", e3[3][1], 0.16)
line(e1, e2[0][1])
line(e2, e3[0][1])
lock([Wr(e3[:3], 56), Wr(e3[3:], 200, 800), Wr(e4, 56)], e5[0][1])
line(e5, s.end)

# ---- S07 "He built Citigroup side by side with his mentor Sandy Weill for 16 years." ----------------------------
b1 = VO.take("He built Citigroup")
b2 = VO.take("side by side with his mentor")
b3 = VO.take("Sandy Weill")
b4 = VO.take("for 16 years")
s = Scene("s07", b1[0][1], VO.items[VO.k][1] + OFF - LEAD)
camCT, _ = s.image("citi_center.jpg", b1[0][1], b2[0][1], push=None)
s.ramp_push(camCT, b1[0][1], b2[0][1], s0=1.0, s1=1.14, fast=5)
s.neg(b1[0][1], 2)
# "side by side": the pair photo arrives as two halves sliding in from either side
for side, (clip, dx) in enumerate((("inset(0 50% 0 0)", -960), ("inset(0 0 0 50%)", 960))):
    camS, vS = s.video("c_weill_dimon_pair.mp4", b2[0][1] + side * F1, b3[0][1], ms=0.04 * side, push=None, cam_extra=f"clip-path:{clip};")
    s.js.append(f'tl.fromTo("#{camS}", {{ x: {dx}, scale: 1.0 }}, {{ x: 0, scale: 1.04, duration: 0.34, ease: "power3.out" }}, {s.at(b2[0][1] + side * F1)});')
s.video("c_weill_laugh.mp4", b3[0][1], b4[0][1], push=(1.0, 1.05))
s.video("c_citi_red.mp4", b4[0][1], s.end, push=(1.0, 1.05))
SCENES.append(s)
sfx("whoosh-short.mp3", b1[0][1], 0.1)
sfx("impact-bass-1.mp3", b1[2][1], 0.16)
sfx("whoosh.mp3", b2[0][1], 0.18)
sfx("whoosh-short.mp3", b3[0][1], 0.1)
sfx("whoosh-short.mp3", b4[0][1], 0.1)
sfx("typing.mp3", b4[1][1], 0.14)
lock([Wr(b1[:2], 56), Wr(b1[2:], 190, 800)], b2[0][1])
line(b2, b3[0][1])
line(b3, b4[0][1])
lock([Wr(b4[:1], 56), COUNT(1, 16, b4[1][1], round(b4[1][1] + 0.3, 3), 240), Wr(b4[2:], 64)], s.end)

# ---- S08 "But then, at 42, he was fired. 18 months of no job." --------------------------------------------------
x1 = VO.take("But then")
x2 = VO.take("at 42")
x3 = VO.take("he was")
x4 = VO.take("fired")
x5 = VO.take("18 months")
x6 = VO.take("of no job")
s = Scene("s08", x1[0][1] - 3 * F1, VO.items[VO.k][1] + OFF - LEAD)
T_F = x4[0][1]
s.flash(s.start, 1, "#8a8a8a")
s.flash(T_F - F1, 1, "#ffffff")
# the user's "fired" shot: the push that knocks the soul out, letterboxed; it then shrinks to a window
camX, vX = s.video("r_strange.mp4", T_F, x5[0][1], grade="doc", push=None, box=(0, 138, 1920, 804))
s.js.append(f'tl.set("#{camX}", {{ scale: 1.0 }}, {s.at(T_F)});')
s.js.append(f'tl.to("#{camX}", {{ scale: 0.6, duration: 0.42, ease: "power3.out" }}, {s.at(T_F + 0.46)});')
s.neg(T_F, 2)
# "18 months": a desk calendar flips a page a month, December 1998 to May 2000 (the reference's flip-calendar)
MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
CAL_STEP = 1.45
s.uses_text = True
s.flipcal(x5[0][1], x6[0][1], [(MON[(11 + k) % 12], str(1998 + (11 + k) // 12)) for k in range(18)], step=CAL_STEP)
s.video("c_hallway.mp4", x6[0][1], s.end, grade="doc_warm", push=(1.0, 1.05))
s.neg(x6[1][1], int(round((s.end - x6[1][1]) / F1)))
SCENES.append(s)
for _, t in x1 + x2 + x3:
    sfx("key-press.mp3", t, 0.2)
sfx("whoosh.mp3", T_F - 0.03, 0.2)
sfx("impact-bass-2.mp3", T_F, 0.42)
sfx("impact-bass-1.mp3", T_F, 0.28)
for k in range(0, 18, 3):
    sfx("click-soft.mp3", round(x5[0][1] + round(k * CAL_STEP) * F1, 3), 0.07)
sfx("whoosh-short.mp3", x6[0][1], 0.1)
bars(x1, x2[0][1] - F1, size=78)
bars(x2, x3[0][1] - F1, size=78)
bars(x3, T_F, size=78)
lock([Wr(x4, 230, 800)], x5[0][1])
lock([COUNT(1, 18, x5[0][1], round(x5[0][1] + 17 * CAL_STEP * F1, 3), 260), Wr(x5[1:], 64), Wr(x6, 56)], s.end, x=300, y=540,
     align="left")

# ---- S09 "He took up boxing, read biographies, even met Bezos for a job at Amazon." -----------------------------
w1 = VO.take("He took up")
w2 = VO.take("boxing")
w3 = VO.take("read biographies")
w4 = VO.take("even met Bezos")
w5 = VO.take("for a job at Amazon")
s = Scene("s09", w1[0][1], VO.items[VO.k][1] + OFF - LEAD)
# the wilderness year, as the documentary shows it: alone at home under a lamp
camAL, _ = s.video("c_alone.mp4", w1[0][1], w2[0][1], grade="doc_warm", push=None)
s.ramp_into(camAL, w1[0][1], w2[0][1], s1=1.32, fast=0.14)
# "boxing": the doc's 1998 photo of Dimon with both fists up, in the reference's six-look style strobe
s.style_strobe("dimon_fists.jpg", w2[0][1], w3[0][1], frames=2)
s.video("c_books.mp4", w3[0][1], w4[0][1], push=(1.0, 1.06))
s.video("c_bezos.mp4", w4[0][1], w5[0][1], push=(1.0, 1.05))
s.image("bezos_laugh.jpg", w5[0][1], s.end, push=(1.0, 1.06), pos="50% 30%")
s.fx_frames("bezos_laugh.jpg", w5[0][1], 2, "half", image=True)
SCENES.append(s)
sfx("whoosh-short.mp3", w1[0][1], 0.1)
sfx("impact-bass-1.mp3", w2[0][1], 0.32)
sfx("glitch-3.mp3", w2[0][1], 0.1)
sfx("whoosh-short.mp3", w3[0][1], 0.1)
sfx("whoosh-short.mp3", w4[0][1], 0.1)
sfx("tv-blip-soft.wav", w5[0][1], 0.14)
line(w1, w2[0][1])
lock([Wr(w2, 170, 800)], w3[0][1], x=1250, y=560, align="left", tone="dk")
line(w3, w4[0][1])
lock([Wr(w4[:2], 56), Wr(w4[2:], 200, 800)], w5[0][1])
lock([Wr(w5[:4], 56), Wr(w5[4:], 200, 800)], s.end)

# ---- S10 "But it was all a premise for the greatest comeback in the history of Wall Street." ---------------------
c1 = VO.take("But it was all a premise for")
c2 = VO.take("the greatest")
c3 = VO.take("comeback")
c4 = VO.take("in the history of Wall Street")
s = Scene("s10", c1[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.uses_text = True
T_CB = c3[0][1]
camDD, _ = s.video("c_dimon_dark.mp4", c1[0][1], c2[0][1], grade="doc_warm", push=None)
s.js.append(f'tl.fromTo("#{camDD}", {{ scale: 1.0 }}, {{ scale: 1.035, duration: {r3(c1[6][1] - c1[0][1])}, ease: "none" }}, {s.at(c1[0][1])});')
s.js.append(f'tl.to("#{camDD}", {{ scale: 1.3, duration: {r3(3 * F1)}, ease: "power3.out" }}, {s.at(c1[6][1])});')
s.js.append(f'tl.to("#{camDD}", {{ scale: 1.36, duration: {r3(c2[0][1] - c1[6][1] - 3 * F1)}, ease: "sine.out" }}, {s.at(c1[6][1] + 3 * F1)});')
s.fx_frames("c_dimon_dark.mp4", c1[5][1], 3, "glitch2", ms=round(c1[5][1] - c1[0][1], 3))
s.neg(c2[0][1] - 3 * F1, 2)
s.flash(c2[0][1] - F1, 1, "#ffffff")
# typed "the greatest" on black (captions), then grey, grey, white -- and the type plane turns into the white card
s.flash(T_CB - 3 * F1, 1, "#8a8a8a")
s.flash(T_CB - 2 * F1, 1, "#9b9b9b")
s.flash(T_CB - F1, 1, "#ffffff")
plane = s.uid("plane")
s.raw(f'<div class="cam" id="{plane}" style="left:0;top:0;width:1920px;height:1080px;z-index:{s.nz()};perspective:1600px">'
      f'<div id="{plane}-in" class="clip" {s.timed(T_CB, c4[4][1])} data-track-index="4" '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px">'
      f'<div class="tx" style="left:330px;top:830px;font-size:120px;font-weight:800;letter-spacing:-0.04em;color:#F6F3EE;'
      f'transform:rotate(-90deg);transform-origin:0 0;text-shadow:{GLOW_TYPED}">the greatest</div>'
      f'<div class="wcard" style="left:430px;top:390px;width:1260px;height:300px"></div>'
      f'<div class="tx" style="left:430px;top:390px;width:1260px;height:300px;display:flex;align-items:center;justify-content:center;'
      f'font-size:270px;font-weight:800;color:#101010;letter-spacing:-0.06em"><span style="display:inline-block;transform:scaleX(0.8)">comeback</span></div>'
      f'</div></div>')
s.js.append(f'tl.fromTo("#{plane}", {{ rotation: -22, rotationY: -34, scale: 1.45 }}, {{ rotation: -8, rotationY: -12, scale: 1.0, '
            f'duration: 0.42, ease: "expo.out" }}, {s.at(T_CB)});')
s.js.append(f'tl.to("#{plane}", {{ rotation: -5, rotationY: -6, scale: 1.05, duration: {r3(c4[4][1] - T_CB - 0.42)}, '
            f'ease: "sine.inOut" }}, {s.at(T_CB + 0.42)});')
s.hud(T_CB, T_CB + 0.9, seed=31, opacity=0.7)
s.neg(c4[4][1], 2)
s.video("c_old_wallst.mp4", c4[4][1], s.end, grade="doc_bw", push=(1.0, 1.05))
SCENES.append(s)
sfx("whoosh-short.mp3", c1[0][1], 0.1)
sfx("glitch-1.mp3", c1[5][1], 0.12)
sfx("impact-bass-1.mp3", c1[6][1], 0.16)
sfx("typing.mp3", c2[0][1], 0.18)
sfx("whoosh-cinematic.mp3", T_CB, 0.2)
sfx("impact-bass-2.mp3", T_CB, 0.3)
sfx("whoosh-short.mp3", c4[4][1], 0.12)
line(c1, c2[0][1])
typed(c2, T_CB - 3 * F1, y=560, size=300, mode="follow")
line(c4[:4], c4[4][1], y=905)
line(c4[4:], s.end)

# ---- S11 "In 2000 he takes over a broken bank in Chicago, cuts the dividend, cleaned it up," ---------------------
k1 = VO.take("in=In 2000")
k2 = VO.take("he takes over")
k3 = VO.take("a broken bank")
k4 = VO.take("in Chicago")
k5 = VO.take("cuts the dividend")
k6 = VO.take("cleaned it up")
s = Scene("s11", k1[0][1] - 2 * F1, VO.items[VO.k][1] + OFF - LEAD)
s.video("c_bankone_podium.mp4", k2[0][1], k3[0][1], push=(1.0, 1.05))
s.neg(k2[0][1], 1)
s.video("c_bankone_night.mp4", k3[0][1], k4[0][1], grade="doc_warm", push=(1.0, 1.05))
s.fx_frames("c_bankone_night.mp4", k3[1][1], 2, "glitch2", ms=round(k3[1][1] - k3[0][1], 3))
s.video("c_chicago.mp4", k4[0][1], k5[0][1], push=(1.0, 1.05))
s.video("c_bankone_stage.mp4", k5[0][1], k6[0][1], push=(1.0, 1.04))
# "cleaned it up": a white panel wipes across and leaves the clean building
camC, iC = s.image("chase_tower.jpg", k6[0][1], s.end, push=(1.0, 1.05), cam_extra="clip-path:inset(0 100% 0 0);")
s.js.append(f'tl.fromTo("#{camC}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.26, ease: "power2.inOut" }}, {s.at(k6[0][1])});')
wb = s.uid("wipe")
s.raw(f'<div id="{wb}" class="clip wipebar" {s.timed(k6[0][1], k6[0][1] + 0.3)} data-track-index="6" style="left:-70px;z-index:{s.nz()}"></div>')
s.js.append(f'tl.fromTo("#{wb}", {{ x: 0 }}, {{ x: 1990, duration: 0.26, ease: "power2.inOut" }}, {s.at(k6[0][1])});')
SCENES.append(s)
sfx("typing.mp3", k1[0][1], 0.18)
sfx("impact-bass-1.mp3", k1[1][1], 0.2)
sfx("whoosh-short.mp3", k2[0][1], 0.1)
sfx("glitch-3.mp3", k3[1][1], 0.14)
sfx("whoosh-short.mp3", k4[0][1], 0.1)
sfx("whoosh-short.mp3", k5[0][1], 0.1)
sfx("whoosh.mp3", k5[2][1] + 0.3, 0.16)
sfx("whoosh.mp3", k6[0][1], 0.14)
typed([k1[1]], k2[0][1], y=600, size=700, mode="center", pre=(k1[0][0], k1[0][1], 64), cadence=3)
line(k2, k3[0][1])
lock([Wr(k3[:1], 56), Wr(k3[1:2], 200, 800), Wr(k3[2:], 56)], k4[0][1])
line(k4, k5[0][1])
lock([Wr(k5[:2], 56), CUT(k5[2], round(k5[2][1] + 0.3, 3), 190)], k6[0][1])
line(k6, s.end)

# ---- S12 "and put $60 million of his own money into the stock," -------------------------------------------------
y1 = VO.take("and put")
y2 = VO.take("$60 million")
y3 = VO.take("of his own money")
y4 = VO.take("into the stock")
s = Scene("s12", y1[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.video("r_cash2.mp4", y1[0][1], y3[0][1], push=(1.0, 1.04))
s.neg(y1[0][1], 2)
s.video("c_dimon_2000s.mp4", y3[0][1], y4[0][1], push=(1.0, 1.04))
camTF, _ = s.video("r_trading_floor.mp4", y4[0][1], s.end, push=None)
s.ramp_into(camTF, y4[0][1], s.end, s1=1.3, fast=0.16)
s.fx_frames("r_trading_floor.mp4", y4[0][1], 1, "half")
SCENES.append(s)
sfx("whoosh-short.mp3", y1[0][1], 0.1)
sfx("impact-bass-1.mp3", y2[1][1], 0.18)
sfx("whoosh-short.mp3", y3[0][1], 0.1)
sfx("whoosh-short.mp3", y4[0][1], 0.1)
lock([Wr(y1, 56), SWAP([("$60", y2[0][1]), ("$60,000", y2[1][1]), ("$60,000,000", round(y2[1][1] + 4 * F1, 3))], 200)], y3[0][1], x=170, y=540, align="left")
line(y3, y4[0][1])
line(y4, s.end)

# ---- S13 "turned a $500 million loss into billions in profit." --------------------------------------------------
z1 = VO.take("turned a")
z2 = VO.take("$500 million")
z3 = VO.take("loss")
z4 = VO.take("into billions in profit")
s = Scene("s13", z1[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.video("r_ticker_led.mp4", z1[0][1], z3[0][1], grade="tv", push=(1.0, 1.04))
# "loss into billions": the reference's line chart, drawing itself with a moving cursor (red fall, white climb)
s.neg(z3[0][1], 2)
s.linechart(z3[0][1], z4[2][1], [(z3[0][1], 0.66), (z4[0][1], 0.1), (z4[1][1], 0.2), (round(z4[2][1] - 0.05, 3), 0.95)])
camWM, _ = s.video("r_wolf_money.mp4", z4[2][1], s.end, ms=0.75, push=None)
s.ramp_land(camWM, z4[2][1], s.end, s0=1.3, fast=0.26)
SCENES.append(s)
sfx("tv-blip-soft.wav", z1[0][1], 0.15)
sfx("impact-bass-1.mp3", z2[1][1], 0.2)
sfx("glitch-3.mp3", z3[0][1], 0.12)
sfx("whoosh.mp3", z4[0][1], 0.14)
sfx("impact-bass-1.mp3", z4[1][1], 0.18)
sfx("whoosh-short.mp3", z4[2][1], 0.12)
lock([Wr(z1, 56), SWAP([("$500", z2[0][1]), ("$500,000", z2[1][1]), ("$500,000,000", round(z2[1][1] + 4 * F1, 3))], 200)], z3[0][1],
     x=170, y=540, align="left")
line(z3, z4[0][1], y=920)
lock([Wr(z4[:1], 56), Wr(z4[1:2], 118, 800)], z4[2][1], y=880)
lock([Wr(z4[2:3], 56), Wr(z4[3:], 200, 800)], s.end)

# ---- S14 "That bank got acquired by JP Morgan in 2004." --------------------------------------------------------
a1 = VO.take("That bank got acquired")
a2 = VO.take("by JP=JPMorgan Morgan=")
a3 = VO.take("in 2004")
s = Scene("s14", a1[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.video("c_jpm_buys.mp4", a1[0][1], a1[3][1], grade="tv", push=(1.0, 1.04))
s.neg(a1[0][1], 2)
camHP, _ = s.video("c_harrison_presser.mp4", a1[3][1], a2[0][1], grade="tv", push=None)
s.ramp_into(camHP, a1[3][1], a2[0][1], s1=1.42)
camJS, _ = s.video("c_jpmco_sign.mp4", a2[0][1], a3[0][1], push=None)
s.ramp_land(camJS, a2[0][1], a3[0][1], s0=1.5)
s.video("c_harrison_backdrop.mp4", a3[0][1], s.end, push=(1.0, 1.05))
SCENES.append(s)
sfx("tv-blip-soft.wav", a1[0][1], 0.15)
sfx("whoosh-short.mp3", a1[3][1], 0.1)
sfx("whoosh-short.mp3", a2[0][1], 0.1)
sfx("impact-bass-1.mp3", a2[1][1], 0.18)
sfx("whoosh-short.mp3", a3[0][1], 0.1)
sfx("impact-bass-1.mp3", a3[1][1], 0.16)
line(a1, a2[0][1])
lock([Wr(a2[:1], 56), Wr(a2[1:], 200, 800)], a3[0][1])
lock([Wr(a3[:1], 56), Wr(a3[1:], 230, 800)], s.end)

# ---- S15 "Then 2008 financial crisis hit," -------------------------------------------------------------------
t1w = VO.take("Then")
t2w = VO.take("2008")
t3w = VO.take("financial crisis hit")
s = Scene("s15", t1w[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.video("s_stopwatch.mp4", t1w[0][1], t2w[0][1], push=(1.0, 1.06))
s.video("r_nyse_floor.mp4", t2w[0][1], t3w[0][1], push=(1.0, 1.04))
s.neg(t2w[0][1], 2)
s.video("r_plunge.mp4", t3w[0][1], s.end, grade="tv", push=(1.0, 1.05))
SCENES.append(s)
sfx("whoosh-short.mp3", t1w[0][1], 0.1)
sfx("impact-bass-2.mp3", t2w[0][1], 0.36)
sfx("tv-blip-soft.wav", t3w[0][1], 0.14)
sfx("impact-bass-1.mp3", t3w[1][1], 0.22)
line(t1w, t2w[0][1])
T8 = t2w[0][1]
lock([SWAP([("2004", T8), ("2005", round(T8 + 2 * F1, 3)), ("2006", round(T8 + 4 * F1, 3)),
            ("2007", round(T8 + 6 * F1, 3)), ("2008", round(T8 + 8 * F1, 3))], 240, chrome=True)], t3w[0][1], y=560)
lock([Wr(t3w[:1], 56), Wr(t3w[1:2], 210, 800), Wr(t3w[2:], 56)], s.end)

# ---- S16 "and when every other bank was dying, he was the only one standing" ------------------------------------
d1 = VO.take("and when every other bank was")
d2 = VO.take("dying")
d3 = VO.take("he was the only one")
d4 = VO.take("standing")
s = Scene("s16", d1[0][1], VO.items[VO.k][1] + OFF - LEAD)
# "every other bank": the reference's collage -- a card flips to a new bank every 2 frames on white, then the
# camera pulls out to the whole wall of them
COL = ["lehman_ts.jpg", "bear_door.jpg", "wamu_floor.jpg", "lehman_nyc.jpg", "bear_sign.jpg", "wamu_center.jpg", "lehman_boxes.jpg"]
s.collage(d1[0][1], d1[4][1], d2[0][1], COL)
s.video("s_bear_3d.mp4", d2[0][1], d3[0][1], push=(1.0, 1.05))
s.neg(d2[0][1], int(round((d3[0][1] - d2[0][1]) / F1)))
s.fx_frames("s_bear_3d.mp4", d2[0][1], 2, "glitch2")
s.video("c_dimon_walk.mp4", d3[0][1], d4[0][1], push=(1.0, 1.04))
camLM, _ = s.video("r_last_man.mp4", d4[0][1], s.end, push=None)
s.ramp_land(camLM, d4[0][1], s.end, s0=1.25, fast=0.22)
SCENES.append(s)
sfx("whoosh-short.mp3", d1[0][1], 0.1)
for k in range(0, int((d1[4][1] - d1[0][1]) / (2 * F1)), 2):
    sfx("click-soft.mp3", round(d1[0][1] + k * 2 * F1, 3), 0.06)
sfx("whoosh.mp3", d1[4][1] - 0.05, 0.15)
sfx("glitch-1.mp3", d2[0][1], 0.14)
sfx("impact-bass-1.mp3", d2[0][1], 0.2)
sfx("whoosh-short.mp3", d3[0][1], 0.1)
sfx("impact-bass-1.mp3", d4[0][1], 0.24)
lock([Wr(d1, 56)], d2[0][1], y=930, tone="dk")
lock([Wr(d2, 220, 800)], d3[0][1])
lock([Wr(d3, 56), Wr(d4, 200, 800)], s.end)

# ---- S17 "with enough money to buy the ones that fell." -------------------------------------------------------
v1 = VO.take("with enough money")
v2 = VO.take("to buy the ones that")
v3 = VO.take("fell")
s = Scene("s17", v1[0][1], VO.items[VO.k][1] + OFF - LEAD)
s.video("c_fortress.mp4", v1[0][1], v2[0][1], push=(1.0, 1.05))
# "to buy the ones that fell": the fallen banks on floating screens; on "fell" they drop one after another
s.screens3d(v2[0][1], v3[0][1], s.end, ["c_fire_sale.mp4", "bear_door.jpg", "wamu_floor.jpg", "bear_sign.jpg", "wamu_center.jpg"])
s.neg(v3[0][1], 2)
SCENES.append(s)
sfx("whoosh-short.mp3", v1[0][1], 0.1)
sfx("tv-blip-soft.wav", v2[0][1], 0.14)
sfx("whoosh-cinematic.mp3", v2[0][1], 0.1)
sfx("whoosh.mp3", v3[0][1], 0.18)
sfx("impact-bass-1.mp3", v3[0][1], 0.22)
line(v1, v2[0][1])
line(v2, v3[0][1])
lock([Wr(v3, 230, 800)], s.end)

# ---- S18 "That's JP Morgan and Chase, the name that moves $10 trillion every single day today." + logo sting -------
p1 = VO.take("That's JP=JPMorgan Morgan=")
p2 = VO.take("and=& Chase")
p3 = VO.take("the name that moves")
p4 = VO.take("$10 trillion dollars=")
p5 = VO.take("every single day")
p6 = VO.take("today")
VO_END = round(OFF + 75.05, 3)
T_LOGO = round(VO_END + 1.35, 3)
s = Scene("s18", p1[0][1], DUR)
s.uses_text = True
s.video("r_jpm_night.mp4", p1[0][1], p2[0][1], push=(1.0, 1.04))
s.neg(p1[0][1], 2)
s.image("park270.jpg", p2[0][1], p3[0][1], push=(1.0, 1.06), pos="50% 30%")
s.video("c_jpmco_sign2.mp4", p3[0][1], p4[0][1], push=(1.0, 1.05))
# "$10 trillion": a ring fills around Dimon while the camera pushes in (the reference's donut around the eye)
s.video("c_money_bg.mp4", p4[0][1], p5[0][1], grade=None, push=(1.0, 1.04), opacity=0.32, blend="screen")
s.ring_beat(p4[0][1], p5[0][1], "c_dimon_xcu.mp4")
camCT2, _ = s.video("r_city_top.mp4", p5[0][1], p6[0][1], push=None)
s.ramp_into(camCT2, p5[0][1], p6[0][1], s1=1.5, drift=0.05, fast=0.18)
# "today" types on black (captions); then the closing face, light streaks and the Chase octagon
T_XCU = round(VO_END + 0.1, 3)
camE, vE = s.video("r_dimon_xcu.mp4", T_XCU, DUR, grade="doc", push=(1.0, 1.06))
s.js.append(f'tl.fromTo("#{camE}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "none" }}, {s.at(T_XCU)});')
s.js.append(f'tl.to("#{camE}", {{ opacity: 0, duration: 0.7, ease: "power1.in" }}, {s.at(T_LOGO - 0.4)});')
for k, (x0, y0, rot) in enumerate(((-560, -300, 28), (1960, -300, 152), (-560, 1380, -28), (1960, 1380, -152))):
    st = s.uid("streak")
    s.raw(f'<div id="{st}" class="clip streak" {s.timed(T_LOGO - 0.62, T_LOGO + 0.04)} data-track-index="6" '
          f'style="left:{x0}px;top:{y0}px;transform-origin:100% 50%;z-index:{s.nz()}"></div>')
    s.js.append(f'tl.fromTo("#{st}", {{ x: 0, y: 0, rotation: {rot}, opacity: 0.2 }}, {{ x: {960 - x0 - 520}, y: {540 - y0}, rotation: {rot}, '
                f'opacity: 1, duration: 0.6, ease: "power2.in" }}, {s.at(T_LOGO - 0.62)});')
logo = s.uid("logo")
s.raw(f'<svg id="{logo}" class="clip" {s.timed(T_LOGO, DUR)} data-track-index="6" viewBox="0 0 56 56" '
      f'style="position:absolute;left:{960 - 70}px;top:{540 - 70}px;width:140px;height:140px;z-index:{s.nz()};'
      f'filter:drop-shadow(0 0 18px rgba(255,255,255,0.7))">'
      f'<path d="M19,0 L37,0 L56,19 L56,37 L37,56 L19,56 L0,37 L0,19 Z M19,19 L19,37 L37,37 L37,19 Z" fill="#ffffff" fill-rule="evenodd"/></svg>')
s.js.append(f'tl.fromTo("#{logo}", {{ scale: 0.7, rotation: -45, opacity: 0 }}, {{ scale: 1.0, rotation: 0, opacity: 1, duration: 0.4, '
            f'ease: "expo.out" }}, {s.at(T_LOGO)});')
s.js.append(f'tl.to("#{logo}", {{ opacity: 0, duration: 0.4, ease: "power1.in" }}, {s.at(DUR - 0.45)});')
s.flash(T_LOGO, 1, "#ffffff")
SCENES.append(s)
sfx("whoosh-short.mp3", p1[0][1], 0.12)
sfx("impact-bass-1.mp3", p1[1][1], 0.2)
sfx("whoosh-short.mp3", p2[0][1], 0.1)
sfx("whoosh-short.mp3", p3[0][1], 0.1)
sfx("impact-bass-2.mp3", p4[1][1], 0.34)
sfx("sparkle.mp3", p4[0][1], 0.1)
sfx("whoosh-short.mp3", p5[0][1], 0.1)
sfx("typing.mp3", p6[0][1], 0.18)
sfx("whoosh-cinematic.mp3", T_LOGO, 0.2)
sfx("impact-bass-1.mp3", T_LOGO, 0.3)
lock([Wr(p1[:1], 56), Wr(p1[1:], 190, 800), Wr(p2, 190, 800)], p3[0][1])
line(p3, p4[0][1])
lock([SWAP([("$10", p4[0][1]), ("$10,000,000", p4[1][1]), ("$10,000,000,000", round(p4[1][1] + 3 * F1, 3)), ("$10,000,000,000,000", round(p4[1][1] + 6 * F1, 3))], 118)], p5[0][1], x=150, y=880, align="left")
line(p5, p6[0][1])
typed(p6, T_XCU, y=560, size=330, mode="center", cadence=2)
assert VO.k == len(VO.items), f"{len(VO.items) - VO.k} voiceover words left over"

# ---------------------------------------------------------------------------------------------------------------
# overlays: the user's textures (old TV RGB screen + print halftone) at low opacity, and a light grain
# ---------------------------------------------------------------------------------------------------------------


def _overlay(cid, css, inner, jit):
    page = f"""<template>
  <style>
  #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
  {css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
    <div id="{cid}-box" class="clip" data-start="0" data-duration="{r3(DUR)}" data-track-index="1" data-layout-ignore
      style="position:absolute;left:0;top:0;width:1920px;height:1080px">{inner}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(DUR)} }}, 0);
    {chr(10).join('    ' + j for j in jit)}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    open(f"{COMP}/{cid}.html", "w").write(page)


def _jitter(el, offs, percent=False, swap=False, step=1 / 12):
    out, t, k = [], 0.0, 0
    while t < DUR:
        dx, dy = offs[k % len(offs)]
        if swap:
            dx, dy = dy, dx
        if percent:
            out.append(f'tl.set("#{el}", {{ xPercent: {dx}, yPercent: {dy} }}, {t:.3f});')
        else:
            out.append(f'tl.set("#{el}", {{ x: {dx}, y: {dy} }}, {t:.3f});')
        t = round(t + step, 3)
        k += 1
    return out


def write_textures():
    """The user's textures, each on its own layer (blend mode on the host): the old-TV RGB screen (overlay), print
    halftone dots (multiply), the print plate (soft light) and a light grain -- all at low opacity."""
    if os.path.exists(f"{COMP}/tex.html"):
        os.remove(f"{COMP}/tex.html")
    tex_css = "#root .tex { position: absolute; left: -115px; top: -65px; width: 2150px; height: 1210px; object-fit: cover; }"
    offs = [(-10, -6), (-22, 8), (6, -18), (-14, 16), (-24, 4), (12, -8), (0, 12), (-18, -14), (8, 6), (-6, 0)]
    _overlay("texrgb", tex_css, '<img id="tx-rgb" class="tex" src="assets/tex/tx_rgb.jpg" alt="" style="opacity:0.10" />', [])
    _overlay("texdots", tex_css, '<img id="tx-dots" class="tex" src="assets/tex/tx_dots.jpg" alt="" style="opacity:0.07" />',
             _jitter("tx-dots", offs))
    _overlay("texprint", tex_css, '<img id="tx-print" class="tex" src="assets/tex/tx_print.jpg" alt="" style="opacity:0.12" />',
             _jitter("tx-print", offs, swap=True))
    g = open(f"{COMP}/components/grain-overlay.html").read()
    m = re.search(r'url\("(data:image/svg\+xml[^"]+)"\)', g)
    data_url = m.group(1) if m else ""
    goffs = [(-5, -5), (-10, 5), (5, -10), (-5, 15), (-10, 5), (15, 0), (0, 10), (-15, 0), (10, 5), (0, 0)]
    _overlay("grain", f'#grain-tex {{ position: absolute; left: -50%; top: -50%; width: 200%; height: 200%; opacity: 0.07; '
                      f'background-image: url("{data_url}"); }}', '<div id="grain-tex"></div>',
             _jitter("grain-tex", goffs, percent=True))
    # the global negative: white frames on a difference layer above everything (merged so they never cancel)
    merged = []
    for a, b in sorted(NEGS):
        if merged and a <= merged[-1][1] + 1e-6:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    divs = "".join(f'<div id="nfx{k}" class="clip nfx" data-start="{r3(a)}" data-duration="{r3(round(b - a, 3))}" '
                   f'data-track-index="2" data-layout-ignore></div>' for k, (a, b) in enumerate(merged))
    _overlay("negfx", "#root .nfx { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #ffffff; }",
             divs, [])
    print("negatives:", len(merged))


def write_root():
    hosts = []
    for k, sc in enumerate(SCENES):
        hosts.append(
            f'<div id="{sc.sid}" class="clip" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" '
            f'data-start="{r3(sc.start)}" data-duration="{r3(sc.dur)}" data-track-index="1" data-track-kind="graphics" '
            f'data-width="1920" data-height="1080" style="z-index:{10 + k}"></div>')
    for cid, z, lane, mode in (("texrgb", 85, 2, "overlay"), ("texdots", 86, 2, "multiply"), ("texprint", 87, 2, "soft-light"),
                               ("grain", 90, 3, "overlay")):
        hosts.append(
            f'<div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
            f'data-start="0" data-duration="{r3(DUR)}" data-track-index="{lane}" data-track-kind="graphics" '
            f'data-width="1920" data-height="1080" style="z-index:{z};mix-blend-mode:{mode}"></div>')
    hosts.append(
        f'<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
        f'data-start="0" data-duration="{r3(DUR)}" data-track-index="4" data-track-kind="captions" '
        f'data-width="1920" data-height="1080" style="z-index:100"></div>')
    hosts.append(
        f'<div id="negfx" class="clip" data-composition-id="negfx" data-composition-src="compositions/negfx.html" '
        f'data-start="0" data-duration="{r3(DUR)}" data-track-index="5" data-track-kind="graphics" '
        f'data-width="1920" data-height="1080" style="z-index:110;mix-blend-mode:difference"></div>')
    auds = [
        f'<audio id="a-soundbite" class="clip" src="assets/audio/soundbite.wav" data-start="0" data-duration="{r3(SB_END)}" '
        f'data-media-start="0" data-volume="1" data-track-index="10"></audio>',
        f'<audio id="a-vo" class="clip" src="assets/audio/vo.wav" data-start="{r3(OFF)}" data-duration="{r3(75.1)}" '
        f'data-media-start="0" data-volume="1" data-fade-out="0.08" data-track-index="11"></audio>',
    ]
    lanes = []
    for k, (name, t, vol, dur) in enumerate(sorted(SFX, key=lambda x: x[1])):
        start = max(0.0, round(t + F1 - PEAK.get(name, 0.05), 3))
        d = dur or SFXDUR.get(name, 1.0)
        if start + d > DUR:
            d = round(DUR - start, 3)
        if d <= 0.05:
            continue
        lane = next((i for i, e in enumerate(lanes) if e <= start), None)
        if lane is None:
            lanes.append(0.0)
            lane = len(lanes) - 1
        lanes[lane] = start + d
        auds.append(f'<audio id="sfx{k:03d}" class="clip" src="assets/audio/sfx/{name}" data-start="{r3(start)}" '
                    f'data-duration="{r3(d)}" data-media-start="0" data-volume="{vol}" data-track-index="{20 + lane}"></audio>')
    page = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #050505; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; background: #050505; }}
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


if __name__ == "__main__":
    os.makedirs(COMP, exist_ok=True)
    for sc in SCENES:
        sc.write()
    build_captions()
    write_textures()
    write_root()
    print("scenes:", [(sc.sid, sc.start, sc.end) for sc in SCENES])
    print("captions:", len(CAPS), "sfx:", len(SFX), "DUR", DUR)
