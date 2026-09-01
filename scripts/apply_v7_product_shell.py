from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
patterns=[r'\n?<link rel="stylesheet" href="assets/opspilot-v7\.css\?v=[^"]+">',r'\n?<link rel="stylesheet" href="assets/opspilot-structure\.css\?v=[^"]+">',r'\n?<link rel="stylesheet" href="assets/opspilot-display\.css\?v=[^"]+">',r'\n?<link rel="stylesheet" href="assets/opspilot-rebuild\.css\?v=[^"]+">',r'\n?<link rel="stylesheet" href="assets/opspilot-ux-v16\.css\?v=[^"]+">',r'\n?<link rel="stylesheet" href="assets/opspilot-v17\.css\?v=[^"]+">',r'\n?<link rel="stylesheet" href="assets/opspilot-v17-fix\.css\?v=[^"]+">',r'\n?<script src="assets/opspilot-v7\.js\?v=[^"]+"></script>',r'\n?<script src="assets/opspilot-rebuild\.js\?v=[^"]+"></script>',r'\n?<script src="assets/opspilot-scrollfix\.js\?v=[^"]+"></script>',r'\n?<script src="assets/opspilot-eventfix\.js\?v=[^"]+"></script>',r'\n?<script src="assets/opspilot-ux-v16\.js\?v=[^"]+"></script>',r'\n?<script src="assets/opspilot-v17\.js\?v=[^"]+"></script>']
for pattern in patterns:s=re.sub(pattern,'',s)
css='<link rel="stylesheet" href="assets/opspilot-rebuild.css?v=15.0.1">\n<link rel="stylesheet" href="assets/opspilot-ux-v16.css?v=16.0.0">\n<link rel="stylesheet" href="assets/opspilot-v17.css?v=17.0.0">\n<link rel="stylesheet" href="assets/opspilot-v17-fix.css?v=17.2.0">'
js='<script src="assets/opspilot-rebuild.js?v=15.0.2"></script>\n<script src="assets/opspilot-scrollfix.js?v=15.0.4"></script>\n<script src="assets/opspilot-ux-v16.js?v=16.0.0"></script>\n<script src="assets/opspilot-v17.js?v=17.4.0"></script>'
s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('OpsPilot v17.4 linked: instant overview numbers after import')
