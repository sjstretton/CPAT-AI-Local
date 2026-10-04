"""Build egypt-final/simple/Egypt_Simple.xlsx: a very small, plain-words workbook of the final Egypt results.
Visible: How it works / Results / Try it (material parameters only). Hidden: Other parameters.
Numbers come from carveout_v1_6_results.json (same source as the final documents)."""
import json
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "egypt-final", "simple", "Egypt_Simple.xlsx"))
_raw = json.load(open(os.path.join(HERE, "carveout_v1_6_results.json"), encoding="utf8"))
R = _raw["results"] if "results" in _raw else _raw
B = ["1A", "2A", "2B", "3A", "3B", "3C"]

INPUT = PatternFill("solid", fgColor="FFF2CC")   # you can change these
CALC = PatternFill("solid", fgColor="EBF1DE")    # worked out for you
HEAD = PatternFill("solid", fgColor="D9E1F2")
BOLD = Font(bold=True)
BIG = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

# ------------------------------------------------------------------ How it works
ws = wb.active
ws.title = "How it works"
ws.column_dimensions["A"].width = 4
ws.column_dimensions["B"].width = 100
lines = [
    ("Egypt carbon price: how the numbers are made", BIG),
    ("Six ideas for putting a price on carbon in Egypt were tested. Everything is for the year 2030 at a price of USD 20 per tonne of CO₂.", None),
    ("", None),
    ("1.  Start with the World Bank climate tool (called CPAT).", BOLD),
    ("     It says how much Egypt's emissions fall when carbon gets a price.", None),
    ("2.  CPAT is weak on four industries: steel, cement, fertiliser and aluminium.", BOLD),
    ("     These are the goods the EU taxes at its border (CBAM). So we remove CPAT's rough guess for them.", None),
    ("3.  We put in our own estimate for those four industries. It has three simple steps:", BOLD),
    ("     a) The price makes the goods dearer, so a little less is made.", None),
    ("     b) Plants burn a little less fuel for each tonne they make.", None),
    ("     c) The chemistry of making the goods gives off a little less for each tonne.", None),
    ("4.  Add it up:  final cut = CPAT's cut − CPAT's guess for the four industries + our estimate.", BOLD),
    ("     In scenario 3B the free allowances reach all industry, so one more small line is added back.", None),
    ("5.  The CBAM bill.", BOLD),
    ("     The EU charges for the emissions inside each tonne of goods that Egypt sells to it.", None),
    ("     If the emissions in each tonne fall by 5%, the bill for each tonne falls by 5%. That is all.", None),
    ("", None),
    ("Sheet 'Results' shows the six scenarios. Sheet 'Try it' lets you change the main numbers for one product and see what happens.", None),
    ("Yellow cells can be changed. Green cells are worked out for you. All other settings are hidden (right-click a sheet tab, then Unhide).", None),
    ("This is a simplified picture. The full method is in the methodology document.", Font(italic=True)),
]
for i, (t, f) in enumerate(lines, start=1):
    c = ws.cell(i, 2, t)
    c.alignment = WRAP
    if f:
        c.font = f

# ------------------------------------------------------------------ Results
rs = wb.create_sheet("Results")
rs.column_dimensions["A"].width = 58
for col in "BCDEFG":
    rs.column_dimensions[col].width = 11
rs["A1"] = "Results for 2030 (carbon price USD 20 per tonne of CO₂)"
rs["A1"].font = BIG
rs["A3"] = "Scenario"
for j, b in enumerate(B):
    rs.cell(3, 2 + j, b)
for c in rs[3]:
    c.font = BOLD
    c.fill = HEAD
rs["A4"] = "What it is"
desc = ["Price on all energy + industry process", "Price on all energy", "Price on all energy, money to people",
        "Price on industry only", "Industry only + free allowances", "Industry only + clean-up fund"]
for j, d in enumerate(desc):
    c = rs.cell(4, 2 + j, d)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=8)
rs.row_dimensions[4].height = 48

