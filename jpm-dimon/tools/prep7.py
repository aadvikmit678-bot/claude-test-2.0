#!/usr/bin/env python3
"""v7 media: the "Meet Jamie Dimon ... the biggest financial company in the world." section, built on the opening of the
Heath Ledger reel (notes/v7/heath_spec.md), and the pictures the later v7 scenes need.

Every picture of the section is a full 1920x1080 still made here, the way the reel shows its photos:
- face centred (or left of centre under words), at eye level, the photo filling the frame;
- dead still: no push, no drift (the reel's holds measure scale 1.000, 0 px);
- the reel's devices are made as separate frames: negatives (202 - v), blur-in, vertical whip smears, the dark hero,
  its silhouette, the Wall Street sign and its focus window, the Gazette front page with its highlighter.

Run:  cd jpm-dimon && CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I tools/prep7.py
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps  # noqa: E402
import prep2, faces  # noqa: E402

cv2 = faces.cv2
SRC, IMG = prep2.SRC, prep2.IMG
W, H = 1920, 1080
OLD = "jamie-old-images/jamie-old-images"
UNT = "UNT"
UNT_LABEL = (1424, 61, 1896, 143)          # the Untold film's "1985 - 1998 (age 26-42)" box, painted out


def grab(key, t):
    """One frame of a source video at t seconds (exact seek)."""
    tmp = tempfile.mktemp(suffix=".png")
    prep2.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(t), "-i", f"{SRC}/{prep2.V[key]}",
               "-frames:v", "1", tmp])
    im = Image.open(tmp).convert("RGB")
    os.remove(tmp)
    return im


def load(src):
    """src: a path under dimon-src, or KEY@t for a video frame; '#fx,fy,fw,fh' after it limits the face search."""
    s, reg = faces.split(src)
    if "@" in s and not os.path.exists(f"{SRC}/{s}"):
        key, t = s.split("@")
        im = grab(key, float(t))
        if key == UNT:
            im = paint_out(im, UNT_LABEL)
    else:
        im = trim(Image.open(f"{SRC}/{s}").convert("RGB"))
    return im, reg


def trim(im, thr=232):
    """Crop away a photo's white paper margins (scanned prints)."""
    a = np.asarray(ImageOps.grayscale(im)).astype(np.float32)
    cols = np.where(a.mean(0) < thr)[0]
    rows = np.where(a.mean(1) < thr)[0]
    if len(cols) < 10 or len(rows) < 10:
        return im
    x0, x1, y0, y1 = int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())
    pad = 4
    return im.crop((min(x0 + pad, x1), min(y0 + pad, y1), max(x1 - pad, x0 + 1), max(y1 - pad, y0 + 1)))


def paint_out(im, box):
    a = np.asarray(im).copy()
    m = np.zeros(a.shape[:2], np.uint8)
    x0, y0, x1, y1 = box
    m[y0:y1, x0:x1] = 255
    return Image.fromarray(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA))


def place(im, f, face_w, cx, cy, dx=0.0, dy=0.0, max_up=1.6):
    """The photo scaled so the face is face_w wide with its centre at (cx, cy). If the photo cannot then cover the
    frame, it is scaled up (at most max_up x) or shifted (at most 18 % of the frame); any edge still bare is filled
    with a blurred, enlarged copy of the photo, as faces.align does."""
    x, y, w, h = f
    fcx, fcy = x + w / 2 + dx * w, y + h / 2 + dy * h
    k0 = face_w / w
    best = None
    for up in np.linspace(1.0, max_up, 13):
        k = k0 * up
        for sx in np.linspace(-0.18 * W, 0.18 * W, 9):
            for sy in np.linspace(-0.18 * H, 0.18 * H, 9):
                tx, ty = cx + sx, cy + sy
                l, t = tx - fcx * k, ty - fcy * k
                r, b = l + im.width * k, t + im.height * k
                bare = max(0, l) * H + max(0, W - r) * H + max(0, t) * W + max(0, H - b) * W
                cost = bare / (W * H) * 40 + (up - 1) * 1.2 + (abs(sx) / W + abs(sy) / H) * 2.0
                if best is None or cost < best[0]:
                    best = (cost, k, tx, ty, bare)
    _, k, tx, ty, bare = best
    big = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    if k > 1.25:
        big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    out = Image.new("RGB", (W, H))
    if bare > 0:
        out.paste(im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(36)), (0, 0))
    out.paste(big, (round(tx - fcx * k), round(ty - fcy * k)))
    return out


