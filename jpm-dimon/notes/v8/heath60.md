# The Heath Ledger reel at its own 60 fps (v8)

Source: instagram DfXuoMjR0Ru, 1920x1080, **60 fps** (v7 read a 720p 30 fps copy, which drops every other frame). Read frame by frame from 0 to 9.6 s with per-frame luma and frame differences. Frame n = n/60 s.

## The shot list, 0-273 (the first 4.55 s)

| Frames | Picture | Frames held | Device |
|---|---|---|---|
| 0-3 | P1: Heath as a child, face centred | 4 | pulls back 7.5 % over 0-2; soft white bars slide in at the name places (1-3) |
| 4 | black | 1 | |
| 5-9 | P1 again | 5 | 5 dimmed (luma 71 against 125); a half-frame negative rectangle on the face (5-13) |
| 10-13 | P2: the school portrait | 4 | the rectangle stays across the cut; 13 dimmed |
| 14 | black | 1 | |
| 15-18 | P2 clean | 4 | the name flanks the face |
| 19-28 | P3: the mugshot board | 10 | |
| 29-37 | P4: the teen with the board | 9 | 36-37 lift brighter (luma 135 against 117) |
| 38-45 | P5: the boxing pose | 8 | 38 blur-in (defocused, small), 39-42 settling |
| 46-49 | the whip | 4 | 46-47 the photo smeared vertically, 48 a grey smear, 49 the red blob on it |
| 50-61 | the Joker in his cell | 12 | the red word flies in from left of centre and resolves (sharp by 59-61, before the voice says it at 69) |
| 62 | black | 1 | |
| 63-65 | the top negative rectangle | 3 | dim, bright, dim |
| 66-67 | black | 2 | |
| 68-81 | the Joker, still | 14 | |
| 82-83 | the X-ray | 2 | |
| 84-85 | the silhouette | 2 | |
| 86-95 | P6: the bedroom still | 10 | 86-87 negative, 88-89 X-ray, then a white bar becoming "Heath" |
| 96-105 | P7: black-and-white, standing | 10 | "Ledger" inside a white box (98-102) |
| 106-114 | P8: the night event | 9 | |
| 115-124 | P9: the leather jacket | 10 | the words leave; a white bar on the right |
| 125-133 | P10: the beanie | 9 | "was" |
| 134-143 | P11: the crowd | 10 | "was the" |
| 144-153 | P12: the talk show | 10 | "guy" in serif italic |
| 154-179 | the Hollywood sign | 26 | the bar (156-160), the word (161-164), black (165), the focus window (166-171; 166 and 171 dim), black (172), clean (173-176), punch-in (177-179) |
| 180-196 | the Gotham Gazette | 17 | a bar on the headline (180-181), its photos negative (182-184), "Couldn't" (185) |
| 197-227 | four film stills | 9, 10, 10, 2 | words arrive as bars |
| 228-234 | the map inset over the last still | 7 | |
| 235-244 | the words turn to bars; a black-and-white photo | 10 | |
| 245-273 | three more photos | 9, 10, 10 | "A kid" in red |

**Count:** five photos before the Joker; seven after it, then four film stills; then three more. Each is held 4-10 frames. Every face sits on the frame's vertical centre line (detected centres at x = 0.47-0.52 of the width).

## Our Meet section (S07), photo for photo
- **The name run (Meet Jamie Dimon):** ten pictures. The reel's five come first, frame for frame (4+5, 4+4, 10, 9, 8), then five from its later run (10, 10, 9, 10, 9).
  - Black frames at 4 and 14, the dims at 5 and 13, the lift at 36-37, the blur-in at 38, the negative entry at 46-47 and a click-in on the last photo.
  - All are face-centred: the user's folder photos (`tools/prep8.py`) and three Dimon videos centred by crop.
- **The whip:** 4 frames.
- **The Golden Boy:** the user's cell picture, the reel's Joker beat frame for frame (12, 1, 3, 2), a longer hold, then the X-ray 2 and the silhouette 2.
- **Of Wall Street:** the user's Wall St sign photo as the Hollywood beat, frame for frame after its bar, then their NYSE street photo with the click-in.
- **The guy everyone said was:** the reel's run again: 10, 10, 9, 10, 10, 9 frames, the 7-frame inset, then video.
- **Next in line:** the Gazette, its portraits negative for 3 frames.
- **To run the biggest financial company in the world:**
  - videos at the reel's 9-10 frame cadence, then the 2-frame shot and its 7-frame inset;
  - then black, six grey box flashes, black, and the aerial;
  - the line becomes one white bar, then the strobe (W W B B W W).
