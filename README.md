# Assumed, Not Measured: replication materials

[![DOI](https://zenodo.org/badge/1381611517.svg)](https://doi.org/10.5281/zenodo.22899156)

Replication materials for *Assumed, Not Measured: What Monetary-Unit Sampling Assumes About Where
Error Lives*. This repository contains the source adjudication of the Peat Marwick Mitchell (PMM)
audit-error tables, the practitioner allocation calculator, and the scripts that generate the
manuscript's PMM figure and the supplement's PMM tables. No proprietary or personal data are
included; the published source articles are identified by hash and are not redistributed.

## Layout

| Path | Contents |
|---|---|
| `pmm/PMM_COMPLETE_CONDITION_REVIEW.md` | Source review: whether the published PMM tables can test the complete proportionality condition (verdict, source map, band-level and audit-wide tests, practitioner statements). |
| `pmm/PMM_SOURCE_COMPATIBILITY.csv` | Every relevant table in Ramage et al. (1979), Johnson et al. (1981) and Neter et al. (1985): page, statistic, exact definition, universe, weighting, exclusions, compatibility. |
| `pmm/PMM_BAND_PROPORTIONALITY_TEST.csv` | Candidate band-level pairings and why each is not computable. |
| `pmm/PMM_COMPLETE_MOMENT_TEST.csv` | Audit-wide test, one row per audit: inputs, `rho_$`, required dollar-unit error rate `F/rho_$`, ceiling bounds, derived-R diagnostic, emission status. Supports manuscript Table 3 and Figure 6, supplement Tables S3.3 and S3.4. |
| `pmm/inputs/` | Cells transcribed from the source tables with page references; the supplement's Table S3.2 values. |
| `pmm/transcriptions/` | Independent, scan-verified transcriptions of Johnson et al. Tables 6, 7, 9, 12, Neter et al. Table 3 and Ramage et al. Appendix A, used as cross-checks; `source_manifest.json` gives the SHA256 of the source PDFs. |
| `pmm/compute.py`, `pmm/verify.py` | Computation and verification (518 assertions). |
| `calculator/` | `MUS_Risk_Aligned_Allocation_Calculator.xlsx`, its methodological note, the build script and an independent check (69 assertions). |
| `figures/` | Manuscript figures and `make_fig7.py`, which regenerates the required-rate figure from the CSV. |
| `tables/` | `make_supp_tables.py` and the generated LaTeX rows for supplement Tables S3.3 and S3.4. |

## Reproduce

```
python3 pmm/verify.py            # recomputes pmm/PMM_COMPLETE_MOMENT_TEST.csv and runs all checks
python3 tables/make_supp_tables.py
python3 figures/make_fig7.py     # needs matplotlib
python3 calculator/check_calculator.py   # after recalculating the workbook in Excel or LibreOffice
```

`calculator/build_calculator.py` rebuilds the workbook with openpyxl; it writes formulas only, so open
and recalculate the file (or run LibreOffice headless) before `check_calculator.py`.

## Not included here

The federal statistical-system estimates, the simulated-ledger allocation calculations, the
literature ledger and the manuscript sources belong to other parts of the reproducibility package and
are not in this repository.

## Citation

Archived on Zenodo. This version: https://doi.org/10.5281/zenodo.22899157. All versions: https://doi.org/10.5281/zenodo.22899156.
