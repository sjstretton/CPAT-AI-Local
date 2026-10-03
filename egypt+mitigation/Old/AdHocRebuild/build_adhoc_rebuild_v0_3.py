"""Build AdHocCalculations_Rebuild_v0.3.xlsx: a formula-driven rebuild of the ad hoc Egypt "PolicyMatrix"
calculations (InitialResultsAndIssues/AdHocCalculations.xlsb, Table 2 of the Egypt results note).

Design (TASK-2b):
  * Inputs      - every assumption and switch lives here (tan = switch, light green = input). Nothing is typed
                  anywhere else. One-cell Mode switch: REBUILD (default, coherent method) / PROTOTYPE (reproduces
                  the AI prototype kernel CPAT_Industry_Kernel_Egypt_v0.11 exactly; verified in Comparison).
  * CPAT_Outputs- trimmed CPAT Outputs sheet (32 codes x EG1..EG4 x 2022..2041) = the only data source.
  * CBAM_Products - six stacked product blocks (one per bundle), the prototype's product-level engine
                  (8 CBAM goods: cost pass-through, output response, fuel-intensity and process-intensity
                  responses, revenue, OBR rebate, CBAM obligation under FULL / NOPHASE / SCALED conventions).
  * Results     - the engine: block totals, block metrics, CPAT national quantities and the composition of
                  every Table-2 metric. PolicyMatrix, Comparison and Checks only read from here.
  * PolicyMatrix- same layout as the original (A..AU; hidden B/D/E; rows 7..12 = bundles 1A,2A,2B,3A,3B,3C);
                  AF..AQ redefined (yellow headers) - see ReadMe 'Format changes'.
  * Comparison  - original workbook vs Table 2 vs rebuilt (live) vs prototype v0.11 (FULL and NOPHASE), plus
                  the cell-level PROTOTYPE-mode verification (all block metrics equal the prototype run).
  * Issues resolved - the 19 items of MajorIssues.docx mapped to root cause / resolution / residual.
  * Checks      - integrity checks (col B text, col D PASS/FAIL, overall cell) read by recalc_and_check_adhoc.py.

Run: python build_adhoc_rebuild_v0_3.py  (openpyxl, writes formulas only) then
     python recalc_and_check_adhoc_v0_3.py (Excel COM: recalculates, verifies PROTOTYPE mode vs the prototype
                                           json to 1e-7, verifies REBUILD mode vs an independent Python mirror,
                                           saves with Mode=REBUILD / Conv=NOPHASE).
Companion note: MethodologyNote_v0.3.md / .docx (same folder).
v0.2 (vs v0.1): emission factors fc/fp/np/no = Egypt CBAM EF v0.1 (egypt+mitigation/EmissionFactors/EGY_CBAM_EF_v0.1.xlsx
Products!D:G; urea CBAM rule np = 0; AN keeps the integrated HNO3 N2O in own 'no' = 0.79 x 1.259) selected by the new
switch EFSet (EGY_EF_V01 default | PROTOTYPE = v0.11 kernel EFs, forced in PROTOTYPE mode); AN process ER100 = N2O-
weighted blend of the TASK-D unabated / abated rows at the EF workbook's 50 % abatement share (central 0.6179).
v0.3 (vs v0.2): IPCC beta anchor PStar = 122 USD2024 (100 USD2019 deflated) for non-prototype beta sets; KappaMode
SCALE default approximates a full-coverage EG3 run by scaling EG3 industry energy responses and fuel receipts by 1/kappa.
Verifier: recalc_and_check_adhoc_v0_3.py.
Sources (read-only): ../InitialResultsAndIssues/AdHocCalculations.xlsb (dump: original_PolicyMatrix_cells.txt),
prototype_v0_11_results.json (COM run of the prototype), cpat_outputs_egypt_2022_2041.csv (CPAT Outputs sheet).
"""
import ast
import csv
import datetime
import json
import os
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "v0.3"
DST = os.path.join(HERE, "AdHocCalculations_Rebuild_%s.xlsx" % VERSION)
CSV_SRC = os.path.join(HERE, "cpat_outputs_egypt_2022_2041.csv")
JSON_SRC = os.path.join(HERE, "prototype_v0_11_results.json")
DUMP_SRC = os.path.join(HERE, "original_PolicyMatrix_cells.txt")
TODAY = datetime.date.today().isoformat()

# NORMS.md colours
TITLE = PatternFill("solid", fgColor="00B050")
SECTION = PatternFill("solid", fgColor="92D050")
GREEN = PatternFill("solid", fgColor="EBF1DE")     # inputs
BLUE = PatternFill("solid", fgColor="DCE6F1")      # codes
TAN = PatternFill("solid", fgColor="DDD9C4")       # switches
GREY = PatternFill("solid", fgColor="F2F2F2")      # inactive / reference only
REVIEW = PatternFill("solid", fgColor="FFF2CC")    # results / to review
ORIG_HDR = PatternFill("solid", fgColor="DBEDFF")  # original PolicyMatrix header fill
ARIAL = Font(name="Arial", size=10)
BOLD = Font(name="Arial", size=10, bold=True)
ITALIC = Font(name="Arial", size=10, italic=True)
WHITE_BOLD = Font(name="Arial", size=14, bold=True, color="FFFFFF")
ORIG_HDR_FONT = Font(name="Arial", size=10, bold=True, color="0078F0")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

ACC2 = '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)'
USD0 = '$#,##0_);[Red]($#,##0)'

BUNDLES = ["1A", "2A", "2B", "3A", "3B", "3C"]
YEARS = list(range(2022, 2042))

# ----------------------------------------------------------------------------------------------------------------
# Assumption tables (written to Inputs; nothing below is used anywhere else)
# ----------------------------------------------------------------------------------------------------------------
# Bundle: code, CPAT scenario, scope (ALL = economy-wide fuel levy, IND = industry-only), process flag,
#         theta (OBR rebate share of the carbon cost), phi (share of net revenue to the abatement fund),
#         recycling label, price-trajectory label
BUNDLE_TBL = [
    ("1A", "EG1", "ALL", 1, 0, 0, "Public investment", "FLAT20"),
    ("2A", "EG1", "ALL", 0, 0, 0, "Public investment", "FLAT20"),
    ("2B", "EG2", "ALL", 0, 0, 0, "Households", "FLAT20"),
    ("3A", "EG3", "IND", 1, 0, 0, "Households", "RAMP"),
    ("3B", "EG3", "IND", 1, 1, 0, "Firms (output)", "RAMP"),
    ("3C", "EG3", "IND", 1, 0, 1, "Firms (abatement)", "RAMP"),
]
# Products: name, Q0 2024 kt, g, EU exports kt, price $/t (prototype v0.11 Manual inputs);
#   fc, fp, np, no = Egypt CBAM EF v0.1 (EGY_CBAM_EF_v0.1.xlsx Products!D:G; AN no = integrated HNO3 N2O 0.79 x 1.2588);
#   ER100 prototype, ER100 IPCC central, ER100 IPCC 2030-horizon, ER100 IPCC long-run (TASK-D drop-in; AN = blend of
#   unabated / abated rows weighted by N2O at 50 % abatement: 0.7368 / 0.2632);
#   fc, fp, np, no of prototype v0.11 (reference; used when EFSet = PROTOTYPE)
PRODUCT_TBL = [
    ("DRI-EAF steel", 5100, 0.044, 580, 750, 0.17797725, 0.39301352, 0.03790102, 0.0, 0.10, 0.3433, 0.1133, 0.5734,
     0.12903, 0.561, 0.04, 0.0),
    ("Scrap-EAF steel", 4800, 0.044, 300, 680, 0.04488, 0.0, 0.04398115, 0.0, 0.02, 0.1810, 0.0951, 0.2669,
     0.14025, 0.0, 0.015, 0.0),
    ("BF-BOF steel", 0, 0.0, 0, 620, 0.1683, 1.25668027, 0.05276542, 0.0, 0.05, 0.2803, 0.1016, 0.4589,
     0.3844, 1.5376, 0.25, 0.0),
    ("Clinker", 50000, 0.033, 800, 110, 0.3135685, 0.0, 0.53702616, 0.0, 0.08, 0.3352, 0.1925, 0.4779,
     0.2883, 0.0, 0.526, 0.0),
    ("Ammonia", 1785, 0.022, 120, 450, 0.71247, 1.26225, 0.0, 0.0, 0.18, 0.2974, 0.1499, 0.4449,
     0.3927, 1.4586, 0.0, 0.0),
    ("Urea", 2800, 0.022, 1600, 380, 0.1122, 0.0, 0.0, 0.0, 0.0, 0.1158, 0.0479, 0.1838,
     0.1122, 0.0, -0.733, 0.0),
    ("Ammonium nitrate", 600, 0.022, 80, 320, 0.1122, 0.0, 0.0, 0.9944125, 0.65, 0.6179, 0.5539, 0.6818,
     0.1122, 0.0, 0.0, 0.97),
    ("Aluminium", 300, 0.055, 167, 2400, 0.12342, 0.0, 1.62349304, 0.774, 0.08, 0.2164, 0.0691, 0.3638,
     0.156, 0.0, 1.5, 0.85),
]
CBF_PATH = {2026: 0.025, 2027: 0.05, 2028: 0.10, 2029: 0.225, 2030: 0.485, 2031: 0.61, 2032: 0.735, 2033: 0.86}
# CPAT codes pulled into Inputs section C: (row label, code, unit, name of the 1x4 row range)
CPAT_ROWS = [
    ("Total GHG incl. LULUCF - baseline", "egy.mit.ghg.tot.inc.1", "MtCO2e", "CV_ghg0"),
    ("Total GHG incl. LULUCF - policy", "egy.mit.ghg.tot.inc.2", "MtCO2e", "CV_ghg1"),
    ("IPPU GHG - baseline", "egy.mit.ghg.ipr.tot.1", "MtCO2e", "CV_ippu0"),
    ("IPPU GHG - policy", "egy.mit.ghg.ipr.tot.2", "MtCO2e", "CV_ippu1"),
    ("Energy CO2 - baseline", "egy.mit.co2.enr.tot.1", "MtCO2", "CV_enr0"),
    ("Energy CO2 - policy", "egy.mit.co2.enr.tot.2", "MtCO2", "CV_enr1"),
    ("Industry energy CO2 - baseline", "egy.mit.co2.ind.1", "MtCO2", "CV_ind0"),
    ("Industry energy CO2 - policy", "egy.mit.co2.ind.2", "MtCO2", "CV_ind1"),
    ("Carbon price trajectory", "egy.mit.cptraj.2", "$/tCO2", "CV_cptraj"),
    ("Effective (coverage-weighted) carbon price", "egy.mit.eff.cptraj.2", "$/tCO2", "CV_effcp"),
    ("Net new revenue - baseline", "egy.mit.rev.new.usd.1", "$bn", "CV_revnew0"),
    ("Net new revenue - policy", "egy.mit.rev.new.usd.2", "$bn", "CV_revnew1"),
    ("Carbon-tax revenue: coal", "egy.mit.rev.new.coa.usd.2", "$bn", None),
    ("Carbon-tax revenue: diesel", "egy.mit.rev.new.die.usd.2", "$bn", None),
    ("Carbon-tax revenue: gasoline", "egy.mit.rev.new.gso.usd.2", "$bn", None),
    ("Carbon-tax revenue: LPG/kerosene", "egy.mit.rev.new.lpk.usd.2", "$bn", None),
    ("Carbon-tax revenue: natural gas", "egy.mit.rev.new.nga.usd.2", "$bn", None),
    ("Carbon-tax revenue: oil products", "egy.mit.rev.new.oil.usd.2", "$bn", None),
    ("Air-pollution deaths avoided, 25-64", "egy.air.ada.2464", "deaths", None),
    ("Air-pollution deaths avoided, 65+", "egy.air.ada.65", "deaths", None),
    ("Air-pollution deaths avoided, under 24", "egy.air.ada.u24", "deaths", None),
    ("Air-pollution deaths - baseline total", "egy.air.mort", "deaths", "CV_mort"),
]
SCENS = ["EG1", "EG2", "EG3", "EG4"]

# ----------------------------------------------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------------------------------------------
wb = Workbook()
NAMES = {}


def name(nm, ref):
    """Workbook-level defined name (ref must be absolute, e.g. Inputs!$D$5)."""
    wb.defined_names[nm] = DefinedName(nm, attr_text=ref)
    NAMES[nm] = ref


def put(ws, addr, value, fmt=None, fill=None, font=None, align=None, border=True):
    c = ws[addr]
    c.value = value
    c.font = font or ARIAL
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if align:
        c.alignment = align
    if border:
        c.border = BOX
    return c


def title_band(ws, text, last_col, row=1):
    ws.merge_cells("A%d:%s%d" % (row, last_col, row))
    c = ws["A%d" % row]
    c.value = text
    c.font = WHITE_BOLD
    c.fill = TITLE
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[row].height = 22


def section_band(ws, row, text, last_col, first_col="A"):
    ws.merge_cells("%s%d:%s%d" % (first_col, row, last_col, row))
    c = ws["%s%d" % (first_col, row)]
    c.value = text
    c.font = BOLD
    c.fill = SECTION
    c.alignment = Alignment(vertical="center")


def header_row(ws, row, labels, first_col=1, fill=GREY):
    for i, lab in enumerate(labels):
        put(ws, "%s%d" % (get_column_letter(first_col + i), row), lab, fill=fill, font=BOLD, align=CENTER)


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def col(c):
    return column_index_from_string(c)


def L(i):
    return get_column_letter(i)


# ----------------------------------------------------------------------------------------------------------------
# Load data: CPAT csv, prototype json, original dump
# ----------------------------------------------------------------------------------------------------------------
with open(CSV_SRC, encoding="utf-8") as fh:
    CSV_ROWS = list(csv.reader(fh))
CSV_HDR, CSV_DATA = CSV_ROWS[0], CSV_ROWS[1:]
assert CSV_HDR[4:] == [str(y) for y in YEARS], CSV_HDR

