"""GTA 6 edit: the cut, as data (beats, captions, transitions, sound).  See gta6/SPEC.md.

Film times in seconds at 30 fps.  The voiceover (gta_Audio.mp3) starts at V0; F(v) maps a voiceover time to film time.
A beat is either footage (one clip, possibly several hard cuts joined: `segs`) or a built scene (`scene`).
"""
import json, os

ROOT = os.environ.get("GTA_ROOT", "/home/user/claude-test-2.0")
DRIVE = f"{ROOT}/gta6-src/_drive"
DIMON = f"{ROOT}/dimon-src"
PIN = f"{DIMON}/money_pinterest videos"
FPS = 30
V0 = 9.26                      # the voiceover's "That's" (V 0.11) lands 0.35 s after CJ's "again."
END = 110.0


def F(v):
    return round(v + V0, 3)


SRC = {k: f"{DRIVE}/{k}.mp4" for k in [
    "billion", "awshit", "millions", "launchps5", "netflix4k", "took13", "trailer1", "trailer2", "realwait", "waiting",
    "freedom", "kidcine", "vcpanzer", "vc10", "vcde", "gta5bye", "escape", "fastclip", "city", "klickpin", "edits",
    "metav3rse", "adultrush", "willnyc", "preload", "editm6", "montage", "montage2", "blade", "ahhshit", "editmontage"]}

# ---- beats: footage (segs = [(source, in, share)] joined by hard cuts) or a built scene
S = []


def shot(i, a, b, src, t, **o):
    S.append(dict(id=i, a=round(a, 3), b=round(b, 3), segs=[(src, t, None, o)]))


def cuts(i, a, b, segs):
    """segs: [(source, in, end-or-None, options)]; `end` is the film time this segment ends (None = the beat's end)."""
    S.append(dict(id=i, a=round(a, 3), b=round(b, 3), segs=segs))


def scene(i, a, b, kind, **o):
    S.append(dict(id=i, a=round(a, 3), b=round(b, 3), scene=kind, **o))


# A. cold open: the news, static, CJ
shot("s01", 0.00, 6.54, "billion", 0.00, grade="news")
scene("s02", 6.54, 6.74, "static")
shot("s03", 6.74, F(1.02), "awshit", 0.00, z=1.12, cy=0.40)               # its subtitles fall off the bottom
# B. the hook
cuts("s04", F(1.02), F(2.76), [("millions", 0.00, F(2.09), dict(cy=0.55)), ("realwait", 2.0, None, dict(cy=0.50))])
shot("s05", F(2.76), F(4.00), "city", 12.50, rot="ccw", grade="dark")      # on November 19th: the city at night
scene("s06", F(4.00), F(5.20), "logogrid", logo_at=F(4.40))               # the Tesla reel's tile wall + the VI card
cuts("s07", F(5.20), F(6.62), [("netflix4k", 760.0, F(5.90), {}), ("launchps5", 73.30, None, {})])
# C. the wait
shot("s08", F(6.62), F(8.51), "took13", 1.41, mode="card")
cuts("s09", F(8.51), F(10.31), [("trailer2", 75.20, F(8.78), {}), ("trailer2", 94.60, F(9.05), {}),
                                 ("preload", 10.80, F(9.68), {}), ("launchps5", 40.00, None, {})])   # + the $2,000,000,000 counter
shot("s10", F(10.31), F(11.14), "trailer1", 31.20)
shot("s11", F(11.14), F(12.43), "editm6", 3.95)                           # the fan edit: billboard, red car, flash
shot("s12", F(12.43), F(13.53), "trailer1", 85.00)                        # COMING 2025
shot("s13", F(13.53), F(14.91), "trailer2", 162.30)                       # MAY 26, 2026
shot("s14", F(14.91), F(16.58), "launchps5", 80.90)                       # NOVEMBER 19, 2026
# D. the question
cuts("s15", F(16.58), F(19.20), [("realwait", 11.80, F(17.50), dict(cy=0.50)), ("willnyc", 0.50, F(18.33), dict(cy=0.45)),
                                  ("edits", 2.40, None, dict(cy=0.30))])
