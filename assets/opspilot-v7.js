(()=>{
  document.body.classList.remove('op-v8','op-v9','op-v10','op-v11','op-ref','v10-empty','v10-has-data');
  document.body.classList.add('opx');
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const ICONS={
    sales:'<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v5c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 10v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/></svg>',
    chart:'<svg viewBox="0 0 24 24"><path d="M5 19V11M12 19V5M19 19v-8"/></svg>',
    qty:'<svg viewBox="0 0 24 24"><path d="M4 7h16l-2 9H7L4 4H2"/><circle cx="9" cy="19" r="1"/><circle cx="17" cy="19" r="1"/></svg>',
    waste:'<svg viewBox="0 0 24 24"><path d="M7 7h10l-1 13H8L7 7Z"/><path d="M5 7h14M9 7V4h6v3M10 10v6M14 10v6"/></svg>',
    clear:'<svg viewBox="0 0 24 24"><path d="M4 7v5l8 8 8-8-8-8H7a3 3 0 0 0-3 3Z"/><circle cx="8" cy="8" r="1"/></svg>',
    people:'<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2"/><path d="M3 19c.6-3.4 2.6-5 6-5s5.4 1.6 6 5M15 14c2.8.1 4.5 1.6 5 4"/></svg>',
    file:'<svg viewBox="0 0 24 24"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v5h5M10 12h5M10 16h5"/></svg>'
  };
  const TONES=['blue','green','amber','rose','violet','teal'];
  function txt(sel,root=document){return ($(sel,root)?.textContent||'').trim()}
  function num(s){const n=parseFloat((s||'').replace(/,/g,'').replace(/[^0-9.\-]/g,''));return Number.isFinite(n)?Math.abs(n):0}
  function iconFor(label){if(/報廢/.test(label))return ICONS.waste;if(/出清/.test(label))return ICONS.clear;if(/銷售量|數量/.test(label))return ICONS.qty;if(/日均|平均/.test(label))return ICONS.chart;if(/人|來客/.test(label))return ICONS.people;if(/報告|明細/.test(label))return ICONS.file;return ICONS.sales}
  function ensureView(page,id){let view=$(`#${id}`,page);if(!view){view=document.createElement('div');view.id=id;view.className='opx-view';page.appendChild(view)}return view}
  function setHidden(el,on=true){if(el)el.classList.toggle('opx-source-hidden',on)}
  function rankRows(card){return $$('.ex513-row',card).slice(0,5).map((r,i)=>({rank:i+1,name:txt('.ex513-name b',r)||txt('b',r),meta:txt('.ex513-name small',r)||txt('small',r),value:txt('.ex513-val',r)||txt('.rank-money b',r)||txt('.v57-value',r)}))}
  function execRender(){
    const page=$('#executive');if(!page)return;const source=$('.exec-v513',page);if(!source)return;setHidden(source,true);setHidden($(':scope>.hero',page),true);setHidden($(':scope>.trust-strip',page),true);setHidden($(':scope>.grid-2',page),true);
    const view=ensureView(page,'opxExecutive');
    const period=txt('.ex513-period',source);const summary=txt('.ex513-summary strong',source)||txt('.ex513-summary',source);
    const kpis=$$('.ex513-kpi',source).map((k,i)=>({label:txt('span',k),value:txt('b',k)||txt('strong',k),sub:txt('small',k),tone:TONES[i%TONES.length]})).filter(x=>x.label||x.value);
    const cards=$$('.ex513-card',source).map(c=>({title:txt('.ex513-head h3',c)||txt('h3',c),sub:txt('.ex513-head p',c)||txt('.ex513-head small',c),rows:rankRows(c)})).filter(x=>x.title&&x.rows.length);
    const khtml=kpis.map(k=>`<div class="opx-kpi" data-tone="${k.tone}"><div class="opx-kpi-icon">${iconFor(k.label)}</div><div><div class="opx-kpi-label">${k.label}</div><div class="opx-kpi-value">${k.value||'—'}</div>${k.sub?`<div class="opx-kpi-sub">${k.sub}</div>`:''}</div></div>`).join('');
    const bhtml=cards.map((c,ci)=>{const vals=c.rows.map(r=>num(r.value)),max=Math.max(1,...vals);return `<section class="opx-board"><div class="opx-board-head"><div class="opx-board-icon">${ci===0?'♛':'●'}</div><div class="opx-board-title"><h2>${c.title}</h2>${c.sub?`<p>${c.sub}</p>`:''}</div><div class="opx-topbadge">TOP 5</div></div><div class="opx-rows">${c.rows.map((r,i)=>`<div class="opx-row"><div class="opx-rank">${r.rank}</div><div class="opx-name"><b>${r.name||'—'}</b><small>${r.meta||''}</small></div><div class="opx-progress"><i style="width:${Math.max(7,(vals[i]/max)*100)}%"></i></div><div class="opx-money">${r.value||'—'}</div></div>`).join('')}</div></section>`}).join('');
    view.innerHTML=`<section class="opx-result"><div class="opx-result-head"><div><div class="opx-eyebrow">PERIOD RESULT</div><h1>本期營運結果</h1><div class="opx-desc">${summary||'依匯入資料呈現本期實際營運結果。'}</div></div><div class="opx-period">${period||''}${period?'<div class="opx-period-pill">本期資料</div>':''}</div></div><div class="opx-kpis">${khtml}</div></section>${bhtml}`;
  }
  function analysisRows(sub){return $$('.v57-row',sub).slice(0,10).map((r,i)=>({rank:i+1,name:txt('.v57-main b',r),meta:txt('.v57-main small',r),value:txt('.v57-value',r)}))}
  function analysisRender(){
    const page=$('#analysis');if(!page)return;const source=$('.analysis-safe-v57',page);if(!source)return;setHidden(source,true);setHidden($(':scope>.toolbar',page),true);setHidden($(':scope>.analysis-layout',page),true);setHidden($(':scope>.top10-sales-panel',page),true);
    const view=ensureView(page,'opxAnalysis');
    const sections=$$('.analysis-v57-card',source).slice(0,3).map((sec,si)=>{
      const title=txt('.analysis-v57-head b',sec),desc=txt('.analysis-v57-head small',sec),no=txt('.analysis-v57-no',sec)||String(si+1),kind=/出清/.test(title)?'clearance':/報廢/.test(title)?'waste':'sales';
      const k=$('.v57-kpi',sec),kl=txt('span',k),kv=txt('strong',k),ks=txt('small',k);
      const subs=$$('.v57-sub',sec).filter(s=>!/改善優先度/.test(txt('h4',s))).slice(0,3);
      const blocks=subs.map(sub=>{const h=txt('h4',sub),rows=analysisRows(sub),vals=rows.map(r=>num(r.value)),max=Math.max(1,...vals);return `<div><div class="opx-mini-title"><span>${h}</span><em>TOP ${rows.length}</em></div><div class="opx-rows">${rows.map((r,i)=>`<div class="opx-row"><div class="opx-rank">${r.rank}</div><div class="opx-name"><b>${r.name||'—'}</b><small>${r.meta||''}</small></div><div class="opx-progress"><i style="width:${Math.max(7,(vals[i]/max)*100)}%"></i></div><div class="opx-money">${r.value||'—'}</div></div>`).join('')}</div></div>`}).join('');
      const det=$('.v57-detail',sec);let detail='';if(det){const label=txt('summary span:first-child',det)||'資料明細';const body=$('.v57-detail-body',det)?.innerHTML||'';detail=`<details class="opx-details"><summary><span>${label}</span><span>查看／收合</span></summary><div class="opx-details-body">${body}</div></details>`}
      return `<section class="opx-analysis-section" data-kind="${kind}"><div class="opx-analysis-head"><div class="opx-analysis-no">${no}</div><div><h2>${title}</h2><p>${desc}</p></div></div><div class="opx-analysis-body"><div class="opx-analysis-kpi"><div><span>${kl}</span><strong>${kv}</strong><small>${ks}</small></div><div class="opx-kpi-icon">${iconFor(title)}</div></div>${blocks}${detail}</div></section>`;
    }).join('');
    view.innerHTML=sections;
  }
  function nav(){const labels={executive:'總覽',overview:'洞察',analysis:'分析',anomaly:'異常',improve:'改善',report:'報告'};$$('.bottom-nav [data-page]').forEach(b=>{const s=$('span',b);if(s&&labels[b.dataset.page])s.textContent=labels[b.dataset.page]})}
  function run(){nav();execRender();analysisRender()}
  run();let pending=false;new MutationObserver(()=>{if(pending)return;pending=true;requestAnimationFrame(()=>{pending=false;run()})}).observe(document.body,{subtree:true,childList:true,characterData:true});
})();