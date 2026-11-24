"""The film's clock. Every boundary is snapped to the 60 fps frame grid (F).

v9 (Nov 24): the film opens on the user's new recording (new_starting_larry_fink_video.mp3, 24.6 s): "This is the most
powerful man on Earth. Larry Fink, the CEO of BlackRock. The most evil company in the world. A $15 trillion cartel of
weaponized capital that owns a piece of everything you touch. A company that's never made a single physical product,
yet it's one of the top shareholders in almost every major US company. It holds more of Nvidia than Jensen Huang, more
of Microsoft than Bill Gates, and more of Apple than Steve Jobs ever did." -- then Elon's question and the second half
("Back in the 1980s ..."), which are unchanged.

Sources of the times:
- the opening recording and the rest recording (rest.mp3): every word force-aligned to the sound (tools/align.py ->
  tools/words/*.json), with the long pauses cut out (tools/pace.py -> tools/words/pace.json): a file time goes through
  squeeze() before it is placed on the film;
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


ALIGN = {k: _load(k) for k in ("open", "rest", "rogan")}
PACE = _load("pace")
OPEN_CUTS = PACE["open"]["cuts"]
OPEN_OUT = PACE["open"]["open_out"]     # "... than Steve Jobs ever did." has fully faded (file seconds)
REST_CUTS = PACE["rest"]["cuts"]
REST1_OUT = PACE["rest"]["rest1_out"]   # the rest recording's first part (now replaced by the opening) ends here
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


ROGAN_T0, ROGAN_T1 = 12.55, 15.28  # the Rogan clip: Elon's question only (the clip's own times)


def O(t):
    """Film time of an opening-recording file time (the opening starts the film)."""
    return F(squeeze(t, OPEN_CUTS))


# the opening's words by key: index into the aligned words (tools/words/open.json), ("end", i) for a word's end,
# (i, frac) for a point inside a word ("weapon|ized")
OPEN_IDX = {
    "this": 0, "is": 1, "the1": 2, "most1": 3, "powerful": 4, "man": 5, "on": 6, "earth": 7, "earth_end": ("end", 7),
    "larry": 8, "fink": 9, "fink_end": ("end", 9), "the2": 10, "ceo": 11, "of0": 12, "blackrock": 13,
    "blackrock_end": ("end", 13), "the3": 14, "most": 15, "evil": 16, "company": 17, "in": 18, "the5": 19, "world": 20,
    "world_end": ("end", 20), "a": 21, "fifteen": 22, "trillion": 23, "dollar": 24, "cartel": 25, "of1": 26,
    "weapon": 27, "ized": (27, 0.52), "capital": 28, "that": 29, "owns": 30, "a2": 31, "piece": 32, "of2": 33,
    "everything": 34, "you": 35, "touch": 36, "touch_end": ("end", 36), "a3": 37, "company2": 38, "thats": 39,
    "never": 40, "made": 41, "a4": 42, "single": 43, "physical": 44, "product": 45, "product_end": ("end", 45),
    "yet": 46, "its": 47, "one": 48, "of3": 49, "the6": 50, "top": 51, "shareholders": 52,
    "shareholders_end": ("end", 52), "in2": 53, "almost": 54, "every": 55, "major": 56, "us": 57, "company3": 58,
    "company3_end": ("end", 58), "it": 59, "holds": 60, "more1": 61, "of4": 62, "nvidia": 63, "than1": 64,
    "jensen": 65, "huang": 66, "huang_end": ("end", 66), "more2": 67, "of5": 68, "microsoft": 69, "than2": 70,
    "bill": 71, "gates": 72, "gates_end": ("end", 72), "and": 73, "more3": 74, "of6": 75, "apple": 76, "than3": 77,
    "steve": 78, "jobs": 79, "jobs_end": ("end", 79), "ever": 80, "did": 81, "did_end": ("end", 81),
}


def _open_file(spec):
    words = ALIGN["open"]
    if isinstance(spec, int):
        return words[spec]["start"]
    if spec[0] == "end":
        return words[spec[1]]["end"] + 0.06          # the aligner's word end is a little early
    w = words[spec[0]]
    return w["start"] + (w["end"] - w["start"]) * spec[1]


W = {k: round(_open_file(v), 3) for k, v in OPEN_IDX.items()}   # opening file seconds
T = {k: O(v) for k, v in W.items()}                              # film seconds

OPEN_END = F(O(OPEN_OUT) + 0.02)
CARTEL_IN = F(T["cartel"] - 3 / 24)    # the cartel clip only for its table flash (frames 14-16 at 24 fps), the faces
                                      # from "cartel"
RISE = 0.40                            # the red scene: Fink's rise before the cut to the close-up
EVIL_IN = F(T["most"] - 2 / FPS - RISE)
LEAD = 2 / FPS                         # a picture changes two frames before its word (the references: 0-1 at 24 fps)
NAME_LEAD = 14 / FPS                   # the name mosaic builds first, so the name lands on "Larry"

TOUCH_END = F(T["touch"] + 15 / FPS)       # the touch clip is white on its frames 45-46, other footage from 47

# beats (film seconds, frame-snapped)
B = {
    "wall": (0.0, T["on"]),                              # "This is the most powerful man": the wall of Finks
    "earth": (T["on"], F(T["larry"] - NAME_LEAD)),       # "on Earth." the red card, held into the pause
    # "Larry Fink, the CEO of BlackRock.": the Hemant video's name mosaic (a big centre tile, small ones either side),
    # his clips first, BlackRock's from the word
    "name": (F(T["larry"] - NAME_LEAD), EVIL_IN),
    "evil": (EVIL_IN, T["company"]),                     # "The most evil": the red horned scene
    "company": (T["company"], T["a"]),                   # "company in the world."
    "money": (T["a"], CARTEL_IN),                        # "A $15 trillion dollar": the article flipbook
    "cartel": (CARTEL_IN, T["of1"]),                     # the cartel clip: its table flash, the faces on "cartel"
    "weap": (T["of1"], T["that"]),                       # "of weaponized capital"
    "logos": (T["that"], T["everything"]),               # "that owns a piece of"
    # "everything you touch.": the fingers meet on "touch", the burst, and its white frames (the touch source.s 29;
    # after it the clip cuts to other footage, so the beat ends there)
    "touch": (T["everything"], TOUCH_END),
    "made": (TOUCH_END, F(T["yet"] - LEAD)),             # "A company that's never made a single physical product,"
    "share": (F(T["yet"] - LEAD), F(T["it"] - LEAD)),    # "yet it's one of the top shareholders in almost every ..."
    "stake": (F(T["it"] - LEAD), OPEN_END),              # "It holds more of Nvidia than Jensen Huang ... ever did."
}
B["open"] = (0.0, OPEN_END)

# ---- the rest of the script: the user's second recording (rest.mp3, 57.39 s). Its first part ("A company that
# manages $15 trillion ... than Steve Jobs ever did.") is replaced by the new opening; the film uses it from
# "Back in the 1980s" (REST2_IN) on, after the Rogan clip
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

# Elon's question, his own shot through "company?" and on into his silent pause, to just before Rogan answers (the
# clip's 15.28 s): real video only, no cut to a still (the user, Nov 22), then the flash into the next part
B["rogan"] = (OPEN_END, F(OPEN_END + ROGAN_T1 - ROGAN_T0))
B["react"] = (B["rogan"][1], B["rogan"][1])               # (Rogan's listening shot is gone: no length)
B["pause"] = B["react"]                                   # (older scripts' name for the beat after the question)
REST2_AT = round(B["react"][1] - squeeze(REST2_IN, REST_CUTS), 4)
B["rest2"] = (B["react"][1], F(REST2_AT + squeeze(REST_END, REST_CUTS) + 0.35))


def R(t):
    """Film time of a rest-recording file time (the second part only: from "Back in the 1980s")."""
    return F(REST2_AT + squeeze(t, REST_CUTS))


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
    print(" ".join(f"{k}={v:.2f}" for k, v in T.items()))
