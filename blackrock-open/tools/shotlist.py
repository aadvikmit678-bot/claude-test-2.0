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
    ("that_r", "r1_tower", X, 175.0, None, False),                        # that manages (the tower at night)
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
    dict(at=146, src="E", t0=0.40, push=0.03, fx_in="flash", note="the user's ending video (centred)"),
    dict(at=156, src="FE3", t0=22.5, look="bw", note="everything you own: the brands"),
    dict(at=158, src="FE3", t0=24.1, look="bw"),
    dict(at=159, src="E", t0=4.44, push=0.03),
    # has a piece of him in it.
    dict(at=162, src="LFM", t0=79.5, note="has a piece"),
    dict(at=(165, -0.1), src="P", t0=1185.3, push=0.08, note="of him in it.: Fink at the panel"),
]
