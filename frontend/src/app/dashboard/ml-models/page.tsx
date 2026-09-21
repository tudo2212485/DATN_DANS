'use client';

import JobStatus, { useBackgroundJob } from '@/components/dashboard/JobStatus';
import Link from 'next/link';
import {fetchTrainingReadiness, HistoryReadiness} from '@/lib/api';
import { getUser } from '@/lib/auth';
import React, { useState, useEffect } from 'react';
import {
  triggerRetrainTaskApi,
  fetchActiveModelApi,
  setActiveModelApi,
  fetchAdminCommodities,
  fetchModelComparisonApi,
} from '@/lib/api';
import {
  ModelComparisonMetrics,
  ActiveModelSetting,
} from '@/types';
import {
  Cpu,
  RefreshCw,
  Play,
  Sparkles,
  Award,
  BarChart2,
  Check,
  Zap,
} from 'lucide-react';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
}

export default function DashboardMLModelsPage() {
  const canEdit = getUser()?.role === 'admin';
  const [error, setError] = useState('');
  const [switching, setSwitching] = useState(false);
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(2); // Default Robusta = 2
  const [modelsMetrics, setModelsMetrics] = useState<ModelComparisonMetrics[]>([]);
  const [activeModelSetting, setActiveModelSetting] = useState<ActiveModelSetting>({
    active_model: 'Đang tải',
    description: 'Đang kiểm tra cấu hình mô hình',
  });
  const [loading, setLoading] = useState(true);
  const [readiness, setReadiness] = useState<HistoryReadiness>();

  // Retrain state
  const [retrainRunning, setRetrainRunning] = useState(false);
  const retrain = useBackgroundJob('retrain', () => { void loadData(); });

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [cData, mSetting, mData, quality] = await Promise.all([
        fetchAdminCommodities(),
        fetchActiveModelApi(),
        fetchModelComparisonApi(selectedCommodityId),
        fetchTrainingReadiness(selectedCommodityId),
      ]);
      setCommodities(cData);
      setActiveModelSetting(mSetting);
      setModelsMetrics(mData);
      setReadiness(quality);
    } catch (e) {
      setModelsMetrics([]);
      setError(e instanceof Error ? e.message : 'Không tải được mô hình');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommodityId]);

  const handleRetrain = async () => {
    setRetrainRunning(true);
    try {
      retrain.begin(await triggerRetrainTaskApi(selectedCommodityId));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Không kích hoạt được huấn luyện');
    } finally { setRetrainRunning(false); }
  };

  const handleSwitchModel = async (modelName: string) => {
    setSwitching(true);
    try {
      const updated = await setActiveModelApi(modelName);
      setActiveModelSetting(updated);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Không thể chuyển đổi mô hình');
    } finally { setSwitching(false); }
  };

  return (
    <div className="space-y-6">
      {error && <p role="alert" className="p-4 bg-rose-50 text-rose-700 rounded-xl">{error}</p>}
      <div className="p-4 bg-brand/10 rounded-xl text-sm"><p>{readiness?.ready ? `Đủ ${readiness.observation_count} ngày có nguồn: ${readiness.start_date} → ${readiness.end_date}.` : readiness?.reason}</p><Link className="underline text-brand" href={`/history?commodity_id=${selectedCommodityId}`}>Xem lịch sử đầu vào / bổ sung dữ liệu →</Link></div>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
        <div>
          <h1 className="text-2xl font-bold text-primary-text flex items-center gap-2.5">
            <Cpu className="w-6 h-6 text-brand" />
            Quản Trị Mô Hình Machine Learning & AI
          </h1>
          <p className="text-sm text-secondary-text mt-1">
            Theo dõi độ chính xác (MAE, RMSE, MAPE, R2), chuyển đổi Model Switcher và kích hoạt huấn luyện lại
          </p>
        </div>

        <div className="flex items-center gap-2">
          <select
            value={selectedCommodityId}
            onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
            className="bg-card border border-border-subtle text-primary-text px-3.5 py-2 rounded-xl text-xs font-medium focus:outline-none shadow-xs"
          >
            {commodities.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name} ({c.code})
              </option>
            ))}
          </select>

          <button
            onClick={loadData}
            disabled={loading}
            className="px-3.5 py-2 rounded-xl bg-card hover:bg-canvas text-secondary-text border border-border-subtle text-xs font-semibold flex items-center gap-2 transition shadow-xs"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Làm Mới
          </button>
        </div>
      </div>

      {/* Model Switcher Banner */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-brand uppercase tracking-wider">
              <Zap className="w-4 h-4" />
              Bộ Chọn Thuật Toán Mặc Định (Active Model Switcher)
            </div>
            <h2 className="text-lg font-bold text-primary-text mt-1">
              Mô hình đang phục vụ API:{' '}
              <span className="text-brand font-mono bg-brand-light px-2.5 py-0.5 rounded-lg border border-brand/20">
                {activeModelSetting.active_model}
              </span>
            </h2>
            <p className="text-xs text-secondary-text mt-1">{activeModelSetting.description}</p>
          </div>

          <div className="flex items-center gap-2">
            {['LSTM', 'XGBOOST', 'PROPHET', 'ARIMA', 'RANDOM FOREST'].map((m) => {
              const isSelected = activeModelSetting.active_model.toUpperCase() === m;
              return (
                <button
                  key={m}
                  disabled={!canEdit || switching || retrain.running} onClick={() => handleSwitchModel(m)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition ${
                    isSelected
                      ? 'bg-brand text-white font-bold shadow-xs'
                      : 'bg-canvas hover:bg-[#EFECE6] text-secondary-text border border-border-subtle'
                  }`}
                >
                  {isSelected && <Check className="w-3.5 h-3.5 stroke-[3]" />}
                  {m}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Retrain Trigger Panel */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-base font-semibold text-primary-text flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand" />
              Kích Hoạt Huấn Luyện Lại (Model Re-train Engine)
            </h2>
            <p className="text-xs text-secondary-text mt-0.5">
              Huấn luyện 5 mô hình trên dữ liệu thu thập/đã xác nhận (tối thiểu 60 ngày quan sát, không có khoảng thiếu quá 7 ngày).
            </p>
          </div>

          <button
            onClick={handleRetrain}
            disabled={!canEdit || retrainRunning || retrain.running || loading || !readiness?.ready}
            className="px-5 py-2.5 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-semibold flex items-center gap-2 shadow-xs transition disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${retrainRunning ? 'animate-spin' : ''}`} />
            {retrainRunning ? 'Đang Huấn Luyện...' : 'Huấn Luyện Lại Ngay'}
          </button>
        </div>

        {/* Progress Bar */}
        <JobStatus job={retrain.job} error={retrain.error} />
      </div>

      {/* Model Performance Comparison Table */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
          <div>
            <h2 className="text-base font-semibold text-primary-text flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-brand" />
              Bảng Đánh Giá & So Sánh Hiệu Năng Mô Hình (Model Accuracy Matrix)
            </h2>
            <p className="text-xs text-secondary-text mt-0.5">
              So sánh các mô hình cùng lần huấn luyện, cùng tập kiểm thử 15% ngày quan sát cuối (tối đa 30), dự báo nhiều bước từ cùng một mốc. Xem trang dự báo để đối chiếu với cách giữ nguyên giá cuối cùng.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-primary-text">
            <thead className="bg-canvas text-secondary-text uppercase text-[11px] font-semibold border-b border-border-subtle">
              <tr>
                <th className="py-3 px-4">Mô Hình (Algorithm)</th>
                <th className="py-3 px-4">MAE (VNĐ)</th>
                <th className="py-3 px-4">RMSE (VNĐ)</th>
                <th className="py-3 px-4">MAPE (%)</th>
                <th className="py-3 px-4">R² Score</th>
                <th className="py-3 px-4">Đánh Giá</th>
                <th className="py-3 px-4 text-right">Trạng Thái</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle font-mono text-[11px]">
              {!loading && modelsMetrics.length === 0 && <tr><td colSpan={7} className="p-4">Chưa có kết quả đánh giá. Hãy huấn luyện mô hình.</td></tr>}
              {modelsMetrics.map((m, idx) => {
                const isActive = activeModelSetting.active_model.toUpperCase() === m.modelName.toUpperCase();
                return (
                  <tr key={idx} className="hover:bg-canvas/60 transition">
                    <td className="py-3.5 px-4 font-sans font-semibold text-primary-text flex items-center gap-2">
                      <span>{m.modelName}</span>
                      {m.isBest && (
                        <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200 text-[10px] flex items-center gap-1 font-sans font-semibold">
                          <Award className="w-3 h-3 text-amber-600" />
                          RMSE thấp nhất
                        </span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-primary-text">{m.mae.toLocaleString('vi-VN')} đ</td>
                    <td className="py-3.5 px-4 text-primary-text font-semibold">{m.rmse.toLocaleString('vi-VN')} đ</td>
                    <td className="py-3.5 px-4 text-secondary-text">{m.mape.toFixed(2)}%</td>
                    <td className="py-3.5 px-4 text-brand font-bold">{m.r2.toFixed(3)}</td>
                    <td className="py-3.5 px-4 font-sans text-secondary-text">
                      {m.r2 > 0.8 ? (
                        <span className="text-brand font-medium">R² &gt; 0,8</span>
                      ) : (
                        <span className="text-secondary-text">Cần xem xét sai số</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-right font-sans">
                      {isActive ? (
                        <span className="px-2.5 py-1 rounded-full bg-brand-light text-brand border border-brand/20 text-[10px] font-semibold">
                          Đang kích hoạt
                        </span>
                      ) : (
                        <button
                          disabled={!canEdit || switching || retrain.running} onClick={() => handleSwitchModel(m.modelName)}
                          className="px-2.5 py-1 rounded-lg bg-canvas hover:bg-[#EFECE6] border border-border-subtle text-secondary-text text-[10px] font-medium transition"
                        >
                          Chọn mô hình này
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
