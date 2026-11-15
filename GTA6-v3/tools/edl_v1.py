"""GTA 6 edit: the edit decision list. Every time is on the final timeline (seconds).

The voiceover is placed at VO_OFFSET; W(i) is the onset of VO word i (words.json), cut(i) the picture cut
two frames ahead of it. News and CJ words come from their own transcripts.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../GTA 6 edit
PROJ = os.path.join(ROOT, "gta6-edit")
FPS = 30
VO_OFFSET = 7.34
NEWS_IN, NEWS_DUR = 0.55, 4.87          # the reporter's line: news.mp4 0.55 -> 5.42
CJ_IN, CJ_DUR = 0.0, 2.47               # "Ah shit, here we go again."
TOTAL = 106.5

_W = json.load(open(os.path.join(PROJ, "words.json"), encoding="utf-8"))
_N = json.load(open(os.path.join(PROJ, "words_news.json"), encoding="utf-8"))
_C = json.load(open(os.path.join(PROJ, "words_cj.json"), encoding="utf-8"))


def W(i):  return round(_W[i]["start"] + VO_OFFSET, 3)
def WE(i): return round(_W[i]["end"] + VO_OFFSET, 3)
def WT(i): return _W[i]["text"]
def cut(i): return round(W(i) - 0.06, 3)
def N(i):  return round(_N[i]["start"] - NEWS_IN, 3)
def NE(i): return round(_N[i]["end"] - NEWS_IN, 3)
def C(i):  return round(_C[i]["start"] + NEWS_DUR, 3)


SRC = {  # alias -> file under ROOT
    "news": "_dl/news/news.mp4",
    "awshit": "Aw shit, here we go again (Original) Grand Theft Auto San Andreas.mp4",
    "t1": "Grand Theft Auto VI Trailer 1.mp4",
    "t2": "Grand Theft Auto VI Trailer 2.mp4",
    "launch": "Grand Theft Auto VI Launch Trailer (1).mp4",          # 4K
    "nlook": "Grand Theft Auto VI An Extended Look   Now Playing   Netflix.mp4",   # 4K
    "preload": "Grand Theft Auto VI Pre-Load Now.mp4",
    "next": "GTA 6 4K Gameplay Trailer FULL NETFLIX EXTENDED.mp4",  # 4K
    "vc10": "Grand Theft Auto Vice City 10th Anniversary Edition Trailer [0-72.7s].mp4",
    "vcde": "How the Vice City Definitive Edition should have looked [0-72.7s].mp4",
    "panzer": "The Rhino Tank - Steal it like a Man - Keep it Forever GTA VC [0-149.2s].mp4",
    "kidlake": "Pinterest video #1125829606870167260 [0-17.4s].mp4",
    "millions": "Men in black [0-8s].mp4",
    "freedom": "From Klickpin.com- Need fresh inspiration Refresh these simple healthy habit ideas perfect for saving sharing and recreating later designed to fee.mp4",
    "escape": "From Klickpin.com- Polished nail design inspiration that look expensive while staying practical realistic and beginner friendly for busy people wh (1).mp4",
    "adult": "From Klickpin.com- Polished nail design inspiration that look expensive while staying practical realistic and beginner friendly for busy people wh.mp4",
    "goodbye": "Video by shamsycreates [0-22s].mp4",
    "waitgta6": "Video by lucanox.2 [0-34.05s].mp4",
    "wait5": "Video by saudalhomud [0-16.96s].mp4",
    "nostalgia": "Video by bykeipker [0-37.3s].mp4",
    "nyc": "Video by will__nyc [0-15s].mp4",
    "vox": "Video by kiuzr [0-15s].mp4",
    "eyes": "Video by ntprimee [0-20s].mp4",
    "city": "Video by __lio.x__ [0-83.9s].mp4",
    "money10": "../../../../Downloads/jpm-dimon-v17-project/jpm-dimon/assets/clips2/MONEY_100_52.mp4",
    "kidA": "../../../../flow-mcp-out/GTA6_kid_computer/KID_A.mp4",    # Flow, pending approval
    "kidB": "../../../../flow-mcp-out/GTA6_kid_computer/KID_B.mp4",
}

# ---------------------------------------------------------------------------------------------------
# Shots.  fit: cover | blurfill (vertical/square source centred on a blurred copy) | card (native aspect)
# crop = (x, y, w, h) in source pixels, applied before scaling.  grade: none | bw | dim | warm | cool
# speed < 1 is slow motion.  Each shot is cut to assets/clips/<id>.mp4 by tools/prep.py.
# ---------------------------------------------------------------------------------------------------
def S(id, src, sin, start, end, fit="cover", crop=None, grade="none", speed=1.0, reverse=False, card=None, push=None, z=None):
    return dict(id=id, src=src, sin=sin, start=round(start, 3), end=round(end, 3), fit=fit, crop=crop,
                grade=grade, speed=speed, reverse=reverse, card=card, push=push, z=z)


SHOTS = [
    # ---- cold open: the FOX 2 line, a flash, CJ ----
    S("news", "news", NEWS_IN, 0.0, NEWS_DUR, crop=(0, 0, 1280, 720)),
    S("cj", "awshit", CJ_IN, NEWS_DUR, VO_OFFSET, crop=(107, 0, 1707, 960)),
    # ---- A: That's exactly how millions of adults are going to feel on November 19th ... ----
    S("a1a", "wait5", 1.60, VO_OFFSET, cut(3), fit="card", card=(560, 996)),
    S("a1b", "wait5", 2.15, VO_OFFSET + 0.30, cut(3), fit="card", card=(560, 996)),
    S("a1c", "wait5", 4.45, VO_OFFSET + 0.62, cut(3), fit="card", card=(560, 996)),
    S("a2", "millions", 0.40, cut(3), cut(6), crop=(0, 187, 720, 405), grade="bw", push=(1.0, 1.07)),
    S("a3", "wait5", 8.05, cut(6), cut(11), fit="blurfill"),
    S("a4", "next", 1573.0, cut(11), cut(13), grade="dim", push=(1.04, 1.12)),
    S("a5", "preload", 6.44, cut(13), cut(18)),
    S("a6", "nlook", 16.6, cut(18), cut(22), push=(1.0, 1.05)),
    # ---- B: GTA 6 took 13 years and 2 billion dollars to make ----
    S("b1", "t1", 2.85, cut(22), cut(25), push=(1.0, 1.06)),
    S("b2", "t1", 35.85, cut(25), cut(27), grade="dim", push=(1.08, 1.0)),
    S("b3", "t2", 33.30, cut(27), cut(30)),
    S("b4", "money10", 0.2, cut(30), cut(31), push=(1.0, 1.1)),
    S("b5", "t1", 30.1, cut(31), cut(33)),
    # ---- C: pushed from 2025 to May 2026, and then again to November ----
    S("c1", "t1", 85.8, cut(33), cut(39), push=None),
    S("c2", "t1", 85.8, cut(39), cut(45), grade="dim"),
    S("c3", "next", 1597.2, cut(45), cut(47) - 0.0),
    # ---- D: And yet, nobody seems to have moved on ----
    S("d1", "nyc", 0.3, cut(47), cut(51), crop=(0, 1180, 1440, 810)),
    S("d2", "waitgta6", 7.2, cut(51), cut(55), crop=(0, 700, 1440, 810)),
    # ---- E: But why? ----
    S("e1", "eyes", 3.62, cut(55), cut(56) + 0.10),
    S("e2", "eyes", 4.42, cut(56) + 0.10, cut(57)),
    # ---- F: Why are grown adults waiting 13 years ... stealing cars? ----
    S("f1", "wait5", 11.2, cut(57), cut(64), fit="card", card=(560, 996)),
    S("f2", "wait5", 13.6, cut(61), cut(64), fit="card", card=(560, 996)),
    S("f3", "vox", 0.05, cut(64), cut(67)),
    S("f3b", "vox", 3.3, cut(67), cut(69)),
    S("f4", "t2", 9.9, cut(69), cut(71)),
    S("f4b", "next", 492.5, cut(71), cut(73)),
    # ---- G: Because GTA was never just about cars and guns ----
    S("g1", "t1", 70.4, cut(73), cut(75)),
    S("g1b", "t2", 34.7, cut(75), cut(79)),
    S("g2", "t1", 32.7, cut(79), cut(81)),
    S("g3", "launch", 72.15, cut(81), cut(82)),
    # ---- H: It was about what it really gave you. Freedom. ----
    S("h1", "t1", 19.3, cut(82), cut(86), push=(1.0, 1.05)),
    S("h1b", "t1", 5.05, cut(86), cut(90), push=(1.0, 1.05)),
    S("h2", "freedom", 0.3, cut(90), cut(91) + 0.12, push=(1.0, 1.04)),
    # ---- I: Back to being 10 years old ... so nobody could hear the gunshots ----
    S("i0", "freedom", 0.3, cut(91) + 0.12, cut(94), reverse=True, speed=3.0, grade="dim"),
    S("i1", "goodbye", 0.25, cut(94), cut(97), crop=(0, 135, 1440, 810)),      # stand-in until the Flow kid shot is approved
    S("i3", "vc10", 23.5, cut(97), cut(101) + 0.10, fit="card", card=(1280, 960), crop=(293, 100, 693, 512)),
    S("i3b", "vc10", 16.65, cut(101) + 0.10, cut(109), fit="card", card=(1280, 960), crop=(293, 100, 693, 512)),
    S("i4", "vc10", 25.2, cut(109), cut(115), fit="card", card=(1280, 960), crop=(293, 100, 693, 512)),
    S("i5", "vc10", 36.9, cut(115), cut(119), grade="dim"),
    S("i5b", "vcde", 37.75, cut(119), cut(121), grade="dim"),
    # ---- J: cheat codes ----
    S("j2", "panzer", 100.0, cut(127), cut(128)),
    # ---- K: For a kid, it wasn't just a game. A psychological escape, an alternate reality ----
    S("k1", "kidlake", 0.5, cut(135), cut(138)),
    S("k1b", "panzer", 30.0, cut(138), cut(143)),
    S("k2", "escape", 0.65, cut(143), cut(147)),
    S("k2b", "escape", 2.75, cut(147), cut(148)),
    S("k3a", "escape", 7.35, cut(148), cut(149) + 0.3),
    S("k3b", "escape", 8.45, cut(149) + 0.3, cut(151)),
    # ---- L: everything you imagined adulthood would be ... owning an entire city ----
    S("l1", "t1", 37.6, cut(151), cut(155)),
    S("l2", "launch", 66.5, cut(155), cut(158)),
    S("l3", "vcde", 52.7, cut(158), cut(159)),
    S("l4", "launch", 25.8, cut(159), cut(161)),
    S("l5", "t1", 76.8, cut(161), cut(163)),
    S("l6", "t2", 142.0, cut(163), cut(165)),
    S("l7", "next", 1129.0, cut(165), cut(168), push=(1.0, 1.06)),
    S("l7b", "city", 24.0, cut(168), cut(170), crop=(0, 875, 1440, 810)),
    # ---- M: the hero / the problem / the bad guy / a world like yours ----
    S("m2", "t1", 63.7, cut(181), cut(183) + 0.10),
    S("m2b", "nlook", 11.7, cut(183) + 0.10, cut(186)),
    S("m3", "launch", 59.4, cut(186), cut(188)),
    S("m4", "t1", 68.8, cut(188), cut(195)),
    S("m5", "t1", 27.6, cut(195), cut(199)),
    S("m5b", "nlook", 2.1, cut(199), cut(201)),
    S("m5c", "t1", 21.9, cut(201), cut(203)),
    # ---- N: those kids grew up. Today ... escape from adulthood, back to the world ----
    S("n1", "goodbye", 2.4, cut(203), cut(208), crop=(0, 135, 1440, 810)),
    S("n2", "goodbye", 18.3, cut(208), cut(212), crop=(0, 135, 1440, 810)),
    S("n3", "adult", 0.7, cut(212), cut(213), grade="bw"),
    S("n3b", "adult", 3.0, cut(213), cut(217), grade="bw"),
    S("n4", "adult", 6.1, cut(217), cut(219) + 0.2, grade="bw"),
    S("n4b", "adult", 7.5, cut(219) + 0.2, cut(222), grade="bw"),
    S("n5", "t1", 11.2, cut(222), cut(226), push=(1.0, 1.05)),
    S("n5b", "t2", 83.2, cut(226), cut(232), push=(1.0, 1.06)),
    # ---- O: November 19th, Rockstar takes you back to Vice City, where it all started ----
    S("o1", "next", 1573.0, cut(232), cut(236), grade="dim", push=(1.0, 1.06)),
    S("o2", "vc10", 11.05, cut(236), cut(241)),
    S("o3", "t1", 39.9, cut(241), cut(243), push=(1.0, 1.06)),
    S("o4", "vc10", 63.4, cut(243), cut(248)),
    S("o4b", "vcde", 54.6, cut(248), cut(249)),
    # ---- P: lost in Los Santos ... don't rush. Take the long way home. Drive slow ----
    S("p1", "nostalgia", 0.1, cut(249), cut(253), crop=(0, 236, 1080, 608)),
    S("p1b", "nostalgia", 5.5, cut(253), cut(259), crop=(0, 236, 1080, 608)),
    S("p2", "nostalgia", 27.5, cut(259), cut(261), crop=(0, 236, 1080, 608), speed=0.6),
    S("p3", "next", 769.0, cut(261), cut(266)),
    S("p4", "next", 781.0, cut(266), cut(268), speed=0.7),
    # ---- Q: that 10-year-old never really left ... waiting 13 years to feel that freedom again ----
    S("q1", "goodbye", 13.0, cut(268), cut(272), crop=(0, 135, 1440, 810)),
    S("q2", "vc10", 48.8, cut(272), cut(275), fit="card", card=(1280, 960), crop=(293, 100, 693, 512)),
    S("q3", "waitgta6", 9.0, cut(275), cut(278), crop=(0, 700, 1440, 810)),
    S("q4", "wait5", 12.7, cut(278), cut(281), fit="blurfill"),
    S("q4b", "wait5", 13.7, cut(281), cut(285), fit="blurfill"),
    S("q5", "nlook", 17.5, cut(285), 103.85, push=(1.0, 1.05)),
    S("q6", "next", 1584.2, 103.85, 105.25),
    S("q7", "next", 1597.2, 105.25, TOTAL),
]
