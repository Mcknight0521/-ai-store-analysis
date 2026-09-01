(()=>{
 document.body.classList.add('op-v7');
 const SVG={
 executive:'<svg viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-7h6v7"/></svg>',
 overview:'<svg viewBox="0 0 24 24"><path d="M4 19V9"/><path d="M10 19V5"/><path d="M16 19v-7"/><path d="M22 19V8"/><path d="m3 7 6-4 6 6 6-5"/></svg>',
 analysis:'<svg viewBox="0 0 24 24"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/></svg>',
 anomaly:'<svg viewBox="0 0 24 24"><path d="M12 3 2.7 20h18.6L12 3Z"/><path d="M12 9v5"/><path d="M12 17.5h.01"/></svg>',
 improve:'<svg viewBox="0 0 24 24"><path d="M4 13l5 5L20 6"/><path d="M20 12v8H4V4h11"/></svg>',
 report:'<svg viewBox="0 0 24 24"><path d="M6 3h12v18H6z"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>'};
 function icons(){document.querySelectorAll('[data-page]').forEach(el=>{const k=el.dataset.page;if(!SVG[k])return;const s=el.querySelector('svg');if(s)s.outerHTML=SVG[k]})}
 function orderInsight(){const p=document.getElementById('overview');if(!p)return;const struct=p.querySelector('.v522-insight-structure');if(!struct)return;const result=[...p.querySelectorAll('section,.panel,.exec-v513')].find(e=>/本期營運結果|PERIOD RESULT/.test(e.textContent||''));if(result&&result.nextElementSibling!==struct)result.after(struct)}
 function strengthenCopy(){document.querySelectorAll('.page-head p,.panel-head p,.ar519-title small').forEach(e=>{e.style.maxWidth='760px'})}
 function run(){icons();orderInsight();strengthenCopy()}run();setInterval(run,900);
})();
