'use client';

import {useEffect, useState} from 'react';
import Link from 'next/link';
import {AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer} from 'recharts';
import {fetchHistory, fetchHistorySources, HistoryResponse, HistorySource, triggerScrapeTaskApi, triggerRetrainTaskApi} from '@/lib/api';
import {getUser} from '@/lib/auth';
import JobStatus, {useBackgroundJob} from '@/components/dashboard/JobStatus';

function localDate(offset = 0) {
  const day = new Date(); day.setDate(day.getDate() + offset);
  return `${day.getFullYear()}-${String(day.getMonth()+1).padStart(2,'0')}-${String(day.getDate()).padStart(2,'0')}`;
}
const input = 'rounded-xl border border-border-subtle bg-white px-3 py-2 text-sm';
const provenanceLabel: Record<string,string> = {collected:'Thu thập từ nguồn',reviewed:'Admin xác nhận',unverified:'Chưa xác minh'};
const formatPrice = (value:number) => value.toLocaleString('vi-VN',{maximumFractionDigits:0});
const formatCompactPrice = (value:number) => new Intl.NumberFormat('vi-VN',{notation:'compact',maximumFractionDigits:1}).format(value);
const formatChartDate = (value:string) => {
  const [year,month,day] = value.split('-');
  return day && month && year ? `${day}/${month}` : value;
};
const formatFullDate = (value:string) => {
  const [year,month,day] = value.split('-');
  return day && month && year ? `${day}/${month}/${year}` : value;
};

