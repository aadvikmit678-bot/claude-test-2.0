---
name: omni-video
description: Generate AI video clips with Google's Gemini Omni Flash (the Gemini API's video model, successor to Veo there) for a HyperFrames edit - b-roll, establishing shots, a shot that continues from a frame of the composition, a transition between two frames, a consistent character. Use when an edit needs footage that does not exist, or the person says generate a clip, Veo, Flow, Omni or AI video. Paid per second; always quote the cost first.
---

# omni-video — generated footage for HyperFrames edits

Generates 3–15 s clips with `gemini-omni-1.2-flash` through the Gemini API Interactions endpoint
and saves an MP4 plus a `<name>.omni.json` record (prompt, settings, interaction id, usage, cost).
Load `/hyperframes` before placing a clip, and `/media-use` (`references/media-treatments.md`)
before changing how it looks.

## Rules

1. **Money first.** Every call is billed. Before generating, run with `--estimate`, tell the person
   the clip(s), length, resolution and total cost, and wait for their OK. A batch can be approved
   at once. Never loop retries on a failure that costs money.
2. **Draft cheap.** Look tests at `360p` (~$0.023/s); finals at `720p` (~$0.07/s). `1080p` (~$0.10/s)
   and `4k` (~$0.21/s) are upscaled, so only use them when the composition needs it.
3. `--max-cost` (default $2) stops a call whose estimate is above it.
4. Generated clips are a fallback: real footage, the person's media and registry blocks come first.

## Run it

```bash
node .claude/skills/omni-video/scripts/omni-video.mjs --prompt "<shot>" --duration 6 --resolution 360p --estimate
```
```bash
node .claude/skills/omni-video/scripts/omni-video.mjs --prompt "<shot>" --duration 6 --resolution 720p --out <project>/assets/generated/<name>.mp4
```

| Option | Use |
|---|---|
| `--duration 3..15` | whole seconds (3–10 with `--last`); default 8 |
| `--aspect 16:9 / 9:16` | match the composition's `data-width`/`data-height` |
| `--first img` | the shot starts on this frame: take it with `npx hyperframes snapshot --at <t>` to continue a shot |
| `--first a --last b` | a generated transition between two frames |
| `--ref img` (×≤6) | keep a character or product consistent (≤3 per subject, ≤2 subjects) |
| `--task` | force `text_to_video`, `image_to_video` or `reference_to_video` if the prompt does not pick the mode |

Prompt like a shot list: subject, action, camera move, lens/look, light, and end state. There is no
negative-prompt field: say what to avoid in the prompt.

## Audio

Clips come with generated sound. When the edit has its own music or voiceover, end the prompt with
"No dialogue, no music." and place the clip `muted`. Keep the clip's sound only when it is wanted:
then the `<video>` carries `data-has-audio="true"` and no `muted` (project rule 4).

## Place it

1. `ffprobe -v error -show_entries format=duration -of csv=p=0 <clip>` for the real length.
2. Put it in the composition as a timed clip (`class="clip"`, `data-start`, a duration), muted unless
   its sound is used.
3. `npm run check`, then `npx hyperframes snapshot --at <times>` around the clip and look at the frames.
4. Keep the `.omni.json` beside the clip; it is how a shot is regenerated or explained later.

## Key and billing

- The script sends `x-goog-api-key`. It reads `$GEMINI_API_KEY`, else the file in `$GEMINI_API_KEY_FILE`,
  else sends a placeholder that the cloud environment's network secret replaces (host
  `generativelanguage.googleapis.com`, header `x-goog-api-key`). Never write a key into the repo.
- `429 ... limit: 0 ... Free Tier` or `RESOURCE_EXHAUSTED`: the key's project has no video quota.
  Video has no free tier: billing must be on for that project in AI Studio.

## Limits

3–15 s per clip; SynthID watermark on every output; English prompts are best supported.
Editing or extending an existing clip (the API's `edit` / `extend` tasks) needs a Files API upload and
is not wired into the script yet.
