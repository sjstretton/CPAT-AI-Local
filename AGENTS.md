# AGENTS.md - instructions for any AI working in this repo

Tool-neutral entry point (Claude, Codex, Gemini, Copilot, Cursor, ...). `CLAUDE.md` just points here. This file only routes you to the existing documentation; the rules live there, so do not duplicate them here.

## What this repo is
Local workspace for the World Bank **Climate Policy Assessment Tool (CPAT)**: the legacy Excel model, Excel-AI prototypes replicating its modules, a Python reimplementation, and the Egypt CBAM / industry work. Layout and key documents: [`README.md`](README.md).

## Read before you start
1. [`README.md`](README.md) - repo map, workflow, key documents.
2. [`NORMS.md`](NORMS.md) - Excel column/colour/input/versioning norms (sections 1-5) and the task-completion process (section 6).
3. [`CAVEATS.md`](CAVEATS.md) - log of completed tasks and their caveats. Read before building on earlier work.
4. [`TODO.md`](TODO.md) - queued kernel tasks and per-task conventions.
5. Egypt work: [`egypt/instructions/context-egypt.md`](egypt/instructions/context-egypt.md) and [`egypt/instructions/instructions-egypt.yaml`](egypt/instructions/instructions-egypt.yaml).

## Hard rules (summary; authority is the documents above)
- `cpat_excel_original/` (legacy workbook) is read-only ground truth.
- Never edit a shipped workbook/spec version in place; copy the old one to `Old/` and create the next version (NORMS section 5).
- Every finished task ends with a new entry appended to `CAVEATS.md` (newest at the bottom, never edit earlier entries), plus the bookkeeping in NORMS section 6.
- Final methodology and version notes are always different documents (NORMS section 7). A methodology describes the current method only: no change history, no version log, no before/after columns. Change history goes in version notes, the workbook version log and `CAVEATS.md`.
- Do not commit unless the user asks.
- Excel builders run via Excel COM (`win32com`, Windows). On Linux/cloud sessions you can read and edit text/Markdown/Python but cannot rebuild or recalculate workbooks; say so rather than guessing.

## Keeping this file useful
Add new generic, tool-agnostic guidance to the documents above (or here, if it is routing only). Tool-specific files (`CLAUDE.md` etc.) must stay thin pointers to this file.
