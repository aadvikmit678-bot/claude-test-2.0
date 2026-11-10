"""v10 stills for the Meet section (S07), from the user's uploads of 10 Nov (night) to the Drive folder
"heath ledger part of edit":
- five front portraits, aligned like v9's (the same face box on the same eye line, tools/prep8.py fb);
- the X-ray: their "jamie skeleton 2.0", the cell picture itself with the skeleton drawn in, so it lays over the cell;
- their parchment map of the United States, for the reel's map pan: a large plate and its pan-blurred copy;
- their "montage jamie" (Dimon at the desk in the rounded frame), for the Wall Street montage's shot at 4.9 s.
usage: python -I tools/prep10.py [desk]   (DIMON_ROOT set, as for prep8)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import prep8  # noqa: E402
from PIL import ImageChops, ImageDraw, ImageFilter, ImageOps  # noqa: E402
from prep8 import Image, ImageEnhance, prep7, SRC, IMG, HEATH, W, H  # noqa: E402

NEW = [("h9_a18", "h18_front1.png"), ("h9_a19", "h19_front2.png"), ("h9_a20", "h20_front3.png"),
       ("h9_a21", "h21_front4.png"), ("h9_a22", "h22_front5.png")]


def xray():
    xr = Image.open(f"{SRC}/{HEATH}/h_xray2.png").convert("RGB").resize((W, H), Image.LANCZOS)
    prep7.vignette(ImageEnhance.Brightness(xr).enhance(0.95), 0.35).save(f"{IMG}/h10_xray.jpg", quality=92)


def usmap(width=2880, blur=84):
    m = Image.open(f"{SRC}/{HEATH}/h_map_usa.png").convert("RGB")
    big = m.resize((width, round(width * m.height / m.width)), Image.LANCZOS)
    big = ImageEnhance.Brightness(ImageEnhance.Color(big).enhance(0.82)).enhance(0.74)   # the reel's map is dim
    big.save(f"{IMG}/h10_map.jpg", quality=92)
    a = np.asarray(big).astype(np.float32)                                              # the pan's motion blur
    pad = np.pad(a, ((0, 0), (blur // 2 + 1, blur - blur // 2), (0, 0)), mode="edge")
    c = np.cumsum(pad, axis=1)
    out = (c[:, blur:] - c[:, :-blur])[:, :a.shape[1]] / blur
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f"{IMG}/h10_map_blur.jpg", quality=90)
    print("map", big.size, flush=True)


def desk():
    """The user's 'montage jamie': Dimon at the desk in the rounded frame, made to stand in for the shot at 4.9 s of
    their Wall Street montage. Its four states there: a gold line drawing, small, on black (one frame); the picture;
    a defocus; black-and-white."""
    d = Image.open(f"{SRC}/{HEATH}/h_desk.png").convert("RGB").resize((W, H), Image.LANCZOS)
    d.save(f"{IMG}/h10_desk.jpg", quality=93)
    d.filter(ImageFilter.GaussianBlur(16)).save(f"{IMG}/h10_desk_blur.jpg", quality=90)
    g = ImageOps.autocontrast(ImageOps.grayscale(d), cutoff=1).convert("RGB")
    ImageEnhance.Contrast(g).enhance(1.12).save(f"{IMG}/h10_desk_bw.jpg", quality=93)
    sw, sh = round(W * 0.64), round(H * 0.64)
    small = d.resize((sw, sh), Image.LANCZOS)
    e = ImageOps.grayscale(small).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(0.9))
    e = ImageOps.autocontrast(e, cutoff=0.5).point(lambda v: min(255, int(v * 2.4)))
    gold = ImageOps.colorize(e, (0, 0, 0), (238, 206, 122))
    mix = ImageChops.screen(ImageEnhance.Brightness(small).enhance(0.42), gold)
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=72, fill=255)
    canvas = Image.new("RGB", (W, H), (4, 4, 4))
    canvas.paste(mix, ((W - sw) // 2, (H - sh) // 2), mask)
    canvas.save(f"{IMG}/h10_desk_line.jpg", quality=92)


if __name__ == "__main__":
    if "desk" not in sys.argv[1:]:
        prep8.align_fb(NEW)
        xray()
        usmap()
    desk()
