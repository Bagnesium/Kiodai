from pathlib import Path
import json, re, hashlib, csv, html
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4

ROOT=Path('/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/daryn-defense-20260912')
OUT=ROOT/'output'
notes=json.loads((ROOT/'.build/content.json').read_text())['notes']
lines=['# Kiodai — сценарий устной защиты','',
       'Основная часть: 10 слайдов, суммарно 7:00. Это редакционное допущение, а не установленный конкурсный лимит. Резервные слайды A–D в эти семь минут не входят. Текст с переходами содержит около 870 слов. Время включает короткие паузы на графики. Источники и оговорки ниже предназначены для подготовки и не добавляются к произносимому тексту.','']
t=0
for i,n in enumerate(notes,1):
    end=t+n['seconds']
    lines += [f"## Слайд {i} · {n['title']} · {n['seconds']} секунд",
              '',f"Время: {t//60}:{t%60:02d}–{end//60}:{end%60:02d}.",'',n['speech'],'',f"**Переход:** {n['transition']}",'',f"**Оговорка для подготовки:** {n['qualification']}",'',f"**Источник:** {n['source']}",'']
    t=end
lines += ['## Репетиция','',
          'На слайде 5 сначала покажите три столбца, затем назовите разности. На слайде 7 ведите рассказ по стрелкам. Перед последним выводом сделайте короткую паузу. Вопросы жюри обсуждайте после основной части с резервными слайдами. Перед защитой проговорите текст вслух с секундомером: индивидуальная скорость речи не проверялась.','']
(OUT/'Сценарий_защиты.md').write_text('\n'.join(lines))

with (OUT/'Данные_диаграмм.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['method','mean_trajectory_Set_F1','micro_Set_F1','TP','FP','FN','calls','API_USD_displayed','API_USD_recorded','hidden_board_queries','query_supported_successes','selection_validation_failures'])
    w.writerows([
      ['A0',.8643,.8462,22,6,2,117,.04047,.04047361,15,6,2],
      ['B_ledger',.8111,.8372,18,4,3,251,.21212,.21212084,8,4,24],
      ['A2',.4806,.6667,12,5,7,234,.19871,.19870816,18,3,15]])

pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold')
title=ParagraphStyle('Title',fontName='ArialBold',fontSize=17,leading=20,spaceAfter=10,textColor=colors.HexColor('#172B36'))
body=ParagraphStyle('Body',fontName='Arial',fontSize=9.8,leading=12.25,spaceAfter=7,textColor=colors.HexColor('#172B36'))
story=[]
for chunk in (OUT/'Спецификация_стенда.md').read_text().split('\n\n'):
    if chunk.startswith('# '): story.append(Paragraph(html.escape(chunk[2:]),title))
    else:
        chunk=html.escape(chunk)
        chunk=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',chunk)
        story.append(Paragraph(chunk,body))
doc=SimpleDocTemplate(str(OUT/'Спецификация_стенда.pdf'),pagesize=A4,rightMargin=32,leftMargin=32,topMargin=30,bottomMargin=30,title='Kiodai — спецификация стенда',author='Материалы защиты Kiodai')
doc.build(story)
print('Created script, CSV and poster specification PDF')
