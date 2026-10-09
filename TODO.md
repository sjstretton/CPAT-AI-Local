# TODO - open work only

Status key: ☐ not started · ◐ in progress. Done work is logged in [`CAVEATS.md`](CAVEATS.md), not here. Current state: Egypt final set **v1.6** (kernel `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`, documents in `egypt/final/`, plain hand-over folder `egypt-final/`).

## 1. Checks on the final set (you)

- ☐ Open the new `.docx` files in Word (`egypt/final/`, `egypt-final/`): layout, tables, tracked changes. They were generated with pandoc / python-docx and never opened in Word.
- ☐ Get Carolyn's confirmation of the definition of Table 2 row O (CBAM-product intensity change, no deduction); then drop `_NeedsCarolynConfirmation` from the CBAM note file name.
- ◐ Citations in `egypt/supporting/OutputElasticity_Note_v0.2.md`: checked by search summaries (EC/CE Delft–Oeko pass-through, Ganapati et al., Colmer et al., cement elasticity range); GTAP values and the steel demand range remain single-source / not found. To finish, allow the publisher hosts in the environment's network settings (or check by hand).

## 2. Modelling

- ◐ **Full-coverage EG3 CPAT run** (you run CPAT; everything else is ready). Spec: `egypt/supporting/EG3_FullCoverage_RunSpec_v0.1.md` (settings, acceptance check κ ≈ 1, export, regeneration steps, statements to rewrite). Tools: `cpat_run_constants.py`, `make_carveout_v0_6.py` (preview), `build_v1_7.py` (kernel refresh). Indicative effect: 3A −20.0 → about −29 Mt, 3B −12.0 → −15, 3C −30.8 → −40.
- ☐ **Emission-factor VERIFY list** (`EGY_CBAM_EF_Methodology_v0.1.md` App. A.6; methodology App. A): ammonia GJ/t, nitric-acid N₂O abatement, Egyptalum PFC rates, kiln fuel mix, DRI gas use, EISCO BF closure. Values are not final until done.
- ☐ Optional, small: fp routing of the ammonia / DRI CCS response (about −0.3 Mt in 1A, 3A–3C); decide whether to build it. Block fuel-intensity channel and the 3B alignment of the kernel's own composition: recommended not to build (see `egypt/supporting/KernelIncrements_Spec_v0.1.md`); label the composition sheet "block-only 3B rebate; reference" at the next kernel rebuild.
- ☐ Fuel-CO₂ reconciliation (cement block fuel 19.05 Mt against CPAT sector 10.91 Mt in 2030; Egypt clinker fuel factor 0.314).
- ☐ Keep under review: β set (IPCC central), shadow price σ = 20 $/t, output elasticities (judgements, Low–Medium confidence), the 3C fund outlay bound (0.2 $bn) against the budget, and the text of `Manual inputs` F66:F68 (says steel pass-through about 0.5; the evidence note says 0.55–0.85).

## 3. Mitigation copy-paste prototype (`cpat_excel_new/mitigation_copypaste/`)

- ☐ Decide (mitigation): (1) price vintage / last historical price year: legacy cached run has no devaluation drop, and holding prices from 2022 cuts the gap to legacy from 45.6% to 17.3% (`legacy_comparison_v0_1.md`); (2) add legacy's 2023 calibration to emission estimates?; (3) ETS cap option (`ETS_Cap_Design_Options_v0_1.md`, recommended A). Then cap-based ETS price; CH4, N2O and local pollutants; power sector.
- ◐ Review CPAT-AI-Mitigation-MVP v1.01 in Excel (incl. MTOutputs and Charts) and the overview deck (presentation/) (no repair prompt, LAMBDA column 2035 calculates, hidden columns D:G, copy a scenario group); then bucket 3 (stress test: add a fuel, a subsector and a scenario by dragging) and bucket 4 (numerical check against legacy CPAT for Egypt). Open assumptions are in the `CAVEATS.md` entry of 2026-10-08.

## Conventions for every kernel task

See `NORMS.md` and `egypt/instructions/instructions-egypt.yaml`.

- Never edit a shipped workbook in place: copy the previous version to `Old/`, build the next with `build_v<n>.py` via Excel COM (Windows, normal shell; COM fails in sandboxed shells). Run builders from `cpat_excel_new/standalone_working_version/`.
- Every new input gets a code, a source and a confidence rating, coloured per the legend (TAN = assumption, REVIEW = needs review).
- Append a row to the `Settings` version log; do not extend the sheet list in `Settings` rows 17–25.
- Regression: results outside the intended change must be identical (max abs diff 0); builders abort without saving otherwise.
- Methodology and version notes are separate documents (`NORMS.md` section 7).
- Finish each task with a `CAVEATS.md` entry and the bookkeeping in `NORMS.md` section 6. Do not commit unless asked.
