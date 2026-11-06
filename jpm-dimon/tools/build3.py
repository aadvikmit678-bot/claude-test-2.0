#!/usr/bin/env python3
"""v3 -- Jamie Dimon / JPMorgan Chase, rebuilt to the references (1920x1080, 30 fps, 93.2 s).

v3 over v2: the Bloomberg open's own music under the whole film (tools/make_music.py), no blurred-side vertical
strips, faster cutting on stronger footage, more photographs (his meetings, logos as printed cards, the Bank One tower,
the hundreds), a flip calendar, a logo merger, the fallen banks dropping off the page, bigger roller cards.

v2 notes (still true):

References: the Larry Fink reel (pace: a new picture every 1-3 words, negative flashes, seal ring, name card, bar
write-on, typed giant words, chunk counters, 2x2 grids, window zoom-out), the AMD reel (headline highlight sweeps,
cream data page), the RC Media reels (Hemant Taneja: words behind cut-outs, photo walls; Dario: bloom glow serif,
name glitch, echo type, year roller with floating cards) and the Pattinson edit (Instrument Serif glow with the
flicker box, lines that slide to re-centre as each word arrives, paper beats).

The clock is the voice: every cut and word lands on Parakeet word times snapped to the waveform.

Run:  python3 -I tools/build2.py --specs   (writes tools/media_v2.json for tools/prep2.py)
      python3 -I tools/prep2.py
      python3 -I tools/build2.py           (writes index.html and compositions/)
"""
import array, json, math, os, random, sys, wave
from fontTools.ttLib import TTFont

ROOT = "/home/user/claude-test-2.0"
PRJ = f"{ROOT}/jpm-dimon"
COMP = f"{PRJ}/compositions"
TX = f"{ROOT}/dimon-work/tx"
F1 = 1 / 30
LEAD = 0.05
DUR = 93.20


def r3(x):
    return f"{round(float(x), 3):.3f}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ================================================================================================
# The clock
# ================================================================================================
def envelope(path, hop=0.01):
    w = wave.open(path)
    n, ch = w.getnframes(), w.getnchannels()
    sr = w.getframerate()
    a = array.array("h", w.readframes(n))
    if ch > 1:
        a = a[::ch]
    step = int(sr * hop)
    return [20 * math.log10(math.sqrt(sum(x * x for x in a[i:i + step]) / step) / 32768 + 1e-9)
            for i in range(0, len(a) - step, step)]


def snap(words, env, quiet, loud, hop=0.01):
    prev = -1.0
    n = len(env)
    for w in words:
        s = w["start"]
        i0 = min(n - 1, max(0, int(round(s / hop))))
        if env[i0] < quiet:
            for i in range(i0, min(n, i0 + int(0.32 / hop))):
                if env[i] > loud:
                    s = i * hop - 0.015
                    break
        else:
            lo = int(max(prev + 0.12, s - 0.25) / hop)
            for i in range(i0, max(lo, 0), -1):
                if env[i - 1] < quiet:
                    s = i * hop - 0.015
                    break
        s = max(s, prev + 0.06)
        w["start"] = round(max(0.0, s), 3)
        prev = w["start"]
    return words


def load(path):
    return [dict(text=w["text"], start=float(w["start"]), end=float(w["end"])) for w in json.load(open(path))]


NEWS = snap(load(f"{TX}/pk_game/transcript.json"), envelope(f"{TX}/game_open.wav"), -44, -32)
QUOTE = load(f"{TX}/pk_bank/transcript.json")
QUOTE.insert(25, dict(text="You", start=8.62, end=8.76))
QUOTE = snap(QUOTE, envelope(f"{TX}/bank_quote.wav"), -50, -34)
VOW = snap(load(f"{TX}/pk_vo/transcript.json"), envelope(f"{ROOT}/dimon-work/vo/vo16k.wav"), -55, -35)

VO1_AT, VO1_IN, VO1_OUT = 9.05, 0.00, 14.10
VO2_IN, VO2_OUT = 18.40, 75.00
VO2_OFF = round(35.25 - VOW[55]["start"], 3)
QUOTE_AT, QUOTE_SRC0 = 23.60, 273.05
QUOTE_OFF = round(QUOTE_AT - (QUOTE_SRC0 - 272.5), 3)
NEWS_J1, NEWS_J2 = (1.12, 2.68), (5.05, 12.30)


def NT(i):
    s = NEWS[i]["start"]
    return round(s - 1.12, 3) if s < 3.0 else round(s - 3.49, 3)


def VT(i):
    s = VOW[i]["start"]
    return round(s + VO1_AT - VO1_IN, 3) if s < 14.2 else round(s + VO2_OFF, 3)


def QT(i):
    return round(QUOTE[i]["start"] + QUOTE_OFF, 3)


def CUT(t):
    return round(t - LEAD, 3)


# ================================================================================================
# Media registry (prep2.py extracts what is registered here)
# ================================================================================================
MEDIA = {"clips": {}, "stills": {}}
VERT = {"P01", "P03", "P04", "P08", "P11", "RIB", "WALLV", "NYSEV", "JPMV"}
FRAME_OF = {"GAME": "BBG", "BANK": "BBG", "HOW": "CNBC", "UNT": "UNTF", "STO": "SIXTY"}


def CL(key, t, dur, frame=None, size=None, xyz=None):
    size = size or ((608, 1080) if key in VERT else (1920, 1080))
    frame = frame or FRAME_OF.get(key, "FULL")
    dur = round(dur + 0.25, 2)
    cid = f"{key}_{int(round(t * 100))}_{int(round(dur * 100))}" + ("v" if size[0] < size[1] else "") + \
          (f"_{frame.lower()}" if frame not in ("FULL", FRAME_OF.get(key, "FULL")) else "") + \
          ("_x" + "_".join(str(int(v * 100)) for v in xyz) if xyz else "")
    MEDIA["clips"][cid] = dict(key=key, t=round(t, 3), dur=dur, frame=frame, size=list(size), frame_xyz=xyz)
    return cid


def ST(sid, **spec):
    MEDIA["stills"][sid] = spec
    return f"{sid}.{spec.get('ext', 'jpg')}"


# stills used by the set pieces
P_IMG = "Jamie_Dimon_Image_Pack"
CUT_DIMON_UP = ST("cut_dimon06", path=f"{ROOT}/dimon-work/cut/dimon06.png", ext="png", edge=1600)
CUT_DIMON_SMILE = ST("cut_dimon09", path=f"{ROOT}/dimon-work/cut/dimon09.png", ext="png", edge=1600, crop=[0.08, 0, 0.92, 1])
CUT_BEZOS = ST("cut_bezos03", path=f"{ROOT}/dimon-work/cut/bezos03.png", ext="png", edge=1500)
SEAL = ST("seal", path="money_pinterest videos/Seal_of_the_President_of_the_United_States.png", ext="png", edge=1400)
NYT = ST("nyt_1093", key="MPB", t=1093.0, frame="FULL")
BOX_GLOVES = ST("gloves", path=f"{P_IMG}/10_Supporting_Illustrative/01_ILLUSTRATIVE_boxing_gloves_generic.jpg", edge=1920)
WB_BLDG = ST("worldbank", path=f"{P_IMG}/08_World_Bank/02_World_Bank_building_Washington.jpg", edge=1920)
GOV = [ST("gov_capitol", path=f"{P_IMG}/07_US_Government_America/01_US_Capitol_west_front.jpg", edge=900),
       ST("gov_whitehouse", path=f"{P_IMG}/07_US_Government_America/02_White_House_north_facade.jpg", edge=900),
       ST("gov_treasury", path=f"{P_IMG}/07_US_Government_America/04_US_Treasury_Building.jpg", edge=900),
       ST("gov_fed", path=f"{P_IMG}/07_US_Government_America/06_Federal_Reserve_Eccles_Building.jpg", edge=900),
       ST("gov_treasury2", path=f"{P_IMG}/07_US_Government_America/05_US_Treasury_Gallatin_statue.jpg", edge=900),
       ST("gov_fed1937", path=f"{P_IMG}/07_US_Government_America/07_Federal_Reserve_Eccles_1937_archival.jpg", edge=900)]
LEADERS = [ST("lead_reeves", path=f"{P_IMG}/01_Jamie_Dimon/07_Jamie_Dimon_meets_Rachel_Reeves_01.jpg", edge=1000),
           ST("lead_macri", path=f"{P_IMG}/01_Jamie_Dimon/10_Jamie_Dimon_with_Mauricio_Macri.jpg", edge=1000),
           ST("lead_japan", path=f"{P_IMG}/01_Jamie_Dimon/12_Jamie_Dimon_Japan_PM_courtesy_call_02.jpg", edge=1000)]
LOGOS = {"lehman": ST("logo_lehman", path=f"{P_IMG}/09_2008_Crisis/07_Lehman_Brothers_logo_svg.svg", ext="svg"),
         "wamu": ST("logo_wamu", path=f"{P_IMG}/09_2008_Crisis/09_WaMu_logo_svg.svg", ext="svg"),
         "jpmc": ST("logo_jpmc", path=f"{P_IMG}/05_JPMorgan_Chase/04_JPMorganChase_logo_2024_svg.svg", ext="svg")}
CRISIS_PICS = [ST("cr_lehman_boxes", path=f"{P_IMG}/09_2008_Crisis/02_Lehman_Brothers_employees_boxes_2008.jpg", edge=1200),
               ST("cr_bear_sign", path=f"{P_IMG}/09_2008_Crisis/05_Bear_Stearns_signage.jpg", edge=1200),
               ST("cr_wamu", path=f"{P_IMG}/09_2008_Crisis/06_WaMu_Center_Seattle_1201_Third.jpg", edge=1200),
               ST("cr_lehman_ts", path=f"{P_IMG}/09_2008_Crisis/03_Lehman_Brothers_Times_Square.jpg", edge=1200),
               ST("cr_lehman_nyc", path=f"{P_IMG}/09_2008_Crisis/01_Lehman_Brothers_NYC_Sept_15_2008.jpg", edge=1200)]
# seal-ring portraits: frames of Dimon from many stages
RING = [ST(f"ring{k}", key=key, t=t, frame=FRAME_OF.get(key, "FULL")) for k, (key, t) in enumerate([
    ("BANK", 36.5), ("BANK", 70.0), ("BANK", 76.0), ("GAME", 64.4), ("CHAIR", 1265.0), ("SPEAK", 20.0),
    ("MPB", 1299.0), ("HOW", 51.5), ("BANK", 1032.0), ("GAME", 124.8), ("CHAIR", 2210.0), ("BANK", 53.0)])]
# photo wall: a century of Wall Street
WALL = [ST(f"wall{k}", key=key, t=t, frame=FRAME_OF.get(key, "FULL"), size=[640, 360]) for k, (key, t) in enumerate([
    ("HOW", 300.5), ("HOW", 303.0), ("HOW", 306.5), ("HOW", 309.0), ("HOW", 312.5), ("HOW", 318.0), ("HOW", 323.5),
    ("HOW", 327.5), ("HOW", 332.0), ("HOW", 43.5), ("HOW", 789.6), ("MPB", 783.5), ("MPB", 786.0), ("MPB", 790.0),
    ("MPB", 799.5), ("MPB", 1490.5), ("MPB", 1507.0), ("MPB", 1512.5), ("MPB", 830.5), ("STO", 346.0),
    ("STO", 349.5), ("BANK", 225.5), ("GAME", 81.5), ("MPB", 1526.0)])]
# floating cards for the year rollers
CARDS_8298 = [ST(f"c16_{k}", key=key, t=t, frame=FRAME_OF.get(key, "FULL"), size=[640, 360]) for k, (key, t) in enumerate([
    ("MPB", 718.0), ("BANK", 440.0), ("BANK", 448.5), ("BANK", 456.0), ("UNT", 558.0), ("UNT", 1017.5), ("MPB", 841.5)])]
CARDS_0408 = [ST(f"c08_{k}", key=key, t=t, frame=FRAME_OF.get(key, "FULL"), size=[640, 360]) for k, (key, t) in enumerate([
    ("MPB", 1891.0), ("STO", 1439.5), ("BANK", 492.0), ("GAME", 409.5), ("STO", 30.0), ("MPB", 1885.0)])]
BOOKS = [CL("MPB", 616.0, 0.5), CL("MPB", 1496.0, 0.5), CL("MPB", 1273.0, 0.5)]
# v3: more photographs
DIMON_PHOTOS = [ST(f"dp{k}", path=f"{P_IMG}/01_Jamie_Dimon/{f}", edge=1400) for k, f in enumerate([
    "01_Jamie_Dimon_CEO_JPMorgan_Healthcare_2013.jpg", "03_Jamie_Dimon_portrait_crop_Davos_2016.jpg",
    "06_Jamie_Dimon_Global_Financial_Context_crop.jpg", "09_Jamie_Dimon_Rachel_Reeves_portrait_crop.jpg",
    "05_Jamie_Dimon_Global_Financial_Context.jpg", "16_Jamie_Dimon_with_Mark_Hoffman_CNBC.jpg"])]
PIN_DIMON = [ST("pin_bw", path="money_pinterest videos/jamie black and white image.jpg", edge=900),
             ST("pin_green", path="money_pinterest videos/jamie dimon pic.jpg", edge=900),
             ST("pin_mic", path="money_pinterest videos/jamie image.jpg", edge=900)]
RING_PICS = [p for trio in zip(DIMON_PHOTOS, RING[:6], PIN_DIMON * 2) for p in trio]
LEADERS = [ST(f"ld{k}", path=f"{P_IMG}/01_Jamie_Dimon/{f}", edge=1100) for k, f in enumerate([
    "07_Jamie_Dimon_meets_Rachel_Reeves_01.jpg", "11_Jamie_Dimon_Japan_PM_courtesy_call_01.jpg",
    "10_Jamie_Dimon_with_Mauricio_Macri.jpg", "02_Jamie_Dimon_WEF_Davos_Becky_Quick_2016.jpg",
    "12_Jamie_Dimon_Japan_PM_courtesy_call_02.jpg", "08_Jamie_Dimon_meets_Rachel_Reeves_02.jpg",
    "15_Jamie_Dimon_WEF_with_Gary_Cohn_panel.jpg", "13_Jamie_Dimon_Japan_PM_courtesy_call_03.jpg",
    "04_Jamie_Dimon_with_Bill_McDermott_Becky_Quick.jpg", "14_Jamie_Dimon_Army_Navy_game_event.jpg"])]
LOGO = {"citi": ST("lg_citi", path=f"{P_IMG}/04_Citigroup/09_Citi_logo_March_2023_svg.svg", ext="svg"),
        "bankone": ST("lg_bankone", path=f"{P_IMG}/06_Bank_One_Chicago/05_Bank_One_logo_svg.svg", ext="svg"),
        "jpm": ST("lg_jpm", path=f"{P_IMG}/05_JPMorgan_Chase/07_JPMorgan_logo_svg.svg", ext="svg"),
        "jpmc08": ST("lg_jpmc08", path=f"{P_IMG}/05_JPMorgan_Chase/05_JPMorgan_Chase_logo_2008_svg.svg", ext="svg"),
        "chase": ST("lg_chase", path=f"{P_IMG}/05_JPMorgan_Chase/06_Chase_logo_2007_svg.svg", ext="svg"),
        "wb": ST("lg_wb", path=f"{P_IMG}/08_World_Bank/04_World_Bank_logo_svg.svg", ext="svg"),
        "lehman": LOGOS["lehman"], "wamu": LOGOS["wamu"], "jpmc": LOGOS["jpmc"]}
BILL = ST("bill100", path=f"{P_IMG}/10_Supporting_Illustrative/06_ILLUSTRATIVE_US_100_note_classic.jpg", edge=1920)
CHI_TOWER = ST("chi_tower", path=f"{P_IMG}/06_Bank_One_Chicago/02_Chase_Tower_Chicago_looking_NE.jpg", edge=1920)
CARDS_04 = [ST(f"c04_{k}", key=key, t=t, frame=FRAME_OF.get(key, "FULL"), size=[640, 360]) for k, (key, t) in enumerate([
    ("HOW", 656.8), ("UNT", 1055.8), ("HOW", 697.2), ("MPB", 1560.0), ("HOW", 692.8)])]


# ================================================================================================
# Gradings (data-color-grading payloads)
# ================================================================================================
BASE = json.load(open(f"{PRJ}/tools/base_grade.json"))


def grade(adjust=None, details=None, effects=None, intensity=1, preset=None):
    g = json.loads(json.dumps(BASE))
    g["preset"], g["intensity"] = preset, intensity
    for sec, vals in (("adjust", adjust), ("details", details), ("effects", effects)):
        for k, v in (vals or {}).items():
            g[sec][k] = v
    return g


