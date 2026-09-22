# PMM complete-condition review

Can the published Peat Marwick Mitchell (PMM) audit-error record say how much error
occurrence would have to rise to offset the observed decline in relative severity, and
whether it did?

Prepared 22 September 2026. Scope: Ramage, Krieger and Spero (1979, JAR Supplement,
"RKS"), Johnson, Leitch and Neter (1981, TAR, "JLN"), Neter, Johnson and Leitch (1985,
TAR, "NJL"), read from the scans in `sources/` (SHA256 in
`transcriptions/source_manifest.json`). Every number below was checked
against the rendered page, not the OCR. Files produced alongside this review:

| File | Content |
|---|---|
| `PMM_SOURCE_COMPATIBILITY.csv` | source map: every relevant table, its exact definition, universe, weighting, exclusions, compatibility |
| `PMM_BAND_PROPORTIONALITY_TEST.csv` | every candidate band-level pairing; all rows `not_computable` with the reason |
| `PMM_COMPLETE_MOMENT_TEST.csv` | audit-wide test, one row per audit, with source inputs, formulas, rounding intervals, emission status |
| `inputs/pmm_inputs.csv` | transcribed source cells with page references |
| `compute.py`, `verify.py` | computation and 300+ assertions (`python3 verify.py` prints `ALL n CHECKS PASSED`) |

Notation follows the task: `F` line-item error rate, `R` dollar-unit error rate,
`rho_$ = E_$[tau^2|err] / E_LI[tau^2|err]`, `G = (R/F) rho_$`.

---

## 1. Executive verdict

**C. PARTIAL TEST ONLY**, with one firm audit-wide result and one conditional one.

- **No band-level test exists.** No PMM paper prints any squared-taint (or any taint)
  severity statistic on the same partition of items on which it prints occurrence. The
  only banded occurrence table (JLN Table 7) and the only banded severity tables (NJL
  Tables 4 and 5) partition different universes by different rules and report different
  statistics. The target sentence "occurrence would have needed to rise from x% to y% in
  the high band; it rose to z%" cannot be written from the printed record for any audit.

- **A hard audit-wide result is available without any new interpretation.** Because the
  dollar-unit error rate is a proportion of book dollars, `R <= 1`. Combined with the
  identity `G = (R/F) rho_$`, this gives `G <= rho_$ / F`. Using only JLN Table 6 (`F`)
  and the `rho_$` already in the supplement, **8 of the 20 audits have `rho_$/F < 1`**
  (16, 69, 13, 22, 23, 27, 32, 33): the dollar-unit error rate that would be needed to
  restore proportionality exceeds 100% of the account's dollars. For 7 of those 8 the
  conclusion survives the worst possible allocation of the 44 excluded zero/negative-book
  errors and the printed rounding. This is the "occurrence would have to rise by more
  than is arithmetically possible" statement, at audit level.

- **A conditional per-audit `G` is computable for 10 audits** through an exact identity
  (`abar_e = ybar / mu_$`, so `R = F ybar / (mu_$ abar)`), which requires reading the
  JLN Table 9 mean as the weighted mean error per erroneous item. That reading is
  strongly supported (the alternative implies `R > 1` in 16 of 18 audits) but is an
  interpretation of a printed definition, so per the task's rule it is flagged and not
  promoted to manuscript-ready status. For the 10 audits whose error universe is the
  same in Tables 9 and 3, it gives `G < 1` with rounding interval excluding 1 in 6
  audits, `G > 1` in 1 (audit 6), and intervals straddling 1 in 3 (91, 14, 56).

- **Per-audit published `R` does not exist.** NJL Table 7 prints only the distribution
  of dollar-unit rates across the 55 receivables and 26 inventory audits. Verdict B as
  literally stated ("compatible line-item/dollar-unit occurrence rates") is therefore
  not available.

---

## 2. Source map

Full detail (page, table, definition, universe, weighting, exclusions, assessment) is
in `PMM_SOURCE_COMPATIBILITY.csv`. The decisive entries:

