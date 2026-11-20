#!/usr/bin/env python3
"""The sound: the panel line, the voiceover, the Rogan clip, a dark synthesized bed and the bundled SFX
(Pixabay licence, see assets/sfx/CREDITS.md), mixed at 48 kHz.

Writes assets/audio/mix.wav (with music and SFX) and assets/audio/mix_dry.wav (speech only), so the render can be
re-muxed without SFX without rendering again.
"""
import os
import shutil
import subprocess

import numpy as np

import timing as TM

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUD = f"{ROOT}/assets/audio"
SFXSRC = "/root/.claude/skills/media-use/audio/assets/sfx"
SFX = f"{ROOT}/assets/sfx"
SR = 48000
N = int(round(TM.TOTAL * SR))
USE_SFX = False   # the user: "remove all the sfx" -- no hits, clicks, whooshes, glitches, thumps or risers
os.makedirs(SFX, exist_ok=True)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def rms_db(x):
    v = x[np.abs(x).max(axis=1) > 1e-3]
    return 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-9)


def place(bus, x, t, gain=1.0, fade_in=0.004, fade_out=0.02):
    i = int(round(t * SR))
    if i >= len(bus):
        return
    x = x[: len(bus) - i].copy()
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    if fi:
        x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo and len(x) > fo:
        x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    bus[i:i + len(x)] += x * gain


def sfx(name):
    src = f"{SFXSRC}/{name}.mp3"
    shutil.copy(src, f"{SFX}/{name}.mp3")
    return load(src)


def kick(f0=120, f1=42, dur=0.45, amp=0.9):
    t = np.arange(int(dur * SR)) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / 0.16) * amp
    return np.stack([y, y], 1).astype(np.float32)


def noise_riser(dur, seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    w = rng.normal(0, 1, n).astype(np.float32)
    # a rising band: brighter and louder towards the end
    out = np.zeros(n, np.float32)
    a = 0.0
    for i0 in range(0, n, 2048):
        seg = w[i0:i0 + 2048]
        k = (i0 / n)
        alpha = 0.02 + 0.5 * k ** 2
        y = np.empty_like(seg)
        for j, v in enumerate(seg):
            a += alpha * (v - a)
            y[j] = a
        out[i0:i0 + 2048] = y
    env = (np.linspace(0, 1, n) ** 2.2)
    out = out / (np.abs(out).max() + 1e-9) * env
    return np.stack([out, out], 1) * 0.5


def drone(dur, seed=3):
    t = np.arange(int(dur * SR)) / SR
    y = np.zeros_like(t)
    for f, a in ((55.0, 0.55), (55.4, 0.35), (82.41, 0.22), (110.0, 0.18), (164.8, 0.06)):
        y += a * np.sin(2 * np.pi * f * t + f)
    y *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t) ** 2
    rng = np.random.default_rng(seed)
    hiss = np.convolve(rng.normal(0, 1, len(t)), np.ones(40) / 40, mode="same") * 0.05
    y = (y + hiss) / 1.6
    return np.stack([y, y * 0.97], 1).astype(np.float32)


def limit(x, ceil=0.93, look=0.004, release=0.06):
    """A look-ahead peak limiter: gain = ceil / peak over a short window, held and released smoothly."""
    a = np.abs(x).max(axis=1)
    w = max(1, int(look * SR))
    pad = np.pad(a, (w, w), mode="edge")
    from numpy.lib.stride_tricks import sliding_window_view
    pk = sliding_window_view(pad, 2 * w + 1).max(axis=1)[: len(a)]
    g = np.minimum(1.0, ceil / np.maximum(pk, 1e-9))
    r = int(release * SR)
    k = np.exp(-np.arange(r) / (r / 4))
    k /= k.sum()
    gs = np.minimum(g, np.convolve(g, k, mode="same"))
    return x * gs[:, None]


def frames_to_times(start, durs):
    out, f = [], round(start * 60)
    for d in durs:
        out.append(f / 60)
        f += d
    return out


