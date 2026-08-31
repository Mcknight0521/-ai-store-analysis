from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

style='''\n<style id="event-ui-v46">\n/* One date = one event row/card. Severity is driven only by closure/typhoon; festivals are supporting context. */\n.event-day.closure-full,.event-card.closure-full{border-color:#F3A6AA!important;background:#FFF4F4!important;box-shadow:0 7px 22px rgba(198,61,61,.10)}\n.event-day.closure-partial,.event-card.closure-partial{border-color:#F3C786!important;background:#FFF9EF!important}\n.event-day.typhoon-only,.event-card.typhoon-only{border-color:#BFD3FF!important;background:#F6F9FF!important}\n.event-day.festival-only,.event-card.festival-only{border-color:#E6EBF1!important;background:#fff!important}\n.event-day.closure-full .date,.event-card.closure-full h4{color:#B4232D!important}\n.event-day.closure-partial .date,.event-card.closure-partial h4{color:#9A5B00!important}\n.event-day.typhoon-only .date,.event-card.typhoon-only h4{color:#245EA8!important}\n.event-pin.closure-full{color:#B4232D!important;background:#FFE1E3;border-radius:999px;padding:5px 8px}\n.event-pin.closure-partial{color:#9A5B00!important;background:#FFF0D5;border-radius:999px;padding:5px 8px}\n.event-pin.typhoon{color:#245EA8!important;background:#EAF1FF;border-radius:999px;padding:5px 8px}\n.event-pin.festival{color:#667085!important;background:#F2F4F7;border-radius:999px;padding:5px 8px}\n.event-card.daily-event{padding:16px 17px}.event-card.daily-event h4{margin:8px 0 5px;font-size:16px;line-height:1.35}.event-card.daily-event p{margin:0;color:#667085;font-size:12px;line-height:1.55}.event-card.daily-event .daily-tags{display:flex;gap:6px;flex-wrap:wrap}\n.event-day .event-main .event-secondary .event-pin{font-size:12px!important;line-height:1.25}.event-day .event-main .event-secondary .event-pin svg{width:12px!important;height:12px!important}.event-day .date{font-size:13px!important}.event-day .event-main small{font-size:10px!important}.event-day .event-main .sales-primary span{font-size:10px!important}\n@media(max-width:760px){.event-day{grid-template-columns:54px minmax(0,1fr) auto!important;padding:15px 12px!important}.event-day .date{font-size:14px!important}.event-day .event-main .event-secondary{gap:6px!important;margin-top:7px!important}.event-day .event-main .event-secondary .event-pin{font-size:12px!important;font-weight:900!important}.event-card.daily-event h4{font-size:17px}.event-card.daily-event p{font-size:12px}}\n</style>\n'''
if 'id="event-ui-v46"' not in s:
    s=s.replace('</head>',style+'</head>',1)

new_cards=r'''  function renderCards(){
    const box=$e('externalEventCards');if(!box)return;
    const hm=historyByDate(),cards=[];
    analysisDates().forEach(x=>{
      const day=iso(x.date),festival=festivalForDate(x.date);
      const history=(hm.get(day)||[]).filter(e=>e.type!=='climate');
      const closures=history.filter(e=>e.type==='closure');
      const typhoons=history.filter(e=>e.type==='typhoon');
      if(!festival&&!closures.length&&!typhoons.length)return;
      const hasFull=closures.some(e=>normalizeClosureScope(e.scope)==='full');
      const hasPartial=!hasFull&&closures.some(e=>normalizeClosureScope(e.scope)==='partial');
      const severity=hasFull?'closure-full':hasPartial?'closure-partial':typhoons.length?'typhoon-only':'festival-only';
      const tags=[];
      if(hasFull)tags.push(eventPin('全縣停班停課','closure-full'));
      else if(hasPartial)tags.push(eventPin('部分地區停班停課','closure-partial'));
      else if(closures.length)tags.push(eventPin('停班停課','closure-partial'));
      typhoons.forEach(e=>tags.push(eventPin(e.name||'颱風影響','typhoon')));
      if(festival)tags.push(eventPin(festival.name,'festival'));
      const headline=hasFull?`${state.region}｜全縣停班停課`:hasPartial?`${state.region}｜部分地區停班停課`:typhoons.length?(typhoons[0].name||'颱風影響'):festival.name;
      cards.push(`<div class="event-card daily-event ${severity}"><div class="daily-tags">${tags.join('')}</div><h4>${esc2(headline)}</h4><p>${day.slice(5).replace('-','/')} · 當日事件合併顯示</p></div>`);
    });
    if(cards.length){box.innerHTML=cards.join('');return}
    if(state.failedSources.length){box.innerHTML=`<div class="empty warn-empty">部分外部資料讀取失敗（${esc2(state.failedSources.join('、'))}），目前不能判定為「無特殊事件」。節慶日曆仍正常。</div>`;return}
    box.innerHTML='<div class="empty">此資料期間沒有已辨識的特殊事件。</div>';
  }
'''

