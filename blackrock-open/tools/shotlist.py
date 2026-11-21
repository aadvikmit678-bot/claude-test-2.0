"""The rest of the script, shot by shot (pure data, read by prep_v3.py to cut the clips and by build.py to place them).

Each shot: (start, name, source, source start s, ffmpeg crop or None, frame-count start). `start` is a word key of the
rest recording (timing.RW), or "rest1" / "rest2" for the first frame of each part. A shot ends where the next starts.
Sources: X = the BlackRock explainer the user gave, J = the Jamie Dimon edit's clip library, D = the BlackRock
downloads, P = the FII panel. Cards (solid colour + a big word) and the opening's touch / logos clips are marked by
the source "card" / "clip".
"""
X, J, D, P = "X", "J", "D", "P"

REST1 = [
    ("rest1", "r1_tower", X, 175.0, None, False),                      # A company that manages
    ("15", "r1_ft", X, 14.2, None, False),                              # $15 trillion in assets (FT: "$15.5tn")
    ("holds", "r1_nv", X, 26.6, "crop=800:450:624:359", False),         # holds more of Nvidia
    ("than1", "card_jensen", "card", 0, ("#76B900", "JENSEN HUANG"), False),
    ("more2", "r1_ms", X, 27.2, "crop=800:450:810:375", False),         # more of Microsoft
    ("than2", "card_gates", "card", 0, ("#0067B8", "BILL GATES"), False),
    ("and1", "r1_ap", X, 27.8, "crop=800:450:690:165", False),          # and more of Apple
    ("than3", "card_jobs", "card", 0, ("#0B0B0C", "STEVE JOBS"), False),  # than Steve Jobs ever did.
]

REST2 = [
    ("rest2", "r2_ticker", J, 0.0, "WSMONT_377_141", False),            # Back in the
    ("1980s", "r2_wolf", J, 0.0, "WOLFE_683_55", False),                # 1980s,
    ("larry1", "r2_finkpie", X, 18.0, None, False),                     # Larry Fink was a
    ("wall1", "r2_floor", J, 0.0, "CRASH_7650_125", False),             # Wall Street prodigy,
    ("but1", "r2_head", J, 0.0, "STO_229460_88", False),                # but one bad bet cost him
    ("100", "r2_bill", J, 0.0, "MONEY_95_134", False),                  # $100 million loss.
    ("that1", "r2_fired", J, 0.0, "FIRED_9693_161", False),             # That was enough to get him thrown out of
    ("wall2", "r2_nyse", J, 0.0, "WSMONT_380_112", False),              # Wall Street
    ("and2", "r2_think", D, 19.0, "fink_interview.mp4", False),         # and to convince him of one thing.
    ("wall3", "r2_plunge", J, 0.0, "CRASH_8850_111", False),            # Wall Street is terrible at seeing
    ("risk1", "r2_lehman", J, 0.0, "STO_124700_70", False),             # risk.
    ("so", "card_1988", "card", 0, ("red", "1988"), False),             # So, in 1988,
    ("he1", "r2_founders", X, 44.0, None, False),                       # he co-founded
    ("blackrock", "r2_brlogo", X, 64.5, None, False),                   # BlackRock
    ("built", "r2_dash", X, 58.5, None, False),                         # and built a system with one job
    ("calculating", "r2_lines", X, 54.5, None, False),                  # calculating risk.
    ("he_called", "r2_aladdin", X, 52.0, None, False),                  # He called it Aladdin.
    ("when", "r2_crash", J, 0.0, "CRASH_11250_89", False),              # When the 2008
    ("crisis1", "r2_cnbc", X, 134.5, None, False),                      # crisis hit,
    ("the_us", "r2_gov", X, 6.0, None, False),                          # the U.S. government called
    ("oneguy", "r2_stage", D, 4.3, "lf_interview2.mp4", True),          # the one guy Wall Street
    ("threw", "r2_fired2", J, 0.0, "FIRED_5500_122", False),            # threw out years ago
    ("clean", "r2_fed", X, 140.0, None, False),                         # to clean up the mess (WSJ: Fed hires BlackRock)
    ("larry2", "r2_cnbcfink", X, 168.0, None, False),                   # Larry Fink.
    ("he2", "r2_cash", J, 0.0, "STO_31075_137", False),                 # He came out of that crisis
    ("three", "r2_piles", J, 0.0, "MPILE_25_180", False),               # with three times the money.
    ("today", "r2_phone", X, 108.5, None, False),                       # Today, every time you buy
    ("sp", "r2_ishares", X, 96.0, None, False),                         # the S&P 500,
    ("your", "r2_puppet", X, 0.3, None, False),                         # your money ends up in
    ("this", "r2_hands", D, 53.6, "fink_interview.mp4", False),         # this guy's hands.
    ("a2", "r2_glass", X, 33.0, None, False),                           # A company that has never made
    ("single", "r2_brbldg", D, 10.48, "blackrock_short.mp4", True),     # a single product,
    ("but2", "r_logos", "clip", 0.0, None, False),                      # but everything you own,
    ("everything2", "r_touch3", "clip", 0.0, None, False),              # everything you touch,
    ("has", "r2_finkend", P, 1185.3, None, False),                      # has a piece of him in it.
]

# big words over the footage (League Gothic, the Nvidia reel's display type): (word key, text, until key or None)
HERO = [("15", "$15 TRILLION", "holds"), ("100", "$100 MILLION", "that1"), ("risk1", "RISK.", "so"),
        ("aladdin", "ALADDIN", "when"), ("2008", "2008", "crisis1"), ("three", "3X", "today")]

# the storyline captions (the Jensen reel's Helvetica caps): (text, start word key or rest-file seconds, end or None)
CAPS1 = [("A company", 0.09), ("that manages", 0.71), ("in assets", 3.04), ("holds more", 4.01), ("of Nvidia", 4.44),
         (None, 5.00), ("more of", 6.20), ("Microsoft", 6.57), (None, 7.24), ("and more of", 8.10), ("Apple", 8.82),
         (None, 9.10)]
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
