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
Egypt Final results/   Egypt final deliverables (all final v1.0: CBAM carve-out Table 2, tracked results text, methodology, caveats, kernel); md sources in Old/, earlier drafts in Old/Superseded/
egypt+mitigation/      Egypt working folder: same final deliverables at top level; supporting work and superseded versions in Old/
instructions/          Egypt task inventory (instructions-egypt.yaml) and context (context-egypt.md)
templates/             Master templates (MTInputs_template.xlsx)
_research/             Source literature: IPCC AR6 WGIII Ch11/Ch12, CBAM regulation and guidance, sector roadmaps (PDF + extracted text)
NORMS.md               Excel column, colour, input and versioning norms; task-completion process (section 6)
CAVEATS.md             Append-only log of completed tasks: task, inputs, outputs, caveats
TODO.md                Queued industry-kernel tasks (T1-T3) with full procedures and per-task conventions
SyncRepo.bat           Local sync helper
```

### Workflow
1. Replicate legacy CPAT modules as Excel prototypes in `cpat_excel_new/` (same columns/colours, validated against `cpat_excel_original/`).
2. Build Egypt-specific functionality in `egypt+mitigation/`, replicating/improving earlier Egypt work.
3. Port validated logic to `cpat_coded/`; codes stay identical across Excel and Python.
4. Log every finished task (below).

### When a task is done
Follow [`NORMS.md` section 6](NORMS.md#6-task-completion-caveats-log-and-bookkeeping). In short:
1. **Append an entry to [`CAVEATS.md`](CAVEATS.md)** (repo root, newest at the bottom, never edit earlier entries) recording the **task**, its **inputs**, its **outputs** and any **caveats** - placeholders, assumptions, known gaps, deferred decisions, explained regression differences. The entry template is at the top of that file.
2. For workbooks: add the version-log row in `Settings`/`ReadMe` and run the `Check`-sheet regression (NORMS section 5).
3. Update the task inventory (`instructions/instructions-egypt.yaml`, `instructions/context-egypt.md`, `egypt+mitigation/EgyptTaskReference.md`) and tick `TODO.md`.
4. Do not commit unless asked.

### Key documents
> **Egypt methodology (start here):** [`egypt+mitigation/EGYPT_Methodology_v1.3.docx`](egypt+mitigation/EGYPT_Methodology_v1.3.docx) (also `.docx`). This is the integrated method for the whole Egypt thread. Appendix A covers emission factors split four ways; Appendix B covers process-emission semi-elasticities.

| Document | Role |
|---|---|
| [`egypt+mitigation/EGYPT_Methodology_v1.3.docx`](egypt+mitigation/EGYPT_Methodology_v1.3.docx) | Integrated Egypt methodology: scenarios, scope, CPAT reading, CBAM block, parameters; App. A EFs, App. B semi-elasticities, App. C glossary |
| [`NORMS.md`](NORMS.md) | Norms for all Excel work (sections 1-5) and the task-completion process for all work (section 6) |
| [`CAVEATS.md`](CAVEATS.md) | Log of completed tasks - task, inputs, outputs, caveats. Read before building on earlier work |
| [`TODO.md`](TODO.md) | Queued kernel tasks T1-T3 and the conventions every kernel increment must follow |
| [`instructions/instructions-egypt.yaml`](instructions/instructions-egypt.yaml) | Egypt task inventory and status; `TASK-1` notes record each kernel version v0.3-v0.11 |
| [`instructions/context-egypt.md`](instructions/context-egypt.md) | Egypt background, key-files table, structural rules |
| [`egypt+mitigation/EgyptTaskReference.md`](egypt+mitigation/EgyptTaskReference.md) | Kernel gap list and Task A-M breakdown |
| [`egypt+mitigation/Old/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`](egypt+mitigation/Old/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md) | IPCC-based process semi-elasticities: drop-in values, procedure, caveats |
| [`egypt+mitigation/Old/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md`](egypt+mitigation/Old/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md) | Pseudocode of the existing ad hoc Egypt calculations |
| [`cpat_excel_new/distribution/README.md`](cpat_excel_new/distribution/README.md), [`LESSONS_LEARNED.md`](cpat_excel_new/distribution/LESSONS_LEARNED.md), [`REGENERATING_THE_DISTRIBUTIONAL_WORKBOOK.md`](cpat_excel_new/distribution/REGENERATING_THE_DISTRIBUTIONAL_WORKBOOK.md) | Distribution module spec/status, LAMBDA-workbook lessons, regeneration steps |
| `cpat_excel_original/CPAT 1.0pre_456_NoPropData.xlsb` | Legacy CPAT - ground truth. Read-only |

### `cpat_excel_original/`
The source workbook (`CPAT 1.0pre_456_NoPropData.xlsb`). Read-only reference; do not edit. Older documents refer to this folder as `original_cpat_excel/`.

### `cpat_excel_new/` - Excel-AI prototypes
- `distribution/` - Distribution module: `docs/` (pseudocode), `data_*` staged data exports, `scripts/` (conversion pipeline), `standalone/` (standalone Egypt workbook + builder; `Old/` holds earlier versions), plus README, lessons learned and regeneration notes
- `standalone_working_version/` - current working version of the industry kernel, `CPAT_Industry_Kernel_Egypt_v1.3.xlsx` (the final Egypt prototype; sheet `CarveOut_Table2` = final Table 2 in live formulas), with its builder `build_v1_0.py` (Excel COM; relabels v0.17); earlier versions, Stream-2 branch files and earlier builders (including `build_v0_17.py`) in `Old/`. See NORMS.md section 5
- `standalone_initial_prototypes/` - first-generation standalone workbooks (distribution v0.4, prices module v1.12, industry kernel v0.1/v0.1b LAMBDA, energy-kernel mock-up, South Africa inputs, mitigation-equations PoC)
- `tecp_and_validation/` - total effective carbon price data and price-elasticity references
- `old/` - archived data from an earlier conversion effort (`Coded_Conversion_Data/`)
- `readme.xlsx`

### `Egypt Final results/` and `egypt+mitigation/` - Egypt case
Both folders hold the same final deliverables at top level; **the final model is the kernel `CPAT_Industry_Kernel_Egypt_v1.3.xlsx`** (the ad hoc rebuild is supporting material only):
- `CPAT_Industry_Kernel_Egypt_v1.3.xlsx` - final kernel (identical to `cpat_excel_new/standalone_working_version/`); sheet `CarveOut_Table2` computes the final Table 2 line by line (live for the bundle in Settings!B10, plus a stored 6-bundle snapshot and check)
- **`EGYPT_Methodology_v1.3.docx` - main methodology document for the Egypt thread (start here); section 4.5 = CBAM block and obligations**
- `EGYPT_CarveOut_Table2_v1.3.docx` - **final Table 2**: original CPAT runs with only the CBAM block replaced; published vs final comparison
- `EgyptResultsInitial_UpdatedResults_v1.3_tracked.docx` - updated results text (tracked changes against the published text)
- `EGYPT_FinalCaveats_v1.3.docx` - key caveats on the final results
- `EGYPT_Table2_Final_CBAMcalc_v1.3.xlsx` - final Table 2 with live CBAM obligations (O) calculation
- `EGYPT_CBAM_ObligationNote_v1.3.docx` - note on how O is calculated
- In `Egypt Final results/`: CBAM workbook and note in `CBAM Guess - Needs Carolyn Input/`; kernel, CarveOut and caveats in `Other/`
- Markdown sources of these documents, `ResultsComparison_Table2_v0.3` and all superseded versions are in each folder's `Old/`
- `egypt+mitigation/EgyptTaskReference.md` - gap list and Task A-M breakdown (working tracker)

`Egypt Final results/Old/` holds superseded deliverables (kernels v0.15/v0.16, methodology v1.1, ad hoc rebuild v0.2/v0.3 and its methodology notes, a `CAVEATS.md` snapshot). `egypt+mitigation/Old/` holds all supporting and superseded work:
- `AdHocRebuild/` - ad hoc rebuild workbooks v0.1-v0.3, builders, verifiers, methodology notes, `md_to_docx.py`
- `EmissionFactors/` - Egypt CBAM emission factors (`EGY_CBAM_EF_v0.1.xlsx` + builder)
- `ProcessEmissions_CarbonPrice_Response/` - derivation of the process semi-elasticities
- `InitialResultsAndIssues/` - reference material, do not edit: ad hoc calculations, major issues, initial results, methodology notes, MACC audit trail
- `TASK-D_ProcessHalfElasticities_DropIn_v0.1/v0.2.md`, `TASK-2a_AdHocCalculations_Pseudocode_v0.1.md`, earlier methodology (v1.0, v1.1), results summary v1.0, kernel v0.1

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


