"""v4 voiceover: the user's cut-down script, up to "Freedom."

    GTA 6 took 13 years [and 2 billion dollars] to make.  [The release got pushed ... to November.]
    And yet, nobody seems to have moved on. But [why?] Why are grown adults waiting 13 years ...
    ... It was about what it really gave you. Freedom.

Every join sits on the quietest 10 ms inside a short window at the word boundary, with a 12 ms equal-power crossfade.
Writes gta6-edit/assets/audio/vo4.wav and gta6-edit/words4.json (kept words with their new VO-local times, keyed by
the original word index).   usage: python -I tools/vo4.py
"""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(os.path.dirname(HERE), "gta6-edit")
SR = 48000
W = json.load(open(os.path.join(PROJ, "words.json"), encoding="utf-8"))


def load(path):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


vo = load(os.path.join(PROJ, "assets", "audio", "vo.wav"))
env = np.sqrt(np.convolve(vo ** 2, np.ones(int(0.010 * SR)) / int(0.010 * SR), mode="same"))   # 10 ms RMS


def quiet(t0, t1):
    """time (s) of the quietest point between t0 and t1"""
    a, b = int(t0 * SR), int(t1 * SR)
    return (a + int(np.argmin(env[a:b]))) / SR


s, e = (lambda i: W[i]["start"]), (lambda i: W[i]["end"])
# (keep_from, keep_to) on the VO's own clock
cut_a1 = quiet(e(26) - 0.10, e(26) + 0.06)          # after "years"
cut_a2 = quiet(s(31) - 0.10, s(31) + 0.02)          # before "to"
cut_b1 = quiet(e(32) + 0.18, e(32) + 0.42)          # in the pause after "make."
cut_b2 = quiet(s(47) - 0.36, s(47) - 0.16)          # in the pause before "And"
cut_c1 = quiet(e(55) - 0.06, e(55) + 0.05)          # after "But"
cut_c2 = quiet(s(57) - 0.12, s(57) + 0.01)          # before "Why"
end = quiet(s(91) - 0.20, s(91) - 0.03)             # before "Back": the cut ends after "Freedom."
KEEP = [(0.0, cut_a1), (cut_a2, cut_b1), (cut_b2, cut_c1), (cut_c2, end)]

XF = int(0.012 * SR)
out = np.zeros(0, np.float32)
segs = []
for k, (a, b) in enumerate(KEEP):
    piece = vo[int(a * SR):int(b * SR)].copy()
    if k == len(KEEP) - 1:                               # 60 ms fade at the very end
        n = int(0.06 * SR); piece[-n:] *= np.cos(np.linspace(0, np.pi / 2, n)) ** 2
    if len(out) == 0:
        segs.append((a, b, 0.0)); out = piece; continue
    fo = np.cos(np.linspace(0, np.pi / 2, XF)); fi = np.sin(np.linspace(0, np.pi / 2, XF))
    dst = (len(out) - XF) / SR
    out = np.concatenate([out[:-XF], out[-XF:] * fo + piece[:XF] * fi, piece[XF:]])
    segs.append((a, b, dst))


def remap(t):
    for a, b, d in segs:
        if a - 1e-6 <= t <= b + 1e-6:
            return round(d + (t - a), 3)
    return None


words4 = []
for i, w in enumerate(W):
    ns, ne = remap(w["start"]), remap(min(w["end"], w["start"] + 2.0))
    if ns is None:
        continue
    if ne is None:          # a word whose tail was trimmed at a join
        ne = round(ns + 0.05, 3)
    words4.append({"i": i, "text": w["text"], "start": ns, "end": ne})
    if i >= 90:
        break

path = os.path.join(PROJ, "assets", "audio", "vo4.wav")
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
               input=pcm, check=True)
json.dump({"segments": [{"from": round(a, 4), "to": round(b, 4), "at": round(d, 4)} for a, b, d in segs],
           "duration": round(len(out) / SR, 3), "words": words4},
          open(os.path.join(PROJ, "words4.json"), "w", encoding="utf-8"), indent=1)
print(f"vo4: {len(out) / SR:.2f} s from {len(vo) / SR:.2f} s;", " | ".join(f"{a:.3f}-{b:.3f}->{d:.3f}" for a, b, d in segs))
print(" ".join(f"{w['i']}:{w['text']}@{w['start']:.2f}" for w in words4))
