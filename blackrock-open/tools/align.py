"""Forced alignment: where every spoken word starts and ends in the film's recordings (to about 20 ms), so the
captions land on the word as it is heard.

Whisper's own word times drift: it put "Back in the 1980s" 0.8 s before it is said (it starts a segment's first
word at the end of the silence before it). Here the transcript is aligned to the sound itself with a character
CTC model (torchaudio's WAV2VEC2_ASR_BASE_960H) and torchaudio.functional.forced_align.

Needs torch + torchaudio (the scratch Demucs venv has both); writes tools/words/<name>.json, which the film's
scripts read, so they don't need torch:
    python -I tools/align.py
"""
import json
import os
import re
import subprocess

import numpy as np
import torch
import torchaudio
import torchaudio.functional as AF

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(f"{HERE}/../../blackrock-src/vo")
AUD = os.path.abspath(f"{HERE}/../assets/audio")
OUT = f"{HERE}/words"

# how a written word is said (the recordings say "fifteen trillion dollars", "S and P five hundred", ...)
SAY = {
    "$15": "FIFTEEN", "$60": "SIXTY", "60": "SIXTY", "$100": "ONE HUNDRED", "1980s": "NINETEEN EIGHTIES",
    "1988": "NINETEEN EIGHTY EIGHT", "2008": "TWO THOUSAND EIGHT", "500": "FIVE HUNDRED", "S&P": "S AND P",
    "U.S.": "U S", "JP": "J P", "CEO": "C E O", "DJ": "D J", "part-time": "PART TIME", "co-founded": "CO FOUNDED",
    "BlackRock": "BLACK ROCK", "BlackRock's": "BLACK ROCK'S", "Blackrock's": "BLACK ROCK'S", "Nvidia": "INVIDIA",
}
SCALE = {"trillion", "million", "billion"}


def spoken(words):
    """[[SPOKEN, WORDS], ...], one list per written word."""
    out = []
    for i, w in enumerate(words):
        key = w.strip().strip(",.?!—-").replace("’", "'")
        say = SAY.get(key, key).upper().replace("’", "'")
        parts = [re.sub(r"[^A-Z']", "", p) for p in say.split()]
        # "$15 trillion in": the dollar sign is said after the scale word, unless the next word is "dollar(s)"
        prev = words[i - 1].strip() if i else ""
        nxt = words[i + 1].strip().lower().strip(",.") if i + 1 < len(words) else ""
        if key.lower() in SCALE and prev.startswith("$") and not nxt.startswith("dollar"):
            parts.append("DOLLARS")
        out.append([p for p in parts if p])
    return out


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


_MODEL = None


def align(path, words):
    global _MODEL
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    if _MODEL is None:
        _MODEL = bundle.get_model().eval()
    labels = bundle.get_labels()
    idx = {c: i for i, c in enumerate(labels)}
    x = load(path)
    with torch.inference_mode():
        em, _ = _MODEL(torch.from_numpy(x)[None])
        lp = torch.log_softmax(em, -1)
    step = len(x) / 16000 / lp.shape[1]          # seconds per emission frame (0.02)
    toks, owner = [], []
    for wi, parts in enumerate(spoken(words)):
        for p in parts:
            if toks:
                toks.append(idx["|"])
                owner.append(-1)
            for ch in p:
                toks.append(idx[ch])
                owner.append(wi)
    ali, sc = AF.forced_align(lp, torch.tensor([toks], dtype=torch.int32), blank=0)
    spans = AF.merge_tokens(ali[0], sc[0].exp())
    assert len(spans) == len(toks), (len(spans), len(toks))
    out = []
    for wi, w in enumerate(words):
        mine = [s for s, o in zip(spans, owner) if o == wi]
        if not mine:
            out.append({"text": w, "start": None, "end": None, "score": 0})
            continue
        out.append({"text": w, "start": round(mine[0].start * step, 3), "end": round(mine[-1].end * step, 3),
                    "score": round(float(np.mean([s.score for s in mine])), 3)})
    return out


def whisper_words(path):
    d = json.load(open(path))
    if isinstance(d, list):
        return [(w.get("text") or w.get("word")).strip() for w in d]
    if "words" in d:
        return [(w.get("text") or w.get("word")).strip() for w in d["words"]]
    return [s["text"].strip() for s in d["transcription"] if s["text"].strip()]


# the FII7 panel line, as said (its words were whisper's times until Nov 22: "big" left too fast, "assemblage" came
# early); line.wav is the panel audio as the film places it (film second 0 = the panel's 32.32 s)
LINE = ("I don't think there's ever been a panel with as big an assemblage of financial talent and skill as you've "
        "been able to put together here.").split()

JOBS = {
    "rest": (f"{SRC}/rest/rest16.wav", f"{SRC}/rest/transcript.json"),
    "vo": (f"{SRC}/vo16.wav", f"{SRC}/vo_dtw.json"),
    "rogan": (f"{AUD}/rogan_vocals.wav", f"{SRC}/rogan/transcript.json"),
    "line": (f"{AUD}/line.wav", LINE),
}

if __name__ == "__main__":
    import sys
    os.makedirs(OUT, exist_ok=True)
    for name, (audio, words) in JOBS.items():
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        res = align(audio, words if isinstance(words, list) else whisper_words(words))
        json.dump(res, open(f"{OUT}/{name}.json", "w"), indent=0)
        low = [f"{r['text']}({r['score']})" for r in res if r["score"] < 0.35]
        print(f"{name}: {len(res)} words, mean score {np.mean([r['score'] for r in res]):.2f}; weak: {' '.join(low)}")
