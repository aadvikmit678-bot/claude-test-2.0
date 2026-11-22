"""The film's clock. Every boundary is snapped to the 60 fps frame grid (F).

Sources of the times:
- the panel line: the FII7 panel video's own audio 32.32-38.95 s, placed at film 0;
- the voiceover (starting_part.mp3) and the rest recording (rest.mp3): every word force-aligned to the sound
  (tools/align.py -> tools/words/*.json; whisper's own times ran up to 0.95 s early), with the long pauses cut out
  (tools/pace.py -> tools/words/pace.json): a file time goes through squeeze() before it is placed on the film;
- the Rogan / Musk clip from its 12.55 s (Elon: "Do you think BlackRock's a bad company?") to 15.28 s: Elon's own shot
  through his short silent pause after "company?", then a flash into "Back in the 1980s".
"""
import json
import os

FPS = 60
_WD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words")


def F(t):
    """Snap a time to the 60 fps frame grid."""
    return round(round(t * FPS) / FPS, 4)


def _load(name):
    with open(f"{_WD}/{name}.json") as f:
        return json.load(f)


ALIGN = {k: _load(k) for k in ("vo", "rest", "rogan")}
PACE = _load("pace")
VO_CUTS = PACE["vo"]["cuts"]
REST_CUTS = PACE["rest"]["cuts"]
REST1_OUT = PACE["rest"]["rest1_out"]   # "... than Steve Jobs ever did." has fully faded
REST2_IN = PACE["rest"]["rest2_in"]     # just before "Back in the 1980s"


def squeeze(t, cuts):
    """A recording's file time, with the pauses cut before it taken out."""
    out = t
    for a, b in cuts:
        if t >= b:
            out -= b - a
        elif t > a:
            out -= t - a
    return out


V0 = 6.70          # voiceover start on the film
VO_END = 22.62     # voiceover file time where "BlackRock." has finished (then the rest recording)
LINE_T0, LINE_T1 = 32.32, 38.95   # panel audio for the opening line
ROGAN_T0, ROGAN_T1 = 12.55, 15.28  # the Rogan clip: Elon's question only (the clip's own times)


def V(t):
    """Film time of a voiceover file time."""
    return F(V0 + squeeze(t, VO_CUTS))


# the voiceover's words by key: index into the aligned words (tools/words/vo.json), ("end", i) for a word's end,
# (i, frac) for a point inside a word ("weapon|ized")
VO_IDX = {
    "these": 0, "powerful": 4, "people": 5, "on": 6, "earth": 7, "a": 8, "sixty": 9, "trillion": 10, "dollar": 11,
    "cartel": 12, "of1": 13, "weapon": 14, "ized": (14, 0.52), "capital": 15, "that": 16, "owns": 17, "a2": 18,
    "piece": 19, "of2": 20, "everything": 21, "you": 22, "touch": 23, "touch_end": ("end", 23), "thats": 24,
    "jamie": 25, "dimon": 26, "the1": 27, "guy1": 28, "running": 29, "jp": 30, "morgan": 31, "chase": 32,
    "chase_end": ("end", 32), "david": 33, "solomon": 34, "solomon_end": ("end", 34), "a3": 35, "parttime": 36,
    "dj": 37, "and": 38, "the2": 39, "ceo": 40, "goldman": 41, "sachs": 42, "sachs_end": ("end", 42), "amongst": 43,
    "them": 44, "is": 45, "this": 46, "guy2": 47, "guy2_end": ("end", 47), "the3": 48, "man": 49, "who": 50,
    "runs": 51, "the4": 52, "most": 53, "evil": 54, "company": 55, "in": 56, "the5": 57, "world": 58,
    "world_end": ("end", 58), "blackrock": 59, "blackrock_end": ("end", 59),
}


def _vo_file(spec):
    words = ALIGN["vo"]
    if isinstance(spec, int):
        return words[spec]["start"]
    if spec[0] == "end":
        return words[spec[1]]["end"] + 0.06          # the aligner's word end is a little early
    w = words[spec[0]]
    return w["start"] + (w["end"] - w["start"]) * spec[1]


W = {k: round(_vo_file(v), 3) for k, v in VO_IDX.items()}   # voiceover file seconds
T = {k: V(v) for k, v in W.items()}                         # film seconds

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
CARTEL_IN = F(T["cartel"] - 3 / 24)    # the cartel clip only for its table flash (frames 14-16 at 24 fps), the main
                                      # frame from "cartel" (the user: "$60 trillion" longer, the table not held)

