from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
import json
import hashlib

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'output/Kiodai_Daryn_2026_defense.pptx'
DEST = ROOT / '.build/three-edits-candidate.pptx'
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

def shape_with(root, needle):
    matches = [s for s in root.findall('.//p:sp', NS)
               if needle in '\n'.join(s.xpath('.//a:t/text()', namespaces=NS))]
    assert len(matches) == 1, (needle, len(matches))
    return matches[0]

def set_lines(shape, lines):
    body = shape.find('p:txBody', NS)
    paragraphs = body.findall('a:p', NS)
    template = deepcopy(paragraphs[0])
    for p in paragraphs:
        body.remove(p)
    for line in lines:
        p = deepcopy(template)
        texts = p.findall('.//a:t', NS)
        assert len(texts) == 1
        texts[0].text = line
        body.append(p)

old3 = 'Различается управление запросами: у B_ledger решение принимает модель, у A2 — ограниченный программный контроллер.'
new3 = 'У B_ledger запросы выбирает модель. Контроллер A2 проверяет до одного канала ожидающих задач за шаг, начиная с давно не проверявшегося.'
old9 = 'В рукописи мой вклад обозначен как постановка вопроса и разработка методики сравнения. Код и текст готовились с ИИ-помощью. Самостоятельность нужно подтверждать историей работы и защитой.'
new9 = 'Мой вклад — постановка эксперимента и организация разработки системы, запуска сравнения и анализа результатов с ИИ-помощью. ИИ также помогал готовить код и текст.'
old_qualification = 'Не утверждать, что весь код написан самостоятельно или что семантический анализ независимо подтверждён. Авторский вклад сформулирован не шире найденной рукописи.'
new_qualification = 'Личный вклад описан как постановка эксперимента и организация работы с ИИ-помощью. Независимая человеческая разметка не заявляется.'
extra_source = ' artifacts/verification/v21-comparison-live-20260911/authorization.txt: автор задаёт условия, санкционирует запуск и поручает анализ; автоматизированное исполнение и ИИ-помощь раскрыты.'

with ZipFile(SOURCE) as zin:
    updates = {}
    for n in (3, 9, 14):
        part = f'ppt/slides/slide{n}.xml'
        root = E.fromstring(zin.read(part))
        if n == 3:
            shape = shape_with(root, 'ограниченный контроллер')
            set_lines(shape, ['Контроллер проверяет до одного',
                              'канала за шаг, начиная с давно',
                              'не проверявшегося.'])
            shape.find('p:spPr/a:xfrm/a:ext', NS).set('cy', str(100 * 9525))
        elif n == 9:
            shape = shape_with(root, 'Вклад автора: вопрос и методика сравнения.')
            set_lines(shape, ['Вклад автора: постановка эксперимента, организация разработки,',
                              'запуска сравнения и анализа результатов с ИИ-помощью.'])
        else:
            shape = shape_with(root, 'Код сам по себе не доказывает')
            shape.getparent().remove(shape)
        updates[part] = E.tostring(root, encoding='utf-8', xml_declaration=True, standalone=True)
    for n, old, new in ((3, old3, new3), (9, old9, new9)):
        part = f'ppt/notesSlides/notesSlide{n}.xml'
        raw = zin.read(part).decode('utf-8')
        assert raw.count(old) == 1
        raw = raw.replace(old, new)
        if n == 9:
            assert raw.count(old_qualification) == 1
            raw = raw.replace(old_qualification, new_qualification)
            root = E.fromstring(raw.encode('utf-8'))
            sources = [t for t in root.findall('.//a:t', NS) if (t.text or '').startswith('Источник:')]
            assert len(sources) == 1
            sources[0].text += extra_source
            raw = E.tostring(root, encoding='unicode')
        updates[part] = raw.encode('utf-8')
    with ZipFile(DEST, 'w') as zout:
        for entry in zin.infolist():
            zout.writestr(entry, updates.get(entry.filename, zin.read(entry.filename)))

with ZipFile(SOURCE) as a, ZipFile(DEST) as b:
    assert a.namelist() == b.namelist()
    changed = [n for n in a.namelist() if a.read(n) != b.read(n)]
    assert sorted(changed) == sorted(updates)

content = json.loads((ROOT / '.build/content.json').read_text())
for index, old, new in ((2, old3, new3), (8, old9, new9)):
    assert old in content['notes'][index]['speech']
    content['notes'][index]['speech'] = content['notes'][index]['speech'].replace(old, new)
content['notes'][8]['qualification'] = new_qualification
content['notes'][8]['source'] += extra_source
(ROOT / '.build/content-three-edits.json').write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n')
script = (ROOT / 'output/Сценарий_защиты.md').read_text()
for old, new in ((old3, new3), (old9, new9), (old_qualification, new_qualification)):
    assert script.count(old) == 1
    script = script.replace(old, new)
(ROOT / 'output/Сценарий_защиты_обновлённый.md').write_text(script)
(ROOT / '.build/three-edits-diff.json').write_text(json.dumps({
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'changed_package_parts': changed,
    'all_other_parts_byte_identical': True,
    'contribution_basis': 'Research question and design in manuscript section 7; user direction and authorization of execution and analysis in authorization.txt. No claim of unaided coding or independent annotation.'
}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'candidate': str(DEST), 'changed_parts': changed}, ensure_ascii=False))
