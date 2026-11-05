#!/usr/bin/env python3
"""Build the Jamie Dimon / JPMorgan Chase edit as a HyperFrames project (1920x1080, 30 fps).

Audio clock (film seconds):
  0.00-9.04   news open (name_of_the_game.mp4 src 1.12-2.68 + 5.05-12.53, joined in natural pauses)
  9.30-23.40  VO 0.00-14.10
  23.60-34.85 Dimon, Bloomberg interview (we_bank.mp4 src 273.05-284.30)
  34.97-91.57 VO 18.40-75.00
Captions follow the Dimon reference reel: Satoshi + Instrument Serif Italic in warm white with a bloom, one word at
a time on its spoken onset, a horizontal motion-blur entrance (3 frames), two-tier lockups and a cascading exit.

Run:  python3 -I tools/build.py
"""
import array, json, math, os, wave

ROOT = "/home/user/claude-test-2.0"
PRJ = f"{ROOT}/jpm-dimon"
COMP = f"{PRJ}/compositions"
TX = f"{ROOT}/dimon-work/tx"
os.makedirs(COMP, exist_ok=True)
F1 = 1 / 30
LEAD = 0.05     # picture cuts land this much before the word
DUR = 93.20


def r3(x):
    return f"{round(float(x), 3):.3f}"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# ------------------------------------------------------------------------------------------------
# Word clocks (Parakeet word times, onsets snapped to the energy envelope after pauses)
# ------------------------------------------------------------------------------------------------
def envelope(path, hop=0.01):
    w = wave.open(path)
    sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
    a = array.array("h", w.readframes(n))
    if ch > 1:
        a = a[::ch]
    step = int(sr * hop)
    out = []
    for i in range(0, len(a) - step, step):
        s = a[i:i + step]
        out.append(20 * math.log10(math.sqrt(sum(x * x for x in s) / step) / 32768 + 1e-9))
    return out


def snap(words, env, quiet, loud, hop=0.01):
    """A word that follows >= 80 ms of quiet starts at the first loud frame after that quiet stretch."""
    for w in words:
        s = w["start"]
        lo = int(max(0.0, s - 0.35) / hop)
        hi = min(len(env) - 1, int((s + 0.32) / hop))
        q, i = None, lo
        while i < hi:
            if env[i] < quiet:
                j = i
                while j < hi and env[j] < quiet:
                    j += 1
                if j - i >= 8:
                    q = j
                i = j
            else:
                i += 1
        if q is None:
            continue
        for i in range(q, hi):
            if env[i] > loud:
                w["start"] = round(max(0.0, i * hop - 0.015), 3)
                break
    for a, b in zip(words, words[1:]):
        if b["start"] < a["start"]:
            b["start"] = a["start"]
    return words


def load(path):
    j = json.load(open(path))
    return [dict(text=w["text"], start=float(w["start"]), end=float(w["end"])) for w in j]


NEWS = snap(load(f"{TX}/pk_game/transcript.json"), envelope(f"{TX}/game_open.wav"), -44, -32)
QUOTE = load(f"{TX}/pk_bank/transcript.json")
QUOTE.insert(25, dict(text="You", start=8.62, end=8.76))   # Parakeet dropped "You" before "have to be big"
QUOTE = snap(QUOTE, envelope(f"{TX}/bank_quote.wav"), -50, -34)
VOW = snap(load(f"{TX}/pk_vo/transcript.json"), envelope(f"{ROOT}/dimon-work/vo/vo16k.wav"), -55, -35)

VO1_AT, VO1_IN, VO1_OUT = 9.05, 0.00, 14.10
VO2_IN, VO2_OUT = 18.40, 75.00
VO2_OFF = round(35.25 - VOW[55]["start"], 3)   # "Meet" lands at 35.25
QUOTE_AT, QUOTE_SRC0 = 23.60, 273.05           # the Dimon clip starts here (film) / there (source)
QUOTE_OFF = round(QUOTE_AT - (QUOTE_SRC0 - 272.5), 3)  # quote.wav time -> film time
NEWS_J1, NEWS_J2, NEWS_END = (1.12, 2.68), (5.05, 12.30), None


def NT(i):  # news word -> film time
    s = NEWS[i]["start"]
    return round(s - 1.12, 3) if s < 3.0 else round(s - 3.49, 3)


def VT(i):  # VO word -> film time
    s = VOW[i]["start"]
    return round(s + VO1_AT - VO1_IN, 3) if s < 14.2 else round(s + VO2_OFF, 3)


def QT(i):  # Dimon quote word -> film time
    return round(QUOTE[i]["start"] + QUOTE_OFF, 3)


# ------------------------------------------------------------------------------------------------
# Gradings (data-color-grading payloads, built on the validated schema of the Pattinson "matte" grade)
# ------------------------------------------------------------------------------------------------
BASE = json.load(open(f"{PRJ}/tools/base_grade.json"))  # a neutral, validated data-color-grading payload


def grade(adjust=None, details=None, effects=None, intensity=1, preset=None):
    g = json.loads(json.dumps(BASE))
    g["preset"], g["intensity"] = preset, intensity
    for sec, vals in (("adjust", adjust), ("details", details), ("effects", effects)):
        for k, v in (vals or {}).items():
            g[sec][k] = v
    return g


DOC_ADJ = dict(contrast=0.08, highlights=-0.14, shadows=0.02, blacks=0.05, saturation=-0.12, temperature=0.05)
DOC_FX = dict(scanlines=0.10, scanlineCount=0.17, scanlineSoftness=1, chromaticAberration=0.035, chromaticAngle=0)
GR = {
    "doc": grade(DOC_ADJ, dict(vignette=0.26, grain=0.11), DOC_FX),
    "doc_soft": grade(dict(DOC_ADJ, contrast=0.02), dict(vignette=0.22, grain=0.10), DOC_FX),
    "bw": grade(dict(DOC_ADJ, saturation=-1, contrast=0.16), dict(vignette=0.30, grain=0.16), DOC_FX),
    "crt": grade(dict(DOC_ADJ, contrast=0.12), dict(vignette=0.30, grain=0.14),
                 dict(DOC_FX, crtCurvature=0.18, scanlines=0.34, scanlineCount=0.17, chromaticAberration=0.08)),
    "gold": grade(dict(DOC_ADJ, temperature=0.24, tint=0.04, saturation=0.02, exposure=0.06),
                  dict(vignette=0.32, grain=0.12), dict(DOC_FX, bloom=0.55, bloomRadius=10)),
    "glitch": grade(DOC_ADJ, dict(vignette=0.26, grain=0.2),
                    dict(DOC_FX, digitalGlitch=0.8, digitalGlitchColorSplit=0.6, digitalGlitchLineTear=0.55,
                         digitalGlitchPixelate=0.2, digitalGlitchBlockAmount=0.6, digitalGlitchBlockDisplacement=0.45,
                         digitalGlitchSpeed=0.6)),
    "dirty": grade(dict(DOC_ADJ, saturation=-0.7, contrast=-0.08, exposure=-0.12), dict(vignette=0.45, grain=0.55),
                   dict(DOC_FX, chromaBleed=0.5, scanlines=0.3)),
}
open(f"{PRJ}/tools/gradings.json", "w").write(json.dumps(GR, indent=1))


def gattr(name):
    return f' data-color-grading="{esc(json.dumps(GR[name], separators=(",", ":")))}"' if name else ""


