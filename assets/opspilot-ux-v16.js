(()=>{
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  function ensureProgress(){
    const stage=$('#importStage1'); if(!stage)return null;
    let box=$('.import-verify-progress',stage);
    if(!box){
      box=document.createElement('div'); box.className='import-verify-progress'; box.hidden=true;
      box.innerHTML='<div class="row"><b>檔案驗證</b><span class="pct">0%</span></div><div class="track"><div class="fill"></div></div><small>檢查檔案是否可讀、資料列是否有效，以及欄位是否可以辨識。</small>';
      const list=$('#fileList',stage); stage.insertBefore(box,list||null);
    }
    return box;
  }
  function setProgress(p,label){
    const box=ensureProgress(); if(!box)return;
    box.hidden=false; const v=Math.max(0,Math.min(100,Math.round(p)));
    $('.fill',box).style.width=v+'%'; $('.pct',box).textContent=v+'%';
    if(label)$('small',box).textContent=label;
  }
  function finishProgress(ok,total){
    setProgress(100,ok===total?`驗證完成：${ok} 個檔案可使用。請按「下一步」查看欄位辨識。`:`驗證完成：${ok}/${total} 個檔案可使用。請確認後按「下一步」。`);
  }
  const original=window.handleFiles;
  if(typeof original==='function'){
    window.handleFiles=async function(files){
      const arr=[...(files||[])]; if(!arr.length)return original.apply(this,arguments);
      setProgress(6,'正在讀取檔案…');
      const list=$('#fileList'); let obs=null;
      if(list){
        obs=new MutationObserver(()=>{
          const rs=$$('.file-row',list),done=rs.filter(r=>['✓','!'].includes(r.querySelector('span')?.textContent?.trim())).length;
          const ok=rs.filter(r=>r.querySelector('span')?.textContent?.trim()==='✓').length;
          const pct=rs.length?10+(done/Math.max(arr.length,rs.length))*82:10;
          setProgress(pct,done<arr.length?`正在驗證 ${Math.min(done+1,arr.length)}/${arr.length}：解析結構與核對資料…`:`正在整理辨識結果…`);
          if(done>=arr.length)finishProgress(ok,arr.length);
        });
        obs.observe(list,{subtree:true,childList:true,characterData:true});
      }
      try{
        const out=await original.apply(this,arguments);
        const ok=$$('.file-row',list||document).filter(r=>r.querySelector('span')?.textContent?.trim()==='✓').length;
        finishProgress(ok,arr.length);
        if(typeof window.setImportStep==='function')window.setImportStep(1);
        const next=$('#nextImportStep'); if(next){next.disabled=!(window.staged?.length||0); next.hidden=false;}
        const prev=$('#prevImportStep'); if(prev)prev.hidden=true;
        const confirm=$('#confirmImport'); if(confirm)confirm.hidden=true;
        return out;
      }finally{if(obs)obs.disconnect();}
    };
  }
  function addMoneyOverview(){
    const content=$('#opxContent'); if(!content)return;
    if(!$('#opxApp .opx-nav button[data-page="analysis"].active'))return;
    if($('.opx-money-overview',content))return;
    const src=$('#executive'); if(!src)return;
    const raw=$$('.ex513-kpi',src).map(n=>({label:(n.querySelector('span')?.textContent||'').trim(),value:(n.querySelector('b,strong')?.textContent||'').trim()}));
    const money=raw.filter(x=>x.value && !x.value.includes('%') && /營業額|出清|報廢|損耗/.test(x.label)).slice(0,4);
    if(!money.length)return;
    const sec=document.createElement('section'); sec.className='opx-card opx-money-overview';
    sec.innerHTML=`<div class="head"><div><h2>金額總覽</h2><p>先看本期金額規模，再往下拆解營業額、出清與報廢。</p></div></div><div class="opx-money-grid">${money.map(x=>`<div class="opx-money-item"><small>${x.label}</small><b>${x.value}</b></div>`).join('')}</div>`;
    const first=content.firstElementChild; first?content.insertBefore(sec,first):content.appendChild(sec);
  }
  function refresh(){requestAnimationFrame(addMoneyOverview)}
  document.addEventListener('click',e=>{if(e.target.closest('#opxApp .opx-nav button[data-page="analysis"]'))setTimeout(refresh,40)});
  new MutationObserver(()=>refresh()).observe(document.body,{subtree:true,childList:true});
  ensureProgress(); refresh();
})();
