"""v4 voiceover: the user's cut-down script, the whole of it (to "... to feel that freedom again.").

    GTA 6 took 13 years [and 2 billion dollars] to make.  [The release got pushed ... to November.]
    And yet, nobody seems to have moved on. But [why?] Why are grown adults waiting 13 years ...
    ... It was about what it really gave you. Freedom. Back to being 10 years old, sitting in front of the family computer,
    ... With cheat codes like aspirin and panzer scribbled at the back of your notebook. For a kid, it wasn't just a
    game. It was a psychological escape, an alternate reality. It was everything you imagined adulthood would be.
    Driving supercars, firing guns, flying planes, and owning an entire city. And while every other game asks you to be
    the hero, But GTA lets you be the problem. It lets you be the bad guy in a world that looks just like yours. And
    somewhere along the way, those kids grew up. Today, it's the exact opposite. It's an escape from adulthood,
    back to the world they once dreamed of living in. And on November 19th, Rockstar takes you back to Vice City ...
    ... He's just been waiting 13 years to feel that freedom again.

Then every silence longer than 0.30 s is cut down to 0.20 s (the user: "reduce the gaps so the video feels faster").
Every join sits on a quiet point with a 12 ms equal-power crossfade.
Writes gta6-edit/assets/audio/vo4.wav and gta6-edit/words4.json (kept words with their new VO-local times, keyed by
the original word index).   usage: python -I tools/vo4.py
"""
import json, os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(os.path.dirname(HERE), "gta6-edit")
SR = 48000
W = json.load(open(os.path.join(PROJ, "words.json"), encoding="utf-8"))
LAST = 288                              # "again." -- the whole script
MAXP, KEEPP = 0.30, 0.20                # pauses longer than MAXP keep KEEPP


def load(path):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


vo = load(os.path.join(PROJ, "assets", "audio", "vo.wav"))
win = int(0.010 * SR)
env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, mode="same"))       # 10 ms RMS
THR = np.percentile(env, 95) * 10 ** (-36 / 20)                              # silence: 36 dB under the speech level
silent = env < THR


def quiet(t0, t1):
    a, b = int(t0 * SR), int(t1 * SR)
    return (a + int(np.argmin(env[a:b]))) / SR


def speech_end(t):
    """the start of the first silence of at least 80 ms after t"""
    i = int(t * SR); n = int(0.08 * SR)
    while i < len(silent) - n:
        if silent[i] and silent[i:i + n].all():
            return i / SR
        i += win // 2
    return t


s, e = (lambda i: W[i]["start"]), (lambda i: W[i]["end"])
cut_a1 = quiet(e(26) - 0.10, e(26) + 0.06)                 # after "years"
cut_a2 = quiet(s(31) - 0.10, s(31) + 0.02)                 # before "to"
cut_b1 = speech_end(s(32) + 0.12) + 0.10                   # just after "make." really ends
cut_b2 = quiet(s(47) - 0.14, s(47) - 0.04)                 # just before "And"
cut_c1 = quiet(s(55) + 0.085, s(55) + 0.125)               # "But" ends here: the first "why?" rises from ~+0.16 s
cut_c2 = s(57) - 0.09                                      # in the silence just before the second "Why"
end = speech_end(s(LAST) + 0.25) + 0.12                    # after "again."
KEEP = [(0.0, cut_a1), (cut_a2, cut_b1), (cut_b2, cut_c1), (cut_c2, end)]

# tighten the long pauses inside each kept piece
pieces = []
for a, b in KEEP:
    ia, ib = int(a * SR), int(b * SR)
    sil = silent[ia:ib]
    runs, i = [], 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]:
                j += 1
            runs.append(((ia + i) / SR, (ia + j) / SR)); i = j
        else:
            i += 1
    cur = a
    for r0, r1 in runs:
        if r1 - r0 > MAXP and r0 > a + 0.05 and r1 < b - 0.05:
            pieces.append((cur, r0 + KEEPP / 2)); cur = r1 - KEEPP / 2
    pieces.append((cur, b))

XF = int(0.012 * SR)
out = np.zeros(0, np.float32)
segs = []
for k, (a, b) in enumerate(pieces):
    piece = vo[int(a * SR):int(b * SR)].copy()
    if k == len(pieces) - 1:
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
for i, w in enumerate(W[:LAST + 1]):
    ns = remap(w["start"])
    if ns is None:
        continue
    ne = remap(min(w["end"], w["start"] + 2.0))
    words4.append({"i": i, "text": w["text"], "start": ns, "end": ne if ne is not None else round(ns + 0.05, 3)})

path = os.path.join(PROJ, "assets", "audio", "vo4.wav")
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
               input=pcm, check=True)
json.dump({"segments": [{"from": round(a, 4), "to": round(b, 4), "at": round(d, 4)} for a, b, d in segs],
           "duration": round(len(out) / SR, 3), "words": words4},
          open(os.path.join(PROJ, "words4.json"), "w", encoding="utf-8"), indent=1)
saved = sum(b - a for a, b in KEEP) - len(out) / SR
print(f"vo4: {len(out) / SR:.2f} s ({len(segs)} pieces; {saved:.2f} s of pauses removed)")
print(" ".join(f"{w['i']}:{w['text']}@{w['start']:.2f}" for w in words4))
