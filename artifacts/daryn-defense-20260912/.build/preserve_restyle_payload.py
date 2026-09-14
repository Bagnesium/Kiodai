from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
import json

R = Path(__file__).resolve().parent.parent
SOURCE = R / 'output/Kiodai_Daryn_2026_defense_revised.pptx'
DRAFT = R / '.build/restyled-draft.pptx'
DEST = R / '.build/restyled-candidate.pptx'
N = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
     'c':'http://schemas.openxmlformats.org/drawingml/2006/chart',
     'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
     'ct':'http://schemas.openxmlformats.org/package/2006/content-types'}
def xml(b): return E.fromstring(b)
def data(r): return E.tostring(r,encoding='utf-8',xml_declaration=True,standalone=True)
with ZipFile(SOURCE) as old, ZipFile(DRAFT) as new:
    parts={n:new.read(n) for n in new.namelist()}
    # Preserve original notes and authorship metadata without any rewriting.
    for n in old.namelist():
        if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml'):
            parts[n]=old.read(n)
        if 'embeddings/' in n or 'charts/_rels/' in n or n=='docProps/core.xml':
            parts[n]=old.read(n)
    # Preserve original chart formulas, cached values and the same original workbooks.
    for number in (1,2):
        name=f'ppt/slides/charts/chart{number}.xml'
        orig=xml(old.read(name)); out=xml(parts[name])
        for a,b in zip(orig.findall('.//c:ser',N),out.findall('.//c:ser',N)):
            for tag in ('tx','cat','val'):
                original=a.find(f'c:{tag}',N); current=b.find(f'c:{tag}',N)
                assert original is not None and current is not None
                index=list(b).index(current); b.remove(current); b.insert(index,deepcopy(original))
        external=orig.find('c:externalData',N)
        assert external is not None
        out.append(deepcopy(external))
        # Preserve the original label formatting, including no currency wrap.
        for fmt in out.findall('.//c:dLbls/c:numFmt',N):
            fmt.set('formatCode','0.0000' if number==1 else '0.00000')
        for body in out.findall('.//c:dLbls//a:bodyPr',N): body.set('wrap','none')
        assert orig.xpath('.//c:v/text()',namespaces=N)==out.xpath('.//c:v/text()',namespaces=N)
        assert orig.xpath('.//c:f/text()',namespaces=N)==out.xpath('.//c:f/text()',namespaces=N)
        parts[name]=data(out)
    # Use thin horizontal rules only for native tables.
    for number in (11,13):
        name=f'ppt/slides/slide{number}.xml'; root=xml(parts[name])
        for cell in root.findall('.//a:tcPr',N):
            for node in list(cell):
                if E.QName(node).localname.startswith('ln'): cell.remove(node)
            for side in ('L','R','T','B','TlToBr','BlToTr'):
                line=E.Element(f'{{{N["a"]}}}ln{side}',w='6350')
                if side=='B':
                    fill=E.SubElement(line,f'{{{N["a"]}}}solidFill')
                    E.SubElement(fill,f'{{{N["a"]}}}srgbClr',val='DCE0E7')
                    E.SubElement(line,f'{{{N["a"]}}}prstDash',val='solid')
                else:E.SubElement(line,f'{{{N["a"]}}}noFill')
                cell.insert(0,line)
        parts[name]=data(root)
    # Register the preserved embedded workbooks in the new package.
    ct=xml(parts['[Content_Types].xml']); original_ct=xml(old.read('[Content_Types].xml'))
    identities={(E.QName(e).localname,e.get('PartName'),e.get('Extension')) for e in ct}
    for e in original_ct:
        if e.get('Extension')=='xlsx' or '/embeddings/' in e.get('PartName',''):
            key=(E.QName(e).localname,e.get('PartName'),e.get('Extension'))
            if key not in identities:ct.append(deepcopy(e))
    parts['[Content_Types].xml']=data(ct)
    with ZipFile(DEST,'w') as z:
        for name,body in parts.items():z.writestr(name,body,compress_type=8)
print('Preserved all original notes, chart values, formulas and embedded workbook bytes.')
