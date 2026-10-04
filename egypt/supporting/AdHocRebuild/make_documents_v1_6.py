"""Regenerate the v1.6 document set (product-specific output elasticities) from a results JSON.

Usage:  python make_documents_v1_6.py [results.json]
Default: carveout_v1_6_results.json (Python mirror, 'results' key). After build_v1_6.py has run, use the live export:
        python make_documents_v1_6.py carveout_v1_6_results_live.json
Produces in egypt/final/: carve-out note, final caveats, CBAM obligation note, version notes (md_sources + docx), the tracked
results text and the methodology (docx edits from v1.5), and updates egypt-final/ and egypt-final/simple/.
Old values are taken from carveout_v1_5_results.json."""
import json
import os
import re
import shutil
import sys
import zipfile

import docx
import pypandoc
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_results_page_v0_7 as m  # noqa: E402
from make_results_page_v1_1 import ins_edit, visible  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FINAL = os.path.join(ROOT, "egypt", "final")
MD = os.path.join(FINAL, "md_sources")
ARCH = os.path.join(ROOT, "egypt", "archive")
EF = os.path.join(ROOT, "egypt-final")
B = ["1A", "2A", "2B", "3A", "3B", "3C"]
M_CBAM = {"1A": 100, "2A": 44, "2B": 44, "3A": 100, "3B": 100, "3C": 100}
arg = sys.argv[1] if len(sys.argv) > 1 else "carveout_v1_6_results.json"
raw = json.load(open(os.path.join(HERE, arg), encoding="utf8"))
R = raw["results"] if "results" in raw else raw
OLD = json.load(open(os.path.join(HERE, "carveout_v1_5_results.json"), encoding="utf8"))
for b in B:
    R[b].setdefault("O_final", OLD[b]["O_final"])
    R[b]["M"] = M_CBAM[b]
MINUS = "−"


def rnd(x, dp):
    q = 10 ** dp
    return (int(abs(x) * q + 0.5 + 1e-9) / q) * (1 if x >= 0 else -1)


def fmt(x, dp=1, plus=False, comma=False):
    v = rnd(x, dp)
    s = ("{:,.%df}" if comma else "{:.%df}") % dp
    s = s.format(abs(v))
    if v < 0:
        return MINUS + s
    return ("+" + s) if plus and v > 0 else s


def row_md(label, vals):
    return "| %s | %s |" % (label, " | ".join(vals))


# ---------------------------------------------------------------- markdown sources
def carve_md():
    s = open(os.path.join(ARCH, "EGYPT_CarveOut_Table2_v1.5.md"), encoding="utf8").read()
    s = s.replace("(final v1.5)", "(final v1.6)").replace("Methodology v1.5", "Methodology v1.6").replace(
        "CPAT_Industry_Kernel_Egypt_v1.5.xlsx", "CPAT_Industry_Kernel_Egypt_v1.6.xlsx")
    s = s.replace("CPAT_Industry_Kernel_Egypt_v1.3.xlsx", "CPAT_Industry_Kernel_Egypt_v1.6.xlsx")
    s = s.replace("**3B rebate (decision 2026-10-04).**", "**3B rebate.**")
    old = "The earlier prototype (kernel v0.16) held non-CBAM IPPU fixed, which is most of why its 1A cut was lower."
    assert old in s
    s = s.replace(old, "The kernel's own composition holds non-CBAM IPPU fixed, which is most of why its 1A cut is lower.")
    spec = {
        "| Coverage, % of GHG (J) |": [fmt(R[b]["J"], 0) for b in B],
        "| Revenue, $bn (P) |": [fmt(R[b]["P"], 1) for b in B],
        "| Emission cut, MtCO₂e (K) |": [fmt(R[b]["K"], 1) for b in B],
        "| Cut, % of GHG |": [fmt(R[b]["L"], 1) for b in B],
        "| CBAM intensity, % (N) |": [fmt(R[b]["N"], 1) for b in B],
        "| CBAM obligations per tonne exported, % (O) |": [fmt(R[b]["O_final"], 1) for b in B],
        "| CBAM block emissions, % (T) |": [fmt(R[b]["T"], 1) for b in B],
        "| Deaths avoided (Q) |": [fmt(R[b]["Q"], 0, comma=True) for b in B],
        "| Emission cut, Mt: **new** |": [fmt(R[b]["K"], 1) for b in B],
        "| Revenue, $bn: **new** |": [fmt(R[b]["P"], 1) for b in B],
        "| Deaths avoided: **new** |": [fmt(R[b]["Q"], 0, comma=True) for b in B],
        "| CBAM intensity, %: **new** |": [fmt(R[b]["N"], 1) for b in B],
        "| CBAM obligations, %: **new** |": [fmt(R[b]["O_final"], 1) for b in B],
        "| CPAT ΔGHG of the run |": [fmt(R[b]["dghg"], 1) for b in B],
        "| CPAT industry change, % (applied to block) |": [fmt(R[b]["r"], 1) for b in B],
        "| Block emissions, baseline (fuel + process) |": [fmt(R[b]["B"], 1) for b in B],
        "| less: CPAT's implied block change |": [fmt(-R[b]["cpat_blk"], 1) for b in B],
        "| memo: CPAT fuel-intensity response, % |": [fmt(R[b]["i_f"], 1) for b in B],
        "| plus: new block change |": [fmt(R[b]["dB"], 1) for b in B],
        "| plus: 3B rebate, non-block covered industry |": [fmt(R[b]["D_nb"], 1) for b in B],
        "| **K** |": [fmt(R[b]["K"], 1) for b in B],
    }
    out, seen = [], set()
    for line in s.split("\n"):
        hit = next((k for k in spec if line.startswith(k)), None)
        if hit:
            label = line.split("|")[1].strip()
            line = row_md(label, spec[hit])
            seen.add(hit)
        out.append(line)
    missing = set(spec) - seen
    assert not missing, missing
    s = "\n".join(out)
    a = "- **Growth.**"
    assert a in s
    s = s.replace(a, "- **Output response.** Output falls with the net carbon cost: Q = Q₀(1 + Δp)^ε, where Δp is the carbon cost as a share of the "
                       "product price. ε is by product: cement −0.10, steel and fertilisers −0.40, aluminium −0.50 (kernel `Manual inputs` "
                       "E66:E73; basis in `OutputElasticity_Note_v0.2`). At USD 20/t only cement matters: its carbon cost is 15% of its price, against "
                       "1–3% for the other goods.\n" + a, 1)
    open(os.path.join(MD, "EGYPT_CarveOut_Table2_v1.6.md"), "w", encoding="utf8").write(s)


