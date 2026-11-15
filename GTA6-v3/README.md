# GTA 6 edit — v2 (the version to work from)

A 1:46.5 16:9 edit: FOX 2 cold open ("…cost the U.S. economy a billion dollars") → white flash → CJ "Ah shit, here we go again" → the voiceover, over GTA VI trailers, gameplay, Vice City footage and montages, cut on the spoken words.

This folder holds v2, the version picked to continue from. The desktop session also built v3 here (curved clip wall, CRT frames, splits); v3 is in git history (commit 93a94ec) and `tools/edl3.py` + `tools/build3.py` still build it. The `gta6/` folder on this branch is a different session's edit.

## Watch

`gta6-edit/renders/gta6_v2_preview720.mp4` (720p). The 1080p render is over GitHub's 100 MB file limit. `renders/` is gitignored, so the preview is added with `git add -f`.

The render made in the cloud session matches the desktop session's v2 preview on all 3,195 frames (mean difference under 1 of 255; every cut, caption entrance, white flash and square flash on the same frame) and in sound (correlation 0.9996; both −14.2 LUFS).

## Open / render

```bash
cd GTA6-v3/gta6-edit
npx hyperframes@0.9.46 preview      # Studio
npx hyperframes@0.9.46 render --fps 30 --quality looks --output renders/gta6_v2.mp4
```

`gta6-edit/` is a complete HyperFrames project:

- `index.html` and `compositions/` hold the news cold open, CJ, the 15 footage sections (`sa`–`sq`), the caption track and the fx layer (white flashes, square flashes, grain, vignette).
- `assets/clips/` holds the 158 pre-cut clips v2 uses.
- `assets/audio/` holds the voiceover, news line and CJ line, normalised.
- `assets/sfx/` holds the six HyperFrames bundled sound effects v2 places (Pixabay Content License; see `CREDITS.md`).
- `assets/fonts/` holds Inter variable (v2) and Instrument Serif (v3).

## Rebuild from the source footage

The source trailers and clips aren't committed. To rebuild:

1. Put them next to `tools/`, using the file names listed in `tools/edl.py` (`SRC`). In this repository they are already downloaded to `gta6-src/_drive/` (and `dimon-src/` for the money clip); link them in once per machine:

   ```bash
   python -I GTA6-v3/tools/link_sources.py
   ```

2. Recut the clips (from `GTA6-v3/`):

   ```bash
   EDL=edl python -I tools/prep.py
   ```

   `assets/clips/_spec.json` records the spec each clip was cut from, so this recuts only the shots whose spec changed (`prep.py <id> …` forces those). prep writes clips with `-fps_mode passthrough`, so ffmpeg 6 (cloud) cuts the same frames with the same timestamps as the desktop session's ffmpeg 8: a clip whose first frame falls just after its in-point starts at 0.033 s instead of getting a duplicated first frame.

3. Write the HTML:

   ```bash
   python -I -X utf8 tools/build.py
   ```

What's in `tools/`:

- `edl.py` is the v2 cut list: beats per section, each cut two frames before its word (`cut(i)`), the 3×3 grid, the end shots, `TOTAL` 106.5.
- `build.py` writes the v2 HTML: the captions, the footage sections, the fx layer and the sound effects.
- `edl3.py` and `build3.py` are v3 (`TOTAL` 107.6). `edl_v1.py` and `build_v1.py` are v1.
- `refine_words.py` makes the voiceover word timings, `catalog.py` makes the shot sheets, and `link_sources.py` links this repository's source downloads under the names in `edl.py`.

## Style (v2)

- Footage under every word, cut on the spoken words (the Tesla Roadster reel's grammar).
- One line of Inter captions at a time, word by word on the voice. Each word enters with a soft fade, a bright pop, a bloom, a scale-down or a vertical streak. The line drifts slowly left.
- "U.S. economy" typed into a blue selection box; a white card behind single words.
- The 3×3 grid on "millions of adults"; white flashes on the big turns; the Tesla reel's two-frame square flashes on about 40% of cuts.
- Sound effects: bass impacts on the white flashes, a glitch on every third square flash, risers and a whoosh into "Freedom." and the end.