def photo(src, face_w=330, cx=960, cy=520, dx=0.0, dy=0.0, bw=False, max_up=1.6, face=None):
    im, reg = load(src)
    f = face or faces.face(im, reg)
    if not f:
        raise SystemExit(f"no face in {src}")
    out = place(im, f, face_w, cx, cy, dx, dy, max_up)
    if bw:
        out = ImageOps.grayscale(out).convert("RGB")
    return out


def neg(im, top=202):
    """The reel's negative: 202 - v on each channel (measured: inside = -1.00 * v + 204 / 199 / 203)."""
    a = np.asarray(im).astype(np.int16)
    return Image.fromarray(np.clip(top - a, 0, 255).astype(np.uint8))


def blur_in(im, sigma=11, scale=0.93):
    """The reel's blur-in frame (f19): the whole picture defocused and a little small."""
    small = im.resize((round(W * scale), round(H * scale)), Image.LANCZOS)
    out = im.filter(ImageFilter.GaussianBlur(sigma * 1.6))
    out.paste(small, ((W - small.width) // 2, (H - small.height) // 2))
    return out.filter(ImageFilter.GaussianBlur(sigma))


def vsmear(im, n):
    """A vertical motion blur n px long (the reel's whip, f23-24)."""
    a = np.asarray(im).astype(np.float32)
    p = np.pad(a, ((n, n), (0, 0), (0, 0)), mode="edge")
    cs = np.cumsum(p, axis=0)
    out = (cs[n:] - cs[:-n]) / n
    off = (out.shape[0] - a.shape[0]) // 2
    return Image.fromarray(np.clip(out[off:off + a.shape[0]], 0, 255).astype(np.uint8))


def dark_bw(im, luma=24, contrast=1.35):
    """The reel's Joker plate: black-and-white, very dark (mean luma 19), contrasty."""
    g = ImageOps.grayscale(im)
    g = ImageEnhance.Contrast(g).enhance(contrast)
    a = np.asarray(g).astype(np.float32)
    a = a * (luma / max(a.mean(), 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGB")


def vignette(im, amount=0.45):
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    m = 1 - amount * np.clip(r - 0.35, 0, 1) ** 1.4
    a = np.asarray(im).astype(np.float32) * m[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def matte(im, out_png):
    """A person matte (hyperframes remove-background) of a still, cached."""
    if not os.path.exists(out_png):
        tmp = tempfile.mktemp(suffix=".png")
        im.save(tmp)
        prep2.run(["npx", "--yes", "hyperframes@0.9.2", "remove-background", tmp, "-o", out_png, "--json"])
        os.remove(tmp)
    return Image.open(out_png).convert("RGBA")


# ---------------------------------------------------------------------------------------------------------------
# The shot list of the section (notes/v7/heath_spec.md, "Mapping onto our line")
# ---------------------------------------------------------------------------------------------------------------
NAME_RUN = [  # id, source, face width, bw  -- youngest first (the reel's child -> teen run)
    ("mt_p01", f"{OLD}/jamie-old-image-03.jpg", 300, False),                 # at college, long hair (B&W photo)
    ("mt_p02", f"{OLD}/jamie-old-image-01.jpg#0,0,0.55,0.6", 400, False),    # Commercial Credit, 1986, at the podium
    ("mt_p03", "UNT@546.2", 430, False),                                     # the B&W studio portrait (close)
    ("mt_p04", f"{OLD}/jamie-old-image-05.jpg#0.45,0,0.55,0.65", 300, False),  # laughing, Weill beside him
    ("mt_p05", "MPB@700.0", 330, False),                                     # the young banker, over his shoulder
    ("mt_p06", "UNT@505.6", 430, False),                                     # the 1990s, mid-sentence
    ("mt_p07", "UNT@582.4", 300, False),                                     # smiling with a colleague
    ("mt_p08", "MPB@871.0", 330, False),                                     # the Travelers years
    ("mt_p09", "MPB@720.0#0.5,0,0.5,0.8", 300, False),                       # beside Weill
    ("mt_p11", "MPB@929.5", 300, False),                                     # Citigroup, 1998, at the citi podium
]
GUY_RUN = [  # words on the right: the face left of centre (the reel's "was the guy", f63-76)
    ("mt_g01", "MPB@747.6#0.5,0,0.5,0.8", 300, False),                       # with Weill (Dimon on the right)
    ("mt_g03", "UNT@592.8#0,0.25,0.5,0.75", 300, False),                     # the Times: "Becoming His Own Man"
    ("mt_g05", "MPB@1007.0#0.5,0,0.5,0.9", 300, False),                      # with Weill under the citibank sign
]
HERO = "UNT@550.2"                       # the golden boy: young Dimon sitting by the window, the towers behind him
TOWER = ("MPB", 855.6)                   # Citigroup's tower from the air (video; prep2 cuts it)
CITI = "MPB@843.0"                       # CITIGROUP: Weill and Reed announce the merger, 1998
WALLST = ("WSMONT", 2.05)                # the green WALL ST sign over the flag (the reel's Hollywood sign)
GAZETTE = "_drive/The Wall Street Gazette Front Page.png"
FOCUS_BOX = (346, 259, 1430, 864)        # the reel's focus window (x 0.18-0.745, y 0.24-0.80)
NEG_TOP = (624, 0, 1295, 581)            # the reel's top negative rectangle (f32)


def gazette():
    """The client's front page, cropped to 16:9 (the masthead to the photos), with its yellow highlight removed
    (gz_clean) so the highlighter can be drawn on, and the original (gz_orig) for the stroke to reveal."""
    im = Image.open(f"{SRC}/{GAZETTE}").convert("RGB")
    a = np.asarray(im).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hsv = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    # the highlight: as bright as the paper but twice as saturated (S 158 vs 86), in the headline band only
    yellow = (hsv[..., 0] > 12) & (hsv[..., 0] < 32) & (hsv[..., 1] > 125) & (hsv[..., 2] > 150)
    yellow[:150] = False
    yellow[400:] = False
    # keep the highlight itself: the components that touch the large blob around GOLDEN BOY
    closed = cv2.morphologyEx(yellow.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(closed)
    big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    region = (lab == big).astype(np.uint8)
    cnts, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    region = cv2.drawContours(np.zeros_like(region), cnts, -1, 1, -1) > 0          # holes (the letters) filled
    ys, xs = np.where(region)
    box = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    # undo the marker like a multiply layer: inside the stroke every pixel is scaled by paper / highlight colour, so
    # the yellow becomes paper and the ink stays ink (the soft ragged edge by saturation)
    hl = a[yellow & region].mean(0)
    pap = a[(hsv[..., 1] < 100) & (hsv[..., 2] > 190)].mean(0)
    alpha = np.clip((hsv[..., 1] - 86) / (158 - 86), 0, 1)
    alpha = np.where(hsv[..., 2] <= 120, 1.0, alpha) * region
    alpha = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 1.2)
    clean = a * (1 + alpha[..., None] * (pap / hl - 1))
    clean = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8))
    k = W / im.width                                      # 1536 -> 1920 wide, 1280 tall; keep y 40-1120
    top = 40
    def fit(x):
        return x.resize((W, round(im.height * k)), Image.LANCZOS).crop((0, top, W, top + H))
    fit(clean).save(f"{IMG}/gz_clean.jpg", quality=92)
    fit(im).save(f"{IMG}/gz_orig.jpg", quality=92)
    # the two portraits: find them as the large dark-grey boxes in the lower left
    gray = np.asarray(ImageOps.grayscale(im)).astype(np.float32)
    rows = slice(430, 990)
    boxes = []
    for xs0, xs1 in ((20, 452), (452, 840)):
        sub = gray[rows, xs0:xs1] < 150
        cols = np.where(sub.mean(0) > 0.35)[0]
        rws = np.where(sub.mean(1) > 0.35)[0]
        boxes.append((xs0 + int(cols.min()), 430 + int(rws.min()), xs0 + int(cols.max()), 430 + int(rws.max())))
    negp = im.copy()
    for (x0, y0, x1, y1) in boxes:
        negp.paste(neg(im.crop((x0, y0, x1, y1)), 225), (x0, y0))
    fit(negp).save(f"{IMG}/gz_neg.jpg", quality=92)
    to_film = lambda bx: [round(bx[0] * k), round(bx[1] * k - top), round(bx[2] * k), round(bx[3] * k - top)]
    info = {"highlight": to_film(box), "portraits": [to_film(bx) for bx in boxes]}
    # the subhead line "THE HEIR APPARENT ..." : the dark-ink rows between the headline and the photos
    sub_rows = np.where((gray[360:440, 40:1500] < 90).mean(1) > 0.02)[0]
    info["subhead"] = to_film((40, 360 + int(sub_rows.min()), 1500, 360 + int(sub_rows.max())))
    sub_cols = np.where((gray[360 + sub_rows.min():360 + sub_rows.max(), :] < 90).mean(0) > 0.04)[0]
    info["subhead"][0] = round(int(sub_cols.min()) * k)
    info["subhead"][2] = round(int(sub_cols.max()) * k)
    # the word gaps of the subhead, to end the second stroke after "THE HEIR APPARENT"
    ink_cols = (gray[360 + sub_rows.min():360 + sub_rows.max(), :] < 90).mean(0) > 0.04
    gaps, run = [], 0
    for x in range(int(sub_cols.min()), int(sub_cols.max())):
        run = run + 1 if not ink_cols[x] else 0
        if run == 9:
            gaps.append(x - 4)
    info["subhead_gaps"] = [round(g * k) for g in gaps]
    json.dump(info, open(f"{IMG}/gz_boxes.json", "w"))
    print("gazette", info, flush=True)


def meet():
    made = {}
    for (pid, src, fw, bw) in NAME_RUN:
        made[pid] = photo(src, fw, 960, 520, bw=bw, max_up=2.3)
        made[pid].save(f"{IMG}/{pid}.jpg", quality=92)
    for (pid, src, fw, bw) in GUY_RUN:
        made[pid] = photo(src, fw, 700, 520, bw=bw, max_up=2.0)
        made[pid].save(f"{IMG}/{pid}.jpg", quality=92)
    # the lead-in: the first photo 7 % big (pulls back on the next frame), its negative over the face, the next photo's
    p1, p2 = made["mt_p01"], made["mt_p02"]
    p1.resize((round(W * 1.075), round(H * 1.075)), Image.LANCZOS).crop(
        (round(W * 0.0375), round(H * 0.0375), round(W * 0.0375) + W, round(H * 0.0375) + H)).save(f"{IMG}/mt_p01z.jpg", quality=92)
    neg(p1).save(f"{IMG}/mt_p01n.jpg", quality=92)
    neg(p2).save(f"{IMG}/mt_p02n.jpg", quality=92)
    # the blur-in (on the 7th photo) and the vertical whip out of the last one
    blur_in(made["mt_p07"]).save(f"{IMG}/mt_p07b.jpg", quality=90)
    last = made["mt_p11"]
    vsmear(last, 150).save(f"{IMG}/mt_whip1.jpg", quality=90)
    vsmear(ImageEnhance.Brightness(ImageOps.grayscale(last).convert("RGB")).enhance(1.6), 700).save(
        f"{IMG}/mt_whip2.jpg", quality=90)
    # the golden boy: the dark black-and-white hero (the reel's Joker), its silhouette, and the top negative box
    him, _ = load(HERO)
    f = faces.face(him)
    hero = place(him, f, 250, 1010, 380) if f else him.resize((W, H))
    plate = vignette(dark_bw(hero, 26), 0.5)
    plate.save(f"{IMG}/mt_hero.jpg", quality=92)
    m = matte(hero, f"{prep2.PRJ}/../dimon-work/v7/mt_hero_matte.png").getchannel("A")
    sil = Image.composite(Image.new("RGB", (W, H), (177, 177, 177)), plate, m.point(lambda v: 255 if v > 110 else 0))
    sil.save(f"{IMG}/mt_hero_sil.jpg", quality=92)
    face_src = made["mt_p03"]                              # the studio portrait, bright, as the reel's f32 negative
    x0, y0, x1, y1 = NEG_TOP
    box = neg(face_src.crop((960 - (x1 - x0) // 2, 520 - 300, 960 + (x1 - x0) // 2, 520 - 300 + (y1 - y0))), 236)
    top = plate.copy()
    top.paste(box, (x0, y0))
    top.save(f"{IMG}/mt_hero_top.jpg", quality=92)
    # of Wall Street: the WALL ST sign, dark and vignetted like the reel's Hollywood sign; its focus window frame
    sign = grab(*WALLST).resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2))
    sign = vignette(ImageEnhance.Brightness(ImageEnhance.Color(sign).enhance(0.85)).enhance(0.82), 0.55)
    sign.save(f"{IMG}/mt_wall.jpg", quality=92)
    neg(sign).save(f"{IMG}/mt_wall_n.jpg", quality=92)       # the next shot enters as a negative (the reel's f43)
    outer = ImageEnhance.Brightness(sign.filter(ImageFilter.GaussianBlur(9))).enhance(0.5)
    fx0, fy0, fx1, fy1 = FOCUS_BOX
    outer.paste(neg(sign.crop(FOCUS_BOX)), (fx0, fy0))
    outer.save(f"{IMG}/mt_wall_focus.jpg", quality=92)
    # in the world: CITIGROUP, 1998
    citi = grab("MPB", 843.0)
    citi.save(f"{IMG}/mt_citi.jpg", quality=92)
    gazette()
    print("meet: made", len(made) + 12, "pictures", flush=True)


if __name__ == "__main__":
    meet()
