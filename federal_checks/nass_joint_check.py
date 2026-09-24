#!/usr/bin/env python3
"""NASS pooled exponent: interval conventions and a dependence-aware joint resampling check.

The frozen pipeline (synthesis_and_figures.py) combines the four crop estimates by DerSimonian-Laird
random effects with a normal (1.96) interval, treating the crop-level jackknife variances as independent.
Crops share states and years, so this script also (i) computes the Hartung-Knapp interval, and
(ii) re-estimates all four crops jointly with one state (or one year) deleted from every crop at once,
recombining each replicate with the same DL rule, so the jackknife variance of the pooled estimate carries
the cross-crop covariance induced by shared states (or years).
"""
import json, os, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

# Federal analysis outputs (not in this repository): set FEDERAL_ERROR_SCALING to their location.
FES = Path(os.environ.get("FEDERAL_ERROR_SCALING",
                          Path(__file__).resolve().parents[2] / "error-statements/federal_error_scaling"))
sys.path.insert(0, str(FES / "scripts"))
from scaling_estimators import _fit

crops = ["corn", "soybeans", "winter_wheat", "cotton"]
R = {r["label"]: r for r in json.load(open(FES / "results/primary_results.json"))}
n = pd.read_csv(FES / "processed/nass_pairs.csv")
n = n[(n.horizon == "benchmark") & (n.a > 0) & (n.a_bench > 0) & n.d.notna()]


def dl(est, v):
    est, v = np.asarray(est), np.asarray(v)
    w = 1 / v; fe = np.sum(w * est) / w.sum(); Q = np.sum(w * (est - fe) ** 2); k = len(est)
    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - np.sum(w ** 2) / w.sum()))
    ws = 1 / (v + tau2); m = np.sum(ws * est) / ws.sum()
    return m, ws, tau2


def report(size_col, key):
    est = np.array([R[f"NASS:{c}_state:benchmark"][key]["e"] for c in crops])
    se = np.array([R[f"NASS:{c}_state:benchmark"][key]["se"] for c in crops])
    m, ws, tau2 = dl(est, se ** 2)
    s_dl = np.sqrt(1 / ws.sum())
    k = len(est)
    q = np.sum(ws * (est - m) ** 2) / (k - 1)
    s_hk = np.sqrt(q / ws.sum()); t = stats.t.ppf(0.975, k - 1)
    out = dict(size=size_col, e=m, tau2=tau2, weights=list(ws / ws.sum()),
               dl_normal=(m - 1.96 * s_dl, m + 1.96 * s_dl), hk_t3=(m - t * s_hk, m + t * s_hk))
    # joint resampling: delete one state (and, separately, one year) from every crop at once
    for unit in ("state", "year"):
        labels = np.unique(n[unit].astype(str))
        reps = []
        for g in labels:
            sub = n[n[unit].astype(str) != g]
            e_c = [_fit(sub[sub.crop == c].d.values ** 2, np.log(sub[sub.crop == c][size_col].values), "gpml")["e"]
                   for c in crops]
            reps.append(np.sum(ws * np.array(e_c)) / ws.sum())   # same DL weights as the full-sample pooling
        reps = np.array(reps); G = len(reps)
        se_j = np.sqrt((G - 1) / G * np.sum((reps - reps.mean()) ** 2)); tj = stats.t.ppf(0.975, G - 1)
        out[f"joint_{unit}_jk"] = dict(G=G, se=se_j, ci=(m - tj * se_j, m + tj * se_j))
    return out


res = [report("a", "primary"), report("a_bench", "final_size")]
for r in res:
    print(json.dumps(r, default=float, indent=1))
json.dump(res, open(Path(__file__).with_suffix(".json"), "w"), default=float, indent=1)
