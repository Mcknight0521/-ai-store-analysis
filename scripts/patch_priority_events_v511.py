from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
# Idempotent cleanup
for tag in ['priority-events-v511-css','priority-events-v511-js']:
 import re
 s=re.sub(rf'<style id="{tag}">.*?</style>','',s,flags=re.S)
 s=re.sub(rf'<script id="{tag}">.*?</script>','',s,flags=re.S)
css='''<style id="priority-events-v511-css">
#overview #externalEventPanel{margin-top:14px}
#overview .priority-v511{margin-top:14px}
.priority-v511 .pv-grid{display:grid;gap:9px}.priority-v511 .pv-row{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:10px;align-items:center;padding:12px;border:1px solid var(--line);border-radius:14px;background:#fff}.priority-v511 .pv-no{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;background:#f1f4f8;font-weight:950}.priority-v511 .pv-main b{display:block;font-size:12px}.priority-v511 .pv-main small{display:block;margin-top:4px;color:var(--muted);font-size:9px;line-height:1.45}.priority-v511 .pv-side{text-align:right}.priority-v511 .pv-side strong{display:block;font-size:12px}.priority-v511 .pv-badge{display:inline-block;margin-top:4px;padding:4px 7px;border-radius:999px;font-size:8px;font-weight:950}.pv-critical{background:#feecec;color:#c83434}.pv-high{background:#fff0df;color:#a95800}.pv-mid{background:#fff8d9;color:#8a6a00}.pv-low{background:#eaf8f0;color:#17754f}.priority-v511 .pv-rule{margin-top:10px;padding:11px 12px;border-radius:12px;background:#f7f9fc;color:#667085;font-size:9px;line-height:1.55}
</style>'''
js='''<script id="priority-events-v511-js">
(function(){
 function thresholds(){try{return JSON.parse(localStorage.getItem('opsAnomalyThresholdsV58')||'null')}catch(e){return null}}
 function n(v){v=Number(v);return Number.isFinite(v)?v:0}
 function moneyV(v){return '$'+Math.round(n(v)).toLocaleString()}
 function renderPriority(){
  const host=document.getElementById('priorityV511'); if(!host)return;
  const rr=Array.isArray(window.rows)?window.rows:[]; if(!rr.length){host.innerHTML='<div class="empty">等待資料</div>';return}
  const t=thresholds(); const ct=t?Number(t.clearance)/100:null, wt=t?Number(t.waste)/100:null;
  const m=new Map(); rr.forEach(r=>{const k=String(r.item||r.sku||'未命名品項').trim();if(!m.has(k))m.set(k,{name:k,sales:0,clearance:0,waste:0});const x=m.get(k);x.sales+=n(r.sales);x.clearance+=n(r.clearance);x.waste+=n(r.waste)});
  let a=[...m.values()].map(x=>{x.loss=x.clearance+x.waste;x.lossRate=x.sales>0?x.loss/x.sales:0;x.cr=x.sales>0?x.clearance/x.sales:0;x.wr=x.sales>0?x.waste/x.sales:0;return x}).filter(x=>x.loss>0);
  const maxLoss=Math.max(...a.map(x=>x.loss),1);
  a.forEach(x=>{const impact=x.loss/maxLoss;const cex=ct&&ct>0?Math.max(0,x.cr/ct-1):0;const wex=wt&&wt>0?Math.max(0,x.wr/wt-1):0;const exceed=Math.min(1,Math.max(cex,wex)/2);const dual=(ct&&wt&&x.cr>ct&&x.wr>wt)?1:0;x.score=Math.round((impact*.5+exceed*.3+dual*.2)*100);if(x.score>=75)x.level='極高';else if(x.score>=50)x.level='高';else if(x.score>=25)x.level='中';else x.level='低';});
  a.sort((x,y)=>y.score-x.score||y.loss-x.loss); const cls={極高:'pv-critical',高:'pv-high',中:'pv-mid',低:'pv-low'};
  host.innerHTML='<div class="pv-grid">'+a.slice(0,5).map((x,i)=>`<div class="pv-row"><div class="pv-no">${i+1}</div><div class="pv-main"><b>${x.name.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}</b><small>損耗 ${moneyV(x.loss)}・損耗率 ${(x.lossRate*100).toFixed(2)}%・出清率 ${(x.cr*100).toFixed(2)}%・報廢率 ${(x.wr*100).toFixed(2)}%</small></div><div class="pv-side"><strong>${x.score} 分</strong><span class="pv-badge ${cls[x.level]}">${x.level}</span></div></div>`).join('')+'</div><div class="pv-rule">改善優先分數＝損耗金額影響 50%＋超標程度 30%＋出清與報廢同時超標 20%。率很高但金額很小的商品，不會自動排到最前面。損耗率＝（單品出清金額＋單品報廢金額）÷ 單品營業額。</div>';
 }
 function place(){
  const ov=document.getElementById('overview'); if(!ov)return;
  let box=document.getElementById('priorityPanelV511');
  if(!box){box=document.createElement('section');box.id='priorityPanelV511';box.className='panel priority-v511';box.innerHTML='<div class="panel-head"><div><div class="panel-kicker">IMPROVEMENT PRIORITY</div><h3>最需要改善的商品</h3><p>同時考慮損耗金額、超標程度與雙重異常，避免只看百分比。</p></div></div><div id="priorityV511"></div>';const grid=ov.querySelector('.overview-grid');grid?.insertAdjacentElement('afterend',box)}
  const ev=document.getElementById('externalEventPanel'); if(ev&&ev.parentElement!==ov)ov.appendChild(ev);
  renderPriority();
 }
 const old=window.renderAll;if(typeof old==='function')window.renderAll=function(){const r=old.apply(this,arguments);setTimeout(place,0);return r};
 document.addEventListener('DOMContentLoaded',place);setTimeout(place,0);
})();
</script>'''
s=s.replace('</head>',css+'</head>',1)
s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('patched priority/events v5.11')
