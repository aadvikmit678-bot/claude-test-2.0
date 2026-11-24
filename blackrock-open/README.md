# BlackRock (16:9, 60 fps, 69.85 s)

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
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 14 -o renders/blackrock_v9_60fps.mp4
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 14 --start 0 --end 23.9 -o renders/blackrock_v9_opening_60fps.mp4   # the new opening only
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

**v9 (Nov 24): a new opening.** The film now opens on the user's new recording ("This is the most powerful man on
Earth. Larry Fink, the CEO of BlackRock. … more of Apple than Steve Jobs ever did.", 24.6 s, its six pauses tightened by
0.64 s). It replaces the FII7 panel line, the Dimon / Solomon intros and the old "$15 trillion … ever did." part. Elon's
question and the second half are unchanged, only moved earlier. Delivered on its own: `renders/blackrock_v9_opening_60fps.mp4`
(0–23.9 s).

| Film s | What |
|---|---|
| 0.00–1.67 | **"This is the most powerful man"**. The Nvidia reel's wall build (a tile every 3 reel frames from the bottom right, each white for a frame): nine different rooms of Fink, live. "powerful" and "man" in the Dario serif glow on their words. The wall ends on "IT ISN'T"'s lead-in (strobe, a negative frame, two cyan). |
| 1.67–2.22 | **"on Earth."** Reel DdB8's "IT ISN'T" red card, as before. |
| 2.22–4.72 | **"Larry Fink, the CEO of BlackRock."** The Hemant video's name mosaic: a big centre tile and three small ones down each side, each arriving as a white card, then a different clip of Fink. "Larry Fink" in the Dario serif with its bloom (the frame washes out for two frames as it lands), "the CEO of" in the bold grotesque word by word. On "BlackRock" every tile flips to BlackRock's own buildings (its lit tower in the middle says the name). |
| 4.72–5.80 | **"The most evil"**. The red horned scene (reel DfhzVs8q9NH), re-timed: Fink rises through the pause, *most* / *evil* behind him. |
| 5.80–7.10 | **"company in the world."** The Earth at night (its 0.5 s slowed with motion interpolation, the puppet strings painted out), "company in the" small and **world** big in the Dario serif (the Dario video's EARTH). |
| 7.10–8.30 | **"A $15 trillion dollar"**. The user's sixteen "$15 trillion" headlines (Reuters, Yahoo Finance, Bloomberg, …) as the Opal reel's flipbook: every page placed so its own "$15 trillion" sits on one spot at the centre, at one height, in the lime highlight. |
| 8.30–11.65 | **"cartel of weaponized capital that owns a piece of everything you touch."** As the user approved it (the cartel table, the blueprint push, the glasses and brand maps, the fingers), ending on the burst's white frame. |
| 11.65–14.57 | **"A company that's never made a single physical product,"** The Hemant / Dario lockup: a card in the middle with things being made (circuit boards, a press, an assembly line), the words either side in the serif; on "product" the card flashes white and is gone, an empty frame. |
| 14.57–18.07 | **"yet it's one of the top shareholders in almost every major US company."** "top shareholders" in the serif; around it, cards with 28 companies' marks and tickers pop in (white for two frames, as the Hemant video's cards), slowly from "one of the", faster and faster to "company". |
| 18.07–23.90 | **"It holds more of Nvidia than Jensen Huang … than Steve Jobs ever did."** Think School's "Founders vs Blackrock" page as a motion graphic: its grey page, the product big on the left (the graphics card, the MS-DOS PC, the Macintosh), the founder switching on on its screen on his name (the Elon reel's old-TV device: Gates in green phosphor, Jobs in black and white; Jensen on a card), BlackRock's and the founder's bars on one scale with their figures rolling up in the serif (8.02 / 3.7, 8.18 / 1.34, 7.97 / 0.24 %), then "2.2× / 6.1× / 33× more". |
| 23.90–26.63 | **Elon: "Do you think BlackRock's a bad company?"** As before. |
| 26.63–69.85 | **"Back in the 1980s" to the end.** As before (the Porsche reel's look on 72 real shots). |

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
python -I tools/align.py          # (torch venv) the word alignment -> tools/words/{open,rest,rogan,...}.json
python -I tools/pace.py           # the pauses cut out -> tools/words/pace.json
python -E -s tools/prep_hook.py weap logos
python -E -s tools/prep_v3.py tiles articles touch jpm rogan2   # + rest_shots(REST1 names), r_tsg, r_jensen, r_gates, r_jobs
python -E -s tools/prep_v4.py finkflip cartel4 ceo4 dj4 orbit4 spot4 panel4 founders
python -E -s tools/prep_v5.py rest2 rogan dimon5 solomon5 owns   # rest2 also renders in parallel: rest2p0 … rest2p3, then rest2join
python -E -s tools/prep_v6.py evil
python -E -s tools/prep_v9.py wall articles mosaic cuts products founders factory   # the v9 opening (+ prep_v3 touch, prep_v4 cartel4, prep_hook weap, prep_v5 owns)
python -E -s tools/mix.py         # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
```
