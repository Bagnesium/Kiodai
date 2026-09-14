import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {applyPresentationChartFont} from '/Users/bagnesium/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations/container_tools/artifact_tool_utils.mjs';

const ROOT='/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/daryn-defense-20260912';
const B=path.join(ROOT,'.build');
const source=JSON.parse(await fs.readFile(path.join(B,'restyle-source.json'),'utf8'));
const C={ink:'#171A21',muted:'#666C78',accent:'#4D6CB5',line:'#DCE0E7',pale:'#F4F6FA',white:'#FFFFFF',bar0:'#363C49',bar1:'#9BA5B9'};
const F='Arial';
const p=Presentation.create({slideSize:{width:1280,height:720}});
const used=new Map();
const slides=[];
const norm=t=>t.replace(/Интерпре-\s*тация/g,'Интерпретация').replace(/\s+/g,' ').trim();
const src=(n,id)=>source[n-1].shapes[String(id)];
function text(s,t,x,y,w,h,size=27,bold=false,color=C.ink,align='left'){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=t;sh.text.style={typeface:F,fontSize:size,bold,color,alignment:align,verticalAlignment:'top',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};
 return sh;
}
function put(s,id,x,y,w,h,size=27,bold=false,color=C.ink,t=null,align='left'){
 const n=slides.indexOf(s)+1,key=`${n}:${id}`;
 if(t===null)t=src(n,id);
 const prev=used.get(key)||[];prev.push(t);used.set(key,prev);
 const sh=text(s,t,x,y,w,h,size,bold,color,align);sh.name=`source-${key}-${prev.length}`;return sh;
}
function rule(s,x,y,w,color=C.line,width=1){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},fill:'none',line:{fill:color,width}});}
function vertical(s,x,y,h){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:0,height:h},fill:'none',line:{fill:C.line,width:1}});}
function rect(s,x,y,w,h,fill=C.white,border=C.line){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:border,width:1}});}
function arrow(s,a,b){return s.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:'#929BAA',width:1.2},tail:{type:'triangle',width:'sm',length:'sm'}});}
const titleIds={2:11,3:18,4:17,5:11,6:9,7:13,8:23,9:12,10:10,11:2,12:2,13:2,14:2};
const backupIds={11:10,12:18,13:10,14:14};
function base(n){
 const s=p.slides.add();s.background.fill=C.white;slides.push(s);
 if(n!==1){
  const title=src(n,titleIds[n]);
  if(n>=11){put(s,backupIds[n],64,30,240,25,17,true,C.accent);put(s,titleIds[n],64,76,1120,59,37,false);}
  else put(s,titleIds[n],64,46,1090,94,n===5||n===6?38:37,false,C.ink,title);
  put(s,n>=11?5:4,1188,48,28,26,18,false,C.muted,null,'right');
  rule(s,64,151,1152,'#B6BEC9');
  put(s,n>=11?4:3,64,680,1152,25,16,false,C.muted);
 }
 s.speakerNotes.textFrame.setText(source[n-1].notes);
 return s;
}
function chart(s,values,max,unit,fmt){
 const c=s.charts.add('bar',{
  position:{left:65,top:244,width:794,height:323},categories:['A2','B_ledger','A0'],
  series:[{name:unit,values:[...values].reverse(),valuesFormatCode:fmt,fill:C.bar0,points:[{idx:0,fill:C.accent},{idx:1,fill:C.bar1},{idx:2,fill:C.bar0}]}],
  barOptions:{direction:'bar',grouping:'clustered',gapWidth:135},hasLegend:false,
  xAxis:{visible:true,textStyle:{fontSize:25,typeface:F,fill:C.ink,bold:false},line:{fill:'none',width:0},majorGridlines:null},
  yAxis:{visible:true,min:0,max,majorUnit:max===1?.2:.05,numberFormatCode:max===1?'0.0':'$0.00',textStyle:{fontSize:18,typeface:F,fill:C.muted},line:{fill:C.line,width:1},majorGridlines:{fill:'#E9ECF1',width:.6}},
  dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:25,typeface:F,fill:C.ink,bold:false}},
  chartFill:'none',plotAreaFill:'none',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}
 });applyPresentationChartFont(c,{fontFamily:F});return c;
}
function nativeTable(s,n,y,h,widths){
 const vals=source[n-1].tables[0];
 const tb=s.tables.add({rows:vals.length,columns:vals[0].length,left:64,top:y,width:1152,height:h,values:vals,columnWidths:widths});
 tb.borders.assign({fill:C.line,width:.7,style:'solid'});
 tb.cells.block({row:0,column:0,rowCount:vals.length,columnCount:vals[0].length}).assign({margins:{left:14,right:14,top:12,bottom:12},anchor:'center'});
 for(let r=0;r<vals.length;r++)for(let c=0;c<vals[0].length;c++){
  const cell=tb.getCell(r,c);
  const highlight=n===11?r===3:c===3;
  cell.fill=highlight?C.pale:C.white;
  cell.text.style={typeface:F,fontSize:r===0?20:(c===0?25:28),bold:r===0,alignment:c===0?'left':'center',verticalAlignment:'middle',color:highlight?C.accent:r===0?C.muted:C.ink};
 }
 return tb;
}