scene("s16", F(19.20), F(20.38), "white")                                 # But why?
cuts("s17", F(20.38), F(21.97), [("waiting", 0.50, F(21.18), dict(cy=0.42)), ("waiting", 12.00, None, dict(cy=0.40))])
shot("s18", F(21.97), F(22.70), "realwait", 2.60, cy=0.50, grade="dark")  # + the 2013 -> 2026 year roller
cuts("s19", F(22.70), F(24.87), [("trailer1", 70.40, F(23.61), {}), ("montage", 4.70, F(24.38), {}), ("trailer2", 27.60, None, {})])
shot("s20", F(24.87), F(25.94), "launchps5", 46.35)                       # the Ocean Drive chase
# E. the answer
scene("s21", F(25.94), F(27.97), "wall")                                  # reel3's wall of faces: every GTA
shot("s22", F(27.97), F(28.27), "launchps5", 47.55)                       # cars
shot("s23", F(28.27), F(29.06), "launchps5", 72.10)                       # guns
cuts("s24", F(29.06), F(31.12), [("trailer1", 25.00, F(29.97), {}), ("montage", 20.20, F(30.49), {}), ("montage", 22.60, None, {})])
shot("s25", F(31.12), F(32.24), "freedom", 2.00)                          # Freedom.
# F. the kid
shot("s26", F(32.24), F(33.77), "kidcine", 0.50)
scene("s27", F(33.77), F(35.64), "crt")                                   # the family computer
shot("s28", F(35.64), F(36.40), "vc10", 21.00)                            # the Vice City logo
cuts("s29", F(36.40), F(38.16), [("vc10", 25.30, F(37.30), {}), ("vc10", 29.50, None, {})])   # + the volume bar
shot("s30", F(38.16), F(40.40), "vc10", 36.48)                            # the explosion lands on "gunshots"
scene("s31", F(40.40), F(44.52), "notebook")                              # ASPIRINE, PANZER
cuts("s32", F(44.52), F(46.74), [("gta5bye", 2.50, F(45.62), {}), ("gta5bye", 8.25, None, {})])
# G. the escape
cuts("s33", F(46.74), F(48.71), [("escape", 0.00, F(47.17), {}), ("ahhshit", 4.85, F(47.80), dict(z=1.18, cy=0.36)), ("escape", 0.90, None, {})])
cuts("s34", F(48.71), F(50.32), [("fastclip", 0.00, F(49.01), {}), ("montage", 20.00, None, {})])
scene("s35", F(50.32), F(53.16), "grid4")                                 # the adult dream, a tile a beat
cuts("s36", F(53.16), F(58.54), [("netflix4k", 520.0, F(53.86), {}), ("vcde", 14.10, F(54.56), {}),
                                  ("launchps5", 52.35, F(55.02), {}), ("launchps5", 60.25, F(55.49), {}),
                                  ("launchps5", 54.80, F(56.04), {}), ("trailer2", 142.00, F(56.58), {}),
                                  ("city", 8.00, None, dict(rot="ccw"))])
# H. the problem
cuts("s37", F(58.54), F(61.24), [("trailer2", 108.50, F(59.37), {}), ("launchps5", 70.25, F(59.94), {}),
                                  ("trailer2", 107.00, F(60.63), {}), ("launchps5", 29.00, None, {})])
cuts("s38", F(61.24), F(63.70), [("blade", 8.00, F(62.54), {}), ("launchps5", 60.25, F(63.10), {}), ("trailer2", 118.00, None, {})])
cuts("s39", F(63.70), F(65.03), [("trailer2", 75.20, F(64.50), {}), ("trailer1", 76.60, None, {})])
scene("s40", F(65.03), F(67.38), "split")                                 # real Miami | the game
shot("s41", F(67.38), F(69.07), "metav3rse", 0.30, band=True)
shot("s42", F(69.07), F(70.38), "gta5bye", 20.80)
# I. the opposite
shot("s43", F(70.38), F(72.70), "adultrush", 0.00)
cuts("s44", F(72.70), F(74.48), [("adultrush", 5.00, F(73.60), {}), ("adultrush", 6.10, None, {})])
cuts("s45", F(74.48), F(77.34), [("trailer1", 2.70, F(75.40), {}), ("blade", 25.70, F(76.39), {}), ("trailer1", 37.60, F(76.99), {}),
                                  ("trailer1", 21.80, None, {})])
