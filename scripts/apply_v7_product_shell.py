from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove every prior presentation skin / renderer. Core inline app logic stays untouched.
patterns=[
 r'\n?<link rel="stylesheet" href="assets/opspilot-v7\.css\?v=[^"]+">',
 r'\n?<link rel="stylesheet" href="assets/opspilot-structure\.css\?v=[^"]+">',
 r'\n?<link rel="stylesheet" href="assets/opspilot-display\.css\?v=[^"]+">',
 r'\n?<link rel="stylesheet" href="assets/opspilot-rebuild\.css\?v=[^"]+">',
 r'\n?<script src="assets/opspilot-v7\.js\?v=[^"]+"></script>',
 r'\n?<script src="assets/opspilot-rebuild\.js\?v=[^"]+"></script>'
]
for pattern in patterns:s=re.sub(pattern,'',s)
css='<link rel="stylesheet" href="assets/opspilot-rebuild.css?v=15.0.1">'
js='<script src="assets/opspilot-rebuild.js?v=15.0.0"></script>'
s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('OpsPilot v15.0.1 mobile import drawer fix; core parser/judgement/formulas preserved')
