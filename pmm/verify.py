#!/usr/bin/env python3
"""Verification of every derived quantity in PMM_COMPLETE_MOMENT_TEST.csv."""
import csv, os, math, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TRANS = os.path.join(HERE, 'transcriptions')
subprocess.run([sys.executable, os.path.join(HERE, 'compute.py')], check=True, capture_output=True)
inp = {int(r['audit']): r for r in csv.DictReader(open(os.path.join(HERE, 'inputs', 'pmm_inputs.csv')))}
res = {int(r['audit']): r for r in csv.DictReader(open(os.path.join(HERE, 'PMM_COMPLETE_MOMENT_TEST.csv')))}
s32 = {int(r['audit']): r for r in csv.DictReader(open(os.path.join(HERE, 'inputs', 'supplement_S3_2_rho.csv')))}
checks = 0
def ok(cond, msg):
    global checks
    assert cond, msg
    checks += 1

AUDITS = [6,11,15,16,59,69,77,80,81,91,13,14,22,23,24,27,32,33,56,60]
ok(sorted(inp) == sorted(AUDITS) == sorted(res) == sorted(s32), 'audit identifiers align across inputs, results, supplement S3.2')

# 1. transcribed inputs agree with the independent transcriptions (visually verified scans)
def read_long(fn, metric_map):
    d = {}
    for r in csv.DictReader(open(os.path.join(TRANS, fn))):
        if r['metric'] in metric_map and r['value'] != '':
            d.setdefault(int(r['audit_id']), {})[metric_map[r['metric']]] = float(r['value'])
    return d
t12 = read_long('jln_table12.csv', {'mean': 'mu', 'sd': 'sd'})
t3 = read_long('njl_table3.csv', {'mean_line': 'muL', 'sd_line': 'sdL', 'mean_dollar': 'muD', 'sd_dollar': 'sdD'})
t9 = read_long('jln_table9.csv', {'mean': 'ybar'})
t6 = {int(r['audit_id']): r for r in csv.DictReader(open(os.path.join(TRANS, 'jln_table6.csv')))}
t7 = {int(r['audit_id']): r for r in csv.DictReader(open(os.path.join(TRANS, 'jln_table7.csv')))}
rks = {int(r['POP']): r for r in csv.DictReader(open(os.path.join(TRANS, 'rks1979_appendixA_rates.csv')))}
rksT = {int(r['POP']): r for r in csv.DictReader(open(os.path.join(TRANS, 'rks1979_appendixA_transcription.csv')))}
for a in AUDITS:
    r = inp[a]
    ok(abs(float(r['mu_LI_jln12']) - t12[a]['mu']) < 1e-9 and abs(float(r['sd_LI_jln12']) - t12[a]['sd']) < 1e-9, f'JLN T12 inputs audit {a}')
    ok(abs(float(r['mu_D_njl3']) - t3[a]['muD']) < 1e-9 and abs(float(r['sd_D_njl3']) - t3[a]['sdD']) < 1e-9, f'NJL T3 inputs audit {a}')
    ok(abs(t12[a]['mu'] - t3[a]['muL']) < 1e-9 and abs(t12[a]['sd'] - t3[a]['sdL']) < 1e-9, f'JLN T12 == NJL T3 line-item cells audit {a} (same error records)')
    ok(abs(float(r['ybar_jln9']) - t9[a]['ybar']) < 1e-9, f'JLN T9 mean audit {a}')
    ok(abs(float(r['F_jln6']) - float(t6[a]['overall_rate'])) < 1e-9 and abs(float(r['abar_jln6']) - float(t6[a]['mean_book_amount'])) < 1e-9, f'JLN T6 audit {a}')
    ok(int(r['n_unw_jln7']) == int(t7[a]['unweighted_errors']), f'JLN T7 error count audit {a}')
    for k, c in (('P_L_jln7', 'low_rate'), ('P_M_jln7', 'middle_rate'), ('P_H_jln7', 'high_rate')):
        ok(abs(float(r[k]) - float(t7[a][c])) < 1e-9, f'JLN T7 {k} audit {a}')
    if r['rks_in_97'] == '1':
        ok(a in rks and abs(float(r['rks_F_appA']) - float(rks[a]['F'])) < 1e-9, f'RKS F audit {a}')
        ok(int(r['rks_NE_appA']) == int(rksT[a]['NE']) == int(r['n_unw_jln7']), f'RKS NE == JLN T7 unweighted errors audit {a}')
        ok(int(r['rks_BVneg_appA']) == int(rksT[a]['BV_lt0']), f'RKS BV<0 audit {a}')
        if a != 24:
            ok(abs(float(r['F_jln6']) - float(rks[a]['F'])) <= 0.0105, f'JLN T6 rate vs RKS F audit {a}')
        else:
            ok(abs(float(r['F_jln6']) - float(rks[a]['F'])) > 0.1, 'audit 24 rate discrepancy is real (.42 vs .624)')
    else:
        ok(a not in rks and a in (22, 80), f'audit {a} absent from RKS 97')
