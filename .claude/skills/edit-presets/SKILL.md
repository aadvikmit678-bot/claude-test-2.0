---
name: edit-presets
description: The user's saved edit presets, named animations from their BlackRock edit, each with its Instagram reference reel and timestamps, reference frames next to ours, the exact numbers and the working code. Use when the user says "apply preset <name>", "use the <name> preset", runs /edit-presets, names one of powerful-man-rise, name-mosaic, built-red-word, founder-squares, counter-roll, crisis-date-grid, money-handoff, or asks which presets exist.
---

# Edit presets

Seven animations from the BlackRock edit (`blackrock-open/`, render v17), saved so a new edit can reuse them by name.

- `/edit-presets` lists them.
- `/edit-presets <name>`, or "apply preset <name>", applies one.

Each preset has a folder under `presets/` with three files:

- `PRESET.md`: what the animation does frame by frame, the reference reel and its timestamps, the numbers, the user's notes that shaped it, and the inputs a new edit swaps.
- `frames.jpg`: the reference reel's frames on top (gold labels) and ours below (blue labels), every frame labelled with its time. The user approved these sheets.
- `recipe.py`: runs the preset's steps with the code in `lib/`.

## The presets

| Preset | Made for (BlackRock v17) | Reference reel and timestamps |
|---|---|---|
| [`powerful-man-rise`](presets/powerful-man-rise/PRESET.md) | "This is the most powerful man on Earth", 0.00–2.68 s | Chainsmokers reel https://www.instagram.com/reel/DgHoW0vhPvb/ 0.2–1.7 s |
| [`name-mosaic`](presets/name-mosaic/PRESET.md) | "Larry Fink, the CEO of BlackRock", 2.68–5.67 s | Hemant Taneja reel (the user's Drive file "Copy of hemant taneja vid.mp4") 5.4–8.7 s |
| [`built-red-word`](presets/built-red-word/PRESET.md) | "...the most evil company ever BUILT", 7.87–9.57 s | Chainsmokers reel https://www.instagram.com/reel/DgHoW0vhPvb/ 8.4–9.8 s |
| [`founder-squares`](presets/founder-squares/PRESET.md) | Jensen Huang / Bill Gates / Steve Jobs, 24.10–29.63 s | Nvidia reel https://www.instagram.com/reel/DdB8LATJ_1z/ 0.0–1.0 s |
| [`counter-roll`](presets/counter-roll/PRESET.md) | "$100 million loss", 37.03–39.68 s | Kalanick reel https://www.instagram.com/reel/DdbK-PAT7O6/ 19.2–20.8 s |
| [`crisis-date-grid`](presets/crisis-date-grid/PRESET.md) | "When the 2008 crisis hit, the U.S. government called the one guy", 53.55–57.10 s | Chainsmokers reel https://www.instagram.com/reel/DgHoW0vhPvb/ 28.17–29.03 s + https://www.instagram.com/reel/DelkyjLP4p_/ 26.8–30.4 s |
| [`money-handoff`](presets/money-handoff/PRESET.md) | "He came out of that crisis with 3x the money", 60.72–63.57 s | Kalanick reel https://www.instagram.com/reel/DdbK-PAT7O6/ 39.0–44.0 s |

With no preset named, show this table and the `frames.jpg` of any preset the user asks about.

## Applying a preset to a new edit

1. Read the preset's `PRESET.md` and look at its `frames.jpg`. The reference row is the target; ours shows how it was matched.
2. Find the moment in the new edit and the word times it needs. Word times come from force alignment of the new voiceover, as in the BlackRock edit's `tools/align.py`. A picture changes 2 frames before its word (`LEAD = 2/60 s`).
3. Copy `lib/` into the new project's `tools/` and change the inputs listed under "Inputs" in `PRESET.md`: the source clips, the person's cut-out, the words and their times. Keep the skill's own `lib/` as the BlackRock reference.
4. Run the steps (`recipe.py`, or the same functions from the copy). The pre-rendered clips go to `assets/clips/` and `assets/img/`, and the scene function writes `compositions/<scene>.html`.
5. Run `npm run check`, snapshot the moment (`npx hyperframes snapshot --at ...`), and put the frames next to `frames.jpg`. Show the user before rendering.

## The rules every preset follows (from the user's notes)

- 1920×1080 at 60 fps, with no sound effects.
- Motion is smooth and subtle. No zoom in and back out; one slow push at most. Nothing sits still after it lands; it keeps drifting.
- Glow on type is white only. The one exception is a preset's own colour, such as BUILT's red.
- Captions have no commas or full stops. Abbreviation dots like "U.S." stay.
- Type is mostly Instrument Serif, with the bold Helvetica (TeX Gyre Heros Bold) for some lines, and never both in one line.
- No footage repeats. No money backgrounds or overlays, except the user's own money graphic.
- Words land on their spoken onset. Cuts land on the base cut's real cut frames, so the previous shot never shows for 2 frames.
- Every preset is matched to its reference frame by frame before it is shown to the user.

## lib/: the code

`lib/` holds the BlackRock edit's own code (`blackrock-open/tools/`), trimmed to what these presets use and copied as it is, comments included. Each preset's `recipe.py` lists its steps.

- **`tools/trim.py`** made `lib/`. It follows every name from each preset's entry functions. Re-run it if the BlackRock code changes: `python3 -I tools/trim.py lib`.
- **`tools/verify.py <preset>`** runs a preset from `lib/` into a scratch project and compares every output with the BlackRock project's own file.
- **Checked 2026-11-28:** run from `lib/` with the BlackRock inputs, every preset rebuilt the film's own files exactly. Every clip was frame-identical, every image identical and every scene file identical.
- **Needs:** Python 3 with numpy, opencv-python(-headless) and pillow (`pip install numpy opencv-python-headless pillow`), plus ffmpeg.
- **Paths (environment variables):**
  - `PRESET_ROOT` is the HyperFrames project it writes to: `assets/clips`, `assets/img`, `assets/fonts`, `compositions`. The default is this repo's `blackrock-open`.
  - `PRESET_SRC` is the project's source media. The default is `blackrock-src`.
  - `PRESET_REPO` is the repo root, used for `dimon-src`.
- **Not in git:** the source media (`blackrock-src/`, `dimon-src/`) came from the user's Drive and isn't committed. A new edit brings its own media anyway. The files each preset read are listed in its `PRESET.md`.
- **Word times:** `lib/timing.py` and `lib/words/*.json` are the BlackRock voiceover's. Map the keys a preset uses (listed in its `PRESET.md`) to the new words.

## Adding a preset

Use the same layout: `presets/<name>/PRESET.md`, `frames.jpg` (reference row above ours, frames labelled with times) and `recipe.py`. Add a row to the table above.
