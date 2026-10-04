"""Recalculate EGY_CBAM_EF_v0.1.xlsx in Excel, verify the Checks sheet, scan for formula errors and print Summary.

Run: python recalc_and_check.py   (Excel installed; closes the workbook afterwards, saved with cached values).
"""
import os
import sys

import win32com.client as win32

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v0.1"
PATH = os.path.join(HERE, "EGY_CBAM_EF_%s.xlsx" % VERSION)


def main():
    xl = win32.DispatchEx("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    wb = xl.Workbooks.Open(PATH)
    try:
        xl.CalculateFullRebuild()
        errors = []
        for k in range(1, wb.Worksheets.Count + 1):
            ws = wb.Worksheets(k)
            ur = ws.UsedRange
            vals = ur.Value
            if vals is None:
                continue
            if not isinstance(vals, tuple):
                vals = ((vals,),)
            for i, row in enumerate(vals):
                for j, v in enumerate(row):
                    if isinstance(v, int) and v < 0 and ws.Cells(ur.Row + i, ur.Column + j).HasFormula \
                            and ws.Cells(ur.Row + i, ur.Column + j).Text.startswith("#"):
                        errors.append((ws.Name, ws.Cells(ur.Row + i, ur.Column + j).Address, ws.Cells(ur.Row + i, ur.Column + j).Text))
        print("formula errors:", len(errors))
        for e in errors[:40]:
            print("  ", e)

        ws = wb.Worksheets("Checks")
        r = 5
        fails = 0
        while ws.Cells(r, 2).Value not in (None, ""):
            res = ws.Cells(r, 4).Text
            print("check %2d %-8s %-14s %s" % (r - 4, res, ws.Cells(r, 3).Text, ws.Cells(r, 2).Value))
            fails += res == "FAIL"
            r += 1
        print("overall:", ws.Cells(r + 1, 4).Text)

        ws = wb.Worksheets("Summary")
        print("\n%-28s %8s %8s %8s %8s %9s %9s" % ("Product", "fc", "fp", "np", "no", "own", "chain"))
        r = 5
        while ws.Cells(r, 1).Value not in (None, ""):
            vals = [ws.Cells(r, c).Value for c in range(4, 10)]
            print("%-28s " % ws.Cells(r, 1).Value + " ".join("%8.3f" % v for v in vals[:4]) + " %9.3f %9.3f" % tuple(vals[4:]))
            r += 1
        print(ws.Cells(r + 1, 3).Text)
        print("cement memo:", ws.Cells(r + 2, 3).Text, ws.Cells(r + 2, 4).Text)

        ws = wb.Worksheets("Products")
        print("\n%-28s %9s %9s %9s %9s" % ("Product", "own", "kernel", "diff", "own/EUdef"))
        for r in range(5, 13):
            print("%-28s %9.3f %9.3f %9.3f %9s" % (ws.Cells(r, 1).Value, ws.Cells(r, 8).Value,
                                                   sum(ws.Cells(r, c).Value for c in range(15, 19)),
                                                   ws.Cells(r, 21).Value, ws.Cells(r, 23).Text))
        wb.Save()
        return 1 if (errors or fails) else 0
    finally:
        wb.Close(SaveChanges=False)
        xl.Quit()


if __name__ == "__main__":
    sys.exit(main())
