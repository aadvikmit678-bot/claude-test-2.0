"""Trimmed from blackrock-open/tools/timing.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

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

ALIGN = {k: _load(k) for k in ("open", "open2", "rest", "rogan")}

OPEN_REC = "open2"                    # the recording the film opens on

PACE = _load("pace")

OPEN_CUTS = PACE[OPEN_REC]["cuts"]      # (none: the user slowed this recording on purpose)

OPEN_OUT = PACE[OPEN_REC]["open_out"]   # "... than Steve Jobs ever did." has fully faded (file seconds)

REST_CUTS = PACE["rest"]["cuts"]

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

# the opening's words by key: index into the aligned words (tools/words/open2.json), ("end", i) for a word's end,
# (i, frac) for a point inside a word ("weapon|ized")
OPEN_IDX = {
    "this": 0, "is": 1, "the1": 2, "most1": 3, "powerful": 4, "man": 5, "on": 6, "earth": 7, "earth_end": ("end", 7),
    "larry": 8, "fink": 9, "fink_end": ("end", 9), "the2": 10, "ceo": 11, "of0": 12, "blackrock": 13,
    "blackrock_end": ("end", 13), "or": 14, "how": 15, "people": 16, "call": 17, "it0": 18, "the3": 19, "most": 20,
    "evil": 21, "evil_end": ("end", 21), "company": 22, "ever0": 23, "built": 24, "built_end": ("end", 24), "a": 25,
    "fifteen": 26, "trillion": 27, "dollar": 28, "cartel": 29, "of1": 30, "weapon": 31, "ized": (31, 0.52),
    "capital": 32, "that": 33, "owns": 34, "a2": 35, "piece": 36, "of2": 37, "everything": 38, "you": 39, "touch": 40,
    "touch_end": ("end", 40), "a3": 41, "company2": 42, "thats": 43, "never": 44, "made": 45, "a4": 46, "single": 47,
    "physical": 48, "product": 49, "product_end": ("end", 49), "yet": 50, "its": 51, "one": 52, "of3": 53,
    "the6": 54, "top": 55, "shareholders": 56, "shareholders_end": ("end", 56), "in2": 57, "almost": 58, "every": 59,
    "major": 60, "us": 61, "company3": 62, "company3_end": ("end", 62), "it": 63, "holds": 64, "more1": 65, "of4": 66,
    "nvidia": 67, "than1": 68, "jensen": 69, "huang": 70, "huang_end": ("end", 70), "more2": 71, "of5": 72,
    "microsoft": 73, "than2": 74, "bill": 75, "gates": 76, "gates_end": ("end", 76), "and": 77, "more3": 78,
    "of6": 79, "apple": 80, "than3": 81, "steve": 82, "jobs": 83, "jobs_end": ("end", 83), "ever": 84, "did": 85,
    "did_end": ("end", 85),
}

def _open_file(spec):
    words = ALIGN[OPEN_REC]
    if isinstance(spec, int):
        return words[spec]["start"]
    if spec[0] == "end":
        return words[spec[1]]["end"] + 0.06          # the aligner's word end is a little early
    w = words[spec[0]]
    return w["start"] + (w["end"] - w["start"]) * spec[1]

W = {k: round(_open_file(v), 3) for k, v in OPEN_IDX.items()}   # opening file seconds

T = {k: O(v) for k, v in W.items()}                              # film seconds

OPEN_END = F(O(OPEN_OUT) + 0.02)

LEAD = 2 / FPS                         # a picture changes two frames before its word (the references: 0-1 at 24 fps)

NAME_LEAD = 14 / FPS                   # the name mosaic builds first, so the name lands on "Larry"

EVIL_IN = F(T["or"] - 0.05)

CARTEL_IN = F(T["cartel"] - LEAD)      # v10: straight from the cutouts to the cartel faces (no table flash: the user)            # the red scene: Fink rises through "or how people call it, the" (the v6 rise)

# beats (film seconds, frame-snapped)
B = {
    # "This is the most powerful man on Earth.": reel DgHoW0vhPvb's opening (the photo wall, its textures) into the
    # Kalanick reel's frame: Fink cut out in front of the line, the line in the serif behind him
    "first": (0.0, F(T["larry"] - NAME_LEAD)),
    # "Larry Fink, the CEO of BlackRock": the Hemant video's name mosaic (a big centre tile, small ones either side),
    # his clips first, BlackRock's from the word
    "name": (F(T["larry"] - NAME_LEAD), EVIL_IN),
    # "or how people call it, the most evil": the red horned scene as v6 had it (the user: "like the original version
    # ... a bit slow"): the rise under the small words, the cut to the close-up two frames before "most"
    "evil": (EVIL_IN, F(T["company"] - LEAD)),
    "built": (F(T["company"] - LEAD), F(T["a"] - LEAD)),     # "company ever built."
    "money": (F(T["a"] - LEAD), CARTEL_IN),                  # "A $15 trillion dollar": the headline cutouts
    "cartel": (CARTEL_IN, T["of1"]),                         # the cartel clip: its table flash, the faces on "cartel"
    "weap": (T["of1"], T["that"]),                           # "of weaponized capital"
    "logos": (T["that"], T["everything"]),                   # "that owns a piece of"
    # "everything you touch.": the fingers meet on "touch", the burst, and its white frames (the touch source.s 29;
    # after it the clip cuts to other footage, so the beat ends there)
    "touch": (T["everything"], F(T["a3"] - LEAD)),           # (v15: the touch clip runs on until "A company")
    "made": (F(T["a3"] - LEAD), F(T["yet"] - LEAD)),         # "A company that's never made a single physical product,"
    "share": (F(T["yet"] - LEAD), F(T["it"] - LEAD)),        # "yet it's one of the top shareholders in almost every ..."
    "stake": (F(T["it"] - LEAD), OPEN_END),                  # "It holds more of Nvidia than Jensen Huang ... ever did."
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