DOC_A = dict(contrast=0.16, highlights=-0.16, shadows=-0.02, blacks=0.03, saturation=-0.2, temperature=0.05)
DOC_D = dict(vignette=0.34, grain=0.12)
DOC_E = dict(scanlines=0.08, scanlineCount=0.17, scanlineSoftness=1, chromaticAberration=0.03, chromaticAngle=0)
GR = {
    "doc": grade(DOC_A, DOC_D, DOC_E),
    "warm": grade(dict(DOC_A, temperature=0.16, saturation=-0.08), DOC_D, DOC_E),
    "teal": grade(dict(DOC_A, temperature=-0.16, tint=-0.04, saturation=-0.32, exposure=-0.06), DOC_D, DOC_E),
    "bw": grade(dict(DOC_A, saturation=-1, contrast=0.22), dict(vignette=0.38, grain=0.18), DOC_E),
    "crt": grade(dict(DOC_A, contrast=0.12), dict(vignette=0.32, grain=0.14),
                 dict(DOC_E, crtCurvature=0.2, scanlines=0.36, scanlineCount=0.17, chromaticAberration=0.08)),
    "gold": grade(dict(DOC_A, temperature=0.32, tint=0.05, saturation=-0.1, exposure=0.04),
                  dict(vignette=0.38, grain=0.14), dict(DOC_E, bloom=0.7, bloomRadius=10)),
    "glitch": grade(DOC_A, dict(vignette=0.3, grain=0.2), dict(DOC_E, digitalGlitch=0.85, digitalGlitchColorSplit=0.65,
                    digitalGlitchLineTear=0.6, digitalGlitchPixelate=0.2, digitalGlitchBlockAmount=0.6,
                    digitalGlitchBlockDisplacement=0.5, digitalGlitchSpeed=0.6)),
    "dirty": grade(dict(DOC_A, saturation=-0.75, contrast=-0.1, exposure=-0.14), dict(vignette=0.48, grain=0.55),
                   dict(DOC_E, chromaBleed=0.5, scanlines=0.32)),
    "blurbg": grade(dict(DOC_A, exposure=-0.7, saturation=-0.4), dict(vignette=0.5, grain=0.1), dict(blur=0.85)),
    "halftone": grade(dict(contrast=0.06), dict(vignette=0.2), dict(halftone=0.95, halftoneSize=0.34)),
    "twoink": grade(dict(contrast=0.08), dict(vignette=0.15), dict(twoInkPrint=1, twoInkPrintSize=0.42)),
    "mono": grade(dict(contrast=0.1), dict(vignette=0.2), dict(monoScreen=1, monoScreenSize=0.35, monoScreenAngle=0.25,
                  monoScreenSpread=0.3)),
    "dither": grade(dict(contrast=0.1), dict(vignette=0.2), dict(dither=1, ditherSize=0.5)),
    "print": grade(dict(DOC_A, saturation=-1, contrast=0.25), dict(vignette=0.3, grain=0.2), dict(halftone=0.6, halftoneSize=0.22)),
}
os.makedirs(f"{PRJ}/tools", exist_ok=True)


def gattr(name):
    return f' data-color-grading="{esc(json.dumps(GR[name], separators=(",", ":")))}"' if name else ""


# ================================================================================================
# Type: fonts, glow, measurement
# ================================================================================================
FONTS_CSS = """
  @font-face { font-family: 'Satoshi'; src: url('assets/fonts/Satoshi-Medium.woff2') format('woff2'); font-weight: 500; font-style: normal; }
  @font-face { font-family: 'Satoshi'; src: url('assets/fonts/Satoshi-Bold.woff2') format('woff2'); font-weight: 700; font-style: normal; }
  @font-face { font-family: 'Satoshi'; src: url('assets/fonts/Satoshi-Black.woff2') format('woff2'); font-weight: 900; font-style: normal; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Regular.woff2') format('woff2'); font-weight: 400; font-style: normal; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Italic.woff2') format('woff2'); font-weight: 400; font-style: italic; }
"""
INK = "#FBF8EC"
# the Pattinson glow (from its build_v5.py): sans glow-in, serif halo, bloom frame, soft frame
GLOW_REST = "0 0 12px rgba(255,255,255,0.55), 0 0 34px rgba(255,255,255,0.22), 0 3px 10px rgba(0,0,0,0.42)"
GLOW_BLOOM = "0 0 34px rgba(255,255,255,0.95), 0 0 90px rgba(255,255,255,0.55), 0 3px 10px rgba(0,0,0,0)"
SERIF_REST = ("0 0 14px rgba(255,255,255,0.62), 0 0 42px rgba(255,255,255,0.30), 0 0 90px rgba(255,255,255,0.12), "
              "0 3px 10px rgba(0,0,0,0.35)")
SERIF_BLOOM = ("0 0 22px rgba(255,255,255,1), 0 0 60px rgba(255,255,255,0.95), 0 0 130px rgba(255,255,255,0.7), "
               "0 3px 10px rgba(0,0,0,0)")
SERIF_SOFT = ("0 0 18px rgba(255,255,255,0.85), 0 0 50px rgba(255,255,255,0.45), 0 0 100px rgba(255,255,255,0.18), "
              "0 3px 10px rgba(0,0,0,0.2)")
GOLD_REST = ("0 0 14px rgba(255,214,140,0.75), 0 0 44px rgba(255,190,90,0.38), 0 0 100px rgba(255,170,60,0.16), "
             "0 3px 10px rgba(0,0,0,0.35)")
_FONTS = {}


def _font(family, weight, italic):
    name = {("Satoshi", 500): "Satoshi-Medium", ("Satoshi", 600): "Satoshi-Bold", ("Satoshi", 700): "Satoshi-Bold",
            ("Satoshi", 800): "Satoshi-Black", ("Satoshi", 900): "Satoshi-Black"}.get((family, weight))
    if family == "Instrument Serif":
        name = "InstrumentSerif-Italic" if italic else "InstrumentSerif-Regular"
    if name not in _FONTS:
        f = TTFont(f"{PRJ}/assets/fonts/{name}.woff2")
        _FONTS[name] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _FONTS[name]


def textw(text, family, weight, size, italic=False, track=0.0):
    cmap, hmtx, upm = _font(family, weight, italic)
    w = 0
    for ch in text:
        g = cmap.get(ord(ch))
        w += hmtx[g][0] if g in hmtx else upm * 0.5
    return w * size / upm + track * size * len(text)


# ================================================================================================
# Scenes
# ================================================================================================
SCENES = []


class Scene:
    def __init__(self, sid, start, end, ground="#070707"):
        self.sid, self.start, self.end, self.ground = sid, round(start, 3), round(end, 3), ground
        self.els, self.js, self.n, self.z = [], [], 0, 10
        SCENES.append(self)

    @property
    def dur(self):
        return round(self.end - self.start, 3)

    def L(self, t):
        return round(t - self.start, 3)

    def uid(self, p):
        self.n += 1
        return f"{self.sid}-{p}{self.n}"

    def nz(self, step=1):
        self.z += step
        return self.z

    def timed(self, t0, t1):
        t0, t1 = max(t0, self.start), min(t1, self.end)
        return f'data-start="{r3(self.L(t0))}" data-duration="{r3(max(t1 - t0, F1))}"'

    def at(self, t):
        return r3(self.L(t))

    def J(self, s):
        self.js.append(s)

    # ---- media ----------------------------------------------------------------------------------
    def v(self, key, src_t, t0, t1, rate=None, grade="doc", push=(1.0, 1.02), box=None, z=None, frame=None,
          cam_style="", origin="50% 50%", xyz=None, vstyle="", size=None):
        """A video shot cut from source `key` at `src_t`, shown over [t0, t1)."""
        rate_v = rate or 1.0
        cid = CL(key, src_t, (t1 - t0) * rate_v, frame=frame, xyz=xyz, size=size)
        cam, vid = self.uid("cam"), self.uid("v")
        z = z or self.nz()
        x, y, w, h = box or (0, 0, 1920, 1080)
        ra = f' data-playback-rate="{rate}"' if rate else ""
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};'
            f'transform-origin:{origin};{cam_style}"><video id="{vid}" class="clip" src="assets/clips2/{cid}.mp4" muted '
            f'playsinline {self.timed(t0, t1)} data-hf-media-start-basis="local" data-media-start="0"{ra}{gattr(grade)} '
            f'data-track-index="2" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:cover;'
            f'{vstyle}"></video></div>')
        if push:
            self.J(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {r3(t1 - t0)}, '
                   f'ease: "none" }}, {self.at(t0)});')
        return cam, vid

    def vert(self, key, src_t, t0, t1, grade="doc", push=(1.0, 1.03), w=608, x=None, bg=True, xyz=None):
        """A vertical source: the clip centred as a 9:16 panel over a blurred, darkened fill of itself."""
        if bg:
            self.v(key, src_t, t0, t1, grade="blurbg", push=(1.25, 1.3), box=(0, 0, 1920, 1080), xyz=xyz)
        xx = (1920 - w) // 2 if x is None else x
        return self.v(key, src_t, t0, t1, grade=grade, push=push, box=(xx, 0, w, 1080), xyz=xyz)

    def img(self, src, t0, t1, grade="doc", push=(1.0, 1.02), box=None, pos="center", fit="cover", z=None,
            cam_style="", istyle="", origin="50% 50%"):
        cam, im = self.uid("cam"), self.uid("i")
        z = z or self.nz()
        x, y, w, h = box or (0, 0, 1920, 1080)
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};'
            f'transform-origin:{origin};{cam_style}"><img id="{im}" class="clip" src="assets/img2/{src}" alt="" '
            f'{self.timed(t0, t1)}{gattr(grade)} data-track-index="3" style="position:absolute;left:0;top:0;width:{w}px;'
            f'height:{h}px;object-fit:{fit};object-position:{pos};{istyle}" /></div>')
        if push:
            self.J(f'tl.fromTo("#{cam}", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {r3(t1 - t0)}, '
                   f'ease: "none" }}, {self.at(t0)});')
        return cam, im

    def black(self, t0, t1, color="#070707", tex=True, z=None):
        sid = self.uid("bk")
        t = '<img class="bktex" src="assets/tex/ht_grunge.jpg" alt="" />' if tex else ""
        self.els.append(f'<div id="{sid}" class="clip solid" {self.timed(t0, t1)} data-track-index="1" '
                        f'style="background:{color};z-index:{z or self.nz()}">{t}</div>')
        return sid

    def paper(self, t0, t1, z=None):
        pid = self.uid("paper")
        self.els.append(f'<img id="{pid}" class="clip paper" src="assets/tex/paper_light.png" alt="" {self.timed(t0, t1)} '
                        f'data-track-index="1" style="z-index:{z or self.nz()}" />')
        return pid

    def raw(self, el, js=()):
        self.els.append(el)
        self.js.extend(js)

    # ---- cuts and flashes --------------------------------------------------------------------------
    def neg(self, t, frames=2):
        nid = self.uid("neg")
        self.els.append(f'<div id="{nid}" class="clip neg" {self.timed(t, t + frames * F1)} data-track-index="6" '
                        f'style="z-index:{self.nz() + 800}"></div>')

    def flash(self, t, d=0.2, peak=0.95):
        fid = self.uid("wf")
        self.els.append(f'<div id="{fid}" class="clip flashw" {self.timed(t - 0.05, t + d)} data-track-index="6" '
                        f'style="z-index:{self.nz() + 800}"></div>')
        self.J(f'tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: {peak}, duration: 0.05, ease: "power4.in", '
               f'immediateRender: false }}, {self.at(t - 0.05)});')
        self.J(f'tl.to("#{fid}", {{ opacity: 0, duration: {r3(d - 0.01)}, ease: "power2.out" }}, {self.at(t)});')

    def whiteframe(self, t, frames=1):
        fid = self.uid("wfr")
        self.els.append(f'<div id="{fid}" class="clip solid" {self.timed(t, t + frames * F1)} data-track-index="6" '
                        f'style="background:#FFFDF6;z-index:{self.nz() + 800}"></div>')

    def streak(self, t, frames=4, y=540, h=170):
        lid = self.uid("streak")
        self.els.append(f'<div id="{lid}" class="clip streak" {self.timed(t, t + frames * F1)} data-track-index="6" '
                        f'style="top:{y - h // 2}px;height:{h}px;z-index:{self.nz() + 800}"></div>')
        self.J(f'tl.fromTo("#{lid}", {{ scaleX: 0.25, opacity: 1 }}, {{ scaleX: 1.6, opacity: 0.0, duration: {r3(frames * F1)}, '
               f'ease: "power2.in", immediateRender: false }}, {self.at(t)});')

    def punch(self, cam, t, scale, origin=None):
        """A hard punch-in at t (a one-frame set, no ease)."""
        if origin:
            self.J(f'tl.set("#{cam}", {{ transformOrigin: "{origin}" }}, {self.at(t)});')
        self.J(f'tl.set("#{cam}", {{ scale: {scale} }}, {self.at(t)});')

    def write(self):
        css = f"""
  {FONTS_CSS}
  #root {{ position: absolute; inset: 0; overflow: hidden; background: {self.ground}; }}
  #root .cam {{ position: absolute; overflow: hidden; }}
  #root .grp {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .solid {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: hidden; }}
  #root .bktex {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover;
    mix-blend-mode: screen; opacity: 0.10; }}
  #root .paper {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; }}
  #root .neg {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #ffffff;
    mix-blend-mode: difference; }}
  #root .flashw {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #FFFDF6; opacity: 0; }}
  #root .streak {{ position: absolute; left: 0; width: 1920px; background: linear-gradient(180deg, rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.85) 38%, #ffffff 50%, rgba(255,255,255,0.85) 62%, rgba(255,255,255,0) 100%);
    box-shadow: 0 0 80px 30px rgba(255,255,255,0.55); transform-origin: 50% 50%; }}
  #root .t {{ position: absolute; white-space: nowrap; line-height: 1; }}
  #root .card {{ position: absolute; overflow: hidden; box-shadow: 0 26px 60px rgba(0,0,0,0.55), 0 4px 12px rgba(0,0,0,0.35); }}
  #root .wcard {{ border: 7px solid #F4EFE6; }}
  #root .hl {{ position: absolute; background: #E5381B; mix-blend-mode: multiply; transform-origin: 0% 50%; }}
  #root .tex {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; pointer-events: none; }}
"""
        tex = (f'<img id="{self.sid}-tx1" class="clip tex" src="assets/tex/ht_grunge.jpg" alt="" data-start="0" '
               f'data-duration="{r3(self.dur)}" data-track-index="9" data-layout-ignore '
               f'style="mix-blend-mode:overlay;opacity:0.40;z-index:2000" />'
               f'<img id="{self.sid}-tx2" class="clip tex" src="assets/tex/ht_paper.jpg" alt="" data-start="0" '
               f'data-duration="{r3(self.dur)}" data-track-index="9" data-layout-ignore '
               f'style="mix-blend-mode:soft-light;opacity:0.28;z-index:2001" />')
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


def seq(shots, end):
    """[(t0, args...)] -> [(t0, t1, args...)] laid end to end."""
    return [(s[0], (shots[k + 1][0] if k + 1 < len(shots) else end)) + tuple(s[1:]) for k, s in enumerate(shots)]


def montage(sc, shots, end, grade="doc"):
    """shots: (t0, key, src_t[, opts]) -> straight cuts."""
    out = []
    for t0, t1, *rest in seq(shots, end):
        key, src_t = rest[0], rest[1]
        o = rest[2] if len(rest) > 2 else {}
        if key in VERT and not o.get("full"):
            out.append(sc.vert(key, src_t, t0, t1, grade=o.get("grade", grade), push=o.get("push", (1.0, 1.03)),
                               xyz=o.get("xyz")))
        else:
            out.append(sc.v(key, src_t, t0, t1, grade=o.get("grade", grade), push=o.get("push", (1.0, 1.025)),
                            rate=o.get("rate"), frame=o.get("frame"), xyz=o.get("xyz")))
    return out


# ================================================================================================
# Set pieces
# ================================================================================================
def sp_mask_word(sc, t0, t1, word, key, src_t, size=780, zoom_at=None):
    """Footage seen through a giant word (multiply knock-out), then the camera dives through a letter."""
    sc.v(key, src_t, t0, t1, grade="doc", push=(1.0, 1.08))
    mid = sc.uid("mask")
    w = textw(word, "Satoshi", 900, size, track=-0.04)
    # dive point: the middle of the first letter's stem
    ox = 960 - w / 2 + size * 0.14
    sc.raw(f'<div id="{mid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'style="background:#000;mix-blend-mode:multiply;z-index:{sc.nz()}"><div id="{mid}-t" class="t" '
           f'style="left:0;width:1920px;top:{540 - size * 0.53:.0f}px;text-align:center;font-family:Satoshi;font-weight:900;'
           f'font-size:{size}px;letter-spacing:-0.04em;color:#fff;transform-origin:{ox:.0f}px {size * 0.55:.0f}px">'
           f'{esc(word)}</div></div>',
           [f'tl.fromTo("#{mid}-t", {{ scale: 1.12, opacity: 0.0 }}, {{ scale: 1.0, opacity: 1, duration: 0.22, ease: "expo.out", '
            f'immediateRender: false }}, {sc.at(t0)});'])
    za = zoom_at or (t1 - 0.32)
    sc.J(f'tl.to("#{mid}-t", {{ scale: 16, duration: {r3(t1 - za)}, ease: "power3.in" }}, {sc.at(za)});')