FONTS_CSS = """
  @font-face { font-family: 'Satoshi'; src: url('assets/fonts/Satoshi-Medium.woff2') format('woff2'); font-weight: 500; font-style: normal; }
  @font-face { font-family: 'Satoshi'; src: url('assets/fonts/Satoshi-Bold.woff2') format('woff2'); font-weight: 700; font-style: normal; }
  @font-face { font-family: 'Satoshi'; src: url('assets/fonts/Satoshi-Black.woff2') format('woff2'); font-weight: 900; font-style: normal; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Italic.woff2') format('woff2'); font-weight: 400; font-style: italic; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Regular.woff2') format('woff2'); font-weight: 400; font-style: normal; }
"""
INK = "#FBF8EC"
GLOW = ("0 0 9px rgba(255,248,232,0.55), 0 0 26px rgba(255,244,222,0.34), 0 0 64px rgba(255,238,210,0.16), "
        "0 2px 14px rgba(0,0,0,0.32)")


# ------------------------------------------------------------------------------------------------
# Scenes
# ------------------------------------------------------------------------------------------------
class Scene:
    def __init__(self, sid, start, end, ground="#0A0908"):
        self.sid, self.start, self.end, self.ground = sid, round(start, 3), round(end, 3), ground
        self.els, self.js, self.n, self.z = [], [], 0, 1

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
        t0, t1 = max(t0, self.start), min(t1, self.end)
        return f'data-start="{r3(self.L(t0))}" data-duration="{r3(t1 - t0)}"'

    def video(self, src, t0, t1, ms=0.0, rate=None, grade="doc", push=(1.0, 1.05), box=None, cam_style="",
              vstyle="", z=None, measure=True):
        cam, vid = self.uid("cam"), self.uid("v")
        z = z or self.nz()
        x, y, w, h = box or (0, 0, 1920, 1080)
        if measure:
            SHOTS.append(dict(t0=max(t0, self.start), t1=min(t1, self.end), kind="video", src=f"{PRJ}/assets/clips/{src}.mp4",
                              ms=ms, rate=rate or 1.0, box=(x, y, w, h), clip_t0=t0))
        rate_attr = f' data-playback-rate="{rate}"' if rate else ""
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{cam_style}">'
            f'<video id="{vid}" class="clip" src="assets/clips/{src}.mp4" muted playsinline {self.timed(t0, t1)} '
            f'data-hf-media-start-basis="local" data-media-start="{r3(ms)}"{rate_attr}{gattr(grade)} data-track-index="2" '
            f'style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:cover;{vstyle}"></video></div>')
        if push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {r3(t1 - t0)}, '
                           f'ease: "none" }}, {r3(self.L(t0))});')
        return cam, vid

    def image(self, src, t0, t1, grade="doc", push=(1.0, 1.06), box=None, pos="center", fit="cover", z=None):
        cam, im = self.uid("cam"), self.uid("i")
        z = z or self.nz()
        x, y, w, h = box or (0, 0, 1920, 1080)
        SHOTS.append(dict(t0=max(t0, self.start), t1=min(t1, self.end), kind="image", src=f"{PRJ}/assets/img/{src}",
                          pos=pos, box=(x, y, w, h)))
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'
            f'<img id="{im}" class="clip" src="assets/img/{src}" alt="" {self.timed(t0, t1)}{gattr(grade)} '
            f'data-track-index="3" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:{fit};'
            f'object-position:{pos}" /></div>')
        if push:
            self.js.append(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {r3(t1 - t0)}, '
                           f'ease: "none" }}, {r3(self.L(t0))});')
        return cam, im

    def solid(self, t0, t1, color="#0A0908", texture=True):
        sid = self.uid("solid")
        SHOTS.append(dict(t0=max(t0, self.start), t1=min(t1, self.end), kind="solid", box=(0, 0, 1920, 1080)))
        tex = ('<img class="soltex" src="assets/tex/ht_paper.jpg" alt="" />' if texture else "")
        self.els.append(f'<div id="{sid}" class="clip solid" {self.timed(t0, t1)} data-track-index="1" '
                        f'style="background:{color};z-index:{self.nz()}">{tex}</div>')
        return sid

    def flash(self, t, d=0.22, peak=0.92):
        fid = self.uid("wf")
        self.els.append(f'<div id="{fid}" class="clip flashw" {self.timed(t - 0.04, t + d)} data-track-index="5" '
                        f'style="z-index:{self.nz() + 40}"></div>')
        self.js.append(f'tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: {peak}, duration: 0.04, ease: "power4.in" }}, '
                       f'{r3(self.L(t - 0.04))});')
        self.js.append(f'tl.to("#{fid}", {{ opacity: 0, duration: {r3(d - 0.01)}, ease: "power2.out" }}, {r3(self.L(t))});')

    def raw(self, el, js=None):
        self.els.append(el)
        if js:
            self.js.extend(js)

    def write(self):
        css = f"""
  {FONTS_CSS}
  #root {{ position: absolute; inset: 0; overflow: hidden; background: {self.ground}; }}
  #root .cam {{ position: absolute; transform-origin: 50% 50%; overflow: hidden; }}
  #root .solid {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: hidden; }}
  #root .soltex {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover;
    mix-blend-mode: overlay; opacity: 0.55; }}
  #root .flashw {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #FFFDF6; opacity: 0; }}
  #root .bar {{ position: absolute; left: 0; width: 1920px; background: #050505; }}
  #root .wipe {{ position: absolute; top: 0; width: 6px; height: 1080px; background: #FFFDF6;
    box-shadow: 0 0 22px 6px rgba(255,253,246,0.75); }}
  #root .page {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #F2E8D6; overflow: hidden; }}
  #root .page .ptex {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover;
    mix-blend-mode: multiply; opacity: 0.42; }}
  #root .lbl {{ position: absolute; white-space: nowrap; line-height: 1; }}
  #root .sctex {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; pointer-events: none; }}
"""
        tex = (f'<img id="{self.sid}-tx1" class="clip sctex" src="assets/tex/ht_grunge.jpg" alt="" data-start="0" '
               f'data-duration="{r3(self.dur)}" data-track-index="9" data-layout-ignore '
               f'style="mix-blend-mode:overlay;opacity:0.42;z-index:900" />'
               f'<img id="{self.sid}-tx2" class="clip sctex" src="assets/tex/ht_paper.jpg" alt="" data-start="0" '
               f'data-duration="{r3(self.dur)}" data-track-index="9" data-layout-ignore '
               f'style="mix-blend-mode:soft-light;opacity:0.30;z-index:901" />')
        body = "\n    ".join(self.els + [tex])
        js = "\n    ".join(self.js)
        open(f"{COMP}/{self.sid}.html", "w").write(f"""<template>
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
""")


SCENES = []
SHOTS = []  # every picture layer in film time, for measuring the brightness behind the captions


def scene(sid, t0, t1, **kw):
    sc = Scene(sid, t0, t1, **kw)
    SCENES.append(sc)
    return sc


def seq(sc, shots, end):
    """shots: [(start, kind, args...)] laid end to end; each runs until the next one's start (or `end`)."""
    out = []
    for k, sh in enumerate(shots):
        t0 = sh[0]
        t1 = shots[k + 1][0] if k + 1 < len(shots) else end
        out.append((t0, t1) + tuple(sh[1:]))
    return out


# ---------------- S1: the news open ----------------
S1_END = round(VT(0) - LEAD, 3)
s1 = scene("s01", 0.0, S1_END)
J = 1.56  # the audio join
o_rep = 4.91  # the reporter on camera, in sync (source 8.40)
s1.video("o_aerial", 0.0, J, rate=0.92, push=(1.06, 1.0))
s1.video("o_wallst", J, round(NT(11) - LEAD, 3), push=(1.0, 1.04))
cam_up, _ = s1.video("o_up", round(NT(11) - LEAD, 3), o_rep, push=None)
BIG = NT(14)
s1.js.append(f'tl.fromTo("#{cam_up}", {{ scale: 1.0 }}, {{ scale: 1.03, duration: {r3(BIG - 0.02 - (NT(11) - LEAD))}, ease: "none" }}, '
             f'{r3(NT(11) - LEAD)});')
