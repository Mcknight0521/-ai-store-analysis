from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
style='''
<style id="interval-top10-lock-v50-css">
.top10-sales-panel.interval-disabled{position:relative;overflow:hidden;background:#F1F3F6!important;border-color:#D8DEE7!important;box-shadow:none!important}
.top10-sales-panel.interval-disabled>*:not(.interval-top10-notice){filter:grayscale(1);opacity:.42;pointer-events:none;user-select:none}
.interval-top10-notice{display:none;margin:0 0 14px;padding:14px 16px;border:1px solid #CDD5DF;border-radius:15px;background:#E4E8EE;color:#344054}
.interval-top10-notice b{display:block;font-size:14px;line-height:1.35}.interval-top10-notice span{display:block;margin-top:5px;font-size:11px;line-height:1.5;color:#667085}
.top10-sales-panel.interval-disabled .interval-top10-notice{display:block;filter:none;opacity:1;pointer-events:auto}
@media(max-width:760px){.interval-top10-notice{padding:13px 14px}.interval-top10-notice b{font-size:13px}.interval-top10-notice span{font-size:11px}}
</style>
'''
if 'id="interval-top10-lock-v50-css"' not in s:s=s.replace('</head>',style+'</head>',1)
js='''
<script id="interval-top10-lock-v50-js">
(function(){
 function dailyReportAvailable(){
   const list=Array.isArray(window.rows)?window.rows:[];
   if(!window.confirmed||!list.length)return true;
   const pm=window.__opsPeriodMode||{};
   if(pm.mode==='mixed-aggregate'||pm.mode==='period-aggregate'||pm.mode==='aggregate')return false;
   const valid=list.filter(r=>r.date instanceof Date&&!isNaN(r.date));
   if(!valid.length)return false;
   const unique=new Set(valid.map(r=>{const d=r.date;return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`}));
   return unique.size>1 || pm.mode==='daily' || pm.dailyAvailable===true;
 }
 function apply(){
   const panel=document.querySelector('.top10-sales-panel');if(!panel)return;
   let note=panel.querySelector('.interval-top10-notice');
   if(!note){note=document.createElement('div');note.className='interval-top10-notice';note.innerHTML='<b>區間銷售報表無法使用</b><span>此功能僅支援「每日銷售報表」分別上傳後分析。</span>';panel.prepend(note)}
   const disabled=window.confirmed&&!dailyReportAvailable();panel.classList.toggle('interval-disabled',disabled);
 }
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);apply()};
 document.addEventListener('DOMContentLoaded',apply);setTimeout(apply,0);
})();
</script>
'''
if 'id="interval-top10-lock-v50-js"' not in s:s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('patched v5.0: interval report disables weekday/weekend sales Top 10')