# J. back to Vice City
shot("s46", F(77.34), F(78.89), "willnyc", 4.30, cy=1.0, z=1.58)
cuts("s47", F(78.89), F(81.04), [("trailer2", 4.30, F(79.42), {}), ("vcde", 7.80, None, {})])
cuts("s48", F(81.04), F(83.06), [("vc10", 23.40, F(81.74), {}), ("trailer1", 32.70, None, {})])
cuts("s49", F(83.06), F(86.62), [("metav3rse", 17.98, F(84.95), dict(band=True)), ("metav3rse", 19.87, None, dict(band=True))])
# K. slow: the way home
shot("s50", F(86.62), F(88.42), "trailer2", 153.00)
shot("s51", F(88.42), F(89.42), "netflix4k", 522.0)
cuts("s52", F(89.42), F(91.82), [("kidcine", 3.00, F(90.62), {}), ("vcde", 26.50, None, {})])
shot("s53", F(91.82), F(93.10), "kidcine", 8.30)
shot("s54", F(93.10), F(94.77), "waiting", 31.50, cy=0.45)
shot("s55", F(94.77), F(96.22), "freedom", 4.00)
cuts("s56", F(96.22), END, [("launchps5", 76.00, 108.00, {}), ("launchps5", 81.20, None, {})])

# ---- scene media: stills and the clips the built scenes use
STILLS = {   # name: (source, time)  -> assets/img/<name>.jpg (960 wide)
    "vilogo": ("launchps5", 23.20), "tank": ("vc10", 62.25),
    # the tile wall behind the VI card (reel1 6.2 s)
    **{f"g{i:02d}": s for i, s in enumerate([
        ("trailer1", 12.0), ("trailer1", 19.5), ("trailer1", 22.5), ("trailer1", 31.5), ("trailer1", 36.5), ("trailer1", 40.5),
        ("trailer2", 7.0), ("trailer2", 12.5), ("trailer2", 33.5), ("trailer2", 63.0), ("trailer2", 81.0), ("trailer2", 95.5),
        ("trailer2", 100.5), ("trailer2", 125.0), ("trailer2", 140.5), ("trailer2", 150.0), ("launchps5", 3.0), ("launchps5", 7.5),
        ("launchps5", 19.0), ("launchps5", 26.5), ("launchps5", 33.5), ("launchps5", 41.0), ("launchps5", 55.0), ("launchps5", 67.0)])},
    # the wall of every GTA (reel3 0-3 s): Tommy, CJ, the V trio, Jason and Lucia
    **{f"w{i:02d}": s for i, s in enumerate([
        ("vcde", 8.6), ("awshit", 1.5), ("metav3rse", 15.0), ("trailer2", 64.5), ("vc10", 35.0), ("trailer2", 12.0),
        ("vcde", 43.0), ("metav3rse", 18.5), ("trailer1", 9.8), ("vc10", 40.0), ("launchps5", 12.0), ("vcde", 27.5),
        ("trailer2", 54.0), ("metav3rse", 6.0), ("vc10", 63.6), ("trailer1", 63.0), ("vcde", 19.0), ("launchps5", 26.0),
        ("awshit", 5.5), ("trailer2", 116.5), ("vcde", 50.0), ("launchps5", 21.5), ("vc10", 8.5), ("trailer2", 89.0)])},
}
LAYERS = [   # clips used inside built scenes (cut by prep to w x h)
    dict(id="l_crt", src="vcpanzer", t=20.0, a=F(33.77), b=F(35.64), w=960, h=720),
    dict(id="l_spl", src="edits", t=6.0, a=F(65.03), b=F(67.38), w=960, h=1080, cy=0.42),
    dict(id="l_spr", src="city", t=12.0, a=F(65.03), b=F(67.38), w=960, h=1080, rot="ccw"),
    dict(id="l_g1", src="trailer2", t=94.6, a=F(50.32), b=F(53.16), w=960, h=540),    # the gold dress
    dict(id="l_g2", src="preload", t=10.6, a=F(50.32), b=F(53.16), w=960, h=540),     # the yacht at speed
    dict(id="l_g3", src="launchps5", t=39.9, a=F(50.32), b=F(53.16), w=960, h=540),   # the red sports car
    dict(id="l_g4", src="trailer2", t=126.0, a=F(50.32), b=F(53.16), w=960, h=540),   # the speedo dancer on Ocean Drive
]

