#!/usr/bin/env python3
"""Figure 2 (figures/fig6_allocation.png) and the Section II / S9 ledger numbers, from one computation.

Frame: 60,000 items, log amount ~ N(0, 1.5), numpy default_rng(7). Expected sample 500 with certainty caps
(capped items absorb their excess; the multiplier is re-solved on the remainder). The top-to-bottom ratio
is the ratio of the selection weights a^e of the median items of the top and bottom amount deciles.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def capped(w, n):
    pi = np.zeros_like(w); free = np.ones(len(w), bool); nn = n
    while True:
        p = nn * w[free] / w[free].sum()
        if (p <= 1).all():
            pi[free] = p; return pi
        idx = np.where(free)[0][p > 1]; pi[idx] = 1; free[idx] = False; nn = n - pi[~free].sum()


a = np.sort(np.exp(np.random.default_rng(7).normal(0, 1.5, 60000)))
dec = np.array_split(np.arange(len(a)), 10)
med_ratio = np.median(a[dec[9]]) / np.median(a[dec[0]])
E = (1.0, 0.7, 0.5); shares, ratios = {}, {}
for e in E:
    pi = capped(a ** e, 500)
    shares[e] = np.array([pi[d].sum() for d in dec]) / pi.sum()
    ratios[e] = med_ratio ** e
    print(f"e={e}: median-item ratio {ratios[e]:.2f} -> {ratios[e]:.0f}x; top decile {100*shares[e][9]:.1f}%; "
          f"bottom three {100*shares[e][:3].sum():.1f}%; bottom five {100*shares[e][:5].sum():.1f}% "
          f"({500*shares[e][:5].sum():.0f} of 500)")

plt.rcParams.update({"font.family": "serif", "font.size": 11, "mathtext.fontset": "dejavuserif"})
fig, ax = plt.subplots(figsize=(7.0, 4.6))
x = np.arange(1, 11)
sty = {1.0: dict(color="#b2182b", marker="o", ls="-", label=r"$e=1$  (MUS)"),
       0.7: dict(color="#2166ac", marker="s", ls="-", label=r"$e=0.7$"),
       0.5: dict(color="#5aae61", marker="^", ls="--", label=r"$e=0.5$")}
for e in E:
    ax.plot(x, 100 * shares[e], lw=2.2, ms=7, **sty[e])
ax.set_xticks(x); ax.set_xlabel("Amount decile of the ledger (10 = largest)")
ax.set_ylabel("Share of expected sample (%)"); ax.set_ylim(0, 63)
ax.legend(loc="upper left", frameon=False)
ax.text(1.3, 42, "Selection-weight ratio,\nmedian top-decile item to\nmedian bottom-decile item:\n"
        + "\n".join(f"$e={e:g}$: {ratios[e]:.0f}$\\times$" for e in E), va="top", fontsize=10.5)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("figures/fig6_allocation.png", dpi=200)
