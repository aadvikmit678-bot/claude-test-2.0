# GTA 6 edit — v3 (desktop session)

A 1:47 16:9 edit: FOX 2 cold open ("…cost the U.S. economy a billion dollars") → white flash → CJ "Ah shit, here we go again" → the voiceover, over GTA VI trailers, gameplay, Vice City footage and montages.

This is separate from the `gta6/` folder on this branch, which is a different session's edit.

## Watch

`gta6-edit/renders/gta6_v3_preview720.mp4`. This is a 720p preview; the 1080p render (206 MB) is over GitHub's 100 MB file limit.

## Open / render

```bash
cd GTA6-v3/gta6-edit
npx hyperframes@0.9.46 preview      # Studio
npx hyperframes@0.9.46 render --fps 30 --quality looks --output renders/gta6_v3.mp4
```

`gta6-edit/` is a complete HyperFrames project:

- `index.html` and `compositions/` hold 18 scenes, the caption track and the fx layer.
- `assets/clips/` holds the 134 pre-cut clips v3 uses.
- `assets/audio/` holds the voiceover, news line and CJ line, normalised.
- `assets/fonts/` holds Inter variable and Instrument Serif.

## Rebuild from the source footage

The source trailers and clips aren't committed. To rebuild:

1. Put them next to `tools/`, using the file names listed in `tools/edl.py` (`SRC`).
2. Recut the clips:

   ```bash
   EDL=edl3 python -I tools/prep.py
   ```

3. Write the HTML:

   ```bash
   python -I -X utf8 tools/build3.py
   ```

What's in `tools/`:

- `edl3.py` is the v3 cut list. Each beat becomes a layer: full, crt, split, strips, grid4, cards or wall.
- `build3.py` writes the v3 HTML.
- `edl.py` and `build.py` are v2. `edl_v1.py` and `build_v1.py` are v1.
- `refine_words.py` makes the voiceover word timings, and `catalog.py` makes the shot sheets.

## Style (v3)

- Small bold sans connecting words with the Tesla-reel bloom entrance.
- Big glowing upright Instrument Serif hero words, and big bold years with the white-box digit flicker.
- White text with glow only.
- CRT-TV frames, splits and strips, a 2×2 grid, floating cards, and a curved clip wall.
- No SFX.
