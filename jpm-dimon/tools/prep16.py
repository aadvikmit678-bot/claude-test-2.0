"""v16 media (the user's third batch of notes on the v13 render, 11 Nov).

- `fonts`: TeX Gyre Heros Bold Italic beside the Bold (the roll-up's title is bold slanted Helvetica, as the Hemant
  reel's "AI roll-up strategy"): assets/fonts/TeXGyreHeros-BoldItalic.woff2.
- `flow2`: the user's second Google Flow clip, for "of his own money into the stock. Turn a $500 million" (Drive
  1hclK-tOU74shZPHlevekEbGRXr6HmoRM; 1920x1080, 24 fps, 83 frames, its own captions burned in, its own sound not used).
  Three painted shots: hands over the coins (frames 0-25), the treasurer at his ledger (28-47), the lady with the
  scales (54-82), a soft dissolve between them. Two things are done to it:
  1. the Gemini sparkle in the bottom-right corner (x 1704-1775, y 864-935) is painted out (OpenCV inpaint over the
     sparkle's own shape, one mask for every frame);
  2. it is retimed so that each of its captions comes up on the narration's word. The clip's words and the voice's:
        clip frame   4 Of   10 his   14 own   18 money   30 into   34 the   38 stock,   54 Turned   56 a   58 $500   64 million
        film s      61.16  61.32   61.50   61.72      62.04    62.28   62.36      63.20       63.32  63.54     64.04
     The first shot already runs at the voice's pace; the second comes sooner in the voice (a 1.5x run through the
     dissolve) and the third is spoken at half the clip's pace. The time map is a smooth curve through the anchors
     below (a monotone cubic, so the pace changes gradually and never runs backwards). Where the clip runs slower than
     0.9x the output frames are cross-faded from the two source frames either side; elsewhere each is the nearest frame.
  Output: dimon-src/_v16/flow2_retimed.mp4, 30 fps (the film's clips are 30 fps), no sound (prep2 key FLOW2).
- `strip`: the crimson edge of the reference's picture card (the Sean Desmond trailer, 15.9-18.0 s), drawn here: a
  crimson ground with soft lighter clouds. assets/img2/r16_strip.png.
- `mattes`: the cut-out of Dimon for "standing" (hyperframes remove-background on each clip the spec marks `matte`).

usage: python3 -I tools/prep16.py [fonts] [flow2] [strip] [mattes]     (DIMON_ROOT as for prep2)"""
import json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402
import prep2  # noqa: E402

SRC, IMG, CLIPS = prep2.SRC, prep2.IMG, prep2.CLIPS
PRJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V16 = f"{SRC}/_v16"
SPEC = "media_v16.json"
FPS_IN, FPS_OUT = 24, 30
# (seconds from the clip's first film frame, source frame). The film cuts to the clip 0.05 s before "of" and away from
# it 0.05 s before "loss", 3.44 s later; tools/build16.py checks its own spans against FLOW2_LEN and FLOW2_SPLIT
ANCHORS = [(0.0, 4.0), (0.5833, 18.0), (0.911, 30.0), (1.231, 38.0), (2.071, 54.0), (2.911, 64.0), (3.80, 74.6)]
FLOW2_LEN = 3.80
LOGO = (1688, 848, 1792, 952)          # the box searched for the sparkle (x0, y0, x1, y1)


def fonts():
    from fontTools.ttLib import TTFont
    src = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bolditalic.otf"
    if not os.path.exists(src):
        raise SystemExit("install TeX Gyre Heros first: apt-get install -y fonts-texgyre")
    f = TTFont(src)
    f.flavor = "woff2"
    out = f"{PRJ}/assets/fonts/TeXGyreHeros-BoldItalic.woff2"
    f.save(out)
    print("fonts", os.path.getsize(out), flush=True)


def pchip(xs, ys):
    """A monotone cubic through (xs, ys) (Fritsch-Carlson): returns f(x) and f'(x)."""
    n = len(xs)
    h = [xs[k + 1] - xs[k] for k in range(n - 1)]
    d = [(ys[k + 1] - ys[k]) / h[k] for k in range(n - 1)]
    m = [d[0]] + [0.0] * (n - 2) + [d[-1]]
    for k in range(1, n - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])

    def f(x):
        k = max(0, min(n - 2, next((i for i in range(n - 1) if x < xs[i + 1]), n - 2)))
        t = (x - xs[k]) / h[k]
        h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
        val = h00 * ys[k] + h10 * h[k] * m[k] + h01 * ys[k + 1] + h11 * h[k] * m[k + 1]
        dv = ((6 * t ** 2 - 6 * t) * ys[k] + (3 * t ** 2 - 4 * t + 1) * h[k] * m[k] + (-6 * t ** 2 + 6 * t) * ys[k + 1] +
              (3 * t ** 2 - 2 * t) * h[k] * m[k + 1]) / h[k]
        return val, dv
    return f


