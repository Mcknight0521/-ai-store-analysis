from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
# 洞察頁不再重複顯示需改善商品；總覽保留唯一一份 Top 5。
if '#overview #priorityPanelV511{display:none!important}' not in s:
    s=s.replace('</head>','<style id="cleanup-v517-css">#overview #priorityPanelV511{display:none!important}</style></head>',1)
# 分析頁移除「區間商品 Top 10」，保留各分析區自己的 Top 10 與明細。
old="flow.innerHTML=intervalBlock()+section('sales',1,'營業額分析'"
new="flow.innerHTML=section('sales',1,'營業額分析'"
if old in s:
    s=s.replace(old,new,1)
else:
    print('note: interval render target not found or already removed')
p.write_text(s,encoding='utf-8')
print('v5.17 cleanup applied')