ok(sum(int(inp[a]['rks_BVneg_appA']) for a in AUDITS if inp[a]['rks_in_97'] == '1') == 50, 'RKS negative-book errors among the 18 shared audits sum to 50 (JLN prose: 44 zero-or-negative of 4,038)')
ok(sum(int(inp[a]['n_unw_jln7']) for a in AUDITS) == 4037, 'JLN T7 counts sum to 4,037 (prose 4,038; known discrepancy)')

# 2. rho_$ reproduces from source inputs and matches supplement Table S3.2 (value and rounding interval)
for a in AUDITS:
    r, o, s = inp[a], res[a], s32[a]
    mu, sd, muD, sdD = map(float, (r['mu_LI_jln12'], r['sd_LI_jln12'], r['mu_D_njl3'], r['sd_D_njl3']))
    rho = (muD**2 + sdD**2) / (mu**2 + sd**2)
    ok(abs(rho - float(o['rho_D'])) < 1e-4, f'rho recomputed audit {a}')
    ok(abs(round(rho, 3) - float(s['rho_S32'])) < 1e-9, f'rho matches supplement S3.2 audit {a}: {rho:.4f} vs {s["rho_S32"]}')
    ok(abs(round(float(o['rho_lo']), 3) - float(s['lo_S32'])) <= 0.0015 and abs(round(float(o["rho_hi"]), 3) - float(s["hi_S32"])) <= 0.0015, f'rho interval matches S3.2 audit {a}')
ok(sum(float(res[a]['rho_D']) < 1 for a in AUDITS) == 19 and sum(float(res[a]['rho_D']) < .5 for a in AUDITS) == 16 and sum(float(res[a]['rho_D']) < .2 for a in AUDITS) == 11, 'supplement counts 19/16/11 reproduce')

