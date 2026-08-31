from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# The detailed timeline is the single source of truth for special events.
# Hide the duplicated summary-card block instead of rendering the same dates twice.
style='''\n<style id="event-single-list-v47">\n#externalEventCards{display:none!important}\n</style>\n'''
if 'id="event-single-list-v47"' not in s:
    s=s.replace('</head>',style+'</head>',1)

# Keep the render function harmless in case other code calls it.
s,n=re.subn(r"  function renderCards\(\)\{.*?\n  \}\n  function renderTimeline\(\)","  function renderCards(){const box=$e('externalEventCards');if(box)box.innerHTML='';}\n  function renderTimeline()",s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'renderCards replacement mismatch: {n}')

p.write_text(s,encoding='utf-8')
print('patched v4.7: removed duplicate event card list; timeline remains the only event display')
# workflow trigger v47