// Cover: title, provenance, then the unchanged task schematic.
{
 const s=base(1);
 put(s,16,64,48,560,106,92,false);
 put(s,15,1188,48,28,26,18,false,C.muted,null,'right');
 put(s,2,64,172,1140,100,38,false);
 rule(s,64,300,1152,'#B6BEC9');
 put(s,3,64,335,580,38,28,true);
 put(s,4,64,390,670,73,23,false,C.muted,src(1,4).replace('естественно-математического\n','\nестественно-математического '));
 put(s,5,805,335,411,104,23,false,C.muted,src(1,5).replace(': ',':\n').replace(' Абылайхан','\nАбылайхан'));
 put(s,6,64,488,1152,41,26,false,C.ink);
 const aa=rect(s,64,549,294,63),bb=rect(s,445,549,363,63),cc=rect(s,895,549,321,63,C.pale,'#C6D1E8');
 put(s,7,79,568,264,32,24,false,C.ink,null,'center');put(s,8,460,568,333,32,24,false,C.ink,null,'center');put(s,9,910,568,291,32,24,false,C.accent,null,'center');
 arrow(s,aa,bb);arrow(s,bb,cc);
 put(s,12,64,630,400,27,18,false,C.muted);put(s,14,64,680,1152,25,16,false,C.muted);
}
{
 const s=base(2);
 put(s,5,64,199,520,43,27,false,C.muted);put(s,6,662,199,554,43,27,true,C.accent);
 rule(s,64,263,1152);
 put(s,8,64,302,1140,158,39,false);
 put(s,9,64,502,643,97,28,false,C.ink,'Гипотеза: условия, действия и состояния\nв явном виде повысят качество.');
 vertical(s,744,503,105);
 put(s,10,793,502,423,125,23,false,C.muted,'Структурированное хранение\nуже исследуется в PIS.\nСама идея хранения\nне заявляется как новая.');
}
{
 const s=base(3);
 put(s,5,64,192,358,62,27,false,C.muted);
 const lines=src(3,6).split('\n');
 put(s,6,64,268,328,60,24,false,C.muted,lines[0]);
 put(s,6,64,356,350,45,34,false,C.ink,lines[2]);
 put(s,6,64,408,350,45,26,false,C.muted,lines[3]);
 put(s,6,64,525,320,70,24,false,C.muted,lines[5]);
 vertical(s,442,196,417);
 put(s,9,492,192,700,40,29,true);
 put(s,10,492,258,170,43,31,false);put(s,11,688,258,528,70,26);
 rule(s,492,346,724);
 put(s,13,492,370,724,75,25,false,C.muted);
 put(s,14,492,470,172,40,30,false);put(s,15,688,473,528,44,26);
 put(s,16,492,548,172,42,31,true,C.accent);
 put(s,17,688,548,528,100,25,false,C.ink,'Контроллер проверяет до одного\nканала за шаг, начиная с давно\nне проверявшегося.');
}
{
 const s=base(4);const xs=[64,468,872];
 [[5,6],[7,8],[9,10]].forEach(([v,l],i)=>{put(s,v,xs[i],188,330,109,92,false,i===2?C.accent:C.ink);put(s,l,xs[i],312,340,43,28,false);});
 put(s,11,64,389,1152,39,25,false,C.muted);
 rule(s,64,448,1152);
 put(s,13,64,479,610,78,28,true,C.ink,'DeepSeek V3.1\nчерез OpenRouter / Novita');
 put(s,14,720,482,496,87,26,false,C.ink,'36 запусков методов,\n288 контрольных точек, 602 вызова');
 put(s,15,64,588,654,64,23,false,C.muted,'Set-F1 учитывает правильные действия,\nпропуски и лишние действия.');
 put(s,16,720,588,496,62,23,false,C.accent,'Сценарии разработки;\nодин запуск на условие.');
}
{
 const s=base(5);put(s,5,64,195,800,37,25,false,C.muted);
 chart(s,[.8643,.8111,.4806],1,'Средний Set-F1 по траекториям','0.0000');
 vertical(s,899,247,326);
 put(s,9,944,251,272,30,20,false,C.muted);
 put(s,7,944,300,272,34,25,false,C.ink,'A2 − B_ledger ≈');put(s,7,940,345,280,70,48,false,C.accent,'−0,3306');
 rule(s,944,434,272);
 put(s,10,944,465,272,30,20,false,C.muted);
 put(s,8,944,506,272,33,25,false,C.ink,'A2 − A0 ≈');put(s,8,944,548,272,59,43,false,C.ink,'−0,3837');
}
{
 const s=base(6);put(s,5,64,195,800,37,25,false,C.muted);
 chart(s,[.04047,.21212,.19871],.25,'API cost, USD','0.00000');
 vertical(s,899,247,326);
 put(s,7,944,286,272,39,27,false,C.muted,'A2 / A0 ≈');
 put(s,7,938,344,280,90,72,false,C.accent,'4,91');put(s,7,944,438,272,39,28,false,C.muted,'раза');
 rule(s,64,606,1152);put(s,8,64,629,1152,35,23,false,C.muted);
}
{
 const s=base(7);put(s,5,64,190,1152,67,27,false);
 const xs=[64,473,882];const panels=xs.map((x,i)=>rect(s,x,292,334,219,i===1?C.pale:C.white,i===1?'#CBD5EA':C.line));
 for(let i=0;i<3;i++){
  const id=6+i,lines=src(7,id).split('\n').filter(Boolean);
  put(s,id,xs[i]+24,316,286,35,25,true,i===1?C.accent:C.ink,lines[0]);
  const main=lines.slice(1,-1).join('\n');put(s,id,xs[i]+24,372,286,76,25,false,C.ink,main);
  put(s,id,xs[i]+24,470,286,29,21,false,i===1?C.accent:C.muted,lines.at(-1));
 }
 arrow(s,panels[0],panels[1]);arrow(s,panels[1],panels[2]);
 put(s,11,64,544,1152,37,25,false);
 put(s,12,64,601,1152,58,25,false,C.accent,'Локальная ошибка обновления и действия.\nПричина общего отставания не установлена.');
}
{
 const s=base(8);const boxes=[];
 for(let i=0;i<7;i++){
  const x=64+i*168;boxes.push(rect(s,x,219,144,77,C.white,'#CCD3DF'));
  const t=src(8,5+i);put(s,5+i,x+4,238,136,57,22,false,C.ink,t,'center');
 }
 for(let i=1;i<7;i++)arrow(s,boxes[i-1],boxes[i]);
 put(s,18,64,358,620,37,25,true);put(s,19,64,419,653,141,28,false);
 vertical(s,754,358,186);
 put(s,20,803,358,413,37,25,true,C.accent);put(s,21,803,419,413,141,26,false,C.muted);
 rule(s,64,571,1152);
 put(s,22,64,598,1152,69,29,false,C.ink);
}
{
 const s=base(9);
 put(s,5,64,195,530,39,29,true,C.accent);put(s,7,683,195,533,39,29,true);
 put(s,6,64,255,550,142,28,false);put(s,8,683,255,533,166,27,false);
 vertical(s,636,198,214);rule(s,64,447,1152);
 put(s,10,64,474,1152,79,25,false,C.muted);
 put(s,11,64,582,1152,82,28,false,C.ink,'Вклад автора: постановка эксперимента, организация разработки,\nзапуска сравнения и анализа результатов с ИИ-помощью.');
}
{
 const s=base(10);
 put(s,5,64,217,1152,132,46,false,C.accent);
 rule(s,64,388,1152);
 put(s,7,64,436,288,68,27,true);
 put(s,8,389,434,827,104,31,false,C.ink,'Какая часть потерь возникает при построении\nи обновлении намерений, а какая при исполнении?');
 put(s,9,389,574,827,89,25,false,C.muted,'Предложение: диагностика с эталонным состоянием\nтолько из доступной к шагу информации. Ещё не проведена.');
}
{
 const s=base(11);nativeTable(s,11,192,279,[169,166,151,84,84,84,168,246]);
 put(s,7,64,503,1152,51,37,false,C.accent);put(s,8,64,568,1152,34,25,false);
 put(s,9,64,618,1152,53,21,false,C.muted);
}
{
 const s=base(12);
 [[6,7],[9,10],[12,13],[15,16]].forEach(([h,b],i)=>{
  const y=193+i*92;put(s,h,64,y,253,65,26,false,C.ink);put(s,b,357,y,859,68,24,false);
  if(i<3)rule(s,64,y+75,1152);
 });
 rule(s,64,572,1152);put(s,17,64,603,1152,66,28,false,C.accent);
}
{
 const s=base(13);nativeTable(s,13,189,259,[637,171,172,172]);
 put(s,7,64,478,1152,77,26,false);
 put(s,8,64,572,1152,78,30,false,C.accent);
 put(s,9,64,648,1152,25,19,false,C.muted);
}
{
 const s=base(14);
 put(s,6,64,193,650,39,27,true);put(s,10,794,193,422,71,27,true);
 vertical(s,748,194,436);
 [[7,264],[8,393],[9,531]].forEach(([id,y])=>{
  const ls=src(14,id).split('\n');put(s,id,64,y,651,38,24,false,C.ink,ls[0]);put(s,id,64,y+37,651,38,23,false,C.muted,ls[1]);put(s,id,64,y+72,651,31,21,false,C.accent,ls[2]);
 });
 rule(s,64,374,651);rule(s,64,510,651);
 put(s,11,794,292,422,139,27,false);put(s,12,794,483,422,136,27,false,C.muted);
}

const mismatches=[];
for(const slide of source)for(const [id,t] of Object.entries(slide.shapes)){
 const got=used.get(`${slide.number}:${id}`)||[];
 if(norm(got.join(' '))!==norm(t))mismatches.push({slide:slide.number,id,expected:t,got:got.join(' ')});
}
if(mismatches.length)throw Error(JSON.stringify(mismatches,null,2));
await fs.writeFile(path.join(B,'restyle-copy-audit.json'),JSON.stringify({source:'Kiodai_Daryn_2026_defense_revised.pptx',textGroups:used.size,mismatches},null,2));
await (await PresentationFile.exportPptx(p)).save(path.join(B,'restyled-draft.pptx'));
await fs.writeFile(path.join(B,'restyled-proto.json'),JSON.stringify(p.toProto()));
await fs.mkdir(path.join(B,'restyle-layouts'),{recursive:true});
for(let i=0;i<slides.length;i++){
 const l=await slides[i].export({format:'layout'});await fs.writeFile(path.join(B,'restyle-layouts',`slide-${i+1}.json`),await l.text());
}
console.log('Exported 14 slides. Preserved all '+used.size+' text groups, 2 tables and 2 native charts.');