def sp_echo(sc, t0, t1, word, size=150, echo=560, inv=True, ground="#060606"):
    """Dario's SUDDENLY: one inverted frame, then the word small and sharp with a giant blurred echo above and below."""
    eid = sc.uid("echo")
    sc.raw(f'<div id="{eid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'data-layout-allow-overlap style="background:{ground};z-index:{sc.nz()}">'
           f'<img class="bktex" src="assets/tex/ht_grunge.jpg" alt="" />'
           f'<div id="{eid}-a" class="t" style="left:-200px;width:2320px;top:{-echo * 0.62:.0f}px;text-align:center;'
           f'font-family:\'Instrument Serif\';font-size:{echo}px;color:rgba(251,248,236,0.20);filter:blur(9px);'
           f'letter-spacing:0.02em">{esc(word.upper())}</div>'
           f'<div id="{eid}-b" class="t" style="left:-200px;width:2320px;top:{1080 - echo * 0.36:.0f}px;text-align:center;'
           f'font-family:\'Instrument Serif\';font-size:{echo}px;color:rgba(251,248,236,0.16);filter:blur(12px);'
           f'letter-spacing:0.02em">{esc(word.upper())}</div>'
           f'<div id="{eid}-w" class="t" style="left:0;width:1920px;top:{540 - size * 0.55:.0f}px;text-align:center;'
           f'font-family:\'Instrument Serif\';font-size:{size}px;color:{INK};letter-spacing:0.06em;'
           f'text-shadow:{SERIF_REST}">{esc(word.upper())}</div></div>',
           [f'tl.fromTo("#{eid}-a", {{ x: -60 }}, {{ x: 60, duration: {r3(t1 - t0)}, ease: "none" }}, {sc.at(t0)});',
            f'tl.fromTo("#{eid}-b", {{ x: 70 }}, {{ x: -70, duration: {r3(t1 - t0)}, ease: "none" }}, {sc.at(t0)});',
            f'tl.fromTo("#{eid}-w", {{ opacity: 0, filter: "blur(12px)", textShadow: "{SERIF_BLOOM}" }}, '
            f'{{ opacity: 1, filter: "blur(0px)", textShadow: "{SERIF_REST}", duration: 0.16, ease: "expo.out", '
            f'immediateRender: false }}, {sc.at(t0 + F1)});'])
    if inv:  # the inverted first frame: a white panel with the word in black
        iid = sc.uid("inv")
        sc.raw(f'<div id="{iid}" class="clip grp" {sc.timed(t0, t0 + F1)} data-track-index="5" '
               f'style="background:#F7F3EA;z-index:{sc.nz() + 1}"><div class="t" style="left:0;width:1920px;'
               f'top:{540 - size * 0.55:.0f}px;text-align:center;font-family:\'Instrument Serif\';font-size:{size}px;'
               f'color:#0A0A0A;letter-spacing:0.06em">{esc(word.upper())}</div></div>')


def sp_seal_ring(sc, t0, t1, photos, glint_at, white_at, photo_step=3, cy=540, D=760):
    """Fink's cold open: the presidential seal grows out of the dark while the portraits inside its ring swap every
    few frames; a glint grows at its centre and its rays burn the frame white."""
    sc.black(t0, t1, color="#040506")
    gid = sc.uid("ring")
    stars = "".join(f'<circle cx="{(k * 733) % 1920}" cy="{(k * 397) % 1080}" r="{1 + (k * 7) % 3 * 0.6:.1f}" '
                    f'fill="#fff" opacity="{0.25 + (k * 13) % 7 / 10:.2f}" />' for k in range(140))
    sc.raw(f'<svg id="{gid}" class="clip" {sc.timed(t0, t1)} data-track-index="2" width="1920" height="1080" '
           f'style="position:absolute;left:0;top:0;z-index:{sc.nz()}">{stars}</svg>')
    sc.raw(f'<div id="{gid}-cam" class="grp" style="z-index:{sc.nz()};transform-origin:960px {cy}px">'
           f'<img id="{gid}-seal" class="clip" src="assets/img2/{SEAL}" alt="" {sc.timed(t0, t1)} data-track-index="3" '
           f'style="position:absolute;left:{960 - D // 2}px;top:{cy - D // 2}px;width:{D}px;height:{D}px" /></div>',
           [f'tl.fromTo("#{gid}-cam", {{ scale: 0.3 }}, {{ scale: 1.0, duration: 1.1, ease: "expo.out" }}, {sc.at(t0)});',
            f'tl.to("#{gid}-cam", {{ scale: 1.08, duration: {r3(t1 - t0 - 1.1)}, ease: "none" }}, {sc.at(t0 + 1.1)});'])
    # the portraits inside the inner field, swapping every few frames until the eagle shows
    R = int(D * 0.33)
    t = t0
    k = 0
    swap_end = glint_at - 0.25
    while t < swap_end - 1e-6:
        te = min(swap_end, t + photo_step * F1)
        pid = sc.uid("rp")
        sc.raw(f'<div class="grp" style="z-index:{sc.nz()};transform-origin:960px {cy}px" id="{pid}-c">'
               f'<img id="{pid}" class="clip" src="assets/img2/{photos[k % len(photos)]}" alt="" {sc.timed(t, te)} '
               f'data-track-index="3"{gattr("bw" if k % 3 == 1 else "doc")} style="position:absolute;left:{960 - R}px;'
               f'top:{cy - R}px;width:{2 * R}px;height:{2 * R}px;object-fit:cover;border-radius:50%" /></div>',
               [f'tl.fromTo("#{pid}-c", {{ scale: {0.3 + 0.7 * min(1, (t - t0) / 1.1) ** 0.4:.3f} }}, '
                f'{{ scale: {0.3 + 0.7 * min(1, (te - t0) / 1.1) ** 0.4:.3f}, duration: {r3(te - t)}, ease: "none" }}, {sc.at(t)});'])
        t, k = te, k + 1
    # glint and rays
    gl = sc.uid("glint")
    sc.raw(f'<div id="{gl}" class="clip grp" {sc.timed(glint_at, white_at + 0.1)} data-track-index="5" '
           f'style="z-index:{sc.nz()}"><div id="{gl}-h" style="position:absolute;left:0;top:{cy - 6}px;width:1920px;height:12px;'
           f'background:linear-gradient(90deg,rgba(255,255,255,0),#fff 50%,rgba(255,255,255,0));transform-origin:50% 50%"></div>'
           f'<div id="{gl}-v" style="position:absolute;left:954px;top:0;width:12px;height:1080px;background:linear-gradient('
           f'180deg,rgba(255,255,255,0),#fff 50%,rgba(255,255,255,0));transform-origin:50% 50%"></div>'
           f'<div id="{gl}-r" style="position:absolute;left:460px;top:{cy - 500}px;width:1000px;height:1000px;border-radius:50%;'
           f'background:radial-gradient(closest-side,#fff 0%,rgba(255,255,255,0.9) 35%,rgba(255,255,255,0) 100%)"></div></div>',
           [f'tl.fromTo("#{gl}-h", {{ scaleX: 0.02 }}, {{ scaleX: 1, duration: {r3(white_at - glint_at)}, ease: "power2.in", '
            f'immediateRender: false }}, {sc.at(glint_at)});',
            f'tl.fromTo("#{gl}-v", {{ scaleY: 0.02 }}, {{ scaleY: 0.8, duration: {r3(white_at - glint_at)}, ease: "power2.in", '
            f'immediateRender: false }}, {sc.at(glint_at)});',
            f'tl.fromTo("#{gl}-r", {{ scale: 0.05, opacity: 0.7 }}, {{ scale: 3.2, opacity: 1, duration: {r3(white_at - glint_at)}, '
            f'ease: "power3.in", immediateRender: false }}, {sc.at(glint_at)});'])
    # HUD wireframes flickering around the seal
    hud = sc.uid("hud")
    sq = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#fff" stroke-width="1.5" opacity="0.7" />'
                 for x, y, w, h in [(250, 180, 120, 120), (1540, 760, 150, 150), (1480, 150, 70, 70), (330, 770, 90, 90)])
    lines = ('<line x1="370" y1="240" x2="700" y2="420" stroke="#fff" stroke-width="1" opacity="0.6" />'
             '<line x1="1540" y1="835" x2="1240" y2="660" stroke="#fff" stroke-width="1" opacity="0.6" />'
             '<text x="252" y="170" fill="#fff" font-size="14" font-family="Satoshi" opacity="0.8">675.800.FFA</text>'
             '<text x="1542" y="750" fill="#fff" font-size="14" font-family="Satoshi" opacity="0.8">0X2A.JPM</text>')
    for a, b in ((t0, t0 + 3 * F1), (t0 + 6 * F1, t0 + 8 * F1), (t0 + 14 * F1, t0 + 15 * F1), (glint_at - 4 * F1, glint_at - 2 * F1)):
        hid = sc.uid("hud")
        sc.raw(f'<svg id="{hid}" class="clip" {sc.timed(a, b)} data-track-index="5" width="1920" height="1080" '
               f'style="position:absolute;left:0;top:0;z-index:{sc.nz()}">{sq}{lines}</svg>')
    sc.whiteframe(white_at, 2)


def sp_seal_portrait(sc, t0, t1, cutout, punch_at, punch=1.55):
    """This man: the cut-out in front of the seal, then a hard punch-in to his face."""
    cam = sc.uid("sp")
    sc.raw(f'<div id="{cam}" class="grp" style="z-index:{sc.nz()};transform-origin:1010px 360px">'
           f'<div id="{cam}-bg" class="clip grp" {sc.timed(t0, t1)} data-track-index="1" style="background:radial-gradient('
           f'ellipse at 50% 42%, #1b2a3a 0%, #0b121b 55%, #05080c 100%)"><img class="bktex" src="assets/tex/ht_grunge.jpg" alt="" /></div>'
           f'<img id="{cam}-seal" class="clip" src="assets/img2/{SEAL}" alt="" {sc.timed(t0, t1)} data-track-index="3" '
           f'style="position:absolute;left:{960 - 470}px;top:{500 - 470}px;width:940px;height:940px;opacity:0.85" />'
           f'<img id="{cam}-cut" class="clip" src="assets/img2/{cutout}" alt="" {sc.timed(t0, t1)} data-track-index="3"'
           f'{gattr("doc")} style="position:absolute;left:{960 - 480}px;top:150px;width:960px;height:1360px;object-fit:contain;'
           f'object-position:50% 0%" /></div>',
           [f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.03, duration: {r3(punch_at - t0)}, ease: "none" }}, {sc.at(t0)});',
            f'tl.set("#{cam}", {{ scale: {punch} }}, {sc.at(punch_at)});',
            f'tl.to("#{cam}", {{ scale: {punch + 0.04}, duration: {r3(t1 - punch_at)}, ease: "none" }}, {sc.at(punch_at)});'])
    sc.neg(t0, 2)
    sc.neg(t0 + 3 * F1, 1)


def sp_face_boxes(sc, t0, t1, boxes):
    """Fink's face-detection boxes on the Wolf: thin purple frames with a 'person' tag, flickering on."""
    for k, (x, y, w, h, label) in enumerate(boxes):
        bid = sc.uid("fb")
        on = t0 + (2 + k * 3) * F1
        sc.raw(f'<div id="{bid}" class="clip" {sc.timed(on, t1)} data-track-index="5" style="position:absolute;'
               f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:3px solid #B455FF;box-shadow:0 0 12px rgba(180,85,255,0.7);'
               f'z-index:{sc.nz() + 300}"><div style="position:absolute;left:-3px;top:-34px;padding:4px 10px;background:#B455FF;'
               f'font-family:Satoshi;font-weight:700;font-size:20px;color:#fff;white-space:nowrap">{label}</div></div>',
               [f'tl.set("#{bid}", {{ opacity: 0 }}, {sc.at(on + F1)});', f'tl.set("#{bid}", {{ opacity: 1 }}, {sc.at(on + 2 * F1)});'])


def sp_nyt(sc, t0, t1, hl1_at, hl1_end, reframe_at, hl2_at, hl2_end):
    """AMD's headline sweep on the real 1998 clipping: red marker under 'Heir Apparent', then a jump down to the body
    text 'the world's largest financial services company'."""
    cam = sc.uid("nyt")
    rot = 1.1
    hl = [  # x, y, w, h (in the 1920x1080 still)
        (1032, 88, 715, 118, hl1_at, hl1_end),   # Heir Apparent
        (288, 300, 492, 52, hl2_at, hl2_at + (hl2_end - hl2_at) * 0.55),   # the world's largest financial
        (72, 350, 372, 50, hl2_at + (hl2_end - hl2_at) * 0.55, hl2_end),   # services company,
    ]
    rects = "".join(f'<div id="{cam}-h{k}" class="hl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'
                    for k, (x, y, w, h, a, b) in enumerate(hl))
    for k in range(len(hl)):
        sc.J(f'tl.set("#{cam}-h{k}", {{ scaleX: 0, rotation: {rot if k == 0 else 0.6} }}, 0);')
    sc.raw(f'<div id="{cam}" class="grp" style="z-index:{sc.nz()};transform-origin:1180px 150px">'
           f'<img id="{cam}-i" class="clip" src="assets/img2/{NYT}" alt="" {sc.timed(t0, t1)} data-track-index="3"'
           f'{gattr("bw")} style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover" />'
           f'{rects}<div id="{cam}-cur" style="position:absolute;left:0;top:0;width:16px;height:96px;background:#E5381B;opacity:0"></div></div>')
    sc.J(f'tl.fromTo("#{cam}", {{ scale: 1.25 }}, {{ scale: 1.32, duration: {r3(reframe_at - t0)}, ease: "none" }}, {sc.at(t0)});')
    for k, (x, y, w, h, a, b) in enumerate(hl):
        sc.J(f'tl.fromTo("#{cam}-h{k}", {{ scaleX: 0, rotation: {rot if k == 0 else 0.6} }}, {{ scaleX: 1, rotation: {rot if k == 0 else 0.6}, '
             f'duration: {r3(b - a)}, ease: "power1.inOut", immediateRender: false }}, {sc.at(a)});')
    # the cursor rides the first sweep's front edge, then blinks
    x, y, w, h, a, b = hl[0]
    sc.J(f'tl.set("#{cam}-cur", {{ opacity: 1 }}, {sc.at(a)});')
    sc.J(f'tl.fromTo("#{cam}-cur", {{ x: {x}, y: {y + 8} }}, {{ x: {x + w}, y: {y + 8 + w * math.tan(math.radians(rot)):.0f}, '
         f'duration: {r3(b - a)}, ease: "power1.inOut", immediateRender: false }}, {sc.at(a)});')
    for k in range(4):
        sc.J(f'tl.set("#{cam}-cur", {{ opacity: {0 if k % 2 == 0 else 1} }}, {sc.at(b + 0.12 * (k + 1))});')
    # jump-reframe down to the body text
    sc.J(f'tl.set("#{cam}", {{ transformOrigin: "420px 330px", scale: 1.85 }}, {sc.at(reframe_at)});')
    sc.J(f'tl.to("#{cam}", {{ scale: 1.95, duration: {r3(t1 - reframe_at)}, ease: "none" }}, {sc.at(reframe_at)});')


