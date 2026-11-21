"""The film's clock. Every boundary is snapped to the 60 fps frame grid (F).

Sources of the times (measured, see SPEC.md):
- the panel line: the FII7 panel video's own audio 32.32-38.95 s, placed at film 0;
- the voiceover (starting_part.mp3) word starts, re-transcribed phrase by phrase and checked against its loudness dips,
  placed at film V0 = 6.70;
- the Rogan / Musk clip from its 12.55 s (Rogan's "Do you think BlackRock's a bad company?") to 19.45 s.
"""
FPS = 60


def F(t):
    """Snap a time to the 60 fps frame grid."""
    return round(round(t * FPS) / FPS, 4)


V0 = 6.70          # voiceover start on the film
VO_END = 22.62     # voiceover file time where "BlackRock." has finished (then cut to Rogan)
LINE_T0, LINE_T1 = 32.32, 38.95   # panel audio for the opening line
ROGAN_T0, ROGAN_T1 = 12.55, 15.28  # the Rogan clip: Elon's question only, ending before Rogan's answer (15.31)


def V(t):
    """Film time of a voiceover file time."""
    return F(V0 + t)


# voiceover word starts (file seconds)
W = {
    "these": 0.05, "powerful": 1.01, "people": 1.48, "on": 2.01, "earth": 2.10,
    "a": 3.12, "sixty": 3.16, "trillion": 3.71, "dollar": 4.255, "cartel": 4.545, "of1": 5.095,
    "weapon": 5.205, "ized": 5.46, "capital": 5.83, "that": 6.29, "owns": 6.485, "a2": 6.72, "piece": 6.82,
    "of2": 7.08, "everything": 7.21, "you": 7.92, "touch": 8.04, "touch_end": 8.43,
    "thats": 9.05, "jamie": 9.37, "dimon": 9.68, "the1": 10.25, "guy1": 10.40, "running": 10.60, "jp": 11.01,
    "morgan": 11.21, "chase": 11.62, "chase_end": 11.97,
    "david": 12.45, "solomon": 12.68, "solomon_end": 13.20, "a3": 13.38, "parttime": 13.43, "dj": 14.12,
    "and": 14.28, "the2": 14.52, "ceo": 14.76, "goldman": 15.15, "sachs": 15.63, "sachs_end": 16.17,
    "amongst": 16.78, "them": 17.24, "is": 17.53, "this": 17.67, "guy2": 17.96, "guy2_end": 18.24,
    "the3": 18.59, "man": 18.69, "who": 18.86, "runs": 19.03, "the4": 19.25, "most": 19.42, "evil": 19.82,
    "company": 20.10, "in": 20.56, "the5": 20.70, "world": 20.92, "world_end": 21.34,
    "blackrock": 21.87, "blackrock_end": 22.59,
}
T = {k: V(v) for k, v in W.items()}

# panel line word starts (film seconds = panel time - 32.32)
LINE_WORDS = [
    ("I", 32.36), ("don't", 32.40), ("think", 32.68), ("there's", 32.88), ("ever", 33.02), ("been", 33.29),
    ("a", 33.42), ("panel", 33.47), ("with", 33.99), ("as", 34.12), ("big", 34.22), ("an", 34.30),
    ("assemblage", 34.38), ("of", 35.04), ("financial", 35.17), ("talent", 35.81), ("and", 36.18),
    ("skill", 36.38), ("as", 36.58), ("you've", 37.03), ("been", 37.25), ("able", 37.52), ("to", 37.82),
    ("put", 37.92), ("together", 38.15), ("here.", 38.76),
]
LINE = [(w, F(t - LINE_T0)) for w, t in LINE_WORDS]

# beats (film seconds, frame-snapped)
CARTEL_IN = F(T["cartel"] - 14 / 24)   # the cartel clip from its table flash (frame 14 at 24 fps) to the cut at frame 28

