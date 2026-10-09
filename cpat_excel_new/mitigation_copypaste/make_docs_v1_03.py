"""Word documentation of CPAT-AI-Mitigation-MVP v1.03, assembled from the Markdown notes (pandoc).

    python make_docs_v1_03.py  ->  CPAT-AI-Mitigation-MVP_Documentation_v1.03.docx
"""
import os
import re
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'CPAT-AI-Mitigation-MVP_Documentation_v1.03.docx')
PARTS = [('Model overview, layout and files', 'README.md'),
         ('Domestic energy prices', 'PriceProjection_Method_v0.4.md'),
         ('New ETS', 'ETS_Method_v0_1.md'),
         ('Multiple scenarios and stored results', 'Scenarios_Method_v0_1.md')]


def part(title, name):
    text = open(os.path.join(HERE, name), encoding='utf-8').read()
    text = re.sub(r'\A# .*\n', '', text)                      # drop the note's own title
    text = re.sub(r'^(#+) ', lambda m: '#' + m.group(1) + ' ', text, flags=re.M)   # demote one level
    return f'# {title}\n\n*Source: `{name}`.*\n\n{text}\n'


def main():
    head = ('---\ntitle: "CPAT-AI-Mitigation-MVP v1.03: documentation"\n'
            'subtitle: "AI-generated, copy-pasteable replacement of the CPAT mitigation module (Egypt data)"\n'
            'date: "2026-10-09"\n---\n\n'
            '# About this document\n\nWorkbook: `CPAT-AI-Mitigation-MVP-v1.03.xlsm` (macro-enabled) (built by `build_v1_03.py`, '
            'checked by `check_v1_03.py`, report `check_report_v1.03.md`: PASS). This document collects the '
            'model overview and the method notes. Differences with legacy CPAT are listed in the workbook sheet '
            '`LegacyDiff`; the version log is on the `Settings` sheet; caveats per task are in `CAVEATS.md`.\n\n')
    md = head + '\n'.join(part(t, n) for t, n in PARTS)
    src = os.path.join(tempfile.mkdtemp(), 'doc.md')
    open(src, 'w', encoding='utf-8').write(md)
    subprocess.run(['pandoc', src, '-o', OUT, '--toc', '--toc-depth=2', '-f', 'markdown-yaml_metadata_block+yaml_metadata_block'],
                   check=True)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
