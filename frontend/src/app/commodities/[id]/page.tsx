'use client';

import React, { useState, useEffect, useMemo, useRef } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  fetchForecastDashboard,
  fetchCommoditiesOverview,
  fetchModelComparison,
} from '@/lib/api';
import {
  ForecastPoint,
  ModelMetrics,
  CommoditySummary,
  ModelComparisonMetrics,
  LocationContextData,
} from '@/types';
import { useLocation } from '@/contexts/LocationContext';
import AIInsightCard from '@/components/dashboard/AIInsightCard';
import {
  formatDateVN,
  formatNumberVN,
  formatPct,
  getCommodityUnit,
} from '@/lib/formatters';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import {
  ArrowLeft,
  ArrowRight,
  TrendingUp,
  TrendingDown,
  Info,
  Layers,
  Award,
  Loader2,
  MapPin,
  History,
} from 'lucide-react';

type SupportedModel = 'LSTM' | 'Prophet' | 'ARIMA' | 'XGBoost' | 'Random Forest';

const MODEL_BUTTONS: { value: SupportedModel; shortLabel: string }[] = [
  { value: 'LSTM', shortLabel: 'LSTM' },
  { value: 'Prophet', shortLabel: 'Prophet' },
  { value: 'ARIMA', shortLabel: 'ARIMA' },
  { value: 'XGBoost', shortLabel: 'XGBoost' },
  { value: 'Random Forest', shortLabel: 'RF' },
];

const SUPPORTED_MODEL_LIST: SupportedModel[] = [
  'LSTM',
  'Prophet',
  'ARIMA',
  'XGBoost',
  'Random Forest',
];

function toSupportedModel(name?: string | null): SupportedModel | null {
  if (!name) return null;
  const target = name.trim().toLowerCase();
  return SUPPORTED_MODEL_LIST.find((m) => m.toLowerCase() === target) || null;
}

