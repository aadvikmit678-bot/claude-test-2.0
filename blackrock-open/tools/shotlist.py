"""The rest of the script, shot by shot (pure data, read by prep_v3.py to cut the clips and by build.py to place them).

Each shot: (start, name, source, source start s, ffmpeg crop or None, frame-count start). `start` is a word key of the
rest recording (timing.RW), or "rest1" / "rest2" for the first frame of each part. A shot ends where the next starts.
Sources: X = the BlackRock explainer the user gave, J = the Jamie Dimon edit's clip library, D = the BlackRock
downloads, P = the FII panel. Cards (solid colour + a big word) and the opening's touch / logos clips are marked by
the source "card" / "clip". N = the five videos the user added on Nov 21 (asher, conspirant, bazzarbyte, axirohq).
"""
X, J, D, P, N, E, FX = "X", "J", "D", "P", "N", "E", "FX"

ASH = "crop=1700:956:204:0"          # asher.mp4: drops the channel badge (bottom left) and the burned-in subtitles


def band(y):
    """A 16:9 band of a vertical 1080x1920 video."""
    return f"crop=1080:608:0:{y}"


# N = the user's new Drive videos (blackrock-src/dl/v3/new): (file, crop)
REST1 = [
    ("rest1", "r1_flags", N, 2.52, ("asher.mp4", ASH), True),            # A company (BlackRock HQ, its flags)
    ("that_r", "r1_tower", X, 175.0, "crop=iw*0.8:ih*0.8:iw*0.1:ih*0.2", False),  # the sign above the caption                        # that manages (the tower at night)
    # "$15 trillion in assets": the user's montage from its 3 s (charts, cash, cars, jets), the big serif over it
    ("15", "r1_montage", N, 3.0, ("../pin/montage15t.mp4", None), False),
    # the founders block (the user's notes): Think School's "Founders vs Blackrock" graphic, one company at a time,
    # centred; each founder in the Nvidia reel's opening treatment (Jensen: the reel's own clip). FX = pre-rendered.
    ("holds", "tsg_nv", FX, 0, None, False),                              # holds more of Nvidia than
    ("jensen", "r1_jensen", FX, 0, None, False),                          # Jensen Huang,
    ("more2", "tsg_ms", FX, 0, None, False),                              # more of Microsoft than
    ("bill", "r1_gates", FX, 0, None, False),                             # Bill Gates,
    ("and1", "tsg_ap", FX, 0, None, False),                               # and more of Apple than
    ("steve", "r1_jobs", FX, 0, None, False),                             # Steve Jobs ever did.
]

