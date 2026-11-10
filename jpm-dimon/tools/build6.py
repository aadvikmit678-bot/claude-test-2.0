#!/usr/bin/env python3
"""v6 -- Jamie Dimon / JPMorgan Chase (1920x1080, 30 fps, 93.2 s): the v6 notes on 0-20.86 s; from 20.86 s exactly v5.

v6 over v5 (0-20.86 s only; s05-s23, grain and the caption groups from 20.86 s are byte-identical to v5):
- "JPMorgan Chase" is one continuous type-on at Dario's DISAPPEAR rate (a letter every 2 frames, the newest letter
  flaring for one frame with a haze), from the reporter's "JP"; it holds 9 frames and leaves through Dario's inverted
  sky-blue tiles (frames 253-254); S2_0 = 8.50 is the next picture's first frame (until S02's cyber portrait takes it,
  the tower holds 8.50-8.60 and v5's slide-up of Dimon follows).
- S03: the Stanford shot is a straight cut (no slide, no pan); the CEO window and the Wolf arrival are as v5.
- S04: "a guy who got FIRED" flips through nine photos of young Dimon (tools/prep6.py), two frames each, youngest
  first, each popping in slightly and settling back while the card and its corner dots grow smoothly, then the B&W
  hero lands on "fired" (sp_fired_flip; v5 had three photos and three size jumps). FIRED and the push are as v5.
- S04: "by his own mentor" is a centred Instrument Serif caption (the film's serif animation) over Sandy Weill's faces.
- FR(n): frame-exact times; caption groups from 20.86 s keep their v5 ids.

v5 -- v4 checked frame by frame against every reference.

v5 over v4 (each matched to the reference frames, REFERENCES.md): Dario's two glitch frames before BIGGER; letters typed
evenly across each spoken word; Hemant's see-through grey silhouette, the live strip through it and the inverted band
through the right-hand word; borderless photo cards after soft glowing (and one red) boxes; the Ackman words blurring in
place, a block glitch into the Wolf, a punch-in and a white frame out; the was-fired page pushes in hard after FIRED;
the Fink screen's glitch boxes, glint and white-block wipe in S06.

v4 notes:

v4 over v3:
- Type: two families only, Instrument Serif (regular, glow) and Inter Tight (the Helvetica role). No italics, no
  Satoshi. A caption line keeps one family; lines no longer slide to re-centre as words arrive (each word lands in its
  final place); captions can sit left or right of the subject.
- The Bloomberg open is re-cut: "The name of the game in American capitalism, is being big, and no one is bigger
  [0.5 s held] on Wall Street than JPMorgan Chase." (tools/make_music.py); word times measured on the new voice track.
- S01: trading floor on "game"; BIG is simply there (negative flash, no zoom); "bigger" is Dario's SUDDENLY with glow;
  "on Wall Street" lands word by word, big; JPMORGAN CHASE is typed letter by letter (Dario's DISAPPEAR) over
  JPMorgan images; then Dimon pops up from the centre as a glowing cut-out.
- S02: Hemant Taneja's opening (his glowing silhouette flickering with live frames, words left and right), then an
  interview that pauses and pops him forward with glow, the presidential seal behind his head, photo cards landing.
- S03: real video only, captions beside the subject, the Ackman reel's "real Wolf of Wall Street" lockup on the
  user's Wolf of Wall Street shot (the dollar bill).
- S04: the four-square faster with the user's money asset (top right), the user's "over a bonus" cartoon, the
  Weill photo reframed so his daughter comes into it on "family grudge".
- No visual styles on untimed wrappers (v3's "square": a box-shadow on an untimed camera wrapper showed all scene).

Run:  cd jpm-dimon && python3 -I -X utf8 tools/build6.py --specs                  (writes tools/media_v6.json only)
      python3 -I tools/prep2.py --spec=media_v6.json && CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I tools/prep6.py
      CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I -X utf8 tools/build6.py   (index.html, compositions/)
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


QUOTE = load(f"{TX}/pk_bank/transcript.json")
QUOTE.insert(25, dict(text="You", start=8.62, end=8.76))
QUOTE = snap(QUOTE, envelope(f"{TX}/bank_quote.wav"), -50, -34)
VOW = snap(load(f"{TX}/pk_vo/transcript.json"), envelope(f"{ROOT}/dimon-work/vo/vo16k.wav"), -55, -35)

VO1_AT, VO1_IN, VO1_OUT = 9.05, 0.00, 14.10
VO2_IN, VO2_OUT = 18.40, 75.00
VO2_OFF = round(35.25 - VOW[55]["start"], 3)
QUOTE_AT, QUOTE_SRC0 = 23.60, 273.05
QUOTE_OFF = round(QUOTE_AT - (QUOTE_SRC0 - 272.5), 3)
# the re-cut open (tools/make_music.py): Parakeet's word order (dimon-work/tx/pk_news4), starts read off the new
# voice track's envelope (10 ms frames); 5.70-6.20 is the held silence after "bigger"
NEWS = [dict(text=w, start=t) for w, t in [
    ("The", 0.58), ("name", 0.68), ("of", 0.80), ("the", 0.90), ("game", 0.99), ("in", 1.36), ("American", 1.60),
    ("capitalism,", 2.06), ("is", 3.05), ("being", 3.16), ("big,", 3.50), ("and", 4.08), ("no", 4.28), ("one", 4.60),
    ("is", 4.76), ("bigger", 5.11), ("on", 6.21), ("Wall", 6.29), ("Street", 6.50), ("than", 6.78), ("JP", 7.28),
    ("Morgan", 7.61), ("Chase.", 7.97)]]
NEWS_DUR = 8.88


def NT(i):
    return NEWS[i]["start"]


def VT(i):
    s = VOW[i]["start"]
    return round(s + VO1_AT - VO1_IN, 3) if s < 14.2 else round(s + VO2_OFF, 3)


def QT(i):
    return round(QUOTE[i]["start"] + QUOTE_OFF, 3)


def CUT(t):
    return round(t - LEAD, 3)


def FR(n):
    """Film frame n (30 fps) as a time half a frame early, so a tl.set or a clip edge put here lands exactly on frame n
    however the ms rounding falls (v5's exit_at - F1 = 8.4667 rounded to 8.467, past frame 254: its pink exit frame
    never rendered and the clean word showed instead)."""
    return round((n - 0.5) / 30, 3)


# ================================================================================================
# Media registry (prep2.py extracts what is registered here)
# ================================================================================================
MEDIA = {"clips": {}, "stills": {}}
VERT = {"P01", "P03", "P04", "P08", "P11", "RIB", "WALLV", "NYSEV", "JPMV"}
FRAME_OF = {"GAME": "BBG", "BANK": "BBG", "HOW": "CNBC", "UNT": "UNTF", "STO": "SIXTY"}


def CL(key, t, dur, frame=None, size=None, xyz=None, matte=False):
    size = size or ((608, 1080) if key in VERT else (1920, 1080))
    frame = frame or FRAME_OF.get(key, "FULL")
    dur = round(dur + 0.25, 2)
    cid = f"{key}_{int(round(t * 100))}_{int(round(dur * 100))}" + ("v" if size[0] < size[1] else "") + \
          (f"_{frame.lower()}" if frame not in ("FULL", FRAME_OF.get(key, "FULL")) else "") + \
          ("_x" + "_".join(str(int(v * 100)) for v in xyz) if xyz else "")
    MEDIA["clips"][cid] = dict(key=key, t=round(t, 3), dur=dur, frame=frame, size=list(size), frame_xyz=xyz,
                               **({"matte": True} if matte or MEDIA["clips"].get(cid, {}).get("matte") else {}))
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
DOC_D = dict(vignette=0.34, grain=0.07)
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
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-600.woff2') format('woff2'); font-weight: 600; font-style: normal; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-700.woff2') format('woff2'); font-weight: 700; font-style: normal; }
  @font-face { font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-800.woff2') format('woff2'); font-weight: 800; font-style: normal; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Regular.woff2') format('woff2'); font-weight: 400; font-style: normal; }
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
    name = {("Inter Tight", 600): "InterTight-600", ("Inter Tight", 700): "InterTight-700",
            ("Inter Tight", 800): "InterTight-800"}.get((family, weight))
    if family == "Instrument Serif":
        name = "InstrumentSerif-Regular"
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
    def __init__(self, sid, start, end, ground="#070707", tex=(0.10, 0.04)):
        self.sid, self.start, self.end, self.ground = sid, round(start, 3), round(end, 3), ground
        self.tex = tex
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
          cam_style="", origin="50% 50%", xyz=None, vstyle="", size=None, cid_override=None, matte=False):
        """A video shot cut from source `key` at `src_t`, shown over [t0, t1)."""
        rate_v = rate or 1.0
        cid = cid_override or CL(key, src_t, (t1 - t0) * rate_v, frame=frame, xyz=xyz, size=size, matte=matte)
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

    def vfile(self, name, t0, t1, grade="doc", z=None, inner="", origin="50% 50%"):
        """A clip made by tools/prep5.py (assets/clips2/<name>), full frame, with optional children riding on it."""
        cam, vid = self.uid("cam"), self.uid("v")
        self.els.append(
            f'<div class="cam" id="{cam}" style="left:0px;top:0px;width:1920px;height:1080px;z-index:{z or self.nz()};'
            f'transform-origin:{origin}"><video id="{vid}" class="clip" src="assets/clips2/{name}" muted playsinline '
            f'{self.timed(t0, t1)} data-hf-media-start-basis="local" data-media-start="0"{gattr(grade)} data-track-index="2" '
            f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover"></video>{inner}</div>')
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
    mix-blend-mode: screen; opacity: 0.05; }}
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
               f'style="mix-blend-mode:overlay;opacity:{self.tex[0]};z-index:2000" />'
               f'<img id="{self.sid}-tx2" class="clip tex" src="assets/tex/ht_paper.jpg" alt="" data-start="0" '
               f'data-duration="{r3(self.dur)}" data-track-index="9" data-layout-ignore '
               f'style="mix-blend-mode:soft-light;opacity:{self.tex[1]};z-index:2001" />')
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
    w = textw(word, "Inter Tight", 800, size, track=-0.04)
    # dive point: the middle of the first letter's stem
    ox = 960 - w / 2 + size * 0.14
    sc.raw(f'<div id="{mid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'style="background:#000;mix-blend-mode:multiply;z-index:{sc.nz()}"><div id="{mid}-t" class="t" '
           f'style="left:0;width:1920px;top:{540 - size * 0.53:.0f}px;text-align:center;font-family:\'Inter Tight\';font-weight:800;'
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
             '<text x="252" y="170" fill="#fff" font-size="14" font-family="Inter Tight" opacity="0.8">675.800.FFA</text>'
             '<text x="1542" y="750" fill="#fff" font-size="14" font-family="Inter Tight" opacity="0.8">0X2A.JPM</text>')
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
               f'z-index:{sc.nz() + 300}"><div style="position:absolute;left:-3px;top:-42px;padding:4px 10px;background:#B455FF;'
               f'font-family:\'Inter Tight\';font-weight:700;font-size:28px;line-height:1.1;color:#fff;white-space:nowrap">{label}</div></div>',
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
           f'<div class="t" style="left:-120px;width:2160px;top:300px;text-align:center;font-family:\'Inter Tight\';font-weight:800;'
           f'font-size:330px;letter-spacing:-0.04em;color:transparent;-webkit-text-stroke:2.5px rgba(20,16,12,0.11)">'
           f'{esc(name.upper())}</div>'
           f'<div id="{nid}-card" class="card" style="left:{cx - cw // 2}px;top:{cy - ch // 2}px;width:{cw}px;height:{ch}px;'
           f'background:radial-gradient(ellipse at 50% 30%, #2b4f7a 0%, #12263f 60%, #0a1626 100%)">'
           f'<img id="{nid}-cut" src="assets/img2/{cutout}" alt=""{gattr("bw")} style="position:absolute;left:-40px;top:70px;'
           f'width:{cw + 80}px;height:{ch + 60}px;object-fit:cover;object-position:50% 0%" /></div>'
           f'<div id="{nid}-s" class="t" style="left:{cx - cw // 2}px;top:{cy - ch // 2 - 64}px;font-family:\'Inter Tight\';'
           f'font-weight:700;font-size:48px;color:#141210;opacity:0">{esc(small)}</div>'
           f'<div class="t" style="left:{cx - 760}px;width:{760 + cw // 2}px;top:{cy + ch // 2 + 26}px;text-align:right;'
           f'font-family:\'Inter Tight\';font-weight:800;font-size:118px;letter-spacing:-0.035em">{spans}</div></div>',
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
               f'style="left:0;width:1920px;top:{540 - size * 0.56:.0f}px;text-align:center;font-family:\'Inter Tight\';font-weight:800;'
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
               f'top:{540 + size * 0.5:.0f}px;text-align:center;font-family:\'Inter Tight\';font-weight:700;font-size:60px;color:{INK};'
               f'text-shadow:{GLOW_REST};z-index:{sc.nz() + 400}">{esc(label)}</div>',
               [f'tl.fromTo("#{lid}", {{ opacity: 0, filter: "blur(14px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.22, '
                f'ease: "expo.out", immediateRender: false }}, {sc.at(la)});'])


def sp_bars(sc, t0, t1, words, size=110, y=540, exit_at=None, ground="#050505"):
    """Fink's bar write-on: each word waits as a solid white bar in its final place and flips into the word on its
    beat; a white bar sweeps the line away."""
    if ground:
        sc.black(t0, t1, color=ground)
    ws = [textw(w, "Inter Tight", 700, size, track=-0.02) for w, _ in words]
    gap = size * 0.26
    W = sum(ws) + gap * (len(ws) - 1)
    x = 960 - W / 2
    bid = sc.uid("bars")
    inner = []
    for k, ((w, t), ww) in enumerate(zip(words, ws)):
        inner.append(f'<div id="{bid}-b{k}" style="position:absolute;left:{x:.0f}px;top:{y - size * 0.36:.0f}px;width:{ww:.0f}px;'
                     f'height:{size * 0.74:.0f}px;background:{INK};box-shadow:0 0 22px rgba(255,255,255,0.45)"></div>'
                     f'<div id="{bid}-w{k}" class="t" style="left:{x:.0f}px;top:{y - size * 0.62:.0f}px;font-family:\'Inter Tight\';'
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
        inner.append(f'<div class="t" style="left:{x}px;top:{y}px;font-family:\'Inter Tight\';font-weight:800;font-size:{size}px;'
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
    size = int(min(size, room / max(textw(v, "Inter Tight", 800, 1, track=-0.035) for v, _ in steps)))
    for k, (val, a) in enumerate(steps):
        b = steps[k + 1][1] if k + 1 < len(steps) else t1
        cid = sc.uid("cn")
        box = f"left:{x}px;" if align == "left" else "left:0;width:1920px;text-align:center;"
        sc.raw(f'<div id="{cid}" class="clip t" {sc.timed(a, b)} data-track-index="5" data-layout-allow-overflow style="{box}'
               f'top:{y - size * 0.56:.0f}px;font-family:\'Inter Tight\';font-weight:800;font-size:{size}px;letter-spacing:-0.035em;'
               f'color:{INK};text-shadow:0 0 18px rgba(255,255,255,0.6), 0 0 60px rgba(255,255,255,0.25);z-index:{sc.nz() + 400}">'
               f'{esc(val)}</div>')
        if k == 0:
            sc.J(f'tl.fromTo("#{cid}", {{ opacity: 0, filter: "blur(16px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, '
                 f'ease: "expo.out", immediateRender: false }}, {sc.at(a)});')
    if small:
        sid = sc.uid("cs")
        box = f"left:{x + 8}px;" if align == "left" else "left:0;width:1920px;text-align:center;"
        sc.raw(f'<div id="{sid}" class="clip t" {sc.timed(small_at, t1)} data-track-index="5" style="{box}top:{y + size * 0.5:.0f}px;'
               f'font-family:\'Inter Tight\';font-weight:700;font-size:58px;color:{INK};text-shadow:{GLOW_REST};z-index:{sc.nz() + 400}">'
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
            f'color:#FBF8EC;font-family:\'Inter Tight\';font-weight:800;font-size:104px;letter-spacing:0.04em;text-align:center;'
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
# hero words burst in blown-out; lines do not slide (since v4 each word lands in its final place).
# ================================================================================================
# ---- v5 set pieces --------------------------------------------------------------------------------
GR["dim"] = grade(dict(DOC_A, exposure=-0.55, saturation=-0.25), dict(vignette=0.5, grain=0.07), DOC_E)
GR["night"] = grade(dict(DOC_A, exposure=-0.32, saturation=-0.12, contrast=0.2), dict(vignette=0.5, grain=0.07), DOC_E)
GR["clean"] = grade(dict(contrast=0.08, saturation=-0.05), dict(vignette=0.22, grain=0.05), dict(scanlines=0.04))
GR["dark"] = grade(dict(DOC_A, exposure=-0.95, saturation=-0.3), dict(vignette=0.55, grain=0.07), dict(DOC_E, scanlines=0.2))
# Hemant Taneja at 22-25 s: CRT lines over the frame (a little lighter than the reference, per the user), the backdrop
# a heavily defocused copy of his own shot
HCRT = dict(DOC_E, scanlines=0.2, scanlineCount=0.5, scanlineSoftness=1, chromaticAberration=0.02)
GR["hcrt"] = grade(dict(DOC_A, saturation=-0.1, highlights=-0.1), dict(vignette=0.28, grain=0.06), HCRT)
GR["hbg"] = grade(dict(DOC_A, exposure=-0.2, saturation=-0.6, contrast=-0.12), dict(vignette=0.45, grain=0.06),
                  dict(HCRT, blur=0.9))
GR["hcard"] = grade(dict(DOC_A, saturation=-0.3, temperature=-0.08), dict(vignette=0.08, grain=0.05), HCRT)
GR["ghost"] = grade(dict(contrast=0.12, saturation=-1), dict(grain=0.04), dict(blur=0.6))
SPK_XYZ = (0.592, 0.40, 1.15)           # the speaking clip: Dimon centred, head top ~100 px, hands in frame


def blk(sc, t, frames, box, color="#ffffff", blend="normal", opacity=1.0, z=None, soft=0):
    """A flat block for a few frames (the references' glitch boxes); soft > 0 blurs it and gives it a glow."""
    bid = sc.uid("blk")
    x, y, w, h = box
    extra = f"filter:blur({soft}px);box-shadow:0 0 {soft * 9}px {soft * 3}px {color};" if soft else ""
    sc.raw(f'<div id="{bid}" class="clip solid" {sc.timed(t, t + frames * F1)} data-track-index="6" style="left:{x}px;'
           f'top:{y}px;width:{w}px;height:{h}px;background:{color};opacity:{opacity};mix-blend-mode:{blend};{extra}'
           f'z-index:{z or sc.nz() + 700}"></div>')
    return bid


def sp_big_static(sc, t0, t1, word, key, src_t, size=860, grade="doc"):
    """BIG (user notes): the footage seen through the giant word, which is simply there -- no scale-in, no dive."""
    sc.v(key, src_t, t0, t1, grade=grade, push=None)
    mid = sc.uid("mask")
    sc.raw(f'<div id="{mid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'style="background:#000;mix-blend-mode:multiply;z-index:{sc.nz()}"><div class="t" '
           f'style="left:0;width:1920px;top:{540 - size * 0.56:.0f}px;text-align:center;font-family:\'Inter Tight\';'
           f'font-weight:800;font-size:{size}px;letter-spacing:-0.045em;color:#fff">{esc(word)}</div></div>')


def sp_suddenly(sc, t0, t1, word, size=340, echo=520, reps=3):
    """Dario's SUDDENLY (16.56-17.40, every frame at 25 fps): a white square in the top-left corner of the outgoing shot
    for two frames and one in the bottom-right for one; a glitch frame (the word smeared through a pale band while the
    echoes already rush past); one frame of the crisp black word in a glowing white bar; then the white word on black
    between rows of giant, blurred, faint echoes that rush in and slow right down (measured: ~30 px a frame falling to
    ~2), the top row to the left, the bottom row to the right. User: much darker; more echoes, fainter, blurred, moving,
    also at the sides; no small copy; the word keeps its glow."""
    W = word.upper()
    blk(sc, t0 - 3 * F1, 2, (0, 0, 216, 208))
    blk(sc, t0 - F1, 1, (1704, 872, 216, 208))
    eid = sc.uid("sud")
    wy = 540 - size * 0.56
    ww = textw(W, "Instrument Serif", 400, size, track=0.04)
    sep = '<span style="display:inline-block;width:0.42em"></span>'
    row = sep.join([esc(W)] * reps)
    rw = textw(W, "Instrument Serif", 400, echo, track=0.03) * reps + 0.42 * echo * (reps - 1)
    rl = (1920 - rw) / 2
    side = (f'<div id="{eid}-l" class="t" style="left:{960 - ww / 2 - 90 - ww:.0f}px;top:{wy:.0f}px;font-family:\'Instrument Serif\';'
            f'font-size:{size}px;letter-spacing:0.04em;color:rgba(251,248,236,0.17);filter:blur(7px)">{esc(W)}</div>'
            f'<div id="{eid}-r" class="t" style="left:{960 + ww / 2 + 90:.0f}px;top:{wy:.0f}px;font-family:\'Instrument Serif\';'
            f'font-size:{size}px;letter-spacing:0.04em;color:rgba(251,248,236,0.17);filter:blur(7px)">{esc(W)}</div>')
    sc.raw(f'<div id="{eid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="4" data-layout-allow-overflow '
           f'data-layout-allow-overlap style="background:#020202;z-index:{sc.nz()}">'
           f'<div id="{eid}-a" class="t" style="left:{rl:.0f}px;top:{-echo * 0.50:.0f}px;font-family:\'Instrument Serif\';'
           f'font-size:{echo}px;color:rgba(251,248,236,0.30);filter:blur(9px);letter-spacing:0.03em">{row}</div>'
           f'<div id="{eid}-b" class="t" style="left:{rl:.0f}px;top:{1080 - echo * 0.40:.0f}px;font-family:\'Instrument Serif\';'
           f'font-size:{echo}px;color:rgba(251,248,236,0.24);filter:blur(11px);letter-spacing:0.03em">{row}</div>'
           f'{side}'
           f'<div id="{eid}-w" class="t" style="left:0;width:1920px;top:{wy:.0f}px;text-align:center;'
           f'font-family:\'Instrument Serif\';font-size:{size}px;color:{INK};letter-spacing:0.04em;opacity:0;'
           f'text-shadow:{SERIF_REST}">{esc(W)}</div></div>',
           [f'tl.fromTo("#{eid}-a", {{ x: 460 }}, {{ x: -40, duration: 0.85, ease: "expo.out", immediateRender: false }}, {sc.at(t0)});',
            f'tl.to("#{eid}-a", {{ x: -70, duration: {r3(max(F1, t1 - t0 - 0.85))}, ease: "none" }}, {sc.at(t0 + 0.85)});',
            f'tl.fromTo("#{eid}-b", {{ x: -460 }}, {{ x: 40, duration: 0.85, ease: "expo.out", immediateRender: false }}, {sc.at(t0)});',
            f'tl.to("#{eid}-b", {{ x: 70, duration: {r3(max(F1, t1 - t0 - 0.85))}, ease: "none" }}, {sc.at(t0 + 0.85)});',
            f'tl.fromTo("#{eid}-l", {{ x: 60 }}, {{ x: -50, duration: {r3(t1 - t0)}, ease: "power2.out", immediateRender: false }}, {sc.at(t0)});',
            f'tl.fromTo("#{eid}-r", {{ x: -60 }}, {{ x: 50, duration: {r3(t1 - t0)}, ease: "power2.out", immediateRender: false }}, {sc.at(t0)});',
            f'tl.set("#{eid}-w", {{ opacity: 1, filter: "blur(8px)", textShadow: "{SERIF_BLOOM}" }}, {sc.at(t0 + 2 * F1)});',
            f'tl.set("#{eid}-w", {{ filter: "blur(2.5px)", textShadow: "{SERIF_SOFT}" }}, {sc.at(t0 + 3 * F1)});',
            f'tl.set("#{eid}-w", {{ filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {sc.at(t0 + 5 * F1)});'])
    # the two glitch frames: the word smeared through a pale band, then crisp black in a glowing white bar
    for k, smear in enumerate((True, False)):
        gid = sc.uid("sudg")
        word = (f'<div class="t" style="left:0;width:1920px;top:{wy:.0f}px;text-align:center;font-family:\'Instrument Serif\';'
                f'font-size:{size}px;color:#0b0b0b;letter-spacing:0.04em;filter:blur({4 if smear else 0}px);'
                f'transform:scaleY({1.6 if smear else 1})">{esc(W)}</div>')
        band = (f'<div style="position:absolute;left:{420 if smear else 330}px;top:{wy + size * (0.04 if smear else 0.1):.0f}px;'
                f'width:{1080 if smear else 1260}px;height:{size * (0.95 if smear else 0.82):.0f}px;'
                f'background:{"rgba(226,226,226,0.88)" if smear else "#F4F1EA"};'
                f'box-shadow:0 0 70px 26px rgba(255,255,255,{0.35 if smear else 0.6})"></div>')
        sc.raw(f'<div id="{gid}" class="clip grp" {sc.timed(t0 + k * F1, t0 + (k + 1) * F1)} data-track-index="5" '
               f'style="z-index:{sc.nz() + 2}">{band}{word}</div>')


# Dario's DISAPPEAR, re-measured every frame (36.20-38.00 at 25 fps, v6): the flare and the exit tiles
FLARE_TS = "0 0 6px #fff, 0 0 16px #fff, 0 0 36px rgba(255,255,255,0.9)"
CRISP_TS = "0 6px 26px rgba(0,0,0,0.42), 0 0 22px rgba(255,255,255,0.28)"
FLARE_HAZE = ("radial-gradient(closest-side, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0.78) 20%, "
              "rgba(255,255,255,0.55) 28%, rgba(255,255,255,0.42) 36%, rgba(255,255,255,0.3) 48%, "
              "rgba(255,255,255,0.2) 62%, rgba(255,255,255,0.08) 82%, rgba(255,255,255,0) 100%)")
# the exit: tiles that invert whatever is under them, on Dario's ~256 x 190-240 px screen grid (x, y, w, h)
DIS_T1 = [(1130, 0, 258, 187)]                                                          # 37.52: one, above the word
DIS_T2 = [(377, 0, 257, 189), (1130, 0, 258, 187), (1130, 187, 258, 240), (880, 403, 251, 237),
          (378, 630, 260, 237), (378, 867, 260, 213), (1140, 630, 257, 237)]            # 37.56: over the word
DIS_T3 = [(123, 0, 254, 183), (123, 183, 254, 237), (377, 0, 256, 189), (377, 189, 256, 238), (620, 400, 260, 244),
          (880, 400, 256, 244), (1131, 189, 257, 238), (1393, 189, 258, 238), (377, 631, 256, 236),
          (377, 867, 256, 213), (633, 867, 255, 213), (1140, 631, 257, 236), (1140, 867, 257, 213),
          (1644, 631, 256, 236)]                                                         # 37.60: the next picture
DIS_BLUE = "#6fb2f0"   # Dario's tiles over the fire read sky blue (81,159,223 .. 213,245,254); multiplying our
                       # inverted night tower by this gives the same blue, and the inverted letters stay black


def sp_tiles(sc, t, boxes, tint=None, z=1990):
    """One frame of Dario's exit tiles: white in difference blend, so the picture (and any type) under them inverts;
    `tint` multiplies them blue (Dario's 37.52-37.56 tiles)."""
    for b in boxes:
        blk(sc, t, 1, b, "#ffffff", blend="difference", z=z)
        if tint:
            blk(sc, t, 1, b, tint, blend="multiply", z=z + 1)


def sp_type_word(sc, t0, t1, text, times, size=450, squeeze=0.70, base=672, track=-0.015, exit_at=None):
    """Dario's DISAPPEAR (36.64-37.64, every frame at 25 fps): the word typed at one steady rate into its final, centred
    layout from the left -- 9 letters in 13 frames in a (1,2,2) pattern, i.e. a 30 fps type-on at one letter every 2
    frames resampled to 25 fps -- the newest letter flaring for one frame (blown out, a haze lighting the picture ~300 px
    round it, its counters filled), crisp white the next; Dario's letters are 0.735 as wide as Instrument Serif's, the
    gaps 2-9 px; the footage cuts mid-word; the word holds 8 frames, then one inverted tile above it (37.52), tiles over
    it (37.56: its letters go black), and the next picture with tiles (37.60, the word gone; drawn by the next scene).
    User: "JPMorgan Chase", spelt properly, not in capitals; v6: "coming unanimously", one rate, not word by word.
    `times`: one per non-space letter (use FR()); `exit_at`: the next picture's first frame (the word is gone there)."""
    tid = sc.uid("typ")
    total = textw(text, "Instrument Serif", 400, size, track=track)
    x0 = 960 - total / 2
    top = base - size * 0.84        # line-height 1: the baseline sits 0.84 em under the box top (ascent .99, descent .31)
    wz = sc.nz() + 300
    spans, js = [], []
    k = 0
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        x = x0 + textw(text[:i], "Instrument Serif", 400, size, track=track)
        lid = f"{tid}-l{i}"
        spans.append(f'<span id="{lid}" class="t" style="left:{x:.1f}px;top:{top:.0f}px;font-family:\'Instrument Serif\';'
                     f'font-size:{size}px;letter-spacing:{track}em;color:#FFFDF6;opacity:0;text-shadow:{CRISP_TS}">'
                     f'{esc(ch)}</span>')
        a = times[k]
        js += [f'tl.set("#{lid}", {{ opacity: 1, filter: "blur(2.5px)", textShadow: "{FLARE_TS}" }}, {sc.at(a)});',
               f'tl.set("#{lid}", {{ filter: "blur(0px)", textShadow: "{CRISP_TS}" }}, {sc.at(a + F1)});']
        cx = 960 + (x + textw(ch, "Instrument Serif", 400, size) / 2 - 960) * squeeze   # the letter's centre on screen
        sc.raw(f'<div id="{lid}-hz" class="clip" {sc.timed(a, a + F1)} data-track-index="5" data-layout-ignore '
               f'style="position:absolute;left:{cx - 320:.0f}px;top:{base - 0.315 * size - 410:.0f}px;width:640px;'
               f'height:820px;background:{FLARE_HAZE};z-index:{wz - 1}"></div>')
        k += 1
    n = int(round(exit_at * 30)) if exit_at else None
    # the word's last frame is n - 1: its clip ends half a frame before frame n (FR), so the edge cannot round past it
    sc.raw(f'<div id="{tid}" class="clip grp" {sc.timed(t0, FR(n) if n else t1)} data-track-index="5" '
           f'data-layout-allow-overflow style="z-index:{wz};transform:scaleX({squeeze});transform-origin:960px 540px">'
           f'{"".join(spans)}</div>', js)
    if n:
        sp_tiles(sc, FR(n - 2), DIS_T1, tint=DIS_BLUE)      # Dario 37.52: one tile above the word
        sp_tiles(sc, FR(n - 1), DIS_T2, tint=DIS_BLUE)      # Dario 37.56: tiles over the word, its letters black
    return tid


def sp_slide_pop(sc, t0, t1, cid, steps=(1080, 700, 400, 190, 70, 14, 0), every=2):
    """User: Dimon slides in from the bottom at a low frame rate with the cut-out glow -- his talking video, matted --
    until he stands exactly where the next scene's silhouette stands (hands in frame); no zoom, no side entry."""
    gid = sc.uid("pop")
    js = [f'tl.set("#{gid}", {{ y: {y} }}, {sc.at(t0 + k * every * F1)});' for k, y in enumerate(steps)]
    sc.raw(f'<div id="{gid}" class="grp" style="z-index:{sc.nz() + 40}">'
           f'<video id="{gid}-h" class="clip" src="assets/clips2/{cid}_halo.webm" muted playsinline {sc.timed(t0, t1)} '
           f'data-hf-media-start-basis="local" data-media-start="0" data-track-index="5" style="position:absolute;left:0;top:0;'
           f'width:1920px;height:1080px;opacity:0.95"></video>'
           f'<video id="{gid}-c" class="clip" src="assets/clips2/{cid}_cut.webm" muted playsinline {sc.timed(t0, t1)} '
           f'data-hf-media-start-basis="local" data-media-start="0"{gattr("doc")} data-track-index="5" style="position:absolute;'
           f'left:0;top:0;width:1920px;height:1080px"></video></div>', js)
    return gid


def sp_hemant_open(sc, t0, t1, name, live, grey_until):
    """Hemant Taneja's opening (0.00-1.67, every frame at 24 fps): the subject held as a silhouette over his darkened
    frame -- pale grey and see-through at first (his face shows faintly), opaque cream with a glow from ~0.67 s -- with
    his live picture showing through for a frame or a few (the clip underneath plays on)."""
    edges = [t0]
    for a, n in live:
        edges += [a, a + n * F1]
    edges.append(t1)
    for a, b in zip(edges[0::2], edges[1::2]):
        if b - a < F1 / 2:
            continue
        seg = sc.uid("hs")
        look = "opacity:0.86;filter:brightness(0.78) saturate(0.5);" if a < grey_until else "opacity:0.97;"
        sc.raw(f'<img id="{seg}-f" class="clip" src="assets/img2/{name}_f.jpg" alt="" {sc.timed(a, b)} data-track-index="3"'
               f'{gattr("dark")} style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{sc.nz()}" />'
               f'<img id="{seg}-s" class="clip" src="assets/img2/{name}_sil.png" alt="" {sc.timed(a, b)} data-track-index="4" '
               f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;{look}z-index:{sc.nz()}" />')


def sp_sil_flash(sc, t, name, frames=2):
    """Hemant 21.375-21.417: two frames of the subject as a blazing white silhouette before his shot."""
    fid = sc.uid("silf")
    sc.raw(f'<div id="{fid}" class="clip grp" {sc.timed(t, t + frames * F1)} data-track-index="6" style="z-index:{sc.nz() + 650}">'
           f'<img src="assets/img2/{name}_halo.png" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px" />'
           f'<img src="assets/img2/{name}_sil.png" alt="" style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
           f'filter:brightness(1.12)" /></div>')


def sp_hemant_stage(sc, t0, t1, cid, cards, zoom=None, seal_at=None, head=(960, 255)):
    """Hemant Taneja at 21.46-25.08 (every frame at 24 fps): him talking -- matted, sharp, with the cut-out glow --
    over a heavily defocused copy of his own shot; photo cards behind him in the four quadrants (two at head height,
    two at the waist), each landing the frame after a soft glowing box at its spot (white, sometimes red); CRT lines
    over the frame. User: a subtle push on his face on "in America" while everything else holds; the presidential seal
    behind his head."""
    sc.v("SPEAK", 0, t0, t1, grade="hbg", push=(1.34, 1.37), xyz=SPK_XYZ, cid_override=cid)
    hx, hy = head
    if seal_at:
        sl = sc.uid("seal")
        sc.raw(f'<img id="{sl}" class="clip" src="assets/img2/{SEAL}" alt="" {sc.timed(seal_at, t1)} data-track-index="3" '
               f'style="position:absolute;left:{hx - 310}px;top:{hy - 310}px;width:620px;height:620px;opacity:0;z-index:{sc.nz()}" />',
               [f'tl.fromTo("#{sl}", {{ opacity: 0, scale: 0.94 }}, {{ opacity: 0.62, scale: 1.0, duration: 0.24, ease: "power2.out", '
                f'immediateRender: false }}, {sc.at(seal_at)});'])
    for (src, cx, cy, w, h, t, red, until) in cards:
        bid = sc.uid("sbox")
        col = "rgba(232,40,32,0.95)" if red else "rgba(255,253,246,0.97)"
        glow = "rgba(232,40,32,0.7)" if red else "rgba(255,255,255,0.85)"
        sc.raw(f'<div id="{bid}" class="clip solid" {sc.timed(t - 2 * F1, t)} data-track-index="6" style="left:{cx - w // 2}px;'
               f'top:{cy - h // 2}px;width:{w}px;height:{h}px;background:{col};filter:blur(6px);'
               f'box-shadow:0 0 48px 18px {glow};z-index:{sc.nz() + 5}"></div>')
        cdid = sc.uid("hc")
        sc.raw(f'<img id="{cdid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(t, until or t1)} data-track-index="3"'
               f'{gattr("hcard")} style="position:absolute;left:{cx - w // 2}px;top:{cy - h // 2}px;width:{w}px;height:{h}px;'
               f'object-fit:cover;z-index:{sc.nz()}" />')
    gid = sc.uid("stage")
    sc.raw(f'<div id="{gid}" class="grp" style="z-index:{sc.nz() + 20};transform-origin:{hx}px {hy}px">'
           f'<video id="{gid}-h" class="clip" src="assets/clips2/{cid}_halo.webm" muted playsinline {sc.timed(t0, t1)} '
           f'data-hf-media-start-basis="local" data-media-start="0" data-track-index="5" style="position:absolute;left:0;top:0;'
           f'width:1920px;height:1080px;opacity:0.75"></video>'
           f'<video id="{gid}-c" class="clip" src="assets/clips2/{cid}_cut.webm" muted playsinline {sc.timed(t0, t1)} '
           f'data-hf-media-start-basis="local" data-media-start="0"{gattr("hcrt")} data-track-index="5" style="position:absolute;'
           f'left:0;top:0;width:1920px;height:1080px"></video></div>',
           ([f'tl.fromTo("#{gid}", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {r3(zoom[1] - zoom[0])}, ease: "power1.inOut", '
             f'immediateRender: false }}, {sc.at(zoom[0])});'] if zoom else []))
    return gid


def sp_white_wipe(sc, t, frames=3):
    """Hemant 25.08-25.17: the frame washes out under a soft white band sweeping in from the left."""
    wid = sc.uid("wipe")
    sc.raw(f'<div id="{wid}" class="clip" {sc.timed(t, t + frames * F1)} data-track-index="6" style="position:absolute;left:0;'
           f'top:0;width:2600px;height:1080px;background:linear-gradient(90deg,#FFFDF6 0%,#FFFDF6 62%,rgba(255,253,246,0) 100%);'
           f'z-index:{sc.nz() + 800}"></div>',
           [f'tl.fromTo("#{wid}", {{ x: -2400 }}, {{ x: 0, duration: {r3(frames * F1)}, ease: "power2.in", immediateRender: false }}, '
            f'{sc.at(t)});'])


def pan_arrive(sc, cam, t, until, dx=220, s0=1.26, s1=1.03, drift=1.05):
    """Pattinson's run (6.63-6.97): the next shot arrives still moving and decelerates into place (x and scale ease
    together so the frame stays covered), then drifts."""
    sc.J(f'tl.fromTo("#{cam}", {{ x: {dx}, scale: {s0} }}, {{ x: 0, scale: {s1}, duration: 0.34, ease: "power2.out", '
         f'immediateRender: false }}, {sc.at(t)});')
    sc.J(f'tl.to("#{cam}", {{ scale: {drift}, duration: {r3(max(F1, until - t - 0.34))}, ease: "none" }}, {sc.at(t + 0.34)});')


def sp_window_ease(sc, cam, t, until, to=0.64, cards=()):
    """Pattinson's 'generational run' (5.40-6.17, frame-matched): the shot eases back from full frame into a centred
    window (power4.out) and photo cards pop out from behind it in low-frame-rate steps, each after a white box."""
    sc.J(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: {to}, duration: 0.42, ease: "power4.out", immediateRender: false }}, '
         f'{sc.at(t)});')
    sc.J(f'tl.to("#{cam}", {{ scale: {to * 0.985:.4f}, duration: {r3(max(F1, until - t - 0.42))}, ease: "none" }}, {sc.at(t + 0.42)});')
    for (src, cx, cy, w, h, ta, rot) in cards:
        blk(sc, ta - 2 * F1, 2, (cx - w // 2, cy - h // 2, w, h), "#FFFDF6", soft=3, z=sc.nz() + 1)
        cdid = sc.uid("wc")
        sc.raw(f'<img id="{cdid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(ta, until)} data-track-index="3"'
               f'{gattr("doc")} style="position:absolute;left:{cx - w // 2}px;top:{cy - h // 2}px;width:{w}px;height:{h}px;'
               f'object-fit:cover;outline:1px solid rgba(255,255,255,0.3);z-index:{sc.nz()}" />',
               [f'tl.set("#{cdid}", {{ scale: 0.62, rotation: {rot}, x: {(960 - cx) * 0.35:.0f}, y: {(540 - cy) * 0.35:.0f} }}, {sc.at(ta)});',
                f'tl.set("#{cdid}", {{ scale: 0.86, x: {(960 - cx) * 0.12:.0f}, y: {(540 - cy) * 0.12:.0f} }}, {sc.at(ta + 2 * F1)});',
                f'tl.set("#{cdid}", {{ scale: 1.0, x: 0, y: 0 }}, {sc.at(ta + 4 * F1)});'])


def sp_wolf_lockup(sc, t1, words, y=930, size=150, color="#FFFFFF", exit_at=None):
    """The Ackman reel's 'THE REAL WOLF OF WALL STREET' (4.2-7.3, every frame at 25 fps): bold condensed caps, each word
    coming out of a blur in place over ~3 frames, held over the shot (user: not yellow)."""
    lid = sc.uid("wolf")
    ws = [(w.upper(), t, textw(w.upper(), "Inter Tight", 800, size, track=-0.035)) for w, t in words]
    gap = size * 0.24
    total = sum(w for *_, w in ws) + gap * (len(ws) - 1)
    x = 960 - total / 2
    spans, js = [], []
    for k, (w, t, wd) in enumerate(ws):
        sid = f"{lid}-w{k}"
        spans.append(f'<span id="{sid}" class="t" style="left:{x:.0f}px;top:{y - size * 0.78:.0f}px;font-family:\'Inter Tight\';'
                     f'font-weight:800;font-size:{size}px;letter-spacing:-0.035em;color:{color};opacity:0;'
                     f'text-shadow:0 4px 18px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.4)">{esc(w)}</span>')
        js.append(f'tl.fromTo("#{sid}", {{ opacity: 0.0, x: -36, scaleX: 1.08, filter: "blur(14px)" }}, {{ opacity: 1, x: 0, '
                  f'scaleX: 1, filter: "blur(0px)", duration: {r3(3 * F1)}, ease: "power2.out", immediateRender: false }}, {sc.at(t)});')
        x += wd + gap
    sc.raw(f'<div id="{lid}" class="clip grp" {sc.timed(words[0][1] - F1, exit_at or t1)} data-track-index="5" '
           f'data-layout-allow-overflow style="z-index:1500">{"".join(spans)}</div>', js)
    return lid


def sp_fired_paper(sc, t0, t1, photos, words, big, cx=1000, cy=560, gap=30, dot=13, push_to=1.3):
    """The was-fired reference's opening ('this guy was REJECTED', every frame at 25 fps): window-lit paper; a square
    photo with four dots just off its corners; each new photo replaces the last at a larger size on the same frame (no
    tween); the spoken words stacked in black Helvetica on its left, the block's edge following the photo; the last
    photo lands big with a zoom blur and the big word on its right; then the page pushes in hard and drifts."""
    sc.paper(t0, t1)
    cam = sc.uid("fp")
    inner, js = [], []
    sizes = [p[2] for p in photos]
    for k, (src, a, size) in enumerate(photos):
        b = photos[k + 1][1] if k + 1 < len(photos) else t1
        pid = f"{cam}-p{k}"
        inner.append(f'<img id="{pid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(a, b)} data-track-index="4"'
                     f'{gattr("clean")} style="position:absolute;left:{cx - size // 2}px;top:{cy - size // 2}px;width:{size}px;'
                     f'height:{size}px;object-fit:cover;box-shadow:0 10px 26px rgba(0,0,0,0.26), 0 2px 6px rgba(0,0,0,0.2)" />')
        if k == len(photos) - 1:  # the hero arrives with a two-frame zoom blur
            js.append(f'tl.fromTo("#{pid}", {{ scale: 0.84, filter: "blur(8px)" }}, {{ scale: 1.0, filter: "blur(0px)", '
                      f'duration: {r3(2 * F1)}, ease: "power2.out", immediateRender: false }}, {sc.at(a)});')
    for j, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        did = f"{cam}-d{j}"
        inner.append(f'<div id="{did}" class="clip" {sc.timed(t0, t1)} data-track-index="4" style="position:absolute;'
                     f'left:{cx - dot // 2}px;top:{cy - dot // 2}px;width:{dot}px;height:{dot}px;border-radius:50%;'
                     f'background:#141414"></div>')
        for k, (src, a, size) in enumerate(photos):
            off = size / 2 + 28
            js.append(f'tl.set("#{did}", {{ x: {sx * off:.1f}, y: {sy * off:.1f} }}, {sc.at(a)});')
    wsz, lh = 56, 56 * 0.98
    widths = [textw(w, "Inter Tight", 700, wsz, track=-0.03) for w, _ in words]
    bw = max(widths)
    blk_id = f"{cam}-wb"
    btop = cy - len(words) * lh / 2 - lh * 0.1
    spans = []
    for k, (w, a) in enumerate(words):
        wid = f"{cam}-w{k}"
        spans.append(f'<span id="{wid}" class="t" style="left:{cx - bw:.0f}px;top:{btop + k * lh:.0f}px;font-family:\'Inter Tight\';'
                     f'font-weight:700;font-size:{wsz}px;letter-spacing:-0.03em;color:#141414;opacity:0">{esc(w)}</span>')
        js.append(f'tl.fromTo("#{wid}", {{ opacity: 0, filter: "blur(5px)" }}, {{ opacity: 1, filter: "blur(0px)", '
                  f'duration: {r3(2 * F1)}, ease: "power2.out", immediateRender: false }}, {sc.at(a)});')
    inner.append(f'<div id="{blk_id}" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" data-layout-allow-overflow>'
                 f'{"".join(spans)}</div>')
    for k, (src, a, size) in enumerate(photos):
        js.append(f'tl.set("#{blk_id}", {{ x: {-(size / 2 + gap):.1f} }}, {sc.at(a)});')
    bwd, bt = big
    hero = sizes[-1]
    bid = f"{cam}-big"
    inner.append(f'<div id="{bid}" class="clip t" {sc.timed(bt, t1)} data-track-index="5" style="left:{cx + hero / 2 + gap:.0f}px;'
                 f'top:{cy - hero / 2 + hero * 0.08:.0f}px;font-family:\'Inter Tight\';font-weight:800;font-size:112px;'
                 f'letter-spacing:-0.035em;color:#141414">{esc(bwd)}</div>')
    js.append(f'tl.fromTo("#{bid}", {{ opacity: 0, x: -26, filter: "blur(8px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", '
              f'duration: 0.12, ease: "power3.out", immediateRender: false }}, {sc.at(bt)});')
    sc.raw(f'<div id="{cam}" class="grp" style="z-index:{sc.nz()};transform-origin:{cx}px {cy}px">{"".join(inner)}</div>',
           js + [f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: {push_to}, duration: 0.3, ease: "power3.out", '
                 f'immediateRender: false }}, {sc.at(bt)});',
                 f'tl.to("#{cam}", {{ scale: {push_to + 0.04}, duration: {r3(max(F1, t1 - bt - 0.3))}, ease: "none" }}, '
                 f'{sc.at(bt + 0.3)});'])


def sp_fired_flip(sc, t0, hero_t, t1, photos, hero, words, big, cx=1000, cy=560, s0=236, s1=362, hs=400, gap=30,
                  dot=13, dot_gap=28, pop=(0.035, 0.011), push_to=1.3):
    """v6 note 4, "a guy who got FIRED" (user: "a lot more [pictures] ... with every picture it zooms in slightly, zooms
    out slightly, till it comes like this at the center"; the was-fired reference's page, 0-1.95 s at 25 fps).
    Window-lit paper; many face-aligned squares of young Dimon, two frames each, youngest first. The card (the photo
    and its four corner dots, which scale with it as in the reference) grows smoothly and continuously from s0 to s1 px
    (sine.in: calm at first, speeding up into the hero), and every photo pops in slightly bigger on its first frame and
    settles back to the growth curve on its second (zoom in, zoom out; the pop shrinks from pop[0] to pop[1] as the growth
    takes over, so the end of the run is one fluid move). The B&W hero then lands at the centre at hs px with a 2-frame
    motion blur, FIRED on its right; the page pushes in hard and drifts, as in v5. The stacked words follow the card's
    left edge (its smooth growth, not the pops). Replaces sp_fired_paper (v5: three photos, three size jumps)."""
    sc.paper(t0, t1)
    cam = sc.uid("fp")
    f0, fh = math.ceil(t0 * 30 - 1e-6), math.ceil(hero_t * 30 - 1e-6)   # first frame of the page, first hero frame
    n = len(photos)
    assert fh - f0 == 2 * n, (f0, fh, n)                                 # two frames a photo, the hero on its word
    T = [t0] + [round((f0 + 2 * k - 0.5) / 30, 3) for k in range(1, n)] + [hero_t]   # cuts half a frame early
    D = round(hero_t - t0, 3)
    inner, js = [], []
    for k, src in enumerate(photos + [hero]):
        pid = f"{cam}-p{k}"
        inner.append(f'<img id="{pid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(T[k], T[k + 1] if k < n else t1)} '
                     f'data-track-index="4"{gattr("clean")} style="position:absolute;left:0;top:0;width:{hs}px;height:{hs}px;'
                     f'object-fit:cover;box-shadow:0 10px 26px rgba(0,0,0,0.26), 0 2px 6px rgba(0,0,0,0.2)" />')
    for j, (ux, uy) in enumerate([(-dot_gap, -dot_gap), (hs + dot_gap, -dot_gap), (-dot_gap, hs + dot_gap),
                                  (hs + dot_gap, hs + dot_gap)]):
        inner.append(f'<div id="{cam}-d{j}" class="clip" {sc.timed(t0, t1)} data-track-index="4" style="position:absolute;'
                     f'left:{ux - dot / 2:.1f}px;top:{uy - dot / 2:.1f}px;width:{dot}px;height:{dot}px;border-radius:50%;'
                     f'background:#141414"></div>')
    # the card: an outer wrapper for the smooth growth, an inner one for the per-photo pop (no visual styles on either;
    # no inline transform either, which GSAP owns: lint gsap_css_transform_conflict)
    card = (f'<div id="{cam}-g" style="position:absolute;left:{cx - hs / 2:.0f}px;top:{cy - hs / 2:.0f}px;width:{hs}px;'
            f'height:{hs}px;transform-origin:50% 50%"><div id="{cam}-u" data-layout-allow-overflow '
            f'style="position:absolute;left:0;top:0;width:{hs}px;height:{hs}px;transform-origin:50% 50%">{"".join(inner)}</div></div>')
    js += [f'tl.fromTo("#{cam}-g", {{ scale: {s0 / hs:.4f} }}, {{ scale: {s1 / hs:.4f}, duration: {r3(D)}, ease: "sine.in", '
           f'immediateRender: false }}, {sc.at(t0)});',
           f'tl.to("#{cam}-g", {{ scale: 1, duration: {r3(2 * F1)}, ease: "power2.out" }}, {sc.at(hero_t)});']
    for k in range(n):   # pop in on the photo's first frame, back on its second (sets at half frames: exact per frame)
        amp = pop[0] + (pop[1] - pop[0]) * k / max(1, n - 1)
        js += [f'tl.set("#{cam}-u", {{ scale: {1 + amp:.4f} }}, {sc.at(T[k])});',
               f'tl.set("#{cam}-u", {{ scale: 1 }}, {sc.at(round((f0 + 2 * k + 0.5) / 30, 3))});']
    js.append(f'tl.fromTo("#{cam}-p{n}", {{ filter: "blur(6px)" }}, {{ filter: "blur(0px)", duration: {r3(2 * F1)}, '
              f'ease: "power2.out", immediateRender: false }}, {sc.at(hero_t)});')
    # the stacked words (as v5), the block's right edge riding the card's smooth growth
    wsz, lh = 56, 56 * 0.98
    bw = max(textw(w, "Inter Tight", 700, wsz, track=-0.03) for w, _ in words)
    btop = cy - len(words) * lh / 2 - lh * 0.1
    spans = []
    for k, (w, a) in enumerate(words):
        wid = f"{cam}-w{k}"
        spans.append(f'<span id="{wid}" class="t" style="left:{cx - bw:.0f}px;top:{btop + k * lh:.0f}px;font-family:\'Inter Tight\';'
                     f'font-weight:700;font-size:{wsz}px;letter-spacing:-0.03em;color:#141414;opacity:0">{esc(w)}</span>')
        js.append(f'tl.fromTo("#{wid}", {{ opacity: 0, filter: "blur(5px)" }}, {{ opacity: 1, filter: "blur(0px)", '
                  f'duration: {r3(2 * F1)}, ease: "power2.out", immediateRender: false }}, {sc.at(a)});')
    wb = (f'<div id="{cam}-wb" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" data-layout-allow-overflow>'
          f'{"".join(spans)}</div>')
    js += [f'tl.fromTo("#{cam}-wb", {{ x: {-(s0 / 2 + gap):.1f} }}, {{ x: {-(s1 / 2 + gap):.1f}, duration: {r3(D)}, '
           f'ease: "sine.in", immediateRender: false }}, {sc.at(t0)});',
           f'tl.to("#{cam}-wb", {{ x: {-(hs / 2 + gap):.1f}, duration: {r3(2 * F1)}, ease: "power2.out" }}, {sc.at(hero_t)});']
    bwd, bt = big   # FIRED and the push: unchanged from v5
    bid = f"{cam}-big"
    fired = (f'<div id="{bid}" class="clip t" {sc.timed(bt, t1)} data-track-index="5" style="left:{cx + hs / 2 + gap:.0f}px;'
             f'top:{cy - hs / 2 + hs * 0.08:.0f}px;font-family:\'Inter Tight\';font-weight:800;font-size:112px;'
             f'letter-spacing:-0.035em;color:#141414">{esc(bwd)}</div>')
    js.append(f'tl.fromTo("#{bid}", {{ opacity: 0, x: -26, filter: "blur(8px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", '
              f'duration: 0.12, ease: "power3.out", immediateRender: false }}, {sc.at(bt)});')
    sc.raw(f'<div id="{cam}" class="grp" data-layout-allow-overflow style="z-index:{sc.nz()};transform-origin:{cx}px {cy}px">'
           f'{card}{wb}{fired}</div>',
           js + [f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: {push_to}, duration: 0.3, ease: "power3.out", '
                 f'immediateRender: false }}, {sc.at(bt)});',
                 f'tl.to("#{cam}", {{ scale: {push_to + 0.04}, duration: {r3(max(F1, t1 - bt - 0.3))}, ease: "none" }}, '
                 f'{sc.at(bt + 0.3)});'])
    return cam


def sp_dario_faces(sc, t0, t1, stills, slots=(3, 2)):
    """Dario's 'every AI tech bro' (17.40-18.40, every frame at 25 fps, measured): a different photo every 2-3 frames,
    every face centred at (960, 505) at close-up size, the edges of each photo zoom-blurred around a sharp circle
    (tools/faces.dario), each photo creeping in ~2-3 % while it is up; four thin white lines frame the face and stay
    fixed on screen (top and bottom 770-1230 at y 194 / 730, sides at x 714 / 1280, y 270-640). v6: no words here --
    the line is a centred serif caption in captions.html (user: "at the center ... in Instrument serif glow")."""
    t, k = t0, 0
    while t < t1 - 1e-6:
        te = min(t1, t + slots[k % len(slots)] * F1)
        fid = sc.uid("df")
        sc.raw(f'<img id="{fid}" class="clip" src="assets/img2/{stills[k % len(stills)]}" alt="" {sc.timed(t, te)} '
               f'data-track-index="3"{gattr("clean")} style="position:absolute;left:0;top:0;width:1920px;height:1080px;'
               f'transform-origin:960px 505px;z-index:{sc.nz()}" />',
               [f'tl.fromTo("#{fid}", {{ scale: 1.0 }}, {{ scale: 1.03, duration: {r3(te - t)}, ease: "none", immediateRender: false }}, '
                f'{sc.at(t)});'])
        t, k = te, k + 1
    lid = sc.uid("brk")
    ln = "position:absolute;background:rgba(255,255,255,0.86);box-shadow:0 0 6px rgba(255,255,255,0.55)"
    sc.raw(f'<div id="{lid}" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" style="z-index:{sc.nz() + 200}">'
           f'<div style="{ln};left:770px;top:193px;width:460px;height:3px"></div>'
           f'<div style="{ln};left:770px;top:729px;width:460px;height:3px"></div>'
           f'<div style="{ln};left:713px;top:270px;width:3px;height:370px"></div>'
           f'<div style="{ln};left:1279px;top:270px;width:3px;height:370px"></div></div>')


def sp_ghost(sc, t0, t1, src, box, segs, opacity=0.45, blend="difference"):
    """The Fink reel's Rogan screen (3.80-6.20, measured at 25 fps): the picture in difference blend, low opacity, slowly
    zooming in (~10 % over 2.3 s) and drifting up-left, and pulling focus from soft to sharp each time it comes back."""
    gid = sc.uid("ghost")
    x, y, w, h = box
    js = [f'tl.fromTo("#{gid}", {{ scale: 1.0, x: 0, y: 0 }}, {{ scale: 1.12, x: -110, y: -36, duration: {r3(t1 - t0)}, ease: "none", '
          f'immediateRender: false }}, {sc.at(t0)});',
          f'tl.fromTo("#{gid}", {{ opacity: 0 }}, {{ opacity: {opacity}, duration: 0.3, ease: "power2.out", immediateRender: false }}, '
          f'{sc.at(t0)});']
    for a in segs:  # the focus pull (a plain blur on the overlay picture: a grading pass would drop its blend mode)
        js.append(f'tl.fromTo("#{gid}", {{ filter: "blur(13px) grayscale(1)" }}, {{ filter: "blur(1px) grayscale(1)", duration: 0.85, '
                  f'ease: "power2.out", immediateRender: false }}, {sc.at(a)});')
    sc.raw(f'<img id="{gid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(t0, t1)} data-track-index="4" '
           f'style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;opacity:0;'
           f'mix-blend-mode:{blend};transform-origin:60% 50%;filter:blur(13px) grayscale(1);z-index:{sc.nz()}" />', js)
    return gid


def sp_quotes(sc, spans, size=210):
    """The Fink screen's big quote marks, hugging each caption block while the interview is up: (t0, t1, open xy,
    close xy) per span."""
    for (a, b, (ox, oy), (qx, qy)) in spans:
        for (x, y, ch) in ((ox, oy, "“"), (qx, qy, "”")):
            qid = sc.uid("qm")
            sc.raw(f'<div id="{qid}" class="clip t" {sc.timed(a, b)} data-track-index="5" style="left:{x:.0f}px;top:{y:.0f}px;'
                   f'font-family:\'Inter Tight\';font-weight:800;font-size:{size}px;line-height:1;color:#FFFFFF;opacity:0.92;'
                   f'text-shadow:0 0 24px rgba(255,255,255,0.35);z-index:{sc.nz() + 400}">{ch}</div>')


import math as _math


def FT(t):
    """A frame-exact time floored to 3 decimals, so a boundary meant for frame n (n/30) never rounds up past it
    (v5's r3(8.4667) = 8.467 made film frame 254 miss S02 and show S01's word again)."""
    return _math.floor(t * 1000 + 1e-6) / 1000



# The B-roll plate (tools/prep6.py cy_broll renders assets/clips2/cy_broll.mp4 from this; build6 writes it into
# media_v6.json["cyber"]). k = frame index from S02's first frame (film frame 254 = 8.4667 s). Rows:
#   main: [k0, frames, source, look, zoom_from, zoom_to, pan_px_per_frame]   (hard cuts, no gaps, no overlaps)
#   sec:  [k0, frames, source, look, opacity, blend]                         (a faint second picture on top)
# Sources: "KEY@t[#cx,cy,zoom]" video (MONT = jpm_montage, BM = the banking montage), "frame:KEY@t" one frame held,
# "img:PATH[@cy]" a still (under dimon-src), "hud1:PATH" / "hud2:PATH" a still with the red HUD drawn on it.
NI, GOV = "new_dimon_images", "Jamie_Dimon_Image_Pack/07_US_Government_America"
CYBER = {
    "frames": 117, "pad": 8,
    "main": [
        # Part A, Karp's montage rhythm (his 24 fps beats x 1.25), cuts on "This" k18, "is" k28, "the" k33, "most" k38
        [0, 1, "MONT@24.10", "night", 1.00, 1.00, 0],                                    # 8.467 fragments frame
        [1, 1, f"img:{NI}/06_Lincoln_Memorial_statue_2024.jpg", "night", 1.04, 1.04, 0],
        [2, 4, "BM@0.10", "warm", 1.02, 1.05, 0],                                        # white flash on k4-5
        [6, 4, f"hud1:{NI}/01_NYSE_August_2017_02.jpg", "navy", 1.06, 1.06, -12],      # red HUD (Karp 0.83)
        [10, 4, "MONT@20.90", "white", 1.00, 1.02, 0],                                   # white pie chart (Karp 0.96)
        [14, 4, f"img:{NI}/14_US_Treasury_2023.jpg", "cool", 1.03, 1.06, 0],
        [18, 4, "MONT@27.10", "cool", 1.02, 1.04, 0],                                    # "This"
        [22, 3, f"img:{NI}/03_NYSE_Wall_Street_1.jpg", "night", 1.04, 1.06, 8],
        [25, 3, f"hud2:{GOV}/06_Federal_Reserve_Eccles_Building.jpg", "grey", 1.00, 1.02, 0],
        [28, 5, f"img:{NI}/02_Capitol_west_front_from_Newseum.jpg", "night", 1.04, 1.07, 0],   # "is"
        [33, 5, "MONT@18.55#0.25,0.45,2.0", "cool", 1.00, 1.03, 0],                      # "the": the world map
        [38, 3, "MONT@14.20", "cool", 1.02, 1.04, 0],                                    # "most": JPMORGAN CHASE & CO.
        [41, 4, "MONT@20.45", "cool", 1.02, 1.04, 0],                                    # the J.P.Morgan lobby
        [45, 22, f"img:{NI}/02_270_Park_Avenue_under_construction_2024.jpg", "cool", 1.00, 1.06, 0],  # "influential"
        # Part B, the Hemant stage: a new picture on each word, ~6 frames each, dimmed in the scene (bgdim 0.45)
        [67, 7, f"img:{NI}/05_White_House_south_facade.jpg", "cool", 1.03, 1.08, 0],     # "man"
        [74, 5, f"img:{NI}/02_NYSE_Wall_Street_facade.jpg@0.40", "cool", 1.04, 1.08, 0],  # "in"
        [79, 7, f"img:{NI}/03_Capitol_west_front_PD.jpg", "warm", 1.03, 1.08, 0],        # "America"
        [86, 7, f"img:{NI}/10_Reflecting_Pool_Washington_Monument.jpg", "cool", 1.03, 1.08, 0],
        [93, 7, "MONT@23.05", "night", 1.02, 1.05, 0],                                   # "right": the ticker
        [100, 7, "BM@2.85", "warm", 1.02, 1.05, 0],                                      # "now": J.P.Morgan at dusk
        [107, 5, "MONT@14.70", "cool", 1.02, 1.04, 0],
        [112, 5, "BM@4.30", "night", 1.02, 1.04, 0],
    ],
    "sec": [
        [14, 8, "frame:BM@0.63", "cool", 0.30, "screen"],
        [22, 3, f"img:{NI}/08_Federal_Hall_historic_1789.jpg", "bw", 0.22, "normal"],
        [45, 11, "frame:MONT@21.60", "white", 0.12, "normal"],
        [56, 11, f"img:{NI}/21_National_City_Bank_Wall_Street_1893.jpg", "bw", 0.16, "normal"],
        [67, 12, f"img:{GOV}/07_Federal_Reserve_Eccles_1937_archival.jpg", "bw", 0.20, "normal"],
        [79, 14, "frame:MONT@19.10", "bw", 0.18, "normal"],
        [93, 14, "frame:BM@1.20", "bw", 0.22, "normal"],
        [107, 10, f"img:{NI}/09_NYSE_panoramio.jpg", "bw", 0.20, "normal"],
    ],
    # Karp 1.46-1.79: a faint list scrolling up (his: Palantir's sectors; ours: JPMorgan's lines of business)
    "list": ["Investment Banking.", "Commercial Banking.", "Asset Management.", "Wealth Management.",
             "Consumer Banking.", "Payments.", "Markets.", "Private Bank.", "Securities Services.",
             "Card Services.", "Home Lending.", "Auto Finance."],
    "list_at": [25, 13], "list_speed": 110, "list_opacity": 0.22,
}
# Exposure of the whole picture (portrait included) per frame k0-k66, Karp's measured logo brightness resampled to
# 30 fps, floor 0.45 (Karp dips to 0.18; raised so it breathes rather than strobes). Part B (k67+) stays at 1.
CY_E = [1.00, 0.50, 0.45, 0.45, 1.00, 1.00, 0.56, 0.45, 0.45, 0.64,
        0.80, 0.66, 0.87, 0.80, 0.50, 0.64, 0.91, 0.85, 1.00, 1.00,
        0.76, 0.55, 0.45, 0.45, 0.45, 0.58, 1.00, 0.57, 0.80, 0.45,
        0.45, 0.45, 0.45, 0.80, 0.57, 0.64, 0.45, 0.45, 0.85, 0.86,
        1.00, 0.55, 0.45, 0.45, 0.48, 1.00, 1.00, 1.00, 0.80, 0.55,
        0.45, 0.55, 0.70, 1.00, 0.90, 0.70, 0.55, 0.60, 0.75, 0.90,
        1.00, 0.90, 0.70, 0.55, 0.60, 0.75, 0.90]
CY_OVL = [(2, 4, 0.15), (6, 4, 0.25), (10, 4, 0.32), (18, 4, 0.25), (25, 3, 0.22), (33, 5, 0.28), (41, 4, 0.18)]
CY_WHITE = [(4, 0.72), (5, 0.88)]                       # Karp 0.75-0.79: the one white flash

KREF = 254 / 30   # the beat grid's k0 (film frame 254, measured against Karp): S02 itself starts on frame 255 = k1, right
                  # after the JPMorgan Chase word's two exit-tile frames (253-254), with Dario's fragments (DIS_T3)
CY_ORIGIN = (965, 478)   # the centre of the band over his eyes in the user's picture (1920x1080): the zoom's fixed point


def sp_cyber_user(sc, cards, seal_at, push, part_b, hud=0.85):
    """v6 note 2, the user's "Glitchy JPMorgan Chase Cyber Portrait" (their own picture, dimon-src/_cyber: Dimon with a
    noisy band and the JPMorganChase wordmark over his eyes, red HUD lines, corner brackets, the JPM NYC tower inset, a
    bar chart) as the centre of the Metro Media House Karp / Palantir opening (0.625-2.417 s of that reel, measured
    every frame: spec_s02.md): Dimon cut out of the picture (cy_cut.png) with its band strip back over his eyes
    (cy_band.png), pulling back from 1.75x on Karp's exponential ease-out (tau 0.48 s); behind him a B-roll plate that
    cuts every 1-7 frames on the voice (cy_broll.mp4, from CYBER), ghosted through him on some beats; the rest of the
    user's picture (its HUD lines, brackets, inset, chart) over the plate in screen blend, zooming with him; the frame
    breathing in exposure (Part A), one white flash. Then (part_b, "man") the Hemant stage: the plate dims, photo cards
    land at the sides after soft white / red boxes, the seal rises behind his head, a subtle push on "in America".
    Entrance: Dario 37.60, the new picture comes through in fragments on the scene's first frame."""
    t0, t1 = sc.start, sc.end
    K = lambda k: FT(KREF + k / 30)                     # film time of beat k (k1 = the scene's first frame)
    ox, oy = CY_ORIGIN
    js = []
    off = r3(t0 - KREF)                                  # the plate's frame k shows on beat k
    sc.raw(f'<video id="{sc.uid("cyb")}" class="clip" src="assets/clips2/cy_broll.mp4" muted playsinline '
           f'{sc.timed(t0, t1)} data-hf-media-start-basis="local" data-media-start="{off}"{gattr("doc")} data-track-index="2" '
           f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;z-index:10"></video>')
    bgd = sc.uid("bgdim")                                # Part B: the plate drops to 55 % so the cards read
    sc.raw(f'<div id="{bgd}" class="clip solid" {sc.timed(K(part_b), t1)} data-track-index="1" data-layout-ignore '
           f'style="background:#000;opacity:0.45;z-index:11"></div>')
    sl = sc.uid("seal")
    sc.raw(f'<img id="{sl}" class="clip" src="assets/img2/{SEAL}" alt="" {sc.timed(seal_at, t1)} data-track-index="3" '
           f'style="position:absolute;left:480px;top:-100px;width:960px;height:960px;opacity:0;z-index:12" />',
           [f'tl.fromTo("#{sl}", {{ opacity: 0, scale: 0.94 }}, {{ opacity: 0.62, scale: 1.0, duration: 0.24, '
            f'ease: "power2.out", immediateRender: false }}, {sc.at(seal_at)});'])
    for i, (src, cx, cy_, w, h, t, red, until) in enumerate(cards):
        col = "rgba(232,40,32,0.95)" if red else "rgba(255,253,246,0.97)"
        glow = "rgba(232,40,32,0.7)" if red else "rgba(255,255,255,0.85)"
        sc.raw(f'<div id="{sc.uid("sbox")}" class="clip solid" {sc.timed(t - 2 * F1, t)} data-track-index="6" '
               f'style="left:{cx - w // 2}px;top:{cy_ - h // 2}px;width:{w}px;height:{h}px;background:{col};'
               f'filter:blur(6px);box-shadow:0 0 48px 18px {glow};z-index:{30 + i}"></div>')
        sc.raw(f'<img id="{sc.uid("hc")}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(t, until or t1)} '
               f'data-track-index="3"{gattr("hcard")} style="position:absolute;left:{cx - w // 2}px;top:{cy_ - h // 2}px;'
               f'width:{w}px;height:{h}px;object-fit:cover;z-index:{20 + i}" />')
    hud_id = sc.uid("cyhud")                             # the user's whole picture: its HUD over the plate (screen)
    sc.raw(f'<div id="{hud_id}" class="grp" data-layout-allow-overflow data-layout-ignore style="z-index:14;'
           f'mix-blend-mode:screen;opacity:{hud};transform-origin:{ox}px {oy}px">'
           f'<img id="{hud_id}-i" class="clip" src="assets/img2/cy_pic.jpg" alt="" {sc.timed(t0, t1)} data-track-index="4" '
           f'style="position:absolute;left:0;top:0;width:1920px;height:1080px" /></div>')
    rig = sc.uid("rig")                                  # Dimon cut out of it, the band strip back over his eyes
    sc.raw(f'<div id="{rig}" class="grp" data-layout-allow-overflow style="z-index:40;transform-origin:{ox}px {oy}px">'
           f'<img id="{rig}-p" class="clip" src="assets/img2/cy_cut.png" alt="" {sc.timed(t0, t1)} data-track-index="4" '
           f'style="position:absolute;left:0;top:0;width:1920px;height:1080px" />'
           f'<img id="{rig}-b" class="clip" src="assets/img2/cy_band.png" alt="" {sc.timed(t0, t1)} data-track-index="5" '
           f'style="position:absolute;left:470px;top:345px;width:990px;height:265px" /></div>')
    both = f"#{rig}, #{hud_id}"
    pk = round((push[0] - t0) / 0.48, 4)
    s_end = round(1 + 0.75 * _math.exp(-(push[0] - t0) / 0.48), 4)
    js += [f'tl.fromTo("{both}", {{ scale: 1.75 }}, {{ scale: {s_end}, duration: {r3(push[0] - t0)}, '
           f'ease: (p) => (1 - Math.exp(-{pk} * p)) / (1 - Math.exp(-{pk})), immediateRender: false }}, 0);',
           f'tl.fromTo("{both}", {{ scale: {s_end} }}, {{ scale: 1.044, duration: {r3(push[1] - push[0])}, '
           f'ease: "power1.inOut", immediateRender: false }}, {sc.at(push[0])});',
           f'tl.to("{both}", {{ scale: 1.054, duration: {r3(t1 - push[1])}, ease: "none" }}, {sc.at(push[1])});']
    ov = sc.uid("ovl")                                   # the plate again, ghosted over him on some beats
    sc.raw(f'<div id="{ov}" class="grp" data-layout-ignore style="z-index:50;opacity:0">'
           f'<video id="{ov}-v" class="clip" src="assets/clips2/cy_broll_ovl.mp4" muted playsinline {sc.timed(t0, t1)} '
           f'data-hf-media-start-basis="local" data-media-start="{off}" data-track-index="2" style="position:absolute;left:0;'
           f'top:0;width:1920px;height:1080px;object-fit:cover"></video></div>')
    for k0, nn, op in CY_OVL:
        if K(k0) >= t0:
            js += [f'tl.set("#{ov}", {{ opacity: {op} }}, {sc.at(K(k0))});', f'tl.set("#{ov}", {{ opacity: 0 }}, {sc.at(K(k0 + nn))});']
    sc.raw(f'<div id="{sc.uid("vig")}" class="clip solid" {sc.timed(t0, t1)} data-track-index="6" data-layout-ignore '
           f'style="background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%);'
           f'z-index:55"></div>')
    ex = sc.uid("expo")
    sc.raw(f'<div id="{ex}" class="clip solid" {sc.timed(t0, K(part_b))} data-track-index="6" data-layout-ignore '
           f'style="background:#000;opacity:0;z-index:60"></div>')
    prev = None
    for k, e in enumerate(CY_E):
        if K(k) < t0:
            continue
        o = round(1 - e, 2)
        if o != prev:
            js.append(f'tl.set("#{ex}", {{ opacity: {o} }}, {sc.at(K(k))});')
            prev = o
    for k, op in CY_WHITE:
        sc.raw(f'<div id="{sc.uid("cyw")}" class="clip solid" {sc.timed(K(k), K(k + 1))} data-track-index="6" '
               f'data-layout-ignore style="background:#FFFDF6;opacity:{op};z-index:61"></div>')
    sp_tiles(sc, t0, DIS_T3, z=900)                       # Dario 37.60: the new picture comes through in fragments
    sc.J("\n    ".join(js))
    return rig


STY = {  # family, weight, size, kind.  A style may carry a size override: "sh@200".
    "s": ("Inter Tight", 700, 84, "sans"),
    "sm": ("Inter Tight", 600, 62, "sans"),
    "b": ("Inter Tight", 800, 160, "sans"),
    "ink": ("Inter Tight", 700, 64, "ink"),       # black Helvetica on paper (the was-fired reference)
    "inkb": ("Inter Tight", 800, 120, "ink"),     # its big bold word
    "ss": ("Instrument Serif", 400, 92, "serif"),  # small serif (lockups: a small word beside a big one)
    "sl": ("Instrument Serif", 400, 128, "serif"),
    "sh": ("Instrument Serif", 400, 236, "hero"),
    "sx": ("Instrument Serif", 400, 300, "hero"),
    "nm": ("Instrument Serif", 400, 250, "name"),
    "gold": ("Instrument Serif", 400, 236, "gold"),
    "p": ("Inter Tight", 800, 96, "paper"),
    "pb": ("Inter Tight", 800, 150, "paper"),
    "ps": ("Instrument Serif", 400, 250, "paper"),
}
CAPS = []
SCOPE_END, V5_EARLY = 20.855, 16   # v6 edits 0-20.86 s only; v5 had 16 caption groups (cg000-cg015) before it


def sty(st):
    key, _, size = st.partition("@")
    fam, wt, sz, kind = STY[key]
    return fam, wt, (float(size) if size else sz), kind


def W_(i, st, text=None):
    return (text or VOW[i]["text"], VT(i), st)


def N_(i, st, text=None):
    return (text or NEWS[i]["text"], NT(i), st)


def Q_(i, st, text=None):
    return (text or QUOTE[i]["text"], QT(i), st)


def cap(lines, end=None, y=540, exit="cut", start=None, x=960, scrim=None, align="center", lh=0.92, blinks=()):
    """lines: [[(text, t, style), ...], ...] stacked about y; each line is anchored at x by align (its centre, left
    or right edge). A line may instead be dict(w=[...], x=, y=, align=) placed on its own (y: its centre)."""
    CAPS.append(dict(lines=lines, end=end, y=y, exit=exit, start=start, x=x, scrim=scrim, align=align, lh=lh,
                     blinks=blinks))


def spread(words, end=None, exit="cut", start=None):
    """Ackman's spread words: each word (text, t, style, x, y, align) on its own spot."""
    cap([dict(w=[(t_, at_, st_)], x=x_, y=y_, align=al_) for t_, at_, st_, x_, y_, al_ in words], end=end, exit=exit,
        start=start)


def _words(line):
    return line["w"] if isinstance(line, dict) else line


def build_captions():
    els, js = [], []
    first_t = lambda g: min(t for line in g["lines"] for _, t, _ in _words(line))
    groups = sorted(CAPS, key=first_t)
    n_early = sum(1 for g in groups if first_t(g) < SCOPE_END)
    for gi, g in enumerate(groups):
        # the groups from S05 on keep their v5 ids (cg016 ...); the earlier ones take a "cx" prefix whenever their count
        # differs from v5's, so no id is shared and the diff stays inside 0-20.86 s
        if gi >= n_early:
            gid = f"cg{gi - n_early + V5_EARLY:03d}"
        else:
            gid = f"cg{gi:03d}" if n_early == V5_EARLY else f"cx{gi:03d}"
        first = first_t(g)
        last = max(t for line in g["lines"] for _, t, _ in _words(line))
        t0 = round(g["start"] if g["start"] is not None else first - 2 * F1, 3)
        if g["end"] is not None:
            t1 = g["end"]
        elif gi + 1 < len(groups):
            t1 = round(first_t(groups[gi + 1]) - 2 * F1, 3)
            if t1 - last > 1.4:
                t1 = round(last + 1.0, 3)
        else:
            t1 = DUR
        stacked = [ln for ln in g["lines"] if not isinstance(ln, dict)]
        heights = [max(sty(st)[2] for _, _, st in ln) for ln in stacked]
        ytop = g["y"] - sum(h * g["lh"] for h in heights) / 2
        lines_html = []
        si = 0
        for li, line in enumerate(g["lines"]):
            if isinstance(line, dict):
                words, ax, align = line["w"], line["x"], line.get("align", "center")
                lh = max(sty(st)[2] for _, _, st in words) * g["lh"]
                base = line["y"] - lh / 2 + lh * 0.80
            else:
                words, ax, align = line, g["x"], g["align"]
                lh = heights[si] * g["lh"]
                si += 1
                base = ytop + lh * 0.80
                ytop += lh
            ws = []
            for text, t, st in words:
                fam, wt, size, kind = sty(st)
                if text not in ("$10", "$60", "$500"):
                    text = text.replace(",", "").replace(".", "")
                tr = -0.03 if fam == "Inter Tight" else -0.01
                ws.append((text, t, st, textw(text, fam, wt, size, track=tr)))
            gaps = [sty(st)[2] * (0.24 if sty(st)[0] == "Inter Tight" else 0.2) for _, _, st, _ in ws]
            Wt = sum(w for *_, w in ws) + sum(gaps[1:])
            x = {"center": ax - Wt / 2, "left": ax, "right": ax - Wt}[align]
            spans = []
            acc = 0.0
            for k, (text, t, st, w) in enumerate(ws):
                fam, wt, size, kind = sty(st)
                if k > 0:
                    acc += gaps[k]
                left = x + acc
                acc += w
                sid = f"{gid}-w{li}{k}"
                color = "#111" if kind in ("paper", "ink") else INK
                shadow = {"sans": GLOW_REST, "serif": SERIF_REST, "hero": SERIF_REST, "name": SERIF_REST,
                          "gold": GOLD_REST, "ink": "none",
                          "paper": "0 0 18px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.5)"}[kind]
                trk = "-0.03em" if fam == "Inter Tight" else "-0.01em"
                top = base - size * 0.80
                style = (f"left:{left:.0f}px;top:{top:.0f}px;font-family:'{fam}';font-weight:{wt};font-size:{size:.0f}px;"
                         f"letter-spacing:{trk};color:{color};")
                if kind in ("serif", "hero", "name", "gold"):
                    spans.append(f'<span id="{sid}" class="w" style="{style}"><span id="{sid}-f" class="fl"></span>'
                                 f'<span id="{sid}-t" class="wt" style="opacity:0;text-shadow:{shadow}">{esc(text)}</span></span>')
                else:
                    spans.append(f'<span id="{sid}" class="w" style="{style}text-shadow:{shadow};opacity:0">{esc(text)}</span>')
                a = max(t0, t)
                if kind == "sans":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
                              f'{{ opacity: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.24, ease: "expo.out", '
                              f'immediateRender: false }}, {r3(a)});')
                elif kind == "ink":  # black type on paper: sharp, in two frames
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", '
                              f'duration: {r3(2 * F1)}, ease: "power2.out", immediateRender: false }}, {r3(a)});')
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
                    js += [f'tl.set("#{sid}-t", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("#{sid}-t", {{ scale: 1.005, filter: "blur(2.5px)" }}, {r3(a + 3 * F1)});',
                           f'tl.set("#{sid}-t", {{ scale: 1, filter: "blur(0px)", textShadow: "{rest}" }}, {r3(a + 4 * F1)});']
            lines_html.append(f'<div id="{gid}-l{li}" class="ln">{"".join(spans)}</div>')
        if g.get("scrim"):
            a = g["scrim"]
            lines_html.insert(0, f'<div class="scrim" data-layout-ignore style="left:{g["x"] - 640}px;top:{g["y"] - 230}px;'
                                 f'background:radial-gradient(closest-side, rgba(6,5,4,{a}) 0%, rgba(6,5,4,{round(a * 0.6, 2)}) 50%, '
                                 f'rgba(6,5,4,0) 100%)"></div>')
        els.append(f'<div id="{gid}" class="clip cg" data-start="{r3(t0)}" data-duration="{r3(t1 - t0)}" data-track-index="1" '
                   f'data-layout-allow-overflow data-layout-allow-overlap>{"".join(lines_html)}</div>')
        for bt, bn in g.get("blinks", ()):
            js += [f'tl.set("#{gid}", {{ opacity: 0 }}, {r3(bt)});', f'tl.set("#{gid}", {{ opacity: 1 }}, {r3(bt + bn * F1)});']
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
# THE EDIT (v6: 0-20.86 s rebuilt to the v6 notes; 20.86-31.7 s as v5; from 31.7 s as v3)
# ================================================================================================
FRAME_OF["MONT"] = "MONT"
CARD = {k: ST(f"cd_{k}", key="MONT", t=t, frame="MONT", size=[840, 560]) for k, t in [
    ("fortune", 25.55), ("whitehouse", 26.05), ("press", 16.55), ("congress", 28.05), ("cash", 11.65), ("park", 18.85)]}
GHOST = "globe_ghost.jpg"                      # the user's globe picture (tools/prep4.py)
WEILL = [f"wf{k}.jpg" for k in range(8)]       # tools/prep5.py: Dario-aligned faces of Sandy Weill
YOUNG = ["yd5_1.jpg", "yd5_2.jpg", "yd5_3.jpg"]  # tools/prep5.py: young Dimon, squares on his face (v5)
YOUNG6 = [f"yd6_{k:02d}.jpg" for k in range(1, 11)]   # tools/prep6.py: face-aligned squares, youngest first; [-1] = the B&W hero
POP0 = 8.60                                    # Dimon slides up here, over the JPMorgan tower (v5)
S2_0 = 8.50                                    # v6: the frame after the word's exit tiles (Dario 37.60, frame 255)


def SPK(t):
    """film time -> the speaking clip's source time (one continuous take from the pop-up to the end of S02)."""
    return round(12.20 + (t - POP0), 3)


def push(sc, cam, t0, t1, a=1.0, b=1.04):
    sc.J(f'tl.fromTo("#{cam}", {{ scale: {a} }}, {{ scale: {b}, duration: {r3(t1 - t0)}, ease: "none" }}, {sc.at(t0)});')


# ---- S01  0.00-9.05  the Bloomberg open, re-cut: "The name of the game in American capitalism, is being big, and no
#      one is bigger [held] on Wall Street than JPMorgan Chase."  (the reporter's voice alone; the music from frame 0)
s = Scene("s01", 0.0, S2_0)   # v6: ends where the cyber portrait comes in
montage(s, [
    (0.0, "GAME", 0.0, {"rate": 0.9}),                  # The: Lower Manhattan
    (CUT(NT(1)), "HOW", 323.2, {"grade": "bw"}),        # name of the: the Wall St sign, 1920s
    (CUT(NT(4)), "HOW", 792.6),                         # game: the NYSE trading floor
    (CUT(NT(6)), "BANK", 750.6),                        # American: the board and the flag
    (CUT(NT(7)), "P07", 1.0),                           # capitalism: the counting machine ... (user: very good)
    (CUT(NT(7)) + 0.45, "GAME", 329.6),                 # ... the vault door
    (CUT(NT(8)), "GAME", 70.2),                         # is being: towers from below
], CUT(NT(10)))
sp_big_static(s, CUT(NT(10)), CUT(NT(11)), "BIG", "GAME", 6.0, size=1000)   # big: simply there (user)
s.neg(CUT(NT(10)), 2)                                                       # the flash (user: fine)
montage(s, [
    (CUT(NT(11)), "GAME", 81.5, {"xyz": (0.57, 0.53, 1.15)}),   # and no: Wall Street at rush hour
    (4.48, "GAME", 8.40),                               # one is: the reporter, in sync (source = film + 3.92)
], CUT(NT(15)))
sp_suddenly(s, CUT(NT(15)), CUT(NT(16)), "bigger", size=340, echo=520)      # bigger: Dario's SUDDENLY, with glow
s.v("GAME", 3.42, CUT(NT(16)), CUT(NT(20)), push=(1.0, 1.04))              # on Wall Street than: the street sign
# JPMorgan Chase, typed like Dario's DISAPPEAR (v6, user: "coming unanimously ... while in the background it's saying
# JP Morgan and Chase"): one steady type-on, a letter every 2 frames (Dario's rate), each new letter flaring for one
# frame, from the reporter's "JP" (frame 219) to the "e" at frame 243 (8.10), well before "Chase" ends (8.36); over the
# J.P.Morgan flag, then the tower, cut mid-word on the "h" (Dario cuts DISA|PPEAR); 9 crisp frames; Dario's tiles at
# frames 253-254; the word is gone from S2_0 (frame 255). Until S02's cyber portrait comes through there in Dario's
# tiles (sp_tiles(s, S2_0, DIS_T3)), the tower holds and Dimon slides up as in v5.
JPF = math.ceil(NT(20) * 30 - 1e-6)                    # 219: the first frame on the reporter's "JP" (7.28)
JPMC_T = [FR(JPF + 2 * k) for k in range(13)]          # 7.283 7.35 7.417 ... 8.083: J P M o r g a n C h a s e
TOW0 = JPMC_T[9]                                       # 7.883 (frame 237): the tower lands with the "h"
camF, _ = s.vfile("flag_slow.mp4", CUT(NT(20)), TOW0, grade="night")
push(s, camF, CUT(NT(20)), TOW0, 1.0, 1.03)
camT, _ = s.vfile("tower_slow.mp4", TOW0, S2_0, grade="night")
push(s, camT, TOW0, S2_0, 1.0, 1.04)
sp_type_word(s, CUT(NT(20)), S2_0, "JPMorgan Chase", JPMC_T, size=450, squeeze=0.70, base=672, track=-0.015,
             exit_at=S2_0)
cap([[N_(0, "s"), N_(1, "s"), N_(2, "s"), N_(3, "s"), N_(4, "s")]], end=1.29)
cap([[N_(5, "s"), N_(6, "s")], [N_(7, "sh")]], end=CUT(NT(8)) + 0.02)       # "in American" as before (user)
cap([[N_(8, "s"), N_(9, "s")]], end=CUT(NT(10)))
cap([[N_(11, "s"), N_(12, "s"), N_(13, "s"), N_(14, "s")]], y=900, end=CUT(NT(15)), scrim=0.45)
cap([[N_(16, "ss@112"), N_(17, "sx@340"), N_(18, "sx@340")]], y=560, end=CUT(NT(19)))
cap([[N_(19, "s")]], end=CUT(NT(20)))

# ---- S02  8.50-12.365  "This is the most influential man in America right now."  The Glitchy JP Morgan Chase Cyber
#      Portrait (user's picture) in the Metro Media House Alex Karp / Palantir opening, with Hemant Taneja's cards and
#      the seal (user, v6 note 2; spec_s02.md). No pop-up, no flicker of live frames, one white flash.
s = Scene("s02", S2_0, CUT(VT(10)), tex=(0.05, 0.0))
SWAP = round(CUT(VT(8)) + 0.07, 3)
sp_cyber_user(s, [
    (CARD["fortune"], 395, 330, 520, 288, 10.86, False, SWAP),
    (CARD["congress"], 1562, 780, 416, 260, 11.00, False, SWAP),
    (CARD["whitehouse"], 1537, 330, 434, 244, 11.20, False, None),
    (CARD["press"], 372, 770, 326, 254, 11.40, False, None),
    (CARD["cash"], 395, 330, 520, 288, SWAP, True, None),
    (CARD["park"], 1562, 780, 416, 260, round(SWAP + 2 * F1, 3), True, None),
], seal_at=VT(7), push=(VT(6), VT(8)), part_b=67)
# plain, centred, aligned (user: "text can be normal ... adjusting size"): small sans over a big serif word, on fixed
# baselines, like the "in American / capitalism" lockup; four groups as in v5 (the first split into its two lines)
CAP_END1 = round(VT(5) - 2 * F1, 3)                                          # 10.663, when "man in" arrives
cap([dict(w=[W_(0, "s@64"), W_(1, "s@64"), W_(2, "s@64"), W_(3, "s@64")], x=960, y=810)], y=885, lh=1.0, scrim=0.42,
    end=CAP_END1)
cap([dict(w=[W_(4, "sh@150")], x=960, y=917)], y=885, lh=1.0, end=CAP_END1)
cap([[W_(5, "s@64"), W_(6, "s@64")], [W_(7, "sh@150")]], x=960, y=885, lh=1.0, scrim=0.42)
cap([[W_(8, "s@64")], [W_(9, "sh@150")]], x=960, y=885, lh=1.0, scrim=0.42)

# ---- S03  12.36-15.07  "He's basically the CEO of Wall Street,"  (real video only; Pattinson's transitions)
s = Scene("s03", CUT(VT(10)), CUT(VT(17)))
s.v("GAME", 61.55, CUT(VT(10)), 12.83, push=(1.0, 1.03))             # He's basically: the 270 Park podium
s.v("CHAIR", 1265.2, 12.83, CUT(VT(13)), push=(1.0, 1.025))           # the: Stanford, a straight cut (v6: no slide)
camC, _ = s.vfile("ceo_slow.mp4", CUT(VT(13)), CUT(VT(14)), z=s.nz() + 60)   # CEO: walking in with his detail ...
sp_window_ease(s, camC, CUT(VT(13)) + 0.08, CUT(VT(14)), to=0.64, cards=[   # ... eases back into a window (Pattinson)
    (DIMON_PHOTOS[0], 215, 330, 330, 220, 13.32, -4),
    (DIMON_PHOTOS[1], 1712, 300, 300, 200, 13.38, 3),
    (LEADERS[3], 250, 820, 320, 214, 13.44, 3),
    (PIN_DIMON[2], 1690, 830, 300, 200, 13.50, -3)])
s.neg(round(CUT(VT(14)) - F1, 3), 1)                                   # Pattinson 6.17: an inverted frame before the run
WOLF0 = CUT(VT(14))
PUNCH = round(CUT(VT(17)) - 0.17, 3)
BOXES = ""
for k, (bx, by, bw, bh, label) in enumerate([(770, 84, 380, 500, "person 0.97"), (690, 600, 540, 250, "currency 0.94")]):
    on = round(WOLF0 + (2 + k * 3) * F1, 3)
    BOXES += (f'<div id="s03-fbx{k}" class="clip" {s.timed(on, CUT(VT(17)) - 2 * F1)} data-track-index="5" '
              f'style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;border:3px solid #B455FF;'
              f'box-shadow:0 0 12px rgba(180,85,255,0.7)"><div style="position:absolute;left:-3px;top:-42px;padding:4px 10px;'
              f'background:#B455FF;font-family:\'Inter Tight\';font-weight:700;font-size:28px;line-height:1.1;color:#fff;'
              f'white-space:nowrap">{label}</div></div>')
    s.J(f'tl.set("#s03-fbx{k}", {{ opacity: 0 }}, {s.at(on + F1)});')
    s.J(f'tl.set("#s03-fbx{k}", {{ opacity: 1 }}, {s.at(on + 2 * F1)});')
camW, _ = s.vfile("wolf_slow.mp4", WOLF0, CUT(VT(17)), grade="warm", inner=BOXES)   # of Wall Street: one continuous
pan_arrive(s, camW, WOLF0, PUNCH)                                                 # shot, arriving still moving
s.J(f'tl.fromTo("#{camW}", {{ scale: 1.05 }}, {{ scale: 1.12, duration: 0.1, ease: "power3.out", immediateRender: false }}, '
    f'{s.at(PUNCH)});')
WOLF_LOCK = sp_wolf_lockup(s, CUT(VT(17)), [("of", VT(14)), ("Wall", VT(15)), ("Street", VT(16))], y=1000, size=165,
                           exit_at=round(CUT(VT(17)) - F1, 3))   # Ackman 7.00: the white frame is clean
XF = round(CUT(VT(17)) - 2 * F1, 3)                                    # Ackman 6.96: purple negative, then white
blk(s, XF, 1, (0, 0, 1920, 1080), "#ffffff", blend="difference", z=1400)
blk(s, XF, 1, (0, 0, 1920, 1080), "#6a1fd0", blend="multiply", opacity=0.62, z=1401)
s.J(f'tl.set("#{WOLF_LOCK} .t", {{ color: "#F59BE0" }}, {s.at(XF)});')
s.whiteframe(round(CUT(VT(17)) - F1, 3), 1)
spread([(VOW[10]["text"], VT(10), "s@62", 170, 560, "left"), (VOW[11]["text"], VT(11), "s@62", 470, 560, "left")],
       end=12.83)
cap([[W_(12, "ss@80"), W_(13, "sh@180")]], x=960, y=975, end=CUT(VT(14)))

# ---- S04  15.07-20.86  "a guy who got fired in 1998 by his own mentor over a bonus and a family grudge,"
s = Scene("s04", CUT(VT(17)), CUT(VT(35)))
F0 = CUT(VT(17))
sp_fired_flip(s, F0, CUT(VT(21)), CUT(VT(23)), YOUNG6[:-1], YOUNG6[-1],    # v6: nine photos, two frames each, then
              [(VOW[k]["text"], VT(k)) for k in (17, 18, 19, 20)], ("FIRED", VT(21)))   # the hero on "fired"
sp_roller(s, CUT(VT(23)), CUT(VT(24)), list(range(1990, 1999)), land_at=VT(23) + 0.22, cards=[], video_bg=("MPB", 850.0),
          invert_digits=2)                                             # in 1998 (user: fine with Citigroup behind)
sp_dario_faces(s, CUT(VT(24)), CUT(VT(28)), WEILL)                     # by his own mentor: Dario's faces, Sandy Weill
BON = 18.74
sp_grid4(s, CUT(VT(28)), BON, [("P07", 1.2), ("MONEY", 1.0), ("MPB", 1784.0), ("HOW", 781.5)], step=2)   # faster
blk(s, CUT(VT(28)), 1, (0, 0, 1920, 1080), "#000000", opacity=0.7, z=1300)   # Dario 18.40: in dark for a frame
s.v("BONUS", 5.90, BON, 19.62, grade="", push=(1.0, 1.03), xyz=(0.5, 0.46, 1.09))   # the user's cartoon
camG, _ = s.v("MPB", 1056.6, 19.62, CUT(VT(35)), push=None)            # family grudge: his daughter comes into it
s.J(f'tl.fromTo("#{camG}", {{ scale: 1.22, x: 170 }}, {{ scale: 1.05, x: -70, duration: {r3(CUT(VT(35)) - 19.62)}, '
    f'ease: "power1.inOut", immediateRender: false }}, {s.at(19.62)});')
s.neg(19.62, 1)
cap([[W_(24, "sh@160"), W_(25, "sh@160"), W_(26, "sh@160"), W_(27, "sh@160")]], y=880, scrim=0.45,
    end=CUT(VT(28)))   # by his own mentor: ONE line at the bottom, under the square, Dario's serif bloom-in (user, v6)
cap([[W_(28, "s"), W_(29, "s")]], end=BON)
cap([[W_(30, "sh@240")]], y=880, end=CUT(VT(31)))
cap([[W_(31, "s"), W_(32, "s"), W_(33, "s")]], y=540, end=CUT(VT(34)))   # user: in the centre
cap([[W_(34, "sh")]], y=540, end=CUT(VT(35)) - 0.02)

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

# ---- S06  23.60-34.85  Dimon in his own words. User: the interview as the base for "We bank some of these companies
#      in 30 countries. We bank countries, we bank the World Bank, the IMF, ... the United States government", cutting
#      to B-roll and back (interview, B-roll, interview, B-roll ...); the captions as in the we-bank reel; the Fink
#      reel's Rogan screen: his globe picture behind him (he is matted above it), low opacity, slowly moving and pulling
#      focus; the quote marks close to the text.
s = Scene("s06", QUOTE_AT, 34.85, tex=(0.05, 0.0))
TWO = round(QUOTE_AT + (281.00 - QUOTE_SRC0), 3)
SY = lambda t: 273.05 + (t - QUOTE_AT)
IV = dict(xyz=(0.63, 0.5, 1.35), push=(1.0, 1.03))
s.v("BANK", SY(QUOTE_AT), QUOTE_AT, TWO, **IV)                          # the interview (one continuous take)
SEGS = [QUOTE_AT, CUT(QT(9)), CUT(QT(12)), CUT(QT(17))]                # back on the interview at these times
sp_ghost(s, QUOTE_AT, TWO, GHOST, (800, 0, 1220, 1080), SEGS, opacity=0.45)
IV_CID = CL("BANK", SY(QUOTE_AT), TWO - QUOTE_AT, xyz=IV["xyz"])
camM, vidM = s.uid("cam"), s.uid("v")
s.raw(f'<div class="cam" id="{camM}" style="left:0px;top:0px;width:1920px;height:1080px;z-index:{s.nz()};'
      f'transform-origin:50% 50%"><video id="{vidM}" class="clip" src="assets/clips2/{IV_CID}_cut.webm" muted playsinline '
      f'{s.timed(QUOTE_AT, TWO)} data-hf-media-start-basis="local" data-media-start="0"{gattr("doc")} data-track-index="2" '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover"></video></div>',
      [f'tl.fromTo("#{camM}", {{ scale: {IV["push"][0]} }}, {{ scale: {IV["push"][1]}, duration: {r3(TWO - QUOTE_AT)}, '
       f'ease: "none" }}, {s.at(QUOTE_AT)});'])
QX = 1110
G = [  # the caption groups (lines), as cap() gets them
    [[Q_(0, "s"), Q_(1, "s")]],
    [[Q_(2, "sm"), Q_(3, "sm"), Q_(4, "sm")], [Q_(5, "b@118")], [Q_(6, "sm"), Q_(7, "b@118"), Q_(8, "sh@150", "countries")]],
    [[Q_(9, "s"), Q_(10, "s")], [Q_(11, "sh@200", "Countries")]],
    [[Q_(12, "sm"), Q_(13, "sm"), Q_(14, "sm")], [Q_(15, "b@112"), Q_(16, "b@112")]],
    [[Q_(17, "sm")], [Q_(18, "sh@230", "IMF")]],
    [[Q_(19, "sm"), Q_(20, "sm"), Q_(21, "sm")], [Q_(22, "b@100"), Q_(23, "b@100")], [Q_(24, "sh@170")]],
]
ENDS = [CUT(QT(2)), CUT(QT(9)), CUT(QT(12)), CUT(QT(17)), CUT(QT(19)), TWO]
for g, e in zip(G, ENDS):
    cap(g, x=QX, y=520, align="left", end=e, exit="blur")


def cap_box(lines, x=QX, y=520, lh=0.92, n=None):
    """The box of the first n lines of a caption group laid out as cap() lays it out (centred about y)."""
    hs = [max(sty(st)[2] for _, _, st in ln) for ln in lines]
    top = y - sum(h * lh for h in hs) / 2
    n = n or len(lines)
    hs, lines = hs[:n], lines[:n]
    right = 0
    for ln in lines:
        w = 0
        for k, (text, _, st) in enumerate(ln):
            fam, wt, size, _ = sty(st)
            w += textw(text.replace(",", "").replace(".", ""), fam, wt, size, track=-0.03 if fam == "Inter Tight" else -0.01)
            if k:
                w += size * (0.24 if fam == "Inter Tight" else 0.2)
        right = max(right, x + w)
    return top, top + sum(h * lh for h in hs), right


QSPANS = []
for gi, (a, b), n in [(0, (QUOTE_AT, CUT(QT(2))), 1), (1, (CUT(QT(2)), CUT(QT(6))), 2), (2, (CUT(QT(9)), CUT(QT(11))), 1),
                      (3, (CUT(QT(12)), CUT(QT(15))), 1), (4, (CUT(QT(17)), CUT(QT(19))), 2),
                      (5, (CUT(QT(19)), CUT(QT(22))), 1)]:   # n: the lines up while the interview is on screen
    top, bot, right = cap_box(G[gi], n=n)
    QSPANS.append((a, b, (QX - 78, top - 132), (right - 4, bot - 74)))
sp_quotes(s, QSPANS)
for a, b, key, t, xyz in [                                             # the B-roll, straight cuts
        (CUT(QT(6)), CUT(QT(8)), "BANK", 52.62, (0.5, 0.42, 1.2)),     # in 30: the JPMorgan Global China Summit
        (CUT(QT(8)), CUT(QT(9)), "BANK", 40.30, None),                 # countries: Davos, the World Economic Forum
        (CUT(QT(11)), CUT(QT(12)), "BANK", 0.30, (0.55, 0.55, 1.15)),  # countries: London from the air
        (CUT(QT(22)), CUT(QT(24)), "BANK", 77.45, None),               # United States: with Obama
        (CUT(QT(24)), TWO, "BANK", 28.35, None)]:                      # government: testifying to Congress
    s.v(key, t, a, b, push=(1.0, 1.04), xyz=xyz, z=s.nz() + 1000)
s.img(WB_BLDG, CUT(QT(15)), CUT(QT(17)), push=(1.0, 1.05), z=s.nz() + 1000)   # World Bank: its building
s.v("BANK", 281.0, TWO, CUT(QT(29)), push=(1.0, 1.02))
s.v("GAME", 70.6, CUT(QT(29)), CUT(QT(30)), push=(1.15, 1.0))                # big: the towers
cam, _ = s.v("BANK", SY(CUT(QT(30))), CUT(QT(30)), 34.85, push=None, origin="50% 50%")
sp_window(s, cam, CUT(QT(37)), to=0.16, dur=0.38)
cap([[Q_(25, "s"), Q_(26, "s"), Q_(27, "s"), Q_(28, "s")], [Q_(29, "b@200")]], end=CUT(QT(30)))
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
             )
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
years = "".join(f'<text x="{x:.0f}" y="{Y0 + 236}" text-anchor="middle" font-family="Inter Tight" font-weight="600" '
                f'font-size="34" fill="#2A2622">{yr}</text>' for (yr, _), (x, _) in zip(pts, P))
