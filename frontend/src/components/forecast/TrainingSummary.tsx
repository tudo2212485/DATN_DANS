import Link from 'next/link';
import {TrainingMetadata} from '@/lib/api';

export default function TrainingSummary({training,commodityId,rmse}:{training:TrainingMetadata;commodityId:number;rmse:number}) {
  const unit = training.cadence === 'periodic' ? 'kỳ báo cáo' : training.cadence === 'irregular' ? 'mốc công bố' : 'ngày có quan sát';
  return <section className="p-5 rounded-2xl bg-brand/10 space-y-2 text-sm">
    <h2 className="font-bold">Dự báo này được tạo từ lịch sử nào?</h2>
    <p>{training.observation_count} {unit}: <strong>{training.start_date} → {training.end_date}</strong>. Huấn luyện lúc {new Date(training.trained_at).toLocaleString('vi-VN')}.</p>
    <p>Biến mục tiêu: <strong>{training.target || 'Giá công bố'}</strong>. Kiểm thử: {training.test_start} → {training.test_end} ({training.test_count} {unit}). {training.evaluation}</p>
    <p>RMSE của cách giữ nguyên giá cuối cùng: <strong>{training.baseline.rmse.toLocaleString('vi-VN')}</strong>. Mô hình hiện tại {rmse < training.baseline.rmse ? 'có sai số thấp hơn' : 'chưa tốt hơn'} cách đơn giản này trên tập kiểm thử.</p>
    <p>{training.cadence === 'periodic' ? 'Không biến báo cáo theo kỳ thành giá quan sát hằng ngày.' : training.cadence === 'irregular' ? 'Mô hình học theo thứ tự các mốc công bố; không tự tạo giá cho ngày nguồn không công bố.' : `${training.filled_days} ngày thiếu được điền bằng giá đã biết trước đó; không tính các ngày điền vào sai số kiểm thử.`} {training.interval_note}</p>
    {training.stale_days>1&&<p className="text-amber-800">Mốc lịch sử cuối cách hiện tại {training.stale_days} ngày. Dự báo bắt đầu sau mốc đó; hãy cập nhật dữ liệu nếu cần dự báo sát hiện tại.</p>}
    <Link className="underline text-brand" href={`/history?commodity_id=${commodityId}`}>Xem bảng và biểu đồ lịch sử →</Link>
  </section>;
}
