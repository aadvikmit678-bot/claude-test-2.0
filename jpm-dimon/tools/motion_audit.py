"""Is a clip real moving footage, or a still photograph with a zoom or pan on it (a documentary's Ken Burns move)?

For frame pairs 0.35 s apart: track corners, fit one similarity transform (the camera: zoom, pan, roll), warp the first
frame onto the second and measure what is left, in 16x16 blocks at 480x270. A still leaves almost nothing (blocks
under about 4 grey levels); a person talking or a crowd leaves a lot in the blocks where things move.
Prints per clip: resid (the 97th percentile block residual, the average of the pairs), cam (how much the fitted
camera moves, in px at 480 wide) and the verdict.

usage: CV4_DIR=... python3 -I tools/motion_audit.py media_v12.json [id-substring ...]
       CV4_DIR=... python3 -I tools/motion_audit.py --file path.mp4 [t0 [dur]]"""
import json, os, sys
sys.path.insert(0, os.environ.get("CV4_DIR", "/home/user/claude-test-2.0/dimon-work/cv4"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402

PRJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def frames(path, times):
    cap = cv2.VideoCapture(path)
    out = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        if not ok:
            break
        out.append(cv2.cvtColor(cv2.resize(f, (480, 270), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY))
    cap.release()
    return out


def pair(a, b):
    pts = cv2.goodFeaturesToTrack(a, 400, 0.01, 6)
    M = np.array([[1, 0, 0], [0, 1, 0]], np.float32)
    if pts is not None and len(pts) >= 12:
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None, winSize=(21, 21), maxLevel=3)
        g = st.ravel() == 1
        if g.sum() >= 12:
            m, _ = cv2.estimateAffinePartial2D(pts[g], nxt[g], method=cv2.RANSAC, ransacReprojThreshold=1.0)
            if m is not None:
                M = m.astype(np.float32)
    w = cv2.warpAffine(a, M, (480, 270), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    d = cv2.absdiff(cv2.GaussianBlur(w, (5, 5), 0), cv2.GaussianBlur(b, (5, 5), 0)).astype(np.float32)[15:255, 20:460]
    blocks = d.reshape(15, 16, -1, 16).mean(axis=(1, 3)) if d.shape == (240, 440) and False else \
        cv2.resize(d, (d.shape[1] // 16, d.shape[0] // 16), interpolation=cv2.INTER_AREA)
    cam = float(np.hypot(M[0, 2], M[1, 2]) + abs(np.hypot(M[0, 0], M[1, 0]) - 1) * 240)
    return float(np.percentile(blocks, 97)), cam


def audit(path, t0=0.05, dur=None, step=0.35):
    cap = cv2.VideoCapture(path)
    n, fps = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS) or 30
    cap.release()
    end = t0 + dur if dur else n / fps - 0.05
    ts = []
    t = t0
    while t + step <= end + 1e-6 and len(ts) < 5:
        ts.append(t)
        t += step
    if not ts:
        ts, step = [t0], max(0.1, (end - t0) * 0.9)
    res = []
    for t in ts:
        f = frames(path, [t, t + step])
        if len(f) == 2:
            res.append(pair(f[0], f[1]))
    if not res:
        return None
    r = float(np.mean([x[0] for x in res]))
    c = float(np.mean([x[1] for x in res]))
    return r, c, ("VIDEO" if r >= 7 else "still?" if r >= 4 else "STILL")


if __name__ == "__main__":
    if sys.argv[1] == "--file":
        t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
        dur = float(sys.argv[4]) if len(sys.argv) > 4 else None
        print(audit(sys.argv[2], t0, dur))
        sys.exit(0)
    m = json.load(open(f"{PRJ}/tools/{sys.argv[1]}"))
    want = sys.argv[2:]
    rows = []
    for cid, sp in m["clips"].items():
        if want and not any(w in cid for w in want):
            continue
        p = f"{PRJ}/assets/clips2/{cid}.mp4"
        if not os.path.exists(p):
            continue
        a = audit(p, 0.05, max(0.2, sp["dur"] - 0.3))
        if a:
            rows.append((a[0], cid, sp["key"], sp["t"], a[1], a[2]))
    for r, cid, key, t, c, v in sorted(rows):
        print(f"{v:6s} resid {r:5.1f}  cam {c:5.1f}  {key:8s} {t:8.2f}  {cid}")
