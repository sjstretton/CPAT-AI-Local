"""Build EGYPT_Table2_Final_CBAMcalc_v1.3.xlsx: final Table 2 (2030) with hard-coded results except CBAM
obligations (O), which are computed live by product from editable assumptions (EU price, CBAM phase-in, deduction).

Data: kernel_products_2030.json (extract_kernel_products_2030.py, kernel v1.3). Other rows: CBAM carve-out v1.3.
Run: python make_table2_cbam_xlsx.py   (writes with openpyxl, then recalculates and saves with Excel so values are cached)
"""
import json
import os
import shutil

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
NAME = "EGYPT_Table2_Final_CBAMcalc_v1.3.xlsx"
OUT = os.path.join(ROOT, "egypt", "final", "EGYPT_Table2_Final_CBAMcalc_v1.3_NeedsCarolynConfirmation.xlsx")
COPY = OUT  # single copy (no duplicate in a second folder)
D = json.load(open(os.path.join(HERE, "kernel_products_2030.json")))
SC = ["1A", "2A", "2B", "3A", "3B", "3C"]

# Hard-coded results: CBAM carve-out v1.3 (kernel v1.3 CarveOut_Table2 stored snapshot rows 80-85)
HARD = {
    "J": [63.209336136123014, 57.33511064434257, 57.33511064434257, 13.9156322940344, 13.9156322940344, 13.9156322940344],
    "P": [6.85949372503708, 6.2668866648981085, 6.229441806962326, 1.5352488618688684, 0.6425370663466966, 0.4060502367633877],
    "K": [-37.389792301353275, -33.077154647427115, -34.82765529925497, -22.76631822644433, -19.140348013204175, -33.0395634616242],
    "M": [100.0, 44.21268510362509, 44.21268510362509, 100.0, 100.0, 100.0],
    "N": [-5.772119167416468, -2.144387041601825, -2.259389839756931, -5.772119167416468, -5.798414912468852, -23.07173117522215],
    "Q": [1501.13411535165, 1456.3479307694702, 1517.1987207126515, 551.5895084820191, 490.67565048441554, 646.3092034690271],
}
PUBLISHED_O = [-26.1, -13.9, -13.9, -26.1, -7.6, -30.4]
DESC = {
    "1A": "Upstream carbon levy on all fossil fuels plus process emissions; revenue to general budget",
    "2A": "Upstream carbon levy on fossil fuels; revenue to households",
    "2B": "Upstream carbon levy on fossil fuels; revenue to green investment",
    "3A": "Downstream carbon price on heavy industry (fuel and process); revenue to households",
    "3B": "As 3A, with output-based free allocation (rebate) to industry",
    "3C": "As 3A, with an industrial abatement rebate (fund)",
}

INP = PatternFill("solid", fgColor="FFF2CC")
KEY = PatternFill("solid", fgColor="F8CBAD")
HEAD = PatternFill("solid", fgColor="D9E1F2")
CALC = PatternFill("solid", fgColor="E2EFDA")
BLUE = Font(color="0000CC", bold=True)
B = Font(bold=True)
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")


def hdr(ws, r, vals, c0=1):
    for j, v in enumerate(vals):
        x = ws.cell(r, c0 + j, v)
        x.font = B
        x.fill = HEAD
        x.border = BOX
        x.alignment = WRAP


def inp(cell, v, key=False, fmt=None):
    cell.value = v
    cell.fill = KEY if key else INP
    cell.font = BLUE
    cell.border = BOX
    if fmt:
        cell.number_format = fmt


