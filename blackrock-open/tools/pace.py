"""The pauses cut out of the two recordings (the user: "after Goldman Sachs there is a 1-second pause … cut direct to
'Amongst them' … pace the video wherever there is such a long pause").

For every gap between two aligned words (tools/words/<name>.json) that is longer than the gap we keep, the silence is
found on the recording's own loudness (10 ms steps, 14 dB over its noise floor): the cut starts after the first word
has really faded (the aligner's word end can be early) and stops before the next word's first sound. A cut is only
ever made in silence, so it is inaudible (the mix fades 6 ms on each side).

Also finds where the first part of the rest recording ends ("… than Steve Jobs ever did." in full -- the Elon clip was
clipping "did") and where the second starts (just before "Back in the 1980s").

Writes tools/words/pace.json; timing.py, the mix and the captions all map file time through the same cuts.
    python -I tools/pace.py      (needs numpy)
"""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(f"{HERE}/../../blackrock-src/vo")
WD = f"{HERE}/words"

KEEP = 0.22          # a sentence pause, after pacing
LONG = 0.34          # pauses longer than this are cut down to KEEP
# (recording, index of the word before the gap): the gap to keep there instead
SPECIAL = {
    ("vo", 23): 0.30,    # "touch." -> "That's": the puppet shot's breath
    ("vo", 42): 0.08,    # "Sachs." -> "Amongst": straight in (the user)
    ("vo", 58): 0.26,    # "world," -> "BlackRock."
    ("rest", None): None,
    # the new opening (Nov 24): the red ON EARTH card holds into its pause, the red "most evil" scene's rise needs
    # the whole pause after "BlackRock." (no cut there), the others keep a short breath
    ("open", 7): 0.36,    # "Earth." -> "Larry"
    ("open", 13): 0.60,   # "BlackRock." -> "The": untouched (Fink rises through it)
    ("open", 20): 0.24,   # "world." -> "A"
    ("open", 36): 0.28,   # "touch." -> "A"
    ("open", 58): 0.26,   # "company." -> "It"
    ("open", 66): 0.24,   # "Huang," -> "more"
    ("open", 72): 0.24,   # "Gates," -> "and"
}
REST_KEEP = {"it": 0.32, "mess—": 0.30}   # "He called it … Aladdin.", "the mess— … Larry Fink." keep their beat


def envelope(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    fr = x[: len(x) // 160 * 160].reshape(-1, 160)
    e = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-7)
    return e, np.percentile(e, 10) + 14


def silence(e, thr, a, b):
    """The silent stretch between word end a and next word start b (seconds), on the loudness: (tail end, onset)."""
    i0, i1 = int(a * 100), int(b * 100)
    loud = e > thr
    t = i0
    while t < i1 and loud[t:t + 3].any():          # the first word's tail: until 30 ms of quiet
        t += 1
    s = i1
    while s > t and loud[s - 1]:                   # the next word's first sound (its attack starts before the aligner's)
        s -= 1
    return t / 100, s / 100


def cuts_for(name, audio, words):
    e, thr = envelope(audio)
    out = []
    for k, (w0, w1) in enumerate(zip(words, words[1:])):
        if w0["end"] is None or w1["start"] is None:
            continue
        keep = SPECIAL.get((name, k), REST_KEEP.get(w0["text"], KEEP) if name == "rest" else KEEP)
        tail, onset = silence(e, thr, w0["end"], w1["start"])
        gap = onset - tail
        if w1["start"] - w0["end"] <= LONG and (name, k) not in SPECIAL:
            continue
        if gap <= keep + 0.02:
            continue
        lead = min(0.13, keep * 0.6)                # keep the fade of the first word's tail
        a, b = tail + lead, tail + lead + (gap - keep)
        out.append([round(a, 3), round(b, 3), w0["text"], w1["text"]])
    return out, e, thr


def main():
    res = {}
    vo = json.load(open(f"{WD}/vo.json"))
    vo = vo[: next(i for i, w in enumerate(vo) if w["text"].startswith("BlackRock")) + 1]
    cuts, _, _ = cuts_for("vo", f"{SRC}/vo16.wav", vo)
    res["vo"] = {"cuts": [c[:2] for c in cuts], "why": [f"{c[2]} -> {c[3]}" for c in cuts]}
    rest = json.load(open(f"{WD}/rest.json"))
    did = next(i for i, w in enumerate(rest) if w["text"] == "did.")
    cuts, e, thr = cuts_for("rest", f"{SRC}/rest/rest16.wav", rest)
    tail, onset = silence(e, thr, rest[did]["end"], rest[did + 1]["start"])
    cuts = [c for c in cuts if not (c[2] == "did.")]          # that gap is where the Elon clip goes
    res["rest"] = {"cuts": [c[:2] for c in cuts], "why": [f"{c[2]} -> {c[3]}" for c in cuts],
                   "rest1_out": round(tail + 0.09, 3), "rest2_in": round(onset - 0.05, 3)}
    # the new opening recording (new_starting_larry_fink_video.mp3): its pauses, and where "... ever did." has faded
    op = json.load(open(f"{WD}/open.json"))
    cuts, e, thr = cuts_for("open", f"{SRC}/open/open16.wav", op)
    tail, _ = silence(e, thr, op[-1]["end"], op[-1]["end"] + 0.2)
    res["open"] = {"cuts": [c[:2] for c in cuts], "why": [f"{c[2]} -> {c[3]}" for c in cuts],
                   "open_out": round(min(tail + 0.09, len(e) / 100), 3)}
    json.dump(res, open(f"{WD}/pace.json", "w"), indent=1)
    for k, v in res.items():
        saved = sum(b - a for a, b in v["cuts"])
        print(f"{k}: {len(v['cuts'])} pauses cut, {saved:.2f} s saved")
        for (a, b), why in zip(v["cuts"], v["why"]):
            print(f"   {a:6.2f}-{b:6.2f} ({b - a:.2f}s)  {why}")
    print("rest1 ends", res["rest"]["rest1_out"], "rest2 starts", res["rest"]["rest2_in"], "open ends", res["open"]["open_out"])


if __name__ == "__main__":
    main()
