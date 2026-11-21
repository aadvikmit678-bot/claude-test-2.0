# "The $100 million bet": the Higgsfield scene

**Where it goes in the film:** 48.1–54.0 s.

**The line:** "But one bad bet cost him a $100 million loss. That was enough to get him thrown out of Wall Street."

**What you approved:**
- You make the three keyframes in ChatGPT.
- I animate them on Higgsfield with **Kling 3.0 Pro**: 3 shots × 2 takes × 8.75 credits = **52.5 credits**. Your balance is 736.3.

## 1. Make the three pictures in ChatGPT

- **Order:** make shot 1 first. Then make shot 2 *from your shot-1 picture*, so it's the same man and the same desk. Then make shot 3.
- **Shape:** landscape 16:9. If ChatGPT gives you 3:2 that's fine; I crop it to 16:9 myself. Keep the man and the action in the middle.
- **The man:** he is never seen face-on, only from behind or as a silhouette. It's a dramatisation, not a fake Larry Fink.
- **Clean pictures:** no text, logos or watermarks. If it adds any, regenerate.
- **Sending them:** download each at full size as `shot1.png`, `shot2.png` and `shot3.png`. Put them in a Drive folder and send me the link, or attach them in the chat.

### Shot 1: "But one bad bet cost him" (48.1–49.7 s)

Attach: `ref_1_lamp_light.jpg`

```
Use the attached picture only for its light and colour: one warm brass lamp over a dark polished table, everything
around it falling into black.

Create a new photoreal 35mm film still, landscape 16:9. New York, 1986, late at night, the bond-trading floor of a
Wall Street investment bank. We look over the shoulder of a young trader in his early thirties, seen from behind so
his face is never visible: short dark hair, white dress shirt with rolled sleeves, dark suspenders. He holds a beige
desk phone with a coiled cord to his ear. In front of him a bank of six old CRT terminals glows green with columns of
tiny, unreadable figures. One hard overhead lamp throws a warm pool of light on his cluttered desk (paper trade
tickets, a calculator, an ashtray with a burning cigarette); the rest of the trading room is dark, empty desks and
screens fading into black, a thin haze of smoke in the light. Deep blacks, warm tungsten highlights, high contrast,
fine film grain, eye-level 35mm lens. No text, no logos, no brand names, no readable numbers, no watermark.
```

### Shot 2: "$100 million loss." (49.7–51.3 s)

Attach: **your `shot1.png`**

```
Same man, same desk and same room as the attached picture. Photoreal 35mm film still, landscape 16:9. The camera is
closer now, right behind him at shoulder height. Every CRT screen has turned deep red, full of tiny unreadable falling
figures; the red light floods over his shoulders, his white shirt and the desk, and the warm lamp has dimmed. He has
put the phone down; one hand rests flat on the desk and his head is slightly bowed. His face stays hidden. Keep the
centre of the frame calm and fairly dark, because a big white title will sit on top of it. Deep blacks, saturated
red, high contrast, fine film grain. No text, no logos, no readable numbers, no watermark.
```

### Shot 3: "That was enough to get him thrown out of Wall Street" (51.3–54.0 s)

Attach: `ref_2_red_city.jpg` **and** your `shot1.png`

```
Use the first attached picture only for its colours (towers glowing red-orange, deep black shadows) and the second
only for the man (the same young trader: short dark hair, white shirt, dark suspenders, now wearing his dark suit
jacket).

Create a new photoreal 35mm film still, landscape 16:9. New York, 1986, dusk. We are inside the dark marble lobby of a
Wall Street bank, behind him, as he walks out through the tall open doors carrying a cardboard office box with papers
and a desk lamp sticking out. He is a black silhouette against the glowing red dusk outside; beyond him, across the
narrow street, the columns of the New York Stock Exchange and old stone towers lit red-orange, an American flag
hanging still. His face is never visible. Deep blacks, red-orange light, high contrast, fine film grain. No text, no
logos, no readable signs, no watermark.
```

## 2. What I run on Higgsfield once you send them

Every take is Kling 3.0 Pro, 5 s, 16:9, sound off (no SFX). Your picture is the first frame.

| Shot | Motion prompt | Takes | Credits |
|---|---|---|---|
| 1 | Slow push-in over his shoulder. The green figures on the screens scroll, then the screens flicker and turn red one after another, left to right. He freezes, then slowly lowers the phone. Smoke drifts through the lamp light. One continuous shot, no cuts, no text. | 2 | 17.5 |
| 2 | Almost still camera with a slow push-in. The red screens pulse and flicker, red light shimmering over his back and the desk. He slowly lowers his head. Smoke drifts. One continuous shot, no cuts, no text. | 2 | 17.5 |
| 3 | He walks out through the doors and away from the camera into the red dusk, getting smaller; the heavy door swings slowly behind him. Slow steady camera with a slight handheld drift. One continuous shot, no cuts, no text. | 2 | 17.5 |
| | | **6** | **52.5** |

## 3. How it goes into the film

- **Shot lengths:** shot 1 runs 1.6 s and shot 2 runs 1.65 s, under the existing "$100 MILLION" title. Shot 3 runs 2.7 s.
- **Cuts:** the Nvidia reel's flash frames sit between the shots. The captions and voice don't change.
- **Callback:** shot 3 comes back for a split second, desaturated, at "the one guy Wall Street threw out years ago" (about 71.5 s).
- **What it replaces:** the five library clips there now: the head-in-hands trader, the ticker, the money, the "fired" clip and the NYSE.

## The reference pictures (not in git; they are frames of the user's Drive videos)

- `ref_1_lamp_light.jpg` is `blackrock-src/dl/v3/cartel_user.mp4`, frame 10 (1920×1080).
- `ref_2_red_city.jpg` is `blackrock-src/dl/v3/ending_user.mp4` at 8.0 s, `crop=566:318:85:80`, scaled to 1280×720, so the "@YS_MR4" watermark is cut off.

Status: waiting for the user's three keyframes. Nothing has been generated on Higgsfield yet. Quotes, all silent 16:9:

| Model | Setting | Credits |
|---|---|---|
| Kling 3.0 Pro | 5 s | 8.75 |
| Kling 3.0 Std | 5 s | 7.5 |
| Seedance 2.5 | 1080p, 5 s | 80 |
| Seedance 2.5 | 480p draft, 8 s | 24 |
| GPT Image 2.6 | 16:9 image | 0.75 |
