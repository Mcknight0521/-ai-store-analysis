from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add a dedicated loss split section before anomaly page.
needle='''    <section class="page" id="anomaly" data-page="anomaly">'''
block='''    <section class="panel loss-split-v49" id="lossSplitPanel">
      <div class="panel-head"><div><div class="panel-kicker">LOSS BREAKDOWN</div><h3>損耗拆解｜出清 vs 報廢</h3><p>期間率一律使用期間總金額 ÷ 期間總營業額；每日資料則依實際日期彙總，不平均百分比、不補缺值。</p></div></div>
      <div id="lossSplitSummary" class="metric-grid"><div class="empty">等待資料</div></div>
      <div class="table-wrap" style="margin-top:12px"><table><thead><tr><th>日期</th><th>營業額</th><th>出清金額</th><th>出清率</th><th>報廢金額</th><th>報廢率</th><th>總損耗</th></tr></thead><tbody id="lossDailyBody"><tr><td colspan="7">等待資料</td></tr></tbody></table></div>
      <div class="loss-top10-v49" style="margin-top:16px">
        <div class="panel-head"><div><div class="panel-kicker">INTERVAL TOP 10</div><h3>區間商品 Top 10</h3><p>同一商品跨整個報表期間加總後再排名。</p></div></div>
        <div class="segmented" id="lossTop10Switch" style="margin-bottom:12px">
          <button type="button" data-loss-top="sales" class="active">營業額</button><button type="button" data-loss-top="clearance">出清金額</button><button type="button" data-loss-top="waste">報廢金額</button><button type="button" data-loss-top="loss">總損耗</button><button type="button" data-loss-top="wasteRate">報廢率</button>
        </div>
        <div id="lossTop10List" class="rank-list"><div class="empty">等待資料</div></div>
      </div>
    </section>

'''
if 'id="lossSplitPanel"' not in s:
    if needle not in s: raise SystemExit('anomaly anchor not found')
    s=s.replace(needle,block+needle,1)

style='''
<style id="loss-split-v49-css">
.loss-split-v49{margin-top:12px}.loss-split-v49 .metric-grid{grid-template-columns:repeat(4,1fr)}
.loss-split-v49 .metric small{display:block;margin-top:5px;color:var(--muted);font-size:10px;line-height:1.4}
#lossTop10Switch{overflow:auto;max-width:100%;justify-content:flex-start}#lossTop10Switch button{white-space:nowrap}
.loss-top-row{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:10px;align-items:center;padding:11px;border:1px solid var(--line);border-radius:14px;background:#fff}.loss-top-rank{width:34px;height:34px;border-radius:11px;background:var(--navy);color:#fff;display:grid;place-items:center;font-size:11px;font-weight:900}.loss-top-main b{display:block;font-size:12px}.loss-top-main small{display:block;margin-top:4px;color:var(--muted);font-size:10px;line-height:1.4}.loss-top-value{text-align:right;font-size:13px;font-weight:900}
@media(max-width:760px){.loss-split-v49 .metric-grid{grid-template-columns:repeat(2,1fr)}.loss-top-row{grid-template-columns:30px minmax(0,1fr) auto;padding:9px}.loss-top-rank{width:30px;height:30px}.loss-top-main b{font-size:11px}.loss-top-main small{font-size:9px}.loss-top-value{font-size:11px}}
</style>
'''
if 'id="loss-split-v49-css"' not in s:s=s.replace('</head>',style+'</head>',1)

