"""The film's captions, every word on its own spoken onset (the force-aligned words of tools/words, through the paced
clock of timing.py), in three styles the user chose (Nov 21):

1. "jensen" -- from the panel line to "...than Steve Jobs ever did.": the Jensen Huang reel (DfxH1gUoKlp). One small
   line at the centre, Inter Display SemiBold, white with a soft shadow; the words cut in one at a time on their
   onsets and build a 2-4 word phrase that re-centres as it grows. Key words ("*") are set alone in Instrument Serif
   with the Dario white glow instead (and the Nvidia reel's DfpiReJKFLO: key words big and glowing). "[...]" is a span
   the film already writes big itself (ON EARTH, CARTEL, WEAPONIZED, the intros' names, $15 TRILLION ...): no line.
   "^" sets a phrase dark, low on the frame, over Think School's light grey page.
2. "palmer" -- Elon's question on Rogan: the Palmer Luckey reel (DfNWN82R0wR) -- lowercase bold Helvetica, stacked a
   word or two to a line beside him, each word blurring in.
3. "porsche" -- "Back in the 1980s" to the end: the Porsche reel (DdazhmWsDem, notes/REF_PORSCHE.md) -- Instrument
   Serif Italic, words set wide apart and laid out before they appear, each fading in from a soft blur in its own place;
   its big glowing figures ("€1.25B." -> "$100 million loss.", "2008", "3x"), its letter-by-letter reveal ("4,500
   people" -> "S&P 500,"), and the ON EARTH red card for "in 1988" (the user).
"""
import json
import os
import re

import timing as TM

F, T, B = TM.F, TM.T, TM.B
LEAD = 0.03          # a word shows this much before its aligned onset (never late; never visibly early)


# ------------------------------------------------------------------ words with film times
def vo_words():
    out = []
    for w in TM.ALIGN["vo"]:
        if w["start"] is None:
            continue
        out.append((w["text"], TM.V(w["start"]), TM.V(w["end"])))
        if w["text"].startswith("BlackRock"):
            break
    return out


def rest_words(part):
    out = []
    for w in TM.ALIGN["rest"]:
        first = w["start"] < TM.REST1_OUT
        if (part == "rest1") == first:
            out.append((w["text"], TM.R(w["start"]), TM.R(w["end"])))
    return out


def rogan_words():
    a = B["rogan"][0]
    return [(w["text"], F(a + w["start"]), F(a + w["end"])) for w in TM.ALIGN["rogan"]]


def line_words():
    L = TM.LINE
    return [(w, t, L[i + 1][1] if i + 1 < len(L) else t + 0.4) for i, (w, t) in enumerate(L)]


def _norm(w):
    w = w.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9'&$%-]", "", w)


def _clean(w):
    """How a word reads on screen: the Jensen reel drops commas and full stops, keeps ? and apostrophes."""
    w = w.replace("'", "’").replace("—", "")
    w = {"U.S.": "US", "Blackrock’s": "BlackRock’s"}.get(w, w)
    return w.rstrip(",.") if not w.endswith("?") else w


# ------------------------------------------------------------------ 1. jensen (+ serif key words)
SCRIPT = {
    "line": "I don't think | there's ever been | a panel | with as big | an assemblage | of financial talent | "
            "and skill | as you've been able | to put together here.",
    "vo": "These are the most | [powerful people on earth,] | [a 60 trillion dollar cartel of weaponized capital] | "
          "^that owns | ^a piece of | *everything | you touch. | [That's Jamie Dimon, the guy running JP Morgan Chase,] | "
          "[David Solomon,] | a part-time DJ | and the CEO~of | [Goldman Sachs.] | [Amongst them is this guy,] | "
          "[the man who runs the most evil] | company in the world, | [BlackRock.]",
    "rest1": "A company | that manages | [$15 trillion] | in assets | ^holds more of | ^Nvidia than | Jensen Huang, | "
             "^more of | ^Microsoft than | Bill Gates, | ^and more of | ^Apple than | Steve Jobs | ever did.",
}


def _words_of(part):
    if part == "line":
        return line_words()
    if part == "vo":
        return vo_words()
    return rest_words("rest1")


def jensen_chunks():
    """[(kind, [(text, onset, end), ...])], kind "small" | "ink" | "emph" | "hidden"."""
    out = []
    for part, script in SCRIPT.items():
        words = _words_of(part)
        i = 0
        for raw in script.split("|"):
            raw = raw.strip()
            kind = "small"
            if raw.startswith("["):
                kind, raw = "hidden", raw.strip("[]")
            elif raw.startswith("*"):
                kind, raw = "emph", raw.lstrip("*")
            elif raw.startswith("^"):
                kind, raw = "ink", raw.lstrip("^")
            elif raw.startswith("%"):                    # white, a heavier halo (over the white brand maps)
                kind, raw = "heavy", raw.lstrip("%")
            ws = []
            for tok in raw.split():
                if i >= len(words):
                    raise SystemExit(f"ran out of words in {part} at {tok!r}")
                w, t, e = words[i]
                if _norm(w)[:1] != _norm(tok)[:1]:
                    for j in range(i + 1, min(i + 4, len(words))):
                        if _norm(words[j][0])[:1] == _norm(tok)[:1]:
                            i, (w, t, e) = j, words[j]
                            break
                ws.append((_clean(tok).replace("~", " "), F(t - LEAD), e))
                i += 1
            out.append((kind, ws))
    return out