export default function HistoryPage() {
  const [sources,setSources] = useState<HistorySource[]>([]);
  const [commodityId,setCommodityId] = useState(2);
  const [start,setStart] = useState(localDate(-89));
  const [end,setEnd] = useState(localDate());
  const [includeUnverified,setIncludeUnverified] = useState(false);
  const [data,setData] = useState<HistoryResponse|null>(null);
  const [error,setError] = useState('');
  const [loading,setLoading] = useState(true);
  const [busy,setBusy] = useState(false);
  const [admin,setAdmin] = useState(false);
  const [revision,setRevision] = useState(0);
  const [page,setPage] = useState(0);
  const scrape = useBackgroundJob('scrape', () => setRevision(v=>v+1), admin);
  const retrain = useBackgroundJob('retrain', () => setRevision(v=>v+1), admin);
  const running = busy || scrape.running || retrain.running;
  useEffect(()=>{
    setAdmin(getUser()?.role === 'admin');
    const id = Number(new URLSearchParams(window.location.search).get('commodity_id'));
    if(id > 0) setCommodityId(id);
    fetchHistorySources().then(setSources).catch(e=>setError(e.message));
  },[]);
  useEffect(()=>{
    let cancelled = false;
    setLoading(true); setData(null); setPage(0); setError('');
    fetchHistory(commodityId,start,end,includeUnverified).then(d=>{if(!cancelled)setData(d);})
      .catch(e=>{if(!cancelled)setError(e.message);}).finally(()=>{if(!cancelled)setLoading(false);});
    return ()=>{cancelled=true;};
  },[commodityId,start,end,includeUnverified,revision]);
  const source = sources.find(s=>s.id===commodityId);
  const chart = [...(data?.records.map(r=>({date:r.date,price:r.price})) || []),...(data?.missing_dates.map(date=>({date,price:null})) || [])].sort((a,b)=>a.date.localeCompare(b.date));
  const chartStats = data?.records.length ? (()=>{
    const first=data.records[0];
    const last=data.records[data.records.length-1];
    const prices=data.records.map(r=>r.price);
    const change=first.price ? ((last.price-first.price)/first.price)*100 : 0;
    return {first,last,min:Math.min(...prices),max:Math.max(...prices),change};
  })() : null;
  async function collect() {
    setBusy(true); setError('');
    try {scrape.begin(await triggerScrapeTaskApi(30,{commodity_id:commodityId,start_date:start,end_date:end}));}
    catch(e){setError(e instanceof Error?e.message:'Không thu thập được dữ liệu');} finally{setBusy(false);}
  }
  async function train() {
    setBusy(true); setError('');
    try {retrain.begin(await triggerRetrainTaskApi(commodityId));}
    catch(e){setError(e instanceof Error?e.message:'Không huấn luyện được');} finally{setBusy(false);}
  }
  function exportCsv() {
    if(!data) return;
    const escape = (value:unknown) => '"'+String(value??'').replace(/"/g,'""')+'"';
    const rows = source?.kind === 'periodic'
      ? [['period_start','period_end','published_date','buying_price','selling_price','unit','market','specification','source'],...data.periodic_records.map(r=>[r.start,r.end,r.published_date,r.buying_price,r.selling_price,r.unit,r.market,r.specification,r.source])]
      : [['record_date','commodity_code','price','unit','source','provenance','market','price_type'],...data.records.map(r=>[r.date,source?.code,r.price,source?.unit,r.source,r.provenance,r.source_details?.market,r.source_details?.price_type])];
    const csv = rows.map(row=>row.map(escape).join(',')).join('\r\n');
    const url=URL.createObjectURL(new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8'}));
    const a=document.createElement('a');a.href=url;a.download=`lich-su-${source?.code}-${start}-${end}.csv`;a.click();URL.revokeObjectURL(url);
  }
  return <div className="space-y-5">
    <div><h1 className="text-2xl font-bold">Lịch sử giá nông sản</h1><p className="text-secondary-text">1. Thu thập quá khứ → 2. Kiểm tra lịch sử → 3. Huấn luyện → 4. Xem dự báo</p></div>
    {error&&<p role="alert" className="p-4 bg-rose-50 text-rose-700 rounded-xl">{error}</p>}
    <section className="p-5 bg-white border border-border-subtle rounded-2xl space-y-4">
      <div className="flex flex-wrap gap-4">
        <label>Nông sản<br/><select aria-label="Nông sản" className={input} value={commodityId} onChange={e=>setCommodityId(Number(e.target.value))}>{sources.map(s=><option key={s.id} value={s.id}>{s.name} ({s.unit})</option>)}</select></label>
        <label>Từ ngày<br/><input className={input} type="date" value={start} max={end} onChange={e=>setStart(e.target.value)}/></label>
        <label>Đến ngày<br/><input className={input} type="date" value={end} min={start} max={localDate()} onChange={e=>setEnd(e.target.value)}/></label>
        <div className="flex gap-2 items-end">{[30,90,365].map(days=><button className={input} key={days} onClick={()=>{setStart(localDate(1-days));setEnd(localDate());}}>{days} ngày</button>)}</div>
      </div>
      <p className="text-sm text-secondary-text">{source?.limitation} {source?.source_url&&<a className="text-brand underline" href={source.source_url} target="_blank" rel="noreferrer">Mở nguồn</a>}</p>
      {source?.suggested_start && <button className={input} onClick={()=>{setStart(source.suggested_start!);setEnd(localDate());}}>Xem từ mốc nguồn có lịch sử ({source.suggested_start})</button>}
      <label className="block text-sm"><input type="checkbox" checked={includeUnverified} onChange={e=>setIncludeUnverified(e.target.checked)}/> Hiển thị thêm dữ liệu cũ/chưa xác minh (không dùng huấn luyện)</label>
      <div className="flex gap-3 flex-wrap">
        {admin&&<><button disabled={running||!source?.automatic||loading||!data} onClick={collect} className="bg-brand text-white rounded-xl px-4 py-2 disabled:opacity-40">Thu thập khoảng đã chọn</button>
        <button disabled={running||!data?.readiness.ready||loading} onClick={train} className="bg-brand text-white rounded-xl px-4 py-2 disabled:opacity-40">Huấn luyện từ toàn bộ lịch sử đủ điều kiện</button></>}
        <Link className={input} href={`/forecast?commodity_id=${commodityId}`}>Xem dự báo →</Link>
        <button className={input} disabled={source?.kind==='periodic'?!data?.periodic_records.length:!data?.records.length} onClick={exportCsv}>{source?.kind==='periodic'?'Xuất báo cáo theo kỳ CSV':'Xuất lịch sử CSV'}</button>
      </div>
      {admin&&<p className="text-xs text-secondary-text">CSV để huấn luyện: commodity_code, record_date, price, source, reviewed=true (chỉ xác nhận sau khi đối chiếu nguồn). <Link href="/dashboard/data-control" className="underline">Nhập CSV</Link></p>}
    </section>
    {admin&&<><JobStatus job={scrape.job} error={scrape.error}/><JobStatus job={retrain.job} error={retrain.error}/></>}
    {loading&&<p role="status">Đang tải lịch sử…</p>}
    {data&&<>
      {source?.kind==='periodic'&&<section className="p-5 bg-white border border-border-subtle rounded-2xl space-y-3 overflow-x-auto">
        <h2 className="font-bold">Lịch sử giá mía theo kỳ công bố</h2>
        <p className="text-sm text-secondary-text">Giá mua và giá bán là hai loại giá riêng, không phải cận thấp/cao. Mỗi báo cáo giữ nguyên kỳ thời gian; không nhân thành quan sát từng ngày và không đưa vào mô hình dự báo ngày.</p>
        {data.periodic_records.length===0?<p>Chưa có báo cáo trong khoảng đã chọn. Chọn mốc nguồn năm 2024 và thu thập để xem các kỳ đã tích hợp.</p>:<table className="w-full text-sm text-left"><thead><tr>{['Kỳ giá','Ngày công bố','Giá mua','Giá bán','Quy cách / địa bàn','Nguồn'].map(h=><th className="p-3" key={h}>{h}</th>)}</tr></thead><tbody>{data.periodic_records.map(r=><tr key={r.id} className="border-t border-border-subtle"><td className="p-3">{r.start} → {r.end}</td><td className="p-3">{r.published_date}</td><td className="p-3">{r.buying_price.toLocaleString('vi-VN')} {r.unit}</td><td className="p-3">{r.selling_price.toLocaleString('vi-VN')} {r.unit}</td><td className="p-3">{r.specification}<br/>{r.market}</td><td className="p-3"><a className="underline text-brand" href={r.source} target="_blank" rel="noreferrer">{r.attribution}</a></td></tr>)}</tbody></table>}
      </section>}
      {(source?.kind!=='periodic'||data.records.length>0)&&<>
      <section className="grid sm:grid-cols-3 gap-3">{[
        ['Ngày có dữ liệu trong khoảng',data.records.length],['Ngày thiếu trong khoảng',data.missing_dates.length],['Bản ghi chưa xác minh',data.unverified_count]
      ].map(([label,value])=><div key={label} className="p-4 bg-white rounded-xl border border-border-subtle"><p className="text-sm text-secondary-text">{label}</p><strong className="text-2xl">{value}</strong></div>)}</section>
      <p className="p-4 rounded-xl bg-brand/10">{data.readiness.ready?`Đủ điều kiện huấn luyện: ${data.readiness.observation_count} ngày từ ${data.readiness.start_date} đến ${data.readiness.end_date}.`:data.readiness.reason} Bộ lọc chỉ giới hạn phần xem/thu thập; huấn luyện dùng toàn bộ lịch sử có nguồn. Ngày thiếu không được coi là giá quan sát.</p>
      <section className="p-5 sm:p-6 bg-white rounded-2xl border border-border-subtle shadow-card overflow-hidden">
        <div className="flex flex-col xl:flex-row xl:items-start xl:justify-between gap-5 pb-5 border-b border-border-subtle">
          <div>
            <div className="flex items-center gap-2"><span className="w-2.5 h-2.5 rounded-full bg-brand shadow-[0_0_0_5px_rgba(78,113,82,0.12)]"/><h2 className="font-bold text-lg text-primary-text">Biến động giá lịch sử</h2></div>
            <p className="mt-1.5 text-sm text-secondary-text">{source?.name} · Đơn vị {source?.unit} · {data.records.length} ngày có giá</p>
          </div>
          {chartStats&&<div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 min-w-0 xl:min-w-[600px]">
            {[
              ['Đầu kỳ',formatPrice(chartStats.first.price),formatFullDate(chartStats.first.date)],
              ['Cuối kỳ',formatPrice(chartStats.last.price),formatFullDate(chartStats.last.date)],
              ['Thấp nhất',formatPrice(chartStats.min),'Trong khoảng chọn'],
              ['Cao nhất',formatPrice(chartStats.max),'Trong khoảng chọn']
            ].map(([label,value,note])=><div key={label} className="rounded-xl border border-border-subtle bg-canvas/70 px-3 py-2.5"><p className="text-[10px] uppercase tracking-wider font-bold text-secondary-text">{label}</p><p className="mt-0.5 font-mono font-bold text-primary-text truncate">{value}</p><p className="text-[10px] text-secondary-text truncate">{note}</p></div>)}
          </div>}
        </div>
        {data.records.length&&chartStats?<>
          <div className="flex flex-wrap items-center justify-between gap-3 pt-5">
            <div><p className="text-xs text-secondary-text">Thay đổi từ đầu đến cuối kỳ</p><p className={`text-xl font-bold font-mono ${chartStats.change>0?'text-emerald-700':chartStats.change<0?'text-rose-600':'text-secondary-text'}`}>{chartStats.change>0?'+':''}{chartStats.change.toLocaleString('vi-VN',{minimumFractionDigits:2,maximumFractionDigits:2})}%</p></div>
            <div className="flex items-center gap-2 text-xs text-secondary-text"><span className="w-6 h-0.5 rounded bg-brand"/>Giá công bố<span className="ml-2 w-2 h-2 rounded-full border-2 border-brand bg-white"/>Điểm dữ liệu</div>
          </div>
          <div className="mt-3 h-[360px] rounded-2xl bg-gradient-to-b from-brand-light/65 via-white to-white px-1 py-4 sm:px-3">
            <ResponsiveContainer width="100%" height="100%"><AreaChart data={chart} margin={{top:8,right:12,left:8,bottom:0}}>
              <defs><linearGradient id="historyPriceFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#4E7152" stopOpacity={0.3}/><stop offset="70%" stopColor="#4E7152" stopOpacity={0.05}/><stop offset="100%" stopColor="#4E7152" stopOpacity={0}/></linearGradient></defs>
              <CartesianGrid vertical={false} stroke="#E5E0D8" strokeDasharray="4 6"/>
              <XAxis dataKey="date" tickFormatter={formatChartDate} minTickGap={42} axisLine={false} tickLine={false} tick={{fill:'#8D7B68',fontSize:11}} dy={10}/>
              <YAxis domain={['auto','auto']} tickFormatter={(value:number)=>formatCompactPrice(value)} axisLine={false} tickLine={false} tick={{fill:'#8D7B68',fontSize:11}} width={58}/>
              <Tooltip cursor={{stroke:'#9C6644',strokeWidth:1,strokeDasharray:'4 4'}} labelFormatter={(label)=>`Ngày ${formatFullDate(String(label))}`} formatter={(value)=>[`${formatPrice(Number(value))} ${source?.unit}`,'Giá']} contentStyle={{border:'1px solid #E5E0D8',borderRadius:14,boxShadow:'0 10px 30px rgba(45,35,30,.12)',fontSize:12}} labelStyle={{color:'#2D231E',fontWeight:700,marginBottom:4}}/>
              <Area type="monotone" dataKey="price" name="Giá" stroke="#4E7152" strokeWidth={3} fill="url(#historyPriceFill)" dot={data.records.length<=60?{r:2.5,fill:'#fff',stroke:'#4E7152',strokeWidth:2}:false} activeDot={{r:5,fill:'#4E7152',stroke:'#fff',strokeWidth:3}} connectNulls={false} isAnimationActive={false}/>
            </AreaChart></ResponsiveContainer>
          </div>
          <p className="mt-3 text-xs text-secondary-text">Khoảng trống trên đường biểu diễn là ngày nguồn không công bố giá; hệ thống không tự tạo giá thay thế trên biểu đồ.</p>
        </>:<div className="mt-5 rounded-xl border border-dashed border-border-strong bg-canvas/60 p-10 text-center text-secondary-text">Chưa có dữ liệu phù hợp. Hãy thu thập hoặc nhập lịch sử có nguồn.</div>}
        <details className="text-sm mt-4 rounded-xl border border-border-subtle bg-canvas/50 px-4 py-3"><summary className="cursor-pointer font-semibold text-primary-text">Xem {data.missing_dates.length} ngày không có công bố</summary><p className="max-h-32 overflow-auto mt-3 text-xs leading-6 text-secondary-text">{data.missing_dates.join(', ')||'Không có ngày thiếu.'}</p></details>
      </section>
      <section className="p-5 bg-white rounded-2xl border border-border-subtle overflow-x-auto"><table className="w-full text-sm text-left"><thead><tr>{['Ngày','Giá','Nguồn / thị trường','Trạng thái'].map(h=><th key={h} className="p-3">{h}</th>)}</tr></thead><tbody>{[...data.records].reverse().slice(page*30,(page+1)*30).map(r=><tr key={r.id} className="border-t border-border-subtle"><td className="p-3">{r.date}</td><td className="p-3">{r.price.toLocaleString('vi-VN')} {source?.unit}</td><td className="p-3">{/^https?:\/\//.test(r.source)?<a className="text-brand underline" href={r.source} target="_blank" rel="noreferrer">Xem nguồn công bố</a>:r.source}{r.source_details&&<span className="block text-xs text-secondary-text mt-1">{[r.source_details.product,r.source_details.market,r.source_details.price_type].filter(Boolean).join(' · ')}</span>}</td><td className="p-3">{provenanceLabel[r.provenance]||r.provenance}</td></tr>)}</tbody></table>
        <div className="flex gap-4 items-center mt-3"><button className={input} disabled={page===0} onClick={()=>setPage(p=>p-1)}>Trước</button><span>Trang {page+1}/{Math.max(1,Math.ceil(data.records.length/30))}</span><button className={input} disabled={(page+1)*30>=data.records.length} onClick={()=>setPage(p=>p+1)}>Sau</button></div>
      </section>
      </>}
    </>}
  </div>;
}
