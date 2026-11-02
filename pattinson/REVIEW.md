# REVIEW — "The Post-Twilight Reinvention"

74.0 s · 1920×1080 (horizontal) · 30 fps · HyperFrames. Style source:
`../reference/f1-horner-reel-breakdown.md`. Shot-by-shot plan: `SPEC.md`.

## Creative calls

- **The reference's grammar, re-mapped to this script.**
  - Cold open on a real moment with diegetic audio: the Venice fan yells "Somebody get these beggars out of here", then the original line from *The Odyssey*.
  - A pixel-mosaic resolve into the hero name.
  - Paper interstitials for the punchlines.
  - Photo cards that drop onto paper.
  - A rolling year counter (2012 → 2026).
  - A 5-panel film-title build.
  - The tile wall.
  - Negative flashes on hard cuts.
  - Archival audio stings as punctuation ("…spider monkey", "…have a seat right there?").
  - "And this year?" becomes the reference's **1-2-3 triptych**, so *The Odyssey*, *Primetime* and *Dune* are the three chapters.
- **Typography.**
  - Small words use Inter Tight Bold, a free stand-in for the reference's Helvetica Neue Bold.
  - Hero words use **Instrument Serif** (regular and italic), as you asked.
  - White words get the **glow entrance**: blur 16 px → 0, scale 1.12 → 1, and a bloom text-shadow → resting glow, in 0.24 s, landing 2 frames before the word.
  - Black ink on paper cuts in at 114 % and settles.
- **Textures.**
  - **Halftone** (CMYK print) on the Twilight-era tabloid and "internet jokes" moments.
  - **VHS** (tape damage, scanlines, chroma bleed) on Primetime, plus a CRT glitch on the chat screen and hidden camera.
  - **Old film** (8mm dust, scratches, vignette, grain) on the Twilight memories.
  - Global grain and two light-leak burns, at "after Twilight" and "post-Twilight".
- **Sound: no music, as you asked.**
  - Your VO, normalised to about -16 LUFS.
  - Three dialogue stings, with the music the source edits had added removed by Demucs (vocal stems only).
  - 93 sound-effect cues from the bundled HyperFrames library: whooshes on moving transitions, pops on card drops, key ticks on counters and strobes, bass hits on "Batman." and "Dune.", glitches in Primetime and a sparkle on "Edward Cullen".
- **Source clean-up.**
  - The cold-open clip had burned-in captions. They were removed by temporal-mask inpainting (`tools/clean_captions.py`) and our captions sit over that band.
  - Watermarks and film-title cards in the montages were cropped out at prep.

## Measured vs looked at

- `hyperframes lint`: 0 errors. `hyperframes check`: ok, 0 errors.
- Snapshots of every scene start and middle, all 16 seams and the phone-width sheet were reviewed.
- Audio was **measured, not heard**: stem levels, kick removal (bass energy fell from about 35–40 dB to 5–15 dB) and loudness.

## Warnings kept on purpose

- `line_unread`: the year counter and the director-name strobe flash 3–5 frames per item, like the reference's photo strobe. They are texture, not reading.
- `timeline_track_too_dense` and `composition_file_too_large`: every caption lives in one captions composition, as the captions guide asks.
- `contrast_aa_failure` (2): small year labels over bright panel footage for under a second.

## Weakest shots / next pass

1. The "Twilight" burn (67.8–68.4 s) reads as a warm light leak rather than film actually burning through.
2. "with the best directors alive" shows only Nolan clearly. The other directors are names over their films' stills, because the only director footage had red names burned in.
3. The 2012–2016 counter stills come from the labelled-clips compilation, cropped and upscaled, so they are slightly soft.

## Assets that would make it better

- The Venice autograph clip and *The Odyssey* "beggars" clip **without burned-in captions**.
- Clean photos of Safdie, Eggers, Bong, Reeves and Villeneuve.
- A high-resolution landscape portrait for the "Robert Pattinson" hero card.

## Rebuild

```bash
python3 tools/prep_media.py          # trims/crops every clip from the Drive folder (pattinson-src/)
python3 tools/clean_captions.py      # inpaints the cold-open captions
python3 tools/build.py               # writes index.html + compositions/
npx hyperframes check && npx hyperframes render --quality delivery -o renders/pattinson-reinvention.mp4
```
