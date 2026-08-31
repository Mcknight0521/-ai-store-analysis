from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove older analysis-order injection so this patch is idempotent.
s=re.sub(r'\n?<script id="analysis-order-v51-js">.*?</script>\n?', '\n', s, flags=re.S)
s=re.sub(r'\n?<style id="analysis-layout-v52-css">.*?</style>\n?', '\n', s, flags=re.S)
s=re.sub(r'\n?<script id="analysis-layout-v52-js">.*?</script>\n?', '\n', s, flags=re.S)

style=r'''
<style id="analysis-layout-v52-css">
#analysis .analysis-flow-v52{display:grid;gap:14px;margin-top:12px}
#analysis .analysis-section-v52{position:relative;border-radius:20px;border:1px solid var(--line);background:#fff;box-shadow:var(--shadow);overflow:hidden}
#analysis .analysis-section-v52>.analysis-section-label{display:flex;align-items:center;gap:10px;padding:14px 16px 0;font-weight:950;letter-spacing:-.02em}
#analysis .analysis-section-label .n{width:30px;height:30px;border-radius:999px;display:grid;place-items:center;color:#fff;font-size:13px;flex:0 0 auto}
#analysis .analysis-section-label b{font-size:17px}
#analysis .analysis-section-v52>.panel{border:0;box-shadow:none;border-radius:0;margin:0;background:transparent}
#analysis .analysis-sales-v52{border-color:#cfe0ff;background:linear-gradient(180deg,#f7fbff,#fff)}
#analysis .analysis-sales-v52 .analysis-section-label{color:#2156b7}.analysis-sales-v52 .analysis-section-label .n{background:#2C64F1}
#analysis .analysis-clearance-v52{border-color:#cfe9dd;background:linear-gradient(180deg,#f7fcf9,#fff)}
#analysis .analysis-clearance-v52 .analysis-section-label{color:#16805B}.analysis-clearance-v52 .analysis-section-label .n{background:#16805B}
#analysis .analysis-waste-v52{border-color:#ffd9cf;background:linear-gradient(180deg,#fff9f7,#fff)}
#analysis .analysis-waste-v52 .analysis-section-label{color:#c64f31}.analysis-waste-v52 .analysis-section-label .n{background:#e85d3d}
#analysis .analysis-loss-v52{border-color:#d9e0ea;background:linear-gradient(180deg,#f8fafc,#fff)}
#analysis .analysis-loss-v52 .analysis-section-label{color:#475467}.analysis-loss-v52 .analysis-section-label .n{background:#52637a}
#analysis .analysis-detail-v52{margin-top:14px;border:1px solid var(--line);border-radius:18px;background:#fff;overflow:hidden}
#analysis .analysis-detail-toggle-v52{width:100%;border:0;background:#fff;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px;color:var(--ink);font-weight:900;font-size:13px}
#analysis .analysis-detail-toggle-v52 span:last-child{font-size:11px;color:var(--muted);font-weight:800}
#analysis .analysis-detail-body-v52{display:none;padding:0 16px 16px}
#analysis .analysis-detail-v52.open .analysis-detail-body-v52{display:block}
#analysis .analysis-detail-v52.open .analysis-detail-toggle-v52 span:last-child:after{content:'收合'}
#analysis .analysis-detail-v52:not(.open) .analysis-detail-toggle-v52 span:last-child:after{content:'展開'}
#analysis .loss-top10-v49{margin-top:8px!important;padding-top:2px}
#analysis .analysis-sales-v52 .loss-top10-v49{order:-1}
@media(max-width:760px){#analysis .analysis-section-v52>.analysis-section-label{padding:12px 13px 0}#analysis .analysis-section-label b{font-size:15px}#analysis .analysis-section-label .n{width:27px;height:27px;font-size:12px}}
</style>
'''

