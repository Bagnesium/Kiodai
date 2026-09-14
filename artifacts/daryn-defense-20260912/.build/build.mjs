import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { resolvePresentationFont, applyPresentationChartFont } from '/Users/bagnesium/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations/container_tools/artifact_tool_utils.mjs';

const ROOT='/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/daryn-defense-20260912';
const B=path.join(ROOT,'.build');
const content=JSON.parse(await fs.readFile(path.join(B,'content.json'),'utf8'));
const F=resolvePresentationFont({fontFamily:'Arial',availableFonts:['Arial']});
const C={bg:'#F8F9F7',ink:'#172B36',muted:'#52656C',line:'#D5DEDF',a0:'#2D5E7C',ledger:'#368276',a2:'#A76449',pale:'#E8EFEC',white:'#FFFFFF'};
const p=Presentation.create({slideSize:{width:1280,height:720}});
const slides=[];

function text(s,t,x,y,w,h,size=30,bold=false,color=C.ink,align='left'){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=t;
 sh.text.style={typeface:F,fontSize:size,bold,color,alignment:align,verticalAlignment:'top',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};
 return sh;
}
function rule(s,x,y,w,color=C.line,width=1.5){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},fill:'none',line:{fill:color,width,style:'solid'}});}
function box(s,t,x,y,w,h,size=28,fill=C.white,color=C.ink){
 const sh=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:C.line,width:1.5}});
 sh.text=t;sh.text.style={typeface:F,fontSize:size,color,verticalAlignment:'middle',alignment:'center',autoFit:'none',insets:{left:12,right:12,top:10,bottom:10}};return sh;
}
function arrow(s,a,b,dashed=false){return s.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:C.muted,width:2,style:dashed?'dashed':'solid'},tail:{type:'triangle',width:'sm',length:'sm'}});}
function base(title,n,source,backup=false){
 const s=p.slides.add();s.background.fill=C.bg;slides.push(s);
 if(backup){text(s,'РЕЗЕРВ '+String.fromCharCode(65+n-11),64,28,400,28,20,true,C.ledger);text(s,title,64,73,1152,100,44,true);}
 else text(s,title,64,43,1152,117,44,true);
 rule(s,64,657,1152);
 text(s,source,64,672,1070,25,18,false,C.muted);
 text(s,backup?String.fromCharCode(65+n-11):String(n).padStart(2,'0'),1140,669,76,31,21,true,C.muted,'right');
 if(n<=10){const v=content.notes[n-1];s.speakerNotes.textFrame.setText(`СЛАЙД ${n}. ${v.title}\nВремя: ${v.seconds} секунд.\n\n${v.speech}\n\nПереход: ${v.transition}\n\nОбязательно проговорить: ${v.qualification}\n\nИсточник: ${v.source}`);}
 return s;
}
function chart(s,values,max,unit,format,y=212,height=338){
 const ch=s.charts.add('bar',{
  position:{left:68,top:y,width:1120,height},
  categories:['A2','B_ledger','A0'],
  series:[{name:unit,values:[...values].reverse(),valuesFormatCode:format,fill:C.a0,points:[{idx:0,fill:C.a2},{idx:1,fill:C.ledger},{idx:2,fill:C.a0}]}],
  barOptions:{direction:'bar',grouping:'clustered',gapWidth:75},
  hasLegend:false,
  yAxis:{visible:true,min:0,max,majorUnit:max===1?0.2:0.05,numberFormatCode:max===1?'0.0':'$0.00',textStyle:{fontSize:24,typeface:F,fill:C.muted},line:{fill:C.line,width:1},majorGridlines:{fill:C.line,width:1,style:'solid'}},
  xAxis:{visible:true,textStyle:{fontSize:29,typeface:F,fill:C.ink,bold:true},line:{fill:'none',width:0},majorGridlines:null},
  dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:29,typeface:F,fill:C.ink,bold:true}},
  chartFill:'none',plotAreaFill:'none',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}
 });
 applyPresentationChartFont(ch,{fontFamily:F});return ch;
}
function table(s,values,x,y,w,h,widths,size=25){
 const tb=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,columnWidths:widths});
 tb.borders.assign({fill:C.line,width:1,style:'solid'});
 tb.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({textStyle:{fontSize:size,typeface:F,color:C.ink},margins:{left:12,right:12,top:12,bottom:12},anchor:'center'});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
  const cell=tb.getCell(r,c);cell.fill=r===0?C.pale:C.bg;
  cell.text.style={typeface:F,fontSize:r===0?size-2:size,bold:r===0||c===0,color:values[0][0]==='Метод'&&r>0&&c===0?[C.a0,C.ledger,C.a2][r-1]:values[0][0]==='Счётчик'&&r===0&&c>0?[C.a0,C.ledger,C.a2][c-1]:C.ink,alignment:c===0?'left':'center',verticalAlignment:'middle'};
 }
 return tb;
}

