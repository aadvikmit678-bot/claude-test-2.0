# BlackRock opening (16:9, 60 fps, 32.1 s)

HyperFrames project. Sources live in `blackrock-src/` (Drive downloads, git-ignored); every derived clip, still and the
mix are rebuilt by the scripts below (the scratch venv needs numpy, pillow, opencv-python-headless<5).

| Beat (film s) | What |
|---|---|
| 0.00-6.70 | the FII7 panel line ("I don't think there's ever been a panel...") on four panel shots, serif glow captions |
| 6.70-9.82 | "These are the most powerful people on earth": negatives, the Nvidia 3x3 tile flash on nine panelists, red ON EARTH card |
| 9.82-11.90 | "a $60 trillion dollar cartel": the money flipbook on white, then the cartel background with the eleven faces matched eye to eye |
| 11.90-14.62 | "weaponized capital that owns a piece of everything": opal's blueprints and tank, then the ownership pages |
| 14.62-15.75 | "you touch": the touch clip's painting and burst, then the panel from above with seats lighting up |
| 15.75-23.48 | Dimon and Solomon intros (the tfg reel): flash, window-light paper, the name behind the head, dark page |
| 23.48-25.28 | "Amongst them is this guy": the panel's orbiting shot with people glowing (the X-creative opening), Fink lit up |
| 25.28-29.37 | Fink on the BlackRock image, the red square on his face ("most evil"), BLACKROCK |
| 29.37-32.10 | Rogan/Musk clip from 12.55 s: Elon's question only, ending before Rogan's answer |

Type: Instrument Serif, League Gothic and Inter Display as before; the captions that were small italic labels are now
the Jensen Huang reel's caption, Helvetica (TeX Gyre Heros Bold) caps.

Rebuild:

```
python -I tools/prep_hook.py      # pre-rendered beats (tiles, money, cartel, weap, logos, touch, glow, these, search, thisguy)
python -I tools/prep_misc.py      # clips, cut-outs, stills, textures
python -I tools/mix.py            # assets/audio/mix.wav (+ mix_dry.wav: speech only)
python3 tools/build.py            # index.html + compositions/s_*.html
npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 -o renders/blackrock_opening_60fps.mp4
```

Cut-outs: `npx --yes hyperframes@0.9.46 remove-background` on the panel segments (Dimon 916 s, Solomon 2826 s), the Fink
interview (40.3 s) and the eleven portraits (see `blackrock-src/work/cut/run_cut*.sh`).
