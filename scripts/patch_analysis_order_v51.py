from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove only our injected analysis presentation layers. Never remove or rewrite the base analysis DOM.
for ident in [
    'analysis-layout-v55-css','analysis-layout-v55-js',
    'analysis-layout-v56-css','analysis-layout-v56-js',
    'analysis-safe-v57-css','analysis-safe-v57-js'
]:
    s = re.sub(r'\n?<(script|style) id="' + re.escape(ident) + r'">.*?</\1>\n?', '\n', s, flags=re.S)

style = r'''<style id="analysis-safe-v57-css">
#analysis .analysis-safe-v57{display:grid;gap:14px;margin-top:12px}
#analysis .analysis-safe-v57~.panel,#analysis .analysis-safe-v57~.analysis-layout,#analysis .analysis-safe-v57~.loss-top10-v49{display:none!important}
#analysis .analysis-v57-card{border:1px solid var(--line);border-radius:20px;background:#fff;box-shadow:var(--shadow);overflow:hidden}
#analysis .analysis-v57-head{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--line)}
#analysis .analysis-v57-no{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:13px;font-weight:950;flex:0 0 auto}
#analysis .analysis-v57-head b{font-size:17px;letter-spacing:-.02em}
#analysis .analysis-v57-head small{display:block;margin-top:3px;color:var(--muted);font-size:10px;font-weight:700}
#analysis .sales-v57{border-color:#cfe0ff}.sales-v57 .analysis-v57-head{color:#2156b7;background:#f7fbff}.sales-v57 .analysis-v57-no{background:#2C64F1}
#analysis .clearance-v57{border-color:#cfe9dd}.clearance-v57 .analysis-v57-head{color:#16805B;background:#f7fcf9}.clearance-v57 .analysis-v57-no{background:#16805B}
#analysis .waste-v57{border-color:#ffd9cf}.waste-v57 .analysis-v57-head{color:#c64f31;background:#fff9f7}.waste-v57 .analysis-v57-no{background:#e85d3d}
#analysis .loss-v57{border-color:#d9e0ea}.loss-v57 .analysis-v57-head{color:#475467;background:#f8fafc}.loss-v57 .analysis-v57-no{background:#52637a}
#analysis .interval-v57{border-color:#cfe0ff;background:linear-gradient(180deg,#f7fbff,#fff)}
#analysis .analysis-v57-body{padding:14px}
#analysis .v57-kpi{padding:14px;border:1px solid var(--line);border-radius:15px;background:#fff;margin-bottom:14px}
#analysis .v57-kpi span{display:block;color:var(--muted);font-size:10px;font-weight:800}
#analysis .v57-kpi strong{display:block;margin-top:5px;font-size:26px;letter-spacing:-.04em}
#analysis .v57-kpi small{display:block;margin-top:5px;color:var(--muted);font-size:10px}
#analysis .v57-sub{margin-top:16px}#analysis .v57-sub:first-child{margin-top:0}
#analysis .v57-sub h4{margin:0 0 9px;font-size:13px}.v57-note{color:var(--muted);font-size:10px;line-height:1.5;margin-top:-4px;margin-bottom:10px}
#analysis .v57-tabs{display:flex;gap:6px;overflow:auto;padding-bottom:2px;margin-bottom:11px}
#analysis .v57-tabs button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 10px;font-size:10px;font-weight:850;white-space:nowrap;color:#667085}
#analysis .v57-tabs button.active{background:var(--navy);color:#fff;border-color:var(--navy)}
#analysis .v57-rank{display:grid;gap:8px}
#analysis .v57-row{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:9px;align-items:center;padding:10px;border:1px solid var(--line);border-radius:13px;background:#fff}
#analysis .v57-rankno{width:30px;height:30px;border-radius:10px;background:#f2f5f9;display:grid;place-items:center;font-size:10px;font-weight:950}
#analysis .v57-main{min-width:0}.v57-main b{display:block;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.v57-main small{display:block;margin-top:3px;color:var(--muted);font-size:9px;line-height:1.35}
#analysis .v57-value{text-align:right;font-size:11px;font-weight:900;white-space:nowrap}.v57-score{display:block;color:var(--muted);font-size:8px;margin-top:2px}
#analysis .v57-detail{margin-top:16px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
#analysis .v57-detail>button{width:100%;border:0;background:#fff;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;font-size:11px;font-weight:900;color:var(--ink)}
#analysis .v57-detail-body{display:none;padding:0 10px 10px}.v57-detail.open .v57-detail-body{display:block}.v57-detail .table-wrap{max-height:420px}
#analysis .v57-empty{padding:16px;text-align:center;border:1px dashed #d8dee8;border-radius:13px;color:var(--muted);font-size:10px;background:#fafbfc}
@media(max-width:760px){#analysis .analysis-v57-head{padding:12px 13px}.analysis-v57-head b{font-size:15px!important}#analysis .analysis-v57-body{padding:11px}.v57-row{grid-template-columns:28px minmax(0,1fr) auto!important;padding:9px!important}.v57-rankno{width:28px!important;height:28px!important}}
</style>'''

