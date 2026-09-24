# MUS Risk-Aligned Allocation Calculator: methodological note

Companion to *Assumed, Not Measured: What Monetary-Unit Sampling Assumes About Where Error Lives*
(Section VII, Equation 11; Supplemental Section S1.6 and S12). Workbook:
`MUS_Risk_Aligned_Allocation_Calculator.xlsx`. Independent check: `check_calculator.py`
(run after opening and recalculating the workbook; prints `ALL n CALCULATOR CHECKS PASSED`).

## What it does, and what it does not do

The workbook distributes a probabilistic sample size that the auditor has already chosen across
three or four recorded-amount bands, after certainty items have been removed. It is an allocation
aid. It does not determine the sample size, evaluate the sample, compute an upper misstatement
limit, or replace the engagement's sampling methodology.

## Inputs (sheet `Calculator`, blue text on yellow)

| Cell(s) | Input | Notes |
|---|---|---|
| B4 | Mode | `Basic` or `Advanced` |
| B5 | Budget basis | `Count` (fixed number of transactions) or `Cost` (fixed expected review budget) |
| B6 | Planned sample size (Count) or expected review budget (Cost) | chosen elsewhere |
| B7 | Reference band | used only for column Q |
| B10:B13 | Band label / amount range | text |
| C10:C13 | Number of transactions in band | used for coverage columns |
| D10:D13 | Share of remaining recorded dollars, D_h | must sum to 100 percent (check in B8) |
| E10:E13 | Expected error occurrence, p_h | probability a transaction in the band is erroneous |
| F10:F13 | Expected RMS percentage error when erroneous | square root of s_h; Advanced mode only |
| G10:G13 | Expected review cost per transaction, c_h | relative units; Advanced mode with Cost basis only |

The example rows are hypothetical planning inputs matching Table 7 of the manuscript. They are not
measured data.

## Two budget bases

The cost term sqrt(1/c_h) is the solution of a fixed expected-**cost** problem (Supplemental Section
S1.1). With the number of transactions fixed instead, review cost does not change the
variance-minimizing allocation. The workbook therefore keeps the two problems apart:

- **Count basis.** B6 is a fixed number of transactions. c_h is set to 1 whatever is entered in
  column G, and the allocation is D_h sqrt(p_h s_h). Use this basis when review costs are equal.
- **Cost basis.** B6 is an expected review budget in the units of column G. The allocation is
  D_h sqrt(p_h s_h / c_h), and the continuous total expected count under each allocation is an
  output: budget / sum_h(share_h c_h) (B17 suggested, B18 MUS). Each band's count is then rounded
  **down**, so the expected review cost of the rounded allocation (B19, B20) cannot exceed the
  budget; B21 reports "Within budget" or "OVER BUDGET". The unspent remainder is less than one
  selection's cost per band and can be assigned by hand where it fits.

## Formulas

For band h with dollar share D_h, occurrence p_h, severity s_h = E[tau^2 | error, band h] (tau is
misstatement divided by recorded amount) and review cost c_h (1 under the Count basis):

    risk multiplier_h   = sqrt(p_h * s_h / c_h) / sqrt(p_ref * s_ref / c_ref)
    weight_h            = D_h * risk multiplier_h
    suggested share_h   = weight_h / sum over bands of weight
    MUS share_h         = D_h
    counts (Count)      = largest-remainder rounding of share_h * total, summing exactly to the total
    counts (Cost)       = floor(share_h * budget / sum_g share_g c_g), so that sum_h count_h c_h <= budget
    occurrence matching the reference band's risk multiplier (column Q)
                        = (p_ref * s_ref / c_ref) * c_h / s_h
    one-band occurrence at which band h's share equals its MUS share, other bands fixed (column R)
                        = (c_h / s_h) * [ sum over j != h of D_j sqrt(p_j s_j / c_j) / (1 - D_h) ]^2

