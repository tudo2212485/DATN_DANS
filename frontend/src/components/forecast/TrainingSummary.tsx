import Link from 'next/link';
import {TrainingMetadata} from '@/lib/api';

export default function TrainingSummary({training,commodityId,rmse}:{training:TrainingMetadata;commodityId:number;rmse:number}) {
  return <section className="p-5 rounded-2xl bg-brand/10 space-y-2 text-sm">
    <h2 className="font-bold">Dự báo này được tạo từ lịch sử nào?</h2>
    <p>{training.observation_count} ngày có quan sát: <strong>{training.start_date} → {training.end_date}</strong>. Huấn luyện lúc {new Date(training.trained_at).toLocaleString('vi-VN')}.</p>
    <p>Kiểm thử: {training.test_start} → {training.test_end} ({training.test_count} ngày quan sát). {training.evaluation}</p>
    <p>RMSE của cách giữ nguyên giá cuối cùng: <strong>{training.baseline.rmse.toLocaleString('vi-VN')}</strong>. Mô hình hiện tại {rmse < training.baseline.rmse ? 'có sai số thấp hơn' : 'chưa tốt hơn'} cách đơn giản này trên tập kiểm thử.</p>
    <p>{training.filled_days} ngày thiếu được điền bằng giá đã biết trước đó; không tính các ngày điền vào sai số kiểm thử. {training.interval_note}</p>
    {training.stale_days>1&&<p className="text-amber-800">Mốc lịch sử cuối cách hiện tại {training.stale_days} ngày. Dự báo bắt đầu sau mốc đó; hãy cập nhật dữ liệu nếu cần dự báo sát hiện tại.</p>}
    <Link className="underline text-brand" href={`/history?commodity_id=${commodityId}`}>Xem bảng và biểu đồ lịch sử →</Link>
  </section>;
}
