# GTA 6 edit: the reference folder, studied

Drive folder `1Li0fFSxSyK9EHdm2Y2T8mp5Pjg2TYvHK` (24 files, 2.2 GB), downloaded to `gta6-src/_drive/<key>.mp4` (not in git; `gta6-src/manifest.tsv` maps keys to Drive ids and titles). Every clip's frames were read by `gta6/tools/study.py` (a 480p proxy of every frame; every cut, flash and black frame; the music's onsets and tempo; a transcript of the speech). The edit references were then looked at frame by frame on `gta6/tools/dense.py`'s sheets (every frame, or every 2nd-15th for long or slow clips); the raw trailers and the long gameplay film were indexed shot by shot (one still per shot, four across every long take). One file per clip in `notes/refs/` has the shot-by-shot breakdown. **Nothing is built yet** (the user's instruction: study first, the script and references come next).

## The folder at a glance
| key | file | format | length | what it is |
|---|---|---|---|---|
| editm6 | edit montage gta 6 | 16:9, 60 fps | 13 s | R* logo, one shot a beat with 2-frame white flashes and split wipes, VI logo |
| ahhshit | edit ahh shit | 16:9, 30 fps | 20 s | "Oh shit!" over black, then a flash-heavy montage: face duel, B&W portraits, VICE sign, logo line-draw |
| blade | Video by blade.fxs | 4:3, 60 fps | 33 s | calm story montage, hard cuts on the beat, logo over the opening aerials, stutter cuts; dance-pop song |
| montage | gta montage | 1:1, 30 fps | 29 s | cinematic long shots, logo built word by word, lens-flare ending, "©BROOKLYNFILMS" |
| montage2 | gta montage 2 | 16:9 **rotated** in 9:16, 60 fps | 16 s | a zoom-blur crossfade on every cut, ~0.65 s a shot, logo over Jason |
| editmontage | gta edit montage | 1.3:1, 60 fps | 12 s | split-screen entries, tilted photo cards, PiP, shrink-to-corner exit; 23 of 24 cuts on the beat |
| vox | gta vox style cuyt | 4:3, 20 fps | 15 s | paper-collage animation of the official key art: cut-outs, echoes, ransom-note lyric type, pull-quote card, postcards |
| gta5nost | gta 5 character vides nostalgia | 1:1, 24 fps | 37 s | **AI** live action: the GTA V trio hand over to Jason and Lucia on a desert road; "See You Again" |
| oldchars | gta old characters meetuop | 4:3, 24 fps | 55 s | **AI** live-action sketch: Tommy Vercetti and CJ, "a very important mission", "YOU ARE READY?" sofa reveal |
| realwait | real people waiting for gta 5 old | 9:16, 50 fps | 17 s | "2013" (GTA V launch crowds) vs "2026" (alone on a sofa waiting for the download) |
| waiting | person waiting for gta 6 | 9:16, 60 fps | 34 s | a man in a red-lit room playing GTA Vice City on his TV, waiting |
| willnyc | Video by will__nyc | 9:16, 60 fps | 15 s | the GTA VI billboards in Times Square and Penn Station; caption "GTA 6 is taking over New York🔥" |
| edits | edits | 9:16, 30 fps | 15 s | real drone: the Miami arena lit "Welcome to Vice City VI" |
| city | gta city | 16:9 **rotated** in 9:16, 60 fps | 84 s | slow night aerials of Vice City, the "Welcome to vice city VI" neon card |
| awshit | Aw shit, here we go again (San Andreas) | 16:9, 30 fps | 11 s | the original 2004 CJ cutscene line |
| billion | GTA 6 launch could drain $1 billion | 16:9, 30 fps | 272 s | FOX 2 Detroit news segment, the "$1 billion / call in sick" story, an interview |
| trailer1 | GTA VI Trailer 1 | 1080p | 90 s | official (Dec 2023): Lucia in prison, Vice City life, social clips, the robbery |
| trailer2 | GTA VI Trailer 2 | 1080p | 167 s | official (May 2025): Jason in the Keys, the prison meeting, the robbery, nightlife, action |
| launchps5 | GTA VI Launch Trailer (PS5) | **4K** | 90 s | official launch trailer: "November 19, 2026"; **the master copy** |
| launch1 | GTA VI Launch Trailer (1) | 4K | 90 s | identical to launchps5 |
| launch | GTA VI Launch Trailer | 1080p | 90 s | the same trailer at 1080p |
| netflix | An Extended Look (Netflix) | 4K | 26 s | Netflix teaser with in-game HUD footage |
| preload | Pre-Load Now | 1080p | 30 s | official "pre-load now" spot, party energy |
| netflix4k | GTA 6 4K Gameplay Trailer FULL NETFLIX EXTENDED | 4K | 26.8 min | 27 minutes of story gameplay: the drug-den pickup, the apartment, Brian's dinner, the store robbery and getaway, an activities montage, the skydive, Andres de Leon and the MegaMundo party attack; HUD on the gameplay shots |

## The edit styles in the references
1. **Flash-beat montage** (editm6, ahhshit): one shot a beat (0.3-0.6 s), a white flash on almost every cut (2 frames at 60 fps; 3-5 fading frames at 30 fps), split wipes, silhouette flashes, B&W runs; logo bookends.
2. **Calm hard-cut story montage** (blade, montage): shots of 2-4 beats, plain cuts on the beat, the trailer's own grade; logo over the opening shots or built word by word; stutter cuts for energy.
3. **Transition-led montage** (montage2, editmontage): every cut is a designed transition: a 2-frame zoom-blur crossfade, or split-screen / card / PiP entries.
4. **Collage / "Vox" explainer** (vox): official key art cut out on paper at 20 fps, echoes, torn paper, ransom-note and newspaper type.
5. **Story and meme shorts** (realwait, gta5nost, oldchars, awshit, waiting): a single idea (then vs now, torch-passing, the old crew reacting, the wait), long holds, dialogue-led.
6. **Real-world hype** (willnyc, edits, billion): billboards, the arena, the news story.

