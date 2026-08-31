from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove prior injected analysis layout versions so this patch is repeatable.
for ident in ['analysis-order-v51-js','analysis-layout-v52-css','analysis-layout-v52-js','analysis-layout-v53-css','analysis-layout-v53-js']:
    s=re.sub(r'\n?<(script|style) id="'+re.escape(ident)+r'">.*?</\1>\n?', '\n', s, flags=re.S)

style=r'''
<style id="analysis-layout-v53-css">
#analysis .analysis-flow-v53{display:grid;gap:14px;margin-top:12px}
#analysis .analysis-section-v53{position:relative;border-radius:20px;border:1px solid var(--line);background:#fff;box-shadow:var(--shadow);overflow:hidden}
#analysis .analysis-section-v53>.analysis-section-label{display:flex;align-items:center;gap:10px;padding:14px 16px 4px;font-weight:950;letter-spacing:-.02em}
#analysis .analysis-section-label .n{width:30px;height:30px;border-radius:999px;display:grid;place-items:center;color:#fff;font-size:13px;flex:0 0 auto}
#analysis .analysis-section-label b{font-size:17px}
#analysis .analysis-section-v53>.panel{border:0;box-shadow:none;border-radius:0;margin:0;background:transparent}
#analysis .analysis-sales-v53{border-color:#cfe0ff;background:linear-gradient(180deg,#f7fbff,#fff)}
#analysis .analysis-sales-v53 .analysis-section-label{color:#2156b7}.analysis-sales-v53 .analysis-section-label .n{background:#2C64F1}
#analysis .analysis-clearance-v53{border-color:#cfe9dd;background:linear-gradient(180deg,#f7fcf9,#fff)}
#analysis .analysis-clearance-v53 .analysis-section-label{color:#16805B}.analysis-clearance-v53 .analysis-section-label .n{background:#16805B}
#analysis .analysis-waste-v53{border-color:#ffd9cf;background:linear-gradient(180deg,#fff9f7,#fff)}
#analysis .analysis-waste-v53 .analysis-section-label{color:#c64f31}.analysis-waste-v53 .analysis-section-label .n{background:#e85d3d}
#analysis .analysis-loss-v53{border-color:#d9e0ea;background:linear-gradient(180deg,#f8fafc,#fff)}
#analysis .analysis-loss-v53 .analysis-section-label{color:#475467}.analysis-loss-v53 .analysis-section-label .n{background:#52637a}
#analysis .topic-detail-v53{margin:8px 14px 14px;border:1px solid var(--line);border-radius:15px;background:#fff;overflow:hidden}
#analysis .topic-detail-toggle-v53{width:100%;border:0;background:#fff;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:12px;color:var(--ink);font-weight:900;font-size:12px}
#analysis .topic-detail-toggle-v53 .hint{font-size:10px;color:var(--muted);font-weight:800}
#analysis .topic-detail-body-v53{display:none;padding:0 12px 12px}
#analysis .topic-detail-v53.open .topic-detail-body-v53{display:block}
#analysis .topic-detail-v53 .chev{transition:.18s transform;font-size:13px;color:var(--muted)}
#analysis .topic-detail-v53.open .chev{transform:rotate(180deg)}
#analysis .topic-detail-v53 .table-wrap{max-height:420px;background:#fff}
#analysis .topic-detail-v53 table{font-size:9px}
#analysis .topic-detail-v53 th{font-size:8px}
#analysis .loss-top10-v49{margin-top:8px!important;padding-top:2px}
#analysis .legacy-analysis-detail-v53{display:none!important}
@media(max-width:760px){#analysis .analysis-section-v53>.analysis-section-label{padding:12px 13px 3px}#analysis .analysis-section-label b{font-size:15px}#analysis .analysis-section-label .n{width:27px;height:27px;font-size:12px}#analysis .topic-detail-v53{margin:7px 10px 11px}}
</style>
'''

