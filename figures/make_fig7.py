import csv, os, matplotlib
HERE = os.path.dirname(os.path.abspath(__file__))
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'pmm', 'PMM_COMPLETE_MOMENT_TEST.csv'))))
rows.sort(key=lambda r: float(r['R_required_for_G1']))
labels = [('AR ' if r['account']=='receivables' else 'INV ') + r['audit'] for r in rows]
vals = [float(r['R_required_for_G1']) for r in rows]
lo = [float(r['R_required_lo']) for r in rows]; hi = [float(r['R_required_hi']) for r in rows]
cols = ['#b2182b' if r['account']=='receivables' else '#2166ac' for r in rows]
mk = ['o' if r['account']=='receivables' else 's' for r in rows]
plt.rcParams.update({'font.family':'serif','font.size':11})
fig, ax = plt.subplots(figsize=(7.2, 6.4))
y = list(range(len(rows)))
for yi, v, l, h, c, m in zip(y, vals, lo, hi, cols, mk):
    ax.plot([l, h], [yi, yi], color=c, lw=1.2, alpha=0.5, solid_capstyle='round')
    ax.plot(v, yi, marker=m, color=c, ms=8, ls='none')
ax.axvline(1.0, color='black', lw=1.6)
ax.axvspan(1.0, 100, color='0.92', zorder=0)
ax.set_xscale('log'); ax.set_xlim(0.02, 100)
ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 50]); ax.set_xticklabels(['5%', '10%', '25%', '50%', '100%', '200%', '500%', '1,000%', '5,000%'])
ax.set_yticks(y); ax.set_yticklabels(labels)
ax.set_xlabel('Share of the account\'s recorded dollars that would have to sit in erroneous items\nfor dollar-proportional allocation to be risk-aligned  ($F/\\rho_{\\$}$)')
ax.text(1.08, len(rows)-0.6, 'impossible:\nmore than 100% of dollars', ha='left', va='top', fontsize=10)
ax.plot([], [], 'o', color='#b2182b', label='Receivables'); ax.plot([], [], 's', color='#2166ac', label='Inventory')
ax.legend(loc='lower right', frameon=False)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='x', color='0.85', lw=0.6, zorder=0); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig7_required_rate.png'), dpi=300)
print('ok', [(l, round(v,2)) for l, v in zip(labels, vals)])