| Paper, page, table | Statistic | Exact printed definition | Verdict for this task |
|---|---|---|---|
| JLN p292 Appendix eq. (2) | error rate | `p_st = sum_h N_h p_h / N` (weighted proportion of line items in error) | `F = E[I]` over the whole population, all detected errors |
| JLN p278 Table 6 | `F`, mean book value, balance, 20 audits | weighted rate; mean book per line item in dollars | `F` and `abar` available for all 20 |
| JLN p279 Table 7 | error rate by lowest/middle/highest book-value third | items grouped by book value into three groups of equal size; rates weighted | banded occurrence, but no severity on this partition; boundaries and dollar shares unpublished |
| JLN p283 Table 9 | mean, SD of error amounts, 20 audits | "characteristics of each of the 20 error amount distributions"; Appendix eq. (1) prints `y_st` with denominator `N` | read as mean per erroneous item (see 4.2); universe = all 4,038 errors |
| JLN p286 | exclusion | 44 of 4,038 unweighted errors with zero or negative book balance excluded from the tainting study | taint universe = 3,994 errors; not identified by audit |
| JLN p287 Table 12 | mean, SD of line-item taints | tainting = error / book value (fn. 13) | `E_LI[tau^2 | err] = mu^2 + sd^2` |
| NJL p490 Table 1 | dollar-unit taint distribution | each line item's taint counted once per book dollar | `mu_$ = sum(w a tau) / sum(w a) = D / A_e` exactly |
| NJL p493 Table 3 | line-item and dollar-unit moments, same 20 audits | line-item columns repeat JLN Table 12; dollar-unit weighted by book amount (fn. 1 p489) | `rho_$` inputs; identical line-item cells verified on both scans |
| NJL p494 Table 4, p495 Table 5 | median positive (negative) taint, small vs large book amount | positive taints divided into two subgroups with approximately equal numbers of line items | partition of erroneous items, not of the population; medians; sign-split. INCOMPATIBLE with Table 7 |
| NJL p496 Table 6 | definitions | dollar-unit error rate = total book amount of line items containing errors / total book amount of all line items | `R = E[aI] / E[a]` exactly as the task defines it |
| NJL p497 Table 7 | distributions of dollar-unit error rates | frequency table across 55 + 26 audits; medians .040 and .186 | per-audit `R` NOT printed |
| RKS p75 | `F` | `sum_i W_i e_i / n_i`, `W_i = N_i/N`, 11 strata plus certainty stratum | agrees with JLN Table 6 within .01 for 17 of 18 shared audits; audit 24 discrepant (.42 vs .624); audits 22 and 80 absent from RKS's 97 |
| RKS p81, p85, Tables 7-8 | `RM = |Y - X| / |X|` and slopes of log RM on log |X| | relative magnitude scaled to AUDIT value, not book value (fn. 10 p81) | not a taint; must not be substituted |
| RKS p88-95 Appendix A | per population `NE`, `NOV`, `CON`, `BV<0`, `F`, `FOV` | counts of negative-book errors among sampled errors | identifies which of the 20 audits have errors excluded from the taint tables |
| RKS p96-99 Tables 13-16 | per-stratum `N`, `n`, rate for populations 10, 11, 93, 94 | eleven ordinal strata, boundaries not printed | banded occurrence for audit 11 only; no severity by stratum anywhere in PMM |
| RKS p75 | data source | item-level book and audited values of every sampled error are in the PMM Executive Office Research Report (EORR), not in the paper | the supplement's statement that these values are "listed in Ramage et al. (1979)" is wrong |

Neter and Loebbecke (1975) is a separate four-population study and contains nothing
PMM-compatible; it was not used.

---

## 3. Band-level test

**Not computable for any audit or band comparison.** The candidate pairings and the
reason each fails are in `PMM_BAND_PROPORTIONALITY_TEST.csv`. Summary of the
compatibility checklist for the only non-trivial pairing (JLN Table 7 occurrence with
NJL Table 4/5 severity):

| Requirement | JLN Table 7 | NJL Tables 4/5 | Same? |
|---|---|---|---|
| audit | 20 audits | same 20 | yes |
| item universe | all line items | erroneous items with positive book value, then split by sign of taint | no |
| exclusions | none stated | zero/negative-book errors excluded; negative (positive) taints excluded in T4 (T5) | no |
| band boundaries | thirds of all line items by book value | halves of erroneous positive-taint (negative-taint) items by book value | no |
| statistic | line-item error rate | median taint | not a second moment |
| weighting | `N_h/n_h` | `N_h/n_h` | yes |

