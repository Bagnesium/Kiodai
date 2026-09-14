from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
B=Path(__file__).parent
ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','dc':'http://purl.org/dc/elements/1.1/','cp':'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
with ZipFile(B/'candidate.pptx') as src, ZipFile(B/'candidate-v2.pptx','w',ZIP_DEFLATED) as dst:
    for info in src.infolist():
        data=src.read(info.filename)
        if info.filename=='ppt/slides/charts/chart2.xml':
            r=E.fromstring(data)
            for n in r.findall('.//c:formatCode',ns):
                if n.text=='$0.00000': n.text='0.00000'
            for labels in r.findall('.//c:dLbls',ns):
                body=labels.find('c:txPr/a:bodyPr',ns)
                if body is not None:body.set('wrap','none')
                fmt=E.Element('{'+ns['c']+'}numFmt',formatCode='0.00000',sourceLinked='0')
                labels.insert(0,fmt)
            data=E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
        elif info.filename=='docProps/core.xml':
            r=E.fromstring(data)
            r.find('dc:creator',ns).text='Беймжан Багдат'
            r.find('cp:lastModifiedBy',ns).text='Codex — подготовка презентации с ИИ-помощью'
            r.find('dc:title',ns).text='Kiodai: структурированная перспективная память языковых ИИ-агентов и методика её оценки'
            data=E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
        dst.writestr(info,data)
print('Refined candidate: metadata and non-wrapping cost labels, units remain on title and axis')
