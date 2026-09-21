# CPAT Distribution Module

Root folder for the household distributional (incidence) analysis module of CPAT —
the model that estimates how a carbon-pricing policy scenario affects household
consumption by income decile, and how revenue recycling offsets that effect.

This module currently exists only inside the main Excel model
(`cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb`, sheet `Distribution`) and
its supporting data tables (`cpat_excel/Distribution/data_*`). The goal of this
folder is to hold the two planned reimplementations of that sheet:

- `python/` (not yet started) — a component under `cpat_coded/cpat_model/components/distribution`
  reimplementing the module in Python, alongside the rest of the CPAT model.
- `excel/` (not yet started) — a standalone Excel workbook that replicates just the
  Distribution module, independent of the full CPAT model.

## Current contents

- `docs/CPAT_Distribution_Module_Pseudocode.docx` — the design specification:
  Inputs, Algorithm (14 steps) and Outputs pseudocode for the module, derived
  directly from the live Excel sheet's structure, row labels and embedded notes.
  This is the reference both future implementations should be built from.

## Status

Pseudocode / design stage only. No Python or Excel implementation exists yet in
this folder — see the document above for the plan.
