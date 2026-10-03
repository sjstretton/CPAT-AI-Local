"""
recalc_and_check_adhoc_v0_3.py - Excel COM verification companion of build_adhoc_rebuild_v0_3.py.

What it does (run after the builder, needs Excel installed):
  1. Opens AdHocCalculations_Rebuild_v0.2.xlsx, sets Mode = PROTOTYPE with Conv = FULL, then NOPHASE; full
     recalculation; compares every CBAM block metric on Results (21 metrics x 6 bundles) with the prototype
     v0.11 results (prototype_v0_11_results.json) and reads the workbook's own ProtoPass / ProtoFail counters.
  2. Sets Mode = REBUILD, Conv = NOPHASE (the shipped setting); recalculation; recomputes every Results row in
     Python from the Inputs tab (product and bundle tables read from the workbook, CPAT values read from the
     CSV) and compares - an independent re-implementation of the same equations, so wiring errors show up.
  3. Scans all sheets for Excel error values, prints the Checks sheet and PolicyMatrix rows 7-12, writes the
     report to recalc_and_check_adhoc_v0_3_report.txt (UTF-8) and saves the workbook with cached values
     (Mode = REBUILD, Conv = NOPHASE).
Exit code 0 = everything passed.
"""
import csv
import json
import math
import os
import sys

import win32com.client as w32

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, "AdHocCalculations_Rebuild_v0.3.xlsx")
JSON_SRC = os.path.join(HERE, "prototype_v0_11_results.json")
CSV_SRC = os.path.join(HERE, "cpat_outputs_egypt_2022_2041.csv")
REPORT = os.path.join(HERE, "recalc_and_check_adhoc_v0_3_report.txt")
BUNDLES = ["1A", "2A", "2B", "3A", "3B", "3C"]
TOL = 1e-7
OUT = []
FAILS = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode())


def fail(msg):
    FAILS.append(msg)
    say("FAIL:", msg)


def close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------------------------------------------
# CPAT csv (independent of the workbook's INDEX/MATCH wiring)
# ---------------------------------------------------------------------------------------------------------------
with open(CSV_SRC, encoding="utf-8", newline="") as fh:
    rows = list(csv.reader(fh))
HDR = rows[0]
YCOL = {int(h): i for i, h in enumerate(HDR) if h.strip().isdigit()}
CPAT = {}
for row in rows[1:]:
    if not row or not row[0]:
        continue
    CPAT[(row[0].strip(), row[1].strip())] = row


def cp(code, scen, yr):
    v = CPAT[(code, scen)][YCOL[yr]]
    return float(v) if v not in ("", None) else 0.0


PROTO = json.load(open(JSON_SRC, encoding="utf-8"))

