from pathlib import Path
import re

p=Path('index.html'); s=p.read_text(encoding='utf-8')
# Patch the already-safe V5.7 presentation only; base DOM remains untouched.
s=s.replace(".sort((a,b)=>b.priorityScore-a.priorityScore).slice(0,10)", ".sort((a,b)=>b.priorityScore-a.priorityScore).slice(0,5)")
# Remove loss analysis card while keeping loss as an interval Top10 metric.
s=s.replace("+section('loss',4,'損耗分析','總損耗率 → 金額 Top 10 → 損耗率 Top 10 → 改善優先度 → 明細',lossBody)", "")
# Fix detail expansion: render content on every open, because render() rebuilds the cards and stale loaded flags could leave empty bodies.
s=s.replace("if(open&&!box.dataset.loaded){box.querySelector('.v57-detail-body').innerHTML=details(kind);box.dataset.loaded='1'}", "if(open){box.querySelector('.v57-detail-body').innerHTML=details(kind)}")
# Make detail rows robust to normalized parser field aliases.
s=s.replace("const rows=list().filter(r=>kind==='sales'?r.sales!=null:kind==='clearance'?r.clearance!=null:kind==='waste'?r.waste!=null:r.clearance!=null||r.waste!=null);", "const rows=list().filter(r=>kind==='sales'?r.sales!=null:kind==='clearance'?(r.clearance!=null||r.clearanceAmount!=null):kind==='waste'?(r.waste!=null||r.wasteAmount!=null):(r.clearance!=null||r.clearanceAmount!=null||r.waste!=null||r.wasteAmount!=null));")
s=s.replace("const amount=kind==='clearance'?r.clearance:kind==='waste'?r.waste:(r.clearance==null&&r.waste==null?null:Number(r.clearance||0)+Number(r.waste||0)),rr=kind==='sales'?null:rate(amount,r.sales);", "const c=r.clearance??r.clearanceAmount,w=r.waste??r.wasteAmount,amount=kind==='clearance'?c:kind==='waste'?w:(c==null&&w==null?null:Number(c||0)+Number(w||0)),rr=kind==='sales'?null:rate(amount,r.sales);")
s=s.replace("${money(r.clearance)}</td><td>${money(r.waste)}", "${money(r.clearance??r.clearanceAmount)}</td><td>${money(r.waste??r.wasteAmount)}")
p.write_text(s,encoding='utf-8')
print('analysis v5.7.1 patched: details fixed, priority top5, loss section removed')
