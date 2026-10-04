# CPAT-AI Excel Norms

Norms for all Excel-based development (prototypes replicating the legacy CPAT model, and the Egypt-specific extensions). Derived from `cpat_excel_original\CPAT 1.0pre_456_NoPropData.xlsb` (older documents call this folder `cpat_excel_original\`) and the existing standalone workbooks. **Draft v0.3 - iterate** (v0.3: added Key documents and section 6). Colours verified against legacy cell fills (Excel COM read of `Mitigation` and `MTInputs`).

Sections 1-5 govern Excel work. **Section 6 (task completion: caveats log and bookkeeping) applies to every task in the repo** - Excel, Python, data and documentation alike.

## Key documents

Read these before starting a task; keep them current when you finish one (section 6).

| Document | Role |
|---|---|
| [`README.md`](README.md) | Repo map, workflow, getting started |
| `NORMS.md` (this file) | Column, colour, input and versioning norms (1-5); task-completion process (6) |
| [`CAVEATS.md`](CAVEATS.md) | **Append-only log of completed tasks**: task, inputs, outputs, caveats. Every finished task adds an entry |
| [`TODO.md`](TODO.md) | Queued kernel tasks (T1-T3) with full procedures, and the per-task conventions (builders, codes, version log, regression, bookkeeping) |
| [`egypt\instructions\instructions-egypt.yaml`](egypt/instructions/instructions-egypt.yaml) | Machine-readable Egypt task inventory: TASK-0/1/2a/2b/D/QUEUE, status, and per-version `notes` for kernel increments v0.3-v0.15 (Tasks E, A, B, C, K, D-scaffold, H, L; F, I, J merged in v0.12; G in v0.13; M in v0.14; T1 Task D values + T5 EFs in v0.15) |
| [`egypt\instructions\context-egypt.md`](egypt/instructions/context-egypt.md) | Egypt background, key-files table, structural rules, sequencing |
| [`egypt\final\EGYPT_Methodology_v1.3.docx`](egypt/final/EGYPT_Methodology_v1.3.docx) (edited Word master) | **Integrated Egypt methodology** (main document); App. A emission factors, App. B process semi-elasticities. Update it when a task changes the method |
| [`egypt\instructions\EgyptTaskReference.md`](egypt/instructions/EgyptTaskReference.md) | Kernel gap list (items 1-5) and the Task A-M breakdown with dependencies |
| [`egypt\supporting\TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`](egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md) | Drop-in spec for IPCC-based process semi-elasticities; section 4 caveats; derivation in `egypt\supporting\ProcessEmissions_CarbonPrice_Response\` |
| [`egypt\supporting\TASK-2a_AdHocCalculations_Pseudocode_v0.1.md`](egypt/supporting/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md) | Pseudocode of the existing (flawed) ad hoc Egypt calculations, mapped to `InitialResultsAndIssues\MajorIssues.docx` |
| `cpat_excel_original\CPAT 1.0pre_456_NoPropData.xlsb` | Legacy CPAT - the reference for columns, rows, colours and values. Read-only |
| [`templates\MTInputs_template.xlsx`](templates/MTInputs_template.xlsx) | Master `MTInputs` template (section 4). Copy, never edit |
| `cpat_excel_new\standalone_working_version\` | Current industry kernel (`CPAT_Industry_Kernel_Egypt_v1.3.xlsx`, final Egypt prototype) and its `build_v0_<n>.py` builders; earlier versions in `Old\` (section 5) |
| [`cpat_excel_new\distribution\README.md`](cpat_excel_new/distribution/README.md), [`LESSONS_LEARNED.md`](cpat_excel_new/distribution/LESSONS_LEARNED.md), [`REGENERATING_THE_DISTRIBUTIONAL_WORKBOOK.md`](cpat_excel_new/distribution/REGENERATING_THE_DISTRIBUTIONAL_WORKBOOK.md) | Distribution module: spec/status and known gaps vs Excel; rules for LAMBDA/VBA workbooks; how to regenerate the distributional workbook |

## 1. Column norms

Match the legacy CPAT column positions exactly so formulas, lookups and Python mappings port 1:1.

### 1.1 Mitigation-layout calculation sheets (e.g. `Mitigation`, kernels)
Matches legacy `Mitigation` exactly. Row 1 = column headers; row 2 = title band; sections start row 3.

| Col | Header |
|---|---|
| A | (section no.) |
| B | Fuel |
| C | Sector |
| D | Description |
| E | Unit |
| F | Source |
| G | Input Code |
| H | Output Code |
| I | Note |
| J | Helper |
| K..AI | Years **2021..2045** (K=2021, L=2022 base year) |

Reference implementation: `cpat_excel_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v0.2.xlsx`.

### 1.1b Distribution-layout sheets (e.g. `Distribution`)
Content starts in column B; column A holds section numbering (`A.`, `A.I.`).

| Col | Header | Notes |
|---|---|---|
| A | (section no.) | e.g. `A.`, `A.I.` |
| B | Checks | row-level check flag |
| C | Country Name | |
| D | Country Code | ISO3 |
| E | Statistic | |
| F | Sample | |
| G | Scenario | |
| H | Item | |
| I | Description | |
| J | Unit | |
| K | Source | |
| L | Input Code 1 | |
| M | Input Code 2 | |
| N | Output Code | |
| O | Sigma, Note | |

Time-series blocks follow to the right of the descriptor columns.

### 1.2 Time-series data sheets (e.g. `Power`)
- Columns A-E: descriptors (section / methodology / unit / data level / source in the documentation header block; `Data section`, `Methodology` in C, `Unit` in K, `Data level` in N, `Data source` in P).
- Year headers start in **column F = 2000**, one column per year thereafter (F=2000, G=2001, ...).

### 1.3 Country-year data sheets (e.g. `Prices_dom`, `EnergyCons`)
- Row-banded header: `Fuels:` / `Sectors:` / `Indicators:` / `Units:` in column A (rows 4-7), then code row.
- Key columns: `country_year` (A, e.g. `EGY2021`), `countrycode_weo` (B), `countrycode` (C), `countryname` (D), `year` (E); data from F.
- Variable codes follow `mit.<indicator>.<fuel>.<sector>` (e.g. `mit.sp.coa.pow`).
- Sector codes: `pow, ind, res, rod, ral, avi, nav, foo, srv, mch, ...`; fuel codes: `coa, gas, gso, die, lpg, ker, ele, bio, oop`.

### 1.4 Sheet order and naming
Follow the legacy tab order: `Cover`, `Data sources`, `Dashboard`, `Manual inputs`, `MODULES->` (`Mitigation`, `Air pollution`, `Distribution`, `Transport`), then `DATA_*->` dividers followed by data tabs. Prototype workbooks keep the same sheet names as the legacy tab they replicate. Each workbook has a `ReadMe` first tab.

## 2. Colour norms

CPAT greens are the primary palette. Values below are the actual legacy fills.

| Use | Hex | Notes |
|---|---|---|
| Module title band (row 2) | `00B050` fill, white bold text | legacy `Mitigation`/`MTInputs` row 1-2 |
| Section band | `92D050` fill | full width A..last year column |
| Input cells / data-table headers | `EBF1DE` (light green) | user-editable values; header rows of data tabs |
| Code cells (Input/Output Code) | `DCE6F1` (light blue) | |
| Base-year column / derived switches | `DDD9C4` (tan) | e.g. column L (2022) |
| Unused / inactive parameters | `F2F2F2` (light grey) | legacy MTInputs grey |
| Calculation cells | no fill | |
| Results / notes to review | `FFF2CC` (light yellow) | e.g. check summaries |

Rules: inputs green only; never hard-code values in unfilled calculation cells; keep the legacy font (Arial; title 14pt bold) on legacy-replicating sheets.

## 3. Other conventions
- Formulas live in Excel; no macros in prototypes unless documented (build via Python scripts, see `cpat_excel_new\...\build_workbook.py`).
- Every prototype records: source legacy sheet, version, and a validation table vs. legacy values (and vs. `cpat_coded` where available).
- Codes (`Input Code`, `Output Code`) must be identical between Excel and Python (`cpat_coded\cpat_model\mappings`).
- Egypt-specific additions go in `egypt\` and are flagged `EGY` in the `Scenario`/`Statistic` columns; do not alter the replicated legacy logic.

## 4. Policy and parameter input norms (MTInputs)

All new models take their policy and parameter inputs from a dedicated input tab/file built on the legacy `MTInputs` structure. Master reference: [`templates\MTInputs_template.xlsx`](templates/MTInputs_template.xlsx) (single tab named `MTInputs`, generated from the legacy workbook; save a copy, never edit the master).

- **Exact row structure.** Every model's input sheet reproduces the legacy `MTInputs` rows exactly, in the same order, **including blank rows and section-heading rows**. Never insert, delete or reorder rows; row numbers must match the legacy tab so references and Python mappings port 1:1.
- **Colouring.** Parameters actually used by the module: green fill (`EBF1DE`) on B:H. All other parameters: light grey (`F2F2F2`) on B:H. Section-heading rows are bold, unfilled. Rows 1-3 carry the title (`00B050`) and section (`92D050`) bands.
- **Columns** (column structure of the legacy tab need not be replicated). Required, in this order:

| Col | Header |
|---|---|
| B | Parameters (parameter name) |
| C | unit |
| D | MT values - **placeholder, hidden** |
| E | "Dashboard" values - **placeholder, hidden** |
| F | Used for calculation |
| G | Defaults |
| H | NameOfParameter |

  Columns D and E carry the header text but are hidden and empty (for now). Other legacy columns (e.g. I, "Use Dashboard even if Defaults selected") are dropped. Column A may hold the legacy `X` flag.
- **Linking.** Module calculations reference the `Used for calculation` column (F) only; defaults feed it until Dashboard/MT columns are activated.
- **Lookup by name.** Read parameters with `INDEX(MTInputs!$F$8:$F$415, MATCH("<NameOfParameter>", MTInputs!$H$8:$H$415, 0))`, not by row reference.
- **Names.** `NameOfParameter` values are the shared codes used by `cpat_coded`.

## 5. Versioning and working versions

- **File names** end in `_v<major>.<minor>` (e.g. `CPAT_Industry_Kernel_Egypt_v0.2.xlsx`). Never overwrite a saved version: every saved change increments the version (minor for fixes/conformance/small features, major for structural or methodological change).
- **Old versions** move into an `Old\` subfolder next to the current file. The folder root holds only the current working version (plus its builder scripts/docs).
- **Working versions** of standalone prototypes live in `cpat_excel_new\standalone_working_version\`; source/experimental drafts (e.g. in `egypt\supporting\`) stay where they are until promoted.
- **Version log.** Each workbook keeps a version log (first/ReadMe or Settings tab): version, date, one-line description of changes.
- **Regression test on every increment.** Recalculate old and new versions in Excel and diff all values (baseline plus input shifts); differences must be zero or explained in the version log. Check sheets must stay at ~0 vs legacy CPAT.

## 6. Task completion: caveats log and bookkeeping

Applies to **every** task (Excel, Python, data, documentation). A task is not finished until it is logged. When a task is done:

1. **Append an entry to [`CAVEATS.md`](CAVEATS.md) (repo root).** This is the single, append-only record of completed work. Use the template at the top of that file and record:
   - **Task** - what was asked and what was done, with the task id (e.g. `TASK-D`, `T1`, `v0.12`);
   - **Inputs** - files, sheets/ranges, data sources, specs and prior versions used;
   - **Outputs** - files created or changed (paths), version numbers, documents updated;
   - **Caveats** - placeholders, assumptions, known gaps, deferred items, regression differences that were explained rather than zero, decisions still open; anything the next person must know before building on the result.

   Newest entry at the bottom. Never edit or delete earlier entries; to resolve a caveat, add a new entry that says so. Keep entries short and point to the task spec, report or yaml notes for detail.
2. **Workbook version log** (section 5). Add the version-log row (version, date, one-line description, max abs regression diff) in the workbook's `Settings`/`ReadMe` tab. The `CAVEATS.md` entry and the version-log row must agree.
3. **Task inventory.** Update the task's `status` and `notes` in [`egypt\instructions\instructions-egypt.yaml`](egypt/instructions/instructions-egypt.yaml); update the key-files table in [`egypt\instructions\context-egypt.md`](egypt/instructions/context-egypt.md) when paths or the latest version change; tick the item (✅/◐) in [`egypt\instructions\EgyptTaskReference.md`](egypt/instructions/EgyptTaskReference.md).
4. **Queue.** Tick the item in [`TODO.md`](TODO.md). Follow-up work the task generated goes in as a new `TODO.md` item, not only as a caveat.
5. **Specs.** When a task applies a versioned spec (e.g. `TASK-D_..._v0.1.md`), retarget it as a new version rather than editing it in place (same rule as section 5 for workbooks).
6. **No commit unless asked.** Leave changes in the working tree; the user decides what to commit.

`CAVEATS.md` summarises and points; detail stays where it is produced - the task spec (e.g. TASK-D section 4), the yaml `notes`, the workbook version log, and `cpat_excel_new\distribution\LESSONS_LEARNED.md` for the LAMBDA/VBA workbook. The per-task conventions in `TODO.md` (builders via Excel COM, codes/source/confidence for every new input, `Settings` version-log row, `Check`-sheet regression) remain in force and are the operational version of sections 3-5 for the industry kernel.

