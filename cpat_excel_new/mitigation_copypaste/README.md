# Mitigation module - copy-pasteable prototype

Replacement for the CPAT mitigation module whose formulas are **fully copy-pasteable**: one formula per block, valid across (years) and down (subsectors x fuels), and a whole scenario group can be copied to a new scenario. Goal: auditable equations that a model builder can extend by dragging.

Current version: `CPAT_Mitigation_CopyPaste_v0.1.xlsx` (price -> fuel use only).

## Design (agreed)

| Dimension | Axis | Nest |
|---|---|---|
| Scenario | columns | outer: one 15-column group per scenario (label, base year 2022, 2023-2035) |
| Year | columns | inner |
| Variable block | rows | outer: Pre-tax price, Tax, Post-tax price, Fuel use, Totals |
| Subsector | rows | middle: the 16 CPAT energy-use subsectors |
| Fuel | rows | inner: coa nga gso die lpg ker oop bio (same set for every subsector) |

- Macro rows (scenario number, year, scenario name, real GDP growth, carbon price) sit at the top of each group.
- Each block has its own parameters on the left: 4 parameter sets (one per scenario) x 5 slots (P5 = buffer). Set 1 holds the lookups; sets 2-4 link to set 1 and can be overwritten. Formulas pick the set with `INDEX(row, (scenario number - 1) x 5 + slot)`.
- Fuel use follows CPAT documentation 3.3.3 (GDP, usage and efficiency price effects, autonomous efficiency with rebound), without the Covid factor and shadow prices. Prices: base pre-tax price plus growth (0 %), tax = base tax + carbon price x EF x coverage.
- Country lookups (`Settings!C4`): elasticities by income group and domestic prices cover all CPAT countries; base-year energy use, GDP growth and EFs are Egypt only so far.

## Files

| File | Role |
|---|---|
| `CPAT_Mitigation_CopyPaste_v0.1.xlsx` | Workbook (formulas only; recalculates on open) |
| `build_v0_1.py` | Builder (openpyxl; no Excel COM needed) |
| `extract_data_v0_1.py` | Writes `data/*.csv` from the legacy workbook, the price-module data and kernel v1.6 (needs `pyxlsb`) |
| `check_v0_1.py` | Recalculates with LibreOffice and checks: no errors, one R1C1 formula per block, scenario-copy test, independent Python recomputation, sanity |
| `check_report_v0.1.md` | Output of the last check run |
| `data/` | Extracted source data (non-proprietary) |

Rebuild: `python extract_data_v0_1.py` (only if sources change), `python build_v0_1.py`, `python check_v0_1.py`.

## Add a scenario

Copy a whole group (e.g. columns `AZ:BN`), paste it at the next group position (`BO`), type the new scenario number in the group's label cell (row 4), edit the carbon prices (row 8). Optionally overwrite parameter set N on the left. Up to 4 scenarios fit without inserting columns.

## Roadmap (buckets)

1. Goal and spec (done in conversation, 2026-10-08).
2. v0.1 skeleton with working equations, Egypt data (this version) - **awaiting review**.
3. Copy-paste stress test: add a fuel, a subsector and a scenario by dragging; fix what breaks.
4. Numerical check against legacy CPAT for Egypt (needs the same simplifications switched off or matched).
5. Later: emissions, power, revenue/macro links, LAMBDA/array variants, Python port.
