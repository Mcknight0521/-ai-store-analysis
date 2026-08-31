from pathlib import Path
import re
p=Path('index.html'); s=p.read_text(encoding='utf-8')

# 1) Thresholds are per-import only: use sessionStorage and never prefill from a prior import.
s=s.replace("localStorage.getItem('opsAnomalyThresholdsV58')","sessionStorage.getItem('opsAnomalyThresholdsV58')")
s=s.replace("localStorage.setItem('opsAnomalyThresholdsV58'","sessionStorage.setItem('opsAnomalyThresholdsV58'")

# Patch v5.18 import threshold flow specifically.
m=re.search(r'<script id="import-threshold-v518-js">(.*?)</script>',s,re.S)
if m:
    body=m.group(1)
    body=body.replace("const getT=()=>{try{const x=JSON.parse(localStorage.getItem(KEY)||'null');return x&&Number.isFinite(Number(x.clearance))&&Number.isFinite(Number(x.waste))?x:null}catch(e){return null}};","const getT=()=>null;")
    body=body.replace("function open(){const m=ensure();if(m.classList.contains('open'))return;const t=getT();document.getElementById('it518C').value=t?(Number(t.clearance)*100).toFixed(2).replace(/\\.00$/,''):'';document.getElementById('it518W').value=t?(Number(t.waste)*100).toFixed(2).replace(/\\.00$/,''):'';m.classList.add('open')}","function open(){const m=ensure();if(m.classList.contains('open'))return;document.getElementById('it518C').value='';document.getElementById('it518W').value='';m.classList.add('open')}")
    body=body.replace("localStorage.setItem(KEY,JSON.stringify({clearance:c/100,waste:w/100}))","sessionStorage.setItem(KEY,JSON.stringify({clearance:c/100,waste:w/100}))")
    reset="""
 function resetForNewUpload(){sessionStorage.removeItem(KEY);sessionStorage.removeItem(SESSION);const m=document.getElementById('it518Modal');if(m)m.classList.remove('open');}
 document.addEventListener('change',e=>{if(e.target&&e.target.matches&&e.target.matches('input[type=file]'))resetForNewUpload()},true);
 document.addEventListener('drop',e=>{if(e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files.length)resetForNewUpload()},true);
 try{localStorage.removeItem(KEY)}catch(e){}
"""
    body=body.replace("setInterval(check,350);document.addEventListener('DOMContentLoaded',()=>{ensure();setTimeout(check,400)});",reset+"\n setInterval(check,350);document.addEventListener('DOMContentLoaded',()=>{ensure();setTimeout(check,400)});")
    s=s[:m.start(1)]+body+s[m.end(1):]

# 2) Total overview uses exactly the same improvement-priority model as anomaly center:
# amount impact 60% + over-threshold severity 30% + dual clearance/waste anomaly 10%.
m=re.search(r'<script id="executive-summary-v513-js">(.*?)</script>',s,re.S)
if m:
    body=m.group(1)
    body=re.sub(r"function thresholds\(\)\{.*?\}","function thresholds(){try{return JSON.parse(sessionStorage.getItem('opsAnomalyThresholdsV58')||'null')}catch{return null}}",body,count=1,flags=re.S)
    old=re.search(r" function priority\(a\)\{.*?\}\n function rank",body,re.S)
    if old:
        new=""" function priority(a){const t=thresholds();if(!a.length||!t)return[];const ct=n(t.clearance),wt=n(t.waste),lt=ct+wt,totalLoss=a.reduce((s,x)=>s+x.loss,0);const abnormal=a.filter(x=>(ct&&x.cr!=null&&x.cr>ct)||(wt&&x.wr!=null&&x.wr>wt)||(lt&&x.lr!=null&&x.lr>lt));if(!abnormal.length)return[];abnormal.forEach(x=>{x.lossShare=totalLoss>0?x.loss/totalLoss:0;const ratios=[];if(ct&&x.cr>ct)ratios.push(x.cr/ct);if(wt&&x.wr>wt)ratios.push(x.wr/wt);if(lt&&x.lr>lt)ratios.push(x.lr/lt);x.overRatio=Math.max(1,...ratios);x.dual=!!(ct&&wt&&x.cr>ct&&x.wr>wt)});const maxShare=Math.max(...abnormal.map(x=>x.lossShare),.000001),maxOver=Math.max(...abnormal.map(x=>Math.max(0,x.overRatio-1)),.000001);abnormal.forEach(x=>{x.ps=(x.lossShare/maxShare)*.60+(Math.max(0,x.overRatio-1)/maxOver)*.30+(x.dual?.10:0)});return abnormal.sort((x,y)=>y.ps-x.ps||y.loss-x.loss).slice(0,5)}
 function rank"""
        body=body[:old.start()]+new+body[old.end():]
    body=body.replace("${card('需改善商品',p.map((x,i)=>row(i,x.name,Math.round(x.ps*100)+' 分',`損耗 ${money(x.loss)}・損耗率 ${pct(x.lr)}`)))}","${card('改善優先商品',p.map((x,i)=>row(i,x.name,money(x.loss),`全店損耗占比 ${pct(x.lossShare)}・超標 ${x.overRatio.toFixed(2)}×・損耗率 ${pct(x.lr)}`)))}")
    s=s[:m.start(1)]+body+s[m.end(1):]

# 3) Anomaly center threshold source is also per-import session storage.
m=re.search(r'<script id="anomaly-rankings-v519-js">(.*?)</script>',s,re.S)
if m:
    body=m.group(1).replace("localStorage.getItem(KEY)","sessionStorage.getItem(KEY)")
    s=s[:m.start(1)]+body+s[m.end(1):]

# Marker for regression checks.
s=s.replace('</head>','<meta name="opspilot-priority-threshold-v520" content="1">\n</head>',1)
p.write_text(s,encoding='utf-8')
print('v5.20 unified priority + per-import thresholds applied')