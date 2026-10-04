"""Check that the final Table 2 numbers printed in the final documents equal the independent Python mirror
(carveout_v1_5_results.json, from make_carveout_v0_4.py). Runs anywhere (no Excel). The workbook-side check is
kernel sheet Table2_Final (build_v1_5.py). Usage: python check_final_documents.py"""
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.abspath(os.path.join(HERE, "..", "..", "final"))
R = json.load(open(os.path.join(HERE, "carveout_v1_5_results.json"), encoding="utf8"))
B = ["1A", "2A", "2B", "3A", "3B", "3C"]
M = {"1A": 100, "2A": 44, "2B": 44, "3A": 100, "3B": 100, "3C": 100}
fails = []


def rnd(x, dp):
    q = 10 ** dp
    return (int(abs(x) * q + 0.5 + 1e-9) / q) * (1 if x >= 0 else -1)


def num(s):
    s = s.replace("−", "-").replace(",", "").replace("%", "").strip()
    return float(s)


def rows(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf8")
    x = re.sub(r"<w:del\b.*?</w:del>", "", x, flags=re.S)
    out = []
    for tr in re.findall(r"<w:tr[ >].*?</w:tr>", x, flags=re.S):
        cells = []
        for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, flags=re.S):
            cells.append("".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", tc, flags=re.S)).strip())
        out.append(cells)
    return out


def check(name, got, exp, tol=0.0005):
    if abs(got - exp) > tol:
        fails.append("%s: document %s vs mirror %s" % (name, got, exp))


# 1. carve-out note, "Table 2 columns" table
spec = {"Coverage, % of GHG (J)": ("J", 0), "Revenue, $bn (P)": ("P", 1), "Emission cut, MtCO₂e (K)": ("K", 1),
        "Cut, % of GHG": ("L", 1), "CBAM intensity, % (N)": ("N", 1),
        "CBAM obligations per tonne exported, % (O)": ("O_final", 1), "CBAM block emissions, % (T)": ("T", 1),
        "Deaths avoided (Q)": ("Q", 0)}
seen = 0
for r in rows(os.path.join(F, "EGYPT_CarveOut_Table2_v1.5.docx")):
    if r and r[0] in spec and len(r) == 7:
        key, dp = spec[r[0]]
        for b, c in zip(B, r[1:]):
            check("carve-out %s %s" % (r[0], b), num(c), rnd(R[b][key], dp))
        seen += 1
    if r and r[0] == "CBAM coverage, % (M)":
        for b, c in zip(B, r[1:]):
            check("carve-out M %s" % b, num(c), M[b])
        seen += 1
if seen != 9:
    fails.append("carve-out note: found %d of 9 Table 2 rows" % seen)

# 2. tracked results text, Table 2 (one row per scenario; numbers in cells)
tr = rows(os.path.join(F, "EgyptResultsInitial_UpdatedResults_v1.5_tracked.docx"))
for r in tr:
    if r and r[0] in B and len(r) >= 9:
        b = r[0]
        vals = [c for c in r[1:] if re.fullmatch(r"[−-]?[\d,.]+%?", c)]
        # expected order after text cells: P, K, M, N, O, Q
        exp = [rnd(R[b]["P"], 1), rnd(R[b]["K"], 1), M[b], rnd(R[b]["N"], 1), rnd(R[b]["O_final"], 1), rnd(R[b]["Q"], 0)]
        got = [num(c) for c in vals][-6:]
        for name, g, e in zip("P K M N O Q".split(), got, exp):
            check("results text %s %s" % (b, name), g, e)
        seen += 1
if seen != 15:
    fails.append("results text: found %d of 6 scenario rows" % (seen - 9))

# 3. prose figures for 3B in the results text
x = zipfile.ZipFile(os.path.join(F, "EgyptResultsInitial_UpdatedResults_v1.5_tracked.docx")).read("word/document.xml").decode("utf8")
x = re.sub(r"<w:del\b.*?</w:del>", "", x, flags=re.S)
txt = "".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", x, flags=re.S))
for bad in ("19.1", "491", "CBAM producers", "USD0.6"):
    if bad in txt:
        fails.append("results text still contains %r" % bad)
for good in ("12.0", "330", "USD0.3 billion"):
    if good not in txt:
        fails.append("results text lacks %r" % good)

print("rows checked: %d; failures: %d" % (seen, len(fails)))
for f in fails:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
