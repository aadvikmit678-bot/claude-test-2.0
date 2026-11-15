"""The cut-out of Lucia and Jason in the user's hero art (gta6-src/v4ref/hero/hero1b.jpg, 1280x720) for tools/hero4.py:
GrabCut seeded with the sky either side as background and their faces, Jason's chest and Lucia's hair as foreground;
the largest part kept, holes filled. Writes gta6-src/v4ref/hero/hero1b_mask.png.   usage: python -I tools/mask4.py
"""
import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(os.path.dirname(HERE)), "gta6-src", "v4ref", "hero")
img = cv2.imread(os.path.join(D, "hero1b.jpg"))
h, w = img.shape[:2]
mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
mask[:, :300] = cv2.GC_BGD; mask[:, 1190:] = cv2.GC_BGD; mask[:20, :] = cv2.GC_BGD
mask[:150, :560] = cv2.GC_BGD                     # sky left of Lucia's head
mask[:60, 880:] = cv2.GC_BGD                      # sky right of Jason's head
mask[60:720, 350:1150] = cv2.GC_PR_FGD
mask[110:330, 660:830] = cv2.GC_FGD               # Jason's face
mask[280:460, 540:660] = cv2.GC_FGD               # Lucia's face
mask[360:720, 650:950] = cv2.GC_FGD               # Jason's chest
mask[200:560, 420:520] = cv2.GC_FGD               # Lucia's hair
bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
cv2.grabCut(img, mask, None, bgd, fgd, 10, cv2.GC_INIT_WITH_MASK)
m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
m = np.where(lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])), 255, 0).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
inv = 255 - m
nn, lab2 = cv2.connectedComponents(inv, connectivity=4)
edge = np.unique(np.concatenate([lab2[0], lab2[-1], lab2[:, 0], lab2[:, -1]]))
m[(inv > 0) & ~np.isin(lab2, edge)] = 255
cv2.imwrite(os.path.join(D, "hero1b_mask.png"), m)
print("hero1b_mask.png", round((m > 0).mean(), 3))