export default function CommodityDetailPage() {
  const params = useParams();
  const commodityId = Number(params.id) || 2;
  const { provinceCode, provinceName } = useLocation();

  const [commodity, setCommodity] = useState<CommoditySummary | null>(null);
  const [forecastPoints, setForecastPoints] = useState<ForecastPoint[]>([]);
  const [comparisonData, setComparisonData] = useState<ModelComparisonMetrics[]>([]);
  const [locationContext, setLocationContext] = useState<LocationContextData | null>(null);
  const [metrics, setMetrics] = useState<ModelMetrics>({
    modelName: 'LSTM',
    mae: 0,
    rmse: 0,
    mape: 0,
    r2: 0,
    trainDate: 'N/A',
  });

  const [selectedModel, setSelectedModel] = useState<SupportedModel>('LSTM');
  const [selectedDays, setSelectedDays] = useState<number>(14);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState('');
  const autoPickedIdRef = useRef<number>(0);

  useEffect(() => {
    let active = true;
    async function loadCommodityAndForecast() {
      setIsLoading(true);
      setError('');
      setForecastPoints([]);
      try {
        const [allComms, compRes] = await Promise.all([
          fetchCommoditiesOverview(provinceCode),
          fetchModelComparison(commodityId).catch(() => []),
        ]);
        if (!active) return;

        const current = allComms.find((c) => c.id === commodityId) || allComms[0] || null;
        setCommodity(current);
        setComparisonData(compRes || []);

        let effectiveModel: SupportedModel = selectedModel;
        if (autoPickedIdRef.current !== commodityId && compRes && compRes.length > 0) {
          const best = toSupportedModel(
            compRes.find((m) => m.isBest)?.modelName || compRes[0]?.modelName
          );
          autoPickedIdRef.current = commodityId;
          if (best && best !== selectedModel) {
            effectiveModel = best;
            setSelectedModel(best);
          }
        }

        const fRes = await fetchForecastDashboard(
          commodityId,
          effectiveModel,
          selectedDays,
          undefined,
          provinceCode
        );
        if (!active) return;
        if (fRes) {
          setForecastPoints(fRes.forecastData || []);
          if (fRes.metrics) setMetrics(fRes.metrics);
          setLocationContext(fRes.location_context || null);
        }
      } catch (e) {
        if (active) {
          setError(e instanceof Error ? e.message : 'Không tải được chi tiết nông sản');
        }
      } finally {
        if (active) setIsLoading(false);
      }
    }
    void loadCommodityAndForecast();
    return () => {
      active = false;
    };
  }, [commodityId, selectedModel, selectedDays, provinceCode]);

  const currentUnit = getCommodityUnit(commodity?.name, commodity?.unit);
  const bestModelName = useMemo(
    () =>
      toSupportedModel(
        comparisonData.find((m) => m.isBest)?.modelName || comparisonData[0]?.modelName
      ),
    [comparisonData]
  );

  // Deduplicate by date & bridge last historical point seamlessly to forecast start
  const chartData = useMemo(() => {
    const dedup = new Map<string, ForecastPoint>();
    for (const pt of forecastPoints) {
      if (pt.date) dedup.set(pt.date.slice(0, 10), pt);
    }
    const ordered = Array.from(dedup.values()).sort((a, b) => a.date.localeCompare(b.date));
    let lastHistIdx = -1;
    for (let i = 0; i < ordered.length; i++) {
      if (!ordered[i].isForecast) lastHistIdx = i;
    }
    return ordered.map((pt, idx) => {
      const isBridge = idx === lastHistIdx;
      const showForecast = pt.isForecast || isBridge;
      const bridgeVal = pt.actualPrice ?? pt.predictedPrice;
      const lo = pt.isForecast ? pt.lowerCI : bridgeVal;
      const hi = pt.isForecast ? pt.upperCI : bridgeVal;
      return {
        date: pt.date,
        shortDate: formatDateVN(pt.date).slice(0, 5),
        actualPrice: !pt.isForecast ? bridgeVal : null,
        predictedPrice: showForecast ? (isBridge ? bridgeVal : pt.predictedPrice) : null,
        lowerCI: pt.isForecast ? lo : null,
        upperCI: pt.isForecast ? hi : null,
        ciBand: showForecast ? [lo, hi] : null,
        isForecast: pt.isForecast,
      };
    });
  }, [forecastPoints]);

  const trendPct = useMemo(() => {
    const forecastPts = forecastPoints.filter((p) => p.isForecast);
    const histPts = forecastPoints.filter((p) => !p.isForecast);
    if (forecastPts.length > 0 && histPts.length > 0) {
      const startPrice = histPts[histPts.length - 1].actualPrice ?? histPts[histPts.length - 1].predictedPrice;
      const endPrice = forecastPts[forecastPts.length - 1].predictedPrice;
      if (startPrice > 0) {
        return ((endPrice - startPrice) / startPrice) * 100;
      }
    }
    return 0;
  }, [forecastPoints]);

  return (
    <div className="space-y-5 max-w-[1440px] mx-auto pb-8 font-sans">
      {error && (
        <p role="alert" className="p-3.5 rounded-xl bg-red-50 text-[#DC2626] border border-red-200 text-xs font-medium">
          {error}
        </p>
      )}

      {/* Top Breadcrumb & Controls */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-3 border-b border-[#E5E7EB]">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="p-2 rounded-xl bg-white border border-[#E5E7EB] hover:bg-[#F8FAF9] text-[#475569] hover:text-[#1E293B] transition shadow-xs"
            title="Quay lại Trang Tổng quan"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-bold text-[#2F6F4E] bg-[#F0F7F4] px-2 py-0.5 rounded-md border border-[#2F6F4E]/20">
                {commodity?.code || 'AGRO'}
              </span>
              <span className="text-xs text-[#64748B]">Chi tiết nông sản & Dự báo AI</span>
              {provinceCode !== 'all' && locationContext && (
                <span
                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold ${
                    locationContext.pricing_mode === 'direct'
                      ? 'bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20'
                      : 'bg-slate-100 text-slate-700 border border-slate-200'
                  }`}
                >
                  <MapPin className="w-3 h-3 shrink-0" />
                  <span>{locationContext.note || provinceName}</span>
                </span>
              )}
            </div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-[#1E293B] tracking-tight mt-0.5">
              {commodity?.name || 'Chi tiết nông sản'}
            </h1>
          </div>
        </div>

        {/* Horizon + 5-Model Selector Controls */}
        <div className="flex items-center flex-wrap gap-2">
          <div className="flex items-center gap-0.5 bg-white p-1 rounded-xl border border-[#E5E7EB] text-xs font-semibold">
            {[7, 14, 30].map((days) => (
              <button
                key={days}
                type="button"
                onClick={() => setSelectedDays(days)}
                className={`px-2.5 py-1 rounded-lg transition cursor-pointer tabular-nums ${
                  selectedDays === days
                    ? 'bg-[#2F6F4E] text-white'
                    : 'text-[#475569] hover:text-[#1E293B]'
                }`}
              >
                {days}N
              </button>
            ))}
          </div>

          <div className="flex items-center flex-wrap gap-0.5 bg-white p-1 rounded-xl border border-[#E5E7EB] text-xs font-semibold">
            {MODEL_BUTTONS.map((m) => {
              const isBest = bestModelName === m.value;
              const isActive = selectedModel === m.value;
              return (
                <button
                  key={m.value}
                  type="button"
                  onClick={() => setSelectedModel(m.value)}
                  className={`px-2.5 py-1 rounded-lg transition cursor-pointer ${
                    isActive
                      ? 'bg-[#2F6F4E] text-white'
                      : 'text-[#475569] hover:text-[#1E293B]'
                  }`}
                >
                  {m.shortLabel}
                  {isBest ? ' ★' : ''}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Interactive Price Chart (8 Cols) */}
        <div className="lg:col-span-8 space-y-5">
          <div className="p-5 rounded-2xl bg-white border border-[#E5E7EB] shadow-card space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#E5E7EB]">
              <div>
                <h2 className="text-[15px] font-bold text-[#1E293B] flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-[#2F6F4E]" />
                  <span>Biểu đồ giá thực tế & Dự báo {selectedModel} ({selectedDays} ngày)</span>
                </h2>
                <p className="text-xs text-[#64748B] mt-0.5">
                  Đường nét liền: Lịch sử thực tế · Đường nét đứt: Dự báo AI · Vùng mờ: Khoảng tin cậy 95% Conformal CI
                </p>
              </div>

              <div className="flex items-center gap-3 text-xs font-semibold">
                {isLoading && (
                  <span className="flex items-center gap-1 text-xs text-[#64748B]">
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-[#2F6F4E]" />
                    Đang tải...
                  </span>
                )}
                <span className="flex items-center gap-1.5 text-[#2F6F4E]">
                  <span className="w-3.5 h-1 rounded bg-[#2F6F4E]" />
                  Thực tế
                </span>
                <span className="flex items-center gap-1.5 text-[#D97706]">
                  <span className="w-3.5 h-0.5 border-t-2 border-dashed border-[#D97706]" />
                  Dự báo AI
                </span>
              </div>
            </div>

            <div className="h-[360px] w-full pt-1">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={chartData} margin={{ top: 10, right: 15, left: 10, bottom: 16 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
                  <XAxis
                    dataKey="shortDate"
                    tickLine={false}
                    axisLine={{ stroke: '#E5E7EB' }}
                    tick={{ fill: '#64748B', fontSize: 11, fontWeight: 500 }}
                  />
                  <YAxis
                    domain={['auto', 'auto']}
                    tickLine={false}
                    axisLine={false}
                    tick={{ fill: '#64748B', fontSize: 11, fontWeight: 500 }}
                    tickFormatter={(val) => formatNumberVN(Math.round(Number(val)))}
                    width={78}
                  />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const row = payload[0]?.payload as {
                          date: string;
                          actualPrice: number | null;
                          predictedPrice: number | null;
                          lowerCI: number | null;
                          upperCI: number | null;
                        };
                        return (
                          <div className="bg-white/95 backdrop-blur-md p-3 rounded-xl border border-[#E5E7EB] shadow-lg text-xs space-y-1.5 min-w-[205px] tabular-nums">
                            <div className="font-bold text-[#1E293B] border-b border-[#E5E7EB] pb-1">
                              Ngày {formatDateVN(row.date)}
                            </div>
                            {row.actualPrice !== null && (
                              <div className="text-[#2F6F4E] font-semibold flex justify-between gap-3">
                                <span>Giá thực tế:</span>
                                <span>{formatNumberVN(Math.round(row.actualPrice))} {currentUnit}</span>
                              </div>
                            )}
                            {row.predictedPrice !== null && (
                              <div className="text-[#D97706] font-bold flex justify-between gap-3">
                                <span>Dự báo {selectedModel}:</span>
                                <span>{formatNumberVN(Math.round(row.predictedPrice))} {currentUnit}</span>
                              </div>
                            )}
                            {row.lowerCI !== null && row.upperCI !== null && (
                              <div className="text-[11px] text-[#64748B] pt-1 border-t border-[#E5E7EB] flex justify-between gap-2">
                                <span>Biên 95% CI:</span>
                                <span>
                                  {formatNumberVN(Math.round(row.lowerCI))} – {formatNumberVN(Math.round(row.upperCI))}
                                </span>
                              </div>
                            )}
                          </div>
                        );
                      }
                      return null;
                    }}
                  />

                  <Area
                    type="monotone"
                    dataKey="ciBand"
                    stroke="none"
                    fill="#F59E0B"
                    fillOpacity={0.14}
                    name="Khoảng tin cậy 95%"
                    isAnimationActive={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="actualPrice"
                    stroke="#2F6F4E"
                    strokeWidth={2.5}
                    dot={false}
                    activeDot={{ r: 5 }}
                    name="Giá thực tế"
                    connectNulls={false}
                    isAnimationActive={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="predictedPrice"
                    stroke="#D97706"
                    strokeWidth={2.5}
                    strokeDasharray="5 5"
                    dot={false}
                    activeDot={{ r: 5 }}
                    name="Giá AI dự báo"
                    connectNulls={false}
                    isAnimationActive={false}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* AI Insight Card */}
          <AIInsightCard
            commodityName={commodity?.name || 'Nông sản'}
            trendPct={trendPct}
            horizonDays={selectedDays}
            modelName={selectedModel}
          />
        </div>

        {/* Right Column: Commodity Stats & Model Metrics (4 Cols) */}
        <div className="lg:col-span-4 space-y-5">
          {/* Commodity Details Card */}
          <div className="p-5 rounded-2xl bg-white border border-[#E5E7EB] shadow-card space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-[#E5E7EB]">
              <span className="font-bold text-sm text-[#1E293B] flex items-center gap-2">
                <Layers className="w-4 h-4 text-[#2F6F4E]" />
                Thông tin hàng hóa
              </span>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#F0F7F4] text-[#2F6F4E]">
                {commodity?.category || 'Nông sản'}
              </span>
            </div>

            <div className="space-y-3 text-xs tabular-nums">
              <div className="flex justify-between items-center py-1.5 border-b border-[#F1F5F9]">
                <span className="text-[#64748B]">Giá chốt gần nhất</span>
                <span className="font-extrabold text-[#2F6F4E] text-base">
                  {commodity ? `${formatNumberVN(Math.round(commodity.currentPrice))} ${currentUnit}` : '—'}
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-[#F1F5F9]">
                <span className="text-[#64748B]">Biến động phiên</span>
                <span
                  className={`font-bold flex items-center gap-1 ${
                    (commodity?.changePct || 0) >= 0 ? 'text-[#15803D]' : 'text-[#DC2626]'
                  }`}
                >
                  {(commodity?.changePct || 0) >= 0 ? (
                    <TrendingUp className="w-3.5 h-3.5" />
                  ) : (
                    <TrendingDown className="w-3.5 h-3.5" />
                  )}
                  {formatPct(commodity?.changePct || 0, 2)}
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-[#F1F5F9]">
                <span className="text-[#64748B]">Đơn vị tính</span>
                <span className="font-semibold text-[#1E293B]">{currentUnit}</span>
              </div>

              <div className="flex justify-between items-center py-1.5">
                <span className="text-[#64748B]">Vùng trọng điểm</span>
                <span className="font-semibold text-[#1E293B] text-right max-w-[190px] truncate" title={commodity?.region}>
                  {commodity?.region || 'Toàn quốc'}
                </span>
              </div>
            </div>

            <div className="pt-2 flex items-center gap-2">
              <Link
                href={`/history?commodity_id=${commodityId}`}
                className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg border border-[#E5E7EB] bg-[#F8FAF9] hover:bg-[#F0F7F4] text-xs font-semibold text-[#334155] transition"
              >
                <History className="w-3.5 h-3.5" />
                <span>Xem lịch sử</span>
              </Link>
              <Link
                href={`/forecast?commodity_id=${commodityId}`}
                className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-xs font-semibold text-white transition"
              >
                <span>Phân tích sâu</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>

          {/* Model Accuracy Matrix */}
          <div className="p-5 rounded-2xl bg-white border border-[#E5E7EB] shadow-card space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-[#E5E7EB]">
              <span className="font-bold text-sm text-[#1E293B] flex items-center gap-2">
                <Award className="w-4 h-4 text-[#D97706]" />
                Kiểm thử {selectedModel}
              </span>
              <span className="text-[11px] font-bold px-2 py-0.5 rounded-md bg-[#F0F7F4] text-[#15803D] tabular-nums">
                R² = {metrics.r2.toFixed(3)}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2.5 text-xs tabular-nums">
              <div className="p-3 rounded-xl bg-[#F8FAF9] border border-[#E5E7EB]">
                <div className="text-[11px] text-[#64748B] font-medium">Sai số MAE</div>
                <div className="text-sm font-extrabold text-[#1E293B] mt-0.5">
                  {formatNumberVN(Math.round(metrics.mae))} {currentUnit}
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#F8FAF9] border border-[#E5E7EB]">
                <div className="text-[11px] text-[#64748B] font-medium">Sai số RMSE</div>
                <div className="text-sm font-extrabold text-[#1E293B] mt-0.5">
                  {formatNumberVN(Math.round(metrics.rmse))} {currentUnit}
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#F8FAF9] border border-[#E5E7EB]">
                <div className="text-[11px] text-[#64748B] font-medium">Tỷ lệ lỗi MAPE</div>
                <div className="text-sm font-extrabold text-[#2F6F4E] mt-0.5">
                  {metrics.mape.toFixed(2)}%
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#F8FAF9] border border-[#E5E7EB]">
                <div className="text-[11px] text-[#64748B] font-medium">Độ chính xác</div>
                <div className="text-sm font-extrabold text-[#15803D] mt-0.5">
                  {(metrics.accuracy ?? Math.max(0, 100 - metrics.mape)).toFixed(2)}%
                </div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-[#F0F7F4] border border-[#2F6F4E]/15 text-[11px] text-[#1E293B] flex items-start gap-2">
              <Info className="w-4 h-4 text-[#2F6F4E] shrink-0 mt-0.5" />
              <span>
                Đánh giá Walk-Forward cuộn 7 ngày (Zero Data Leakage) tích hợp biến ngoại sinh nhân quả USD/VND & dầu thô WTI.
                {metrics.picp95 != null ? ` Độ phủ thực nghiệm 95% CI (PICP): ${metrics.picp95.toFixed(1)}%.` : ''}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
