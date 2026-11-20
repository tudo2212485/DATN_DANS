'use client';

import { useBackgroundJob } from '@/components/dashboard/JobStatus';
import ModelComparisonChart from '@/components/forecast/ModelComparisonChart';
import {
  fetchTrainingReadiness,
  HistoryReadiness,
  triggerRetrainTaskApi,
  fetchActiveModelApi,
  setActiveModelApi,
  fetchAdminCommodities,
  fetchModelComparisonApi,
} from '@/lib/api';
import { getUser } from '@/lib/auth';
import {
  formatNumberVN,
  getCommodityUnit,
} from '@/lib/formatters';
import React, { useState, useEffect, useMemo } from 'react';
import {
  ModelComparisonMetrics,
  ActiveModelSetting,
} from '@/types';
import {
  RefreshCw,
  Play,
  Award,
  Check,
  CheckCircle2,
  AlertTriangle,
  AlertCircle,
  ArrowUpDown,
} from 'lucide-react';

interface CommodityItem {
  id: number;
  code: string;
  name: string;
  unit?: string;
}

const MODEL_PILLS = [
  { apiValue: 'LSTM', label: 'LSTM' },
  { apiValue: 'XGBOOST', label: 'XGBoost' },
  { apiValue: 'PROPHET', label: 'Prophet' },
  { apiValue: 'ARIMA', label: 'ARIMA' },
  { apiValue: 'RANDOM FOREST', label: 'Random Forest' },
];

