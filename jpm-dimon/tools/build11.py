#!/usr/bin/env python3
"""v6 -- Jamie Dimon / JPMorgan Chase (1920x1080, 30 fps, 87.117 s): the user's v6 notes on 0-28.77 s; from "Meet
Jamie Dimon" on exactly v5, SHIFT (6.083 s) earlier.

v6 over v5:
- S01: "JPMorgan Chase" is one continuous type-on at Dario's DISAPPEAR rate (a letter every 2 frames, the newest letter
  flaring for one frame with a haze), from the reporter's "JP"; it holds 9 frames and leaves through Dario's inverted
  sky-blue tiles (frames 253-254); S2_0 = 8.50 is S02's first frame.
- S02: "This is the most influential man in America right now" is the user's Glitchy JPMorgan Chase Cyber Portrait:
  Dimon cut out of it and pulling back from 1.75x on Karp's ease (tau 0.48 s), a B-roll plate rolling fast behind and
  through him at low opacity (tools/prep6.py cy_broll renders CYBER), Hemant's side cards with their flashes, the seal;
  the captions plain and centred (no pop-up, no continuous flash).
- S03: the Stanford shot is a straight cut (no slide, no pan); the CEO window and the Wolf arrival are as v5.
- S04: "a guy who got FIRED" flips through nine photos of young Dimon (prep6 young6), two frames each, while the card
  grows smoothly, then the B&W hero lands on "fired"; "by his own mentor" is ONE horizontal line at the bottom in
  Dario's serif glow over the Sandy Weill faces; "over a bonus" is the user's cartoon; "and a family grudge" is the
  opening of the reel the user sent (sp_grudge_slide: the Weills slide in from the left under a 3x3 grid, the
  background goes colour, white, black-and-white; prep6 grudge makes its pictures).
- S05: "the biggest bank" in the big serif glow, like "capitalism".
- S06: the quote runs from "We bank countries" to "...the United States government." ("some of these companies in 30
  countries" and "You have to be big ..." are cut): on the interview the text stays on the right; on each B-roll beat
  the words are centred in the serif glow: countries (London), World Bank (its building), the IMF (the user's money
  animation), back on him, then the United States government in one line along the lawn of an ungraded, completely
  clear Capitol that pulls back from its dome.
- No music bed (MUSIC = False) and no sound effects in these renders: the voices only.
- FR(n)/FT(t): frame-exact times.

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

Run:  cd jpm-dimon && python3 -I -X utf8 tools/build6.py --specs                  (writes tools/media_v7.json only)
      python3 -I tools/prep2.py --spec=media_v7.json && CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I tools/prep6.py
      npx --yes hyperframes@0.9.2 remove-background assets/clips2/BANK_27585_413_x63_50_135.mp4 \
          -o assets/clips2/BANK_27585_413_x63_50_135_cut.webm --json                    (S06: him matted over the globe)
      CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I -X utf8 tools/build6.py   (index.html, compositions/)
"""
import array, json, math, os, random, sys, wave
from fontTools.ttLib import TTFont

ROOT = os.environ.get("DIMON_ROOT", "/home/user/claude-test-2.0")  # local runs: set DIMON_ROOT to the repo root
PRJ = f"{ROOT}/jpm-dimon"
COMP = f"{PRJ}/compositions"
TX = f"{ROOT}/dimon-work/tx"
F1 = 1 / 30
LEAD = 0.05
DUR = 93.20   # v5's length; v6 cuts "You have to be big ..." and takes SHIFT off it (below)


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

TIGHT0 = 14 / 30   # v9 (user): the 0.6 s of air after "JP Morgan Chase" is cut; everything after it comes 14 frames sooner
VO1_AT, VO1_IN, VO1_OUT = round(9.05 - TIGHT0, 3), 0.00, 14.10
VO2_IN, VO2_OUT = 18.40, 75.00
# v11 (user: "a very slight pause from the 11th second to the 12th, from right now to He's ... reduce that pause", and
# "a subtle pause after Grudge and then now ... remove that pause, it's looking very bad"): two spans of the narration
# (vo.wav time) are cut, each inside the silence (below -55 dB, envelope read at 10 ms): 0.40 s of air after "now."
# becomes 0.14 s, 0.37 s after "grudge," becomes 0.09 s. Everything after each cut comes that much sooner.
VO_CUTS = [(3.03, 3.29), (11.53, 11.81)]


def vo_gone(t):
    """Seconds of the narration cut before vo.wav time t."""
    return round(sum(min(max(t - a, 0.0), b - a) for a, b in VO_CUTS), 3)


def RT(t):
    """A v10 film time (a hand-placed time before the cuts) -> the v11 film time."""
    return round(t - sum(min(max(t - (a + VO1_AT - VO1_IN), 0.0), b - a) for a, b in VO_CUTS), 3)


# v6 (user): the quote starts straight at "We bank countries" (wav 3.345, "We" at 3.445) and ends on "...the United
# States government." (spoken to wav 8.26; cut at 8.512, before "You" at 8.65): "some of these companies in 30
# countries" and "You have to be big ..." are gone, so "Meet Jamie Dimon" follows "government" and everything from
# there on comes SHIFT earlier (v5: S07 at 34.85, "Meet" at 35.25, the film 93.20 s).
QGAP_CUT = 0.30          # v9: the 0.54 s of dead air between the narration and his soundbite cut to 0.23 s (user: pace it)
QUOTE_AT, QUOTE_SRC0 = RT(round(23.60 - TIGHT0 - QGAP_CUT, 3)), 275.845   # v11: after the two cuts
QUOTE_END = round(math.ceil((8.56 + 0.04 + QUOTE_AT - (QUOTE_SRC0 - 272.5)) * 30) / 30, 3)   # v9 (user): the quote
#   ends on "...the United States government." (spoken to wav 8.56) and "Meet Jamie Dimon" follows at once; "You have
#   to be big." is cut again (v8 keeps it)
MEET_GAP = 0.04                          # 29.867, on a frame. v7 (user): "You have to be big." is back
#                                                         ("big." is spoken to wav 9.38; cut at 9.61, before "You can't...")
SHIFT = round(34.85 - QUOTE_END, 3)
VO2_OFF = round(QUOTE_END + MEET_GAP - VOW[55]["start"], 3)   # v9: "Meet" 0.04 s after the quote (was 0.40)
DUR = round(DUR - SHIFT - (0.40 - MEET_GAP), 3)
QUOTE_OFF = round(QUOTE_AT - (QUOTE_SRC0 - 272.5), 3)
# the re-cut open (tools/make_music.py): Parakeet's word order (dimon-work/tx/pk_news4), starts read off the new
# voice track's envelope (10 ms frames); 5.70-6.20 is the held silence after "bigger"
NEWS = [dict(text=w, start=t) for w, t in [
    ("The", 0.58), ("name", 0.68), ("of", 0.80), ("the", 0.90), ("game", 0.99), ("in", 1.36), ("American", 1.60),
    ("capitalism,", 2.06), ("is", 3.05), ("being", 3.16), ("big,", 3.50), ("and", 4.08), ("no", 4.28), ("one", 4.60),
    ("is", 4.76), ("bigger", 5.11), ("on", 6.21), ("Wall", 6.29), ("Street", 6.50), ("than", 6.78), ("JP", 7.28),
    ("Morgan", 7.61), ("Chase.", 7.97)]]
NEWS_DUR = 8.62   # v9: ends as the narration starts


def NT(i):
    return NEWS[i]["start"]


def VT(i):
    s = VOW[i]["start"]
    return round(s + VO1_AT - VO1_IN - vo_gone(s), 3) if s < 14.2 else round(s + VO2_OFF, 3)   # v11: the cuts


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
CAPITOL_HD = ST("capitol_hd", path=f"{P_IMG}/07_US_Government_America/01_US_Capitol_west_front.jpg", edge=1920)
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
IMF_BG = ST("imf_bg", path=f"{P_IMG}/07_US_Government_America/06_Federal_Reserve_Eccles_Building.jpg", edge=1920)
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
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Italic.woff2') format('woff2'); font-weight: 400; font-style: italic; }
"""
INK = "#FBF8EC"
YELLOW = "#F4C542"                                  # v8 (user): "Wall Street" in yellow
# the Pattinson glow (from its build_v5.py): sans glow-in, serif halo, bloom frame, soft frame
GLOW_REST = "0 0 12px rgba(255,255,255,0.55), 0 0 34px rgba(255,255,255,0.22), 0 3px 10px rgba(0,0,0,0.42)"
GLOW_BLOOM = "0 0 34px rgba(255,255,255,0.95), 0 0 90px rgba(255,255,255,0.55), 0 3px 10px rgba(0,0,0,0)"
SERIF_REST = ("0 0 14px rgba(255,255,255,0.62), 0 0 42px rgba(255,255,255,0.30), 0 0 90px rgba(255,255,255,0.12), "
              "0 3px 10px rgba(0,0,0,0.35)")
SERIF_BLOOM = ("0 0 22px rgba(255,255,255,1), 0 0 60px rgba(255,255,255,0.95), 0 0 130px rgba(255,255,255,0.7), "
               "0 3px 10px rgba(0,0,0,0)")
HERO_BLOWN = ("0 0 26px rgba(255,255,255,1), 0 0 70px rgba(255,255,255,1), 0 0 150px rgba(255,255,255,0.85), "
              "0 0 240px rgba(255,255,255,0.5)")      # v11: Dario's "AI" / "Atomic" on its first frame
HERO_HALO = ("0 0 16px rgba(255,255,255,0.80), 0 0 46px rgba(255,255,255,0.46), 0 0 110px rgba(255,255,255,0.24), "
             "0 3px 10px rgba(0,0,0,0.40)")         # v11: the highlighted hero's halo, stronger than SERIF_REST
D_SQ, F25 = 0.80, 0.04                              # v11: Dario's hero type is condensed; one frame of the reel
SERIF_SOFT = ("0 0 18px rgba(255,255,255,0.85), 0 0 50px rgba(255,255,255,0.45), 0 0 100px rgba(255,255,255,0.18), "
              "0 3px 10px rgba(0,0,0,0.2)")
GOLD_REST = ("0 0 14px rgba(255,214,140,0.75), 0 0 44px rgba(255,190,90,0.38), 0 0 100px rgba(255,170,60,0.16), "
             "0 3px 10px rgba(0,0,0,0.35)")
_FONTS = {}


def _font(family, weight, italic):
    name = {("Inter Tight", 600): "InterTight-600", ("Inter Tight", 700): "InterTight-700",
            ("Inter Tight", 800): "InterTight-800"}.get((family, weight))
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
               f'style="mix-blend-mode:soft-light;opacity:{self.tex[1]};z-index:2001" />'
               f'<img id="{self.sid}-tx3" class="clip tex" src="assets/tex/ht_dots.jpg" alt="" data-start="0" '
               f'data-duration="{r3(self.dur)}" data-track-index="9" data-layout-ignore '
               f'style="mix-blend-mode:overlay;opacity:{HALFTONE};z-index:2002" />')
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
    # seeded by v5's time (v6 moved every scene after the quote SHIFT earlier; the cards keep v5's drift)
    rnd = random.Random(len(years) * 31 + int(round(t0 + (SHIFT if t0 >= QUOTE_END else 0), 3) * 10))
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
    sc.raw(f'<div id="{bid}" class="clip solid" {sc.timed(t, t + frames * F1)} data-track-index="6" data-layout-ignore '
           f'style="left:{x}px;'
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


def sp_type_word(sc, t0, t1, text, times, size=450, squeeze=0.70, base=672, track=-0.015, exit_at=None, z=None):
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
    wz = z or (sc.nz() + 300)      # v11: z, to sit over a picture placed high (S06's B-roll)
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


def sp_wolf_lockup11(sc, t1, words, y=560, size=165, color="#F4C542", exit_at=None, gap=0.14):
    """v11 (user: "of Wall Street is perfect in Helvetica ... close that gap a bit ... yellow with more of a difference
    effect ... animate it better"): the Ackman lockup with the word gap closed (0.24 -> 0.13 of the size); each word
    rises into its place out of a blur and a tall stretch in 4 frames (expo out, from its baseline); every landing is a
    negative: the word's own box inverts for 2 frames (the shot and the yellow in it go negative), and STREET's landing
    inverts the whole frame for one; the lockup creeps in (+4 %) while it holds. S03's purple negative still ends it."""
    lid = sc.uid("wolf")
    ws = [(w.upper(), t, textw(w.upper(), "Inter Tight", 800, size, track=-0.035)) for w, t in words]
    g = size * gap
    total = sum(w for *_, w in ws) + g * (len(ws) - 1)
    x = 960 - total / 2
    spans, js = [], []
    for k, (w, t, wd) in enumerate(ws):
        sid = f"{lid}-w{k}"
        spans.append(f'<span id="{sid}" class="t" style="left:{x:.0f}px;top:{y - size * 0.78:.0f}px;font-family:\'Inter Tight\';'
                     f'font-weight:800;font-size:{size}px;letter-spacing:-0.035em;color:{color};opacity:0;'
                     f'transform-origin:50% 92%;text-shadow:0 4px 18px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.4)">{esc(w)}</span>')
        js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, y: {size * 0.42:.0f}, scaleY: 1.45, filter: "blur(12px)" }}, '
                  f'{{ opacity: 1, y: 0, scaleY: 1, filter: "blur(0px)", duration: {r3(4 * F1)}, ease: "expo.out", '
                  f'immediateRender: false }}, {sc.at(t)});')
        land = round(t + 2 * F1, 3)
        blk(sc, land, 2, (round(x - 16), round(y - size * 0.84), round(wd + 32), round(size * 0.98)), "#ffffff",
            blend="difference", z=1600)
        if k == len(ws) - 1:
            blk(sc, round(land + 2 * F1, 3), 1, (0, 0, 1920, 1080), "#ffffff", blend="difference", z=1601)
        x += wd + g
    t_in, t_out = words[0][1] - F1, exit_at or t1
    js.append(f'tl.fromTo("#{lid}", {{ scale: 1 }}, {{ scale: 1.04, duration: {r3(t_out - t_in)}, ease: "none", '
              f'immediateRender: false }}, {sc.at(t_in)});')
    sc.raw(f'<div id="{lid}" class="clip grp" {sc.timed(t_in, t_out)} data-track-index="5" '
           f'data-layout-allow-overflow style="z-index:1500;transform-origin:960px {y - size * 0.3:.0f}px">{"".join(spans)}</div>', js)
    return lid


def sp_name_pop(sc, word, t, t1, size=250, y=540):
    """v11 (user: "bonus coming with the Instrument Serif animation, like the word Dario Amodei comes in the Dario
    video at the very start"): Dario's name entrance (the reel's 10.68-10.88 s, every frame at 25 fps): the word pops in
    whole and crisp in its glow, condensed, with a white square in the top-left corner (one reel frame); a square in
    the bottom-right corner (the next two); then for two frames the word's row is a negative band (the shot inverted,
    the word black in it); then it holds in its glow."""
    w = textw(word, "Instrument Serif", 400, size, track=-0.01) * D_SQ
    x, z = 960 - w / 2, sc.nz() + 800
    wid = sc.uid("nm")
    sc.raw(f'<div id="{wid}" class="clip t" {sc.timed(t, t1)} data-track-index="5" data-layout-allow-overflow '
           f'style="left:{x:.0f}px;top:{y - size * 0.56:.0f}px;font-family:\'Instrument Serif\';font-weight:400;'
           f'font-size:{size}px;letter-spacing:-0.01em;color:{INK};text-shadow:{SERIF_REST};transform:scaleX({D_SQ});'
           f'transform-origin:0 50%;z-index:{z}">{esc(word)}</div>')
    for (a, b), (bx, by, bw, bh), blend in (((t, t + F25), (0, 0, 216, 104), "normal"),
                                            ((t + F25, t + 3 * F25), (1712, 884, 208, 196), "normal"),
                                            ((t + 3 * F25, t + 5 * F25), (150, round(y - size * 0.46), 1620, round(size * 0.86)),
                                             "difference")):
        sc.raw(f'<div id="{sc.uid("np")}" class="clip solid" {sc.timed(round(a, 3), round(b, 3))} data-track-index="6" '
               f'data-layout-ignore style="left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;background:#FFFFFF;'
               f'mix-blend-mode:{blend};z-index:{z + 10}"></div>')
    return wid