dots = "".join(f'<circle id="{pg}-d{k}" cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#E5381B" opacity="0" />' for k, (x, y) in enumerate(P))
s.raw(f'<div id="{pg}" class="clip grp" {s.timed(PAGE0, CUT(VT(173)))} data-track-index="4" data-layout-allow-overflow '
      f'style="background:#F2E8D6;z-index:{s.nz()}"><img class="tex" src="assets/tex/ht_warm.jpg" alt="" style="mix-blend-mode:multiply;opacity:0.42" />'
      f'<div id="{pg}-cam" class="grp" style="transform-origin:{P[3][0]:.0f}px {P[3][1]:.0f}px">'
      f'<div class="t" style="left:{X0 - 6}px;top:150px;font-family:\'Instrument Serif\';font-size:92px;color:#14110F">Bank One</div>'
      f'<div class="t" style="left:{X0}px;top:258px;font-family:\'Inter Tight\';font-weight:600;font-size:34px;color:#4A433C">net income, 2000 - 2003</div>'
      f'<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0">'
      f'<line x1="{X0 - 80}" y1="{Y0}" x2="{X1 + 80}" y2="{Y0}" stroke="#2A2622" stroke-width="2" stroke-dasharray="10 10" opacity="0.55" />'
      f'{years}<path id="{pg}-line" d="{path}" fill="none" stroke="#E5381B" stroke-width="9" stroke-linecap="round" '
      f'stroke-linejoin="round" stroke-dasharray="{seglen:.1f}" stroke-dashoffset="{seglen:.1f}" />{dots}</svg>'
      f'<div id="{pg}-loss" class="t" style="left:{P[0][0] + 34:.0f}px;top:{P[0][1] + 14:.0f}px;font-family:\'Instrument Serif\';'
      f'font-size:84px;color:#E5381B;opacity:0">-$500M <span style="font-family:\'Inter Tight\';'
      f'font-weight:500;font-size:34px;color:#2A2622">loss</span></div>'
      f'<div id="{pg}-prof" class="t" style="left:{P[3][0] - 330:.0f}px;top:{P[3][1] - 150:.0f}px;font-family:\'Instrument Serif\';'
      f'font-size:118px;color:#14110F;opacity:0">+$3.5B <span style="font-family:\'Inter Tight\';'
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
for sc_, t_ in ((SCENES[4], CUT(VT(38))), (SCENES[8], CUT(VT(83))), (SCENES[11], CUT(VT(113))),
                (SCENES[13], CUT(VT(145))), (SCENES[15], CUT(VT(161))), (SCENES[21], CUT(VT(203)))):
    sc_.neg(t_, 1)


# ================================================================================================
# Root
# ================================================================================================
def write_aux():
    import re as _re
    g = open(f"{COMP}/components/grain-overlay.html").read()
    m = _re.search(r'url\("(data:image/svg\+xml[^"]+)"\)', g)
    data_url = m.group(1) if m else ""
    offs = [(-5, -5), (-10, 5), (5, -10), (-5, 15), (-10, 5), (15, 0), (0, 10), (-15, 0), (10, 5), (0, 0)]
    jit, t, k = [], 0.0, 0
    while t < DUR:
        dx, dy = offs[k % len(offs)]
        jit.append(f'tl.set("#grain-tex", {{ xPercent: {dx}, yPercent: {dy} }}, {t:.3f});')
        t, k = round(t + 1 / 12, 3), k + 1
    open(f"{COMP}/grain.html", "w").write(f"""<template>
  <style>
  #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
  #grain-tex {{ position: absolute; left: -50%; top: -50%; width: 200%; height: 200%; opacity: 0.06;
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
""")


def write_root():
    hosts = []
    for k, sc in enumerate(SCENES):
        hosts.append(f'<div id="{sc.sid}" class="clip" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" '
                     f'data-start="{r3(sc.start)}" data-duration="{r3(sc.dur)}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1920" data-height="1080" style="z-index:{10 + k}"></div>')
    hosts.append(f'<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{r3(DUR)}" data-track-index="3" data-track-kind="captions" '
                 f'data-width="1920" data-height="1080" style="z-index:100"></div>')
    hosts.append(f'<div id="grain" class="clip" data-composition-id="grain" data-composition-src="compositions/grain.html" '
                 f'data-start="0" data-duration="{r3(DUR)}" data-track-index="4" data-width="1920" data-height="1080" '
                 f'style="z-index:150"></div>')
    auds = [("news", "news_voice.wav", 0.0, NEWS_DUR, 0.0, 0.0, 0.02),
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
    MEDIA["cyber"] = CYBER
    json.dump(MEDIA, open(f"{PRJ}/tools/media_v6.json", "w"), indent=1)
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
    write_aux()
    write_root()
    print("scenes:", [(sc.sid, sc.start, sc.end) for sc in SCENES])
    print("caption groups:", n, "clips:", len(MEDIA["clips"]), "stills:", len(MEDIA["stills"]))
