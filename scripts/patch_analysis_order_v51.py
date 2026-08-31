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
   const firstMovable=all.find(x=>x!==sales&&x!==clearance&&x!==split&&x!==loss) || null;
   if(firstMovable) firstMovable.before(sales); else page.appendChild(sales);
   sales.after(clearance);
   if(split){clearance.after(split);split.after(loss)}else{clearance.after(loss)}
 }
 document.addEventListener('DOMContentLoaded',reorder);
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);reorder()};
 setTimeout(reorder,0);
})();
</script>
'''
if 'id="analysis-order-v51-js"' not in s:s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('patched v5.1: analysis order sales -> clearance -> waste -> total loss')
# trigger deployment 2026-09-01