def sp_diff_line(sc, words, t1, y=540, size=150, wt=800, gap=0.24):
    """v11 (user: "by his own mentor ... in Helvetica bold at the center with a different difference effect"): one
    centred line of bold Helvetica drawn in difference (white, mix-blend-mode difference): every letter is the negative
    of the face under it, so it reads on light and dark alike while Dario's faces flip under it. Each word lands in its
    final place (the line never re-centres): one frame as a solid difference block its size, then the word, settling
    from 112 % and a slight blur in 3 frames."""
    trk = -0.03
    ws = [(w.strip(",."), t, textw(w.strip(",."), "Inter Tight", wt, size, track=trk)) for w, t in words]
    g = size * gap
    total = sum(w for *_, w in ws) + g * (len(ws) - 1)
    x = 960 - total / 2
    for k, (w, t, wd) in enumerate(ws):
        blk(sc, t, 1, (round(x - 6), round(y - size * 0.40), round(wd + 12), round(size * 0.80)), "#ffffff",
            blend="difference", z=sc.nz() + 800)
        wid = sc.uid("dw")
        a = round(t + F1, 3)
        sc.raw(f'<div id="{wid}-h" class="clip t" {sc.timed(a, t1)} data-track-index="5" data-layout-allow-overflow '
               f'style="left:{x:.0f}px;top:{y - size * 0.52:.0f}px;font-family:\'Inter Tight\';font-weight:{wt};'
               f'font-size:{size}px;letter-spacing:{trk}em;color:#000000;opacity:0.62;filter:blur(13px);'
               f'z-index:{sc.nz() + 790}" data-layout-ignore>{esc(w)}</div>')   # the halo (blurred dark letters), then the word
        sc.raw(f'<div id="{wid}" class="clip t" {sc.timed(a, t1)} data-track-index="5" data-layout-allow-overflow '
               f'style="left:{x:.0f}px;top:{y - size * 0.52:.0f}px;font-family:\'Inter Tight\';font-weight:{wt};'
               f'font-size:{size}px;letter-spacing:{trk}em;color:#FFFFFF;mix-blend-mode:difference;'
               f'transform-origin:50% 55%;z-index:{sc.nz() + 800}">{esc(w)}</div>',
               [f'tl.fromTo("#{wid}", {{ scale: 1.12, filter: "blur(4px)" }}, {{ scale: 1, filter: "blur(0px)", '
                f'duration: {r3(3 * F1)}, ease: "power3.out", immediateRender: false }}, {sc.at(a)});'])
        x += wd + g


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
    per = (fh - f0) // n                                                 # v8: frames a photo (even, to the hero)
    assert fh - f0 == per * n and per >= 2, (f0, fh, n)
    T = [t0] + [round((f0 + per * k - 0.5) / 30, 3) for k in range(1, n)] + [hero_t]   # cuts half a frame early
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
            f'style="position:absolute;left:0;top:0;width:{hs}px;height:{hs}px;transform-origin:50% 50%">{"".join(inner)}'
            f'@@FIRED@@</div></div>')
    js += [f'tl.fromTo("#{cam}-g", {{ scale: {s0 / hs:.4f} }}, {{ scale: {s1 / hs:.4f}, duration: {r3(D)}, ease: "sine.in", '
           f'immediateRender: false }}, {sc.at(t0)});',
           f'tl.to("#{cam}-g", {{ scale: 1, duration: {r3(2 * F1)}, ease: "power2.out" }}, {sc.at(hero_t)});']
    for k in range(n):   # pop in on the photo's first frame, back on its second (sets at half frames: exact per frame)
        amp = pop[0] + (pop[1] - pop[0]) * k / max(1, n - 1)
        js += [f'tl.set("#{cam}-u", {{ scale: {1 + amp:.4f} }}, {sc.at(T[k])});',
               f'tl.set("#{cam}-u", {{ scale: 1 }}, {sc.at(round((f0 + per * k + 0.5) / 30, 3))});']
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
    bwd, bt = big   # v11 (user: "the FIRED word is not coming animated along with the square ... it's just still
    #   there"): FIRED sits in the card's own frame (right of the photo), so it grows with the card, pops with every
    #   photo and settles with the hero, at the same final place and size as before
    bid = f"{cam}-big"
    fired = (f'<div id="{bid}" class="clip t" {sc.timed(bt, t1)} data-track-index="5" style="left:{hs + gap:.0f}px;'
             f'top:{hs * 0.08:.0f}px;font-family:\'Inter Tight\';font-weight:800;font-size:112px;'
             f'letter-spacing:-0.035em;color:#141414">{esc(bwd)}</div>')
    card = card.replace("@@FIRED@@", fired)
    js.append(f'tl.fromTo("#{bid}", {{ opacity: 0, x: -26, filter: "blur(8px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", '
              f'duration: 0.12, ease: "power3.out", immediateRender: false }}, {sc.at(bt)});')
    push = [] if push_to == 1.0 else [   # v8 (user): no zooms after the hero lands
        f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: {push_to}, duration: 0.3, ease: "power3.out", '
        f'immediateRender: false }}, {sc.at(bt)});',
        f'tl.to("#{cam}", {{ scale: {push_to + 0.04}, duration: {r3(max(F1, t1 - bt - 0.3))}, ease: "none" }}, '
        f'{sc.at(bt + 0.3)});']
    sc.raw(f'<div id="{cam}" class="grp" data-layout-allow-overflow style="z-index:{sc.nz()};transform-origin:{cx}px {cy}px">'
           f'{card}{wb}</div>', js + push)
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
# media_v7.json["cyber"]). k = frame index from S02's first frame (film frame 254 = 8.4667 s). Rows:
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


def sp_grudge_slide(sc, t0, t1):
    """v6 (user): "and a family grudge" as the opening of the Jamie Dimon reel the user sent (instagram De__bppBwhC,
    0-1.0 s, every frame at 29.75 fps): a colour photo (Citigroup Center) under a 3x3 grid of thin dark lines, its cells
    dimmed and revealed one by one with soft white rectangles flashing in single cells; the cut-out (Sandy and Joan
    Weill) slides in from the left with heavy horizontal motion blur on an ease-out, settled by frame 11; frame 16 the
    background loses colour, 17-18 it burns to white, 19-20 it comes back black-and-white and soft, from 21 sharp; the
    couple stays in colour with a thin white edge glow; everything pushes in slowly."""
    F = lambda f: FT(t0 + f / 30)
    js = []
    bgc, bgw, bgs = sc.uid("grc"), sc.uid("grw"), sc.uid("grs")
    for bid, src, a, b in ((bgc, "gr_bg_col.jpg", t0, F(17)), (bgs, "gr_bg_bw_soft.jpg", F(19), F(21)),
                           (bgw, "gr_bg_bw.jpg", F(16), t1)):
        sc.raw(f'<img id="{bid}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(a, b)} data-track-index="2" '
               f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;transform-origin:50% 45%;'
               f'z-index:{10 if bid == bgc else 11 if bid == bgw else 12}" />')
    js += [f'tl.fromTo("#{bgc}, #{bgw}, #{bgs}", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {r3(t1 - t0)}, ease: "none", '
           f'immediateRender: false }}, {sc.at(t0)});',
           f'tl.set("#{bgw}", {{ opacity: 0.5 }}, {sc.at(F(16))});', f'tl.set("#{bgw}", {{ opacity: 1 }}, {sc.at(F(17))});']
    # the 3x3 cells: dimmed at first, revealed one by one; soft white rectangles flash in single cells
    reveal = {(2, 0): 3, (2, 1): 6, (1, 0): 7, (2, 2): 8, (1, 1): 9, (1, 2): 10, (0, 0): 11, (0, 1): 12, (0, 2): 13}
    for (c, r), f in reveal.items():
        d = sc.uid("grd")
        sc.raw(f'<div id="{d}" class="clip solid" {sc.timed(t0, F(f))} data-track-index="3" data-layout-ignore '
               f'style="left:{640 * c}px;top:{360 * r}px;width:640px;height:360px;background:url(assets/img2/{GR_PREV}) '
               f'-{640 * c}px -{360 * r}px / 1920px 1080px;z-index:20"></div>')   # v8: the previous picture
    for (c, r), f, n, op in (((2, 0), 2, 1, 0.55), ((2, 1), 4, 2, 0.82), ((2, 2), 6, 1, 0.78), ((0, 1), 11, 2, 0.5),
                             ((1, 1), 14, 1, 0.45)):
        sc.raw(f'<div id="{sc.uid("grf")}" class="clip solid" {sc.timed(F(f), F(f + n))} data-track-index="3" data-layout-ignore '
               f'style="left:{640 * c}px;top:{360 * r}px;width:640px;height:360px;background:#f4f4f2;opacity:{op};'
               f'box-shadow:0 0 30px rgba(255,255,255,0.35);z-index:21"></div>')
    blk(sc, F(15), 1, (640, 360, 640, 360), "#05070a", opacity=0.45, z=21)
    grid = "".join(f'<div style="position:absolute;left:{x}px;top:0;width:2px;height:1080px;background:rgba(8,8,10,0.55)"></div>'
                   for x in (639, 1279)) + "".join(
                   f'<div style="position:absolute;left:0;top:{y}px;width:1920px;height:2px;background:rgba(8,8,10,0.55)"></div>'
                   for y in (359, 719))
    sc.raw(f'<div id="{sc.uid("grg")}" class="clip grp" {sc.timed(t0, t1)} data-track-index="3" data-layout-ignore '
           f'style="z-index:22">{grid}</div>')
    # the burn to white, under the couple (the reel's subject stays visible over it)
    for f, op in ((16, 0.22), (17, 0.86), (18, 0.72)):
        sc.raw(f'<div id="{sc.uid("grb")}" class="clip solid" {sc.timed(F(f), F(f + 1))} data-track-index="3" data-layout-ignore '
               f'style="background:#fbfbf8;opacity:{op};z-index:23"></div>')
    # the couple: slides in from the left on an ease-out (11 frames), motion-blur steps fading, then sharp, glow edge
    cp = sc.uid("cpl")
    W, Hh, X, Y = 1500, 1124, 210, 40
    steps = [("gr_couple_mb3.png", 19, 21)]                    # v8 (user): no slide; only the reel's soft frames 19-20
    imgs = "".join(f'<img id="{cp}-m{i}" class="clip" src="assets/img2/{src}" alt="" {sc.timed(F(a), F(b))} data-track-index="4" '
                   f'style="position:absolute;left:0;top:0;width:{W}px;height:{Hh}px" />' for i, (src, a, b) in enumerate(steps))
    sharp = [(t0, F(19)), (F(21), t1)]
    imgs += "".join(f'<img id="{cp}-s{i}" class="clip" src="assets/img2/gr_couple.png" alt="" {sc.timed(a, b)} data-track-index="4" '
                    f'style="position:absolute;left:0;top:0;width:{W}px;height:{Hh}px" />' for i, (a, b) in enumerate(sharp))
    halo = (f'<img id="{cp}-h" class="clip" src="assets/img2/gr_couple_halo.png" alt="" {sc.timed(F(21), t1)} data-track-index="4" '
            f'style="position:absolute;left:0;top:0;width:{W}px;height:{Hh}px;opacity:0.9" />')
    sc.raw(f'<div id="{cp}" class="grp" data-layout-allow-overflow style="left:{X}px;top:{Y}px;width:{W}px;height:{Hh}px;'
           f'z-index:30;transform-origin:50% 40%">{halo}{imgs}</div>')
    blk(sc, t0, 1, (0, 0, 1920, 1080), "#ffffff", opacity=0.55, z=29)   # v8: the couple lands with a white flash
    js += [f'tl.fromTo("#{cp}", {{ scale: 1.0 }}, {{ scale: 1.035, duration: {r3(t1 - t0)}, ease: "none", immediateRender: false }}, '
           f'{sc.at(t0)});']
    sc.J("\n    ".join(js))

HALFTONE = 0.16   # v8 (user): the Drive's halftone pack (Copy of Halftone 2) over every scene, overlay
MUSIC = False   # v6 (user): no background music or sound effects in these renders; set True to put the bed back
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
    "sxy": ("Instrument Serif", 400, 300, "heroy"),   # v8 (user): "Wall Street" can be yellow
    "shy": ("Instrument Serif", 400, 236, "heroy"),
    "sy": ("Inter Tight", 800, 120, "sansy"),
    "nm": ("Instrument Serif", 400, 250, "name"),
    "gold": ("Instrument Serif", 400, 236, "gold"),
    "p": ("Inter Tight", 800, 96, "paper"),
    "pb": ("Inter Tight", 800, 150, "paper"),
    "ps": ("Instrument Serif", 400, 250, "paper"),
    "pss": ("Instrument Serif", 400, 220, "ink"),  # v8: dark serif on the pinboard
    # v11 (user: "wherever I say Instrument Serif glow ... this kind of animation and typography exactly as in the Dario
    # video"), read frame by frame (25 fps): normal words ("He built the", "wants to save humanity": small, spread on
    # one line, each in its final place; a glowing white square marks the word's place for 2 frames, then the word comes
    # in stretched tall and settles in 2 frames; the words leave in the order they came); hero words ("AI", "Atomic
    # Bomb": big, condensed, one frame blown out, then crisp in the glow); the highlighted hero (the "CEO": two frames
    # black in a glowing white bar, as Dario's SUDDENLY, then blown out, then a strong halo that stays)
    "dn": ("Instrument Serif", 400, 92, "dnorm"),
    "dh": ("Instrument Serif", 400, 230, "dhero"),
    "dhl": ("Instrument Serif", 400, 230, "dhl"),
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
                sq = D_SQ if kind in ("dhero", "dhl") else 1.0
                ws.append((text, t, st, textw(text, fam, wt, size, track=tr) * sq))
            gaps = [sty(st)[2] * (0.24 if sty(st)[0] == "Inter Tight" else 0.42 if sty(st)[3] == "dnorm" else 0.2)
                    for _, _, st, _ in ws]
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
                color = "#111" if kind in ("paper", "ink") else YELLOW if kind in ("heroy", "sansy") else INK
                shadow = {"sans": GLOW_REST, "sansy": GOLD_REST, "serif": SERIF_REST, "hero": SERIF_REST,
                          "heroy": GOLD_REST, "name": SERIF_REST, "dnorm": SERIF_REST, "dhero": SERIF_REST,
                          "dhl": HERO_HALO,
                          "gold": GOLD_REST, "ink": "none",
                          "paper": "0 0 18px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.5)"}[kind]
                trk = "-0.03em" if fam == "Inter Tight" else "-0.01em"
                top = base - size * 0.80
                style = (f"left:{left:.0f}px;top:{top:.0f}px;font-family:'{fam}';font-weight:{wt};font-size:{size:.0f}px;"
                         f"letter-spacing:{trk};color:{color};")
                if kind in ("dnorm", "dhero", "dhl"):    # v11: Dario's words (the hero squeezed as one box)
                    sq = "" if kind == "dnorm" else f"transform:scaleX({D_SQ});transform-origin:0 50%;"
                    fl = ' style="top:0.06em;bottom:0.12em;left:-0.08em;right:-0.08em"' if kind == "dhl" else ""
                    spans.append(f'<span id="{sid}" class="w" style="{style}{sq}"><span id="{sid}-f" class="fl"{fl}></span>'
                                 f'<span id="{sid}-t" class="wt" style="opacity:0;transform-origin:50% 72%;'
                                 f'text-shadow:{shadow}">{esc(text)}</span></span>')
                    g.setdefault("sids", []).append(sid)
                elif kind in ("serif", "hero", "heroy", "name", "gold"):
                    spans.append(f'<span id="{sid}" class="w" style="{style}"><span id="{sid}-f" class="fl"></span>'
                                 f'<span id="{sid}-t" class="wt" style="opacity:0;text-shadow:{shadow}">{esc(text)}</span></span>')
                else:
                    spans.append(f'<span id="{sid}" class="w ws" style="{style}text-shadow:{shadow};opacity:0">{esc(text)}</span>')
                a = max(t0, t)
                if kind in ("sans", "sansy"):
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
                              f'{{ opacity: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.24, ease: "expo.out", '
                              f'immediateRender: false }}, {r3(a)});')
                elif kind == "ink":  # black type on paper: sharp, in two frames
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", '
                              f'duration: {r3(2 * F1)}, ease: "power2.out", immediateRender: false }}, {r3(a)});')
                elif kind == "paper":
                    js.append(f'tl.fromTo("#{sid}", {{ opacity: 0, y: 44 }}, {{ opacity: 1, y: 0, duration: 0.28, ease: "steps(4)", '
                              f'immediateRender: false }}, {r3(a)});')
                elif kind == "dnorm":    # the glowing square marks the place, the word comes in stretched tall
                    b0 = max(t0, round(a - 2 * F25, 3))
                    js += ([f'tl.set("#{sid}-f", {{ opacity: 1 }}, {r3(b0)});', f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(a)});']
                           if a - b0 > 0.02 else [])
                    js += [f'tl.set("#{sid}-t", {{ opacity: 1, scaleY: 1.42, filter: "blur(1.5px)", textShadow: "{SERIF_BLOOM}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ scaleY: 1.12, filter: "blur(0px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F25)});',
                           f'tl.set("#{sid}-t", {{ scaleY: 1, textShadow: "{SERIF_REST}" }}, {r3(a + 2 * F25)});']
                elif kind == "dhero":    # one frame blown out, then crisp in the glow
                    js += [f'tl.set("#{sid}-t", {{ opacity: 1, filter: "blur(7px)", textShadow: "{HERO_BLOWN}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(1.5px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F25)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {r3(a + 2 * F25)});']
                elif kind == "dhl":      # highlighted: black in the glowing bar, then blown out, then a halo that stays
                    js += [f'tl.set("#{sid}-f", {{ opacity: 1 }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ opacity: 1, color: "#0b0b0b", textShadow: "none" }}, {r3(a)});',
                           f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(a + 2 * F25)});',
                           f'tl.set("#{sid}-t", {{ color: "{INK}", filter: "blur(7px)", textShadow: "{HERO_BLOWN}" }}, {r3(a + 2 * F25)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(0px)", textShadow: "{HERO_HALO}" }}, {r3(a + 3 * F25)});']
                elif kind == "serif":
                    b0 = max(t0, a - 4 * F1)
                    js += [f'tl.set("#{sid}-f", {{ opacity: 1, filter: "blur(3px)" }}, {r3(b0)});',
                           f'tl.set("#{sid}-f", {{ filter: "blur(0px)" }}, {r3(b0 + F1)});',
                           f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(max(b0 + 2 * F1, a - F1))});',
                           f'tl.set("#{sid}-t", {{ opacity: 1, filter: "blur(8px)", textShadow: "{SERIF_BLOOM}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(3px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("#{sid}-t", {{ filter: "blur(0px)", textShadow: "{SERIF_REST}" }}, {r3(a + 3 * F1)});']
                else:  # hero, gold and name words burst in blown-out, then settle crisp with their halo
                    rest = GOLD_REST if kind in ("gold", "heroy") else SERIF_REST
                    js += [f'tl.set("#{sid}-t", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {r3(a)});',
                           f'tl.set("#{sid}-t", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("#{sid}-t", {{ scale: 1.005, filter: "blur(2.5px)" }}, {r3(a + 3 * F1)});',
                           f'tl.set("#{sid}-t", {{ scale: 1, filter: "blur(0px)", textShadow: "{rest}" }}, {r3(a + 4 * F1)});']
            if g["exit"] == "bar":            # v8: one white bar the length of the line (the Heath reel's f187-188)
                hb = max(sty(st)[2] for _, _, st, _ in ws)
                spans.append(f'<span class="lbar" style="left:{x:.0f}px;top:{base - hb * 0.58:.0f}px;width:{Wt:.0f}px;'
                             f'height:{hb * 0.68:.0f}px"></span>')
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
        if g["exit"] in ("bars", "bar"):   # v8: the Heath reel's words turning into white bars on the way out
            tb = r3(t1 - 2 * F1)
            js.append(f'tl.set("#{gid} .wt, #{gid} .ws", {{ opacity: 0 }}, {tb});')
            js.append(f'tl.set("#{gid} .{"fl" if g["exit"] == "bars" else "lbar"}", {{ opacity: 1, filter: "blur(0px)" }}, {tb});')
        if g["exit"] == "order":
            sids = g.get("sids", [])
            for k, sid in enumerate(sids):
                js.append(f'tl.set("#{sid}", {{ opacity: 0 }}, {r3(t1 - (len(sids) - 1 - k) * F25)});')
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
  #root .lbar {{ position: absolute; opacity: 0; background: #ffffff; box-shadow: 0 0 16px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.45); }}
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
cap([[N_(11, "s"), N_(12, "s"), N_(13, "s"), N_(14, "s")]], end=CUT(NT(15)), scrim=0.45)   # v8: centred (user)
cap([[N_(16, "s")], [N_(17, "sx@300"), N_(18, "sx@300")]], end=round(CUT(NT(19)) + 0.1, 3))   # v10 (user): "Wall Street" white here, not yellow
cap([[(NEWS[19]["text"], round(NT(19) + 0.1, 3), "s")]], end=CUT(NT(20)))   # v9 (user): "than" landed under the end of "Street"