CAVEAT_EDITS = [
    ("ad hoc rebuild `AdHocCalculations_Rebuild_v0.4.xlsx`", "ad hoc rebuild `AdHocCalculations_Rebuild_v0.5.xlsx`"),
    ("     - reductions of \u221225.1 / \u221219.6 / \u221230.6 Mt (rebuild) and \u221221.1 / \u221217.4 / \u221232.9 Mt (prototype);\n     - deaths avoided of 850 / 714 / 997.\n   - These replace the previous figures of \u221218.2 / \u221212.7 / \u221222.6 Mt, which were lower bounds.\n",
     "     - reductions of \u221223.4 / \u221212.3 / \u221229.0 Mt (rebuild) and \u221219.4 / \u221217.5 / \u221231.6 Mt (prototype);\n     - deaths avoided of 850 / 412 / 997 (rebuild).\n   - Without the scaling, as in the final Table 2, these scenarios are lower bounds.\n"),
    ("(USD 0.93bn), solved as a fixed point. The other industrial carbon revenue (USD 0.73bn) stays with the budget.",
     "(USD 0.97bn), solved as a fixed point. The other industrial carbon revenue (USD 0.71bn) stays with the budget."),
    ("the prototype's 3C reduction (\u221232.9 Mt) exceeds the rebuild's (\u221230.6 Mt).", "the prototype's 3C reduction (\u221231.6 Mt) exceeds the rebuild's (\u221229.0 Mt)."),
    ("(rebuild \u22122.2%)", "(rebuild \u22122.1%)"),
    ("The rebuild gives 8\u201329% smaller reductions for these scenarios and about USD 1bn more revenue.",
     "The rebuild gives about 29\u201330% smaller reductions for these scenarios and about USD 1bn more revenue."),
    ("(3A \u221225.1 vs \u221221.5 Mt)", "(3A \u221223.4 vs \u221221.5 Mt)"),
    ("`ResultsComparison_Table2_v0.4`", "`ResultsComparison_Table2_v0.5`"),
]


def caveats_md():
    s = open(os.path.join(ARCH, "EGYPT_FinalCaveats_v1.5.md"), encoding="utf8").read()
    s = s.replace("(final v1.5)", "(final v1.6)").replace("_v1.5", "_v1.6")
    a = "   - the output elasticity ε_Q (−0.5);"
    assert a in s
    s = s.replace(a, "   - the output elasticity ε_Q (cement −0.10, steel and fertilisers −0.40, aluminium −0.50: judgements from sourced components, "
                     "Low–Medium confidence; only cement matters, and with the old uniform −0.5 the 1A cut would be about 2.7 Mt larger);")
    a = "F3. **Output and process responses come from the kernel,**"
    assert a in s
    for old, new in CAVEAT_EDITS:
        assert old in s, old[:70]
        s = s.replace(old, new)
    open(os.path.join(MD, "EGYPT_FinalCaveats_v1.6.md"), "w", encoding="utf8").write(s)


