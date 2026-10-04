"""Tracked results page v1.5: v1.3 with the 3B rebate decision (2026-10-04) applied: free allocation covers all covered
industry, so 3B revenue 0.3 $bn, emission cut 12.0 Mt, deaths avoided 330. Tracked as Stephen Stretton."""
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_results_page_v0_7 as m  # noqa: E402
from make_results_page_v1_1 import ins_edit, visible  # noqa: E402

F = os.path.abspath(os.path.join(HERE, "..", "..", "final"))
SRC = os.path.join(F, "..", "archive", "EgyptResultsInitial_UpdatedResults_v1.3_tracked.docx")
DST = os.path.join(F, "EgyptResultsInitial_UpdatedResults_v1.5_tracked.docx")
m.DATE = "2026-10-08T12:00:00Z"
m.nid[0] = 90000

# (anchor, old, new): tracked replacement of original text, or an edit inside an existing insertion
EDITS = [
    # scenario description (table row label and text)
    ("Downstream carbon price on heavy industry + free allocation for", "CBAM producers", "all covered industry"),
    ("3B provides free allocation for", "CBAM producers", "all covered industry"),
    ("The two remaining downstream scenarios raise much less carbon revenue: free allocation for", "CBAM producers",
     "all covered industry"),
    ("The downstream price paired with free allocation for", "CBAM producers", "all covered industry"),
    # Table 2, row 3B
    ("Firms (output)", "0.6", "0.3"),
    ("Firms (output)", "-19.1", "-12.0"),
    ("Firms (output)", "491", "330"),
    # narrative
    ("(3B) raises USD", "0.6", "0.3"),
    ("Estimated emission reductions range from", "19.1", "12.0"),
    ("Estimated emission reductions range from 12.0 to 37.4 MtCO₂ across the scenarios, equal to about", "8–15%", "5–15%"),
    ("The free-allocation scenario (3B) delivers the smallest reduction at", "19.1", "12.0"),
    ("The free-allocation scenario (3B) delivers the smallest reduction at 12.0 MtCO₂ (about", "8", "5"),
    ("avoided premature deaths range from", "491", "330"),
    ("the free-allocation scenario (3B) with", "491", "330"),
]


def main():
    z = zipfile.ZipFile(SRC)
    x = z.read("word/document.xml").decode("utf8")
    for anchor, old, new in EDITS:
        try:
            x = m.tr(x, anchor, old, new)
            how = "tracked"
        except AssertionError:
            x = ins_edit(x, anchor, old, new)
            how = "in-insertion"
        print(how, "|", old, "->", new)
    v = visible(x)
    for t in ("19.1", "491", "CBAM producers", "USD0.6"):
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
    main()