s1.js.append(f'tl.fromTo("#{cam_up}", {{ scale: 1.03 }}, {{ scale: 1.16, duration: 0.45, ease: "expo.out", immediateRender: false }}, '
             f'{r3(BIG - 0.02)});')
s1.js.append(f'tl.to("#{cam_up}", {{ scale: 1.19, duration: {r3(o_rep - BIG - 0.45)}, ease: "none" }}, {r3(BIG + 0.43)});')
s1.video("o_reporter", o_rep, round(NT(24) - LEAD, 3), push=(1.0, 1.03), grade="doc_soft")
s1.video("o_jpmsign", round(NT(24) - LEAD, 3), S1_END, push=(1.0, 1.05))

# ---------------- S2: VO part 1 ----------------
S2_END = QUOTE_AT
s2 = scene("s02", S1_END, S2_END)
s2.solid(S1_END, round(VT(3) - LEAD, 3))
shots = [
    (round(VT(3) - LEAD, 3), "v_dimon_up", "doc", (1.0, 1.07)),
    (round(VT(7) - LEAD, 3), "v_flag", "doc", (1.0, 1.05)),
    (round(VT(10) - LEAD, 3), "v_walk", "doc", (1.0, 1.04)),
    (round(VT(15) - LEAD, 3), "v_wolf", "doc", (1.02, 1.08)),
    (round(VT(17) - LEAD, 3), "v_dimon_int", "doc", (1.0, 1.04)),
    (round(VT(21) - LEAD, 3), "v_heir", "bw", (1.0, 1.06)),
    (round(VT(24) - LEAD, 3), "v_weill", "doc", (1.0, 1.06)),
    (round(VT(28) - LEAD, 3), "v_money", "doc", (1.0, 1.05)),
    (round(VT(31) - LEAD, 3), "v_jessica", "doc", (1.0, 1.06)),
    (round(VT(35) - LEAD, 3), "v_tsq", "doc", (1.0, 1.04)),
    (round(VT(38) - LEAD, 3), "v_jpmsign2", "doc", (1.0, 1.05)),
    (round(VT(40) - LEAD, 3), "v_aerial2", "doc", (1.0, 1.08)),
]
for t0, t1, clip, gr, push in seq(s2, shots, S2_END):
    s2.video(clip, t0, t1, grade=gr, push=push)

# ---------------- S3: Dimon in his own words ----------------
S3_END = round(QUOTE_AT + 11.25, 3)
s3 = scene("s03", S2_END, S3_END)
TWO = round(QUOTE_AT + (281.00 - QUOTE_SRC0), 3)  # the source's own cut to the two-shot
WB, IMF, WE4 = round(QT(15) - LEAD, 3), round(QT(18) - LEAD, 3), round(QT(19) - LEAD, 3)
BIGQ, YOU2 = round(QT(29) - 0.02, 3), round(QT(30) - LEAD, 3)
s3.video("d_dimon", QUOTE_AT, WB, push=(1.0, 1.04), grade="doc")
s3.image("worldbank.jpg", WB, IMF, push=(1.0, 1.06))
s3.video("d_dimon2", IMF, WE4, ms=round(IMF - (QUOTE_AT + 278.30 - QUOTE_SRC0), 3), push=(1.04, 1.06))
s3.video("d_capitol", WE4, TWO, push=(1.0, 1.05))
s3.video("d_two", TWO, BIGQ, push=(1.0, 1.02))
s3.video("d_big", BIGQ, YOU2, push=(1.12, 1.0), grade="doc")
s3.video("d_two", YOU2, S3_END, ms=round(YOU2 - TWO, 3), push=(1.02, 1.05))

# ---------------- S4: the golden boy and Citigroup ----------------
S4_END = round(VT(95) - LEAD, 3)
s4 = scene("s04", S3_END, S4_END)
shots = [
    (S3_END, "m_name", "doc", (1.0, 1.05)),
    (round(VT(58) - LEAD, 3), "m_golden", "gold", (1.0, 1.06)),
    (round(VT(64) - LEAD, 3), "m_press", "doc", (1.0, 1.05)),
    (round(VT(69) - LEAD, 3), "m_nextline", "doc", (1.0, 1.04)),
    (round(VT(72) - LEAD, 3), "m_citicenter", "doc", (1.0, 1.08)),
    (round(VT(81) - LEAD, 3), "m_citigroup", "doc", (1.0, 1.05)),
    (round(VT(84) - LEAD, 3), "m_sidebyside", "doc", (1.0, 1.04)),
    (round(VT(90) - LEAD, 3), "m_weill", "doc", (1.0, 1.06)),
    (round(VT(92) - LEAD, 3), "m_16a", "doc", (1.04, 1.04)),
]
a16 = round(VT(92) - LEAD, 3)
step16 = round((S4_END - a16) / 3, 3)
shots += [(round(a16 + step16, 3), "m_16b", "bw", (1.04, 1.04)), (round(a16 + 2 * step16, 3), "m_16c", "doc", (1.04, 1.04))]
for t0, t1, clip, gr, push in seq(s4, shots, S4_END):
    s4.video(clip, t0, t1, grade=gr, push=push)

# ---------------- S5: fired, exile, comeback ----------------
S5_END = round(VT(137) - LEAD, 3)
s5 = scene("s05", S4_END, S5_END)
s5.solid(S4_END, round(VT(97) - LEAD, 3))
HEWAS = round(VT(99) - LEAD, 3)
FIRED = VT(101)
s5.video("m_42", round(VT(97) - LEAD, 3), HEWAS, grade="bw", push=(1.0, 1.06))
# letterboxed film strike: the soul is knocked out on "fired" (source 97.0 lands on the word, rate 1.4)
STRIKE_MS = round(97.0 - 96.35 - (FIRED - HEWAS) * 1.4, 3)
s5.raw(f'<div id="s05-bars" class="clip" {s5.timed(HEWAS, VT(104) - LEAD)} data-track-index="1" '
       f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:#050505;z-index:{s5.nz()}"></div>')
s5.video("m_strange", HEWAS, round(VT(102) - LEAD, 3), ms=max(0.0, STRIKE_MS), rate=1.4, push=(1.0, 1.06),
         box=(0, 138, 1920, 804), grade="doc")
s5.flash(FIRED, d=0.26)
s5.video("m_fall", round(VT(102) - LEAD, 3), round(VT(104) - LEAD, 3), push=(1.0, 1.08), box=(0, 138, 1920, 804))
shots = [
    (round(VT(104) - LEAD, 3), "v:m_bed", "doc", (1.0, 1.05)),
    (round(VT(107) - LEAD, 3), "i:boxing.jpg", "doc", None),
    (round(VT(111) - LEAD, 3), "v:m_snowball", "doc", (1.0, 1.06)),
    (round(VT(113) - LEAD, 3), "v:m_bezos", "doc", (1.0, 1.05)),
    (round(VT(116) - LEAD, 3), "i:bezos_amazon.jpg", "doc", (1.0, 1.06)),
    (round(VT(121) - LEAD, 3), "v:m_premise", "doc", (1.0, 1.04)),
    (round(VT(127) - LEAD, 3), "v:m_walkback", "doc", (1.0, 1.06)),
    (round(VT(131) - LEAD, 3), "v:m_wallst_hist", "bw", (1.0, 1.06)),
    (round(VT(135) - LEAD, 3), "v:m_nyse_hist", "bw", (1.0, 1.06)),
]
for t0, t1, clip, gr, push in seq(s5, shots, S5_END):
    kind, name = clip.split(":")
    if kind == "v":
        s5.video(name, t0, t1, grade=gr, push=push)
    else:
        cam, _ = s5.image(name, t0, t1, grade=gr, push=push, pos=("50% 22%" if name == "bezos_amazon.jpg" else "center"))
        if name == "boxing.jpg":  # the punch lands on "boxing"
            BX = VT(110)
            s5.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.02, duration: {r3(BX - 0.03 - t0)}, ease: "none" }}, '
                         f'{r3(s5.L(t0))});')
            s5.js.append(f'tl.fromTo("#{cam}", {{ scale: 1.02 }}, {{ scale: 1.22, duration: 0.3, ease: "expo.out", '
                         f'immediateRender: false }}, {r3(s5.L(BX - 0.03))});')
            s5.js.append(f'tl.to("#{cam}", {{ scale: 1.25, duration: {r3(t1 - BX - 0.3)}, ease: "none" }}, {r3(s5.L(BX + 0.27))});')
            s5.flash(BX, d=0.16, peak=0.55)