with open(JSON_SRC, encoding="utf-8") as fh:
    PROTO = json.load(fh)

DUMP_LINE = re.compile(r"^([A-Z]+\d+)\t([VF])\t(.*?)\t(.*?)\t\[(.*)\] fill=(\S*) font=(\S*)\s*([MWI]*)\s*$")


def _lit(s):
    s = s.strip()
    if s == "":
        return None
    s = re.sub(r"Decimal\('([^']*)'\)", r"\1", s)
    try:
        return ast.literal_eval(s)
    except Exception:
        return s


def parse_dump(path):
    """Return {addr: dict(kind, value, formula, cached, fmt, fill, fontcolor, bold, italic, wrap)}."""
    cells = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            m = DUMP_LINE.match(line)
            if not m:
                raise ValueError("unparsed dump line: %r" % line)
            addr, kind, a, b, fmt, fill, font, flags = m.groups()
            d = {"kind": kind, "fmt": fmt, "fill": fill or None, "wrap": "W" in flags, "merged": "M" in flags}
            fcol = font[:6] if re.match(r"^[0-9A-F]{6}", font) else None
            d["fontcolor"] = fcol if fcol not in (None, "000000") else None
            d["bold"] = font.endswith("B") or font[6:].startswith("B") if fcol else False
            d["italic"] = "I" in font[6:] if fcol else False
            if kind == "V":
                d["value"], d["formula"], d["cached"] = _lit(a), None, None
            else:
                b = b[2:].strip() if b.startswith("=>") else b
                d["value"], d["formula"], d["cached"] = None, a, _lit(b)
            cells[addr] = d
    return cells


ORIG = parse_dump(DUMP_SRC)
assert ORIG["K7"]["formula"] == "=K9+AL7" and abs(ORIG["K7"]["cached"] + 41.62107989197109) < 1e-9

# ================================================================================================================
# Sheet 1: ReadMe (filled at the end), Sheet 2: Inputs
# ================================================================================================================
ws_readme = wb.active
ws_readme.title = "ReadMe"
wsI = wb.create_sheet("Inputs")
IN = {}  # row bookkeeping
widths(wsI, {"A": 46, "B": 14, "C": 15, "D": 14, "E": 14, "F": 13, "G": 13, "H": 13, "I": 12, "J": 12, "K": 12,
             "L": 12, "M": 12, "N": 12, "O": 12, "P": 12, "Q": 12, "R": 10, "S": 10, "T": 10, "U": 10})
title_band(wsI, "Inputs - all assumptions and switches (AdHoc Calculations rebuild %s)" % VERSION, "U")
wsI.merge_cells("A2:P2")
put(wsI, "A2", "Edit only tan cells (switches) and light-green cells (inputs). Every other cell in the workbook is "
    "a formula. Defined names are listed in column E.", font=ITALIC, border=False)

# --- A. Switches ---------------------------------------------------------------------------------------------
section_band(wsI, 4, "A. Switches", "P")
header_row(wsI, 5, ["Switch", "Value (edit)", "Allowed values", "Effective (named)", "Name", "Notes"])
wsI.merge_cells("F5:P5")
SWITCHES = [
    ("Mode", "Calculation mode", "REBUILD", "REBUILD, PROTOTYPE", "=UPPER(TRIM(B{r}))",
     "REBUILD = coherent method (headline). PROTOTYPE = reproduce CPAT_Industry_Kernel_Egypt_v0.11 exactly "
     "(xf=1, prototype beta set, fund shadow price 0); verified cell by cell in Comparison section 2."),
    ("Conv", "CBAM obligation convention", "NOPHASE", "NOPHASE, FULL, SCALED", "=UPPER(TRIM(B{r}))",
     "NOPHASE (default): full certificate price EUR/USD 100 with no phase-in, deduction of carbon price paid - the "
     "definition behind column O of the original (intensity + price credit). FULL: 2030 phase-in factor 0.485 on "
     "the obligation, full deduction. SCALED: phase-in on both obligation and deduction (prototype memo)."),
    ("Yr", "Reporting year", 2030, "2026 .. 2041", "=B{r}",
     "All Table-2 metrics are for this year; CPAT values are looked up live for it."),
    ("SigmaEff", "Fund shadow price sigma ($/tCO2) for bundle 3C", 20, ">= 0", '=IF(Mode="PROTOTYPE",0,B{r})',
     "Abatement-fund payments modelled as a shadow price added to the carbon price in the fuel-intensity and "
     "process-intensity responses (TechNote: fund enters the efficiency term only). 0 in PROTOTYPE mode."),
    ("BetaSet", "Process half-elasticity (beta) set", "IPCC_CENTRAL",
     "IPCC_CENTRAL, IPCC_2030, IPCC_LONGRUN, PROTOTYPE", '=IF(Mode="PROTOTYPE","PROTOTYPE",UPPER(TRIM(B{r})))',
     "beta_s = -LN(1-ER100_s)/100 from IPCC MACC bands (TASK-D drop-in). PROTOTYPE set forced in PROTOTYPE mode."),
    ("EFSet", "Emission-factor set (fc, fp, np, no)", "EGY_EF_V01", "EGY_EF_V01, PROTOTYPE",
     '=IF(Mode="PROTOTYPE","PROTOTYPE",UPPER(TRIM(B{r})))',
     "EGY_EF_V01 = Egypt CBAM EF v0.1 (EmissionFactors/EGY_CBAM_EF_v0.1.xlsx; urea CBAM rule np = 0; AN integrated "
     "HNO3 N2O in no). PROTOTYPE = kernel v0.11 EFs (Inputs E, columns R:U); forced in PROTOTYPE mode."),
    ("BfScen", "CPAT scenario used to calibrate the fuel-intensity semi-elasticity b_f", "EG1", "EG1, EG2, EG3",
     "=UPPER(TRIM(B{r}))", "b_f = s_int * LN(ind.2/ind.1) / price (section B). EG1 is the economy-wide $20 run."),
    ("ThetaOther", "OBR rebate (3B) also for non-CBAM priced industry? (0 = CBAM producers only)", 0, "0, 1",
     "=B{r}", "Original 3B text says 'free allocation for CBAM producers'. 0 keeps revenue from non-CBAM industry "
     "(3B raises revenue); 1 rebates all covered industry (output channel removed everywhere, revenue ~0)."),
    ("IppuOther", "Non-CBAM IPPU response to a fuel-only price", "NONE", "NONE, CPAT", "=UPPER(TRIM(B{r}))",
     "CPAT scales all IPPU with industrial energy CO2 (MajorIssues #17). NONE removes it (process emissions "
     "respond only where priced or via output); CPAT keeps CPAT's scaling for the non-CBAM IPPU remainder."),
    ("KappaMode", "Coverage factor kappa / EG3 full-coverage approximation", "SCALE", "SCALE, AUTO, ONE", "=UPPER(TRIM(B{r}))",
     "SCALE (default): approximation of a full-coverage EG3 run (pending a CPAT re-run), scaling EG3 industry "
     "energy responses and fuel receipts by 1/kappa while coverage J uses kappa = 1. AUTO: expose CPAT's partial "
     "coverage. ONE: assume CPAT was already full coverage without scaling."),
]
r = 6
for nm, label, val, allowed, eff, note in SWITCHES:
    put(wsI, "A%d" % r, label, font=BOLD)
    put(wsI, "B%d" % r, val, fill=TAN, align=CENTER)
    put(wsI, "C%d" % r, allowed, align=WRAP)
    put(wsI, "D%d" % r, eff.format(r=r), fill=REVIEW, align=CENTER)
    put(wsI, "E%d" % r, nm, fill=BLUE)
    wsI.merge_cells("F%d:P%d" % (r, r))
    put(wsI, "F%d" % r, note, align=WRAP)
    wsI.row_dimensions[r].height = 42
    name(nm, "Inputs!$D$%d" % r)
    IN[nm] = r
    r += 1
DV = {
    "Mode": '"REBUILD,PROTOTYPE"', "Conv": '"NOPHASE,FULL,SCALED"', "BetaSet": '"IPCC_CENTRAL,IPCC_2030,IPCC_LONGRUN,PROTOTYPE"',
    "EFSet": '"EGY_EF_V01,PROTOTYPE"',
    "BfScen": '"EG1,EG2,EG3"', "ThetaOther": '"0,1"', "IppuOther": '"NONE,CPAT"', "KappaMode": '"SCALE,AUTO,ONE"',
}
for nm, lst in DV.items():
    dv = DataValidation(type="list", formula1=lst, allow_blank=False)
    wsI.add_data_validation(dv)
    dv.add("B%d" % IN[nm])
dv = DataValidation(type="whole", operator="between", formula1="2026", formula2="2041")
wsI.add_data_validation(dv)
dv.add("B%d" % IN["Yr"])

# --- B. Core parameters -------------------------------------------------------------------------------------
r += 1
section_band(wsI, r, "B. Core parameters", "P")
r += 1
header_row(wsI, r, ["Parameter", "Value (edit)", "Unit", "Effective / derived (named)", "Name", "Source / notes"])
wsI.merge_cells("F%d:P%d" % (r, r))
r += 1
PARAMS = [
    ("EpsU", "Own-price elasticity of industrial output demand (eps_U)", -0.5, "-", "=B{r}",
     "TechNote App. A (CPAT industry fuel-demand split)."),
    ("EpsF", "Price elasticity of fuel intensity (eps_F)", -0.5, "-", "=B{r}", "TechNote App. A."),
    ("SInt", "Intensity share of the CPAT industrial fuel response s_int", None, "-",
     "=EpsF*(1+EpsU)/(EpsU+EpsF*(1+EpsU))",
     "TechNote App. A: eps_F(1+eps_U)/(eps_U+eps_F(1+eps_U)); = 1/3 at -0.5/-0.5 (the '(2/3)/0.5' of K11 is the "
     "output share divided by |eps|). Output share = 1 - s_int."),
    ("EpsQ", "CBAM-product output response to cost pass-through (eps, prototype)", -0.5, "-", "=B{r}",
     "Prototype v0.11 Manual inputs. Q = Q_base * (1 + dp)^eps with dp = net carbon cost / product price."),
    ("PEU", "CBAM certificate price (EU ETS proxy)", 100, "$/tCO2", "=B{r}", "Prototype v0.11 (T79)."),
    ("PStar", "IPCC process semi-elasticity anchor price P* (USD2024/tCO2)", 122, "$/tCO2", "=B{r}",
     "USD2019 100 deflated to USD2024 (US GDP deflator ≈ 1.22); Medium confidence. Used only for IPCC beta sets: "
     "beta = -LN(1-ER100)/P*. PROTOTYPE mode / BetaSet = PROTOTYPE keeps the old /100 divisor."),
    ("Bf", "Fuel-intensity semi-elasticity b_f (derived)", None, "1/($/tCO2)",
     "=SInt*LN(INDEX(CV_ind1,MATCH(BfScen,CV_Hdr,0))/INDEX(CV_ind0,MATCH(BfScen,CV_Hdr,0)))"
     "/INDEX(CV_cptraj,MATCH(BfScen,CV_Hdr,0))",
     "Replaces the untraceable -0.549%/2 per $ of the original (AF7). Fuel intensity factor xf = EXP(b_f * "
     "(carbon price + fund shadow price)); EG1 gives -0.00250 (original -0.00274)."),
    ("CBFyr", "CBAM phase-in factor in the reporting year (derived)", None, "-", "=INDEX(YV_CBF,MATCH(Yr,YV_Years,0))",
     "From section F (EU CBAM definitive-period phase-in: 2.5% 2026 .. 100% 2034)."),
    ("CBFsel", "Phase-in factor applied to the obligation under the selected convention", None, "-",
     '=IF(Conv="NOPHASE",1,CBFyr)', "NOPHASE -> 1; FULL / SCALED -> CBFyr."),
    ("Ssel", "Scale applied to the carbon-price deduction under the selected convention", None, "-",
     '=IF(Conv="SCALED",CBFyr,1)', "SCALED -> CBFyr; otherwise 1 (full deduction of the carbon price paid)."),
    ("BaseYr", "Base year of the product activity data Q0", 2024, "year", "=B{r}", "Prototype v0.11 Manual inputs."),
]
for nm, label, val, unit, eff, note in PARAMS:
    put(wsI, "A%d" % r, label, font=BOLD)
    if val is not None:
        put(wsI, "B%d" % r, val, fill=GREEN, align=CENTER)
    else:
        put(wsI, "B%d" % r, "(derived)", fill=GREY, align=CENTER)
    put(wsI, "C%d" % r, unit, align=CENTER)
    put(wsI, "D%d" % r, eff.format(r=r), fill=REVIEW, align=CENTER, fmt="0.00000" if nm in ("Bf",) else "General")
    put(wsI, "E%d" % r, nm, fill=BLUE)
    wsI.merge_cells("F%d:P%d" % (r, r))
    put(wsI, "F%d" % r, note, align=WRAP)
    wsI.row_dimensions[r].height = 30
    name(nm, "Inputs!$D$%d" % r)
    IN[nm] = r
    r += 1

# --- C. CPAT values in the reporting year --------------------------------------------------------------------
r += 1
section_band(wsI, r, "C. CPAT values in the reporting year (live lookups into CPAT_Outputs; nothing typed)", "P")
r += 1
header_row(wsI, r, ["Quantity", "CPAT code"] + SCENS + ["Unit", "Notes"])
wsI.merge_cells("H%d:P%d" % (r, r))
name("CV_Hdr", "Inputs!$C$%d:$F$%d" % (r, r))
IN["cv_hdr"] = r
r += 1
CV = {}
for label, code, unit, nm in CPAT_ROWS:
    put(wsI, "A%d" % r, label)
    put(wsI, "B%d" % r, code, fill=BLUE)
    for j, sc in enumerate(SCENS):
        cl = L(3 + j)
        put(wsI, "%s%d" % (cl, r), '=INDEX(CPO_Data,MATCH($B%d&"|"&%s$%d,CPO_Keys,0),MATCH(Yr,CPO_Years,0))'
            % (r, cl, IN["cv_hdr"]), fmt="#,##0.000")
    put(wsI, "G%d" % r, unit, align=CENTER)
    if nm:
        name(nm, "Inputs!$C$%d:$F$%d" % (r, r))
    CV[code] = r
    r += 1
