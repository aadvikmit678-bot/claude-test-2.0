# BlackRock (16:9, 60 fps, 85.13 s)

This is a HyperFrames project.

- **Sources:** the Drive downloads live in `blackrock-src/` (git-ignored). Also used:
  - the clip library in `jpm-dimon/assets/clips2/`;
  - the Dimon drive's sources in `dimon-src/`, including the Larry Fink documentary "larry fink metro media house".
- **Derived media:** every clip, still and the mix are rebuilt by the scripts below. The scratch venv needs numpy, pillow and opencv-python-headless<5. `tools/align.py` also needs torch and torchaudio.
- **References:**
  - `notes/REFERENCES_v2.md`;
  - `notes/REF_PORSCHE.md`: the Porsche reel, measured frame by frame, the model for the second half;
  - `notes/HIGGSFIELD_SCENE.md`.

## Preview and render

```
npx --yes hyperframes@0.9.46 preview                 # Studio in the browser (http://localhost:3002)
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 -o renders/blackrock_60fps.mp4
```

## Sync and pace

**Sync:** every caption appears on its word as it is spoken.
- The three recordings (the voiceover, the rest of the script and Elon's question) are force-aligned word by word to their sound: `tools/align.py`, which writes `tools/words/*.json`.
- Whisper's own times had been up to 0.95 s early ("Back in the 1980s" came 0.8 s before it was said).

**Pace:** the long pauses are cut out of both recordings (`tools/pace.py` → `tools/words/pace.json`).
- Sentence breaks keep 0.22 s.
- "Goldman Sachs." goes straight into "Amongst them".
- Every cut is in silence.
- The mix and the captions both go through the same clock (`timing.squeeze`).

**"did":** "… than Steve Jobs ever did." now ends after "did" has faded, then the Elon clip.

## Beats

| Film s | What |
|---|---|
| 0.00–6.70 | **The FII7 panel line.** Then the panelists with white flashes: Fink, Schwarzman, **Jamie Dimon (3rd)**, **Ray Dalio (4th)**. |
| 6.70–8.82 | **"These are the most powerful people".** The tile flash; POWERFUL and PEOPLE. |
| 8.82–9.48 | **ON EARTH** on the user's red. |
| 9.48–10.80 | **"a $60 trillion".** The article flipbook. |
| 10.80–11.48 | **"cartel".** The cartel clip's table flash, then the faces on the word. **CARTEL** is centred, in difference. |
| 11.48–12.68 | **"of weaponized capital".** Nothing is written at the cut. **WEAPONIZED** comes in on its word, then **CAPITAL** under it, centred, in difference, with no bounce. |
| 12.68–15.10 | **"that owns a piece of everything you touch".** The ownership pages, the hands, the puppet. |
| 15.10–16.87 | **"That's Jamie Dimon, the guy running".** refff's device: the band in the **ON EARTH red** and **"Jamie Dimon" in the white glow**. |
| 16.87–18.18 | **"JP Morgan Chase".** The OpenAI device. |
| 18.18–19.77 | **"David Solomon, a part-time".** The same device as Dimon. "a part-time DJ" is written by the captions; no vertical text. |
| 19.77–22.05 | **"DJ and the CEO of Goldman Sachs".** His DJ nights, then the JPMorgan device exactly, with no shot repeated. Straight into "Amongst". |
| 22.05–23.70 | **"Amongst them is this guy".** The spotlight reel: "Amongst them" as big glowing serif words over the table, then the face flash, the dark punch-in on Fink and "is this guy" under his face. |
| 23.70–25.38 | **"the man who runs the most evil".** Reel DeHkRtts3bI's opening: a Fink picture every 4 frames, tilted out of perspective, blurred on the cuts, with light leaks and negatives. The user's 12 new photos come first. No red box. |
| 25.38–27.52 | **"company in the world, BlackRock."** |
| 27.52–38.18 | **"A company that manages $15 trillion in assets … than Steve Jobs ever did."** The $15T montage with the Dario serif glow. Think School's columns, Jensen, Gates and Jobs carry the money texture at low opacity and the soft corners. |
| 38.18–40.32 | **Elon: "Do you think BlackRock's a bad company?"** The music is removed. It has the Palmer Luckey reel's look: a slow push, soft corners, grain, and stacked lowercase bold captions blurring in. |
| 40.32–41.92 | **Rogan, chin on hand, saying nothing.** The cut is on "company". A flash leads into the next part. |
| 41.92–85.13 | **"Back in the 1980s" to the end.** The Porsche reel's look: 72 shots, each on a word, each moving, with flashes, whips and zoom punches. Details below. |

**The second half in detail:**
- **Footage:**
  - mostly the Larry Fink documentary: 1980s Wall Street, the 1980s photo of young Fink on the floor, 2008 on the NYSE, BlackRock's signs, iShares;
  - the Higgsfield trader scene, cut tighter;
  - the user's genie clip on "Aladdin.", their chalkboard on "calculating" and their ending video, now centred with its watermark painted out.
- **The 1980s look:** warm and faded, with grain at low opacity.
- **The red card:** "in 1988" is exactly the ON EARTH card.
- **Big words:** "$100 million loss." is one glowing line. "2008" and "3x" are big glowing figures, with "the money." on a printing press. "S&P 500," comes in letter by letter.

## Type and sound

**Captions:** `tools/captions.py`, all in the composition `s_caps`, each word on its aligned onset. There are three styles:
- **To "…ever did.":** the Jensen reel's centre line, Inter Display SemiBold. The words cut in and the line re-centres. Key words ("everything", "evil", "BlackRock") are set alone in Instrument Serif with the Dario white glow.
- **Elon:** the Palmer Luckey reel's stacked lowercase Helvetica.
- **From "Back in the 1980s":** the Porsche reel's Instrument Serif Italic.
  - The words are set wide apart and laid out first.
  - Each fades in from a soft blur in its place.

**Sound:** no sound effects. A low drone sits under the voice, ducked; there is none under Elon and Rogan.

## Rebuild

```
python -I tools/align.py          # (torch venv) the word alignment -> tools/words/{vo,rest,rogan}.json
python -I tools/pace.py           # the pauses cut out -> tools/words/pace.json
python -E -s tools/prep_hook.py weap logos
python -E -s tools/prep_v3.py tiles articles touch jpm rogan2   # + rest_shots(REST1 names), r_tsg, r_jensen, r_gates, r_jobs
python -E -s tools/prep_v4.py finkflip cartel4 ceo4 dj4 orbit4 spot4 panel4 founders
python -E -s tools/prep_v5.py rest2 rogan dimon5 solomon5
python -E -s tools/mix.py         # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
```