# ---- S02  8.50-12.365  "This is the most influential man in America right now."  The Glitchy JP Morgan Chase Cyber
#      Portrait (user's picture) in the Metro Media House Alex Karp / Palantir opening, with Hemant Taneja's cards and
#      the seal (user, v6 note 2; spec_s02.md). No pop-up, no flicker of live frames, one white flash.
s = Scene("s02", S2_0, CUT(VT(10)), tex=(0.05, 0.0))
SWAP = round(CUT(VT(8)) + 0.07, 3)
sp_cyber_user(s, [
    (CARD["fortune"], 395, 330, 520, 288, round(10.86 - TIGHT0, 3), False, SWAP),
    (CARD["congress"], 1562, 780, 416, 260, round(11.00 - TIGHT0, 3), False, SWAP),
    (CARD["whitehouse"], 1537, 330, 434, 244, round(11.20 - TIGHT0, 3), False, None),
    (CARD["press"], 372, 770, 326, 254, round(11.40 - TIGHT0, 3), False, None),
    (CARD["cash"], 395, 330, 520, 288, SWAP, True, None),
    (CARD["park"], 1562, 780, 416, 260, round(SWAP + 2 * F1, 3), True, None),
], seal_at=VT(7), push=(VT(6), VT(8)), part_b=67)
# plain, centred, aligned (user: "text can be normal ... adjusting size"): small sans over a big serif word, on fixed
# baselines, like the "in American / capitalism" lockup; four groups as in v5 (the first split into its two lines)
CAP_END1 = round(VT(5) - 2 * F1, 3)                                          # 10.663, when "man in" arrives
# v11 (user: "I don't want the text to be in the center. I want it at the bottom, and all of it in Instrument Serif
# glow ... no Helvetica above and serif down"): Dario's normal words and heroes along the bottom (title-safe), each
# line replacing the last, the words leaving in the order they came: "This is the most" / INFLUENTIAL / "man in"
# AMERICA / "right now"
BOT_N, BOT_H = 930, 902
cap([[W_(0, "dn"), W_(1, "dn"), W_(2, "dn"), W_(3, "dn")]], y=BOT_N, scrim=0.42, end=round(VT(4) - F25, 3), exit="order")
cap([[W_(4, "dh@210")]], y=BOT_H, scrim=0.42, end=round(VT(5) - F25, 3), exit="order")
cap([[W_(5, "dn"), W_(6, "dn"), W_(7, "dh@190")]], y=BOT_H, scrim=0.42, end=round(VT(8) - F25, 3), exit="order")
cap([[W_(8, "dn"), W_(9, "dn")]], y=BOT_N, scrim=0.42, end=CUT(VT(10)), exit="order")

# ---- S03  12.36-15.07  "He's basically the CEO of Wall Street,"  (real video only; Pattinson's transitions)
s = Scene("s03", CUT(VT(10)), CUT(VT(17)))
s.v("GAME", 61.55, CUT(VT(10)), RT(round(12.83 - TIGHT0, 3)), push=(1.0, 1.03))             # He's basically: the 270 Park podium
s.v("CHAIR", 1265.2, RT(round(12.83 - TIGHT0, 3)), CUT(VT(13)), push=(1.0, 1.025))           # the: Stanford, a straight cut (v6: no slide)
camC, _ = s.vfile("ceo_slow.mp4", CUT(VT(13)), CUT(VT(14)), z=s.nz() + 60)   # CEO: walking in with his detail ...
sp_window_ease(s, camC, CUT(VT(13)) + 0.08, CUT(VT(14)), to=0.64, cards=[   # ... eases back into a window (Pattinson)
    (DIMON_PHOTOS[0], 215, 330, 330, 220, RT(round(13.32 - TIGHT0, 3)), -4),
    (DIMON_PHOTOS[1], 1712, 300, 300, 200, RT(round(13.38 - TIGHT0, 3)), 3),
    (LEADERS[3], 250, 820, 320, 214, RT(round(13.44 - TIGHT0, 3)), 3),
    (PIN_DIMON[2], 1690, 830, 300, 200, RT(round(13.50 - TIGHT0, 3)), -3)])
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
WOLF_LOCK = sp_wolf_lockup11(s, CUT(VT(17)), [("of", VT(14)), ("Wall", VT(15)), ("Street", VT(16))], y=560, size=165,
                           color=YELLOW,
                           exit_at=round(CUT(VT(17)) - F1, 3))   # Ackman 7.00; v8: centred and yellow (user)
XF = round(CUT(VT(17)) - 2 * F1, 3)                                    # Ackman 6.96: purple negative, then white
blk(s, XF, 1, (0, 0, 1920, 1080), "#ffffff", blend="difference", z=1400)
blk(s, XF, 1, (0, 0, 1920, 1080), "#6a1fd0", blend="multiply", opacity=0.62, z=1401)
s.J(f'tl.set("#{WOLF_LOCK} .t", {{ color: "#F59BE0" }}, {s.at(XF)});')
s.whiteframe(round(CUT(VT(17)) - F1, 3), 1)
cap([[W_(10, "dn"), W_(11, "dn")]], end=RT(round(12.83 - TIGHT0, 3)), scrim=0.6, exit="order")   # v11: Dario's serif
cap([[W_(12, "dn"), W_(13, "dhl", "CEO")]], end=CUT(VT(14)), scrim=0.45, exit="order")             # the CEO highlighted

# ---- S04  15.07-20.86  "a guy who got fired in 1998 by his own mentor over a bonus and a family grudge,"
s = Scene("s04", CUT(VT(17)), CUT(VT(35)))
F0 = CUT(VT(17))
FLIP_PER = (round(CUT(VT(23)) * 30) - math.ceil(F0 * 30 - 1e-6) - 7) // 9   # v8 (user): an even stream (3 frames a
FLIP_HERO = round((math.ceil(F0 * 30 - 1e-6) + 9 * FLIP_PER) / 30 - 0.0004, 4) # photo) to the hero, the square's zoom
sp_fired_flip(s, F0, FLIP_HERO, CUT(VT(23)), YOUNG6[:-1], YOUNG6[-1],          # ending on it; no zooms after
              [(VOW[k]["text"], VT(k)) for k in (17, 18, 19, 20)], ("FIRED", VT(21)), push_to=1.0)
sp_roller(s, CUT(VT(23)), CUT(VT(24)), list(range(1990, 1999)), land_at=VT(23) + 0.22, cards=[], video_bg=("MPB", 850.0),
          invert_digits=2)                                             # in 1998 (user: fine with Citigroup behind)
sp_dario_faces(s, CUT(VT(24)), CUT(VT(28)), WEILL)                     # by his own mentor: Dario's faces, Sandy Weill
BON = RT(round(18.74 - TIGHT0, 3))
G0 = CUT(VT(31))                                                       # 19.24, "and": the grudge beat starts
sp_grid4(s, CUT(VT(28)), BON, [("P07", 1.2), ("MONEY", 1.0), ("MPB", 1784.0), ("HOW", 781.5)], step=2)   # faster
blk(s, CUT(VT(28)), 1, (0, 0, 1920, 1080), "#000000", opacity=0.7, z=1300)   # Dario 18.40: in dark for a frame
s.v("BONUS", 5.90, BON, G0, grade="", push=(1.0, 1.03), xyz=(0.5, 0.46, 1.09))   # over a bonus: the user's cartoon
GR_PREV = ST("gr_prev", key="BONUS", t=round(5.90 + (G0 - BON), 3), frame="FULL", frame_xyz=[0.5, 0.46, 1.09])
sp_grudge_slide(s, G0, CUT(VT(35)))                                    # and a family grudge: the reel's opening (user)
sp_diff_line(s, [(VOW[k]["text"], VT(k)) for k in (24, 25, 26, 27)], CUT(VT(28)))   # v11: bold, centred, difference
cap([[W_(28, "s"), W_(29, "s")]], end=BON)
sp_name_pop(s, "bonus", VT(30), G0)                                    # v11: Dario's name entrance (user)
cap([[W_(31, "s"), W_(32, "s"), W_(33, "s"), W_(34, "sh@200", "Grudge")]], scrim=0.42,   # v8: one line, centred; v10: capital G (user)
    end=CUT(VT(35)) - 0.02)                                            # and a family / grudge: centred lockup

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
cap([[W_(35, "s"), W_(36, "s"), W_(37, "s")], [W_(38, "sh"), W_(39, "sh")]], end=CUT(VT(40)))   # v6: "biggest bank" in the big serif glow, like capitalism (user)
cap([[W_(40, "s"), W_(41, "s")], [W_(42, "sh")]], end=QUOTE_AT - 0.05, exit="fade")

# ---- S06  23.60-28.77  Dimon in his own words. v6 (user): straight from "We bank countries" to "...the United States
#      government." On the interview the text stays on the right with the quote marks (the Fink reel's Rogan screen:
#      his globe picture behind him, he is matted above it). On each B-roll beat the words are centred in Dario's serif
#      glow: countries (London from the air), the World Bank (its building), the IMF (the user's money animation), back
#      on him for "we bank the", then the United States government on a completely clear, ungraded Capitol that comes
#      in on Karp's pull-back ease.
s = Scene("s06", QUOTE_AT, QUOTE_END, tex=(0.05, 0.0))
SY = lambda t: round(QUOTE_SRC0 + (t - QUOTE_AT), 3)
IV = dict(xyz=(0.63, 0.5, 1.35), push=(1.0, 1.03))
IV_END = CUT(QT(22))                                                   # his close-up ends on "United" (the source cuts
#                                                                        to a wide two-shot at 280.99 s, under the Capitol)
s.v("BANK", SY(QUOTE_AT), QUOTE_AT, IV_END, **IV)                       # the interview (one continuous take)
SEGS = [QUOTE_AT, CUT(QT(12)), CUT(QT(19))]                            # back on the interview at these times
sp_ghost(s, QUOTE_AT, IV_END, GHOST, (800, 0, 1220, 1080), SEGS, opacity=0.45)
IV_CID = CL("BANK", SY(QUOTE_AT), round(IV_END - QUOTE_AT, 3), xyz=IV["xyz"])
camM, vidM = s.uid("cam"), s.uid("v")
s.raw(f'<div class="cam" id="{camM}" style="left:0px;top:0px;width:1920px;height:1080px;z-index:{s.nz()};'
      f'transform-origin:50% 50%"><video id="{vidM}" class="clip" src="assets/clips2/{IV_CID}_cut.webm" muted playsinline '
      f'{s.timed(QUOTE_AT, IV_END)} data-hf-media-start-basis="local" data-media-start="0"{gattr("doc")} data-track-index="2" '
      f'style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover"></video></div>',
      [f'tl.fromTo("#{camM}", {{ scale: {IV["push"][0]} }}, {{ scale: {IV["push"][1]}, duration: {r3(IV_END - QUOTE_AT)}, '
       f'ease: "none" }}, {s.at(QUOTE_AT)});'])
QX = 1110
G = [  # on the interview: the text on the right, as v5 had it
    [[Q_(9, "s"), Q_(10, "s")]],
    [[Q_(12, "sm"), Q_(13, "sm"), Q_(14, "sm")]],
    [[Q_(19, "sm"), Q_(20, "sm"), Q_(21, "sm")]],
]
SPANS = [(QUOTE_AT, CUT(QT(11))), (CUT(QT(12)), CUT(QT(15))), (CUT(QT(19)), CUT(QT(22)))]
for g, (a, b) in zip(G, SPANS):
    cap(g, x=QX, y=520, align="left", end=b, exit="blur")


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
for g, (a, b) in zip(G, SPANS):
    top, bot, right = cap_box(g)
    QSPANS.append((a, b, (QX - 78, top - 132), (right - 4, bot - 74)))
sp_quotes(s, QSPANS)
BZ = s.nz() + 1000                                                     # the B-roll over him, straight cuts
s.v("BANK", 0.30, CUT(QT(11)), CUT(QT(12)), push=(1.0, 1.04), xyz=(0.55, 0.55, 1.15), z=BZ)   # countries: London
s.img(WB_BLDG, CUT(QT(15)), CUT(QT(17)), push=(1.0, 1.05), z=BZ)                             # World Bank: its building
s.img(IMF_BG, CUT(QT(17)), CUT(QT(19)), push=(1.0, 1.06), z=BZ)                             # the IMF: an institution's
#   v10 (user: "from IMF, remove the money symbol"): the money animation over the facade is gone
CAP_T0 = CUT(QT(22))                                                   # the United States government: the Capitol,
CAP_T1 = QUOTE_END                                                     # ... to the end of the quote (v9)
CAP_D = round(CAP_T1 - CAP_T0, 3)                                      # ungraded, pulling back from its dome
cam, _ = s.img(CAPITOL_HD, CAP_T0, CAP_T1, grade="", push=None, origin="50% 24%", z=BZ)
pk = round(CAP_D / 0.48, 4)
s.J(f'tl.fromTo("#{cam}", {{ scale: 1.35 }}, {{ scale: {round(1 + 0.35 * math.exp(-CAP_D / 0.48), 4)}, '
    f'duration: {r3(CAP_D)}, ease: (p) => (1 - Math.exp(-{pk} * p)) / (1 - Math.exp(-{pk})), immediateRender: false }}, '
    f'{s.at(CAP_T0)});')
cap([[Q_(11, "sh@240", "countries")]], end=CUT(QT(12)))                                     # centred, Dario's glow
cap([[Q_(15, "sh@210", "World"), Q_(16, "sh@210", "Bank")]], end=CUT(QT(17)), scrim=0.42)
cap([[Q_(17, "s@64", "the")], [Q_(18, "sh@250", "IMF")]], lh=1.0, end=CUT(QT(19)), scrim=0.62)   # the bills are bright
# v11 (user): "United States government" typed like "JPMorgan Chase" (Dario's DISAPPEAR), at the centre: one line in
# its final centred layout, squeezed to 0.70 like Dario's type; each word types letter by letter across its own spoken
# span ("government." is spoken to wav 8.56), the newest letter flaring; it holds, then Dario's tiles take it out on
# the frame before "Meet". A soft dark band behind the line keeps it readable on the white building (the dome and the
# lawn stay clear above and below).
US_TXT = "United States government"
US_SIZE = round(1580 / 0.70 / textw(US_TXT, "Instrument Serif", 400, 100, track=-0.015) * 100)
US_END = round(8.56 + QUOTE_OFF, 3)                                    # "government." ends
US_SPANS = [(QT(22), QT(23)), (QT(23), QT(24)), (QT(24), round(QT(24) + 0.6 * (US_END - QT(24)), 3))]
US_T = []
for (wa, wb), word in zip(US_SPANS, US_TXT.split()):
    for k in range(len(word)):
        US_T.append(round((round((wa + k * (wb - wa) / len(word)) * 60) - 0.5) / 60, 4))   # on 60 fps frames
s.raw(f'<div id="{s.uid("usb")}" class="clip solid" {s.timed(round(CAP_T0, 3), CAP_T1)} data-track-index="4" '
      f'data-layout-ignore style="background:linear-gradient(180deg, rgba(0,0,0,0) 30%, rgba(4,8,16,0.50) 44%, '
      f'rgba(4,8,16,0.56) 56%, rgba(0,0,0,0) 70%);z-index:{BZ + 40}"></div>')
sp_type_word(s, CAP_T0, CAP_T1, US_TXT, US_T, size=US_SIZE, squeeze=0.70, base=round(540 + 0.30 * US_SIZE),
             exit_at=CAP_T1, z=BZ + 60)

# ---- S07  29.87-37.86  "Meet Jamie Dimon, the golden boy of Wall Street, the guy everyone said was next in line to run
#      the biggest financial company in the world."
#      v8 (user, 10 Nov): rebuilt again, exactly like the opening of the Heath Ledger reel (instagram DfXuoMjR0Ru). The
#      reel is a 60 fps edit, so this scene is timed on a 60 fps grid (F8 frames) and the film renders at 60 fps; every
#      photo is held for the reel's own number of frames (notes/v8/heath60.md has the reel's shot list). The user's notes:
#      - photos only from their folder for this part (tools/prep8.py), every face on the frame's centre line like
#        Heath's, filling the frame; video too, more of it toward the end;
#      - the words centred, in the film's Instrument Serif glow; "The Golden Boy" in gold Helvetica where the reel has
#        its red "Joker", over their cell picture; "of Wall Street" in Helvetica where it has "Hollywood", over their
#        Wall St photos;
#      - the reel's devices: difference rectangles, black frames, blur-ins, the vertical whip, the strobe and the top
#        difference box, the X-ray, the silhouette, the focus window, the lens blur, the punch-ins ("click cam").
T7, S7_END = QUOTE_END, CUT(VT(81))
s = Scene("s07", T7, S7_END, tex=(0.04, 0.0))
FR7 = lambda n: FT(T7 + n / 60)                         # n: a 60 fps frame of the scene
K7 = lambda i: max(0, round((VT(i) - T7) * 60))
E7 = round((S7_END - T7) * 60)                          # the section's length in 60 fps frames (480)
SANS7 = "0 2px 14px rgba(0,0,0,0.55)"                   # the reel's plain white words, a soft dark shadow
REEL7 = "0 0 22px rgba(255,255,255,0.40), 0 2px 14px rgba(0,0,0,0.62)"   # v10: with the reel's soft white bloom
G7 = json.load(open(f"{PRJ}/assets/img2/gz_boxes.json")) if os.path.exists(f"{PRJ}/assets/img2/gz_boxes.json") else \
    {"highlight": [1068, 148, 1919, 459], "portraits": [[40, 504, 561, 1165], [574, 505, 1035, 1165]]}
FULL = (0, 0, 1920, 1080)


def m_img(src, a, b, istyle="", z=None):
    """A still for frames [a, b): dead still, no grade (the reel never moves a photo)."""
    return s.img(src, FR7(a), FR7(b), grade="", push=None, istyle=istyle, z=z)


def m_vid(key, t, a, b, xyz=None, z=None, box=None, vstyle=""):
    """A video shot for frames [a, b), no grade and no drift (the reel's cuts); xyz centres a face (prep2 crop)."""
    return s.v(key, t, FR7(a), FR7(b), grade="", push=None, xyz=xyz, z=z, box=box, vstyle=vstyle)


def m_word(text, a, b, x, y, fam="Inter Tight", wt=700, size=96, color="#FFFFFF", align="left", shadow=SANS7, z=None,
           italic=False, track=None, opacity=1.0):
    """A word on screen for frames [a, b), its vertical centre at y; returns (id, left, width)."""
    wid = s.uid("w")
    trk = track if track is not None else (-0.03 if fam == "Inter Tight" else -0.01)
    tw = textw(text, fam, wt, size, italic=italic, track=trk)
    left = {"left": x, "right": x - tw, "center": x - tw / 2}[align]
    top = y - size * (0.52 if fam == "Inter Tight" else 0.56)
    s.raw(f'<div id="{wid}" class="clip t" {s.timed(FR7(a), FR7(b))} data-track-index="5" data-layout-allow-overflow '
          f'style="left:{left:.0f}px;top:{top:.0f}px;font-family:\'{fam}\';font-weight:{wt};font-size:{size}px;'
          f'{"font-style:italic;" if italic else ""}{f"opacity:{opacity};" if opacity != 1.0 else ""}'
          f'letter-spacing:{trk}em;color:{color};text-shadow:{shadow};z-index:{z or s.nz() + 500}">{esc(text)}</div>')
    return wid, left, tw