first_fuel, last_fuel = CV["egy.mit.rev.new.coa.usd.2"], CV["egy.mit.rev.new.oil.usd.2"]
first_d, last_d = CV["egy.air.ada.2464"], CV["egy.air.ada.u24"]
DERIVED = [
    ("CV_revctax", "Carbon-tax revenue, six fuels (derived)", "=SUM({c}%d:{c}%d)" % (first_fuel, last_fuel), "$bn",
     "Gross carbon-tax receipts of the CPAT run (post-response). Replaces the original 'price x 2026 covered "
     "emissions' (V7)."),
    ("CV_deaths", "Air-pollution deaths avoided, all ages (derived)", "=SUM({c}%d:{c}%d)" % (first_d, last_d), "deaths",
     "CPAT's own estimate for the scenario and year."),
    ("CV_kappa", "Coverage factor kappa of the CPAT run (derived)",
     '=IF(KappaMode="ONE",1,IFERROR(MIN(1,({c}%d/{c}%d)*{c}%d/{c}%d),1))'
     % (CV["egy.mit.eff.cptraj.2"], CV["egy.mit.cptraj.2"], CV["egy.mit.co2.enr.tot.1"], CV["egy.mit.co2.ind.1"]),
     "-", "Share of industrial energy CO2 actually priced in the CPAT run (eff.cptraj is coverage-weighted over "
     "energy CO2). SCALE keeps this raw kappa for 1/kappa adjustments; ONE forces 1."),
    ("CV_dghg", "Delta total GHG, policy - baseline (derived)", "={c}%d-{c}%d" % (CV["egy.mit.ghg.tot.inc.2"],
     CV["egy.mit.ghg.tot.inc.1"]), "MtCO2e", "Single base: policy minus baseline in the reporting year."),
    ("CV_dippu", "Delta IPPU GHG (derived)", "={c}%d-{c}%d" % (CV["egy.mit.ghg.ipr.tot.2"], CV["egy.mit.ghg.ipr.tot.1"]),
     "MtCO2e", "CPAT's IPPU response (scaled with industrial energy CO2; MajorIssues #17)."),
    ("CV_denr", "Delta energy CO2 (derived)", "={c}%d-{c}%d" % (CV["egy.mit.co2.enr.tot.2"], CV["egy.mit.co2.enr.tot.1"]),
     "MtCO2", "Drives air-pollution deaths."),
    ("CV_dind", "Delta industry energy CO2 (derived)", "={c}%d-{c}%d" % (CV["egy.mit.co2.ind.2"], CV["egy.mit.co2.ind.1"]),
     "MtCO2", "Intensity share s_int, output share 1 - s_int (TechNote App. A)."),
    ("CV_drev", "Delta net new revenue, policy - baseline (derived)", "={c}%d-{c}%d" % (CV["egy.mit.rev.new.usd.2"],
     CV["egy.mit.rev.new.usd.1"]), "$bn", "PolicyMatrix column AR (was 10.62 for 2A = EG2 value; MajorIssues #6)."),
]
for nm, label, f, unit, note in DERIVED:
    put(wsI, "A%d" % r, label, font=BOLD)
    put(wsI, "B%d" % r, nm, fill=BLUE)
    for j in range(4):
        cl = L(3 + j)
        put(wsI, "%s%d" % (cl, r), f.format(c=cl), fmt="#,##0.000", fill=REVIEW)
    put(wsI, "G%d" % r, unit, align=CENTER)
    wsI.merge_cells("H%d:P%d" % (r, r))
    put(wsI, "H%d" % r, note, align=WRAP)
    name(nm, "Inputs!$C$%d:$F$%d" % (r, r))
    CV[nm] = r
    r += 1
IN["cv_last"] = r - 1

# --- D. Policy bundles ----------------------------------------------------------------------------------------
r += 1
section_band(wsI, r, "D. Policy bundles (scenario mapping and instrument settings)", "P")
r += 1
header_row(wsI, r, ["Bundle", "CPAT scenario", "Scope (ALL/IND)", "Process priced (1/0)", "theta: OBR rebate share",
                    "phi: fund share of net revenue", "tau: carbon price in Yr ($/t)", "Recycling", "Trajectory",
                    "Notes"])
wsI.merge_cells("J%d:P%d" % (r, r))
wsI.row_dimensions[r].height = 40
r += 1
IN["bt_first"] = r
BT_NOTES = {
    "1A": "Economy-wide fuel levy (EG1) + CBAM process emissions priced. Original used EG2 values (MajorIssues #3).",
    "2A": "Economy-wide fuel levy (EG1), process not priced.",
    "2B": "As 2A with household transfers (EG2).",
    "3A": "Industry-only price (EG3): industrial energy CO2 + CBAM process emissions.",
    "3B": "3A + output-based rebate for CBAM producers (theta = 1: benchmark = own baseline intensity). Built from "
          "EG3 with OBR logic; EG4 (feebate run) is unusable (MajorIssues #8).",
    "3C": "3A with net revenue paid into an abatement fund (phi = 1) acting as shadow price sigma (Inputs A).",
}
for code_, scen, scope, flag, theta, phi, recyc, traj in BUNDLE_TBL:
    put(wsI, "A%d" % r, code_, font=BOLD, fill=BLUE)
    put(wsI, "B%d" % r, scen, fill=GREEN, align=CENTER)
    put(wsI, "C%d" % r, scope, fill=GREEN, align=CENTER)
    put(wsI, "D%d" % r, flag, fill=GREEN, align=CENTER)
    put(wsI, "E%d" % r, theta, fill=GREEN, align=CENTER)
    put(wsI, "F%d" % r, phi, fill=GREEN, align=CENTER)
    put(wsI, "G%d" % r, "=INDEX(CV_cptraj,MATCH(B%d,CV_Hdr,0))" % r, fmt="0.00", align=CENTER)
    put(wsI, "H%d" % r, recyc, fill=GREEN)
    put(wsI, "I%d" % r, traj, fill=GREEN, align=CENTER)
    wsI.merge_cells("J%d:P%d" % (r, r))
    put(wsI, "J%d" % r, BT_NOTES[code_], align=WRAP)
    wsI.row_dimensions[r].height = 30
    r += 1
IN["bt_last"] = r - 1
for nm, cl in [("BT_Code", "A"), ("BT_Scen", "B"), ("BT_Scope", "C"), ("BT_Flag", "D"), ("BT_Theta", "E"),
               ("BT_Phi", "F"), ("BT_Tau", "G"), ("BT_Recyc", "H"), ("BT_Traj", "I")]:
    name(nm, "Inputs!$%s$%d:$%s$%d" % (cl, IN["bt_first"], cl, IN["bt_last"]))

# --- E. CBAM products ------------------------------------------------------------------------------------------
r += 1
section_band(wsI, r, "E. CBAM products (activity, trade, prices from prototype v0.11 Manual inputs; emission factors "
                     "Egypt CBAM EF v0.1; process half-elasticity sets from TASK-D)", "U")
r += 1
header_row(wsI, r, ["Product", "Q0 output in BaseYr (kt)", "g: output growth /yr", "X: EU exports (kt)",
                    "P: price ($/t)", "fc: fuel combustion (tCO2/t) EF v0.1", "fp: fuel-based process (tCO2/t) EF v0.1",
                    "np: non-fuel process (tCO2/t) EF v0.1", "no: non-CO2 process (tCO2e/t) EF v0.1",
                    "F = fc + fp (selected EF set)", "G = max(np,0) + max(no,0) (selected EF set)", "ER100: prototype",
                    "ER100: IPCC central", "ER100: IPCC 2030 horizon", "ER100: IPCC long-run", "ER100: selected set",
                    "beta = -LN(1-ER100)/100", "fc prototype v0.11", "fp prototype v0.11", "np prototype v0.11",
                    "no prototype v0.11"])
wsI.row_dimensions[r].height = 54
r += 1
IN["pt_first"] = r
for row_ in PRODUCT_TBL:
    nm_, q0, g, x, p, fc, fp, np_, no, e_pro, e_cen, e_30, e_lr, pfc, pfp, pnp, pno = row_
    put(wsI, "A%d" % r, nm_, font=BOLD, fill=BLUE)
    for cl, v, fmt in [("B", q0, "#,##0"), ("C", g, "0.0%"), ("D", x, "#,##0"), ("E", p, "#,##0"),
                       ("F", fc, "0.0000"), ("G", fp, "0.0000"), ("H", np_, "0.000"), ("I", no, "0.000"),
                       ("L", e_pro, "0.0%"), ("M", e_cen, "0.00%"), ("N", e_30, "0.00%"), ("O", e_lr, "0.00%")]:
        put(wsI, "%s%d" % (cl, r), v, fill=GREEN, fmt=fmt)
    for cl, v in [("R", pfc), ("S", pfp), ("T", pnp), ("U", pno)]:
        put(wsI, "%s%d" % (cl, r), v, fill=GREY, fmt="0.0000")
    put(wsI, "J%d" % r, '=IF(EFSet="PROTOTYPE",R{r}+S{r},F{r}+G{r})'.format(r=r), fmt="0.0000")
    put(wsI, "K%d" % r, '=IF(EFSet="PROTOTYPE",MAX(T{r},0)+MAX(U{r},0),MAX(H{r},0)+MAX(I{r},0))'.format(r=r),
        fmt="0.0000")
    put(wsI, "P%d" % r, '=IF(BetaSet="PROTOTYPE",L{r},IF(BetaSet="IPCC_2030",N{r},IF(BetaSet="IPCC_LONGRUN",O{r},M{r})))'
        .format(r=r), fmt="0.00%", fill=REVIEW)
    put(wsI, "Q%d" % r, '=IF(BetaSet="PROTOTYPE",-LN(1-P%d)/100,-LN(1-P%d)/PStar)' % (r, r), fmt="0.00000", fill=REVIEW)
    r += 1
IN["pt_last"] = r - 1
for nm, cl in [("PT_Name", "A"), ("PT_Q0", "B"), ("PT_Growth", "C"), ("PT_X", "D"), ("PT_P", "E"), ("PT_FuelFac", "J"),
               ("PT_ProcFac", "K"), ("PT_ER", "P"), ("PT_Beta", "Q")]:
    name(nm, "Inputs!$%s$%d:$%s$%d" % (cl, IN["pt_first"], cl, IN["pt_last"]))
wsI.merge_cells("A%d:U%d" % (r, r))
put(wsI, "A%d" % r, "ER100 = emission-intensity reduction at $100/tCO2. Prototype values are the v0.11 placeholders; "
    "IPCC sets are the TASK-D drop-in (AR6 WGIII Ch.11 / IEA sectoral MACC bands); AN = N2O-weighted blend of the "
    "unabated (0.721) and abated (0.329) rows at the EF workbook's 50 % HNO3 N2O abatement share. EF v0.1 = "
    "EGY_CBAM_EF_v0.1.xlsx Products!D:G (CBAM conventions; urea np = 0 under the CBAM rule; AN 'no' = integrated "
    "HNO3 N2O, kernel convention). For IPCC sets beta = -LN(1-ER100)/PStar (PStar default 122 USD2024/t); "
    "the PROTOTYPE set keeps -LN(1-ER100)/100. Prototype v0.11 EFs (R:U, grey) are used when EFSet = PROTOTYPE "
    "(urea np -0.733 enters G as 0).", font=ITALIC, align=WRAP, border=False)
wsI.row_dimensions[r].height = 30
r += 1

# --- F. Year vectors --------------------------------------------------------------------------------------------
r += 1
section_band(wsI, r, "F. Year vectors 2022-2041", "U")
r += 1
header_row(wsI, r, ["Vector"] + YEARS)
name("YV_Years", "Inputs!$B$%d:$U$%d" % (r, r))
IN["yv_hdr"] = r
r += 1
put(wsI, "A%d" % r, "CBAM phase-in factor CBF (EU definitive period)", font=BOLD)
for j, y in enumerate(YEARS):
    v = 0 if y < 2026 else (1 if y >= 2034 else CBF_PATH[y])
    put(wsI, "%s%d" % (L(2 + j), r), v, fill=GREEN, fmt="0.0%")
name("YV_CBF", "Inputs!$B$%d:$U$%d" % (r, r))
r += 1
put(wsI, "A%d" % r, "Price trajectory 1 'flat' ($20 from 2028; label check only)", font=BOLD)
for j, y in enumerate(YEARS):
    put(wsI, "%s%d" % (L(2 + j), r), 20 if y >= 2028 else 0, fill=GREEN, fmt="0.0")
name("YV_FLAT", "Inputs!$B$%d:$U$%d" % (r, r))
r += 1
put(wsI, "A%d" % r, "Price trajectory 2 'rising' = CPAT EG3 cptraj.2 (live)", font=BOLD)
for j, y in enumerate(YEARS):
    put(wsI, "%s%d" % (L(2 + j), r), '=INDEX(CPO_Data,MATCH("egy.mit.cptraj.2|EG3",CPO_Keys,0),MATCH(%s$%d,CPO_Years,0))'
        % (L(2 + j), IN["yv_hdr"]), fmt="0.0")
name("YV_RAMP", "Inputs!$B$%d:$U$%d" % (r, r))
r += 1
put(wsI, "A%d" % r, "Memo: CPAT EG1 cptraj.2 (live; should equal trajectory 1)", font=ITALIC)
for j, y in enumerate(YEARS):
    put(wsI, "%s%d" % (L(2 + j), r), '=INDEX(CPO_Data,MATCH("egy.mit.cptraj.2|EG1",CPO_Keys,0),MATCH(%s$%d,CPO_Years,0))'
        % (L(2 + j), IN["yv_hdr"]), fmt="0.0")
