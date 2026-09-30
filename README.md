# CPAT-AI-Local

Local workspace for the **Climate Policy Assessment Tool (CPAT)** — a World
Bank model for assessing the fiscal, economic, energy and distributional
impacts of carbon pricing and related climate policy reforms. This repo
contains both the original Excel-based model and an in-progress Python
reimplementation, plus supporting data-conversion tooling.

## Repository layout

```
├── cpat_coded/      Python reimplementation of the CPAT model
├── cpat_excel/       Original Excel model, data exports and conversion scripts
└── old/              Archived/legacy data from earlier conversion attempts
```

### `cpat_coded/` — Python model

A component-based reimplementation of the CPAT model, driven by
`run_model.py` and configured via `config.py` (selected countries, scenarios,
data path).

- `cpat_model/` — the model itself
  - `components/` — one subpackage per model component: `gdp`, `policies`,
    `carbon_pricing`, `efs` (emission factors), `elasticities`, `prices`,
    `energy_consumption`, `emissions`, `power`, and `distribution` (the
    household distributional/incidence analysis module)
  - `inputs/` — dashboard, distribution and input-data loaders
  - `mappings/`, `constants.py` — shared lookups and coded constants
  - `scenario_results.py` — bundles a finished scenario's outputs so later
    scenarios (and the Distribution module) can compare against a baseline
- `cpat_data/` — Egypt (EGY), Middle East & North Africa (MEA) and global
  input data (`new_data/` CSVs, `new_data_pkl/` pickles)
- `cpat_testing/` — pytest suite (`model/` mirrors the `cpat_model/`
  component structure)
- `cpat_documentation/developer/` — developer-facing documentation
- `environment.yml` / `requirements.txt` — Conda/pip dependencies
  (Python 3.11, pandas, numpy, openpyxl, pyxlsb, pytest)

The Distribution module is the most complete component so far: all 14 steps
of its pseudocode spec are implemented and running end-to-end against real
Egypt data. See `cpat_excel/distribution/README.md` for its design spec,
current status and known accuracy gaps versus the Excel model.

### `cpat_excel/` — Original Excel model & conversion pipeline

- `original/` — the source Excel workbook,
  `CPAT 1.0pre_456_NoPropData.xlsb`
- `distribution/` — design docs, standalone-module plans and staged data
  exports (`data_bymodule`, `data_bymodule_regenerated`, `data_standardized`,
  `data_tabular`, `data_tabular_regenerated`) for the Distribution module
- `standalone-final/` — standalone Excel workbooks split out of the main
  model (`CPAT_Distribution_Standalone_Egypt_v0.4.xlsx`,
  `CPAT_PricesModule_v1.12.xlsx`)
- `scripts/` — data-conversion tooling: `build_from_source.py`,
  `tabular_from_standardized.py`, `bymodule_from_tabular.py`,
  `build_distribution_model_data.py`, `build_readme.py`, `run_all.py`,
  `common.py`

### `old/`

Archived data from an earlier conversion effort
(`Coded_Conversion_Data/`), kept for reference.

## Getting started

```powershell
# Create the Conda environment
conda env create -f cpat_coded\environment.yml
conda activate cpat_sisepuede

# Or install with pip
pip install -r cpat_coded\requirements.txt

# Run the model
cd cpat_coded
python run_model.py
```

Run the test suite with:

```powershell
cd cpat_coded
pytest
```
