const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty=x=>esc(JSON.stringify(x,null,2));
let count=0;
async function api(path){const r=await fetch(path);if(!r.ok)throw Error(await r.text());return r.json();}
function query(){return new URLSearchParams({trajectory:$('trajectory').value,method:$('method').value,index:$('step').value||0});}
async function render(reset=false){try{if(reset)$('step').innerHTML='<option value="0">1</option>';const s=await api('/api/step?'+query());const selected=$('step').value||'0';count=s.completed_steps;$('step').innerHTML=Array.from({length:count},(_,i)=>`<option value="${i}">${i+1}</option>`).join('');$('step').value=selected;
 const last=s.agent.at(-1);$('time').textContent=s.time;$('progressText').textContent=`Checkpoint ${Number(selected)+1} of ${count} · ${s.method} · ${s.status}`;
 $('agent').innerHTML=`<p class="label">Current received observation</p><div class="observations">${esc(last?.frame.messages.filter(m=>m.role==='user').at(-1)?.content)}</div><p class="label">Queries and returned evidence</p><pre>${pretty(s.queries)}</pre><p class="label">Selections and bindings</p><pre>${pretty(last?.decision)}</pre><p class="label">Simulator receipts</p><pre>${pretty(s.execution_receipts)}</pre><details><summary>Full public frames and raw model attempts</summary><pre>${pretty({agent:s.agent,calls:s.model_attempts})}</pre></details>`;
 $('memory').innerHTML=Object.values(s.intentions).map(r=>`<details open><summary>${esc(r.action)} · v${r.version} · ${esc(r.status)}</summary><pre>${pretty(r)}</pre></details>`).join('')||'<p class="empty">No intention records are stored at this checkpoint.</p>';
 $('evaluator').textContent='Hidden until revealed.';$('notice').textContent='Showing saved artifacts; navigating makes no model calls.';
 const report=await api('/api/report');$('report').textContent=JSON.stringify(report.cases.filter(r=>r.trajectory===$('trajectory').value&&r.method===$('method').value),null,2);
 }catch(e){$('notice').textContent=e.message;}}
$('trajectory').onchange=()=>render(true);$('method').onchange=()=>render(true);$('step').onchange=()=>render();$('next').onclick=()=>{if(Number($('step').value)+1<count){$('step').value=String(Number($('step').value)+1);render();}};
$('reveal').onclick=async()=>{$('evaluator').innerHTML='<pre>'+pretty(await api('/api/evaluator?'+query()))+'</pre>';};
(async()=>{const c=await api('/api/catalog');$('modeBadge').textContent=c.mode==='LOCAL_MODEL'?'LOCAL MODEL':c.mode;$('boundary').textContent=c.source_mode==='MOCK'?'MOCK language fixtures verify software mechanics only. They are not measurements of model performance.':c.source_mode==='LOCAL_MODEL'?'Real local development model. This is an exposed smoke test, not the frozen OpenRouter evaluation.':'RECORDED genuine LIVE output. No new inference during replay.';$('trajectory').innerHTML=c.trajectories.map(t=>`<option>${esc(t)}</option>`).join('');$('method').innerHTML=c.methods.map(m=>`<option>${esc(m)}</option>`).join('');await render(true);})();
