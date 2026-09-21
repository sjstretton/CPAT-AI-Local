# Standalone Distribution module (Egypt)

`CPAT_Distribution_Standalone_Egypt.xlsx` is a standalone rebuild of the household
distributional/incidence module from `cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb`
(sheet "Distribution"), scoped to Egypt only. See the workbook's own **ReadMe** tab for
scope, structure and verification notes.

## Pipeline

```
extract_egypt.py   reads the source .xlsb (pyxlsb) + cpat_excel/Distribution/data_tabular,
                    filters everything to Egypt, and writes egypt_data.pkl

build_workbook.py   reads egypt_data.pkl and writes
                    CPAT_Distribution_Standalone_Egypt.xlsx (data tabs, Distribution_Inputs,
                    the LAMBDA library in the Name Manager, Distribution_Outputs, ReadMe)

reference_calc.py   a pure-Python re-implementation of the same LAMBDA logic, used to
                    validate the design against the source workbook's cached Egypt values
                    before it was encoded as Excel formulas. Not part of the shipped
                    workbook; kept for anyone who wants to re-verify or extend the model.
```

Re-run with:

```
python3 extract_egypt.py     # needs cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb
python3 build_workbook.py    # needs egypt_data.pkl
```

`egypt_data.pkl` is checked in so `build_workbook.py` can be re-run (e.g. to tweak
formatting or add sections) without re-reading the large source `.xlsb`.
