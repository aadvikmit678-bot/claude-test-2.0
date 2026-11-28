"""Trimmed from blackrock-open/tools/prep_v17.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import sys

from common import *  # noqa: F401,F403

import prep_v10 as P10

import prep_v16 as P16

Lr, RI, nf = P16.Lr, P16.RI, P10.nf

LUM = P16.LUM

S16 = P16.S16

def r_bgs():
    """a box filter three pixels wide cancels the every-third-column lines exactly; a light blur takes the grain"""
    for src, dst in (("v15_bg_wall.jpg", "v17_bg_wall.jpg"), ("v12_bg_b.jpg", "v17_bg_b.jpg")):
        im = np.asarray(Image.open(f"{IMG}/{src}").convert("RGB")).astype(np.float32)
        im = cv2.filter2D(im, -1, np.full((1, 3), 1 / 3, np.float32), borderType=cv2.BORDER_REFLECT)
        im = cv2.GaussianBlur(im, (0, 0), 1.4)
        save_jpg(im, f"{IMG}/{dst}", q=94)
        print(f"   bgs: {dst}")

def r_count3():
    P10.LOSS_TEXT = "$100 million loss"
    P10.glow_white = P16.glow_white2
    old = P10.CLIPS
    tmp = f"{WORK}/v17tmp"
    os.makedirs(tmp, exist_ok=True)
    P10.CLIPS = tmp
    try:
        P10.r_count()
    finally:
        P10.CLIPS = old
    os.replace(f"{tmp}/v14_count.mp4", f"{CLIPS}/v17_count.mp4")
    print("   count3 -> v17_count.mp4")

def r_date2():
    n = nf(Lr(94), Lr(97))
    src = [f.astype(np.float32) for f in grab(S16["QC"], 8.38, 8)]           # the clock, clean of its captions
    k = len(src)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    hole = np.exp(-(((xx - W / 2) / 470) ** 2 + ((yy - 545) / 330) ** 2))[..., None]
    fm = P16.curved_frame_mask()
    white = 244.0
    masks = {y: P16.text_mask_c(y, P16.HB, 112, W / 2, 545) for y in ("2012", "2011", "2009", "2008")}
    wr = Writer(f"{CLIPS}/v17_date.mp4")
    for i in range(n):
        p = i / max(1, n - 1) * (k - 1)                                       # slowed, blended frame to frame
        a = int(np.floor(p))
        b = min(k - 1, a + 1)
        w = p - a
        clock = cover(src[a] * (1 - w) + src[b] * w)
        s = 1.0 + 0.045 * (i / max(1, n - 1))                                 # a gentle push all the way
        clock = cv2.warpAffine(clock, cv2.getRotationMatrix2D((W / 2, H / 2), 0, s), (W, H), flags=cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_REFLECT)
        g = clock @ LUM
        sep = np.clip(g[..., None] * np.float32([1.10, 0.93, 0.72]) + np.float32([8, 4, 0]), 0, 255)
        img = vignette(cv2.GaussianBlur(P10.concave(sep * (1 - 0.95 * hole), 0.20), (0, 0), 1.3), strength=0.30)
        year, mode = ("2008", "neg") if i < 4 else ("2012", "lift") if i < 10 else ("2011", "n") if i < 14 else \
                     ("2009", "n") if i < 18 else ("2008", "n")
        if mode == "lift":
            img = cv2.GaussianBlur(img * 0.5 + 116, (0, 0), 2.0)
        fr = P16.glow_on(img, masks[year], 1.0)
        if mode == "neg":
            fr = cv2.GaussianBlur(255 - fr, (0, 0), 5.0)
        wr.write(fr * fm + white * (1 - fm) + grain(seed=8800 + i // 2, amt=4))
    wr.close()
    print(f"   date2: {n} frames from the clock's {k} frames")

def r_grid2():
    P16.GRID_DATE, P16.GRID_OUT = "v17_date.mp4", "v17_grid.mp4"
    P16.r_grid()

def r_money2():
    P16.MONEY.update(fink_s=0.70, fink_x=-290, cash_w=560, cash_x=575, cash_y=592, out="v17_money.mp4")
    P16.r_money()
