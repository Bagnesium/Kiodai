from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from collections import Counter
import re,json,hashlib

R=Path(__file__).resolve().parent.parent
OLD=R/'output/Kiodai_Daryn_2026_defense_revised.pptx'
NEW=R/'output/Kiodai_Daryn_2026_redesigned.pptx'
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
def xml(z,n):return E.fromstring(z.read(n))
def normalize(t):return re.sub(r'\s+',' ',t).strip()
def paragraph_text(root):return '\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=N)) for p in root.findall('.//a:p',N))
def tokens(t):return Counter(normalize(t).split(' '))
def table_values(root):return [[['\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=N)) for p in c.findall('a:txBody/a:p',N)) for c in row.findall('a:tc',N)] for row in tb.findall('a:tr',N)] for tb in root.findall('.//a:tbl',N)]
checks=[]
with ZipFile(OLD) as a,ZipFile(NEW) as b:
 for i in range(1,15):
  part=f'ppt/slides/slide{i}.xml';x=xml(a,part);y=xml(b,part)
  tx=tokens(paragraph_text(x));ty=tokens(paragraph_text(y))
  assert tx==ty,(i,tx-ty,ty-tx)
  assert table_values(x)==table_values(y),i
  assert len(x.findall('.//p:cxnSp',N))==len(y.findall('.//p:cxnSp',N)),i
  note=f'ppt/notesSlides/notesSlide{i}.xml'
  assert a.read(note)==b.read(note),i
  checks.append({'slide':i,'text_tokens_preserved':True,'table_cells_preserved':True,'connector_count_preserved':True,'notes_byte_identical':True})
 for i in (1,2):
  part=f'ppt/slides/charts/chart{i}.xml';x=xml(a,part);y=xml(b,part)
  for tag in ('tx','cat','val'):
   xx=x.findall(f'.//c:ser/c:{tag}',N);yy=y.findall(f'.//c:ser/c:{tag}',N)
   assert len(xx)==len(yy)
   for k,j in zip(xx,yy):assert E.tostring(k,method='c14n',exclusive=True)==E.tostring(j,method='c14n',exclusive=True),(i,tag)
  part=f'ppt/embeddings/chart-data-snapshot-{i:03}.xlsx'
  assert a.read(part)==b.read(part)
 count=len([n for n in b.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)])
 assert count==14
report={'source':str(OLD),'output':str(NEW),'sha256':hashlib.sha256(NEW.read_bytes()).hexdigest(),'slides':checks,'slide_count':14,'original_chart_data_formulas_and_workbooks_preserved':True,'all_speaker_notes_byte_identical':True,'all_native_table_cells_exactly_equal':True}
(R/'.build/restyle-final-content-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: 14 slides; all text tokens, tables, chart data/formulas/workbooks, notes and diagram connector counts preserved.')