js='''
<script id="loss-split-v49-js">
(function(){
 let mode='sales';
 const rate=(n,d)=>n!=null&&d!=null&&Number(d)>0?Number(n)/Number(d):null;
 const val=(r,k)=>r[k]==null?null:Number(r[k]);
 const add=(a,b)=>b==null?a:(a??0)+Number(b);
 const dayKey=d=>{if(!(d instanceof Date)||isNaN(d))return null;const y=d.getFullYear(),m=String(d.getMonth()+1).padStart(2,'0'),dd=String(d.getDate()).padStart(2,'0');return `${y}-${m}-${dd}`};
 function itemRows(list){
   const m=new Map();
   list.forEach(r=>{const key=String(r.sku||r.item||'').trim();if(!key)return;if(!m.has(key))m.set(key,{name:r.item||r.sku||'未命名商品',sales:null,clearance:null,waste:null});const x=m.get(key);x.sales=add(x.sales,val(r,'sales'));x.clearance=add(x.clearance,val(r,'clearance'));x.waste=add(x.waste,val(r,'waste'))});
   return [...m.values()].map(x=>({...x,loss:(x.clearance==null&&x.waste==null)?null:(x.clearance??0)+(x.waste??0),wasteRate:rate(x.waste,x.sales),clearanceRate:rate(x.clearance,x.sales)}));
 }
 function render(){
   const list=Array.isArray(window.rows)?window.rows:[], summary=document.getElementById('lossSplitSummary'),body=document.getElementById('lossDailyBody'),box=document.getElementById('lossTop10List');if(!summary||!body||!box)return;
   if(!window.confirmed||!list.length){summary.innerHTML='<div class="empty">等待資料</div>';body.innerHTML='<tr><td colspan="7">等待資料</td></tr>';box.innerHTML='<div class="empty">等待資料</div>';return}
   let sales=null,clearance=null,waste=null;list.forEach(r=>{sales=add(sales,val(r,'sales'));clearance=add(clearance,val(r,'clearance'));waste=add(waste,val(r,'waste'))});const loss=(clearance==null&&waste==null)?null:(clearance??0)+(waste??0);
   const cr=rate(clearance,sales),wr=rate(waste,sales),lr=rate(loss,sales);
   summary.innerHTML=`<div class="metric"><span>總損耗率</span><strong>${lr==null?'無資料':pct(lr)}</strong><small>${maybeMoney(loss)} ÷ ${maybeMoney(sales)}</small></div><div class="metric"><span>出清率</span><strong>${cr==null?'無資料':pct(cr)}</strong><small>出清 ${maybeMoney(clearance)}</small></div><div class="metric"><span>報廢率</span><strong>${wr==null?'無資料':pct(wr)}</strong><small>報廢 ${maybeMoney(waste)}</small></div><div class="metric"><span>期間報廢金額</span><strong>${maybeMoney(waste)}</strong><small>只加總實際報廢欄位</small></div>`;
   const dm=new Map();list.forEach(r=>{const k=dayKey(r.date);if(!k)return;if(!dm.has(k))dm.set(k,{sales:null,clearance:null,waste:null});const x=dm.get(k);x.sales=add(x.sales,val(r,'sales'));x.clearance=add(x.clearance,val(r,'clearance'));x.waste=add(x.waste,val(r,'waste'))});
   body.innerHTML=[...dm].sort((a,b)=>a[0].localeCompare(b[0])).map(([d,x])=>{const l=(x.clearance==null&&x.waste==null)?null:(x.clearance??0)+(x.waste??0);return `<tr><td>${d.replaceAll('-','/')}</td><td>${maybeMoney(x.sales)}</td><td>${maybeMoney(x.clearance)}</td><td>${rate(x.clearance,x.sales)==null?'無資料':pct(rate(x.clearance,x.sales))}</td><td>${maybeMoney(x.waste)}</td><td>${rate(x.waste,x.sales)==null?'無資料':pct(rate(x.waste,x.sales))}</td><td>${maybeMoney(l)}</td></tr>`}).join('')||'<tr><td colspan="7">此報表只有期間彙總，沒有逐日資料；不強拆每日金額。</td></tr>';
   const all=itemRows(list);let ranked=all.filter(x=>x[mode]!=null);ranked.sort((a,b)=>(b[mode]??-Infinity)-(a[mode]??-Infinity));ranked=ranked.slice(0,10);
   const label={sales:'營業額',clearance:'出清金額',waste:'報廢金額',loss:'總損耗',wasteRate:'報廢率'}[mode];
   box.innerHTML=ranked.map((x,i)=>`<div class="loss-top-row"><div class="loss-top-rank">${i+1}</div><div class="loss-top-main"><b>${esc(x.name)}</b><small>營業額 ${maybeMoney(x.sales)} · 出清 ${maybeMoney(x.clearance)} · 報廢 ${maybeMoney(x.waste)} · 報廢率 ${x.wasteRate==null?'—':pct(x.wasteRate)}</small></div><div class="loss-top-value">${mode==='wasteRate'?pct(x.wasteRate):maybeMoney(x[mode])}<small style="display:block;color:var(--muted);font-size:9px;margin-top:3px">${label}</small></div></div>`).join('')||'<div class="empty">此指標沒有可排名的商品資料</div>';
 }
 document.addEventListener('click',e=>{const b=e.target.closest?.('[data-loss-top]');if(!b)return;mode=b.dataset.lossTop;document.querySelectorAll('[data-loss-top]').forEach(x=>x.classList.toggle('active',x===b));render()});
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);render()};
 document.addEventListener('DOMContentLoaded',render);setTimeout(render,0);
})();
</script>
'''
if 'id="loss-split-v49-js"' not in s:s=s.replace('</body>',js+'</body>',1)

p.write_text(s,encoding='utf-8')
print('patched v4.9: loss split, daily waste/clearance, interval Top 10')
