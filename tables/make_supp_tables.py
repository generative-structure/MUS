import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
s32 = {int(r['audit']): r for r in csv.DictReader(open(os.path.join(HERE, '..', 'pmm', 'inputs', 'supplement_S3_2_rho.csv')))}
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'pmm', 'PMM_COMPLETE_MOMENT_TEST.csv'))))
order = ['receivables', 'inventory']
rows.sort(key=lambda r: (order.index(r['account']), float(r['R_required_for_G1'])))
def pct(x): 
    v = float(x)*100
    return f"{v:,.0f}\\%" if v >= 100 else f"{v:.0f}\\%"
def fmt(x, d=3): return f"{float(x):.{d}f}"
# Table S3.3 : ceiling result
out = []
for r in rows:
    acct = 'Receivables' if r['account']=='receivables' else 'Inventory'
    k = r['rks_BVneg'] if r['rks_BVneg'] != 'not in RKS 97' else 'n/a'
    gnom, gw = float(r['G_ceiling_max_nominal']), float(r['G_ceiling_max_worstcase'])
    verdict = 'Impossible (robust)' if gw < 1 else ('Impossible (audit record)' if gnom < 1 else 'Attainable')
    out.append(f"{acct} & {r['audit']} & {fmt(r['F'],2)} & {fmt(r['rho_D'])} & [{s32[int(r['audit'])]['lo_S32']}, {s32[int(r['audit'])]['hi_S32']}] & {pct(r['R_required_for_G1'])} & [{pct(r['R_required_lo'])}, {pct(r['R_required_hi'])}] & {k}/{r['n_unweighted_errors']} & {fmt(gnom,3)} & {fmt(gw,3)} & {verdict} \\\\")
open(os.path.join(HERE, 'S33_rows.tex'),'w').write('\n'.join(out)+'\n\\bottomrule\n')
# Table S3.4 : derived R diagnostic
out = []
for r in rows:
    acct = 'Receivables' if r['account']=='receivables' else 'Inventory'
    comp = {'compatible':'compatible','universe_mismatch':'universe mismatch','unverified_universe':'unverified (not in RKS)','internally_inconsistent':'inconsistent in print'}[r['compatibility']]
    if r['G_derived']:
        cells = f"{fmt(r['R_derived'])} & {fmt(r['abar_e_over_abar_derived'],2)} & {fmt(r['G_derived'])} & [{fmt(r['G_lo'])}, {fmt(r['G_hi'])}] & {r['derived_verdict'].replace('(interval excludes 1)','').strip().replace('G<1','$G<1$').replace('G>1','$G>1$')}"
    else:
        g = r['G_nominal_not_emitted']
        cells = f"--- & --- & ({fmt(g)})$^{{n}}$ & --- & not emitted"
    out.append(f"{acct} & {r['audit']} & {fmt(r['ybar'],0)} & {fmt(r['mu_D'],2)} & {fmt(r['abar'],0)} & {comp} & {cells} \\\\")
open(os.path.join(HERE, 'S34_rows.tex'),'w').write('\n'.join(out)+'\n\\bottomrule\n')
# counts for the text
req = {int(r['audit']): float(r['R_required_for_G1']) for r in rows}
lo = {int(r['audit']): float(r['R_required_lo']) for r in rows}
print('>=50% point:', sum(v>=.5 for v in req.values()), 'robust:', sum(v>=.5 for v in lo.values()))
print('>=25% point:', sum(v>=.25 for v in req.values()), 'robust:', sum(v>=.25 for v in lo.values()))
print('>100% worst:', sorted(int(r['audit']) for r in rows if float(r['G_ceiling_max_worstcase'])<1))
print('>100% nominal:', sorted(int(r['audit']) for r in rows if float(r['G_ceiling_max_nominal'])<1))
