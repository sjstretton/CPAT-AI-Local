"""Tracked results page v1.0 (final): v0.7 plus proofreading fixes, all tracked as Stephen Stretton."""
import os
import re
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_results_page_v0_7 as m  # noqa: E402

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\egypt\final"
SRC = F + r"\Old\Superseded\EgyptResultsInitial_UpdatedResults_v0.7_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v1.0_tracked.docx"
m.DATE = "2026-10-04T12:00:00Z"
m.nid[0] = 60000


def main():
    z = zipfile.ZipFile(SRC)
    x = z.read("word/document.xml").decode("utf8")

    x = m.tr(x, "upstream carbon price on all", "all  fossil", "all fossil")
    x = m.tr(x, "It can also improve employment", "outcomes  by", "outcomes by")
    x = m.tr(x, "is the most balanced option", "It  combines", "It combines")
    x = m.tr(x, "By convention, revenues", "macroeconomically \u2014for", "macroeconomically\u2014for")
    x = m.tr(x, "By contrast, free allocation", "(3B), protects", "(3B) protects")
    x = m.tr(x, "The second family", "model upstream", "models upstream")
    x = m.tr(x, "3C offers an", "rebate, to support", "rebate to support")
    x = m.tr(x, "low-income households or", "or to public services", "or to fund public services")
    x = m.tr(x, "independent from its contribution", "reduced CBAM liabilities", "reduced CBAM obligations")
    x = m.tr(x, "Summary of tradeoffs", "tradeoffs", "trade-offs")
    x = m.tr(x, "would help assess the", "tradeoffs", "trade-offs")
    x = m.tr(x, "The industrial carbon price", "industrial carbon price", "downstream price")
    x = m.tins(x, "CBAM obligations reduced", "CBAM obligations reduced", " (% of baseline, 2030 CBAM phase-in)")

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


if __name__ == "__main__":
    main()
