"""The numbers of each studied clip as a short text file for the reading agents (gta6-work/<key>/facts.md): every shot
with its time, length, brightness, motion and colour, every flash / black / white frame, the music's tempo and which
cuts fall on an onset, and the transcript with times.

usage: python3 -I gta6/tools/facts.py [key ...]"""
import json, os, sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = f"{ROOT}/gta6-work"


def facts(key):
    d = json.load(open(f"{WORK}/{key}/study.json"))
    m, fps = d["meta"], d["meta"]["fps"]
    on = np.array(d["onsets"]) if d["onsets"] else np.array([1e9])
    out = [f"# {key}: {d['title']}", "",
           f"- kind: {d['kind']}; {m['w']}x{m['h']}, {fps:g} fps, {m['duration']:.2f} s, {d['frames_read']} frames read; "
           f"video starts {m['v_start']:.3f} s, audio {m['a_start']:.3f} s (all times below on the player's clock)",
           f"- shots: {len(d['shots'])}; cuts: {len(d['cuts'])}; median shot {np.median([s['dur'] for s in d['shots']]):.2f} s, "
           f"shortest {min(s['frames'] for s in d['shots'])} frames, longest {max(s['dur'] for s in d['shots']):.2f} s"]
    t = d["tempo"]
    if t:
        out.append(f"- music: tempo about {t['bpm']} BPM (autocorrelation strength {t['strength']}); {len(d['onsets'])} onsets; "
                   f"{d['cuts_on_onsets']} of {len(d['cuts'])} cuts within a frame of an onset (median cut-to-onset "
                   f"offset {d['cut_onset_median_offset_ms']} ms; negative = the cut comes first)")
    out += ["", "## Shots", "", "| # | start s | end s | frames | dur s | luma | motion | mean RGB | cut on onset? |",
            "|---|---|---|---|---|---|---|---|---|"]
    for s in d["shots"]:
        dist = float(np.min(np.abs(on - s["t0"]))) if s["i"] else None
        hit = "" if dist is None else ("yes" if dist <= 1 / fps + 0.02 else f"no ({dist * 1000:.0f} ms)")
        out.append(f"| {s['i']} | {s['t0']:.3f} | {s['t1']:.3f} | {s['frames']} | {s['dur']:.2f} | {s['luma']} | "
                   f"{s['motion']} | {tuple(s['rgb'])} | {hit} |")
    if d["events"]:
        out += ["", "## Flash, black and white frames", ""]
        out += [f"- {e['kind']} at frame {e['frame']} ({e['t']:.3f} s), {e['frames']} frame(s)" for e in d["events"]]
    if d["transcript"].strip():
        out += ["", "## Transcript (whisper small.en, word times; check names against the picture)", ""]
        line, t0 = [], None
        for w in d["words"]:
            if t0 is None:
                t0 = w["t"]
            line.append(w["w"])
            if w["w"].endswith((".", "?", "!")) or len(line) >= 14:
                out.append(f"- {t0:.2f}: {' '.join(line)}")
                line, t0 = [], None
        if line:
            out.append(f"- {t0:.2f}: {' '.join(line)}")
    if d["onsets"]:
        out += ["", "## Onsets (s)", "", ", ".join(f"{x:.2f}" for x in d["onsets"][:400])]
    p = f"{WORK}/{key}/facts.md"
    open(p, "w").write("\n".join(out) + "\n")
    return p


if __name__ == "__main__":
    keys = sys.argv[1:] or [k for k in sorted(os.listdir(WORK)) if os.path.exists(f"{WORK}/{k}/study.json")]
    for k in keys:
        print(facts(k))
