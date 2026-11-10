# Running jpm-dimon on a Windows PC

**Update, 10 Nov 2026 (night): v9, 86.09 s at 60 fps (tag `jpm-dimon-v9`).** The builder is `tools/build9.py`, which writes `tools/media_v9.json`. v8 is unchanged: tag `jpm-dimon-v8`, built by `tools/build8.py`. `notes/v9/mix.md` lists what changed and which footage is kept out.

**v9 sources:**
- The portraits `h12`-`h17` in `../dimon-src/_heath/`, from the Drive folder "heath ledger part of edit". `tools/prep8.py` aligns them into `h9_a01` … `h9_a17` (the `ALIGN` list).
- `../dimon-src/_drive9/`: two clips from the same folder.
  - The money pan: `1ZoAeY5-kuokp-w6cUPTop7gCOAgIc5pP`, saved as `a_1ZoAeY5/clip_a.mp4`.
  - The fast collage: `1kw8XDrJgmRlZqJhQ9rQym5Gq0q1TxWvp`, saved as `b_1kw8XDr/clip_b.mp4`.
  - Sped up with the ffmpeg-skill: `python scripts/speedramp.py clip_a.mp4 --segment 0-56.48:4.0 -o x4/money_pile_4x.mp4` (`MPILE`) and `python scripts/speedramp.py clip_b.mp4 --segment 0-11.448:3.0 -o x3/trip_3x.mp4` (`TRIP`).

**v9 steps:**
1. `python -I tools/prep8.py fb` (face-box alignment of the Meet portraits).
2. `python -I -X utf8 tools/build9.py --specs`
3. `python -I tools/prep2.py --spec=media_v9.json`
4. `python -I -X utf8 tools/build9.py`

Set `DIMON_ROOT` to the folder that holds `dimon-src`, `dimon-work` and `jpm-dimon` for every step.

---

**Update, 10 Nov 2026 (evening): v8, the whole film, rendered at 60 fps.** The builder is now `tools/build8.py`, which writes `tools/media_v8.json`. Its parts:
- **S07, "Meet Jamie Dimon…":** rebuilt on the Heath Ledger reel at its own 60 fps (`notes/v8/heath60.md`). This scene's timing uses 60 fps frames.
- **S09 and S11-S23:** rebuilt in the Alex Karp reel's editing (`notes/v8/karp.md`), with the "cut cut" panels on the last line (`notes/v8/cutcut_panels.md`).
- **0-30 s fixes:** the words are centred (small Helvetica over the Instrument Serif glow), "Wall Street" is yellow, the grudge has no slide, the fired photos stream evenly, the IMF sits over a building, and a halftone layer is on every scene.

**v8 sources:**
- `../dimon-src/_heath/`: the user's photos for the Meet section, copied from their Desktop folder "jamie dimon" and the Drive folder "heath ledger part of edit" (`h01_teen` … `h10_blue`, `h_cell`, `h_xray`, `h_wallst_sign`, `h_wallst_street`).
- `assets/tex/ht_dots.jpg`: made from the Drive's `halftone textures/Copy of Halftone 2.jpg`.
- `../dimon-work/v8/tx/`: whisper transcripts of the documentaries. They were used to find matching footage.

