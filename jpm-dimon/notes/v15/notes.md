# v15: the second batch of notes on the v13 render (43-60 s)

`tools/build15.py` (from build14) writes `tools/media_v15.json`. The film is 85.62 s. **Not rendered yet.**

Rebuild: as v14, with `python3 -I tools/prep15.py` first (the retimed Flow clip, the Bezos cut-out, the warehouse background) and `build15.py`.

| Note | What v15 does |
|---|---|
| "For '18 months of no job, he took up boxing and read biographies' ... the video I've created with Google Flow. Remove the Gemini logo." | Their clip plays for the three phrases with its own captions; nothing of ours is drawn over it. The sparkle (bottom right) is removed with ffmpeg delogo. The boxer and the reader already run at the voice's pace; the 1 s title is held for the 2.2 s the phrase takes (its bloom-in as it is, its settled part stretched with blended frames). The Renaissance cards of v13 are gone. |
| "'Even met Bezos for a job at Amazon': this frame from the 48-second Dario video. I want it exactly like that." | `kflank`, read off the Dario reel's 47.36-49.0 s frame by frame: their warehouse picture dim and still; their Bezos picture cut out; the head alone for three frames, then the whole figure on a white burst; "even met / Bezos" and "for a job at / Amazon" flanking him as "one of the / most" and "powerful / AI" flank Dario; the reel's way out (the left words in a white box, two soft frames with a teal box over the eyes). The words are in the film's emphasis serif. |
| "That transition [after Amazon] is very very bad ... this 50-second clip is also very bad ... this photos clip, clips coming, is also very bad. It is not smooth." | The shrinking Bezos card, the finger-to-his-lips clip and the popping cards are gone. One steady shot for "But it was all a premise": him walking up the street in his coat (MPB 1909.6), plain cuts in and out. |
| "Why, in 'cleaned it up', is the image panning to the left?" | The office-floor shot and its arrival are gone. He stays on screen for "cuts the dividend, cleaned it up", one continuous take. |
| "I want 'up' in Helvetica" | "cleaned it up" is all Helvetica Bold. |
| "$60 million: why are 60 and million looking very different?" | "$60 million", "$500 million" and "$10 trillion" are each one phrase in one style, the emphasis serif. The bold Helvetica counters beside serif units are gone (the year counters stay). |

`lint`: 0 errors. `check`: ok, 0 errors. Stills looked at for every change. No render.