name("YV_EG1", "Inputs!$B$%d:$U$%d" % (r, r))
IN["last"] = r
wsI.freeze_panes = "B6"

# ================================================================================================================
# Sheet 3: CPAT_Outputs (data only)
# ================================================================================================================
wsC = wb.create_sheet("CPAT_Outputs")
widths(wsC, {"A": 30, "B": 10, "C": 34, "D": 48})
for j in range(len(YEARS)):
    wsC.column_dimensions[L(5 + j)].width = 9.5
title_band(wsC, "CPAT_Outputs - trimmed CPAT 'Outputs' sheet (Egypt, scenarios EG1..EG4, 2022-2041)", "X")
wsC.merge_cells("A2:X2")
put(wsC, "A2", "Provenance: CPAT Outputs sheet read via Excel COM (cpat_outputs_egypt_2022_2041.csv in this folder). "
    "Values are static data; the rest of the workbook reads them via INDEX/MATCH on the key column C (= code|scenario) "
    "and the year header. Mt for emissions, $bn for revenues, $/tCO2 for prices, deaths for air pollution.",
    font=ITALIC, align=WRAP, border=False)
wsC.row_dimensions[2].height = 30
header_row(wsC, 3, ["CPAT code", "Scenario", "Key (code|scenario)", "Label"] + YEARS, fill=BLUE)
for i, row_ in enumerate(CSV_DATA):
    rr = 4 + i
    put(wsC, "A%d" % rr, row_[0], fill=BLUE)
    put(wsC, "B%d" % rr, row_[1], fill=BLUE, align=CENTER)
    put(wsC, "C%d" % rr, row_[2], fill=BLUE)
    put(wsC, "D%d" % rr, row_[3])
    for j in range(len(YEARS)):
        v = row_[4 + j]
        try:
            v = float(v)
        except ValueError:
            pass
        put(wsC, "%s%d" % (L(5 + j), rr), v, fmt="#,##0.000")
CPO_LAST = 4 + len(CSV_DATA) - 1
name("CPO_Keys", "CPAT_Outputs!$C$4:$C$%d" % CPO_LAST)
name("CPO_Data", "CPAT_Outputs!$E$4:$X$%d" % CPO_LAST)
name("CPO_Years", "CPAT_Outputs!$E$3:$X$3")
wsC.freeze_panes = "E4"

# ================================================================================================================
# Sheet 4: CBAM_Products - six stacked blocks (prototype v0.11 engine, extended by xf / beta set / fund)
# ================================================================================================================
wsB = wb.create_sheet("CBAM_Products")
widths(wsB, {"A": 20})
for j in range(2, 49):
    wsB.column_dimensions[L(j)].width = 10.5
title_band(wsB, "CBAM_Products - product-level engine, one block per bundle (eight CBAM goods)", "AV")
wsB.merge_cells("A2:AV2")
put(wsB, "A2", "Each block: row 1 scalars (from Inputs), rows 2-9 products, row 10 totals. Units: Q kt, emissions "
    "MtCO2(e), revenues and rebates $m, prices $/t, obligations $/t of product. Formulas are the prototype's "
    "(cost pass-through dp -> output Q = Qb(1+dp)^eps; process intensity via beta; CBAM obligation per tonne "
    "obl = MAX(0, CBF*P_EU*EI - S*MAX(0,d)) with d = carbon price paid net of rebate per tonne) plus the "
    "fuel-intensity factor xf (REBUILD only; = 1 in PROTOTYPE mode).", font=ITALIC, align=WRAP, border=False)
wsB.row_dimensions[2].height = 42
SCALAR_LABELS = ["Bundle", "tau: carbon price", "tau_p: process price", "obrrb: OBR rebate rate", "fundsp: fund shadow price",
                 "incl_f", "incl_p", "xf: fuel-intensity factor", "CBF (selected conv.)", "P_EU", "S (selected conv.)",
                 "CBF (FULL)", "CBF (NOPHASE)", "Year", "CPAT scenario", "b_f", "beta set", "Mode"]
PROD_HDR = ["Product", "Q0 (kt)", "g", "X exports (kt)", "P ($/t)", "F (tCO2/t)", "G (tCO2e/t)", "beta",
            "Qb: baseline output", "kf: fuel cost $/t", "kp: process cost $/t", "m: rebate $/t", "dp: cost/price",
            "Q: output", "Ef: fuel emis.", "Ep: process emis.", "ER_f: fuel-int. resp.", "ER_p: process-int. resp.",
            "post fuel", "post process", "post total", "emrq_i: output ch.", "emrq_proc_i", "J_i: process>0",
            "revf_i $m", "revp_i $m", "rev_i $m", "rebate_i $m", "EI: tCO2/t", "d: net price paid $/t",
            "obl (sel.) $/t", "obl (FULL) $/t", "obl (NOPHASE) $/t", "cbobl_i $m", "cbobl0_i $m",
            "w_den sel", "w_den FULL", "w_den NOPHASE", "w_num sel", "w_num FULL", "w_num NOPHASE",
            "X*post/Q", "X*(Ef+Ep)/Q", "X*covered/Q", "covered_i", "Ebase_i", "Efbase_i", "Epbase_i"]
assert len(PROD_HDR) == 48
BLK = {}
BLOCK_H = 16
for b, code_ in enumerate(BUNDLES):
    r0 = 4 + BLOCK_H * b
    s = r0 + 2
    section_band(wsB, r0, "Bundle %s  -  %s" % (code_, BT_NOTES[code_]), "AV")
    header_row(wsB, r0 + 1, SCALAR_LABELS)
    wsB.row_dimensions[r0 + 1].height = 30
    mt = "MATCH($A$%d,BT_Code,0)" % s
    scal = [code_, "=INDEX(BT_Tau,%s)" % mt, "=B{s}*INDEX(BT_Flag,%s)" % mt, "=INDEX(BT_Theta,%s)*B{s}" % mt,
            "=INDEX(BT_Phi,%s)*SigmaEff" % mt, 1, "=INDEX(BT_Flag,%s)" % mt,
            '=IF(Mode="PROTOTYPE",1,EXP(Bf*(F{s}*B{s}+E{s})))', "=CBFsel", "=PEU", "=Ssel", "=CBFyr", 1, "=Yr",
            "=INDEX(BT_Scen,%s)" % mt, "=Bf", "=BetaSet", "=Mode"]
    for j, v in enumerate(scal):
        if isinstance(v, str):
            v = v.format(s=s)
        put(wsB, "%s%d" % (L(1 + j), s), v, fill=(BLUE if j == 0 else REVIEW), align=CENTER,
            fmt="0.0000" if j in (7,) else "General")
    header_row(wsB, r0 + 3, PROD_HDR)
    wsB.row_dimensions[r0 + 3].height = 54
    first, last = r0 + 4, r0 + 11
    for i in range(8):
        rr = first + i
        pr = IN["pt_first"] + i
        F = dict(r=rr, s=s)
        cells = {
            "A": "=Inputs!$A$%d" % pr, "B": "=Inputs!$B$%d" % pr, "C": "=Inputs!$C$%d" % pr, "D": "=Inputs!$D$%d" % pr,
            "E": "=Inputs!$E$%d" % pr, "F": "=Inputs!$J$%d" % pr, "G": "=Inputs!$K$%d" % pr, "H": "=Inputs!$Q$%d" % pr,
            "I": "=B{r}*(1+C{r})^($N${s}-BaseYr)", "J": "=$F${s}*$B${s}*F{r}", "K": "=$G${s}*$C${s}*G{r}",
            "L": "=MIN($D${s},$B${s})*$F${s}*F{r}+MIN($D${s},$C${s})*$G${s}*G{r}",
            "M": "=IF(E{r}>0,(J{r}+K{r}-L{r})/E{r},0)", "N": "=I{r}*(1+M{r})^EpsQ", "O": "=N{r}*F{r}/1000",
            "P": "=N{r}*G{r}/1000", "Q": "=O{r}*($H${s}-1)", "R": "=-P{r}*(1-EXP(-H{r}*($G${s}*$C${s}+$E${s})))",
            "S": "=O{r}+Q{r}", "T": "=P{r}+R{r}", "U": "=S{r}+T{r}", "V": "=(O{r}+P{r})*(1-(1+M{r})^(-EpsQ))",
            "W": "=P{r}*(1-(1+M{r})^(-EpsQ))", "X": "=IF(G{r}>0,1,0)", "Y": "=S{r}*$F${s}*$B${s}",
            "Z": "=(P{r}*X{r}+R{r})*$G${s}*$C${s}", "AA": "=Y{r}+Z{r}", "AB": "=L{r}*N{r}/1000",
            "AC": "=IF(N{r}>0,U{r}*1000/N{r},0)", "AD": "=IF(N{r}>0,AA{r}*1000/N{r}-L{r},0)",
            "AE": "=MAX(0,$I${s}*$J${s}*AC{r}-$K${s}*MAX(0,AD{r}))", "AF": "=MAX(0,$L${s}*$J${s}*AC{r}-MAX(0,AD{r}))",
            "AG": "=MAX(0,$M${s}*$J${s}*AC{r}-MAX(0,AD{r}))", "AH": "=IF(B{r}>0,D{r}*N{r}/B{r}*AE{r}/1000,0)",
            "AI": "=D{r}*(1+C{r})^($N${s}-BaseYr)*$I${s}*$J${s}*(F{r}+G{r})/1000",
            "AJ": "=D{r}*$I${s}*$J${s}*(F{r}+G{r})", "AK": "=D{r}*$L${s}*$J${s}*(F{r}+G{r})",
            "AL": "=D{r}*$M${s}*$J${s}*(F{r}+G{r})", "AM": "=D{r}*AE{r}", "AN": "=D{r}*AF{r}", "AO": "=D{r}*AG{r}",
            "AP": "=IF(N{r}>0,D{r}*U{r}/N{r},0)", "AQ": "=IF(N{r}>0,D{r}*(O{r}+P{r})/N{r},0)",
            "AR": "=IF(N{r}>0,D{r}*AS{r}/N{r},0)", "AS": "=O{r}*IF($F${s}>0,1,0)+P{r}*X{r}*IF($G${s}>0,1,0)",
            "AT": "=I{r}*(F{r}+G{r})/1000", "AU": "=I{r}*F{r}/1000", "AV": "=I{r}*G{r}/1000",
        }
        for cl, f in cells.items():
            put(wsB, "%s%d" % (cl, rr), f.format(**F), fmt="#,##0.0000", fill=(BLUE if cl == "A" else None))
    tot = r0 + 12
    put(wsB, "A%d" % tot, "Total", font=BOLD, fill=GREY)
    for cl in ["I", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "Z", "AA", "AB", "AH", "AI", "AJ", "AK", "AL",
               "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV"]:
        put(wsB, "%s%d" % (cl, tot), "=SUM(%s%d:%s%d)" % (cl, first, cl, last), fmt="#,##0.0000", font=BOLD, fill=GREY)
    BLK[code_] = dict(sc=s, first=first, last=last, tot=tot)
wsB.freeze_panes = "B4"

# ================================================================================================================
# Sheet 5: Results - the engine (everything PolicyMatrix / Comparison / Checks read)
# ================================================================================================================
wsR = wb.create_sheet("Results")
widths(wsR, {"A": 58, "B": 16, "C": 12, "D": 12, "E": 12, "F": 12, "G": 12, "H": 12, "I": 10, "J": 90})
title_band(wsR, "Results - engine: block totals, block metrics, CPAT national quantities and metric composition", "J")
wsR.merge_cells("A2:J2")
put(wsR, "A2", "Columns C..H = bundles. Keys (column B) are referenced by PolicyMatrix, Comparison and Checks via "
    "INDEX/MATCH. Block quantities come from CBAM_Products; national quantities from Inputs section C (CPAT). "
    "Mode / convention indicator: see row 3.", font=ITALIC, align=WRAP, border=False)
wsR.merge_cells("A3:J3")
put(wsR, "A3", '="Mode = "&Mode&"   |   CBAM convention = "&Conv&"   |   reporting year = "&Yr&"   |   beta set = "'
    '&BetaSet&"   |   sigma = "&SigmaEff&" $/t"', font=BOLD, fill=REVIEW, border=False)
header_row(wsR, 4, ["Metric", "Key"] + BUNDLES + ["Unit", "Definition / formula"])
RES = {}
RROW = [5]
TOKEN = re.compile(r"@(\w+)@")


def res(key, label, tmpl, unit, defn, fmt="#,##0.0000", fill=None, bold=False):
    row = RROW[0]
    put(wsR, "A%d" % row, label, font=(BOLD if bold else ARIAL))
    put(wsR, "B%d" % row, key, fill=BLUE)
    for b, code_ in enumerate(BUNDLES):
        c = L(3 + b)
        f = TOKEN.sub(lambda m: "%s%d" % (c, RES[m.group(1)]), tmpl)
        f = f.replace("{sc}", str(BLK[code_]["sc"])).replace("{tot}", str(BLK[code_]["tot"])).replace("{c}", c)
        put(wsR, "%s%d" % (c, row), f, fmt=fmt, fill=fill, align=Alignment(horizontal="right"))
    put(wsR, "I%d" % row, unit, align=CENTER)
    put(wsR, "J%d" % row, defn, align=WRAP)
    RES[key] = row
    RROW[0] += 1
    return row


def res_band(text):
    section_band(wsR, RROW[0], text, "J")
    RROW[0] += 1


