# BlackRock (16:9, 60 fps, 83.92 s)

This is a HyperFrames project.

- **Sources:** the Drive downloads live in `blackrock-src/` (git-ignored). Also used:
  - the clip library in `jpm-dimon/assets/clips2/`;
  - the Dimon drive's sources in `dimon-src/`, including the Larry Fink documentary "larry fink metro media house".
- **Derived media:** every clip, still and the mix are rebuilt by the scripts below. The scratch venv needs numpy, pillow and opencv-python-headless<5. `tools/align.py` also needs torch and torchaudio.
- **References:**
  - `notes/REFERENCES_v2.md`;
  - `notes/REF_PORSCHE.md`: the Porsche reel, measured frame by frame, the model for the second half;
  - `notes/REF_TERRIBLE_BOSS.md`: reel DfhzVs8q9NH's "terrible boss" scene, measured frame by frame, the model for "the man who runs the most evil";
  - `notes/HIGGSFIELD_SCENE.md`.

## Preview and render

```
npx --yes hyperframes@0.9.46 preview                 # Studio in the browser (http://localhost:3002)
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 14 -o renders/blackrock_v6_60fps.mp4
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
| 6.70–8.82 | **"These are the most powerful people".** The tile flash; "powerful" and "people" in the Dario serif white glow, blooming in on their words. |
| 8.82–9.48 | **ON EARTH** on the user's red. |
| 9.48–10.80 | **"a $60 trillion".** The article flipbook. |
| 10.80–11.48 | **"cartel".** The cartel clip's table flash, then the faces on the word. **CARTEL** is centred, in difference. |
| 11.48–12.68 | **"of weaponized capital".** The blueprint pages flip under a continuous push, with no frame held. **WEAPONIZED** comes in on its word, then **CAPITAL** under it, centred, in difference, with no bounce. |
| 12.68–13.78 | **"that owns a piece of".** The user's ending video from its glasses for 0.45 s, each object moved down to the centre, then the brand maps ("everything you own"). |
| 13.78–15.10 | **"everything you touch".** A cut on "everything" to the fingers meeting on "touch". The puppet shot is gone. |
| 15.10–16.87 | **"That's Jamie Dimon, the guy running".** refff's band (ON EARTH red) and flashes. The words are centred in the **JPMorgan Chase title type**, the name with refff's flicker. |
| 16.87–18.18 | **"JP Morgan Chase".** The OpenAI device. |
| 18.18–19.77 | **"David Solomon, a part-time".** The same device. "David Solomon" is in the Goldman Sachs / JPMorgan title type with the flicker; "a part-time DJ" is the captions' line. |
| 19.77–22.05 | **"DJ and the CEO of Goldman Sachs".** His DJ nights, then the JPMorgan device exactly. The two-up's left half is the Goldman Sachs tower sign, no longer Solomon at the panel again. Straight into "Amongst". |
| 22.05–23.70 | **"Amongst them is this guy".** The spotlight reel: "Amongst them" as big glowing serif words over the table, then the face flash, the dark punch-in on Fink and "is this guy" under his face. |
| 23.70–25.38 | **"the man who runs the most evil".** Reel DfhzVs8q9NH's "terrible boss" scene, rebuilt on the user's red with the user's Fink cut-outs.<br>• Fink rises slowly on the reference's curve while "the", "man", "who", "runs" and "the" come in as its small words.<br>• The horns fade in, then a smooth cut to the close-up.<br>• **most** and **evil** sit behind him as its **terrible** / **boss**.<br>See `notes/REF_TERRIBLE_BOSS.md`. |
| 25.38–27.52 | **"company in the world, BlackRock."** |
| 27.52–38.18 | **"A company that manages $15 trillion in assets … than Steve Jobs ever did."**<br>• The $15T montage, with "$15 trillion" in the Dario serif white glow.<br>• Think School's columns, Jensen, Gates and Jobs have no money overlay (corner softening only). |
| 38.18–40.32 | **Elon: "Do you think BlackRock's a bad company?"** The music is removed. It has the Palmer Luckey reel's look: a slow push, soft corners, grain, and stacked lowercase bold captions blurring in. |
| 40.32–40.70 | **Rogan, chin on hand.** The cut is on "company". There is no pause: a white flash goes straight into the next part. |
| 40.70–83.92 | **"Back in the 1980s" to the end.** The Porsche reel's look, on 71 real video shots. Each shot is cut on a word, and there are no stills. Details below. |

**The second half in detail** (`tools/shotlist.py` REST2_V6, rendered by `tools/prep_v5.py rest2`):
- **Footage, all real moving video:** every source was searched with a CLIP index, and each span was checked for real motion and for hidden cuts. The sources are:
  - the Larry Fink, Jamie Dimon and Wall Street drives;
  - the BlackRock documentaries;
  - the 2008, JPMorgan and Dimon documentaries.

  Channel logos and burned-in words are cropped out, and no footage repeats from anywhere in the film.
- **The 1980s run:** warm and faded, with grain at low opacity and a little gate weave.
- **"but one bad bet … $100 million loss.":** one smooth take, from the Higgsfield trader scene motion-interpolated to 60 fps, at real speed under a slow push. The screens flip from green to red on "$100 million".
- **"That was enough" / "threw out":** the walk-out, at 60 fps.
- **"in 1988":** exactly the ON EARTH card, with a flash and the Tesla reel's boxes snapping around the year.
- **"He called it":** one plain cut of Fink, with no zoom.
- **"Aladdin.":** the user's genie clip (8–9 s).
- **"calculating":** the user's chalkboard clip.
- **"the U.S. government":** the Capitol from the air, then the dome.
- **"to clean up the mess— Larry Fink.":** a man carrying his box out, boxes leaving the bank, then Fink's face.
- **"with three times the money.":** the user's fire clip, with no money overlay anywhere in the film.
- **"S&P 500, your money ends up in this guy's hands.":** the S&P 500 wall, a trader's screens, the cash, iShares by BlackRock on the NYSE, then Fink.
- **"A company that has never made a single product, but everything you own, everything you touch":**
  - BlackRock's lobby and doors;
  - the user's ending video, after its glasses part, which now plays at "that owns a piece of";
  - the brands;
  - the wall of logos.
- **Bright shots:** they are dimmed under the white type. The glow is white everywhere, with no dark glow or shadow.

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
python -E -s tools/prep_v5.py rest2 rogan dimon5 solomon5 owns   # rest2 also renders in parallel: rest2p0 … rest2p3, then rest2join
python -E -s tools/prep_v6.py evil
python -E -s tools/mix.py         # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
```
