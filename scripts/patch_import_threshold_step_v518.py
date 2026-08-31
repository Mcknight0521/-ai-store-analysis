from pathlib import Path
import re
p=Path('index.html'); s=p.read_text(encoding='utf-8')
for ident in ['import-threshold-v518-css','import-threshold-v518-js']:
 s=re.sub(r'\n?<(script|style) id="'+ident+r'">.*?</\1>\n?','\n',s,flags=re.S)
css=r'''<style id="import-threshold-v518-css">
/* v5.18: anomaly page is display-only; threshold input belongs to import completion. */
#anomaly .av58-settings,#anomaly .av58-start,#av58Modal{display:none!important}
.it518-modal{position:fixed;inset:0;z-index:160;background:rgba(7,15,29,.58);backdrop-filter:blur(7px);display:none;align-items:flex-end;justify-content:center;padding:14px}.it518-modal.open{display:flex}.it518-sheet{width:min(560px,100%);background:#fff;border-radius:24px;padding:19px;box-shadow:0 28px 80px rgba(0,0,0,.3)}.it518-step{font-size:8px;font-weight:950;letter-spacing:.16em;color:#2c64f1}.it518-sheet h3{margin:6px 0 5px;font-size:20px}.it518-sheet p{margin:0;color:#7a8699;font-size:10px;line-height:1.55}.it518-fields{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}.it518-field label{display:block;margin-bottom:6px;font-size:10px;font-weight:900;color:#475467}.it518-input{display:flex;align-items:center;border:1px solid #e1e7ef;border-radius:13px;padding:0 11px}.it518-input input{min-width:0;width:100%;border:0;outline:0;padding:12px 2px;font-size:18px;font-weight:900}.it518-input span{font-size:11px;color:#7a8699}.it518-note{margin-top:11px;padding:10px 11px;border-radius:12px;background:#f5f8fc;color:#667085;font-size:9px;line-height:1.55}.it518-actions{display:flex;justify-content:flex-end;margin-top:15px}.it518-go{border:0;border-radius:12px;background:#2c64f1;color:#fff;padding:12px 16px;font-size:11px;font-weight:950;box-shadow:0 8px 20px rgba(44,100,241,.22)}
@media(max-width:620px){.it518-fields{grid-template-columns:1fr}.it518-sheet{border-radius:22px 22px 18px 18px}}
</style>'''
js=r'''<script id="import-threshold-v518-js">
(function(){
 const KEY='opsAnomalyThresholdsV58', SESSION='opsImportThresholdSigV518';
 const getT=()=>{try{const x=JSON.parse(localStorage.getItem(KEY)||'null');return x&&Number.isFinite(Number(x.clearance))&&Number.isFinite(Number(x.waste))?x:null}catch(e){return null}};
 function sig(){const r=Array.isArray(window.rows)?window.rows:[];if(!r.length)return '';const a=r[0]||{},z=r[r.length-1]||{};return [r.length,a.periodStart||'',z.periodEnd||'',a.item||a.sku||'',z.item||z.sku||''].join('|')}
 function ensure(){let m=document.getElementById('it518Modal');if(m)return m;document.body.insertAdjacentHTML('beforeend',`<div class="it518-modal" id="it518Modal" role="dialog" aria-modal="true"><div class="it518-sheet"><div class="it518-step">IMPORT · FINAL STEP</div><h3>設定本次分析警戒值</h3><p>這是匯入流程最後一步。OpsPilot 會使用同一組標準判斷總覽、異常與改善優先商品。</p><div class="it518-fields"><div class="it518-field"><label>出清率警戒值</label><div class="it518-input"><input id="it518C" type="number" min="0" max="100" step="0.1" inputmode="decimal" placeholder="請輸入"><span>%</span></div></div><div class="it518-field"><label>報廢率警戒值</label><div class="it518-input"><input id="it518W" type="number" min="0" max="100" step="0.1" inputmode="decimal" placeholder="請輸入"><span>%</span></div></div></div><div class="it518-note">沒有警戒值就不判定商品好壞。設定後，主力商品不會只因損耗金額大就被判定為需改善；系統會先確認是否超標，再比較影響程度。</div><div class="it518-actions"><button type="button" class="it518-go">開始分析</button></div></div></div>`);return document.getElementById('it518Modal')}
 function open(){const m=ensure(),t=getT();document.getElementById('it518C').value=t?(Number(t.clearance)*100).toFixed(2).replace(/\.00$/,''):'';document.getElementById('it518W').value=t?(Number(t.waste)*100).toFixed(2).replace(/\.00$/,''):'';m.classList.add('open')}
 function check(){if(!window.confirmed||!Array.isArray(window.rows)||!window.rows.length)return;const s=sig();if(!s||sessionStorage.getItem(SESSION)===s)return;open()}
 document.addEventListener('click',e=>{if(!e.target.closest('.it518-go'))return;const c=Number(document.getElementById('it518C').value),w=Number(document.getElementById('it518W').value);if(!Number.isFinite(c)||!Number.isFinite(w)||c<0||c>100||w<0||w>100){if(typeof toast==='function')toast('請輸入 0～100 的出清率與報廢率警戒值');return}localStorage.setItem(KEY,JSON.stringify({clearance:c/100,waste:w/100}));sessionStorage.setItem(SESSION,sig());document.getElementById('it518Modal').classList.remove('open');if(typeof window.renderAnomalyCenterV58==='function')window.renderAnomalyCenterV58();if(typeof window.renderAll==='function')window.renderAll();if(typeof toast==='function')toast('警戒值已套用，開始分析')});
 // Import completion can happen through PDF/Excel and aggregate-period paths; observe the exposed confirmed/rows state instead of changing parser/import code.
 setInterval(check,350);document.addEventListener('DOMContentLoaded',()=>{ensure();setTimeout(check,400)});
})();
</script>'''
s=s.replace('</head>',css+'</head>',1);s=s.replace('</body>',js+'</body>',1)
p.write_text(s,encoding='utf-8');print('v5.18 threshold step injected safely')