new_timeline=r'''  function renderTimeline(){
    const box=$e('salesEventTimeline');if(!box)return;const days=analysisDates();
    if(!days.length){box.innerHTML='<div class="empty">匯入含日期範圍的報表後，這裡會自動標示颱風、停班停課與節慶。</div>';return}
    const hm=historyByDate();
    const display=days.map(x=>({...x,festival:festivalForDate(x.date),history:(hm.get(iso(x.date))||[]).filter(e=>e.type!=='climate')})).filter(x=>x.festival||x.history.length).sort((a,b)=>a.date-b.date).slice(0,60);
    if(!display.length){if(state.failedSources.length){box.innerHTML=`<div class="empty warn-empty">部分外部資料讀取失敗（${esc2(state.failedSources.join('、'))}），暫時無法完整判定這段期間是否有特殊事件。</div>`}else{box.innerHTML='<div class="empty">此資料期間沒有已辨識的特殊事件。</div>'}return}
    box.innerHTML=display.map(x=>{
      const day=iso(x.date),labels=[],classes=['event-day'];
      const closures=x.history.filter(e=>e.type==='closure'),typhoons=x.history.filter(e=>e.type==='typhoon');
      const hasFull=closures.some(e=>normalizeClosureScope(e.scope)==='full');
      const hasPartial=!hasFull&&closures.some(e=>normalizeClosureScope(e.scope)==='partial');
      if(hasFull){labels.push(eventPin('全縣停班停課','closure-full'));classes.push('closure-full')}
      else if(hasPartial){labels.push(eventPin('部分地區停班停課','closure-partial'));classes.push('closure-partial')}
      else if(closures.length){labels.push(eventPin('停班停課','closure-partial'));classes.push('closure-partial')}
      typhoons.forEach(e=>labels.push(eventPin(e.name||'颱風影響','typhoon')));
      if(!closures.length&&typhoons.length)classes.push('typhoon-only');
      if(x.festival){labels.push(eventPin(x.festival.name,'festival'));if(!closures.length&&!typhoons.length)classes.push('festival-only')}
      const joined=labels.join('<span class="event-plus">＋</span>');
      if(!x.hasSales)return `<div class="${classes.join(' ')}"><div class="date">${day.slice(5).replace('-','/')}</div><div class="event-main"><div class="event-secondary">${joined}</div><small>當日事件</small></div><div class="delta">—</div></div>`;
      const delta=x.baseline==null?'—':`${x.delta>=0?'+':''}${(x.delta*100).toFixed(1)}%`,deltaClass=x.delta>0?'up':x.delta<0?'down':'';
      return `<div class="${classes.join(' ')}"><div class="date">${day.slice(5).replace('-','/')}</div><div class="event-main"><div class="sales-primary"><strong>${money(x.sales)}</strong><span>營業額</span></div><div class="event-secondary">${joined}</div><small>${x.baseline!=null?`平常 ${money(x.baseline)}`:'當日事件'}</small></div><div class="delta ${deltaClass}">${delta}</div></div>`;
    }).join('');
  }
'''

s,n=re.subn(r"  function renderCards\(\)\{.*?\n  \}\n  function renderTimeline\(\)\{.*?\n  \}\n  function eventPromiseTimeout",new_cards+new_timeline+'  function eventPromiseTimeout',s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'event render replacement mismatch: {n}')

s=s.replace("setStatus('ok',`事件資料已載入 · ${state.region} · 停班停課 ${c} 筆${closureBreakdown} · 豪雨以上 ${rain} 筆 · 在地影響颱風 ${t} 筆`);","setStatus('ok',`事件資料已載入 · ${state.region} · 停班停課 ${c} 筆${closureBreakdown} · 颱風影響 ${t} 筆`);",1)

p.write_text(s,encoding='utf-8')
print('patched event UI v4.6: daily merged labels, closure severity, no rain labels')
# workflow trigger