export default function DashboardMLModelsPage() {
  const canEdit = getUser()?.role === 'admin';
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
  const [switching, setSwitching] = useState(false);
  const [commodities, setCommodities] = useState<CommodityItem[]>([]);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(2); // Cà phê Robusta mặc định
  const [modelsMetrics, setModelsMetrics] = useState<ModelComparisonMetrics[]>([]);
  const [activeModelSetting, setActiveModelSetting] = useState<ActiveModelSetting>({
    active_model: 'LSTM',
    description: '',
  });
  const [loading, setLoading] = useState(true);
  const [readiness, setReadiness] = useState<HistoryReadiness>();
  const [sortCol, setSortCol] = useState<'rmse' | 'mae' | 'mape' | 'r2' | 'accuracy'>('mape');
  const [sortDir, setSortDir] = useState<'ascending' | 'descending'>('ascending');

  const [retrainTriggering, setRetrainTriggering] = useState(false);

  const loadData = async () => {
    setLoading(true);
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
      setToast({
        text: e instanceof Error ? e.message : 'Không tải được dữ liệu mô hình',
        type: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const retrain = useBackgroundJob('retrain', () => {
    void loadData();
    setToast({
      text: 'Đã huấn luyện lại 5 mô hình và cập nhật bảng chỉ số mới nhất.',
      type: 'success',
    });
  });

  useEffect(() => {
    void loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommodityId]);

  const handleRetrain = async () => {
    setRetrainTriggering(true);
    setToast(null);
    try {
      retrain.begin(await triggerRetrainTaskApi(selectedCommodityId));
      setToast({
        text: 'Đã kích hoạt huấn luyện lại 5 mô hình. Hệ thống sẽ tự động cập nhật khi hoàn tất.',
        type: 'success',
      });
    } catch (e) {
      setToast({
        text: e instanceof Error ? e.message : 'Không kích hoạt được huấn luyện',
        type: 'error',
      });
    } finally {
      setRetrainTriggering(false);
    }
  };

  const handleSwitchModel = async (apiValue: string, displayLabel: string) => {
    setSwitching(true);
    setToast(null);
    try {
      const updated = await setActiveModelApi(apiValue);
      setActiveModelSetting(updated);
      setToast({
        text: `Đã lưu "${displayLabel}" làm mô hình mặc định cho toàn hệ thống.`,
        type: 'success',
      });
    } catch (err: unknown) {
      setToast({
        text: err instanceof Error ? err.message : 'Không thể chuyển đổi mô hình mặc định',
        type: 'error',
      });
    } finally {
      setSwitching(false);
    }
  };

  const currentCommodity = commodities.find((c) => c.id === selectedCommodityId);
  const currentUnit = getCommodityUnit(currentCommodity?.name, currentCommodity?.unit);

  const sortedMetrics = useMemo(() => {
    const factor = sortDir === 'ascending' ? 1 : -1;
    return [...modelsMetrics].sort((a, b) => {
      const av = sortCol === 'accuracy' ? (a.accuracy ?? Math.max(0, 100 - (a.mape || 0))) : (a[sortCol] || 0);
      const bv = sortCol === 'accuracy' ? (b.accuracy ?? Math.max(0, 100 - (b.mape || 0))) : (b[sortCol] || 0);
      return factor * (av - bv);
    });
  }, [modelsMetrics, sortCol, sortDir]);

  const handleSort = (col: 'rmse' | 'mae' | 'mape' | 'r2' | 'accuracy') => {
    if (sortCol === col) {
      setSortDir((prev) => (prev === 'ascending' ? 'descending' : 'ascending'));
    } else {
      setSortCol(col);
      setSortDir(col === 'r2' || col === 'accuracy' ? 'descending' : 'ascending');
    }
  };

  const isTrainingBusy = retrainTriggering || retrain.running;

  return (
    <div className="space-y-5 font-sans">
      {/* Compact 1-Line Header */}
      <div className="flex items-center justify-between gap-3 pb-3 border-b border-[#E5E7EB]">
        <h1 className="text-lg sm:text-xl font-bold text-[#1E293B] tracking-tight">
          Quản lý Mô hình ML
        </h1>

        <button
          type="button"
          onClick={() => void loadData()}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-white hover:bg-[#F8FAF9] text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB] text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Làm mới</span>
        </button>
      </div>

      {/* Toast Notification */}
      {(toast || retrain.error) && (
        <div
          role={toast?.type === 'error' || retrain.error ? 'alert' : 'status'}
          className={`p-3 rounded-lg text-xs font-medium flex items-center justify-between border ${
            toast?.type === 'error' || retrain.error
              ? 'bg-red-50 text-[#DC2626] border-red-200'
              : 'bg-[#F0F7F4] text-[#15803D] border-[#15803D]/25'
          }`}
        >
          <div className="flex items-center gap-2">
            {toast?.type === 'error' || retrain.error ? (
              <AlertCircle className="w-4 h-4 shrink-0" />
            ) : (
              <CheckCircle2 className="w-4 h-4 shrink-0" />
            )}
            <span>{retrain.error || toast?.text}</span>
          </div>
          <button
            type="button"
            onClick={() => setToast(null)}
            className="text-[#64748B] hover:text-[#1E293B] font-bold px-1 cursor-pointer"
          >
            ✕
          </button>
        </div>
      )}

      {/* Single Unified Control Card (2 Compact Rows) */}
      <section className="bg-white rounded-xl border border-[#E5E7EB] p-4 space-y-3">
        {/* Row 1: Commodity Selector + Data Validity Badge + Retrain Button */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2.5">
            <select
              aria-label="Chọn nông sản"
              value={selectedCommodityId}
              onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
              className="bg-white border border-[#E5E7EB] text-[#1E293B] px-3 py-1.5 rounded-lg text-xs font-semibold focus:outline-none focus:border-[#2F6F4E]"
            >
              {commodities.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({getCommodityUnit(c.name, c.unit)})
                </option>
              ))}
            </select>

            {readiness?.ready ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20 text-xs font-semibold tabular-nums">
                <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                <span>{formatNumberVN(readiness.observation_count)} ngày hợp lệ</span>
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 text-xs font-semibold">
                <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                <span>{readiness?.reason || 'Đang kiểm tra dữ liệu...'}</span>
              </span>
            )}
          </div>

          <button
            type="button"
            onClick={handleRetrain}
            disabled={!canEdit || isTrainingBusy || loading || !readiness?.ready}
            className="px-4 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white text-xs font-semibold inline-flex items-center gap-1.5 transition-colors disabled:opacity-50 shrink-0 cursor-pointer"
          >
            {isTrainingBusy ? (
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Play className="w-3.5 h-3.5 fill-current" />
            )}
            <span>{isTrainingBusy ? 'Đang huấn luyện...' : 'Huấn luyện lại ngay'}</span>
          </button>
        </div>

        {/* Live Progress Bar ONLY while training is actively running */}
        {retrain.running && retrain.job && (
          <div className="pt-1 space-y-1">
            <div className="flex items-center justify-between text-[11.5px] text-[#2F6F4E] font-medium">
              <span>{retrain.job.message || 'Đang huấn luyện 5 mô hình dự báo...'}</span>
              <span className="tabular-nums font-semibold">{retrain.job.progress || 0}%</span>
            </div>
            <div className="w-full h-1.5 bg-[#E5E7EB] rounded-full overflow-hidden">
              <div
                className="h-full bg-[#2F6F4E] transition-all duration-300"
                style={{ width: `${Math.max(8, retrain.job.progress || 0)}%` }}
              />
            </div>
          </div>
        )}

        {/* Row 2: Default Active Model Pills */}
        <div className="pt-3 border-t border-[#E5E7EB] flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold text-[#64748B] mr-1">
            Mô hình mặc định:
          </span>
          <div className="flex flex-wrap items-center gap-1.5">
            {MODEL_PILLS.map((m) => {
              const isSelected = activeModelSetting.active_model.toUpperCase() === m.apiValue;
              return (
                <button
                  key={m.apiValue}
                  type="button"
                  disabled={!canEdit || switching || isTrainingBusy}
                  onClick={() => handleSwitchModel(m.apiValue, m.label)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold inline-flex items-center gap-1.5 transition-colors cursor-pointer disabled:opacity-50 ${
                    isSelected
                      ? 'bg-[#2F6F4E] text-white'
                      : 'bg-[#F8FAF9] hover:bg-white text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB]'
                  }`}
                >
                  {isSelected && <Check className="w-3.5 h-3.5 stroke-[2.5]" />}
                  <span>{m.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* Visual Model Comparison Chart (Y-axis starts cleanly at 0) */}
      {modelsMetrics.length > 0 && (
        <ModelComparisonChart data={modelsMetrics} unit={currentUnit} />
      )}

      {/* Detailed 5-Model Comparison Table */}
      <section className="bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
        <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex items-center justify-between gap-2">
          <h2 className="text-[14px] font-bold text-[#1E293B]">
            Bảng so sánh chi tiết 5 mô hình — {currentCommodity?.name || 'Nông sản'}
          </h2>
          <span className="text-xs tabular-nums font-semibold text-[#64748B]">
            {modelsMetrics.length} / 5 mô hình
          </span>
        </div>

        <div
          tabIndex={0}
          role="region"
          aria-label="Bảng so sánh chi tiết 5 mô hình"
          className="overflow-x-auto"
        >
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-[#F8FAF9] text-[#64748B] uppercase text-[11px] font-semibold tracking-wider border-b border-[#E5E7EB]">
              <tr>
                <th scope="col" className="py-2.5 px-3.5">
                  Mô hình
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'mae' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('mae')}
                    className="inline-flex items-center justify-end gap-1 font-semibold uppercase tracking-wider text-[#64748B] hover:text-[#1E293B] ml-auto cursor-pointer"
                  >
                    <span>MAE ({currentUnit})</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'rmse' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('rmse')}
                    className="inline-flex items-center justify-end gap-1 font-semibold uppercase tracking-wider text-[#64748B] hover:text-[#1E293B] ml-auto cursor-pointer"
                  >
                    <span>RMSE ({currentUnit})</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'mape' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('mape')}
                    className="inline-flex items-center justify-end gap-1 font-semibold uppercase tracking-wider text-[#64748B] hover:text-[#1E293B] ml-auto cursor-pointer"
                  >
                    <span>MAPE (%)</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'accuracy' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('accuracy')}
                    className="inline-flex items-center justify-end gap-1 font-semibold uppercase tracking-wider text-[#64748B] hover:text-[#1E293B] ml-auto cursor-pointer"
                  >
                    <span>Độ chính xác</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'r2' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('r2')}
                    className="inline-flex items-center justify-end gap-1 font-semibold uppercase tracking-wider text-[#64748B] hover:text-[#1E293B] ml-auto cursor-pointer"
                  >
                    <span>R²</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th scope="col" className="py-2.5 px-3.5 text-right">
                  PICP 95%
                </th>
                <th scope="col" className="py-2.5 px-3.5 text-right">
                  Trạng thái
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7EB] text-[13px]">
              {!loading && sortedMetrics.length === 0 && (
                <tr>
                  <td colSpan={8} className="p-6 text-center text-[#64748B]">
                    Chưa có kết quả đánh giá. Nhấn &ldquo;Huấn luyện lại ngay&rdquo; để huấn luyện đủ 5 mô hình.
                  </td>
                </tr>
              )}
              {sortedMetrics.map((m) => {
                const isActive =
                  activeModelSetting.active_model.toUpperCase() === m.modelName.toUpperCase();
                const acc = m.accuracy ?? Math.max(0, 100 - (m.mape || 0));
                return (
                  <tr key={m.modelName} className="hover:bg-[#F8FAF9] transition-colors">
                    <td className="py-2.5 px-3.5 font-semibold text-[#1E293B]">
                      <div className="flex items-center gap-2">
                        <span>{m.modelName}</span>
                        {m.isBest && (
                          <span className="px-2 py-0.5 rounded-md bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20 text-[11px] inline-flex items-center gap-1 font-semibold">
                            <Award className="w-3 h-3 text-[#15803D]" />
                            Tốt nhất
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums text-[#334155]">
                      {formatNumberVN(Math.round(m.mae))}
                    </td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums font-bold text-[#1E293B]">
                      {formatNumberVN(Math.round(m.rmse))}
                    </td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums text-[#334155]">
                      {m.mape.toLocaleString('vi-VN', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })}
                      %
                    </td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums font-bold text-[#2F6F4E]">
                      {acc.toLocaleString('vi-VN', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })}
                      %
                    </td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums font-semibold text-[#15803D]">
                      {m.r2.toLocaleString('vi-VN', {
                        minimumFractionDigits: 3,
                        maximumFractionDigits: 3,
                      })}
                    </td>
                    <td className="py-2.5 px-3.5 text-right tabular-nums text-[#334155]">
                      {m.picp95 != null
                        ? `${m.picp95.toLocaleString('vi-VN', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`
                        : '—'}
                    </td>
                    <td className="py-2.5 px-3.5 text-right">
                      {isActive ? (
                        <span className="px-2.5 py-1 rounded-md bg-[#2F6F4E] text-white text-[11px] font-semibold">
                          Đang kích hoạt
                        </span>
                      ) : (
                        <button
                          type="button"
                          disabled={!canEdit || switching || isTrainingBusy}
                          onClick={() => handleSwitchModel(m.modelName.toUpperCase(), m.modelName)}
                          className="px-2.5 py-1 rounded-md bg-white hover:bg-[#F8FAF9] border border-[#E5E7EB] text-[#1E293B] text-[11px] font-semibold transition-colors cursor-pointer disabled:opacity-40"
                        >
                          Chọn mặc định
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="px-4 py-2.5 bg-[#F8FAF9] border-t border-[#E5E7EB] text-[11.5px] text-[#64748B]">
          Độ chính xác kiểm thử = <strong className="text-[#334155]">100% − MAPE</strong> (đánh giá Walk-Forward lịch sử không rò rỉ dữ liệu, không cam kết tuyệt đối cho biến động bất thường tương lai).
        </div>
      </section>
    </div>
  );
}
