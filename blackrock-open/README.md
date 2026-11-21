# BlackRock (16:9, 60 fps, 90.85 s)

This is a HyperFrames project.

- **Sources:** the Drive downloads live in `blackrock-src/` (git-ignored), plus the clip library in `jpm-dimon/assets/clips2/`.
- **Derived media:** every clip, still and the mix are rebuilt by the scripts below. The scratch venv needs numpy, pillow and opencv-python-headless<5.
- **References:** what was measured from them is in `notes/REFERENCES_v2.md`.
- **Higgsfield scene:** 48.1–54.0 s is the Higgsfield scene; its prompts, picks and credits are in `notes/HIGGSFIELD_SCENE.md`.

## Preview and render

```
npx --yes hyperframes@0.9.46 preview                 # Studio in the browser (http://localhost:3002)
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 -o renders/blackrock_60fps.mp4
```

## Beats

| Film s | What |
|---|---|
| 0.00–6.70 | **The FII7 panel line.** Wide, then overhead. From "financial talent", four panelists talk, with a white flash into each one. No zooms. |
| 6.70–8.72 | **"These are the most powerful people".** From "These": the Nvidia reel's negative frames and its 3×3 tile flash, over nine panelists. |
| 8.72–9.82 | **ON EARTH** on the user's plain red. |
| 9.82–10.67 | **"a $60 trillion".** An Opal-style article flipbook made from the user's cut-outs, centred, with a subtle zoom. |
| 10.67–11.90 | **"cartel".** The user's cartel video as it is: from the flash on the table, then the faces with their glitches. |
| 11.90–12.98 | **"weaponized capital".** Opal's tank. WEAPONIZED comes and goes; CAPITAL has no bounce. |
| 12.98–14.25 | **"that owns a piece of everything".** The ownership pages. |
| 14.25–15.13 | **"you touch".** The touch clip, from the black hands. |
| 15.13–15.75 | **The explainer's puppet.** |
| 15.75–17.72 | **"That's Jamie Dimon, the guy running".** The reference edit's "intelligence" intro: a red band, white type, Instrument Serif glow. |
| 17.72–19.15 | **"JP Morgan Chase".** The Attention Compounds "man behind OpenAI" device, using JPMorgan videos. |
| 19.15–20.82 | **"David Solomon, the part-time DJ".** His name huge in white glow behind him, a broad red bar, and "a part-time DJ" vertical in yellow. |
| 20.82–21.47 | **The DJ clips.** |
| 21.47–22.87 | **"and the CEO of Goldman Sachs".** The OpenAI device again, using the Goldman video. |
| 22.87–24.23 | **"Amongst them".** The camera circles the table while people light up at random. |
| 24.23–25.28 | **"is this guy".** The group picture, with the spotlight reel's third-second treatment on Fink. |
| 25.28–29.37 | **"the man who runs the most evil company in the world, BlackRock."** Fink on stage, the red box on "most evil", then BlackRock's letters, building, doors and sign. |
| 29.37–33.38 | **"A company that manages $15 trillion in assets".** The HQ flags, the tower, the FT's $15.5tn, and the glass tower. |
| 33.38–39.93 | **"holds more of Nvidia than Jensen Huang … than Steve Jobs ever did."** Think School's graphic, one company at a time, with dark captions on its grey page. Jensen is the Nvidia reel's own opening clip; Gates and Jobs get the same negative and tile-flash treatment. |
| 39.93–43.67 | **Elon on Rogan: "Do you think BlackRock's a bad company?"** The clip's burned-in subtitle is removed and the film's own captions go on top. Then a 1 s pause on the same shot. |
| 43.67–83.47 | **"Back in the 1980s … in this guy's hands."** Videos only: Fink, BlackRock, Wall Street, 2008. Big words: $100 MILLION, RISK., 2008, 3X. A red 1988 card. |
| 48.07–54.03 | **The Higgsfield scene.** "But one bad bet cost him a $100 million loss. That was enough to get him thrown out of Wall Street." The user's ChatGPT keyframes, animated with Kling 3.0 Pro: the trader's green screens turn red, then the red room under $100 MILLION, then he walks out into Wall Street with his box. The walk-out comes back in grey at "threw out years ago" (71.52 s). |
| 83.47–88.90 | **"A company that has never made a single product, but everything you own, everything you touch".** The user's ending video, cropped below its watermark. |
| 88.90–90.85 | **"has a piece of him in it."** Fink at the panel. |

## Type and sound

**Display type:**
- ON EARTH, WEAPONIZED, CAPITAL and the big words: League Gothic.
- POWERFUL and PEOPLE: Inter Display.
- The Dimon and Solomon intros: Instrument Serif glow.

**Storyline captions:** every one is the Jensen Huang reel's caption, Helvetica caps (TeX Gyre Heros Bold), white with a soft shadow. There are two exceptions:
- they're dark over Think School's page;
- they get a heavier halo over the ending video, which strobes white.

**Sound:** no sound effects. A low drone sits under the voice, ducked.

## Rebuild

```
python -E -s tools/prep_hook.py   # hook beats (these, tiles, money, cartel, weap, logos, touch)
python -E -s tools/prep_misc.py   # panel clips, cut-outs, stills, the line / vo / rogan audio
python -E -s tools/prep_v2.py     # glow, orbit, the Fink box, BlackRock, the v2 plain-cut shots
python -E -s tools/prep_v3.py     # v3: opening b-rolls, tiles, articles, cartel, Dimon/JPM, Solomon/CEO, orbit, spot,
                                  # Think School, Jensen/Gates/Jobs, rogan2 (caption removed), the Higgsfield scene (bet),
                                  # every rest-of-script shot
python -E -s tools/mix.py         # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
```

- **Shot list:** the rest of the script, shot by shot, is `tools/shotlist.py`.
- **Timings:** `tools/timing.py` holds every time, on a 60 fps grid.
- **Rogan clip:** its subtitle is removed with a clean plate made from the clip's own caption-free frames (`rogan_plate` and `rogan_clean` in `tools/prep_v3.py`).
