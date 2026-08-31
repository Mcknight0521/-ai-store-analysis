from pathlib import Path
import re
p=Path('index.html'); s=p.read_text(encoding='utf-8')
# Overview-only removal: delete the legacy loss breakdown panel and its dedicated presentation/runtime.
s=re.sub(r'\s*<section class="panel loss-split-v49" id="lossSplitPanel">.*?</section>\s*(?=<section class="page" id="anomaly")','\n    ',s,flags=re.S)
s=re.sub(r'\n?<style id="loss-split-v49-css">.*?</style>\n?','\n',s,flags=re.S)
s=re.sub(r'\n?<script id="loss-split-v49-js">.*?</script>\n?','\n',s,flags=re.S)
p.write_text(s,encoding='utf-8')
print('removed overview loss breakdown panel; analysis safe layer untouched')
