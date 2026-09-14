"""Editable vector charts from audited records; ReportLab chart engine."""
from pathlib import Path
import csv,subprocess
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF,renderSVG
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
OUT=Path(__file__).resolve().parents[1];TMP=OUT.parents[1]/'tmp/daryn_qa'
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
with (OUT/'data/method_summary.csv').open(newline='') as data_file:
 a={'totals':{r['method']:r for r in csv.DictReader(data_file)}}
methods=['A0','B_ledger','A2']
colors=[HexColor(c) for c in ['#5A6E83','#588D86','#A06155']]
poppler='/Users/bagnesium/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
def save(d,name):
 renderSVG.drawToFile(d,str(OUT/f'figures/{name}.svg'))
 renderPDF.drawToFile(d,str(TMP/f'{name}.pdf'))
 subprocess.run([poppler,'-scale-to','1800','-png','-singlefile',str(TMP/f'{name}.pdf'),str(OUT/f'figures/{name}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
for name,key,label,maxi,step,fmt in [('mean_f1','mean_trajectory_set_f1','Среднее траекторное Set-F1',1,.2,'.4f'),('api_cost','api_cost_usd','Расходы API, USD',.25,.05,'.5f')]:
 d=Drawing(468,195);vals=[float(a['totals'][m][key]) for m in methods]
 chart=VerticalBarChart();chart.x=48;chart.y=30;chart.width=405;chart.height=137;chart.data=[vals]
 chart.categoryAxis.categoryNames=methods;chart.categoryAxis.labels.fontName='Arial';chart.categoryAxis.labels.fontSize=11
 chart.categoryAxis.strokeColor=HexColor('#9BA4AB');chart.categoryAxis.tickDown=0
 chart.valueAxis.valueMin=0;chart.valueAxis.valueMax=maxi;chart.valueAxis.valueStep=step;chart.valueAxis.labels.fontName='Arial';chart.valueAxis.labels.fontSize=9
 chart.valueAxis.labelTextFormat=lambda v:f'{v:g}'.replace('.',',');chart.valueAxis.visibleGrid=True;chart.valueAxis.gridStrokeColor=HexColor('#DFE3E6');chart.valueAxis.gridStrokeWidth=.5;chart.valueAxis.strokeColor=HexColor('#9BA4AB');chart.valueAxis.tickLeft=0
 chart.barSpacing=0;chart.groupSpacing=36
 for i,c in enumerate(colors):chart.bars[(0,i)].fillColor=c;chart.bars[(0,i)].strokeColor=c
 d.add(chart);d.add(String(48,182,label,fontName='Arial',fontSize=10,fillColor=HexColor('#222222')))
 for i,v in enumerate(vals):d.add(String(48+405*(i+.5)/3,30+137*v/maxi+6,format(v,fmt).replace('.',','),fontName='Arial-Bold',fontSize=11,textAnchor='middle'))
 save(d,name)
d=Drawing(468,278)
def box(x,y,w,h,text,fill='#F0F3F5',size=10):
 d.add(Rect(x,y,w,h,fillColor=HexColor(fill),strokeColor=HexColor('#66727A'),strokeWidth=.7,rx=3,ry=3))
 ls=text.split('\n')
 for i,t in enumerate(ls):d.add(String(x+w/2,y+h/2+(len(ls)-1)*6-i*12-3,t,textAnchor='middle',fontName='Arial',fontSize=size))
def arrow(x1,y1,x2,y2,dashed=False):
 import math
 l=Line(x1,y1,x2,y2,strokeColor=HexColor('#46545D'),strokeWidth=.8)
 if dashed:l.strokeDashArray=[3,2]
 d.add(l);theta=math.atan2(y2-y1,x2-x1);ang=.45;length=6
 d.add(Polygon([x2,y2,x2-length*math.cos(theta-ang),y2-length*math.sin(theta-ang),x2-length*math.cos(theta+ang),y2-length*math.sin(theta+ang)],fillColor=HexColor('#46545D'),strokeColor=None))
box(3,235,135,39,'Публичная история\nи наблюдения')
box(168,235,135,39,'Модель извлекает\nи пересматривает')
box(333,235,132,39,'Общий Store\nзаписи и версии')
arrow(139,254,165,254);arrow(304,254,330,254)
box(60,160,157,43,'B_ledger\nЗапрос выбирает модель','#E7F0ED')
box(262,160,160,43,'A2\nКанал выбирает контроллер','#F2E6E1')
arrow(360,233,340,205);arrow(335,236,143,205)
box(68,84,332,45,'Свидетельство → модель выбирает действие\nПроверяются привязка, версия и статус',size=10)
arrow(140,158,156,131);arrow(342,158,314,131)
box(3,6,222,48,'Исполнение в симуляторе → receipt\nРезультат обновляет общий Store',size=9.5)
box(248,6,217,48,'Отдельное состояние оценщика\nСопоставление действия с due',size=9.5)
arrow(156,82,115,57);arrow(314,82,358,57,True)
save(d,'architecture')
