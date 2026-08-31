from pathlib import Path
import re
p=Path('index.html'); s=p.read_text(encoding='utf-8')
KEY='opsAnomalyThresholdsV58'

# Thresholds are per-import only. Never keep a default across uploads.
s=s.replace("localStorage.getItem('opsAnomalyThresholdsV58')","sessionStorage.getItem('opsAnomalyThresholdsV58')")
s=s.replace("localStorage.setItem('opsAnomalyThresholdsV58'","sessionStorage.setItem('opsAnomalyThresholdsV58'")

# Import final step: blank every upload, reset current threshold on file selection/drop,
# and keep the chosen values only for the current analysis session.
m=re.search(r'<script id="import-threshold-v518-js">(.*?)</script>',s,re.S)
if m:
    body=m.group(1)
    body=re.sub(r"const getT=.*?;\n","const getT=()=>null;\n",body,count=1)
    body=re.sub(r"function open\(\)\{.*?m\.classList\.add\('open'\)\}","function open(){const m=ensure();if(m.classList.contains('open'))return;document.getElementById('it518C').value='';document.getElementById('it518W').value='';m.classList.add('open')}",body,count=1,flags=re.S)
    body=body.replace("localStorage.setItem(KEY,JSON.stringify({clearance:c/100,waste:w/100}))","sessionStorage.setItem(KEY,JSON.stringify({clearance:c/100,waste:w/100}))")
    body=body.replace("localStorage.getItem(KEY)","sessionStorage.getItem(KEY)")
    if 'function resetForNewUpload()' not in body:
        reset="""
 function resetForNewUpload(){sessionStorage.removeItem(KEY);sessionStorage.removeItem(SESSION);const m=document.getElementById('it518Modal');if(m)m.classList.remove('open');}
 document.addEventListener('change',e=>{if(e.target&&e.target.matches&&e.target.matches('input[type=file]'))resetForNewUpload()},true);
 document.addEventListener('drop',e=>{if(e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files.length)resetForNewUpload()},true);
 try{localStorage.removeItem(KEY)}catch(e){}
"""
        body=body.replace("setInterval(check,350);",reset+"\n setInterval(check,350);",1)
    s=s[:m.start(1)]+body+s[m.end(1):]

# Total overview: same exact improvement-priority model as anomaly center.
m=re.search(r'<script id="executive-summary-v513-js">(.*?)</script>',s,re.S)
if m:
    body=m.group(1)
    # repair any malformed thresholds() left by an earlier patch, then set canonical version
    body=re.sub(r"function thresholds\(\)\{.*?\n function priority","function thresholds(){try{return JSON.parse(sessionStorage.getItem('opsAnomalyThresholdsV58')||'null')}catch{return null}}\n function priority",body,count=1,flags=re.S)
    pr=re.search(r" function priority\(a\)\{.*?\}\n function rank",body,re.S)
    if pr:
        new=""" function priority(a){const t=thresholds();if(!a.length||!t)return[];const ct=n(t.clearance),wt=n(t.waste),lt=ct+wt,totalLoss=a.reduce((s,x)=>s+x.loss,0);const abnormal=a.filter(x=>(ct&&x.cr!=null&&x.cr>ct)||(wt&&x.wr!=null&&x.wr>wt)||(lt&&x.lr!=null&&x.lr>lt));if(!abnormal.length)return[];abnormal.forEach(x=>{x.lossShare=totalLoss>0?x.loss/totalLoss:0;const ratios=[];if(ct&&x.cr>ct)ratios.push(x.cr/ct);if(wt&&x.wr>wt)ratios.push(x.wr/wt);if(lt&&x.lr>lt)ratios.push(x.lr/lt);x.overRatio=Math.max(1,...ratios);x.dual=!!(ct&&wt&&x.cr>ct&&x.wr>wt)});const maxShare=Math.max(...abnormal.map(x=>x.lossShare),.000001),maxOver=Math.max(...abnormal.map(x=>Math.max(0,x.overRatio-1)),.000001);abnormal.forEach(x=>{x.ps=(x.lossShare/maxShare)*.60+(Math.max(0,x.overRatio-1)/maxOver)*.30+(x.dual?.10:0)});return abnormal.sort((x,y)=>y.ps-x.ps||y.loss-x.loss).slice(0,5)}
 function rank"""
        body=body[:pr.start()]+new+body[pr.end():]
    # Current overview may show a reason label instead of a score. Replace either form with the same transparent metrics.
    body=re.sub(r"\$\{card\('需改善商品',p\.map\(\(x,i\)=>row\(i,x\.name,.*?\)\)\)\}","${card('改善優先商品',p.map((x,i)=>row(i,x.name,money(x.loss),`全店損耗占比 ${pct(x.lossShare)}・超標 ${x.overRatio.toFixed(2)}×・損耗率 ${pct(x.lr)}`)))}",body,count=1,flags=re.S)
    s=s[:m.start(1)]+body+s[m.end(1):]

# New anomaly center: same per-import threshold source.
m=re.search(r'<script id="anomaly-rankings-v519-js">(.*?)</script>',s,re.S)
if m:
    body=m.group(1).replace("localStorage.getItem(KEY)","sessionStorage.getItem(KEY)")
    s=s[:m.start(1)]+body+s[m.end(1):]

# Hide legacy anomaly ranking UI so only the canonical v5.19 ranking is visible.
if 'v520-hide-legacy-anomaly' not in s:
    s=s.replace('</head>',"<style id=\"v520-hide-legacy-anomaly\">#anomaly .anomaly-top20-v516{display:none!important}</style>\n</head>",1)
if 'opspilot-priority-threshold-v520' not in s:
    s=s.replace('</head>','<meta name="opspilot-priority-threshold-v520" content="1">\n</head>',1)

p.write_text(s,encoding='utf-8')
print('v5.20.1 unified priority + per-import thresholds applied')