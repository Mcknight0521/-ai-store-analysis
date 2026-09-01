(()=>{
  const reset=()=>requestAnimationFrame(()=>requestAnimationFrame(()=>window.scrollTo({top:0,left:0,behavior:'auto'})));
  window.addEventListener('pageshow',reset,{once:true});
  document.addEventListener('DOMContentLoaded',reset,{once:true});
  document.addEventListener('click',e=>{
    const b=e.target.closest('#opxApp .opx-nav button[data-page]');
    if(b) reset();
  });
})();