# ---------------- S6: Bank One ----------------
S6_END = round(VT(173) - LEAD, 3)
s6 = scene("s06", S5_END, S6_END)
s6.solid(S5_END, round(VT(139) - LEAD, 3))
BB0, CHI = round(VT(139) - LEAD, 3), round(VT(146) - LEAD, 3)
s6.video("m_bankone", BB0, CHI, push=(1.0, 1.06))
BROKEN = VT(143)
for gt0, gt1 in ((BROKEN - 0.02, BROKEN + 4 * F1), (BROKEN + 0.30, BROKEN + 0.30 + 2 * F1)):
    s6.video("m_bankone", gt0, gt1, ms=round(gt0 - BB0, 3), grade="glitch", push=None, z=s6.nz() + 20, measure=False)
s6.video("m_chicago", CHI, round(VT(147) - LEAD, 3), push=(1.0, 1.06))
s6.video("m_dividend", round(VT(147) - LEAD, 3), round(VT(150) - LEAD, 3), push=(1.0, 1.05))
# "cleaned it up": a dirty copy wipes away to the clean shot on "up"
CL0, CL1, UP = round(VT(150) - LEAD, 3), round(VT(153) - LEAD, 3), VT(152)
s6.video("m_cleaned", CL0, CL1, push=(1.0, 1.04))
cam_d, vid_d = s6.video("m_cleaned", CL0, CL1, grade="dirty", push=(1.0, 1.04), cam_style="clip-path: inset(0 0 0 var(--wx)); --wx: 0%;", measure=False)
wid = s6.uid("wipe")
s6.raw(f'<div id="{wid}" class="clip wipe" {s6.timed(UP - 0.06, UP + 0.30)} data-track-index="5" style="left:-10px;z-index:{s6.nz() + 30}"></div>',
       [f'tl.fromTo("#{cam_d}", {{ "--wx": "0%" }}, {{ "--wx": "100%", duration: 0.32, ease: "power2.inOut", immediateRender: false }}, {r3(s6.L(UP - 0.06))});',
        f'tl.fromTo("#{wid}", {{ x: 0 }}, {{ x: 1930, duration: 0.32, ease: "power2.inOut", immediateRender: false }}, {r3(s6.L(UP - 0.06))});'])
MO0, OWN, STK, PAGE0 = CL1, round(VT(157) - LEAD, 3), round(VT(161) - LEAD, 3), round(VT(164) - LEAD, 3)
s6.video("m_money", MO0, OWN, push=(1.0, 1.06))
s6.solid(OWN, STK, color="#060606")
s6.video("m_ownmoney", OWN, STK, push=(1.0, 1.05), box=(656, 0, 608, 1080))
s6.video("m_stock", STK, PAGE0, push=(1.0, 1.06))

# The cream data page (AMD reference): Bank One net income, the red line from a $500M loss to billions.
pg = s6.uid("page")
X0, X1, Y0, YS = 360, 1560, 640, 112  # x of 2000 / 2003, y of $0, px per $1B
pts = [(2000, -0.511), (2001, 2.64), (2002, 3.30), (2003, 3.54)]
P = [(X0 + (yr - 2000) * (X1 - X0) / 3, Y0 - v * YS) for yr, v in pts]
path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in P)
seglen = sum(math.dist(P[k], P[k + 1]) for k in range(3))
LOSS, INTO, BILL, PROF = VT(168), VT(169), VT(170), VT(172)
years = "".join(f'<text x="{x:.0f}" y="{Y0 + 236}" text-anchor="middle" font-family="Satoshi" font-weight="500" '
                f'font-size="34" fill="#2A2622">{yr}</text>' for (yr, _), (x, _) in zip(pts, P))
dots = "".join(f'<circle id="{pg}-d{k}" cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#E5381B" opacity="0" />' for k, (x, y) in enumerate(P))
s6.raw(
    f'<div id="{pg}" class="clip page" {s6.timed(PAGE0, S6_END)} data-track-index="4" style="z-index:{s6.nz()}">'
    f'<img class="ptex" src="assets/tex/ht_warm.jpg" alt="" />'
    f'<div id="{pg}-cam" style="position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:{P[3][0]:.0f}px {P[3][1]:.0f}px">'
    f'<div class="lbl" style="left:{X0 - 6}px;top:150px;font-family:\'Instrument Serif\';font-style:italic;font-size:92px;color:#14110F">Bank One</div>'
    f'<div class="lbl" style="left:{X0}px;top:258px;font-family:Satoshi;font-weight:500;font-size:34px;color:#4A433C">net income, 2000 - 2003</div>'
    f'<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0">'
    f'<line x1="{X0 - 80}" y1="{Y0}" x2="{X1 + 80}" y2="{Y0}" stroke="#2A2622" stroke-width="2" stroke-dasharray="10 10" opacity="0.55" />'
    f'{years}<path id="{pg}-line" d="{path}" fill="none" stroke="#E5381B" stroke-width="9" stroke-linecap="round" '
    f'stroke-linejoin="round" stroke-dasharray="{seglen:.1f}" stroke-dashoffset="{seglen:.1f}" />{dots}</svg>'
    f'<div id="{pg}-loss" class="lbl" style="left:{P[0][0] + 34:.0f}px;top:{P[0][1] + 14:.0f}px;font-family:\'Instrument Serif\';'
    f'font-style:italic;font-size:84px;color:#E5381B;opacity:0">-$500M <span style="font-family:Satoshi;font-style:normal;'
    f'font-weight:500;font-size:34px;color:#2A2622">loss</span></div>'
    f'<div id="{pg}-prof" class="lbl" style="left:{P[3][0] - 330:.0f}px;top:{P[3][1] - 150:.0f}px;font-family:\'Instrument Serif\';'
    f'font-style:italic;font-size:118px;color:#14110F;opacity:0">+$3.5B <span style="font-family:Satoshi;font-style:normal;'
    f'font-weight:700;font-size:40px;color:#14110F">profit</span></div>'
    f'</div></div>',
    [f'tl.fromTo("#{pg}-d0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, immediateRender: false }}, {r3(s6.L(VT(166) - F1))});',
     f'tl.fromTo("#{pg}-loss", {{ opacity: 0, x: -18 }}, {{ opacity: 1, x: 0, duration: 0.18, ease: "power3.out", immediateRender: false }}, {r3(s6.L(LOSS - F1))});',
     f'tl.fromTo("#{pg}-line", {{ strokeDashoffset: {seglen:.1f} }}, {{ strokeDashoffset: 0, duration: {r3(BILL + 0.22 - INTO)}, ease: "power2.inOut", immediateRender: false }}, {r3(s6.L(INTO))});']
    + [f'tl.fromTo("#{pg}-d{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06, immediateRender: false }}, {r3(s6.L(INTO + (BILL + 0.22 - INTO) * (k / 3) ** 0.9))});' for k in (1, 2, 3)]
    + [f'tl.fromTo("#{pg}-prof", {{ opacity: 0, x: 18 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out", immediateRender: false }}, {r3(s6.L(BILL + 0.2))});',
       f'tl.fromTo("#{pg}-cam", {{ scale: 1.0 }}, {{ scale: 1.16, duration: {r3(S6_END - PAGE0)}, ease: "power1.in" }}, {r3(s6.L(PAGE0))});'])