# the rest of the script, cut fast (the user: "a fast-paced edit"; no still held): a shot starts on a word key or, as a
# number, at a rest-recording time between words. "../pin" and "../../" reach the user's Pinterest clips and downloads.
REST2 = [
    ("rest2", "r2_ticker", J, 0.0, "WSMONT_377_141", False),            # Back in
    ("1980s", "r2_wolf", J, 0.0, "WOLFE_683_55", False),                # the 1980s,
    (11.95, "r2_gekko", J, 0.0, "WSMONT_420_141", False),               # (Wall Street, 1987)
    ("larry1", "r2_finkwalk", N, 3.55, ("../../m_fink_fast.mp4", "crop=1080:608:0:236"), False),  # Larry Fink was a
    ("wall1", "r2_bull", N, 2.535, ("axirohq.mp4", None), True),        # Wall (the Charging Bull)
    ("street1", "r2_nysefloor", N, 4.34, ("axirohq.mp4", None), True),  # Street (the NYSE floor)
    ("prodigy", "r2_floor", J, 0.0, "CRASH_7650_125", False),           # prodigy,
    # "But one bad bet cost him a $100 million loss. That was enough to get him thrown out of Wall Street." -- the
    # Higgsfield scene: the user's ChatGPT keyframes animated with Kling 3.0 Pro (FX = pre-rendered by r_bet)
    ("but1", "bet1", FX, 0, None, False),                               # But one bad bet cost him (green -> red)
    ("100", "bet2", FX, 0, None, False),                                # $100 million loss. (the red screens)
    ("that1", "bet3", FX, 0, None, False),                              # That was enough ... thrown out of Wall Street
    ("and2", "r2_eye", N, 1.3, ("../pin/eye.mp4", None), False),        # and to convince him (an eye opens)
    ("onething", "r2_chess", N, 0.15, ("../pin/crash_chess.mp4", "crop=720:405:0:330"), False),  # of one thing. (chess)
    ("wall3", "r2_screens2", N, 42.0, ("bazzarbyte.mp4", band(700)), True),  # Wall Street is
    ("terrible", "r2_floor2", J, 0.0, "CRASH_7630_69", False),          # terrible
    ("seeing", "r2_eye2", N, 16.3, ("../pin/eye.mp4", None), False),    # at seeing (the blue eye)
    ("risk1", "r2_lehman", J, 0.0, "STO_124700_70", False),             # risk.
    ("so", "r2_nyc", N, 0.2, ("bazzarbyte.mp4", band(700)), True),      # So, in 1988, (Manhattan at night; 1988 big)
    ("he1", "r2_towerbase", N, 20.30, ("bazzarbyte.mp4", band(820)), True),  # he co-founded (a glass tower)
    ("blackrock", "r2_brmark", N, 4.0, ("conspirant.mp4", band(650)), True),  # BlackRock (its red mark, money falling)
    ("built", "r2_screens", N, 7.75, ("asher.mp4", ASH), True),         # and built (BlackRock's own screens)
    ("system", "r2_datacenter", N, 59.42, ("bazzarbyte.mp4", band(1000)), True),  # a system with one
    ("job", "r2_ring", N, 60.45, ("bazzarbyte.mp4", band(760)), True),  # job --
    ("calculating", "r2_lines", X, 54.5, None, False),                  # calculating
    ("risk2", "r2_map", N, 16.2, ("bazzarbyte.mp4", band(820)), True),  # risk. (the network over the map)
    ("he_called", "r2_halo", N, 5.3, ("../pin/cinematic_user.mp4", "crop=968:545:156:88"), False),  # He called it
    ("aladdin", "r2_earth", N, 55.2, ("bazzarbyte.mp4", band(560)), True),  # Aladdin. (the globe of lights)
    ("when", "r2_crash", J, 0.0, "CRASH_11250_89", False),              # When the
    ("2008", "r2_floor3", J, 0.0, "CRASH_7660_42", False),              # 2008
    ("crisis1", "r2_alert", J, 0.0, "CRASH_13650_104", False),          # crisis hit, (the news alert)
    ("the_us", "r2_flag", J, 0.0, "flag_slow", False),                  # the U.S. (the flag)
    ("government", "r2_gov", X, 6.0, None, False),                      # government called
    ("oneguy", "r2_king", N, 1.0, ("../pin/pint_videos.mp4", "crop=720:405:0:440"), False),  # the one guy (the king)
    ("threw", "bet3fb", FX, 0, None, False),                            # threw out years ago (the walk-out again, grey)
    ("clean", "r2_indu", J, 0.0, "CRASH_16000_160", False),             # to clean up (the INDU board)
    ("mess", "r2_mess", N, 3.0, ("../pin/money_laundering.mp4", "crop=720:405:0:440"), False),  # the mess --
    ("larry2", "r2_finklive", N, 13.3, ("../../m_fink1.mp4", None), False),   # Larry Fink. (him on a stage)
    ("he2", "r2_cash", J, 0.12, "STO_31075_137", False),                # He came out
    (42.47, "r2_anchor", J, 0.0, "CRASH_18460_71", False),              # of that crisis (the news)
    ("three", "r2_towerup", N, 22.70, ("bazzarbyte.mp4", band(420)), True),  # with three times (the tower)
    ("money1", "r2_piles", J, 0.0, "MPILE_200_119", False),             # the money. (stacks of $100 bills)
    ("today", "r2_trails", N, 62.3, ("bazzarbyte.mp4", band(900)), True),  # Today, every time (the city's lights)
    ("buy", "r2_trade", N, 5.2, ("bazzarbyte.mp4", band(700)), True),   # you buy (the screens)
    ("sp", "r2_sp", N, 22.45, ("conspirant.mp4", band(0)), True),       # the S&P (its logo wall)
    ("500", "r2_logos", N, 25.0, ("conspirant.mp4", band(700)), True),  # 500, (the giants it owns)
    ("your", "r2_network", N, 26.80, ("conspirant.mp4", band(590)), True),  # your money ends up in (the web)
    ("this", "r2_finkcash", N, 3.0, ("conspirant.mp4", band(600)), True),   # this guy's hands (Fink holding a dollar)
    # "A company that has never made a single product, but everything you own, everything you touch," -- the user's
    # video for the last part (products, falling figures); cropped below its "@YS_MR4" watermark (y 50-75) and above
    # its bottom bar; then Fink on "has a piece of him"
    ("a2", "r2_ending", E, 0.40, "crop=566:318:85:80", False),
    ("has", "r2_finkend", P, 1185.3, None, False),                      # has a piece of him in it. (a slow push in)
]

