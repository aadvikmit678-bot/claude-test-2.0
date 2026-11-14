# GTA 6: "here we go again" (edit spec)

1920x1080, 30 fps, ~110 s. HyperFrames. Voiceover: the user's `gta_Audio.mp3` (96.44 s), starting at film **9.26 s** (V = film − 9.26). No music bed (as in the Dimon film; the user adds music); the clips' own lines are used only in the cold open. Bundled sound effects on the transitions.

## Typography (from the three reels; see notes/refs/reel1-3.md)
| | value |
|---|---|
| font | Instrument Serif Regular; Italic only for a word the line leans on |
| colour | #FBF8EC with the Dimon serif glow (`SERIF_REST`); on light shots #0E0E0E with no glow |
| sizes | running 64 px · key line 96 px · hero 132 px · cold-open peaks 150-160 px (never the Dimon 190-240 px) |
| reveal | word by word on the spoken word (whisper word starts, 1 frame early), every word in its final place from the start |
| entrances | **bloom** (reel3): f0 blur 6 px + `SERIF_BLOOM` + scale 1.03 → f1 blur 2 px + `SERIF_SOFT` → f3 rest. **weight** (reel1): f0-1 faux-bold (2.5 px stroke) + blur 1.5 px + `HERO_BLOWN` + scaleX 1.08 (f1 smeared), f2 rest. **pop** (reel1): f0 scale 1.45 + bloom, f1 rest. **streak** (reel1): f0-1 vertical white streaks in the word's box, f2 the word in bloom, f3 rest |
| hold | never still: the block drifts left 30 px/s (linear), or slides in 70 px with an ease-out over 1.1 s and keeps drifting 12 px/s (reel3) |
| layouts | one centred line (y 540-640); reel3's stacked pair (line 2 indented 0.18 em·len, leading 0.82); reel2's words either side of a subject |
| exit | with the shot (hard cut) unless a transition carries it |

## Transitions (from the reels)
flash cut: 1 white frame (reel1) · bloom cut: overexposed frame → 1 negative frame → light-leak frame (reel3) · white bar wipe: a soft white band sweeps right→left over 6 frames (reel3) · TV static: 6 frames of noise (reel3) · double exposure: 2 frames at 50% (reel3) · vertical whip: 2 frames of vertical smear (reel2). Sound: `whoosh-short` on wipes and whips, `impact-bass` on the heroes, `glitch` on static.

## Footage rules
Plain cuts on the word. No pushes or slides on footage except where noted (the CRT push, the end logo). Vertical sources (took13, realwait, waiting, willnyc, edits, metav3rse) are cropped to a 16:9 band or shown as a 9:16 card over a blurred copy of themselves. Low-resolution clips (kidcine, escape, adultrush, fastclip, klickpin, millions) stay short and sit under the film grain. A light grain and vignette over everything (the Dimon grain).

## The film (as built: gta6/tools/edit.py is the source of truth)
Mostly GTA footage cut fast (trailers, the launch trailer, the Netflix gameplay, the fan montages in the folder), the named clips on their lines, no money footage. 94 shots in 110 s (median 0.9 s; the energetic middle ~0.5-0.8 s, the slow ending 1.3-1.8 s), plus the built scenes.

