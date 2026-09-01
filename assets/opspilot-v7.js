(()=>{
 document.body.classList.add('op-v7','op-v75');
 const SVG={
 executive:'<svg viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-7h6v7"/></svg>',
 overview:'<svg viewBox="0 0 24 24"><path d="M4 19V9"/><path d="M10 19V5"/><path d="M16 19v-7"/><path d="M22 19V8"/><path d="m3 7 6-4 6 6 6-5"/></svg>',
 analysis:'<svg viewBox="0 0 24 24"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/></svg>',
 anomaly:'<svg viewBox="0 0 24 24"><path d="M12 3 2.7 20h18.6L12 3Z"/><path d="M12 9v5"/><path d="M12 17.5h.01"/></svg>',
 improve:'<svg viewBox="0 0 24 24"><path d="M4 13l5 5L20 6"/><path d="M20 12v8H4V4h11"/></svg>',
 report:'<svg viewBox="0 0 24 24"><path d="M6 3h12v18H6z"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>'};
 const NAV={executive:'總覽',overview:'洞察',analysis:'分析',anomaly:'異常',improve:'改善',report:'報告'};
 function applyNav(){document.querySelectorAll('.bottom-nav [data-page]').forEach(el=>{const k=el.dataset.page;if(SVG[k]){const s=el.querySelector('svg');if(s&&!s.dataset.v75)s.outerHTML=SVG[k].replace('<svg ','<svg data-v75="1" ')}const span=el.querySelector('span');if(span&&NAV[k])span.textContent=NAV[k]})}
 function applyPageLabels(){
   const exec=document.querySelector('#executive .page-head');
   if(exec){const e=exec.querySelector('.eyebrow'),h=exec.querySelector('h1'),p=exec.querySelector('p');if(e)e.textContent='OPERATIONS OVERVIEW';if(h)h.textContent='總覽';if(p)p.textContent='本期結果、關鍵影響與需要優先注意的營運項目。'}
   const insight=document.querySelector('#overview .page-head');
   if(insight){const e=insight.querySelector('.eyebrow'),h=insight.querySelector('h1'),p=insight.querySelector('p');if(e)e.textContent='INSIGHTS';if(h)h.textContent='洞察';if(p)p.textContent='從本期數字看營運結構與目前最值得注意的變化。'}
 }
 function decorate(){document.querySelectorAll('.kpi,.metric,.mini-card,.v522-card').forEach((e,i)=>{if(!e.dataset.skinTone)e.dataset.skinTone=['blue','green','amber','violet','rose','cyan'][i%6]})}
 function orderInsight(){const p=document.getElementById('overview');if(!p)return;const struct=p.querySelector('.v522-insight-structure');if(!struct)return;const result=[...p.querySelectorAll('section,.panel,.exec-v513')].find(e=>/本期營運結果|PERIOD RESULT/.test(e.textContent||''));if(result&&result.nextElementSibling!==struct)result.after(struct)}
 function run(){applyNav();applyPageLabels();decorate();orderInsight()}
 run();new MutationObserver(()=>requestAnimationFrame(run)).observe(document.body,{subtree:true,childList:true});
})();