# talking heads that barely move get a slow push in (the user: no shot that looks still)
PUSH = {"r2_finklive": 0.07, "r2_finkend": 0.08}

# big words over the footage: (word key, text, until key)
HERO = [("15", "$15 trillion", "holds"), ("100", "$100 million", "that1"), ("risk1", "risk.", "so"),
        ("1988", "1988", "he1"), ("2008", "2008", "crisis1"), ("three", "3x", "today")]
# set in Instrument Serif with the Dario video's white glow (the user, Nov 21: not League Gothic)

# the storyline captions (the Jensen reel's Helvetica caps): (text, start word key or rest-file seconds, end or None)
# a third item "ink" sets the caption dark (over Think School's light grey page)
CAPS1 = [("A company", 0.09), ("that manages", 0.71), ("in assets", 3.04), ("holds more", 4.01, "ink"),
         ("of Nvidia", 4.44, "ink"), ("than", 5.00, "ink"), ("Jensen Huang,", 5.19), ("more of", 6.20, "ink"),
         ("Microsoft", 6.57, "ink"), ("than", 7.24, "ink"), ("Bill Gates,", 7.38), ("and more of", 8.10, "ink"),
         ("Apple", 8.82, "ink"), ("than", 9.10, "ink"), ("Steve Jobs", 9.61), ("ever did.", 10.16)]
CAPS2 = [("Back in", 10.63), ("the 1980s,", 11.14), ("Larry Fink", 12.63), ("was a", 13.14),
         ("Wall Street prodigy,", 13.44), ("but one", 14.96), ("bad bet", 15.52), ("cost him", 16.08), (None, 16.56),
         ("loss.", 17.87), ("That was enough", 18.21), ("to get him", 19.12), ("thrown out", 19.56),
         ("of Wall Street", 20.14), ("and to convince him", 20.92), ("of one thing.", 21.95), ("Wall Street", 23.31),
         ("is terrible", 23.85), ("at seeing", 24.56), (None, 25.02), ("he co-founded", 27.52), ("BlackRock", 28.31),
         ("and built a system", 28.96), ("with one job", 29.95), ("calculating risk.", 30.87), ("He called it", 32.39),
         (None, 33.42), ("When the", 34.16), (None, 34.56), ("crisis hit,", 35.24), ("the U.S. government", 36.03),
         ("called", 37.04), ("the one guy", 37.38), ("Wall Street threw out", 37.88), ("years ago", 38.84),
         ("to clean up the mess", 39.36), ("Larry Fink.", 40.80), ("He came out", 41.63), ("of that crisis", 42.26),
         (None, 43.44), ("the money.", 44.16), ("Today,", 45.13), ("every time", 45.46), ("you buy", 46.11),
         ("the S&P 500,", 46.64), ("your money", 48.19), ("ends up", 48.69), ("in this guy’s hands.", 49.07),
         ("A company", 50.36), ("that has never made", 50.90), ("a single product,", 51.84), ("but everything", 53.31),
         ("you own,", 54.03), ("everything", 54.57), ("you touch,", 55.17), ("has a piece", 55.80),
         ("of him in it.", 56.37)]


