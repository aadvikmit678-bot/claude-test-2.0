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
    ("15", "r1_ft", X, 14.2, None, False),                                # $15 trillion (FT: "$15.5tn")
    ("assets", "r1_glass", N, 4.24, ("asher.mp4", ASH), True),            # in assets (the BlackRock glass tower)
    # the founders block (the user's notes): Think School's "Founders vs Blackrock" graphic, one company at a time,
    # centred; each founder in the Nvidia reel's opening treatment (Jensen: the reel's own clip). FX = pre-rendered.
    ("holds", "tsg_nv", FX, 0, None, False),                              # holds more of Nvidia than
    ("jensen", "r1_jensen", FX, 0, None, False),                          # Jensen Huang,
    ("more2", "tsg_ms", FX, 0, None, False),                              # more of Microsoft than
    ("bill", "r1_gates", FX, 0, None, False),                             # Bill Gates,
    ("and1", "tsg_ap", FX, 0, None, False),                               # and more of Apple than
    ("steve", "r1_jobs", FX, 0, None, False),                             # Steve Jobs ever did.
]

REST2 = [
    ("rest2", "r2_ticker", J, 0.0, "WSMONT_377_141", False),            # Back in the
    ("1980s", "r2_wolf", J, 0.0, "WOLFE_683_55", False),                # 1980s,
    ("larry1", "r2_finkpie", X, 18.0, None, False),                     # Larry Fink was a
    ("wall1", "r2_bull", N, 2.535, ("axirohq.mp4", None), True),        # Wall (the Charging Bull)
    ("street1", "r2_nysefloor", N, 4.34, ("axirohq.mp4", None), True),  # Street (the NYSE floor)
    ("prodigy", "r2_floor", J, 0.0, "CRASH_7650_125", False),           # prodigy,
    # "But one bad bet cost him a $100 million loss. That was enough to get him thrown out of Wall Street." -- the
    # Higgsfield scene: the user's ChatGPT keyframes animated with Kling 3.0 Pro (FX = pre-rendered by r_bet)
    ("but1", "bet1", FX, 0, None, False),                               # But one bad bet cost him (green -> red)
    ("100", "bet2", FX, 0, None, False),                                # $100 million loss. (the red screens)
    ("that1", "bet3", FX, 0, None, False),                              # That was enough ... thrown out of Wall Street
    ("and2", "r2_think", D, 19.0, "fink_interview.mp4", False),         # and to convince him of one thing.
    ("wall3", "r2_plunge", J, 0.0, "CRASH_8850_111", False),            # Wall Street is terrible at seeing
    ("risk1", "r2_lehman", J, 0.0, "STO_124700_70", False),             # risk.
    ("so", "card_1988", "card", 0, ("red", "1988"), False),             # So, in 1988,
    ("he1", "r2_towerbase", N, 20.30, ("bazzarbyte.mp4", band(820)), True),  # he co-founded (a glass tower)
    ("blackrock", "r2_brlogo", X, 64.5, None, False),                   # BlackRock
    ("built", "r2_screens", N, 7.75, ("asher.mp4", ASH), True),         # and built (BlackRock's own screens)
    ("system", "r2_datacenter", N, 59.42, ("bazzarbyte.mp4", band(1000)), True),  # a system with one
    ("job", "r2_ring", N, 60.45, ("bazzarbyte.mp4", band(760)), True),  # job --
    ("calculating", "r2_lines", X, 54.5, None, False),                  # calculating risk.
    ("he_called", "r2_aladdin", X, 52.0, None, False),                  # He called it Aladdin.
    ("when", "r2_crash", J, 0.0, "CRASH_11250_89", False),              # When the 2008
    ("crisis1", "r2_cnbc", X, 134.5, None, False),                      # crisis hit,
    ("the_us", "r2_capitol", N, 8.67, ("axirohq.mp4", None), True),     # the U.S. (the Capitol)
    ("government", "r2_gov", X, 6.0, None, False),                      # government called
    ("oneguy", "r2_stage", D, 4.3, "lf_interview2.mp4", True),          # the one guy Wall Street
    ("threw", "bet3fb", FX, 0, None, False),                            # threw out years ago (the walk-out again, grey)
    ("clean", "r2_fed", X, 140.0, None, False),                         # to clean up the mess (WSJ: Fed hires BlackRock)
    ("larry2", "r2_cnbcfink", X, 168.0, None, False),                   # Larry Fink.
    ("he2", "r2_cash", J, 0.12, "STO_31075_137", False),                 # He came out of that crisis
    ("three", "r2_towerup", N, 22.70, ("bazzarbyte.mp4", band(420)), True),  # with three times (the tower)
    ("money1", "r2_piles", J, 0.0, "MPILE_200_119", False),            # the money. (stacks of $100 bills)
    ("today", "r2_phone", X, 108.5, None, False),                       # Today, every time you buy
    ("sp", "r2_sp", N, 22.45, ("conspirant.mp4", band(0)), True),       # the S&P 500 (its logo wall)
    ("your", "r2_network", N, 26.80, ("conspirant.mp4", band(590)), True),  # your money ends up in (the web)
    ("this", "r2_hands", D, 53.6, "fink_interview.mp4", False),         # this guy's hands.
    # "A company that has never made a single product, but everything you own, everything you touch," -- the user's
    # video for the last part (products, falling figures); cropped below its "@YS_MR4" watermark (y 50-75) and above
    # its bottom bar; then Fink on "has a piece of him"
    ("a2", "r2_ending", E, 0.40, "crop=566:318:85:80", False),
    ("has", "r2_finkend", P, 1185.3, None, False),                      # has a piece of him in it.
]

# big words over the footage (League Gothic, the Nvidia reel's display type): (word key, text, until key or None)
HERO = [("15", "$15 TRILLION", "holds"), ("100", "$100 MILLION", "that1"), ("risk1", "RISK.", "so"),
        ("2008", "2008", "crisis1"), ("three", "3X", "today")]   # no ALADDIN: the shot carries its own title

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