# 3. identities
for a in AUDITS:
    r, o = inp[a], res[a]
    F, abar, ybar, muD = map(float, (r['F_jln6'], r['abar_jln6'], r['ybar_jln9'], r['mu_D_njl3']))
    muL, sdL, sdD = map(float, (r['mu_LI_jln12'], r['sd_LI_jln12'], r['sd_D_njl3']))
    rho = (muD**2 + sdD**2) / (muL**2 + sdL**2)
    R = F * ybar / (muD * abar)
    ok(abs(R - float(o['R_derived'])) < 5e-4, f'R identity audit {a}')
    ok(abs(R / F - float(o['abar_e_over_abar_derived'])) < 5e-4, f'R/F = abar_e/abar audit {a}')
    Gnom = float(o['G_derived'] or o['G_nominal_not_emitted'])
    ok(abs(rho * R / F - Gnom) < 2e-4, f'G = (R/F) rho identity audit {a}')
    ok(abs(ybar / (muD * abar) - float(o['R_per_population_item_reading'])) < 5e-4, f'alt reading audit {a}')
    ok(abs(F / rho - float(o['R_required_for_G1'])) < 2e-3 * max(1, F / rho), f'required R audit {a}')
    # ceiling: required R > 1  <=>  ceiling forces G<1 (point values), and G <= rho/F_tau holds for emitted G
    ok((float(o['R_required_for_G1']) > 1) == (rho / F < 1), f"ceiling equivalence audit {a}")
    ok(float(o['G_ceiling_max_nominal']) >= float(o['G_ceiling_max_worstcase']) * 0 and float(o['G_ceiling_max_worstcase']) >= float(o['G_ceiling_max_nominal']) - 1e-9, f'worst-case ceiling is looser audit {a}')
    if o['G_derived'] != '':
        ok(float(o['G_lo']) <= float(o['G_derived']) <= float(o['G_hi']), f'G inside interval audit {a}')
        ok(float(o['G_hi']) <= float(o['G_ceiling_max_nominal']) + 1e-9 or float(o['R_derived']) > 1, f'derived G respects ceiling audit {a}')
        ok(0 < float(o['R_derived']) <= 1, f'derived R in (0,1] audit {a}')

# 4. emission rules
for a in AUDITS:
    o = res[a]
    if o['compatibility'] != 'compatible':
        ok(o['G_derived'] == '' and o['G_lo'] == '' and o['G_hi'] == '', f'no derived result emitted for non-compatible audit {a} ({o["compatibility"]})')
    else:
        ok(int(inp[a]['rks_BVneg_appA']) == 0 and inp[a]['rks_in_97'] == '1', f'compatible audit {a} has zero negative-book errors in RKS')
ok(sorted(a for a in AUDITS if res[a]['compatibility'] == 'compatible') == [6, 13, 14, 27, 32, 56, 60, 69, 81, 91], 'compatible set')
ok(sorted(a for a in AUDITS if res[a]['compatibility'] == 'internally_inconsistent') == [24, 33], 'inconsistent set')
ok(all(res[a]['R_per_population_item_reading'] and (float(res[a]['R_per_population_item_reading']) > 1) for a in [6, 11, 15, 16, 59, 69, 80, 81, 91, 13, 14, 22, 23, 32, 56, 60]), 'per-population-item reading of JLN T9 implies R>1 in 16 audits (reading rejected)')
ok(sorted(a for a in AUDITS if float(res[a]['G_ceiling_max_nominal']) < 1) == [13, 16, 22, 23, 27, 32, 33, 69], 'ceiling-forced set (nominal)')
ok(sorted(a for a in AUDITS if float(res[a]['G_ceiling_max_worstcase']) < 1) == [13, 16, 22, 23, 27, 32, 33], 'ceiling-forced set (worst case)')
ok(sorted(a for a in AUDITS if res[a]['derived_verdict'] == 'G<1 (interval excludes 1)') == [13, 27, 32, 60, 69, 81], 'derived G<1 set')
ok(sorted(a for a in AUDITS if res[a]['derived_verdict'] == 'G>1 (interval excludes 1)') == [6], 'derived G>1 set')
ok(sorted(a for a in AUDITS if res[a]['derived_verdict'] == 'interval straddles 1') == [14, 56, 91], 'derived straddle set')

# 5. band file: nothing computed from incompatible pairs
band = list(csv.DictReader(open(os.path.join(HERE, 'PMM_BAND_PROPORTIONALITY_TEST.csv'))))
ok(len(band) > 0 and all(b['status'] == 'not_computable' and b['observed_XY'] == '' and b['required_P_H'] == '' for b in band), 'band-level file contains no computed results')
compat = list(csv.DictReader(open(os.path.join(HERE, 'PMM_SOURCE_COMPATIBILITY.csv'))))
ok(any('INCOMPATIBLE' in c['compatibility_assessment'] for c in compat if c['table'] in ('T4', 'T5')), 'NJL T4/T5 marked incompatible with JLN T7 in the source map')
print(f'ALL {checks} CHECKS PASSED')
