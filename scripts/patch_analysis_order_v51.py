from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
js='''
<script id="analysis-order-v51-js">
(function(){
 function reorder(){
   const page=document.getElementById('analysis');
   if(!page)return;
   const all=[...page.querySelectorAll(':scope > section, :scope > .panel')];
   const sales=all.find(x=>x.classList.contains('top10-sales-panel')||x.querySelector('#salesTop10List'));
   const clearance=all.find(x=>x.querySelector('#clearanceRateSummary'));
   const split=all.find(x=>x.id==='lossSplitPanel'||x.querySelector('#lossSplitSummary'));
   const loss=all.find(x=>x.querySelector('#analysisBars'));
   if(!sales||!clearance||!loss)return;
   // Reading order: sales -> clearance -> waste -> total loss.
   // The split panel owns waste metrics; keep it after clearance and before the legacy total-loss ranking.
   const anchor=sales;
   anchor.after(clearance);
   if(split){
     clearance.after(split);
     split.after(loss);
   }else{
     clearance.after(loss);
   }
   const t=loss.querySelector('#analysisTitle');
   if(t && /品項損耗排行|每日損耗趨勢/.test(t.textContent||'')){
     const kicker=loss.querySelector('.panel-kicker');
     if(kicker)kicker.textContent='TOTAL LOSS';
   }
 }
 document.addEventListener('DOMContentLoaded',reorder);
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);reorder()};
 setTimeout(reorder,0);
})();
</script>
'''
if 'id="analysis-order-v51-js"' not in s:s.replace('</body>',js+'</body>',1)
else: raise SystemExit('v51 already present')
# fix assignment typo safely
if 'id="analysis-order-v51-js"' not in s:
    s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('patched v5.1: analysis order sales -> clearance -> waste -> total loss')
