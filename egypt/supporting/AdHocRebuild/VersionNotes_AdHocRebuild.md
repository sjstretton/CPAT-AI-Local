# AdHoc rebuild (TASK-2b): version notes

Change history only. The method itself is in `MethodologyNote_v0.4.md` (current state, no history); numbers compared with the final Table 2 are in `ResultsComparison_Table2_v0.4.md`. Per `NORMS.md` section 7, history does not go in the methodology.

## v0.5 (builder and verifier drafted 2026-10-08, not run)

- Output elasticity by product (`EpsQ1`..`EpsQ8` on `Inputs`: cement -0.10, steel and fertilisers -0.40, aluminium -0.50), from `egypt/supporting/OutputElasticity_Note_v0.1.md`. `PROTOTYPE` mode keeps the uniform `EpsQ` = -0.5, so the reproduction of kernel v0.11 is unchanged. No other change.
- Files: `build_adhoc_rebuild_v0_5.py`, `recalc_and_check_adhoc_v0_5.py`. Results and notes (`MethodologyNote_v0.5`, `ResultsComparison_Table2_v0.5`) to be written after the verifier has run.

## v0.4 (2026-10-04)

- **Defaults changed, no formula changes.** `Conv` = FULL (was NOPHASE) and `ThetaOther` = 1 (was 0), following the decisions recorded in `CAVEATS.md` (2026-10-04). `ThetaOther` is forced to 0 in PROTOTYPE mode, so the reproduction of kernel v0.11 is unchanged.
- **Builder / verifier:** `build_adhoc_rebuild_v0_4.py`, `recalc_and_check_adhoc_v0_4.py`; report `recalc_and_check_adhoc_v0_4_report.txt` (ALL PASSED: PROTOTYPE 132/132 for FULL and NOPHASE; REBUILD 588/588 against the Python mirror).
- **Effect on 2030 results (v0.4 vs v0.3).** Only 3B moves. The convention switch only changes which of FULL / NOPHASE is the headline for O; the values of each are unchanged.

| 3B, 2030 | v0.3 (`ThetaOther` = 0) | v0.4 (`ThetaOther` = 1) |
|---|---:|---:|
| K, Mt | -19.63 | -12.31 |
| D_obr, Mt | +3.29 | +10.61 |
| Net revenue P, $bn | 1.13 | 0.20 |
| Rebates, $bn | 1.25 | 2.18 |
| Deaths avoided Q | 714 | 412 |
| T, % | -6.6 | -5.8 |
| Delta net revenue AR, $bn | 1.44 | 0.51 |

## v0.3

- IPCC process semi-elasticity anchor deflated to the model's price basis: `PStar` = 122 USD2024 (100 USD2019 x about 1.22; confidence Medium); beta = -ln(1-ER100)/122. `BetaSet` = PROTOTYPE keeps the /100 divisor.
- `KappaMode` = SCALE became the default: EG3 industry energy responses and CPAT fuel receipts are scaled by 1/kappa and coverage J is set at kappa = 1 (an approximation pending a CPAT re-run).
- Nothing else changed (Egypt EF v0.1, sigma = 20 $/t, `Conv` = NOPHASE, `ThetaOther` = 0 stayed).

2030 K effect of the v0.3 changes (Mt):

| Bundle | v0.2 K | Deflation only | SCALE only | v0.3 K | Total change |
|---|---:|---:|---:|---:|---:|
| 1A | -31.79 | -31.35 | -31.79 | -31.35 | +0.45 |
| 2A | -27.82 | -27.82 | -27.82 | -27.82 | 0.00 |
| 2B | -29.34 | -29.34 | -29.34 | -29.34 | 0.00 |
| 3A | -18.15 | -17.70 | -25.51 | -25.07 | -6.91 |
| 3B | -12.74 | -12.26 | -20.11 | -19.63 | -6.88 |
| 3C | -22.62 | -21.79 | -31.43 | -30.60 | -7.99 |

Other v0.3 versus v0.2 changes: J (3A-3C) 13.9 % to 20.8 %; P net (3A) 1.53 to 2.34 $bn; deaths (3A) 546 to 850; N (1A/3A) -6.56 % to -5.79 %.

## v0.2

- Emission factors fc / fp / np / no = Egypt CBAM EF v0.1 (`EmissionFactors/EGY_CBAM_EF_v0.1.xlsx`, Products D:G), selected by `EFSet` (EGY_EF_V01 default; PROTOTYPE = kernel v0.11 EFs, forced in PROTOTYPE mode).
- AN process ER100 = N2O-weighted blend of the TASK-D unabated and abated rows at the EF workbook's 50 % abatement share (central 0.6179). E_base 2030 = 62.42 Mt (61.16 Mt with the prototype EFs).
- The kernel adopted the same EFs and beta in kernel v0.15.

## v0.1

- First rebuild of the ad hoc PolicyMatrix: formula-driven, openpyxl build, Excel COM verified. `Mode` switch REBUILD / PROTOTYPE (reproduces kernel v0.11 exactly), 19 MajorIssues items mapped on `Issues resolved`, 19 Checks. Defaults `Conv` = NOPHASE, `ThetaOther` = 0, kernel EFs.
