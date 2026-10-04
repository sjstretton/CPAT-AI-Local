"""Carve-out mirror (final Table 2, 2030) for a NEW CPAT run: make_carveout_v0_5 with the CPAT national quantities read from a
csv (cpat_outputs_egypt_2022_2041.csv format) instead of the constants behind v1.6.

Usage:  python make_carveout_v0_6.py [csv_path] [out.json]
Default csv = the current one (then the result equals carveout_v1_6_results.json). After a full-coverage EG3 run, replace the
EG3 rows of the csv and run this to preview the new final Table 2. What is overridden for the runs: IND1, kappa, dIPPU and
Table2_Industry rows 47 (receipts), 48 (deaths), 49 (dGHG), 51 (dEnergy CO2). The CBAM block (kernel rows, output elasticities,
fund) does not depend on the CPAT run and is unchanged; the growth factors use EG1/baseline series (unchanged).
Writes carveout_v1_7_results.json (same layout as carveout_v1_6_results.json)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cpat_run_constants as crc  # noqa: E402
import make_carveout_v0_3 as base  # noqa: E402
import make_carveout_v0_4 as v4  # noqa: E402
import make_carveout_v0_5 as v5  # noqa: E402


def run(csv_path=None):
    c = crc.constants(csv_path)
    for r in ("EG1", "EG2", "EG3"):
        base.IND1[r] = c[r]["ind1"]
    base.GHG0, base.ENR0, base.IND0 = c["EG1"]["ghg0"], c["EG1"]["enr0"], c["EG1"]["ind0"]
    base.KAPPA_EG3 = c["EG3"]["kappa"]
    v4.DIPPU.update({r: c[r]["dippu"] for r in ("EG1", "EG2", "EG3")})
    for bd in base.BUNDLES:
        t, k = base.T2[bd], c[base.RUN[bd]]
        t["47"], t["48"], t["49"], t["51"] = k["rec"], k["deaths"], k["dghg"], k["dE"]
    n_old = {bd: base.n_kernel(bd) for bd in base.BUNDLES}
    v5.apply()
    for bd in base.BUNDLES:
        base.T2[bd]["87"] += base.n_kernel(bd) - n_old[bd]
    f, R = v4.carve()
    return c, R


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else None
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "carveout_v1_7_results.json")
    c, R = run(csv_path)
    json.dump({"results": {b: dict(R[b]) for b in base.BUNDLES}, "kappa_EG3": c["EG3"]["kappa"]}, open(out, "w"), indent=1)
    ref = json.load(open(os.path.join(HERE, "carveout_v1_6_results.json"), encoding="utf8"))["results"]
    print("kappa(EG3) = %.3f" % c["EG3"]["kappa"])
    print("scenario: K new (v1.6) | P | Q | J")
    for b in base.BUNDLES:
        r, o = R[b], ref[b]
        print(b, "K %.2f (%.2f) | P %.3f (%.3f) | Q %.0f (%.0f) | J %.1f (%.1f)" % (
            r["K"], o["K"], r["P"], o["P"], r["Q"], o["Q"], r["J"], o["J"]))


if __name__ == "__main__":
    main()
