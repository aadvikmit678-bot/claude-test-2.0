"""Merge whisper.cpp token output (transcript.json) into words with start/end seconds."""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
words = []
for seg in d["transcription"]:
    for t in seg["tokens"]:
        txt = t["text"]
        if txt.startswith("[_") or txt.strip() == "":
            continue
        s, e = t["offsets"]["from"] / 1000, t["offsets"]["to"] / 1000
        if txt.startswith(" ") or not words:
            words.append({"text": txt.strip(), "start": s, "end": e, "p": t["p"]})
        else:
            words[-1]["text"] += txt
            words[-1]["end"] = e
            words[-1]["p"] = min(words[-1]["p"], t["p"])
for i, w in enumerate(words):
    w["id"] = f"w{i}"
json.dump(words, open(dst, "w", encoding="utf-8"), indent=1)
for w in words:
    print(f'{w["id"]:>5} {w["start"]:7.2f} {w["end"]:7.2f} {w["p"]:.2f} {w["text"]}')