# ---- v5: "Back in the 1980s" to the end, re-cut (the user, Nov 21 late night: fast, many clips per line, Larry Fink and
# BlackRock themselves, no still held, no slideshow). Each shot starts on a word of the aligned rest recording: `at` is
# the word's index in tools/words/rest.json, (index, seconds after its onset), or None for the part's first frame.
# Sources: prep_v5.SRC (LFM = the Larry Fink documentary on the Dimon drive, its burned-in words painted out).
def band(y):
    return f"crop=1080:608:0:{y}"


REST2_V5 = [
    # Back in the 1980s,  (the old film look: warm, faded, grain at low opacity)
    dict(at=None, src="LFM", t0=15.3, look="old", fx_in="flash", note="the 80s: the crowd on Wall Street"),
    dict(at=33, src="LFM", t0=22.95, look="old", note="1980s,: the trading floor"),
    dict(at=(33, 0.45), src="LFM", t0=43.25, look="old", note="men on Wall Street"),
    # Larry Fink was a Wall Street prodigy,
    dict(at=34, src="LFM", t0=55.85, look="old", push=0.10, fx=0.62, fy=0.35, fx_in="over", note="young Fink and his desk (1980s)"),
    dict(at=(35, 0.10), src="LFM", t0=56.55, look="old", push=0.06, fx=0.6, fy=0.4, note="the photo, closer"),
    dict(at=38, src="LFM", t0=18.85, look="old", note="Wall Street, the flag on the NYSE"),
    dict(at=40, src="MF", t0=8.12, look="old", note="prodigy,: a 1980s trader, phone and green screens"),
    dict(at=(40, 0.37), src="LFM", t0=17.65, look="old", note="a bond"),
    # but one bad bet cost him $100 million loss.  (the Higgsfield scene, cut tighter)
    dict(at=41, src="HF1_a", t0=1.2, span=1.7, note="the trader, green screens"),
    dict(at=43, src="HF1_b", t0=2.5, span=3.1),
    dict(at=45, src="HF1_b", t0=3.8, span=4.5, note="the screens flip red"),
    dict(at=47, src="HF2_a", t0=1.2, span=2.0, note="$100 million loss. (big words)"),
    dict(at=(48, 0.25), src="HF2_b", t0=1.0, span=1.6),
    dict(at=49, src="LFM", t0=47.2, look="old", note="loss.: a man at his terminal"),
    # That was enough to get him thrown out of Wall Street
    dict(at=50, src="HF3_b", t0=0.3, span=1.2, fx_in="over", note="the walk-out"),
    dict(at=56, src="FI", t0=96.95, note="thrown: the push"),
    dict(at=58, src="LFM", t0=35.35, look="old", fx_in="whip", note="of Wall Street"),
    dict(at=60, src="LFM", t0=35.85, look="old", note="the NYSE"),
    # and to convince him of one thing.
    dict(at=61, src="LFM", t0=36.45, look="old", note="a young trader (1980s)"),
    dict(at=64, src="FE3", t0=9.05, look="bw", note="him: Fink, black and white"),
    dict(at=66, src="LFM", t0=59.22, speed=0.75, note="one thing.: the chess clock"),
    # Wall Street is terrible at seeing risk.
    dict(at=68, src="LFM", t0=22.45, look="old", fx_in="zoom", note="the Charging Bull"),
    dict(at=70, src="LFM", t0=50.12, note="terrible: the floor"),
    dict(at=71, src="LFM", t0=50.32),
    dict(at=(71, 0.37), src="LFM", t0=51.02),
    dict(at=73, src="LFM", t0=20.9, speed=0.6, fx_in="zoom", note="seeing: the eye"),
    dict(at=74, src="FK2", t0=11.88, note="risk.: the eye in the charts"),
    # So, in 1988, he co-founded BlackRock
    dict(at=75, src="LFM", t0=18.25, note="So,: the old board"),
    dict(at=76, src="BLACK", t0=0, push=0, note="in 1988: the red card (HTML, as ON EARTH)"),
    dict(at=78, src="MBS", t0=15.6, note="he co-founded: through BlackRock's doors"),
    dict(at=80, src="LFM", t0=67.95, fx_in="whip", note="BlackRock: its sign"),
    dict(at=(80, 0.35), src="LFM", t0=68.35),
    # and built a system with one job— calculating risk.
    dict(at=81, src="MBS", t0=6.75, note="a tower from below"),
    dict(at=84, src="BZ", t0=59.42, crop=band(1000), note="a system: a data centre"),
    dict(at=86, src="LFM", t0=60.55, note="one job: the glass brain"),
    dict(at=88, src="CALC", t0=0.55, look="bw", fx_in="zoom", note="calculating: the user's chalkboard clip"),
    dict(at=89, src="FK2", t0=4.75, note="risk.: the money's eye"),
    # He called it Aladdin.
    dict(at=90, src="LFM", t0=61.65, fx_in="over", note="Fink waving at the NYSE"),
    dict(at=93, src="AL", t0=8.0, span=8.9, fx_in="flash", note="Aladdin.: the user's genie clip, its 8-9 s"),
    # When the 2008 crisis hit,
    dict(at=94, src="CR", t0=46.4, note="When the: the board"),
    dict(at=96, src="LFM", t0=50.62, fx_in="flash", note="2008 (big word): the floor"),
    dict(at=(96, 0.33), src="LFM", t0=51.32, note="a man carrying his box out"),
    dict(at=97, src="CR", t0=124.3, note="crisis: head in hands"),
    dict(at=98, src="CR", t0=184.5, note="hit,: Main St / Wall St"),
    # the U.S. government called the one guy Wall Street threw out years ago to clean up the mess— Larry Fink.
    dict(at=99, src="B2", t0=0.05, note="the U.S.: the flag over One World Trade"),
    dict(at=101, src="LFM", t0=3.35, note="government: Fink and the seal"),
    dict(at=102, src="CR", t0=116.0, note="called: Bernanke"),
    dict(at=104, src="FE3", t0=5.85, look="bw", fx_in="zoom", note="the one guy (circled)"),
    dict(at=106, src="LFM", t0=44.30, speed=0.8, look="old", note="Wall Street threw out (1980s)"),
    dict(at=108, src="HF3_a", t0=1.4, span=1.9, look="bw", note="the walk-out, grey"),
    dict(at=110, src="LFM", t0=56.6, look="old", push=0.08, fx=0.6, fy=0.4, note="years ago: the 1980s photo"),
    dict(at=112, src="LFM", t0=50.82, speed=0.4, note="to clean up: the floor"),
    dict(at=116, src="ML", t0=3.0, note="the mess"),
    dict(at=117, src="LFM", t0=58.62, speed=0.7, push=0.07, fx_in="over", note="Larry Fink."),
    # He came out of that crisis with three times the money.
    dict(at=119, src="FK2", t0=5.55, note="He came out: Fink walking"),
    dict(at=124, src="CR", t0=157.0, note="crisis: the board"),
    dict(at=125, src="BLACK", t0=1.0, tex=0.10, push=0, note="3x (big words, on black)"),
    dict(at=128, src="GE", t0=29.3, note="the money.: the printing press (the user: a different money)"),
    # Today, every time you buy the S&P 500,
    dict(at=130, src="B2", t0=7.42, fx_in="whip", note="Today,: the skyline"),
    dict(at=131, src="B2", t0=5.62, note="the street"),
    dict(at=134, src="B2", t0=9.38, note="you buy: the screens"),
    dict(at=136, src="CO", t0=22.45, crop=band(0), note="the S&P wall"),
    dict(at=(137, 0.4), src="CO", t0=25.0, crop=band(700), note="its companies"),
    # your money ends up in this guy's hands.
    dict(at=138, src="BM", t0=0.15, note="your money: the floor"),
    dict(at=140, src="LFM", t0=67.65, note="iShares by BlackRock"),
    dict(at=143, src="CO", t0=3.0, crop=band(600), note="Fink holding a dollar"),
    dict(at=145, src="LFM", t0=80.1, push=0.07, note="hands."),
    # A company that has never made a single product, but everything you own, everything you touch,
    dict(at=146, src="E", t0=0.40, push=0.03, fx_in="flash", pan="E", note="the user's ending video (its objects centred)"),
    dict(at=156, src="GE", t0=46.2, note="everything you own: American Airlines in its holdings"),
    dict(at=157, src="GE", t0=47.75, note="Nike"),
    dict(at=158, src="GE", t0=48.02, speed=0.5, note="Kraft"),
    dict(at=159, src="E", t0=4.44, push=0.03),
    # has a piece of him in it.
    dict(at=162, src="LFM", t0=79.5, note="has a piece"),
    dict(at=(165, -0.1), src="P", t0=1185.3, push=0.08, note="of him in it.: Fink at the panel"),
]


