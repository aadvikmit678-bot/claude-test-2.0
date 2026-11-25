#!/usr/bin/env python3
"""v17 renderers (Nov 25): the user's notes on the v16 full render.

  bgs     the Fink frame's two backgrounds without the screen-line texture ("remove any effects in the background")
  card    "A company that's never made": the card's footage as six pictures at equal times (no money press)
  count3  the counter with "$100 million loss" -- no full stop (none anywhere, the user)
  date2   "When the 2008": the clock playing (its gears moving, slowed to fill the frame), a gentle push -- "more animated,
          a video playing inside it"
  grid2   the grid again, its datamosh in from the new date frame
  page2   "threw out years ago": a video of Fink (talking) at the same faint opacity on the page, not a still
  money2  the hand-off with Fink smaller and further left, so "He came out of that crisis" can sit in the middle, bigger

Run: <venv>/bin/python -E -s tools/prep_v17.py [names...]
"""
import sys

from common import *  # noqa: F401,F403
import timing as TM
import prep_v10 as P10
import prep_v16 as P16

T, B, F = TM.T, TM.B, TM.F
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


CARD = [("BRL", 167.05, 0.42, 0.56, 1.22), ("HOW", 193.0, 0.46, 0.56, 1.2), ("BRL", 172.0, 0.45, 0.58, 1.2),
        ("HOW", 210.0, 0.44, 0.57, 1.18), ("HOW", 175.0, 0.45, 0.57, 1.2), ("HOW", 221.0, 0.44, 0.58, 1.2)]


def r_card():
    a, b = B["made"][0], F(T["a4"] - TM.LEAD)
    n = nf(a, b)
    per = [n // len(CARD) + (1 if k < n % len(CARD) else 0) for k in range(len(CARD))]
    wr = Writer(f"{CLIPS}/v17_card.mp4", w=960, h=540)
    for (key, t0, cx, cy, z), m in zip(CARD, per):
        for fr in P16.tile_clip(key, t0, m, 960, 540, cx, cy, z):
            wr.write(grade(fr, sat=1.0, contrast=1.05))
    wr.close()
    print(f"   card: {n} frames, {len(CARD)} pictures of {per}")


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


def r_page2():
    """the Kalanick reel's "8 years later" page with the man's picture faint behind it -- ours Fink talking (his
    interview), grey, soft, fading in at its 10 fps steps to a quarter, the edges into the page"""
    p0, m0 = Lr(108), F(RI(112))
    n = nf(p0, m0)
    frs = grab(S16["FIN"], 1.0, n, fps=FPS)
    w0, h0, _ = probe(S16["FIN"])
    z, cx, cy = 1.55, 0.70, 0.40
    cw, ch = w0 / z, h0 / z
    x0 = int(np.clip(cx * w0 - cw / 2, 0, w0 - cw))
    y0 = int(np.clip(cy * h0 - ch / 2, 0, h0 - ch))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fade = np.clip(np.exp(-(((xx - 960) / 930) ** 4 + ((yy - 560) / 660) ** 4)), 0, 1)[..., None]
    page = np.float32([246, 246, 244])
    steps = [0.0, 0.07, 0.13, 0.18, 0.22, 0.25]
    wr = Writer(f"{CLIPS}/v17_page.mp4")
    for i, f in enumerate(frs):
        g = f.astype(np.float32)[y0:y0 + int(ch), x0:x0 + int(cw)] @ LUM
        g = cv2.GaussianBlur(cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 1.4)
        o = steps[min(len(steps) - 1, i // 6)] * fade
        wr.write(page * (1 - o) + g[..., None] * o)
    wr.close()
    print(f"   page2: {n} frames ({p0:.3f}-{m0:.3f})")


def r_money2():
    P16.MONEY.update(fink_s=0.70, fink_x=-290, cash_w=560, cash_x=575, cash_y=592, out="v17_money.mp4")
    P16.r_money()


ALL = {"bgs": r_bgs, "card": r_card, "count3": r_count3, "date2": r_date2, "grid2": r_grid2, "page2": r_page2,
       "money2": r_money2}

if __name__ == "__main__":
    for nm in sys.argv[1:] or list(ALL):
        print(f"-- {nm}")
        ALL[nm]()
