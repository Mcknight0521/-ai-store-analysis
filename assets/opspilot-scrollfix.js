(()=>{
  function hardTop(){
    const se=document.scrollingElement||document.documentElement;
    if(se) se.scrollTop=0;
    document.documentElement.scrollTop=0;
    document.body.scrollTop=0;
    window.scrollTo(0,0);
    const app=document.getElementById('opxApp');
    if(app) app.scrollIntoView({block:'start',inline:'nearest',behavior:'auto'});
  }
  function reset(){
    hardTop();
    requestAnimationFrame(()=>{hardTop();requestAnimationFrame(hardTop)});
    setTimeout(hardTop,40);
    setTimeout(hardTop,140);
  }
  window.addEventListener('pageshow',reset);
  window.addEventListener('load',reset,{once:true});
  document.addEventListener('DOMContentLoaded',reset,{once:true});
  document.addEventListener('click',e=>{
    const b=e.target.closest('#opxApp .opx-nav button[data-page]');
    if(!b)return;
    reset();
  },true);
})();