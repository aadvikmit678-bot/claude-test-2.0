# GTA 6 edit — v4 (in progress: part 1, to "freedom")

v4 is v2 (the desktop session's cut, picked to continue from) with the user's notes, built part by part. Part 1 runs 0:00–0:32.5: the FOX 2 cold open, CJ, and the voiceover up to "freedom", on the user's cut-down script:

> That's exactly how millions of adults are going to feel on November 19th when they play GTA 6 for the first time. GTA 6 took 13 years to make. And yet, nobody seems to have moved on. But why are grown adults waiting 13 years for a game that's supposedly just about stealing cars? Because GTA was never just about cars and guns. It was about what it really gave you: freedom.

v2 is in git history (commit 193a7c7) and `tools/edl.py` + `tools/build.py` still build it; v3 is at 93a94ec (`edl3.py`, `build3.py`). The `gta6/` folder on this branch is a different session's edit.

## What part 1 does (the user's notes)

- **Voiceover** (`tools/vo4.py` → `assets/audio/vo4.wav`, `words4.json`): "and 2 billion dollars", the release line and the first "why?" are cut; every join sits on the quietest 10 ms with a 12 ms crossfade. No sound effects.
- **Type**: the Tesla Roadster reel ("reference 7"): a Helvetica Neue Medium look (TeX Gyre Heros, thickened to medium), words on the spoken word in their final places, the line drifting left at a constant speed, entrances snapped by frame (plain, scale pop, two-frame weight flash, light streak); black on light cards.
- **"U.S. economy"**: the highlight types in, the frame zooms onto it, speeding up, then punches into the FOX banner; the corners blur in during the zooms (a pre-blurred copy of the clip under a radial mask).
- **"millions of adults"** grid: five cells replaced with GTA VI shots (all landscape); the centre kept. **"are going to feel"**: the 2013 fan's face, reframed.
- **"GTA 6 took 13 years to make. And yet, nobody seems to have moved on."**: reference 7 — the grey card, eight GTA VI tiles arriving clockwise from the top left (each inverted for its first frame), "GTA VI" in the centre, a square flash, the grid zooms 1.5x, "GTA" and "VI" slide apart around the GTA VI logo (`tools/logo4.py`), "took 13 years to make." as a normal caption on top; then the white card, "And yet, nobody seems to have" word by word, the curved black bars closing on the reel's measured per-frame curve with "moved on." landing in a weight flash at their fastest frame, the reel's three square flashes, cut.
- **"But why are grown adults waiting 13 years"**: the GTA V handover and the GTA V crew (nostalgia) added to v2's B-roll; the split frame under "supposedly" replaced by a full-frame shot.
- **"It was about what it really gave you"**: a 2-second burst after the scoopedfriday reel (1-4 frame cuts, posterised and black-and-white flash frames, one held shot).
- **"freedom"**: the freedom clip with the word big, white, glowing, in the centre.
- Textures: the Jamie Dimon halftone set (grunge, paper, dots) at low opacity over everything, with the grain and vignette.

## Open / render

```bash
cd GTA6-v3/gta6-edit
npx hyperframes@0.9.46 preview      # Studio
npx hyperframes@0.9.46 render --fps 30 --quality looks --output renders/gta6_v4_part1.mp4
```

## Rebuild

```bash
python -I GTA6-v3/tools/link_sources.py        # once per machine: links the source downloads under the names in edl.py
cd GTA6-v3
python -I tools/vo4.py                          # the cut voiceover and its word times
python -I tools/logo4.py                        # the GTA VI logo cut-out
EDL=edl4 python -I tools/prep.py                # cuts only the shots whose spec changed (assets/clips/_spec.json)
python -I -X utf8 tools/build4.py               # writes index.html and compositions/
```

prep writes clips with `-fps_mode passthrough`, so ffmpeg 6 (cloud) cuts the same frames with the same timestamps as the desktop session's ffmpeg 8.

`tools/`: `edl4.py` / `build4.py` are v4; `edl.py` / `build.py` v2; `edl3.py` / `build3.py` v3; `edl_v1.py` / `build_v1.py` v1. Fonts: TeX Gyre Heros (GUST Font License, see `assets/fonts/`). Textures: the user's halftone scans from the Dimon edit.