js=r'''
<script id="analysis-layout-v52-js">
(function(){
 function closestPanel(el){return el ? (el.classList&&el.classList.contains('panel')?el:el.closest('.panel')) : null}
 function findPanelByText(page,re){return [...page.querySelectorAll('.panel')].find(p=>re.test((p.textContent||'').replace(/\s+/g,' ')))||null}
 function mkSection(kind,no,title){
   const sec=document.createElement('section');sec.className=`analysis-section-v52 analysis-${kind}-v52`;
   sec.innerHTML=`<div class="analysis-section-label"><span class="n">${no}</span><b>${title}</b></div>`;return sec
 }
 function setupDetails(page,flow,used){
   let detail=[...page.querySelectorAll('.panel')].find(p=>/資料明細/.test(p.textContent||''));
   if(!detail||used.has(detail))return;
   const wrap=document.createElement('section');wrap.className='analysis-detail-v52';
   const btn=document.createElement('button');btn.type='button';btn.className='analysis-detail-toggle-v52';btn.setAttribute('aria-expanded','false');btn.innerHTML='<span>資料明細</span><span></span>';
   const body=document.createElement('div');body.className='analysis-detail-body-v52';
   [...detail.children].forEach(ch=>{if(!/資料明細/.test(ch.textContent||'')||ch.querySelector?.('table'))body.appendChild(ch)});
   detail.remove();wrap.append(btn,body);flow.appendChild(wrap);
   btn.addEventListener('click',()=>{const open=wrap.classList.toggle('open');btn.setAttribute('aria-expanded',open?'true':'false')});
 }
 function apply(){
   const page=document.getElementById('analysis');if(!page)return;
   if(page.dataset.layoutV52==='1')return;

   const sales=closestPanel(page.querySelector('.top10-sales-panel'))||closestPanel(page.querySelector('#salesTop10List'))||findPanelByText(page,/平日\s*\/\s*假日.*Top\s*10|SALES\s*TOP\s*10/i);
   const clearance=closestPanel(page.querySelector('#clearanceRateSummary'))||findPanelByText(page,/出清率分析|出清.*Top\s*10/i);
   const waste=document.getElementById('lossSplitPanel')||closestPanel(page.querySelector('#lossSplitSummary'));
   const loss=closestPanel(page.querySelector('#analysisBars'))||findPanelByText(page,/品項損耗排行|每日損耗趨勢|損耗總覽/i);
   if(!sales)return;

   const oldFlow=page.querySelector('.analysis-flow-v52');if(oldFlow)oldFlow.remove();
   const flow=document.createElement('div');flow.className='analysis-flow-v52';
   const toolbar=page.querySelector('.toolbar');
   if(toolbar)toolbar.after(flow);else page.appendChild(flow);
   const used=new Set();

   const salesSec=mkSection('sales',1,'營業額分析');salesSec.appendChild(sales);used.add(sales);flow.appendChild(salesSec);
   const intervalTop=page.querySelector('.loss-top10-v49');
   if(intervalTop){
     const salesPanel=salesSec.querySelector('.panel')||salesSec;
     const firstBody=[...salesPanel.children].find(x=>!x.classList.contains('panel-head')&&!x.classList.contains('interval-top10-notice'));
     if(firstBody)firstBody.before(intervalTop);else salesPanel.appendChild(intervalTop);
     const h=intervalTop.querySelector('h3');if(h)h.textContent='區間商品 Top 10';
   }

   if(clearance&&clearance!==sales){const sec=mkSection('clearance',2,'出清分析');sec.appendChild(clearance);used.add(clearance);flow.appendChild(sec)}
   if(waste&&waste!==sales&&waste!==clearance){
     const sec=mkSection('waste',3,'報廢分析');sec.appendChild(waste);used.add(waste);flow.appendChild(sec);
     const h=waste.querySelector('.panel-head h3');if(h)h.textContent='報廢分析';
     const p=waste.querySelector('.panel-head p');if(p)p.textContent='檢視期間報廢金額、報廢率與每日報廢變化；不補缺值、不把缺少資料視為 0。';
   }
   if(loss&&loss!==sales&&loss!==clearance&&loss!==waste){const sec=mkSection('loss',4,'損耗總覽');sec.appendChild(loss);used.add(loss);flow.appendChild(sec)}

   setupDetails(page,flow,used);
   page.dataset.layoutV52='1';
 }
 document.addEventListener('DOMContentLoaded',()=>setTimeout(apply,0));
 const old=window.renderAll;window.renderAll=function(){if(typeof old==='function')old.apply(this,arguments);const p=document.getElementById('analysis');if(p)p.dataset.layoutV52='';apply()};
 setTimeout(apply,100);
})();
</script>
'''

s=s.replace('</head>',style+'</head>',1)
s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8')
print('patched v5.2: sales -> clearance -> waste -> loss; interval Top10 first; details collapsed')
