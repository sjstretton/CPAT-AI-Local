"""Extract 2030 CBAM product data per scenario from kernel v1.0 (Mitigation_Industry policy block, CarveOut_Table2)."""
import json
import os
import win32com.client as w
K = r"C:\Users\wb547395\Repos\CPAT-ai-local\cpat_excel_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v1.0.xlsx"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kernel_products_2030.json")
xl = w.DispatchEx("Excel.Application"); xl.Visible = False; xl.DisplayAlerts = False
res = {}
try:
    wb = xl.Workbooks.Open(K, 0, True)
    s = wb.Worksheets("Settings"); sc = wb.Worksheets("Scenarios")
    names = [sc.Range("B%d" % r).Value for r in range(17, 24)]
    print(names)
    m = wb.Worksheets("Mitigation_Industry"); c = wb.Worksheets("CarveOut_Table2")
    print([(r, c.Range("B%d" % r).Value) for r in range(17, 63) if c.Range("B%d" % r).Value])
    for nm in names:
        if not nm or nm == "LEGACY":
            continue
        s.Range("B10").Value = nm
        xl.CalculateFull()
        code = c.Range("D6").Value
        t0 = 644; T = 20
        g = lambda n, col=T: m.Cells(t0 + n, col).Value
        prods = []
        for k in range(8):
            prods.append(dict(
                name=g(31 + k, 4), X=g(31 + k, 9), Q=g(31 + k, T), Q24=g(31 + k, 14), gr=g(31 + k, 7),
                F0=g(85 + k, 6), P0=g(85 + k, 7), fuel=g(85 + k), dfuel=g(107 + k), proc=g(96 + k), dproc=g(118 + k),
                rev=g(147 + k), f6=g(54 + k, 6), f5=g(54 + k, 5), p6=g(65 + k, 6), p5=g(65 + k, 5)))
        res[nm] = dict(code=code, tau=g(2), pp=g(63), obr=g(6), prods=prods,
                       co={r: c.Range("D%d" % r).Value for r in range(6, 77)})
        print(nm, code, res[nm]["co"].get(62), res[nm]["co"].get(51))
    wb.Close(False)
finally:
    xl.Quit()
json.dump(res, open(OUT, "w"), indent=1, default=str)