def jensen_phrases():
    """[(start, end, [(text, onset, end)], kind)] -- a phrase holds until the next one starts (or 0.9 s after its
    last word ends, whichever is first)."""
    cs = jensen_chunks()
    out = []
    for k, (kind, ws) in enumerate(cs):
        if kind == "hidden" or not ws:
            continue
        nxt = cs[k + 1][1][0][1] if k + 1 < len(cs) and cs[k + 1][1] else B["rest1"][1]
        end = min(nxt, ws[-1][2] + 0.9, B["rest1"][1])
        out.append((F(ws[0][1]), F(min(nxt, max(end, ws[-1][1] + 6 / 60))), ws, kind))
    return out


# ------------------------------------------------------------------ 2. palmer (Elon's question)
PALMER_LINES = [(0, 2), (3, 4), (5, 6)]        # "do you think / BlackRock's a / bad company?" (the user)


def palmer_lines():
    ws = rogan_words()
    out = []
    for a, b in PALMER_LINES:
        out.append([((w if w.startswith("Black") else w.lower()).replace("Blackrock", "BlackRock").replace("'", "’"),
                     F(t - LEAD)) for w, t, _ in ws[a:b + 1]])
    return out


# ------------------------------------------------------------------ 3. porsche ("Back in the 1980s" to the end)
# (kind, first word index, last word index, text) -- indices into tools/words/rest.json; a phrase's words map onto
# its index range in order. kinds: "por" (the small italic line), "word" (one word, larger), "big" (the glowing
# figure), "type" (letter by letter), "card" (the red card, "IN" then "1988" on its word).
PORSCHE = [
    ("por", 30, 31, "Back in"), ("por", 32, 33, "the 1980s,"), ("por", 34, 35, "Larry Fink"), ("por", 36, 37, "was a"),
    ("por", 38, 39, "Wall Street"), ("word", 40, 40, "prodigy,"),
    ("por", 41, 42, "but one"), ("por", 43, 44, "bad bet"), ("por", 45, 46, "cost him"),
    ("big", 47, 49, "$100 million loss."),
    ("por", 50, 52, "That was enough"), ("por", 53, 55, "to get him"), ("por", 56, 57, "thrown out"),
    ("por", 58, 60, "of Wall Street"), ("por", 61, 64, "and to convince him"), ("por", 65, 67, "of one thing."),
    ("por", 68, 69, "Wall Street"), ("por", 70, 71, "is terrible"), ("por", 72, 73, "at seeing"), ("word", 74, 74, "risk."),
    ("por", 75, 75, "So,"), ("card", 76, 77, "IN|1988"), ("por", 78, 79, "he co-founded"), ("word", 80, 80, "BlackRock"),
    ("por", 81, 82, "and built"), ("por", 83, 84, "a system"), ("por", 85, 87, "with one job"),
    ("por", 88, 88, "calculating"), ("word", 89, 89, "risk."),
    ("por", 90, 92, "He called it"), ("word", 93, 93, "Aladdin."),
    ("por", 94, 95, "When the"), ("big", 96, 96, "2008"), ("por", 97, 98, "crisis hit,"),
    ("por", 99, 101, "the U.S. government"), ("por", 102, 102, "called"), ("por", 103, 105, "the one guy"),
    ("por", 106, 109, "Wall Street threw out"), ("por", 110, 111, "years ago"), ("por", 112, 114, "to clean up"),
    ("por", 115, 116, "the mess"), ("word", 117, 118, "Larry Fink."),
    ("por", 119, 121, "He came out"), ("por", 122, 124, "of that crisis"), ("por", 125, 125, "with"),
    ("big", 126, 127, "3x"), ("por", 128, 129, "the money."),
    ("por", 130, 130, "Today,"), ("por", 131, 132, "every time"), ("por", 133, 135, "you buy the"),
    ("type", 136, 137, "S&P 500,"),
    ("por", 138, 139, "your money"), ("por", 140, 142, "ends up in"), ("por", 143, 145, "this guy’s hands."),
    ("por", 146, 147, "A company"), ("por", 148, 150, "that has never"), ("por", 151, 152, "made a"),
    ("por", 153, 154, "single product,"), ("por", 155, 156, "but everything"), ("por", 157, 158, "you own,"),
    ("por", 159, 159, "everything"), ("por", 160, 161, "you touch,"), ("por", 162, 164, "has a piece"),
    ("por", 165, 168, "of him in it."),
]


def porsche_phrases():
    """[(start, end, kind, [(text, onset)], text)]: each phrase until the next starts (at most 1.0 s after its last
    word ends); a word's onset is its aligned onset (a phrase with fewer display words than spoken ones maps in order)."""
    ws = TM.ALIGN["rest"]
    film = lambda i: TM.R(ws[i]["start"])
    out = []
    for k, (kind, a, b, text) in enumerate(PORSCHE):
        toks = text.split("|") if kind == "card" else text.split()
        idx = list(range(a, b + 1))
        words = [(tok, F(film(idx[min(j, len(idx) - 1)]) - LEAD)) for j, tok in enumerate(toks)]
        nxt = film(PORSCHE[k + 1][1]) - LEAD if k + 1 < len(PORSCHE) else B["rest2"][1]
        end = min(nxt, TM.R(ws[b]["end"]) + 1.0, B["rest2"][1] - 2 / 60)
        out.append((F(words[0][1]), F(min(nxt, max(end, words[-1][1] + 0.2))), kind, words, text))
    return out


if __name__ == "__main__":
    for a, b, ws, kind in jensen_phrases():
        print(f"{a:7.3f}-{b:7.3f} {kind:5s} " + " ".join(f"{w}@{t:.2f}" for w, t, _ in ws))
    print("palmer", palmer_lines())
    for a, b, kind, ws, text in porsche_phrases():
        print(f"{a:7.3f}-{b:7.3f} {kind:5s} " + " ".join(f"{w}@{t:.2f}" for w, t in ws))