The global MUS allocation is recovered only when all band multipliers sqrt(p_h s_h / c_h) are
equal. Column Q gives, band by band, the occurrence at which that band's multiplier would equal the
reference band's; MUS is the allocation only if every band meets its column-Q value at the same
time, so changing one band's occurrence to its column-Q value does not by itself make MUS
risk-aligned. Column R answers the one-band question: holding the others fixed, the occurrence at
which this band's own share equals its MUS share. The other bands' shares still differ from MUS
unless their multipliers also match. The reference band only rescales the multiplier and cancels in
the shares.

Mode rules: in `Basic` mode the workbook sets s_h = 1 and c_h = 1 for every band, so
suggested share_h is proportional to D_h sqrt(p_h). In `Advanced` mode s_h = (entered RMS %)^2, and
under the Cost basis c_h = entered cost; a blank or zero entry falls back to 1.

Sheet `Sensitivity` varies one band's occurrence rate by a set of multipliers while holding the other
bands at their `Calculator` values. With w_b the varied band's base weight and m the multiplier, its
new weight is w_b sqrt(m) and every share is recomputed over the new total. The row with multiplier
1.00 reproduces the `Calculator` sheet's shares; the varied band's count there is rounded on its own
and can differ by one from the largest-remainder count.

## Assumptions

1. **Risk-aligned allocation.** Inclusion probability proportional to RMS residual misstatement,
   sqrt(E[d^2 | a]), under equal review cost (manuscript Equation 2). With a fixed review budget, cost enters as a square root in
   the denominator (Supplemental Section S1.1).
2. **Within-band homogeneity.** The general band quantity is q_h = (1/A_h) sum_{i in h} m_i / a_i,
   the band's dollar-weighted mean squared taint, and share_h is proportional to D_h sqrt(q_h / c_h)
   with selection dollar-proportional within the band (Supplemental Section S1.6). Entering
   q_h = p_h s_h is the simplification that holds when occurrence and severity are homogeneous within
   the band; with heterogeneity inside a band, enter p_h and s_h so that their product is the band's
   dollar-weighted mean of occurrence times squared taint.
3. **MUS is the special case.** The global MUS allocation is recovered only when all band
   multipliers sqrt(p_h s_h / c_h) are equal; the suggested share then equals D_h in every band.
   `check_calculator.py` asserts this.
4. **Basic mode assumes equal severity and cost across bands.** State that assumption when the
   basic mode is used.
5. **Inputs are planning judgments unless measured.** Acceptable sources: prior audits of the same
   population, pilot or reference samples, re-performance, adjudicated historical results, or
   explicit planning assumptions subjected to the `Sensitivity` sheet. Label the source.
6. **Certainty items are removed first.** Individually material, high-consequence, and
   policy-required items are tested with certainty outside the workbook; D_h refers to what remains.
7. **Rounding.** Under the Count basis, counts are allocated by largest-remainder rounding and sum
   exactly to the planned total. Under the Cost basis, each band's count is rounded down, which
   guarantees that the rounded allocation's expected review cost does not exceed the budget; B21
   flags any violation.

## Verification

The workbook was recalculated with LibreOffice (157 formulas, zero errors) in both budget bases, and
`check_calculator.py` (173 checks) reproduces every multiplier, share, count, column-Q and column-R
value, total, review cost, budget check, and sensitivity cell independently in Python, and asserts that
the Cost-basis allocation never exceeds the budget; it also confirms that at the column-R
occurrence the band's share equals its MUS share, and that equal multipliers reproduce MUS. The
example allocation (Count basis, 400 transactions) is 14.4 / 37.4 / 36.4 / 11.8 percent
(57 / 150 / 146 / 47 transactions) against MUS shares of 10 / 30 / 40 / 20 percent
(40 / 120 / 160 / 80). Column Q (reference band 2) is 0.75 / 1.50 / 3.75 / 11.25 percent; column R is
0.44 / 0.77 / 2.71 / 8.80 percent.
