# REVIEW — "The Post-Twilight Reinvention"

74.0 s · 1920×1080 (horizontal) · 30 fps · HyperFrames. Style source:
`../reference/f1-horner-reel-breakdown.md`. Shot-by-shot plan: `SPEC.md`. Generator: `tools/build.py`.

## Versions

- **v1** (`8c212a6`): first cut.
- **v2** (`a313966`): rebuilt against the reference after a frame-by-frame audit of v1.
  - **What the audit found in v1:**
    - About 40 % of the runtime was paper (the reference uses about 20 %).
    - Everyday captions were 54 px; the reference's are about 110–120 px.
    - There was a 2 s still under the Primetime line.
    - Only 6 inversion flashes (the reference: one every ~5 s).
    - Frame-to-frame motion was about 3.5× lower than the reference.
  - **What changed:**
    - Mostly full-frame footage, with 27 new clips cut from footage v1 hadn't used.
    - Captions at the reference's sizes.
    - Paper words one at a time.
    - Whip pans, snap zooms, exposure blowouts and RGB-split frames.
    - A Mickey 1→17 counter.
    - Photo-to-card shrink and zoom-through.
    - A CRT glitch with a REC glyph.
    - The real, lip-synced "have a seat right there" footage.
- **v3**: the user's notes on v1, in order.
  1. **Opening:** three fast real-life clips (Venice, red carpet, Kimmel), darkened, under a one-line, full-width, heavier Instrument Serif "Robert Pattinson". The two words glow in and glide together.
  2. **"Is having a generational run":** his roles flick by under a light halftone. The 2026 slate is cut into four strips (The Drama, The Odyssey, Primetime, Dune), and each steps up from below at a low frame rate, one per word. The text sits on the right.
  3. **"Honestly":** the same Kimmel laugh, as clearly moving video.
  4. **Textures:** halftone, VHS and glitch effects cut to about 25–55 % of their v2 strength. Halftone is at 25 %.
  5. **Sounds removed:**
     - every pop, click and tick, including at 11 s and on the counters and director strobe;
     - the sparkle chime on "Edward Cullen";
     - the dark whoosh into "vampire".

     The Primetime glitch effects are at half volume.
  6. **Film titles:** centred in frame. The five panels now build over the Mickey 17 shot, which keeps playing behind them.
  7. **"And while the internet / kept making / Twilight jokes":** full-width, glowing Instrument Serif lines. "Twilight jokes" lands on the word at 29.25 s.
  8. **"Spider monkey":** now in the glowing serif instead of the blue shout.
  9. **"Respected actors in Hollywood":** red-carpet video plays behind five portraits that pop in.
  10. **"Christopher Nolan's The Odyssey":** Odyssey footage with Nolan's photo popping in. No poster, no click.
  11. **"One box":** Edward plays as video inside the framed square.
  12. **"Pattinson" (payoff):** video, not a still.

## Measured vs looked at

- `hyperframes check`: ok, 0 errors (v2 and v3).
- Every changed beat was snapshot-reviewed. v1 was audited from the render at 4 fps against the reference at 5 fps.
- Motion and cut rate were compared with `motion.py` (mean frame difference and histogram cuts) against the reference.
- Audio was measured, not heard. v1 measured -16.2 LUFS integrated, -2.9 dBTP, no clipping.

## Warnings kept on purpose

- **`line_unread`:** the year counter, the Mickey counter and the director strobe flash 2–5 frames per item, like the reference's strobe and counters.
- **`contrast_aa_failure` (3):** a year label during the Tenet blowout (0.2 s), and "with Pattinson" over a light wall (still readable thanks to its glow and shadow).
- **`timeline_track_too_dense` / `composition_file_too_large`:** every caption lives in one captions composition.

## Weakest shots / next pass

1. "With the best directors alive" still shows only Nolan clearly. The others are names over their films' stills.
2. The 2012–2016 counter stills come from the labelled-clips compilation and are slightly soft.

## Assets that would make it better

- The Venice autograph clip and *The Odyssey* "beggars" clip without burned-in captions.
- Clean photos or footage of Safdie, Eggers, Bong, Reeves and Villeneuve.
- More non-Antinous *Odyssey* footage (ships, sea, Nolan's set) for the chapter opener.

## Rebuild

```bash
python3 tools/prep_media.py          # trims/crops every clip from the Drive folder (pattinson-src/)
python3 tools/clean_captions.py      # inpaints the cold-open captions
python3 tools/build.py               # writes index.html + compositions/
npx hyperframes check && npx hyperframes render --quality delivery -o renders/pattinson-reinvention.mp4
```