# ---------------- S7: 2004 and 2008 ----------------
S7_END = round(VT(209) - LEAD, 3)
s7 = scene("s07", S6_END, S7_END)
shots = [
    (S6_END, "m_fox", "crt", (1.0, 1.04)),
    (round(VT(178) - LEAD, 3), "m_harrison", "doc", (1.0, 1.05)),
    (round(VT(181) - LEAD, 3), "m_flags", "doc", (1.0, 1.06)),
    (round(VT(182) - LEAD, 3), "m_dow", "crt", (1.0, 1.04)),
    (round(VT(184) - LEAD, 3), "m_2008", "doc", (1.0, 1.08)),
    (round(VT(186) - LEAD, 3), "m_fire", "doc", (1.1, 1.0)),
    (round(VT(187) - LEAD, 3), "m_lehman", "doc", (1.0, 1.05)),
    (round(VT(189) - LEAD, 3), "m_bankrun", "bw", (1.0, 1.05)),
    (round(VT(191) - LEAD, 3), "m_fdic", "crt", (1.0, 1.04)),
    (round(VT(193) - LEAD, 3), "m_head", "doc", (1.0, 1.05)),
    (round(VT(194) - LEAD, 3), "m_chess", "doc", (1.0, 1.04)),
    (round(VT(199) - LEAD, 3), "m_lastman", "doc", (1.0, 1.06)),
    (round(VT(200) - LEAD, 3), "m_heli", "doc", (1.0, 1.06)),
    (round(VT(203) - LEAD, 3), "m_firesale", "crt", (1.0, 1.04)),
    (round(VT(208) - LEAD, 3), "m_bear", "doc", (1.0, 1.05)),
]
for t0, t1, clip, gr, push in seq(s7, shots, S7_END):
    if clip == "m_chess":
        s7.solid(t0, t1, color="#030303", texture=False)
        s7.video(clip, t0, t1, grade=gr, push=push, box=(656, 0, 608, 1080))
    else:
        s7.video(clip, t0, t1, grade=gr, push=push)
for ft in (VT(183), VT(186), VT(199)):
    s7.flash(ft, d=0.22, peak=0.85)

# ---------------- S8: JP Morgan & Chase, $10 trillion a day ----------------
s8 = scene("s08", S7_END, DUR)
shots = [
    (S7_END, "m_jpmstone", "doc", (1.0, 1.05)),
    (round(VT(213) - LEAD, 3), "m_chase", "doc", (1.0, 1.04)),
    (round(VT(214) - LEAD, 3), "m_nyseboard", "doc", (1.0, 1.05)),
    (round(VT(218) - LEAD, 3), "m_screens", "doc", (1.0, 1.06)),
    (round(VT(220) - LEAD, 3), "m_moneyfall", "doc", (1.0, 1.05)),
    (round(VT(223) - LEAD, 3), "m_end", "doc", (1.0, 1.07)),
]
for t0, t1, clip, gr, push in seq(s8, shots, DUR):
    s8.video(clip, t0, t1, grade=gr, push=push)
s8.raw(f'<div id="s08-fade" class="clip" {s8.timed(DUR - 0.75, DUR)} data-track-index="6" '
       f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:#000;opacity:0;z-index:950"></div>',
       [f'tl.fromTo("#s08-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.62, ease: "power1.in", immediateRender: false }}, '
        f'{r3(s8.L(DUR - 0.75))});'])


# ------------------------------------------------------------------------------------------------
# Captions (the Dimon reel's system)
# ------------------------------------------------------------------------------------------------
# style: (family, weight, italic, size)
STY = {
    "s": ("Satoshi", 500, False, 62),      # the small line
    "b": ("Satoshi", 700, False, 150),     # the key noun
    "bm": ("Satoshi", 500, False, 150),    # "World Bank" (medium, as in the reference)
    "bb": ("Satoshi", 900, False, 250),    # a giant word ("big.")
    "i": ("Instrument Serif", 400, True, 172),   # the emotive noun
    "ii": ("Instrument Serif", 400, True, 236),
    "si": ("Instrument Serif", 400, True, 72),   # the small serif "We"
    "n": ("Satoshi", 700, False, 176),     # numbers
    "xs": ("Instrument Serif", 400, True, 40),   # "small." -- set small
    "name": ("Satoshi", 700, False, 168),  # "Jamie Dimon"
}

CAPS = []


def cap(lines, y=770, end=None, x=0, kind=None, scrim=None):
    """lines: [[(text, t, style, opts)], ...]; t = film time the word is spoken."""
    CAPS.append(dict(lines=lines, y=y, end=end, x=x, kind=kind, scrim=scrim))


def w(text, t, st, **o):
    return (text, t, st, o)


def N(i, st, text=None, **o):
    return w(text or NEWS[i]["text"], NT(i), st, **o)


def V(i, st, text=None, **o):
    return w(text or VOW[i]["text"], VT(i), st, **o)


def Q(i, st, text=None, **o):
    return w(text or QUOTE[i]["text"], QT(i), st, **o)


def phrase(fn, idxs, st, text):
    """Several spoken words shown as one caption word: it lands on the first one."""
    return fn(idxs[0], st, text)


# --- the news open ---
cap([[N(0, "s", "The"), N(1, "s", "name"), N(2, "s", "of"), N(3, "s", "the")], [N(4, "i", "game")]])
cap([[N(5, "s", "in")], [N(9, "b", "American")]])
cap([[N(10, "s", "financial")], [N(11, "i", "capitalism")]])
cap([[N(12, "s", "is"), N(13, "s", "being")], [N(14, "bb", "big")]])
cap([[N(15, "s", "and"), N(16, "s", "no"), N(17, "s", "one"), N(18, "s", "is")], [N(19, "i", "bigger")]])
cap([[N(20, "s", "on")], [N(21, "b", "Wall"), N(22, "b", "Street")]])
cap([[N(23, "s", "than")], [N(24, "b", "JPMorgan"), N(26, "i", "Chase")]], end=round(VT(0) - 0.12, 3))
# --- VO part 1 ---
cap([[V(0, "s", "This"), V(1, "s", "is")]], y=540)
cap([[V(2, "s", "the"), V(3, "s", "most")], [V(4, "i", "influential")]])
cap([[V(5, "s", "man"), V(6, "s", "in")], [V(7, "b", "America")]])
cap([[V(8, "s", "right")], [V(9, "i", "now")]])
cap([[V(10, "s", "He's"), V(11, "s", "basically"), V(12, "s", "the")], [V(13, "b", "CEO")]])
cap([[V(14, "s", "of")], [V(15, "i", "Wall"), V(16, "i", "Street")]])
cap([[V(17, "s", "a"), V(18, "s", "guy"), V(19, "s", "who"), V(20, "s", "got")], [V(21, "b", "fired")]])
cap([[V(22, "s", "in")], [V(23, "n", "1998", typed=True)]])
cap([[V(24, "s", "by"), V(25, "s", "his"), V(26, "s", "own")], [V(27, "i", "mentor")]])
cap([[V(28, "s", "over"), V(29, "s", "a")], [V(30, "b", "bonus")]])
cap([[V(31, "s", "and"), V(32, "s", "a"), V(33, "s", "family")], [V(34, "i", "grudge")]])
cap([[V(35, "s", "now"), V(36, "s", "runs"), V(37, "s", "the")], [V(38, "b", "biggest"), V(39, "b", "bank")]], y=470)
cap([[V(40, "s", "in"), V(41, "s", "the")], [V(42, "i", "world")]], end=round(QT(0) - 0.08, 3))
# --- Dimon (the reference reel's own lockups) ---
cap([[Q(0, "si", "We"), Q(1, "s", "bank")]])
cap([[Q(2, "s", "some")], [Q(4, "b", "these")]])
cap([[Q(5, "i", "companies")]])
cap([[Q(7, "b", "30", dx=-150)], [Q(8, "i", "Countries")]])
cap([[Q(9, "si", "We"), Q(10, "s", "bank")], [Q(11, "i", "Countries")]])
cap([[Q(12, "si", "We"), Q(13, "s", "bank")], [Q(15, "bm", "World"), Q(16, "bm", "Bank")]])
cap([[w("We", QT(18), "si", settled=True), w("bank", QT(18), "s", settled=True)], [Q(18, "ii", "IMF")]])
cap([[Q(19, "s", "we"), Q(20, "s", "bank"), Q(21, "s", "the")], [Q(22, "b", "United"), Q(23, "b", "States")]])
cap([[Q(24, "i", "government")]])
cap([[Q(25, "s", "You"), Q(26, "s", "have"), Q(27, "s", "to"), Q(28, "s", "be")], [Q(29, "bb", "big")]])
cap([[Q(30, "s", "You"), Q(31, "s", "can't"), Q(32, "s", "do"), Q(33, "s", "those"), Q(34, "s", "things")],
     [Q(35, "s", "and"), Q(36, "s", "be"), Q(37, "xs", "small")]], end=round(VT(55) - 0.1, 3))