def sp_grid4(sc, t0, t1, cells, step=4):
    """Fink's 2x2 grid: four clips fill their quadrants one by one, each with a one-frame flash."""
    sc.black(t0, t1, color="#050505", tex=False)
    g = 8
    for k, (key, src_t) in enumerate(cells):
        r, c = divmod(k, 2)
        on = t0 + k * step * F1
        box = (c * (960 + g // 2), r * (540 + g // 2), 960 - g // 2, 540 - g // 2)
        if key in VERT:
            sc.v(key, src_t, on, t1, grade="doc", push=(1.0, 1.04), box=box)
        else:
            sc.v(key, src_t, on, t1, grade="doc", push=(1.0, 1.04), box=box, frame=FRAME_OF.get(key, "FULL"))
        fid = sc.uid("gf")
        sc.raw(f'<div id="{fid}" class="clip" {sc.timed(on, on + F1)} data-track-index="5" style="position:absolute;'
               f'left:{box[0]}px;top:{box[1]}px;width:{box[2]}px;height:{box[3]}px;background:#fff;z-index:{sc.nz() + 200}"></div>')


def sp_name_card(sc, t0, t1, cutout, small_at, name_at, small="Meet", name="Jamie Dimon"):
    """Fink's name card: a cut-out on a coloured card settles on paper; the name decodes letter by letter under it,
    with a giant pale outline echo of the name behind everything."""
    sc.paper(t0, t1)
    nid = sc.uid("nc")
    cw, ch = 560, 700
    cx, cy = 960, 470
    letters = list(name)
    rnd = random.Random(7)
    order = [i for i, ch_ in enumerate(letters) if ch_ != " "]
    rnd.shuffle(order)
    spans = "".join(f'<span id="{nid}-l{i}" style="opacity:0;color:#C9C3B8">{esc(ch_) if ch_ != " " else "&nbsp;"}</span>'
                    for i, ch_ in enumerate(letters))
    sc.raw(f'<div id="{nid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'data-layout-allow-overlap style="z-index:{sc.nz()}">'
           f'<div class="t" style="left:-120px;width:2160px;top:300px;text-align:center;font-family:Satoshi;font-weight:900;'
           f'font-size:330px;letter-spacing:-0.04em;color:transparent;-webkit-text-stroke:2.5px rgba(20,16,12,0.11)">'
           f'{esc(name.upper())}</div>'
           f'<div id="{nid}-card" class="card" style="left:{cx - cw // 2}px;top:{cy - ch // 2}px;width:{cw}px;height:{ch}px;'
           f'background:radial-gradient(ellipse at 50% 30%, #2b4f7a 0%, #12263f 60%, #0a1626 100%)">'
           f'<img id="{nid}-cut" src="assets/img2/{cutout}" alt=""{gattr("bw")} style="position:absolute;left:-40px;top:70px;'
           f'width:{cw + 80}px;height:{ch + 60}px;object-fit:cover;object-position:50% 0%" /></div>'
           f'<div id="{nid}-s" class="t" style="left:{cx - cw // 2}px;top:{cy - ch // 2 - 64}px;font-family:Satoshi;'
           f'font-weight:700;font-size:48px;color:#141210;opacity:0">{esc(small)}</div>'
           f'<div class="t" style="left:{cx - 760}px;width:{760 + cw // 2}px;top:{cy + ch // 2 + 26}px;text-align:right;'
           f'font-family:Satoshi;font-weight:900;font-size:118px;letter-spacing:-0.035em">{spans}</div></div>',
           [f'tl.fromTo("#{nid}-card", {{ scale: 1.65 }}, {{ scale: 1.0, duration: 0.36, ease: "power3.out", immediateRender: false }}, '
            f'{sc.at(t0)});',
            f'tl.fromTo("#{nid}-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, immediateRender: false }}, {sc.at(small_at)});'])
    for j, i in enumerate(order):
        a = name_at + j * 0.035
        sc.J(f'tl.set("#{nid}-l{i}", {{ opacity: 1, color: "#D9D3C8" }}, {sc.at(a)});')
        sc.J(f'tl.set("#{nid}-l{i}", {{ color: "#8E877C" }}, {sc.at(a + 3 * F1)});')
        sc.J(f'tl.set("#{nid}-l{i}", {{ color: "#141210" }}, {sc.at(a + 6 * F1)});')


def sp_gleam(sc, t0, t1, z=None):
    """A gold light sweep across the frame (screen blend)."""
    gid = sc.uid("gleam")
    sc.raw(f'<div id="{gid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" style="z-index:{z or sc.nz() + 100};'
           f'mix-blend-mode:screen;background:linear-gradient(105deg, rgba(255,200,110,0) 30%, rgba(255,222,160,0.75) 46%, '
           f'rgba(255,245,220,0.9) 50%, rgba(255,222,160,0.75) 54%, rgba(255,200,110,0) 70%);background-size:260% 100%"></div>',
           [f'tl.fromTo("#{gid}", {{ backgroundPosition: "110% 0%" }}, {{ backgroundPosition: "-10% 0%", duration: {r3(t1 - t0)}, '
            f'ease: "power2.inOut", immediateRender: false }}, {sc.at(t0)});'])


def sp_roller(sc, t0, t1, years, land_at, cards, label=None, label_at=None, ground="#07090b", size=330, video_bg=None,
              invert_digits=2):
    """Dario's 2023: a glowing year counter rolls (fast, then slowing) to land on the beat, with photo cards drifting
    in the dark around it."""
    if video_bg:
        sc.v(video_bg[0], video_bg[1], t0, t1, grade="teal", push=(1.0, 1.06))
        sc.black(t0, t1, color="rgba(4,6,8,0.62)", tex=True)
    else:
        sc.black(t0, t1, color=ground)
    rnd = random.Random(len(years) * 31 + int(t0 * 10))
    slots = [(210, 170, 0.95), (1450, 150, 0.85), (300, 760, 0.8), (1530, 720, 1.0), (760, 100, 0.6), (1180, 860, 0.7),
             (60, 460, 0.55), (1760, 430, 0.6)]
    for k, src in enumerate(cards[:len(slots)]):
        x, y, s = slots[k]
        w, h = int(450 * s), int(253 * s)
        cid = sc.uid("fc")
        on = t0 + k * 2 * F1
        sc.raw(f'<div id="{cid}" class="grp" style="z-index:{sc.nz()}"><img id="{cid}-i" class="clip card wcard" '
               f'src="assets/img2/{src}" alt="" {sc.timed(on, t1)} data-track-index="3"{gattr("doc")} '
               f'style="left:{x - w // 2}px;top:{y - h // 2}px;width:{w}px;height:{h}px;object-fit:cover;opacity:{0.55 + 0.45 * s:.2f}" /></div>',
               [f'tl.fromTo("#{cid}", {{ x: {rnd.randint(-40, 40)}, y: {rnd.randint(30, 60)} }}, {{ x: {rnd.randint(-40, 40)}, '
                f'y: {rnd.randint(-60, -30)}, duration: {r3(t1 - on)}, ease: "none" }}, {sc.at(on)});'])
    # the digits
    rid = sc.uid("yr")
    n = len(years)
    span = max(0.05, land_at - t0 - 0.05)
    times = [t0 + span * (k / (n - 1)) ** 1.8 for k in range(n)] if n > 1 else [t0]
    for k, y in enumerate(years):
        a = times[k]
        b = times[k + 1] if k + 1 < n else t1
        yid = sc.uid("y")
        sc.raw(f'<div id="{yid}" class="clip t" {sc.timed(a, b)} data-track-index="5" data-layout-allow-overflow '
               f'style="left:0;width:1920px;top:{540 - size * 0.56:.0f}px;text-align:center;font-family:Satoshi;font-weight:900;'
               f'font-size:{size}px;letter-spacing:-0.03em;color:{INK};text-shadow:0 0 18px rgba(255,255,255,0.75), '
               f'0 0 60px rgba(255,255,255,0.35), 0 0 140px rgba(255,255,255,0.15);z-index:{sc.nz() + 400}">'
               + (f'<span id="{yid}-a">{esc(str(y)[:invert_digits])}</span><span>{esc(str(y)[invert_digits:])}</span>'
                  if k == n - 1 and invert_digits else esc(str(y))) + '</div>')
        if k == n - 1 and invert_digits:  # Dario's partial inversion on the landed year
            for f, on in ((6, 1), (8, 0), (10, 1), (11, 0)):
                sc.J(f'tl.set("#{yid}-a", {{ backgroundColor: "{INK if on else "rgba(0,0,0,0)"}", color: "{"#0a0a0a" if on else INK}", '
                     f'textShadow: "{"none" if on else "0 0 18px rgba(255,255,255,0.75)"}" }}, {sc.at(a + f * F1)});')
    if label:
        lid = sc.uid("yl")
        la = label_at or land_at
        sc.raw(f'<div id="{lid}" class="clip t" {sc.timed(la, t1)} data-track-index="5" style="left:0;width:1920px;'
               f'top:{540 + size * 0.5:.0f}px;text-align:center;font-family:Satoshi;font-weight:700;font-size:60px;color:{INK};'
               f'text-shadow:{GLOW_REST};z-index:{sc.nz() + 400}">{esc(label)}</div>',
               [f'tl.fromTo("#{lid}", {{ opacity: 0, filter: "blur(14px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.22, '
                f'ease: "expo.out", immediateRender: false }}, {sc.at(la)});'])


def sp_bars(sc, t0, t1, words, size=110, y=540, exit_at=None, ground="#050505"):
    """Fink's bar write-on: each word waits as a solid white bar in its final place and flips into the word on its
    beat; a white bar sweeps the line away."""
    if ground:
        sc.black(t0, t1, color=ground)
    ws = [textw(w, "Satoshi", 700, size, track=-0.02) for w, _ in words]
    gap = size * 0.26
    W = sum(ws) + gap * (len(ws) - 1)
    x = 960 - W / 2
    bid = sc.uid("bars")
    inner = []
    for k, ((w, t), ww) in enumerate(zip(words, ws)):
        inner.append(f'<div id="{bid}-b{k}" style="position:absolute;left:{x:.0f}px;top:{y - size * 0.36:.0f}px;width:{ww:.0f}px;'
                     f'height:{size * 0.74:.0f}px;background:{INK};box-shadow:0 0 22px rgba(255,255,255,0.45)"></div>'
                     f'<div id="{bid}-w{k}" class="t" style="left:{x:.0f}px;top:{y - size * 0.62:.0f}px;font-family:Satoshi;'
                     f'font-weight:700;font-size:{size}px;letter-spacing:-0.02em;color:{INK};text-shadow:{GLOW_REST};opacity:0">'
                     f'{esc(w)}</div>')
        sc.J(f'tl.set("#{bid}-b{k}", {{ opacity: 0 }}, {sc.at(t)});')
        sc.J(f'tl.set("#{bid}-w{k}", {{ opacity: 1 }}, {sc.at(t)});')
        x += ww + gap
    ex = exit_at or (t1 - 4 * F1)
    sc.raw(f'<div id="{bid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" data-layout-allow-overlap '
           f'style="z-index:{sc.nz() + 300}">{"".join(inner)}<div id="{bid}-sw" style="position:absolute;left:{960 - W / 2 - 10:.0f}px;'
           f'top:{y - size * 0.4:.0f}px;width:{W + 20:.0f}px;height:{size * 0.82:.0f}px;background:{INK};transform-origin:0% 50%;'
           f'opacity:0"></div></div>',
           [f'tl.set("#{bid}-sw", {{ scaleX: 0, opacity: 1 }}, 0);',
            f'tl.fromTo("#{bid}-sw", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {r3(3 * F1)}, ease: "none", immediateRender: false }}, '
            f'{sc.at(ex)});'])
    for k in range(len(words)):
        sc.J(f'tl.set("#{bid}-w{k}", {{ opacity: 0 }}, {sc.at(ex + 3 * F1)});')
    sc.J(f'tl.set("#{bid}-sw", {{ opacity: 0 }}, {sc.at(ex + 4 * F1)});')


def sp_strobe(sc, t0, t1, src, looks, punch_at=None):
    """Fink's style strobe: one picture in several print looks, 2-3 frames each."""
    t = t0
    k = 0
    cams = []
    while t < t1 - 1e-6:
        te = min(t1, t + (2 if k % 2 else 3) * F1)
        cams.append(sc.img(src, t, te, grade=looks[k % len(looks)], push=None))
        t, k = te, k + 1
    if punch_at:
        for cam, _ in cams:
            sc.J(f'tl.set("#{cam}", {{ scale: 1.0 }}, {sc.at(t0)});')
            sc.J(f'tl.set("#{cam}", {{ scale: 1.35 }}, {sc.at(punch_at)});')


def sp_text_behind(sc, t0, t1, cutout, word, size=470, cut_box=(560, 120, 800, 960), ground=None, word_y=520):
    """Hemant's EUDIA: a giant glowing word behind a cut-out of the subject; the word slides slowly behind him."""
    gid = sc.uid("tb")
    bg = ground or "radial-gradient(ellipse at 50% 45%, #3a2a1a 0%, #1a120b 55%, #080605 100%)"
    x, y, w, h = cut_box
    sc.raw(f'<div id="{gid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="1" style="background:{bg};z-index:{sc.nz()}">'
           f'<img class="bktex" src="assets/tex/ht_grunge.jpg" alt="" /></div>')
    wid = sc.uid("tbw")
    sc.raw(f'<div id="{wid}" class="clip t" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'style="left:-300px;width:2520px;top:{word_y - size * 0.55:.0f}px;text-align:center;font-family:\'Instrument Serif\';'
           f'font-size:{size}px;letter-spacing:0.01em;color:{INK};text-shadow:{SERIF_REST};z-index:{sc.nz()}">{esc(word)}</div>',
           [f'tl.fromTo("#{wid}", {{ x: 180, opacity: 0, filter: "blur(14px)" }}, {{ x: 120, opacity: 1, filter: "blur(0px)", '
            f'duration: 0.25, ease: "expo.out", immediateRender: false }}, {sc.at(t0)});',
            f'tl.to("#{wid}", {{ x: -160, duration: {r3(t1 - t0 - 0.25)}, ease: "none" }}, {sc.at(t0 + 0.25)});'])
    cam = sc.uid("tbc")
    sc.raw(f'<div id="{cam}" class="grp" style="z-index:{sc.nz()};transform-origin:960px 900px"><img id="{cam}-i" class="clip" '
           f'src="assets/img2/{cutout}" alt="" {sc.timed(t0, t1)} data-track-index="3" data-layout-allow-occlusion{gattr("warm")} style="position:absolute;'
           f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:contain;object-position:50% 100%" /></div>',
           [f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.04, duration: {r3(t1 - t0)}, ease: "none" }}, {sc.at(t0)});'])


def sp_wall(sc, t0, t1, tiles, cols=6, rows=4, build=0.55):
    """Dario's 'the lead': a wall of archival frames assembles tile by tile, then pushes in slowly."""
    sc.black(t0, t1, color="#050505", tex=False)
    wid = sc.uid("wall")
    gap = 6
    tw, th = (1920 + gap) / cols - gap, (1080 + gap) / rows - gap
    rnd = random.Random(11)
    order = list(range(cols * rows))
    rnd.shuffle(order)
    inner = []
    for j, k in enumerate(order):
        r, c = divmod(k, cols)
        on = t0 + build * j / len(order)
        tid = f"{wid}-t{k}"
        inner.append((tid, on, c * (tw + gap), r * (th + gap), tiles[k % len(tiles)]))
    sc.raw(f'<div id="{wid}" class="grp" style="z-index:{sc.nz()};transform-origin:960px 540px">' + "".join(
        f'<img id="{tid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(on, t1)} data-track-index="3"{gattr("bw")} '
        f'style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{tw:.0f}px;height:{th:.0f}px;object-fit:cover" />'
        for tid, on, x, y, src in inner) + '</div>',
        [f'tl.fromTo("#{wid}", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {r3(t1 - t0)}, ease: "none" }}, {sc.at(t0)});'])
    for tid, on, x, y, src in inner[::3]:  # a one-frame flash on some tiles as they land
        fid = sc.uid("wf")
        sc.raw(f'<div id="{fid}" class="clip" {sc.timed(on, on + F1)} data-track-index="5" style="position:absolute;left:{x:.0f}px;'
               f'top:{y:.0f}px;width:{tw:.0f}px;height:{th:.0f}px;background:#fff;z-index:{sc.nz() + 200}"></div>')
    vid = sc.uid("vig")  # darken the centre for the word
    sc.raw(f'<div id="{vid}" class="clip grp" {sc.timed(t0 + build * 0.6, t1)} data-track-index="5" style="z-index:{sc.nz() + 250};'
           f'background:radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.5) 38%, rgba(0,0,0,0.0) 75%)"></div>')


def sp_typed(sc, t0, t1, parts, ground="#050505"):
    """Fink's typed giant words: characters arrive dark grey and brighten to white over three frames; the camera
    follows the cursor with hard jump-reframes. parts: [(text, t_start, size, x, y)]."""
    sc.black(t0, t1, color=ground)
    gid = sc.uid("ty")
    inner, js = [], []
    for p, (text, ts, size, x, y) in enumerate(parts):
        step = 0.055
        chars = []
        for k, ch in enumerate(text):
            cid = f"{gid}-p{p}c{k}"
            chars.append(f'<span id="{cid}" style="opacity:0;color:#555">{esc(ch) if ch != " " else "&nbsp;"}</span>')
            a = ts + k * step
            js += [f'tl.set("#{cid}", {{ opacity: 1, color: "#5c5c5c" }}, {sc.at(a)});',
                   f'tl.set("#{cid}", {{ color: "#a8a8a8" }}, {sc.at(a + F1)});',
                   f'tl.set("#{cid}", {{ color: "{INK}" }}, {sc.at(a + 2 * F1)});']
        inner.append(f'<div class="t" style="left:{x}px;top:{y}px;font-family:Satoshi;font-weight:900;font-size:{size}px;'
                     f'letter-spacing:-0.04em;text-shadow:0 0 20px rgba(255,255,255,0.55), 0 0 70px rgba(255,255,255,0.25)">'
                     f'{"".join(chars)}</div>')
    sc.raw(f'<div id="{gid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" data-layout-allow-overflow '
           f'style="z-index:{sc.nz() + 300};transform-origin:0px 0px">{"".join(inner)}</div>', js)
    return gid


def sp_slice(sc, key, src_t, t0, t1, cut_at, grade="doc"):
    """'cuts': the frame is sliced along a diagonal and the halves shear apart."""
    top = "polygon(0 0, 100% 0, 100% 38%, 0 66%)"
    bot = "polygon(0 66%, 100% 38%, 100% 100%, 0 100%)"
    ca, _ = sc.v(key, src_t, t0, t1, grade=grade, push=None, cam_style=f"clip-path:{top};")
    cb, _ = sc.v(key, src_t, t0, t1, grade=grade, push=None, cam_style=f"clip-path:{bot};")
    sc.J(f'tl.fromTo("#{ca}", {{ x: 0, y: 0 }}, {{ x: -34, y: -16, duration: 0.16, ease: "power3.out", immediateRender: false }}, {sc.at(cut_at)});')
    sc.J(f'tl.fromTo("#{cb}", {{ x: 0, y: 0 }}, {{ x: 34, y: 16, duration: 0.16, ease: "power3.out", immediateRender: false }}, {sc.at(cut_at)});')
    lid = sc.uid("cutl")
    ang = math.degrees(math.atan2(-0.28 * 1080, 1920))
    sc.raw(f'<div id="{lid}" class="clip" {sc.timed(cut_at - F1, cut_at + 2 * F1)} data-track-index="6" style="position:absolute;'
           f'left:-100px;top:{0.52 * 1080:.0f}px;width:2120px;height:6px;background:#fff;box-shadow:0 0 24px 8px rgba(255,255,255,0.8);'
           f'transform:rotate({ang:.2f}deg);transform-origin:50% 50%;z-index:{sc.nz() + 500}"></div>')


def sp_wipe(sc, key, src_t, t0, t1, wipe_at, dur=0.32):
    """A dirty copy of the shot is wiped away left to right by a glowing line, leaving it clean."""
    sc.v(key, src_t, t0, t1, grade="doc", push=(1.0, 1.04))
    cam, _ = sc.v(key, src_t, t0, t1, grade="dirty", push=(1.0, 1.04), cam_style="clip-path: inset(0 0 0 var(--wx)); --wx: 0%;")
    wid = sc.uid("wipe")
    sc.raw(f'<div id="{wid}" class="clip" {sc.timed(wipe_at, wipe_at + dur)} data-track-index="6" style="position:absolute;'
           f'left:-10px;top:0;width:8px;height:1080px;background:#FFFDF6;box-shadow:0 0 26px 8px rgba(255,253,246,0.8);'
           f'z-index:{sc.nz() + 500}"></div>',
           [f'tl.fromTo("#{cam}", {{ "--wx": "0%" }}, {{ "--wx": "100%", duration: {dur}, ease: "power2.inOut", immediateRender: false }}, '
            f'{sc.at(wipe_at)});',
            f'tl.fromTo("#{wid}", {{ x: 0 }}, {{ x: 1930, duration: {dur}, ease: "power2.inOut", immediateRender: false }}, {sc.at(wipe_at)});'])


def sp_counter(sc, t0, t1, steps, x=190, y=540, size=230, small=None, small_at=None, align="left"):
    """Fink's chunk counter: $100 -> $100,000 -> $100,000,000, left-aligned, each chunk on its word."""
    room = (1920 - 2 * x) if align == "left" else 1700
    size = int(min(size, room / max(textw(v, "Satoshi", 900, 1, track=-0.035) for v, _ in steps)))
    for k, (val, a) in enumerate(steps):
        b = steps[k + 1][1] if k + 1 < len(steps) else t1
        cid = sc.uid("cn")
        box = f"left:{x}px;" if align == "left" else "left:0;width:1920px;text-align:center;"
        sc.raw(f'<div id="{cid}" class="clip t" {sc.timed(a, b)} data-track-index="5" data-layout-allow-overflow style="{box}'
               f'top:{y - size * 0.56:.0f}px;font-family:Satoshi;font-weight:900;font-size:{size}px;letter-spacing:-0.035em;'
               f'color:{INK};text-shadow:0 0 18px rgba(255,255,255,0.6), 0 0 60px rgba(255,255,255,0.25);z-index:{sc.nz() + 400}">'
               f'{esc(val)}</div>')
        if k == 0:
            sc.J(f'tl.fromTo("#{cid}", {{ opacity: 0, filter: "blur(16px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, '
                 f'ease: "expo.out", immediateRender: false }}, {sc.at(a)});')
    if small:
        sid = sc.uid("cs")
        box = f"left:{x + 8}px;" if align == "left" else "left:0;width:1920px;text-align:center;"
        sc.raw(f'<div id="{sid}" class="clip t" {sc.timed(small_at, t1)} data-track-index="5" style="{box}top:{y + size * 0.5:.0f}px;'
               f'font-family:Satoshi;font-weight:700;font-size:58px;color:{INK};text-shadow:{GLOW_REST};z-index:{sc.nz() + 400}">'
               f'{esc(small)}</div>',
               [f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(12px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, '
                f'ease: "expo.out", immediateRender: false }}, {sc.at(small_at)});'])


def sp_cards(sc, t0, t1, srcs, step=5, box_w=560, ground="#0b0b0c"):
    """Photo cards land one after another on a dark ground (card settle from 1.5x)."""
    sc.black(t0, t1, color=ground)
    pos = [(560, 470, -3), (1360, 430, 2.5), (960, 640, -1)]
    for k, src in enumerate(srcs):
        x, y, rot = pos[k % len(pos)]
        w, h = box_w, int(box_w * 0.66)
        on = t0 + k * step * F1
        cid = sc.uid("pc")
        sc.raw(f'<div id="{cid}" class="grp" style="z-index:{sc.nz()};transform-origin:{x}px {y}px"><img id="{cid}-i" '
               f'class="clip card wcard" src="assets/img2/{src}" alt="" {sc.timed(on, t1)} data-track-index="3"{gattr("doc")} '
               f'style="left:{x - w // 2}px;top:{y - h // 2}px;width:{w}px;height:{h}px;object-fit:cover;transform:rotate({rot}deg)" /></div>',
               [f'tl.fromTo("#{cid}", {{ scale: 1.5 }}, {{ scale: 1.0, duration: 0.3, ease: "power3.out", immediateRender: false }}, {sc.at(on)});'])


def sp_window(sc, cam, t, to=0.3, dur=0.42):
    """Fink's window zoom-out: the shot shrinks into a small window on black."""
    sc.J(f'tl.to("#{cam}", {{ scale: {to}, duration: {dur}, ease: "power3.out" }}, {sc.at(t)});')


def sp_drop(sc, t0, t1, logos, fall_at):
    """The fallen banks: their logos hang on a dark ground and drop out of frame on 'fell'."""
    sc.black(t0, t1, color="#08090a")
    xs = [520, 1400] if len(logos) == 2 else [400, 960, 1520]
    for k, src in enumerate(logos):
        lid = sc.uid("lg")
        w = 620 if len(logos) == 2 else 470
        sc.raw(f'<div id="{lid}" class="grp" style="z-index:{sc.nz()}"><img id="{lid}-i" class="clip" src="assets/img2/{src}" alt="" '
               f'{sc.timed(t0, t1)} data-track-index="3" style="position:absolute;left:{xs[k] - w // 2}px;top:{540 - w // 4}px;'
               f'width:{w}px;height:{w // 2}px;object-fit:contain;filter:brightness(0) invert(1) drop-shadow(0 0 18px rgba(255,255,255,0.4))" /></div>',
               [f'tl.fromTo("#{lid}", {{ y: 0, rotation: 0 }}, {{ y: 1250, rotation: {(-1) ** k * (9 + 4 * k)}, duration: 0.55, '
                f'ease: "power2.in", immediateRender: false }}, {sc.at(fall_at + k * 0.07)});'])


def sp_logo_wipe(sc, t0, t1, src, w=1300):
    """The JPMorganChase wordmark revealed by a light sweep on black."""
    sc.black(t0, t1, color="#050505")
    lid = sc.uid("lw")
    h = int(w * 0.1418)
    sc.raw(f'<div id="{lid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" style="z-index:{sc.nz()}">'
           f'<img id="{lid}-i" src="assets/img2/{src}" alt="" style="position:absolute;left:{960 - w // 2}px;top:{540 - h // 2}px;'
           f'width:{w}px;height:{h}px;filter:brightness(0) invert(1) drop-shadow(0 0 22px rgba(255,255,255,0.6));'
           f'clip-path:inset(0 var(--r) 0 0);--r:100%" /></div>',
           [f'tl.fromTo("#{lid}-i", {{ "--r": "100%" }}, {{ "--r": "0%", duration: 0.32, ease: "power2.out", immediateRender: false }}, '
            f'{sc.at(t0)});'])
    sc.streak(t0 + 0.08, frames=5, y=540, h=120)


def sp_screens(sc, t0, t1, cells, cols=3, rows=3):
    """A wall of trading screens (each cell its own clip)."""
    sc.black(t0, t1, color="#030303", tex=False)
    g = 6
    tw, th = (1920 + g) / cols - g, (1080 + g) / rows - g
    for k, (key, src_t) in enumerate(cells[:cols * rows]):
        r, c = divmod(k, cols)
        on = t0 + (k % 4) * F1
        sc.v(key, src_t, on, t1, grade="doc", push=(1.0, 1.05), box=(int(c * (tw + g)), int(r * (th + g)), int(tw), int(th)))


# ---- v3 set pieces -------------------------------------------------------------------------------
def sp_logo_card(sc, t0, t1, src, w=860, h=320, x=960, y=540, rot=0.0, settle=0.3, z=None, pad=52, bg="#FBFAF6"):
    """A logo printed on a white card that lands on the paper (Fink's First Boston card, AMD's cream cards)."""
    cid = sc.uid("lc")
    sc.raw(f'<div id="{cid}" class="grp" style="z-index:{z or sc.nz()};transform-origin:{x}px {y}px">'
           f'<div id="{cid}-c" class="clip card" {sc.timed(t0, t1)} data-track-index="4" style="left:{x - w // 2}px;'
           f'top:{y - h // 2}px;width:{w}px;height:{h}px;background:{bg}"><img src="assets/img2/{src}" alt="" '
           f'style="position:absolute;left:{pad}px;top:{pad}px;width:{w - 2 * pad}px;height:{h - 2 * pad}px;'
           f'object-fit:contain" /></div></div>',
           [f'tl.fromTo("#{cid}", {{ scale: 1.6, rotation: {rot * 2.5} }}, {{ scale: 1.0, rotation: {rot}, duration: {settle}, '
            f'ease: "power3.out", immediateRender: false }}, {sc.at(t0)});'])
    return cid


def sp_flip_collage(sc, t0, t1, photos, collage_at, flip=2):
    """Fink's 'mortgages': photo cards flip every `flip` frames at full size on paper, then the camera pulls back and
    the pile becomes a wall of cards scattered across the paper."""
    sc.paper(t0, t1)
    cam = sc.uid("fcam")
    cw, ch = 780, 520
    cx, cy = 960, 540
    rnd = random.Random(23)
    slots = [(330, 230), (960, 175), (1590, 235), (250, 560), (1670, 545), (360, 880), (980, 900), (1580, 870),
             (640, 400), (1290, 410), (660, 720), (1280, 720)]
    inner = []
    for k, (x, y) in enumerate(slots):
        src = photos[(k + 3) % len(photos)]
        w, h = 400, 268
        r = rnd.uniform(-7, 7)
        on = collage_at + (k % 6) * F1
        inner.append(f'<div class="grp" style="transform-origin:{x}px {y}px" id="{cam}-s{k}"><img id="{cam}-si{k}" class="clip card wcard" '
                     f'src="assets/img2/{src}" alt="" {sc.timed(on, t1)} data-track-index="3"{gattr("doc")} '
                     f'style="left:{x - w // 2}px;top:{y - h // 2}px;width:{w}px;height:{h}px;object-fit:cover" /></div>')
        sc.J(f'tl.set("#{cam}-s{k}", {{ rotation: {r:.2f} }}, 0);')
    t = t0
    k = 0
    while t < t1 - 1e-6:  # the centre card: flipping, then still on the last photo
        te = t + flip * F1 if t < collage_at - 1e-6 else t1
        te = min(te, collage_at) if t < collage_at - 1e-6 else te
        inner.append(f'<img id="{cam}-f{k}" class="clip card wcard" src="assets/img2/{photos[k % len(photos)]}" alt="" {sc.timed(t, te)} '
                     f'data-track-index="3"{gattr("doc")} style="left:{cx - cw // 2}px;top:{cy - ch // 2}px;width:{cw}px;'
                     f'height:{ch}px;object-fit:cover;z-index:50" />')
        t, k = te, k + 1
    sc.raw(f'<div id="{cam}" class="grp" style="z-index:{sc.nz()};transform-origin:{cx}px {cy}px">{"".join(inner)}</div>',
           [f'tl.fromTo("#{cam}", {{ scale: 2.15 }}, {{ scale: 2.05, duration: {r3(collage_at - t0)}, ease: "none" }}, {sc.at(t0)});',
            f'tl.fromTo("#{cam}", {{ scale: 2.05 }}, {{ scale: 1.0, duration: 0.42, ease: "power3.out", immediateRender: false }}, '
            f'{sc.at(collage_at)});',
            f'tl.to("#{cam}", {{ scale: 0.96, duration: {r3(t1 - collage_at - 0.42)}, ease: "none" }}, {sc.at(collage_at + 0.42)});'])


MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def sp_calendar(sc, t0, t1, first=(1998, 11), last=(2000, 3), land_at=None, x=960, y=430, w=470, h=560):
    """Fink's flip calendar: month pages flip every two frames and land on the month he went back to work."""
    sc.black(t0, t1, color="#0b0a09")
    pages = []
    yy, mm = first
    while (yy, mm) <= last:
        pages.append((MONTHS[mm - 1], yy))
        mm += 1
        if mm > 12:
            yy, mm = yy + 1, 1
    land_at = land_at or (t1 - 0.4)
    start = land_at - (len(pages) - 1) * 2 * F1
    cam = sc.uid("cal")
    inner = []
    for k, (mon, yr) in enumerate(pages):
        a = t0 if k == 0 else start + k * 2 * F1
        b = start + (k + 1) * 2 * F1 if k + 1 < len(pages) else t1
        last_page = k + 1 == len(pages)
        inner.append(
            f'<div id="{cam}-p{k}" class="clip card" {sc.timed(a, b)} data-track-index="4" style="left:{x - w // 2}px;top:{y - h // 2}px;'
            f'width:{w}px;height:{h}px;background:#F3EEE3">'
            f'<div style="position:absolute;left:0;top:0;width:{w}px;height:46px;background:#1b1a18"></div>'
            + "".join(f'<div style="position:absolute;left:{70 + j * 82}px;top:-14px;width:26px;height:44px;border-radius:13px;'
                      f'background:#8a8580"></div>' for j in range(5)) +
            f'<div style="position:absolute;left:0;top:46px;width:{w}px;height:150px;background:{"#C8322A" if last_page else "#B52B24"};'
            f'color:#FBF8EC;font-family:Satoshi;font-weight:900;font-size:104px;letter-spacing:0.04em;text-align:center;'
            f'line-height:150px">{mon}</div>'
            f'<div style="position:absolute;left:0;top:220px;width:{w}px;text-align:center;font-family:\'Instrument Serif\';'
            f'font-size:250px;line-height:1;color:#141210">{yr}</div></div>')
    sc.raw(f'<div id="{cam}" class="grp" style="z-index:{sc.nz()};transform-origin:{x}px {y}px">{"".join(inner)}</div>',
           [f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {r3(t1 - t0)}, ease: "none" }}, {sc.at(t0)});'])
    sc.flash(land_at, d=0.16, peak=0.45)


def sp_merge(sc, t0, t1, left_src, right_src, result_src, merge_at):
    """Two logo cards slide into each other and become the merged company's card (white flash on the hit)."""
    sc.paper(t0, t1)
    gid = sc.uid("mg")
    for side, src, x0 in (("l", left_src, 520), ("r", right_src, 1400)):
        sc.raw(f'<div id="{gid}-{side}" class="grp" style="z-index:{sc.nz()}"><div id="{gid}-{side}c" class="clip card" {sc.timed(t0, merge_at)} '
               f'data-track-index="4" style="left:{x0 - 330}px;top:{540 - 120}px;width:660px;height:240px;background:#FBFAF6">'
               f'<img src="assets/img2/{src}" alt="" style="position:absolute;left:46px;top:46px;width:568px;height:148px;'
               f'object-fit:contain" /></div></div>',
               [f'tl.fromTo("#{gid}-{side}", {{ x: 0, rotation: {-3 if side == "l" else 3} }}, {{ x: {960 - x0}, rotation: 0, '
                f'duration: {r3(merge_at - t0)}, ease: "power3.in", immediateRender: false }}, {sc.at(t0)});'])
    sp_logo_card(sc, merge_at, t1, result_src, w=1180, h=280, settle=0.34)
    sc.flash(merge_at, d=0.2, peak=0.85)


def sp_cards_fall(sc, t0, t1, items, fall_at):
    """The fallen banks: their cards lie on the paper and drop out of frame on the word."""
    sc.paper(t0, t1)
    pos = [(560, 600, -4), (1380, 560, 3), (980, 780, -1.5)]
    for k, (kind, src) in enumerate(items):
        x, y, rot = pos[k % len(pos)]
        gid = sc.uid("cf")
        if kind == "logo":
            w, h = 660, 230
            body = (f'<div id="{gid}-c" class="clip card" {sc.timed(t0, t1)} data-track-index="4" style="left:{x - w // 2}px;top:{y - h // 2}px;'
                    f'width:{w}px;height:{h}px;background:#FBFAF6"><img src="assets/img2/{src}" alt="" style="position:absolute;'
                    f'left:44px;top:40px;width:{w - 88}px;height:{h - 80}px;object-fit:contain" /></div>')
        else:
            w, h = 560, 380
            body = (f'<img id="{gid}-c" class="clip card wcard" src="assets/img2/{src}" alt="" {sc.timed(t0, t1)} data-track-index="3"'
                    f'{gattr("bw")} style="left:{x - w // 2}px;top:{y - h // 2}px;width:{w}px;height:{h}px;object-fit:cover" />')
        sc.raw(f'<div id="{gid}" class="grp" style="z-index:{sc.nz()};transform-origin:{x}px {y}px">{body}</div>',
               [f'tl.fromTo("#{gid}", {{ scale: 1.45, rotation: {rot * 2} }}, {{ scale: 1.0, rotation: {rot}, duration: 0.26, '
                f'ease: "power3.out", immediateRender: false }}, {sc.at(t0 + k * 3 * F1)});',
                f'tl.to("#{gid}", {{ y: 1300, rotation: {rot * 6 + (14 if k % 2 else -14)}, duration: 0.55, ease: "power2.in" }}, '
                f'{sc.at(fall_at + k * 0.06)});'])


# ================================================================================================
# Captions -- the Pattinson engine: sans words glow in, serif words land after a white flicker box with a bloom,
# hero words burst in blown-out, and each line slides to stay centred as its words arrive.
# ================================================================================================
STY = {  # family, weight, size, kind
    "s": ("Satoshi", 700, 84, "sans"),
    "sm": ("Satoshi", 700, 60, "sans"),
    "b": ("Satoshi", 900, 160, "sans"),
    "sl": ("Instrument Serif", 400, 128, "serif"),
    "sh": ("Instrument Serif", 400, 236, "hero"),
    "sx": ("Instrument Serif", 400, 300, "hero"),
    "nm": ("Instrument Serif", 400, 250, "name"),
    "gold": ("Instrument Serif", 400, 236, "gold"),
    "p": ("Satoshi", 800, 96, "paper"),
    "pb": ("Satoshi", 900, 150, "paper"),
    "ps": ("Instrument Serif", 400, 250, "paper"),
}
CAPS = []


def W_(i, st, text=None):
    return (text or VOW[i]["text"], VT(i), st)


def N_(i, st, text=None):
    return (text or NEWS[i]["text"], NT(i), st)


def Q_(i, st, text=None):
    return (text or QUOTE[i]["text"], QT(i), st)


def cap(lines, end=None, y=540, exit="cut", start=None, x=960, scrim=None):
    CAPS.append(dict(lines=lines, end=end, y=y, exit=exit, start=start, x=x, scrim=scrim))


def build_captions():
    els, js = [], []
    groups = sorted(CAPS, key=lambda g: min(t for line in g["lines"] for _, t, _ in line))
    for gi, g in enumerate(groups):
        gid = f"cg{gi:03d}"
        first = min(t for line in g["lines"] for _, t, _ in line)
        last = max(t for line in g["lines"] for _, t, _ in line)
        t0 = round(g["start"] if g["start"] is not None else first - 2 * F1, 3)
        if g["end"] is not None:
            t1 = g["end"]
        elif gi + 1 < len(groups):
            nf = min(t for line in groups[gi + 1]["lines"] for _, t, _ in line)
            t1 = round(nf - 2 * F1, 3)
            if t1 - last > 1.4:
                t1 = round(last + 1.0, 3)
        else:
            t1 = DUR
        # vertical layout: line heights by their biggest word
        heights = [max(STY[st][2] for _, _, st in line) for line in g["lines"]]
        total = sum(h * 0.92 for h in heights)
        ytop = g["y"] - total / 2
        lines_html = []
        for li, line in enumerate(g["lines"]):
            lh = heights[li] * 0.92
            base = ytop + lh * 0.80  # baseline of this line
            ytop += lh
            ws = []
            for text, t, st in line:
                fam, wt, size, kind = STY[st]
                text = text.replace(",", "").replace(".", "") if text not in ("$10", "$60", "$500") else text
                tr = -0.035 if fam == "Satoshi" else -0.01
                ws.append((text, t, st, textw(text, fam, wt, size, track=tr)))
            gaps = [(STY[st][2] * (0.26 if STY[st][0] == "Satoshi" else 0.2)) for _, _, st, _ in ws]
            Wt = sum(w for *_, w in ws) + sum(gaps[1:])
            x = g["x"] - Wt / 2
            spans = []
            prefix = []
            acc = 0.0
            for k, (text, t, st, w) in enumerate(ws):
                fam, wt, size, kind = STY[st]
                if k > 0:
                    acc += gaps[k]
                left = x + acc
                acc += w
                prefix.append(acc)
                sid = f"{gid}-w{li}{k}"
                color = "#111" if kind == "paper" else INK
                shadow = {"sans": GLOW_REST, "serif": SERIF_REST, "hero": SERIF_REST, "name": SERIF_REST,
                          "gold": GOLD_REST, "paper": "0 0 18px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.5)"}[kind]
                tr = "-0.035em" if fam == "Satoshi" else "-0.01em"
                top = base - size * 0.80
                style = (f"left:{left:.0f}px;top:{top:.0f}px;font-family:'{fam}';font-weight:{wt};font-size:{size}px;"
                         f"letter-spacing:{tr};color:{color};")
                if kind in ("serif", "hero", "name", "gold"):
                    spans.append(f'<span id="{sid}" class="w" style="{style}"><span id="{sid}-f" class="fl"></span>'
                                 f'<span id="{sid}-t" class="wt" style="opacity:0;text-shadow:{shadow}">{esc(text)}</span></span>')
                else:
                    spans.append(f'<span id="{sid}" class="w" style="{style}text-shadow:{shadow};opacity:0">{esc(text)}</span>')
                a = max(t0, t - 0.0)
                if kind == "sans":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
                              f'{{ opacity: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.24, ease: "expo.out", '
                              f'immediateRender: false }}, {r3(a)});')
                elif kind == "paper":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, y: 44 }}, {{ opacity: 1, y: 0, duration: 0.28, ease: "steps(4)", '
                              f'immediateRender: false }}, {r3(a)});')
                elif kind == "serif":
                    b0 = max(t0, a - 4 * F1)
                    js += [f'tl.set("#{sid}-f", {{ opacity: 1, filter: "blur(3px)" }}, {r3(b0)});',
                           f'tl.set("#{sid}-f", {{ filter: "blur(0px)" }}, {r3(b0 + F1)});',
                           f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(max(b0 + 2 * F1, a - F1))});',
                           f'tl.set("#{sid}-t", {{ opacity: 1, filter: "blur(8px)", textShadow: "{SERIF_BLOOM}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(3px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {r3(a + 3 * F1)});']
                else:  # hero, gold and name words burst in blown-out, then settle crisp with their halo
                    rest = GOLD_REST if kind == "gold" else SERIF_REST
                    if kind == "name" and k == 1:  # Dario's glitch frames on the second name word
                        first_id = f"{gid}-w{li}0-t"
                        js += [f'tl.set("#{sid}-f", {{ opacity: 1, backgroundColor: "#EFE3A0", boxShadow: "none" }}, {r3(a - 2 * F1)});',
                               f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(a)});',
                               f'tl.set("#{first_id}", {{ color: "#0d0d0d", textShadow: "none" }}, {r3(a - 2 * F1)});',
                               f'tl.set("#{first_id}", {{ color: "{INK}", textShadow: "{SERIF_REST}" }}, {r3(a)});']
                    js += [f'tl.set("#{sid}-t", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("#{sid}-t", {{ scale: 1.005, filter: "blur(2.5px)" }}, {r3(a + 3 * F1)});',
                           f'tl.set("#{sid}-t", {{ scale: 1, filter: "blur(0px)", textShadow: "{rest}" }}, {r3(a + 4 * F1)});']
            # the slide: the line's visible words stay centred as each new word lands
            lid = f"{gid}-l{li}"
            paper = all(STY[st][3] == "paper" for _, _, st, _ in ws)
            if not paper and len(ws) > 1:
                dx = [(Wt - prefix[k]) / 2 for k in range(len(ws))]
                js.append(f'tl.set("#{lid}", {{ x: {dx[0]:.1f} }}, {r3(t0)});')
                for k in range(1, len(ws)):
                    a = max(t0, ws[k][1])
                    nxt = ws[k + 1][1] if k + 1 < len(ws) else a + 1.0
                    d = max(0.04, min(0.2, nxt - a - 0.01))
                    js.append(f'tl.to("#{lid}", {{ x: {dx[k]:.1f}, duration: {r3(d)}, ease: "power3.out" }}, {r3(a)});')
            lines_html.append(f'<div id="{lid}" class="ln">{"".join(spans)}</div>')
        if g.get("scrim"):
            a = g["scrim"]
            lines_html.insert(0, f'<div class="scrim" data-layout-ignore style="left:{g["x"] - 640}px;top:{g["y"] - 230}px;'
                                 f'background:radial-gradient(closest-side, rgba(6,5,4,{a}) 0%, rgba(6,5,4,{round(a * 0.6, 2)}) 50%, '
                                 f'rgba(6,5,4,0) 100%)"></div>')
        els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(t1 - t0)}" data-track-index="1" '
                   f'data-layout-allow-overflow data-layout-allow-overlap>{"".join(lines_html)}</div>')
        if g["exit"] == "blur":
            js.append(f'tl.to("#{gid} .w", {{ opacity: 0, filter: "blur(10px)", duration: 0.18, ease: "power2.in" }}, {r3(t1 - 0.18)});')
        elif g["exit"] == "fade":
            js.append(f'tl.to("#{gid}", {{ opacity: 0, duration: 0.12, ease: "power1.in" }}, {r3(t1 - 0.12)});')
    css = f"""
  {FONTS_CSS}
  #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; }}
  #root .cg {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .ln {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .w {{ position: absolute; white-space: nowrap; line-height: 1; display: inline-block; }}
  #root .w .wt {{ display: inline-block; position: relative; }}
  #root .scrim {{ position: absolute; width: 1280px; height: 460px; }}
  #root .w .fl {{ position: absolute; left: -0.03em; right: -0.03em; top: 0.22em; bottom: 0.10em; opacity: 0;
    background: #ffffff; box-shadow: 0 0 16px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.45); }}
"""
    open(f"{COMP}/captions.html", "w").write(f"""<template>
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
""")
    return len(groups)


