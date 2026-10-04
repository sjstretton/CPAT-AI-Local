# TODO - open work only

Status key: ☐ not started · ◐ in progress. Done work is logged in [`CAVEATS.md`](CAVEATS.md), not here. Current state: Egypt final set **v1.6** (kernel `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`, documents in `egypt/final/`, plain hand-over folder `egypt-final/`).

## 1. Checks on the final set (you)

- ☐ Open the new `.docx` files in Word (`egypt/final/`, `egypt-final/`): layout, tables, tracked changes. They were generated with pandoc / python-docx and never opened in Word.
- ☐ Get Carolyn's confirmation of the definition of Table 2 row O (CBAM-product intensity change, no deduction); then drop `_NeedsCarolynConfirmation` from the CBAM note file name.
- ☐ Check the citations in `egypt/supporting/OutputElasticity_Note_v0.1.md` against the papers (they came from search summaries; the papers could not be opened).

## 2. Modelling

- ☐ **True full-coverage EG3 CPAT run** (the run prices only κ = 0.54 of industrial energy CO₂; the final Table 2 uses EG3 as run, 3A–3C are lower bounds). After the run: replace `CPAT_Outputs` (`cpat_outputs_egypt_2022_2041.csv`), set `Inputs!KappaMode = ONE` in the rebuild, rebuild, rerun the kernel carve-out and regenerate the documents.
- ☐ **Emission-factor VERIFY list** (`EGY_CBAM_EF_Methodology_v0.1.md` App. A.6; methodology App. A): ammonia GJ/t, nitric-acid N₂O abatement, Egyptalum PFC rates, kiln fuel mix, DRI gas use, EISCO BF closure. Values are not final until done.
- ☐ **Route the ammonia / urea CCS β to fp** (App. B.5): ammonia and urea process response is 0 today, which understates fertiliser response.
- ☐ **Block fuel-intensity channel in the kernel** (the prototype holds block fuel intensity fixed; the final Table 2 takes CPAT's response instead).
- ☐ **Fuel-CO₂ reconciliation** (cement block fuel 19.05 Mt against CPAT sector 10.91 Mt in 2030; Egypt clinker fuel factor 0.314).
- ☐ **Align the kernel's own composition** (`Table2_Industry`, `Rebate_Industry`) with the 3B decision (rebate to all covered industry); today it rebates the CBAM block only and is reference material.
- ☐ Keep under review: β set (IPCC central), shadow price σ = 20 $/t, output elasticities (judgements, Low–Medium confidence), and the 3C fund outlay bound (0.2 $bn) against the budget.

## Conventions for every kernel task

See `NORMS.md` and `egypt/instructions/instructions-egypt.yaml`.

- Never edit a shipped workbook in place: copy the previous version to `Old/`, build the next with `build_v<n>.py` via Excel COM (Windows, normal shell; COM fails in sandboxed shells). Run builders from `cpat_excel_new/standalone_working_version/`.
- Every new input gets a code, a source and a confidence rating, coloured per the legend (TAN = assumption, REVIEW = needs review).
- Append a row to the `Settings` version log; do not extend the sheet list in `Settings` rows 17–25.
- Regression: results outside the intended change must be identical (max abs diff 0); builders abort without saving otherwise.
- Methodology and version notes are separate documents (`NORMS.md` section 7).
- Finish each task with a `CAVEATS.md` entry and the bookkeeping in `NORMS.md` section 6. Do not commit unless asked.
