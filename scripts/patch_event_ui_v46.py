from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

changes=0

def replace_once(old,new,label):
    global s,changes
    if old in s:
        s=s.replace(old,new,1)
        changes+=1
        print('updated:',label)
    elif new in s:
        print('already applied:',label)
    else:
        raise SystemExit(f'missing expected source for {label}')

# Root cause hardening: old browser-local official-event caches may survive a corrected backend dataset.
# Move to a new cache namespace so stale closure records cannot reappear after the database is fixed.
replace_once(
    "const start=iso(range.start),end=iso(range.end),key=`opsOfficialEventsV45:${state.region}:${start}:${end}`;",
    "const start=iso(range.start),end=iso(range.end),key=`opsOfficialEventsV48:${state.region}:${start}:${end}`;",
    'official event cache namespace V48'
)

# Official event state must contain only official closure/typhoon records. Climate can still be used privately
# as supporting evidence for typhoon-local-impact filtering, but it must never become a visible/history event.
replace_once(
    "state.historyEvents=[...closures,...climate,...typhoons];",
    "state.historyEvents=[...closures,...typhoons];",
    'remove climate from visible history state'
)

replace_once(
    "function allowedHistoryEvent(e){return !!e&&['closure','typhoon','climate'].includes(e.type)&&/^\\d{4}-\\d{2}-\\d{2}$/.test(String(e.date||''))}",
    "function allowedHistoryEvent(e){return !!e&&['closure','typhoon'].includes(e.type)&&/^\\d{4}-\\d{2}-\\d{2}$/.test(String(e.date||''))}",
    'restrict visible history to closure and typhoon'
)

# Keep wording aligned with the product rule: only typhoon and closure are surfaced.
s=s.replace('same full date:停班停課 or 豪雨以上。This avoids unrelated typhoons.','same full date using local operational evidence. This avoids unrelated typhoons.')
s=s.replace(' · 豪雨以上 ${rain} 筆','')
s=s.replace(' · 在地影響颱風 ${t} 筆',' · 颱風影響 ${t} 筆')
s=s.replace(' · 颱風影響 ${t} 筆',' · 颱風影響 ${t} 筆')

# One-time purge of every older OpsPilot official-event cache namespace in the browser.
# This executes before future reads and prevents previously incorrect dates such as stale closure cards
# from being resurrected even if localStorage still contains an older payload.
marker='function purgeLegacyOfficialEventCachesV48()'
if marker not in s:
    anchor='  let officialEventRequest=null;\n'
    purge="""  function purgeLegacyOfficialEventCachesV48(){\n    try{\n      const remove=[];\n      for(let i=0;i<localStorage.length;i++){\n        const k=localStorage.key(i)||'';\n        if(/^opsOfficialEventsV(?:4[0-7]|[0-3]\\d):/.test(k))remove.push(k);\n      }\n      remove.forEach(k=>localStorage.removeItem(k));\n    }catch(e){}\n  }\n  purgeLegacyOfficialEventCachesV48();\n"""
    if anchor not in s:
        raise SystemExit('missing officialEventRequest anchor')
    s=s.replace(anchor,purge+anchor,1)
    changes+=1
    print('updated: purge legacy official event caches')
else:
    print('already applied: purge legacy official event caches')

p.write_text(s,encoding='utf-8')
print(f'patched v4.8 event-source hardening; changes={changes}')
# workflow trigger v48
