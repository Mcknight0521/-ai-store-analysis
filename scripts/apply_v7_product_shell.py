from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
base_css='<link rel="stylesheet" href="assets/opspilot-v7.css?v=11.0.0">'
structure_css='<link rel="stylesheet" href="assets/opspilot-structure.css?v=12.0.0">'
display_css='<link rel="stylesheet" href="assets/opspilot-display.css?v=14.0.0">'
js='<script src="assets/opspilot-v7.js?v=14.0.0"></script>'
import re
s=re.sub(r'\n?<link rel="stylesheet" href="assets/opspilot-v7\.css\?v=[^"]+">','',s)
s=re.sub(r'\n?<link rel="stylesheet" href="assets/opspilot-structure\.css\?v=[^"]+">','',s)
s=re.sub(r'\n?<link rel="stylesheet" href="assets/opspilot-display\.css\?v=[^"]+">','',s)
s=re.sub(r'\n?<script src="assets/opspilot-v7\.js\?v=[^"]+"></script>','',s)
s=s.replace('</head>',base_css+'\n'+structure_css+'\n'+display_css+'\n</head>',1)
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('OpsPilot full six-page UI rebuild linked; core business logic untouched')
