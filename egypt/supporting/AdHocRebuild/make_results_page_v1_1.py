"""Tracked results page v1.1: v1.0 plus one scenario term ("scenario") throughout, tracked as Stephen Stretton."""
import os
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_results_page_v0_7 as m  # noqa: E402

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\egypt\final"
SRC = F + r"\EgyptResultsInitial_UpdatedResults_v1.0_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v1.1_tracked.docx"
m.DATE = "2026-10-05T12:00:00Z"
m.nid[0] = 70000

# (anchor, old, new): "bundle/option/family/design" used for a scenario -> "scenario".
# Recycling options/choices and "policy design" (not scenarios) are left unchanged.
EDITS = [
    ("Policy bundle", "Policy bundle", "Policy scenario"),
    ("The first scenario (1A)", "most comprehensive option", "most comprehensive scenario"),
    ("The second family", "The second family", "The second set of scenarios"),
    ("The third family", "The third family", "The third set of scenarios"),
    ("It represents the narrowest", "narrowest option", "narrowest scenario"),
    ("The two remaining downstream", "downstream designs", "downstream scenarios"),
    ("ductions range from 19.1", "across the bundles", "across the scenarios"),
    ("The downstream-only", "downstream-only options", "downstream-only scenarios"),
    ("followed by the household-recycling design (3A) at", "household-recycling design", "household-recycling scenario"),
    ("The free-allocation design (3B) delivers", "free-allocation design", "free-allocation scenario"),
    ("The bundles differ", "The bundles differ", "The scenarios differ"),
    ("The downstream heavy-industry options", "heavy-industry options", "heavy-industry scenarios"),
    ("Among these options", "Among these options", "Among these scenarios"),
    ("followed by the household-recycling design (3A) with", "household-recycling design", "household-recycling scenario"),
    ("the free-allocation design (3B) with", "free-allocation design", "free-allocation scenario"),
    ("The six bundles", "The six bundles", "The six scenarios"),
    ("central trade-off: the options", "the options that", "the scenarios that"),
    ("no single option performs", "single option", "single scenario"),
    ("the most balanced option", "balanced option", "balanced scenario"),
    ("the \"best\" bundle", "\"best\" bundle", "\"best\" scenario"),
    ("the rebate-based industrial design", "industrial design", "industrial scenario"),
    ("Pairing any of these options", "these options", "these scenarios"),
]


def visible(x):
    rs = m.runs_from(x, 0, len(x))
    return "".join(r["text"] for r in rs if r["st"] != "w:del")


def ins_edit(x, anchor, old, new):
    """Edit inside an existing Stephen Stretton insertion, only the occurrence after `anchor`."""
    rs = m.runs_from(x, 0, len(x))
    full = "".join(r["text"] for r in rs)
    a = full.find(anchor)
    assert a >= 0, anchor
    i = full.find(old, a)
    pos = 0
    for r in rs:
        if pos <= i and i + len(old) <= pos + len(r["text"]) and r["st"] == "w:ins":
            seg = x[r["s"]:r["e"]]
            k = seg.find(old)
            assert k >= 0, (anchor, old)
            return x[:r["s"]] + seg[:k] + new + seg[k + len(old):] + x[r["e"]:]
        pos += len(r["text"])
    raise AssertionError(("not in a single inserted run", anchor, old))


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
    for t in ("bundle", " family", "Policy bundle"):
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


if __name__ == "__main__":
    main()