B = {
    "quote": (0.0, F(V0)),
    "tiles": (F(V0), T["on"]),                 # "These are the most powerful people": the 3x3 tile flash from "These"
    "earth": (T["on"], T["a"]),
    "money": (T["a"], CARTEL_IN),              # "a $60 trillion": the article flipbook
    "cartel": (CARTEL_IN, T["of1"]),           # the user's cartel clip: its table flash, the faces cut in on "cartel"
    "weap": (T["of1"], T["that"]),             # the tank from "of", so WEAPONIZED comes in on its word
    "logos": (T["that"], T["everything"]),
    "touch": (T["everything"], T["thats"]),    # cut on "everything": the fingers meet on "touch" (the puppet is gone)
    "dimon": (T["thats"], T["jp"]),            # "That's Jamie Dimon, the guy running" (the reference edit's intro)
    "jpm": (T["jp"], T["david"]),              # "JP Morgan Chase" (the reel's "the man behind OpenAI")
    "solomon": (T["david"], T["dj"]),          # "David Solomon, a part-time"
    "dj": (T["dj"], T["ceo"]),                 # "DJ and the": the DJ videos
    "ceo": (T["ceo"], T["amongst"]),           # "CEO of Goldman Sachs" -- straight into "Amongst" (the user)
    "orbit": (T["amongst"], T["is"]),          # the camera circling the table, through "Amongst them"
    "thisguy": (T["is"], T["the3"]),           # "is this guy": the group image, the spotlight on Fink
    "walk": (T["the3"], T["runs"]),            # "the man who runs the most evil": the Fink flipbook
    "box": (T["runs"], T["company"]),
    "company": (T["company"], T["blackrock"]), # "company in the world": BlackRock's letters, building, doors
    "brand": (T["blackrock"], F(V(VO_END) + 0.045)),  # "BlackRock.": the letters on its facade
}
B["evil"] = (T["the3"], T["company"])     # "the man who runs the most evil": the red horned scene (reel DfhzVs8q9NH)
B["fink"] = (B["thisguy"][0], B["brand"][1])

# ---- the rest of the script: the user's second recording (rest.mp3, 57.39 s), split after "...than Steve Jobs ever
# did." for the Rogan clip ("Do you think BlackRock's a bad company?")
REST_END = 57.39
# the rest recording's words by key: index into tools/words/rest.json
RW_IDX = {
    'a': 0, 'that_r': 2, 'manages': 3, '15': 4, 'trillion': 5, 'assets': 7, 'holds': 8, 'nvidia': 11, 'than1': 12,
    'jensen': 13, 'more2': 15, 'microsoft': 17, 'than2': 18, 'bill': 19, 'and1': 21, 'apple': 24, 'than3': 25,
    'steve': 26, 'ever': 28, 'back': 30, '1980s': 33, 'larry1': 34, 'was1': 36, 'wall1': 38, 'street1': 39,
    'prodigy': 40, 'but1': 41, 'bad': 43, 'cost': 45, '100': 47, 'loss': 49, 'that1': 50, 'enough': 52, 'thrown': 56,
    'wall2': 59, 'and2': 61, 'convince': 63, 'onething': 66, 'wall3': 68, 'terrible': 71, 'seeing': 73, 'risk1': 74,
    'so': 75, '1988': 77, 'he1': 78, 'cofounded': 79, 'blackrock': 80, 'built': 82, 'system': 84, 'job': 87,
    'calculating': 88, 'risk2': 89, 'he_called': 90, 'aladdin': 93, 'when': 94, '2008': 96, 'crisis1': 97, 'hit': 98,
    'the_us': 99, 'government': 101, 'called2': 102, 'oneguy': 104, 'wall4': 106, 'threw': 108, 'years': 110,
    'clean': 113, 'mess': 116, 'larry2': 117, 'fink2': 118, 'he2': 119, 'crisis2': 124, 'three': 126, 'money1': 129,
    'today': 130, 'every': 131, 'buy': 134, 'sp': 136, '500': 137, 'your': 138, 'ends': 140, 'this': 143,
    'hands': 145, 'a2': 146, 'never': 150, 'single': 153, 'product': 154, 'but2': 155, 'own': 158,
    'everything2': 159, 'touch2': 161, 'has': 162, 'piece': 164, 'him': 166, 'it': 168,
}
RW = {k: ALIGN["rest"][i]["start"] for k, i in RW_IDX.items()}   # rest-recording file seconds

REST1_AT = B["brand"][1]
B["rest1"] = (REST1_AT, F(REST1_AT + squeeze(REST1_OUT, REST_CUTS)))
# Elon's question, his own shot through "company?" and on into his silent pause, to just before Rogan answers (the
# clip's 15.28 s): real video only, no cut to a still of Rogan (the user, Nov 22: "extended only a slight second when
# Elon Musk pauses ... that pause and then cut. I don't want any still photo frame"), then the flash into the next part
B["rogan"] = (B["rest1"][1], F(B["rest1"][1] + ROGAN_T1 - ROGAN_T0))
B["react"] = (B["rogan"][1], B["rogan"][1])               # (Rogan's listening shot is gone: no length)
B["pause"] = B["react"]                                   # (older scripts' name for the beat after the question)
REST2_AT = round(B["react"][1] - squeeze(REST2_IN, REST_CUTS), 4)
B["rest2"] = (B["react"][1], F(REST2_AT + squeeze(REST_END, REST_CUTS) + 0.35))


def R(t):
    """Film time of a rest-recording file time."""
    return F((REST1_AT if t < REST1_OUT else REST2_AT) + squeeze(t, REST_CUTS))


def RT(key):
    """Film time of a word in the rest recording."""
    return R(RW[key])


def RTX(key):
    """RT for a word key, or a rest-recording time in seconds (a cut between words)."""
    return R(RW[key] if isinstance(key, str) else float(key))


REST_SPLIT = REST1_OUT       # (older scripts' name)
TOTAL = B["rest2"][1]

if __name__ == "__main__":
    for k, (a, b) in B.items():
        print(f"{k:8s} {a:7.3f} {b:7.3f}  {b - a:6.3f}s  frames {round(a * FPS)}-{round(b * FPS)}")
    print("TOTAL", TOTAL, round(TOTAL * FPS), "frames")
