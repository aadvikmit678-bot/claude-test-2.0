"""Study the GTA 6 reference folder frame by frame (no editing): for every clip in gta6-src/manifest.tsv make a 480p
proxy (every frame kept), read every frame numerically, find every cut, flash, black and white frame, find the music's
onsets and tempo, transcribe the speech, and draw labelled contact sheets for looking at:

  gta6-work/<key>/proxy.mp4            every frame of the source, 480 px tall (the sheets and stats come from it)
  gta6-work/<key>/study.json           meta, per-frame luma, cuts, shots, events, onsets, tempo, transcript, sheet list
  gta6-work/<key>/shots_NN.jpg         one frame per shot (the middle), labelled  #shot  start-end  frames
  gta6-work/<key>/flow_NN.jpg          (edits) 12 frames a second, 6 x 6 = 3 s a sheet, labelled  frame / time
  gta6-work/<key>/cuts_NN.jpg          (edits) every cut at full frame rate: the 4 frames before and 4 after, one row each

usage: python3 -I gta6/tools/study.py [key ...]        (default: every clip; ROOT = the repo root)
"""
import json, math, os, subprocess, sys, struct
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.environ.get("GTA6_ROOT", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC, WORK = f"{ROOT}/gta6-src", f"{ROOT}/gta6-work"
RAW = {"netflix4k", "launchps5", "launch1", "launch", "trailer1", "trailer2", "netflix", "preload"}   # source footage
SKIP = {"launch1"}                    # identical to launchps5 (same frames)
WHISPER = os.path.expanduser("~/.claude/models/ggml-small.en.bin")
SW, SH = 96, 54                       # the per-frame analysis size
FLOW_FPS = {"billion": 4}             # frames a second on the flow sheets (default 12): the news piece cuts every ~6 s


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    if r.returncode:
        raise SystemExit(f"FAILED {' '.join(map(str, cmd))[:300]}\n{r.stderr[-800:]}")
    return r


def probe(path):
    d = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames,sample_rate,channels,start_time",
                        "-of", "json", path]).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    n, dn = v["r_frame_rate"].split("/")
    a = [s for s in d["streams"] if s["codec_type"] == "audio"]
    return dict(duration=float(d["format"]["duration"]), w=v["width"], h=v["height"], fps=int(n) / int(dn),
                frames=int(v.get("nb_frames") or 0), audio=bool(a), v_start=float(v.get("start_time") or 0),
                a_start=float(a[0].get("start_time") or 0) if a else 0.0)


def proxy(key, src):
    out = f"{WORK}/{key}/proxy.mp4"
    if not os.path.exists(out):
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vf", "scale=-2:480:flags=bicubic", "-fps_mode",
             "passthrough", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-g", "30", "-c:a", "aac", "-b:a",
             "128k", out])
    return out


