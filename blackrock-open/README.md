# BlackRock (16:9, 60 fps, 84.13 s)

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
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 14 -o renders/blackrock_v7_60fps.mp4
```

## Sync and pace

**Sync:** every caption appears on its word as it is spoken.
- All four recordings (the panel line, the voiceover, the rest of the script and Elon's question) are force-aligned word by word to their sound: `tools/align.py`, which writes `tools/words/*.json`. The panel line was on whisper's times until v7: "big" left too fast and "assemblage" came 0.7 s early.
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
| 0.00–6.70 | **The FII7 panel line.** Its captions and cuts sit on the aligned words ("with as big an" / "assemblage" / "of financial talent"). Then the panelists with white flashes: Fink, Schwarzman, **Jamie Dimon (3rd)**, **Ray Dalio (4th)**. |
| 6.70–8.82 | **"These are the most powerful people".** The tile flash; "powerful" and "people" in the Dario serif white glow, blooming in on their words. |
| 8.82–9.48 | **ON EARTH**, exactly as reel DdB8's "IT ISN'T":<br>• the tiles' last frames strobe, go negative for a frame and cyan for two;<br>• the user's red card;<br>• ON lands in its final place one reel frame 1.25× large, and EARTH joins on its word;<br>• League Gothic, caps about 15 % of the height. |
| 9.48–10.80 | **"a $60 trillion".** The article flipbook at its own brightness, with no caption: the articles show "$60 trillion" themselves.<br>From "cartel" to "everything" the words are written in the "$100 million loss." italic with Dario's entrance: each word's place lights up as a glowing white bar, then the word appears, the big ones blown out and crisp four frames later. |
| 10.80–11.48 | **"cartel".** The cartel clip's table flash, then the faces on the word; *cartel* big. |
| 11.48–12.68 | **"of weaponized capital".** The blueprint pages flip under a continuous push, with no frame held. *of weaponized capital* is one italic line. |
| 12.68–13.78 | **"that owns a piece of".** The user's ending video from its glasses for 0.45 s, each object moved down to the centre, then the brand maps ("everything you own"). "that owns" and "a piece of" are in the italic. |
| 13.78–15.10 | **"everything you touch".** A cut on "everything" to the fingers meeting on "touch". Only "everything" is written, big, in the italic; it clears as the fingers meet. There is no "you touch." caption, and the puppet shot is gone. |
| 15.10–16.87 | **"That's Jamie Dimon, the guy running".** refff's band (ON EARTH red) and flashes. "That's Jamie Dimon" sits inside the red band, top left, clear of his face, in the **JPMorgan Chase title type** (140 px) with a white glow and refff's flicker. "the guy running" stays centred below. |
| 16.87–18.18 | **"JP Morgan Chase".** The OpenAI device, the title with a subtle white glow (so is Goldman Sachs'). |
| 18.18–19.77 | **"David Solomon, a part-time".** The same device. "David" over "Solomon" (145 px) inside the red band beside his face, in the same title type with the glow and the flicker; "a part-time DJ" is the captions' line. |
| 19.77–22.05 | **"DJ and the CEO of Goldman Sachs".** His DJ nights, then the JPMorgan device exactly. The two-up's left half is the Goldman Sachs tower sign, no longer Solomon at the panel again. Straight into "Amongst". |
| 22.05–23.70 | **"Amongst them is this guy".** The spotlight reel: the table in its original colours (no grade, no grain), "Amongst them" in the captions' line (as "a part-time DJ"), then the face flash, the dark punch-in on Fink and "is this guy" under his face. |
| 23.70–25.38 | **"the man who runs the most evil".** Reel DfhzVs8q9NH's "terrible boss" scene, rebuilt on the user's red with the user's Fink cut-outs.<br>• Fink rises slowly on the reference's curve while "the", "man", "who", "runs" and "the" come in as its small words.<br>• The horns fade in, then a smooth cut to the close-up.<br>• **most** and **evil** sit behind him as its **terrible** / **boss**.<br>• No grain is added on him: only the photo's own (the user).<br>See `notes/REF_TERRIBLE_BOSS.md`. |
| 25.38–27.52 | **"company in the world, BlackRock."** |
| 27.52–38.18 | **"A company that manages $15 trillion in assets … than Steve Jobs ever did."**<br>• The $15T montage, with "$15 trillion" in the Dario serif white glow.<br>• Think School's columns, Jensen, Gates and Jobs have no money overlay (corner softening only). |
| 38.18–40.92 | **Elon: "Do you think BlackRock's a bad company?"** His own shot, through his short silent pause after "company?" (real video, no still), then a flash. The music is removed. It has the Palmer Luckey reel's look: a slow push, soft corners, grain, and stacked lowercase bold captions blurring in. |
| 40.92–84.13 | **"Back in the 1980s" to the end.** The Porsche reel's look, on 72 real video shots. Each shot is cut on a word, and there are no stills. Details below. |

**The second half in detail** (`tools/shotlist.py` REST2_V6, rendered by `tools/prep_v5.py rest2`):
- **Footage, all real moving video:** every source was searched with a CLIP index, and each span was checked for real motion and for hidden cuts. The sources are:
  - the Larry Fink, Jamie Dimon and Wall Street drives;
  - the BlackRock documentaries;
  - the 2008, JPMorgan and Dimon documentaries.

  Channel logos and burned-in words are cropped out, and no footage repeats from anywhere in the film.
- **The 1980s run:** warm and faded, with grain at low opacity and a little gate weave.
- **"but one bad bet … $100 million loss.":** the Higgsfield trader scene at 60 fps, at real speed under a slow push; on "$100 million loss." a white flash into the red take (the user's red keyframe of the same scene, animated).
- **"That was enough" / "threw out":** the walk-out, at 60 fps.
- **"in 1988":** exactly like ON EARTH (reel DdB8's "IT ISN'T"), with the Tesla reel's boxes snapping around the year.
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

**Captions:** `tools/captions.py`, all in the composition `s_caps`, each word on its aligned onset (the hook's line and "$15 trillion" are written in their scenes, in Dario's style). There are three styles:
- **To "…ever did.":** the Jensen reel's centre line, Inter Display SemiBold. The words cut in and the line re-centres. Key words ("everything", "evil", "BlackRock") are set alone in Instrument Serif with the Dario white glow.
- **Elon:** the Palmer Luckey reel's stacked lowercase Helvetica.
- **From "Back in the 1980s":** the Porsche reel's Instrument Serif Italic.
  - The words are set wide apart and laid out first.
  - Each fades in from a soft blur in its place.

**Sound:** no sound effects. A low drone sits under the voice, ducked; there is none under Elon and Rogan.

## Rebuild

```
python -I tools/align.py          # (torch venv) the word alignment -> tools/words/{vo,rest,rogan,line}.json
python -I tools/pace.py           # the pauses cut out -> tools/words/pace.json
python -E -s tools/prep_hook.py weap logos
python -E -s tools/prep_v3.py tiles articles touch jpm rogan2   # + rest_shots(REST1 names), r_tsg, r_jensen, r_gates, r_jobs
python -E -s tools/prep_v4.py finkflip cartel4 ceo4 dj4 orbit4 spot4 panel4 founders
python -E -s tools/prep_v5.py rest2 rogan dimon5 solomon5 owns   # rest2 also renders in parallel: rest2p0 … rest2p3, then rest2join
python -E -s tools/prep_v6.py evil
python -E -s tools/mix.py         # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
```
