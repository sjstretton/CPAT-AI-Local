# Standalone Distribution module (Egypt)

`CPAT_Distribution_Standalone_Egypt_vN.N.xlsx` (top-level = latest confirmed-working
version; `Old/` = earlier snapshots) is a standalone rebuild of the household
distributional/incidence module from `cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb`
(sheet "Distribution"), scoped to Egypt only. See the workbook's own **ReadMe** tab for
scope, structure and verification notes, and its **Tests** tab (cell C5) for a live
pass/fail check after running the macro.

## Pipeline

```
extract_egypt.py   reads the source .xlsb (pyxlsb) + cpat_excel/Distribution/data_tabular,
                    filters everything to Egypt, and writes egypt_data.pkl

build_workbook.py   reads egypt_data.pkl and writes:
                      - CPAT_Distribution_Standalone_Egypt.xlsx (data tabs, Distribution_
                        Inputs, Distribution_Outputs, ReadMe -- all labels/structure/
                        styling, but with formula cells and the LAMBDA library left BLANK)
                      - RebuildDistributionModule.bas (a VBA macro that adds the LAMBDA
                        names and writes every formula cell via Excel's own object model)

reference_calc.py   a pure-Python re-implementation of the same LAMBDA logic, used to
                    validate the design against the source workbook's cached Egypt values
                    before it was encoded as Excel formulas. Not part of the shipped
                    workbook; kept for anyone who wants to re-verify or extend the model.
```

### Why the .bas file

Excel's .xlsx format requires every "future function" (LAMBDA, LET, XLOOKUP, HSTACK,
SCAN, MAKEARRAY -- anything added after the OOXML spec froze) to be written internally
with an `_xlfn.` prefix, and every LAMBDA/LET parameter name to carry an `_xlpm.` prefix,
in both its declaration and every reference to it. Getting this byte-for-byte right by
hand-writing XML (via openpyxl) proved unreliable across Excel versions/builds -- Excel
would silently strip the offending names/formulas and show a "needs repair" prompt.
Shipping the workbook with everything left blank, plus a macro that recreates the LAMBDA
names and formulas through Excel's own `Names.Add` / `Range.Formula2` API, sidesteps the
encoding problem entirely: Excel does its own internal encoding, guaranteed correct.

To use: open the .xlsx, Alt+F11, Insert > Module, paste in `RebuildDistributionModule.bas`,
then run `RebuildDistributionModule` (F5). It defines all 39 named LAMBDA functions plus
the plain named ranges, then writes all ~1,460 formula cells across Distribution_Inputs,
Distribution_Outputs and Tests, then forces a full recalculation.

### Automated testing (less manual re-checking after a formula change)

Two layers, both run automatically as part of `build_workbook.py` (no extra step needed):

1. **Build-time static checks** -- every LAMBDA formula is scanned for the two array-
   broadcasting bug *shapes* that caused real, hard-to-diagnose failures during manual
   testing: `INDEX(range, 0, X)` where `X` can be array-valued (only well-defined when the
   *other* index is scalar -- this produced ELASTADJ/ASPIRE_PC's `#VALUE!`), and
   `MIN`/`MAX` called with an array-valued argument (Excel's MIN/MAX reduce *all* arguments
   to one value instead of broadcasting element-wise -- this produced PIT_REDUCTION's
   `#VALUE!`). The build raises `AssertionError` and names the offending LAMBDA/call if
   either shape reappears, instead of waiting to be found by hand in Excel again. Same
   collision check as before also still runs (defined names vs. Excel Table names, which
   share one case-insensitive namespace -- the ELASTADJ/"ElastAdj" bug).
2. **Tests sheet** (in the workbook itself, populated by the same macro as everything
   else) -- ~20 checks, each calling a LAMBDA with the *full* `DECILE_ARRAY` (the exact
   call pattern that triggered both bugs above; a scalar-decile smoke test would not have
   caught either) and comparing the live Excel result against `reference_calc.py`'s
   independently-computed value, plus 3 checks of the live Gini cells. Open the workbook,
   run the macro, read cell `Tests!C5` -- `"ALL 20 TESTS PASS"` or a failure count pointing
   at exactly which block to look at, instead of typing test formulas into blank cells by
   hand after every change.

Re-run with:

```
python3 extract_egypt.py     # needs cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb
python3 build_workbook.py    # needs egypt_data.pkl
```

`egypt_data.pkl` is checked in so `build_workbook.py` can be re-run (e.g. to tweak
formatting or add sections) without re-reading the large source `.xlsb`.
