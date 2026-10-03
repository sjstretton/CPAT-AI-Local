"""Build EgyptResultsInitial_UpdatedResults_v0.5_tracked.docx from v0.3: CBAM carve-out v0.2 values, 2030
(original CPAT runs; CBAM block from kernel output/process response plus CPAT fuel-intensity response).

Tracked changes stay relative to the original EgyptResultsInitial text. O uses the NOPHASE convention (as Table 2).
"""
import re
import shutil
import zipfile

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\Egypt Final results"
SRC = F + r"\Old\EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v0.5_tracked.docx"
DATE = "2026-10-03T16:00:00Z"
CO2 = "MtCO\u2082"

# index of existing w:ins (in v0.3) -> new text
INS = {
    # Table 2: 1A, 2A, 2B, 3A, 3B, 3C
    0: "63%", 1: "6.9", 2: "-37.4", 3: "-5.8%", 4: "-24.0%", 5: "1,501",
    6: "57%", 7: "6.3", 8: "-33.1", 9: "-2.1%", 10: "-12.2%",
    11: "6.2", 12: "-34.8", 13: "-2.3%", 14: "-12.3%",
    15: "14%", 16: "1.5", 17: "-22.8", 18: "-5.8%", 19: "-24.0%", 20: "552",
    21: "0.6", 22: "-19.1", 23: "-5.8%", 24: "-5.1%", 25: "491",
    26: "-33.0", 27: "-23.1%", 28: "-36.2%", 29: "646",
    # narrative
    30: "63%", 31: "57%", 32: "14%",
    33: "USD6.9 billion\u2014roughly 12%", 34: "USD6.2-6.3", 35: "USD1.5", 36: "much less",
    37: "raises USD0.6 billion and", 38: "USD0.4 billion, as both",
    39: "19.1 to 37.4", 40: "8-15%", 41: "37.4 " + CO2 + " (about 15%", 42: "13-14%",
    43: "34.8", 44: "33.1", 45: " generally reduce",
    46: " a narrower industrial base; the exception is the abatement rebate (3C), whose rebate-funded "
        "process abatement brings it close to the economy-wide levies",
    47: "33.0 " + CO2 + " (about 13%", 48: "22.8 " + CO2 + " (about 9%", 49: "19.1", 50: "8",
    51: "5", 52: "36", 53: "about ", 54: "6%", 55: "24%", 56: "5%",
    57: "about 2%", 58: "12%", 59: " 23", 60: " 36",
    61: "491 to 1,517", 62: "a health gain of 1,501", 63: "yield similar gains:", 64: "deaths, the largest,",
    65: "646", 66: "552", 67: "491",
    68: "37.4", 69: "USD6.9", 70: "large air pollution co-benefits (1,501", 71: "24%",
}

nid = [40000]


def ins_run(rpr, text):
    nid[0] += 1
    return ('<w:ins w:id="%d" w:author="Copilot" w:date="%s"><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:ins>'
            % (nid[0], DATE, rpr, text))


def del_run(rpr, text):
    nid[0] += 1
    return ('<w:del w:id="%d" w:author="Copilot" w:date="%s"><w:r>%s<w:delText xml:space="preserve">%s</w:delText></w:r></w:del>'
            % (nid[0], DATE, rpr, text))


def plain_run(rpr, text):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, text) if text else ""


def in_tracked(x, pos):
    for tag in ("w:ins", "w:del"):
        o, c = x.rfind("<%s " % tag, 0, pos), x.rfind("</%s>" % tag, 0, pos)
        if o > c:
            return True
    return False


def tracked(x, old, new, after=0, exact=False):
    """Tracked replace of `old` in the first plain (untracked) run containing it, searching from `after`."""
    pat = re.compile(r'<w:t(?: [^>]*)?>(%s)</w:t>' % (re.escape(old) if exact else r'[^<]*' + re.escape(old) + r'[^<]*'))
    for m in pat.finditer(x, after):
        if not in_tracked(x, m.start()):
            break
    else:
        raise AssertionError(old)
    wt = m.group(1)
    rs = max(x.rfind("<w:r>", 0, m.start()), x.rfind("<w:r ", 0, m.start()))
    re_ = x.find("</w:r>", m.end()) + len("</w:r>")
    run = x[rs:re_]
    assert run.count("<w:t") == 1, run
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', run, re.S)
    rpr = rpr.group(0) if rpr else ""
    i = wt.index(old)
    out = plain_run(rpr, wt[:i]) + del_run(rpr, old) + (ins_run(rpr, new) if new else "") + plain_run(rpr, wt[i + len(old):])
    return x[:rs] + out + x[re_:], rs + len(out)


def main():
    x = zipfile.ZipFile(SRC).read("word/document.xml").decode("utf8")
    spans = [m.span(1) for m in re.finditer(r'<w:ins [^>]*>(.*?)</w:ins>', x, re.S)]
    assert len(spans) == 72, len(spans)
    for k in sorted(INS, reverse=True):
        a, b = spans[k]
        seg = x[a:b]
        ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', seg))
        new = seg[:ts[0].start()] + '<w:t xml:space="preserve">' + INS[k] + "</w:t>"
        last = ts[0].end()
        for t in ts[1:]:
            new += seg[last:t.start()] + t.group(1) + t.group(3)
            last = t.end()
        new += seg[last:]
        x = x[:a] + new + x[b:]

    # Table 2 cells unchanged in v0.3 (2A/2B deaths, 3C revenue)
    p = x.find("Table 2. Simulated outcomes")
    x, _ = tracked(x, "1,564", "1,456", p, exact=True)
    x, _ = tracked(x, "1,631", "1,517", p, exact=True)
    x, _ = tracked(x, "0.0", "0.4", p, exact=True)
    x, _ = tracked(x, "nearly ", "", x.find("household-recycling variant (2B) and"), exact=True)
    p = x.find("yield similar gains:")
    x, p = tracked(x, "1,631", "1,517", p)
    x, p = tracked(x, "1,564", "1,456", p, exact=True)

    zin = zipfile.ZipFile(SRC)
    tmp = DST + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                data = x.encode("utf8")
            zo.writestr(it, data)
    zin.close()
    shutil.move(tmp, DST)
    print("saved", DST)


if __name__ == "__main__":
    main()
