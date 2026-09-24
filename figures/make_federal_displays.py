#!/usr/bin/env python3
"""Table 4 values, Table S8.1 rows, and Figure 7 (figures/fig5_federal_forest.png) from one source.

Source: error-statements/federal_error_scaling/FEDERAL_CROSS_FAMILY_RESULTS.csv inputs, i.e. the full-precision
estimates in results/primary_results.json (BLS, Census, BEA) and the DerSimonian-Laird combination of the four
NASS crop estimates. Rounding rule: every displayed value is the full-precision value rounded once, half up,
to the displayed precision (two decimals in Table 4 and Figure 7, three in Table S8.1).
"""
import json, os, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Federal analysis outputs (not in this repository): set FEDERAL_ERROR_SCALING to their location.
FES = Path(os.environ.get("FEDERAL_ERROR_SCALING",
                          Path(__file__).resolve().parents[1] / "error-statements/federal_error_scaling"))
R = {r["label"]: r for r in json.load(open(FES / "results/primary_results.json"))}


def dl(est, se):
    est, v = np.asarray(est), np.asarray(se) ** 2
    w = 1 / v; fe = np.sum(w * est) / w.sum(); Q = np.sum(w * (est - fe) ** 2); k = len(est)
    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - np.sum(w ** 2) / w.sum()))
    ws = 1 / (v + tau2); m = np.sum(ws * est) / ws.sum(); s = np.sqrt(1 / ws.sum())
    return dict(e=m, ci_low=m - 1.96 * s, ci_high=m + 1.96 * s)


def rnd(x, nd):
    return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


crops = [R[f"NASS:{c}_state:benchmark"] for c in ["corn", "soybeans", "winter_wheat", "cotton"]]
fam = {
    "BLS CES": (R["BLS:B1_leaf_all_years:benchmark"]["primary"], R["BLS:B1_leaf_all_years:benchmark"]["final_size"]),
    "USDA NASS": (dl([c["primary"]["e"] for c in crops], [c["primary"]["se"] for c in crops]),
                  dl([c["final_size"]["e"] for c in crops], [c["final_size"]["se"] for c in crops])),
    "Census population": (R["CENSUS:county_pooled:benchmark"]["primary"], R["CENSUS:county_pooled:benchmark"]["final_size"]),
    "BEA regional": (R["BEA:county_pi:benchmark"]["primary"], R["BEA:county_pi:benchmark"]["final_size"]),
}
print("Table 4 (two decimals):")
for k, (p, b) in fam.items():
    print(f"  {k:18s} {rnd(p['e'],2)} [{rnd(p['ci_low'],2)}, {rnd(p['ci_high'],2)}] | "
          f"{rnd(b['e'],2)} [{rnd(b['ci_low'],2)}, {rnd(b['ci_high'],2)}]")
rows = [f"{k} & {rnd(p['e'],3)} & [{rnd(p['ci_low'],3)}, {rnd(p['ci_high'],3)}] & {rnd(b['e'],3)} & "
        f"[{rnd(b['ci_low'],3)}, {rnd(b['ci_high'],3)}] \\\\" for k, (p, b) in fam.items()]
Path("tables/S81_rows.tex").write_text("\n".join(rows) + "\n\\bottomrule")
print("\n".join(rows))

plt.rcParams.update({"font.family": "serif", "font.size": 11, "mathtext.fontset": "dejavuserif"})
fig, ax = plt.subplots(figsize=(7.4, 3.6))
names = list(fam)[::-1]
for y, k in enumerate(names):
    p = fam[k][0]
    ax.errorbar(p["e"], y, xerr=[[p["e"] - p["ci_low"]], [p["ci_high"] - p["e"]]], fmt="s", color="#2166ac",
                ms=9, lw=2, capsize=4)
    ax.text(p["e"], y + 0.28, f"{rnd(p['e'],2)} [{rnd(p['ci_low'],2)}, {rnd(p['ci_high'],2)}]", ha="center", fontsize=10.5)
ax.axvline(1.0, color="#b2182b", ls="--", lw=2)
ax.text(1.012, -0.45, r"$e=1$: dollar-proportional (MUS)", rotation=90, color="#b2182b", va="bottom", fontsize=10.5)
ax.set_yticks(range(len(names))); ax.set_yticklabels(names); ax.set_ylim(-0.6, len(names) - 0.3)
ax.set_xlim(0.5, 1.12); ax.set_xlabel(r"Estimated error elasticity $\hat{e}$  (ex ante size)")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("figures/fig5_federal_forest.png", dpi=200)