def m_bar(a, b, left, y, w, h, blur=0, z=None):
    """The reel's white bar: the size of the coming word, solid, for frames [a, b)."""
    bid = s.uid("bar")
    s.raw(f'<div id="{bid}" class="clip solid" {s.timed(FR7(a), FR7(b))} data-track-index="5" data-layout-ignore '
          f'style="left:{left:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;background:#FFFFFF;'
          f'{f"filter:blur({blur}px);" if blur else ""}z-index:{z or s.nz() + 520}"></div>')
    return bid


def m_solid(a, b, color):
    """A full black or white frame (the reel's single black frames and strobes), over everything in the scene."""
    s.raw(f'<div id="{s.uid("fr")}" class="clip solid" {s.timed(FR7(a), FR7(b))} data-track-index="6" '
          f'style="background:{color};z-index:{s.nz() + 900}"></div>')


def m_box(a, b, box, color, blend="normal", z=None):
    """A flat box for frames [a, b): blend 'difference' with light grey is the reel's negative rectangle
    (inside = 202 - picture); 'normal' grey is its box flash; a translucent black or white dims or lifts a frame."""
    x, y, w, h = box
    s.raw(f'<div id="{s.uid("box")}" class="clip solid" {s.timed(FR7(a), FR7(b))} data-track-index="6" data-layout-ignore '
          f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};mix-blend-mode:{blend};'
          f'z-index:{z or s.nz() + 700}"></div>')


def m_scale(cam, steps, origin="50% 42%"):
    """Scale sets on a shot, one per listed frame: the click cam (the reel's +7.5 %, +6.5 %, +2 % over 3 frames),
    the first photo's pull-back, the blur-in's settle."""
    s.J(f'tl.set("#{cam}", {{ transformOrigin: "{origin}" }}, {s.at(FR7(steps[0][0]))});')
    for f, sc in steps:
        s.J(f'tl.set("#{cam}", {{ scale: {sc} }}, {s.at(FR7(f))});')


def cap_layout(words, y=540, lh=0.92):
    """Where build_captions puts a one-line group's words: [(left, width, size)], and the line's baseline."""
    ws = []
    for text, st in words:
        fam, wt, size, kind = sty(st)
        ws.append((textw(text, fam, wt, size, track=-0.01 if fam != "Inter Tight" else -0.03), size, fam))
    gaps = [sz * (0.24 if fam == "Inter Tight" else 0.2) for _, sz, fam in ws]
    tot = sum(w for w, _, _ in ws) + sum(gaps[1:])
    h = max(sz for _, sz, _ in ws)
    base = y - h * lh / 2 + h * lh * 0.80
    out, acc = [], 960 - tot / 2
    for k, (w, sz, _) in enumerate(ws):
        if k:
            acc += gaps[k]
        out.append((acc, w, sz))
        acc += w
    return out, base


def m_run(shots, f0, flow=True):
    """A photo run: [(picture or (key, t, xyz), frames)] from frame f0, each held its frames; returns the cut frames
    and the cams. v9 (user: the pictures came "very abrupt, robotic and static"): each picture drifts the whole time
    it is on (a slow push, alternating in and out), and comes in through a 3-frame defocus, so the run flows."""
    cuts, cams, f = [], [], f0
    for k, (src, n) in enumerate(shots):
        if isinstance(src, tuple):
            cam, _ = m_vid(src[0], src[1], f, f + n, xyz=src[2])
        else:
            cam, _ = m_img(src, f, f + n)
        if flow:
            a, b = (1.0, 1.045) if k % 2 == 0 else (1.045, 1.0)
            s.J(f'tl.fromTo("#{cam}", {{ scale: {a} }}, {{ scale: {b}, duration: {r3(n / 60)}, ease: "none", '
                f'immediateRender: false }}, {s.at(FR7(f))});')
            s.J(f'tl.fromTo("#{cam}", {{ filter: "blur(9px)" }}, {{ filter: "blur(0px)", duration: {r3(3 / 60)}, '
                f'ease: "power1.out", immediateRender: false }}, {s.at(FR7(f))});')
        cuts.append(f)
        cams.append(cam)
        f += n
    return cuts + [f], cams


def h_word(text, a, b, x, y, size=88, wt=600, align="left", bar=2, out=0, box=0, fam="Inter Tight", italic=False,
           color="#FFFFFF", track=None):
    """The reel's word (v10): a solid white bar its size for `bar` frames, then the word for [a, b). `box`: the word
    first sits in a white box for that many frames (the reel's "Ledger"). `out`: it turns back into a bar for its
    last frames (the reel's words -> bars). x is its left edge, right edge or centre by `align`; y its centre."""
    trk = track if track is not None else (-0.03 if fam == "Inter Tight" else -0.01)
    tw = textw(text, fam, wt, size, italic=italic, track=trk)
    left = {"left": x, "right": x - tw, "center": x - tw / 2}[align]
    bh, pad = size * (0.80 if fam == "Inter Tight" else 0.70), size * 0.07
    if bar:
        m_bar(a - bar, a, left - pad, y, tw + 2 * pad, bh)
    if box:
        m_box(a, a + box, (round(left - pad * 1.6), round(y - bh / 2 - 5), round(tw + pad * 3.2), round(bh + 10)),
              "rgba(255,255,255,0.80)", z=s.nz() + 490)
    wid, _, _ = m_word(text, a, b - out, left, y, fam=fam, wt=wt, size=size, color=color, shadow=REEL7, italic=italic,
                       track=trk)
    if out:
        m_bar(b - out, b, left - pad, y, tw + 2 * pad, bh)
    return wid, left, tw


def h_line(words, x=960, gap=0.30):
    """A centred line of words [(text, size, weight, track)]: their left edges, the line's left edge and width."""
    ws = [textw(t, "Inter Tight", wt, sz, track=trk) for t, sz, wt, trk in words]
    gaps = [gap * max(words[k][1], words[k + 1][1]) * 0.92 for k in range(len(words) - 1)]
    tot = sum(ws) + sum(gaps)
    out, acc = [], x - tot / 2
    for k, w in enumerate(ws):
        out.append(acc)
        acc += w + (gaps[k] if k < len(gaps) else 0)
    return out, x - tot / 2, tot


def h_blur(wid, f, px):
    s.J(f'tl.set("#{wid}", {{ filter: "blur({px}px)" }}, {s.at(FR7(f))});')


W7 = {k: K7(i) for k, i in (("meet", 55), ("jamie", 56), ("dimon", 57), ("the1", 58), ("golden", 59), ("boy", 60),
                            ("of", 61), ("wall", 62), ("street", 63), ("the2", 64), ("guy", 65), ("every", 66),
                            ("said", 67), ("was", 68), ("next", 69), ("in1", 70), ("line", 71), ("to", 72),
                            ("run", 73), ("the3", 74), ("biggest", 75), ("fin", 76), ("comp", 77), ("in2", 78),
                            ("the4", 79), ("world", 80))}
CAP_Y = 560                                                # v8/v9 (user): the words in the middle of the frame
FACE_BOX = (480, 280, 960, 540)                            # the reel's half-frame negative box, on the first face

# ---- 1. Meet Jamie Dimon: the reel's name runs (f0-45 and f86-133 at 60 fps), photo for photo and frame for frame:
#      4+5 (under the negative box), 4+4, 10, 9, 8 (the blur-in), then 10, 10, 9, 10, 9; black frames at 4 and 14
# v9 (user: "exactly like the Heath Ledger video ... maintain symmetry, maintain equality: each photo gets the same
# frames up to the Joker part ... the pictures are not center-aligned"): five portraits from the user's Drive folder,
# every face at the same size on the same eye line (tools/prep8.py fb), each held the same number of frames, dead still;
# the reel's devices in its order: soft bars, the negative box across the first cut, a black frame, the lift and the
# blur-in on the last, the whip. "Meet" opens the section, so the run ends where the gold word starts.
NAME9 = ["h9_a01.jpg", "h9_a22.jpg", "h9_a03.jpg", "h9_a04.jpg", "h9_a06.jpg"]   # v10: all front-facing, youngest
#   to today; h9_a22 is the user's new front-on college photo (tools/prep10.py)
M8_RUN_END = W7["golden"] - 10 - 13 - 4
H9 = (M8_RUN_END - 1) // len(NAME9)                       # frames a portrait (one black frame in the run)
M8_cut = [0, H9, 2 * H9 + 1, 3 * H9 + 1, 4 * H9 + 1, 5 * H9 + 1]
M8_cams = [m_img(src, M8_cut[k], M8_cut[k + 1] - (1 if k == 1 else 0))[0] for k, src in enumerate(NAME9)]
M8_WHIP = M8_cut[-1]
FACE_BOX9 = (480, 250, 960, 540)
m_box(H9 - 4, H9 + 4, FACE_BOX9, "#CACACA", blend="difference")   # the negative box across the first cut (f5-13)
m_box(H9 - 4, H9 - 3, FULL, "rgba(0,0,0,0.43)", z=s.nz() + 690)  # it comes in dim (f5)
m_box(H9 + 3, H9 + 4, FULL, "rgba(0,0,0,0.40)", z=s.nz() + 690)  # and dims before the black (f13)
m_solid(2 * H9, 2 * H9 + 1, "#000000")                           # the black frame (f14)
m_box(M8_cut[4] - 2, M8_cut[4], FULL, "rgba(255,255,255,0.16)")   # the lift before the blur-in (f36-37)
m_img("h9_a06b.jpg", M8_cut[4], M8_cut[4] + 1, z=s.nz() + 30)     # the blur-in (f38)
m_img("h9_whip1.jpg", M8_WHIP, M8_WHIP + 2)              # f46-47: the photo smeared vertically,
m_img("h9_whip2.jpg", M8_WHIP + 2, M8_WHIP + 4)          # f48-49: a pure grey smear
M8_CELL = M8_WHIP + 4                                      # 98
# v10 (user: "exact typography ... the placement is the Heath Ledger video's"): the reel's name flank. Bold sans, cap
# height 75 px, the words either side of the face on the frame's centre row: the left word's right edge at x 473, the
# right word's left edge at x 1401 (notes/v7/heath_spec.md). Soft bars at the name places first (f1-3, f5); "Jamie"
# comes blurred under the negative box and is sharp on its word; "Dimon" is a white bar until it is said, then sits in
# a white box for two frames (the reel's "Ledger"); both blur with the blur-in and smear with the whip.
NAME_Y, NAME_XL, NAME_XR, NAME_SZ = 543, 473, 1401, 104
M8_jw = textw("Jamie", "Inter Tight", 700, NAME_SZ, track=-0.03)
M8_dw = textw("Dimon", "Inter Tight", 700, NAME_SZ, track=-0.03)
for a_, b_ in ((1, 4), (5, 6)):
    m_bar(a_, b_, NAME_XL - M8_jw, NAME_Y, M8_jw, NAME_SZ * 0.62, blur=9)
    m_bar(a_, b_, NAME_XR, NAME_Y, M8_dw, NAME_SZ * 0.62, blur=9)
M8_j, _, _ = m_word("Jamie", W7["jamie"] - 4, M8_WHIP + 2, NAME_XL, NAME_Y, wt=700, size=NAME_SZ, align="right",
                    shadow=REEL7)
for k, px in enumerate((15, 11, 7, 4)):
    h_blur(M8_j, W7["jamie"] - 4 + k, px)
h_blur(M8_j, W7["jamie"], 0)
M8_d, _, _ = h_word("Dimon", W7["dimon"], M8_WHIP + 2, NAME_XR, NAME_Y, size=NAME_SZ, wt=700, bar=5, box=2)
for wid in (M8_j, M8_d):
    h_blur(wid, M8_cut[4], 9)                              # the blur-in frame: the words defocus with the picture
    h_blur(wid, M8_cut[4] + 1, 0)
    s.J(f'tl.set("#{wid}", {{ scaleY: 2.4, filter: "blur(8px)", opacity: 0.85 }}, {s.at(FR7(M8_WHIP))});')   # the whip

# ---- 2. The Golden Boy: the user's cell picture (the reel's Joker, f49-85, frame for frame; the hold is longer to
#      reach "of")
M8_WALL = W7["of"] - 9                                     # the Wall Street picture enters as a negative (f86)
m_img("h8_cell.jpg", M8_CELL, M8_WALL)
M8_RED = "#E7323C"                                         # v10 (user): the reel's red, as its "Joker" is
RED7 = "0 0 16px rgba(231,50,60,0.80), 0 0 46px rgba(189,34,54,0.55), 0 2px 10px rgba(0,0,0,0.5)"
M8_gw, _, _ = m_word("Golden Boy", M8_WHIP + 3, M8_WALL, 960, 541, wt=800, size=110, color=M8_RED,
                     align="center", shadow=RED7)
M8_fly = [(-480, 0.48, 26), (-420, 0.52, 24), (-330, 0.62, 21), (-240, 0.72, 18), (-160, 0.80, 15), (-100, 0.87, 12),
          (-58, 0.92, 9), (-30, 0.95, 7), (-14, 0.975, 5), (-6, 0.99, 3), (-2, 1.0, 2), (0, 1.0, 1), (0, 1.0, 0)]
for k, (dx, sc, px) in enumerate(M8_fly):                  # f49-61: a gold blur from the left, resolving in the centre
    s.J(f'tl.set("#{M8_gw}", {{ x: {dx}, scale: {sc}, filter: "blur({px}px)" }}, {s.at(FR7(M8_WHIP + 3 + k))});')
M8_NEG = M8_WHIP + 3 + len(M8_fly)                         # f62: black; f63-65 the top difference box; f66-67 black
m_solid(M8_NEG, M8_NEG + 1, "#000000")
for k, op in enumerate((0.55, 1.0, 0.55)):
    m_box(M8_NEG + 1 + k, M8_NEG + 2 + k, (624, 0, 671, 581), f"rgba(228,228,228,{op})", blend="difference",
          z=s.nz() + 950)
m_solid(M8_NEG + 4, M8_NEG + 6, "#000000")
m_img("h10_xray.jpg", M8_WALL - 4, M8_WALL - 2, z=s.nz() + 40)  # f82-83: the X-ray (v10: the user's "jamie skeleton
#   2.0", the cell picture itself with the skeleton drawn in, so it sits exactly over him)
m_img("h8_sil.jpg", M8_WALL - 2, M8_WALL, z=s.nz() + 40)        # f84-85: the silhouette

# ---- 3. of Wall Street: the reel's Hollywood picture (f154-179) on the user's Wall St sign, then their street photo
M8_GUY = W7["the2"]
M8_wall_cam, _ = m_img("h8_wall.jpg", M8_WALL, M8_GUY)
m_box(M8_WALL, M8_WALL + 2, FULL, "#E8E8E8", blend="difference")   # it enters as a negative (f86-87)
M8_WS_Y, WS_W, WS_S, OF_S = 742, 600, 104, 62             # v10: the reel's weight and place, under the sign
M8_of_w = textw("of", "Inter Tight", WS_W, OF_S, track=-0.03)
M8_wall_w = textw("Wall", "Inter Tight", WS_W, WS_S, track=-0.03)
M8_st_w = textw("Street", "Inter Tight", WS_W, WS_S, track=-0.03)
M8_tot = M8_of_w + OF_S * 0.34 + M8_wall_w + WS_S * 0.22 + M8_st_w
M8_xl = 960 - M8_tot / 2
M8_wall_l = M8_xl + M8_of_w + OF_S * 0.34
M8_st_l = M8_wall_l + M8_wall_w + WS_S * 0.22
M8_FOCUS = W7["street"] + 8                                # black, the focus window 6 frames, black, clean, click
m_bar(M8_WALL + 4, W7["wall"], M8_wall_l - 7, M8_WS_Y, M8_wall_w + WS_S * 0.22 + M8_st_w + 14, WS_S * 0.80)
m_bar(W7["wall"], W7["street"], M8_st_l - 7, M8_WS_Y, M8_st_w + 14, WS_S * 0.80)
M8_CLEAN = M8_FOCUS + 8
for (txt, xl, a_, sz) in (("of", M8_xl, W7["of"], OF_S), ("Wall", M8_wall_l, W7["wall"], WS_S),
                          ("Street", M8_st_l, W7["street"], WS_S)):
    yy = M8_WS_Y + (WS_S - sz) * 0.18
    m_word(txt, a_, M8_FOCUS, xl, yy, size=sz, wt=WS_W, shadow=REEL7)
    m_word(txt, M8_FOCUS + 1, M8_FOCUS + 7, xl, yy, size=sz, wt=WS_W, color="#0B0B0B", shadow="none")   # black in the window
    m_word(txt, M8_CLEAN, M8_GUY - 2, xl, yy, size=sz, wt=WS_W, shadow=REEL7)
m_bar(M8_GUY - 2, M8_GUY, M8_xl - 7, M8_WS_Y, M8_tot + 14, WS_S * 0.80)   # the words leave as one bar
m_solid(M8_FOCUS, M8_FOCUS + 1, "#000000")                 # f165
m_img("h8_wall_focus.jpg", M8_FOCUS + 1, M8_FOCUS + 2, istyle="filter:brightness(0.62)", z=s.nz() + 40)   # f166 dim
m_img("h8_wall_focus.jpg", M8_FOCUS + 2, M8_FOCUS + 6, z=s.nz() + 40)                                     # f167-170
m_img("h8_wall_focus2.jpg", M8_FOCUS + 6, M8_FOCUS + 7, istyle="filter:brightness(0.62)", z=s.nz() + 40)  # f171
m_solid(M8_FOCUS + 7, M8_FOCUS + 8, "#000000")             # f172
M8_w2_cam, _ = m_img("h8_wall2.jpg", M8_CLEAN, M8_GUY, z=s.nz() + 40)   # f173-: the clean picture, the street
s.J(f'tl.fromTo("#{M8_w2_cam}", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {r3((M8_GUY - M8_CLEAN) / 60)}, '
    f'ease: "power1.inOut", immediateRender: false }}, {s.at(FR7(M8_CLEAN))});')   # v9: a slow push, no click

# ---- 4. the guy: the reel's second photo run (f86-153), short: three of the user's new front portraits, the same
#      face on the same line, equal holds; the words right of the face, "guy" in serif italic under "the"
M8_MONT = W7["every"] + 1                                  # the user's montage starts on "everyone"
GUY10 = ["h9_a19.jpg", "h9_a16.jpg", "h9_a20.jpg"]
G10 = (M8_MONT - M8_GUY) // len(GUY10)
M8_gcut = [M8_GUY + k * G10 for k in range(len(GUY10))] + [M8_MONT]
for k, pic in enumerate(GUY10):
    m_img(pic, M8_gcut[k], M8_gcut[k + 1])