js=r'''
<script id="analysis-layout-v53-js">
(function(){
 const money=v=>v==null||Number.isNaN(Number(v))?'—':new Intl.NumberFormat('zh-TW',{style:'currency',currency:'TWD',maximumFractionDigits:0}).format(Number(v));
 const num=v=>v==null||Number.isNaN(Number(v))?'—':new Intl.NumberFormat('zh-TW',{maximumFractionDigits:2}).format(Number(v));
 const pctv=(n,d)=>n!=null&&d!=null&&Number(d)>0?`${(Number(n)/Number(d)*100).toFixed(2)}%`:'—';
 const escv=v=>String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
 const datev=d=>d instanceof Date&&!isNaN(d)?`${d.getFullYear()}/${String(d.getMonth()+1).padStart(2,'0')}/${String(d.getDate()).padStart(2,'0')}`:'—';
 function closestPanel(el){return el ? (el.classList&&el.classList.contains('panel')?el:el.closest('.panel')) : null}
 function findPanelByText(page,re){return [...page.querySelectorAll('.panel')].find(p=>re.test((p.textContent||'').replace(/\s+/g,' ')))||null}
 function mkSection(kind,no,title){const sec=document.createElement('section');sec.className=`analysis-section-v53 analysis-${kind}-v53`;sec.dataset.kind=kind;sec.innerHTML=`<div class="analysis-section-label"><span class="n">${no}</span><b>${title}</b></div>`;return sec}
 function detailColumns(kind){
   if(kind==='sales')return [['日期',r=>datev(r.date)],['單品編號',r=>escv(r.sku||'—')],['商品名稱',r=>escv(r.item||r.sku||'—')],['營業額',r=>money(r.sales)],['銷售量',r=>num(r.qty)]];
   if(kind==='clearance')return [['日期',r=>datev(r.date)],['單品編號',r=>escv(r.sku||'—')],['商品名稱',r=>escv(r.item||r.sku||'—')],['營業額',r=>money(r.sales)],['出清金額',r=>money(r.clearance)],['出清率',r=>pctv(r.clearance,r.sales)]];
   if(kind==='waste')return [['日期',r=>datev(r.date)],['單品編號',r=>escv(r.sku||'—')],['商品名稱',r=>escv(r.item||r.sku||'—')],['營業額',r=>money(r.sales)],['報廢金額',r=>money(r.waste)],['報廢率',r=>pctv(r.waste,r.sales)]];
   return [['日期',r=>datev(r.date)],['單品編號',r=>escv(r.sku||'—')],['商品名稱',r=>escv(r.item||r.sku||'—')],['營業額',r=>money(r.sales)],['出清',r=>money(r.clearance)],['報廢',r=>money(r.waste)],['總損耗',r=>money((r.clearance==null&&r.waste==null)?null:(Number(r.clearance||0)+Number(r.waste||0)))]];
 }
 function rowsFor(kind){
   const list=Array.isArray(window.rows)?window.rows:[];
   if(kind==='sales')return list.filter(r=>r.sales!=null);
   if(kind==='clearance')return list.filter(r=>r.clearance!=null);
   if(kind==='waste')return list.filter(r=>r.waste!=null);
   return list.filter(r=>r.clearance!=null||r.waste!=null);
 }
 function renderDetail(box,kind){
   const body=box.querySelector('.topic-detail-body-v53');if(!body)return;
   const cols=detailColumns(kind),list=rowsFor(kind);
   if(!list.length){body.innerHTML='<div class="empty">此分類目前沒有可顯示的明細資料</div>';return}
   body.innerHTML=`<div class="table-wrap"><table><thead><tr>${cols.map(c=>`<th>${c[0]}</th>`).join('')}</tr></thead><tbody>${list.map(r=>`<tr>${cols.map(c=>`<td>${c[1](r)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
 }
 function addDetail(sec,kind,title){
   let box=sec.querySelector(`.topic-detail-v53[data-detail="${kind}"]`);
   if(!box){
     box=document.createElement('div');box.className='topic-detail-v53';box.dataset.detail=kind;
     box.innerHTML=`<button type="button" class="topic-detail-toggle-v53" aria-expanded="false"><span>${title}</span><span class="hint">查看明細 <span class="chev">⌄</span></span></button><div class="topic-detail-body-v53"></div>`;
     sec.appendChild(box);
     box.querySelector('button').addEventListener('click',()=>{const open=box.classList.toggle('open');box.querySelector('button').setAttribute('aria-expanded',open?'true':'false');if(open)renderDetail(box,kind)});
   }
   if(box.classList.contains('open'))renderDetail(box,kind);
 }
 function apply(){
   const page=document.getElementById('analysis');if(!page)return;
   const toolbar=page.querySelector('.toolbar');
   let flow=page.querySelector('.analysis-flow-v53');
   if(!flow){flow=document.createElement('div');flow.className='analysis-flow-v53';if(toolbar)toolbar.after(flow);else page.appendChild(flow)}

   const sales=closestPanel(page.querySelector('.top10-sales-panel'))||closestPanel(page.querySelector('#salesTop10List'))||findPanelByText(page,/平日\s*\/\s*假日.*Top\s*10|SALES\s*TOP\s*10/i);
   const clearance=closestPanel(page.querySelector('#clearanceRateSummary'))||findPanelByText(page,/出清率分析|出清.*Top\s*10/i);
   const waste=document.getElementById('lossSplitPanel')||closestPanel(page.querySelector('#lossSplitSummary'));
   const loss=closestPanel(page.querySelector('#analysisBars'))||findPanelByText(page,/品項損耗排行|每日損耗趨勢|損耗總覽/i);
   if(!sales)return;

   flow.innerHTML='';
   const salesSec=mkSection('sales',1,'營業額分析');salesSec.appendChild(sales);flow.appendChild(salesSec);
   const intervalTop=page.querySelector('.loss-top10-v49');if(intervalTop){const salesPanel=salesSec.querySelector('.panel')||salesSec;const firstBody=[...salesPanel.children].find(x=>!x.classList.contains('panel-head')&&!x.classList.contains('interval-top10-notice'));if(firstBody)firstBody.before(intervalTop);else salesPanel.appendChild(intervalTop);const h=intervalTop.querySelector('h3');if(h)h.textContent='區間商品 Top 10'}
   addDetail(salesSec,'sales','銷售資料明細');

   if(clearance&&clearance!==sales){const sec=mkSection('clearance',2,'出清分析');sec.appendChild(clearance);flow.appendChild(sec);addDetail(sec,'clearance','出清資料明細')}
   if(waste&&waste!==sales&&waste!==clearance){const sec=mkSection('waste',3,'報廢分析');sec.appendChild(waste);flow.appendChild(sec);const h=waste.querySelector('.panel-head h3');if(h)h.textContent='報廢分析';const p=waste.querySelector('.panel-head p');if(p)p.textContent='檢視期間報廢金額、報廢率與每日報廢變化；不補缺值、不把缺少資料視為 0。';addDetail(sec,'waste','報廢資料明細')}
   if(loss&&loss!==sales&&loss!==clearance&&loss!==waste){const sec=mkSection('loss',4,'損耗總覽');sec.appendChild(loss);flow.appendChild(sec);addDetail(sec,'loss','損耗資料明細')}

   [...page.querySelectorAll('.panel')].filter(p=>/資料明細/.test(p.textContent||'')&&!p.closest('.analysis-section-v53')).forEach(p=>p.classList.add('legacy-analysis-detail-v53'));
 }
 document.addEventListener('DOMContentLoaded',()=>setTimeout(apply,0));
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);apply()};
 setTimeout(apply,120);
})();
</script>
'''

s=s.replace('</head>',style+'</head>',1)
s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('patched v5.3: per-topic collapsed details inside sales/clearance/waste/loss sections')
