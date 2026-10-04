# Context: Egypt CBAM / industry work

Companion to `instructions-egypt.yaml` (task codes TASK-0, TASK-1, TASK-2a, TASK-2b).

## Background
- Egypt-specific analysis of CBAM (EU Carbon Border Adjustment Mechanism) exposure for industry.
- Earlier Egypt results were produced partly **off-CPAT** in an ad hoc spreadsheet with substantial errors. These need redoing.
- In parallel, CPAT (Climate Policy Assessment Tool) is being re-built as an **AI-coded prototype**. The first scope is only the **CBAM-related industrial modules** (CPAT_industry).

## Key files and folders (repo root: `CPAT-ai-local`)
| Item | Path | Role |
|---|---|---|
| Legacy CPAT (reference, read-only) | `cpat_excel_original/CPAT 1.0pre_456_NoPropData.xlsb` | Ground truth for column/row structure. Older documents call this folder `original_cpat_excel/`. |
| CBAM block in legacy CPAT | rows **12198–12353** of the above | CBAM calculations to replicate |
| Ad hoc calculations (flawed) | `egypt/supporting/InitialResultsAndIssues/AdHocCalculations.xlsb` | Off-CPAT calculations producing current final results |
| Issues list | `egypt/supporting/InitialResultsAndIssues/MajorIssues.docx` | Describes problems with the ad hoc calculations |
| Initial results | `egypt/supporting/InitialResultsAndIssues/EgyptResultsInitial.docx` | Results produced so far |
| Methodology note | `egypt/supporting/InitialResultsAndIssues/TechnicalNoteonCPATResults_expanded_v2.docx` | Method description |
| Existing kernel | `egypt/archive/CPAT_Industry_Kernel_Egypt_v0.1.xlsx` | Early Egypt industry kernel (superseded; all superseded versions are in `egypt/archive/`) |
| Prototype (CBAM block response) | `cpat_excel_new/standalone_working_version/CPAT_Industry_Kernel_Egypt_v1.6.xlsx` | Final CPAT_industry prototype; sheet `CarveOut_Table2` = final Table 2 in live formulas; identical copy in `egypt/final/`. Builder `build_v1_0.py` (relabels v0.17; `build_v0_17.py` in `Old/`); older versions and builders in `Old/` |
| Final deliverables | `egypt/final/` | Final deliverables, all v1.6: **CarveOut_Table2 (final Table 2: original CPAT runs, CBAM block replaced; O = CBAM-product embedded-intensity change)**, UpdatedResults tracked, Methodology, FinalCaveats, kernel. The CBAM obligation note carries `_NeedsCarolynConfirmation` in its filename (guess pending Carolyn); the former CBAM-calc workbook is retired into `Table2_Final` in the kernel. Methodology and version notes are always separate documents (NORMS section 7). Markdown sources of the caveats, Table 2 and CBAM note in `egypt/final/md_sources/`; earlier versions in `egypt/archive/`; builders in `egypt/supporting/AdHocRebuild/` |
| Egypt folder | `egypt/` | Single Egypt root: `final/` (deliverables), `supporting/` (ad hoc rebuild, emission factors, process-emissions derivation, task specs), `archive/` (superseded versions), `instructions/` (this file, the yaml inventory and `EgyptTaskReference.md`). See `egypt/README.md` |
| **Integrated methodology (main document)** | `egypt/final/EGYPT_Methodology_v1.6.docx` (edited Word master; no Markdown source) | Whole-thread method: scenarios, scope, CPAT reading, CBAM block, parameters; App. A four-way EFs, App. B process semi-elasticities, App. C glossary |
| Emission factors (Task EF) | `egypt/supporting/EmissionFactors/EGY_CBAM_EF_Methodology_v0.1.md` + `EGY_CBAM_EF_v0.1.xlsx` | Egypt fc/fp/np/no EFs for the 8 CBAM goods; builder `build_ef_v0_1.py`, verifier `recalc_and_check.py`; applied in kernel v0.15 (T5); the VERIFY list is still open, so the values are not final |
| Process half-elasticities (Task D) | `egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` | Paste-ready IPCC-based values + steps; applied in kernel v0.15 (`'Manual inputs'` rows 53–60 / `E50`; legacy v0.8: `E40:F47`); derivation in `egypt/supporting/ProcessEmissions_CarbonPrice_Response/` |
| Ad hoc pseudocode (TASK-2a) | `egypt/supporting/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md` | What `AdHocCalculations.xlsb` does as-is, mapped to MajorIssues |
| Ad hoc rebuild (TASK-2b) | `egypt/supporting/AdHocRebuild/AdHocCalculations_Rebuild_v0.5.xlsx` + `MethodologyNote_v0.5.md/.docx` | Live rebuild of Table 2 in the original PolicyMatrix format; Inputs tab, Mode switch REBUILD/PROTOTYPE (v0.11 reproduced exactly), Comparison, Issues resolved, Checks. Defaults `Conv` = FULL, `ThetaOther` = 1. Builder `build_adhoc_rebuild_v0_5.py`, verifier `recalc_and_check_adhoc_v0_5.py`; change history in `VersionNotes_AdHocRebuild.md`; v0.1–v0.2 in `egypt/archive/AdHocRebuild/` |
| Queued kernel tasks | `TODO.md` (repo root) | T1, T2, T5 done; T3 (CBAM market data into `Manual inputs`, kernel v1.4) done; T4 follow-ups open |
| Instructions | `egypt/instructions/` | This file, `instructions-egypt.yaml` and `EgyptTaskReference.md` |
| Repo conventions | `NORMS.md`, `README.md` | Follow these |

## Structural rules (TASK-1)
- **Columns**: must match the legacy CPAT workbook exactly.
- **Rows**: number of rows per process/block must match exactly; absolute row numbers need not.
- Additions: process emissions and other CBAM-relevant industrial items from the main CPAT.

## Ad hoc calculations (TASK-2a / TASK-2b)
- The CPAT CBAM block is not fully used; final results rely on extra ad hoc calculations.
- TASK-2a: pseudocode describing the **existing** ad hoc calculations, mapped to issues in `MajorIssues.docx` (v0.1 written).
- TASK-2b (done, v0.5): rebuilt workbook `egypt/supporting/AdHocRebuild/` — same PolicyMatrix layout, assumptions on `Inputs`, `Mode` = REBUILD (coherent method, default) or PROTOTYPE (= kernel v0.11 block), 19 MajorIssues items mapped on `Issues resolved`, 19 Checks. Open flags: κ(EG3) = 0.54 → re-run EG3 with full industry coverage; β set / σ judgements. Defaults: O on FULL, `ThetaOther` = 1 (3B rebate to all covered industry).
- Results comparison (`AdHocRebuild/ResultsComparison_Table2_v0.5.md/.docx`): Table 2 of `EgyptResultsInitial.docx` vs rebuild v0.5 vs the prototype kernel's own composition (2030). Not the final Table 2, which is the CBAM carve-out (`egypt/final/EGYPT_CarveOut_Table2_v1.3.docx`).

## Sequencing
- TASK-0, TASK-1, TASK-2a, TASK-2b (rebuild v0.5) are done; kernel final v1.6 (final Table 2 = carve-out sheet `CarveOut_Table2`). T1, T2, T5 done; T3 done (v1.4); kernel v1.5 holds the single confirmation workbook (sheet `Table2_Final`).