## Device library (frame-exact, from the references)
| device | where | how |
|---|---|---|
| white flash on the cut | editm6 f242-243, 275-276, 395-396 ... | 2 pure white frames at 60 fps (33 ms) |
| warm fading flash | ahhshit f22-24, 49-51, 130-132 ... | blown-out frame fading over 3-5 frames into the next shot |
| half-frame split wipe | editm6 f199-204, 303-307, 427-429, 493-494 | the new shot fills one half (vertical or horizontal) for 2-5 frames |
| silhouette matte flash | editm6 f269-270, 388-389 | a moving person filled solid white (or black) for 1-2 frames |
| X light streak | editm6 f351-356 | two diagonal streaks with RGB fringe, a white frame, the X lingers |
| radial spin zoom | editm6 f555-560 | a swirl into the next shot |
| zoom-blur crossfade | montage2, every cut | 1-2 frames blending both shots with radial blur |
| split-screen entry | editmontage f29, 268, 382 | the next shot as a half for 15-30 frames, then full; halves swap |
| tilted photo cards | editmontage f156-196 | a card a half-beat, slightly rotated, ending on the key art |
| PiP grow | editmontage f337-366 | the next shot in a card, which grows to full frame |
| shrink to corner | editmontage f674 | the whole frame shrinks into the top-left corner, black |
| face duel | ahhshit f105-170 | two extreme close-ups alternating every ~10 frames, tighter each time, a flash on each switch |
| B&W portrait run | ahhshit f329-425 | high-contrast black and white faces |
| logo line-draw | ahhshit f472-503 | the VI outline drawn stroke by stroke, a burst into the filled logo |
| logo word build | montage f0-112 | VI, then GRAND, THEFT, AUTO, a word each ~0.27 s |
| logo overlay | blade 0-3.9 s, montage2 5.25-5.92 s | the wordmark small and centred over shots |
| stutter cuts | blade f702-772, 918-940, 1807-1875 | jump forward 2-6 frames at a time on the beat |
| fade through white | editm6 f659-662 | 4 frames, for the calmer ending |
| lens flare + iris out | montage f806-866 | teal anamorphic flare, vignette closes to black |
| collage cut-outs, echoes, torn paper | vox | 20 fps stop-motion, 6-8 stepped copies, paper wipes |
| type-on lyric blocks | vox f122-145 | white condensed caps in black blocks, word by word |
| newspaper pull quote | vox f158-188 | condensed caps on a black tab, red brush underlines, serif body text |
| year label | realwait | one white "2013" / "2026" centred for the whole section |
| social caption | willnyc | white typewriter font "GTA 6 is taking over New York🔥" |
| title stickers | oldchars f1020- | "grand theft auto VI" + "YOU" "ARE" "READY" "?" placed round the frame, GTA font, black outlines |

## Audio in the folder
- Meme lines: "Ah shit, here we go again" (awshit 0.13 s, CJ, clean), "Oh shit!" (ahhshit 0.12 s).
- Trailer dialogue: Lucia "Bad luck, I guess" (trailer1); "I am here for Lucia Caminos" / "What's your name?" "Jason." (trailer2); "I got in some trouble in the army..." / "Are we gonna be okay?" (launch).
- The long gameplay film (netflix4k): "I guess they know we're coming" (0.0); Brian's carousel story, ending "You gotta know when to get off, Jason" (684-744); "Are you a professional?" "We'll see." (~903); "This could be the start of something good" (~1000); Brian's closing "These are your glory days ... nothing is gonna beat who you are now ... Trust me." (1549-1570). Strong language elsewhere.
- News: "A video game so popular it could cost the US economy a billion dollars in just one day" (billion 0.04 s) and the guest's quotes (see refs/billion.md).
- AI sketches: "You did good." / "We've got it from here." / "Go. They're waiting for you." (gta5nost); "I got a mission" / "a very important mission" (oldchars).
- Songs (copyrighted, for reference only): Tom Petty "Love Is a Long Road" (trailer1), The Pointer Sisters "Hot Together" (trailer2), Wiz Khalifa "See You Again" (gta5nost), and the edits' tracks.

## Raw footage: what to cut from
Use the 4K launch trailer (launchps5) and the 4K Netflix files first (the 26-minute netflix4k has the most variety: real gameplay with the HUD, the party, the races, the skydive), then trailer2 and trailer1 (1080p). Each has a shot index with times in `refs/`. Avoid the frames with burned-in text when a clean shot is needed: ESRB cards, "ROCKSTAR GAMES PRESENTS", the PS5 cards, the Netflix HUD.

## Caveats
- montage2 and city are landscape pictures rotated 90° inside a 9:16 file: rotate before use.
- gta5nost and oldchars are AI-generated live action, not official footage.
- Burned-in text: ahhshit (a small "ent" watermark), vox (yellow subtitles, PEGI badge), willnyc (the caption), oldchars (subtitles, the end title), realwait (the year labels), billion (FOX 2 graphics), awshit (game subtitles).
- The launch trailer exists three times (two identical 4K copies and a 1080p copy).
