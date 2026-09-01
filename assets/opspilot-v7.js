(()=>{
  document.body.classList.remove('op-v8','op-v9','op-v10','op-v11','v10-empty','v10-has-data');
  document.body.classList.add('op-ref');
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const ICONS={executive:'<svg viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-7h6v7"/></svg>',overview:'<svg viewBox="0 0 24 24"><path d="M4 19V9"/><path d="M10 19V5"/><path d="M16 19v-7"/><path d="M22 19V8"/><path d="m3 7 6-4 6 6 6-5"/></svg>',analysis:'<svg viewBox="0 0 24 24"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/></svg>',anomaly:'<svg viewBox="0 0 24 24"><path d="M12 3 2.7 20h18.6L12 3Z"/><path d="M12 9v5"/><path d="M12 17.5h.01"/></svg>',improve:'<svg viewBox="0 0 24 24"><path d="M4 13l5 5L20 6"/><path d="M20 12v8H4V4h11"/></svg>',report:'<svg viewBox="0 0 24 24"><path d="M6 3h12v18H6z"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>'};
  const META={executive:['總覽','PERIOD RESULT','本期結果與最值得注意的營運項目。'],overview:['洞察','INSIGHTS','看懂營運結構與變化，再往下追原因。'],analysis:['分析','ANALYSIS','營業額、出清與報廢的結構拆解。'],anomaly:['異常','ANOMALY','辨識超標項目，不把排序當成根因。'],improve:['改善','IMPROVEMENT','把值得先處理的異常轉成可驗證行動。'],report:['報告','REPORT','把本期判斷整理成可分享的管理摘要。']};
  const tones=['blue','green','amber','rose','violet','cyan'];
  function cleanup(){ $('#v10Landing')?.remove();$('#v9Landing')?.remove();document.body.classList.remove('v10-empty','v10-has-data'); }
  function nav(){ $$('.bottom-nav [data-page]').forEach(el=>{const k=el.dataset.page;if(!META[k])return;let svg=$('svg',el);if(svg&&!svg.dataset.opref)svg.outerHTML=ICONS[k].replace('<svg ','<svg data-opref="1" ');let t=$('span',el);if(t)t.textContent=META[k][0];}); }
  function heads(){ Object.entries(META).forEach(([id,[title,eyebrow,desc]])=>{let h=$(`#${id}>.page-head`);if(!h)return;let e=$('.eyebrow',h),t=$('h1',h),p=$('p',h);if(e)e.textContent=eyebrow;if(t)t.textContent=title;if(p)p.textContent=desc;}); }
  function tone(nodes){nodes.forEach((el,i)=>el.dataset.opTone=tones[i%tones.length]);}
  function decorate(){tone($$('#executive .ex513-kpi'));$$('#executive .ex513-card').forEach((el,i)=>el.dataset.opTone=['blue','amber','rose','violet'][i%4]);tone($$('#overview .metric'));$$('#analysis .analysis-v57-card').forEach((el,i)=>el.dataset.opTone=['blue','amber','rose'][i%3]);$$('#anomaly .ar519-panel').forEach((el,i)=>el.dataset.opTone=i===0?'rose':tones[(i+1)%tones.length]);tone($$('#improve .improve-stat'));}
  function numberFrom(text){let s=(text||'').replace(/,/g,'').replace(/[^0-9.\-]/g,'');let n=parseFloat(s);return Number.isFinite(n)?Math.abs(n):0;}
  function analysisStructure(){
    $$('#analysis .analysis-v57-card').forEach(card=>{
      const body=$('.analysis-v57-body',card);if(!body)return;
      [...body.querySelectorAll(':scope > .v57-sub')].forEach(sub=>{let h=$('h4',sub);if(h&&/改善優先度/.test(h.textContent||''))sub.dataset.opPriority='1';});
      if(!body.querySelector(':scope > .op-analysis-grid')){
        const grid=document.createElement('div');grid.className='op-analysis-grid';
        [...body.children].forEach(ch=>grid.appendChild(ch));body.appendChild(grid);
      }
      $$('.v57-rank',body).forEach(rank=>{
        const rows=$$('.v57-row',rank), vals=rows.map(r=>numberFrom($('.v57-value',r)?.textContent));const max=Math.max(1,...vals);
        rows.forEach((row,i)=>{let main=$('.v57-main',row);if(!main)return;let p=$('.op-rank-progress',main);if(!p){p=document.createElement('div');p.className='op-rank-progress';p.innerHTML='<i></i>';main.appendChild(p);}let fill=$('i',p);if(fill)fill.style.width=Math.max(5,Math.min(100,(vals[i]/max)*100))+'%';});
      });
    });
  }
  function run(){cleanup();nav();heads();decorate();analysisStructure();}
  run();let scheduled=false;new MutationObserver(()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(()=>{scheduled=false;run();});}).observe(document.body,{subtree:true,childList:true,characterData:true});
})();
