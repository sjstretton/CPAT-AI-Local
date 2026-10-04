"""National constants of the CPAT runs from the exported csv (cpat_outputs_egypt_2022_2041.csv format).

Usage:  python cpat_run_constants.py [csv_path] [year]      (default: the current csv, 2030)
Prints, per run, the quantities the carve-out uses (Table2_Industry rows 47-54 logic) and kappa, and checks them against the
values the final Table 2 was built on. After a new EG3 run, replace the EG3 rows of the csv and run this first: kappa should
be about 1."""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FUELS = ["coa", "die", "gso", "lpk", "nga", "oil"]
DEATHS = ["egy.air.ada.u24", "egy.air.ada.2464", "egy.air.ada.65"]
EXPECTED = {   # values behind the final Table 2 (2030)
    "EG1": dict(ghg0=594.156, enr0=340.66, ind0=88.973, ind1=76.6, kappa=1.0),
    "EG2": dict(ind1=75.971, kappa=1.0),
    "EG3": dict(ind1=80.422, kappa=0.537, rec=0.93, deaths=546.0, dghg=-21.542, dE=-13.207, dippu=-8.262),
}


def load(path):
    rows = list(csv.reader(open(path, encoding="utf8")))
    hdr = rows[0]
    out = {}
    for r in rows[1:]:
        out[(r[0], r[1])] = dict(zip(hdr[4:], [float(x) if x not in ("", None) else 0.0 for x in r[4:]]))
    return out


def constants(path=None, year="2030"):
    path = path or os.path.join(HERE, "cpat_outputs_egypt_2022_2041.csv")
    d = load(path)
    g = lambda code, run: d[(code, run)][year]
    res = {}
    for run in ("EG1", "EG2", "EG3", "EG4"):
        ind0, enr0 = g("egy.mit.co2.ind.1", run), g("egy.mit.co2.enr.tot.1", run)
        eff, cp = g("egy.mit.eff.cptraj.2", run), g("egy.mit.cptraj.2", run)
        res[run] = dict(
            ghg0=g("egy.mit.ghg.tot.inc.1", run), enr0=enr0, ind0=ind0, ind1=g("egy.mit.co2.ind.2", run),
            rec=sum(g("egy.mit.rev.new.%s.usd.2" % f, run) for f in FUELS), deaths=sum(g(c, run) for c in DEATHS),
            dghg=g("egy.mit.ghg.tot.inc.2", run) - g("egy.mit.ghg.tot.inc.1", run),
            dE=g("egy.mit.co2.enr.tot.2", run) - enr0, dind=g("egy.mit.co2.ind.2", run) - ind0,
            dippu=g("egy.mit.ghg.ipr.tot.2", run) - g("egy.mit.ghg.ipr.tot.1", run),
            price=cp, eff_price=eff, kappa=min(1.0, (eff / cp) * enr0 / ind0) if cp and ind0 else 1.0)
    return res


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    year = sys.argv[2] if len(sys.argv) > 2 else "2030"
    res = constants(path, year)
    ok = True
    for run, v in res.items():
        print(run, {k: round(x, 3) for k, x in v.items()})
        for k, e in EXPECTED.get(run, {}).items():
            if abs(v[k] - e) > max(0.0015 * abs(e), 0.002):
                ok = False
                print("   differs from the value behind the final Table 2: %s = %.3f (was %.3f)" % (k, v[k], e))
    json.dump(res, open(os.path.join(HERE, "cpat_run_constants.json"), "w"), indent=1)
    print("matches the values behind the final Table 2" if ok else "DIFFERS from the values behind the final Table 2 (expected after a new run)")


if __name__ == "__main__":
    main()