B = {
    "quote": (0.0, F(V0)),
    "tiles": (F(V0), T["on"]),                 # "These are the most powerful people": the 3x3 tile flash from "These"
    "earth": (T["on"], T["a"]),
    "money": (T["a"], CARTEL_IN),              # "a $60 trillion": the article flipbook (shortened for the cartel clip)
    "cartel": (CARTEL_IN, T["weapon"]),        # the user's cartel clip: its table flash, the faces cut in on "cartel"
    "weap": (T["weapon"], T["that"]),
    "logos": (T["that"], F(14.25)),
    "touch": (F(14.25), T["touch_end"]),       # the hands come together, touch on "touch"
    "puppet": (T["touch_end"], T["thats"]),    # the explainer's puppet shot
    "dimon": (T["thats"], T["jp"]),            # "That's Jamie Dimon, the guy running" (the reference edit's intro)
    "jpm": (T["jp"], T["david"]),              # "JP Morgan Chase" (the reel's "the man behind OpenAI")
    "solomon": (T["david"], T["dj"]),          # "David Solomon, a part-time" (the reference edit's "AI")
    "dj": (T["dj"], T["ceo"]),                 # "DJ and the": the D-Sol video
    "ceo": (T["ceo"], T["sachs_end"]),         # "CEO of Goldman Sachs" (the reel's OpenAI device)
    "orbit": (T["sachs_end"], T["is"]),        # the camera circling the table, people lighting up, through "Amongst them"
    "thisguy": (T["is"], T["the3"]),           # "is this guy": the group image, the spotlight on Fink (reel DeJRKmqTPdg)
    "walk": (T["the3"], T["runs"]),            # "the man who": Fink on stage
    "box": (T["runs"], T["company"]),          # "runs the most evil": the interview, the red square on "most"
    "company": (T["company"], T["blackrock"]), # "company in the world": BlackRock's letters, building, doors
    "brand": (T["blackrock"], F(V0 + VO_END + 0.045)),  # "BlackRock.": the letters on its facade
}
B["fink"] = (B["thisguy"][0], B["brand"][1])

# ---- the rest of the script: the user's second recording (larryfink video audio rest.mp3, 57.39 s), split after
# "...than Steve Jobs ever did." for the Rogan clip ("Do you think BlackRock's a bad company?")
REST_SPLIT, REST_END = 10.56, 57.39
RW = {  # word starts in the rest recording (whisper small.en, file seconds)
    "a": 0.09, "that_r": 0.71, "manages": 1.06, "15": 1.73, "trillion": 2.30, "assets": 3.24, "holds": 4.01, "nvidia": 4.51,
    "than1": 5.00, "jensen": 5.19, "more2": 6.20, "microsoft": 6.57, "than2": 7.24, "bill": 7.38, "and1": 8.10,
    "apple": 8.82, "than3": 9.10, "steve": 9.61, "ever": 10.16,
    "back": 10.63, "1980s": 11.39, "larry1": 12.63, "was1": 13.14, "wall1": 13.44, "street1": 13.74, "prodigy": 14.20, "but1": 14.96,
    "bad": 15.52, "cost": 16.08, "100": 16.56, "loss": 17.87, "that1": 18.21, "enough": 18.66, "thrown": 19.56,
    "wall2": 20.27, "and2": 20.92, "convince": 21.24, "onething": 22.08, "wall3": 23.31, "terrible": 23.98,
    "seeing": 24.63, "risk1": 25.02, "so": 25.52, "1988": 26.11, "he1": 27.52, "cofounded": 27.65, "blackrock": 28.31,
    "built": 29.03, "system": 29.55, "job": 30.52, "calculating": 30.87, "risk2": 31.81, "he_called": 32.39,
    "aladdin": 33.42, "when": 34.16, "2008": 34.56, "crisis1": 35.24, "hit": 35.75, "the_us": 36.03,
    "government": 36.49, "called2": 37.04, "oneguy": 37.56, "wall4": 37.88, "threw": 38.41, "years": 38.84,
    "clean": 39.46, "mess": 40.00, "larry2": 40.80, "fink2": 41.19, "he2": 41.63, "crisis2": 42.76, "three": 43.44,
    "money1": 44.38, "today": 45.13, "every": 45.46, "buy": 46.32, "sp": 46.80, "500": 47.43, "your": 48.19,
    "ends": 48.69, "this": 49.22, "hands": 49.82, "a2": 50.36, "never": 51.37, "single": 52.09, "product": 52.56,
    "but2": 53.31, "own": 54.22, "everything2": 54.57, "touch2": 55.36, "has": 55.80, "piece": 56.05, "him": 56.49,
    "it": 56.81,
}
REST1_AT = B["brand"][1]
B["rest1"] = (REST1_AT, F(REST1_AT + REST_SPLIT))
B["rogan"] = (B["rest1"][1], F(B["rest1"][1] + ROGAN_T1 - ROGAN_T0))
B["pause"] = (B["rogan"][1], F(B["rogan"][1] + 1.0))   # the user: a 1-second pause after Elon's question
REST2_AT = round(B["pause"][1] - REST_SPLIT, 4)
B["rest2"] = (B["pause"][1], F(REST2_AT + REST_END + 0.35))


def RT(key):
    """Film time of a word in the rest recording."""
    t = RW[key]
    return F((REST1_AT if t < REST_SPLIT else REST2_AT) + t)


TOTAL = B["rest2"][1]

if __name__ == "__main__":
    for k, (a, b) in B.items():
        print(f"{k:8s} {a:7.3f} {b:7.3f}  {b - a:6.3f}s  frames {round(a * FPS)}-{round(b * FPS)}")
    print("TOTAL", TOTAL, round(TOTAL * FPS), "frames")
