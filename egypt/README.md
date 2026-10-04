# egypt/ - Egypt CBAM / industry work

Single root for everything Egypt. Repo-wide rules: [`../AGENTS.md`](../AGENTS.md), [`../NORMS.md`](../NORMS.md). Log every finished task in [`../CAVEATS.md`](../CAVEATS.md).

| Folder | Contents |
|---|---|
| `final/` | Current deliverables, all **v1.6**: kernel `CPAT_Industry_Kernel_Egypt_v1.6.xlsx` (the final model and the one workbook that confirms the final numbers, identical to the copy in `cpat_excel_new/standalone_working_version/`; produced by `build_v1_6.py`; the file in `final/` is v1.5 until it has been run), `EGYPT_Methodology_v1.6.docx` (start here; current method only), `EGYPT_VersionNotes_v1.6.docx` (change history, always separate from the methodology), `EGYPT_CarveOut_Table2_v1.6.docx` (final Table 2), results text, final caveats, and the CBAM obligation note (`_NeedsCarolynConfirmation`: still a guess). `md_sources/` holds Markdown sources |
| `supporting/` | `AdHocRebuild/` (rebuild workbooks, builders, verifiers), `EmissionFactors/`, `ProcessEmissions_CarbonPrice_Response/`, `InitialResultsAndIssues/` (reference, do not edit), TASK-D and TASK-2a specs |
| `archive/` | Superseded versions of the deliverables (kernels v0.1-v1.0 and v1.3, earlier methodology/caveats/Table 2/results text, the retired CBAM-calculation workbook, superseded rebuild files in `AdHocRebuild/`) |
| `instructions/` | `instructions-egypt.yaml` (task inventory and status), `context-egypt.md` (background, key files, structural rules), `EgyptTaskReference.md` (gap list, Task A-M) |

Conventions: never edit a shipped version in place; new versions go in `final/` and the previous one moves to `archive/`. Prototype kernel increments are built in `cpat_excel_new/standalone_working_version/` and copied to `final/` on release.
