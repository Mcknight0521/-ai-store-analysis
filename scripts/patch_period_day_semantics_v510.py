from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
old="""   const miss=period.missingDates||[];
   const missText=miss.length?`<br><span style=\"font-weight:700;color:#C45555\">缺少 ${miss.map(d=>d.slice(5).replace('-','/')).join('、')}</span>`:'';
   const dayText=miss.length?`期間 ${period.days} 天・實際彙總 <strong>${period.aggregateDays} 天</strong>`:`${period.aggregateDays} 天彙總`;
   pb.innerHTML=`資料期間　<strong>${period.label}</strong>　・　${dayText}${missText}<br><span style=\"font-weight:500;color:#7A8699\">日均＝期間總額 ÷ ${period.aggregateDays} 個實際彙總日；缺少日期不視為 0。</span>`;
"""
new="""   const miss=period.missingDates||[];
   const validDates=[...new Set(rows.filter(r=>r.date instanceof Date&&!isNaN(r.date)).map(r=>`${r.date.getFullYear()}-${String(r.date.getMonth()+1).padStart(2,'0')}-${String(r.date.getDate()).padStart(2,'0')}`))];
   const hasDaily=validDates.length>0;
   const denom=hasDaily?validDates.length:period.days;
   period.displayDays=denom;
   const missText=hasDaily&&miss.length?`<br><span style=\"font-weight:700;color:#C45555\">缺少 ${miss.map(d=>d.slice(5).replace('-','/')).join('、')}</span>`:'';
   const dayText=hasDaily?`有效銷售日 <strong>${denom} 天</strong>`:`報表涵蓋 <strong>${period.days} 個曆日</strong>`;
   const note=hasDaily?`日均＝期間總額 ÷ ${denom} 個有實際資料的日期；缺少日期不視為 0。`:`區間日均＝期間總額 ÷ ${period.days} 個報表涵蓋日；此報表未提供逐日明細，無法確認各日期是否有銷售。`;
   pb.innerHTML=`資料期間　<strong>${period.label}</strong>　・　${dayText}${missText}<br><span style=\"font-weight:500;color:#7A8699\">${note}</span>`;
"""
if old not in s: raise SystemExit('period banner block not found')
s=s.replace(old,new,1)
old2="""function avgOverReportDays(value,rr=rows){
 const p=activePeriodInfo(rr);
 return value!=null&&p?.aggregateDays?value/p.aggregateDays:null;
}"""
new2="""function avgOverReportDays(value,rr=rows){
 const p=activePeriodInfo(rr);
 if(value==null||!p)return null;
 const validDates=[...new Set(rr.filter(r=>r.date instanceof Date&&!isNaN(r.date)).map(r=>`${r.date.getFullYear()}-${String(r.date.getMonth()+1).padStart(2,'0')}-${String(r.date.getDate()).padStart(2,'0')}`))];
 const days=validDates.length||p.days;
 return days?value/days:null;
}"""
if old2 not in s: raise SystemExit('average helper not found')
s=s.replace(old2,new2,1)
# Clarify average KPI labels depending on whether true daily rows exist.
needle=""" $('#ovSales').textContent=maybeMoney(a.sales);"""
insert=""" const hasDailyRows=rows.some(r=>r.date instanceof Date&&!isNaN(r.date));
 $('#ovAvgSales')?.previousElementSibling && ($('#ovAvgSales').previousElementSibling.textContent=hasDailyRows?'日均營業額':'區間日均營業額');
 $('#ovAvgQty')?.previousElementSibling && ($('#ovAvgQty').previousElementSibling.textContent=hasDailyRows?'日均銷售量':'區間日均銷售量');
 $('#ovAvgWaste')?.previousElementSibling && ($('#ovAvgWaste').previousElementSibling.textContent=hasDailyRows?'日均報廢':'區間日均報廢');
 $('#ovAvgClearance')?.previousElementSibling && ($('#ovAvgClearance').previousElementSibling.textContent=hasDailyRows?'日均出清':'區間日均出清');
 $('#ovSales').textContent=maybeMoney(a.sales);"""
if needle not in s: raise SystemExit('overview average anchor not found')
s=s.replace(needle,insert,1)
p.write_text(s,encoding='utf-8')
print('patched period day semantics v5.10')
