"""The film's clock. Every boundary is snapped to the 60 fps frame grid (F).

Sources of the times (measured, see SPEC.md):
- the panel line: the FII7 panel video's own audio 32.32-38.95 s, placed at film 0;
- the voiceover (starting_part.mp3) word starts, re-transcribed phrase by phrase and checked against its loudness dips,
  placed at film V0 = 6.70;
- the Rogan / Musk clip from its 12.55 s (Rogan's "Do you think BlackRock's a bad company?") to 19.45 s.
"""
FPS = 60


def F(t):
    """Snap a time to the 60 fps frame grid."""
    return round(round(t * FPS) / FPS, 4)


V0 = 6.70          # voiceover start on the film
VO_END = 22.62     # voiceover file time where "BlackRock." has finished (then cut to Rogan)
LINE_T0, LINE_T1 = 32.32, 38.95   # panel audio for the opening line
ROGAN_T0, ROGAN_T1 = 12.55, 15.28  # the Rogan clip: Elon's question only, ending before Rogan's answer (15.31)


def V(t):
    """Film time of a voiceover file time."""
    return F(V0 + t)


# voiceover word starts (file seconds)
W = {
    "these": 0.05, "powerful": 1.01, "people": 1.48, "on": 2.01, "earth": 2.10,
    "a": 3.12, "sixty": 3.16, "trillion": 3.71, "dollar": 4.255, "cartel": 4.545, "of1": 5.095,
    "weapon": 5.205, "ized": 5.46, "capital": 5.83, "that": 6.29, "owns": 6.485, "a2": 6.72, "piece": 6.82,
    "of2": 7.08, "everything": 7.21, "you": 7.92, "touch": 8.04, "touch_end": 8.43,
    "thats": 9.05, "jamie": 9.37, "dimon": 9.68, "the1": 10.25, "guy1": 10.40, "running": 10.60, "jp": 11.01,
    "morgan": 11.21, "chase": 11.62, "chase_end": 11.97,
    "david": 12.45, "solomon": 12.68, "solomon_end": 13.20, "a3": 13.38, "parttime": 13.43, "dj": 14.12,
    "and": 14.28, "the2": 14.52, "ceo": 14.76, "goldman": 15.15, "sachs": 15.63, "sachs_end": 16.17,
    "amongst": 16.78, "them": 17.24, "is": 17.53, "this": 17.67, "guy2": 17.96, "guy2_end": 18.24,
    "the3": 18.59, "man": 18.69, "who": 18.86, "runs": 19.03, "the4": 19.25, "most": 19.42, "evil": 19.82,
    "company": 20.10, "in": 20.56, "the5": 20.70, "world": 20.92, "world_end": 21.34,
    "blackrock": 21.87, "blackrock_end": 22.59,
}
T = {k: V(v) for k, v in W.items()}

# panel line word starts (film seconds = panel time - 32.32)
LINE_WORDS = [
    ("I", 32.36), ("don't", 32.40), ("think", 32.68), ("there's", 32.88), ("ever", 33.02), ("been", 33.29),
    ("a", 33.42), ("panel", 33.47), ("with", 33.99), ("as", 34.12), ("big", 34.22), ("an", 34.30),
    ("assemblage", 34.38), ("of", 35.04), ("financial", 35.17), ("talent", 35.81), ("and", 36.18),
    ("skill", 36.38), ("as", 36.58), ("you've", 37.03), ("been", 37.25), ("able", 37.52), ("to", 37.82),
    ("put", 37.92), ("together", 38.15), ("here.", 38.76),
]
LINE = [(w, F(t - LINE_T0)) for w, t in LINE_WORDS]

# beats (film seconds, frame-snapped)
B = {
    "quote": (0.0, F(V0)),
    "these": (F(V0), T["powerful"]),
    "tiles": (T["powerful"], T["on"]),
    "earth": (T["on"], T["a"]),
    "money": (T["a"], T["cartel"]),
    "cartel": (T["cartel"], T["weapon"]),
    "weap": (T["weapon"], T["that"]),
    "logos": (T["that"], F(14.25)),
    "touch": (F(14.25), T["touch_end"]),      # the hands come together from mid "everything", touch on "touch"
    "glow": (T["touch_end"], T["thats"]),      # split second: the panel from above, people lighting up (X-creative)
    "dimon": (T["thats"], T["jp"]),            # the tfg page: "That's Jamie Dimon, the guy running"
    "jpm": (T["jp"], T["david"]),              # "JP Morgan Chase": the bank, in plain cuts
    "solomon": (T["david"], T["a3"]),          # his speaking clip, then the Hemant flash on him
    "dj": (T["a3"], T["and"]),                 # "a part-time DJ": the D-Sol video
    "ceo": (T["and"], T["sachs_end"]),         # the panel's own title lands on "CEO"
    "search": (T["sachs_end"], T["this"]),     # the camera circling the table; from "Amongst" people light up
    "thisguy": (T["this"], T["the3"]),         # Fink's close-up at the panel
    "walk": (T["the3"], T["runs"]),            # "the man who": Fink walking
    "box": (T["runs"], T["company"]),          # "runs the most evil": the interview, the red square on "most"
    "company": (T["company"], T["blackrock"]), # "company in the world": BlackRock's lobby and building
    "brand": (T["blackrock"], F(V0 + VO_END + 0.045)),  # "BlackRock.": the letters on its facade
}
B["fink"] = (B["thisguy"][0], B["brand"][1])   # the Fink run as a whole (the Rogan clip follows it)
B["rogan"] = (B["fink"][1], F(B["fink"][1] + ROGAN_T1 - ROGAN_T0))
TOTAL = B["rogan"][1]

if __name__ == "__main__":
    for k, (a, b) in B.items():
        print(f"{k:8s} {a:7.3f} {b:7.3f}  {b - a:6.3f}s  frames {round(a * FPS)}-{round(b * FPS)}")
    print("TOTAL", TOTAL, round(TOTAL * FPS), "frames")