# --- VO part 2 ---
cap([[V(55, "s", "Meet")], [V(56, "name", "Jamie", letters=True), V(57, "name", "Dimon", letters=True)]])
cap([[V(58, "s", "the")], [V(59, "i", "golden"), V(60, "i", "boy")]])
cap([[V(61, "s", "of")], [V(62, "b", "Wall"), V(63, "b", "Street")]])
cap([[V(64, "s", "the"), V(65, "s", "guy"), V(66, "s", "everyone"), V(67, "s", "said"), V(68, "s", "was")],
     [V(69, "b", "next"), V(70, "b", "in"), V(71, "b", "line")]])
cap([[V(72, "s", "to"), V(73, "s", "run"), V(74, "s", "the"), V(75, "s", "biggest")], [V(76, "i", "financial"), V(77, "i", "company")]])
cap([[V(78, "s", "in"), V(79, "s", "the")], [V(80, "i", "world")]])
cap([[V(81, "s", "He"), V(82, "s", "built")], [V(83, "b", "Citigroup")]])
cap([[V(84, "s", "side"), V(85, "s", "by"), V(86, "s", "side"), V(87, "s", "with"), V(88, "s", "his")], [V(89, "i", "mentor")]])
cap([[V(90, "b", "Sandy"), V(91, "b", "Weill")]])
cap([[V(92, "s", "for")], [V(93, "n", "16", count=[1, 4, 7, 10, 13, 16]), V(94, "i", "years")]])
cap([[V(95, "s", "But"), V(96, "s", "then")]], y=540)
cap([[V(97, "s", "at")], [V(98, "n", "42")]])
cap([[V(99, "s", "he"), V(100, "s", "was")], [V(101, "bb", "fired")]])
cap([[V(102, "n", "18", count=[1, 4, 8, 12, 15, 18]), V(103, "s", "months")], [V(104, "i", "of"), V(105, "i", "no"), V(106, "i", "job")]])
cap([[V(107, "s", "He"), V(108, "s", "took"), V(109, "s", "up")], [V(110, "b", "boxing")]])
cap([[V(111, "s", "read")], [V(112, "i", "biographies")]])
cap([[V(113, "s", "even"), V(114, "s", "met")], [V(115, "b", "Bezos")]])
cap([[V(116, "s", "for"), V(117, "s", "a"), V(118, "s", "job"), V(119, "s", "at")], [V(120, "i", "Amazon")]])
cap([[V(121, "s", "But"), V(122, "s", "it"), V(123, "s", "was"), V(124, "s", "all"), V(125, "s", "a")], [V(126, "i", "premise")]])
cap([[V(127, "s", "for"), V(128, "s", "the"), V(129, "s", "greatest")], [V(130, "b", "comeback")]])
cap([[V(131, "s", "in"), V(132, "s", "the"), V(133, "s", "history"), V(134, "s", "of")], [V(135, "i", "Wall"), V(136, "i", "Street")]])
cap([[V(137, "s", "In")], [V(138, "n", "2000", typed=True)]], y=560)
cap([[V(139, "s", "he"), V(140, "s", "takes"), V(141, "s", "over"), V(142, "s", "a")], [V(143, "i", "broken"), V(144, "i", "bank")]])
cap([[V(145, "s", "in")], [V(146, "b", "Chicago")]])
cap([[V(147, "s", "cuts"), V(148, "s", "the")], [V(149, "i", "dividend", slice=True)]])
cap([[V(150, "s", "cleaned"), V(151, "s", "it")], [V(152, "b", "up")]])
cap([[V(153, "s", "and"), V(154, "s", "put")], [V(155, "n", "$60", count=["$5", "$14", "$26", "$39", "$51", "$60"]), V(156, "i", "million")]])
cap([[V(157, "s", "of"), V(158, "s", "his")], [V(159, "i", "own"), V(160, "i", "money")]])
cap([[V(161, "s", "into"), V(162, "s", "the")], [V(163, "b", "stock")]], end=round(VT(164) - LEAD, 3))
# (the data page carries "turned a $500 million loss into billions in profit" in its own labels)
cap([[V(173, "s", "That"), V(174, "s", "bank"), V(175, "s", "got")], [V(176, "b", "acquired")]], y=545)
cap([[V(177, "s", "by")], [V(178, "b", "JP"), V(179, "b", "Morgan")]])
cap([[V(180, "s", "in")], [V(181, "n", "2004", typed=True)]])
cap([[V(182, "s", "Then")], [V(183, "n", "2008", typed=True)]])
cap([[V(184, "s", "financial")], [V(185, "i", "crisis"), V(186, "b", "hit")]])
cap([[V(187, "s", "and"), V(188, "s", "when"), V(189, "s", "every"), V(190, "s", "other"), V(191, "s", "bank"), V(192, "s", "was")],
     [V(193, "i", "dying")]])
cap([[V(194, "s", "he"), V(195, "s", "was"), V(196, "s", "the")], [V(197, "b", "only"), V(198, "b", "one")]], scrim=0.62)
cap([[V(199, "ii", "standing")]])
cap([[V(200, "s", "with"), V(201, "s", "enough")], [V(202, "b", "money")]])
cap([[V(203, "s", "to"), V(204, "s", "buy"), V(205, "s", "the"), V(206, "s", "ones"), V(207, "s", "that")], [V(208, "i", "fell")]])
cap([[V(209, "s", "That's")], [V(210, "b", "JP"), V(211, "b", "Morgan"), V(212, "i", "&"), V(213, "i", "Chase")]])
cap([[V(214, "s", "the"), V(215, "s", "name"), V(216, "s", "that"), V(217, "s", "moves")],
     [V(218, "n", "$10", count=["$1", "$3", "$5", "$8", "$10"]), V(219, "i", "trillion")]], y=860)
cap([[V(220, "s", "every"), V(221, "s", "single")], [V(222, "i", "day")]])
cap([[V(223, "ii", "today")]], end=round(DUR - 0.25, 3))


