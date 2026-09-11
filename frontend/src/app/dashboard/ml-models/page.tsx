'use client';

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
  TaskRunResult,
  ActiveModelSetting,
} from '@/types';
import {
  Cpu,
  RefreshCw,
  Play,
  CheckCircle2,
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
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(2); // Default Robusta = 2
  const [modelsMetrics, setModelsMetrics] = useState<ModelComparisonMetrics[]>([]);
  const [activeModelSetting, setActiveModelSetting] = useState<ActiveModelSetting>({
    active_model: 'LSTM',
    description: 'Mô hình Mạng Nơ-ron hồi quy LSTM 2 lớp',
  });
  const [loading, setLoading] = useState(true);

  // Retrain state
  const [retrainRunning, setRetrainRunning] = useState(false);
  const [retrainProgress, setRetrainProgress] = useState(0);
  const [retrainResult, setRetrainResult] = useState<TaskRunResult | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [cData, mSetting, mData] = await Promise.all([
        fetchAdminCommodities(),
        fetchActiveModelApi(),
        fetchModelComparisonApi(selectedCommodityId),
      ]);
      setCommodities(cData);
      setActiveModelSetting(mSetting);
      setModelsMetrics(mData);
    } catch (e) {
      console.error(e);
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
    setRetrainProgress(10);
    setRetrainResult(null);

    const interval = setInterval(() => {
      setRetrainProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + 15;
      });
    }, 800);

    try {
      const res = await triggerRetrainTaskApi(selectedCommodityId);
      clearInterval(interval);
      setRetrainProgress(100);
      setRetrainResult(res);
      // Reload metrics
      const updatedMetrics = await fetchModelComparisonApi(selectedCommodityId);
      setModelsMetrics(updatedMetrics);
    } catch (err: unknown) {
      clearInterval(interval);
      setRetrainProgress(0);
      setRetrainResult({
        taskName: 'Huấn luyện lại mô hình AI',
        status: 'FAILED',
        message: err instanceof Error ? err.message : 'Lỗi khi kích hoạt huấn luyện lại',
        timestamp: new Date().toLocaleTimeString('vi-VN'),
      });
    } finally {
      setTimeout(() => {
        setRetrainRunning(false);
      }, 1200);
    }
  };

  const handleSwitchModel = async (modelName: string) => {
    try {
      const updated = await setActiveModelApi(modelName);
      setActiveModelSetting(updated);
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Không thể chuyển đổi mô hình');
    }
  };

  return (
    <div className="space-y-6">
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
            {['LSTM', 'XGBOOST', 'PROPHET', 'ARIMA'].map((m) => {
              const isSelected = activeModelSetting.active_model.toUpperCase() === m;
              return (
                <button
                  key={m}
                  onClick={() => handleSwitchModel(m)}
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
              Huấn luyện lại toàn bộ mô hình (Prophet, XGBoost, LSTM) với chuỗi dữ liệu giá mới nhất
            </p>
          </div>

          <button
            onClick={handleRetrain}
            disabled={retrainRunning}
            className="px-5 py-2.5 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-semibold flex items-center gap-2 shadow-xs transition disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${retrainRunning ? 'animate-spin' : ''}`} />
            {retrainRunning ? 'Đang Huấn Luyện...' : 'Huấn Luyện Lại Ngay'}
          </button>
        </div>

        {/* Progress Bar */}
        {retrainRunning && (
          <div className="space-y-2 pt-2">
            <div className="flex items-center justify-between text-xs text-secondary-text">
              <span>Đang tính toán đặc trưng & tối ưu trọng số neural network...</span>
              <span className="font-mono text-brand font-semibold">{retrainProgress}%</span>
            </div>
            <div className="w-full h-2.5 rounded-full bg-canvas border border-border-subtle overflow-hidden">
              <div
                className="h-full bg-brand transition-all duration-300"
                style={{ width: `${retrainProgress}%` }}
              />
            </div>
          </div>
        )}

        {retrainResult && (
          <div className="p-3.5 rounded-xl bg-canvas border border-border-subtle flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-brand" />
              <span className="font-semibold text-primary-text">Hoàn tất:</span>
              <span className="text-brand font-medium">{retrainResult.message}</span>
            </div>
            <span className="text-secondary-text text-[11px]">{retrainResult.timestamp}</span>
          </div>
        )}
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
              Chỉ số sai số thực nghiệm trên tập kiểm thử (Test Split 15%)
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
              {modelsMetrics.map((m, idx) => {
                const isActive = activeModelSetting.active_model.toUpperCase() === m.modelName.toUpperCase();
                return (
                  <tr key={idx} className="hover:bg-canvas/60 transition">
                    <td className="py-3.5 px-4 font-sans font-semibold text-primary-text flex items-center gap-2">
                      <span>{m.modelName}</span>
                      {m.isBest && (
                        <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200 text-[10px] flex items-center gap-1 font-sans font-semibold">
                          <Award className="w-3 h-3 text-amber-600" />
                          Độ chính xác cao nhất
                        </span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-primary-text">{m.mae.toLocaleString('vi-VN')} đ</td>
                    <td className="py-3.5 px-4 text-primary-text font-semibold">{m.rmse.toLocaleString('vi-VN')} đ</td>
                    <td className="py-3.5 px-4 text-secondary-text">{m.mape.toFixed(2)}%</td>
                    <td className="py-3.5 px-4 text-brand font-bold">{m.r2.toFixed(3)}</td>
                    <td className="py-3.5 px-4 font-sans text-secondary-text">
                      {m.r2 > 0.8 ? (
                        <span className="text-brand font-medium">Rất tốt (Khuyên dùng)</span>
                      ) : (
                        <span className="text-secondary-text">Đạt tiêu chuẩn kiểm duyệt</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-right font-sans">
                      {isActive ? (
                        <span className="px-2.5 py-1 rounded-full bg-brand-light text-brand border border-brand/20 text-[10px] font-semibold">
                          Đang kích hoạt
                        </span>
                      ) : (
                        <button
                          onClick={() => handleSwitchModel(m.modelName)}
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