m_box(M8_GUY, M8_GUY + 2, FULL, "#E4E4E4", blend="difference")     # the run enters as a negative (f86-87)
G_X, G_Y1, G_Y2 = 1392, 405, 506                           # right of the face (the reel's "was the / guy")
h_word("the", M8_GUY + 2, M8_MONT, G_X, G_Y1, out=2)
h_word("guy", W7["guy"] + 1, M8_MONT, G_X + 64, G_Y2, size=150, fam="Instrument Serif", wt=400, italic=True, out=2)

# ---- 5. everyone said was next in line to run: the user's Wall Street montage ("wall street videos montge edits",
#      from its 3rd second, as they asked): the green ticker, the price board, NYSE, the man waiting in the dark. It
#      plays as it is; the reveal at its 4.83 s lands on "the biggest". Words the reel's way: three spread along one
#      row (its "Couldn't ... figure ... out"), then a line under the figure (its "Hollywood")
M8_REV = M8_MONT + 105                                     # source 3.0-4.75 s
m_vid("WSMONT", 3.0, M8_MONT, M8_REV)
S_Y = 383
h_word("everyone", M8_MONT, W7["next"], 194, S_Y, out=2)
h_word("said", W7["said"], W7["next"], 845, S_Y, out=2)
h_word("was", W7["was"], W7["next"], 1594, S_Y, out=2)
U_Y = 772
L1, _, _ = h_line([("next", 88, 600, -0.03), ("in", 88, 600, -0.03), ("line", 88, 600, -0.03)])
for (txt, a_), xl in zip((("next", W7["next"]), ("in", W7["in1"]), ("line", W7["line"])), L1):
    h_word(txt, a_, W7["to"], xl, U_Y, out=2)
L2, _, _ = h_line([("to", 88, 600, -0.03), ("run", 88, 600, -0.03)])
for (txt, a_), xl in zip((("to", W7["to"]), ("run", W7["run"])), L2):
    h_word(txt, a_, M8_REV, xl, U_Y, out=2, bar=2 if txt == "run" else 0)

# ---- 6. the biggest financial company: the user's picture of Dimon at the desk ("montage jamie", made to stand in
#      for the montage's shot at 4.9 s), arriving the montage's way: the shot as a gold line drawing, small in its
#      rounded frame; the picture, on a slow push; a defocus on "company" and black-and-white. The words flank him
#      (the reel's name places)
M8_GB = W7["in2"] - 5                                      # black, grey boxes x6, black (the reel's f295-302)
m_img("h10_desk_line.jpg", M8_REV, M8_REV + 4)
M8_DK0, M8_DK1 = M8_REV + 4, M8_GB - 1
for pic, fa, fb in (("h10_desk.jpg", M8_DK0, W7["comp"]), ("h10_desk_blur.jpg", W7["comp"], W7["comp"] + 2),
                    ("h10_desk_bw.jpg", W7["comp"] + 2, M8_DK1)):
    cam, _ = m_img(pic, fa, fb)
    sc = lambda f: round(1.0 + 0.05 * (f - M8_DK0) / (M8_DK1 - M8_DK0), 4)
    s.J(f'tl.fromTo("#{cam}", {{ scale: {sc(fa)} }}, {{ scale: {sc(fb)}, duration: {r3((fb - fa) / 60)}, ease: "none", '
        f'immediateRender: false }}, {s.at(FR7(fa))});')
F_XL, F_XR, F_Y1, F_Y2 = 512, 1408, 497, 589
h_word("the", W7["the3"], M8_DK1, F_XL, F_Y1, size=84, align="right", out=2)
h_word("biggest", W7["biggest"], M8_DK1, F_XL, F_Y2, size=84, align="right", out=2)
h_word("financial", W7["fin"], M8_DK1, F_XR, F_Y1, size=84, out=2)
h_word("company", W7["comp"], M8_DK1, F_XR, F_Y2, size=84, out=2)
m_solid(M8_GB - 1, M8_GB, "#000000")
for k, (box, col) in enumerate((((760, 300, 780, 440), "#575757"), ((900, 330, 780, 440), "#C8C8C8"),
                                ((900, 330, 780, 440), "#C8C8C8"), ((300, 320, 780, 440), "#C8C8C8"),
                                ((300, 320, 780, 440), "#C8C8C8"), ((620, 310, 780, 440), "#575757"))):
    m_box(M8_GB + k, M8_GB + k + 1, box, col)
m_solid(M8_GB + 6, M8_GB + 7, "#000000")

# ---- 7. in the world: the user's map of America as the reel's map pan (its f310-376): moving east, pulling back,
#      blurred while it is fast; the line centred, its words from bars, the last in bold caps with a place label over
#      it (the reel's "who landed in AMERICA" under "LOS ANGELES"); the line turns into one bar, then the strobe
M8_MAP, M8_STROBE = M8_GB + 7, E7 - 6
M8_mp = [m_img("h10_map.jpg", M8_MAP, M8_STROBE)[0], m_img("h10_map_blur.jpg", M8_MAP, M8_MAP + 22)[0]]
for cam in M8_mp:
    s.J(f'tl.fromTo("#{cam}", {{ scale: 1.62, x: 560, y: -36 }}, {{ scale: 1.34, x: -318, y: -8, '
        f'duration: {r3((M8_STROBE - M8_MAP) / 60)}, ease: "power2.out", immediateRender: false }}, {s.at(FR7(M8_MAP))});')
s.J(f'tl.fromTo("#{M8_mp[1]}", {{ opacity: 1 }}, {{ opacity: 0, duration: {r3(14 / 60)}, ease: "power1.in", '
    f'immediateRender: false }}, {s.at(FR7(M8_MAP + 8))});')
s.black(FR7(M8_MAP), FR7(M8_STROBE), color="rgba(0,0,0,0.36)", tex=False, z=s.nz() + 60)   # the reel's map is dim
s.raw(f'<div id="{s.uid("scr")}" class="clip solid" {s.timed(FR7(M8_MAP), FR7(M8_STROBE))} data-track-index="5" data-layout-ignore '
      f'style="left:180px;top:300px;width:1560px;height:480px;background:radial-gradient(ellipse at center, '
      f'rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.38) 38%, rgba(0,0,0,0) 72%);z-index:{s.nz() + 300}"></div>')   # a shade under the line
W_S, W_T = 104, 0.015
L3, M8_lx, M8_lw = h_line([("in", 88, 600, -0.03), ("the", 88, 600, -0.03), ("WORLD", W_S, 800, W_T)])
h_word("in", M8_MAP + 1, M8_STROBE - 2, L3[0], 540, bar=0)
h_word("the", W7["the4"], M8_STROBE - 2, L3[1], 540)
M8_ww = textw("WORLD", "Inter Tight", 800, W_S, track=W_T)
h_word("WORLD", W7["world"], M8_STROBE - 2, L3[2], 536, size=W_S, wt=800, track=W_T, bar=3)
m_word("NEW YORK", W7["world"], M8_STROBE - 2, L3[2] + M8_ww / 2, 444, wt=600, size=27, align="center", shadow=SANS7,
       track=0.34, opacity=0.92)
m_word("40.71° N   74.00° W", W7["world"], M8_STROBE - 2, L3[2] + M8_ww / 2, 475, wt=600, size=17, align="center",
       shadow=SANS7, track=0.16, opacity=0.8)
m_bar(M8_STROBE - 2, M8_STROBE, M8_lx - 8, 540, M8_lw + 16, 88 * 0.80)     # the whole line becomes one white bar
for k, col in enumerate(("#FFFFFF", "#FFFFFF", "#000000", "#000000", "#FFFFFF", "#FFFFFF")):   # f425-433, W W B B W W
    m_solid(M8_STROBE + k, M8_STROBE + k + 1, col)

# ================================================================================================
# v8 (user, 10 Nov): from "He built Citigroup" to the end, the editing of the Alex Karp reel (instagram Dfc3GMjxrP5,
# notes/v8/karp.md): video first, cut on the phrase, the clip showing what the words say (the documentaries' own
# footage, found through their transcripts); black beats with a few small words; video and photo cards with white
# edges; the pinboard (its 14-19 s); a posterize flash; black-and-white archive for history. The typography stays the
# film's: centred, small Helvetica over the big Instrument Serif glow ("now runs the / biggest bank"). Dimon's video
# over photos wherever there is one (user).
# ================================================================================================
EDGE = "outline:9px solid #F6F3EC;outline-offset:-9px"     # a card's white edge, drawn only while its clip plays


def kc(sc, shots, end, grade="doc", push=(1.0, 1.035)):
    """Straight cuts: shots = [(t0, key, src_t, xyz)], each until the next t0 (or end); returns the cams."""
    cams = []
    for k, (t0, key, st, xyz) in enumerate(shots):
        t1 = shots[k + 1][0] if k + 1 < len(shots) else end
        cam, _ = sc.v(key, st, t0, t1, grade=grade, push=push, xyz=xyz)
        cams.append(cam)
    return cams


def kblack(sc, t0, t1):
    """The Karp reel's black beat: a few small words on black (23.5-24.0 s, 29.5-30.0 s)."""
    sc.black(t0, t1, color="#030303", tex=False, z=sc.nz() + 400)


def kflash(sc, cam, t, n=4):
    """The Karp reel's posterize flash (frames 354-358): the picture blown out to a threshold for 4 frames."""
    looks = ["contrast(2.4) saturate(2.4) brightness(1.35)", "contrast(4.5) saturate(3.2) brightness(1.9)",
             "contrast(6) saturate(2) brightness(2.4) grayscale(0.25)", "contrast(3) brightness(1.5)"]
    for k in range(n):
        sc.J(f'tl.set("#{cam}", {{ filter: "{looks[k % 4]}" }}, {sc.at(round(t + k * F1, 3))});')
    sc.J(f'tl.set("#{cam}", {{ filter: "none" }}, {sc.at(round(t + n * F1, 3))});')


def kvcard(sc, key, st, t0, t1, box, rot=0.0, slide=None, grade="doc", xyz=None):
    """A video card with a white edge, slightly turned; slide=(dx, dy) brings it in on an expo ease."""
    cam, _ = sc.v(key, st, t0, t1, grade=grade, push=None, box=box, xyz=xyz, z=sc.nz() + 200, vstyle=EDGE)
    sc.J(f'tl.set("#{cam}", {{ rotation: {rot} }}, {sc.at(t0)});')
    if slide:
        sc.J(f'tl.fromTo("#{cam}", {{ x: {slide[0]}, y: {slide[1]} }}, {{ x: 0, y: 0, duration: 0.34, ease: "expo.out", '
             f'immediateRender: false }}, {sc.at(t0)});')
    return cam


def kpcard(sc, src, t0, t1, box, rot=0.0, slide=None):
    """A photo card with a white edge (the Karp reel's Habermas and Thiel cards), part of a montage over video."""
    cam, _ = sc.img(src, t0, t1, grade="", push=None, box=box, z=sc.nz() + 220, istyle=EDGE)
    sc.J(f'tl.set("#{cam}", {{ rotation: {rot} }}, {sc.at(t0)});')
    if slide:
        sc.J(f'tl.fromTo("#{cam}", {{ x: {slide[0]}, y: {slide[1]} }}, {{ x: 0, y: 0, duration: 0.3, ease: "expo.out", '
             f'immediateRender: false }}, {sc.at(t0)});')
    sc.J(f'tl.fromTo("#{cam}", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {r3(t1 - t0)}, ease: "none", immediateRender: false }}, '
         f'{sc.at(t0)});')
    return cam


def kdiff(sc, t, frames=1, box=(0, 0, 1920, 1080), color="#E6E6E6"):
    """A difference flash (the Heath reel's negative), a frame or two on a cut."""
    blk(sc, t, frames, box, color, blend="difference", z=sc.nz() + 700)


def kpinboard(sc, t0, t1, cards, moves, fill_from=0, push_last=None):
    """The Karp reel's pinboard (14.75-19.5 s): video cards with white edges and red pins on a pale board; the camera
    starts on the first card filling the frame (the full-frame shot shrinking into it), then whips from card to card.
    cards: [(key, src_t, cx, cy, w, h, rot)] in board pixels; moves: [(t, card index)]; push_last=(t, k): the camera
    pushes into card k until it fills the frame."""
    bid = sc.uid("board")
    BW, BH = 6000, 3600
    inner = [f'<img src="assets/tex/ht_paper.jpg" alt="" style="position:absolute;left:0;top:0;width:{BW}px;height:{BH}px;'
             f'object-fit:cover;opacity:0.5;mix-blend-mode:multiply" />']
    for k, (key, st, cx, cy, w, h, rot) in enumerate(cards):
        cid = CL(key, st, t1 - t0)
        inner.append(
            f'<div style="position:absolute;left:{cx - w / 2 - 14:.0f}px;top:{cy - h / 2 - 14:.0f}px;width:{w + 28}px;'
            f'height:{h + 28}px;background:#F7F5F0;box-shadow:0 22px 46px rgba(0,0,0,0.30), 0 3px 9px rgba(0,0,0,0.18);'
            f'rotate:{rot}deg"><video id="{bid}-v{k}" class="clip" src="assets/clips2/{cid}.mp4" muted playsinline '
            f'{sc.timed(t0, t1)} data-hf-media-start-basis="local" data-media-start="0"{gattr("doc")} data-track-index="2" '
            f'style="position:absolute;left:14px;top:14px;width:{w}px;height:{h}px;object-fit:cover"></video>'
            f'<div style="position:absolute;left:{w / 2 + 14 - 17:.0f}px;top:-16px;width:34px;height:34px;border-radius:50%;'
            f'background:radial-gradient(circle at 34% 32%, #ff8a8a 0%, #e02222 42%, #7c0909 100%);'
            f'box-shadow:3px 6px 7px rgba(0,0,0,0.38)"></div></div>')
    sc.raw(f'<div id="{bid}" class="grp" data-layout-allow-overflow data-layout-ignore style="width:{BW}px;height:{BH}px;'
           f'background:radial-gradient(ellipse at 50% 45%, #EEF3F4 0%, #DCE4E7 60%, #C3CDD1 100%);'
           f'transform-origin:0 0;z-index:{sc.nz()}">{"".join(inner)}</div>')

    def at(k, scale=1.0, y=440):
        _, _, cx, cy, w, h, _ = cards[k]
        return round(960 - cx * scale, 1), round(y - cy * scale, 1)
    _, _, _, _, w0, h0, _ = cards[fill_from]
    sf = round(1920 / (w0 + 28) * 1.02, 4)
    x0, y0 = at(fill_from, sf, 540)
    x1, y1 = at(fill_from)
    # v9 (user: too fast, "make it in low frame rate"): every move takes 0.6 s and steps at 12 positions a second
    step = lambda d, kind: (f'(p) => {{ const q = Math.round(p * {max(2, round(d * 12))}) / {max(2, round(d * 12))}; '
                            + ('return 1 - Math.pow(1 - q, 3); }' if kind == "out" else
                               'return q < 0.5 ? 4 * q * q * q : 1 - Math.pow(-2 * q + 2, 3) / 2; }'))
    js = [f'tl.set("#{bid}", {{ x: {x0}, y: {y0}, scale: {sf} }}, {sc.at(t0)});',
          f'tl.to("#{bid}", {{ x: {x1}, y: {y1}, scale: 1, duration: 0.5, ease: {step(0.5, "out")} }}, {sc.at(t0)});']
    for t, k in moves:
        x, y = at(k)
        js.append(f'tl.to("#{bid}", {{ x: {x}, y: {y}, scale: 1, duration: 0.6, ease: {step(0.6, "inout")} }}, {sc.at(t)});')
    if push_last:
        t, k = push_last
        _, _, _, _, w, h, _ = cards[k]
        sp = round(1920 / (w + 28) * 1.04, 4)
        x, y = at(k, sp, 540)
        js.append(f'tl.to("#{bid}", {{ x: {x}, y: {y}, scale: {sp}, duration: 0.36, ease: {step(0.36, "inout")} }}, '
                  f'{sc.at(t)});')
    sc.J("\n    ".join(js))
    return bid


def kpanels(sc, t0, t1, key, st, n=6, step=5):
    """The user's 'cut cut' reference (Edit style cut cut photos, 7.30-8.67 s; notes/v8/cutcut_panels.md): the next shot
    opens one glass pane at a time, left to right, a pane every few frames, each pane its own slightly offset crop,
    dark mullions between them; then it holds full frame."""
    pw = 1920 / n
    for k in range(n):
        a = round(t0 + k * step * F1, 3)
        x0 = round(k * pw)
        w = round((k + 1) * pw) - x0
        off = (-1) ** k * 1.6
        cam, _ = sc.v(key, round(st + (a - t0), 3), a, t1, grade="doc", push=None, box=(x0, 0, w, 1080),
                      z=sc.nz() + 120, vstyle=f"object-position:{x0 / (1920 - w) * 100 + off:.2f}% 50%")
        sc.J(f'tl.set("#{cam}", {{ scale: {1.0 + 0.03 * (k % 2)} }}, {sc.at(a)});')
        if k:
            sc.raw(f'<div id="{sc.uid("mul")}" class="clip solid" {sc.timed(a, t1)} data-track-index="6" data-layout-ignore '
                   f'style="left:{x0 - 4}px;width:8px;background:#0d1114;z-index:{sc.nz() + 140}"></div>')
    return round(t0 + n * step * F1, 3)


BEZ_LAUGH = ST("bezos_laugh", path=f"{P_IMG}/10_Supporting_Illustrative/03_ILLUSTRATIVE_Jeff_Bezos_laugh_portrait.jpg",
               edge=1400)
BEZ_AMZ = ST("bezos_amz", path=f"{P_IMG}/10_Supporting_Illustrative/04_ILLUSTRATIVE_Jeff_Bezos_Amazon_Seattle_2016.jpg",
             edge=1400)
UNT_ZOOM = 1.26          # the Untold film's inner white frame and its age label, cropped away

