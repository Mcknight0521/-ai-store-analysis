from pathlib import Path
import re
p=Path('index.html'); s=p.read_text(encoding='utf-8')
# Keep original analysis DOM untouched. Patch only the injected safe presentation layer.
old="function detailBlock(kind,label){return `<div class=\"v57-detail\" data-v57-detail=\"${kind}\"><button type=\"button\"><span>${label}</span><span>查看明細　⌄</span></button><div class=\"v57-detail-body\"></div></div>`}"
new="function detailBlock(kind,label){return `<div class=\"v57-detail\" data-v57-detail=\"${kind}\"><button type=\"button\"><span>${label}</span><span>查看明細　⌄</span></button><div class=\"v57-detail-body\">${details(kind)}</div></div>`}"
if old not in s: raise SystemExit('detailBlock target not found')
s=s.replace(old,new,1)
# Opening/closing now only controls visibility; table HTML already exists after every render.
old2="if(open){box.querySelector('.v57-detail-body').innerHTML=details(kind)}"
s=s.replace(old2,"if(open){const body=box.querySelector('.v57-detail-body');if(body&&!body.innerHTML.trim())body.innerHTML=details(kind)}",1)
p.write_text(s,encoding='utf-8')
print('analysis detail v5.12: detail HTML rendered eagerly')
