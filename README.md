# CPAT-AI-Local

Local workspace for the **Climate Policy Assessment Tool (CPAT)** — a World
Bank model for assessing the fiscal, economic, energy and distributional
impacts of carbon pricing and related climate policy reforms. This repo
contains both the original Excel-based model and an in-progress Python
reimplementation, plus supporting data-conversion tooling.

## Repository layout

The repo serves two parallel purposes: **Coded CPAT** (Python) and **Excel-AI** (Excel-based prototypes built/maintained with AI assistance). All Excel work follows [`NORMS.md`](NORMS.md) (column, colour, input and versioning norms); **every task**, Excel or not, ends by logging task/inputs/outputs/caveats in [`CAVEATS.md`](CAVEATS.md) (see [When a task is done](#when-a-task-is-done)).

```
cpat_coded/            Coded CPAT: Python reimplementation of the model
cpat_excel_original/   Legacy CPAT workbook (CPAT 1.0pre_456_NoPropData.xlsb) - the reference (older docs: original_cpat_excel/)
cpat_excel_new/        Excel-AI: new Excel prototypes replicating legacy CPAT modules
egypt/                 Egypt case (single root): final/ deliverables, supporting/ work, archive/ superseded versions, instructions/ task inventory and context (see egypt/README.md)
egypt-final/           Simplified, version-free hand-over of the final Egypt results: 2-page summary, results table, methodology, and the two supporting Excel files
templates/             Master templates (MTInputs_template.xlsx)
_research/             Source literature: IPCC AR6 WGIII Ch11/Ch12, CBAM regulation and guidance, sector roadmaps (PDF + extracted text)
NORMS.md               Excel column, colour, input and versioning norms; task-completion process (section 6)
CAVEATS.md             Append-only log of completed tasks: task, inputs, outputs, caveats
TODO.md                Open work only (checks, modelling) and the per-task conventions
SyncRepo.bat           Local sync helper
```

### Workflow
1. Replicate legacy CPAT modules as Excel prototypes in `cpat_excel_new/` (same columns/colours, validated against `cpat_excel_original/`).
2. Build Egypt-specific functionality in `egypt/`, replicating/improving earlier Egypt work.
3. Port validated logic to `cpat_coded/`; codes stay identical across Excel and Python.
4. Log every finished task (below).

### When a task is done
Follow [`NORMS.md` section 6](NORMS.md#6-task-completion-caveats-log-and-bookkeeping). In short:
1. **Append an entry to [`CAVEATS.md`](CAVEATS.md)** (repo root, newest at the bottom, never edit earlier entries) recording the **task**, its **inputs**, its **outputs** and any **caveats** - placeholders, assumptions, known gaps, deferred decisions, explained regression differences. The entry template is at the top of that file.
2. For workbooks: add the version-log row in `Settings`/`ReadMe` and run the `Check`-sheet regression (NORMS section 5).
3. Update the task inventory (`egypt/instructions/instructions-egypt.yaml`, `egypt/instructions/context-egypt.md`, `egypt/instructions/EgyptTaskReference.md`) and tick `TODO.md`.
4. Do not commit unless asked.

### Key documents
> **Egypt methodology (start here):** [`egypt/final/EGYPT_Methodology_v1.6.docx`](egypt/final/EGYPT_Methodology_v1.6.docx) (edited Word master). This is the integrated method for the whole Egypt thread. Appendix A covers emission factors split four ways; Appendix B covers process-emission semi-elasticities.

| Document | Role |
|---|---|
| [`egypt/final/EGYPT_Methodology_v1.6.docx`](egypt/final/EGYPT_Methodology_v1.6.docx) | Integrated Egypt methodology: scenarios, scope, CPAT reading, CBAM block, parameters; App. A EFs, App. B semi-elasticities, App. C glossary |
| [`NORMS.md`](NORMS.md) | Norms for all Excel work (sections 1-5) and the task-completion process for all work (section 6) |
| [`CAVEATS.md`](CAVEATS.md) | Log of completed tasks - task, inputs, outputs, caveats. Read before building on earlier work |
| [`TODO.md`](TODO.md) | Open work and the conventions every kernel increment must follow |
| [`egypt/instructions/instructions-egypt.yaml`](egypt/instructions/instructions-egypt.yaml) | Egypt task inventory and status; `TASK-1` notes record each kernel version v0.3-v0.11 |
| [`egypt/instructions/context-egypt.md`](egypt/instructions/context-egypt.md) | Egypt background, key-files table, structural rules |
| [`egypt/instructions/EgyptTaskReference.md`](egypt/instructions/EgyptTaskReference.md) | Kernel gap list and Task A-M breakdown |
| [`egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`](egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md) | IPCC-based process semi-elasticities: drop-in values, procedure, caveats |
| [`egypt/supporting/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md`](egypt/supporting/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md) | Pseudocode of the existing ad hoc Egypt calculations |
| [`cpat_excel_new/distribution/README.md`](cpat_excel_new/distribution/README.md), [`LESSONS_LEARNED.md`](cpat_excel_new/distribution/LESSONS_LEARNED.md), [`REGENERATING_THE_DISTRIBUTIONAL_WORKBOOK.md`](cpat_excel_new/distribution/REGENERATING_THE_DISTRIBUTIONAL_WORKBOOK.md) | Distribution module spec/status, LAMBDA-workbook lessons, regeneration steps |
| [`cpat_excel_new/mitigation_copypaste/README.md`](cpat_excel_new/mitigation_copypaste/README.md) | CPAT-AI-Mitigation-MVP (copy-pasteable mitigation module): design, files, rebuild, how to add and batch-run scenarios; method notes `PriceProjection_Method_v0.4.md`, `ETS_Method_v0_1.md`, `Scenarios_Method_v0_1.md`, `PowerPrices_Method_v0_1.md`; Word documentation `CPAT-AI-Mitigation-MVP_Documentation_v1.05.docx`; decks in `presentation/` |
| `cpat_excel_original/CPAT 1.0pre_456_NoPropData.xlsb` | Legacy CPAT - ground truth. Read-only |

### `cpat_excel_original/`
The source workbook (`CPAT 1.0pre_456_NoPropData.xlsb`). Read-only reference; do not edit. Older documents refer to this folder as `cpat_excel_original/`.

### `cpat_excel_new/` - Excel-AI prototypes
- `distribution/` - Distribution module: `docs/` (pseudocode), `data_*` staged data exports, `scripts/` (conversion pipeline), `standalone/` (standalone Egypt workbook + builder; `Old/` holds earlier versions), plus README, lessons learned and regeneration notes
- `standalone_working_version/` - current working version of the industry kernel, `CPAT_Industry_Kernel_Egypt_v1.6.xlsx` (the final Egypt prototype; sheet `CarveOut_Table2` = final Table 2 in live formulas), with its builder `build_v1_0.py` (Excel COM; relabels v0.17); earlier versions, Stream-2 branch files and earlier builders (including `build_v0_17.py`) in `Old/`. See NORMS.md section 5
- `mitigation_copypaste/` - copy-pasteable mitigation module prototype (design 2: scenario groups across, block > subsector > fuel down); CPAT-AI-Mitigation-MVP v1.05 (renamed at v1.00; power generation costs and residential/industrial electricity prices in section 3, generation mix interim data until the engineer model (v1.05); first-run test macro CheckBatchRun for Excel (v1.04); multiple scenarios with a VBA batch run, StoredResults and ScenarioCompare (v1.03, .xlsm); cap-based new ETS with benchmarks, volatility adjustment and goal-seek script (v1.02); MTOutputs and Charts sheets; 7-slide overview deck and 4-slide advanced-features deck in presentation/; Word documentation `CPAT-AI-Mitigation-MVP_Documentation_v1.05.docx`) = Mitigation first tab (75%, rolled up, one-level column groups, spacer column between scenarios, two beiges), corrected Egypt price block, 2022-2040, revenues (existing taxes, existing subsidies, new policies), CO2 from fuel combustion, legacy CPAT section layout (policies, retail energy prices, sectors > subsectors > variables), domestic price projection in real USD of the results year (legacy method; other oil products and VAT rate by assumption, marked bright yellow), policy wedges (carbon tax, new ETS, fuel price reform), existing taxes and subsidies, feebates with sectoral shadow prices, LegacyDiff tab, on the efficiency margin, from MTInputs per scenario, price -> fuel use, Egypt base data; builder, data extraction and LibreOffice check script (see its README)
- `working_version/` - current hand-over copies of the mitigation MVP (workbook, Word documentation, decks); earlier copies in `Old/`
- `standalone_initial_prototypes/` - first-generation standalone workbooks (distribution v0.4, prices module v1.12, industry kernel v0.1/v0.1b LAMBDA, energy-kernel mock-up, South Africa inputs, mitigation-equations PoC)
- `tecp_and_validation/` - total effective carbon price data and price-elasticity references
- `old/` - archived data from an earlier conversion effort (`Coded_Conversion_Data/`)
- `readme.xlsx`

### `egypt/` - Egypt case
One folder holds all Egypt material (details in [`egypt/README.md`](egypt/README.md)); **the final model is the kernel `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`** (the ad hoc rebuild is supporting material only):
- `final/` - final deliverables, all v1.6:
  - `CPAT_Industry_Kernel_Egypt_v1.6.xlsx` - **the one workbook that confirms the final numbers** (identical to `cpat_excel_new/standalone_working_version/`); sheet `CarveOut_Table2` computes the final Table 2 line by line (live for the scenario in Settings!B10, plus a stored 6-scenario snapshot and check); sheet `Table2_Final` holds the six-scenario Table 2, the figures printed in the documents, their differences (zero) and a live recomputation of row O
  - **`EGYPT_Methodology_v1.6.docx` - main methodology document for the Egypt thread (start here)**; section 4.5 = CBAM block and obligations, 4.7 = composition of the final Table 2. Current method only, no change history. Edited Word master, no Markdown source
  - `EGYPT_VersionNotes_v1.6.docx` - change history of the final set and the kernel (kept out of the methodology, `NORMS.md` section 7)
  - `EGYPT_CarveOut_Table2_v1.6.docx` - **final Table 2**: original CPAT runs with only the CBAM block replaced; published vs final comparison
  - `EgyptResultsInitial_UpdatedResults_v1.6_tracked.docx` - updated results text (tracked changes against the published text)
  - `EGYPT_FinalCaveats_v1.6.docx` - key caveats on the final results
  - `EGYPT_CBAM_ObligationNote_v1.6_NeedsCarolynConfirmation.docx` - note on how row O is calculated; a guess pending Carolyn's confirmation
  - `md_sources/` - Markdown sources of the caveats, Table 2, version notes and CBAM note
- `supporting/` - supporting work: `AdHocRebuild/` (current rebuild workbook v0.5 and v0.3 with builders, verifiers, `MethodologyNote_v0.5`, `ResultsComparison_Table2_v0.5`, `VersionNotes_AdHocRebuild.md`, `md_to_docx.py`; v0.1-v0.2 and earlier notes are in `egypt/archive/AdHocRebuild/`), `EmissionFactors/` (Egypt CBAM EFs `EGY_CBAM_EF_v0.1.xlsx` + builder), `ProcessEmissions_CarbonPrice_Response/` (derivation of the process semi-elasticities), `InitialResultsAndIssues/` (reference material, do not edit), and the `TASK-D_...` / `TASK-2a_...` specs
- `archive/` - all superseded versions: kernels v0.1-v1.0 and v1.3, methodology v1.0-v1.3, the retired CBAM-calculation workbook, caveats, Table 2, results text, CBAM note, results summary, `CAVEATS.md` snapshots
- `instructions/` - `instructions-egypt.yaml` (task inventory), `context-egypt.md` (background, key files, structural rules) and `EgyptTaskReference.md` (gap list, Task A-M tracker)

### `cpat_coded/` - Python model

A component-based reimplementation of the CPAT model, driven by
`run_model.py` and configured via `config.py` (selected countries, scenarios,
data path).

- `cpat_model/` - the model: `components/` (`gdp`, `policies`, `carbon_pricing`, `efs`, `elasticities`, `prices`, `energy_consumption`, `emissions`, `power`, `distribution`), `inputs/`, `mappings/`, `constants.py`, `scenario_results.py`
- `cpat_data/` - Egypt (EGY), MENA and global input data
- `cpat_testing/` - pytest suite mirroring `cpat_model/`
- `cpat_documentation/developer/` - developer docs
- `environment.yml` / `requirements.txt` - dependencies (Python 3.11, pandas, numpy, openpyxl, pyxlsb, pytest)

The Distribution module is the most complete component; see `cpat_excel_new/distribution/README.md` for its spec, status and known gaps versus the Excel model.

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


