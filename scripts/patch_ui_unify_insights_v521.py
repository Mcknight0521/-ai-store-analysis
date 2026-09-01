from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='opspilot-product-ui-v522'
if MARK in s:
    print('v5.22 already applied'); raise SystemExit

css=r'''<style id="opspilot-product-ui-v522">
:root{--op-blue:#315FE8;--op-blue-soft:#F1F5FF;--op-amber:#A96A10;--op-amber-soft:#FFF8E9;--op-red:#C94B47;--op-red-soft:#FFF2F1;--op-green:#16805B;--op-ink:#111827;--op-muted:#65738A;--op-line:#DFE6EF;--op-page:#F4F7FB}
body{background:var(--op-page)!important;color:var(--op-ink)}
.panel,.exec-v513 .card,.anomaly-rank-v519 .ar-card,.analysis-safe-v57 .as57-card{border:1px solid var(--op-line)!important;border-radius:20px!important;box-shadow:0 8px 28px rgba(22,34,51,.055)!important;background:#fff}
.page-head h1,.panel-head h3{letter-spacing:-.025em}.sub,.muted,.hint,.desc,.ar-sub,.exec-v513 .sub{color:var(--op-muted)!important}
/* stronger mobile typography */
@media(max-width:700px){body{font-size:16px}.panel p,.panel .sub,.panel .muted,.exec-v513 .sub,.anomaly-rank-v519 .ar-sub{font-size:13px!important;line-height:1.55!important}.rank-item small,.anomaly-rank-v519 .ar-item small,.analysis-safe-v57 small{font-size:12px!important;line-height:1.45!important}.panel-head h3,.anomaly-rank-v519 h3{font-size:21px!important}}
/* restrained product accents */
.v522-result{border-top:3px solid var(--op-blue)!important}.v522-structure{background:linear-gradient(145deg,#fff 0%,#F8FAFE 100%)!important}
/* distinguish management priority from anomaly detection */
#anomaly .anomaly-rank-v519 .ar-section:first-of-type .ar-item{border-left:4px solid var(--op-red)!important;background:linear-gradient(100deg,#FFF9F8 0%,#fff 32%)!important}
#anomaly .anomaly-rank-v519 .ar-section:not(:first-of-type) .ar-item{border-left:0!important;background:#fff!important}
#anomaly .anomaly-rank-v519 .ar-section:not(:first-of-type) .ar-item:nth-child(-n+4){background:linear-gradient(100deg,#FAFBFD,#fff)!important}
/* labels */
#anomaly .ar-tag{border-radius:999px!important;font-weight:800!important}
/* insight order + hierarchy */
#overview .v522-insight-structure{display:grid;gap:12px;margin:12px 0}.v522-structure-head{padding:18px 19px;border:1px solid var(--op-line);border-radius:20px;background:linear-gradient(135deg,#fff,#F5F8FF);box-shadow:0 8px 28px rgba(22,34,51,.045)}.v522-eyebrow{font-size:11px;font-weight:900;letter-spacing:.12em;color:var(--op-blue);margin-bottom:7px}.v522-structure-head h3{margin:0 0 7px;font-size:21px}.v522-structure-head p{margin:0;font-size:13px;line-height:1.6;color:var(--op-muted)}.v522-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.v522-card{background:#fff;border:1px solid var(--op-line);border-radius:17px;padding:15px}.v522-card i{display:block;width:30px;height:3px;border-radius:9px;margin-bottom:10px}.v522-card b{display:block;font-size:15px;margin-bottom:5px}.v522-card p{font-size:13px;line-height:1.5;margin:0;color:var(--op-muted)}
@media(max-width:700px){.v522-grid{grid-template-columns:1fr}.v522-structure-head{padding:17px}.v522-card{padding:16px}.v522-card b{font-size:16px}.v522-card p{font-size:14px}}
</style>'''
js=r'''<script id="opspilot-product-ui-v522">
(()=>{
 const n=(r,ks)=>{for(const k of ks){const v=Number(r&&r[k]);if(Number.isFinite(v))return v}return 0},money=v=>'$'+Math.round(v||0).toLocaleString('zh-TW'),pct=v=>((v||0)*100).toFixed(2)+'%';
 function structure(){const page=document.getElementById('overview');if(!page||page.querySelector('.v522-insight-structure')||!Array.isArray(window.rows)||!window.rows.length)return;let sales=0,c=0,w=0;window.rows.forEach(r=>{sales+=n(r,['sales','revenue','amount','營業額']);c+=n(r,['clearance','clearanceAmount','出清','出清金額']);w+=n(r,['waste','wasteAmount','報廢','報廢金額'])});const cr=sales?c/sales:0,wr=sales?w/sales:0,lr=sales?(c+w)/sales:0;let t=null;try{t=JSON.parse(sessionStorage.getItem('opsAnomalyThresholdsV58')||'null')}catch{};const co=t&&+t.clearance>0&&cr>+t.clearance,wo=t&&+t.waste>0&&wr>+t.waste;let title='本期營運結構';if(t)title=co&&wo?'出清與報廢皆需關注':co?'本期主要壓力來自出清':wo?'本期主要壓力來自報廢':'本期損耗結構在警戒標準內';const x=document.createElement('section');x.className='v522-insight-structure';x.innerHTML=`<div class="v522-structure-head"><div class="v522-eyebrow">OPERATING STRUCTURE</div><h3>${title}</h3><p>在本期營運結果之後，進一步拆解營業額、出清與報廢結構；商品層級問題再到分析與異常頁追查。</p></div><div class="v522-grid"><article class="v522-card"><i style="background:var(--op-blue)"></i><b>營業額結構</b><p>${money(sales)}｜先確認主力商品與營收集中度。</p></article><article class="v522-card"><i style="background:var(--op-amber)"></i><b>出清觀察</b><p>${money(c)}｜出清率 ${pct(cr)}${t?'｜'+(co?'超過':'未超過')+'警戒值':''}</p></article><article class="v522-card"><i style="background:var(--op-red)"></i><b>報廢與損耗</b><p>${money(w)}｜報廢率 ${pct(wr)}｜總損耗率 ${pct(lr)}</p></article></div>`;
 // Result first: insert structure after the existing Period Result panel when identifiable.
 const candidates=[...page.querySelectorAll('.panel,section,.exec-v513')];const result=candidates.find(e=>/本期營運結果|PERIOD RESULT/.test(e.textContent||''));if(result)result.after(x);else page.append(x);
 // Remove only our previous v5.21 insight presentation, never native DOM.
 const old=page.querySelector('.v521-insights');if(old)old.style.display='none';
 }
 function anomalySemantics(){const root=document.querySelector('#anomaly .anomaly-rank-v519');if(!root)return;const secs=[...root.querySelectorAll('.ar-section')];secs.forEach(sec=>{const h=sec.querySelector('h2,h3,.ar-title');if(!h)return;if(/改善優先/.test(h.textContent)){const sub=sec.querySelector('.ar-sub,p');if(sub)sub.textContent='管理優先度｜先確認異常，再依金額影響 60%＋超標程度 30%＋雙重異常 10% 排序。';}else if(/出清率超標/.test(h.textContent)){const sub=sec.querySelector('.ar-sub,p');if(sub)sub.textContent='異常偵測｜依出清率超過本次警戒值的程度排序，小金額高比率商品仍會保留。';}else if(/報廢率超標/.test(h.textContent)){const sub=sec.querySelector('.ar-sub,p');if(sub)sub.textContent='異常偵測｜依報廢率超過本次警戒值的程度排序。';}else if(/損耗率超標/.test(h.textContent)){const sub=sec.querySelector('.ar-sub,p');if(sub)sub.textContent='異常偵測｜用出清＋報廢的整體損耗觀察異常，不等同改善優先度。';}})}
 function run(){structure();anomalySemantics()}run();setInterval(run,700);
})();
</script>'''
s=s.replace('Top 20','Top 10').replace('.slice(0,20)','.slice(0,10)')
s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('</body>',js+'\n</body>',1) if '</body>' in s else s+js
p.write_text(s,encoding='utf-8')
print('Applied OpsPilot product UI v5.22')