def build():
    wb = Workbook()

    # ---------------- Table2 ----------------
    t = wb.active
    t.title = "Table2"
    t["A1"] = "Table 2. Simulated outcomes of carbon policy scenarios for Egypt, 2030 (USD 20/tCO2 in 2030 in all scenarios)"
    t["A1"].font = Font(bold=True, size=12)
    t["A2"] = ("All rows are hard-coded from the final CBAM carve-out (EGYPT_CarveOut_Table2_v1.3), except row O, which is "
               "computed live on sheet 'CBAM_calc' as the export-weighted change in the embedded emission intensity of CBAM "
               "products only. Change the yellow cells on 'Scenarios' and 'CBAM_data' to test alternatives.")
    t["A2"].alignment = WRAP
    t.merge_cells("A2:I2")
    t.row_dimensions[2].height = 45
    hdr(t, 4, ["Code", "Indicator", "Unit"] + SC + ["Source"])
    rows = [
        ("J", "Coverage of national GHG emissions", "%", "J"),
        ("P", "Carbon revenue", "USD bn", "P"),
        ("K", "Emission reduction vs baseline", "MtCO2e", "K"),
        ("M", "CBAM coverage (share of CBAM-sector embedded emissions priced)", "%", "M"),
        ("N", "CBAM-sector emission intensity change", "%", "N"),
        ("O", "CBAM obligations (change in embedded emissions per tonne exported to the EU)", "%", None),
        ("Q", "Premature deaths avoided (local air pollution)", "deaths", "Q"),
    ]
    for i, (code, lab, unit, key) in enumerate(rows):
        r = 5 + i
        t.cell(r, 1, code).font = B
        t.cell(r, 2, lab)
        t.cell(r, 3, unit)
        for j, s in enumerate(SC):
            c = t.cell(r, 4 + j)
            if key:
                c.value = HARD[key][j]
                c.number_format = "#,##0" if key == "Q" else "0.0"
                t.cell(r, 10, "Hard-coded: CBAM carve-out v1.3")
            else:
                c.value = "=CBAM_calc!%s5" % chr(ord("C") + j)
                c.number_format = "0.0"
                c.fill = CALC
                c.font = B
                t.cell(r, 10, "LIVE: CBAM_calc row 5 (CBAM-product intensity only)")
            c.border = BOX
    r = 13
    t.cell(r, 1, "Memo").font = B
    memo = [
        ("O-pub", "CBAM obligations, initial (published) Table 2", None),
    ]
    for i, (code, lab, f) in enumerate(memo):
        rr = r + 1 + i
        t.cell(rr, 1, code)
        t.cell(rr, 2, lab)
        t.cell(rr, 3, "%")
        for j in range(6):
            c = t.cell(rr, 4 + j)
            c.value = f % chr(ord("C") + j) if f else PUBLISHED_O[j]
            c.number_format = "0.0"
            c.border = BOX
    t.cell(18, 1, "Scenario definitions").font = B
    for i, s in enumerate(SC):
        t.cell(19 + i, 1, s)
        t.cell(19 + i, 2, DESC[s])
    t.column_dimensions["A"].width = 8
    t.column_dimensions["B"].width = 62
    t.column_dimensions["C"].width = 9
    for col in "DEFGHI":
        t.column_dimensions[col].width = 9
    t.column_dimensions["J"].width = 52
    t.freeze_panes = "D5"

    # ---------------- Assumptions ----------------
    a = wb.create_sheet("Assumptions")
    a["A1"] = "Assumptions. Table 2 row O uses only F1-F10 below (CBAM-product intensity). Inputs A1-A7 drive the memo rows 6-7 on CBAM_calc only."
    a["A1"].font = Font(bold=True, size=12)
    a["A2"] = "Orange = key contestable assumption; yellow = other input. All other cells are formulas or fixed data."
    hdr(a, 4, ["Ref", "Assumption", "Value", "Unit", "Basis / comment"])
    items = [
        ("A1", "EU allowance (CBAM certificate) price in 2030", 100, "USD/tCO2", True, "0",
         "Kept from the initial analysis (about EUR 90/t at 1.10 USD/EUR). Treated as a real 2030 price. "
         "Please replace with your preferred EU ETS outlook for 2030. A higher price lowers the share of the "
         "obligation offset by Egypt's USD 20 price."),
        ("A2", "CBAM convention used in Table 2 row O", "Full implementation", "", True, None,
         "'Full implementation': CBF = 1, as in the initial table (structural exposure once EU free allocation "
         "has ended, 2034 onwards). '2030 phase-in': CBF = value in A3; the 2030 obligation is then much smaller, "
         "so the same domestic payment offsets a larger share of it."),
        ("A3", "CBAM factor in 2030 (CBF, 2030 phase-in convention only)", 0.485, "share", False, "0.0%",
         "Share of embedded emissions charged in 2030 = 1 - EU ETS free allocation share. Regulation (EU) 2023/956 "
         "Art. 31; Directive 2003/87/EC Art. 10a(1a). Schedule below."),
        ("A4", "CBAM factor used (CBF)", '=IF(C6="Full implementation",1,C7)', "share", None, "0.0%", "Formula."),
        ("A5", "Scale the domestic-price deduction by CBF?", "No", "Yes/No", True, None,
         "'No': the carbon price effectively paid in Egypt is deducted in full (Art. 9). 'Yes': the deduction is "
         "reduced in line with the EU free allocation still given to EU producers. The EU implementing rules on this "
         "interaction are not final. With 'Yes', the result equals the full-implementation result."),
        ("A6", "Deduction scaling used (S)", '=IF(C9="Yes",C8,1)', "share", None, "0.000", "Formula."),
        ("A7", "Net the 3C industrial abatement rebate off the deductible price?", "No", "Yes/No", True, None,
         "'No' as in the initial table. Art. 9 deducts the price 'effectively paid', taking into account any "
         "rebate or compensation. Under 'Yes', the 3C fund (Scenarios!G) is allocated to products in proportion "
         "to the carbon payment and subtracted. The 3B output-based rebate is always netted."),
    ]
    for i, (ref, lab, v, unit, key, fmt, note) in enumerate(items):
        r = 5 + i
        a.cell(r, 1, ref)
        a.cell(r, 2, lab).alignment = WRAP
        c = a.cell(r, 3)
        if key is None:
            c.value = v
            c.fill = CALC
            c.border = BOX
            if fmt:
                c.number_format = fmt
        else:
            inp(c, v, key, fmt)
        a.cell(r, 4, unit)
        a.cell(r, 5, note).alignment = WRAP
        a.row_dimensions[r].height = 62
    dv1 = DataValidation(type="list", formula1='"Full implementation,2030 phase-in"', allow_blank=False)
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
    a.add_data_validation(dv1)
    a.add_data_validation(dv2)
    dv1.add("C6")
    dv2.add("C9")
    dv2.add("C11")

    r = 13
    a.cell(r, 1, "EU CBAM phase-in (CBF = share of embedded emissions charged)").font = B
    hdr(a, r + 1, ["Year"] + list(range(2026, 2035)), c0=2)
    a.cell(r + 2, 2, "CBF")
    for j, v in enumerate([0.025, 0.05, 0.10, 0.225, 0.485, 0.61, 0.735, 0.86, 1.0]):
        c = a.cell(r + 2, 3 + j, v)
        c.number_format = "0.0%"

    r = 18
    a.cell(r, 1, "Fixed assumptions (built into the product data)").font = B
    fixed = [
        "F1. Metric (row O): % change in CBAM obligations per tonne exported to the EU in 2030, measured as the change in "
        "embedded emissions of CBAM products only, weighted by 2024 EU export volumes (export mix and volumes held fixed).",
        "F2. O = sum_i X_i x EI_i / sum_i X_i x EI0_i - 1. Obligation = CBF x P_EU x EI, so the EU price and phase-in cancel. "
        "No deduction for the Egyptian carbon price is applied (memo rows 6-7 on CBAM_calc show that variant).",
        "F3. EI = direct embedded emissions per tonne (fuel combustion + process). Indirect (electricity) emissions are "
        "not included. Urea-bound CO2 is not deducted (CBAM rule). Actual (verified) emissions are assumed, not EU default values.",
        "F4. d_i = carbon price effectively paid in Egypt per tonne of product = tau_fuel x fuel intensity + tau_process x "
        "process intensity, less output-based rebates (3B) and, if A7 = Yes, the 3C fund. Floored at zero.",
        "F5. Domestic price USD 20/tCO2 in 2030 in all scenarios. 2A and 2B price fuel only (upstream levy); process "
        "emissions are unpriced there. 1A and 3A-3C price fuel and process emissions.",
        "F6. Policy fuel intensity = baseline x (1 + i_f), where i_f is CPAT's fuel-intensity response (one third of CPAT's "
        "industry fuel response; 3A-3C use the 1A value as the CBAM sectors are fully priced), plus, in 3C, the kernel's "
        "fund-financed fuel abatement.",
        "F7. Policy process intensity = industry kernel (CPAT_Industry_Kernel_Egypt_v1.3) process abatement response.",
        "F8. Products: DRI-EAF and scrap-EAF steel, grey clinker, ammonia, urea, ammonium nitrate, primary aluminium "
        "(BF-BOF steel not produced in Egypt). Baseline intensities: Egypt CBAM EF v0.1 (Methodology App. A).",
        "F9. EU export volumes: 2024 (kt): see CBAM_data column C.",
        "F10. Row O uses the same CBAM-product intensities as row N; it differs from N only by weighting (EU exports "
        "rather than output).",
    ]
    for i, s in enumerate(fixed):
        c = a.cell(r + 1 + i, 1, s)
        a.merge_cells(start_row=r + 1 + i, start_column=1, end_row=r + 1 + i, end_column=5)
        c.alignment = WRAP
        a.row_dimensions[r + 1 + i].height = 32
    a.column_dimensions["A"].width = 6
    a.column_dimensions["B"].width = 46
    a.column_dimensions["C"].width = 20
    a.column_dimensions["D"].width = 11
    a.column_dimensions["E"].width = 90
    for col in "FGHIJK":
        a.column_dimensions[col].width = 8

    # ---------------- Scenarios ----------------
    s = wb.create_sheet("Scenarios")
    s["A1"] = "Scenario parameters for the CBAM calculation (2030)"
    s["A1"].font = Font(bold=True, size=12)
    hdr(s, 3, ["Scenario", "Carbon price on fuel CO2 (USD/t)", "Carbon price on process emissions (USD/t)",
               "Output-based rebate rate (USD/t, 3B)", "Fuel-intensity response i_f (CPAT)",
               "3C abatement fund (USD bn)", "Description"])
    for i, sc in enumerate(SC):
        b = D[sc]
        co = {int(k): v for k, v in b["co"].items()}
        r = 4 + i
        s.cell(r, 1, sc).font = B
        inp(s.cell(r, 2), b["tau"], fmt="0.0")
        inp(s.cell(r, 3), b["pp"], fmt="0.0")
        inp(s.cell(r, 4), b["obr"], fmt="0.0")
        inp(s.cell(r, 5), co[31], fmt="0.00%")
        inp(s.cell(r, 6), co[60] if sc == "3C" else 0.0, fmt="0.000")
        s.cell(r, 7, DESC[sc])
    s.column_dimensions["A"].width = 10
    for col in "BCDEF":
        s.column_dimensions[col].width = 18
    s.column_dimensions["G"].width = 80
    s.row_dimensions[3].height = 45

    # ---------------- CBAM_data (by scenario x product) ----------------
    d = wb.create_sheet("CBAM_data")
    d["A1"] = ("CBAM products by scenario, 2030. Columns C-H are data from kernel v1.3 (hard-coded); "
               "columns I onwards are formulas.")
    d["A1"].font = B
    cols = ["Scenario", "Product", "EU exports 2024 (kt)", "Output 2030, policy (kt)",
            "Baseline fuel intensity EI0f (tCO2/t)", "Baseline process intensity EI0p (tCO2e/t)",
            "Kernel extra fuel abatement (tCO2/t; 3C fund)", "Policy process intensity (tCO2e/t; kernel)",
            "tau fuel", "tau process", "Rebate rate", "i_f",
            "Policy fuel intensity", "Policy embedded intensity EI", "Carbon price paid, gross (USD/t product)",
            "Output-based rebate (USD/t product)", "Carbon payment (USD m)", "3C fund share", "3C fund netted (USD/t product)",
            "Deductible price d (USD/t product)", "Baseline obligation (USD/t)", "Policy obligation (USD/t)",
            "X x baseline", "X x policy",
            "Full impl.: X x baseline", "Full impl.: X x policy", "2030: X x baseline", "2030: X x policy",
            "X x baseline EI (ktCO2e)", "X x policy EI (ktCO2e)"]
    hdr(d, 3, cols)
    d.row_dimensions[3].height = 75
    r = 4
    first = {}
    for sc in SC:
        b = D[sc]
        first[sc] = r
        n = 0
        for p in b["prods"]:
            if not p["X"]:
                continue
            n += 1
        last = r + n - 1
        for p in b["prods"]:
            if not p["X"]:
                continue
            Q = p["Q"]
            vals = [sc, p["name"], p["X"], Q, p["F0"], p["P0"], p["dfuel"] * 1000 / Q, (p["proc"] + p["dproc"]) * 1000 / Q]
            for j, v in enumerate(vals):
                c = d.cell(r, 1 + j, v)
                if j >= 2:
                    c.number_format = "0.0000" if j >= 4 else "#,##0"
            m = "MATCH($A{r},Scenarios!$A$4:$A$9,0)".format(r=r)
            f = {
                "I": "=INDEX(Scenarios!$B$4:$B$9,%s)" % m,
                "J": "=INDEX(Scenarios!$C$4:$C$9,%s)" % m,
                "K": "=INDEX(Scenarios!$D$4:$D$9,%s)" % m,
                "L": "=INDEX(Scenarios!$E$4:$E$9,%s)" % m,
                "M": "=E{r}*(1+L{r})+G{r}",
                "N": "=M{r}+H{r}",
                "O": "=I{r}*M{r}+J{r}*H{r}",
                "P": "=MIN(K{r},I{r})*E{r}+MIN(K{r},J{r})*F{r}",
                "Q": "=MAX(0,O{r}-P{r})*D{r}/1000",
                "R": "=IF(SUM($Q${a}:$Q${z})=0,0,Q{r}/SUM($Q${a}:$Q${z}))",
                "S": "=IF(Assumptions!$C$11=\"Yes\",INDEX(Scenarios!$F$4:$F$9,%s)*1000*R{r}/D{r}*1000,0)" % m,
                "T": "=MAX(0,O{r}-P{r}-S{r})",
                "U": "=Assumptions!$C$8*Assumptions!$C$5*(E{r}+F{r})",
                "V": "=MAX(0,Assumptions!$C$8*Assumptions!$C$5*N{r}-Assumptions!$C$10*T{r})",
                "W": "=C{r}*U{r}",
                "X": "=C{r}*V{r}",
                "Y": "=C{r}*Assumptions!$C$5*(E{r}+F{r})",
                "Z": "=C{r}*MAX(0,Assumptions!$C$5*N{r}-T{r})",
                "AA": "=C{r}*Assumptions!$C$7*Assumptions!$C$5*(E{r}+F{r})",
                "AB": "=C{r}*MAX(0,Assumptions!$C$7*Assumptions!$C$5*N{r}-IF(Assumptions!$C$9=\"Yes\",Assumptions!$C$7,1)*T{r})",
                "AC": "=C{r}*(E{r}+F{r})",
                "AD": "=C{r}*N{r}",
            }
            for colname, ff in f.items():
                c = d[colname + str(r)]
                c.value = ff.format(r=r, a=first[sc], z=last)
                c.number_format = "0.0000" if colname in ("L", "M", "N", "R") else "0.00"
                c.fill = CALC
            r += 1
    d.column_dimensions["A"].width = 9
    d.column_dimensions["B"].width = 26
    for j in range(3, 31):
        d.column_dimensions[d.cell(3, j).column_letter].width = 13
    d.freeze_panes = "C4"
    lastrow = r - 1

    # ---------------- CBAM_calc ----------------
    k = wb.create_sheet("CBAM_calc", 1)
    k["A1"] = "CBAM obligations, 2030: % change in embedded emissions per tonne exported to the EU (CBAM products only)"
    k["A1"].font = Font(bold=True, size=12)
    k["A2"] = ("O = sum_i X_i x EI_i(policy) / sum_i X_i x EI0_i - 1  (X = 2024 EU exports; EI = direct fuel + process "
               "intensity). The EU price and phase-in cancel out. Rows 6-7: memo only, not used in Table 2.")
    hdr(k, 4, ["Row", "Convention"] + SC)
    spec = [
        (5, "Embedded-intensity change (CBAM products only) -> Table 2 row O", "AC", "AD"),
        (6, "Memo: obligation net of Egyptian carbon-price deduction, full implementation", "Y", "Z"),
        (7, "Memo: obligation net of Egyptian carbon-price deduction, 2030 phase-in", "AA", "AB"),
    ]
    rng = lambda c: "CBAM_data!$%s$4:$%s$%d" % (c, c, lastrow)
    for rr, lab, cb, cp in spec:
        k.cell(rr, 1, "O")
        k.cell(rr, 2, lab)
        for j, sc in enumerate(SC):
            c = k.cell(rr, 3 + j)
            c.value = "=100*(SUMIF(%s,\"%s\",%s)/SUMIF(%s,\"%s\",%s)-1)" % (rng("A"), sc, rng(cp), rng("A"), sc, rng(cb))
            c.number_format = "0.0"
            c.fill = CALC
            c.border = BOX
    k.column_dimensions["A"].width = 6
    k.column_dimensions["B"].width = 70
    for col in "CDEFGH":
        k.column_dimensions[col].width = 10

    wb.save(OUT)
    return OUT


def recalc(path):
    import win32com.client as w
    xl = w.DispatchEx("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    try:
        wb = xl.Workbooks.Open(path)
        xl.CalculateFull()
        k = wb.Worksheets("CBAM_calc")
        out = [[round(k.Cells(r, c).Value, 2) for c in range(3, 9)] for r in (5, 6, 7)]
        wb.BuiltinDocumentProperties("Author").Value = "Stephen Stretton"
        wb.BuiltinDocumentProperties("Last Author").Value = "Stephen Stretton"
        wb.Worksheets("Table2").Activate()
        wb.Save()
        wb.Close(False)
    finally:
        xl.Quit()
    return out


if __name__ == "__main__":
    p = build()
    res = recalc(p)
    for lab, v in zip(("selected", "full impl.", "2030 phase-in"), res):
        print(lab, v)
    shutil.copy2(p, COPY)
    print("saved", p, "and", COPY)