js = r'''<script id="analysis-safe-v57-js">
(function(){
 const money=v=>v==null||Number.isNaN(Number(v))?'—':new Intl.NumberFormat('zh-TW',{style:'currency',currency:'TWD',maximumFractionDigits:0}).format(Number(v));
 const pct=v=>v==null||Number.isNaN(Number(v))?'—':(Number(v)*100).toFixed(2)+'%';
 const num=v=>v==null||Number.isNaN(Number(v))?'—':new Intl.NumberFormat('zh-TW',{maximumFractionDigits:2}).format(Number(v));
 const esc=v=>String(v??'—').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
 const list=()=>Array.isArray(window.rows)?window.rows:[];
 const add=(a,b)=>b==null?a:(a??0)+Number(b);
 const rate=(n,d)=>n!=null&&d!=null&&Number(d)>0?Number(n)/Number(d):null;
 function aggregate(){
   const m=new Map();
   list().forEach(r=>{const k=String(r.sku||r.item||'').trim();if(!k)return;if(!m.has(k))m.set(k,{sku:r.sku||'',name:r.item||r.sku||'未命名商品',sales:null,qty:null,clearance:null,waste:null});const x=m.get(k);x.sales=add(x.sales,r.sales);x.qty=add(x.qty,r.qty);x.clearance=add(x.clearance,r.clearance);x.waste=add(x.waste,r.waste)});
   return [...m.values()].map(x=>{const loss=(x.clearance==null&&x.waste==null)?null:(x.clearance??0)+(x.waste??0);return {...x,loss,clearanceRate:rate(x.clearance,x.sales),wasteRate:rate(x.waste,x.sales),lossRate:rate(loss,x.sales)}});
 }
 function totals(){let sales=null,clearance=null,waste=null;list().forEach(r=>{sales=add(sales,r.sales);clearance=add(clearance,r.clearance);waste=add(waste,r.waste)});const loss=(clearance==null&&waste==null)?null:(clearance??0)+(waste??0);return {sales,clearance,waste,loss,clearanceRate:rate(clearance,sales),wasteRate:rate(waste,sales),lossRate:rate(loss,sales)}}
 function rankData(key){return aggregate().filter(x=>x[key]!=null&&Number.isFinite(Number(x[key]))).sort((a,b)=>Number(b[key])-Number(a[key])).slice(0,10)}
 function rankHtml(data,key,isRate=false,extra=''){return data.length?`<div class="v57-rank">${data.map((x,i)=>`<div class="v57-row"><div class="v57-rankno">${i+1}</div><div class="v57-main"><b>${esc(x.name)}</b><small>營業額 ${money(x.sales)}${extra?` · ${extra.replace('{amount}',money(x[key])).replace('{rate}',pct(x[key]))}`:''}</small></div><div class="v57-value">${isRate?pct(x[key]):money(x[key])}</div></div>`).join('')}</div>`:'<div class="v57-empty">此指標目前沒有可排名的商品資料</div>'}
 function priority(kind){const amount=kind==='clearance'?'clearance':kind==='waste'?'waste':'loss',rateKey=kind==='clearance'?'clearanceRate':kind==='waste'?'wasteRate':'lossRate',a=aggregate().filter(x=>x[amount]!=null&&x[rateKey]!=null);if(!a.length)return[];const maxA=Math.max(1,...a.map(x=>Number(x[amount])||0)),maxR=Math.max(.000001,...a.map(x=>Number(x[rateKey])||0));return a.map(x=>({...x,priorityScore:.6*((Number(x[amount])||0)/maxA)+.4*((Number(x[rateKey])||0)/maxR)})).sort((a,b)=>b.priorityScore-a.priorityScore).slice(0,10)}
 function priorityHtml(kind){const amount=kind==='clearance'?'clearance':kind==='waste'?'waste':'loss',rateKey=kind==='clearance'?'clearanceRate':kind==='waste'?'wasteRate':'lossRate',a=priority(kind);return a.length?`<div class="v57-rank">${a.map((x,i)=>`<div class="v57-row"><div class="v57-rankno">${i+1}</div><div class="v57-main"><b>${esc(x.name)}</b><small>金額影響 ${money(x[amount])} · 比率 ${pct(x[rateKey])}</small></div><div class="v57-value">${Math.round(x.priorityScore*100)}<span class="v57-score">優先分數</span></div></div>`).join('')}</div>`:'<div class="v57-empty">需要同時有金額與營業額資料才能計算改善優先度</div>'}
 function details(kind){const rows=list().filter(r=>kind==='sales'?r.sales!=null:kind==='clearance'?r.clearance!=null:kind==='waste'?r.waste!=null:r.clearance!=null||r.waste!=null);if(!rows.length)return'<div class="v57-empty">此分類目前沒有明細資料</div>';return `<div class="table-wrap"><table><thead><tr><th>商品</th><th>營業額</th><th>出清</th><th>報廢</th><th>比率</th></tr></thead><tbody>${rows.map(r=>{const amount=kind==='clearance'?r.clearance:kind==='waste'?r.waste:(r.clearance==null&&r.waste==null?null:Number(r.clearance||0)+Number(r.waste||0)),rr=kind==='sales'?null:rate(amount,r.sales);return `<tr><td>${esc(r.item||r.sku)}</td><td>${money(r.sales)}</td><td>${money(r.clearance)}</td><td>${money(r.waste)}</td><td>${rr==null?'—':pct(rr)}</td></tr>`}).join('')}</tbody></table></div>`}
 function section(kind,no,title,subtitle,body){return `<section class="analysis-v57-card ${kind}-v57"><div class="analysis-v57-head"><span class="analysis-v57-no">${no}</span><div><b>${title}</b><small>${subtitle}</small></div></div><div class="analysis-v57-body">${body}</div></section>`}
 function detailBlock(kind,label){return `<div class="v57-detail" data-v57-detail="${kind}"><button type="button"><span>${label}</span><span>查看明細　⌄</span></button><div class="v57-detail-body"></div></div>`}
 function intervalBlock(){const tabs=[['sales','營業額'],['clearance','出清金額'],['waste','報廢金額'],['loss','總損耗'],['wasteRate','報廢率']],active=window.__v57IntervalTab||'sales';return `<section class="analysis-v57-card interval-v57"><div class="analysis-v57-head"><div><b>區間商品 Top 10</b><small>完整保留所有區間排行分頁</small></div></div><div class="analysis-v57-body"><div class="v57-tabs">${tabs.map(([k,l])=>`<button type="button" data-v57-tab="${k}" class="${k===active?'active':''}">${l}</button>`).join('')}</div><div id="v57IntervalRank">${rankHtml(rankData(active),active,active.endsWith('Rate'))}</div></div></section>`}
 function render(){const page=document.getElementById('analysis');if(!page)return;let flow=page.querySelector('.analysis-safe-v57');if(!flow){flow=document.createElement('div');flow.className='analysis-safe-v57';const toolbar=page.querySelector('.toolbar');toolbar?toolbar.after(flow):page.appendChild(flow)}const t=totals();
   const salesBody=`<div class="v57-kpi"><span>期間營業額</span><strong>${money(t.sales)}</strong><small>依匯入資料實際營業額加總</small></div><div class="v57-sub"><h4>營業額 Top 10</h4>${rankHtml(rankData('sales'),'sales')}</div>${detailBlock('sales','銷售資料明細')}`;
   const clearanceBody=`<div class="v57-kpi"><span>總出清率</span><strong>${t.clearanceRate==null?'無資料':pct(t.clearanceRate)}</strong><small>${money(t.clearance)} ÷ ${money(t.sales)}</small></div><div class="v57-sub"><h4>出清金額 Top 10</h4>${rankHtml(rankData('clearance'),'clearance')}</div><div class="v57-sub"><h4>出清率 Top 10</h4>${rankHtml(rankData('clearanceRate'),'clearanceRate',true)}</div><div class="v57-sub"><h4>改善優先度</h4><div class="v57-note">同時考慮金額影響 60%＋比率 40%，避免只看金額或只看百分比。</div>${priorityHtml('clearance')}</div>${detailBlock('clearance','出清資料明細')}`;
   const wasteBody=`<div class="v57-kpi"><span>總報廢率</span><strong>${t.wasteRate==null?'無資料':pct(t.wasteRate)}</strong><small>${money(t.waste)} ÷ ${money(t.sales)}</small></div><div class="v57-sub"><h4>報廢金額 Top 10</h4>${rankHtml(rankData('waste'),'waste')}</div><div class="v57-sub"><h4>報廢率 Top 10</h4>${rankHtml(rankData('wasteRate'),'wasteRate',true)}</div><div class="v57-sub"><h4>改善優先度</h4><div class="v57-note">同時考慮金額影響 60%＋比率 40%。</div>${priorityHtml('waste')}</div>${detailBlock('waste','報廢資料明細')}`;
   const lossBody=`<div class="v57-kpi"><span>總損耗率</span><strong>${t.lossRate==null?'無資料':pct(t.lossRate)}</strong><small>${money(t.loss)} ÷ ${money(t.sales)}；損耗＝出清＋報廢</small></div><div class="v57-sub"><h4>損耗金額 Top 10</h4>${rankHtml(rankData('loss'),'loss')}</div><div class="v57-sub"><h4>損耗率 Top 10</h4>${rankHtml(rankData('lossRate'),'lossRate',true)}</div><div class="v57-sub"><h4>改善優先度</h4><div class="v57-note">同時考慮金額影響 60%＋比率 40%。</div>${priorityHtml('loss')}</div>${detailBlock('loss','損耗資料明細')}`;
   flow.innerHTML=intervalBlock()+section('sales',1,'營業額分析','先看營業結構，再往下看出清、報廢與總損耗。',salesBody)+section('clearance',2,'出清分析','總出清率 → 金額 Top 10 → 出清率 Top 10 → 改善優先度 → 明細',clearanceBody)+section('waste',3,'報廢分析','總報廢率 → 金額 Top 10 → 報廢率 Top 10 → 改善優先度 → 明細',wasteBody)+section('loss',4,'損耗分析','總損耗率 → 金額 Top 10 → 損耗率 Top 10 → 改善優先度 → 明細',lossBody);
 }
 document.addEventListener('click',e=>{const tab=e.target.closest?.('[data-v57-tab]');if(tab){window.__v57IntervalTab=tab.dataset.v57Tab;render();return}const btn=e.target.closest?.('.v57-detail>button');if(!btn)return;const box=btn.closest('.v57-detail'),kind=box.dataset.v57Detail,open=box.classList.toggle('open');btn.lastElementChild.textContent=open?'收合　⌃':'查看明細　⌄';if(open&&!box.dataset.loaded){box.querySelector('.v57-detail-body').innerHTML=details(kind);box.dataset.loaded='1'}});
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);render()};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(render,0));else setTimeout(render,0);setTimeout(render,120);
})();</script>'''

s = s.replace('</head>', style + '</head>', 1)
s = s.replace('</body>', js + '</body>', 1)
p.write_text(s, encoding='utf-8')
print('v5.7 safe analysis renderer deployed; base DOM preserved')
