#!/usr/bin/env python3
"""The music bed: the Bloomberg open's own music, continued under the whole film.

1. Separate voice and music in the first 4 minutes of name_of_the_game.mp4 (Demucs htdemucs, two stems).
2. The open keeps the reporter's voice only (vocals stem, spliced like the picture: src 1.12-2.68 + 5.05-12.30).
3. The bed is the opening cue (0-53.5 s, 120 BPM) played from 2.17 s, with one jump on a downbeat
   (source 45.085 -> 3.215, 80 ms equal-power crossfade), so the cue's own ending lands on the film's last frame:
   film 0-42.915 = cue 2.17-45.085, film 42.915-93.2 = cue 3.215-53.5. The jump was chosen by comparing the
   spectra of the bars on both sides of every downbeat pair.
4. Loudness: voice parts -16 LUFS; the bed -30 LUFS (about 14 dB under the voice, as in the Bloomberg mix).

Needs: pip install torch torchaudio (CPU) demucs soundfile.   Run: python3 -I tools/make_music.py
"""
import json, os, re, subprocess

ROOT = "/home/user/claude-test-2.0"
PRJ = f"{ROOT}/jpm-dimon"
WORK = f"{ROOT}/dimon-work/music"
AUD = f"{PRJ}/assets/audio"
SRC = f"{ROOT}/dimon-src/_direct/name_of_the_game.mp4"
os.makedirs(WORK, exist_ok=True)
os.makedirs(AUD, exist_ok=True)

SEP = r'''
import sys, soundfile as sf, torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import AudioFile
inp, out = sys.argv[1], sys.argv[2]
torch.set_num_threads(4)
m = get_model("htdemucs"); m.eval()
wav = AudioFile(inp).read(streams=0, samplerate=m.samplerate, channels=m.audio_channels)
ref = wav.mean(0); mu, sd = ref.mean(), ref.std(); wav = (wav - mu) / sd
with torch.no_grad():
    s = apply_model(m, wav[None], device="cpu", shifts=1, split=True, overlap=0.25, progress=False)[0]
s = s * sd + mu
v = s[m.sources.index("vocals")]; r = s.sum(0) - v
sf.write(out + "/vocals.wav", v.T.numpy(), m.samplerate, subtype="PCM_16")
sf.write(out + "/no_vocals.wav", r.T.numpy(), m.samplerate, subtype="PCM_16")
'''

CUE_IN, JUMP_FROM, JUMP_TO, CUE_END, XF = 2.17, 45.085, 3.215, 53.5, 0.08
FILM = 93.2


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-1500:]}")
    return r


def loudnorm(inp, out, target, extra_af=""):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", inp, "-af",
                        f"{extra_af}loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    af = (f"{extra_af}loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", inp, "-af", af, "-ar", "48000", "-ac", "2",
         "-c:a", "pcm_s16le", out])


if __name__ == "__main__":
    stems = f"{WORK}/sep240"
    if not os.path.exists(f"{stems}/no_vocals.wav"):
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", "0", "-t", "240", "-i", SRC, "-vn", "-ac", "2",
             "-ar", "44100", f"{WORK}/bbg_0_240.wav"])
        os.makedirs(stems, exist_ok=True)
        open(f"{WORK}/_sep.py", "w").write(SEP)
        run(["python3", "-I", f"{WORK}/_sep.py", f"{WORK}/bbg_0_240.wav", stems])
    # the reporter's voice alone, spliced like the picture
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{stems}/vocals.wav", "-filter_complex",
         "[0:a]atrim=1.12:2.68,asetpts=PTS-STARTPTS,afade=t=out:st=1.54:d=0.02[a];"
         "[0:a]atrim=5.05:12.30,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=7.0:d=0.25[b];[a][b]concat=n=2:v=0:a=1",
         f"{WORK}/news_voice_raw.wav"])
    loudnorm(f"{WORK}/news_voice_raw.wav", f"{AUD}/news_voice.wav", -16)
    # the bed: one bar-aligned jump, the cue's own ending on the last frame
    a_end, b_start = JUMP_FROM + XF / 2, JUMP_TO - XF / 2
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{stems}/no_vocals.wav", "-filter_complex",
         f"[0:a]atrim={CUE_IN}:{a_end},asetpts=PTS-STARTPTS[a];"
         f"[0:a]atrim={b_start}:{CUE_END},asetpts=PTS-STARTPTS[b];"
         f"[a][b]acrossfade=d={XF}:c1=qsin:c2=qsin,atrim=0:{FILM},afade=t=out:st={FILM - 0.6}:d=0.6",
         f"{WORK}/bed_raw.wav"])
    loudnorm(f"{WORK}/bed_raw.wav", f"{AUD}/music_bed.wav", -30)
    d = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{AUD}/music_bed.wav"]).stdout
    print("bed", d.strip(), "s;  voice:", f"{AUD}/news_voice.wav")
