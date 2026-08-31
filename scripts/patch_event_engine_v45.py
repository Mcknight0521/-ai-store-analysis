from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    actual=s.count(old)
    if actual!=count:
        raise SystemExit(f'replacement mismatch: expected {count}, found {actual}: {old[:90]}')
    s=s.replace(old,new)

rep('營業額為主；依匯入日期自動補上節慶、歷史颱風與停班停課。','營業額為主；依完整日期與地區，自動補上節慶、豪雨／大豪雨、實際影響颱風與停班停課。')
rep('事件層會依報表日期自動回查；營運影響優先顯示停班停課與颱風，節慶僅作輔助。','事件層以 YYYY-MM-DD ＋地區精準比對；優先顯示停班停課、豪雨／大豪雨與有實際在地影響的颱風，節慶僅作輔助；強風不顯示。')
rep("const start=iso(range.start),end=iso(range.end),key=`opsOfficialEventsV44:${state.region}:${start}:${end}`;","const start=iso(range.start),end=iso(range.end),key=`opsOfficialEventsV45:${state.region}:${start}:${end}`;")
rep("events:events.filter(e=>e&&['closure','typhoon'].includes(e.type)&&typeof e.date==='string'),","events:events.filter(e=>e&&['closure','typhoon'].includes(e.type)&&/^\\d{4}-\\d{2}-\\d{2}$/.test(String(e.date||''))),")
rep("function allowedHistoryEvent(e){return !!e&&['closure','typhoon'].includes(e.type)}","function allowedHistoryEvent(e){return !!e&&['closure','typhoon','climate'].includes(e.type)&&/^\\d{4}-\\d{2}-\\d{2}$/.test(String(e.date||''))}")
rep("    groupHistory('typhoon').forEach(g=>cards.push(`<div class=\"event-card typhoon\"><span class=\"tag\">${eventPin('颱風','typhoon')}</span><h4>${esc2(g.name)}</h4><p>${iso(g.start).slice(5).replace('-','/')}－${iso(g.end).slice(5).replace('-','/')}</p><strong>${g.days} 天</strong><small class=\"source-note\">${esc2(g.source)}</small></div>`));\n    groupHistory('closure').forEach", "    groupHistory('typhoon').forEach(g=>cards.push(`<div class=\"event-card typhoon\"><span class=\"tag\">${eventPin('颱風','typhoon')}</span><h4>${esc2(g.name)}</h4><p>${iso(g.start).slice(5).replace('-','/')}－${iso(g.end).slice(5).replace('-','/')}</p><strong>${g.days} 天</strong><small class=\"source-note\">${esc2(g.source)}</small></div>`));\n    groupHistory('climate').forEach(g=>cards.push(`<div class=\"event-card climate\"><span class=\"tag\">${eventPin('豪雨','climate')}</span><h4>${esc2(g.name)}</h4><p>${iso(g.start).slice(5).replace('-','/')}${g.days>1?'－'+iso(g.end).slice(5).replace('-','/') : ''}</p><strong>${g.days} 天</strong><small class=\"source-note\">${esc2(g.source)}</small></div>`));\n    groupHistory('closure').forEach")
rep("const ordered=[...x.history].sort((a,b)=>({closure:0,typhoon:1}[a.type]??9)-({closure:0,typhoon:1}[b.type]??9));ordered.forEach(e=>{const label=e.type==='closure'?closureDisplayName(e):e.name;labels.push(eventPin(label,e.type));classes.push(e.type)});", "const ordered=[...x.history].sort((a,b)=>({closure:0,climate:1,typhoon:2}[a.type]??9)-({closure:0,climate:1,typhoon:2}[b.type]??9));ordered.forEach(e=>{const label=e.type==='closure'?closureDisplayName(e):e.name;labels.push(eventPin(label,e.type));classes.push(e.type)});")
rep("      const [closures,typhoons]=await Promise.all([loadHistoricalClosures(range,force),loadHistoricalTyphoons(range,force)]);\n      if(token!==state.syncToken)return;\n      state.historyEvents=[...closures,...typhoons];state.lastSync=new Date();state.status='success';renderCards();renderTimeline();\n      const c=closures.length,t=typhoons.length,partial=closures.filter(e=>normalizeClosureScope(e.scope)==='partial').length,full=closures.filter(e=>normalizeClosureScope(e.scope)==='full').length;", "      const [closures,typhoonsRaw,climate]=await Promise.all([loadHistoricalClosures(range,force),loadHistoricalTyphoons(range,force),loadHistoricalClimate(range)]);\n      if(token!==state.syncToken)return;\n      // A typhoon warning is nationwide context, but the UI only promotes it when the selected region\n      // has concrete local impact on the same full date:停班停課 or 豪雨以上。This avoids unrelated typhoons.\n      const localImpactDates=new Set([...closures,...climate].map(e=>e.date));\n      const typhoons=typhoonsRaw.filter(e=>localImpactDates.has(e.date));\n      state.historyEvents=[...closures,...climate,...typhoons];state.lastSync=new Date();state.status='success';renderCards();renderTimeline();\n      const c=closures.length,t=typhoons.length,rain=climate.length,partial=closures.filter(e=>normalizeClosureScope(e.scope)==='partial').length,full=closures.filter(e=>normalizeClosureScope(e.scope)==='full').length;")
rep("      setStatus('ok',`官方資料已載入 · ${state.region} · 停班停課 ${c} 筆${closureBreakdown} · 颱風 ${t} 筆`);", "      setStatus('ok',`事件資料已載入 · ${state.region} · 停班停課 ${c} 筆${closureBreakdown} · 豪雨以上 ${rain} 筆 · 在地影響颱風 ${t} 筆`);")
rep("if(k&&k.startsWith('opsOfficialEventsV42:'))localStorage.removeItem(k)","if(k&&(k.startsWith('opsOfficialEventsV42:')||k.startsWith('opsOfficialEventsV44:')))localStorage.removeItem(k)")

p.write_text(s,encoding='utf-8')
print('patched index.html for event engine v4.5')
