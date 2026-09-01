from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='opspilot-ui-v521'
if MARK in s:
    print('v5.21 already applied')
    raise SystemExit

css=r'''<style id="opspilot-ui-v521">
:root{--v521-blue:#2C64F1;--v521-amber:#A96A10;--v521-red:#C83D3D;--v521-green:#16805B;--v521-line:#E4EAF1;--v521-soft:#F7F9FC}
/* One visual system: restrained surfaces, shared radius/spacing/shadows. */
.panel,.exec-v513 .card,.anomaly-rank-v519 .ar-card,.analysis-safe-v57 .as57-card{border-color:var(--v521-line)!important;border-radius:18px!important;box-shadow:0 7px 24px rgba(18,29,45,.055)!important}
.rank-item,.metric,.mini-card,.anomaly-rank-v519 .ar-item,.analysis-safe-v57 .as57-item{border-color:var(--v521-line)!important;border-radius:13px!important}
.page-head h1{letter-spacing:-.04em}.panel-head h3{letter-spacing:-.02em}
/* Semantic accents only; no decorative rainbow blocks. */
[data-tone="sales"]{--tone:var(--v521-blue)}[data-tone="clearance"]{--tone:var(--v521-amber)}[data-tone="waste"]{--tone:var(--v521-red)}
.v521-accent{border-left:3px solid var(--tone,var(--v521-blue))!important}
/* Insight 2.0 */
#overview .v521-insights{display:grid;gap:12px;margin:0 0 12px}
.v521-diagnosis{padding:18px 19px;border:1px solid var(--v521-line);border-radius:18px;background:linear-gradient(110deg,#fff 0%,#F8FAFD 100%);box-shadow:0 7px 24px rgba(18,29,45,.05)}
.v521-kicker{font-size:8px;font-weight:900;letter-spacing:.15em;color:var(--v521-blue)}
.v521-diagnosis h3{font-size:17px;margin:6px 0 5px}.v521-diagnosis p{font-size:11px;line-height:1.65;color:#59677A;margin:0}
.v521-insight-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.v521-insight-card{padding:14px 15px;background:#fff;border:1px solid var(--v521-line);border-radius:16px;min-width:0}
.v521-insight-card b{display:block;font-size:12px;margin-bottom:5px}.v521-insight-card p{margin:0;color:#667085;font-size:10px;line-height:1.55}.v521-insight-card .v521-mark{width:28px;height:3px;border-radius:99px;margin-bottom:10px;background:var(--tone)}
/* Bottom nav icon system */
.bottom-nav button svg,.bottom-nav .nav-item svg,nav button svg{stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
@media(max-width:700px){.v521-insight-grid{grid-template-columns:1fr}.v521-diagnosis{padding:15px}}
</style>'''

