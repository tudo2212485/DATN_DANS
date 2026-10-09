import Link from 'next/link';
import {TrainingMetadata} from '@/lib/api';
import {CalendarClock, CheckCircle2, Database, ExternalLink, TriangleAlert} from 'lucide-react';

export default function TrainingSummary({training,commodityId,rmse}:{training:TrainingMetadata;commodityId:number;rmse:number}) {
  const unit = training.cadence === 'periodic' ? 'kỳ báo cáo' : training.cadence === 'irregular' ? 'mốc công bố' : 'ngày có quan sát';
  const beatsBaseline=rmse<training.baseline.rmse;
  return <section className="rounded-2xl border border-brand/20 bg-brand/5 p-5 shadow-card">
    <div className="flex flex-col lg:flex-row lg:items-center gap-4">
      <div className="min-w-0 lg:flex-1"><p className="text-xs font-bold uppercase tracking-wider text-brand">Nguồn tạo dự báo</p><h2 className="mt-1 font-bold text-primary-text">{training.observation_count} {unit} từ {training.start_date} đến {training.end_date}</h2><p className="mt-1 text-xs text-secondary-text">Mục tiêu: {training.target || 'Giá công bố'} · Huấn luyện {new Date(training.trained_at).toLocaleString('vi-VN')}</p></div>
      <div className="grid grid-cols-2 gap-2 lg:w-[390px]">
        <div className="rounded-xl border border-border-subtle bg-white px-3 py-2"><div className="flex items-center gap-1.5 text-[10px] font-bold uppercase text-secondary-text"><Database className="w-3.5 h-3.5 text-brand"/>Tập kiểm thử</div><p className="mt-1 text-sm font-bold text-primary-text">{training.test_count} {unit}</p></div>
        <div className={`rounded-xl border px-3 py-2 ${beatsBaseline?'border-emerald-200 bg-emerald-50':'border-amber-200 bg-amber-50'}`}><div className="flex items-center gap-1.5 text-[10px] font-bold uppercase text-secondary-text">{beatsBaseline?<CheckCircle2 className="w-3.5 h-3.5 text-emerald-700"/>:<TriangleAlert className="w-3.5 h-3.5 text-amber-700"/>}So với baseline</div><p className="mt-1 text-sm font-bold text-primary-text">{beatsBaseline?'Tốt hơn':'Chưa tốt hơn'}</p></div>
      </div>
    </div>
    {training.stale_days>1&&<p className="mt-3 flex gap-2 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-800"><CalendarClock className="w-4 h-4 shrink-0"/>Dữ liệu cuối cách hiện tại {training.stale_days} ngày. Nên cập nhật lịch sử trước khi dùng kết quả để ra quyết định.</p>}
    <details className="mt-3 border-t border-brand/15 pt-3 text-xs text-secondary-text"><summary className="cursor-pointer font-bold text-primary-text">Xem cách hệ thống huấn luyện và kiểm thử</summary><div className="mt-2 space-y-1.5 leading-5"><p>Kiểm thử: {training.test_start} → {training.test_end}. {training.evaluation}</p><p>RMSE baseline: <strong>{training.baseline.rmse.toLocaleString('vi-VN')}</strong>. {training.cadence === 'periodic' ? 'Báo cáo theo kỳ được giữ nguyên.' : training.cadence === 'irregular' ? 'Mô hình học theo thứ tự mốc công bố và không tự tạo giá cho ngày trống.' : `${training.filled_days} ngày thiếu chỉ được điền cho đầu vào; không tính vào sai số kiểm thử.`} {training.interval_note}</p><Link className="inline-flex items-center gap-1 font-bold text-brand underline" href={`/history?commodity_id=${commodityId}`}>Mở bảng và biểu đồ lịch sử<ExternalLink className="w-3 h-3"/></Link></div></details>
  </section>;
}
