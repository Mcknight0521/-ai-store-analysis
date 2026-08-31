from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
old="${card('需改善商品',p.map((x,i)=>row(i,x.name,Math.round(x.ps*100)+' 分',`損耗 ${money(x.loss)}・損耗率 ${pct(x.lr)}`)))}"
new="${card('需改善商品',p.map((x,i)=>row(i,x.name,reason(x,a,t),`損耗 ${money(x.loss)}・損耗率 ${pct(x.lr)}`)))}"
if old not in s: raise SystemExit('priority card target not found')
# Add a human-readable reason function immediately before render(). Internal score remains sorting-only.
anchor=' function render(){const page=document.getElementById(\'executive\');'
reason=""" function reason(x,a,t){
  const ct=t?n(t.clearance):0,wt=t?n(t.waste):0;
  const dual=ct&&wt&&x.cr!=null&&x.wr!=null&&x.cr>ct&&x.wr>wt;
  const losses=a.map(v=>v.loss).filter(v=>Number.isFinite(v)&&v>0).sort((q,w)=>w-q), highAmount=losses.length&&x.loss>=losses[Math.min(losses.length-1,Math.max(0,Math.ceil(losses.length*.2)-1))];
  const extreme=x.lr!=null&&x.lr>=1;
  const highRate=x.lr!=null&&x.lr>=.3;
  if(dual)return '出清＋報廢雙重超標';
  if(highAmount&&highRate)return '金額高＋損耗率高';
  if(extreme)return '損耗率極高';
  if(highAmount)return '損耗金額高';
  if(ct&&x.cr!=null&&x.cr>ct)return '出清率超標';
  if(wt&&x.wr!=null&&x.wr>wt)return '報廢率超標';
  return '優先改善';
 }
"""
if anchor not in s: raise SystemExit('render anchor not found')
s=s.replace(anchor,reason+anchor,1).replace(old,new,1)
# render currently has const p=priority(a); expose threshold object to reason()
s=s.replace('const p=priority(a);root.innerHTML=', 'const p=priority(a),t=thresholds();root.innerHTML=',1)
p.write_text(s,encoding='utf-8');print('priority reason v5.15 patched')
