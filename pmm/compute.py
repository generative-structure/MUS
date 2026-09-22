#!/usr/bin/env python3
"""PMM complete-condition test: audit-wide moment route.

Identities (all among the taint universe = errors on positive book values):
  rho_$   = E_$[tau^2|err] / E_LI[tau^2|err] = (mu_D^2+sd_D^2)/(mu_LI^2+sd_LI^2)
  mu_D    = sum(w a tau)/sum(w a) = D/A_e          (NJL 1985 Table 1 definition)
  ybar    = D/n_e (JLN 1981 Table 9 mean error per erroneous item)  [interpretation, see review]
  abar_e  = ybar/mu_D                              (derived erroneous-item mean book)
  R       = A_e/A = F * abar_e/abar                (NJL Table 6 definition; F = JLN Table 6 rate)
  G       = (R/F) rho_$ = rho_$ * ybar/(mu_D*abar) = E[a tau^2 I]/(E[a] E[tau^2 I])
  ceiling: R <= 1  =>  G <= rho_$/F_tau, F_tau = line-item rate on the taint universe.
Rounding: F +-.005, abar +-.5, ybar +-.5, moments +-.005 (half-unit of printed precision);
rounding corners implying R > 1 are infeasible and excluded from the G interval.
"""
import csv, itertools, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'inputs', 'pmm_inputs.csv'))))
JLN_EXCLUDED_TOTAL = 44   # JLN 1981 p.286: 44 of 4,038 unweighted errors excluded (zero/negative book)

def f(x):
    return float(x) if x not in ('', None) else None

def corners(*ivs):
    return itertools.product(*ivs)

def rho_interval(muD, sdD, muLI, sdLI):
    vals = []
    for a, b, c, d in corners((muD-.005, muD+.005), (sdD-.005, sdD+.005),
                              (muLI-.005, muLI+.005), (sdLI-.005, sdLI+.005)):
        vals.append((a*a+b*b)/(c*c+d*d))
    return min(vals), max(vals)

def G_interval(muD, sdD, muLI, sdLI, ybar, abar, F, ngrid=401):
    # feasibility: the implied dollar-unit rate R = F*y/(m*a) cannot exceed 1;
    # a corner is admissible only if R <= 1 for the lowest F in its rounding interval.
    vals = []
    for i in range(ngrid):
        m = muD - .005 + .01*i/(ngrid-1)
        for b, c, d, y, a in corners((sdD-.005, sdD+.005), (muLI-.005, muLI+.005),
                                     (sdLI-.005, sdLI+.005), (ybar-.5, ybar+.5),
                                     (abar-.5, abar+.5)):
            if (F-.005) * y/(m*a) > 1:
                continue
            rho = (m*m+b*b)/(c*c+d*d)
            vals.append(rho * y/(m*a))
    return min(vals), max(vals)

def compat(r):
    aud = int(r['audit'])
    if aud in (24, 33):
        return 'internally_inconsistent'
    if r['rks_in_97'] == '0':
        return 'unverified_universe'
    if int(r['rks_BVneg_appA']) == 0:
        return 'compatible'
    return 'universe_mismatch'

NOTES = {
    24: 'JLN T9 mean error -249 (negative) while NJL T3 mu_D=+.03 and JLN T12 mu_LI=+.08 (positive): sign contradiction between the Table 9 universe (all errors) and the taint universe; JLN T9 printed minimum 17,500 exceeds the mean; JLN T6 rate .42 vs RKS App.A F=.624 for the same 284 errors.',
    33: 'JLN T9 mean error -124 driven by the -1,505,800 extreme outlier while NJL T3 mu_D=+.24: the outlier must lie outside the taint universe (RKS App.A: one negative-book error in pop 33). D differs materially between Table 9 and Table 3.',
}

