"""The film's sound, mixed exactly as index.html places it (news, CJ, the voiceover, the effects), limited to -1 dBTP.
python3 -I gta6/tools/mix.py OUT.wav            (then mux onto a render with ffmpeg -c:v copy)"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edit

A = f"{edit.ROOT}/gta6/assets"
out = sys.argv[1]
items = [(f"{A}/audio/news_n.wav", 0.0, 6.70, 1.0), (f"{A}/audio/cj_n.wav", edit.CJ0, 2.45, 1.0),
         (f"{A}/audio/vo_n.wav", edit.V0, 96.44, 1.0)]
items += [(f"{A}/sfx/{n}.mp3", t, None, edit.SFX_GAIN[n]) for n, t, _ in edit.SFX]
cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y"]
fc = []
for i, (path, t, dur, g) in enumerate(items):
    cmd += ["-i", path]
    ms = int(round(t * 1000))
    trim = f"atrim=0:{dur}," if dur else ""
    fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{trim}adelay={ms}|{ms},volume={g}[a{i}]")
mixin = "".join(f"[a{i}]" for i in range(len(items)))
fc.append(f"{mixin}amix=inputs={len(items)}:normalize=0:dropout_transition=0,apad,atrim=0:{edit.END},"
          f"alimiter=limit=0.891:level=false:attack=3:release=60[out]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", "-ac", "2", out]
subprocess.run(cmd, check=True)
r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true:framelog=quiet",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
summ = r[r.index("Summary"):]
print(out, " ".join(l.strip() for l in summ.splitlines() if l.strip().startswith(("I:", "Peak:"))))
