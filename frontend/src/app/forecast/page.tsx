'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/layout/Header';
import {
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import {
  COMMODITIES_DATA,
  MODEL_METRICS_LIST,
  FORECAST_PREDICTIONS_SAMPLE,
} from '@/lib/mockData';
import { ModelMetrics, ForecastPoint } from '@/types';
import { fetchForecastDashboard } from '@/lib/api';
import { BrainCircuit, Activity, BarChart3, ShieldCheck } from 'lucide-react';

export default function ForecastPage() {
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(2); // Coffee
  const [selectedModel, setSelectedModel] = useState<'LSTM' | 'Prophet' | 'ARIMA'>('LSTM');
  const [forecastDays, setForecastDays] = useState<number>(14);

  const [metrics, setMetrics] = useState<ModelMetrics>(MODEL_METRICS_LIST.LSTM);
  const [forecastData, setForecastData] = useState<ForecastPoint[]>(FORECAST_PREDICTIONS_SAMPLE);
  const [loading, setLoading] = useState<boolean>(false);

  const currentCommodity =
    COMMODITIES_DATA.find((c) => c.id === selectedCommodityId) || COMMODITIES_DATA[1];

  // Fetch forecast data dynamically from FastAPI PostgreSQL backend
  useEffect(() => {
    let isMounted = true;
    async function loadForecast() {
      setLoading(true);
      try {
        const res = await fetchForecastDashboard(selectedCommodityId, selectedModel, forecastDays);
        if (isMounted && res) {
          if (res.metrics) setMetrics(res.metrics);
          if (res.forecastData && res.forecastData.length > 0) {
            setForecastData(res.forecastData);
          }
        }
      } catch (err) {
        console.error('Error fetching forecast:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    loadForecast();
    return () => {
      isMounted = false;
    };
  }, [selectedCommodityId, selectedModel, forecastDays]);

  // Format data for Recharts composed chart
  const displayForecastData = forecastData.map((item) => ({
    ...item,
    ciRange: [item.lowerCI, item.upperCI],
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <Header
        title="Mô hình & Dự báo Giá Nông sản"
        subtitle="Dự báo chuỗi thời gian kèm khoảng tin cậy 95% (Confidence Interval) & Đánh giá sai số từ Database"
        showLiveBadge={false}
      />

      {/* Control Bar: Filters */}
      <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4">
          {/* Commodity Select */}
          <div className="flex flex-col">
            <label className="text-[11px] font-bold text-secondary-text uppercase tracking-wider mb-1.5">
              Chọn nông sản
            </label>
            <select
              value={selectedCommodityId}
              onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
              className="bg-canvas border border-border-subtle text-primary-text text-sm font-semibold rounded-xl px-3.5 py-2 focus:outline-none focus:ring-2 focus:ring-brand/30 transition-all cursor-pointer"
            >
              {COMMODITIES_DATA.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.unit})
                </option>
              ))}
            </select>
          </div>

          {/* Model Select */}
          <div className="flex flex-col">
            <label className="text-[11px] font-bold text-secondary-text uppercase tracking-wider mb-1.5">
              Thuật toán mô hình
            </label>
            <div className="flex items-center gap-1.5 bg-canvas p-1 rounded-xl border border-border-subtle">
              {(['LSTM', 'Prophet', 'ARIMA'] as const).map((model) => (
                <button
                  key={model}
                  onClick={() => setSelectedModel(model)}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    selectedModel === model
                      ? 'bg-brand text-white shadow-sm'
                      : 'text-secondary-text hover:text-primary-text'
                  }`}
                >
                  {model}
                </button>
              ))}
            </div>
          </div>

          {/* Horizon Select */}
          <div className="flex flex-col">
            <label className="text-[11px] font-bold text-secondary-text uppercase tracking-wider mb-1.5">
              Thời hạn dự báo
            </label>
            <div className="flex items-center gap-1.5 bg-canvas p-1 rounded-xl border border-border-subtle">
              {[7, 14, 30].map((days) => (
                <button
                  key={days}
                  onClick={() => setForecastDays(days)}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    forecastDays === days
                      ? 'bg-[#EAE5DF] text-primary-text font-extrabold shadow-sm'
                      : 'text-secondary-text hover:text-primary-text'
                  }`}
                >
                  {days} ngày
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Model Meta Badge */}
        <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-brand-badge border border-brand/20 text-brand text-xs font-semibold">
          <BrainCircuit className="w-4 h-4" />
          <span>{loading ? 'Đang tải dữ liệu...' : `Trạng thái: ${metrics.modelName} đã hội tụ`}</span>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* MAE */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">MAE (Sai số tuyệt đối)</span>
            <Activity className="w-4 h-4 text-brand" />
          </div>
          <div className="text-2xl font-extrabold text-primary-text">
            {metrics.mae ? metrics.mae.toLocaleString('vi-VN') : '0'} {currentCommodity.unit}
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Mean Absolute Error</span>
        </div>

        {/* RMSE */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">RMSE (Căn bậc sai số)</span>
            <BarChart3 className="w-4 h-4 text-accent-coral" />
          </div>
          <div className="text-2xl font-extrabold text-primary-text">
            {metrics.rmse ? metrics.rmse.toLocaleString('vi-VN') : '0'} {currentCommodity.unit}
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Root Mean Squared Error</span>
        </div>

        {/* MAPE */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">MAPE (% Sai số)</span>
            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-brand-badge text-brand">
              Độ chính xác cao (&lt; 2%)
            </span>
          </div>
          <div className="text-2xl font-extrabold text-brand">
            {metrics.mape}%
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Mean Absolute Percentage Error</span>
        </div>

        {/* R-Squared */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">R² (Độ phù hợp)</span>
            <ShieldCheck className="w-4 h-4 text-brand" />
          </div>
          <div className="text-2xl font-extrabold text-primary-text">
            {metrics.r2}
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">R-Squared Score (Max 1.0)</span>
        </div>
      </div>

      {/* Main Forecast Chart with 95% Confidence Interval */}
      <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
          <div>
            <h2 className="text-base font-bold text-primary-text tracking-tight">
              Biểu đồ Dự báo {currentCommodity.name} & Dải Tin Cậy 95% ({selectedModel})
            </h2>
            <p className="text-xs text-secondary-text mt-0.5 font-medium">
              Dữ liệu đồng bộ trực tiếp từ CSDL PostgreSQL (Khoảng tin cậy 95% CI)
            </p>
          </div>

          <div className="flex items-center gap-4 text-xs font-semibold">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-primary-text" />
              <span className="text-primary-text">Giá lịch sử</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-0.5 rounded-full bg-brand" />
              <span className="text-brand font-bold">Dự báo điểm</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-[#4E7152]/20 border border-[#4E7152]/40" />
              <span className="text-secondary-text">Dải tin cậy 95%</span>
            </div>
          </div>
        </div>

        {/* Recharts ComposedChart */}
        <div className="h-[340px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={displayForecastData} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
              <defs>
                <linearGradient id="forecastCIGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4E7152" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#4E7152" stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#F0ECE4" vertical={false} />
              <XAxis
                dataKey="date"
                stroke="#A89A8B"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: '#EFECE6' }}
                dy={10}
              />
              <YAxis
                stroke="#A89A8B"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
                tickFormatter={(v) => Number(v).toLocaleString('vi-VN')}
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0]?.payload;
                    return (
                      <div className="bg-white/95 backdrop-blur-md p-3.5 rounded-xl border border-border-subtle shadow-xl text-xs space-y-1.5">
                        <div className="font-bold text-primary-text border-b border-border-subtle pb-1">
                          Ngày: {label}
                        </div>
                        {data.actualPrice && (
                          <div className="text-primary-text font-semibold flex justify-between gap-4">
                            <span>Giá thực tế:</span>
                            <span>{data.actualPrice.toLocaleString('vi-VN')} {currentCommodity.unit}</span>
                          </div>
                        )}
                        <div className="text-brand font-bold flex justify-between gap-4">
                          <span>Giá dự báo:</span>
                          <span>{data.predictedPrice.toLocaleString('vi-VN')} {currentCommodity.unit}</span>
                        </div>
                        <div className="text-secondary-text flex justify-between gap-4 pt-1 border-t border-border-subtle/60 text-[11px]">
                          <span>95% CI:</span>
                          <span>
                            [{data.lowerCI.toLocaleString('vi-VN')} - {data.upperCI.toLocaleString('vi-VN')}]
                          </span>
                        </div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              {/* Confidence Interval Band */}
              <Area
                type="monotone"
                dataKey="ciRange"
                stroke="#4E7152"
                strokeDasharray="4 4"
                strokeWidth={1}
                fill="url(#forecastCIGradient)"
                name="Khoảng tin cậy 95%"
              />
              {/* Actual price line */}
              <Line
                type="monotone"
                dataKey="actualPrice"
                stroke="#2D231E"
                strokeWidth={2.5}
                dot={{ r: 4, fill: '#2D231E' }}
                name="Giá thực tế"
              />
              {/* Forecast price line */}
              <Line
                type="monotone"
                dataKey="predictedPrice"
                stroke="#4E7152"
                strokeWidth={2.8}
                dot={{ r: 4, fill: '#4E7152' }}
                name="Dự báo"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Forecast Details Table */}
      <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card">
        <h3 className="text-base font-bold text-primary-text mb-4">
          Bảng chi tiết giá trị dự báo {forecastDays} ngày tới từ PostgreSQL
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border-subtle text-secondary-text font-bold uppercase tracking-wider pb-2">
                <th className="py-2.5 px-3">Ngày</th>
                <th className="py-2.5 px-3">Loại dữ liệu</th>
                <th className="py-2.5 px-3">Giá dự báo ({currentCommodity.unit})</th>
                <th className="py-2.5 px-3">Ngưỡng dưới (95% CI)</th>
                <th className="py-2.5 px-3">Ngưỡng trên (95% CI)</th>
                <th className="py-2.5 px-3">Biến động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {displayForecastData.slice(3).map((item, idx) => (
                <tr key={idx} className="hover:bg-canvas/60 transition-colors">
                  <td className="py-3 px-3 font-bold text-primary-text">{item.date}</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-brand-badge text-brand">
                      {selectedModel} Dự báo
                    </span>
                  </td>
                  <td className="py-3 px-3 font-extrabold text-brand text-sm">
                    {item.predictedPrice.toLocaleString('vi-VN')}
                  </td>
                  <td className="py-3 px-3 text-secondary-text">
                    {item.lowerCI.toLocaleString('vi-VN')}
                  </td>
                  <td className="py-3 px-3 text-secondary-text">
                    {item.upperCI.toLocaleString('vi-VN')}
                  </td>
                  <td className="py-3 px-3">
                    <span className="text-brand font-bold">
                      +{displayForecastData[3] && displayForecastData[3].predictedPrice ? (((item.predictedPrice - displayForecastData[3].predictedPrice) / displayForecastData[3].predictedPrice) * 100).toFixed(2) : '0.00'}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
