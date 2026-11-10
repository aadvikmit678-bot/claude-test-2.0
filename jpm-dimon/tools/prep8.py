#!/usr/bin/env python3
"""v8 media: "Meet Jamie Dimon, the golden boy of Wall Street, the guy everyone said was next in line to run the biggest
financial company in the world." rebuilt a second time on the opening of the Heath Ledger reel (orozcocreative,
instagram DfXuoMjR0Ru, read frame by frame at its own 60 fps on 10 Nov; notes/v8/heath60.md).

Round 2 (user, 10 Nov): the photos come only from the user's own folder for this part (dimon-src/_heath, copied from
their "jamie dimon" folder and Drive's "heath ledger part of edit"), every face centred like the reel's, the photo
filling the frame; the golden boy is the user's cell picture (the reel's Joker in his cell) with the user's X-ray.

What is made here (assets/img2/h8_*):
- h8_pNN.jpg: each photo 1920x1080 with the face's centre on x = 960 (the reel's faces measure cx 0.47-0.52), its
  vertical place free within the reel's range (cy 0.27-0.54), scaled until the photo covers the frame;
- the reel's devices as frames: the first photo 7.5 % big (pull-back), a blur-in, the vertical whip smears, the dark
  cell plate, its X-ray, its silhouette, the Wall Street picture with the reel's lens blur and its focus window.

Run:  cd jpm-dimon && DIMON_ROOT=<repo> python -I tools/prep8.py [sheet]
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
from PIL import Image, ImageEnhance, ImageFilter, ImageOps  # noqa: E402
import prep2, prep7, faces  # noqa: E402

SRC, IMG = prep2.SRC, prep2.IMG
W, H = 1920, 1080
HEATH = "_heath"
WORK = f"{prep2.PRJ}/../dimon-work/v8"

# id, file, target face width (px), target face-centre y (px)  -- the reel's run: youngest first
PHOTOS = [
    ("h8_p01", "h01_teen.png", 520, 470),          # the teen portrait: big and central, like the reel's child (f0)
    ("h8_p02", "h02_college.png", 420, 420),       # college, long hair
    ("h8_p03", "h03_podium.png", 360, 380),        # the 1980s, at the podium
    ("h8_p04", "h04_portrait90s.png", 420, 400),   # the 1990s studio portrait
    ("h8_p06", "h06_smile.png", 420, 400),
    ("h8_p07", "h07_office_smile.png", 380, 380),
    ("h8_p08", "h08_office.png", 380, 380),
    ("h8_p09", "h09_outdoor.png", 400, 380),
    ("h8_p10", "h10_blue.png", 360, 360),
]
# not used: h05_close (547 px wide) and h11_hearing (700 px) would need 3-4x enlargement to fill the frame centred
FACE_FIX = {}      # file -> (x, y, w, h) when the detector misses


def centre_place(im, f, face_w, cy, cy_lo=300, cy_hi=600, max_up=2.4):
    """The photo scaled and placed so the face's centre sits on x = 960 at a height near cy, covering the frame.
    Returns the frame and what was done."""
    x, y, w, h = f
    fcx, fcy = x + w / 2, y + h / 2
    Ws, Hs = im.size
    best = None
    for ty in np.linspace(cy_lo, cy_hi, 31):
        k_cover = max(960 / fcx, 960 / max(Ws - fcx, 1), ty / max(fcy, 1), (H - ty) / max(Hs - fcy, 1))
        k = max(face_w / w, k_cover)
        cost = abs(ty - cy) / H * 1.2 + max(0.0, k * w - face_w) / face_w
        if best is None or cost < best[0]:
            best = (cost, k, ty)
    _, k, ty = best
    big = im.resize((max(1, round(Ws * k)), max(1, round(Hs * k))), Image.LANCZOS)
    if k > 1.25:
        big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    out = Image.new("RGB", (W, H))
    out.paste(big, (round(960 - fcx * k), round(ty - fcy * k)))
    return out, dict(scale=round(float(k), 3), face_w=int(round(k * w)), face_cy=int(round(ty)),
                     too_soft=bool(k > max_up))


def lens(im, rx=0.40, ry=0.44, sigma=10.0, feather=0.30, dim=0.0):
    """The reel's circular lens blur: sharp inside an ellipse round the centre, defocused (and optionally darker)
    toward the edges."""
    a = np.asarray(im).astype(np.float32)
    b = np.asarray(im.filter(ImageFilter.GaussianBlur(sigma))).astype(np.float32)
    yy, xx = np.mgrid[0:im.height, 0:im.width]
    r = np.sqrt(((xx - im.width / 2) / (im.width * rx)) ** 2 + ((yy - im.height / 2) / (im.height * ry)) ** 2)
    m = np.clip((r - 1) / feather, 0, 1)[..., None]
    out = a * (1 - m) + b * m
    if dim:
        out *= (1 - dim * m)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def focus_window(im, box, inner_shift=(0, 0), outer_sigma=9, outer_dim=0.5, top=230):
    """The reel's focus window (f83-85 at 30 fps; 166-171 at 60): inside the box the picture is sharp and inverted,
    outside it is defocused and dimmed to half."""
    outer = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(outer_sigma))).enhance(1 - outer_dim)
    x0, y0, x1, y1 = box
    sx, sy = inner_shift
    inner = im.crop((x0 - sx, y0 - sy, x1 - sx, y1 - sy))
    outer.paste(prep7.neg(inner, top), (x0, y0))
    return outer


def face_of(im, name):
    f = FACE_FIX.get(name) or faces.face(im)
    if not f:
        raise SystemExit(f"no face found in {name}; add it to FACE_FIX")
    return f


def photos():
    made, info = {}, {}
    for pid, name, fw, cy in PHOTOS:
        im = Image.open(f"{SRC}/{HEATH}/{name}").convert("RGB")
        out, inf = centre_place(im, face_of(im, name), fw, cy)
        out.save(f"{IMG}/{pid}.jpg", quality=93)
        made[pid], info[pid] = out, dict(inf, src=name)
        print(pid, name, inf, flush=True)
    return made, info


def devices(made):
    p1 = made["h8_p01"]
    # the reel's first frame: the photo 7.5 % big, pulling back to full on the next frame
    z = 1.075
    p1.resize((round(W * z), round(H * z)), Image.LANCZOS).crop(
        (round(W * (z - 1) / 2), round(H * (z - 1) / 2), round(W * (z - 1) / 2) + W, round(H * (z - 1) / 2) + H)
    ).save(f"{IMG}/h8_p01z.jpg", quality=92)
    # blur-ins (the reel's f38: the whole frame defocused and a little small, sharp on the next frame)
    for pid in ("h8_p06", "h8_p07"):
        prep7.blur_in(made[pid], sigma=11, scale=0.92).save(f"{IMG}/{pid}b.jpg", quality=90)
    # the vertical whip out of the run's last photo (the reel's f46-48)
    last = made["h8_p10"]
    prep7.vsmear(last, 160).save(f"{IMG}/h8_whip1.jpg", quality=90)
    prep7.vsmear(ImageEnhance.Brightness(ImageOps.grayscale(last).convert("RGB")).enhance(1.6), 720).save(
        f"{IMG}/h8_whip2.jpg", quality=90)


def golden():
    """The golden boy: the user's cell picture (the reel's Joker in his cell), its X-ray and its silhouette."""
    cell = Image.open(f"{SRC}/{HEATH}/h_cell.png").convert("RGB").resize((W, H), Image.LANCZOS)
    plate = prep7.vignette(ImageEnhance.Brightness(cell).enhance(0.9), 0.35)
    plate.save(f"{IMG}/h8_cell.jpg", quality=93)
    # the X-ray: the user's skeleton picture, full frame for its one frame (the reel's f82-83). Its pose is not the
    # cell's (head 316 px against 230, hands 0.66 against 0.90 of the height), so it flashes in whole rather than
    # being laid over him.
    xr = Image.open(f"{SRC}/{HEATH}/h_xray.png").convert("RGB").resize((W, H), Image.LANCZOS)
    prep7.vignette(ImageEnhance.Brightness(xr).enhance(0.92), 0.35).save(f"{IMG}/h8_xray.jpg", quality=92)
    # the silhouette: his figure as flat light grey (#B1B1B1) on the dark picture (the reel's f84-85)
    m = prep7.matte(cell, f"{WORK}/h8_cell_matte.png").getchannel("A")
    sil = Image.composite(Image.new("RGB", (W, H), (177, 177, 177)), plate, m.point(lambda v: 255 if v > 110 else 0))
    sil.save(f"{IMG}/h8_sil.jpg", quality=92)


FOCUS_BOX = (346, 259, 1430, 864)   # the reel's focus window, x 0.18-0.745, y 0.24-0.80


def fill(im, cx=0.5, cy=0.5, zoom=1.0):
    """A 1920x1080 frame cut from a picture: the window centred on (cx, cy) (fractions), zoom >= 1 tighter."""
    a = W / H
    w, h = (im.height * a, im.height) if im.width / im.height > a else (im.width, im.width / a)
    w, h = w / zoom, h / zoom
    x0 = min(max(cx * im.width - w / 2, 0), im.width - w)
    y0 = min(max(cy * im.height - h / 2, 0), im.height - h)
    out = im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((W, H), Image.LANCZOS)
    return out.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))


def wall():
    """Of Wall Street (the user's two Wall Street photos): the reel's Hollywood picture is the Wall St sign, centred,
    dark, its edges in the lens blur, with its focus window; the clean picture after it is the street with the NYSE's
    flags."""
    sign = Image.open(f"{SRC}/{HEATH}/h_wallst_sign.jpg").convert("RGB")
    im = fill(sign, cx=0.44, cy=0.47, zoom=1.08)
    im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.9)).enhance(0.80)
    im = prep7.vignette(lens(im, sigma=11, dim=0.18), 0.5)
    im.save(f"{IMG}/h8_wall.jpg", quality=93)
    focus_window(im, FOCUS_BOX).save(f"{IMG}/h8_wall_focus.jpg", quality=92)
    focus_window(im, FOCUS_BOX, inner_shift=(-70, 60)).save(f"{IMG}/h8_wall_focus2.jpg", quality=92)
    street = Image.open(f"{SRC}/{HEATH}/h_wallst_street.jpg").convert("RGB")
    st = fill(street, cx=0.62, cy=0.5)
    st = ImageEnhance.Brightness(st).enhance(0.86)
    prep7.vignette(lens(st, sigma=9, dim=0.12), 0.45).save(f"{IMG}/h8_wall2.jpg", quality=93)


def sheet(info):
    from PIL import ImageDraw
    cells = [Image.open(f"{IMG}/{pid}.jpg").resize((480, 270), Image.LANCZOS) for pid, *_ in PHOTOS]
    sh = Image.new("RGB", (4 * 486, ((len(cells) + 3) // 4) * 276), "white")
    for i, c in enumerate(cells):
        d = ImageDraw.Draw(c)
        d.line((240, 0, 240, 270), fill=(255, 0, 0))
        pid = PHOTOS[i][0]
        d.text((6, 6), f"{pid} x{info[pid]['scale']} face {info[pid]['face_w']}", fill=(255, 255, 0))
        sh.paste(c, ((i % 4) * 486, (i // 4) * 276))
    sh.save(f"{WORK}/h8_sheet.jpg", quality=85)
    print("sheet", f"{WORK}/h8_sheet.jpg")


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    made, info = photos()
    json.dump(info, open(f"{WORK}/h8_photos.json", "w"), indent=1)
    sheet(info)
    if "sheet" in sys.argv[1:]:
        raise SystemExit
    devices(made)
    golden()
    wall()
    print("prep8: done", flush=True)
