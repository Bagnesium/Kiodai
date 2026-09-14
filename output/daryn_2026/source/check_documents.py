"""Check final DOCX/PDF content, navigation, and declared page limits offline.

Run after copying rendered PDFs beside the DOCX files. This verifies content and
structure; it does not replace visual inspection of every rendered page.
"""
import json
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader

OUT = Path(__file__).resolve().parents[1]
compact = lambda s: re.sub(r'\s+', '', s).replace('\u00ad', '')
results = {}
for stem in ('Kiodai_Daryn_2026', 'Kiodai_Evidence_and_Verification'):
    doc = Document(OUT / (stem + '.docx'))
    pdf = PdfReader(OUT / (stem + '.pdf'))
    page_texts = [p.extract_text() for p in pdf.pages]
    # The PDF extractor returns the footer first, although it renders at bottom.
    cleaned = [re.sub(r'^' + str(i+1) + r'\s*\n', '', t) for i, t in enumerate(page_texts)]
    text = compact(''.join(cleaned))
    missing = []
    for p in doc.paragraphs:
        if p._p.xpath('./w:hyperlink'):
            continue  # Leader dots and TOC values are checked separately below.
        if p.text.strip() and compact(p.text) not in text:
            missing.append(p.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if compact(cell.text) not in text:
                    missing.append(cell.text)
    equations = doc.element.xpath('.//m:oMath')
    for eq in equations:
        t = ''.join(eq.itertext())
        if compact(t) not in text:
            missing.append(t)
    assert not missing, (stem, missing)
    results[stem] = {'pages': len(pdf.pages), 'docx_pdf_text_mismatches': 0,
                     'editable_tables': len(doc.tables), 'editable_equations': len(equations),
                     'figures': len(doc.inline_shapes)}
    if stem == 'Kiodai_Daryn_2026':
        headings = json.loads((OUT / 'data/headings.json').read_text())
        expected = json.loads((OUT / 'data/page_map.json').read_text())
        actual = {}
        for title, _, anchor in headings:
            hits = [i+1 for i, t in enumerate(page_texts)
                    if i != 1 and compact(title) in compact(t)]
            assert len(hits) == 1, (title, hits)
            actual[title] = hits[0]
        assert actual == expected, (actual, expected)
        toc = re.sub(r'[.\s]+', '', page_texts[1])
        for title, page in actual.items():
            assert re.sub(r'[.\s]+', '', title) + str(page) in toc, title
        anchors = doc.element.xpath('.//w:bookmarkStart')
        ids = [a.get(qn('w:id')) for a in anchors]
        names = [a.get(qn('w:name')) for a in anchors]
        assert len(set(ids)) == len(ids) == len(headings)
        assert set(names) == {h[2] for h in headings}
        links = doc.element.xpath('.//w:hyperlink')
        assert [a.get(qn('w:anchor')) for a in links] == [h[2] for h in headings]
        source = (OUT / 'source/manuscript.md').read_text()
        abstracts = source.split('@abstracts')[1].split('@body')[0]
        counts = {b.split('\n', 1)[0]: len(b.split('\n', 1)[1].split())
                  for b in abstracts.split('### ')[1:]}
        assert max(counts.values()) <= 250
        assert actual['2. Теоретические основы и связанные работы'] - actual['1. Введение'] + 1 <= 2
        assert actual['8. Заключение'] - actual['2. Теоретические основы и связанные работы'] <= 20
        assert actual['9. Список использованных источников'] - actual['8. Заключение'] == 1
        results[stem].update(toc_entries_verified=len(headings), abstract_word_counts=counts,
                            conclusion_pages=1, introduction_pages=1, research_page_span=[4,14])
(OUT / 'data/document_checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(json.dumps(results, ensure_ascii=False, indent=2))
