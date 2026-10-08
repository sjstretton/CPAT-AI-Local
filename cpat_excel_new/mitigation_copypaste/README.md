# Mitigation module - copy-pasteable prototype

Replacement for the CPAT mitigation module whose formulas are **fully copy-pasteable**: one formula per block, valid across (years) and down (subsectors x fuels), and a whole scenario group can be copied to a new scenario. Goal: auditable equations that a model builder can extend by dragging.

Current version: `CPAT_Mitigation_CopyPaste_v0.2.xlsx` (price -> fuel use only). Earlier versions in `Old/`.

## Design (agreed)

| Dimension | Axis | Nest |
|---|---|---|
| Scenario | columns | outer: one group per scenario (base year 2022 in column L as in legacy, 2023-2035, one gap column) |
| Year | columns | inner |
| Variable block | rows | outer: Pre-tax price, Tax, Post-tax price, Fuel use, Totals |
| Subsector | rows | middle: the 16 CPAT energy-use subsectors |
| Fuel | rows | inner: coa nga gso die lpg ker oop bio (same set for every subsector) |

- **Data step separate from formulas.** Sheet `Inputs` has one row per fuel|subsector (the taxonomy of `Mitigation` columns B:C) with every lookup: mappings, elasticities expanded to fuel|subsector for the selected income group, base prices, base tax, EF, base-year fuel use. `Mitigation` reads it with one short INDEX/MATCH in the four parameter columns D:G (hidden by default) and in the base-year column. Calculation cells hold no lookups.
- **Parameters are global.** Scenarios differ only in their assumption rows (carbon price); parameters and the carbon price are not changed together.
- **Formulas:** 2023-2034 plain formulas; 2035 calls named LAMBDAs (`PRETAX`, `TAX`, `POSTTAX`, `FUELUSE`; orange) so they can be dragged back over the row.
- Fuel use follows CPAT documentation 3.3.3 (GDP, usage and efficiency price effects, autonomous efficiency with rebound), without the Covid factor and shadow prices. Prices: base pre-tax price plus growth (0 %), tax = base tax + carbon price x EF x coverage.
- Country lookups (`Settings!C4`): elasticities by income group and domestic prices cover all CPAT countries; base-year energy use, GDP growth and EFs are Egypt only so far.

## Files

| File | Role |
|---|---|
| `CPAT_Mitigation_CopyPaste_v0.2.xlsx` | Workbook (formulas only; recalculates on open) |
| `build_v0_2.py` | Builder (openpyxl; no Excel COM needed) |
| `extract_data_v0_1.py` | Writes `data/*.csv` from the legacy workbook, the price-module data and kernel v1.6 (needs `pyxlsb`) |
| `check_v0_2.py` | LibreOffice checks: errors only in the LAMBDA column, one R1C1 formula per block, LAMBDA encoding, LAMBDA expansion and drag-forward vs an independent Python recomputation, scenario-copy test, regression vs v0.1 |
| `check_report_v0.2.md` | Output of the last check run |
| `data/` | Extracted source data (non-proprietary) |
| `Old/` | v0.1 workbook, builder, check script and report |

Rebuild: `python extract_data_v0_1.py` (only if sources change), `python build_v0_2.py`, `python check_v0_2.py`.

## Add a scenario

Copy a whole group with its gap column (scenario 2 = `AA:AO`), paste at `AP`, rename it in row 5 and edit the carbon prices in row 7.

## Roadmap (buckets)

1. Goal and spec (done, 2026-10-08).
2. Skeleton with working equations, Egypt data: v0.1, revised to v0.2 after review - **awaiting review in Excel**.
3. Copy-paste stress test: add a fuel, a subsector and a scenario by dragging; fix what breaks.
4. Numerical check against legacy CPAT for Egypt.
5. Later: emissions, power, revenue/macro links, Python port.