out = []
for r in rows:
    aud = int(r['audit']); F = f(r['F_jln6']); abar = f(r['abar_jln6']); ybar = f(r['ybar_jln9'])
    muLI, sdLI, muD, sdD = map(f, (r['mu_LI_jln12'], r['sd_LI_jln12'], r['mu_D_njl3'], r['sd_D_njl3']))
    n = int(r['n_unw_jln7'])
    rho = (muD**2+sdD**2)/(muLI**2+sdLI**2)
    rlo, rhi = rho_interval(muD, sdD, muLI, sdLI)
    status = compat(r)
    k_rks = int(r['rks_BVneg_appA']) if r['rks_BVneg_appA'] != '' else None
    # ceiling bound: G <= rho / F_tau ; F_tau >= (F-.005)*(1-k/n)
    k_nom = k_rks if k_rks is not None else JLN_EXCLUDED_TOTAL
    k_worst = min(JLN_EXCLUDED_TOTAL, n-1)
    Ftau_nom = (F-.005)*(1-k_nom/n)
    Ftau_worst = (F-.005)*(1-k_worst/n)
    Gceil_nom = rhi/Ftau_nom
    Gceil_worst = rhi/Ftau_worst
    R_req = F/rho                         # dollar-unit rate needed for G=1 (point)
    R_req_lo, R_req_hi = (F-.005)/rhi, (F+.005)/rlo
    # derived R route
    abar_e = ybar/muD
    R = F*abar_e/abar
    RoverF = abar_e/abar
    G = rho*RoverF
    Glo, Ghi = G_interval(muD, sdD, muLI, sdLI, ybar, abar, F)
    # per-population-item reading of Table 9 (rejected if R>1)
    R_alt = ybar/(muD*abar)
    emit = status == 'compatible'
    if emit and not (0 < R <= 1):
        emit = False; status = 'derived_R_out_of_range'
    ceiling_verdict = ('G<1 forced (required R>1)' if Gceil_nom < 1 else 'not bounded by ceiling')
    ceiling_verdict_worst = ('G<1 forced' if Gceil_worst < 1 else 'not bounded')
    if emit:
        if Ghi < 1: dr = 'G<1 (interval excludes 1)'
        elif Glo > 1: dr = 'G>1 (interval excludes 1)'
        else: dr = 'interval straddles 1'
    else:
        dr = 'not emitted'
    out.append(dict(
        account=r['account'], audit=aud, F=F, F_source='JLN1981 T6 p278 (weighted line-item rate, Appendix eq.2)',
        abar=abar, ybar=ybar, mu_LI=muLI, sd_LI=sdLI, mu_D=muD, sd_D=sdD,
        rho_D=round(rho,4), rho_lo=round(rlo,4), rho_hi=round(rhi,4),
        rho_formula='(mu_D^2+sd_D^2)/(mu_LI^2+sd_LI^2); NJL1985 T3 p493 + JLN1981 T12 p287',
        n_unweighted_errors=n, rks_BVneg=k_rks if k_rks is not None else 'not in RKS 97',
        compatibility=status,
        Ftau_min_nominal=round(Ftau_nom,4), G_ceiling_max_nominal=round(Gceil_nom,4), ceiling_verdict_nominal=ceiling_verdict,
        Ftau_min_worstcase=round(Ftau_worst,4), G_ceiling_max_worstcase=round(Gceil_worst,4), ceiling_verdict_worstcase=ceiling_verdict_worst,
        R_required_for_G1=round(R_req,3), R_required_lo=round(R_req_lo,3), R_required_hi=round(R_req_hi,3),
        R_required_formula='F/rho_D (dollar-unit error rate needed for G=1); must be <=1 to be attainable',
        abar_e_over_abar_derived=round(RoverF,3), R_derived=round(R,3),
        R_derived_formula='R = F*ybar/(mu_D*abar); ybar JLN1981 T9 p283 read as mean per erroneous item',
        R_per_population_item_reading=round(R_alt,3),
        G_derived=round(G,4) if emit else '', G_lo=round(Glo,4) if emit else '', G_hi=round(Ghi,4) if emit else '',
        G_nominal_not_emitted='' if emit else round(G,4),
        G_formula='G = rho_D * ybar/(mu_D*abar) = (R/F)*rho_D',
        derived_verdict=dr,
        notes=NOTES.get(aud, '' if status=='compatible' else
              ('not in RKS 97-population set; exclusion count unknown (worst case 44)' if status=='unverified_universe'
               else f'{k_rks} of {n} unweighted errors have negative book value (RKS App.A) and are excluded from the taint tables but not from JLN T9; ybar not adjustable')),
    ))

fields = list(out[0].keys())
with open(os.path.join(HERE, 'PMM_COMPLETE_MOMENT_TEST.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(out)

# console summary
print(f"{'aud':>4} {'F':>5} {'rho':>6} {'rho_hi/Ftau':>11} {'ceil':>6} {'Rreq':>6} {'R_alt':>6} {'ae/a':>6} {'R':>6} {'G':>7} {'Glo':>7} {'Ghi':>7}  status")
for o in out:
    print(f"{o['audit']:>4} {o['F']:>5} {o['rho_D']:>6} {o['G_ceiling_max_nominal']:>11} {('<1' if o['G_ceiling_max_nominal']<1 else '  '):>6} {o['R_required_for_G1']:>6} {o['R_per_population_item_reading']:>6} {o['abar_e_over_abar_derived']:>6} {o['R_derived']:>6} {str(o['G_derived'] or o['G_nominal_not_emitted']):>7} {str(o['G_lo']):>7} {str(o['G_hi']):>7}  {o['compatibility']}")
print('per-population-item reading gives R>1 in', sum(1 for o in out if o['R_per_population_item_reading']>1), 'of', sum(1 for o in out if o['R_per_population_item_reading']>0), 'audits with positive ratio')
print('ceiling forces G<1 (nominal):', [o['audit'] for o in out if o['G_ceiling_max_nominal']<1])
print('ceiling forces G<1 (worst):', [o['audit'] for o in out if o['G_ceiling_max_worstcase']<1])
print('emitted derived:', [(o['audit'], o['derived_verdict']) for o in out if o['G_derived']!=''])
