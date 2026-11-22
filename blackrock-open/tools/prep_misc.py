#!/usr/bin/env python3
"""Clips, cut-outs, stills and textures for the HTML scenes.

  clips     panel shots for the opening line and the hook, the Dimon close-up, the Fink interview, the Rogan clip
            (its 16:9 band, 60 fps), each cut with its own audio so picture and sound stay in sync
  cutouts   the three speaking cut-outs (VP9 + alpha): colour copies and black-and-white copies
  stills    the search box's eleven aligned faces, the BlackRock background (with a soft ring around Fink's face),
            the DJ photos as 16:9 frames, the warm window-light paper, the red card's texture

Run: <venv>/bin/python -I tools/prep_misc.py [clips|cutouts|stills]
"""
import sys

from common import *  # noqa: F401,F403
import timing as TM
from prep_hook import CARTEL_ORDER, aligned_cut


def run(cmd):
    subprocess.run(cmd, check=True)


def cut(src, t0, dur, out, vf=None, fps=None, audio=True, crf=12):
    """A clip from t0 for dur seconds, picture (and sound) together."""
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", src, "-t", f"{dur:.3f}"]
    filt = [vf] if vf else []
    if fps:
        filt.append(f"fps={fps}")
    if filt:
        cmd += ["-vf", ",".join(filt)]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p"]
    cmd += (["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"] if audio else ["-an"])
    run(cmd + [out])


PANEL_SHOTS = {  # id: (panel time, seconds)
    "p_wide": (TM.LINE_T0, 1.75),        # the line starts on the wide, its own picture
    "p_over": (954.40, 1.80),            # from above: the whole table (longer: the aligned "with" .. "financial")
    "p_side": (1195.00, 1.50),           # the stage from the side
    "p_dolly": (1199.00, 2.50),          # behind the chairs, moving
    "p_these": (1192.00, 1.10),          # high wide for "These are the most powerful people"
    "p_dimon": (915.20, 0.70),           # Dimon close-up for the zoom on "That's"
}


def clips():
    for cid, (t, d) in PANEL_SHOTS.items():
        cut(PANEL, t, d, f"{CLIPS}/{cid}.mp4", audio=False)
        print("  ", cid)
    # the opening line's sound, cut the same way as its first picture so they stay in sync
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{TM.LINE_T0:.3f}", "-i", PANEL, "-t", f"{TM.LINE_T1 - TM.LINE_T0:.3f}",
         "-vn", "-ac", "2", "-ar", "48000", f"{AUD}/line.wav"])
    cut(f"{DL}/fink_interview.mp4", 39.30, 1.20, f"{CLIPS}/fink_int.mp4", audio=False)
    # Rogan: the 16:9 picture inside the vertical post (content rows 662-1256), 60 fps
    cut(f"{DL}/rogan_elon.mp4", TM.ROGAN_T0, TM.ROGAN_T1 - TM.ROGAN_T0, f"{CLIPS}/rogan.mp4",
        vf="crop=1048:590:16:664,scale=1920:1080:flags=lanczos,unsharp=5:5:0.6", audio=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{CLIPS}/rogan.mp4", "-vn", "-ac", "2", "-ar", "48000", f"{AUD}/rogan.wav"])
    # the voiceover through "BlackRock."
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/vo/starting_part.mp3", "-t", f"{TM.VO_END:.3f}", "-ac", "2",
         "-ar", "48000", f"{AUD}/vo.wav"])
    print("   clips done")


def cutouts():
    for name, src in (("dimon", "dimon_cut.webm"), ("solomon", "solomon_cut.webm"), ("fink", "fink_cut.webm")):
        s = f"{CUT}/{src}"
        common = ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "18", "-row-mt", "1",
                  "-auto-alt-ref", "0", "-an"]
        run(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", s] + common + [f"{CLIPS}/{name}_cut.webm"])
        run(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", s, "-vf",
             "format=yuva420p,hue=s=0,eq=contrast=1.12:brightness=0.02"] + common + [f"{CLIPS}/{name}_bw.webm"])
        print("  ", name)


def stills():
    # 1. the search box's faces: the eleven aligned cut-outs on the paper tone, square, eyes on one spot
    for name, f, _ in CARTEL_ORDER:
        rgba, _ = aligned_cut(f, fade=90)
        base = np.full((H, W, 3), (236, 231, 224), np.float32)
        im = over(base, rgba)
        sq = im[405 - 300:405 + 340, 960 - 320:960 + 320]
        save_jpg(cv2.resize(sq, (560, 560), interpolation=cv2.INTER_AREA), f"{IMG}/face_{name}.jpg")
    # 2. BlackRock's image for the Fink scene: cover 1920x1080, and a copy with the edges zoom-blurred about his face
    br = np.asarray(Image.open(f"{DL}/blackrock_evil.png").convert("RGB"))
    bg = cover(br)
    save_jpg(bg, f"{IMG}/br_bg.jpg")
    save_jpg(center_focus(bg.astype(np.float32), cx=1180, cy=330, r0=320, r1=900, zoom=0.016, n=10, gblur=3.0),
             f"{IMG}/br_bg_ring.jpg")
    # 3. the DJ photos (press pictures of David Solomon DJ-ing as D-Sol), 16:9
    for i, (fn, cx, cy) in enumerate((("dj_5.jpg", 0.42, 0.40), ("dj_7.jpg", 0.55, 0.30), ("dj_3.jpg", 0.5, 0.42))):
        p = f"/tmp/claude-0/-home-user-claude-test-2-0/dd47b2ff-9452-5314-9518-0cad753f86b8/scratchpad/dsol/{fn}"
        im = np.asarray(Image.open(p).convert("RGB"))
        save_jpg(cover(im, cx=cx, cy=cy, scale=1.06), f"{IMG}/dj_{i + 1}.jpg")
    # 4. warm window-light paper (the Dario / Pattinson paper, tinted to the tfg reel's cream)
    pl = np.asarray(Image.open(f"{ROOT}/assets/tex/paper_light.png").convert("RGB")).astype(np.float32)
    warm = pl * np.array([1.0, 0.955, 0.915], np.float32) + np.array([6, 2, 0], np.float32)
    save_jpg(warm, f"{IMG}/paper_warm.jpg", q=95)
    # 5. the red card: Nvidia's dark red with faint vertical streaks
    rng = np.random.default_rng(7)
    streak = cv2.GaussianBlur(rng.normal(0, 1, (1, W)).astype(np.float32), (0, 0), 3)[0]
    streak = (streak - streak.min()) / (streak.max() - streak.min())
    red = np.zeros((H, W, 3), np.float32)
    red[:] = (164, 8, 10)
    red *= (0.9 + 0.16 * streak)[None, :, None]
    red *= (1 - 0.25 * radial(W / 2, H / 2, 500, 1300, sy=0.7))[..., None]
    red += grain(seed=11, amt=3)
    save_jpg(red, f"{IMG}/red_card.jpg", q=95)
    print("   stills done")


if __name__ == "__main__":
    steps = {"clips": clips, "cutouts": cutouts, "stills": stills}
    for s in (sys.argv[1:] or steps):
        print("--", s)
        steps[s]()