rs["A6"] = "How much emissions fall (million tonnes of CO₂e)"
rs["A6"].font = BOLD
rows = [
    (7, "CPAT's own cut (whole country)", lambda r: r["dghg"]),
    (8, "Take out CPAT's guess for steel, cement, fertiliser, aluminium", lambda r: -r["cpat_blk"]),
    (9, "Put in our estimate for those four", lambda r: r["dB"]),
    (10, "3B only: free allowances reach all industry (adds back)", lambda r: r["D_nb"]),
]
for rr, lab, f in rows:
    rs.cell(rr, 1, lab)
    for j, b in enumerate(B):
        c = rs.cell(rr, 2 + j, round(f(R[b]), 4))
        c.number_format = "0.0"
        c.fill = INPUT
rs["A11"] = "Final cut"
rs["A11"].font = BOLD
for j in range(6):
    col = "BCDEFG"[j]
    c = rs.cell(11, 2 + j, "=SUM(%s7:%s10)" % (col, col))
    c.number_format = "0.0"
    c.font = BOLD
    c.fill = CALC
rs["A12"] = "(Rows may not add exactly on screen because of rounding.)"
rs["A12"].font = Font(italic=True, size=8)

rs["A14"] = "Other results"
rs["A14"].font = BOLD
other = [
    (15, "Money raised (USD billion)", "P", "0.0"),
    (16, "People spared early death from air pollution (per year)", "Q", "#,##0"),
    (17, "Share of Egypt's emissions that are priced (%)", "J", "0"),
]
for rr, lab, key, nf in other:
    rs.cell(rr, 1, lab)
    for j, b in enumerate(B):
        c = rs.cell(rr, 2 + j, round(R[b][key], 4))
        c.number_format = nf
        c.fill = INPUT

rs["A19"] = "The CBAM bill"
rs["A19"].font = BOLD
rs["A20"] = "Emissions in each tonne of CBAM goods: change before → after (%)"
rs["A21"] = "Emissions in each tonne before (index)"
rs["A22"] = "Emissions in each tonne after (index)"
rs["A23"] = "Change in the CBAM bill for each tonne sold to the EU (%)"
for j, b in enumerate(B):
    col = "BCDEFG"[j]
    o = round(R[b]["O_final"], 3)
    rs.cell(21, 2 + j, 100).fill = INPUT
    c = rs.cell(22, 2 + j, round(100 * (1 + o / 100), 3))
    c.fill = INPUT
    c.number_format = "0.0"
    c = rs.cell(23, 2 + j, "=(%s22/%s21-1)*100" % (col, col))
    c.number_format = "0.0"
    c.font = BOLD
    c.fill = CALC
rs["A25"] = "Reading the table: a minus sign means a fall. The bill moves by the same percentage as the emissions in each tonne, because the EU price and the EU's phase-in cancel out."
rs["A25"].alignment = WRAP
rs.merge_cells("A25:G25")
rs.row_dimensions[25].height = 42
rs["A26"] = "Yellow = a result taken from the full model. Green = worked out here."
rs["A26"].font = Font(italic=True, size=8)
for row in rs.iter_rows(min_row=3, max_row=23, min_col=1, max_col=7):
    for c in row:
        if c.value is not None:
            c.border = BOX

# ------------------------------------------------------------------ Try it
ty = wb.create_sheet("Try it")
ty.column_dimensions["A"].width = 62
ty.column_dimensions["B"].width = 12
ty.column_dimensions["C"].width = 70
ty["A1"] = "Try it: what a carbon price does to one product"
ty["A1"].font = BIG
ty["A2"] = "Example: cement clinker, carbon price on both fuel and process emissions. Change the yellow cells."
ty["A2"].font = Font(italic=True)
inputs = [
    (4, "Carbon price (USD per tonne of CO₂)", 20, "0", "The price on each tonne of CO₂."),
    (5, "Price of the product (USD per tonne)", 110, "0", "What a tonne of clinker sells for."),
    (6, "Emissions per tonne from burning fuel (tonnes CO₂)", 0.314, "0.000", "Heat for the kiln."),
    (7, "Emissions per tonne from the process itself (tonnes CO₂)", 0.537, "0.000", "Chemistry: limestone turning into lime."),
    (8, "Output response (1% dearer → this % less made)", -0.1, "0.00", "-0.1 for cement: 1% dearer gives 0.1% less output. Steel and fertiliser -0.4, aluminium -0.5. Based on studies of demand and pass-through."),
    (9, "Fuel saved per tonne at this price", -0.049, "0.0%", "Plants get a little more efficient. From the climate tool."),
    (10, "Process emissions saved per tonne at this price", 0.065, "0.0%", "From international cost studies of cleaner methods."),
]
for rr, lab, v, nf, note in inputs:
    ty.cell(rr, 1, lab)
    c = ty.cell(rr, 2, v)
    c.number_format = nf
    c.fill = INPUT
    ty.cell(rr, 3, note).font = Font(size=9, italic=True)
