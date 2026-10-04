"""Rebuild v0.5 notes: MethodologyNote_v0.5.md (current method) and ResultsComparison_Table2_v0.5.md, from the verified
workbook AdHocCalculations_Rebuild_v0.5.xlsx, the kernel v1.6 stored snapshot and the live final Table 2 results."""
import json
import os
import warnings

import openpyxl

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
B = ["1A", "2A", "2B", "3A", "3B", "3C"]
MINUS = "−"
rb = openpyxl.load_workbook(os.path.join(HERE, "AdHocCalculations_Rebuild_v0.5.xlsx"), data_only=True)
pm, rs = rb["PolicyMatrix"], rb["Results"]
ker = openpyxl.load_workbook(os.path.join(ROOT, "egypt", "final", "CPAT_Industry_Kernel_Egypt_v1.6.xlsx"), data_only=True)["Table2_Industry"]
FIN = json.load(open(os.path.join(HERE, "carveout_v1_6_results_live.json"), encoding="utf8"))


def rnd(x, dp):
    q = 10 ** dp
    return (int(abs(x) * q + 0.5 + 1e-9) / q) * (1 if x >= 0 else -1)


def f(x, dp=1, comma=False):
    v = rnd(x, dp)
    s = (("{:,.%df}" if comma else "{:.%df}") % dp).format(abs(v))
    return (MINUS + s) if v < 0 else s


def pmv(c):
    return [pm["%s%d" % (c, r)].value for r in range(7, 13)]


def res(key):
    for row in rs.iter_rows(min_row=4, max_row=rs.max_row):
        if row[1].value == key:
            return [c.value for c in row[2:8]]


# prototype (kernel composition) stored snapshot rows 103-108: C.. = J K L M N O P Q R T U AR
proto = {}
for r in range(103, 109):
    code = ker.cell(r, 2).value
    vals = [ker.cell(r, c).value for c in range(6, 18)]
    proto[code] = dict(zip("J K L M N O P Q R T U AR".split(), vals))
assert list(proto) == B, list(proto)
J, K, L, Mv, N, O, P, Q, T, U, AR = (pmv(c) for c in ("J", "K", "L", "M", "N", "O", "P", "Q", "T", "U", "AR"))
Ofull, Onp, Pg, Reb = res("O_full"), res("O_nophase"), res("P_gross"), res("rebate_bn")
AF, AG, AH, AI, AJ, AK, AL = (pmv(c) for c in ("AF", "AG", "AH", "AI", "AJ", "AK", "AL"))


def row(label, vals):
    return "| %s | %s |" % (label, " | ".join(vals))


def hdr():
    return "| Source | 1A | 2A | 2B | 3A | 3B | 3C |\n|---|---|---|---|---|---|---|"


