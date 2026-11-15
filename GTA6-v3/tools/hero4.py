"""'the hero, But GTA lets you be the problem. It lets you be the bad guy' -- reference 3's Palmer Luckey part.

The hero (the user's GTA VI art of Lucia and Jason) with BE THE HERO in big letters behind them (the text between the
sky and a cut-out of the two, tools/text4.cjs), coming in the reference's way: a jagged glowing white line round
their outline on alternate frames and glitch strips across the eyes, then a slow push-in; at "the problem." the
reference's switch -- small inverted cyan squares, a big inverted square over his face, a blur, the new picture (the
user's GTA bad guys: Johnny, Franklin, Niko) arriving blurred under the square, a ghost, then sharp -- held to the end of
"the bad guy". Both pictures through the reference's lens: a slight curve, soft colour-fringed edges, a vignette.
Writes gta6-edit/assets/clips/hero.mp4.   usage: python -I tools/hero4.py [--stills=n,n,...]
"""
import os, subprocess, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl4 as E

FPS, OW, OH = 30, 1920, 1080
REPO = os.path.dirname(os.path.dirname(HERE))
SRCD = os.path.join(REPO, "gta6-src", "v4ref", "hero")
t0, tx, t1 = E.HERO["t0"], E.HERO["tx"], E.HERO["t1"]
N = int(round((t1 - t0) * FPS)) + 5
JX = int(round((tx - t0) * FPS))                 # the first frame of the bad guys
STILLS = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--stills=")), None)