# ================================================================================================
# THE EDIT (v3)
# ================================================================================================
# ---- S01  0.00-8.85  the Bloomberg open (the reporter's voice alone; the music bed runs from frame 0)
s = Scene("s01", 0.0, 8.85)
montage(s, [
    (0.0, "GAME", 0.0, {"rate": 0.9}),                  # The: Lower Manhattan
    (CUT(NT(1)), "HOW", 323.2, {"grade": "bw"}),        # name: the Wall St sign, 1920s
], CUT(NT(4)))
s.paper(CUT(NT(4)), CUT(NT(5)))                          # game: the chess hand, a card on paper
cam, _ = s.v("P01", 6.2, CUT(NT(4)), CUT(NT(5)), grade="bw", push=None, box=(640 - 260, 540 - 390, 520, 780),
             cam_style="box-shadow:0 26px 60px rgba(0,0,0,0.45);")
s.J(f'tl.fromTo("#{cam}", {{ scale: 1.55 }}, {{ scale: 1.0, duration: 0.3, ease: "power3.out", immediateRender: false }}, {s.at(CUT(NT(4)))});')
montage(s, [
    (CUT(NT(5)), "BANK", 750.6),                        # in American: the NYSE board and the flag
    (CUT(NT(10)), "BANK", 760.5),                       # financial: a terminal
    (CUT(NT(11)), "P07", 1.0),                          # capitalism: the counting machine ...
    (CUT(NT(11)) + 0.45, "GAME", 329.6),                # ... the vault door
    (CUT(NT(12)), "GAME", 70.2),                        # is being: towers from below
], CUT(NT(14)))
sp_mask_word(s, CUT(NT(14)), CUT(NT(15)), "BIG", "GAME", 6.0)
s.neg(CUT(NT(14)), 2)
montage(s, [
    (CUT(NT(15)), "GAME", 81.5),                        # and no one: Wall Street at rush hour
    (4.91, "GAME", 8.40),                               # the reporter, in sync
], CUT(NT(19)))
sp_echo(s, CUT(NT(19)), CUT(NT(20)), "bigger")
montage(s, [
    (CUT(NT(20)), "HOW", 309.0, {"grade": "bw"}),       # on: the NYSE, 1907
    (CUT(NT(21)), "GAME", 82.6),                        # Wall Street
    (CUT(NT(23)), "GAME", 202.6),                       # than: the blue CHASE signs at night
    (CUT(NT(24)), "GAME", 108.1),                       # JP: JPMORGAN CHASE & CO. cut in stone
    (CUT(NT(25)), "GAME", 109.6),                       # Morgan: J.P. Morgan etched on the glass door
    (CUT(NT(26)), "GAME", 522.05),                      # Chase: the 383 Madison sign
], 8.85)
s.streak(8.52, frames=5)
s.flash(8.80, d=0.18)
cap([[N_(0, "s"), N_(1, "s"), N_(2, "s"), N_(3, "s")]], end=CUT(NT(4)))
cap([[N_(4, "ps")]], x=1330, y=600, end=CUT(NT(5)))
cap([[N_(5, "s"), N_(9, "s"), N_(10, "s")], [N_(11, "sh")]], end=CUT(NT(12)) + 0.02)
cap([[N_(12, "s"), N_(13, "s")]], end=CUT(NT(14)))
cap([[N_(15, "s"), N_(16, "s"), N_(17, "s"), N_(18, "s")]], end=CUT(NT(19)), scrim=0.5)
cap([[N_(20, "s")], [N_(21, "sl"), N_(22, "sl")]], end=CUT(NT(23)))
cap([[N_(23, "s")], [N_(24, "nm", "JPMorgan"), N_(26, "nm", "Chase")]], y=870, end=8.80, exit="fade")