# ------------------------------------------------------------ methodology note
s = open(os.path.join(HERE, "MethodologyNote_v0.4.md"), encoding="utf8").read()
s = s.replace("methodology note v0.4", "methodology note v0.5").replace("AdHocCalculations_Rebuild_v0.4", "AdHocCalculations_Rebuild_v0.5")
s = s.replace("build_adhoc_rebuild_v0_4", "build_adhoc_rebuild_v0_5").replace("recalc_and_check_adhoc_v0_4", "recalc_and_check_adhoc_v0_5")
a = "IPCC beta anchor `PStar` = 122 USD2024;"
assert a in s
s = s.replace(a, "output elasticity by product (`EpsQ1`..`EpsQ8`: cement −0.10, steel and fertilisers −0.40, aluminium −0.50; the uniform `EpsQ` = −0.5 applies in PROTOTYPE mode); " + a, 1)
s = s.replace("eps_Q = -0.5;", "eps_Q by product (defaults paragraph);")
i = s.index("## 3. Results, 2030"); j = s.index("Verification: `Mode = PROTOTYPE`")
t = []
t.append("## 3. Results, 2030 (Mode = REBUILD, Conv = FULL, EFSet = EGY_EF_V01, KappaMode = SCALE, ThetaOther = 1)\n")
t.append("The EG3 industry scenarios (3A/3B/3C) approximate a full-coverage EG3 run with `KappaMode` = SCALE (1/kappa scaling; a linear approximation, not a CPAT re-run). O is shown for the default FULL convention and, in parentheses, NOPHASE.\n")
t.append("| Metric | 1A | 2A | 2B | 3A | 3B | 3C |\n|---|---:|---:|---:|---:|---:|---:|")
t.append(row("J coverage, % GHG", [f(100 * x) for x in J]))
t.append(row("K reduction, Mt", [f(x, 2) for x in K]))
t.append(row("L, % of GHG", [f(100 * x, 2) for x in L]))
t.append(row("M CBAM coverage, %", [f(100 * x) for x in Mv]))
t.append(row("N intensity, %", [f(100 * x, 2) for x in N]))
t.append(row("O obligation per unit, % FULL (NOPHASE)", ["%s (%s)" % (f(100 * a, 2), f(100 * b, 2)) for a, b in zip(Ofull, Onp)]))
t.append(row("P net revenue, $bn", [f(x, 2) for x in P]))
t.append(row("P gross revenue, $bn", [f(x, 2) for x in Pg]))
t.append(row("Rebates, $bn", [f(x, 2) for x in Reb]))
t.append(row("Q deaths avoided", [f(x, 0, True) for x in Q]))
t.append(row("T block emissions, %", [f(100 * x) for x in T]))
t.append(row("U block output, %", [f(100 * x) for x in U]))
t.append(row("AR Dnet revenue, $bn", [f(x, 2) for x in AR]))
t.append("\nK decomposition (PolicyMatrix AF-AM, Mt):\n")
t.append("| Bundle | AF DeltaGHG_adj | AG -DeltaIPPU_adj | AH IPPU_other | AI ER_p | AJ emrq_proc | AK D_obr | AL F_fund | AM check |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for k in range(6):
    t.append("| %s | %s | %s | %s | %s | %s | %s | %s | 0.00 |" % (B[k], f(AF[k], 2), f(AG[k], 2).replace(MINUS, ""), f(AH[k], 2).replace(MINUS, ""),
                                                               f(AI[k], 2), f(AJ[k], 2), f(AK[k], 2).replace(MINUS, ""), f(AL[k], 2)))
t.append("\n3B: with `ThetaOther` = 1 the rebate (2.18 $bn: 1.25 to CBAM producers, 0.94 to the rest of covered industry) offsets almost all of the gross revenue, so net P is about 0, and D_obr removes the output channel for all covered industry. With the product-specific elasticities, output falls only 1.5% in the priced scenarios (cement −0.10 carries almost all of the output channel).\n")
s = s[:i] + "\n".join(t) + "\n" + s[j:]
open(os.path.join(HERE, "MethodologyNote_v0.5.md"), "w", encoding="utf8").write(s)

# ------------------------------------------------------------ results comparison
o = ["# Table 2 of EgyptResultsInitial.docx, the final Table 2, the rebuilt ad hoc calculations and the prototype: what differs and why (2030), v0.5\n",
     "**Sources.**\n",
     "- (i) Table 2 and the narrative of `EgyptResultsInitial.docx`.",
     "- (ii) The final Table 2: CBAM carve-out (`EGYPT_CarveOut_Table2_v1.6`; kernel sheets `CarveOut_Table2`, `Table2_Final`).",
     "- (iii) Rebuild v0.5: `AdHocCalculations_Rebuild_v0.5.xlsx`, `Mode` = REBUILD, `Conv` = FULL, `ThetaOther` = 1, `KappaMode` = SCALE (see `MethodologyNote_v0.5.md`).",
     "- (iv) Prototype: kernel `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`, sheet `Table2_Industry` (stored 2030 snapshot, kernel composition).\n",
     "All values are for 2030 at USD 20/t. The rebuild and the prototype scale EG3 to full industrial coverage (a linear approximation); the final Table 2 uses EG3 as run. All three models use output elasticities by product (cement −0.10, steel and fertilisers −0.40, aluminium −0.50; the rebuild's PROTOTYPE mode keeps −0.5).\n",
     "## 1. Side by side (2030)\n"]
oT = {"K": (-41.6, -38.9, -41.0, -21.5, -18.1, -24.5), "P": (5.8, 5.2, 5.2, 1.1, 0.0, 0.0), "Q": (1656, 1564, 1631, 546, 345, 621),
      "N": (-7.6, -5.5, -5.5, -7.6, -7.6, -13.1), "O": (-26.1, -13.9, -13.9, -26.1, -7.6, -30.4), "J": (72, 65, 65, 20, 20, 20)}


def block(title, key, ofin, orb, opr, dp, comma=False):
    o.append("**%s**\n" % title)
    o.append(hdr())
    o.append(row("Table 2 (initial)", [f(x, dp, comma) for x in oT[key]]))
    if ofin:
        o.append(row("Final Table 2", [f(x, dp, comma) for x in ofin]))
    o.append(row("Rebuild v0.5", orb))
    o.append(row("Prototype", opr))
    o.append("")


block("Total emissions reduction, MtCO₂e (K)", "K", [FIN[b]["K"] for b in B], [f(x, 1) for x in K], [f(proto[b]["K"], 1) for b in B], 1)
block("Carbon revenue, $bn (P)", "P", [FIN[b]["P"] for b in B], [f(x, 1) for x in P], [f(proto[b]["P"], 1) for b in B], 1)
block("Air-pollution deaths avoided per year (Q)", "Q", [FIN[b]["Q"] for b in B], [f(x, 0, True) for x in Q], [f(proto[b]["Q"], 0, True) for b in B], 0, True)
block("CBAM-sector emission intensity change, % (N)", "N", [FIN[b]["N"] for b in B], [f(100 * x, 1) for x in N], [f(proto[b]["N"], 1) for b in B], 1)
block("National GHG covered, % (J)", "J", [FIN[b]["J"] for b in B], [f(100 * x, 1) for x in J], [f(proto[b]["J"], 1) for b in B], 0)
o.append("**CBAM obligations, % per unit exported (O).** The final Table 2 reports the intensity-only measure (−5.4 / −2.6 / −2.7 / −5.4 / −5.4 / −20.7). The rebuild and the prototype report the deduction-based obligation; it is not comparable with the final row O.\n")
o.append(hdr())
o.append(row("Table 2 (initial, ≈ NOPHASE)", [f(x, 1) for x in oT["O"]]))
o.append(row("Rebuild FULL (NOPHASE)", ["%s (%s)" % (f(100 * a, 1), f(100 * b, 1)) for a, b in zip(Ofull, Onp)]))
o.append(row("Prototype FULL", [f(proto[b]["O"], 1) for b in B]))
o.append("")
o.append("**Other PolicyMatrix columns** (rebuild; not in Table 2): T block emissions, % " + ", ".join("%s %s" % (b, f(100 * x)) for b, x in zip(B, T)) +
         ". U block output, % " + ", ".join("%s %s" % (b, f(100 * x)) for b, x in zip(B, U)) + ". AR change in net revenue, $bn " +
         ", ".join("%s %s" % (b, f(x, 2)) for b, x in zip(B, AR)) + ".\n")
o.append("## 2. Why the models differ\n")
o += ["- **Scope of the national response.** The final Table 2 keeps CPAT's own response everywhere except the CBAM block and uses EG3 as run, so 3A–3C are lower bounds (coverage 14%). The rebuild and the prototype scale EG3's industry response by 1/κ (κ = 0.537), which raises coverage to 18.5–20.8% and the 3A–3C reductions.",
      "- **IPPU.** The final Table 2 keeps CPAT's proportional IPPU response for non-CBAM IPPU. The rebuild removes CPAT's IPPU scaling altogether (`IppuOther` = NONE); the prototype replaces it by the kernel's IPPU. This is the main reason the rebuild's 1A–2B cuts (−27 to −30 Mt) are smaller than the final Table 2's.",
      "- **3B rebate scope.** The rebuild and the final Table 2 rebate all covered industry; the prototype rebates the CBAM block only, so its 3B cut is larger and its revenue higher.",
      "- **3C fund.** The rebuild sends all industrial carbon revenue to the fund at a fixed USD 20/t shadow price (net revenue 0). The prototype's fund equals the block's own payments after abatement, solved as a fixed point, and the final Table 2 takes the prototype's fund.",
      "- **Data vintage.** The prototype combines changes from two CPAT data vintages (industry energy CO₂ 75.4 Mt stored against 89.0 Mt in the new Egypt runs); this lowers its coverage and revenue for 3A–3C.",
      "- **Fixed block fuel intensity in the prototype.** Its CBAM intensity change for 2A/2B is 0 (rebuild and final Table 2 about −2%).",
      "- **Obligations.** The rebuild and the prototype compute a deduction-based obligation (FULL: 2030 phase-in, CBAM factor 0.485; NOPHASE: factor 1). The final Table 2 reports the CBAM-product intensity change only.\n",
      "## 3. Internal inconsistencies in EgyptResultsInitial.docx\n",
      "1. **3B reduction:** the table gives −18.1 Mt, the text 13.6 Mt.",
      "2. **Mixed bases.** \"5–17% of Egypt's annual CO₂ of about 249 Mt\" uses a CO₂-only base, while the coverage shares use total GHG (594 Mt).",
      "3. **Obligations and intensity:** the text says \"about 8 to 30%\" for obligations and \"nearly 8%\" for intensity, while the table gives −7.6%.",
      "4. **3A revenue:** 1.1 $bn (gross block payments) against 2.38 in the workbook cell.",
      "5. **Coverage:** 72/65% is typed in; the workbook's own columns imply 59/53% and 24.3%.\n",
      "## 4. Caveats that matter for this comparison\n",
      "- The 1/κ scaling is linear; a full-coverage EG3 CPAT run would differ (fuel mix of aluminium and other manufacturing, general-equilibrium effects).",
      "- The 3C fund convention and the 3B rebate scope differ between the models (section 2).",
      "- Block fuel intensity is fixed in the prototype; process β is not routed to fp.",
      "- Provisional parameters: the Egypt EF v0.1 VERIFY list is open; AN 50% abatement blend; aluminium combined β; ammonia/urea β = 0; output elasticities are judgements (Low–Medium confidence). See `EGYPT_FinalCaveats_v1.6`.\n"]
open(os.path.join(HERE, "ResultsComparison_Table2_v0.5.md"), "w", encoding="utf8").write("\n".join(o))
print("written")