res_band("1. Bundle settings")
res("scen", "CPAT scenario used", "=INDEX(BT_Scen,MATCH({c}$4,BT_Code,0))", "-", "Inputs section D.", fmt="General")
res("scope", "Scope of the fuel levy", "=INDEX(BT_Scope,MATCH({c}$4,BT_Code,0))", "-", "ALL = economy-wide, IND = industry only.", fmt="General")
res("flag", "Process emissions priced (1/0)", "=INDEX(BT_Flag,MATCH({c}$4,BT_Code,0))", "-", "Inputs section D.", fmt="0")
res("theta", "theta: OBR rebate share", "=INDEX(BT_Theta,MATCH({c}$4,BT_Code,0))", "-", "1 = output-based rebate at the firm's baseline intensity (3B).", fmt="0.00")
res("phi", "phi: fund share of net revenue", "=INDEX(BT_Phi,MATCH({c}$4,BT_Code,0))", "-", "1 = all net revenue to the abatement fund (3C).", fmt="0.00")
res("tau", "tau: carbon price in the reporting year", "=CBAM_Products!$B${sc}", "$/tCO2", "CPAT cptraj.2 of the scenario (block scalar B).", fmt="0.00")
res("taup", "tau_p: price on process emissions", "=CBAM_Products!$C${sc}", "$/tCO2", "tau x process flag.", fmt="0.00")
res("obrrb", "OBR rebate rate", "=CBAM_Products!$D${sc}", "$/tCO2", "theta x tau.", fmt="0.00")
res("fundsp", "Fund shadow price applied in the block", "=CBAM_Products!$E${sc}", "$/tCO2", "phi x sigma (0 in PROTOTYPE mode).", fmt="0.00")
res("xf", "xf: fuel-intensity factor", "=CBAM_Products!$H${sc}", "-", "EXP(b_f (tau + fundsp)); 1 in PROTOTYPE mode.", fmt="0.00000")

res_band("2. CBAM block totals (eight products; Mt CO2e, $m)")
for key, cl_, label, unit, defn in [
    ("Ebase", "AT", "E_base: block emissions at baseline output and intensity", "Mt", "Sum Qb (F+G)/1000; 62.424 in 2030 with EF v0.1 (prototype EFs: 61.157)."),
    ("Efbase", "AU", "E_base fuel part", "Mt", "Sum Qb F/1000."), ("Epbase", "AV", "E_base process part", "Mt", "Sum Qb G/1000."),
    ("Qb", "I", "Baseline output", "kt", "Sum Q0 (1+g)^(Yr-BaseYr)."), ("Q", "N", "Output after response", "kt", "Sum Qb (1+dp)^eps."),
    ("Ef", "O", "Fuel emissions at post-response output, baseline intensity", "Mt", ""),
    ("Ep", "P", "Process emissions at post-response output, baseline intensity", "Mt", ""),
    ("ERf", "Q", "ER_f: fuel-intensity response", "Mt", "Ef (xf - 1); 0 in PROTOTYPE mode."),
    ("ERp", "R", "ER_p: process-intensity response", "Mt", "-Ep (1 - EXP(-beta (tau_p + fundsp)))."),
    ("emisf", "S", "Post-response fuel emissions", "Mt", "Ef + ER_f."), ("emisp", "T", "Post-response process emissions", "Mt", "Ep + ER_p."),
    ("emis", "U", "Post-response block emissions", "Mt", "emisf + emisp."),
    ("emrq", "V", "emrq: output-channel reduction (fuel + process)", "Mt", "Sum (Ef+Ep)(1-(1+dp)^-eps) (negative = reduction)."),
    ("emrq_proc", "W", "emrq (process part)", "Mt", "Sum Ep (1-(1+dp)^-eps)."),
    ("revf", "Y", "Carbon revenue on fuel emissions", "$m", "(Ef+ER_f) tau."), ("revp", "Z", "Carbon revenue on process emissions", "$m", "(Ep J + ER_p) tau_p."),
    ("rev", "AA", "Block carbon revenue", "$m", "revf + revp."), ("rebate", "AB", "OBR rebate paid to block producers", "$m", "Sum m Q/1000."),
    ("cbobl", "AH", "CBAM obligation on EU exports (selected convention)", "$m", "Sum X Q/Q0 obl/1000."),
    ("cbobl0", "AI", "CBAM obligation with no domestic policy", "$m", "Sum X (1+g)^t CBF P_EU (F+G)/1000."),
    ("covered", "AS", "Block emissions covered by the carbon price", "Mt", "Fuel if incl_f, process if incl_p and G>0."),
]:
    res(key, label, "=CBAM_Products!$%s${tot}" % cl_, unit, defn)
res("emr", "emr: intensity-channel reduction (fuel + process)", "=@ERf@+@ERp@", "Mt", "ER_f + ER_p.")
res("emrt", "emrt: total block reduction (output + intensity)", "=@emrq@+@emr@", "Mt", "emrq + emr.")

res_band("3. CBAM block metrics (prototype v0.11 definitions)")
res("cbcov", "cbcov: CBAM coverage (share of block emissions priced)", "=@covered@/(@Ef@+@Ep@)", "-", "PolicyMatrix M.", fmt="0.0000")
res("cbcovx", "cbcovx: coverage, export-weighted", "=CBAM_Products!$AR${tot}/CBAM_Products!$AQ${tot}", "-", "Memo.", fmt="0.0000")
res("cbintch", "cbintch: emissions-intensity change of the block", "=@emis@/(@Ef@+@Ep@)-1", "-", "PolicyMatrix N.", fmt="0.0000")
res("cbintchx", "cbintchx: intensity change, export-weighted", "=CBAM_Products!$AP${tot}/CBAM_Products!$AQ${tot}-1", "-", "PolicyMatrix AN.", fmt="0.0000")
res("cbqch", "cbqch: output-channel reduction / E_base", "=@emrq@/@Ebase@", "-", "PolicyMatrix U (industrial output change).", fmt="0.0000")
res("emrt_pct", "emrt / E_base: total block emissions change", "=@emrt@/@Ebase@", "-", "PolicyMatrix T.", fmt="0.0000")
res("cbint", "cbint: block emissions intensity after response", "=@emis@*1000/@Q@", "tCO2e/t", "Memo.", fmt="0.0000")
res("cbobch", "cbobch: change in CBAM obligation (incl. export volume change)", "=@cbobl@/@cbobl0@-1", "-", "Memo.", fmt="0.0000")
res("cbobchu", "cbobchu: change in CBAM obligation per unit exported (selected convention)",
    "=CBAM_Products!$AM${tot}/CBAM_Products!$AJ${tot}-1", "-", "PolicyMatrix O.", fmt="0.0000")
res("cbobchu_full", "cbobchu under FULL (2030 phase-in on obligation, full deduction)",
    "=CBAM_Products!$AN${tot}/CBAM_Products!$AK${tot}-1", "-", "PolicyMatrix AQ.", fmt="0.0000")
res("cbobchu_nophase", "cbobchu under NOPHASE (no phase-in)",
    "=CBAM_Products!$AO${tot}/CBAM_Products!$AL${tot}-1", "-", "Memo.", fmt="0.0000")

res_band("4. CPAT national quantities for the bundle's scenario, reporting year (Inputs section C)")
for key, nm_, label, unit in [
    ("ghg0", "CV_ghg0", "Total GHG incl. LULUCF - baseline", "Mt"), ("ghg1", "CV_ghg1", "Total GHG incl. LULUCF - policy", "Mt"),
    ("ippu0", "CV_ippu0", "IPPU GHG - baseline", "Mt"), ("ippu1", "CV_ippu1", "IPPU GHG - policy", "Mt"),
    ("enr0", "CV_enr0", "Energy CO2 - baseline", "Mt"), ("enr1", "CV_enr1", "Energy CO2 - policy", "Mt"),
    ("ind0", "CV_ind0", "Industry energy CO2 - baseline", "Mt"), ("ind1", "CV_ind1", "Industry energy CO2 - policy", "Mt"),
    ("dghg", "CV_dghg", "Delta total GHG (CPAT)", "Mt"), ("dippu", "CV_dippu", "Delta IPPU (CPAT)", "Mt"),
    ("denr", "CV_denr", "Delta energy CO2 (CPAT)", "Mt"), ("dind", "CV_dind", "Delta industry energy CO2 (CPAT)", "Mt"),
    ("kappa", "CV_kappa", "kappa: coverage factor of the CPAT run", "-"), ("revctax", "CV_revctax", "Carbon-tax revenue, six fuels (CPAT)", "$bn"),
    ("deaths", "CV_deaths", "Air-pollution deaths avoided (CPAT)", "deaths"), ("mort", "CV_mort", "Baseline air-pollution deaths (CPAT)", "deaths"),
    ("drev", "CV_drev", "Delta net new revenue (CPAT)", "$bn"),
]:
    res(key, label, "=INDEX(%s,MATCH(@scen@,CV_Hdr,0))" % nm_, unit, "CPAT code row '%s' for the bundle's scenario." % nm_)

res_band("5. Composition of the Table-2 metrics (REBUILD method; PROTOTYPE mode changes only the block)")
res("scale_active", "SCALE active (1 = approximating full-coverage EG3)", '=IF(AND(KappaMode="SCALE",@kappa@<0.999999),1,0)', "-",
    "Only runs with kappa < 1 are scaled; EG1/EG2 are numerically unchanged.", fmt="0")
res("scale_fac", "Full-coverage scale factor for partial industry runs", '=IF(@scale_active@=1,1/@kappa@,1)', "-",
    "SCALE approximation factor (1/kappa); 1 otherwise.", fmt="0.0000")
res("dind_adj", "Delta industry energy CO2 after SCALE adjustment", "=@dind@*@scale_fac@", "Mt",
    "DeltaIndCO2_adj = DeltaIndCO2/kappa under SCALE.")
res("denr_adj", "Delta energy CO2 after SCALE adjustment", "=@denr@+(@scale_fac@-1)*@dind@", "Mt",
    "DeltaEnergyCO2_adj = DeltaEnergyCO2 + (1/kappa - 1) DeltaIndCO2 under SCALE.")
res("dippu_adj", "Delta IPPU after SCALE adjustment", "=@dippu@*@scale_fac@", "Mt",
    "DeltaIPPU_adj = DeltaIPPU/kappa under SCALE.")
res("dghg_adj", "Delta total GHG after SCALE adjustment", "=@dghg@+(@scale_fac@-1)*(@dind@+@dippu@)", "Mt",
    "DeltaGHG_adj = DeltaGHG + (1/kappa - 1)(DeltaIndCO2 + DeltaIPPU) under SCALE.")
res("ind1_adj", "Industry energy CO2 policy level after SCALE adjustment", "=@ind0@+@dind_adj@", "Mt",
    "IndCO2_1_adj = IndCO2_0 + DeltaIndCO2_adj.")
res("Ef0_adj", "Fuel emissions covered by the levy after SCALE adjustment", '=IF(@scope@="ALL",@enr0@,IF(@scale_active@=1,@ind0@,@kappa@*@ind0@))', "Mt",
    "Coverage J uses kappa = 1 under SCALE; otherwise EnergyCO2 (ALL) or kappa x industry CO2 (IND).")
res("revctax_adj", "Carbon-tax revenue, six fuels after SCALE adjustment", "=@revctax@*@scale_fac@", "$bn",
    "SCALE approximation: CPAT carbon-tax receipts on fuels are multiplied by 1/kappa.")
res("ippu_other", "IPPU_other: response of non-CBAM IPPU", '=IF(IppuOther="CPAT",(1-@Epbase@/@ippu0@)*@dippu@,0)', "Mt",
    "0 unless IppuOther = CPAT (then CPAT's scaling of the non-block IPPU remainder is kept).")
res("w", "w: block share of the priced industrial fuel CO2", "=IF(ThetaOther=1,1,MIN(1,@Efbase@/@Ef0_adj@))", "-",
    "Weight of the OBR output-channel correction; under SCALE, w = E_f^base / IndCO2_0.", fmt="0.0000")
res("D_obr", "D_obr: output-channel reduction removed by the OBR", "=IF(@theta@>0,-(1-SInt)*@w@*@dind_adj@,0)", "Mt",
    "OBR neutralises the output share (1 - s_int) of the adjusted industrial fuel response for rebated producers (positive = less reduction).")
res("F_fund", "F_fund: extra fuel-intensity reduction bought by the fund outside the block", "=IF(@phi@>0,IF(@scale_active@=1,@ind1_adj@,@kappa@*@ind1@)*(EXP(Bf*@fundsp@)-1),0)", "Mt",
    "Adjusted IndCO2_1 (EXP(b_f sigma) - 1) under SCALE; otherwise kappa x IndCO2_1 as in v0.2. Block products already carry sigma through xf and beta.")
res("K", "K: total emissions reduction", "=@dghg_adj@-@dippu_adj@+@ippu_other@+@ERp@+@emrq_proc@+@D_obr@+@F_fund@", "Mt",
    "CPAT delta GHG minus CPAT's IPPU scaling, plus block process responses (intensity + output), OBR and fund terms. PolicyMatrix K.", bold=True)
