"""The kid in front of the TV (the user's green-screen file) with Vice City gameplay playing on the TV.

The green screen sits at x 288-409, y 24-121 of the 736x414 source; the kid is scaled to 1920x1080, keyed, and laid
over the Vice City PC gameplay (vcpanzer, the helicopter over the city) placed in the TV's screen.
Writes gta6-edit/assets/clips/tv10.mp4.   usage: python -I tools/tv4.py
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl
REPO = os.path.dirname(os.path.dirname(HERE))
KID = os.path.join(REPO, "gta6-src", "v4ref", "1jex_mEwF0SqAZt-BaenXGVFXbbHgbbJG.mp4")
GAME = os.path.normpath(os.path.join(edl.ROOT, edl.SRC["panzer"]))
k = 1920 / 736
x, y, w, h = round(284 * k), round(20 * k), round(130 * k), round(106 * k)        # the screen plus a margin
fc = (f"[1:v]scale=-2:{h}:flags=lanczos,crop={w}:{h},eq=brightness=-0.03:saturation=0.92,setpts=PTS-STARTPTS[g];"
      f"color=c=black:s=1920x1080:r=30:d=4.5[bg];[bg][g]overlay={x}:{y}:shortest=0[b];"
      f"[0:v]scale=1920:1080:flags=lanczos,chromakey=color=0x03F903:similarity=0.2:blend=0.08[k];"
      f"[b][k]overlay=0:0,fps=30,format=yuv420p[v]")
out = os.path.join(edl.PROJ, "assets", "clips", "tv10.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-t", "4.5", "-i", KID, "-ss", "20.0", "-t", "4.5", "-i", GAME,
                "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
                "-g", "15", "-fps_mode", "passthrough", "-movflags", "+faststart", out], check=True)
print("tv10", out)