# ---- words: voiceover (whisper word starts), the news line, CJ
def _load_vo():
    d = json.load(open(f"{ROOT}/gta6-work/vo/words.json"))
    return [(s["text"].strip(), s["offsets"]["from"] / 1000) for s in d["transcription"] if s["text"].strip()]


VO = _load_vo()
NEWS = [("A", 0.04), ("video", 0.12), ("game", 0.59), ("so", 0.98), ("popular", 1.18), ("it", 1.87), ("could", 2.08),
        ("cost", 2.56), ("the", 3.00), ("U.S.", 3.20), ("economy", 3.39), ("a", 4.08), ("billion", 4.17), ("dollars", 4.80),
        ("in", 5.44), ("just", 5.62), ("one", 5.84), ("day.", 6.20)]
CJ = [("Ah", 0.13), ("shit,", 0.40), ("here", 1.11), ("we", 1.54), ("go", 1.77), ("again.", 1.96)]
CJ0 = 6.74


def words(clock, a, b):
    if clock == "vo":
        return [(w, F(t)) for w, t in VO if a - 0.005 <= t < b - 0.005]
    if clock == "news":
        return [(w, t) for w, t in NEWS if a <= t < b]
    return [(w, round(CJ0 + t, 3)) for w, t in CJ if a <= t < b]


# ---- captions. text tokens match the spoken words in order; "|" breaks the line.
#  marks: * italic.  entrance (default = the Dimon serif: a glowing square, then the word blooms in):
#  ! hero burst   ^ year (hero + the 1998 square inversion on its first two characters)   # highlight bar
#  ~ light streaks (Tesla reel)   = Dario's square then dim-to-full   % the Tesla weight flash
#  word@size sets a size.
C = []


def cap(gid, clock, a, b, text, size=64, pos=(960, 840), end=None, layout="line", drift=30, ink="light",
        indent=0.22, l2=None, scrim=0.0):
    ws = words(clock, a, b)
    toks = [t for t in text.split() if t != "|"]
    assert len(toks) == len(ws), (gid, toks, ws)
    C.append(dict(id=gid, text=text, words=ws, size=size, pos=pos, end=end, layout=layout, drift=drift, ink=ink,
                  indent=indent, l2=l2, scrim=scrim))


COUNTERS = [   # (id, start, land, values, x, y, size, end): a number rolling in place, fast then landing (Dario's 2023)
    ("cn1", 4.17, 4.80, ["$3", "$48", "$910", "$7,204", "$63,815", "$512,077", "$4,180,336", "$29,904,512", "$163,027,880",
                         "$388,450,101", "$604,912,377", "$792,330,846", "$918,004,219", "$973,551,602", "$996,120,450",
                         "$999,870,331", "$1,000,000,000"], 960, 545, 150, 5.40),
    ("cn2", F(8.78), F(9.40), ["$7", "$5,312", "$880,410", "$63,190,442", "$400,915,027", "$1,088,402,736", "$1,634,190,553",
                               "$1,902,447,018", "$1,977,031,264", "$1,996,880,412", "$2,000,000,000"], 960, 545, 150, F(10.31)),
    ("cn3", F(21.97), F(22.37), ["2013", "2015", "2017", "2019", "2021", "2023", "2024", "2025", "2026"], 900, 520, 170, F(22.70)),
]

# A. the cold open (crazy type)
cap("n1", "news", 0.0, 1.87, "A video game | so *!popular@118", size=74, pos=(960, 470), end=1.87, layout="stack", scrim=0.35)
cap("n2", "news", 1.87, 4.08, "it could cost | the !U.S. %economy", size=74, pos=(930, 480), end=4.08, layout="stack",
    l2=104, scrim=0.35)
cap("n3", "news", 4.08, 4.17, "a", size=74, pos=(600, 400), end=5.40, drift=24)          # + the counter, then "dollars"
cap("n3b", "news", 4.80, 5.40, "dollars", size=74, pos=(1320, 680), end=5.40, drift=24)
cap("n4", "news", 5.40, 6.54, "in just | one #day.@156", size=74, pos=(960, 480), end=6.54, layout="stack", l2=156,
    scrim=0.35)