res("L", "L: total reduction, % of baseline total GHG", "=@K@/@ghg0@", "-", "Single 2030 base (CPAT baseline incl. LULUCF). PolicyMatrix L.", fmt="0.0000")
res("Ef0", "Fuel emissions covered by the levy", "=@Ef0_adj@", "Mt", "Energy CO2 (ALL), kappa x industry energy CO2 (IND/AUTO), or full industry CO2 under SCALE.")
res("J", "J: emissions coverage, % of total GHG", "=(@Ef0@+@flag@*@Epbase@)/@ghg0@", "-", "Covered fuel CO2 plus priced block process emissions over baseline total GHG. PolicyMatrix J.", fmt="0.0000", bold=True)
res("J_int", "J as intended (kappa = 1: all industry priced)", '=(IF(@scope@="ALL",@enr0@,@ind0@)+@flag@*@Epbase@)/@ghg0@', "-", "Memo: coverage if the industry run had priced all industrial energy CO2.", fmt="0.0000")
res("M", "M: CBAM coverage", "=@cbcov@", "-", "PolicyMatrix M.", fmt="0.0000", bold=True)
res("N", "N: CBAM emissions-intensity reduction", "=@cbintch@", "-", "PolicyMatrix N.", fmt="0.0000", bold=True)
res("O", "O: CBAM obligations reduced per unit exported (selected convention)", "=@cbobchu@", "-", "PolicyMatrix O.", fmt="0.0000", bold=True)
res("O_full", "O under FULL convention", "=@cbobchu_full@", "-", "PolicyMatrix AQ.", fmt="0.0000")
res("O_nophase", "O under NOPHASE convention", "=@cbobchu_nophase@", "-", "Memo.", fmt="0.0000")
res("P_gross", "Gross carbon revenue", "=@revctax_adj@+@revp@/1000", "$bn", "CPAT carbon-tax receipts on fuels (scaled by 1/kappa under SCALE) + block process revenue. PolicyMatrix V / AO.")
res("rebate_other", "OBR rebate to non-CBAM priced industry", "=IF(AND(@theta@>0,ThetaOther=1),@tau@*(IF(@scale_active@=1,@ind1_adj@,@kappa@*@ind1@)-@emisf@)/1000,0)", "$bn", "Only if ThetaOther = 1.")
res("rebate_bn", "Total OBR rebates", "=@rebate@/1000+@rebate_other@", "$bn", "PolicyMatrix AP.")
res("P_net", "P: carbon revenues raised (net of rebates and fund)", "=(1-@phi@)*(@P_gross@-@rebate_bn@)", "$bn", "PolicyMatrix P.", bold=True)
res("fund_budget", "Fund budget (3C)", "=@phi@*(@P_gross@-@rebate@/1000)", "$bn", "phi x net revenue.")
res("fund_outlay", "Fund outlay upper bound (3C)", "=IF(@phi@>0,SigmaEff*ABS(@emr@+@F_fund@)/1000,0)", "$bn", "sigma x all intensity abatement (upper bound: pays sigma per tonne for all of it).")
res("Q_deaths", "Q: air-pollution deaths avoided", '=@deaths@*IF(@scope@="IND",(@denr_adj@+@D_obr@+@F_fund@)/@denr@,1)', "deaths",
    "CPAT deaths for the scenario, scaled by DeltaEnergyCO2_adj / DeltaEnergyCO2 under SCALE, then by OBR / fund energy-CO2 corrections. PolicyMatrix Q.", fmt="#,##0.0", bold=True)
res("R", "R: % of total air-pollution deaths", "=@Q_deaths@/@mort@", "-", "PolicyMatrix R.", fmt="0.0000")
res("T", "T: industrial (block) emissions change", "=@emrt_pct@", "-", "PolicyMatrix T.", fmt="0.0000")
res("U", "U: industrial (block) output change", "=@cbqch@", "-", "PolicyMatrix U.", fmt="0.0000")
res("AR", "AR: total change in net revenues (CPAT, less rebates / fund)", "=@drev@-(@P_gross@-@P_net@)", "$bn",
    "CPAT delta net new revenue of the scenario minus the part returned as OBR rebates or paid into the fund. PolicyMatrix AR.")
res("AB_cov", "Total covered emissions (fuel + priced process)", "=@Ef0@+@flag@*@Epbase@", "Mt", "PolicyMatrix AB.")
res("AE_cov", "Total covered CBAM emissions (pre-response)", "=@cbcov@*@Ebase@", "Mt", "PolicyMatrix AE.")
res("K_check", "K decomposition check (should be 0)", "=@dghg_adj@-@dippu_adj@+@ippu_other@+@ERp@+@emrq_proc@+@D_obr@+@F_fund@-@K@", "Mt", "PolicyMatrix AM.", fmt="0.000000")
RES_LAST = RROW[0] - 1
name("SumKeys", "Results!$B$5:$B$%d" % RES_LAST)
name("SumTbl", "Results!$C$5:$H$%d" % RES_LAST)
name("SumHdr", "Results!$C$4:$H$4")
wsR.freeze_panes = "C5"


def RLOOK(key, code_):
    """Formula fragment: Results value for key / bundle code (bundle code may be a cell ref)."""
    return 'INDEX(SumTbl,MATCH("%s",SumKeys,0),MATCH(%s,SumHdr,0))' % (key, code_)