# ---- v6 (the user's notes of Nov 22): every shot of the second half is real, moving footage ("use more videos … not a
# stock photo zooming in", "no slideshow"), found by a CLIP search over every source (the Larry Fink, Jamie Dimon and
# Wall Street drives and the new BlackRock documentaries), each span checked for a hidden cut and for real motion, no
# footage repeated from anywhere in the film. Crops (source-relative, 16:9) drop the channel logos and burned-in text.
CNBC = "crop=iw*0.86:ih*0.86:iw*0.07:ih*0.12"      # the CNBC peacock (top right) and the show's line (top left)
MPU = "crop=iw*0.86:ih*0.86:iw*0.07:ih*0.14"       # More Perfect Union's badge (top right)
MPU_R = "crop=iw*0.86:ih*0.86:iw*0.14:ih*0.14"     # the same, keeping the right edge (Fink walks in there)
SIXTY = "crop=iw*0.86:ih*0.86:iw*0.14:ih*0.14"     # the 60 Minutes stopwatch (top left)
UNT_C = "crop=iw*0.82:ih*0.82:iw*0.09:ih*0.14"     # the year badge (top right)
MPB_TOP = "crop=iw*0.72:ih*0.72:iw*0.14:0"         # the ABC News lower third
MFC_C = "crop=iw*0.72:ih*0.72:iw*0.14:ih*0.04"     # the TCR timecode (bottom) and the corner letter
BRE_C = "crop=1440:810:0:100"                      # br_edit is 4:3: a 16:9 band (the trader's face)
BRE_WALL = "crop=1440:810:0:135"
FE3_C = "crop=1000:562:40:70"                      # fink_edit3 (1180x714): 16:9 without the event line (top left)
DOME = "crop=iw*0.86:ih*0.86:iw*0.04:ih*0.06"      # the Capitol dome without the CNBC peacock