def kboard10(sc, t0, t1, Z, cards, T1, W2, stack, lower):
    """v10 (user: "see this video exactly from the 15th second: how smoothly it pans ... the typography ... how they are
    playing videos in it, not just still photos ... they have softened the edges of the videos"). The Karp reel's
    pinboard, frame by frame at 24 fps:
    - 14.75 the full-frame clip blows out (2 frames), 14.83 a posterize-white frame (2), 14.91 the clip is a card, 69 %
      of the frame wide, still blown out (2), 15.00 the card as it is; it slides a little;
    - 15.15 the camera whips right: the next card's left edge is at 0.82 of the width at 15.33, 0.60 at 15.50, 0.45 at
      15.66, 0.36 at 15.83, 0.29 at 16.00, 0.23 at 16.25, 0.21 from 16.41, i.e. the distance left halves every 0.2 s
      (expo out over about 1.9 s), blurred while fast. The card: 61 % of the width, turned 3.5 degrees, a white edge,
      a red pushpin right of its top centre; five bold black words stacked at its right;
    - 17.00 the camera whips down and left and pushes in: the third card rises from the bottom left and ends 77 % of
      the frame wide, turned the other way; small bold white words build on the card;
    - 19.25 one negative frame, then black.
    cards: [(key, src_t, cx, cy, w, h, rot, pin)] in board px (pin: its place along the top edge, or None), the first
    being the full-frame clip's own continuation; Z: the posterize frame; T1, W2: the whips; stack: dict(x, y, pitch,
    size, lines=[[(word, t), ...]]) on the board; lower: dict(card, size, y, phrases=[([(word, t), ...], end)])."""
    bid = sc.uid("board")
    BW, BH, EDGE_C, SKY = 6400, 4000, "#F6F1F0", "#9FD4FC"
    inner = [f'<div id="{bid}-g" style="position:absolute;left:0;top:0;width:{BW}px;height:{BH}px;background:{SKY};'
             f'opacity:0"></div>']
    for k, (key, st, cx, cy, w, h, rot, pin) in enumerate(cards):
        cid = CL(key, st, t1 - t0)
        extra = ""
        if pin is not None:
            extra += (f'<div style="position:absolute;left:{(w + 28) * pin - 26:.0f}px;top:-28px;width:52px;height:52px;'
                      f'border-radius:50%;background:radial-gradient(circle at 34% 30%, #ff9c9c 0%, #e32626 40%, #7a0808 100%);'
                      f'box-shadow:4px 9px 9px rgba(10,30,60,0.42)"></div>')
        if lower and lower["card"] == k:
            sz = lower["size"]
            for j, (words, end) in enumerate(lower["phrases"]):
                ws = [textw(wd, "Inter Tight", 700, sz, track=-0.03) for wd, _ in words]
                acc = (w + 28) / 2 - (sum(ws) + sz * 0.26 * (len(ws) - 1)) / 2
                for i, ((wd, tw_), ww) in enumerate(zip(words, ws)):
                    extra += (f'<div id="{bid}-l{j}{i}" class="clip" {sc.timed(tw_, end)} data-track-index="5" data-layout-ignore '
                              f'style="position:absolute;left:{acc:.0f}px;top:{14 + h * lower["y"] - sz * 0.5:.0f}px;'
                              f'font-family:\'Inter Tight\';font-weight:700;font-size:{sz}px;line-height:1;'
                              f'letter-spacing:-0.03em;color:#FFFFFF;white-space:nowrap;'
                              f'text-shadow:0 2px 12px rgba(0,0,0,0.65), 0 0 3px rgba(0,0,0,0.5)">{esc(wd)}</div>')
                    acc += ww + sz * 0.26
        inner.append(
            f'<div id="{bid}-c{k}" style="position:absolute;left:{cx - w / 2 - 14:.0f}px;top:{cy - h / 2 - 14:.0f}px;'
            f'width:{w + 28}px;height:{h + 28}px;background:{EDGE_C};'
            f'box-shadow:0 26px 54px rgba(20,50,90,0.36), 0 3px 10px rgba(20,50,90,0.24);rotate:{rot}deg">'
            f'<video id="{bid}-v{k}" class="clip" src="assets/clips2/{cid}.mp4" muted playsinline {sc.timed(t0, t1)} '
            f'data-hf-media-start-basis="local" data-media-start="0"{gattr("doc")} data-track-index="2" '
            f'style="position:absolute;left:14px;top:14px;width:{w}px;height:{h}px;object-fit:cover"></video>'
            f'<div style="position:absolute;left:14px;top:14px;width:{w}px;height:{h}px;'
            f'box-shadow:inset 0 0 16px 8px {EDGE_C}"></div>{extra}</div>')            # the video's softened edge
    sz = stack["size"]
    for i, line in enumerate(stack["lines"]):
        acc = 0
        for j, (wd, tw_) in enumerate(line):
            inner.append(f'<div id="{bid}-s{i}{j}" class="clip" {sc.timed(tw_, t1)} data-track-index="5" data-layout-ignore '
                         f'style="position:absolute;left:{stack["x"] + acc:.0f}px;top:{stack["y"] + i * stack["pitch"]:.0f}px;'
                         f'font-family:\'Inter Tight\';font-weight:700;font-size:{sz}px;line-height:1;letter-spacing:-0.03em;'
                         f'color:#12161B;white-space:nowrap">{esc(wd)}</div>')
            acc += textw(wd, "Inter Tight", 700, sz, track=-0.03) + sz * 0.24
    zb = sc.nz()
    sc.raw(f'<div id="{bid}" class="grp" data-layout-allow-overflow data-layout-ignore style="width:{BW}px;height:{BH}px;'
           f'background-color:{SKY};background-image:linear-gradient(rgba(104,176,238,0.55) 2px, transparent 2px), '
           f'linear-gradient(90deg, rgba(104,176,238,0.55) 2px, transparent 2px);background-size:34px 34px;'
           f'transform-origin:0 0;z-index:{zb}">{"".join(inner)}</div>')
    sc.raw(f'<div id="{sc.uid("vg")}" class="clip solid" {sc.timed(t0, t1)} data-track-index="4" data-layout-ignore '
           f'style="background:radial-gradient(ellipse at 50% 47%, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 46%, '
           f'rgba(24,74,134,0.24) 100%);z-index:{zb + 1}"></div>')                      # the reel's board vignette

    D = 1.9
    pos = lambda k, sx, sy, s_=1.0: (round(sx - cards[k][2] * s_, 1), round(sy - cards[k][3] * s_, 1))
    P1 = pos(0, 830, 520)
    P1b = (P1[0] - 70, P1[1])                              # it slides a little before the whip
    P2 = pos(1, 900, 560)
    S3 = 1.30
    P3 = pos(2, 912, 621, S3)
    r1 = (W2 - T1) / D
    k1 = 1 - 2 ** (-10 * r1)                               # how far the first whip has got when the second starts
    Pw = (round(P1b[0] + (P2[0] - P1b[0]) * k1, 1), round(P1b[1] + (P2[1] - P1b[1]) * k1, 1))
    te = round(t1 - 4 / 60, 3)
    js = [f'tl.set("#{bid}", {{ x: {P1[0]}, y: {P1[1]}, scale: 1 }}, {sc.at(t0)});',
          f'tl.fromTo("#{bid}", {{ x: {P1[0]} }}, {{ x: {P1b[0]}, duration: {r3(T1 - Z - 2 / 24)}, ease: "none", '
          f'immediateRender: false }}, {sc.at(round(Z + 2 / 24, 3))});',
          f'tl.fromTo("#{bid}", {{ x: {P1b[0]}, y: {P1b[1]} }}, {{ x: {Pw[0]}, y: {Pw[1]}, duration: {r3(W2 - T1)}, '
          f'ease: (q) => (1 - Math.pow(2, -10 * q * {r1:.4f})) / {k1:.6f}, immediateRender: false }}, {sc.at(T1)});',
          f'tl.fromTo("#{bid}", {{ x: {Pw[0]}, y: {Pw[1]}, scale: 1 }}, {{ x: {P3[0]}, y: {P3[1]}, scale: {S3}, '
          f'duration: {D}, ease: "expo.out", immediateRender: false }}, {sc.at(W2)});']
    if te > W2 + D:                                        # the slow push on the last card
        S4 = round(S3 + 0.035, 3)
        P4 = pos(2, 912, 621, S4)
        js.append(f'tl.fromTo("#{bid}", {{ x: {P3[0]}, y: {P3[1]}, scale: {S3} }}, {{ x: {P4[0]}, y: {P4[1]}, scale: {S4}, '
                  f'duration: {r3(te - W2 - D)}, ease: "none", immediateRender: false }}, {sc.at(round(W2 + D, 3))});')
    for tw_ in (T1, W2):                                   # the whips: the cards blur, the grid's lines smear out
        for k in range(len(cards)):
            js.append(f'tl.fromTo("#{bid}-c{k}", {{ filter: "blur(13px)" }}, {{ filter: "blur(0px)", duration: 0.42, '
                      f'ease: "power2.out", immediateRender: false }}, {sc.at(tw_)});')
        js.append(f'tl.fromTo("#{bid}-g", {{ opacity: 0.88 }}, {{ opacity: 0, duration: 0.62, ease: "power2.out", '
                  f'immediateRender: false }}, {sc.at(tw_)});')
    js.append(f'tl.set("#{bid}-c0", {{ filter: "saturate(1.9) brightness(1.55) contrast(1.35)" }}, {sc.at(t0)});')
    js.append(f'tl.set("#{bid}-c0", {{ filter: "none" }}, {sc.at(round(Z + 4 / 24, 3))});')   # the card, blown out 2 frames
    sc.J("\n    ".join(js))
    sc.raw(f'<div id="{sc.uid("neg")}" class="clip solid" {sc.timed(te, round(t1 - 2 / 60, 3))} data-track-index="6" '
           f'data-layout-ignore style="background:#FFFFFF;mix-blend-mode:difference;z-index:{zb + 600}"></div>')   # negative
    sc.raw(f'<div id="{sc.uid("blk")}" class="clip solid" {sc.timed(round(t1 - 2 / 60, 3), t1)} data-track-index="6" '
           f'data-layout-ignore style="background:#030303;z-index:{zb + 601}"></div>')
    return bid


def kboard11(sc, t0, t1, Z, cards, T1, W2, stack, lower):
    """v10 (user: "see this video exactly from the 15th second: how smoothly it pans ... the typography ... how they are
    playing videos in it, not just still photos ... they have softened the edges of the videos"). The Karp reel's
    pinboard, frame by frame at 24 fps:
    - 14.75 the full-frame clip blows out (2 frames), 14.83 a posterize-white frame (2), 14.91 the clip is a card, 69 %
      of the frame wide, still blown out (2), 15.00 the card as it is; it slides a little;
    - 15.15 the camera whips right: the next card's left edge is at 0.82 of the width at 15.33, 0.60 at 15.50, 0.45 at
      15.66, 0.36 at 15.83, 0.29 at 16.00, 0.23 at 16.25, 0.21 from 16.41, i.e. the distance left halves every 0.2 s
      (expo out over about 1.9 s), blurred while fast. The card: 61 % of the width, turned 3.5 degrees, a white edge,
      a red pushpin right of its top centre; five bold black words stacked at its right;
    - 17.00 the camera whips down and left and pushes in: the third card rises from the bottom left and ends 77 % of
      the frame wide, turned the other way; small bold white words build on the card;
    - 19.25 one negative frame, then black.
    cards: [(key, src_t, cx, cy, w, h, rot, pin)] in board px (pin: its place along the top edge, or None), the first
    being the full-frame clip's own continuation; Z: the posterize frame;
    v11: each card is [(key, src_t, from), ...] cut on the words, a white flash on every cut inside a card and on each
    whip, a glow blooming behind each card as it lands, the words on the last card in the serif glow; T1, W2: the whips; stack: dict(x, y, pitch,
    size, lines=[[(word, t), ...]]) on the board; lower: dict(card, size, y, phrases=[([(word, t), ...], end)])."""
    bid = sc.uid("board")
    BW, BH, EDGE_C, SKY = 6400, 4000, "#F6F1F0", "#9FD4FC"
    inner = [f'<div id="{bid}-g" style="position:absolute;left:0;top:0;width:{BW}px;height:{BH}px;background:{SKY};'
             f'opacity:0"></div>']
    fj = []
    for k, (clips, cx, cy, w, h, rot, pin) in enumerate(cards):
        vids = ""
        for j, (key, st, ca) in enumerate(clips):
            cb = clips[j + 1][2] if j + 1 < len(clips) else t1
            cid = CL(key, st, cb - ca)
            vids += (f'<video id="{bid}-v{k}{j}" class="clip" src="assets/clips2/{cid}.mp4" muted playsinline '
                     f'{sc.timed(ca, cb)} data-hf-media-start-basis="local" data-media-start="0"{gattr("doc")} '
                     f'data-track-index="2" style="position:absolute;left:14px;top:14px;width:{w}px;height:{h}px;'
                     f'object-fit:cover"></video>')
            if j:                                          # the cut inside the card: a white flash over the picture
                vids += (f'<div id="{bid}-f{k}{j}" class="clip" {sc.timed(ca, round(ca + 0.15, 3))} data-track-index="3" '
                         f'style="position:absolute;left:14px;top:14px;width:{w}px;height:{h}px;background:#FFFFFF"></div>')
                fj.append(f'tl.fromTo("#{bid}-f{k}{j}", {{ opacity: 0.95 }}, {{ opacity: 0, duration: 0.15, ease: "power2.out", '
                          f'immediateRender: false }}, {sc.at(ca)});')
        if k:                                              # the glow that blooms behind the card as it lands
            inner.append(f'<div id="{bid}-h{k}" style="position:absolute;left:{cx - w / 2 - 110:.0f}px;'
                         f'top:{cy - h / 2 - 110:.0f}px;width:{w + 220}px;height:{h + 220}px;rotate:{rot}deg;opacity:0;'
                         f'background:radial-gradient(ellipse at center, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.7) 46%, '
                         f'rgba(255,255,255,0) 72%)"></div>')
        extra = ""
        if pin is not None:
            extra += (f'<div style="position:absolute;left:{(w + 28) * pin - 26:.0f}px;top:-28px;width:52px;height:52px;'
                      f'border-radius:50%;background:radial-gradient(circle at 34% 30%, #ff9c9c 0%, #e32626 40%, #7a0808 100%);'
                      f'box-shadow:4px 9px 9px rgba(10,30,60,0.42)"></div>')
        if lower and lower["card"] == k:
            sz = lower["size"]
            for j, (words, end) in enumerate(lower["phrases"]):
                ws = [textw(wd, "Instrument Serif", 400, sz, track=-0.01) for wd, _ in words]
                acc = (w + 28) / 2 - (sum(ws) + sz * 0.22 * (len(ws) - 1)) / 2
                for i, ((wd, tw_), ww) in enumerate(zip(words, ws)):   # v11: the film's serif glow, blooming in
                    extra += (f'<div id="{bid}-l{j}{i}" class="clip" {sc.timed(tw_, end)} data-track-index="5" data-layout-ignore '
                              f'style="position:absolute;left:{acc:.0f}px;top:{14 + h * lower["y"] - sz * 0.56:.0f}px;'
                              f'font-family:\'Instrument Serif\';font-weight:400;font-size:{sz}px;line-height:1;'
                              f'letter-spacing:-0.01em;color:{INK};white-space:nowrap;'
                              f'text-shadow:{GLOW_REST}">{esc(wd)}</div>')
                    fj.append(f'tl.fromTo("#{bid}-l{j}{i}", {{ opacity: 0, filter: "blur(16px)", textShadow: "{GLOW_BLOOM}" }}, '
                              f'{{ opacity: 1, filter: "blur(0px)", textShadow: "{GLOW_REST}", duration: 0.24, ease: "expo.out", '
                              f'immediateRender: false }}, {sc.at(tw_)});')
                    acc += ww + sz * 0.22
        inner.append(
            f'<div id="{bid}-c{k}" style="position:absolute;left:{cx - w / 2 - 14:.0f}px;top:{cy - h / 2 - 14:.0f}px;'
            f'width:{w + 28}px;height:{h + 28}px;background:{EDGE_C};'
            f'box-shadow:0 26px 54px rgba(20,50,90,0.36), 0 3px 10px rgba(20,50,90,0.24);rotate:{rot}deg">'
            f'{vids}<div style="position:absolute;left:14px;top:14px;width:{w}px;height:{h}px;'
            f'box-shadow:inset 0 0 16px 8px {EDGE_C}"></div>{extra}</div>')            # the video's softened edge
    sz = stack["size"]
    for i, line in enumerate(stack["lines"]):
        acc = 0
        for j, (wd, tw_) in enumerate(line):
            inner.append(f'<div id="{bid}-s{i}{j}" class="clip" {sc.timed(tw_, t1)} data-track-index="5" data-layout-ignore '
                         f'style="position:absolute;left:{stack["x"] + acc:.0f}px;top:{stack["y"] + i * stack["pitch"]:.0f}px;'
                         f'font-family:\'Inter Tight\';font-weight:700;font-size:{sz}px;line-height:1;letter-spacing:-0.03em;'
                         f'color:#12161B;white-space:nowrap">{esc(wd)}</div>')
            acc += textw(wd, "Inter Tight", 700, sz, track=-0.03) + sz * 0.24
    zb = sc.nz()
    sc.raw(f'<div id="{bid}" class="grp" data-layout-allow-overflow data-layout-ignore style="width:{BW}px;height:{BH}px;'
           f'background-color:{SKY};background-image:linear-gradient(rgba(104,176,238,0.55) 2px, transparent 2px), '
           f'linear-gradient(90deg, rgba(104,176,238,0.55) 2px, transparent 2px);background-size:34px 34px;'
           f'transform-origin:0 0;z-index:{zb}">{"".join(inner)}</div>')
    sc.raw(f'<div id="{sc.uid("vg")}" class="clip solid" {sc.timed(t0, t1)} data-track-index="4" data-layout-ignore '
           f'style="background:radial-gradient(ellipse at 50% 47%, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 46%, '
           f'rgba(24,74,134,0.24) 100%);z-index:{zb + 1}"></div>')                      # the reel's board vignette

    D = 1.9
    pos = lambda k, sx, sy, s_=1.0: (round(sx - cards[k][1] * s_, 1), round(sy - cards[k][2] * s_, 1))   # v11: (clips, cx, cy, ...)
    P1 = pos(0, 830, 520)
    P1b = (P1[0] - 70, P1[1])                              # it slides a little before the whip
    P2 = pos(1, 900, 560)
    S3 = 1.30
    P3 = pos(2, 912, 621, S3)
    r1 = (W2 - T1) / D
    k1 = 1 - 2 ** (-10 * r1)                               # how far the first whip has got when the second starts
    Pw = (round(P1b[0] + (P2[0] - P1b[0]) * k1, 1), round(P1b[1] + (P2[1] - P1b[1]) * k1, 1))
    te = round(t1 - 4 / 60, 3)
    js = [f'tl.set("#{bid}", {{ x: {P1[0]}, y: {P1[1]}, scale: 1 }}, {sc.at(t0)});',
          f'tl.fromTo("#{bid}", {{ x: {P1[0]} }}, {{ x: {P1b[0]}, duration: {r3(T1 - Z - 2 / 24)}, ease: "none", '
          f'immediateRender: false }}, {sc.at(round(Z + 2 / 24, 3))});',
          f'tl.fromTo("#{bid}", {{ x: {P1b[0]}, y: {P1b[1]} }}, {{ x: {Pw[0]}, y: {Pw[1]}, duration: {r3(W2 - T1)}, '
          f'ease: (q) => (1 - Math.pow(2, -10 * q * {r1:.4f})) / {k1:.6f}, immediateRender: false }}, {sc.at(T1)});',
          f'tl.fromTo("#{bid}", {{ x: {Pw[0]}, y: {Pw[1]}, scale: 1 }}, {{ x: {P3[0]}, y: {P3[1]}, scale: {S3}, '
          f'duration: {D}, ease: "expo.out", immediateRender: false }}, {sc.at(W2)});']
    if te > W2 + D:                                        # the slow push on the last card
        S4 = round(S3 + 0.035, 3)
        P4 = pos(2, 912, 621, S4)
        js.append(f'tl.fromTo("#{bid}", {{ x: {P3[0]}, y: {P3[1]}, scale: {S3} }}, {{ x: {P4[0]}, y: {P4[1]}, scale: {S4}, '
                  f'duration: {r3(te - W2 - D)}, ease: "none", immediateRender: false }}, {sc.at(round(W2 + D, 3))});')
    for tw_ in (T1, W2):                                   # the whips: the cards blur, the grid's lines smear out
        for k in range(len(cards)):
            js.append(f'tl.fromTo("#{bid}-c{k}", {{ filter: "blur(13px)" }}, {{ filter: "blur(0px)", duration: 0.42, '
                      f'ease: "power2.out", immediateRender: false }}, {sc.at(tw_)});')
        js.append(f'tl.fromTo("#{bid}-g", {{ opacity: 0.88 }}, {{ opacity: 0, duration: 0.62, ease: "power2.out", '
                  f'immediateRender: false }}, {sc.at(tw_)});')
    for k, tl_ in ((1, round(T1 + 0.30, 3)), (2, round(W2 + 0.34, 3))):   # the glows as the cards land
        js.append(f'tl.fromTo("#{bid}-h{k}", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.08, ease: "power2.out", '
                  f'immediateRender: false }}, {sc.at(tl_)});')
        js.append(f'tl.to("#{bid}-h{k}", {{ opacity: 0, duration: 0.55, ease: "power2.in" }}, {sc.at(round(tl_ + 0.08, 3))});')
    js += fj
    js.append(f'tl.set("#{bid}-c0", {{ filter: "saturate(1.9) brightness(1.55) contrast(1.35)" }}, {sc.at(t0)});')
    js.append(f'tl.set("#{bid}-c0", {{ filter: "none" }}, {sc.at(round(Z + 4 / 24, 3))});')   # the card, blown out 2 frames
    sc.J("\n    ".join(js))
    for tw_ in (T1, W2):                                   # v11: a white flash on each whip
        sc.flash(round(tw_ + 0.05, 3), d=0.14, peak=0.62)
    sc.raw(f'<div id="{sc.uid("neg")}" class="clip solid" {sc.timed(te, round(t1 - 2 / 60, 3))} data-track-index="6" '
           f'data-layout-ignore style="background:#FFFFFF;mix-blend-mode:difference;z-index:{zb + 600}"></div>')   # negative
    sc.raw(f'<div id="{sc.uid("blk")}" class="clip solid" {sc.timed(round(t1 - 2 / 60, 3), t1)} data-track-index="6" '
           f'data-layout-ignore style="background:#030303;z-index:{zb + 601}"></div>')
    return bid