# ================================================================================================================
# Sheet 6: PolicyMatrix - original layout, live values
# ================================================================================================================
wsP = wb.create_sheet("PolicyMatrix")
with open(DUMP_SRC, encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("# ColWidths:"):
            for tok in line.split(":", 1)[1].split():
                cl_, w_ = tok.split("=")
                wsP.column_dimensions[cl_].width = float(w_)
for cl_ in ("B", "D", "E"):
    wsP.column_dimensions[cl_].hidden = True


def orig_font(d):
    return Font(name="Arial", size=10, bold=d["bold"], italic=d["italic"], color=d["fontcolor"] or "000000")


def copy_orig(addr, value=None, formula=None, fmt=None, fill=None):
    """Write an original cell verbatim (value / cached value for formulas), with its number format and font."""
    d = ORIG.get(addr)
    if d is None:
        return None
    v = value if value is not None else (formula if formula is not None else
                                         (d["value"] if d["kind"] == "V" else d["cached"]))
    c = wsP[addr]
    c.value = v
    c.number_format = fmt or d["fmt"]
    c.font = orig_font(d)
    if fill is not None:
        c.fill = fill
    elif d["fill"]:
        c.fill = PatternFill("solid", fgColor=d["fill"])
    c.alignment = Alignment(wrap_text=d["wrap"], vertical="top")
    return c


# rows 1-4: notes
for addr in ("D1", "D2", "D3", "E4", "V4", "AS4"):
    copy_orig(addr)
copy_orig("C1", value="Egypt - Policy Options Matrix (rebuild %s of AdHocCalculations.xlsb)" % VERSION)
copy_orig("C2", value="Built %s" % TODAY, fmt="General")
copy_orig("C3", formula='="All results for "&Yr&", at the CPAT carbon price of that year ($"&TEXT(%s,"0")&" for 1A)."'
          % RLOOK("tau", '"1A"'), fmt="General")
put(wsP, "C4", '="Mode: "&Mode&"   |   CBAM convention: "&Conv&"   |   process beta set: "&BetaSet&"   |   edit only on Inputs"',
    font=BOLD, fill=REVIEW, border=False)
# row 5: headers (verbatim A..AE, AR..AU; AF..AQ redefined)
NEW_HDR = {"AF": "CPAT: change in total GHG, adjusted (Mt)", "AG": "less CPAT IPPU scaling, adjusted (Mt)", "AH": "Non-CBAM IPPU response (Mt)",
           "AI": "CBAM process intensity response (Mt)", "AJ": "CBAM process output response (Mt)",
           "AK": "OBR output-channel correction (Mt)", "AL": "Fund extra fuel-intensity reduction (Mt)",
           "AM": "K decomposition check (=0)", "AN": "Intensity change, export-weighted",
           "AO": "Gross carbon revenue ($bn)", "AP": "OBR rebates ($bn)", "AQ": "CBAM obligations reduced, FULL phase-in"}
for ci in range(1, col("AU") + 1):
    cl_ = L(ci)
    addr = "%s5" % cl_
    if cl_ in NEW_HDR:
        put(wsP, addr, NEW_HDR[cl_], fill=REVIEW, font=ORIG_HDR_FONT, align=WRAP)
    elif addr in ORIG:
        copy_orig(addr)
wsP.row_dimensions[5].height = 66
# row 6 band
wsP.merge_cells("C6:R6")
copy_orig("C6")
for addr in ("AS6", "AT6", "AU6"):
    copy_orig(addr)
# rows 7-12: bundles (live)
PM_FMT = {"J": "0%", "K": "0.0", "L": "0.0%", "M": "0%", "N": "0.0%", "O": "0.0%", "P": "0.0", "Q": "0", "R": "0.0%",
          "T": "0%", "U": "0%", "V": ACC2, "W": ACC2, "X": ACC2, "Y": ACC2, "Z": ACC2, "AA": ACC2, "AB": ACC2, "AC": "0%",
          "AD": ACC2, "AE": ACC2, "AF": "0.00", "AG": "0.00", "AH": "0.00", "AI": "0.00", "AJ": "0.00", "AK": "0.00",
          "AL": "0.00", "AM": "0.000000", "AN": "0.0%", "AO": "0.00", "AP": "0.00", "AQ": "0.0%", "AR": "0.0", "H": USD0}
PM_KEY = {"H": "tau", "J": "J", "K": "K", "L": "L", "M": "M", "N": "N", "O": "O", "P": "P_net", "Q": "Q_deaths", "R": "R",
          "T": "T", "U": "U", "V": "P_gross", "W": "tau", "X": "ghg0", "Y": "ind0", "Z": "Efbase", "AA": "Epbase",
          "AB": "AB_cov", "AC": "J", "AD": "Ebase", "AE": "AE_cov", "AF": "dghg_adj", "AG": "dippu_adj", "AH": "ippu_other",
          "AI": "ERp", "AJ": "emrq_proc", "AK": "D_obr", "AL": "F_fund", "AM": "K_check", "AN": "cbintchx",
          "AO": "P_gross", "AP": "rebate_bn", "AQ": "O_full", "AR": "AR"}
for i, code_ in enumerate(BUNDLES):
    rr = 7 + i
    copy_orig("A%d" % rr)
    put(wsP, "B%d" % rr, "=INDEX(BT_Scen,MATCH($A%d,BT_Code,0))" % rr, border=False)
    for cl_ in ("C", "D", "E", "F", "I", "AS", "AT", "AU"):
        copy_orig("%s%d" % (cl_, rr))
    if rr == 7:
        copy_orig("G7", value="$20 flat from 2028 (CPAT EG1 trajectory)")
    else:
        copy_orig("G%d" % rr)
    for cl_, key in PM_KEY.items():
        f = "=" + RLOOK(key, "$A%d" % rr)
        if cl_ == "AG":
            f = "=-" + RLOOK(key, "$A%d" % rr)
        c = wsP["%s%d" % (cl_, rr)]
        c.value = f
        c.number_format = PM_FMT[cl_]
        c.font = Font(name="Arial", size=10, italic=(cl_ in ("T", "U")))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if cl_ in NEW_HDR:
            c.fill = REVIEW
    wsP.row_dimensions[rr].height = 96
# rows 13-22: verbatim (non-modelled bundles; not recomputed)
for addr, d in ORIG.items():
    m = re.match(r"([A-Z]+)(\d+)$", addr)
    cl_, rn = m.group(1), int(m.group(2))
    if 13 <= rn <= 22:
        if rn in (14, 15) and col("AF") <= col(cl_) <= col("AP"):
            continue  # legacy half-elasticity block dropped
        if addr == "G14":
            copy_orig(addr, formula="=G11")
        elif addr == "G15":
            copy_orig(addr, formula="=G12")
        else:
            copy_orig(addr)
wsP.merge_cells("C13:R13")
wsP.merge_cells("C18:R18")
for rn in range(14, 23):
    for ci in range(col("J"), col("AU") + 1):
        c = wsP["%s%d" % (L(ci), rn)]
        if c.value is not None and c.fill.fill_type is None:
            c.fill = GREY
    wsP.row_dimensions[rn].height = 80 if rn != 18 else 18
# rows 24-29: price trajectories and CBAM phase-in (live from Inputs section F)
put(wsP, "C24", "Rows 7-12 are live (Results sheet). Rows 14-22 are copied verbatim from the original (non-modelled "
    "bundles, not recomputed, grey). Columns AF-AQ are redefined (yellow headers) - see ReadMe.", font=ITALIC, border=False)
copy_orig("C26", value="Standard Price Trajectories ($/tCO2) and CBAM phase-in (live from Inputs)")
TRAJ_YEARS = list(range(2027, 2035))
for j, y in enumerate(TRAJ_YEARS):
    cl_ = L(col("F") + j)
    put(wsP, "%s26" % cl_, y, font=BOLD, align=CENTER, fmt="0")
    put(wsP, "%s27" % cl_, "=INDEX(YV_FLAT,MATCH(%s$26,YV_Years,0))" % cl_, fmt="0.0")
    put(wsP, "%s28" % cl_, "=INDEX(YV_RAMP,MATCH(%s$26,YV_Years,0))" % cl_, fmt="0.0")
    put(wsP, "%s29" % cl_, "=INDEX(YV_CBF,MATCH(%s$26,YV_Years,0))" % cl_, fmt="0.0%")
copy_orig("C27", value="Price Trajectory 1 (flat; 1A, 2A, 2B = CPAT EG1/EG2)")
copy_orig("C28", value="Price Trajectory 2 (rising; 3A, 3B, 3C = CPAT EG3 cptraj.2)")
put(wsP, "C29", "CBAM phase-in factor (EU definitive period)", border=False)
wsP.freeze_panes = "F7"

# ================================================================================================================
# Sheet 7: Comparison - original vs Table 2 vs rebuilt (live) vs prototype v0.11
# ================================================================================================================
wsX = wb.create_sheet("Comparison")
widths(wsX, {"A": 44, "B": 10, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14, "H": 14, "I": 16, "J": 16, "K": 60})
title_band(wsX, "Comparison - original PolicyMatrix (static), results-note Table 2 (static), rebuilt (live), prototype v0.11 (static)", "K")
wsX.merge_cells("A2:K2")
put(wsX, "A2", "Static columns were transcribed from AdHocCalculations.xlsb (2030 values) and the results note; prototype columns "
    "from CPAT_Industry_Kernel_Egypt_v0.11.xlsx run per bundle and convention (prototype_v0_11_results.json). "
    "Section 2 is the PROTOTYPE-mode verification: with Mode = PROTOTYPE every row must PASS.", font=ITALIC, align=WRAP, border=False)
# --- Section 1 -------------------------------------------------------------------------------------------------
ORIG_2030 = {  # PolicyMatrix 2030 cached values, bundles 1A,2A,2B,3A,3B,3C
    "J": [.72, .65, .65, .243, .243, .243], "K": [-41.621, -38.877, -41.002, -21.542, -18.123, -24.485],
    "L": [-.0852, -.0795, -.0839, -.0441, -.0371, -.0501], "M": [1, .445, .445, 1, 1, 1],
    "N": [-.0757, -.0549, -.0549, -.0757, -.0757, -.1306], "O": [-.2606, -.1390, -.1390, -.2606, -.0757, -.3045],
    "P_net": [5.772, 5.176, 5.176, 2.375, 0, 0], "Q_deaths": [1655.6, 1564, 1631, 546, 345, 620.6],
    "R": [.0200, .0189, .0197, .0066, .0026, .0075], "T": [-.153, -.134, -.134, -.181, -.153, -.206],
    "U": [-.083, -.083, -.083, -.114, -.083, -.087], "AR": [10.62, 10.62, 10.62, 2.69, 0, None]}
TABLE2 = {"J": [.72, .65, .65, .20, .20, .20], "K": [-41.6, -38.9, -41.0, -21.5, -18.1, -24.5], "M": [1, .44, .44, 1, 1, 1],
          "N": [-.076, -.055, -.055, -.076, -.076, -.131], "O": [-.261, -.139, -.139, -.261, -.076, -.304],
          "P_net": [5.8, 5.2, 5.2, 1.1, 0, 0], "Q_deaths": [1656, 1564, 1631, 546, 345, 621]}
PROTO_KEY = {"M": "cbcov", "N": "cbintch", "O": "cbobchu", "T": None, "U": "cbqch"}
SEC1 = [("J", "J: emissions coverage (% total GHG)", "0.0%"), ("K", "K: total emissions reduction (Mt)", "0.00"),
        ("L", "L: reduction, % of baseline GHG", "0.00%"), ("M", "M: CBAM coverage", "0.0%"),
        ("N", "N: CBAM intensity reduction", "0.00%"), ("O", "O: CBAM obligations reduced per unit", "0.00%"),
        ("P_net", "P: carbon revenues raised ($bn)", "0.00"), ("Q_deaths", "Q: deaths avoided", "#,##0"),
        ("R", "R: % of air-pollution deaths", "0.00%"), ("T", "T: industrial emissions change", "0.0%"),
        ("U", "U: industrial output change", "0.0%"), ("AR", "AR: change in net revenues ($bn)", "0.00")]
r = 4
section_band(wsX, r, "1. Table-2 metrics by bundle: original | Table 2 | rebuilt (live, selected Mode/Conv) | prototype FULL | prototype NOPHASE", "K")
r += 1
header_row(wsX, r, ["Metric", "Bundle", "Original (2030)", "Table 2", "Rebuilt (live)", "Proto FULL", "Proto NOPHASE",
                    "Rebuilt - Original", "Rebuilt - Proto(sel)", "", "Comment"])
r += 1
SEC1_FIRST = r
for key, label, fmt in SEC1:
    for i, code_ in enumerate(BUNDLES):
        put(wsX, "A%d" % r, label if i == 0 else "", font=(BOLD if i == 0 else ARIAL))
        put(wsX, "B%d" % r, code_, fill=BLUE, align=CENTER)
        ov = ORIG_2030[key][i]
        put(wsX, "C%d" % r, ov if ov is not None else "n/a", fmt=fmt)
        tv = TABLE2.get(key, [None] * 6)[i]
        put(wsX, "D%d" % r, tv if tv is not None else "", fmt=fmt)
        put(wsX, "E%d" % r, "=" + RLOOK(key, "$B%d" % r), fmt=fmt, fill=GREEN)
        pk = PROTO_KEY.get(key)
        if key == "T":
            pf = PROTO["%s|FULL" % code_]
            pn = PROTO["%s|NOPHASE" % code_]
            put(wsX, "F%d" % r, pf["emrt.2"] / pf["emis.1"], fmt=fmt)
            put(wsX, "G%d" % r, pn["emrt.2"] / pn["emis.1"], fmt=fmt)
        elif pk:
            put(wsX, "F%d" % r, PROTO["%s|FULL" % code_][pk + ".2"], fmt=fmt)
            put(wsX, "G%d" % r, PROTO["%s|NOPHASE" % code_][pk + ".2"], fmt=fmt)
        else:
            put(wsX, "F%d" % r, "", fill=GREY)
            put(wsX, "G%d" % r, "", fill=GREY)
        put(wsX, "H%d" % r, '=IF(ISNUMBER(C%d),E%d-C%d,"")' % (r, r, r), fmt=fmt)
        put(wsX, "I%d" % r, '=IF(ISNUMBER(F%d),E%d-IF(Conv="NOPHASE",G%d,F%d),"")' % (r, r, r, r), fmt=fmt)
        put(wsX, "K%d" % r, "", align=WRAP)
        r += 1
SEC1_LAST = r - 1
# --- Section 2 -------------------------------------------------------------------------------------------------
r += 1
section_band(wsX, r, "2. PROTOTYPE-mode verification: CBAM block metrics (live) vs prototype v0.11 for the selected convention", "K")
r += 1
header_row(wsX, r, ["Metric (prototype name)", "Bundle", "Live (Results)", "Proto FULL", "Proto NOPHASE", "Proto (sel. conv.)",
                    "Live - Proto(sel)", "Check", "", "", "Definition"])
r += 1
SEC2_FIRST = r
SEC2 = [("cbcov", "cbcov", "CBAM coverage"), ("cbintch", "cbintch", "Intensity change"), ("cbintchx", "cbintchx", "Intensity change, export-weighted"),
        ("cbcovx", "cbcovx", "Coverage, export-weighted"), ("cbqch", "cbqch", "Output-channel reduction / E_base"),
        ("emrq", "emrq", "Output-channel reduction (Mt)"), ("emrt", "emrt", "Total block reduction (Mt)"), ("emis", "emis", "Post-response block emissions (Mt)"),
        ("ERp", "emrp", "Process intensity response (Mt)"), ("ERf", "emrf", "Fuel intensity response (Mt)"), ("emr", "emr", "Intensity-channel reduction (Mt)"),
        ("revf", "revf", "Fuel carbon revenue ($m)"), ("revp", "revp", "Process carbon revenue ($m)"), ("rev", "rev", "Block carbon revenue ($m)"),
        ("cbobl", "cbobl", "CBAM obligation ($m)"), ("cbobl0", "cbobl0", "CBAM obligation, no policy ($m)"),
        ("cbobch", "cbobch", "Change in CBAM obligation"), ("cbobchu", "cbobchu", "Change in CBAM obligation per unit"),
        ("cbint", "cbint", "Block intensity (t/t)"), ("emisf", "emisf", "Post-response fuel emissions (Mt)"), ("emisp", "emisp", "Post-response process emissions (Mt)")]
for key, pname, defn in SEC2:
    for i, code_ in enumerate(BUNDLES):
        put(wsX, "A%d" % r, pname if i == 0 else "", font=(BOLD if i == 0 else ARIAL))
        put(wsX, "B%d" % r, code_, fill=BLUE, align=CENTER)
        put(wsX, "C%d" % r, "=" + RLOOK(key, "$B%d" % r), fmt="0.000000", fill=GREEN)
        put(wsX, "D%d" % r, PROTO["%s|FULL" % code_][pname + ".2"], fmt="0.000000")
        put(wsX, "E%d" % r, PROTO["%s|NOPHASE" % code_][pname + ".2"], fmt="0.000000")
        put(wsX, "F%d" % r, '=IF(Conv="NOPHASE",E%d,IF(Conv="FULL",D%d,NA()))' % (r, r), fmt="0.000000")
        put(wsX, "G%d" % r, "=IFERROR(C%d-F%d,NA())" % (r, r), fmt="0.000000")
        put(wsX, "H%d" % r, '=IF(Mode<>"PROTOTYPE","n/a (REBUILD)",IF(Conv="SCALED","n/a (SCALED)",'
            'IF(ABS(G%d)<1E-7*MAX(1,ABS(F%d)),"PASS","FAIL")))' % (r, r), align=CENTER)
        put(wsX, "K%d" % r, defn if i == 0 else "", align=WRAP)
        r += 1
SEC2_LAST = r - 1
r += 1
put(wsX, "A%d" % r, "PROTOTYPE-mode checks passed / failed", font=BOLD)
put(wsX, "C%d" % r, '=COUNTIF(H%d:H%d,"PASS")' % (SEC2_FIRST, SEC2_LAST), fmt="0", fill=GREEN)
put(wsX, "D%d" % r, '=COUNTIF(H%d:H%d,"FAIL")' % (SEC2_FIRST, SEC2_LAST), fmt="0", fill=GREEN)
name("ProtoPass", "Comparison!$C$%d" % r)
name("ProtoFail", "Comparison!$D$%d" % r)
wsX.freeze_panes = "C6"

# ================================================================================================================
# Sheet 8: Issues resolved (MajorIssues.docx, 19 items)
# ================================================================================================================
wsQ = wb.create_sheet("Issues resolved")
widths(wsQ, {"A": 4, "B": 46, "C": 52, "D": 70, "E": 26, "F": 14, "G": 52})
title_band(wsQ, "Issues resolved - the 19 items of MajorIssues.docx mapped to the rebuild", "G")
header_row(wsQ, 3, ["#", "Issue (MajorIssues.docx)", "Root cause in AdHocCalculations.xlsb", "Resolution in the rebuild",
                    "Where", "Status", "Residual / flag for review"])
ISSUES = [
    (1, "GHG-tab percentage denominators (division by 2022 values gives e.g. 107%).",
     "GHG tab divided 2030 policy values by 2022 baseline values.",
     "All percentages use the CPAT baseline of the reporting year (Inputs section C, Yr). GHG tab not rebuilt (unused by Table 2).",
     "Inputs C; Results L, R", "Resolved", "GHG tab omitted; nothing in Table 2 depended on it."),
    (2, "3B deaths avoided (345) stale / unexplained.",
     "Hard-typed number from an earlier run, not linked to any scenario.",
     "Q = CPAT deaths of the bundle's scenario (EG3 for 3B), rescaled by the change in energy CO2 after the OBR correction.",
     "Results Q_deaths", "Resolved", "Rescaling is proportional (approximation) - see methodology note."),
    (3, "1A built on EG2 (two-sector CPAT run) instead of EG1 (all-fuel run).",
     "Row 7 referenced row 9 values (Q7 = Q9 x K7/K9 etc.).",
     "Bundle table maps 1A -> EG1 explicitly; every 1A quantity reads EG1 columns.", "Inputs D; Results scen", "Resolved", ""),
    (4, "Mixed base years (2026 in some cells, 2030 in others).",
     "Hand-copied values from different CPAT columns.",
     "One reporting year switch (Yr) drives every CPAT lookup; price trajectories read the same year.", "Inputs A (Yr)", "Resolved", ""),
    (5, "Price start '2027' in the text vs 2028 in CPAT.",
     "Typed label.", "G7 label corrected; trajectories rows 27-28 are live from the CPAT cptraj vector (first non-zero year 2028).",
     "PolicyMatrix G7, rows 26-29", "Resolved", ""),
    (6, "AR = 10.62 (EG2 value) used for 2A although 2A is EG1 (10.43).",
     "Row-7/8 cells copied from row 9.", "AR = CPAT delta net revenue of the bundle's own scenario, less rebates / fund.",
     "Results AR", "Resolved", "Definition broadened (net of OBR / fund); original AR was gross."),
    (7, "Inputs tab misaligned (columns I-N drift from ~row 110).",
     "Pasted blocks of different length.", "CPAT data are a single keyed table (code|scenario) read by INDEX/MATCH; no positional pasting.",
     "CPAT_Outputs; Inputs C", "Resolved", ""),
    (8, "EG4 misconfigured (feebate off; near-zero effect).",
     "CPAT scenario set-up.", "EG4 is not used by any bundle (kept in CPAT_Outputs as memo only).", "Inputs D", "Resolved (by exclusion)",
     "Re-run EG4 in CPAT if a feebate bundle is wanted."),
    (9, "3B: table says -18.1 Mt, text says 13.6.",
     "Two unreconciled calculations.", "Single K for every bundle, decomposed in AF-AM; 3B = EG3 with the OBR output-channel correction D_obr.",
     "Results K, D_obr; PolicyMatrix AF-AM", "Resolved", "3B K is now smaller in magnitude than 3A (OBR removes the output channel)."),
    (10, "3A revenue 1.1 / 2.4 / 0.9 $bn inconsistent (1.1 = 20 x 53.6).",
     "Three different revenue concepts in different places.", "P = CPAT carbon-tax receipts on fuels (post-response) + block process revenue (post-response), net of rebates / fund; gross shown in AO.",
     "Results P_gross, P_net", "Resolved", "3A ~1.5 $bn (0.93 fuels + 0.62 process)."),
    (11, "Three different percentage denominators (249 / 488.7 / 594 Mt).",
     "Mixed sector totals and years.", "One denominator: CPAT total GHG incl. LULUCF, baseline, reporting year (X column).", "Results ghg0, L, J", "Resolved", ""),
    (12, "Coverage 72% / 65% typed; the sheet's own columns imply 59% / 53%.",
     "Typed values.", "J computed: covered fuel CO2 (economy-wide energy CO2 for ALL; kappa x industry energy CO2 for IND) + priced block process emissions, over total GHG.",
     "Results J, J_int, kappa", "Resolved", "Industry bundles: kappa(EG3) = 0.54 (only part of industry priced in the CPAT run) - J_int shows the intended coverage."),
    (13, "'All industry' in 3A but only part of industrial energy CO2 is priced in EG3 (14% reduction vs 2A's).",
     "CPAT EG3 run priced a subset of industrial fuel use.", "kappa = eff.cptraj / cptraj x enr0/ind0 (capped at 1) makes the partial coverage explicit; J_int memo shows the intended full-industry coverage.",
     "Inputs C (CV_kappa), KappaMode", "Flagged", "v0.3 default KappaMode=SCALE approximates full coverage; recommend re-running EG3 with all industrial fuels priced, then set KappaMode = ONE or retire SCALE."),
    (14, "-0.549%/$ half-elasticity untraceable.", "Legacy constant.", "Replaced by process half-elasticities beta = -LN(1-ER100)/100 from the IPCC-based set (BetaSet switch; PROTOTYPE set available).",
     "Inputs E (PT_ER, PT_Beta)", "Resolved", "beta set choice is a judgement (TASK-D)."),
    (15, "K11 = -13.592 x (2/3)/0.5 untraceable.", "Legacy constant.", "3B K built from CPAT EG3 with the OBR correction D_obr = -(1-s_int) w dInd; s_int from the elasticities on Inputs.",
     "Results D_obr, SInt", "Resolved", ""),
    (16, "CBAM base 53.6 Mt untraceable.", "Legacy constant.", "E_base = sum over eight products of Qb (F+G)/1000 from the product table (62.424 Mt in 2030 with Egypt CBAM EF v0.1; 61.157 Mt with the prototype EFs, EFSet = PROTOTYPE).",
     "Inputs E; Results Ebase", "Resolved", ""),
    (17, "Process emissions double-counted (CPAT scales IPPU with industrial energy CO2).",
     "CPAT delta GHG already contains an IPPU response proportional to the fuel response.",
     "K removes CPAT's IPPU change (AG) and adds the block's explicit process responses (AI intensity via beta, AJ output channel); non-block IPPU set to 0 unless IppuOther = CPAT.",
     "Results K; PolicyMatrix AF-AM", "Resolved", "Non-block IPPU (~43% of IPPU) assumed unresponsive by default."),
    (18, "Output change for 1A/2A/2B set equal to 3B's -8.3%.", "Cross-row reference U = $U$11.",
     "U = cbqch of the bundle's own block (output channel), T = emrt / E_base.", "Results U, T", "Resolved", ""),
    (19, "Deaths scaled by process CO2 (no air-quality effect).", "Scaling by total K.",
     "Deaths rescaled by the change in energy CO2 only ((dEnr + D_obr + F_fund)/dEnr); process emissions excluded.", "Results Q_deaths", "Resolved", ""),
]
for i, (n, issue, cause, fix, where, status, resid) in enumerate(ISSUES):
    rr = 4 + i
    put(wsQ, "A%d" % rr, n, align=CENTER)
    put(wsQ, "B%d" % rr, issue, align=WRAP)
    put(wsQ, "C%d" % rr, cause, align=WRAP)
    put(wsQ, "D%d" % rr, fix, align=WRAP)
    put(wsQ, "E%d" % rr, where, align=WRAP)
    put(wsQ, "F%d" % rr, status, align=CENTER, fill=(GREEN if status.startswith("Resolved") else REVIEW))
    put(wsQ, "G%d" % rr, resid, align=WRAP)
    wsQ.row_dimensions[rr].height = 64
wsQ.freeze_panes = "B4"

# ================================================================================================================
# Sheet 9: Checks
# ================================================================================================================
wsK = wb.create_sheet("Checks")
widths(wsK, {"A": 4, "B": 84, "C": 16, "D": 12})
title_band(wsK, "Checks - all PASS expected (PROTOTYPE verification is n/a in REBUILD mode)", "D")
header_row(wsK, 3, ["#", "Check", "Value", "Result"])
CHECKS = [
    ("Mode switch valid (REBUILD / PROTOTYPE)", "=Mode", '=IF(OR(Mode="REBUILD",Mode="PROTOTYPE"),"PASS","FAIL")'),
    ("CBAM convention valid (FULL / NOPHASE / SCALED)", "=Conv", '=IF(OR(Conv="FULL",Conv="NOPHASE",Conv="SCALED"),"PASS","FAIL")'),
    ("Reporting year present in CPAT_Outputs", "=Yr", '=IF(ISNUMBER(MATCH(Yr,CPO_Years,0)),"PASS","FAIL")'),
    ("No errors in Inputs section C (CPAT values)", "=SUMPRODUCT(--ISERROR(Inputs!$C$%d:$F$%d))" % (IN["cv_hdr"] + 1, IN["cv_last"]),
     '=IF(C{r}=0,"PASS","FAIL")'),
    ("No errors in Results", "=SUMPRODUCT(--ISERROR(SumTbl))", '=IF(C{r}=0,"PASS","FAIL")'),
    ("No errors in CBAM_Products", "=SUMPRODUCT(--ISERROR(CBAM_Products!$A$4:$AV$%d))" % (4 + BLOCK_H * 6), '=IF(C{r}=0,"PASS","FAIL")'),
    ("No errors in PolicyMatrix rows 7-12", "=SUMPRODUCT(--ISERROR(PolicyMatrix!$A$7:$AU$12))", '=IF(C{r}=0,"PASS","FAIL")'),
    ("E_base (2030) = prototype 61.1572316750106 Mt when Yr = 2030 and EFSet = PROTOTYPE", "=" + RLOOK("Ebase", '"1A"'),
     '=IF(OR(Yr<>2030,EFSet<>"PROTOTYPE"),"n/a",IF(ABS(C{r}-61.1572316750106)<1E-6,"PASS","FAIL"))'),
    ("PolicyMatrix K equals Results K for all six bundles",
     "=" + "+".join("ABS(PolicyMatrix!$K$%d-Results!$%s$%d)" % (7 + i, L(3 + i), RES["K"]) for i in range(6)),
     '=IF(C{r}<1E-9,"PASS","FAIL")'),
    ("K decomposition closes (sum of AF..AL = K) for all bundles", "=SUMPRODUCT(ABS(INDEX(SumTbl,MATCH(\"K_check\",SumKeys,0),0)))", '=IF(C{r}<1E-9,"PASS","FAIL")'),
    ("Coverage J within [0,1]", "=MIN(INDEX(SumTbl,MATCH(\"J\",SumKeys,0),0))&\" / \"&MAX(INDEX(SumTbl,MATCH(\"J\",SumKeys,0),0))",
     '=IF(AND(MIN(INDEX(SumTbl,MATCH("J",SumKeys,0),0))>=0,MAX(INDEX(SumTbl,MATCH("J",SumKeys,0),0))<=1),"PASS","FAIL")'),
    ("CBAM coverage M within [0,1]", "=MAX(INDEX(SumTbl,MATCH(\"M\",SumKeys,0),0))",
     '=IF(AND(MIN(INDEX(SumTbl,MATCH("M",SumKeys,0),0))>=0,C{r}<=1),"PASS","FAIL")'),
    ("Intensity change N <= 0 and output change U <= 0 for all bundles",
     "=MAX(MAX(INDEX(SumTbl,MATCH(\"N\",SumKeys,0),0)),MAX(INDEX(SumTbl,MATCH(\"U\",SumKeys,0),0)))", '=IF(C{r}<=1E-12,"PASS","FAIL")'),
    ("Total reduction K <= 0 for all bundles", "=MAX(INDEX(SumTbl,MATCH(\"K\",SumKeys,0),0))", '=IF(C{r}<=0,"PASS","FAIL")'),
    ("PROTOTYPE mode: all Comparison section-2 rows PASS (0 FAIL)", "=ProtoFail", '=IF(Mode<>"PROTOTYPE","n/a",IF(ProtoFail=0,"PASS","FAIL"))'),
    ("3C fund outlay upper bound <= fund budget", "=" + RLOOK("fund_outlay", '"3C"') + "-" + RLOOK("fund_budget", '"3C"'), '=IF(C{r}<=1E-9,"PASS","FAIL")'),
    ("Net revenue P >= 0 for all bundles", "=MIN(INDEX(SumTbl,MATCH(\"P_net\",SumKeys,0),0))", '=IF(C{r}>=-0.001,"PASS","FAIL")'),
    ("Flat trajectory (Yr) equals CPAT EG1 cptraj.2 (Yr)",
     "=INDEX(YV_FLAT,MATCH(Yr,YV_Years,0))-INDEX(YV_EG1,MATCH(Yr,YV_Years,0))", '=IF(ABS(C{r})<1E-9,"PASS","FAIL")'),
    ("Block process + fuel baseline emissions below CPAT IPPU / industry energy CO2 (EG1 2030)",
     "=" + RLOOK("Epbase", '"1A"') + "-" + RLOOK("ippu0", '"1A"'), '=IF(C{r}<0,"PASS","FAIL")'),
]
for i, (txt, val, res_) in enumerate(CHECKS):
    rr = 4 + i
    put(wsK, "A%d" % rr, i + 1, align=CENTER)
    put(wsK, "B%d" % rr, txt, align=WRAP)
    put(wsK, "C%d" % rr, val.replace("{r}", str(rr)), fmt="General")
    put(wsK, "D%d" % rr, res_.replace("{r}", str(rr)), align=CENTER)
CK_LAST = 4 + len(CHECKS) - 1
put(wsK, "B%d" % (CK_LAST + 1), "overall", font=BOLD, fill=SECTION)
put(wsK, "D%d" % (CK_LAST + 1), '=IF(COUNTIF(D4:D%d,"FAIL")=0,"PASS","FAIL")' % CK_LAST, font=BOLD, fill=SECTION, align=CENTER)
name("ChecksOverall", "Checks!$D$%d" % (CK_LAST + 1))

# ================================================================================================================
# Sheet 1: ReadMe (filled last)
# ================================================================================================================
ws = ws_readme
widths(ws, {"A": 30, "B": 120})
title_band(ws, "AdHocCalculations - rebuild %s (Egypt policy-options matrix, Table 2 of the results note)" % VERSION, "B")
README = [
    ("Purpose", "Transparent rebuild of AdHocCalculations.xlsb (PolicyMatrix tab) behind Table 2 of the Egypt results note. "
     "Every number on PolicyMatrix rows 7-12 is a formula reading Inputs / CPAT_Outputs / CBAM_Products / Results; nothing is typed."),
    ("How to use", "Change assumptions ONLY on the Inputs tab (tan cells). Mode = REBUILD (default, coherent method) or PROTOTYPE "
     "(reproduces CPAT_Industry_Kernel_Egypt_v0.11 block exactly - verify on Comparison section 2 and Checks). Conv = CBAM "
     "convention for O (NOPHASE default). Yr = reporting year (2030 default)."),
    ("Sheets", "Inputs (all assumptions, switches, CPAT values for Yr, bundle table, product table, year vectors) | CPAT_Outputs "
     "(trimmed CPAT Outputs 2022-2041, 32 codes x 4 scenarios) | CBAM_Products (eight-product block per bundle, prototype v0.11 "
     "equations) | Results (engine: every metric by bundle, keyed) | PolicyMatrix (original layout, live) | Comparison (original / "
     "Table 2 / rebuilt / prototype) | Issues resolved (19 items) | Checks."),
    ("Format changes vs original", "(1) Assumptions moved to Inputs (original had typed constants inside PolicyMatrix and a misaligned "
     "Inputs tab). (2) Columns AF-AQ redefined (yellow headers): the legacy half-elasticity block (AF-AP) is replaced by the K "
     "decomposition (AF-AM), export-weighted intensity change (AN), gross revenue (AO), rebates (AP) and O under FULL phase-in (AQ). "
     "(3) Rows 14-22 (non-modelled bundles) copied verbatim, grey, not recomputed. (4) Trajectory rows 26-29 rebuilt as contiguous "
     "years 2027-2034 in F-M, live from Inputs, plus a CBAM phase-in row. (5) Row 4 mode indicator added; C3 is a formula. "
     "(6) New sheets: CPAT_Outputs, CBAM_Products, Results, Comparison, Issues resolved, Checks. (7) GHG tab not rebuilt."),
    ("Method differences vs original", "Single 2030 base (CPAT total GHG 594.2 Mt); coverage computed (kappa for partial industry runs); "
     "CBAM base bottom-up (62.42 Mt, eight products, Egypt CBAM EF v0.1); process response via beta and the output channel, CPAT's IPPU scaling removed; "
     "1A on EG1; 3B from EG3 with explicit OBR output-channel correction; revenue = CPAT fuel receipts + block process revenue, "
     "net of rebates / fund; deaths rescaled by energy CO2 only; price start 2028; no untraceable constants; b_f calibrated on CPAT; "
     "O convention explicit."),
    ("Method differences vs prototype v0.11", "REBUILD mode adds: fuel-intensity channel xf = EXP(b_f (tau + fund)); IPCC-based process beta set "
     "(prototype set selectable); fund shadow price sigma on both channels; national totals from CPAT; OBR rebates in net revenue; "
     "kappa coverage; 3C differs from 3A. PROTOTYPE mode switches all of these off for the block."),
    ("Provenance", "CPAT values: cpat_outputs_egypt_2022_2041.csv (CPAT Outputs sheet, Egypt EG1-EG4). Prototype: prototype_v0_11_results.json "
     "(run via Excel COM). Original: original_PolicyMatrix_cells.txt (verbatim dump). Builder: build_adhoc_rebuild_v0_3.py; "
     "verification: recalc_and_check_adhoc_v0_3.py (report recalc_and_check_adhoc_v0_3_report.txt). EFs: "
     "EmissionFactors/EGY_CBAM_EF_v0.1.xlsx. "
     "Methodology note (core equations, results, differences, open flags): MethodologyNote_v0.3.md / .docx."),
    ("Colour code", "Tan = input; blue = key / identifier; green = computed; yellow = switch-dependent or review; grey = static copy."),
    ("Version log", "v0.1 - first rebuild (openpyxl build, Excel COM verified). v0.2 - Egypt CBAM EF v0.1 "
     "(switch EFSet) and AN blended process ER100. %s %s - PStar = 122 USD2024 for IPCC beta sets, and "
     "KappaMode=SCALE default to approximate a full-coverage EG3 industry run pending a CPAT re-run." % (VERSION, TODAY)),
]
for i, (k, v) in enumerate(README):
    rr = 3 + i
    put(ws, "A%d" % rr, k, font=BOLD, fill=GREY, align=Alignment(vertical="top"))
    put(ws, "B%d" % rr, v, align=WRAP)
    ws.row_dimensions[rr].height = 15 * max(2, len(v) // 110 + 1)

wb.save(DST)
print("saved", DST, "names:", len(NAMES))
