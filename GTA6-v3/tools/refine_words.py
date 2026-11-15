"""Fuse Parakeet (text, robust) and whisper (fine) word onsets, snapping phrase starts to real pause ends.
usage: python -I refine_words.py parakeet.json whisper_words.json audio.mp3 out.json"""
import json, re, subprocess, sys
pk_path, wh_path, audio, dst = sys.argv[1:5]
pk = json.load(open(pk_path, encoding="utf-8"))
wh = json.load(open(wh_path, encoding="utf-8"))
assert len(pk) == len(wh), (len(pk), len(wh))
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", "silencedetect=noise=-38dB:d=0.10", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
sil = list(zip(st, en))
out = []
used = set()
for i, (p, w) in enumerate(zip(pk, wh)):
    P, W = p["start"], w["start"]
    lo, hi = min(P, W) - 0.08, max(P, W) + 0.08
    snap = [s1 for s0, s1 in sil if lo <= s1 <= hi and s1 not in used]
    if snap:
        used.add(snap[0])
        s = snap[0]; how = "pause"
    elif abs(W - P) <= 0.15:
        s = W; how = "whisper"
    else:
        s = P; how = "parakeet"
    if out and s <= out[-1]["start"] + 0.05:      # keep onsets strictly increasing
        s = max(P, W, out[-1]["start"] + 0.08); how = "mono"
    out.append({"id": f"w{i}", "text": p["text"], "start": round(s, 3), "how": how})
for i, o in enumerate(out):
    nxt = out[i + 1]["start"] if i + 1 < len(out) else 96.3
    # end: the next onset, or the start of a pause that sits between them
    ends = [s0 for s0, s1 in sil if o["start"] < s0 < nxt]
    o["end"] = round(ends[0] if ends else nxt, 3)
    if o["end"] - o["start"] < 0.06:
        o["end"] = round(o["start"] + 0.06, 3)
json.dump(out, open(dst, "w", encoding="utf-8"), indent=1)
print(" | ".join(f'{i} {o["start"]:.2f}-{o["end"]:.2f}{o["how"][0]} {o["text"]}' for i, o in enumerate(out)))
