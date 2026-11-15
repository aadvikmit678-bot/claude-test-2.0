"""Shot catalog: scene-detect each source clip and tile one labelled thumbnail per shot.
usage: python -I catalog.py <src_dir> <out_dir>"""
import json, os, re, subprocess, sys
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
ALIAS = {  # Drive names the user gave (matched by file size) -> local file
 "news_1billion": "_dl/news/news.mp4",
 "awshit": "Aw shit, here we go again (Original) Grand Theft Auto San Andreas.mp4",
 "t1": "Grand Theft Auto VI Trailer 1.mp4",
 "t2": "Grand Theft Auto VI Trailer 2.mp4",
 "launch": "Grand Theft Auto VI Launch Trailer.mp4",
 "launch4k": "Grand Theft Auto VI Launch Trailer (1).mp4",
 "netflix_look": "Grand Theft Auto VI An Extended Look   Now Playing   Netflix.mp4",
 "preload": "Grand Theft Auto VI Pre-Load Now.mp4",
 "netflix_ext": "GTA 6 4K Gameplay Trailer FULL NETFLIX EXTENDED.mp4",
 "vc10": "Grand Theft Auto Vice City 10th Anniversary Edition Trailer [0-72.7s].mp4",
 "vcde": "How the Vice City Definitive Edition should have looked [0-72.7s].mp4",
 "vc_panzer": "The Rhino Tank - Steal it like a Man - Keep it Forever GTA VC [0-149.2s].mp4",
 "took13": "Pinterest video #1086986060086955075 [0-8.3s].mp4",
 "kid": "Pinterest video #1125829606870167260 [0-17.4s].mp4",
 "fastclip": "Pinterest video #597008494394941567 [0-2.1s].mp4",
 "millions": "Men in black [0-8s].mp4",
 "freedom": "From Klickpin.com- Need fresh inspiration Refresh these simple healthy habit ideas perfect for saving sharing and recreating later designed to fee.mp4",
 "escape": "From Klickpin.com- Polished nail design inspiration that look expensive while staying practical realistic and beginner friendly for busy people wh (1).mp4",
 "adulthood": "From Klickpin.com- Polished nail design inspiration that look expensive while staying practical realistic and beginner friendly for busy people wh.mp4",
 "klick_wedding": "From Klickpin.com- Classy wedding centerpiece ideas that can help you create a more curated classy and Pinterest-worthy result for beginners who w.mp4",
 "gta5_goodbye": "Video by shamsycreates [0-22s].mp4",
 "waiting_gta6": "Video by lucanox.2 [0-34.05s].mp4",
 "waiting_gta5_old": "Video by saudalhomud [0-16.96s].mp4",
 "old_chars_meetup": "Video by kaye.creatives [0-54.4s].mp4",
 "gta5_nostalgia": "Video by bykeipker [0-37.3s].mp4",
 "gta_city": "Video by __lio.x__ [0-83.9s].mp4",
 "montage": "Video by _brooklynfilms_ [0-28.9s].mp4",
 "montage2": "Video by swxft_404 [0-16s].mp4",
 "edit_montage": "Video by nevalcuts [0-12s].mp4",
 "edit_montage_gta6": "Video by 6u.x9 [0-13s].mp4",
 "edits": "Video by matthewhoyos [0-15s].mp4",
 "edit_awshit": "Video by ntprimee [0-20s].mp4",
 "vox_cut": "Video by kiuzr [0-15s].mp4",
 "blade": "Video by blade.fxs [0-32.6s].mp4",
 "metav3rse": "Video by metav3rse [0-23.2s].mp4",
 "will_nyc": "Video by will__nyc [0-15s].mp4",
}
only = set(sys.argv[3:])
index = {}
for alias, rel in ALIAS.items():
    if only and alias not in only:
        continue
    path = os.path.join(SRC, rel)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                               capture_output=True, text=True).stdout.strip())
    if dur > 400:   # the 27-min gameplay reel: one frame every 12 s instead of shot detection
        cuts = [round(t * 12.0, 2) for t in range(int(dur // 12))]
    else:
        log = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vf",
                              "scale=320:-2,select='gt(scene,0.28)',showinfo", "-an", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        cuts = [0.0] + [float(x) for x in re.findall(r"pts_time:([0-9.]+)", log)]
        cuts = [c for i, c in enumerate(cuts) if i == 0 or c - cuts[i - 1] > 0.25]
    shots = [(c, cuts[i + 1] if i + 1 < len(cuts) else dur) for i, c in enumerate(cuts)]
    index[alias] = {"file": rel, "duration": dur, "shots": [[round(a, 2), round(b, 2)] for a, b in shots]}
    # one thumbnail from the middle of each shot, labelled "start-end"
    tdir = os.path.join(OUT, "_t", alias); os.makedirs(tdir, exist_ok=True)
    for i, (a, b) in enumerate(shots):
        mid = a + min((b - a) / 2, 1.5)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{mid:.3f}", "-i", path, "-frames:v", "1", "-vf",
                        f"scale=240:135:force_original_aspect_ratio=decrease,pad=240:135:(ow-iw)/2:(oh-ih)/2,"
                        f"drawtext=text='{a:.1f}-{b:.1f}':x=3:y=3:fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.7",
                        os.path.join(tdir, f"{i:04d}.png")], capture_output=True)
    cols = 8
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", os.path.join(tdir, "%04d.png"), "-vf",
                    f"tile={cols}x{max(1, -(-len(shots) // cols))}:margin=2:padding=2:color=red", "-frames:v", "1",
                    os.path.join(OUT, f"{alias}.png")], capture_output=True)
    print(f"{alias}: {len(shots)} shots, {dur:.1f}s", flush=True)
json.dump(index, open(os.path.join(OUT, "shots.json" if not only else f"shots_{'_'.join(sorted(only))}.json"), "w"), indent=1)