SCRIMS = []


def _frame(shot, t):
    """The picture layer as a 1920x1080 grey image at film time t (approximate: no grade, no camera push)."""
    import io, subprocess
    from PIL import Image
    canvas = Image.new("L", (1920, 1080), 12)
    if shot["kind"] == "solid":
        return canvas
    x, y, w, h = shot["box"]
    if shot["kind"] == "image":
        im = Image.open(shot["src"]).convert("L")
        sc = max(w / im.width, h / im.height)
        im = im.resize((max(w, round(im.width * sc)), max(h, round(im.height * sc))))
        ox, oy = (im.width - w) // 2, (im.height - h) // 2
        if shot.get("pos", "center") != "center":
            oy = int((im.height - h) * float(shot["pos"].split()[1].rstrip("%")) / 100)
        im = im.crop((ox, oy, ox + w, oy + h))
    else:
        mt = max(0.0, shot["ms"] + (t - shot["clip_t0"]) * shot["rate"])
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{mt:.3f}", "-i", shot["src"], "-frames:v", "1",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        if not r.stdout:
            return canvas
        im = Image.open(io.BytesIO(r.stdout)).convert("L").resize((w, h))
    canvas.paste(im, (x, y))
    return canvas


def caption_lum(g, toks, t0, t1):
    """Mean brightness (0-255) of the picture behind a caption group, sampled at its first and its biggest word."""
    from PIL import ImageStat
    big = max(toks, key=lambda tk: STY[tk[2]][3])
    vals = []
    for t in sorted({round(t0 + 0.05, 3), round(min(big[1] + 0.1, t1 - 0.02), 3)}):
        cover = [s for s in SHOTS if s["t0"] <= t < s["t1"]]
        if not cover:
            continue
        fr = _frame(cover[-1], t)
        y = g["y"]
        vals.append(ImageStat.Stat(fr.crop((560, max(0, y - 130), 1360, min(1080, y + 120)))).mean[0])
    return max(vals) if vals else 0.0


def build_captions():
    els, js, filters = [], [], []
    groups = CAPS
    for gi, g in enumerate(groups):
        gid = f"cg{gi:03d}"
        toks = [t for line in g["lines"] for t in line]
        onsets = [t[1] for t in toks if not t[3].get("settled")]
        first = min(onsets) if onsets else toks[0][1]
        t0 = round(first - F1, 3)
        nxt = None
        if gi + 1 < len(groups):
            nt = [t[1] for line in groups[gi + 1]["lines"] for t in line if not t[3].get("settled")]
            nxt = round(min(nt) - F1, 3)
        last = max(onsets) if onsets else first
        t1 = g["end"] if g["end"] is not None else (nxt if nxt is not None else DUR)
        if nxt is not None and t1 > nxt:
            t1 = nxt
        if g["end"] is None and nxt is not None and nxt - last > 1.6:  # a long pause: let it go before the next
            t1 = round(last + 1.1, 3)
        lines_html = []
        order = []  # reading order of word element ids
        for li, line in enumerate(g["lines"]):
            spans = []
            for wi, (text, tt, st, o) in enumerate(line):
                fam, wt, it, size = STY[st]
                sid = f"{gid}-w{li}{wi}"
                ml = "" if wi == 0 else ("margin-left:0.24em;" if fam == "Satoshi" else "margin-left:0.18em;")
                if o.get("dx"):
                    ml += f"position:relative;left:{o['dx']}px;"
                track = "-0.035em" if (fam == "Satoshi" and size >= 120) else ("-0.012em" if fam == "Satoshi" else "-0.01em")
                style = (f"{ml}font-family:'{fam}';font-weight:{wt};font-style:{'italic' if it else 'normal'};font-size:{size}px;"
                         f"letter-spacing:{track};")
                settled = o.get("settled")
                fid = f"{sid}-hb"
                filt = "" if settled else f"filter:url(#{fid});"
                inner = esc(text)
                if o.get("letters"):
                    inner = "".join(f'<span id="{sid}-l{k}" class="lt">{esc(ch)}</span>' for k, ch in enumerate(text))
                if o.get("typed"):
                    inner = "".join(f'<span id="{sid}-l{k}" class="lt">{esc(ch)}</span>' for k, ch in enumerate(text))
                if o.get("count"):
                    vals = [str(v) for v in o["count"]]
                    inner = "".join(f'<span id="{sid}-c{k}" class="cv" style="opacity:{1 if k == 0 else 0}">{esc(v)}</span>'
                                    for k, v in enumerate(vals))
                if o.get("slice"):
                    inner = (f'<span class="slb">{esc(text)}</span>'
                             f'<span id="{sid}-sa" class="sla">{esc(text)}</span>'
                             f'<span id="{sid}-sb" class="slz">{esc(text)}</span>'
                             f'<span id="{sid}-sl" class="slice-line"></span>')
                cls = "w" + (" cnt" if o.get("count") else "") + (" slw" if o.get("slice") else "")
                spans.append(f'<span id="{sid}" class="{cls}" style="{style}{filt}opacity:{1 if settled else 0}">{inner}</span>')
                order.append((sid, size))
                if settled:
                    continue
                filters.append(f'<filter id="{fid}" x="-60%" y="-80%" width="220%" height="260%" color-interpolation-filters="sRGB">'
                               f'<feGaussianBlur id="{fid}-g" in="SourceGraphic" stdDeviation="0 0" /></filter>')
                at = round(tt - F1 - t0, 3)  # the entrance starts one frame before the onset
                blur = 34 if size >= 140 else 22
                js.append(f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, ease: "power2.out", '
                          f'immediateRender: false }}, {r3(t0 + at)});')
                js.append(f'tl.fromTo("#{fid}-g", {{ attr: {{ stdDeviation: "{blur} 0" }} }}, {{ attr: {{ stdDeviation: "0 0" }}, '
                          f'duration: 0.12, ease: "power2.out", immediateRender: false }}, {r3(t0 + at)});')
                if o.get("letters"):
                    for k in range(len(text)):
                        lt = round(t0 + at + k * 0.035, 3)
                        js.append(f'tl.fromTo("#{sid}-l{k}", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.12, ease: "power1.out", '
                                  f'immediateRender: false }}, {r3(lt)});')
                if o.get("typed"):
                    for k in range(len(text)):
                        js.append(f'tl.set("#{sid}-l{k}", {{ opacity: 1 }}, {r3(t0 + at + k * 0.065)});')
                if o.get("count"):
                    vals = o["count"]
                    for k in range(1, len(vals)):
                        ct = round(t0 + at + 0.1 + k * 0.07, 3)
                        js.append(f'tl.set("#{sid}-c{k - 1}", {{ opacity: 0 }}, {r3(ct)});')
                        js.append(f'tl.set("#{sid}-c{k}", {{ opacity: 1 }}, {r3(ct)});')
                if o.get("slice"):
                    ts = round(tt + 0.30, 3)
                    if ts < t1 - 0.12:
                        js.append(f'tl.fromTo("#{sid}-sa", {{ x: 0, y: 0 }}, {{ x: -18, y: -8, duration: 0.16, ease: "power3.out", immediateRender: false }}, {r3(ts)});')
                        js.append(f'tl.fromTo("#{sid}-sb", {{ x: 0, y: 0 }}, {{ x: 18, y: 8, duration: 0.16, ease: "power3.out", immediateRender: false }}, {r3(ts)});')
                        js.append(f'tl.set("#{sid}-sl", {{ opacity: 1 }}, {r3(ts - F1)});')
                        js.append(f'tl.set("#{sid}-sl", {{ opacity: 0 }}, {r3(ts + 2 * F1)});')
            lines_html.append(f'<div class="ln">{"".join(spans)}</div>')
        # cascading exit in reading order; the biggest word goes last. With under 0.45 s left after the last word the
        # group is simply replaced by the next one on its onset (the reference does this when the speech is quick).
        hold = t1 - last
        span = min(0.26, max(0.14, hold * 0.4))
        E = round(t1 - span, 3)
        lum = caption_lum(g, toks, t0, t1)
        if lum > 85 or g.get("scrim"):  # a soft scrim sized to the text when the picture behind it is bright or busy
            a = g.get("scrim") or (0.40 if lum < 140 else (0.52 if lum < 185 else 0.60))
            scr = f"{gid}-scr"
            lines_html.insert(0, f'<div id="{scr}" class="scrim" data-layout-ignore style="background:radial-gradient(closest-side, '
                                 f'rgba(8,7,6,{a}) 0%, rgba(8,7,6,{round(a * 0.62, 3)}) 48%, rgba(8,7,6,0) 100%)"></div>')
            js.append(f'tl.fromTo("#{scr}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, ease: "power1.out", immediateRender: false }}, {r3(t0)});')
            if hold >= 0.45 or g["end"] is not None:
                js.append(f'tl.to("#{scr}", {{ opacity: 0, duration: {r3(span)}, ease: "power1.in" }}, {r3(E)});')
        SCRIMS.append((gid, round(lum)))
        if hold >= 0.45 or g["end"] is not None:
            ids = [sid for sid, _ in order]
            big = max(order, key=lambda o: o[1])[0]
            ids = [i for i in ids if i != big] + [big]
            stp = (span - 0.1) / max(1, len(ids) - 1) if len(ids) > 1 else 0
            for k, sid in enumerate(ids):
                te = round(max(E + k * stp, last + 0.06), 3)
                js.append(f'tl.to("#{sid}", {{ opacity: 0.5, duration: 0.05, ease: "none" }}, {r3(te)});')
                js.append(f'tl.to("#{sid}", {{ opacity: 0, duration: 0.07, ease: "power1.in" }}, {r3(te + 0.05)});')
        els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(t1 - t0)}" data-track-index="1" '
                   f'data-layout-allow-overflow data-layout-allow-overlap style="top:{g["y"] - 540}px">{"".join(lines_html)}</div>')
    css = f"""
  {FONTS_CSS}
  #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; }}
  #root .cg {{ position: absolute; left: 0; width: 1920px; height: 1080px; display: flex; flex-direction: column;
    align-items: center; justify-content: center; }}
  #root .ln {{ display: flex; flex-direction: row; align-items: baseline; justify-content: center; white-space: nowrap;
    line-height: 0.98; }}
  #root .w {{ display: inline-block; position: relative; white-space: nowrap; color: {INK}; text-shadow: {GLOW}; }}
  #root .lt {{ opacity: 0; }}
  #root .scrim {{ position: absolute; left: 385px; top: 330px; width: 1150px; height: 420px; opacity: 0; }}
  #root .w.cnt {{ display: inline-grid; }}
  #root .w.cnt .cv {{ grid-area: 1 / 1; justify-self: center; }}
  #root .slw .slb {{ visibility: hidden; }}
  #root .slw .sla, #root .slw .slz {{ position: absolute; left: 0; top: 0; }}
  #root .slw .sla {{ clip-path: polygon(-10% -20%, 110% -20%, 110% 36%, -10% 66%); }}
  #root .slw .slz {{ clip-path: polygon(-10% 66%, 110% 36%, 110% 120%, -10% 120%); }}
  #root .slw .slice-line {{ position: absolute; left: -12%; width: 124%; top: 50%; height: 4px; background: #FFFDF6;
    box-shadow: 0 0 18px 4px rgba(255,253,246,0.8); transform: rotate(-6deg); opacity: 0; }}
"""
    open(f"{COMP}/captions.html", "w").write(f"""<template>
  <style>{css}  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">
    <svg width="0" height="0" style="position:absolute;left:0;top:0" aria-hidden="true"><defs>
      {chr(10).join('      ' + f for f in filters)}
    </defs></svg>
    {chr(10).join('    ' + e for e in els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(DUR)} }}, 0);
    {chr(10).join('    ' + j for j in js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
""")
    return len(groups)


