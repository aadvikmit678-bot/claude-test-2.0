# v18: the notes on the v17 render

`tools/build18.py` (from build17) writes `tools/media_v18.json`. The film is 85.02 s at 60 fps (0.13 s shorter than v17: the pause after "Chase").

Rebuild (after the earlier prep steps in `notes/v16/notes.md` and `notes/v17/notes.md`):

```bash
export DIMON_ROOT=<repo root> CV4_DIR=<repo root>/dimon-work/cv4
python3 -I tools/prep18.py fired                   # the nine photo squares of "a guy who got FIRED"
python3 -I -X utf8 tools/build18.py --specs        # writes tools/media_v18.json
python3 -I tools/prep2.py --spec=media_v18.json    # cuts the clips
python3 -I -X utf8 tools/build18.py                # writes index.html and compositions/
npx --yes hyperframes@0.9.2 render --fps 60 --workers 2 -o renders/jpm-dimon-v18.mp4
```

## The notes and what v18 does

| Note | What v18 does |
|---|---|
| "For the very start, 'the name of the game in American capitalism', I want that to be Instrument Serif, exactly the way we animated with that glow effect … that comes like the Dario video." | "The name of the game" and "in American" are Dario's serif words: a glowing square marks each word's place for two frames, the word comes in dim for a frame and then sits in its glow, and the line leaves in the order it came. They are 120 and 108 px (Dario's are 92) because they carry the opening alone. "capitalism" keeps its big serif and flash. |
| "After JP Morgan Chase … there's a slight pause to 'This is the most influential' … reduce that pause, slightly." | The reporter's "Chase" ends at 8.37 s and the narration's "This" started at 8.63 s. Four frames (0.13 s) of that silence come off the end of the opening scene: the cyber portrait now comes in as "Chase" ends, and everything after it comes four frames sooner (`PAUSE_CUT`; the portrait's own beat grid moves with its first frame, so nothing inside it changes against the voice). |
| "A guy who got fired: the last photo comes there for a very long time … I want more photos, so the photos keep on happening, and the frame keeps on getting bigger. Then directly cut to 1998 … the last photo can be the black-and-white one … faces at the side … another person in the 7th or 8th photo … a wall in the second-last … the zoom at the end is abrupt; maintain the consistency of the zoom." | `sp_fired_run`: nine new squares of young Dimon (`tools/prep18.py fired`), each alone in the frame and centred on his face at the same size, youngest first, the black-and-white portrait last. They change every three frames up to the cut; the black-and-white one has the last five. The square grows at one steady rate (the same ratio every frame) from the first photo to the cut, with no jump, blur-in or hold on the last one, and the film cuts straight to 1998. |
| "The grudge word also, I want in Instrument Serif normal." | "Grudge" is upright, with the flash. |
| "The G of United States government to be capital." | "United States Government". |
| "Bezos … only his cut-out head is coming … I don't know why you have cut out the body … you can have the glow on full masking on his face too." | No head-only frames. The whole cut-out of him comes up from below in two low-frame-rate steps and lands with a white glow over his whole shape, face included (one frame, then one at half), then he simply stands there. The words keep their times. |
| "He takes over the broken bank. The photo in the background is very bad. Change it for a video." | "he takes over": Dimon walking out of the building towards the camera. "a broken bank": the Bank One tower with its sign. Both are moving shots from the documentary. |
| "Billions in Profit: B and P capital." | "Billions" and "Profit". |

## Checks

`hyperframes lint`: 0 errors. `hyperframes check`: ok, 0 errors in lint, runtime, layout, contrast (10 of 10 samples pass) and audio. Every changed moment was looked at in stills before the render.
