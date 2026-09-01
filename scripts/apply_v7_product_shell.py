from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
css='<link rel="stylesheet" href="assets/opspilot-v7.css?v=9.0.0">'
js='<script src="assets/opspilot-v7.js?v=9.0.0"></script>'
import re
s=re.sub(r'\n?<link rel="stylesheet" href="assets/opspilot-v7\.css\?v=[^"]+">','',s)
s=re.sub(r'\n?<script src="assets/opspilot-v7\.js\?v=[^"]+"></script>','',s)
s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('OpsPilot v9 distinct application shell linked; core logic untouched')