| film s | line | picture | type |
|---|---|---|---|
| 0.00-6.54 | news: "A video game so popular it could cost the US economy a billion dollars in just one day." | FOX 2 segment as is | stacked serif pairs, the $1,000,000,000 counter, "one day." highlight bar |
| 6.54-6.74 | | TV static | |
| 6.74-10.28 | CJ: "Ah shit, here we go again." + "That's exactly how" | San Andreas cutscene, subtitles cropped | italic flank either side of CJ |
| 10.28-12.02 | millions of adults are going to feel | millions (B&W crowd) → the 2013 launch crowd | **millions** hero |
| 12.02-13.26 | on November 19th | the city at night, darkened | "on November / 19th" (year inversion) |
| 13.26-14.46 | when they play GTA 6 | the Tesla reel's tile wall of trailer frames, the VI logo card lands on "GTA" | |
| 14.46-15.88 | for the first time. | Netflix gameplay (HUD) → the pool jump | weight flash |
| 15.88-17.77 | GTA 6 took 13 years | took13 as a 9:16 card | flank: "GTA 6 took" · "13 years" |
| 17.77-19.57 | and 2 billion dollars | robbery → gold dress → yacht → Jason and Lucia at the red car | the $2,000,000,000 counter |
| 19.57-20.40 | to make. | Vice City from the air | |
| 20.40-25.84 | The release got pushed from 2025 to May 2026, and then again to November. | the fan edit (billboard, flash) → COMING 2025 (struck) → MAY 26, 2026 (struck) → NOVEMBER 19, 2026 | captions above the cards |
| 25.84-28.46 | And yet, nobody seems to have moved on. | 2026 on the sofa → Times Square → "Welcome to Vice City" | stacked, top |
| 28.46-29.64 | But why? | the Tesla reel's white card | black serif, hero |
| 29.64-31.23 | Why are grown adults waiting | the red room, Vice City on the TV | |
| 31.23-31.96 | 13 years | the 2013 store, darkened | the 2013 → 2026 year roller + "years" |
| 31.96-35.20 | for a game that's supposedly just about stealing cars? | donuts → the red classic (fan montage) → Jason driving → the Ocean Drive chase | weight flash on "stealing" |
| 35.20-37.23 | Because GTA was never just about | reel3's wall of every GTA (Tommy, CJ, the V trio, Jason, Lucia) | stacked over a scrim |
| 37.23-38.32 | cars and guns. | the green supercar → Lucia firing | heroes, a flash on each |
| 38.32-40.38 | It was about what it really gave you. | arms up on the convertible → the cave diver → the dive | |
| 40.38-41.50 | Freedom. | freedom.mp4 | hero, bloom cut + bass |
| 41.50-43.03 | Back to being 10 years old, | kidcine | year inversion on 10 |
| 43.03-44.90 | sitting in front of the family computer, | the CRT with Vice City inside, a jump cut in | |
| 44.90-45.66 | playing Vice City | the Vice City logo | |
| 45.66-47.42 | with the volume turned all the way down | Vice City gameplay + a TV volume bar 16 → 0 | |
| 47.42-49.66 | so nobody could hear the gunshots. | the 10th-anniversary trailer, the explosion on "gunshots" | muzzle flashes |
| 49.66-53.78 | With cheat codes like ASPIRINE and PANZER scribbled at the back of your notebook. | the notebook page: ASPIRINE and PANZER written on the word, a jump cut in on PANZER, the Rhino polaroid | dark ink |
| 53.78-56.00 | For a kid, it wasn't just a game. | 2013: the boy and GTA V | |
| 56.00-59.58 | It was a psychological escape. An alternate reality. | escape.mp4 → Lucia's eyes → the fast clip → the cave | streaks on "escape" |
| 59.58-62.42 | It was everything you imagined adulthood would be. | the 2x2 grid filling a tile a word: gold dress, yacht, red car, Ocean Drive | |
| 62.42-67.80 | Driving supercars, firing guns, flying planes and owning an entire city. | 7 cuts: convertible, the Cheetah, firing, explosion, banner plane, seaplane gunman, the city with the Vice City blimp | weight flashes |
| 67.80-70.50 | And while every other game asks you to be the hero, | cops, the sheriff chase, Jason under the EXIT light | |
| 70.50-72.96 | but GTA lets you be the problem. | the masked robbery → static → the explosions | highlight bar on "problem." |
| 72.96-74.29 | It lets you be the bad guy | Lucia in the skull mask → running out of the store | |
| 74.29-76.64 | in a world that looks just like yours. | split: real Miami / Vice City | |
| 76.64-79.64 | And somewhere along the way, those kids grew up. | GTA V's ending → 2026: the boy, grown up | |
| 79.64-86.60 | Today, it's the exact opposite. It's an escape from adulthood, back to the world they once dreamed of living in. | the commuter rush → metro doors → the crossing → white wipe → sunset highway, golden hour, the balcony, the beach | |
| 86.60-92.32 | And on November 19th, Rockstar takes you back to Vice City, the city where it all started. | the NOVEMBER 19 billboard → R* → Tommy in pink → Ocean Drive 2002 → Ocean Drive 2026 | |
| 92.32-95.88 | So if you're still lost in Los Santos this week, don't rush. | Trevor → the dirt road (GTA V) | |
| 95.88-105.48 | Take the long way home. Drive slow. Because that 10-year-old ... never really left. He's just been waiting 13 years to feel that freedom again. | slow: sunset highway, the convertible, the kid, Tommy and Lance, the kid lying back, the red room, freedom.mp4 | Dario's square-then-dim on the slow lines |
| 105.48-110.00 | | the VI logo, then NOVEMBER 19, 2026 / PRE-ORDER NOW, fade out | |
