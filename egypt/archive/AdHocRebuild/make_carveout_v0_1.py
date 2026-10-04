"""CBAM carve-out of Table 2 (2030), v0.1.

Original CPAT run results everywhere except the CBAM block, which comes from kernel v0.16.
  K = CPAT dGHG(run) - r(run) * B + dB
    r  = CPAT industry energy CO2 % change of the run (csv); CPAT scales all IPPU by the same %,
         so r * B is what CPAT implicitly assigns to the block (fuel + process).
    B, dB = kernel block emissions (fuel + process) 2030 baseline and policy change, by sector,
         rescaled so 2024-2030 growth matches CPAT sector energy CO2 growth (irn, cem); mch and nfm
         have CPAT sector energy = 0, so they follow total CPAT industry energy CO2 growth.
  3A-3C use CPAT run EG3 as run (no 1/kappa scaling).
Inputs: carveout_kernel_block_2030.json, carveout_kernel_table2_2030.json (kernel v0.16 via Excel COM,
Settings!B10 = bundle), CPAT csv national values (CPAT_National sheet).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
BLK = json.load(open(HERE / "carveout_kernel_block_2030.json", encoding="utf8"))
T2 = json.load(open(HERE / "carveout_kernel_table2_2030.json", encoding="utf8"))
BUNDLES = ("1A", "2A", "2B", "3A", "3B", "3C")
RUN = {"1A": "EG1", "2A": "EG1", "2B": "EG2", "3A": "EG3", "3B": "EG3", "3C": "EG3"}
GHG0 = 594.156                      # CPAT total GHG incl. LULUCF, baseline 2030 (csv)
ENR0 = 340.66                       # CPAT energy CO2, baseline 2030 (csv)
IND0 = 88.973                       # CPAT industry energy CO2, baseline 2030 (csv)
IND1 = {"EG1": 76.6, "EG2": 75.971, "EG3": 80.422}
KAPPA_EG3 = 0.537
TAU = 20.0
# kernel Mitigation_Industry rows (scenario 1 baseline; +399 = scenario 2 policy): fuel, process
SEC = {"mch": (374, 385), "irn": (375, 386), "nfm": (376, 387), "cem": (378, 389)}
# CPAT growth 2024 -> 2030 (kernel stored vintage, Emissions_Industry / IPPU_Industry)
CPAT_G = {"irn": 5.469979 / 4.329075, "cem": 10.913917 / 8.974050, "ind": 75.384270 / 57.158577}
# CBAM metrics kept from kernel v0.16 (O on NOPHASE, as Table 2)
N = {"1A": -3.6, "2A": 0.0, "2B": 0.0, "3A": -3.6, "3B": -3.6, "3C": -21.1}
O = {"1A": -22.3, "2A": -10.5, "2B": -10.5, "3A": -22.3, "3B": -2.9, "3C": -34.6}
M = {"1A": 100, "2A": 44, "2B": 44, "3A": 100, "3B": 100, "3C": 100}
ORIG = {"P": (5.8, 5.2, 5.2, 1.1, 0.0, 0.0), "K": (-41.6, -38.9, -41.0, -21.5, -18.1, -24.5),
        "Q": (1656, 1564, 1631, 546, 345, 621), "J": (72, 65, 65, 20, 20, 20)}
PROTO = {"P": (6.9, 6.3, 6.2, 1.9, 1.0, 0.7), "K": (-29.0, -25.5, -26.7, -21.1, -17.4, -32.9),
         "Q": (1421, 1421, 1473, 816, 746, 985), "J": (63, 57, 57, 19, 19, 19)}


def v(bd, row, yi=3):
    return BLK[bd][str(row)][yi] or 0.0


def factors():
    f = {}
    for s, (rf, rp) in SEC.items():
        b24, b30 = v("1A", rf, 2) + v("1A", rp, 2), v("1A", rf) + v("1A", rp)
        f[s] = CPAT_G.get(s, CPAT_G["ind"]) / (b30 / b24)
    return f


def carve():
    f, res = factors(), {}
    for bd in BUNDLES:
        t = T2[bd]
        run = RUN[bd]
        r = IND1[run] / IND0 - 1
        Bf = sum(f[s] * v(bd, rf) for s, (rf, rp) in SEC.items())
        Bp = sum(f[s] * v(bd, rp) for s, (rf, rp) in SEC.items())
        dF = sum(f[s] * (v(bd, rf + 399) - v(bd, rf)) for s, (rf, rp) in SEC.items())
        dP = sum(f[s] * (v(bd, rp + 399) - v(bd, rp)) for s, (rf, rp) in SEC.items())
        adj_f, adj_p = dF - r * Bf, dP - r * Bp
        dghg, dE, deaths, rec = t["49"], t["51"], t["48"], t["47"]
        K = dghg + adj_f + adj_p
        Q = deaths * (dE + adj_f) / dE
        P = rec + TAU * adj_f / 1000 + t["73"] - t["74"] - t["75"]
        cov_e = ENR0 if bd[0] in "12" else KAPPA_EG3 * IND0
        J = 100 * (cov_e + (Bp if bd in ("1A", "3A", "3B", "3C") else 0)) / GHG0
        res[bd] = dict(r=100 * r, B=Bf + Bp, dB=dF + dP, cpat_blk=r * (Bf + Bp), adj=adj_f + adj_p,
                       K=K, L=100 * K / GHG0, P=P, Q=Q, J=J, dghg=dghg, deaths=deaths, rec=rec)
    return f, res


def fmt(x, d=1):
    return ("{:,.%df}" % d).format(x).replace("-", "\u2212")


def main():
    f, R = carve()
    hd = "| | " + " | ".join(BUNDLES) + " |\n|---|" + "---|" * len(BUNDLES) + "\n"
    row = lambda lab, vals, d=1: "| %s | %s |\n" % (lab, " | ".join(fmt(x, d) for x in vals))
    md = ["# Egypt Table 2 (2030): CPAT results with a CBAM carve-out, v0.1\n",
          "**What this is.** The original CPAT runs give every result, except the CBAM block (steel, cement, "
          "fertilisers, aluminium). For the block, CPAT's implied change is taken out and kernel v0.16's "
          "product-level change is put in. 3A\u20133C use CPAT run EG3 exactly as run (no scaling to full "
          "industry coverage). Carbon price USD 20/t in 2030 in every bundle.\n",
          "## Table 2 columns\n", hd,
          row("Coverage, % of GHG (J)", [R[b]["J"] for b in BUNDLES], 0),
          row("Revenue, $bn (P)", [R[b]["P"] for b in BUNDLES]),
          row("Emission cut, MtCO\u2082e (K)", [R[b]["K"] for b in BUNDLES]),
          row("Cut, % of GHG", [R[b]["L"] for b in BUNDLES]),
          row("CBAM coverage, % (M)", [M[b] for b in BUNDLES], 0),
          row("CBAM intensity, % (N)", [N[b] for b in BUNDLES]),
          row("CBAM obligations per unit, % (O, NOPHASE)", [O[b] for b in BUNDLES]),
          row("Deaths avoided (Q)", [R[b]["Q"] for b in BUNDLES], 0),
          "\n## Comparison\n", hd]
    for key, lab, d in (("K", "Emission cut, Mt", 1), ("P", "Revenue, $bn", 1), ("Q", "Deaths avoided", 0)):
        md.append(row(lab + ": original Table 2", ORIG[key], d))
        md.append(row(lab + ": **carve-out**", [R[b][key] for b in BUNDLES], d))
        md.append(row(lab + ": prototype v0.16", PROTO[key], d))
    md += ["\n## How K is built, MtCO\u2082e\n", hd,
           row("CPAT \u0394GHG of the run", [R[b]["dghg"] for b in BUNDLES]),
           row("CPAT industry change, % (applied to block)", [R[b]["r"] for b in BUNDLES]),
           row("Block emissions, baseline (fuel + process)", [R[b]["B"] for b in BUNDLES]),
           row("less: CPAT's implied block change", [-R[b]["cpat_blk"] for b in BUNDLES]),
           row("plus: kernel block change", [R[b]["dB"] for b in BUNDLES]),
           row("**K**", [R[b]["K"] for b in BUNDLES]),
           "\n## Method notes\n",
           "- **Runs.** 1A and 2A = EG1, 2B = EG2, 3A\u20133C = EG3 (CPAT csv, 2030).\n",
           "- **IPPU.** CPAT scales all IPPU with industrial energy CO\u2082. The carve-out keeps that for "
           "non-CBAM IPPU (about 50 Mt, mainly F-gases and other process emissions) and replaces it only for "
           "the block. Prototype v0.16 held non-CBAM IPPU fixed, which is most of why its 1A cut was lower.\n",
           "- **Growth.** Block output is rescaled so 2024\u20132030 growth matches CPAT sector energy CO\u2082: "
           "steel (irn) x%.3f, cement (cem) x%.3f. CPAT has no energy in mining & chemicals (mch) or "
           "non-ferrous metals (nfm) for Egypt, so fertilisers (mch) x%.3f and aluminium (nfm) x%.3f follow "
           "total CPAT industry growth.\n" % (f["irn"], f["cem"], f["mch"], f["nfm"]),
           "- **Sectors.** irn = iron and steel; cem = cement (non-metallic minerals); mch = mining and "
           "chemicals (ammonia, urea, ammonium nitrate); nfm = non-ferrous metals (aluminium).\n",
           "- **Revenue P.** CPAT carbon-tax receipts of the run, plus the block fuel-revenue adjustment, plus "
           "block process fees; less the 3B output-based rebate and the 3C abatement fund (kernel v0.16).\n",
           "- **Deaths Q.** CPAT deaths of the run, scaled by (CPAT \u0394energy CO\u2082 + block fuel "
           "adjustment) / CPAT \u0394energy CO\u2082.\n",
           "- **Coverage J.** 1A: all energy CO\u2082 plus block process; 2A/2B: energy CO\u2082; 3A\u20133C: "
           "EG3's priced industry energy (\u03ba = 0.537 of 89.0 Mt) plus block process.\n",
           "- **M, N, O** are kernel v0.16 values. The growth rescaling only reweights sectors, so they are "
           "not recomputed.\n",
           "- **Why 3A\u20133C are low.** EG3 prices only about 54 % of industrial energy CO\u2082, as CPAT ran it.\n"]
    import re
    txt = re.sub(r"(?m)^(#.*\n)", r"\1\n", "".join(md)).replace("put in. 3A", "put in. 3A").replace("in every bundle.\n", "in every bundle.\n\n")
    txt = re.sub(r"(?m)^(- \*\*Runs)", r"\1", txt)
    out = HERE.parent.parent / "EGYPT_CarveOut_Table2_v0.1.md"
    out.write_text(txt, encoding="utf-8")
    print(txt[:400])


if __name__ == "__main__":
    main()