**v8 steps:**
1. `python -I tools/prep8.py` (the Meet section's pictures).
2. `python -I -X utf8 tools/build8.py --specs`
3. `python -I tools/prep2.py --spec=media_v8.json`
4. `python -I -X utf8 tools/build8.py`

**Render:** `npx --yes hyperframes@0.9.2 render --fps 60 -o renders/<name>.mp4`.

---

**Update, 10 Nov 2026: v7.** The checkout is at `f7d31ec`, "v7 round 1". The film is a 45.8 s preview that ends after "he was fired" (`PREVIEW_END` in `build7.py`). The reference is the user's render `Downloads/jpm-dimon_2026-11-10_16-01-02.mp4`, 45.83 s.

**v6/v7 sources** (under `../dimon-src/`, from the same Drive folder):
- `_drive/`: The Wall Street Gazette Front Page.png, wall street videos montge edits.mp4 (`WSMONT`), Jp morgab edit w flashes.mp4 (`JPFLASH`), JP mogran building horizontal.mp4 (`JPHORIZ`), Edit style cut cut photos..mp4 (`CUTCUT`), jp morgan edit use clips in the last fast paced.mp4 (`LASTFAST`), banking montage 1-2 sec clip can be used.mp4 (`BM`), jamie-old-images.zip.
- `jamie-old-images/jamie-old-images/`: the zip unpacked. Git Bash's `tar` can't read zips; use `C:\Windows\System32\tar.exe`.
- `_cyber/Glitchy JPMorgan Chase Cyber Portrait.png`.
- `new_dimon_images/`: 14 images. Their Drive ids are in `tools/rebuild/drive_files.tsv`.
- Not downloaded: `JPD`, "J P Morgan The Man Who Bought America" (480 MB). No v7 media uses it.

**v6/v7 media steps,** run after the v5 steps below: `prep2.py --spec=media_v6.json`, then `prep6.py`, then the `BANK_27585_413_x63_50_135` matte (`remove-background`), then `prep2.py --spec=media_v7.json`, then `prep7.py`. The Windows fixes also cover `prep6.py` (`ROOT`, `npx.cmd`) and `build6.py`/`build7.py` (`ROOT`).

---

The v5 rebuild of 9 Nov matched the v5 share clip (`jpm-dimon-v5-0-31-share.mp4`):

- **Picture:** 0.986 overall similarity over 0–31.7 s, with every sampled frame the same.
- **Loudness:** −16.3 LUFS here against −16.4 LUFS in the share clip.

## What git does not hold
These are kept out of git and rebuilt by `tools/`:
- `renders/`
- `assets/clips2`, `assets/img2`, `assets/audio` and `assets/tex`
- `../dimon-src/`, the Drive sources

## Sources: `../dimon-src/`
These are hard links to the Drive folder's files, saved under the names the scripts use.

| Drive file | Script name |
| --- | --- |
| name of the game.mp4 | `_direct/name_of_the_game.mp4` |
| we bank the countries, we bank the world bank.mp4 | `_direct/we_bank.mp4` |
| Jamie Dimon - The Most Powerful Banker in America Full Documentary.mp4 | `_direct/most_powerful_banker_doc.mp4` |
| The Untold Career Story of Jamie Dimon (CEO of JPMorgan).mp4 | `_direct/untold_career_story.mp4` |
| How JP Morgan Chase Became The Largest Bank In The US.mp4 | `_direct/how_jpm_became_largest.mp4` |
| Stories from 2008's Great Recession (…).mp4 | `_direct/stories_2008_recession.mp4` |
| Jamie Dimon, Chairman, President, and CEO of JPMorgan Chase.mp4 | `_direct/dimon_chairman_interview.mp4` |
| Stock Market Crash of 2008.mp4 | `_direct/crash_2008.mp4` |
| wolf of wall street clip to be used when he says wolf of wall street.mp4 | `_direct/wolf_of_wall_street.mp4` |
| fiered him push scene punch one. that takes soul out.mp4 | `_direct/fired_push_scene.mp4` |
| cool cinematic clip.mp4 | `_direct/cool_cinematic.mp4` |
| jamie dimon speaking video.mp4 | `_direct/dimon_speaking.mp4` |
| Dimon Cuts Ribbon on JPMorgan's New Manhattan HQ.mp4 | `_direct/ribbon_hq.mp4` |
| watch-citadel-s-high-speed-trading-in-action….mp4 | `_direct/citadel_trading.mp4` |
| 💰Wall Street New York … shorts.mp4 | `_direct/wallst_ny_short.mp4` |
| NEW YORK STOCK EXCHANGE Closing Bell Ceremony 🇺🇸.mp4 | `_direct/nyse_closing_bell.mp4` |
| JPMorgan building aura farming!! #shorts #aura.mp4 | `_direct/jpm_building_aura.mp4` |
| jp morgan montage.mp4 | `_direct/jpm_montage.mp4` |
| over a bonus.mp4 | `_bonus/over_a_bonus.mp4` |
| money asset.mp4 | `_money/money_asset.mp4` |
| wolf of wwall street vid.mp4 | `_wolf2/wolf_first_part.mp4` |
| jamie dimon audi.mp3 | `jamie dimon audi.mp3`, the voiceover |
| jamie ghost image.webp | `_globe/`, the "We bank" ghost |
| sandie weil images/images.jpg and images (1).jpg to images (6).jpg | `_weill/weill_0.jpg` to `weill_6.jpg`, numbered in name order |
| The Pinterest clips (2008 chess, rustic wedding, wedding hair, shell-toned, entryway, 11 classy, money laundering, eye, money bg, pint videos) | `_pin/p01`–`p04` and `_pin/p06`–`p11`, in that order |

`Jamie_Dimon_Image_Pack/`, `money_pinterest videos/` and `halftone textures/` are folder links (junctions) to the Drive download.

`assets/tex/paper_light.png` is the Pattinson v5 window-light paper, taken from the `claude/pattinson-v5-notes5` branch.

## Windows changes to the tools
- `ROOT` reads the `DIMON_ROOT` environment variable. The cloud default is unchanged.
- `npx` is called as `npx.cmd` on Windows.
- `make_music.py` runs Demucs with the current Python.
- Python on Windows fails on paths over 260 characters. `DIMON_ROOT` therefore points at a short junction, `C:\Users\ASUS\AppData\Local\Temp\dm`, which links to the repo root. Run the tools and renders from `C:\Users\ASUS\AppData\Local\Temp\dm\jpm-dimon`.

## Rebuild order
Use Python 3.12 with these packages:
- numpy, Pillow, `opencv-python<5`, fontTools, soundfile;
- torch and torchaudio, the CPU builds from download.pytorch.org;
- demucs.

Run each step with `DIMON_ROOT` set:
1. `python -I tools/prep_media.py ht_grunge ht_paper ht_warm audio`: the textures, `vo.wav` and `dimon_quote.wav`.
2. `python -I tools/prep2.py --spec=media_v5.json`: 113 clips and 111 stills.
3. `python -I tools/make_music.py`: Demucs makes `news_voice.wav` and `music_bed.wav`.
4. `python -I tools/prep4.py`: the ghost and the freeze cut-outs.
5. `python -I tools/prep5.py`: the mattes, slow motion, the Weill faces and the young-Dimon squares. Also matte `BANK_27305_820_x63_50_135` with `prep5.matte(...)`; the "We bank" layer needs it.

**Render:** `npx --yes hyperframes@0.9.2 render -o renders/<name>.mp4`. Version 0.9.2 renders the whole 93.2 s film.
