"""Tracked results page v1.2: v1.1 with CBAM obligations (row O) restated as the change in embedded emissions of CBAM
products per tonne exported to the EU (no domestic-price deduction; EU price and phase-in cancel). Stephen Stretton."""
import os
import re
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_results_page_v0_7 as m  # noqa: E402
from make_results_page_v1_1 import ins_edit, visible  # noqa: E402

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\Egypt Final results"
SRC = F + r"\EgyptResultsInitial_UpdatedResults_v1.1_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v1.2_tracked.docx"
m.DATE = "2026-10-06T12:00:00Z"
m.nid[0] = 80000

# Table cells (inside our insertions): old FULL values -> intensity-only values (EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx)
CELLS = {"-44.2%": "-5.4%", "-22.9%": "-2.6%", "-23.0%": "-2.7%", "-5.0%": "-5.4%", "-53.1%": "-20.7%"}

# (anchor, old, new) edits inside existing insertions
INS = [
    ("CBAM obligations reduced", " (% of baseline, 2030 CBAM phase-in)",
     " (% of baseline: embedded emissions per tonne exported)"),
    ("Reductions in CBAM obligations range from about", "5", "3"),
    ("Reductions in CBAM obligations range from about 3 to ", "53", "21"),
    ("Reductions in CBAM obligations range from", " under the 2030 CBAM phase-in, depending on sector", " depending on sector"),
    ("and each cut CBAM obligations by", "44%", "5%"),
    ("they result in a", "23%", "3%"),
    ("it reduces intensity by", " 53", " 21"),
    ("while reducing CBAM obligations by", "44%", "5%"),
    ("reduces the CBAM obligations the most", "by 53%", "by 21%"),
    ("protects competitiveness but", "delivers the smallest CBAM relief", "delivers no additional CBAM relief"),
]
# tracked replacements of original (plain) text
TR = [
    ("achieves the same intensity reduction", ", and that is the only factor driving the", " and the same"),
    ("reduction in CBAM obligations, since free allocation",
     ", since free allocation on an output-based intensity benchmark fully offsets the carbon price effectively paid on "
     "embodied emissions", ", as the obligation depends only on the emissions embedded in exports"),
]


def main():
    z = zipfile.ZipFile(SRC)
    x = z.read("word/document.xml").decode("utf8")
    for old, new in CELLS.items():
        n = 0
        for mm in list(re.finditer(r'(<w:t(?: [^>]*)?>)%s(</w:t>)' % re.escape(old), x))[::-1]:
            if m.state(x, mm.start()) == "w:ins":
                x = x[:mm.start()] + mm.group(1) + new + mm.group(2) + x[mm.end():]
                n += 1
        print("cell", old, "->", new, n)
        assert n == (2 if old == "-44.2%" else 1), old
    for a, o, n in INS:
        x = ins_edit(x, a, o, n)
        print("ins |", o, "->", n)
    for a, o, n in TR:
        try:
            x = m.tr(x, a, o, n)
            print("tracked |", o[:40], "->", n)
        except AssertionError as e:
            print("FAILED tr", e)
            raise
    v = visible(x)
    for t in ("phase-in", "53%", "44%"):
        print("remaining", repr(t), v.count(t))
    assert 'w:author="Copilot"' not in x
    tmp = DST + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in z.infolist():
            data = z.read(it.filename)
            if it.filename == "word/document.xml":
                data = x.encode("utf8")
            zo.writestr(it, data)
    z.close()
    shutil.move(tmp, DST)
    print("saved", DST)
    return v


if __name__ == "__main__":
    v = main()
    i = v.find("The scenarios differ considerably")
    print(v[i:i + 1700])