cap("c1", "cj", 0.0, 1.0, "*Ah *shit,", size=96, pos=(560, 500), end=F(0.0), drift=18)
cap("c2", "cj", 1.0, 2.4, "*here *we *go *again.", size=96, pos=(1390, 600), end=F(0.0), drift=18)
cap("h1", "vo", 0.0, 1.02, "That's exactly how", pos=(960, 860), end=F(1.02))
cap("h2", "vo", 1.02, 2.76, "!millions@132 | of adults are going to feel", size=64, pos=(960, 520), end=F(2.76),
    layout="stack", indent=0.05)
cap("h3", "vo", 2.76, 4.00, "on November | ^19th@150", size=96, pos=(960, 520), end=F(4.00), layout="stack", scrim=0.35)
cap("h4", "vo", 4.00, 5.20, "when they play GTA 6", pos=(960, 900), end=F(5.20), scrim=0.5)
cap("h5", "vo", 5.20, 6.62, "for the first %time.", size=96, pos=(960, 520), end=F(6.62))
# C. the wait
cap("b1", "vo", 6.62, 7.52, "GTA 6 took", size=96, pos=(470, 540), end=F(8.51), drift=16)
cap("b2", "vo", 7.52, 8.51, "^13@132 years", size=96, pos=(1460, 540), end=F(8.51), drift=16)
cap("b3", "vo", 8.51, 8.78, "and", size=72, pos=(640, 400), end=F(10.31), drift=20)        # + the $2,000,000,000 counter
cap("b3b", "vo", 9.68, 10.31, "%dollars", size=96, pos=(1280, 690), end=F(10.31), drift=20)
cap("b4", "vo", 10.31, 11.14, "to make.", size=96, pos=(960, 540), end=F(11.14))
cap("b5", "vo", 11.14, 13.53, "The release got pushed from ^2025", pos=(960, 120), end=F(13.53), scrim=0.4)
cap("b6", "vo", 13.53, 14.91, "to May ^2026,", pos=(960, 120), end=F(14.91))
cap("b7", "vo", 14.91, 16.58, "and then again to #November.", pos=(960, 120), end=F(16.58), scrim=0.4)
cap("b8", "vo", 16.58, 19.20, "And yet, | *nobody seems to have moved on.", size=64, pos=(960, 300), end=F(19.20),
    layout="stack", scrim=0.45)
cap("b9", "vo", 19.20, 20.38, "But !why?", size=118, pos=(960, 540), end=F(20.38), ink="dark", drift=24)
cap("b10", "vo", 20.38, 21.97, "Why are grown adults waiting", pos=(960, 880), end=F(21.97))
cap("b11", "vo", 22.37, 22.70, "years", size=96, pos=(1180, 650), end=F(22.70), drift=0)   # + the 2013 -> 2026 roller
cap("b12", "vo", 22.70, 24.87, "for a game that's *supposedly just about", pos=(960, 880), end=F(24.87))
cap("b13", "vo", 24.87, 25.94, "%stealing cars?", size=96, pos=(960, 540), end=F(25.94))
cap("b14", "vo", 25.94, 27.97, "Because GTA was | *never just about", size=96, pos=(960, 520), end=F(27.97),
    layout="stack", drift=0, scrim=0.55)
cap("b15", "vo", 27.97, 28.27, "!cars", size=132, pos=(960, 540), end=F(28.27), drift=0)
cap("b16", "vo", 28.27, 29.06, "and !guns.@132", size=96, pos=(960, 540), end=F(29.06))
cap("b17", "vo", 29.06, 31.12, "It was about what it really gave you.", pos=(960, 880), end=F(31.12))
cap("b18", "vo", 31.12, 32.24, "!Freedom.", size=132, pos=(960, 540), end=F(32.24), drift=14)
# F. the kid
cap("k1", "vo", 32.24, 33.77, "Back to being | ^10 years old,", size=64, pos=(960, 500), end=F(33.77), layout="stack", l2=96)
cap("k2", "vo", 33.77, 35.64, "sitting in front of | the *family *computer,", size=64, pos=(960, 935), end=F(35.64),
    layout="stack", l2=84)
