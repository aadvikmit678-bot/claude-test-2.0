#!/bin/bash
# Rebuild every media file the Jamie Dimon v5 edit uses (assets/clips2, img2, audio, tex) from the user's Google
# Drive folder "Jamie Dimon" (1nC7mwKB1Baj2aL5CQehlxG5ztOkuh7WJ, shared by link), so the project renders again.
# Git keeps the edit (compositions, tools/build5.py, notes) but never the media: .gitignore keeps them local.
#
# Verified 2026-11-09 on a fresh cloud session (ffmpeg 6.1.1, python 3.13, node 22, hyperframes@0.9.2):
#   - the full render's 0-31.7 s matches the user's v5 share render (renders/jpm-dimon-v5-0-31-share.mp4, Drive id
#     1lMc957Cg69_7NMju71amKNro3LdIChDO): `hyperframes diff` SSIM 0.977, all 47 cuts, sound 0 ms off;
#   - tools/build5.py regenerates index.html, compositions/ and tools/media_v5.json byte for byte.
#
# The repo must be at /home/user/claude-test-2.0 (every tool hard-codes that root). Needs about 4 GB of downloads,
# ffmpeg with libx264 and libvpx-vp9, python3 + pip, node/npx. Takes about 30 min (Demucs is the slow step).
#
# Run:  bash jpm-dimon/tools/rebuild/rebuild_media.sh
# Then: cd jpm-dimon && npx --yes hyperframes@0.9.2 render -o renders/<name>.mp4
set -euo pipefail
ROOT=/home/user/claude-test-2.0
PRJ=$ROOT/jpm-dimon
SRC=$ROOT/dimon-src
WORK=$ROOT/dimon-work
KIT=$PRJ/tools/rebuild
HF="npx --yes hyperframes@0.9.2"
say() { printf '\n== %s\n' "$*"; }

say "1. Python packages (CPU torch before demucs, so pip does not pull the CUDA build)"
python3 -I -c 'import torch' 2>/dev/null || pip install --break-system-packages -q --index-url https://download.pytorch.org/whl/cpu torch
pip install --break-system-packages -q demucs==4.1.0 soundfile numpy pillow fonttools brotli
# tools/faces.py needs OpenCV 4.x (Haar cascades) from a private folder: OpenCV 5 dropped CascadeClassifier
[ -d "$WORK/cv4/cv2" ] || pip install --break-system-packages -q --target "$WORK/cv4" "opencv-python-headless==4.14.0.94"
export CV4_DIR=$WORK/cv4

say "2. Drive downloads into dimon-src (skips complete files, stops on a size mismatch)"
grep -v '^#' "$KIT/drive_files.tsv" | while IFS=$'\t' read -r id size path; do
  f="$SRC/$path"
  [ -f "$f" ] && [ "$(stat -c %s "$f")" = "$size" ] && continue
  mkdir -p "$(dirname "$f")"
  for try in 1 2 3 4; do
    curl -sSL --retry 3 -o "$f.part" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t" || true
    [ "$(stat -c %s "$f.part" 2>/dev/null || echo 0)" = "$size" ] && break
    sleep $((try * 4))
  done
  [ "$(stat -c %s "$f.part" 2>/dev/null || echo 0)" = "$size" ] || { echo "download failed: $path"; exit 1; }
  mv "$f.part" "$f"
  echo "got $path"
done

say "3. Links under the names the scripts read (_direct, _pin, _bonus, _money, _globe, _weill, the narration)"
# _weill: the two user photos in 'by his own mentor', matched to the v5 render frame by frame (wf0 and wf3);
# _globe: the user's globe picture for the S06 ghost (prep4.py draws a stand-in if this folder is empty)
grep -v '^#' "$KIT/links.tsv" | while IFS=$'\t' read -r link target; do
  mkdir -p "$SRC/$(dirname "$link")"
  ln -sfn "$target" "$SRC/$link"
  [ -e "$SRC/$link" ] || { echo "broken link: $link"; exit 1; }
done

say "4. build5.py clock files: the narration and Dimon's answer at 16 kHz, plus the verified Parakeet word times"
mkdir -p "$WORK/vo" "$WORK/tx/pk_vo" "$WORK/tx/pk_bank"
ffmpeg -nostdin -loglevel error -y -i "$SRC/jamie dimon audi.mp3" -ar 16000 -ac 1 "$WORK/vo/vo16k.wav"
# output seeking (-ss after -i) on purpose: input seeking moves a word by 80 ms and shifts a caption
ffmpeg -nostdin -loglevel error -y -i "$SRC/_direct/we_bank.mp4" -ss 272.5 -t 12.5 -vn -ac 1 -ar 16000 "$WORK/tx/bank_quote.wav"
cp "$KIT/clock/pk_vo/transcript.json" "$WORK/tx/pk_vo/transcript.json"
cp "$KIT/clock/pk_bank/transcript.json" "$WORK/tx/pk_bank/transcript.json"

cd "$PRJ"
say "5. Textures and voice audio"
python3 -I tools/prep_media.py ht_grunge ht_paper ht_warm audio
python3 -I tools/rebuild/paper_light.py

say "6. The 113 clips and 111 stills of the v5 spec (and the three cut-outs prep2 makes on the way)"
python3 -I tools/prep2.py --spec=media_v5.json

say "7. The globe ghost (prep4), then mattes, glow, slow motion, Weill faces and young-Dimon squares (prep5)"
python3 -I tools/prep4.py
python3 -I tools/prep5.py

say "8. The S06 interview matte (v4 made it by hand with the same remove-background call)"
[ -s assets/clips2/BANK_27305_820_x63_50_135_cut.webm ] ||
  $HF remove-background assets/clips2/BANK_27305_820_x63_50_135.mp4 -o assets/clips2/BANK_27305_820_x63_50_135_cut.webm --json

say "9. The music bed and the re-cut news voice (Demucs; about 10-15 min on 4 cores)"
python3 -I tools/make_music.py

say "10. Checks"
python3 -I -X utf8 tools/build5.py >/dev/null
git -C "$ROOT" diff --exit-code --stat -- jpm-dimon/index.html jpm-dimon/compositions jpm-dimon/tools/media_v5.json &&
  echo "build5.py reproduces the committed v5 composition"
missing=0
for p in $(grep -ohE 'assets/[A-Za-z0-9_./-]+[.](mp4|webm|jpg|png|wav|woff2)' index.html compositions/*.html | sort -u); do
  [ -s "$p" ] || { echo "MISSING $p"; missing=$((missing + 1)); }
done
echo "$missing referenced assets missing"
[ "$missing" = 0 ]
$HF lint | tail -2