def write_texture():
    """The user's halftone print textures over every frame, low opacity (the 'old TV' scanlines live in the grades)."""
    open(f"{COMP}/texture.html", "w").write(f"""<template>
  <style>
  #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
  #root .tx {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; }}
  </style>
  <div id="root" data-composition-id="texture" data-width="1920" data-height="1080">
    <img id="tex-grunge" class="clip tx" src="assets/tex/ht_grunge.jpg" alt="" data-start="0" data-duration="{r3(DUR)}"
      data-track-index="1" data-layout-ignore style="mix-blend-mode:overlay;opacity:0.42" />
    <img id="tex-paper" class="clip tx" src="assets/tex/ht_paper.jpg" alt="" data-start="0" data-duration="{r3(DUR)}"
      data-track-index="2" data-layout-ignore style="mix-blend-mode:soft-light;opacity:0.30" />
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(DUR)} }}, 0);
    window.__timelines["texture"] = tl;
  </script>
</template>
""")


def write_root():
    hosts = []
    for k, sc in enumerate(SCENES):
        hosts.append(
            f'<div id="{sc.sid}" class="clip" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" '
            f'data-start="{r3(sc.start)}" data-duration="{r3(sc.dur)}" data-track-index="1" data-track-kind="graphics" '
            f'data-width="1920" data-height="1080" style="z-index:{10 + k}"></div>')
    hosts.append(f'<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{r3(DUR)}" data-track-index="3" data-track-kind="captions" '
                 f'data-width="1920" data-height="1080" style="z-index:100"></div>')
    auds = [
        ("news-a", "news_open.wav", 0.0, NEWS_J1[1] - NEWS_J1[0], NEWS_J1[0], 0.0, 0.02),
        ("news-b", "news_open.wav", NEWS_J1[1] - NEWS_J1[0], NEWS_J2[1] - NEWS_J2[0], NEWS_J2[0], 0.02, 0.25),
        ("vo-a", "vo.wav", VO1_AT, VO1_OUT - VO1_IN, VO1_IN, 0.0, 0.06),
        ("dimon", "dimon_quote.wav", QUOTE_AT, 11.25, QUOTE_SRC0 - 272.5, 0.02, 0.06),
        ("vo-b", "vo.wav", round(VO2_IN + VO2_OFF, 3), VO2_OUT - VO2_IN, VO2_IN, 0.0, 0.08),
    ]
    a_html = []
    for aid, src, st, d, ms, fi, fo in auds:
        a_html.append(f'<audio id="{aid}" class="clip" src="assets/audio/{src}" data-start="{r3(st)}" data-duration="{r3(d)}" '
                      f'data-media-start="{r3(ms)}" data-volume="1"{f" data-fade-in={chr(34)}{fi}{chr(34)}" if fi else ""} '
                      f'data-fade-out="{fo}" data-track-index="10"></audio>')
    page = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0A0908; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; background: #0A0908; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r3(DUR)}" data-width="1920" data-height="1080">
      <div id="bg"></div>
{chr(10).join('      ' + h for h in hosts)}
{chr(10).join('      ' + a for a in a_html)}
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
    for sc in SCENES:
        sc.write()
    n = build_captions()
    write_root()
    print("scenes:", [(sc.sid, sc.start, sc.end) for sc in SCENES])
    print("caption groups:", n, " VO2 offset:", VO2_OFF, " quote offset:", QUOTE_OFF)
    print("key times: big", NT(14), "influential", VT(4), "fired", VT(101), "standing", VT(199), "today", VT(223))
