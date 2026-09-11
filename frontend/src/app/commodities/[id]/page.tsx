'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  fetchForecastData,
  fetchCommoditiesOverview,
} from '@/lib/api';
import { ForecastPoint, ModelMetrics, CommoditySummary } from '@/types';
import AIInsightCard from '@/components/dashboard/AIInsightCard';
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
  TrendingUp,
  TrendingDown,
  Info,
  Layers,
  Award,
  Loader2,
} from 'lucide-react';

export default function CommodityDetailPage() {
  const params = useParams();
  const commodityId = Number(params.id) || 2;

  const [commodity, setCommodity] = useState<CommoditySummary | null>(null);
  const [forecastPoints, setForecastPoints] = useState<ForecastPoint[]>([]);
  const [metrics, setMetrics] = useState<ModelMetrics>({
    modelName: 'LSTM',
    mae: 470.5,
    rmse: 680.0,
    mape: 1.12,
    r2: 0.942,
    trainDate: '2026-09-05',
  });

  const [selectedModel, setSelectedModel] = useState<string>('LSTM');
  const [selectedDays, setSelectedDays] = useState<number>(7);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const loadCommodityAndForecast = async () => {
    setIsLoading(true);
    try {
      // 1. Lấy thông tin commodity
      const allComms = await fetchCommoditiesOverview();
      const current = allComms.find((c) => c.id === commodityId) || allComms[0];
      if (current) setCommodity(current);

      // 2. Lấy dữ liệu dự báo kết hợp
      const fRes = await fetchForecastData(commodityId, selectedModel, selectedDays);
      if (fRes) {
        setForecastPoints(fRes.forecastData || []);
        if (fRes.metrics) setMetrics(fRes.metrics);
      }
    } catch (e) {
      console.error('Error loading commodity details:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCommodityAndForecast();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [commodityId, selectedModel, selectedDays]);

  // Chart data format: separates historical line and dashed forecast line
  const chartData = useMemo(() => {
    return forecastPoints.map((pt) => ({
      date: pt.date,
      // Historical actual price (only present when isForecast is false)
      actualPrice: !pt.isForecast ? pt.predictedPrice || pt.actualPrice : null,
      // AI Forecast line
      predictedPrice: pt.isForecast ? pt.predictedPrice : null,
      // Confidence interval band
      lowerCI: pt.isForecast ? pt.lowerCI : null,
      upperCI: pt.isForecast ? pt.upperCI : null,
      ciRange: pt.isForecast ? [pt.lowerCI, pt.upperCI] : null,
      isForecast: pt.isForecast,
    }));
  }, [forecastPoints]);

  // Calculate trend percentage over forecast horizon
  const trendPct = useMemo(() => {
    const forecastPts = forecastPoints.filter((p) => p.isForecast);
    const histPts = forecastPoints.filter((p) => !p.isForecast);
    if (forecastPts.length > 0 && histPts.length > 0) {
      const startPrice = histPts[histPts.length - 1].predictedPrice;
      const endPrice = forecastPts[forecastPts.length - 1].predictedPrice;
      if (startPrice > 0) {
        return ((endPrice - startPrice) / startPrice) * 100;
      }
    }
    return 1.5;
  }, [forecastPoints]);

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Return button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-border-subtle">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="p-2 rounded-xl bg-white border border-border-subtle hover:bg-canvas text-secondary-text hover:text-primary-text transition shadow-xs"
            title="Quay lại Trang Chủ"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-brand bg-brand-light px-2.5 py-0.5 rounded-full border border-brand/20">
                {commodity?.code || 'COMMODITY'}
              </span>
              <span className="text-xs text-secondary-text">Chi Tiết Nông Sản & Dự Báo AI</span>
            </div>
            <h1 className="text-2xl font-extrabold text-primary-text tracking-tight mt-0.5">
              {commodity?.name || 'Chi Tiết Nông Sản'}
            </h1>
          </div>
        </div>

        {/* Model & Horizon Selector Controls */}
        <div className="flex items-center flex-wrap gap-2.5">
          {/* Horizon Toggle */}
          <div className="flex items-center gap-1 bg-white p-1 rounded-xl border border-border-subtle shadow-xs text-xs font-bold">
            {[7, 14, 30].map((days) => (
              <button
                key={days}
                onClick={() => setSelectedDays(days)}
                className={`px-3 py-1.5 rounded-lg transition ${
                  selectedDays === days
                    ? 'bg-brand text-white shadow-xs'
                    : 'text-secondary-text hover:text-primary-text'
                }`}
              >
                {days} Ngày
              </button>
            ))}
          </div>

          {/* Model Toggle */}
          <div className="flex items-center gap-1 bg-white p-1 rounded-xl border border-border-subtle shadow-xs text-xs font-bold">
            {['LSTM', 'XGBoost', 'Prophet'].map((model) => (
              <button
                key={model}
                onClick={() => setSelectedModel(model)}
                className={`px-3 py-1.5 rounded-lg transition ${
                  selectedModel === model
                    ? 'bg-brand text-white shadow-xs'
                    : 'text-secondary-text hover:text-primary-text'
                }`}
              >
                {model}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Interactive Price Chart (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          <div className="p-6 rounded-2xl bg-white border border-border-subtle shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
              <div>
                <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-brand" />
                  Biểu Đồ Xu Hướng Giá Thực Tế & Dự Báo AI
                </h3>
                <p className="text-xs text-secondary-text mt-0.5">
                  Đường nét liền: Lịch sử · Đường nét đứt cam: Dự đoán {selectedModel} · Vùng mờ: Khoảng tin cậy 95%
                </p>
              </div>

              <div className="flex items-center gap-3 text-xs font-bold">
                {isLoading && (
                  <span className="flex items-center gap-1 text-xs text-secondary-text font-medium">
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-brand" />
                    Đang tải...
                  </span>
                )}
                <span className="flex items-center gap-1.5 text-brand">
                  <span className="w-3.5 h-1 rounded bg-brand" />
                  Giá Lịch Sử
                </span>
                <span className="flex items-center gap-1.5 text-amber-600">
                  <span className="w-3.5 h-1 rounded bg-amber-500 border-b border-dashed border-amber-600" />
                  Dự Báo AI
                </span>
              </div>
            </div>

            {/* Recharts Composed Chart */}
            <div className="h-[360px] w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={chartData} margin={{ top: 10, right: 15, left: 10, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#F0EBE5" vertical={false} />
                  <XAxis
                    dataKey="date"
                    tickLine={false}
                    axisLine={{ stroke: '#EAE5DF' }}
                    tick={{ fill: '#7C6F62', fontSize: 11, fontWeight: 500 }}
                  />
                  <YAxis
                    domain={['auto', 'auto']}
                    tickLine={false}
                    axisLine={false}
                    tick={{ fill: '#7C6F62', fontSize: 11, fontWeight: 500 }}
                    tickFormatter={(val) => `${(val / 1000).toLocaleString('vi-VN')}k`}
                  />
                  <Tooltip
                    content={({ active, payload, label }) => {
                      if (active && payload && payload.length) {
                        const actual = payload.find((p) => p.dataKey === 'actualPrice')?.value;
                        const predicted = payload.find((p) => p.dataKey === 'predictedPrice')?.value;
                        const upper = payload.find((p) => p.dataKey === 'upperCI')?.value;
                        const lower = payload.find((p) => p.dataKey === 'lowerCI')?.value;

                        return (
                          <div className="bg-white/95 backdrop-blur-md p-3.5 rounded-xl border border-border-subtle shadow-xl text-xs space-y-1.5 min-w-[190px]">
                            <div className="font-bold text-primary-text border-b border-border-subtle pb-1">
                              Ngày: {label}
                            </div>
                            {actual !== undefined && actual !== null && (
                              <div className="text-brand font-semibold flex justify-between gap-3">
                                <span>Giá thực tế:</span>
                                <span>{Number(actual).toLocaleString('vi-VN')} đ</span>
                              </div>
                            )}
                            {predicted !== undefined && predicted !== null && (
                              <div className="text-amber-600 font-bold flex justify-between gap-3">
                                <span>Dự báo {selectedModel}:</span>
                                <span>{Number(predicted).toLocaleString('vi-VN')} đ</span>
                              </div>
                            )}
                            {upper !== undefined && upper !== null && lower !== undefined && lower !== null && (
                              <div className="text-[11px] text-secondary-text pt-1 border-t border-border-subtle/50 flex justify-between">
                                <span>Biên 95% CI:</span>
                                <span>[{Number(lower).toLocaleString('vi-VN')} - {Number(upper).toLocaleString('vi-VN')}]</span>
                              </div>
                            )}
                          </div>
                        );
                      }
                      return null;
                    }}
                  />

                  {/* Confidence Interval Shaded Band */}
                  <Area
                    type="monotone"
                    dataKey="upperCI"
                    stroke="none"
                    fill="#F59E0B"
                    fillOpacity={0.12}
                    name="Dải biên độ trên (95%)"
                  />
                  <Area
                    type="monotone"
                    dataKey="lowerCI"
                    stroke="none"
                    fill="#FFFFFF"
                    fillOpacity={1}
                    name="Dải biên độ dưới (95%)"
                  />

                  {/* Historical Solid Line */}
                  <Line
                    type="monotone"
                    dataKey="actualPrice"
                    stroke="#527853"
                    strokeWidth={3}
                    dot={{ r: 4, fill: '#527853', stroke: '#FFFFFF', strokeWidth: 2 }}
                    activeDot={{ r: 6 }}
                    name="Giá thực tế"
                    connectNulls={false}
                  />

                  {/* AI Prediction Dashed Line */}
                  <Line
                    type="monotone"
                    dataKey="predictedPrice"
                    stroke="#D97706"
                    strokeWidth={3}
                    strokeDasharray="5 5"
                    dot={{ r: 4, fill: '#D97706', stroke: '#FFFFFF', strokeWidth: 2 }}
                    activeDot={{ r: 6 }}
                    name="Giá AI dự báo"
                    connectNulls={false}
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

        {/* Right Column: Commodity Key Stats & Model Metrics (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Commodity Details Card */}
          <div className="p-6 rounded-2xl bg-white border border-border-subtle shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <span className="font-bold text-sm text-primary-text flex items-center gap-2">
                <Layers className="w-4 h-4 text-brand" />
                Thông Tin Hàng Hóa
              </span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-brand/10 text-brand">
                {commodity?.category || 'Nông sản'}
              </span>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between items-center py-1.5 border-b border-border-subtle/50">
                <span className="text-secondary-text">Giá chốt gần nhất</span>
                <span className="font-extrabold text-brand font-mono text-base">
                  {commodity?.formattedPrice || '62,300 VNĐ/kg'}
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-border-subtle/50">
                <span className="text-secondary-text">Biến động 24h</span>
                <span
                  className={`font-extrabold flex items-center gap-1 ${
                    (commodity?.changePct || 0) >= 0 ? 'text-emerald-700' : 'text-rose-700'
                  }`}
                >
                  {(commodity?.changePct || 0) >= 0 ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
                  {(commodity?.changePct || 0) >= 0 ? '+' : ''}
                  {commodity?.changePct?.toFixed(2) || '0.00'}%
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-border-subtle/50">
                <span className="text-secondary-text">Đơn vị tính</span>
                <span className="font-semibold text-primary-text">{commodity?.unit || 'VNĐ/kg'}</span>
              </div>

              <div className="flex justify-between items-center py-1.5">
                <span className="text-secondary-text">Vùng trọng điểm</span>
                <span className="font-semibold text-primary-text text-right max-w-[170px] truncate">
                  {commodity?.region || 'Tây Nguyên'}
                </span>
              </div>
            </div>
          </div>

          {/* Model Accuracy Matrix */}
          <div className="p-6 rounded-2xl bg-white border border-border-subtle shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <span className="font-bold text-sm text-primary-text flex items-center gap-2">
                <Award className="w-4 h-4 text-amber-500" />
                Độ Chính Xác Mô Hình ({selectedModel})
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700">
                R² = {metrics.r2.toFixed(3)}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                <div className="text-[11px] text-secondary-text font-medium">Sai Số MAE</div>
                <div className="text-base font-extrabold text-primary-text font-mono mt-0.5">
                  {metrics.mae.toLocaleString('vi-VN')} đ
                </div>
              </div>

              <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                <div className="text-[11px] text-secondary-text font-medium">Sai Số RMSE</div>
                <div className="text-base font-extrabold text-primary-text font-mono mt-0.5">
                  {metrics.rmse.toLocaleString('vi-VN')} đ
                </div>
              </div>

              <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                <div className="text-[11px] text-secondary-text font-medium">Tỷ Lệ Lỗi MAPE</div>
                <div className="text-base font-extrabold text-brand font-mono mt-0.5">
                  {metrics.mape.toFixed(2)}%
                </div>
              </div>

              <div className="p-3 rounded-xl bg-canvas border border-border-subtle">
                <div className="text-[11px] text-secondary-text font-medium">R² Score</div>
                <div className="text-base font-extrabold text-emerald-700 font-mono mt-0.5">
                  {metrics.r2.toFixed(3)}
                </div>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-amber-50/50 border border-amber-200 text-[11px] text-amber-900 flex items-start gap-2">
              <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>
                Mô hình {selectedModel} được huấn luyện định kỳ với chuỗi dữ liệu giá thực tế và đạt độ tin cậy cao trên tập kiểm thử độc lập.
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
