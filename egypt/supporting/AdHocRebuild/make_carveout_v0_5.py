"""CBAM carve-out of Table 2 (2030), final v1.6: carve-out v0.4 with product-specific output elasticities
(OutputElasticity_Note_v0.2: cement -0.10, steel -0.40, fertilisers -0.40, aluminium -0.50; was -0.5 for all).

The kernel stores 2030 product outputs and sector emissions computed with eps = -0.5. Because emissions scale linearly with
output, the response to a different eps is exact per product: ratio_i = (1 + dp_i)^(eps_new) / (1 + dp_i)^(-0.5), with
dp_i = net carbon cost / product price. This mirror applies those ratios to the stored kernel block rows (policy rows 773-788,
product outputs 675-682) and to the block revenue / fund items of Table2_Industry, then reruns the carve-out arithmetic
(make_carveout_v0_4). Approximations: the 3C fund is scaled with block payments (shadow price not re-solved); kernel N is
shifted by the change in the output weights. The kernel rebuild (build_v1_6.py) gives the exact values; its live results are
written to carveout_v1_6_results_live.json and the documents can be regenerated from them.

Writes carveout_v1_6_results.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_carveout_v0_3 as base  # noqa: E402
import make_carveout_v0_4 as v4  # noqa: E402

KP = json.load(open(HERE.parent.parent / "archive" / "AdHocRebuild" / "kernel_products_2030.json", encoding="utf8"))
PRICE = [750, 680, 620, 110, 450, 380, 320, 2400]
EPS_OLD = -0.5
# DRI-EAF, Scrap-EAF, BF-BOF, clinker, ammonia, urea, AN, aluminium
EPS_NEW = [-0.40, -0.40, -0.40, -0.10, -0.40, -0.40, -0.40, -0.50]
SECTOR_PRODS = {"mch": (4, 5, 6), "irn": (0, 1, 2), "nfm": (7,), "cem": (3,)}
OUT_ROWS = 675        # policy product output rows 675..682
POL = 399


def ratios(bd):
    d = KP[bd]
    tau, pp, obr = d["tau"], d["pp"], d["obr"]
    out = []
    for p, pr, e in zip(d["prods"], PRICE, EPS_NEW):
        if not p["Q"]:
            out.append(1.0)
            continue
        F, G = p["F0"], p["P0"]
        dp = (tau * F + pp * G - min(obr, tau) * F - min(obr, pp) * G) / pr
        out.append((1 + dp) ** e / (1 + dp) ** EPS_OLD)
    return out


def apply():
    """Patch base.BLK / base.T2 in place with the new-eps values; return the list of scale factors."""
    info = {}
    for bd in base.BUNDLES:
        r = ratios(bd)
        prods = KP[bd]["prods"]
        blk, t2 = base.BLK[bd], base.T2[bd]
        # product outputs
        for k in range(8):
            row = str(OUT_ROWS + k)
            blk[row][3] = blk[row][3] * r[k]
        # sector fuel / process rows (policy block)
        for s, (rf, rp) in base.SEC.items():
            idx = SECTOR_PRODS[s]
            fuel = [prods[i]["fuel"] + prods[i]["dfuel"] for i in idx]
            proc = [prods[i]["proc"] + prods[i]["dproc"] for i in idx]
            fr = sum(f * r[i] for f, i in zip(fuel, idx)) / sum(fuel) if sum(fuel) else 1.0
            pr_ = sum(f * r[i] for f, i in zip(proc, idx)) / sum(proc) if sum(proc) else 1.0
            blk[str(rf + POL)][3] *= fr
            blk[str(rp + POL)][3] *= pr_
        # block process revenue (T73) and fund (T75)
        procs = [p["proc"] + p["dproc"] for p in prods]
        tp = sum(procs)
        if tp:
            t2["73"] *= sum(x * ri for x, ri in zip(procs, r)) / tp
        if t2["75"]:
            pay = [KP[bd]["tau"] * p["fuel"] + KP[bd]["pp"] * (p["proc"] + p["dproc"]) for p in prods]
            t2["75"] *= sum(x * ri for x, ri in zip(pay, r)) / sum(pay)
        info[bd] = [round(x, 4) for x in r]
    return info


def main():
    # kernel N before / after the change (mirror of the kernel formula) to shift the stored kernel N
    n_old = {bd: base.n_kernel(bd) for bd in base.BUNDLES}
    info = apply()
    for bd in base.BUNDLES:
        base.T2[bd]["87"] += base.n_kernel(bd) - n_old[bd]
    f, R = v4.carve()
    out = {b: dict(R[b]) for b in base.BUNDLES}
    json.dump({"results": out, "ratios": info, "eps": EPS_NEW}, open(HERE / "carveout_v1_6_results.json", "w"), indent=1)
    old = json.load(open(HERE / "carveout_v1_5_results.json", encoding="utf8"))
    print("scenario: K new (old) | P | Q | T | N | cement ratio")
    for b in base.BUNDLES:
        r, o = R[b], old[b]
        print(b, "K %.2f (%.2f) | P %.3f (%.3f) | Q %.0f (%.0f) | T %.2f (%.2f) | N %.2f (%.2f) | %.3f" % (
            r["K"], o["K"], r["P"], o["P"], r["Q"], o["Q"], r["T"], o["T"], r["N"], o["N"], info[b][3]))


if __name__ == "__main__":
    main()