# ---- S02  8.85-12.36  "This is the most influential man in America right now."  (the seal ring, the punch-in)
s = Scene("s02", 8.85, CUT(VT(10)))
sp_seal_ring(s, 8.85, CUT(VT(5)), RING_PICS, glint_at=CUT(VT(5)) - 0.3, white_at=CUT(VT(5)) - 0.04, cy=420, D=620)
sp_seal_portrait(s, CUT(VT(5)), CUT(VT(8)), CUT_DIMON_UP, punch_at=CUT(VT(7)))
montage(s, [(CUT(VT(8)), "BANK", 19.6, {"xyz": (0.45, 0.56, 1.2)})], CUT(VT(10)))   # right now: the walk-in
cap([[W_(0, "s"), W_(1, "s"), W_(2, "s"), W_(3, "s")], [W_(4, "sh")]], y=900, end=CUT(VT(5)) - 0.3, exit="blur")
cap([[W_(5, "s"), W_(6, "s")], [W_(7, "sh")]], end=CUT(VT(8)))
cap([[W_(8, "s"), W_(9, "s")]], end=CUT(VT(10)))

# ---- S03  12.36-15.07  "He's basically the CEO of Wall Street,"  (a different stage on every word)
s = Scene("s03", CUT(VT(10)), CUT(VT(17)))
montage(s, [
    (CUT(VT(10)), "GAME", 61.4),                        # He's: at the 270 Park podium, arm up
    (CUT(VT(11)), "CHAIR", 1265.2),                     # basically: Stanford
    (CUT(VT(11)) + 0.24, "HOW", 49.2),                  # CNBC
    (CUT(VT(12)), "BANK", 40.6),                        # the: Bloomberg
    (CUT(VT(13)), "GAME", 193.2),                       # CEO: in his office
    (CUT(VT(14)), "GAME", 121.6),                       # of: under the press lights
], CUT(VT(15)))
s.v("WOLF", 1.25, CUT(VT(15)), CUT(VT(17)), grade="warm", push=(1.0, 1.03))
sp_face_boxes(s, CUT(VT(15)), CUT(VT(17)), [(800, 140, 330, 410, "person 0.97"), (560, 470, 760, 600, "person 0.91"),
                                           (875, 760, 120, 210, "microphone 0.88")])
s.neg(CUT(VT(15)), 1)
cap([[W_(10, "s"), W_(11, "s"), W_(12, "s")], [W_(13, "sh")]], end=CUT(VT(14)))
cap([[W_(14, "s")], [W_(15, "sh"), W_(16, "sh")]], y=870, end=CUT(VT(17)))

# ---- S04  15.07-20.86  "a guy who got fired in 1998 by his own mentor over a bonus and a family grudge,"
s = Scene("s04", CUT(VT(17)), CUT(VT(35)))
montage(s, [
    (CUT(VT(17)), "UNT", 543.5, {"grade": "bw"}),               # a guy who got: young Dimon
    (CUT(VT(21)), "MPB", 1067.6, {"grade": "crt"}),             # fired: the old TV ...
    (CUT(VT(21)) + 3 * F1, "MPB", 1071.0, {"grade": "crt"}),    # ... the evening news
], CUT(VT(23)))
s.neg(CUT(VT(21)), 2)
sp_roller(s, CUT(VT(23)), CUT(VT(24)), list(range(1990, 1999)), land_at=VT(23) + 0.22, cards=[], video_bg=("MPB", 850.0),
          invert_digits=2)
montage(s, [
    (CUT(VT(24)), "BANK", 447.6),                      # by his own: Weill and Dimon
    (CUT(VT(27)), "MPB", 438.2),                       # mentor: Weill
], CUT(VT(28)))
sp_grid4(s, CUT(VT(28)), CUT(VT(31)), [("P07", 1.2), ("P10", 2.2), ("MPB", 1784.0), ("HOW", 781.5)])
montage(s, [
    (CUT(VT(31)), "UNT", 618.6, {"xyz": (0.45, 0.415, 1.7)}),   # and a family: Jessica Weill Bibliowicz
    (CUT(VT(34)), "MPB", 1054.0, {"grade": "warm"}),           # grudge
], CUT(VT(35)))
s.neg(CUT(VT(34)), 2)
cap([[W_(17, "s"), W_(18, "s"), W_(19, "s"), W_(20, "s")], [W_(21, "sh")]], end=CUT(VT(23)))
cap([[W_(24, "s"), W_(25, "s"), W_(26, "s")], [W_(27, "sh")]], end=CUT(VT(28)))
cap([[W_(28, "s"), W_(29, "s")], [W_(30, "sh")]], end=CUT(VT(31)))
cap([[W_(31, "s"), W_(32, "s"), W_(33, "s")], [W_(34, "sh")]], y=820, end=CUT(VT(35)))