# ---- the hero plate: the art, BE THE HERO, the two of them cut out on top
H1 = cv2.resize(cv2.imread(os.path.join(SRCD, "hero1b.jpg"))[..., ::-1], (OW, OH), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
M1 = cv2.resize(cv2.imread(os.path.join(SRCD, "hero1b_mask.png"), cv2.IMREAD_GRAYSCALE), (OW, OH), interpolation=cv2.INTER_LINEAR)
M1f = cv2.GaussianBlur(M1.astype(np.float32) / 255, (0, 0), 1.6)[..., None]
TXT = cv2.imread(os.path.join(E.PROJ, "assets", "img", "be_the_hero.png"), cv2.IMREAD_UNCHANGED)
T_RGB, T_A = TXT[..., 2::-1].astype(np.float32), TXT[..., 3:4].astype(np.float32) / 255


def hero_plate(text_on):
    bg = H1 * (1 - T_A * text_on) + T_RGB * (T_A * text_on)
    return bg * (1 - M1f) + H1 * M1f


# the jagged outline: the silhouette grown outward, simplified to long straight runs, the bottom edge left open
grown = cv2.dilate(M1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
cnts, _ = cv2.findContours((grown > 127).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
poly = cv2.approxPolyDP(max(cnts, key=cv2.contourArea), 34, True)[:, 0, :]
LINE = [p for p in poly.tolist() if p[1] < OH - 6]


def outline(img):
    layer = np.zeros((OH, OW), np.float32)
    pts = np.array(LINE, np.int32).reshape(-1, 1, 2)
    cv2.polylines(layer, [pts], False, 1.0, 7, cv2.LINE_AA)
    glow = cv2.GaussianBlur(layer, (0, 0), 14) * 2.2 + cv2.GaussianBlur(layer, (0, 0), 4) * 1.2
    a = np.clip(layer + glow, 0, 1)[..., None]
    return img * (1 - a) + 255 * a


# ---- the bad guys: the 700x438 art to the frame's width, heads kept in
src2 = cv2.imread(os.path.join(SRCD, "hero2.jpg"))[..., ::-1]
sc = OW / src2.shape[1]
big = cv2.resize(src2, (OW, int(round(src2.shape[0] * sc))), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
big = big[40:40 + OH]
H2 = np.clip(big * 1.6 - cv2.GaussianBlur(big, (0, 0), 3) * 0.6, 0, 255)          # unsharp after the upscale
H2 = np.clip((H2 - 128) * 1.06 + 128 - 6, 0, 255)                                  # a touch darker and harder


# ---- the reference's lens
ys, xs = np.mgrid[0:OH, 0:OW].astype(np.float32)
xn, yn = (xs - OW / 2) / (OW / 2), (ys - OH / 2) / (OW / 2)
R2 = xn * xn + yn * yn
MAPS = []
for s in (1.0035, 1.0, 0.9965):                  # R, G, B: the fringes grow toward the edges
    f = (1 + 0.06 * R2) / 1.03 * (1 + (s - 1) * R2)
    MAPS.append((xn * f * (OW / 2) + OW / 2, yn * f * (OW / 2) + OH / 2))
R = np.sqrt(R2)
SOFT = np.clip((R - 0.6) / 0.45, 0, 1)[..., None].astype(np.float32)
VIG = (1 - 0.5 * np.clip((R - 0.55) / 0.7, 0, 1) ** 1.5)[..., None].astype(np.float32)


def lens(img):
    out = np.empty_like(img)
    for c in range(3):
        out[..., c] = cv2.remap(img[..., c], MAPS[c][0], MAPS[c][1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    out = out * (1 - SOFT) + cv2.GaussianBlur(out, (0, 0), 7) * SOFT
    return out * VIG


def push(img, k, cx=1000, cy=440):
    s = 1 + k
    A = np.float32([[s, 0, cx * (1 - s)], [0, s, cy * (1 - s)]])
    return cv2.warpAffine(img, A, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def strip(img, x0, y0, x1, y1, dx, gain):
    out = img.copy()
    out[y0:y1, x0:x1] = np.clip(np.roll(img[y0:y1, x0 - 60:x1 + 60], dx, axis=1)[:, 60:60 + (x1 - x0)] * gain, 0, 255)
    return out


def inv_square(img, x, y, w, h):
    out = img.copy()
    blk = 255 - img[y:y + h, x:x + w]
    blk = np.clip(blk * np.float32([0.78, 0.97, 1.12]) + 18, 0, 255)
    out[y:y + h, x:x + w] = blk
    cv2.rectangle(out, (x, y), (x + w - 1, y + h - 1), (245, 250, 255), 2)
    return out


EYES_J, EYES_L = (960, 250, 1250, 312), (790, 470, 1010, 520)   # strips across Jason's and Lucia's eyes (1080p)
FACE_J = (930, 150, 300, 300)                                    # the big square over his face (x, y, w, h)
SMALL = [(1210, 560, 92, 80), (760, 640, 78, 70), (1050, 470, 70, 64)]


def frame(n):
    if n < JX:                                   # ---- the hero
        k = 0.05 * n / max(1, JX - 1)
        text_on = 0.0 if n == 0 else min(1.0, n / 3)
        img = push(hero_plate(text_on), k)
        if n in (0, 2):
            img = outline(img)
        if n in (0, 1, 3, 4):
            img = strip(img, *EYES_J, 26 if n % 2 == 0 else -18, 1.28)
        if n in (1, 3):
            img = strip(img, *EYES_L, -22, 1.22)
        d = JX - n                               # the switch, from the hero's side
        if d in (4, 3):
            for sq in SMALL[: 2 if d == 4 else 3]:
                img = inv_square(img, *sq)
        if d == 2:
            img = inv_square(inv_square(img, *SMALL[0]), *FACE_J)
        if d == 1:
            img = inv_square(cv2.GaussianBlur(img, (0, 0), 9), *FACE_J)
        return lens(img)
    m = n - JX                                   # ---- the bad guys
    k = 0.05 * m / max(1, N - JX - 1)
    img = push(H2, k, 960, 420)
    if m == 0:
        img = inv_square(cv2.GaussianBlur(img, (0, 0), 11) * 0.72, *FACE_J)
    elif m == 1:
        img = inv_square(cv2.GaussianBlur(img, (0, 0), 6) * 0.85, *FACE_J)
    elif m == 2:
        img = inv_square(inv_square(cv2.GaussianBlur(img, (0, 0), 3), *SMALL[2]), *SMALL[0])
    elif m == 3:
        img = img * 0.6 + np.roll(img, 34, axis=1) * 0.4
    return lens(img)


if STILLS:
    d = os.path.join(os.environ.get("HERO_STILLS", "/tmp"), "hero_stills")
    os.makedirs(d, exist_ok=True)
    for n in (int(x) for x in STILLS.split(",")):
        cv2.imwrite(os.path.join(d, f"f{n:03d}.png"), np.clip(frame(n), 0, 255).astype(np.uint8)[..., ::-1])
    print("stills", d, "JX", JX, "N", N)
    sys.exit(0)

enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}",
                        "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "15",
                        "-keyint_min", "15", "-sc_threshold", "0", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        os.path.join(E.PROJ, "assets", "clips", "hero.mp4")], stdin=subprocess.PIPE)
for n in range(N):
    enc.stdin.write(np.clip(frame(n) + 0.5, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close()
assert enc.wait() == 0
print(f"hero: {N} frames | the bad guys from frame {JX} ({tx - t0:.3f} s) | outline {len(LINE)} points")
