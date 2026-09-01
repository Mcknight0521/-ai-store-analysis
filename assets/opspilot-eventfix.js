(()=>{
  const esc=s=>(s??'').toString().replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot',"'":'&#39;'}[m]));
  function parse(raw){
    const text=(raw||'').replace(/\s+/g,' ').trim();
    const events=[];
    const re=/(\d{2}\/\d{2})([^—]*?)當日事件/g;
    let m;
    while((m=re.exec(text))){
      let label=m[2].trim().replace(/^[：:、\-\s]+/,'').replace(/[。；;]+$/,'');
      if(label&&!events.some(x=>x.date===m[1]&&x.label===label)) events.push({date:m[1],label});
    }
    const closure=text.match(/停班停課\s*(\d+)\s*筆(?:（部分地區\s*(\d+)）)?/);
    const typhoon=text.match(/颱風影響\s*(\d+)\s*筆/);
    return {events,closure:closure?closure[1]:null,partial:closure?.[2]||null,typhoon:typhoon?typhoon[1]:null};
  }
  function render(){
    const box=document.querySelector('#opxApp .opx-context-item');
    if(!box||box.dataset.eventFixed==='1') return;
    const raw=box.textContent||'';
    if(!/事件|停班停課|颱風|節慶/.test(raw)) return;
    const d=parse(raw);
    box.dataset.eventFixed='1';
    if(!d.events.length){
      box.innerHTML='<b>本期事件摘要</b><p>本期未辨識到需要特別標示的節慶、豪雨、大豪雨、停班停課或實際影響颱風事件。</p>';
      return;
    }
    const chips=[];
    if(d.closure!==null) chips.push(`<span>停班停課 ${esc(d.closure)} 筆${d.partial?`・部分地區 ${esc(d.partial)}`:''}</span>`);
    if(d.typhoon!==null) chips.push(`<span>颱風影響 ${esc(d.typhoon)} 筆</span>`);
    box.innerHTML=`<div class="opx-event-summary"><div><b>本期事件摘要</b><p>依日期與地區比對，只呈現本期實際需要注意的事件。</p></div>${chips.length?`<div class="opx-event-stats">${chips.join('')}</div>`:''}</div><div class="opx-event-list">${d.events.map(e=>`<div class="opx-event-row"><time>${esc(e.date)}</time><strong>${esc(e.label)}</strong></div>`).join('')}</div>`;
  }
  const style=document.createElement('style');
  style.textContent=`#opxApp .opx-event-summary{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:12px}#opxApp .opx-event-summary p{margin:4px 0 0!important;color:#8a96a9!important;font-size:11px!important;line-height:1.45!important}#opxApp .opx-event-stats{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}#opxApp .opx-event-stats span{padding:5px 8px;border-radius:999px;background:#fff4df;color:#9a681e;font-size:9px;font-weight:800;white-space:nowrap}#opxApp .opx-event-list{display:grid;grid-template-columns:1fr 1fr;gap:7px}#opxApp .opx-event-row{display:grid;grid-template-columns:52px minmax(0,1fr);align-items:center;gap:9px;padding:10px 11px;border:1px solid #e4eaf2;border-radius:13px;background:#fbfcfe}#opxApp .opx-event-row time{font-size:10px;font-weight:900;color:#5979b9}#opxApp .opx-event-row strong{font-size:10px;line-height:1.4;color:#263b59}@media(max-width:620px){#opxApp .opx-event-summary{display:block}#opxApp .opx-event-stats{justify-content:flex-start;margin-top:9px}#opxApp .opx-event-list{grid-template-columns:1fr}}`;
  document.head.appendChild(style);
  render();
  let raf=0;
  new MutationObserver(()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(render)}).observe(document.body,{subtree:true,childList:true,characterData:true});
})();