# ---- S05  20.86-23.60  "now runs the biggest bank in the world."
s = Scene("s05", CUT(VT(35)), QUOTE_AT)
montage(s, [
    (CUT(VT(35)), "GAME", 93.6),                       # now: cutting the ribbon at 270 Park
    (CUT(VT(36)), "GAME", 99.2),                       # runs: on stage, the hard hats in front
    (CUT(VT(38)), "GAME", 114.2),                      # the biggest: the tower from below
    (CUT(VT(39)), "GAME", 108.2),                      # bank: JPMORGAN CHASE & CO. on the glass
    (CUT(VT(40)), "BANK", 1.2, {"xyz": (0.55, 0.58, 1.2)}),   # in the: London
    (CUT(VT(42)), "GAME", 80.2),                       # world: Manhattan from straight above
], QUOTE_AT)
s.flash(QUOTE_AT - 0.02, d=0.16, peak=0.85)
cap([[W_(35, "s"), W_(36, "s"), W_(37, "s")], [W_(38, "b"), W_(39, "b")]], end=CUT(VT(40)))
cap([[W_(40, "s"), W_(41, "s")], [W_(42, "sh")]], end=QUOTE_AT - 0.05, exit="fade")

# ---- S06  23.60-34.85  Dimon in his own words (Bloomberg) with the reference reel's lockups
s = Scene("s06", QUOTE_AT, 34.85)
TWO = round(QUOTE_AT + (281.00 - QUOTE_SRC0), 3)
SY = lambda t: 273.05 + (t - QUOTE_AT)
s.v("BANK", SY(QUOTE_AT), QUOTE_AT, CUT(QT(5)), push=(1.0, 1.04))
montage(s, [
    (CUT(QT(5)), "GAME", 315.6),                       # companies: towers ...
    (CUT(QT(5)) + 0.18, "BANK", 207.6),
    (CUT(QT(5)) + 0.36, "GAME", 514.2),
], CUT(QT(7)))
sp_flip_collage(s, CUT(QT(7)), CUT(QT(9)), LEADERS, collage_at=CUT(QT(8)))   # 30 countries: his meetings, flipping
s.v("BANK", SY(CUT(QT(9))), CUT(QT(9)), CUT(QT(15)), push=(1.02, 1.05))
s.img(WB_BLDG, CUT(QT(15)), CUT(QT(16)), push=(1.0, 1.05))                   # World
s.paper(CUT(QT(16)), CUT(QT(17)))
sp_logo_card(s, CUT(QT(16)), CUT(QT(17)), LOGO["wb"], w=980, h=300)          # Bank: the logo on a card
s.v("BANK", SY(CUT(QT(17))), CUT(QT(17)), CUT(QT(19)), push=(1.04, 1.06))
sp_seal_ring(s, CUT(QT(19)), CUT(QT(24)), GOV, glint_at=CUT(QT(24)) - 0.26, white_at=CUT(QT(24)) - 0.04, photo_step=3,
             cy=420, D=620)
s.v("GAME", 183.6, CUT(QT(24)), TWO, push=(1.0, 1.05))                       # government: waving at the Capitol
s.v("BANK", 281.0, TWO, CUT(QT(29)), push=(1.0, 1.02))
s.v("GAME", 70.6, CUT(QT(29)), CUT(QT(30)), push=(1.15, 1.0))                # big: the towers
cam, _ = s.v("BANK", SY(CUT(QT(30))), CUT(QT(30)), 34.85, push=None, origin="50% 50%")
sp_window(s, cam, CUT(QT(37)), to=0.16, dur=0.38)
cap([[Q_(0, "sm"), Q_(1, "sm")]], y=760, end=CUT(QT(2)))
cap([[Q_(2, "sm")], [Q_(4, "b")]], y=760, end=CUT(QT(5)))
cap([[Q_(5, "sh")]], end=CUT(QT(7)))
cap([[Q_(7, "b")], [Q_(8, "sh", "Countries")]], y=900, end=CUT(QT(9)))
cap([[Q_(9, "sm"), Q_(10, "sm")], [Q_(11, "sh", "Countries")]], y=760, end=CUT(QT(12)))
cap([[Q_(12, "sm"), Q_(13, "sm"), Q_(14, "sm")], [Q_(15, "b"), Q_(16, "b")]], y=860, end=CUT(QT(17)))
cap([[Q_(17, "sm")], [Q_(18, "sx", "IMF")]], y=720, end=CUT(QT(19)))
cap([[Q_(19, "sm"), Q_(20, "sm"), Q_(21, "sm")], [Q_(22, "b"), Q_(23, "b")]], y=905, end=CUT(QT(24)))
cap([[Q_(24, "sh")]], y=800, end=TWO)
cap([[Q_(25, "s"), Q_(26, "s"), Q_(27, "s"), Q_(28, "s")], [Q_(29, "sx")]], end=CUT(QT(30)))
cap([[Q_(30, "s"), Q_(31, "s"), Q_(32, "s"), Q_(33, "s"), Q_(34, "s")], [Q_(35, "s"), Q_(36, "s"), Q_(37, "sm")]], y=820,
    end=34.80, exit="fade")

# ---- S07  34.85-38.43  "Meet Jamie Dimon, the golden boy of Wall Street,"  (the name card)
s = Scene("s07", 34.85, CUT(VT(64)))
s.whiteframe(34.85, 1)
sp_name_card(s, 34.85 + F1, CUT(VT(58)), CUT_DIMON_SMILE, small_at=VT(55), name_at=VT(56))
montage(s, [
    (CUT(VT(58)), "MPB", 294.8, {"grade": "gold", "xyz": (0.68, 0.45, 1.5)}),   # the golden: young Dimon laughing
    (CUT(VT(60)), "MPB", 356.2, {"grade": "gold"}),                             # boy
    (CUT(VT(61)), "HOW", 323.6, {"grade": "bw"}),                               # of Wall Street
], CUT(VT(64)))
sp_gleam(s, CUT(VT(58)) + 0.05, CUT(VT(58)) + 0.5)
sp_gleam(s, CUT(VT(60)) + 0.03, CUT(VT(61)))
cap([[W_(58, "s")], [W_(59, "gold"), W_(60, "gold")]], end=CUT(VT(61)))
cap([[W_(61, "s")], [W_(62, "sh"), W_(63, "sh")]], end=CUT(VT(64)))

# ---- S08  38.43-42.85  "the guy everyone said was next in line to run the biggest financial company in the world."
s = Scene("s08", CUT(VT(64)), CUT(VT(81)))
montage(s, [
    (CUT(VT(64)), "MPB", 850.6),                       # the guy: the press flashes at the Citigroup launch
    (CUT(VT(66)), "BANK", 34.6),                       # everyone: the press around him
], CUT(VT(67)))
sp_nyt(s, CUT(VT(67)), CUT(VT(81)), hl1_at=VT(69), hl1_end=VT(71) + 0.3, reframe_at=CUT(VT(72)),
       hl2_at=VT(75), hl2_end=VT(78))
s.neg(CUT(VT(67)), 1)
s.neg(CUT(VT(72)), 1)
cap([[W_(64, "s"), W_(65, "s"), W_(66, "s")]], end=CUT(VT(67)))
cap([[W_(67, "sm"), W_(68, "sm")], [W_(69, "sh"), W_(70, "sh"), W_(71, "sh")]], y=760, end=CUT(VT(72)))
cap([[W_(72, "sm"), W_(73, "sm"), W_(74, "sm"), W_(75, "sm"), W_(76, "sm"), W_(77, "sm")], [W_(78, "sm"), W_(79, "sm"), W_(80, "sh")]],
    y=770, end=CUT(VT(81)))

# ---- S09  42.85-47.76  "He built Citigroup side-by-side with his mentor Sandy Weill for 16 years."
s = Scene("s09", CUT(VT(81)), CUT(VT(95)))
montage(s, [
    (CUT(VT(81)), "MPB", 734.6),                       # He: Commercial Credit, where they started
    (CUT(VT(82)), "MPB", 1018.6),                      # built: Smith Barney
], CUT(VT(83)))
s.v("MPB", 840.4, CUT(VT(83)), CUT(VT(84)), push=(1.0, 1.04))   # Citigroup: the launch
s.black(CUT(VT(84)), CUT(VT(90)), color="#050505")             # side by side
s.v("BANK", 455.8, CUT(VT(84)), CUT(VT(90)), push=(1.0, 1.05), box=(0, 0, 954, 1080))
s.v("MPB", 438.6, CUT(VT(86)), CUT(VT(90)), push=(1.0, 1.05), box=(966, 0, 954, 1080))
s.whiteframe(CUT(VT(86)), 1)
s.v("MPB", 860.4, CUT(VT(90)), CUT(VT(92)), grade="warm", push=(1.0, 1.04))   # Sandy Weill
sp_roller(s, CUT(VT(92)), CUT(VT(95)), list(range(1982, 1999)), land_at=VT(94) + 0.1, cards=CARDS_8298,
          label="16 years", label_at=VT(94))
cap([[W_(81, "s"), W_(82, "s")], [W_(83, "sh")]], end=CUT(VT(84)))
cap([[W_(84, "s"), W_(85, "s"), W_(86, "s"), W_(87, "s"), W_(88, "s"), W_(89, "s")]], y=930, end=CUT(VT(90)))
cap([[W_(90, "nm"), W_(91, "nm", "Weill")]], y=800, end=CUT(VT(92)))

# ---- S10  47.76-50.81  "But then, at 42, he was fired."
s = Scene("s10", CUT(VT(95)), CUT(VT(102)))
sp_bars(s, CUT(VT(95)), CUT(VT(97)), [("But", VT(95)), ("then", VT(96))])
cam, _ = s.v("UNT", 543.8, CUT(VT(97)), CUT(VT(99)), grade="bw", push=(1.0, 1.02))
s.punch(cam, VT(98) + 0.12, 1.45, origin="46% 34%")
s.neg(CUT(VT(97)), 1)
sp_bars(s, CUT(VT(99)), CUT(VT(101)) + 2 * F1, [("he", VT(99)), ("was", VT(100))], exit_at=CUT(VT(101)) - F1)
STRIKE_MS = round(97.0 - 96.35 - (VT(101) - CUT(VT(101))) * 1.4, 3)
s.black(CUT(VT(101)), CUT(VT(102)), color="#030303", tex=False)
s.v("FIRED", 96.35 + max(0.0, STRIKE_MS), CUT(VT(101)), CUT(VT(102)), rate=1.4, push=(1.0, 1.08), box=(0, 138, 1920, 804),
    size=(1920, 804))
s.flash(VT(101), d=0.24)
s.neg(VT(101) + 2 * F1, 2)
cap([[W_(97, "s")], [W_(98, "sx", "42")]], end=CUT(VT(99)))
cap([[W_(101, "sx", "fired")]], y=560, end=CUT(VT(102)))

# ---- S11  50.81-53.02  "18 months of no job."  (the flip calendar, Nov 1998 to Mar 2000)
s = Scene("s11", CUT(VT(102)), CUT(VT(107)))
sp_calendar(s, CUT(VT(102)), CUT(VT(107)), first=(1998, 11), last=(2000, 3), land_at=VT(106), x=620, y=540)
cap([[W_(102, "b", "18"), W_(103, "s")], [W_(104, "sl"), W_(105, "sl"), W_(106, "sh")]], x=1330, y=540, end=CUT(VT(107)))

# ---- S12  53.02-57.76  "He took up boxing, read biographies, even met Bezos for a job at Amazon."
s = Scene("s12", CUT(VT(107)), CUT(VT(121)))
montage(s, [(CUT(VT(107)), "CHAIR", 2875.0)], CUT(VT(110)))
sp_strobe(s, CUT(VT(110)), CUT(VT(111)), BOX_GLOVES, ["doc", "halftone", "twoink", "mono", "dither", "print"],
          punch_at=VT(110) + 0.05)
s.flash(VT(110), d=0.16, peak=0.7)
montage(s, [(CUT(VT(111)), "MPB", 1180.0, {"grade": "warm"})], CUT(VT(112)))
for k, bk in enumerate(BOOKS):                          # biographies: the covers flip
    t0b = CUT(VT(112)) + k * 3 * F1
    t1b = CUT(VT(112)) + (k + 1) * 3 * F1 if k < len(BOOKS) - 1 else CUT(VT(113))
    s.v(bk.split("_")[0], float(bk.split("_")[1]) / 100, t0b, t1b, grade="warm", push=(1.0, 1.04))
montage(s, [(CUT(VT(113)), "GAME", 256.6)], CUT(VT(116)))           # even met Bezos
sp_text_behind(s, CUT(VT(116)), CUT(VT(121)), CUT_BEZOS, "Amazon", cut_box=(610, 170, 700, 910))
s.neg(CUT(VT(116)), 2)
cap([[W_(107, "s"), W_(108, "s"), W_(109, "s")], [W_(110, "sh")]], end=CUT(VT(111)))
cap([[W_(111, "s")], [W_(112, "sh")]], end=CUT(VT(113)))
cap([[W_(113, "s"), W_(114, "s")], [W_(115, "sh")]], end=CUT(VT(116)))
cap([[W_(116, "s"), W_(117, "s"), W_(118, "s"), W_(119, "s")]], y=180, end=CUT(VT(121)))

# ---- S13  57.76-62.08  "But it was all a premise for the greatest comeback in the history of Wall Street."
s = Scene("s13", CUT(VT(121)), CUT(VT(137)))
s.v("BANK", 36.6, CUT(VT(121)), CUT(VT(126)), push=(1.0, 1.05))     # But it was all a: Dimon, thinking
s.paper(CUT(VT(126)), CUT(VT(127)))                                  # premise: the chess hand again (the game)
cam, _ = s.v("P01", 6.40, CUT(VT(126)), CUT(VT(127)), grade="bw", push=None, box=(640 - 260, 540 - 390, 520, 780),
             cam_style="box-shadow:0 26px 60px rgba(0,0,0,0.45);")
s.J(f'tl.fromTo("#{cam}", {{ scale: 1.55 }}, {{ scale: 1.0, duration: 0.28, ease: "power3.out", immediateRender: false }}, {s.at(CUT(VT(126)))});')
s.v("GAME", 61.4, CUT(VT(127)), CUT(VT(130)), push=(1.0, 1.05))     # for the greatest: on stage, arm raised
sp_echo(s, CUT(VT(130)), CUT(VT(130)) + 0.3, "comeback", inv=True)
s.v("MPB", 1468.4, CUT(VT(130)) + 0.3, CUT(VT(131)), push=(1.0, 1.06))   # he walks back in
s.streak(CUT(VT(130)) + 0.3, frames=4)
sp_wall(s, CUT(VT(131)), CUT(VT(137)), WALL)
cap([[W_(121, "s"), W_(122, "s"), W_(123, "s"), W_(124, "s"), W_(125, "s")]], end=CUT(VT(126)))
cap([[W_(126, "ps")]], x=1330, y=600, end=CUT(VT(127)))
cap([[W_(127, "s"), W_(128, "s"), W_(129, "s")]], end=CUT(VT(130)))
cap([[W_(131, "s"), W_(132, "s"), W_(133, "s"), W_(134, "s")], [W_(135, "sx"), W_(136, "sx")]], end=CUT(VT(137)), exit="blur")

# ---- S14  62.08-65.32  "In 2000, he takes over a broken bank in Chicago,"
s = Scene("s14", CUT(VT(137)), CUT(VT(147)))
ty = sp_typed(s, CUT(VT(137)), CUT(VT(139)), [("In", VT(137), 150, 330, 250), ("2000", VT(138), 520, 250, 360)])
s.J(f'tl.set("#{ty}", {{ scale: 1.5, x: -120, y: -60 }}, {s.at(CUT(VT(137)))});')
s.J(f'tl.set("#{ty}", {{ scale: 1.15, x: -60, y: -40 }}, {s.at(VT(138) + 0.12)});')
s.J(f'tl.set("#{ty}", {{ scale: 1.0, x: 30, y: -10 }}, {s.at(VT(138) + 0.36)});')
montage(s, [
    (CUT(VT(139)), "MPB", 1446.2),                    # he takes over: Dimon at Bank One
    (CUT(VT(143)), "MPB", 1192.2),                    # a broken bank
    (CUT(VT(145)), "MPB", 1248.0),                    # in: Chicago from the air
], CUT(VT(146)))
for gt0, gt1 in ((VT(143) - 0.02, VT(143) + 4 * F1), (VT(143) + 0.3, VT(143) + 0.3 + 2 * F1)):
    s.v("MPB", 1192.2 + (gt0 - CUT(VT(143))), gt0, gt1, grade="glitch", push=None, z=s.nz() + 40)
s.img(CHI_TOWER, CUT(VT(146)), CUT(VT(147)), push=(1.0, 1.07))       # Chicago: the Bank One tower
s.neg(CUT(VT(139)), 1)
cap([[W_(139, "s"), W_(140, "s"), W_(141, "s"), W_(142, "s")], [W_(143, "sh"), W_(144, "sh")]], end=CUT(VT(145)))
cap([[W_(145, "s")], [W_(146, "b")]], end=CUT(VT(147)))

# ---- S15  65.32-67.14  "cuts the dividend, cleaned it up,"
s = Scene("s15", CUT(VT(147)), CUT(VT(153)))
sp_slice(s, "MPB", 1446.0, CUT(VT(147)), CUT(VT(150)), cut_at=VT(149) + 0.06)
sp_wipe(s, "MPB", 1323.0, CUT(VT(150)), CUT(VT(153)), wipe_at=VT(152) - 0.06)
cap([[W_(147, "s"), W_(148, "s")], [W_(149, "sh")]], end=CUT(VT(150)))
cap([[W_(150, "s"), W_(151, "s")], [W_(152, "sh")]], end=CUT(VT(153)))

