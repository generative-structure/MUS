# Assumed, Not Measured: replication materials

[![DOI](https://zenodo.org/badge/1381611517.svg)](https://doi.org/10.5281/zenodo.22899156)

Replication materials for *Assumed, Not Measured: What Monetary-Unit Sampling Assumes About Where
Error Lives*: the source adjudication of the Peat Marwick Mitchell (PMM) audit-error tables, the
allocation calculator, and the scripts that generate the manuscript's PMM, simulated-ledger and federal
displays and the Online Appendix tables. No proprietary or personal data are included; the published
source articles are identified by hash and are not redistributed.

## Layout

| Path | Contents |
|---|---|
| `pmm/inputs/` | Cells transcribed from the source tables with page references; Online Appendix Table S3.2 values. |
| `pmm/transcriptions/` | Independent, scan-verified transcriptions of Johnson et al. (1981) Tables 6, 7, 9, 12, Neter et al. (1985) Table 3 and Ramage et al. (1979) Appendix A; `source_manifest.json` gives the SHA256 of the source PDFs. |
| `pmm/compute.py`, `pmm/verify.py` | Computation of `pmm/PMM_COMPLETE_MOMENT_TEST.csv` and its verification (518 assertions). |
| `pmm/PMM_COMPLETE_MOMENT_TEST.csv` | One row per audit: inputs, `rho_$`, required dollar-unit error rate `F/rho_$` and its rounding interval, count-based exclusion sensitivity, derived-R diagnostic. Supports Table 3, Figure 6 and Online Appendix Tables S3.3 and S3.4. |
| `pmm/PMM_SOURCE_COMPATIBILITY.csv`, `pmm/PMM_BAND_PROPORTIONALITY_TEST.csv` | Source map (page, statistic, definition, universe, weighting, exclusions) and the band-level pairings, both read by `verify.py`. |
| `tables/make_supp_tables.py` | Generates `tables/S33_rows.tex` (including the break-even excluded share `1 - rho_hi/(F - 0.005)`) and `tables/S34_rows.tex`. |
| `figures/make_fig7.py` | Figure 6 (required dollar-unit error rate) from the moment-test CSV. |
| `figures/make_fig2.py` | Figure 2 and its ledger numbers (60,000-item simulated ledger, `default_rng(7)`). |
| `figures/make_federal_displays.py` | Figure 7, Table 4 values and `tables/S81_rows.tex` from the full-precision federal results. |
| `federal_checks/` | `nass_joint_check.py` and its output: NASS random-effects, Hartung-Knapp, and joint delete-one-state and delete-one-year intervals (Online Appendix S7.2). |
| `calculator/` | `MUS_Risk_Aligned_Allocation_Calculator.xlsx` (Count and Cost budget bases), its methodological note, the build script, and an independent check (173 assertions across both bases). |

## Reproduce

Run from the repository root:

```
python3 pmm/verify.py                   # runs all PMM checks
python3 tables/make_supp_tables.py
python3 figures/make_fig7.py            # needs matplotlib
python3 figures/make_fig2.py            # needs numpy, matplotlib
cd calculator && python3 build_calculator.py && cd ..   # writes formulas only; recalculate in Excel or LibreOffice
cd calculator && python3 check_calculator.py && cd ..   # optionally pass recalculated workbooks as arguments
```

`figures/make_federal_displays.py` and `federal_checks/nass_joint_check.py` read the outputs of the federal
estimation pipeline, which is not in this repository; set `FEDERAL_ERROR_SCALING` to their location. Their
outputs are committed (`tables/S81_rows.tex`, `federal_checks/nass_joint_check.json`).

## Citation

Archived on Zenodo: https://doi.org/10.5281/zenodo.22899156 (resolves to the latest version).