cap("k3", "vo", 35.64, 36.40, "playing !Vice !City", size=96, pos=(960, 880), end=F(36.40))
cap("k4", "vo", 36.40, 38.16, "with the volume turned all the way down", pos=(960, 880), end=F(38.16))
cap("k5", "vo", 38.16, 40.40, "so nobody could hear | the *gunshots.", size=64, pos=(960, 800), end=F(40.40),
    layout="stack", l2=96)
cap("k6", "vo", 40.40, 41.44, "With cheat codes like", pos=(960, 150), end=F(42.00), ink="dark", drift=10)
cap("k7", "vo", 42.35, 44.52, "scribbled at the back | of your notebook.", pos=(960, 920), end=F(44.52), ink="dark",
    layout="stack", drift=10)
cap("k8", "vo", 44.52, 46.74, "For a kid, | it wasn't just a *game.", size=64, pos=(960, 860), end=F(46.74),
    layout="stack", l2=84)
cap("k9", "vo", 46.74, 48.71, "It was a psychological | ~*escape,", size=64, pos=(960, 520), end=F(48.71), layout="stack",
    l2=118, scrim=0.6)
cap("k10", "vo", 48.71, 50.32, "an alternate %reality.", size=96, pos=(960, 540), end=F(50.32))
cap("k11", "vo", 50.32, 53.16, "It was everything you imagined | *adulthood would be.", size=64, pos=(960, 540),
    end=F(53.16), layout="stack", l2=96, scrim=0.6, drift=0)
cap("k12", "vo", 53.16, 54.56, "Driving %supercars,", size=96, pos=(960, 540), end=F(54.56))
cap("k13", "vo", 54.56, 55.49, "firing %guns,", size=96, pos=(960, 540), end=F(55.49))
cap("k14", "vo", 55.49, 56.58, "flying %planes,", size=96, pos=(960, 540), end=F(56.58))
cap("k15", "vo", 56.58, 58.54, "and owning | an *entire !city.@132", size=64, pos=(960, 520), end=F(58.54),
    layout="stack", l2=96)
# H. the problem
cap("p1", "vo", 58.54, 61.24, "And while every other game asks you | to be the *hero,", size=64, pos=(960, 820),
    end=F(61.24), layout="stack", l2=96)
cap("p2", "vo", 61.24, 63.70, "but GTA lets you be | the #problem.@132", size=64, pos=(960, 520), end=F(63.70),
    layout="stack", l2=96)
cap("p3", "vo", 63.70, 65.03, "It lets you be | the !bad !guy", size=64, pos=(960, 520), end=F(65.03), layout="stack", l2=96)
cap("p4", "vo", 65.03, 67.38, "in a world that looks | just like *yours.", size=64, pos=(960, 540), end=F(67.38),
    layout="stack", drift=0, l2=96, scrim=0.4)
cap("p5", "vo", 67.38, 69.07, "And somewhere along the way,", pos=(960, 300), end=F(69.07))
cap("p6", "vo", 69.07, 70.38, "those kids | *grew *up.", size=64, pos=(960, 820), end=F(70.38), layout="stack", l2=118)
cap("p7", "vo", 70.38, 72.70, "Today, | it's the exact *opposite.", size=64, pos=(960, 520), end=F(72.70), layout="stack", l2=96)
cap("p8", "vo", 72.70, 74.48, "It's an escape from | ~*adulthood,", size=64, pos=(960, 520), end=F(74.48), layout="stack",
    l2=118)
cap("p9", "vo", 74.48, 77.34, "back to the world | they once dreamed of living in.", size=64, pos=(960, 820),
    end=F(77.34), layout="stack", l2=84)
# J. back to Vice City
cap("v1", "vo", 77.34, 78.89, "And on | #November ^19th,", size=64, pos=(960, 260), end=F(78.89), layout="stack", l2=96)
cap("v2", "vo", 78.89, 81.04, "Rockstar takes you back to | !Vice !City,", size=64, pos=(960, 840), end=F(81.04),
    layout="stack", l2=132)