REST2_V6 = [
    # Back in the 1980s,  (the old film look: warm, faded, grain at low opacity)
    dict(at=None, src="LFM", t0=15.27, speed=0.98, look="old", fx_in="flash", note="Back in: the crowd on Wall Street (1980s)"),
    dict(at=33, src="MPB", t0=800.0, look="old", note="1980s,: the trading floor on a 1980s TV set"),
    dict(at=(33, 0.45), src="LFM", t0=43.245, speed=0.78, look="old", note="men on Wall Street (1980s)"),
    # Larry Fink was a Wall Street prodigy,
    dict(at=34, src="FE3", t0=21.5, crop=FE3_C, look="old", fx_in="over", note="Larry Fink: at the table, his name card"),
    dict(at=36, src="UNT", t0=412.0, crop=UNT_C, look="old", note="was a: the 1980s boards"),
    dict(at=38, src="LFM", t0=18.85, look="old", note="Wall Street: the NYSE, its flag"),
    dict(at=40, src="BRE", t0=7.9, crop=BRE_C, look="old", note="prodigy,: a trader on two phones"),
    dict(at=(40, 0.37), src="MFC", t0=106.0, crop=MFC_C, look="old", note="a trader shouting (black and white)"),
    # but one bad bet cost him $100 million loss. -- ONE take, real speed, 60 fps (the user: "smoothed out as a
    # single video"; it was cut four times, slowed and looped): the screens flip from green to red on "$100 million"
    dict(at=41, src="HF6_1b", t0=1.2, push=0.08, note="the trader at his screens, one slow push"),
    # That was enough to get him thrown out of Wall Street
    dict(at=50, src="HF6_3b", t0=0.0, fx_in="over", note="That was enough: the walk-out (60 fps)"),
    dict(at=56, src="FI", t0=96.95, note="thrown out: the push"),
    dict(at=58, src="LFM", t0=35.35, look="old", fx_in="whip", note="of Wall Street"),
    dict(at=60, src="BR15", t0=868.0, look="old", note="Street: the NYSE and its flag, people passing"),
    # and to convince him of one thing.
    dict(at=61, src="LFM", t0=36.45, look="old", note="and to convince: a young trader (1980s)"),
    dict(at=64, src="FE3", t0=9.02, look="bw", note="him: Fink, black and white"),
    dict(at=66, src="LFM", t0=59.18, speed=0.75, note="one thing.: the chess clock"),
    # Wall Street is terrible at seeing risk.
    dict(at=68, src="BRL", t0=697.0, crop=CNBC, fx_in="zoom", note="Wall Street: the Charging Bull"),
    dict(at=70, src="STO", t0=1412.2, crop=SIXTY, note="is: traders at their screens"),
    dict(at=71, src="MPB", t0=1772.0, crop=MPB_TOP, note="terrible: the NYSE floor from above"),
    dict(at=(71, 0.37), src="BRL", t0=185.0, crop=CNBC, note="traders on their phones"),
    dict(at=73, src="LFM", t0=20.85, speed=0.6, fx_in="zoom", note="seeing: the eye"),
    dict(at=74, src="CR", t0=92.0, note="risk.: the Dow plunges"),
    # So, in 1988, he co-founded BlackRock
    dict(at=75, src="LFM", t0=18.21, note="So,: the old board"),
    dict(at=76, src="BLACK", t0=0, push=0, note="in 1988: the red card (HTML, as ON EARTH)"),
    dict(at=78, src="BRC", t0=17.0, crop=MPU, look="dimw", note="he co-founded: BlackRock's glass front"),
    dict(at=80, src="BRL", t0=33.0, crop=CNBC, fx_in="whip", note="BlackRock: its entrance at night"),
    dict(at=(80, 0.35), src="BRC", t0=358.0, crop=MPU, note="its doors on the street"),
    # and built a system with one job— calculating risk.
    dict(at=81, src="MBS", t0=6.675, look="dimw", note="and built: a tower from below"),
    dict(at=84, src="BZ", t0=59.42, crop=band(1000), note="a system: a data centre"),
    dict(at=86, src="LFM", t0=60.81, note="one job: the glass brain, then in pixels"),
    dict(at=88, src="CALC", t0=0.55, look="bw", fx_in="zoom", note="calculating: the user's chalkboard clip"),
    dict(at=89, src="FK2", t0=4.75, note="risk.: the money's eye"),
    # He called it Aladdin.
    dict(at=90, src="BRL", t0=786.6, crop=CNBC, push=0, note="He called it: Fink, one plain cut, no zoom (the user)"),
    dict(at=93, src="AL", t0=8.0, span=8.9, fx_in="flash", note="Aladdin.: the user's genie clip, its 8-9 s"),
    # When the 2008 crisis hit,
    dict(at=94, src="BRL", t0=75.0, crop=CNBC, note="When the: the ticker"),
    dict(at=96, src="AX", t0=4.5, crop=CNBC, fx_in="flash", note="2008 (big word): the NYSE floor"),
    dict(at=(96, 0.33), src="STO", t0=885.7, crop=SIXTY, note="Lehman Brothers"),
    dict(at=97, src="BR15", t0=462.0, note="crisis: a trader, his hand on his head"),
    dict(at=98, src="UNT", t0=1131.0, crop=UNT_C, note="hit,: the floor, 2008"),
    # the U.S. government called the one guy Wall Street threw out years ago to clean up the mess— Larry Fink.
    dict(at=99, src="MPB", t0=1804.0, look="dimw", note="the U.S.: the Capitol from the air"),
    dict(at=101, src="HOW", t0=631.0, crop=DOME, look="dimw", note="government: the dome"),
    dict(at=102, src="CR", t0=116.0, note="called: Bernanke"),
    dict(at=104, src="FE3", t0=5.85, look="bw", fx_in="zoom", note="the one guy (circled)"),
    dict(at=106, src="LFM", t0=44.305, speed=0.76, look="old", note="Wall Street threw out (1980s)"),
    dict(at=108, src="HF6_3a", t0=1.4, look="bw", note="threw out: the walk-out, grey (60 fps)"),
    dict(at=110, src="UNT", t0=418.0, crop=UNT_C, look="old", note="years ago: the 1980s floor"),
    dict(at=112, src="BR15", t0=585.62, note="to clean up: a man carrying his box out"),
    dict(at=116, src="HOW", t0=817.6, crop=CNBC, note="the mess: boxes out of the bank"),
    dict(at=117, src="MBS", t0=9.55, fx_in="over", note="Larry Fink.: his face"),
    # He came out of that crisis with three times the money.
    dict(at=119, src="BRC", t0=254.95, crop=MPU_R, note="He came out: he walks on and waves"),
    dict(at=122, src="STO", t0=2449.5, crop=SIXTY, look="dimw", note="of that crisis: BANK OWNED"),
    dict(at=125, src="MONEY", t0=2.0, push=0.07, look="dimw", note="with 3x the money.: the user's fire clip"),
    # Today, every time you buy the S&P 500,
    dict(at=130, src="B2", t0=7.375, speed=0.88, fx_in="whip", note="Today,: the skyline"),
    dict(at=(130, 0.40), src="B2", t0=7.745, speed=0.95, note="the Wall St sign"),
    dict(at=131, src="B2", t0=5.64, note="every time: the street"),
    dict(at=(131, 0.32), src="B2", t0=5.975, note="One World Trade Center"),
    dict(at=134, src="B2", t0=9.44, speed=0.8, note="you buy: the screens"),
    dict(at=136, src="CO", t0=22.45, crop=band(0), look="dimw", note="the S&P 500: its companies"),
    dict(at=(137, 0.4), src="BRL", t0=240.0, crop=CNBC, note="a trader at his screens"),
    # your money ends up in this guy's hands.
    dict(at=138, src="STO", t0=632.0, crop=SIXTY, note="your money: the cash"),
    dict(at=140, src="BR15", t0=871.2, crop="crop=iw*0.8:ih*0.8:iw*0.1:ih*0.2", note="ends up in: iShares by BlackRock on the NYSE"),
    dict(at=143, src="CO", t0=3.0, crop=band(600), look="dimw", note="this guy's: the dollars fly"),
    dict(at=145, src="LFM", t0=80.04, push=0.07, note="hands.: Fink"),
    # A company that has never made a single product, but everything you own, everything you touch,
    dict(at=146, src="ASH", t0=5.5, crop=ASH, look="dimw", fx_in="flash", note="A company: into BlackRock's lobby"),
    dict(at=148, src="BRL", t0=711.5, crop=CNBC, note="that has never: its revolving doors"),
    dict(at=151, src="E", t0=1.15, push=0.03, look="dimw", note="made a single product, but: the user's ending video"),
    dict(at=156, src="BRC", t0=626.0, crop=MPU, note="everything you own: the brands"),
    dict(at=158, src="BRE", t0=83.0, crop=BRE_WALL, look="dimw", note="own,: the wall of logos"),
    dict(at=159, src="E", t0=4.38, push=0.03, note="everything you touch"),
    # has a piece of him in it.
    dict(at=162, src="LFM", t0=79.5, look="dimw", note="has a piece: Fink"),
    dict(at=(165, -0.1), src="P", t0=1185.3, push=0.08, note="of him in it.: Fink at the panel"),
]