// 1. A title and an editable conceptual timeline.
{
 const s=p.slides.add();s.background.fill=C.bg;slides.push(s);
 text(s,'Kiodai',64,42,520,84,78,true,C.ink);
 text(s,'Структурированная перспективная память\nязыковых ИИ-агентов и методика её оценки',64,145,1150,108,39,true);
 text(s,'Беймжан Багдат, 10 класс',64,280,610,40,30,true);
 text(s,'Назарбаев Интеллектуальная школа естественно-математического\nнаправления района Нура города Астаны',64,330,1150,65,24,false,C.muted);
 text(s,'Руководитель: Омаров Абылайхан Бауржанович',64,407,1150,36,25,false,C.muted);
 text(s,'Когда появится нужное условие, выполни ранее заданное поручение.',64,476,1150,41,28,true);
 const a=box(s,'Поручение',64,540,275,64,25);
 const b=box(s,'Другая деятельность',411,540,394,64,25);
 const c=box(s,'Условие и действие',877,540,339,64,25);
 arrow(s,a,b);arrow(s,b,c);
 text(s,'Схема задачи',64,615,600,27,20,false,C.muted);
 rule(s,64,657,1152);text(s,'Астана, 2026    Секция: информатика',64,672,1050,27,20,false,C.muted);text(s,'01',1150,669,66,31,21,true,C.muted,'right');
 const v=content.notes[0];s.speakerNotes.textFrame.setText(`Время: ${v.seconds} секунд.\n\n${v.speech}\n\nПереход: ${v.transition}\n\nОговорка: ${v.qualification}\n\nИсточник: ${v.source}`);
}
// 2.
{
 const s=base('Исследовательский вопрос и гипотеза',2,'Источники: статья, § 1–2; PM-Bench (2026); PIS (2026)');
 text(s,'Вспомнить поручение',64,184,535,46,34,true);
 text(s,'Выполнить его вовремя',665,184,550,46,34,true,C.ledger);
 rule(s,64,250,1152);
 text(s,'Помогает ли явная поддержка намерений\nдействовать вовремя по сравнению с тем же\nагентом без такой поддержки?',64,290,1152,150,37,true);
 text(s,'Гипотеза: условия, действия и состояния\nв явном виде повысят качество.',64,469,1130,84,32);
 text(s,'Структурированное хранение уже исследуется в PIS.\nСама идея хранения не заявляется как новая.',64,582,1150,57,23,false,C.muted);
}
// 3.
{
 const s=base('Что построено и с чем сравнивается',3,'Источники: FOLLOWUP_RESULTS; замороженный протокол comparison-v1');
 text(s,'Исторические пилоты A1',64,176,365,39,28,true,C.muted);
 text(s,'Дополнение к инструкции\n\nA0 = A1: 1,00\nПозднее: ≈ 0,9565\n\nБольше входных токенов',64,233,340,256,28,false,C.muted);
 rule(s,442,178,0,C.line);s.shapes.add({geometry:'line',position:{left:442,top:178,width:0,height:423},line:{fill:C.line,width:2}});
 text(s,'Финальное сравнение',488,176,680,39,28,true);
 text(s,'A0',488,235,150,40,32,true,C.a0);text(s,'История и разрешённые инструменты',662,238,542,72,28);
 rule(s,488,325,728);
 text(s,'Общие извлечение, хранилище, версии\nи обработка подтверждений:',488,344,720,75,27);
 text(s,'B_ledger',488,448,180,42,31,true,C.ledger);text(s,'Запросами управляет модель',710,451,494,77,28);
 text(s,'A2',488,548,180,42,32,true,C.a2);text(s,'Запросами управляет\nограниченный контроллер',710,545,505,83,28);
}
// 4.
{
 const s=base('Дизайн эксперимента',4,'Источник: comparison-v1, протокол и итоговый отчёт от 11.09.2026');
 const xs=[64,465,866];const nums=['12','4','3'];const labs=['траекторий','семейства шаблонов','метода'];
 xs.forEach((x,i)=>{text(s,nums[i],x,164,345,96,84,true,i===2?C.ledger:C.ink);text(s,labs[i],x,267,348,44,30);});
 text(s,'События, скрытые условия, другой день, изменения поручений',64,339,1152,44,27,false,C.muted);
 rule(s,64,404,1152);
 text(s,'DeepSeek V3.1 через OpenRouter / Novita',64,429,1152,43,30,true);
 text(s,'36 запусков методов, 288 контрольных точек, 602 вызова',64,488,1152,41,27);
 text(s,'Set-F1 учитывает правильные действия, пропуски и лишние действия.',64,545,1152,61,26);
 text(s,'Сценарии разработки; один запуск на условие.',64,611,1152,35,27,true,C.a2);
}
// 5.
{
 const s=base('В этом сравнении A0 получил\nнаивысший результат',5,'Источник: COMPARISON_RESULTS, Primary results; comparison_report_reviewed.json');
 text(s,'Средний Set-F1 по траекториям',64,172,1115,43,28,false,C.muted);
 chart(s,[0.8643,0.8111,0.4806],1,'Средний Set-F1 по траекториям','0.0000',220,327);
 text(s,'A2 − B_ledger ≈ −0,3306',64,568,550,43,31,true,C.a2);
 text(s,'A2 − A0 ≈ −0,3837',684,568,532,43,31);
 text(s,'Основная разность',64,615,540,29,22,false,C.muted);
 text(s,'Вторичная разность',684,615,532,29,22,false,C.muted);
}
// 6.
{
 const s=base('Дополнительные вычисления не дали\nулучшения в этой серии',6,'Источник: COMPARISON_RESULTS, Resources and billing status');
 text(s,'Записанная стоимость API, USD',64,172,1090,43,28,false,C.muted);
 chart(s,[0.04047,0.21212,0.19871],0.25,'API cost, USD','$0.00000',220,327);
 text(s,'A2 / A0 ≈ 4,91 раза',64,568,700,49,36,true,C.a2);
 text(s,'Стоимость этой серии по API. Не текущие тарифы и не затраты разработки.',64,622,1152,29,22,false,C.muted);
}
// 7.
{
 const s=base('После замены условия вернулся старый триггер',7,'Трасса A2: v2_visible_events_91310, steps.jsonl, точки 3–7; перевод и сокращение');
 text(s,'Поручение: запечатать контейнер при новом сигнале «треугольник».',64,176,1152,74,30);
 const aa=box(s,'Точка 3\n\nСохранён\nтреугольник\nВерсия 2',64,276,324,231,29);
 const bb=box(s,'Точка 4\n\nПоявился фонарь\nОн вернулся в запись\nВерсия 3',476,276,326,231,28,C.white,C.a2);
 const cc=box(s,'Действие\n\nПопытка запечатать\nБез подтверждения\nFP = 1',890,276,326,231,28);
 arrow(s,aa,bb);arrow(s,bb,cc);
 text(s,'Точка 5: условие восстановлено. Ранняя ошибка осталась в оценке.',64,540,1152,45,26);
 text(s,'Локальная ошибка обновления и действия. Причина общего отставания не установлена.',64,601,1152,52,25,true,C.a2);
}
// 8.
{
 const s=base('Где может возникнуть ошибка',8,'Источники: журналы A2 visible_events_91310 и hidden_91320; семантический разбор');
 const names=['Инструкция','Интерпре-\nтация','Состояние','Пересмотр','Мониторинг','Выбор\nдействия','Исполнение'];
 const boxes=names.map((v,i)=>box(s,v,64+i*167,199,150,106,23));
 boxes.forEach(b=>{b.text.insets={left:3,right:3,top:10,bottom:10};});
 for(let i=1;i<boxes.length;i++)arrow(s,boxes[i-1],boxes[i]);
 text(s,'Наблюдается в журналах',64,345,550,42,28,true);
 text(s,'Старое условие вернулось в запись.\nПоложительный ответ скрытого канала\nполучен, но действие не выполнено.',64,399,680,141,28);
 text(s,'Возможное объяснение',820,345,396,74,28,true,C.a2);
 text(s,'Ошибочная интерпретация\nможет влиять на следующие\nрешения. Вклад не изолирован.',820,415,396,145,27,false,C.muted);
 text(s,'Наличие сохранённой информации само по себе\nне обеспечило правильного действия.',64,582,1152,65,29,true);
}
// 9.
{
 const s=base('Ограничения и фактический вклад',9,'Источники: итоговый отчёт, Methods and discussion; статья, § 7');
 text(s,'Установлено',64,181,520,43,33,true,C.ledger);
 text(s,'Система реализована и сравнена.\nУ A2 самый низкий основной балл.\nВ журналах есть конкретные сбои.',64,248,532,159,29);
 text(s,'Не установлено',682,181,534,43,33,true);
 text(s,'Перенос на другие модели и практику.\nРезультат на закрытой выборке.\nПричинный вклад каждого этапа.\nУспешность исправления.',682,248,534,185,28);
 rule(s,64,457,1152);
 text(s,'4 семейства, 1 запуск на условие, известные сценарии,\nнеравные вычисления, разбор ошибок с ИИ-помощью.',64,479,1152,81,27,false,C.muted);
 text(s,'Вклад автора: вопрос и методика сравнения.\nКод и текст подготовлены с ИИ-помощью.',64,576,1152,71,28,true);
}
// 10.
{
 const s=base('Проверенная A2 не улучшила основную метрику',10,'Источник: финальное сравнение v2.1; диагностика с эталонным состоянием предложена');
 text(s,'Гипотеза об улучшении не получила\nподдержки в проверенных условиях.',64,197,1152,111,43,true,C.a2);
 rule(s,64,351,1152);
 text(s,'Следующий вопрос',64,388,1110,42,30,true);
 text(s,'Какая часть потерь возникает при построении\nи обновлении намерений, а какая при исполнении?',64,448,1152,99,34);
 text(s,'Предложение: диагностика с эталонным состоянием\nтолько из доступной к шагу информации. Ещё не проведена.',64,575,1152,76,27,false,C.muted);
}
// Backup A.
{
 const s=base('Метрики и полные результаты',11,'Источник: COMPARISON_RESULTS, Primary results и Resources; все 12 траекторий',true);
 table(s,[['Метод','Среднее\nSet-F1','Micro\nSet-F1','TP','FP','FN','Вызовы','API, USD'],['A0','0,8643','0,8462','22','6','2','117','0,04047'],['B_ledger','0,8111','0,8372','18','4','3','251','0,21212'],['A2','0,4806','0,6667','12','5','7','234','0,19871']],64,204,1152,257,[175,160,145,75,75,75,155,292].map(x=>x*1152/1152),26);
 text(s,'Set-F1 = 2TP / (2TP + FP + FN)',64,491,1152,48,34,true);
 text(s,'TP: верное действие. FP: лишнее. FN: пропущенное.',64,547,1152,35,25);
 text(s,'Среднее: равный вес каждой траектории. Micro: сначала сумма TP, FP, FN.\nСуммарные счётчики не восстанавливают распределение оценок по траекториям.',64,593,1152,56,23,false,C.muted);
 s.speakerNotes.textFrame.setText('Резерв A. Среднее по траекториям является основной мерой. Micro-F1 вычисляется из сумм счётчиков и имеет другие веса. Суммарные TP/FP/FN могут не отражать все неисполненные обязательства: зависимые задачи, которые не стали due, не следует произвольно добавлять в FN. Официальный оценщик не менялся. Контрасты из полного отчёта: A2−B_ledger = −0.330556, A2−A0 = −0.383730. Источник: docs/v2_1/COMPARISON_RESULTS.md; comparison_report_reviewed.json.');
}
// Backup B.
{
 const s=base('Валидность сравнения',12,'Источники: comparison_v1.json; COMPARISON_PROTOCOL; COMPARISON_RESULTS',true);
 const rows=[['Парные условия','Одинаковые стартовые инструкции, инструменты и 8 точек.\nУ каждого метода своё состояние и последующая история.'],['Экспозиция','Все 12 сценариев известны при разработке.\nОдна траектория также использовалась в сетевой smoke-проверке.'],['Фиксация','Конфигурация, промпты и сценарии заморожены до запуска.\nИтоговый отчёт фиксирует завершение и сохранение ошибок.'],['Граница оценивания','Эталонные ответы остаются на стороне оценщика.\nНевалидный ответ после повтора даёт отсутствие действия.']];
 rows.forEach((r,i)=>{const y=200+i*93;text(s,r[0],64,y,260,51,28,true);text(s,r[1],348,y,868,77,25);if(i<3)rule(s,64,y+80,1152);});
 text(s,'288 точек и 602 вызова принадлежат тем же траекториям.\nЭто нагрузка, а не независимые повторения.',64,589,1152,63,28,true,C.a2);
 s.speakerNotes.textFrame.setText('Резерв B. Подготовительный COMPARISON_PROTOCOL.md сохраняет историческое «not executed»; фактическое завершение подтверждено COMPARISON_RESULTS.md и журналами. Кандидат 959db38dac8b68f63ecf79420dcd53bea2278cf2. Manifest SHA-256 bfaf52df48553e35978f39f406fd5eb3d78c918a5ac2713a0a169746f23036d5. Все методы стартуют заново для каждой траектории. Порядок балансирует позиции методов, но не все возможные порядки. Вычисления не выровнены. Проверки разделения оценщика не дают абсолютной гарантии отсутствия любой утечки.');
}
// Backup C.
{
 const s=base('Диагностика и её ограничения',13,'Источники: статья, § 5.3; comparison-v1, сценарии revision; semantic_review.json',true);
 table(s,[['Счётчик','A0','B_ledger','A2'],['Запросы скрытого канала','15','8','18'],['Успехи с опорой на запрос','6','4','3'],['Ошибки проверки выбора','2','24','15']],64,200,1152,231,[650,167,168,167],27);
 text(s,'Больше запросов не означает больше успешных действий.\nОшибки проверки не равны числу ошибочных намерений.',64,463,1152,75,27);
 text(s,'Учёт уточнён: 27 поручений = 24 завершённых\nили незавершённых без отменённых + 3 отменённых.',64,550,1152,72,30,true,C.a2);
 text(s,'Три отмены подтверждены в сценариях revision. Этот баланс не заменяет Set-F1.',64,628,1152,28,20,false,C.muted);
 s.speakerNotes.textFrame.setText('Резерв C. Счётчики включают разные сущности: запросы, успехи с доступной поддержкой и ошибки валидации выбора. Их отношения нельзя превращать в точность мониторинга без общего знаменателя. Не выполненный зависимый шаг не становится автоматически официальным FN. Баланс уточнён по актуальной статье, §5.3, и непосредственно проверен по трём сценариям revision, instructions cp5 и финальным снимкам оценщика. A0: 22 завершено + 2 не завершено без отменённых + 3 отменено = 27. B_ledger: 18+6+3=27. A2: 12+12+3=27. Это официальные отмены поручений пользователем, не ошибочные отмены в памяти агента. Не вводится процент выполнения как замена Set-F1. AI-assisted semantic review не является независимой человеческой разметкой. Техническая проверка JSON не равна семантической правильности.');
}
// Backup D.
{
 const s=base('Источники, авторство и воспроизводимость',14,'Полные локальные пути и проверенные ссылки приведены в заметках и записке об источниках',true);
 text(s,'Предшествующие работы',64,195,660,39,29,true);
 text(s,'Liu G., Gabriel S. PM-Bench (2026)\nПостановка задачи, среда и Set-F1\narXiv:2607.12385v1',64,249,623,99,25);
 text(s,'Zhao J., Wu C. Typed Intention Stores (2026)\nPIS: типизированные намерения и жизненный цикл\narXiv:2609.01272v1',64,380,638,111,25);
 text(s,'Zhang T. et al. TriggerBench (2026)\nПроверка условий срабатывания\narXiv:2606.23459v1',64,518,627,108,25);
 text(s,'Автор и доступные материалы',765,195,451,77,29,true);
 text(s,'Вопрос и методика сравнения.\nИИ помогал с кодом, текстом\nи разбором ошибок.',765,293,451,124,27);
 text(s,'Локально сохранены код,\nпромпты, конфигурации,\nзапросы, ответы и оценки.',765,431,451,122,27);
 text(s,'Код сам по себе не доказывает\nсамостоятельность и корректность.',765,586,451,64,23,true,C.muted);
 s.speakerNotes.textFrame.setText('Резерв D. Полные ссылки: https://arxiv.org/abs/2607.12385v1; https://arxiv.org/abs/2609.01272v1; https://arxiv.org/abs/2606.23459v1. Карточки arXiv проверены 12.09.2026. PM-Bench: PM-Bench: Evaluating Prospective Memory in LLM Agents. PIS: Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents. TriggerBench: Investigating Prospective Memory for Large Language Models. Структурированная система Kiodai является PIS-inspired инженерной интеграцией, не заявленной точной репродукцией. Актуальная статья, §7: авторский вклад в постановку вопроса и методику; ИИ используется для программирования и текста. Артефакты: results/v2_1/comparison-v1/, research/v2_1/comparison_v1.json, prompts/v2_1/, docs/v2_1/COMPARISON_RESULTS.md, artifacts/verification/v21-comparison-live-20260911/. Ссылка на публичный репозиторий не включена, потому что не была предоставлена и проверена для этой презентации.');
}

await (await PresentationFile.exportPptx(p)).save(path.join(B,'candidate.pptx'));
await fs.writeFile(path.join(B,'presentation.json'),JSON.stringify(p.toProto()));
await fs.mkdir(path.join(B,'preview'),{recursive:true});
for(let i=0;i<slides.length;i++){
 const blob=await p.export({slide:slides[i],format:'png',scale:1});
 await fs.writeFile(path.join(B,'preview',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
 const layout=await slides[i].export({format:'layout'});
 await fs.writeFile(path.join(B,'preview',`slide-${String(i+1).padStart(2,'0')}.json`),await layout.text());
 console.log('Rendered',i+1);
}
console.log('Draft created:',path.join(B,'candidate.pptx'));