# ---- S09  35.74-40.65  "He built Citigroup side-by-side with his mentor Sandy Weill for 16 years."
#      v10 (user): the Karp reel's pinboard exactly (kboard10), on the user's blue grid. Video in every card: the two of
#      them under the citi sign (the full-frame shot that becomes the first card), Dimon speaking at the citi wall,
#      Weill at the lectern (user: "one can be of Sandy Weill ... the rest Jamie Dimon's videos"). The words the reel's
#      way: small white Helvetica on the full-frame shot, bold black words stacked beside the second card, bold white
#      words building on the third.
s = Scene("s09", CUT(VT(81)), CUT(VT(95)), tex=(0.06, 0.0))
B0 = round(CUT(VT(83)) + 0.08, 3)                      # "Citigroup": the posterize frame (late enough to read "built")
B_T1 = round(B0 + 0.40, 3)                             # the whip to Dimon's card
B_W2 = round(CUT(VT(90)) - 0.20, 3)                    # the whip down to Weill's card, in place on "Sandy"
kboard11(s, CUT(VT(81)), CUT(VT(95)), B0,                 # v11: video cut on the words in every card (user)
         [([("MPB", 1001.6, CUT(VT(81)))], 1500, 1100, 1297, 730, 0.0, None),
          ([("MPB", 927.0, CUT(VT(81))), ("MPB", 716.0, CUT(VT(84))), ("MPB", 852.0, CUT(VT(87)))],
           4300, 1180, 1120, 630, 3.5, 0.62),           # Dimon at the citi wall; the two side by side; the press
          ([("MPB", 727.3, CUT(VT(81))), ("MPB", 868.0, CUT(VT(92)))],
           3500, 2900, 1120, 630, -1.2, 0.60)],         # Weill at the lectern; then the two of them, for 16 years
         B_T1, B_W2,
         dict(x=4918, y=1040, pitch=58, size=58,
              lines=[[("Citigroup", B_T1)], [("side", VT(84))], [("by", VT(85)), ("side", VT(86))],
                     [("with", VT(87)), ("his", VT(88))], [("mentor", VT(89))]]),
         dict(card=2, size=72, y=0.66,
              phrases=[([("Sandy", VT(90)), ("Weill", VT(91))], round(VT(92) - 0.02, 3)),
                       ([("for", VT(92)), ("16", VT(93)), ("years", VT(94))], CUT(VT(95)))]))
camA, _ = s.v("MPB", 1001.6, CUT(VT(81)), round(B0 + 2 / 24, 3), grade="doc", push=None, z=s.nz() + 300)
s.J(f'tl.set("#{camA}", {{ filter: "contrast(1.5) saturate(1.9) brightness(1.5)" }}, {s.at(round(B0 - 2 / 24, 3))});')
s.J(f'tl.set("#{camA}", {{ filter: "brightness(3.4) contrast(3.2) saturate(1.5)" }}, {s.at(B0)});')   # the posterize frame: nearly white
s.raw(f'<div id="{s.uid("wh")}" class="clip solid" {s.timed(B0, round(B0 + 2 / 24, 3))} data-track-index="6" data-layout-ignore '
      f'style="background:rgba(255,255,255,0.66);z-index:{s.nz() + 400}"></div>')
cap([[W_(81, "s"), W_(82, "s")]], end=B0, scrim=0.4)

# ---- S10  47.76-50.81  "But then, at 42, he was fired."
s = Scene("s10", CUT(VT(95)), CUT(VT(102)))
sp_bars(s, CUT(VT(95)), CUT(VT(97)), [("But", VT(95)), ("then", VT(96))])
cam, _ = s.v("MPB", 1090.5, CUT(VT(97)), CUT(VT(99)), grade="bw", push=(1.0, 1.05))   # v9 (user): video at "42"
s.neg(CUT(VT(97)), 1)
sp_bars(s, CUT(VT(99)), CUT(VT(101)) + 2 * F1, [("he", VT(99)), ("was", VT(100))], exit_at=CUT(VT(101)) - F1)
s.black(CUT(VT(101)), CUT(VT(102)), color="#030303", tex=False)
s.v("FIRED", 55.0, CUT(VT(101)), CUT(VT(102)), push=(1.0, 1.04), box=(0, 138, 1920, 804),   # v7 (user): the push from
    size=(1920, 804))                                                   # its 55th second, a slow-motion pause
s.flash(VT(101), d=0.24)
s.neg(VT(101) + 2 * F1, 2)
cap([[W_(97, "s")], [W_(98, "sx", "42")]], end=CUT(VT(99)))
cap([[W_(101, "sx", "fired")]], y=560, end=CUT(VT(102)))

# ================================================================================================
# v9 (user, 10 Nov): after "fired" the second half mixes the two references: the Alex Karp reel's video-first cutting
# and black beats with the Heath Ledger reel's later devices (notes/v9/mix.md, read from its 9.6-33 s): clips framed
# on a grey vignette (11.1-13.1, 20.6-21.6), the 3x3 grid with inverted cells (18.6-19.1), the difference box over the
# eyes (11.1), white flash frames (12.1), the white silhouette (24.1), the word behind the cut-out ("HE PITCHED",
# 23.6), the prism streak over a word (22.1-23.1), cards cycling (the villains, 20.6-21.6), and a faster cut
# (Heath 0.27 s a shot, Karp 0.55 s; here about 0.35-0.5 s). Typography as everywhere: centred, small Helvetica
# over the Instrument Serif glow.
# ================================================================================================
VIGNETTE = "radial-gradient(ellipse at 50% 46%, #E9E9E7 0%, #C9C9C6 46%, #7C7C79 100%)"


def hframe(sc, key, st, t0, t1, xyz=None, inset=0.82, grade="doc"):
    """Heath 11.1-13.1 and 20.6-21.6: the clip as a frame on a grey vignette, a soft shadow under it, drifting in."""
    sc.black(t0, t1, color=VIGNETTE, tex=False)
    w, h = round(1920 * inset), round(1080 * inset)
    x, y = (1920 - w) // 2, (1080 - h) // 2
    cam, _ = sc.v(key, st, t0, t1, grade=grade, push=None, box=(x, y, w, h), xyz=xyz, z=sc.nz() + 10,
                  cam_style="filter:drop-shadow(0 26px 36px rgba(0,0,0,0.42))")
    sc.J(f'tl.fromTo("#{cam}", {{ scale: 1.03 }}, {{ scale: 1.0, duration: {r3(t1 - t0)}, ease: "none", '
         f'immediateRender: false }}, {sc.at(t0)});')
    return cam


def hcards(sc, items, t0, t1, inset=0.74):
    """Heath 20.6-21.6 (the villains): clips or photos framed on the vignette, one after another, each tilted a little
    differently. items: [(kind, src..., rot)] with kind 'v' (key, st) or 'i' (still)."""
    sc.black(t0, t1, color=VIGNETTE, tex=False)
    n = len(items)
    w, h = round(1920 * inset), round(1080 * inset)
    x, y = (1920 - w) // 2, (1080 - h) // 2
    for k, it in enumerate(items):
        a = round(t0 + (t1 - t0) * k / n, 3)
        b = round(t0 + (t1 - t0) * (k + 1) / n, 3)
        if it[0] == "v":
            _, key, st, rot = it
            cam, _ = sc.v(key, st, a, b, grade="doc", push=None, box=(x, y, w, h), z=sc.nz() + 10,
                          cam_style="filter:drop-shadow(0 24px 34px rgba(0,0,0,0.42))")
        else:
            _, src, rot = it
            cam, _ = sc.img(src, a, b, grade="", push=None, box=(x, y, w, h), z=sc.nz() + 10,
                            cam_style="filter:drop-shadow(0 24px 34px rgba(0,0,0,0.42))")
        sc.J(f'tl.set("#{cam}", {{ rotation: {rot} }}, {sc.at(a)});')
        sc.J(f'tl.fromTo("#{cam}", {{ scale: 1.03 }}, {{ scale: 1.0, duration: {r3(b - a)}, ease: "none", '
             f'immediateRender: false }}, {sc.at(a)});')


def hgrid(sc, t0, t1, cells, invert=(), lines=True):
    """Heath 18.6-19.1: a 3x3 grid of clips, thin dark lines between them, some cells inverted."""
    for k, (key, st) in enumerate(cells[:9]):
        c, r = k % 3, k // 3
        sc.v(key, st, t0, t1, grade="doc", push=None, box=(640 * c, 360 * r, 640, 360), z=sc.nz() + 10)
    for k in invert:
        c, r = k % 3, k // 3
        blk(sc, t0, max(1, round((t1 - t0) / F1)), (640 * c, 360 * r, 640, 360), "#E6E6E6", blend="difference",
            z=sc.nz() + 600)
    if lines:
        grid = "".join(f'<div style="position:absolute;left:{x}px;top:0;width:3px;height:1080px;background:#0b0b0b"></div>'
                       for x in (639, 1279)) + "".join(
                       f'<div style="position:absolute;left:0;top:{y}px;width:1920px;height:3px;background:#0b0b0b"></div>'
                       for y in (359, 719))
        sc.raw(f'<div id="{sc.uid("hgl")}" class="clip grp" {sc.timed(t0, t1)} data-track-index="5" data-layout-ignore '
               f'style="z-index:{sc.nz() + 620}">{grid}</div>')


def heyes(sc, t, frames=3, box=(700, 250, 520, 130)):
    """Heath 11.1: a difference box over the eyes, a few frames."""
    blk(sc, t, frames, box, "#D8E6E6", blend="difference", z=sc.nz() + 650)


def hwhite(sc, t, frames=1):
    """Heath 12.1: a white flash frame."""
    blk(sc, t, frames, (0, 0, 1920, 1080), "#FFFDF8", z=sc.nz() + 900)


def hsil(sc, cutout, t, frames=2, box=(560, 120, 800, 960)):
    """Heath 24.1: the subject as a white glowing silhouette for two frames."""
    x, y, w, h = box
    sc.raw(f'<img id="{sc.uid("sil")}" class="clip" src="assets/img2/{cutout}" alt="" {sc.timed(t, round(t + frames * F1, 3))} '
           f'data-track-index="4" data-layout-allow-occlusion style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
           f'height:{h}px;object-fit:contain;object-position:50% 100%;filter:brightness(0) invert(1) '
           f'drop-shadow(0 0 30px rgba(255,255,255,0.9));z-index:{sc.nz() + 800}" />')


def hprism(sc, t, y=600, frames=6, w=1100):
    """Heath 22.1-23.1: a prism streak sweeping across the words."""
    pid = sc.uid("prism")
    sc.raw(f'<div id="{pid}" class="clip solid" {sc.timed(t, round(t + frames * F1, 3))} data-track-index="6" data-layout-ignore '
           f'style="left:{960 - w // 2}px;top:{y - 22}px;width:{w}px;height:44px;background:linear-gradient(90deg, rgba(255,60,60,0) 0%, '
           f'#ff4a4a 14%, #ffb23b 28%, #fff24a 42%, #4aff8a 56%, #4ad8ff 70%, #7a5bff 84%, rgba(255,60,220,0) 100%);'
           f'filter:blur(6px);mix-blend-mode:screen;opacity:0.9;z-index:{sc.nz() + 1500}"></div>',
           [f'tl.fromTo("#{pid}", {{ x: -520 }}, {{ x: 520, duration: {r3(frames * F1)}, ease: "power1.inOut", '
            f'immediateRender: false }}, {sc.at(t)});'])


# ---- S11  45.83-48.04  "18 months of no job."  him alone at home, framed on the vignette; the family photos; a black
#      beat; the paper's "Quits Abruptly" with the box over his eyes
s = Scene("s11", CUT(VT(102)), CUT(VT(107)), tex=(0.06, 0.0))
hframe(s, "MPB", 1134.0, CUT(VT(102)), round(CUT(VT(104)) - 0.3, 3))
kc(s, [(round(CUT(VT(104)) - 0.3, 3), "MPB", 1121.0, None)], CUT(VT(104)))
kblack(s, CUT(VT(104)), CUT(VT(106)))
kc(s, [(CUT(VT(106)), "MPB", 1124.0, None)], CUT(VT(107)), push=(1.0, 1.05))   # v9 (user): him, on video
heyes(s, round(CUT(VT(106)) + 3 * F1, 3), 3, (700, 250, 520, 120))
cap([[W_(102, "sx", "18"), W_(103, "sh", "months")]], end=CUT(VT(104)), scrim=0.4)
cap([[W_(104, "s"), W_(105, "s")]], end=CUT(VT(106)))
cap([[W_(106, "sx", "job")]], end=CUT(VT(107)), scrim=0.5)

# ---- S12  48.04-52.78  "He took up boxing, read biographies, even met Bezos for a job at Amazon."  no boxing gloves:
#      old footage of him (user); the books fast; Bezos: the grid of him and Dimon, a card slamming in, then the cards
#      cycling (Heath's villains) - video behind, photos only as cards (user)
s = Scene("s12", CUT(VT(107)), CUT(VT(121)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(107)), "MPB", 1090.0, None)], round(CUT(VT(110)) - 0.05, 3))
hframe(s, "MPB", 1105.0, round(CUT(VT(110)) - 0.05, 3), CUT(VT(111)))
kc(s, [(CUT(VT(111)), "MPB", 616.0, None), (round(CUT(VT(111)) + 0.3, 3), "MPB", 1496.0, None),
       (round(CUT(VT(112)) + 0.25, 3), "MPB", 1120.0, None), (round(CUT(VT(113)) - 0.45, 3), "MPB", 1110.0, None)],
   CUT(VT(113)))
hwhite(s, round(CUT(VT(113)) - 0.45, 3))
hgrid(s, CUT(VT(113)), CUT(VT(116)), [("UNT", 836.0), ("MPB", 1300.0), ("UNT", 840.0), ("MPB", 1090.5), ("UNT", 844.0),
                                       ("MPB", 1105.5), ("UNT", 838.0), ("MPB", 1330.0), ("UNT", 842.0)], invert=(4, 8))
kpcard(s, BEZ_LAUGH, CUT(VT(115)), CUT(VT(116)), (560, 170, 800, 560), rot=-3.0, slide=(900, 0))
hcards(s, [("i", BEZ_AMZ, 2.5), ("v", "UNT", 840.0, -2.0), ("i", BEZ_LAUGH, 1.5), ("v", "UNT", 836.5, -1.5)],
       CUT(VT(116)), CUT(VT(121)))
cap([[W_(107, "s"), W_(108, "s"), W_(109, "s")], [W_(110, "sh", "boxing")]], end=CUT(VT(111)), scrim=0.4)
cap([[W_(111, "s")], [W_(112, "sh", "biographies")]], end=CUT(VT(113)), scrim=0.45)
cap([[W_(113, "s"), W_(114, "s")], [W_(115, "sh")]], end=CUT(VT(116)), scrim=0.45)
cap([[W_(116, "s"), W_(117, "s"), W_(118, "s"), W_(119, "s")], [W_(120, "shy", "Amazon")]], end=CUT(VT(121)),
    scrim=0.45)

# ---- S13  52.78-57.10  "But it was all a premise for the greatest comeback in the history of Wall Street."
s = Scene("s13", CUT(VT(121)), CUT(VT(137)), tex=(0.06, 0.0))
kblack(s, CUT(VT(121)), CUT(VT(126)))
kc(s, [(CUT(VT(126)), "MPB", 1319.0, None), (CUT(VT(127)), "MPB", 1299.0, None)], CUT(VT(130)))
sp_text_behind(s, CUT(VT(130)), CUT(VT(131)), CUT_DIMON_SMILE, "comeback", size=430)   # Heath 23.6: the word behind him
hsil(s, CUT_DIMON_SMILE, round(CUT(VT(131)) - 2 * F1, 3))                              # Heath 24.1: white for two frames
kc(s, [(CUT(VT(131)), "HOW", 32.0, None), (round(CUT(VT(133)) + 0.05, 3), "HOW", 146.0, None),
       (CUT(VT(135)), "HOW", 306.0, None)], CUT(VT(137)), grade="bw")
