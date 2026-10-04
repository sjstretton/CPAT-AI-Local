"""CBAM carve-out of Table 2 (2030), final v1.5: carve-out v0.3 plus the 3B rebate decision (2026-10-04).

Everything is as in make_carveout_v0_3.py (imported; O is the intensity-only measure and is not computed here)
except 3B, where the output-based rebate now covers ALL covered industry (rebuild switch ThetaOther = 1):

  * The rebate neutralises the output channel of CPAT's response in non-block covered industry. CPAT's response
    of that industry (fuel plus its proportional IPPU) is  NB = dInd + dIPPU - r x (Bf + Bp);  the output share
    of it, (1 - s_int) = 2/3, is removed:  D_nb = -(1 - s_int) x NB.
  * Deaths: the fuel part only, D_nb_f = -(1 - s_int) x (dInd - r x Bf), enters the energy-CO2 adjustment.
  * Revenue: the rebate to non-block covered industry, tau x (kappa x IND1 - block post-policy fuel CO2) / 1000,
    is deducted. As in carve-out v0.3 there is no feedback of the changed emissions onto receipts.
  * N, M, O, T, J are unchanged (the block is already unaffected by the rebate; coverage is of the run).

Writes carveout_v1_5_results.json (read by build_v1_5.py as the independent check and by the document scripts).
Inputs: the kernel extracts used by make_carveout_v0_3.py (kernel v0.16 block / Table2_Industry values).
"""
import json
from pathlib import Path

import make_carveout_v0_3 as base

HERE = Path(__file__).parent
THETA_OTHER = 1
DIPPU_EG3 = None            # filled from the stored CPAT IPPU change of the run (Table2_Industry T50)

# CPAT national IPPU change of the run, 2030 (csv; Table2_Industry!T50): policy - baseline, MtCO2e
DIPPU = {"EG1": 74.015 - 85.97, "EG2": 73.407 - 85.97, "EG3": 77.708 - 85.97}
# published O (Table 2 row O, intensity-only; from EGYPT_Table2_Final_CBAMcalc, CBAM_calc row 5)
O_FINAL = {"1A": -5.423, "2A": -2.553, "2B": -2.69, "3A": -5.423, "3B": -5.423, "3C": -20.742}


def carve():
    f, R = base.carve()
    for bd in base.BUNDLES:
        R[bd]["D_nb"] = R[bd]["dnb_f"] = R[bd]["rebate_other"] = 0.0
    bd, run = "3B", base.RUN["3B"]
    r = R[bd]["r"] / 100
    Bf = sum(f[s] * base.v(bd, rf) for s, (rf, rp) in base.SEC.items())
    Bp = R[bd]["B"] - Bf
    dF = sum(f[s] * (base.v(bd, rf + 399) * (1 + base.i_fuel(bd)) - base.v(bd, rf)) for s, (rf, rp) in base.SEC.items())
    dind = base.IND1[run] - base.IND0
    NB = dind + DIPPU[run] - r * (Bf + Bp)
    D_nb = -(1 - base.S_INT) * NB * THETA_OTHER
    dnb_f = -(1 - base.S_INT) * (dind - r * Bf) * THETA_OTHER
    rebate_other = THETA_OTHER * base.TAU * (base.KAPPA_EG3 * base.IND1[run] - (Bf + dF)) / 1000
    t = base.T2[bd]
    R[bd].update(D_nb=D_nb, dnb_f=dnb_f, rebate_other=rebate_other)
    R[bd]["K"] += D_nb
    R[bd]["L"] = 100 * R[bd]["K"] / base.GHG0
    R[bd]["P"] -= rebate_other
    adj_f = dF - r * Bf
    R[bd]["Q"] = t["48"] * (t["51"] + adj_f + dnb_f) / t["51"]
    for b in base.BUNDLES:
        R[b]["O_final"] = O_FINAL[b]
    return f, R


def main():
    f, R = carve()
    out = {b: {k: v for k, v in R[b].items()} for b in base.BUNDLES}
    json.dump(out, open(HERE / "carveout_v1_5_results.json", "w"), indent=1)
    for b in base.BUNDLES:
        r = R[b]
        print(b, "K %.3f L %.3f P %.3f Q %.1f J %.3f N %.3f T %.3f O %.3f D_nb %.3f rebate_other %.3f" % (
            r["K"], r["L"], r["P"], r["Q"], r["J"], r["N"], r["T"], r["O_final"], r["D_nb"], r["rebate_other"]))


if __name__ == "__main__":
    main()
