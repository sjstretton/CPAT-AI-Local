# CPAT Distribution Module

Root folder for the household distributional (incidence) analysis module of CPAT —
the model that estimates how a carbon-pricing policy scenario affects household
consumption by income decile, and how revenue recycling offsets that effect.

This module currently exists in full only inside the main Excel model
(`cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb`, sheet `Distribution`) and
its supporting data tables (`cpat_excel/Distribution/data_*`). The goal of this
folder is to hold the two planned reimplementations of that sheet:

- Python — lives in `cpat_coded/cpat_model/components/distribution` (not under this
  folder, so it sits alongside every other component), wired into the rest of the
  model. **Plumbing is in place** (see below); the calculation steps themselves are
  not yet implemented.
- `excel/` (not yet started) — a standalone Excel workbook that replicates just the
  Distribution module, independent of the full CPAT model.

## Current contents

- `docs/CPAT_Distribution_Module_Pseudocode.docx` — the design specification:
  Inputs, Algorithm (14 steps) and Outputs pseudocode for the module, derived
  directly from the live Excel sheet's structure, row labels and embedded notes.
  This is the reference both implementations are built from.

## Python plumbing (cpat_coded)

What exists so far, ahead of implementing the actual 14 calculation steps:

- `cpat_model/components/distribution/distribution.py` — the `Distribution` class.
  `__init__` wires in `DistributionInputsDict`, `InputData`, and a baseline vs.
  policy `ScenarioResults` pair, and implements **Step 1** (direct fuel price
  changes + a first-pass carbon-pricing revenue figure) to prove the wiring
  works end to end. Steps 2-14 are stubbed (`_step2_...` .. `_step14_...`,
  each raising `NotImplementedError`), one method per pseudocode step, not yet
  called from `__init__`.
- `cpat_model/components/distribution/data.py` — loaders for the module's own
  data tables (IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios, and
  the GTAP↔CPAT↔ISIC sector crosswalk), following the same `DATA_PATH` CSV
  convention as every other component. **The xlsx → CSV export these loaders
  expect does not exist yet** — see `cpat_excel/Distribution/data_standardized/`
  for the source data and `cpat_excel/scripts/` for the existing extraction
  pipeline this needs to feed into.
- `cpat_model/inputs/distribution_inputs.py` — `DistributionInputsDict` +
  `DistributionInputs`, mirroring `DashboardInputs` but kept separate, since the
  Distribution sheet has its own independent input block in the Excel model.
- `cpat_model/scenario_results.py` — `ScenarioResults`, a new bundle type.
  Distribution needs *two* finished scenario runs (baseline and policy) to
  derive a price change, which nothing in the existing per-scenario loop in
  `run_model.py` previously captured; `run_model()` now stores one
  `ScenarioResults` per scenario and instantiates `Distribution` once per
  policy scenario, after the main year loop, comparing it to the baseline.
- `cpat_model/constants.py` — added the Distribution-specific fuel/category/
  decile/sample/statistic codes (flagged one naming collision: the Excel
  model's `hea` code is reused for both "heat" (Mitigation) and "health
  services" (Distribution); given distinct Python names, `HEA` and
  `HEALTH_SRV`, since they never appear in the same index dimension).
- `cpat_testing/model/components/distribution/test_distribution.py` — unit
  tests for the Step 1 logic, using synthetic data (no CSVs required), same
  style as the rest of `cpat_testing`.

## Status

Plumbing in place; algorithm (Steps 2-14) and the Excel-to-CSV data export not
yet implemented. See the pseudocode document above for the full spec.