def obligation_md():
    s = open(os.path.join(ARCH, "EGYPT_CBAM_ObligationNote_v1.5.md"), encoding="utf8").read()
    s = s.replace("(v1.5)", "(v1.6)").replace("v1.5.xlsx", "v1.6.xlsx")
    a = "| Updated (Table 2) | −5.4 | −2.6 | −2.7 | −5.4 | −5.4 | −20.7 |"
    assert a in s
    s = s.replace(a, row_md("Updated (Table 2)", [fmt(R[b]["O_final"], 1) for b in B]))
    open(os.path.join(MD, "EGYPT_CBAM_ObligationNote_v1.6.md"), "w", encoding="utf8").write(s)


def versionnotes_md():
    s = open(os.path.join(ARCH, "EGYPT_VersionNotes_v1.5.md"), encoding="utf8").read()
    s = s.replace("(final v1.5)", "(final v1.6)").replace("EGYPT_Methodology_v1.5", "EGYPT_Methodology_v1.6")
    new = ("## Final set v1.6 (2026-10-08)\n\n- **Product-specific output elasticities.** `Manual inputs` E66:E73 change from the uniform −0.5 placeholder to "
           "cement −0.10, steel −0.40, ammonia / urea / ammonium nitrate −0.40, aluminium −0.50 (`OutputElasticity_Note_v0.2`). Only cement matters "
           "(carbon cost 15%% of its price). 2030 emission cut (Mt), old to new: 1A %s to %s; 2A %s to %s; 2B %s to %s; 3A %s to %s; 3B unchanged %s; "
           "3C %s to %s. Deaths avoided, old to new: 1A %s to %s; 2A %s to %s; 2B %s to %s; 3A %s to %s; 3C %s to %s. Revenue changes by "
           "less than USD 0.1bn. Obligations (row O) are unchanged.\n- Rebuild v0.5 (per-product elasticities) and kernel v1.6 are the supporting models.\n\n"
           % (fmt(OLD["1A"]["K"]), fmt(R["1A"]["K"]), fmt(OLD["2A"]["K"]), fmt(R["2A"]["K"]), fmt(OLD["2B"]["K"]), fmt(R["2B"]["K"]),
              fmt(OLD["3A"]["K"]), fmt(R["3A"]["K"]), fmt(R["3B"]["K"]), fmt(OLD["3C"]["K"]), fmt(R["3C"]["K"]),
              fmt(OLD["1A"]["Q"], 0, comma=True), fmt(R["1A"]["Q"], 0, comma=True), fmt(OLD["2A"]["Q"], 0, comma=True),
              fmt(R["2A"]["Q"], 0, comma=True), fmt(OLD["2B"]["Q"], 0, comma=True), fmt(R["2B"]["Q"], 0, comma=True),
              fmt(OLD["3A"]["Q"], 0, comma=True), fmt(R["3A"]["Q"], 0, comma=True), fmt(OLD["3C"]["Q"], 0, comma=True),
              fmt(R["3C"]["Q"], 0, comma=True)))
    a = "## Final set v1.5 (2026-10-08)"
    assert a in s
    s = s.replace(a, new + a, 1)
    s = s.replace("| v1.5 | 3B rebate decision; sheet `Table2_Final` |",
                  "| v1.5 | 3B rebate decision; sheet `Table2_Final` |\n| v1.6 | Product-specific output elasticities (cement −0.10); fund fixed point and stored snapshots re-solved |")
    s = s.replace("## Earlier final sets\n\n| Set | Date | Change |\n|---|---|---|\n",
                  "## Earlier final sets\n\n| Set | Date | Change |\n|---|---|---|\n| v1.5 | 2026-10-08 | 3B rebate to all covered industry; one CBAM convention; single confirmation workbook |\n")
    s = s.replace("**Process semi-elasticities.**",
                  "**Output elasticity.** Before v1.6 the kernel used a uniform −0.5 placeholder for every product.\n\n**Process semi-elasticities.**")
    open(os.path.join(MD, "EGYPT_VersionNotes_v1.6.md"), "w", encoding="utf8").write(s)


def to_docx(md, out, ref):
    pypandoc.convert_file(os.path.join(MD, md), "docx", outputfile=os.path.join(FINAL, out),
                          extra_args=["--reference-doc=" + os.path.join(ARCH, ref)])


# ---------------------------------------------------------------- tracked results text (v1.5 -> v1.6)
def replace_all_ins(x, old, new, anchor="", minimum=1):
    n = 0
    while True:
        try:
            x2 = ins_edit(x, anchor, old, new)
        except AssertionError:
            break
        if x2 == x:
            break
        x = x2
        n += 1
        if n > 20:
            raise AssertionError(("runaway", old))
    assert n >= minimum, ("not found", old, anchor)
    return x


