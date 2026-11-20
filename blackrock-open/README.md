# BlackRock opening (16:9, 60 fps, 32.1 s)

HyperFrames project. Sources live in `blackrock-src/` (Drive downloads, git-ignored), plus the JPMorgan clips from
`jpm-dimon/assets/clips2/`; every derived clip, still and the mix are rebuilt by the scripts below (the scratch venv
needs numpy, pillow, opencv-python-headless<5). The references and what was measured from them: `notes/REFERENCES_v2.md`.

| Beat (film s) | What |
|---|---|
| 0.00-6.70 | the FII7 panel line ("I don't think there's ever been a panel...") on four panel shots |
| 6.70-9.82 | "These are the most powerful people on earth": negatives, the Nvidia 3x3 tile flash on nine panelists, red ON EARTH card |
| 9.82-11.90 | "a $60 trillion dollar cartel": the money flipbook on white, then the cartel background with the eleven faces matched eye to eye |
| 11.90-14.25 | "weaponized capital that owns a piece of everything": opal's blueprints and tank (cropped to 16:9), the ownership pages |
| 14.25-15.13 | "you touch": the touch clip's painting, the pixel hands sliding together, the burst |
| 15.13-15.75 | split second: the panel from above in the X-creative grade, one snap push-in, people lighting up as white silhouettes |
| 15.75-17.72 | "That's Jamie Dimon, the guy running": the tfg page -- tiled coral JAMIE DIMON closing up behind him, his ~2 s rise |
| 17.72-19.15 | "JP Morgan Chase": HQ with its flags, people at its doors, its NYSE board, its sign -- plain cuts |
| 19.15-20.08 | "David Solomon": his speaking close-up, then the Hemant flash (his silhouette strobing cream) |
| 20.08-20.98 | "a part-time DJ": the D-Sol video, three plain cuts |
| 20.98-22.87 | "and the CEO of Goldman Sachs": the panel shot where its own title lands on "CEO" |
| 22.87-24.37 | the camera circling the table; from "Amongst them" people light up at random, then Fink alone |
| 24.37-25.28 | "is this guy": Fink's close-up at the panel |
| 25.28-26.80 | "the man who runs the most evil": Fink on stage; the interview, the VC reel's red square on "most" |
| 26.80-29.37 | "company in the world. BlackRock.": its letters on stone, building and flags, its doors, the steel letters |
| 29.37-32.10 | Rogan/Musk clip from 12.55 s: Elon's question only, ending before Rogan's answer |

Type: ON EARTH / WEAPONIZED / CAPITAL in League Gothic, POWERFUL / PEOPLE and the "$60 trillion" words in Inter Display,
the giant JAMIE DIMON in Bodoni Moda (compressed to the tfg reel's letters), "most evil" in Instrument Serif; every
storyline caption is the Jensen Huang reel's caption, Helvetica (TeX Gyre Heros Bold) caps. No sound effects.

Rebuild:

```
python -E -s tools/prep_hook.py   # hook beats (these, tiles, money, cartel, weap, logos, touch)
python -E -s tools/prep_misc.py   # panel clips, cut-outs, stills, the line / vo / rogan audio
python -E -s tools/prep_v2.py     # glow, orbit, the Dimon page, the Solomon flash, every plain-cut shot
python -E -s tools/mix.py         # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 -o renders/blackrock_opening_60fps.mp4
```

Cut-outs: `npx --yes hyperframes@0.9.46 remove-background` on the panel segments (Dimon 916 s, Solomon 2826 s), the Fink
interview (40.3 s) and the eleven portraits (see `blackrock-src/work/cut/run_cut*.sh`). The glowing people are hand
outlines (`OVER_POLY`, `ORBIT_POLY` in `tools/prep_v2.py`): the remover keeps only one or two people in a wide shot.