# ---- S16  67.14-70.73  "and puts $60 million of his own money into the stock."
s = Scene("s16", CUT(VT(153)), CUT(VT(164)))
s.v("P10", 1.5, CUT(VT(153)), CUT(VT(157)), grade="warm", push=(1.0, 1.06))
s.black(CUT(VT(153)), CUT(VT(157)), color="rgba(5,5,5,0.55)", tex=False)
sp_counter(s, CUT(VT(155)), CUT(VT(157)), [("$60", VT(155)), ("$60,000", VT(155) + 0.14), ("$60,000,000", VT(156))])
cam, _ = s.img(BILL, CUT(VT(157)), CUT(VT(161)), grade="warm", push=(1.0, 1.04))   # of his own money: his own hundreds
s.punch(cam, VT(160), 1.4, origin="50% 45%")
montage(s, [
    (CUT(VT(161)), "HOW", 1023.2),                    # into the stock
    (CUT(VT(163)), "BANK", 757.9),
], CUT(VT(164)))
cap([[W_(153, "s"), W_(154, "s")]], end=CUT(VT(155)))
cap([[W_(157, "s"), W_(158, "s")], [W_(159, "sh"), W_(160, "sh")]], end=CUT(VT(161)), scrim=0.45)
cap([[W_(161, "s"), W_(162, "s")], [W_(163, "sh")]], end=CUT(VT(164)))

# ---- S17  70.73-74.50  "Turn a $500 million loss into billions in profit."  (the AMD data page)
s = Scene("s17", CUT(VT(164)), CUT(VT(173)), ground="#F2E8D6")
pg = s.uid("page")
X0, X1, Y0, YS = 360, 1560, 640, 112
pts = [(2000, -0.511), (2001, 2.64), (2002, 3.30), (2003, 3.54)]
P = [(X0 + (yr - 2000) * (X1 - X0) / 3, Y0 - v * YS) for yr, v in pts]
path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in P)
seglen = sum(math.dist(P[k], P[k + 1]) for k in range(3))
PAGE0, LOSS, INTO, BILL_T = CUT(VT(164)), VT(168), VT(169), VT(170)
years = "".join(f'<text x="{x:.0f}" y="{Y0 + 236}" text-anchor="middle" font-family="Satoshi" font-weight="500" '
                f'font-size="34" fill="#2A2622">{yr}</text>' for (yr, _), (x, _) in zip(pts, P))
dots = "".join(f'<circle id="{pg}-d{k}" cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#E5381B" opacity="0" />' for k, (x, y) in enumerate(P))
s.raw(f'<div id="{pg}" class="clip grp" {s.timed(PAGE0, CUT(VT(173)))} data-track-index="4" data-layout-allow-overflow '
      f'style="background:#F2E8D6;z-index:{s.nz()}"><img class="tex" src="assets/tex/ht_warm.jpg" alt="" style="mix-blend-mode:multiply;opacity:0.42" />'
      f'<div id="{pg}-cam" class="grp" style="transform-origin:{P[3][0]:.0f}px {P[3][1]:.0f}px">'
      f'<div class="t" style="left:{X0 - 6}px;top:150px;font-family:\'Instrument Serif\';font-style:italic;font-size:92px;color:#14110F">Bank One</div>'
      f'<div class="t" style="left:{X0}px;top:258px;font-family:Satoshi;font-weight:500;font-size:34px;color:#4A433C">net income, 2000 - 2003</div>'
      f'<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0">'
      f'<line x1="{X0 - 80}" y1="{Y0}" x2="{X1 + 80}" y2="{Y0}" stroke="#2A2622" stroke-width="2" stroke-dasharray="10 10" opacity="0.55" />'
      f'{years}<path id="{pg}-line" d="{path}" fill="none" stroke="#E5381B" stroke-width="9" stroke-linecap="round" '
      f'stroke-linejoin="round" stroke-dasharray="{seglen:.1f}" stroke-dashoffset="{seglen:.1f}" />{dots}</svg>'
      f'<div id="{pg}-loss" class="t" style="left:{P[0][0] + 34:.0f}px;top:{P[0][1] + 14:.0f}px;font-family:\'Instrument Serif\';'
      f'font-style:italic;font-size:84px;color:#E5381B;opacity:0">-$500M <span style="font-family:Satoshi;font-style:normal;'
      f'font-weight:500;font-size:34px;color:#2A2622">loss</span></div>'
      f'<div id="{pg}-prof" class="t" style="left:{P[3][0] - 330:.0f}px;top:{P[3][1] - 150:.0f}px;font-family:\'Instrument Serif\';'
      f'font-style:italic;font-size:118px;color:#14110F;opacity:0">+$3.5B <span style="font-family:Satoshi;font-style:normal;'
      f'font-weight:700;font-size:40px;color:#14110F">profit</span></div></div></div>',
      [f'tl.fromTo("#{pg}-d0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, immediateRender: false }}, {s.at(VT(166) - F1)});',
       f'tl.fromTo("#{pg}-loss", {{ opacity: 0, x: -18 }}, {{ opacity: 1, x: 0, duration: 0.18, ease: "power3.out", immediateRender: false }}, {s.at(LOSS - F1)});',
       f'tl.fromTo("#{pg}-line", {{ strokeDashoffset: {seglen:.1f} }}, {{ strokeDashoffset: 0, duration: {r3(BILL_T + 0.22 - INTO)}, ease: "power2.inOut", immediateRender: false }}, {s.at(INTO)});']
      + [f'tl.fromTo("#{pg}-d{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06, immediateRender: false }}, {s.at(INTO + (BILL_T + 0.22 - INTO) * (k / 3) ** 0.9)});' for k in (1, 2, 3)]
      + [f'tl.fromTo("#{pg}-prof", {{ opacity: 0, x: 18 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out", immediateRender: false }}, {s.at(BILL_T + 0.2)});',
         f'tl.fromTo("#{pg}-cam", {{ scale: 1.0 }}, {{ scale: 1.22, duration: {r3(CUT(VT(173)) - PAGE0)}, ease: "power2.in" }}, {s.at(PAGE0)});'])
s.whiteframe(PAGE0, 1)

# ---- S18  74.50-77.67  "That bank got acquired by JP Morgan in 2004."
s = Scene("s18", CUT(VT(173)), CUT(VT(182)))
s.v("HOW", 697.0, CUT(VT(173)), CUT(VT(177)), grade="crt", push=(1.0, 1.04))   # That bank got acquired: the Fox report
sp_merge(s, CUT(VT(177)), CUT(VT(180)), LOGO["bankone"], LOGO["jpm"], LOGO["jpmc08"], merge_at=VT(179))
sp_roller(s, CUT(VT(180)), CUT(VT(182)), [2000, 2001, 2002, 2003, 2004], land_at=VT(181) + 0.05, cards=CARDS_04,
          video_bg=("HOW", 692.6))
cap([[W_(173, "s"), W_(174, "s"), W_(175, "s")], [W_(176, "b")]], y=545, end=CUT(VT(177)))
cap([[W_(177, "s")], [W_(178, "nm", "JP"), W_(179, "nm", "Morgan")]], y=880, end=CUT(VT(180)))

# ---- S19  77.67-80.19  "Then, 2008 financial crisis hit,"
s = Scene("s19", CUT(VT(182)), CUT(VT(187)))
s.v("HOW", 698.0, CUT(VT(182)), CUT(VT(183)), grade="bw", push=(1.0, 1.05), xyz=(0.36, 0.27, 3.0))   # Then: the hourglass
sp_roller(s, CUT(VT(183)), CUT(VT(184)), [2004, 2005, 2006, 2007, 2008], land_at=VT(183) + 0.18, cards=CARDS_0408,
          video_bg=("HOW", 793.0))
montage(s, [
    (CUT(VT(184)), "CRASH", 72.5, {"grade": "crt"}),  # financial: Fox, the Dow falls 733
    (CUT(VT(185)), "STO", 1438.6),                    # crisis: Lehman
    (CUT(VT(186)), "P02", 1.2, {"grade": "warm"}),    # hit: the room on fire
], CUT(VT(187)))
s.flash(VT(186), d=0.22)
s.neg(CUT(VT(184)), 2)
cap([[W_(182, "s")]], y=880, end=CUT(VT(183)))
cap([[W_(184, "s")], [W_(185, "sh"), W_(186, "b")]], end=CUT(VT(187)))

# ---- S20  80.19-82.04  "and when every other bank was dying,"
s = Scene("s20", CUT(VT(187)), CUT(VT(194)))
fl = [("img", CRISIS_PICS[0]), ("v", "MPB", 1891.2), ("img", CRISIS_PICS[2]), ("v", "HOW", 1010.6), ("v", "GAME", 409.6),
      ("v", "STO", 346.2), ("v", "STO", 30.4), ("img", CRISIS_PICS[3]), ("v", "STO", 1723.0), ("img", CRISIS_PICS[4])]
t = CUT(VT(187))
dy = CUT(VT(193))
step = (dy - t) / len(fl)
for k, it in enumerate(fl):
    te = t + step
    if it[0] == "img":
        s.img(it[1], t, te, grade="bw" if k % 2 else "doc", push=None)
    else:
        s.v(it[1], it[2], t, te, grade="bw" if k % 2 else "doc", push=None)
    if k % 3 == 1:
        s.neg(t, 1)
    t = te
s.v("STO", 2294.6, CUT(VT(193)), CUT(VT(194)), push=(1.0, 1.05))   # dying
cap([[W_(187, "s"), W_(188, "s"), W_(189, "s"), W_(190, "s"), W_(191, "s"), W_(192, "s")], [W_(193, "sh")]], end=CUT(VT(194)))

# ---- S21  82.04-83.50  "he was the only one standing"
s = Scene("s21", CUT(VT(194)), CUT(VT(200)))
s.black(CUT(VT(194)), CUT(VT(199)), color="#030303", tex=False)
s.v("P11", 0.9, CUT(VT(194)), CUT(VT(199)), grade="doc", push=(1.0, 1.05), box=(560, 0, 800, 1080), size=(800, 1080),
    xyz=(0.5, 0.5, 1.0))
s.v("MPB", 1916.6, CUT(VT(199)), CUT(VT(200)), push=(1.0, 1.05))
s.flash(VT(199), d=0.2)
cap([[W_(194, "s"), W_(195, "s"), W_(196, "s")], [W_(197, "b"), W_(198, "b")]], y=880, end=CUT(VT(199)))
cap([[W_(199, "sx")]], y=850, end=CUT(VT(200)))

# ---- S22  83.50-86.11  "with enough money to buy the ones that fell."
s = Scene("s22", CUT(VT(200)), CUT(VT(209)))
montage(s, [
    (CUT(VT(200)), "P06", 1.0),                       # with enough money: pallets of cash lifted off the Fed
    (CUT(VT(203)), "UNT", 1157.6, {"grade": "crt"}),  # to buy: 'Fire Sale'
    (CUT(VT(205)), "MPB", 1890.4),                    # the ones: Bear Stearns
    (CUT(VT(206)), "HOW", 1010.8),                    # Washington Mutual
], CUT(VT(207)))
sp_cards_fall(s, CUT(VT(207)), CUT(VT(209)), [("logo", LOGO["lehman"]), ("logo", LOGO["wamu"]), ("photo", CRISIS_PICS[1])],
              fall_at=VT(208))
cap([[W_(200, "s"), W_(201, "s")], [W_(202, "sh")]], end=CUT(VT(203)))
cap([[W_(203, "s"), W_(204, "s"), W_(205, "s"), W_(206, "s")]], end=CUT(VT(207)))
cap([[W_(207, "p")], [W_(208, "ps")]], y=230, end=CUT(VT(209)))

# ---- S23  86.11-93.20  "That's JP Morgan and Chase, the name that moves $10 trillion every single day today."
s = Scene("s23", CUT(VT(209)), DUR)
montage(s, [
    (CUT(VT(209)), "MPB", 1517.6),                    # That's JP: the stone sign
    (CUT(VT(211)), "GAME", 109.6),                    # Morgan: the glass door
    (CUT(VT(212)), "GAME", 202.8),                    # and Chase: the blue signs
], CUT(VT(213)))
sp_logo_wipe(s, CUT(VT(213)), CUT(VT(214)), LOGO["jpmc"])
montage(s, [
    (CUT(VT(214)), "BANK", 750.8),                    # the name that moves: the NYSE board
    (CUT(VT(216)), "BANK", 756.6),
], CUT(VT(218)))
sp_screens(s, CUT(VT(218)), CUT(VT(220)), [("BANK", 756.0), ("BANK", 761.0), ("HOW", 1024.0), ("BANK", 759.6),
                                          ("HOW", 1026.5), ("BANK", 763.6), ("CRASH", 160.0), ("HOW", 1022.6), ("BANK", 757.9)])
s.v("P10", 3.2, CUT(VT(218)), CUT(VT(220)), push=(1.0, 1.08), vstyle="mix-blend-mode:screen;opacity:0.55;")
s.black(CUT(VT(218)), CUT(VT(220)), color="rgba(0,0,0,0.42)", tex=False)
sp_counter(s, CUT(VT(218)), CUT(VT(220)), [("$10", VT(218)), ("$10,000,000", VT(218) + 0.18),
                                         ("$10,000,000,000,000", VT(219))], x=0, size=200, align="center")
montage(s, [
    (CUT(VT(220)), "P07", 2.0),
    (CUT(VT(221)), "BANK", 744.6),
    (CUT(VT(222)), "GAME", 128.9),                    # day: the floor at work
], CUT(VT(223)))
TODAY_END = round(VOW[223]["end"] + VO2_OFF + 0.35, 3)
ty = sp_typed(s, CUT(VT(223)), TODAY_END, [("Today", VT(223), 420, 300, 330)])
s.v("BANK", 1031.4, TODAY_END, DUR, push=(1.0, 1.08))
s.neg(TODAY_END, 2)
fd = s.uid("fade")
s.raw(f'<div id="{fd}" class="clip grp" {s.timed(DUR - 0.75, DUR)} data-track-index="6" style="background:#000;opacity:0;'
      f'z-index:{s.nz() + 900}"></div>',
      [f'tl.fromTo("#{fd}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.62, ease: "power1.in", immediateRender: false }}, {s.at(DUR - 0.75)});'])
cap([[W_(209, "s")], [W_(210, "nm", "JP"), W_(211, "nm", "Morgan")]], end=CUT(VT(212)))
cap([[W_(212, "s")], [W_(213, "sh")]], end=CUT(VT(213)))
cap([[W_(214, "s"), W_(215, "s"), W_(216, "s"), W_(217, "s")]], end=CUT(VT(218)))
cap([[W_(220, "s"), W_(221, "s"), W_(222, "sh")]], y=860, end=CUT(VT(223)))

# ---- negative-flash rhythm (Fink: one every few seconds, on cuts that change world)
for sc_, t_ in ((SCENES[2], CUT(VT(13))), (SCENES[4], CUT(VT(38))), (SCENES[8], CUT(VT(83))), (SCENES[11], CUT(VT(113))),
                (SCENES[13], CUT(VT(145))), (SCENES[15], CUT(VT(161))), (SCENES[21], CUT(VT(203)))):
    sc_.neg(t_, 1)


# ================================================================================================
# Root
# ================================================================================================
def write_root():
    hosts = []
    for k, sc in enumerate(SCENES):
        hosts.append(f'<div id="{sc.sid}" class="clip" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" '
                     f'data-start="{r3(sc.start)}" data-duration="{r3(sc.dur)}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1920" data-height="1080" style="z-index:{10 + k}"></div>')
    hosts.append(f'<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{r3(DUR)}" data-track-index="3" data-track-kind="captions" '
                 f'data-width="1920" data-height="1080" style="z-index:100"></div>')
    auds = [("news", "news_voice.wav", 0.0, 8.81, 0.0, 0.0, 0.02),
            ("music", "music_bed.wav", 0.0, DUR, 0.0, 0.0, 0.05),
            ("vo-a", "vo.wav", VO1_AT, VO1_OUT - VO1_IN, VO1_IN, 0.0, 0.06),
            ("dimon", "dimon_quote.wav", QUOTE_AT, 11.25, QUOTE_SRC0 - 272.5, 0.02, 0.06),
            ("vo-b", "vo.wav", round(VO2_IN + VO2_OFF, 3), VO2_OUT - VO2_IN, VO2_IN, 0.0, 0.08)]
    a_html = []
    lane = {"music": 11}
    for aid, src, st, d, ms, fi, fo in auds:
        fin = f' data-fade-in="{fi}"' if fi else ""
        a_html.append(f'<audio id="{aid}" class="clip" src="assets/audio/{src}" data-start="{r3(st)}" data-duration="{r3(d)}" '
                      f'data-media-start="{r3(ms)}" data-volume="1"{fin} data-fade-out="{fo}" data-track-index="{lane.get(aid, 10)}"></audio>')
    open(f"{PRJ}/index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #070707; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; background: #070707; }}
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
""")


if __name__ == "__main__":
    json.dump(MEDIA, open(f"{PRJ}/tools/media_v3.json", "w"), indent=1)
    if "--specs" in sys.argv:
        print("clips:", len(MEDIA["clips"]), "stills:", len(MEDIA["stills"]))
        sys.exit(0)
    os.makedirs(COMP, exist_ok=True)
    for f in os.listdir(COMP):
        if f.endswith(".html"):
            os.remove(f"{COMP}/{f}")
    for sc in SCENES:
        sc.write()
    n = build_captions()
    write_root()
    print("scenes:", [(sc.sid, sc.start, sc.end) for sc in SCENES])
    print("caption groups:", n, "clips:", len(MEDIA["clips"]), "stills:", len(MEDIA["stills"]))