def tracked():
    src = os.path.join(ARCH, "EgyptResultsInitial_UpdatedResults_v1.5_tracked.docx")
    dst = os.path.join(FINAL, "EgyptResultsInitial_UpdatedResults_v1.6_tracked.docx")
    z = zipfile.ZipFile(src)
    x = z.read("word/document.xml").decode("utf8")
    f1 = lambda v: fmt(abs(v), 1)
    # 1. emission cuts (replace all: table cell "-37.4" and prose "37.4 MtCO2")
    for b in ("1A", "2A", "2B", "3A", "3C"):
        old, new = f1(OLD[b]["K"]), f1(R[b]["K"])
        if old != new:
            x = replace_all_ins(x, old, new)
    # 2. deaths (table and prose)
    for b in ("1A", "2A", "2B", "3A", "3C"):
        old, new = fmt(OLD[b]["Q"], 0, comma=True), fmt(R[b]["Q"], 0, comma=True)
        if old != new:
            x = replace_all_ins(x, old, new)
    # 3. CBAM intensity cells (document order; 3B unchanged)
    for b in ("1A", "2A", "2B", "3A", "3C"):
        old, new = fmt(OLD[b]["N"], 1).replace(MINUS, "-") + "%", fmt(R[b]["N"], 1).replace(MINUS, "-") + "%"
        if old != new:
            x = ins_edit(x, "", old, new)
    # 4. 3A revenue (table and prose)
    if fmt(OLD["3A"]["P"], 1) != fmt(R["3A"]["P"], 1):
        x = ins_edit(x, "Industry only", fmt(OLD["3A"]["P"], 1), fmt(R["3A"]["P"], 1))
        x = ins_edit(x, "(3A) raises considerably less, at USD", fmt(OLD["3A"]["P"], 1), fmt(R["3A"]["P"], 1))
    # 5. percentages of national CO2 (249 Mt)
    pc = lambda b: "%d" % rnd(100 * -R[b]["K"] / 249.0, 0)
    pco = lambda b: "%d" % rnd(100 * -OLD[b]["K"] / 249.0, 0)
    lo, hi = pc("3B"), pc("1A")
    x = ins_edit(x, "equal to about", "%s\u2013%s%%" % (pco("3B"), pco("1A")), "%s\u2013%s%%" % (lo, hi)) if (pco("3B"), pco("1A")) != (lo, hi) else x
    for b, anchor in (("1A", "(1A) achieves the largest reduction, at about %s MtCO\u2082 (about" % f1(R["1A"]["K"])),
                      ("3C", "(3C) cuts emissions by %s MtCO\u2082 (about" % f1(R["3C"]["K"])),
                      ("3A", "household-recycling scenario (3A) at %s MtCO\u2082 (about" % f1(R["3A"]["K"]))):
        if pc(b) != pco(b):
            x = ins_edit(x, anchor, pco(b), pc(b))
    v = visible(x)
    # sanity: no old figures remain
    for b in ("1A", "2A", "2B", "3A", "3C"):
        for tok in (f1(OLD[b]["K"]), fmt(OLD[b]["Q"], 0, comma=True)):
            if tok not in (f1(R[bb]["K"]) for bb in B) and tok not in [fmt(R[bb]["Q"], 0, comma=True) for bb in B]:
                assert tok not in v, ("old figure remains", tok)
    assert 'w:author="Copilot"' not in x
    tmp = dst + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in z.infolist():
            data = z.read(it.filename)
            if it.filename == "word/document.xml":
                data = x.encode("utf8")
            zo.writestr(it, data)
    z.close()
    shutil.move(tmp, dst)
    print("tracked text:", dst)


def main():
    m.DATE = "2026-10-08T18:00:00Z"
    m.nid[0] = 95000
    carve_md()
    caveats_md()
    obligation_md()
    versionnotes_md()
    to_docx("EGYPT_CarveOut_Table2_v1.6.md", "EGYPT_CarveOut_Table2_v1.6.docx", "EGYPT_CarveOut_Table2_v1.5.docx")
    to_docx("EGYPT_FinalCaveats_v1.6.md", "EGYPT_FinalCaveats_v1.6.docx", "EGYPT_FinalCaveats_v1.5.docx")
    to_docx("EGYPT_CBAM_ObligationNote_v1.6.md", "EGYPT_CBAM_ObligationNote_v1.6_NeedsCarolynConfirmation.docx",
            "EGYPT_CBAM_ObligationNote_v1.5_NeedsCarolynConfirmation.docx")
    to_docx("EGYPT_VersionNotes_v1.6.md", "EGYPT_VersionNotes_v1.6.docx", "EGYPT_VersionNotes_v1.5.docx")
    tracked()
    print("documents v1.6 written")


if __name__ == "__main__":
    main()
