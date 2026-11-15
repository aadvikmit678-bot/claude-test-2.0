# GTA 6 edit — v4 (in progress: 0:00 to "...so nobody could hear the gunshots.")

v4 is v2 (the desktop session's cut, picked to continue from) with the user's notes, built part by part; each render
runs only as far as the user has gone through the script. Now 0:00–0:37.4: the FOX 2 cold open, CJ, and the voiceover
up to "gunshots.", on the user's cut-down script:

> That's exactly how millions of adults are going to feel on November 19th when they play GTA 6 for the first time. GTA 6 took 13 years to make. And yet, nobody seems to have moved on. But why are grown adults waiting 13 years for a game that's supposedly just about stealing cars? Because GTA was never just about cars and guns. It was about what it really gave you: freedom. Back to being 10 years old, sitting in front of the family computer, playing Vice City with the volume turned all the way down so nobody could hear the gunshots.

v2 is in git history (commit 193a7c7; `tools/edl.py` + `tools/build.py` still build it); v3 is at 93a94ec.
The `gta6/` folder on this branch is a different session's edit.

## What v4 does (the user's notes)

- **Type: v2's, exactly** (Inter variable, 76 px, weight 540, v2's glow and word entrances). Captions do not slide.
  Black type on the light cards. No textures (v2's grain and vignette only). No sound effects.
- **Voiceover** (`tools/vo4.py` → `assets/audio/vo4.wav`, `words4.json`): "and 2 billion dollars", the release line
  and the first "why?" cut ("But" ends on its own dip, before any of that "why"); every silence over 0.3 s cut to 0.2 s.
- **Cold open**: the frame zooms onto the "U.S. economy" highlight (corner blur), then cuts to the money clip on
  "a billion dollars"; CJ "Ah shit,"; on "here we go again" the user's beat-drop clip (from its 0.43 s drop) until "millions".
- **"millions of adults"** grid with GTA VI cells; the 2013 fan's face on "are going to feel"; the GTA VI logo
  (Pre-Load, 2x) landing on "GTA 6".
- **Reference 7** for "GTA 6 took 13 years to make. And yet, nobody seems to have moved on.": tiles in from the top
  left on the grey card, "GTA VI" splitting around the logo, "took 13 years to make." as a caption on top; the white
  card with the black bars closing right after "And yet", "moved on." in the band; square flashes.
- **"But why are grown adults waiting 13 years"**: the GTA V handover (its burned-in "2013" painted out) and the GTA V
  crew; the split frame replaced. **"guns"**: the shotgun from lenojoga.
- **"It was about what it really gave you"**: a fast burst mixing the user's Pinterest cinematic clips with GTA shots,
  posterised and black-and-white flash frames; **"freedom"** big, white, glowing.
- **"Back to being"**: the Vice City car. **"10 years old, sitting in front of the family computer,"**: the user's
  green-screen kid with Vice City gameplay on the TV (`tools/tv4.py`), full screen, then reference 1 / 2's move — a
  bright frame, two negative frames, a white square growing into a card, the picture in the card and the words in glow
  either side. **"playing Vice City"**: the VICE letters (beat-drop clip) for a moment, then v2's Vice City shots.
- Square flashes (white / grey / white rectangles on consecutive frames, as in reference 7) before most cuts.

## Open / render

```bash
cd GTA6-v3/gta6-edit
npx hyperframes@0.9.46 preview      # Studio
npx hyperframes@0.9.46 render --fps 30 --quality looks --output renders/gta6_v4.mp4
```

## Rebuild

```bash
python -I GTA6-v3/tools/link_sources.py        # once per machine: links the source downloads under their Drive names
cd GTA6-v3
python -I tools/vo4.py                          # the cut voiceover and its word times
python -I tools/logo4.py                        # the GTA VI logo cut-out
python -I tools/tv4.py                          # the green-screen kid with Vice City on the TV
EDL=edl4 python -I tools/prep.py                # cuts only the shots whose spec changed (assets/clips/_spec.json)
python -I -X utf8 tools/build4.py               # writes index.html and compositions/
```

prep writes clips with `-fps_mode passthrough`, so ffmpeg 6 (cloud) cuts the same frames with the same timestamps as
the desktop session's ffmpeg 8. The user's reference and B-roll files (beat drop, green-screen kid, Pinterest clips)
are downloaded to `gta6-src/` (not committed) and linked by `link_sources.py`.

`tools/`: `edl4.py` / `build4.py` are v4; `edl.py` / `build.py` v2; `edl3.py` / `build3.py` v3; `edl_v1.py` / `build_v1.py` v1.
