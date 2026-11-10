# v9: the user's notes on v8, and the second half as a Heath + Karp mix

v8 stays as it was (tag `jpm-dimon-v8`). v9 is a separate build: `tools/build9.py` writes `tools/media_v9.json`. It runs 86.09 s at 60 fps.

## Pacing
- The ~0.5 s pause after "JP Morgan Chase" is gone (`TIGHT0`). "This is the most influential man" follows straight on, and everything after it moves up.
- "than" appears on its word, not before it.
- "Meet Jamie Dimon" starts 0.04 s after "…the US government" (`MEET_GAP`). The pictures start with the voice. The quote clip is trimmed to fit (the audio is cut, not treated as final).
- Dimon's soundbite comes in 0.3 s sooner after "…in the world" (`QGAP_CUT`). The 0.54 s of dead air between the narration and his voice is now a 0.23 s breath.
- The pinboard moves in 12 steps a second (a low frame rate), with 0.6 s moves.

## Meet Jamie Dimon (S07), on the Heath Ledger reel
- **The name run:** five front-facing portraits from the Drive folder "heath ledger part of edit", from the teen to today (`h9_a01`, `a03`, `a04`, `a07`, `a06`). The side-on college photo `h9_a02` is out.
  - Every face is the same size on the same eye line (`tools/prep8.py fb`, face-box alignment).
  - Each portrait gets the same number of frames, held still. There are no zooms.
  - The reel's devices run in its order: soft bars where the name lands, the negative box across the first cut, a black frame, the lift and the blur-in, then the whip.
- **The Golden Boy and Wall Street:** the reel's Joker and Hollywood beats, frame for frame.
- **The guy run:** six front-facing portraits, each held the same number of frames. Two of them are the newest Drive photos: `h16_capitol` (n6 image16) and `h17_red` (n8 image15).
- **Captions:** in the middle of the frame, small Helvetica over the Instrument Serif glow (the user's rule: centre, the bottom only when someone speaks).

## After 47 s: video, not stills (the Karp reel's pace)
- **"at 42":** Dimon on video (MPB 1090.5), with no punch-in.
- **"no job":** Dimon on video at the podium (MPB 1124).
- **"cuts the dividend":** Dimon on video (MPB 1343). On "cuts" the frame splits in two and the halves slide apart.
- **"and puts $60 million…":** the Economic Club shot (UNT 902) is cropped to 1.52×. That keeps it clear of the Untold film's burned-in place label (top) and its subtitle (bottom).
- **"billions in profit":** the user's money clip at 4× (`MPILE`), full frame. It's an overhead pan across $100 and $50 bills; only its first 7 s are used, which hold dollars only (euros appear from 16 s).
- **"Then, 2008 financial crisis hit":** the user's fast collage at 3× (`TRIP`) flickers at 45 % opacity through the black beat on "Then,": an eye, walking figures, the collage.
- **"$10 trillion":** the money clip again, faint (32 %, screen blend), as a double exposure on the office and the stock board. It ends where the pale notebook shot dissolves in.
- **Both clips** come from the Drive folder "heath ledger part of edit" (ids `1ZoAeY5-kuokp-w6cUPTop7gCOAgIc5pP` and `1kw8XDrJgmRlZqJhQ9rQym5Gq0q1TxWvp`). They were sped up with the ffmpeg-skill's `speedramp.py` into `../dimon-src/_drive9/x4/` and `x3/`.
- **"in 2004":** the JPMorgan Chase facade with flags in the windows (HOW 692.3). This is where the documentary says "…merged with Bank One in 2004".
- **S20:** the cards are videos.

## Footage that must not appear
- **The Untold film's narrator:** gone everywhere. All 15 UNT clips v9 uses were checked frame by frame: the Economic Club, the Bank One facade, trading floors and news footage.
- **The flash edit (`JPFLASH`, the user's reference):** it carries its creator's Instagram watermark at 10.20-10.65 s and white cut-out blobs at 4.33-4.43, 9.93-10.06, 10.7-10.8, 11.55-11.65 and 12.35.
  - v9 uses only its clean stretches: 1.30-2.17, 5.50-6.42, 8.60-9.77 and 9.30-9.885.
  - The S23 sign shot (10.20) is cropped to its top 74 % (`x50_40_135`), clear of the watermark.
- **Every clip in v9** was swept as contact sheets (one row per clip, `clipsweep.py`).
