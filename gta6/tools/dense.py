"""Dense frame sheets for reading a clip frame by frame: every frame (or every Nth for 60 fps and long takes) as small
labelled thumbnails, 100 to a sheet for landscape clips and 72 for vertical ones; the first frame of every detected cut
has a red border, flash frames a yellow one.

  gta6-work/<key>/dense_NN.jpg

usage: python3 -I gta6/tools/dense.py [key ...]"""
import json, math, os, subprocess, sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = f"{ROOT}/gta6-work"
STEP = {"ahhshit": 1, "editm6": 1, "vox": 1, "blade": 2, "montage2": 2, "editmontage": 2, "montage": 2, "willnyc": 3,
        "realwait": 2, "edits": 3, "awshit": 3, "gta5nost": 2, "oldchars": 3, "waiting": 10, "city": 15, "billion": 15}


def font(sz):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def dense(key):
    d = json.load(open(f"{WORK}/{key}/study.json"))
    fps, v0 = d["meta"]["fps"], d["meta"]["v_start"]
    n = d["frames_read"]
    step = STEP.get(key, 1)
    vertical = d["meta"]["h"] > d["meta"]["w"]
    cols, rows, tw = (12, 6, 150) if vertical else (10, 10, 180)
    th = round(tw * d["meta"]["h"] / d["meta"]["w"] / 2) * 2
    cuts = set(d["cuts"])
    flashes = {e["frame"] for e in d["events"] if e["kind"] == "flash"}
    # sample every step-th frame, plus every cut frame and the frame before it
    want = sorted(set(range(0, n, step)) | {c for c in cuts} | {c - 1 for c in cuts if c > 0} | flashes)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f"{WORK}/{key}/proxy.mp4", "-vf",
                          f"scale={tw}:{th}:flags=area", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-"], capture_output=True, check=True).stdout
    fsz = tw * th * 3
    per = cols * rows
    f = font(11)
    lab = 13
    out = []
    for k in range(0, len(want), per):
        part = want[k:k + per]
        S = Image.new("RGB", (cols * (tw + 2) + 2, math.ceil(len(part) / cols) * (th + lab + 2) + 2), (20, 20, 20))
        dr = ImageDraw.Draw(S)
        for j, fr in enumerate(part):
            x, y = 2 + (j % cols) * (tw + 2), 2 + (j // cols) * (th + lab + 2)
            if fr * fsz + fsz <= len(raw):
                S.paste(Image.frombytes("RGB", (tw, th), raw[fr * fsz:fr * fsz + fsz]), (x, y + lab))
            col = (255, 60, 60) if fr in cuts else (255, 220, 0) if fr in flashes else None
            if col:
                dr.rectangle((x - 1, y + lab - 1, x + tw, y + lab + th), outline=col, width=2)
            dr.text((x + 1, y), f"{fr} {v0 + fr / fps:.2f}", fill=col or (200, 200, 200), font=f)
        p = f"{WORK}/{key}/dense_{k // per:02d}.jpg"
        S.save(p, quality=85)
        out.append(p)
    print(key, f"step {step}, {len(want)} frames, {len(out)} sheets, thumbs {tw}x{th}", flush=True)
    return out


if __name__ == "__main__":
    for k in sys.argv[1:] or list(STEP):
        dense(k)