hwhite(s, CUT(VT(131)))
kdiff(s, CUT(VT(135)), 1)
cap([[W_(121, "s"), W_(122, "s"), W_(123, "s"), W_(124, "s"), W_(125, "s")]], end=CUT(VT(126)))
cap([[W_(126, "sh")]], end=CUT(VT(127)), scrim=0.4)
cap([[W_(127, "s"), W_(128, "s")], [W_(129, "sh")]], end=CUT(VT(130)), scrim=0.4)
cap([[W_(131, "s"), W_(132, "s")], [W_(133, "sh")]], end=CUT(VT(134)), scrim=0.45)
cap([[W_(134, "s")], [W_(135, "shy"), W_(136, "shy", "Street")]], end=CUT(VT(137)), scrim=0.45)

# ---- S14  57.10-60.34  "In 2000, he takes over a broken bank in Chicago,"
s = Scene("s14", CUT(VT(137)), CUT(VT(147)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(137)), "UNT", 865.9, (0.5, 0.5, UNT_ZOOM)), (CUT(VT(139)), "MPB", 1308.5, None)], CUT(VT(143)))
hframe(s, "MPB", 1310.5, CUT(VT(143)), CUT(VT(145)))
for k, f in enumerate((1, 3, 4)):                       # broken: the frame cracks for a moment
    blk(s, round(CUT(VT(143)) + f * F1, 3), 1, (0, 300 + 160 * k, 1920, 140 + 40 * k), "#E6E6E6", blend="difference",
        z=s.nz() + 700)
hwhite(s, CUT(VT(145)))
kc(s, [(round(CUT(VT(145)) + F1, 3), "MPB", 1249.0, None)], CUT(VT(147)))
cap([[W_(137, "s")], [W_(138, "sx", "2000")]], end=CUT(VT(139)), scrim=0.45)
cap([[W_(139, "s"), W_(140, "s"), W_(141, "s"), W_(142, "s")], [W_(143, "sh"), W_(144, "sh")]], end=CUT(VT(145)), scrim=0.45)
cap([[W_(145, "s")], [W_(146, "sh", "Chicago")]], end=CUT(VT(147)), scrim=0.4)

# ---- S15  60.34-62.16  "cuts the dividend, cleaned it up,"
s = Scene("s15", CUT(VT(147)), CUT(VT(153)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(147)), "MPB", 1343.0, None)], CUT(VT(150)))                      # v9 (user): his video
CUTS_A, CUTS_B = round(CUT(VT(147)) + 2 * F1, 3), round(CUT(VT(147)) + 9 * F1, 3)
for half, (y0, dx) in enumerate(((0, -90), (540, 90))):                            # on "cuts": the frame splits in two,
    hc, _ = s.v("MPB", round(1343.0 + 2 * F1, 3), CUTS_A, CUTS_B, grade="doc", push=None, box=(0, y0, 1920, 540),
                z=s.nz() + 300, vstyle=f"object-position:50% {0 if half == 0 else 100}%")   # the halves slide apart
    s.J(f'tl.fromTo("#{hc}", {{ x: 0 }}, {{ x: {dx}, duration: {r3(4 * F1)}, ease: "power3.out", immediateRender: false }}, '
        f'{s.at(CUTS_A)});')
    s.J(f'tl.to("#{hc}", {{ x: 0, duration: {r3(3 * F1)}, ease: "power3.in" }}, {s.at(round(CUTS_A + 4 * F1, 3))});')
blk(s, CUTS_A, 7, (0, 532, 1920, 16), "#ffffff", z=s.nz() + 700)                  # the white cut between them
heyes(s, CUT(VT(149)), 3, (720, 230, 520, 120))
hframe(s, "MPB", 1339.0, CUT(VT(150)), CUT(VT(153)))
cap([[W_(147, "s"), W_(148, "s")], [W_(149, "sh", "dividend")]], end=CUT(VT(150)), scrim=0.45)
cap([[W_(150, "s"), W_(151, "s")], [W_(152, "sh", "up")]], end=CUT(VT(153)), scrim=0.4)

# ---- S16  62.16-65.75  "and puts $60 million of his own money into the stock."  him telling it (the Untold clip:
#      2 million shares for $57 million); the prism over the money; his white silhouette; the ticker
s = Scene("s16", CUT(VT(153)), CUT(VT(164)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(153)), "UNT", 902.0, (0.5, 0.4575, 1.52)), (CUT(VT(157)), "MPB", 1329.0, None)], CUT(VT(161)))
#   v9: cropped between the Untold film's burned-in place label (top, to y 0.12) and its subtitle (from y 0.795)
hprism(s, round(CUT(VT(155)) + 4 * F1, 3), y=560, frames=7)
hsil(s, CUT_DIMON_UP, round(CUT(VT(157)) - 2 * F1, 3))
hgrid(s, CUT(VT(161)), CUT(VT(164)), [("WSMONT", 3.77), ("BM", 0.10), ("WSMONT", 4.20), ("JPFLASH", 5.50), ("CRASH", 4.5),
                                       ("BM", 4.25), ("WSMONT", 3.95), ("JPFLASH", 8.60), ("BM", 7.15)], invert=(2, 6))
cap([[W_(153, "s"), W_(154, "s")]], end=CUT(VT(155)), scrim=0.4)
cap([[W_(155, "sxy@280", "$60"), W_(156, "shy", "million")]], end=CUT(VT(157)), scrim=0.45)
cap([[W_(157, "s"), W_(158, "s"), W_(159, "s")], [W_(160, "sh", "money")]], end=CUT(VT(161)), scrim=0.4)
cap([[W_(161, "s"), W_(162, "s")], [W_(163, "sh", "stock")]], end=CUT(VT(164)), scrim=0.55)

# ---- S17  65.75-69.52  "Turn a $500 million loss into billions in profit."
s = Scene("s17", CUT(VT(164)), CUT(VT(173)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(164)), "UNT", 944.0, (0.5, 0.5, UNT_ZOOM))], CUT(VT(168)))
hframe(s, "CRASH", 88.5, CUT(VT(168)), CUT(VT(169)))
kc(s, [(CUT(VT(169)), "UNT", 954.0, (0.5, 0.5, UNT_ZOOM)), (CUT(VT(170)), "MPILE", 0.25, None)], CUT(VT(173)))   # v9 (user):
#   their money clip at 4x under "billions in profit" (source 1.0-7.2 s, dollars only)
hprism(s, round(CUT(VT(170)) + 3 * F1, 3), y=600, frames=7)
hwhite(s, CUT(VT(171)))
cap([[W_(164, "s"), W_(165, "s")], [W_(166, "sh", "$500"), W_(167, "sh", "million")]], end=CUT(VT(168)), scrim=0.45)
cap([[W_(168, "sx", "loss")]], end=CUT(VT(169)), scrim=0.45)
cap([[W_(169, "s")], [W_(170, "shy", "billions")]], end=CUT(VT(171)), scrim=0.45)
cap([[W_(171, "s")], [W_(172, "sh", "profit")]], end=CUT(VT(173)), scrim=0.45)

# ---- S18  69.52-72.69  "That bank got acquired by JP Morgan in 2004."  the announcement, CNBC and the building as cards
#      cycling on the vignette (Heath's villains), then the sign full frame
s = Scene("s18", CUT(VT(173)), CUT(VT(182)), tex=(0.06, 0.0))
hcards(s, [("v", "UNT", 1045.0, -2.0), ("v", "UNT", 1041.0, 2.0), ("v", "HOW", 691.5, -1.5)], CUT(VT(173)), CUT(VT(180)))
kc(s, [(CUT(VT(180)), "HOW", 692.3, None)], CUT(VT(182)))   # v9: the JPMorgan Chase facade, flags in the windows (the
#   documentary's own '...merged with Bank One in 2004'); no narrator, and not the flash edit's sign, which carries its
#   creator's watermark
hwhite(s, CUT(VT(180)))
cap([[W_(173, "s"), W_(174, "s"), W_(175, "s")], [W_(176, "sh")]], end=CUT(VT(178)), scrim=0.45)
cap([[W_(177, "s")], [W_(178, "sh"), W_(179, "sh")]], end=CUT(VT(180)), scrim=0.45)
cap([[W_(180, "s")], [W_(181, "sx", "2004")]], end=CUT(VT(182)), scrim=0.45)

# ---- S19  72.69-75.21  "Then, 2008 financial crisis hit,"  a black beat; the crash on nine screens (Heath's grid)
s = Scene("s19", CUT(VT(182)), CUT(VT(187)), tex=(0.06, 0.0))
kblack(s, CUT(VT(182)), CUT(VT(183)))
s.v("TRIP", 0.36, CUT(VT(182)), CUT(VT(183)), grade="doc", push=None, z=s.nz() + 450,   # v9 (user's fast collage, 3x):
    cam_style="opacity:0.45")                   # the walkers, the eye and the collage flicker through the black beat
kc(s, [(CUT(VT(183)), "CRASH", 112.5, None)], CUT(VT(184)))
hgrid(s, CUT(VT(184)), CUT(VT(186)), [("CRASH", 4.5), ("CRASH", 16.5), ("CRASH", 64.5), ("CRASH", 52.5), ("MPB", 1769.0),
                                       ("CRASH", 88.5), ("CRASH", 136.5), ("CRASH", 160.5), ("CRASH", 100.5)], invert=(1, 5, 6))
kc(s, [(CUT(VT(186)), "CRASH", 184.5, None)], CUT(VT(187)))
hwhite(s, CUT(VT(186)))
cap([[W_(182, "s", "Then")]], end=CUT(VT(183)))
cap([[W_(183, "sx", "2008")]], end=CUT(VT(184)), scrim=0.45)
cap([[W_(184, "s")], [W_(185, "sh", "crisis")]], end=CUT(VT(186)), scrim=0.55)
cap([[W_(186, "sx", "hit")]], end=CUT(VT(187)), scrim=0.45)

# ---- S20  75.21-77.06  "and when every other bank was dying,"  the floor; the dying banks as cards (Heath's villains)
s = Scene("s20", CUT(VT(187)), CUT(VT(194)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(187)), "UNT", 1129.0, (0.5, 0.5, UNT_ZOOM))], CUT(VT(190)), grade="bw")
hcards(s, [("v", "MPB", 1781.0, -2.5), ("v", "CRASH", 76.5, 2.0), ("v", "MPB", 1789.0, -1.5), ("v", "CRASH", 148.5, 2.5)],
       CUT(VT(190)), CUT(VT(192)))
kc(s, [(CUT(VT(192)), "CRASH", 136.5, None)], CUT(VT(194)), grade="bw")
cap([[W_(187, "s"), W_(188, "s"), W_(189, "s")], [W_(190, "sh"), W_(191, "sh")]], end=CUT(VT(192)), scrim=0.45)
cap([[W_(192, "s")], [W_(193, "sh", "dying")]], end=CUT(VT(194)), scrim=0.45)

# ---- S21  77.06-78.51  "he was the only one standing"  him; his white silhouette; the book: LAST MAN STANDING
s = Scene("s21", CUT(VT(194)), CUT(VT(200)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(194)), "MPB", 1859.0, None), (CUT(VT(198)), "MPB", 1915.5, None)], CUT(VT(200)))
hsil(s, CUT_DIMON_UP, round(CUT(VT(198)) - 2 * F1, 3))
cap([[W_(194, "s"), W_(195, "s"), W_(196, "s"), W_(197, "s")]], end=CUT(VT(198)), scrim=0.4)
cap([[W_(198, "s")], [W_(199, "sx", "standing")]], end=CUT(VT(200)), scrim=0.45)

# ---- S22  78.51-81.13  "with enough money to buy the ones that fell."
s = Scene("s22", CUT(VT(200)), CUT(VT(209)), tex=(0.06, 0.0))
kc(s, [(CUT(VT(200)), "MPB", 1829.0, None), (CUT(VT(203)), "UNT", 1159.0, (0.5, 0.5, UNT_ZOOM))], CUT(VT(205)))
heyes(s, round(CUT(VT(203)) + 2 * F1, 3), 3, (760, 300, 560, 120))
hframe(s, "MPB", 1780.0, CUT(VT(205)), CUT(VT(207)), grade="bw")
kc(s, [(CUT(VT(207)), "CRASH", 76.5, None)], CUT(VT(209)), grade="doc")
sp_cards_fall(s, CUT(VT(207)), CUT(VT(209)), [("logo", LOGO["lehman"]), ("logo", LOGO["wamu"]), ("photo", CRISIS_PICS[1])],
              VT(208))
cap([[W_(200, "s"), W_(201, "s")], [W_(202, "sh", "money")]], end=CUT(VT(203)), scrim=0.45)
cap([[W_(203, "s")], [W_(204, "sh", "buy")]], end=CUT(VT(205)), scrim=0.45)
cap([[W_(205, "s"), W_(206, "s"), W_(207, "s")], [W_(208, "sh", "fell")]], end=CUT(VT(209)), scrim=0.45)

# ---- S23  81.13-88.22  "That's JP Morgan and Chase, the name that moves $10 trillion every single day today."  the
#      user's 'cut cut' panels; the prism over the $10 trillion; every single day on nine screens; the building
s = Scene("s23", CUT(VT(209)), DUR, tex=(0.06, 0.0))
P0 = CUT(VT(211))
kc(s, [(CUT(VT(209)), "JPFLASH", 9.30, None), (P0, "JPFLASH", 10.20, (0.5, 0.40, 1.35))], CUT(VT(214)) + 0.1)
#   v9: the ticker from the flash edit's own white frame, out before its cut-out blob (9.93); the sign shot cropped to
#   its top three quarters, clear of the creator's watermark
P1 = kpanels(s, P0, CUT(VT(214)), "CUTCUT", 8.70, n=6, step=5)
kc(s, [(CUT(VT(214)), "CUTCUT", round(8.70 + (CUT(VT(214)) - P0), 3), None), (CUT(VT(219)), "BM", 4.25, None)],
   CUT(VT(220)))
hprism(s, round(CUT(VT(218)) + 4 * F1, 3), y=600, frames=8)
s.v("MPILE", 2.0, CUT(VT(218)), min(round(CUT(VT(219)) + 0.5, 3), CUT(VT(220))), grade="doc", push=None,
    z=s.nz() + 150, cam_style="opacity:0.32;mix-blend-mode:screen")   # v9: their money clip, faint, under "$10 trillion"
#   (a double exposure on the office and the stock board; it ends where the pale notebook shot dissolves in)
hgrid(s, CUT(VT(220)), CUT(VT(223)), [("BM", 0.15), ("JPFLASH", 5.55), ("WSMONT", 8.05), ("LASTFAST", 3.70),
                                       ("JPHORIZ", 2.0), ("BM", 2.85), ("JPFLASH", 1.30), ("WSMONT", 3.80), ("BM", 7.20)],
      invert=(3, 7))
kc(s, [(CUT(VT(223)), "GAME", 108.0, None)], DUR)
hwhite(s, CUT(VT(223)))
blk(s, round(DUR - 0.35, 3), 11, (0, 0, 1920, 1080), "#000000", opacity=0.55, z=s.nz() + 700)
cap([[W_(209, "s", "That's")], [W_(210, "sh"), W_(211, "sh")]], end=CUT(VT(212)), scrim=0.45)
cap([[W_(212, "s")], [W_(213, "sh", "Chase")]], end=CUT(VT(214)), scrim=0.45)
cap([[W_(214, "s"), W_(215, "s"), W_(216, "s"), W_(217, "s")], [W_(218, "shy", "$10"), W_(219, "shy", "trillion")]],
    end=CUT(VT(220)), scrim=0.45)
cap([[W_(220, "s"), W_(221, "s")], [W_(222, "sh", "day")]], end=CUT(VT(223)), scrim=0.55)
cap([[W_(223, "sx", "today")]], end=DUR, scrim=0.4, exit="fade")


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
    # v11: the narration's first part in three pieces, the two pauses cut (VO_CUTS); each joint sits in silence
    VO1_PIECES, at, ms = [], VO1_AT, VO1_IN
    for k, (a, b) in enumerate(VO_CUTS + [(VO1_OUT, None)]):
        VO1_PIECES.append((f"vo-a{k or ''}", "vo.wav", round(at, 3), round(a - ms, 3), round(ms, 3), 0.01 if k else 0.0,
                           0.01 if b is not None else 0.06))
        at, ms = at + (a - ms), b
    auds = [("news", "news_voice.wav", 0.0, NEWS_DUR, 0.0, 0.0, 0.02),
            *([("music", "music_bed.wav", 0.0, DUR, 0.0, 0.0, 0.05)] if MUSIC else []),
            *VO1_PIECES,
            ("dimon", "dimon_quote.wav", QUOTE_AT, round(QUOTE_END - QUOTE_AT, 3), round(QUOTE_SRC0 - 272.5, 3), 0.02, 0.08),
            ("vo-b", "vo.wav", round(VO2_IN + VO2_OFF, 3), VO2_OUT - VO2_IN, VO2_IN, 0.0, 0.08)]
    a_html = []
    lane = {"music": 11}
    for aid, src, st, d, ms, fi, fo in auds:
        d = round(min(d, DUR - st), 3)
        if d <= 0:
            continue
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


PREVIEW_END = None   # v8 (user): the whole film (v7 round 1 ended after "he was fired")
if os.environ.get("DIMON_PREVIEW") == "board":  # v10 round 2: up to the end of the pinboard (S09)
    PREVIEW_END = CUT(VT(95))
if os.environ.get("DIMON_PREVIEW") == "meet":   # v10 round 1: the film up to the end of the Meet section (the pinned
    PREVIEW_END = S7_END                         # renderer's --end needs under 2 GB of media, and this film has 2.6)


def trim_to_preview():
    """Keep the scenes, captions and audio before PREVIEW_END (the later scenes are rebuilt next round)."""
    global DUR
    if not PREVIEW_END:
        return
    DUR = PREVIEW_END
    SCENES[:] = [sc for sc in SCENES if sc.start < DUR - 1e-6]
    for sc in SCENES:
        sc.end = min(sc.end, DUR)
    first = lambda g: min(t for line in g["lines"] for _, t, _ in _words(line))
    CAPS[:] = [g for g in CAPS if first(g) < DUR - 1e-6]
    for g in CAPS:
        if g["end"] is not None:
            g["end"] = min(g["end"], DUR)


if __name__ == "__main__":
    trim_to_preview()
    MEDIA["cyber"] = CYBER
    json.dump(MEDIA, open(f"{PRJ}/tools/media_v11.json", "w"), indent=1)
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