cap("v3", "vo", 81.04, 83.06, "the city where | it all *started.", size=64, pos=(960, 840), end=F(83.06), layout="stack", l2=96)
cap("v4", "vo", 83.06, 85.63, "So if you're still lost in | *Los *Santos this week,", size=64, pos=(960, 840),
    end=F(85.63), layout="stack", l2=84)
cap("v5", "vo", 85.63, 86.62, "=don't =rush.", size=96, pos=(960, 540), end=F(86.62), drift=12)
cap("v6", "vo", 86.62, 88.42, "=Take =the =long =way =home.", size=96, pos=(960, 540), end=F(88.42), drift=16)
cap("v7", "vo", 88.42, 89.42, "=Drive =slow.", size=96, pos=(960, 540), end=F(89.42), drift=12)
cap("v8", "vo", 89.42, 91.82, "because that 10-year-old | playing GTA Vice City", size=64, pos=(960, 820), end=F(91.82),
    layout="stack", l2=84)
cap("v9", "vo", 91.82, 93.10, "never really *left.", size=96, pos=(960, 540), end=F(93.10), drift=12)
cap("v10", "vo", 93.10, 94.77, "He's just been waiting | ^13 years", size=64, pos=(960, 820), end=F(94.77),
    layout="stack", l2=96)
cap("v11", "vo", 94.77, 96.30, "to feel that | *!freedom@132 again.", size=64, pos=(960, 520), end=F(96.22),
    layout="stack", drift=14, l2=96)

# ---- transitions and accents (film time)
FX = [
    ("flash", 4.80, 2), ("flash", 6.74, 1), ("flash", F(1.02), 1), ("flash", F(2.09), 1),
    ("wipe", F(2.76)), ("flash", F(4.40), 2), ("flash", F(5.90), 1), ("bloomcut", F(6.62)), ("flash", F(8.51), 2),
    ("flash", F(9.41), 1), ("strike", F(13.22), 650, 1270, 950), ("strike", F(14.62), 650, 1270, 906),
    ("flash", F(17.50), 1), ("flash", F(18.33), 1), ("neg", F(19.20), 1), ("neg", F(19.59), 1),
    ("flash", F(21.97), 1), ("flash", F(23.80), 1), ("whip", F(25.94)), ("flash", F(27.97), 1), ("flash", F(28.27), 1),
    ("flash", F(30.10), 1), ("bloomcut", F(31.12)), ("wipe", F(32.24)), ("static", F(35.64) - 0.10, 4),
    ("flash", F(39.78), 1), ("flash", F(39.98), 1), ("whip", F(40.40)), ("flash", F(45.62), 1),
    ("bloomcut", F(46.74)), ("flash", F(48.21), 1), ("flash", F(48.71), 1), ("wipe", F(50.32)),
    ("flash", F(53.86), 1), ("flash", F(54.56), 1), ("flash", F(55.49), 1), ("flash", F(56.58), 1),
    ("flash", F(59.89), 1), ("static", F(62.54) - 0.07, 3), ("neg", F(63.70), 1), ("flash", F(64.35), 1),
    ("wipe", F(65.03)), ("whip", F(70.38)), ("flash", F(73.60), 1), ("wipe", F(74.48)),
    ("flash", F(78.89), 1), ("double", F(81.74)), ("bloomcut", F(94.77)), ("fadeout", END - 0.8, END),
]
SFX = [
    ("impact-bass-1", 4.80, 0.55), ("glitch-1", 6.52, 0.45), ("whoosh-short", F(2.70), 0.40),
    ("impact-bass-2", F(4.40), 0.40), ("whoosh-cinematic", F(6.50), 0.40), ("impact-bass-2", F(8.51), 0.50),
    ("click", F(19.20), 0.40), ("whoosh-short", F(25.88), 0.40), ("impact-bass-1", F(31.12), 0.55),
    ("whoosh", F(32.18), 0.35), ("glitch-3", F(35.54), 0.40), ("whoosh-short", F(40.34), 0.40),
    ("whoosh-cinematic", F(46.62), 0.40), ("whoosh", F(50.26), 0.35), ("glitch-2", F(62.47), 0.45),
    ("whoosh-short", F(64.97), 0.40), ("whoosh-short", F(70.32), 0.40), ("whoosh", F(74.42), 0.35),
    ("impact-bass-2", F(94.77), 0.45),
]