The pooled taint histograms (JLN Table 11, NJL Table 2) and pooled moments (JLN Table
12, NJL Table 3) carry no band split. JLN Table 13 partitions erroneous items into
deciles without amount coordinates and reports error-amount SDs, not taint moments. RKS
Tables 13-16 give stratum error rates for four populations (one of them audit 11) but
no severity by stratum exists in any PMM paper. The supplement's earlier attempt to bound
subgroup second moments from medians plus pooled histograms (17 of 20 straddling one)
stands as the only band-level statement and was not repeated here.

---

## 4. Audit-wide moment test

### 4.1 Definitions and identities used

All quantities are on the taint universe (errors on positive book values), design
weights `w = N_h/n_h` throughout.

```
mu_$   = sum(w a tau) / sum(w a) = D / A_e          NJL Table 1
R      = A_e / A                                    NJL Table 6
F      = n_e / N                                    JLN Appendix eq. (2)
abar   = A / N                                      JLN Table 6
R / F  = (A_e / n_e) / (A / N) = abar_e / abar
G      = (R / F) rho_$ = E[a tau^2 I] / (E[a] E[tau^2 I])
```

Two consequences:

1. **Ceiling.** `R <= 1` (erroneous-item dollars cannot exceed the account's dollars),
   so `G <= rho_$ / F_tau`, where `F_tau` is the line-item rate on the taint universe,
   `F_tau >= (F - .005)(1 - k/n)` with `k` the number of the audit's `n` unweighted
   errors excluded for zero/negative book value. Needs only Tables 6, 12 and 3.
   Equivalently, the dollar-unit rate that proportionality would require is
   `R_required = F / rho_$`, and it is unattainable when it exceeds 1.
2. **Derived `R`.** `abar_e = ybar / mu_$` with `ybar` the weighted mean error per
   erroneous item (JLN Table 9), so `R = F ybar / (mu_$ abar)` and
   `G = rho_$ ybar / (mu_$ abar)`. Needs Table 9 in addition.

### 4.2 Compatibility findings

- `F` (JLN Table 6) is available for all 20 audits. It is the weighted line-item rate
  over the whole population, all errors. RKS Appendix A reproduces it within .01 for 17
  of the 18 shared audits; audit 24 is printed as .42 in JLN and .624 in RKS for the
  same 284 sampled errors.
- `R` per audit is **not published** anywhere (NJL Table 7 is an across-audit
  distribution; RKS has no dollar-unit rate).
- `rho_$` inputs: JLN Table 12 and NJL Table 3 line-item columns are cell-for-cell
  identical for all 20 audits on both scans; NJL states that the dollar-unit
  distributions cover the same audits and error records (p490: the ranges "do not, of
  course, differ"). Exclusions are therefore identical. The supplement's characterisation
  of the weighting (line-item: design weights; dollar-unit: book amount times design
  weights) matches NJL fn. 1 and Table 1. Neither paper states the SD denominator; the
  supplement's sensitivity note stands. The supplement's counts (19 of 20 below 1, 16
  below .5, 11 below .2) and every Table S3.2 value and rounding interval reproduce
  from the transcribed cells (`verify.py`).
- **JLN Table 9 reading.** The Appendix's eq. (1) divides by `N`, which would make the
  printed mean an error per population item. Under that reading `R = ybar/(mu_$ abar)`
  exceeds 1 in 16 of the 18 audits with a positive ratio (e.g. audit 6: 1.63; audit 16:
  2.08), which is impossible. Under the per-erroneous-item reading `R` lies in (0, 1]
  for all 18. Table 9 is therefore read as the weighted mean per erroneous item
  ("characteristics of each of the 20 error amount distributions", p281). This is the
  one interpretive step in route 2, and it is flagged as such.
- **Universe mismatch.** Table 9 includes the 44 zero/negative-book errors; Tables 12
  and 3 exclude them. RKS Appendix A counts negative-book sampled errors: 11 (9 of 173),
  15 (15 of 131), 16 (2 of 71), 59 (9 of 79), 77 (6 of 39), 23 (6 of 1,139), 24 (2 of
  284), 33 (1 of 174); zero for 6, 69, 81, 91, 13, 14, 27, 32, 56, 60; unknown for 22
  and 80 (absent from RKS). RKS's negative-book total is 50 against JLN's 44
  zero-or-negative, so the two data cuts differ slightly and zero-book errors cannot be
  many. For the mismatch audits the excluded errors' amounts are unknown and `ybar`
  cannot be adjusted, so no derived result is emitted.
- **Internal inconsistencies.** Audit 24: `ybar = -249` while `mu_LI = +.08` and
  `mu_$ = +.03` (sign contradiction), a printed minimum (17,500) above the mean, and
  the JLN/RKS rate discrepancy. Audit 33: `ybar = -124` is driven by the -1,505,800
  outlier while `mu_$ = +.24`; the outlier must be the one negative-book error RKS
  reports for population 33 and hence outside the taint universe. Neither audit yields
  a derived `R`; the ceiling bound (route 1) still applies to 33.

### 4.3 Results

Point values; rounding intervals propagate half a printed unit on every input
(`F +-.005`, moments `+-.005`, `ybar +-.5`, `abar +-.5`); rounding corners that would imply `R > 1` are infeasible and excluded. Full detail in
`PMM_COMPLETE_MOMENT_TEST.csv`.

**Route 1, ceiling (no Table 9 needed).** `R_required = F/rho_$`; `G_max` uses the
upper `rho_$` bound and the lower `F_tau` bound with the RKS exclusion count (44 for
audits 22 and 80).

| Audit | Account | F | rho_$ | R required for G = 1 | G_max (ceiling) | Verdict |
|---|---|---|---|---|---|---|
| 16 | AR | .27 | .006 | 41.8 | .038 | G < 1 forced |
| 13 | INV | .71 | .020 | 35.6 | .029 | G < 1 forced |
| 33 | INV | .65 | .036 | 18.0 | .059 | G < 1 forced |
| 22 | INV | .32 | .034 | 9.5 | .119 | G < 1 forced |
| 27 | INV | .13 | .020 | 6.4 | .169 | G < 1 forced |
| 23 | INV | .29 | .056 | 5.2 | .205 | G < 1 forced |
| 32 | INV | .71 | .270 | 2.6 | .408 | G < 1 forced |
| 69 | AR | .14 | .101 | 1.39 | .826 | G < 1 forced (needs RKS's zero exclusions for 69; not forced if the 44 excluded errors were all in this audit) |
| 14 | INV | .55 | .547 | 1.01 | 1.08 | at the ceiling; not decided |
| 60 | INV | .76 | .788 | .96 | 1.10 | not bounded |
| 91 | AR | .86 | .946 | .91 | 1.13 | not bounded |
| 24 | INV | .42 | .484 | .87 | 1.33 | not bounded |
| 59 | AR | .06 | .077 | .78 | 1.73 | not bounded |
| 15 | AR | .16 | .226 | .71 | 1.77 | not bounded |
| 56 | INV | .30 | .453 | .66 | 1.89 | not bounded |
| 80 | AR | .09 | .175 | .52 | 21.3 | not bounded |
| 11 | AR | .09 | .178 | .51 | 2.47 | not bounded |
| 81 | AR | .06 | .184 | .33 | 3.50 | not bounded |
| 77 | AR | .12 | .449 | .27 | 4.90 | not bounded |
| 6 | AR | .12 | 3.189 | .04 | 30.6 | not bounded |

Under the strict worst case (all 44 excluded errors assigned to the audit in question)
the forced set is 16, 13, 33, 22, 27, 23, 32 (7 audits); 69 drops out.

**Route 2, derived `R` (Table 9 per-erroneous-item reading; emitted only for the 10
universe-compatible audits).**

| Audit | Account | F | R derived | rho_$ | R/F = abar_e/abar | G | G interval | Implication |
|---|---|---|---|---|---|---|---|---|
| 13 | INV | .71 | .833 | .020 | 1.17 | .023 | [.021, .027] | G < 1 |
| 27 | INV | .13 | .111 | .020 | .86 | .017 | [.016, .019] | G < 1 |
| 69 | AR | .14 | .202 | .101 | 1.45 | .146 | [.120, .180] | G < 1 |
| 81 | AR | .06 | .101 | .184 | 1.68 | .310 | [.294, .326] | G < 1 |
| 32 | INV | .71 | .826 | .270 | 1.16 | .314 | [.148, .407] | G < 1 |
| 60 | INV | .76 | .868 | .788 | 1.14 | .900 | [.845, .960] | G < 1 |
| 56 | INV | .30 | .538 | .453 | 1.79 | .813 | [.655, 1.029] | straddles 1 |
| 14 | INV | .55 | .889 | .547 | 1.62 | .884 | [.698, 1.073] | straddles 1 |
| 91 | AR | .86 | .917 | .946 | 1.07 | 1.009 | [.971, 1.048] | straddles 1 |
| 6 | AR | .12 | .195 | 3.189 | 1.63 | 5.18 | [4.72, 5.71] | G > 1 |

Nominal values for the non-emitted audits, shown only so the reader can see they do
not contradict the pattern: 11 (.29), 15 (.51), 16 (.013), 59 (.15), 77 (.38), 80
(.31), 22 (.042), 23 (.077); 24 and 33 are negative and meaningless (sign
contradictions above). Sanity checks that passed for every emitted audit: `0 < R <= 1`;
`G <= G_max`; `R/F > 1` (erroneous items larger than average) wherever JLN Table 7
shows a rising rate, and `R/F < 1` for audit 27, whose Table 7 rate falls in the top
third.

Tally over the 20 audits, combining the two routes: `G < 1` established for 10 (8 by
the ceiling, plus 81 and 60 by the derived route); `G > 1` for 1 (audit 6); undecided
with intervals straddling 1 for 3 (91, 14, 56); not decidable from the printed record
for 6 (11, 15, 59, 77, 80, 24). No audit other than 6 shows `G > 1`. Under the
manuscript's power representation `E[d^2 | a] ~ a^(2e)`, `G < 1` is the direction
`e < 1`; no numerical `e` is inferred.

---

## 5. Practitioner-readable implications

Only statements directly supported by the printed cells are listed. "Dollars in error"
means the share of the account's book value sitting in line items that contain an
error (NJL's dollar-unit error rate).

Statements needing only Tables 6, 12 and 3 (route 1):

- **Audit 13 (inventory).** Dollar weighting cut the expected squared taint to 2% of its
  line-item level. To offset that one for one, 3,560% of the account's dollars would
  have to sit in erroneous items. The maximum is 100%. Proportional scaling is
  arithmetically impossible in this audit, and the complete quantity is at most 3% of
  what proportionality requires.
- **Audit 16 (receivables).** Severity fell to 0.6% under dollar weighting. Offsetting
  it would need 4,180% of the dollars in error. Impossible; G is at most .04.
- **Audit 33 (inventory).** Severity fell to 3.6%; offsetting needs 1,800% of dollars in
  error. Impossible; G at most .06.
- **Audit 22 (inventory).** Severity fell to 3.4%; offsetting needs 950% of dollars in
  error. Impossible; G at most .12.
- **Audit 27 (inventory).** Severity fell to 2.0%; offsetting needs 640% of dollars in
  error. Impossible; G at most .17.
- **Audit 23 (inventory).** Severity fell to 5.6%; offsetting needs 520% of dollars in
  error. Impossible; G at most .20.
- **Audit 32 (inventory).** Severity fell to 27%; offsetting needs 260% of dollars in
  error. Impossible; G at most .41.
- **Audit 69 (receivables).** Severity fell to 10%; offsetting needs 139% of dollars in
  error. Impossible; G at most .83 (this one relies on RKS's report of no negative-book
  errors in the audit).

Statements that additionally use the derived erroneous-item mean (route 2, flagged):

- **Audit 81 (receivables).** Proportionality would need 33% of the dollars in error.
  The record implies 10%. Occurrence rose (erroneous items averaged 1.7 times the
  population mean) but by a third of what severity required; G = .31.
- **Audit 60 (inventory).** Proportionality would need 96% of dollars in error; the
  record implies 87%. G = .90, interval [.85, .96]. Close to, but below, one.
- **Audit 6 (receivables), the reversal.** Proportionality would need only 4% of
  dollars in error; the record implies 20%. Dollar weighting raised severity here
  (rho_$ = 3.2) and occurrence also rose; G = 5.2. This is the one audit where the
  complete quantity moves the other way.
- **Audit 91 (receivables).** Needs 91%; record implies 92%. G = 1.01, indistinguishable
  from one: an audit in which 84% of errors are 100% taints behaves as MUS assumes.
- **Audits 14 and 56 (inventory).** Intervals straddle one; the printed precision does
  not decide them.

What cannot be said: any statement of the form "occurrence in the high band was x%
against a required y%". No PMM table supports it.

---

## 6. What remains unidentified

- Any band-level quantity: `P_h` and `S_h` on a common partition, the band boundaries
  of JLN Table 7 or NJL Tables 4/5, band dollar shares, and hence `gamma` and the
  between-band versus within-band split of the amount-severity covariance.
- Dollar-weighted occurrence by band, at any resolution.
- Per-audit published `R`. It is derivable only through Table 9 and only for audits
  whose error universe is unchanged by the zero/negative-book exclusion.
- The audit-by-audit allocation of the 44 excluded errors (RKS gives negative-book
  counts summing to 50 across 18 audits; zero-book counts are not printed; audits 22
  and 80 are outside RKS).
- The amounts of the excluded errors, which is why `ybar` cannot be corrected for
  audits 11, 15, 16, 59, 77, 23.
- The SD denominator convention in JLN Table 12 and NJL Table 3.
- The cause of the audit 24 inconsistencies (rate .42 versus .624; sign of the mean
  error; the printed minimum).
- A numerical `e`. `G < 1` fixes the sign of `Cov(a, E[d^2|a]/a^2)`, not its size in
  exponent units.
- The item-level book and audited values. RKS state that these are listed in the PMM
  Executive Office Research Report, which is not published.

---

## 7. Manuscript recommendation

What the manuscript and supplement may now say that they could not before:

1. **Add the ceiling result as a hard, source-level statement.** "For 8 of the 20 PMM
   audits (7 under the most adverse treatment of the excluded errors), the published
   line-item error rate and the line-item and dollar-unit second moments jointly imply
   that no pattern of error occurrence could restore dollar proportionality: the
   dollar-unit error rate required for the complete expected squared taint to be
   invariant to dollar weighting exceeds 100% of the account's book value (from 139% to
   4,180%)." This uses only JLN Table 6, JLN Table 12 and NJL Table 3, the identity
   `G = (R/F) rho_$`, and NJL's own definition of the dollar-unit error rate. It
   answers the "occurrence term is missing" objection at audit level for those audits.
   It is manuscript-ready.

2. **Report the derived-`R` results (Section 4.3, route 2) in the supplement, flagged.**
   State the identity, the Table 9 reading, the impossibility argument that supports it,
   the ten-audit compatibility restriction, and the rounding intervals. Do not promote
   these to the main text until the Table 9 definition is treated as settled. If
   reported, audit 6 (G = 5.2) and audit 91 (G = 1.0) should be named as the exception
   and the boundary case, matching the existing rho_$ narrative.

3. **Keep, and sharpen, the band-level absence statement.** Replace "no PMM source
   publishes dollar-weighted error occurrence by amount band" with the fuller finding:
   no PMM source publishes any severity statistic on the partition on which it publishes
   occurrence; NJL Tables 4/5 split erroneous items, JLN Table 7 splits the population;
   the medians are not second moments. The supplement's negative bounding exercise
   remains the only band-level statement.

4. **Correct one factual sentence in the supplement.** The item-level book and audited
   values are in the unpublished PMM Executive Office Research Report (RKS p75), not
   "listed in Ramage et al. (1979)".

5. **Optionally note two source inconsistencies** already visible in the transcription
   checks (audit 24's rate and sign; audit 33's outlier outside the taint universe), as
   the reason those audits are excluded from any audit-wide calculation beyond the
   ceiling.

6. **Terminology.** Throughout: "20 audits" or "20 audit populations in the PMM research
   file"; the PMM material remains one evidence family. The counts above (8 of 20, 10 of
   20) are counts of audits, not of families.

7. **Do not** infer `e` numerically from `G` or `rho_$`; do not treat the three
   straddling audits as evidence for `e = 1`; do not present required rates as observed
   rates (the tables above label them explicitly).

---

## Verification

`python3 verify.py` re-runs the computation and asserts: audit identifiers align across
JLN Tables 6, 7, 9, 12, NJL Table 3, RKS Appendix A and the supplement's Table S3.2;
every transcribed input equals the independent, scan-verified transcription;
JLN Table 12 and NJL Table 3 line-item cells are identical for all 20 audits; JLN Table
7 error counts equal RKS `NE`; JLN Table 6 rates equal RKS `F` within .01 except audit
24; `rho_$` and its rounding interval reproduce Table S3.2 for all 20 audits and the
19/16/11 counts; the identities `R = F ybar/(mu_$ abar)`, `R/F = abar_e/abar`,
`G = (R/F) rho_$`, `R_required = F/rho_$` hold numerically; `G` lies inside its
interval and below its ceiling; derived results are emitted only for audits marked
compatible; the band-level file contains no computed result; NJL Tables 4/5 are marked
incompatible in the source map.