def flow2(src=None):
    import cv2
    src = src or f"{V16}/flow2_ref.mp4"
    os.makedirs(V16, exist_ok=True)
    W, H = 1920, 1080
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         check=True, stdout=subprocess.PIPE).stdout
    n = len(raw) // (W * H * 3)
    fr = np.frombuffer(raw, np.uint8).reshape(n, H, W, 3)
    # the sparkle: near-white pixels inside its box in most frames (the painting behind it is dark there), grown 7 px
    x0, y0, x1, y1 = LOGO
    box = fr[:, y0:y1, x0:x1, :].astype(np.int16)
    white = (box.min(axis=3) > 150) & ((box.max(axis=3) - box.min(axis=3)) < 60)
    core = white.mean(axis=0) > 0.5
    mask = np.zeros((H, W), np.uint8)
    mask[y0:y1, x0:x1] = core.astype(np.uint8) * 255
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    ys, xs = np.where(mask > 0)
    print("flow2 frames", n, "sparkle", (xs.min(), ys.min(), xs.max(), ys.max()), int(core.sum()), "px", flush=True)
    clean = np.empty_like(fr)
    for k in range(n):
        clean[k] = cv2.inpaint(fr[k], mask, 9, cv2.INPAINT_TELEA)
    f = pchip([a for a, _ in ANCHORS], [b for _, b in ANCHORS])
    n_out = round(FLOW2_LEN * FPS_OUT)
    out = f"{V16}/flow2_retimed.mp4"
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s",
                            f"{W}x{H}", "-r", str(FPS_OUT), "-i", "-", "-an", "-c:v", "libx264", "-crf", "12", "-preset",
                            "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    log = []
    for j in range(n_out):
        p, dp = f(j / FPS_OUT)
        speed = dp / FPS_IN
        p = min(max(p, 0.0), n - 1.0)
        a, w = int(p), p - int(p)
        b = min(a + 1, n - 1)
        blend = min(1.0, max(0.0, (0.95 - speed) / 0.25))           # 0 at >= 0.95x, 1 at <= 0.70x
        w = blend * w + (1 - blend) * (1.0 if w >= 0.5 else 0.0)
        img = clean[a] if w < 0.004 else clean[b] if w > 0.996 else cv2.addWeighted(clean[a], 1 - w, clean[b], w, 0)
        enc.stdin.write(img.tobytes())
        log.append((j, round(p, 2), round(speed, 2)))
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("ffmpeg failed")
    print("flow2", out, n_out, "frames;", " ".join(f"{j}:{p}@{s}x" for j, p, s in log[::10]), flush=True)


def strip():
    rng = np.random.default_rng(16)
    w, h = 36, 1356
    low = rng.random((h // 60 + 3, 3))
    cloud = np.asarray(Image.fromarray((low * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(
        ImageFilter.GaussianBlur(9)), np.float32) / 255
    cloud = np.clip((cloud - 0.5) * 2.6, 0, 1) ** 1.4                     # a few soft light clouds on the crimson
    fine = np.asarray(Image.fromarray((rng.random((h // 6, w // 6 + 1)) * 255).astype(np.uint8)).resize(
        (w, h), Image.BICUBIC), np.float32) / 255
    base, light = np.array([198, 22, 56], np.float32), np.array([226, 124, 142], np.float32)
    k = np.clip(cloud * 0.85 + (fine - 0.5) * 0.10, 0, 1)[..., None]
    Image.fromarray(np.clip(base + (light - base) * k, 0, 255).astype(np.uint8), "RGB").save(f"{IMG}/r16_strip.png")
    print("strip", (w, h), flush=True)


def mattes():
    m = json.load(open(f"{PRJ}/tools/{SPEC}"))
    for cid, sp in m["clips"].items():
        if not sp.get("matte"):
            continue
        src, out = f"{CLIPS}/{cid}.mp4", f"{CLIPS}/{cid}_cut.webm"
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
            continue
        subprocess.run([("npx.cmd" if os.name == "nt" else "npx"), "--yes", "hyperframes@0.9.2", "remove-background", src,
                        "-o", out, "--json"], check=True, stdout=subprocess.DEVNULL)
        print("matte", cid, flush=True)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["fonts", "flow2", "strip", "mattes"]):
        {"fonts": fonts, "flow2": flow2, "strip": strip, "mattes": mattes}[step]()