def main():
    speech = np.zeros((N, 2), np.float32)
    line, vo, rogan = load(f"{AUD}/line.wav"), load(f"{AUD}/vo.wav"), load(f"{AUD}/rogan.wav")
    target = -19.0
    place(speech, line * 10 ** ((target - rms_db(line)) / 20), 0.0, fade_in=0.01, fade_out=0.03)
    place(speech, vo * 10 ** ((target - rms_db(vo)) / 20), TM.V0, fade_in=0.005, fade_out=0.03)
    place(speech, rogan * 10 ** ((target + 1 - rms_db(rogan)) / 20), TM.B["rogan"][0], fade_in=0.004, fade_out=0.08)

    music = np.zeros((N, 2), np.float32)
    T, B = TM.T, TM.B
    end = B["rogan"][0]
    d = drone(end)
    env = np.ones(len(d), np.float32)
    env[: int(1.5 * SR)] = np.linspace(0.0, 1.0, int(1.5 * SR))
    place(music, d * env[:, None], 0.0, fade_out=0.06)
    fx = np.zeros((N, 2), np.float32)
    if USE_SFX:
        add_sfx(music, fx, T, B)

    # duck the music and effects under speech a little
    lvl = np.abs(speech).max(axis=1)
    win = int(0.08 * SR)
    sm = np.convolve(lvl, np.ones(win) / win, mode="same")
    duck = 1.0 - 0.45 * np.clip(sm / 0.05, 0, 1)
    mix = speech + music * 0.11 * duck[:, None] + fx * (0.75 + 0.25 * duck[:, None])
    dry = speech.copy()
    for name, x in (("mix", limit(mix)), ("mix_dry", limit(dry))):
        peak = np.abs(x).max()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-c:a", "pcm_s16le", f"{AUD}/{name}.wav"], input=x.astype(np.float32).tobytes(), check=True)
        print(f"  {name}.wav  {len(x) / SR:.3f}s  peak {20 * np.log10(peak + 1e-9):.1f} dBFS")


def add_sfx(music, fx, T, B):
    """The effects, off by default: the hook's thumps, the risers, the bundled hits and the flipbook clicks."""
    # the hook's pulse: a sub thump every beat (83.3 BPM, Nvidia's tempo) from "These" to "That's"
    beat = 0.72
    t = B["these"][0]
    while t < B["dimon"][0] - 0.05:
        place(music, kick(), t, 0.55)
        t += beat
    # the intros: half-time thumps
    t = T["dimon"]
    while t < B["fink"][1] - 0.2:
        place(music, kick(100, 38, 0.6), t, 0.42)
        t += beat * 2
    place(music, noise_riser(1.25, 1), T["dimon"] - 1.25, 0.35)
    place(music, noise_riser(1.05, 2), T["guy2"] - 1.05, 0.32)
    place(music, noise_riser(1.4, 3), T["blackrock"] - 1.4, 0.38)
    S = {n: sfx(n) for n in ("impact-bass-1", "impact-bass-2", "whoosh", "whoosh-short", "glitch-1", "glitch-2",
                              "glitch-3", "click-soft", "click", "pop", "sparkle", "whoosh-cinematic")}
    hits = [  # (time, name, gain)
        (B["these"][0], "impact-bass-2", 0.55), (T["these"] + 0.017, "glitch-1", 0.22),
        (B["tiles"][0], "impact-bass-1", 0.5), (B["tiles"][0] + 40 / 60, "glitch-2", 0.18),
        (B["earth"][0], "impact-bass-2", 0.7), (T["earth"], "click", 0.25),
        (B["money"][0], "whoosh-short", 0.35),
        (B["cartel"][0], "impact-bass-1", 0.45),
        (B["weap"][0], "glitch-3", 0.4), (T["ized"], "impact-bass-2", 0.75), (T["capital"], "whoosh", 0.35),
        (B["logos"][0], "whoosh-short", 0.3),
        (T["touch"], "sparkle", 0.35), (B["glow"][0], "impact-bass-1", 0.35),
        (B["dimon"][0], "whoosh", 0.35), (T["dimon"], "impact-bass-2", 0.75),
        (T["chase"], "glitch-1", 0.3), (B["solomon"][0], "whoosh-short", 0.4),
        (T["a3"], "impact-bass-1", 0.45), (T["and"], "glitch-1", 0.28),
        (B["search"][0], "whoosh-short", 0.3), (B["thisguy"][0], "impact-bass-2", 0.85), (B["thisguy"][0], "whoosh", 0.3),
        (T["guy2"], "impact-bass-1", 0.4),
        (B["fink"][0], "impact-bass-1", 0.55), (T["most"], "pop", 0.4), (T["world_end"] + 0.05, "whoosh-short", 0.3),
        (T["blackrock"], "impact-bass-2", 0.95), (T["blackrock"], "glitch-2", 0.2),
    ]
    for t, n, g in hits:
        place(fx, S[n], t, g)
    # one soft click per flipbook page / face (the Nvidia flipbook's 12 Hz clicks)
    clicks = []
    clicks += frames_to_times(B["money"][0], [5] * 17)
    clicks += frames_to_times(B["cartel"][0], [4, 4, 4, 3, 4, 3, 4, 3, 3, 3, 4])
    clicks += frames_to_times(B["logos"][0], [6] * 10 + [5] * 6 + [8])
    for t in clicks:
        place(fx, S["click-soft"], t, 0.22)
    for f0 in (3, 11, 19, 27, 35, 43):  # the orbit's glows, one light each
        place(fx, S["sparkle"], B["search"][0] + f0 / 60, 0.16)
    for k, f0 in enumerate((10, 13, 16, 19, 22, 25, 28, 31, 34)):
        place(fx, S["click"], B["tiles"][0] + f0 / 60, 0.12)


if __name__ == "__main__":
    main()
