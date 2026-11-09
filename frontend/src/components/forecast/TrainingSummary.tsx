import Link from 'next/link';
import { TrainingMetadata } from '@/lib/api';
import { ExternalLink } from 'lucide-react';

export default function TrainingSummary({
  training,
  commodityId,
  rmse,
}: {
  training: TrainingMetadata;
  commodityId: number;
  rmse: number;
}) {
  const unit =
    training.cadence === 'periodic'
      ? 'kỳ báo cáo'
      : training.cadence === 'irregular'
        ? 'mốc công bố'
        : 'ngày quan sát';
  const beatsBaseline = rmse < training.baseline.rmse;

  return (
    <section className="rounded-xl border border-zinc-200/90 bg-white p-5">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="text-[14px] font-semibold text-zinc-900">
              Dữ liệu huấn luyện: {training.observation_count} {unit} ({training.start_date} – {training.end_date})
            </h3>
            <span
              className={`text-[11px] font-medium px-2 py-0.5 rounded-md ${
                beatsBaseline
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200/60'
                  : 'bg-zinc-100 text-zinc-600'
              }`}
            >
              {beatsBaseline ? 'Tốt hơn chuẩn cơ sở (Baseline)' : 'Tương đương chuẩn cơ sở'}
            </span>
          </div>
          <p className="mt-1 text-[12.5px] text-zinc-500">
            Mục tiêu: {training.target || 'Giá công bố'} · Tập kiểm thử: {training.test_count} {unit} ({training.test_start} → {training.test_end}) · Cập nhật mô hình: {new Date(training.trained_at).toLocaleDateString('vi-VN')}
          </p>
        </div>

        <Link
          className="inline-flex items-center gap-1.5 text-[12.5px] font-medium text-zinc-700 hover:text-zinc-900 px-3 py-1.5 rounded-lg border border-zinc-200 hover:bg-zinc-50 transition-colors shrink-0 w-fit"
          href={`/history?commodity_id=${commodityId}`}
        >
          <span>Xem chuỗi dữ liệu gốc</span>
          <ExternalLink className="w-3.5 h-3.5 text-zinc-400" />
        </Link>
      </div>

      {training.stale_days > 1 && (
        <p className="mt-3 rounded-lg bg-amber-50/70 border border-amber-200/60 px-3 py-2 text-[12px] text-amber-800">
          Mốc dữ liệu gần nhất cách hiện tại {training.stale_days} ngày. Khuyến nghị cập nhật thêm lịch sử trước khi ra quyết định giao dịch.
        </p>
      )}
    </section>
  );
}
