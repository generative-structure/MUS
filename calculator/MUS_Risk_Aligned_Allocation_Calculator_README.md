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
| B5 | Total planned probabilistic sample size | transactions, chosen elsewhere |
| B6 | Reference band | used only for column Q |
| B10:B13 | Band label / amount range | text |
| C10:C13 | Number of transactions in band | used for coverage columns |
| D10:D13 | Share of remaining recorded dollars, D_h | must sum to 100 percent (check in B7) |
| E10:E13 | Expected error occurrence, p_h | probability a transaction in the band is erroneous |
| F10:F13 | Expected RMS percentage error when erroneous | square root of s_h; Advanced mode only |
| G10:G13 | Expected review cost per transaction, c_h | optional, relative units; Advanced mode only |

The example rows are hypothetical planning inputs matching Table 7 of the manuscript. They are not
measured data.

## Formulas

For band h with dollar share D_h, occurrence p_h, severity s_h = E[tau^2 | error, band h] (tau is
misstatement divided by recorded amount) and review cost c_h:

    risk multiplier_h   = sqrt(p_h * s_h / c_h) / sqrt(p_ref * s_ref / c_ref)
    weight_h            = D_h * risk multiplier_h
    suggested share_h   = weight_h / sum over bands of weight
    MUS share_h         = D_h
    suggested count_h   = round(suggested share_h * planned sample size)
    MUS count_h         = round(MUS share_h * planned sample size)
    p_h that justifies MUS = (p_ref * s_ref / c_ref) * c_h / s_h

The reference band only rescales the multiplier and cancels in the shares; it matters only for the
last line, which reports the occurrence rate at which band h's product p_h s_h / c_h would equal the
reference band's.

Mode rules: in `Basic` mode the workbook sets s_h = 1 and c_h = 1 for every band, so
suggested share_h is proportional to D_h sqrt(p_h). In `Advanced` mode s_h = (entered RMS %)^2 and
c_h = entered cost; a blank or zero entry falls back to 1.

Sheet `Sensitivity` varies one band's occurrence rate by a set of multipliers while holding the other
bands at their `Calculator` values. With w_b the varied band's base weight and m the multiplier, its
new weight is w_b sqrt(m) and every share is recomputed over the new total. The row with multiplier
1.00 reproduces the `Calculator` sheet.

## Assumptions

1. **Risk-aligned allocation.** Inclusion probability proportional to RMS residual misstatement,
   sqrt(E[d^2 | a]), under equal review cost (manuscript Equation 2). Cost enters as a square root in
   the denominator (Supplemental Section S1.1).
2. **Within-band homogeneity.** p_h, s_h and c_h are treated as constant within a band, so that
   E[d^2 | a] = a^2 p_h s_h for an item of amount a in band h and selection within the band stays
   dollar-proportional (Supplemental Section S1.6).
3. **MUS is the special case.** If p_h s_h / c_h is the same in every band, the multiplier cancels
   and the suggested share equals D_h, the monetary-unit sampling allocation. `check_calculator.py`
   asserts this.
4. **Basic mode assumes equal severity and cost across bands.** State that assumption when the
   basic mode is used.
5. **Inputs are planning judgments unless measured.** Acceptable sources: prior audits of the same
   population, pilot or reference samples, re-performance, adjudicated historical results, or
   explicit planning assumptions subjected to the `Sensitivity` sheet. Label the source.
6. **Certainty items are removed first.** Individually material, high-consequence, and
   policy-required items are tested with certainty outside the workbook; D_h refers to what remains.
7. **Rounding.** Counts are rounded to whole transactions; the rounded total may differ from the
   planned size by one or two.

## Verification

The workbook was recalculated with LibreOffice (117 formulas, zero errors) and
`check_calculator.py` reproduces every multiplier, share, count, justifying-occurrence value, and
sensitivity cell independently in Python, and confirms the reduction to MUS when p_h s_h / c_h is
constant. The example allocation is 14.4 / 37.4 / 36.4 / 11.8 percent (58 / 150 / 146 / 47
transactions of 400) against MUS shares of 10 / 30 / 40 / 20 percent (40 / 120 / 160 / 80).