js=r'''<script id="opspilot-ui-v521">
(()=>{
 const SVG={
  executive:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-7h6v7"/></svg>',
  overview:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19V9"/><path d="M10 19V5"/><path d="M16 19v-7"/><path d="M22 19V8"/><path d="m3 7 6-4 6 6 6-5"/></svg>',
  analysis:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/></svg>',
  anomaly:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2.7 20h18.6L12 3Z"/><path d="M12 9v5"/><path d="M12 17.5h.01"/></svg>',
  improve:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 13l5 5L20 6"/><path d="M20 12v8H4V4h11"/></svg>'
 };
 function navIcons(){
  document.querySelectorAll('[data-page]').forEach(el=>{
   const k=el.dataset.page;if(!SVG[k])return;
   const svg=el.querySelector('svg'); if(svg) svg.outerHTML=SVG[k];
  });
 }
 function rows(){return Array.isArray(window.rows)?window.rows:[]}
 const num=(r,keys)=>{for(const k of keys){const v=Number(r&&r[k]);if(Number.isFinite(v))return v}return 0};
 function insight2(){
  const page=document.getElementById('overview');if(!page||page.querySelector('.v521-insights'))return;
  const a=rows();if(!a.length)return;
  let sales=0,clearance=0,waste=0;
  a.forEach(r=>{sales+=num(r,['sales','revenue','amount','營業額']);clearance+=num(r,['clearance','clearanceAmount','出清','出清金額']);waste+=num(r,['waste','wasteAmount','報廢','報廢金額'])});
  const cr=sales?clearance/sales:0, wr=sales?waste/sales:0, lr=sales?(clearance+waste)/sales:0;
  let t=null;try{t=JSON.parse(sessionStorage.getItem('opsAnomalyThresholdsV58')||'null')}catch{}
  const cOver=t&&Number(t.clearance)>0?cr>Number(t.clearance):false,wOver=t&&Number(t.waste)>0?wr>Number(t.waste):false;
  let headline='本期營運結構已整理完成';
  if(t) headline=cOver&&wOver?'出清與報廢同時超過本次警戒值':cOver?'本期主要壓力來自出清率':wOver?'本期主要壓力來自報廢率':'出清與報廢目前皆在本次警戒值內';
  const wrap=document.createElement('section');wrap.className='v521-insights';
  wrap.innerHTML=`<div class="v521-diagnosis"><div class="v521-kicker">營運診斷</div><h3>${headline}</h3><p>洞察頁先說明整體狀況，再把營業額、出清與報廢拆開看；詳細商品排名仍留在分析與異常頁，避免重複。</p></div><div class="v521-insight-grid"><article class="v521-insight-card" style="--tone:var(--v521-blue)"><div class="v521-mark"></div><b>營業額結構</b><p>本期營業額 ${money(sales)}。先確認主力商品是否穩定，再判讀損耗是否合理。</p></article><article class="v521-insight-card" style="--tone:var(--v521-amber)"><div class="v521-mark"></div><b>出清觀察</b><p>出清 ${money(clearance)}，出清率 ${pct(cr)}${t?'；'+(cOver?'高於':'未高於')+'本次警戒值':''}。</p></article><article class="v521-insight-card" style="--tone:var(--v521-red)"><div class="v521-mark"></div><b>報廢與總損耗</b><p>報廢 ${money(waste)}，報廢率 ${pct(wr)}；整體損耗率 ${pct(lr)}${t?'，'+(wOver?'報廢需優先注意':'報廢目前在標準內'):''}。</p></article></div>`;
  const head=page.querySelector('.page-head');(head?head.after(wrap):page.prepend(wrap));
 }
 function money(v){return '$'+Math.round(v||0).toLocaleString('zh-TW')}
 function pct(v){return ((v||0)*100).toFixed(2)+'%'}
 function top10Text(){
  document.querySelectorAll('#anomaly *').forEach(el=>{if(el.childNodes.length===1&&el.firstChild.nodeType===3&&/Top 20/i.test(el.textContent))el.textContent=el.textContent.replace(/Top 20/ig,'Top 10')});
 }
 function trimAnomaly(){
  const root=document.querySelector('#anomaly .anomaly-rank-v519');if(!root)return;
  root.querySelectorAll('.ar-section').forEach(sec=>{
   const title=sec.querySelector('h3,h2,.ar-title'); if(title&&/改善優先/.test(title.textContent))return;
   const items=[...sec.querySelectorAll('.ar-item')];items.slice(10).forEach(x=>x.style.display='none');
  });top10Text();
 }
 function run(){navIcons();insight2();trimAnomaly()}
 run();setInterval(run,700);
})();
</script>'''

# Make generated anomaly renderer canonical Top10 where possible.
s=s.replace(".slice(0,20)", ".slice(0,10)").replace("Top 20", "Top 10")
# Inject safely without moving/removing existing DOM.
if '</head>' in s:s=s.replace('</head>',css+'\n</head>',1)
if '</body>' in s:s=s.replace('</body>',js+'\n</body>',1)
else:s+=js
p.write_text(s,encoding='utf-8')
print('Applied v5.21 unified UI, Insights 2.0, icons, anomaly Top10')