# ---------------------------------------------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------------------------------------------
xl = w32.DispatchEx("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
wb = xl.Workbooks.Open(XLSX)
wsI = wb.Worksheets("Inputs")
wsR = wb.Worksheets("Results")
wsP = wb.Worksheets("PolicyMatrix")
wsK = wb.Worksheets("Checks")


def nm(name):
    """Value of a defined name: scalar, 1-D list (row or column vector) or 2-D list."""
    v = wb.Names(name).RefersToRange.Value
    if not isinstance(v, tuple):
        return v
    if len(v) == 1:
        return list(v[0])
    if all(len(r) == 1 for r in v):
        return [r[0] for r in v]
    return [list(r) for r in v]


def set_switch(label_row, value):
    wsI.Range("B%d" % label_row).Value = value


MODE_ROW, CONV_ROW = 6, 7


def recalc():
    xl.CalculateFullRebuild()
    xl.Calculate()


def results():
    keys = nm("SumKeys")
    tbl = nm("SumTbl")
    hdr = nm("SumHdr")
    out = {}
    for k, row in zip(keys, tbl):
        if k is None:
            continue
        out[k] = {b: row[i] for i, b in enumerate(hdr)}
    return out


# ---------------------------------------------------------------------------------------------------------------
# 1. PROTOTYPE mode vs prototype v0.11
# ---------------------------------------------------------------------------------------------------------------
PROTO_MAP = [("cbcov", "cbcov"), ("cbintch", "cbintch"), ("cbintchx", "cbintchx"), ("cbcovx", "cbcovx"), ("cbqch", "cbqch"),
             ("emrq", "emrq"), ("emrt", "emrt"), ("emis", "emis"), ("ERp", "emrp"), ("ERf", "emrf"), ("emr", "emr"),
             ("revf", "revf"), ("revp", "revp"), ("rev", "rev"), ("cbobl", "cbobl"), ("cbobl0", "cbobl0"),
             ("cbobch", "cbobch"), ("cbobchu", "cbobchu"), ("cbint", "cbint"), ("emisf", "emisf"), ("emisp", "emisp"),
             ("Ebase", "emis.1")]
for conv in ("FULL", "NOPHASE"):
    set_switch(MODE_ROW, "PROTOTYPE")
    set_switch(CONV_ROW, conv)
    recalc()
    R = results()
    n_ok = n_bad = 0
    for b in BUNDLES:
        p = PROTO["%s|%s" % (b, conv)]
        for rk, pk in PROTO_MAP:
            pv = p[pk] if pk.endswith(".1") else p[pk + ".2"]
            rv = R[rk][b]
            if isinstance(rv, (int, float)) and close(rv, float(pv)):
                n_ok += 1
            else:
                n_bad += 1
                fail("PROTOTYPE/%s %s %s: workbook %r vs prototype %r" % (conv, b, rk, rv, pv))
    say("PROTOTYPE/%s: %d block values match the prototype, %d differ; workbook ProtoPass=%s ProtoFail=%s; "
        "Checks overall=%s" % (conv, n_ok, n_bad, nm("ProtoPass"), nm("ProtoFail"), nm("ChecksOverall")))
    if nm("ProtoFail") != 0 or nm("ChecksOverall") != "PASS":
        fail("PROTOTYPE/%s: workbook self-check not clean" % conv)

# ---------------------------------------------------------------------------------------------------------------
# 2. REBUILD mode vs an independent Python mirror
# ---------------------------------------------------------------------------------------------------------------
set_switch(MODE_ROW, "REBUILD")
set_switch(CONV_ROW, "NOPHASE")
recalc()
R = results()
S = {k: nm(k) for k in ["Mode", "Conv", "Yr", "SigmaEff", "BetaSet", "BfScen", "ThetaOther", "IppuOther", "KappaMode",
                        "EpsU", "EpsF", "SInt", "EpsQ", "PEU", "PStar", "Bf", "CBFyr", "CBFsel", "Ssel", "BaseYr"]}
yr = int(S["Yr"])
say("Switches / parameters:", {k: (round(v, 8) if isinstance(v, float) else v) for k, v in S.items()})
# parameter cross-checks
sint = S["EpsF"] * (1 + S["EpsU"]) / (S["EpsU"] + S["EpsF"] * (1 + S["EpsU"]))
if not close(S["SInt"], sint):
    fail("SInt %r vs %r" % (S["SInt"], sint))
bf = sint * math.log(cp("egy.mit.co2.ind.2", S["BfScen"], yr) / cp("egy.mit.co2.ind.1", S["BfScen"], yr)) / cp("egy.mit.cptraj.2", S["BfScen"], yr)
if not close(S["Bf"], bf):
    fail("Bf %r vs %r" % (S["Bf"], bf))
PT_NAMES = {"Name": "PT_Name", "Q0": "PT_Q0", "g": "PT_Growth", "X": "PT_X", "P": "PT_P", "F": "PT_FuelFac", "G": "PT_ProcFac",
            "ER": "PT_ER", "Beta": "PT_Beta"}
PT = {k: nm(v) for k, v in PT_NAMES.items()}
BT = {k: nm("BT_" + k) for k in ["Code", "Scen", "Scope", "Flag", "Theta", "Phi", "Tau"]}
for i in range(8):
    div = 100 if S["BetaSet"] == "PROTOTYPE" else S["PStar"]
    if not close(PT["Beta"][i], -math.log(1 - PT["ER"][i]) / div):
        fail("beta of %s" % PT["Name"][i])


def kappa_of(scen):
    if S["KappaMode"] == "ONE":
        return 1.0
    cpt = cp("egy.mit.cptraj.2", scen, yr)
    if cpt == 0:
        return 1.0
    return min(1.0, cp("egy.mit.eff.cptraj.2", scen, yr) / cpt * cp("egy.mit.co2.enr.tot.1", scen, yr) / cp("egy.mit.co2.ind.1", scen, yr))


def mirror(b):
    i = BT["Code"].index(b)
    scen, scope, flag, theta, phi, tau = BT["Scen"][i], BT["Scope"][i], BT["Flag"][i], BT["Theta"][i], BT["Phi"][i], BT["Tau"][i]
    if not close(tau, cp("egy.mit.cptraj.2", scen, yr)):
        fail("tau of %s" % b)
    taup, obr, fundsp, inclf, inclp = tau * flag, theta * tau, phi * S["SigmaEff"], 1, flag
    eps, peu, cbf_sel, cbf_yr, s_sel, base = S["EpsQ"], S["PEU"], S["CBFsel"], S["CBFyr"], S["Ssel"], S["BaseYr"]
    xf = 1.0 if S["Mode"] == "PROTOTYPE" else math.exp(S["Bf"] * (inclf * tau + fundsp))
    m = dict((k, 0.0) for k in ["Ebase", "Efbase", "Epbase", "Qb", "Q", "Ef", "Ep", "ERf", "ERp", "emisf", "emisp", "emis", "emrq",
                               "emrq_proc", "revf", "revp", "rev", "rebate", "cbobl", "cbobl0", "covered", "wnum", "wden",
                               "wnum_f", "wden_f", "wnum_n", "wden_n", "AP", "AQ", "AR"])
    for j in range(8):
        Q0, g, X, P, F, G, beta = PT["Q0"][j], PT["g"][j], PT["X"][j], PT["P"][j], PT["F"][j], PT["G"][j], PT["Beta"][j]
        Qb = Q0 * (1 + g) ** (yr - base)
        kf, kp = inclf * tau * F, inclp * taup * G
        mm = min(obr, tau) * inclf * F + min(obr, taup) * inclp * G
        dp = (kf + kp - mm) / P if P > 0 else 0.0
        Q = Qb * (1 + dp) ** eps
        Ef, Ep = Q * F / 1000, Q * G / 1000
        ERf = Ef * (xf - 1)
        ERp = -Ep * (1 - math.exp(-beta * (inclp * taup + fundsp)))
        Sf, Tp = Ef + ERf, Ep + ERp
        U = Sf + Tp
        J = 1 if G > 0 else 0
        Y, Z = Sf * inclf * tau, (Ep * J + ERp) * inclp * taup
        EI = U * 1000 / Q if Q > 0 else 0.0
        d = Y + Z
        d = d * 1000 / Q - mm if Q > 0 else 0.0
        obl = max(0.0, cbf_sel * peu * EI - s_sel * max(0.0, d))
        obl_f = max(0.0, cbf_yr * peu * EI - max(0.0, d))
        obl_n = max(0.0, peu * EI - max(0.0, d))
        cov = Ef * (1 if inclf > 0 else 0) + Ep * J * (1 if inclp > 0 else 0)
        m["Ebase"] += Qb * (F + G) / 1000; m["Efbase"] += Qb * F / 1000; m["Epbase"] += Qb * G / 1000
        m["Qb"] += Qb; m["Q"] += Q; m["Ef"] += Ef; m["Ep"] += Ep; m["ERf"] += ERf; m["ERp"] += ERp
        m["emisf"] += Sf; m["emisp"] += Tp; m["emis"] += U
        m["emrq"] += (Ef + Ep) * (1 - (1 + dp) ** (-eps)); m["emrq_proc"] += Ep * (1 - (1 + dp) ** (-eps))
        m["revf"] += Y; m["revp"] += Z; m["rev"] += Y + Z; m["rebate"] += mm * Q / 1000
        m["cbobl"] += X * Q / Q0 * obl / 1000 if Q0 > 0 else 0.0
        m["cbobl0"] += X * (1 + g) ** (yr - base) * cbf_sel * peu * (F + G) / 1000
        m["covered"] += cov
        m["wnum"] += X * obl; m["wden"] += X * cbf_sel * peu * (F + G)
        m["wnum_f"] += X * obl_f; m["wden_f"] += X * cbf_yr * peu * (F + G)
        m["wnum_n"] += X * obl_n; m["wden_n"] += X * peu * (F + G)
        if Q > 0:
            m["AP"] += X * U / Q; m["AQ"] += X * (Ef + Ep) / Q; m["AR"] += X * cov / Q
    m["emr"] = m["ERf"] + m["ERp"]; m["emrt"] = m["emrq"] + m["emr"]
    m["cbcov"] = m["covered"] / (m["Ef"] + m["Ep"]); m["cbcovx"] = m["AR"] / m["AQ"]
    m["cbintch"] = m["emis"] / (m["Ef"] + m["Ep"]) - 1; m["cbintchx"] = m["AP"] / m["AQ"] - 1
    m["cbqch"] = m["emrq"] / m["Ebase"]; m["emrt_pct"] = m["emrt"] / m["Ebase"]; m["cbint"] = m["emis"] * 1000 / m["Q"]
    m["cbobch"] = m["cbobl"] / m["cbobl0"] - 1; m["cbobchu"] = m["wnum"] / m["wden"] - 1
    m["cbobchu_full"] = m["wnum_f"] / m["wden_f"] - 1; m["cbobchu_nophase"] = m["wnum_n"] / m["wden_n"] - 1
    # national
    c = lambda code: cp(code, scen, yr)
    ghg0, ghg1 = c("egy.mit.ghg.tot.inc.1"), c("egy.mit.ghg.tot.inc.2")
    ippu0, ippu1 = c("egy.mit.ghg.ipr.tot.1"), c("egy.mit.ghg.ipr.tot.2")
    enr0, enr1 = c("egy.mit.co2.enr.tot.1"), c("egy.mit.co2.enr.tot.2")
    ind0, ind1 = c("egy.mit.co2.ind.1"), c("egy.mit.co2.ind.2")
    kap = kappa_of(scen)
    revctax = sum(c("egy.mit.rev.new.%s.usd.2" % f) for f in ["coa", "die", "gso", "lpk", "nga", "oil"])
    deaths = c("egy.air.ada.2464") + c("egy.air.ada.65") + c("egy.air.ada.u24")
    mort = c("egy.air.mort")
    drev = c("egy.mit.rev.new.usd.2") - c("egy.mit.rev.new.usd.1")
    dghg, dippu, denr, dind = ghg1 - ghg0, ippu1 - ippu0, enr1 - enr0, ind1 - ind0
    m.update(dict(ghg0=ghg0, ghg1=ghg1, ippu0=ippu0, ippu1=ippu1, enr0=enr0, enr1=enr1, ind0=ind0, ind1=ind1, dghg=dghg,
                  dippu=dippu, denr=denr, dind=dind, kappa=kap, revctax=revctax, deaths=deaths, mort=mort, drev=drev))
    m["scale_active"] = 1.0 if (S["KappaMode"] == "SCALE" and kap < 0.999999) else 0.0
    m["scale_fac"] = (1.0 / kap) if m["scale_active"] == 1.0 else 1.0
    m["dind_adj"] = dind * m["scale_fac"]
    m["denr_adj"] = denr + (m["scale_fac"] - 1.0) * dind
    m["dippu_adj"] = dippu * m["scale_fac"]
    m["dghg_adj"] = dghg + (m["scale_fac"] - 1.0) * (dind + dippu)
    m["ind1_adj"] = ind0 + m["dind_adj"]
    m["Ef0_adj"] = enr0 if scope == "ALL" else (ind0 if m["scale_active"] == 1.0 else kap * ind0)
    m["revctax_adj"] = revctax * m["scale_fac"]
    m["ippu_other"] = (1 - m["Epbase"] / ippu0) * dippu if S["IppuOther"] == "CPAT" else 0.0
    m["w"] = 1.0 if S["ThetaOther"] == 1 else min(1.0, m["Efbase"] / m["Ef0_adj"])
    m["D_obr"] = -(1 - S["SInt"]) * m["w"] * m["dind_adj"] if theta > 0 else 0.0
    fund_base = m["ind1_adj"] if m["scale_active"] == 1.0 else kap * ind1
    m["F_fund"] = fund_base * (math.exp(S["Bf"] * fundsp) - 1) if phi > 0 else 0.0
    m["K"] = m["dghg_adj"] - m["dippu_adj"] + m["ippu_other"] + m["ERp"] + m["emrq_proc"] + m["D_obr"] + m["F_fund"]
    m["L"] = m["K"] / ghg0
    m["Ef0"] = m["Ef0_adj"]
    m["J"] = (m["Ef0"] + flag * m["Epbase"]) / ghg0
    m["J_int"] = ((enr0 if scope == "ALL" else ind0) + flag * m["Epbase"]) / ghg0
    m["M"], m["N"], m["O"] = m["cbcov"], m["cbintch"], m["cbobchu"]
    m["O_full"], m["O_nophase"] = m["cbobchu_full"], m["cbobchu_nophase"]
    m["P_gross"] = m["revctax_adj"] + m["revp"] / 1000
    rebate_base = m["ind1_adj"] if m["scale_active"] == 1.0 else kap * ind1
    m["rebate_other"] = tau * (rebate_base - m["emisf"]) / 1000 if (theta > 0 and S["ThetaOther"] == 1) else 0.0
    m["rebate_bn"] = m["rebate"] / 1000 + m["rebate_other"]
    m["P_net"] = (1 - phi) * (m["P_gross"] - m["rebate_bn"])
    m["fund_budget"] = phi * (m["P_gross"] - m["rebate"] / 1000)
    m["fund_outlay"] = S["SigmaEff"] * abs(m["emr"] + m["F_fund"]) / 1000 if phi > 0 else 0.0
    m["Q_deaths"] = deaths * ((m["denr_adj"] + m["D_obr"] + m["F_fund"]) / denr if scope == "IND" else 1.0)
    m["R"] = m["Q_deaths"] / mort
    m["T"], m["U"] = m["emrt_pct"], m["cbqch"]
    m["AR"] = drev - (m["P_gross"] - m["P_net"])
    m["AB_cov"] = m["Ef0"] + flag * m["Epbase"]; m["AE_cov"] = m["cbcov"] * m["Ebase"]; m["K_check"] = 0.0
    m.update(dict(scen=scen, scope=scope, flag=flag, theta=theta, phi=phi, tau=tau, taup=taup, obrrb=obr, fundsp=fundsp, xf=xf))
    return m


n_ok = n_bad = 0
for b in BUNDLES:
    m = mirror(b)
    for k, v in m.items():
        if k not in R:
            continue
        rv = R[k][b]
        ok = (rv == v) if isinstance(v, str) else (isinstance(rv, (int, float)) and close(float(rv), float(v), 1e-9))
        if ok:
            n_ok += 1
        else:
            n_bad += 1
            fail("REBUILD %s %s: workbook %r vs mirror %r" % (b, k, rv, v))
missing = [k for k in R if k not in mirror("1A")]
say("REBUILD/NOPHASE: %d Results values match the Python mirror, %d differ; keys not mirrored: %s" % (n_ok, n_bad, missing))

# ---------------------------------------------------------------------------------------------------------------
# 3. Error scan, Checks, PolicyMatrix, save
# ---------------------------------------------------------------------------------------------------------------
for ws in wb.Worksheets:
    try:
        errs = ws.UsedRange.SpecialCells(-4123, 16)
        fail("%s has %d error cells (first %s)" % (ws.Name, errs.Count, errs.Cells(1).Address))
    except Exception:
        pass
say("")
say("Checks sheet:")
r = 4
while True:
    txt = wsK.Range("B%d" % r).Value
    if txt is None:
        break
    res = wsK.Range("D%d" % r).Value
    val = wsK.Range("C%d" % r).Value
    say("  %-2s %-95s %-28s %s" % (r - 3 if txt != "overall" else "", txt, "" if val is None else val, res))
    if txt == "overall" and res != "PASS":
        fail("Checks overall = %s" % res)
    if res == "FAIL":
        fail("Check '%s' failed" % txt)
    if txt == "overall":
        break
    r += 1
say("")
say("PolicyMatrix rows 7-12 (live, Mode=REBUILD, Conv=NOPHASE, Yr=%d):" % yr)
cols = ["A", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U", "AR", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ"]
say("  " + " ".join("%9s" % c for c in cols))
for rr in range(7, 13):
    vals = []
    for c in cols:
        v = wsP.Range("%s%d" % (c, rr)).Value
        vals.append("%9s" % (v if not isinstance(v, float) else ("%9.4f" % v)))
    say("  " + " ".join(vals))
say("")
say("C3:", wsP.Range("C3").Value)
say("C4:", wsP.Range("C4").Value)
say("Trajectories F26:M29:", [[wsP.Cells(rw, cc).Value for cc in range(6, 14)] for rw in range(26, 30)])

wb.Save()
wb.Close(SaveChanges=False)
xl.Quit()
say("")
say("RESULT:", "ALL PASSED" if not FAILS else "%d FAILURE(S)" % len(FAILS))
with open(REPORT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if not FAILS else 1)
