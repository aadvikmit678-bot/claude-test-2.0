"""Cut every shot of gta6/tools/edit.py to 1920x1080 30 fps clips, plus the audio, fonts, sound effects and stills.

python3 -I gta6/tools/prep.py [shot ids ...]     (no ids: everything)
"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edit

PROJ = f"{edit.ROOT}/gta6"
CLIPS = f"{PROJ}/assets/clips"
FPS = edit.FPS


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(map(str, cmd))[:400]}\n{r.stderr[-1500:]}")
    return r


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0",
               path], text=True).stdout.strip().split(",")
    return int(out[0]), int(out[1])


def crop_expr(W, H, Wt, Ht, cx=0.5, cy=0.5, z=1.0):
    A = Wt / Ht
    if W / H > A:
        h = H; w = H * A
    else:
        w = W; h = W / A
    w /= z; h /= z
    x = min(max(cx * W - w / 2, 0), W - w)
    y = min(max(cy * H - h / 2, 0), H - h)
    w, h, x, y = int(w) // 2 * 2, int(h) // 2 * 2, int(x), int(y)
    return f"crop={w}:{h}:{x}:{y},scale={Wt}:{Ht}:flags=lanczos,setsar=1"


def band_of(src, t):
    """The 16:9 picture inside a vertical frame: the longest run of non-black rows."""
    W, H = probe(src)
    raw = run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-f", "rawvideo",
               "-pix_fmt", "gray", "-"]).stdout
    a = np.frombuffer(raw, np.uint8).reshape(H, W)
    rows = a.mean(1) > 10
    best, cur, start = (0, 0, 0), 0, 0
    for i, v in enumerate(list(rows) + [False]):
        if v:
            if cur == 0:
                start = i
            cur += 1
        else:
            if cur > best[0]:
                best = (cur, start, i)
            cur = 0
    _, y0, y1 = best
    return y0, y1


GRADES = {"news": "eq=brightness=-0.035:contrast=1.03", "dark": "eq=brightness=-0.16:contrast=1.05:saturation=0.8"}


def vf_for(s, W, H, Wt=1920, Ht=1080):
    f = []
    if s.get("rot"):
        f.append("transpose=1" if s["rot"] == "cw" else "transpose=2")
        W, H = H, W
    if s.get("band"):
        y0, y1 = band_of(edit.SRC[s["src"]], s["t"] + 0.3)
        f.append(f"crop={W}:{(y1 - y0) // 2 * 2}:0:{y0}")
        H = (y1 - y0) // 2 * 2
        s = dict(s, z=s.get("z", 1.07), cy=s.get("cy", 0.44))        # trims the burned subtitles at the bottom
    f.append(crop_expr(W, H, Wt, Ht, s.get("cx", 0.5), s.get("cy", 0.5), s.get("z", 1.0)))
    if s.get("grade"):
        f.append(GRADES[s["grade"]])
    sp = s.get("speed", 1.0)
    f.append(f"setpts=(PTS-STARTPTS)/{sp}" if sp != 1.0 else "setpts=PTS-STARTPTS")
    f.append(f"fps={FPS},format=yuv420p")
    return ",".join(f)


def encode(out):
    return ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-g", "10", "-movflags", "+faststart", out]


def cut_one(src_key, t, n, o, out, Wt=1920, Ht=1080):
    src = edit.SRC[src_key]
    W, H = probe(src)
    sp = o.get("speed", 1.0)
    dur_in = n / FPS * sp + 0.6
    s = dict(o, src=src_key, t=t)
    if o.get("mode") == "card":
        fc = (f"[0:v]split[a][b];[a]{crop_expr(W, H, 1920, 1080)},gblur=sigma=34,eq=brightness=-0.24:saturation=0.85[bg];"
              f"[b]scale=-2:1080:flags=lanczos,setsar=1[fg];[bg][fg]overlay=(W-w)/2:0,setpts=PTS-STARTPTS,fps={FPS},"
              f"format=yuv420p[v]")
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-t", f"{dur_in:.3f}",
             "-filter_complex", fc, "-map", "[v]", "-frames:v", str(n)] + encode(out))
    else:
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-t", f"{dur_in:.3f}",
             "-vf", vf_for(s, W, H, Wt, Ht), "-frames:v", str(n)] + encode(out))


def frames(path):
    return int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                    "stream=nb_read_frames", "-of", "csv=p=0", path], text=True).stdout.strip())


def make(b):
    """One clip per beat: its segments cut on whole frames of the film clock and joined with hard cuts."""
    out = f"{CLIPS}/{b['id']}.mp4"
    fa = round(b["a"] * FPS)
    total = round(b["b"] * FPS) - fa
    segs = b["segs"]
    if len(segs) == 1:
        src, t, _, o = segs[0]
        cut_one(src, t, total, o, out, b.get("w", 1920), b.get("h", 1080))
    else:
        parts, prev = [], fa
        for k, (src, t, e, o) in enumerate(segs):
            fe = round((e if e is not None else b["b"]) * FPS)
            part = f"{CLIPS}/_{b['id']}_{k}.mp4"
            cut_one(src, t, fe - prev, o, part)
            parts.append(part)
            prev = fe
        lst = f"{CLIPS}/_{b['id']}.txt"
        open(lst, "w").write("".join(f"file '{os.path.basename(x)}'\n" for x in parts))
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
             "-movflags", "+faststart", out])
        for x in parts + [lst]:
            os.remove(x)
    return b["id"], total, frames(out)


def make_layer(l):
    out = f"{CLIPS}/{l['id']}.mp4"
    n = round(l["b"] * FPS) - round(l["a"] * FPS)
    cut_one(l["src"], l["t"], n, l, out, l["w"], l["h"])
    return l["id"], n, frames(out)


def make_still(name, src_key, t):
    src = edit.SRC[src_key]
    W, H = probe(src)
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf",
         crop_expr(W, H, 960, 540), "-q:v", "3", f"{PROJ}/assets/img/{name}.jpg"])
    return name


def make_static():
    """6 frames of TV static (seeded, so the same every run)."""
    out = f"{CLIPS}/s02.mp4"
    rng = np.random.default_rng(6)
    frames = []
    for i in range(8):
        a = rng.integers(0, 256, (270, 480), dtype=np.uint8).astype(np.float32)
        a = a * 0.75 + rng.integers(0, 256, (270, 1), dtype=np.uint8) * 0.25          # horizontal bands
        a[rng.integers(0, 270, 6)] = 235                                               # bright lines
        frames.append(np.clip(a, 0, 255).astype(np.uint8))
    raw = b"".join(np.repeat(np.repeat(f, 4, 0), 4, 1).tobytes() for f in frames)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", "1920x1080",
                    "-r", str(FPS), "-i", "-", "-vf", "format=yuv420p"] + encode(out), input=raw, check=True)
    return "s02 static"


def loudnorm(src, out, target):
    """Two-pass EBU R128 loudness normalisation (linear when it can be), true peak -1.5 dBTP."""
    import json as _j
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", src, "-af",
                        f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    m = _j.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-af", af, "-ar", "48000", "-ac", "2", out])


def assets():
    A = f"{PROJ}/assets"
    for d in ["audio", "fonts", "sfx", "img", "tex"]:
        os.makedirs(f"{A}/{d}", exist_ok=True)
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", edit.SRC["billion"], "-t", "6.70", "-vn", "-ac", "2", "-ar", "48000",
         "-af", "afade=t=out:st=6.64:d=0.06", f"{A}/audio/news.wav"])
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", edit.SRC["awshit"], "-t", "2.45", "-vn", "-ac", "2", "-ar", "48000",
         "-af", "afade=t=out:st=2.33:d=0.12", f"{A}/audio/cj.wav"])
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{edit.ROOT}/gta6-src/_vo/gta_Audio.mp3", "-vn", "-ac", "2",
         "-ar", "48000", f"{A}/audio/vo.wav"])
    for name, target in [("news", -17.0), ("cj", -16.0), ("vo", -16.0)]:
        loudnorm(f"{A}/audio/{name}.wav", f"{A}/audio/{name}_n.wav", target)
    sfx = "/root/.claude/skills/media-use/audio/assets/sfx"
    for name in sorted({x[0] for x in edit.SFX}):
        shutil.copy(f"{sfx}/{name}.mp3", f"{A}/sfx/{name}.mp3")
    shutil.copy(f"{sfx}/CREDITS.md", f"{A}/sfx/CREDITS.md")
    for f in ["InstrumentSerif-Regular.woff2", "InstrumentSerif-Italic.woff2"]:
        shutil.copy(f"{edit.ROOT}/jpm-dimon/assets/fonts/{f}", f"{A}/fonts/{f}")
    cf = "/mnt/skills/examples/canvas-design/canvas-fonts"
    for f in ["NothingYouCouldDo-Regular.ttf", "NothingYouCouldDo-OFL.txt", "Silkscreen-Regular.ttf", "Silkscreen-OFL.txt"]:
        shutil.copy(f"{cf}/{f}", f"{A}/fonts/{f}")
    shutil.copy(f"{edit.ROOT}/jpm-dimon/assets/tex/paper_light.png", f"{A}/tex/paper_light.png")
    return "assets"


SPECS = f"{CLIPS}/.specs.json"


def spec_key(x):
    """What a clip is cut from: if this changes, the clip is stale (v2: a changed in-point is never left uncut)."""
    import hashlib, json as _j
    keep = {k: x[k] for k in sorted(x) if k not in ("id",)}
    return hashlib.sha1(_j.dumps(keep, sort_keys=True, default=str).encode()).hexdigest()[:16]


if __name__ == "__main__":
    import json as _j
    os.makedirs(CLIPS, exist_ok=True)
    os.makedirs(f"{PROJ}/assets/img", exist_ok=True)
    only = set(sys.argv[1:]) - {"--stale"}
    stale_only = "--stale" in sys.argv[1:]
    old = _j.load(open(SPECS)) if os.path.exists(SPECS) else {}
    def wanted(x):
        if only:
            return x["id"] in only
        if stale_only:
            return old.get(x["id"]) != spec_key(x) or not os.path.exists(f"{CLIPS}/{x['id']}.mp4")
        return True
    jobs = [b for b in edit.S if b.get("segs") and wanted(b)]
    lay = [l for l in edit.LAYERS if wanted(l)]
    print("cutting:", " ".join(x["id"] for x in jobs + lay) or "(nothing stale)")
    with ThreadPoolExecutor(4) as ex:
        futs = [ex.submit(make, b) for b in jobs] + [ex.submit(make_layer, l) for l in lay]
        if (not only and not stale_only) or "stills" in only:
            futs += [ex.submit(make_still, k, *v) for k, v in edit.STILLS.items()]
        if (not only and not stale_only) or "s02" in only:
            futs.append(ex.submit(make_static))
        if (not only and not stale_only) or "assets" in only:
            futs.append(ex.submit(assets))
        bad = 0
        for f in futs:
            r = f.result()
            if isinstance(r, tuple) and r[1] != r[2]:
                print("FRAME MISMATCH", r); bad += 1
        print("done", len(futs), "jobs,", bad, "mismatches")
    new = dict(old)
    for x in jobs + lay:
        new[x["id"]] = spec_key(x)
    _j.dump(new, open(SPECS, "w"), indent=0, sort_keys=True)
