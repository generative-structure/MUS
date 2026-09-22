#!/usr/bin/env python3
"""Independent check of MUS_Risk_Aligned_Allocation_Calculator.xlsx after LibreOffice/Excel recalculation."""
import math, sys
from openpyxl import load_workbook
wb = load_workbook("MUS_Risk_Aligned_Allocation_Calculator.xlsx", data_only=True)
ws = wb["Calculator"]; sv = wb["Sensitivity"]
n_total = ws["B5"].value; ref = ws["B6"].value; mode = ws["B4"].value
bands = []
for r in range(10, 14):
    D, p, rms, cost = ws[f"D{r}"].value, ws[f"E{r}"].value, ws[f"F{r}"].value, ws[f"G{r}"].value
    s = rms**2 if (mode == "Advanced" and rms) else 1.0
    c = cost if (mode == "Advanced" and cost) else 1.0
    bands.append((D, p, s, c))
pr, sr, cr = bands[ref-1][1], bands[ref-1][2], bands[ref-1][3]
mult = [math.sqrt(p*s/c)/math.sqrt(pr*sr/cr) if D and p else 0 for D, p, s, c in bands]
w = [D*m for (D, p, s, c), m in zip(bands, mult)]
share = [x/sum(w) for x in w]; mus = [D/sum(b[0] for b in bands) for D, *_ in bands]
just = [pr*sr/cr*c/s for D, p, s, c in bands]
ok = 0
def check(a, b, msg, tol=1e-9):
    global ok
    assert abs(a-b) <= tol, f"{msg}: sheet {a} vs python {b}"; ok += 1
for i, r in enumerate(range(10, 14)):
    check(ws[f"J{r}"].value, mult[i], f"multiplier band {i+1}")
    check(ws[f"M{r}"].value, share[i], f"suggested share band {i+1}")
    check(ws[f"L{r}"].value, mus[i], f"MUS share band {i+1}")
    check(ws[f"O{r}"].value, round(share[i]*n_total), f"suggested count band {i+1}")
    check(ws[f"N{r}"].value, round(mus[i]*n_total), f"MUS count band {i+1}")
    check(ws[f"Q{r}"].value, just[i], f"justifying occurrence band {i+1}")
# MUS special case: equal p*s/c => shares equal D
eq = [(D, 0.02, 1.0, 1.0) for D, *_ in bands]
we = [D*math.sqrt(0.02) for D, *_ in eq]; assert all(abs(x/sum(we) - D/sum(b[0] for b in eq)) < 1e-12 for x, (D, *_) in zip(we, eq)); ok += 1
# manuscript Table 7 values
exp_share = [0.144, 0.374, 0.364, 0.118]; exp_cnt = [58, 150, 146, 47]; exp_just = [0.0075, 0.015, 0.0375, 0.1125]
for i in range(4):
    check(round(share[i], 3), exp_share[i], f"Table 7 share band {i+1}"); check(round(share[i]*n_total), exp_cnt[i], f"Table 7 count band {i+1}"); check(just[i], exp_just[i], f"Table 7 justifying p band {i+1}", 1e-9)
# sensitivity: multiplier 1 row reproduces calculator shares for varied band
b = sv["B4"].value
for r in range(10, 18):
    m = sv[f"A{r}"].value
    wv = w[b-1]*math.sqrt(m); den = sum(w) - w[b-1] + wv
    for j, c in enumerate("CDEF"):
        expect = (wv if j == b-1 else w[j])/den
        check(sv[f"{c}{r}"].value, expect, f"sensitivity row {r} band {j+1}")
print(f"ALL {ok} CALCULATOR CHECKS PASSED; shares={[round(x,4) for x in share]} counts={[round(x*n_total) for x in share]}")
