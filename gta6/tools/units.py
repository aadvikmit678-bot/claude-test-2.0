"""Split the studied clips into analysis units for the reading agents: each unit is one clip (or one stretch of a long
clip) with the exact sheets an agent should look at (no more than MAX each) and the clip's facts file.

usage: python3 -I gta6/tools/units.py [key ...] > gta6-work/units.json"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = f"{ROOT}/gta6-work"
MAX = 22
DUP = {"launch": "launchps5"}          # the 1080p launch trailer is the same film as the 4K one (mean frame diff 0.3/255)


def num(p):
    return int(re.search(r"_(\d+)\.jpg$", p).group(1))


units = []
keys = sys.argv[1:] or sorted(os.listdir(WORK))
for key in keys:
    p = f"{WORK}/{key}/study.json"
    if not os.path.exists(p) or key in DUP:
        continue
    d = json.load(open(p))
    sh = d["sheets"]
    shots = sorted([s for s in sh if "/shots_" in s], key=num)
    longs = sorted([s for s in sh if "/long_" in s], key=num)
    flow = sorted([s for s in sh if "/flow_" in s], key=num)
    cuts = sorted([s for s in sh if "/cuts_" in s], key=num)
    fps, dur = d["meta"]["fps"], d["meta"]["duration"]
    base = dict(key=key, title=d["title"], kind=d["kind"], facts=f"{WORK}/{key}/facts.md",
                proxy=f"{WORK}/{key}/proxy.mp4", duration=dur, fps=fps, size=f"{d['meta']['w']}x{d['meta']['h']}",
                flow_fps=None if not flow else (4 if key == "billion" else 12))
    if d["kind"] == "raw footage":
        # shot sheets hold 48 shots each, long sheets 10 long shots each (in order): group by shot range
        long_ids = [s["i"] for s in d["shots"] if s["dur"] >= 2.5]
        per_unit = 4                                   # shot sheets per unit (192 shots)
        for k in range(0, len(shots), per_unit):
            part = shots[k:k + per_unit]
            lo, hi = 48 * num(part[0]), 48 * num(part[-1]) + 47
            ls = [s for s in longs if any(lo <= long_ids[j] <= hi for j in range(10 * num(s), min(len(long_ids), 10 * num(s) + 10)))]
            t0 = d["shots"][min(lo, len(d["shots"]) - 1)]["t0"]
            t1 = d["shots"][min(hi, len(d["shots"]) - 1)]["t1"]
            units.append(dict(base, unit=f"{key}#{k // per_unit}" if len(shots) > per_unit else key,
                              part=f"shots {lo}-{min(hi, len(d['shots']) - 1)} ({t0:.1f}-{t1:.1f} s)", sheets=part + ls))
        continue
    total = len(shots) + len(flow) + len(cuts)
    if total <= MAX:
        units.append(dict(base, unit=key, part="whole clip", sheets=shots + flow + cuts))
        continue
    # split the timeline in n parts: flow sheets in order, cut sheets by the times of their cuts
    n = -(-total // MAX)
    span = 36 / (base["flow_fps"] or 12)                # seconds a flow sheet covers
    v0 = d["meta"]["v_start"]
    marks = sorted(set(d["cuts"]) | {e["frame"] for e in d["events"] if e["kind"] == "flash"})
    for j in range(n):
        a, b = dur * j / n, dur * (j + 1) / n
        last = j == n - 1
        fl = [s for s in flow if a <= num(s) * span < b or (last and num(s) * span >= b)]
        cs = []
        for s in cuts:
            m = marks[num(s) * 6:num(s) * 6 + 6]
            if m and (a <= v0 + m[0] / fps < b or (last and v0 + m[0] / fps >= b)):
                cs.append(s)
        units.append(dict(base, unit=f"{key}#{j}", part=f"{a:.1f}-{b:.1f} s of {dur:.1f} s",
                          sheets=(shots if j == 0 else []) + fl + cs))
json.dump(units, sys.stdout, indent=1)
print(f"{len(units)} units; sheets per unit: {[len(u['sheets']) for u in units]}", file=sys.stderr)
