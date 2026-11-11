"""v14 media (the user's notes of 11 Nov on the v13 render).

- `grudge`: "Masking is not proper" in "and a family grudge" (their screenshot circles the edge of Sandy Weill's hair and a
  spot left of his neck). The v6 cut-out (tools/prep6.py grudge) erased the staff member standing behind the couple with
  four hand polygons: one of them cut a straight vertical line through his hair at x 1199, another left a sliver of her
  neck by his collar, and the hedge behind them was still in the matte as a green rim round his hair. Here the matte is
  made again from the same raw cut-out (dimon-work/grudge/couple_raw.png, hyperframes remove-background of the Met Opera
  photo): one polygon traced along his own outline (hair, ear, jaw, collar, shoulder; source pixels, read off 3x crops
  with a 20 px grid), the hedge keyed out of the edge by its green (and the green cast taken off the rim), two
  pixels in and a soft feather. The white edge layer is now a faint wide glow, not an outline.
  Writes assets/img2/gr_couple.png, gr_couple_mb3.png, gr_couple_halo.png (same size and place as before).
- `fonts`: TeX Gyre Heros Bold (the GUST e-foundry's open-licence Helvetica Bold; Debian package fonts-texgyre) as
  assets/fonts/TeXGyreHeros-Bold.woff2, with its licence beside it. The user asked for Helvetica Neue Bold, a commercial
  face that cannot be fetched here; this is the same design (their sample's sans matches it letter for letter). Drop a
  licensed HelveticaNeue-Bold file into assets/fonts and change SANS_FILE in the builder to use it instead.

- `meet`: the blur-in frame and whip smears of the name run's new last portrait.

usage: python3 -I tools/prep14.py [grudge] [fonts] [meet]     (DIMON_ROOT as for prep2)"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402
import prep2  # noqa: E402

ROOT, IMG = prep2.ROOT, prep2.IMG
PRJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUDGE_SRC = f"{prep2.SRC}/Jamie_Dimon_Image_Pack/02_Sandy_Weill/01_Sanford_Weill_Metropolitan_Opera_2009_with_Joan.jpg"
HAIR = [(1140, 120, 1740, 540), (200, 240, 820, 600)]     # Sandy's and Joan's hair against the hedge (source pixels)
# The staff member behind the couple, bounded on the right and below by Sandy Weill's own outline (source pixels):
# down his hair, round his ear, along his jaw to the collar, then along the top of his shoulder
STAFF = [(880, 262), (1212, 262), (1203, 300), (1194, 320), (1183, 340), (1175, 360), (1172, 390), (1173, 420),
         (1178, 442), (1186, 458), (1191, 472), (1198, 500), (1201, 522), (1202, 560), (1205, 584), (1213, 602),
         (1223, 616), (1232, 622), (1240, 640), (1248, 662), (1257, 682), (1263, 702), (1272, 722), (1277, 731),
         (1197, 758), (1138, 773), (1084, 781), (1030, 791), (976, 805), (922, 823), (890, 838), (880, 843)]


def grudge(out_dir=IMG):
    raw = Image.open(f"{ROOT}/dimon-work/grudge/couple_raw.png").convert("RGBA")
    rgb = np.asarray(Image.open(GRUDGE_SRC).convert("RGB")).astype(np.float32)       # colours from the photo itself
    a = np.asarray(raw.getchannel("A")).astype(np.float32)
    m = Image.new("L", raw.size, 0)
    ImageDraw.Draw(m).polygon(STAFF, fill=255)
    a[np.asarray(m) > 0] = 0
    # the hedge: within 22 px of the matte's edge, anything green goes (his hair is grey, skin and cloth are not green)
    solid = (a > 128).astype(np.uint8) * 255
    inner = np.asarray(Image.fromarray(solid).filter(ImageFilter.MinFilter(45)))      # 22 px inside the edge
    band = (solid > 0) & (inner == 0)
    hair = np.zeros(a.shape, bool)             # only round the two heads: the dinner jacket is a green-black, and keying
    for x0, y0, x1, y1 in HAIR:                # its edge by colour follows the photo's JPEG blocks (a jagged shoulder)
        hair[y0:y1, x0:x1] = True
    band &= hair
    green = rgb[..., 1] - (rgb[..., 0] + rgb[..., 2]) / 2
    keep = np.clip(1 - (green - 4.0) / 9.0, 0, 1)
    a = np.where(band, a * keep, a)
    # two pixels in (the mixed rim goes), then a soft feather; the colours stay the photo's own, sharp
    al = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    al = al.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(al).astype(np.float32)
    out = rgb.copy()
    g2 = out[..., 1] - (out[..., 0] + out[..., 2]) / 2                                 # any green cast left on the rim
    out[..., 1] -= np.clip(g2 - 1.0, 0, None) * band
    cut = Image.fromarray(np.dstack([np.clip(out, 0, 255), a]).astype(np.uint8), "RGBA")
    c = cut.resize((1500, round(1500 * cut.height / cut.width)), Image.LANCZOS)
    c.save(f"{out_dir}/gr_couple.png", optimize=True)
    arr = np.asarray(c).astype(np.float32)
    prem = arr.copy()
    prem[..., :3] *= prem[..., 3:4] / 255.0
    n = 16                                                                             # the reel's soft frames 19-20
    p = np.pad(prem, ((0, 0), (n, n), (0, 0)), mode="constant")
    cs = np.cumsum(p, axis=1)
    b = (cs[:, n:, :] - cs[:, :-n, :]) / n
    off = (b.shape[1] - prem.shape[1]) // 2
    b = b[:, off:off + prem.shape[1], :]
    bal = np.clip(b[..., 3:4], 1e-3, 255)
    Image.fromarray(np.dstack([np.clip(b[..., :3] * 255.0 / bal, 0, 255), b[..., 3:4]]).astype(np.uint8), "RGBA").save(
        f"{out_dir}/gr_couple_mb3.png", optimize=True)
    wide = np.asarray(Image.fromarray(np.asarray(c)[..., 3]).filter(ImageFilter.GaussianBlur(16)), np.float32) / 255
    halo = np.zeros(wide.shape + (4,), np.uint8)
    halo[..., :3] = 255
    halo[..., 3] = (np.clip(wide * 0.42, 0, 1) * 255).astype(np.uint8)                 # a glow, not an outline
    Image.fromarray(halo, "RGBA").save(f"{out_dir}/gr_couple_halo.png", optimize=True)
    print("grudge", c.size, flush=True)


def fonts():
    from fontTools.ttLib import TTFont
    src = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf"
    if not os.path.exists(src):
        raise SystemExit("install TeX Gyre Heros first: apt-get install -y fonts-texgyre")
    f = TTFont(src)
    f.flavor = "woff2"
    f.save(f"{PRJ}/assets/fonts/TeXGyreHeros-Bold.woff2")
    for lic in ("/usr/share/doc/fonts-texgyre/copyright", "/usr/share/doc/fonts-texgyre/README-TeX-Gyre-Heros.txt"):
        if os.path.exists(lic):
            shutil.copy(lic, f"{PRJ}/assets/fonts/TeXGyreHeros-{os.path.basename(lic)}.txt".replace(".txt.txt", ".txt"))
    print("fonts", os.path.getsize(f"{PRJ}/assets/fonts/TeXGyreHeros-Bold.woff2"), flush=True)


def meet():
    """The name run's new last portrait (h9_a17, tools/prep8.py aligned it): its blur-in frame and the two whip smears,
    made as prep8 made them for the old last one."""
    import prep7
    from PIL import ImageEnhance, ImageOps
    last = Image.open(f"{IMG}/h9_a17.jpg").convert("RGB")
    prep7.blur_in(last, sigma=11, scale=0.92).save(f"{IMG}/h9_a17b.jpg", quality=90)
    prep7.vsmear(last, 160).save(f"{IMG}/h14_whip1.jpg", quality=90)
    prep7.vsmear(ImageEnhance.Brightness(ImageOps.grayscale(last).convert("RGB")).enhance(1.6), 720).save(
        f"{IMG}/h14_whip2.jpg", quality=90)
    print("meet", flush=True)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["grudge", "fonts", "meet"]):
        {"grudge": grudge, "fonts": fonts, "meet": meet}[step]()