ty["A12"] = "What happens"
ty["A12"].font = BOLD
calc = [
    (13, "Extra cost for each tonne (USD)", "=B4*(B6+B7)", "0.00", "Carbon price × emissions in a tonne."),
    (14, "Cost rise (%)", "=B13/B5", "0.0%", "Extra cost ÷ price of the product."),
    (15, "Change in how much is made", "=(1+B14)^B8-1", "0.0%", "Dearer goods, a little less sold."),
    (16, "Emissions in a tonne, before", "=B6+B7", "0.000", "Fuel plus process."),
    (17, "Emissions in a tonne, after", "=B6*(1+B9)+B7*(1-B10)", "0.000", "Less fuel and less process emissions per tonne."),
    (18, "Change in emissions in each tonne", "=B17/B16-1", "0.0%", "This is also the change in the CBAM bill for each tonne sold to the EU."),
    (19, "Change in total emissions from this product", "=(1+B15)*(1+B18)-1", "0.0%", "Fewer tonnes made, and fewer emissions in each."),
]
for rr, lab, f, nf, note in calc:
    ty.cell(rr, 1, lab)
    c = ty.cell(rr, 2, f)
    c.number_format = nf
    c.fill = CALC
    ty.cell(rr, 3, note).font = Font(size=9, italic=True)
ty["A18"].font = BOLD
ty["B18"].font = BOLD
ty["A21"] = "This is one product only. The real model does this for eight products, then adds them up and combines them with the climate tool's results."
ty["A21"].alignment = WRAP
ty.merge_cells("A21:C21")
ty.row_dimensions[21].height = 30

# ------------------------------------------------------------------ hidden parameters
hp = wb.create_sheet("Other parameters")
hp.column_dimensions["A"].width = 60
hp.column_dimensions["B"].width = 18
hp.column_dimensions["C"].width = 60
hp["A1"] = "Settings that are not needed to follow the story (hidden sheet)"
hp["A1"].font = BIG
params = [
    ("EU carbon price (USD per tonne)", 100, "Placeholder. Cancels out of the CBAM bill change."),
    ("EU CBAM phase-in share in 2030", 0.485, "Cancels out of the CBAM bill change."),
    ("Efficiency share of the climate tool's industry fuel response", "1/3", "The other two thirds is less output."),
    ("Share of industry energy CO₂ priced in the industry-only run (EG3)", 0.537, "Used as run, no scaling."),
    ("Growth of steel output 2024-2030 (adjustment)", 0.976, "Matches the climate tool."),
    ("Growth of cement output 2024-2030 (adjustment)", 1.001, "Matches the climate tool."),
    ("CBAM goods' emissions before any policy (million tonnes CO₂e)", 63.1, "Fuel plus process."),
    ("3B rebate to the rest of covered industry (USD billion)", 0.33, "Comes off revenue."),
    ("Price base for process clean-up studies", "USD 122 (2024)", "100 in 2019 dollars."),
    ("Climate tool runs used", "EG1, EG2, EG3", "1A, 2A: EG1. 2B: EG2. 3A-3C: EG3."),
    ("Where the numbers come from", "Egypt_Model.xlsx", "Sheets CarveOut_Table2 and Table2_Final."),
]
for i, (a, b, c) in enumerate(params, start=3):
    hp.cell(i, 1, a)
    hp.cell(i, 2, b)
    hp.cell(i, 3, c)
hp.sheet_state = "hidden"

wb.active = 0
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("saved", OUT)
