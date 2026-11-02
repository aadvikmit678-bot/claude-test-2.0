# REVIEW — Robert Pattinson "post-Twilight reinvention" edit

Style source: `../reference/sam-altman-reel-breakdown.md`. Plan: `SPEC.md`. Generator: `tools/build.py`
(re-cuts every source from `source/` (the person's Drive folder), writes the scenes, bakes the looks).

## Creative calls

- **Format:** 1440 × 1080 (4:3), 24 fps, horizontal — the reference's own frame; several of the person's
  montages were already 4:3.
- **Cold open (0–5.9 s):** the person's `Starting frame.mp4` — the Venice fan shouting "Somebody get these
  beggars out of here!" at the autograph signing, then Antinous saying it in *The Odyssey*. Voices only
  (Demucs stem; the meme edit's music removed). The clip's burned meme captions are covered word-for-word by
  the reference-style glow captions (Odyssey half also has the old text softened underneath).
- **Receipts, like the reference's news clips:** the VO is never cut mid-sentence, but three original-audio
  moments play in measured silences between sentences:
  1. *Twilight* (2008) "You better hold on tight, spider monkey." after "…Twilight jokes,"
  2. Jimmy Kimmel Live: "Our first guest tonight is Batman, and the vampire" after "…he became Batman." —
     it hands straight into "The vampire kid everyone laughed at…"
  3. *Primetime* trailer: "I'm Chris Hansen." after "…predator sting operations."
  Each is easy to remove (one `INS` value + one block in `tools/build.py`).
- **Captions:** the script's words, two faces exactly as in the reference — Instrument Serif Italic for
  connective words, Inter Tight 760 (tight tracking) for the meaning words — white with a two-layer glow; each
  word blurs in with a glow burst (the "glow coming in animated" the person asked for), groups hard-clear.
  Black-with-white-glow automatically on bright shots (measured per caption).
- **Textures:** halftone (Twilight-era stills, set photos, the cast), old-film build-up (dust/wear + heavy
  grain on *The Lighthouse*), VHS for the 2008 internet-joke beat, print halftone on the *Mickey 17* poster and
  the 2026 slate, red mono-screen for "antagonists", base look everywhere (contrast, crushed blacks, vignette,
  chromatic edges, film artifacts, bloom).
- **Reference moves used:** pixel-mosaic reveal, word slams (PATTINSON, TWILIGHT, BATMAN, ODYSSEY, DUNE),
  Polaroid with flanking words, black breath cards, montages on twos, five vertical role strips, 3×3 role grid
  with a white flash on "box.", meme cards popping in, split screen, negative flash (*Tenet* inversion),
  red flash, stepped 12 fps end sting.
- **Sound:** no music (as asked). Bundled HyperFrames SFX only, each on a visible cause (slams = bass impacts,
  cuts = whooshes, glitch/negative/red = glitches, sparkle on Edward's skin, riser cresting on "Batman.",
  pops for the meme cards, cinematic whoosh into the grid flash and the sting).

## Built for this machine

The container has no GPU: HyperFrames' live colour-grading shaders ran at ~1.5 s per frame (≈10 h for the
film with every look live). Every look is therefore rendered **once** through HyperFrames' own
media-treatment shaders (same JSON, normalised by the CLI) and the film plays the baked files
(`assets/baked/`, made by `bake_all()`). The look is identical; the final render takes minutes.

## Checked

- Final render `renders/robert-pattinson-reinvention.mp4`: 1440×1080, 24 fps, 76.83 s, H.264 + AAC 48 kHz;
  rendered in 5 min 21 s from baked media.
- Every one of the 1,844 frames scanned for black gaps: none (one dark frame at 73.92 s is the end sting
  stepping in from black, intended). A 4-decimal rounding bug that left 1-frame black gaps at cuts was found
  this way and fixed (times now written to 6 decimals, each element starting 0.2 ms early).
- Sound (measured, not heard): −15.3 LUFS integrated, true peak −2.8 dBTP, no clipping; silences only at the
  VO's own pauses and the sting's fade.

- `npx hyperframes check`: 0 errors. Kept warnings: `nested_media_start_basis_ambiguous` (media timing is
  intentionally local to each scene), `timeline_track_too_dense` / `composition_file_too_large` (one captions
  file holds all 77 groups — needed so Studio shows one captions track).
- Snapshot passes at every caption, slam, title card, receipt, strip, grid and the sting (work/snap1–5);
  issues found and fixed: word spacing, burned meme text, framing of the hero portrait, label remnants from the
  movie-clips reel, Riddler-graffiti frames standing in for Batman, unreadable halftone/strip images,
  white-on-bright captions, shots that ran through the receipts (block-boundary bug).

## Weakest spots / with more time

- The Twilight-era fan-frenzy shots come from a vertical fan edit and are soft after the 4:3 crop.
- Openverse was unreachable, so SFX are the 12 bundled files (rotated takes); a camera shutter, record
  scratch and crowd screams would sharpen the Polaroid, spider-monkey and premiere beats.
- No logo was supplied, so the end sting is the name in the caption faces.