def frame_stats(path, chunk=1500):
    """Every frame at 96x54: luma mean, mean abs diff to the previous frame, colour-histogram distance, mean RGB.
    Streamed in chunks of frames, so a long film never sits in memory whole."""
    fsz = SW * SH * 3
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vf", f"scale={SW}:{SH}:flags=area",
                          "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    W3 = np.array([0.299, 0.587, 0.114], np.float32)
    luma, diff, hd, rgb = [], [], [], []
    prev_g, prev_h = None, None
    while True:
        buf = p.stdout.read(fsz * chunk)
        if not buf:
            break
        k = len(buf) // fsz
        a = np.frombuffer(buf[:k * fsz], np.uint8).reshape(k, SH, SW, 3).astype(np.float32)
        g = a @ W3
        q = (a // 16).astype(np.int32)                             # 16 bins per channel
        h = np.stack([np.stack([np.bincount(q[i, ..., c].ravel(), minlength=16) for c in range(3)])
                      for i in range(k)]).astype(np.float32) / (SW * SH)
        gg = g if prev_g is None else np.concatenate([prev_g[None], g])
        hh = h if prev_h is None else np.concatenate([prev_h[None], h])
        d = np.abs(np.diff(gg, axis=0)).mean(axis=(1, 2))
        e = 0.5 * np.abs(np.diff(hh, axis=0)).sum(axis=(1, 2)) / 3
        if prev_g is None:
            d, e = np.r_[0.0, d], np.r_[0.0, e]
        luma.append(g.mean(axis=(1, 2))); diff.append(d); hd.append(e); rgb.append(a.mean(axis=(1, 2)))
        prev_g, prev_h = g[-1], h[-1]
    p.wait()
    return np.concatenate(luma), np.concatenate(diff), np.concatenate(hd), np.concatenate(rgb)


def detect_cuts(path, fps, luma, diff, hd):
    """PySceneDetect's content detector (min shot 2 frames) united with a local-ratio test on the histogram distance
    (a cut is a frame much less like its neighbour than its neighbours are like theirs)."""
    from scenedetect import detect, ContentDetector
    cuts = set()
    try:
        for s, _ in detect(path, ContentDetector(threshold=27.0, min_scene_len=2))[1:]:
            cuts.add(s.frame_num)
    except Exception as e:  # noqa: BLE001
        print("scenedetect failed", path, e, flush=True)
    n = len(hd)
    for i in range(1, n):
        lo, hi = max(1, i - 6), min(n, i + 7)
        nb = np.r_[hd[lo:i], hd[i + 1:hi]]
        med = float(np.median(nb)) if len(nb) else 0.0
        if hd[i] > 0.30 and hd[i] > 3.0 * med + 0.05 and diff[i] > 12:
            cuts.add(i)
    return sorted(c for c in cuts if 0 < c < n)


def events(luma):
    """Flash frames (a jump of 40+ luma that falls back within 3 frames), black (< 14) and white (> 238) runs."""
    ev = []
    n = len(luma)
    for i in range(1, n - 1):
        if luma[i] - luma[i - 1] > 40:
            for k in range(1, 4):
                if i + k < n and luma[i + k] < luma[i] - 35:
                    ev.append(dict(kind="flash", frame=i, frames=k))
                    break
    for kind, test in (("black", lambda v: v < 14), ("white", lambda v: v > 238)):
        i = 0
        while i < n:
            if test(luma[i]):
                j = i
                while j + 1 < n and test(luma[j + 1]):
                    j += 1
                ev.append(dict(kind=kind, frame=i, frames=j - i + 1))
                i = j + 1
            else:
                i += 1
    return sorted(ev, key=lambda e: e["frame"])


def audio_analysis(src, key, a0=0.0):
    """Onsets and tempo from a 16 kHz mono mix (spectral flux at 100 Hz), and the wav for the transcript."""
    wav = f"{WORK}/{key}/audio16k.wav"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav])
    raw = open(wav, "rb").read()
    x = np.frombuffer(raw[44:], np.int16).astype(np.float32) / 32768.0
    if len(x) < 16000:
        return wav, [], None, []
    hop, win = 160, 1024
    nfr = (len(x) - win) // hop
    idx = np.arange(win)[None, :] + hop * np.arange(nfr)[:, None]
    spec = np.abs(np.fft.rfft(x[idx] * np.hanning(win), axis=1))
    logm = np.log1p(100 * spec)
    flux = np.r_[0, np.maximum(np.diff(logm, axis=0), 0).sum(axis=1)]
    env = (flux - flux.mean()) / (flux.std() + 1e-9)
    rms = np.sqrt((x[idx] ** 2).mean(axis=1))
    onsets = []
    for i in range(3, len(env) - 3):
        w = env[max(0, i - 50):i + 50]
        if env[i] == env[max(0, i - 5):i + 6].max() and env[i] > w.mean() + 1.2 * w.std() and env[i] > 0.8:
            onsets.append(round((i * hop + win / 2) / 16000 + a0, 3))
    # tempo: autocorrelation of the onset envelope, 70-180 BPM
    e = np.maximum(env, 0)
    ac = np.correlate(e, e, mode="full")[len(e) - 1:]
    lags = np.arange(len(ac))
    lo, hi = int(60 / 180 * 100), int(60 / 70 * 100)
    best = lo + int(np.argmax(ac[lo:hi]))
    bpm = round(6000 / best, 1)
    phase = max(range(best), key=lambda p: e[p::best].sum())
    beats = [round((phase + k * best) / 100 + win / 2 / 16000 + a0, 3) for k in range((len(e) - phase) // best + 1)]
    loud = [round(float(v), 4) for v in rms[::10]]                     # 10 Hz loudness curve
    return wav, onsets, dict(bpm=bpm, beats=beats, strength=round(float(ac[best] / (ac[0] + 1e-9)), 3)), loud


def transcribe(wav, key, a0=0.0):
    out = f"{WORK}/{key}/tr"
    if not os.path.exists(out + ".json"):
        subprocess.run(["whisper-cli", "-m", WHISPER, "-f", wav, "-t", "2", "-ojf", "-of", out, "-ml", "1", "-sow"],
                       capture_output=True)
    try:
        d = json.load(open(out + ".json"))
    except Exception:  # noqa: BLE001
        return [], ""
    words = [dict(t=round(s["offsets"]["from"] / 1000 + a0, 2), w=s["text"].strip()) for s in d.get("transcription", [])
             if s["text"].strip()]
    return words, " ".join(w["w"] for w in words)


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def grab(path, frames, tw):
    """The listed frame numbers of the proxy as PIL images tw wide (one decode pass)."""
    frames = sorted(set(int(f) for f in frames))
    if not frames:
        return {}
    sel = "+".join(f"eq(n,{f})" for f in frames)
    info = probe(path)
    th = round(tw * info["h"] / info["w"] / 2) * 2
    out = {}
    for k in range(0, len(frames), 400):                               # ffmpeg's expression length stays sane
        part = frames[k:k + 400]
        sel = "+".join(f"eq(n,{f})" for f in part)
        raw = run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vf", f"select='{sel}',scale={tw}:{th}",
                   "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]).stdout
        n = len(raw) // (tw * th * 3)
        for j in range(min(n, len(part))):
            out[part[j]] = Image.frombytes("RGB", (tw, th), raw[j * tw * th * 3:(j + 1) * tw * th * 3])
    return out


def sheet(items, cols, tw, out):
    """items: [(PIL image or None, label)] -> a labelled grid."""
    if not items:
        return None
    th = max(im.height for im, _ in items if im is not None) if any(im for im, _ in items) else tw
    f = font(max(11, tw // 16))
    lab = max(14, tw // 13)
    rows = math.ceil(len(items) / cols)
    S = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + lab + 4) + 4), (30, 30, 30))
    d = ImageDraw.Draw(S)
    for k, (im, text) in enumerate(items):
        x, y = 4 + (k % cols) * (tw + 4), 4 + (k // cols) * (th + lab + 4)
        d.text((x + 2, y), text, fill=(255, 230, 80), font=f)
        if im is not None:
            S.paste(im, (x, y + lab))
    S.save(out, quality=82)
    return out


def study(key, title):
    src = f"{SRC}/_drive/{key}.mp4"
    os.makedirs(f"{WORK}/{key}", exist_ok=True)
    meta = probe(src)
    raw_kind = key in RAW
    px = proxy(key, src)
    luma, diff, hd, rgb = frame_stats(px)
    fps = meta["fps"]
    v0 = meta["v_start"]                     # times below are on the player's clock: frame f shows at v0 + f / fps
    T = lambda f: round(v0 + f / fps, 3)
    n = len(luma)
    cuts = detect_cuts(px, fps, luma, diff, hd)
    bounds = [0] + cuts + [n]
    shots = []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if b <= a:
            continue
        m = rgb[a:b].mean(axis=0)
        shots.append(dict(i=len(shots), a=a, b=b - 1, t0=T(a), t1=T(b), frames=b - a,
                          dur=round((b - a) / fps, 3), luma=round(float(luma[a:b].mean()), 1),
                          rgb=[round(float(v)) for v in m], motion=round(float(diff[a + 1:b].mean()) if b - a > 1 else 0, 2)))
    ev = events(luma)
    wav, onsets, tempo, loud = audio_analysis(src, key, meta["a_start"]) if meta["audio"] else (None, [], None, [])
    words, text = transcribe(wav, key, meta["a_start"]) if wav else ([], "")
    # how many cuts land on an onset (within one frame + 20 ms), and the typical offset (negative: the cut leads)
    on = np.array(onsets) if onsets else np.array([1e9])
    offs = [float((T(c) - on[np.argmin(np.abs(on - T(c)))])) for c in cuts]
    sync = [o for o in offs if abs(o) <= 1.0 / fps + 0.02]
    sync_ms = round(1000 * float(np.median(offs)), 1) if offs else None
    sheets = []
    # 1. one frame per shot
    tw = 300 if raw_kind else 320
    mids = [(s["a"] + s["b"]) // 2 for s in shots]
    ims = grab(px, mids, tw)
    per = 48 if raw_kind else 36
    for k in range(0, len(shots), per):
        items = [(ims.get(mids[j]), f"#{shots[j]['i']} {shots[j]['t0']:.2f}-{shots[j]['t1']:.2f}s {shots[j]['frames']}f")
                 for j in range(k, min(len(shots), k + per))]
        p = sheet(items, 8 if raw_kind else 6, tw, f"{WORK}/{key}/shots_{k // per:02d}.jpg")
        sheets.append(p)
    if raw_kind:
        longs = [s for s in shots if s["dur"] >= 2.5]
        pts = {s["i"]: [s["a"] + 1, s["a"] + (s["frames"]) // 3, s["a"] + 2 * s["frames"] // 3, s["b"] - 1] for s in longs}
        ims = grab(px, [f for v in pts.values() for f in v], 240)
        for k in range(0, len(longs), 10):
            items = [(ims.get(f), (f"#{s['i']} {s['t0']:.1f}-{s['t1']:.1f}s" if j == 0 else f"f{f}"))
                     for s in longs[k:k + 10] for j, f in enumerate(pts[s["i"]])]
            sheets.append(sheet(items, 4, 240, f"{WORK}/{key}/long_{k // 10:02d}.jpg"))
    if not raw_kind:
        # 2. flow: 12 frames a second
        step = max(1, round(fps / FLOW_FPS.get(key, 12)))
        fl = list(range(0, n, step))
        ims = grab(px, fl, 300)
        for k in range(0, len(fl), 36):
            items = [(ims.get(f), f"f{f} {T(f):.2f}s") for f in fl[k:k + 36]]
            sheets.append(sheet(items, 6, 300, f"{WORK}/{key}/flow_{k // 36:02d}.jpg"))
        # 3. every cut and every flash at full frame rate: 4 frames before, 4 after
        marks = sorted(set(cuts) | {e["frame"] for e in ev if e["kind"] == "flash"})
        need = {f for c in marks for f in range(c - 4, c + 4) if 0 <= f < n}
        ims = grab(px, need, 240)
        rows = []
        for c in marks:
            rows.append([(ims.get(f) if 0 <= f < n else None,
                          (f"CUT f{f} {T(f):.3f}s" if f == c else f"f{f}")) for f in range(c - 4, c + 4)])
        for k in range(0, len(rows), 6):
            items = [it for r in rows[k:k + 6] for it in r]
            sheets.append(sheet(items, 8, 240, f"{WORK}/{key}/cuts_{k // 6:02d}.jpg"))
    rep = dict(key=key, title=title, source=src, kind="raw footage" if raw_kind else "edit reference", meta=meta,
               frames_read=n, cuts=cuts, cut_times=[T(c) for c in cuts], shots=shots,
               events=[dict(e, t=T(e["frame"])) for e in ev], onsets=onsets, tempo=tempo, loudness_10hz=loud,
               cuts_on_onsets=len(sync), cut_onset_median_offset_ms=sync_ms, transcript=text, words=words,
               luma=[round(float(v), 1) for v in luma] if not raw_kind else None,
               sheets=[p for p in sheets if p])
    json.dump(rep, open(f"{WORK}/{key}/study.json", "w"), indent=1)
    print(f"{key}: {n} frames, {len(shots)} shots, {len(ev)} events, tempo {tempo and tempo['bpm']}, "
          f"{len(sync)}/{len(cuts)} cuts on onsets (median {sync_ms} ms), {len(words)} words, {len(rep['sheets'])} sheets",
          flush=True)
    return rep


if __name__ == "__main__":
    man = [l.rstrip("\n").split("\t") for l in open(f"{SRC}/manifest.tsv") if l.strip()]
    keys = sys.argv[1:] or [k for k, _, _ in man if k not in SKIP]
    titles = {k: t for k, _, t in man}
    big = [k for k in keys if k == "netflix4k"]
    rest = [k for k in keys if k != "netflix4k"]
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(study, k, titles[k]) for k in big + rest]
        for f in futs:
            try:
                f.result()
            except SystemExit as e:
                print(e, flush=True)
