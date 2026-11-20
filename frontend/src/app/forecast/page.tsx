'use client';

import React, { useState, useEffect, useMemo, useRef } from 'react';
import Link from 'next/link';
import {
  TrainingMetadata,
  fetchHistory,
  fetchHistorySources,
  fetchTrainingReadiness,
  HistorySource,
  fetchForecastDashboard,
  fetchModelComparison,
} from '@/lib/api';
import { useLocation } from '@/contexts/LocationContext';
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
  ReferenceLine,
} from 'recharts';
import { ModelMetrics, ForecastPoint, ModelComparisonMetrics, LocationContextData } from '@/types';
import ModelComparisonChart from '@/components/forecast/ModelComparisonChart';
import AgroGrid, { AgroColumn } from '@/components/ui/AgroGrid';
import { formatDateVN, formatNumberVN, formatPct, getCommodityUnit } from '@/lib/formatters';
import { MapPin } from 'lucide-react';

type SupportedModel = 'LSTM' | 'Prophet' | 'ARIMA' | 'XGBoost' | 'Random Forest';
type ChartMode = 'forecast' | 'history' | 'periodic' | 'empty';
type ChartPoint = ForecastPoint & { sellingPrice?: number };

const MODEL_BUTTONS: { value: SupportedModel; shortLabel: string }[] = [
  { value: 'LSTM', shortLabel: 'LSTM' },
  { value: 'Prophet', shortLabel: 'Prophet' },
  { value: 'ARIMA', shortLabel: 'ARIMA' },
  { value: 'XGBoost', shortLabel: 'XGBoost' },
  { value: 'Random Forest', shortLabel: 'RF' },
];

function formatShortDate(raw: string): string {
  if (!raw) return '';
  if (/^\d{4}-\d{2}-\d{2}$/.test(raw)) {
    const [, m, d] = raw.split('-');
    return `${d}/${m}`;
  }
  return raw;
}

const SUPPORTED_MODEL_LIST: SupportedModel[] = ['LSTM', 'Prophet', 'ARIMA', 'XGBoost', 'Random Forest'];

function toSupportedModel(name?: string | null): SupportedModel | null {
  if (!name) return null;
  const target = name.trim().toLowerCase();
  return SUPPORTED_MODEL_LIST.find((m) => m.toLowerCase() === target) || null;
}

const REGION_GROUP_ORDER = ['Nam Trung Bộ', 'Tây Nguyên', 'ĐBSCL', 'Đông Nam Bộ', 'Miền Bắc'];

export default function ForecastPage() {
  const { provinceCode, provinceName, regions, setProvinceCode } = useLocation();
  const [training, setTraining] = useState<TrainingMetadata>();
  const [catalog, setCatalog] = useState<HistorySource[]>([]);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(0);
  const [selectedModel, setSelectedModel] = useState<SupportedModel>('ARIMA');
  const [forecastDays, setForecastDays] = useState<number>(10);
  const [locationContext, setLocationContext] = useState<LocationContextData | null>(null);
  const [activeBottomTab, setActiveBottomTab] = useState<'table' | 'models'>('table');
  const autoPickedCommodityRef = useRef<number>(0);

  const [metrics, setMetrics] = useState<ModelMetrics>({
    modelName: 'ARIMA',
    mae: 0,
    rmse: 0,
    mape: 0,
    r2: 0,
    trainDate: 'N/A',
  });
  const [forecastData, setForecastData] = useState<ChartPoint[]>([]);
  const [comparisonData, setComparisonData] = useState<ModelComparisonMetrics[]>([]);
  const [metricToDisplay, setMetricToDisplay] = useState<'mae' | 'rmse' | 'mape' | 'r2'>('mae');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState('');
  const [chartMode, setChartMode] = useState<ChartMode>('empty');

  const groupedProvinces = useMemo(() => {
    const groups: Record<string, typeof regions> = {};
    for (const r of regions) {
      const key = r.region_name || 'Khác';
      if (!groups[key]) groups[key] = [];
      groups[key].push(r);
    }
    return Object.entries(groups).sort(([a], [b]) => {
      const ia = REGION_GROUP_ORDER.indexOf(a);
      const ib = REGION_GROUP_ORDER.indexOf(b);
      return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
    });
  }, [regions]);

  useEffect(() => {
    let active = true;
    async function initializeCommodity() {
      try {
        const sources = await fetchHistorySources();
        if (!active) return;
        setCatalog(sources);
        const requestedId = Number(new URLSearchParams(window.location.search).get('commodity_id'));
        if (requestedId > 0 && sources.some((source) => source.id === requestedId)) {
          setSelectedCommodityId(requestedId);
          return;
        }
        const states = await Promise.all(
          sources.map(async (source) => ({
            source,
            readiness: await fetchTrainingReadiness(source.id).catch(() => null),
          }))
        );
        if (active) {
          setSelectedCommodityId(
            states.find((item) => item.readiness?.ready)?.source.id || sources[0]?.id || 0
          );
        }
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : 'Không tải được danh mục nông sản');
      }
    }
    void initializeCommodity();
    return () => {
      active = false;
    };
  }, []);

  const rawCommodity =
    catalog.find((c) => c.id === selectedCommodityId) || {
      name: 'Nông sản',
      unit: 'VNĐ/kg',
      code: '',
      kind: 'daily' as const,
    };
  const currentCommodity = {
    ...rawCommodity,
    unit: getCommodityUnit(rawCommodity.name, rawCommodity.unit),
  };

  // Auto-select the ★ best-performing model whenever switching commodity
  useEffect(() => {
    if (selectedCommodityId <= 0) return;
    let active = true;
    async function loadForecast() {
      setLoading(true);
      setError('');
      setForecastData([]);
      setTraining(undefined);
      setLocationContext(null);
      setChartMode('empty');
      try {
        const compRes = await fetchModelComparison(selectedCommodityId);
        if (!active) return;
        setComparisonData(compRes || []);

        let effectiveModel: SupportedModel = selectedModel;
        if (autoPickedCommodityRef.current !== selectedCommodityId && compRes && compRes.length > 0) {
          const bestMatch = toSupportedModel(compRes.find((m) => m.isBest)?.modelName || compRes[0]?.modelName);
          autoPickedCommodityRef.current = selectedCommodityId;
          if (bestMatch && bestMatch !== selectedModel) {
            effectiveModel = bestMatch;
            setSelectedModel(bestMatch);
          }
        }

        setMetrics({ modelName: effectiveModel, mae: 0, rmse: 0, mape: 0, r2: 0, trainDate: 'N/A' });
        const res = await fetchForecastDashboard(
          selectedCommodityId,
          effectiveModel,
          forecastDays,
          undefined,
          provinceCode
        );
        if (active) {
          if (res?.metrics) setMetrics(res.metrics);
          setTraining(res.training);
          setLocationContext(res.location_context || null);
          if (res?.forecastData && res.forecastData.length > 0) {
            setForecastData(res.forecastData);
            setChartMode('forecast');
          }
        }
      } catch (err) {
        const forecastError = err instanceof Error ? err.message : 'Không tải được dữ liệu dự báo';
        try {
          const end = new Date();
          const start = new Date(end);
          start.setDate(start.getDate() - 1825);
          const history = await fetchHistory(
            selectedCommodityId,
            start.toISOString().slice(0, 10),
            end.toISOString().slice(0, 10),
            false,
            provinceCode
          );
          if (!active) return;
          setLocationContext(history.location_context || null);
          if (history.records.length > 0) {
            setForecastData(
              history.records.slice(-180).map((record) => ({
                date: record.date,
                actualPrice: record.price,
                predictedPrice: record.price,
                lowerCI: record.price,
                upperCI: record.price,
                isForecast: false,
              }))
            );
            setChartMode('history');
            setError(`${forecastError} Đang hiển thị dữ liệu lịch sử đã xác minh.`);
          } else {
            setError(forecastError);
          }
        } catch {
          if (active) setError(forecastError);
        }
      } finally {
        if (active) setLoading(false);
      }
    }
    void loadForecast();
    return () => {
      active = false;
    };
  }, [selectedCommodityId, selectedModel, forecastDays, provinceCode]);

  const chartSeries = useMemo(() => {
    let lastHistoryIdx = -1;
    for (let i = 0; i < forecastData.length; i++) {
      if (!forecastData[i].isForecast) lastHistoryIdx = i;
    }

    return forecastData.map((item, idx) => {
      const isBridgePoint = idx === lastHistoryIdx && chartMode === 'forecast';
      const showForecast = item.isForecast || isBridgePoint;
      const bridgePrice = item.actualPrice ?? item.predictedPrice;

      return {
        ...item,
        shortDate: formatShortDate(item.date),
        actualLine: !item.isForecast ? item.actualPrice : null,
        forecastLine: showForecast
          ? isBridgePoint
            ? bridgePrice
            : Math.round(item.predictedPrice)
          : null,
        ciBand: showForecast
          ? isBridgePoint
            ? [bridgePrice, bridgePrice]
            : [Math.round(item.lowerCI), Math.round(item.upperCI)]
          : null,
      };
    });
  }, [forecastData, chartMode]);

  const yDomain = useMemo<[number, number]>(() => {
    const values: number[] = [];
    for (const p of chartSeries) {
      if (typeof p.actualLine === 'number' && p.actualLine > 0) values.push(p.actualLine);
      if (typeof p.forecastLine === 'number' && p.forecastLine > 0) values.push(p.forecastLine);
      if (Array.isArray(p.ciBand)) {
        if (p.ciBand[0] > 0) values.push(p.ciBand[0]);
        if (p.ciBand[1] > 0) values.push(p.ciBand[1]);
      }
    }
    if (values.length === 0) return [0, 100000];
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);
    const span = maxVal - minVal;
    const pad = span > 0 ? span * 0.12 : minVal * 0.05;
    const step = minVal > 50000 ? 1000 : minVal > 5000 ? 200 : 50;
    const lower = Math.max(0, Math.floor((minVal - pad) / step) * step);
    const upper = Math.ceil((maxVal + pad) / step) * step;
    return [lower, upper];
  }, [chartSeries]);

  const forecastOnlyData = useMemo(
    () => forecastData.filter((item) => item.isForecast),
    [forecastData]
  );
  const lastHistoryPoint = useMemo(
    () => [...forecastData].reverse().find((item) => !item.isForecast),
    [forecastData]
  );
  const basePrice = lastHistoryPoint
    ? lastHistoryPoint.actualPrice || lastHistoryPoint.predictedPrice
    : 0;
  const lastForecastPoint = forecastOnlyData.length
    ? forecastOnlyData[forecastOnlyData.length - 1]
    : undefined;
  const projectedChange =
    basePrice && lastForecastPoint
      ? ((lastForecastPoint.predictedPrice - basePrice) / basePrice) * 100
      : 0;
  const projectedDiffVnd =
    basePrice && lastForecastPoint ? Math.round(lastForecastPoint.predictedPrice - basePrice) : 0;

  const bestModelName = comparisonData.find((m) => m.isBest)?.modelName;
  const activeRegionLabel =
    provinceCode === 'all'
      ? locationContext?.reference_province || 'Toàn quốc (Vùng trọng điểm)'
      : locationContext?.province_name || provinceName;

  return (
    <div className="space-y-4 max-w-[1440px] mx-auto pb-8 font-sans">
      <Header
        title="Phân tích & Dự báo giá nông sản"
        subtitle={
          loading
            ? 'Đang tải dữ liệu dự báo...'
            : 'Dự báo chuỗi thời gian ngắn hạn 7–30 ngày kèm khoảng tin cậy 95% theo từng địa phương'
        }
      />

      {error && (
        <div
          role="alert"
          className="px-4 py-2.5 rounded-lg border text-xs bg-amber-50 text-amber-900 border-amber-200"
        >
          {error}
        </div>
      )}

      {/* Single-Row Control Toolbar: [Nông sản ▼] [Khu vực ▼] [Mô hình: LSTM | Prophet | ARIMA | XGBoost | RF] [Kỳ hạn: 7N | 10N | 14N | 30N] */}
      <div className="bg-white rounded-xl border border-[#E5E7EB] p-3 flex flex-wrap items-center justify-between gap-2.5 shadow-card">
        {/* Left: Commodity Dropdown & Region Dropdown */}
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex items-center gap-1.5">
            <label htmlFor="commodity-select" className="text-xs font-medium text-[#64748B]">
              Nông sản:
            </label>
            <select
              id="commodity-select"
              value={selectedCommodityId}
              onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
              className="bg-[#F8FAF9] border border-[#E5E7EB] text-[#1E293B] text-xs font-semibold rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#2F6F4E] cursor-pointer"
            >
              {catalog.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({getCommodityUnit(c.name, c.unit)})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-1.5">
            <label htmlFor="province-select" className="text-xs font-medium text-[#64748B]">
              Tỉnh/Thành:
            </label>
            <select
              id="province-select"
              value={provinceCode}
              onChange={(e) => setProvinceCode(e.target.value)}
              className="bg-[#F8FAF9] border border-[#E5E7EB] text-[#1E293B] text-xs font-semibold rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#2F6F4E] cursor-pointer max-w-[230px]"
            >
              <option value="all">Toàn quốc (Vùng trọng điểm)</option>
              {groupedProvinces.map(([regionLabel, items]) => (
                <optgroup key={regionLabel} label={regionLabel}>
                  {items.map((r) => (
                    <option key={r.code} value={r.code}>
                      {r.name}
                    </option>
                  ))}
                </optgroup>
              ))}
            </select>
          </div>
        </div>

        {/* Right: Model Tabs & Horizon Tabs */}
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-medium text-[#64748B] hidden sm:inline">Mô hình:</span>
            <div className="flex items-center gap-0.5 bg-[#F8FAF9] p-0.5 rounded-lg border border-[#E5E7EB]">
              {MODEL_BUTTONS.map((m) => {
                const isBest = bestModelName?.toLowerCase() === m.value.toLowerCase();
                return (
                  <button
                    key={m.value}
                    type="button"
                    onClick={() => setSelectedModel(m.value)}
                    title={isBest ? `${m.value} (Độ chính xác kiểm thử cao nhất)` : m.value}
                    className={`px-2.5 py-1 rounded-md text-xs transition-colors cursor-pointer inline-flex items-center gap-1 ${
                      selectedModel === m.value
                        ? 'bg-[#2F6F4E] text-white font-semibold'
                        : 'text-[#334155] font-medium hover:text-[#1E293B]'
                    }`}
                  >
                    <span>{m.shortLabel}</span>
                    {isBest && (
                      <span
                        className={`text-[10px] leading-none ${
                          selectedModel === m.value ? 'text-amber-300' : 'text-[#2F6F4E]'
                        }`}
                        aria-label="Tốt nhất"
                      >
                        ★
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex items-center gap-1.5">
            <span className="text-xs font-medium text-[#64748B] hidden md:inline">Kỳ hạn:</span>
            <div className="flex items-center gap-0.5 bg-[#F8FAF9] p-0.5 rounded-lg border border-[#E5E7EB]">
              {[7, 10, 14, 30].map((days) => (
                <button
                  key={days}
                  type="button"
                  onClick={() => setForecastDays(days)}
                  className={`px-2.5 py-1 rounded-md text-xs tabular-nums transition-colors cursor-pointer ${
                    forecastDays === days
                      ? 'bg-[#2F6F4E] text-white font-semibold'
                      : 'text-[#334155] font-medium hover:text-[#1E293B]'
                  }`}
                >
                  {days}N
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 4 Compact KPI Summary Cards (Each has max 3 elements: Small Label + Large Number + 1 Short Sub-line) */}
      {chartMode === 'forecast' && forecastData.length > 0 && (
        <section
          aria-label="Chỉ số dự báo tóm tắt"
          className="bg-white rounded-xl border border-[#E5E7EB] shadow-card grid grid-cols-2 lg:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-[#E5E7EB]"
        >
          {/* Card 1 */}
          <div className="p-4">
            <p className="text-xs font-medium text-[#64748B]">Giá hiện tại</p>
            <p className="mt-1 text-2xl font-bold tabular-nums text-[#1E293B]">
              {formatNumberVN(Math.round(basePrice))}
            </p>
            <p className="mt-1 text-xs text-[#64748B] truncate">
              {currentCommodity.unit} · {activeRegionLabel}
            </p>
          </div>

          {/* Card 2 */}
          <div className="p-4">
            <p className="text-xs font-medium text-[#64748B]">Dự báo {forecastDays} ngày</p>
            <p className="mt-1 text-2xl font-bold tabular-nums text-[#1E293B]">
              {lastForecastPoint ? formatNumberVN(Math.round(lastForecastPoint.predictedPrice)) : '—'}
            </p>
            <p
              className={`mt-1 text-xs font-semibold tabular-nums ${
                projectedChange >= 0 ? 'text-[#15803D]' : 'text-[#DC2626]'
              }`}
            >
              {formatPct(projectedChange, 2)} ({projectedDiffVnd >= 0 ? `+${formatNumberVN(projectedDiffVnd)}` : formatNumberVN(projectedDiffVnd)} {currentCommodity.unit})
            </p>
          </div>

          {/* Card 3 */}
          <div className="p-4">
            <p className="text-xs font-medium text-[#64748B]">Khoảng tin cậy 95%</p>
            <p className="mt-1 text-lg sm:text-xl font-bold tabular-nums text-[#1E293B] truncate">
              {lastForecastPoint
                ? `${formatNumberVN(Math.round(lastForecastPoint.lowerCI))} – ${formatNumberVN(Math.round(lastForecastPoint.upperCI))}`
                : '—'}
            </p>
            <p className="mt-1 text-xs text-[#64748B] tabular-nums">
              {metrics.picp95 != null
                ? `Bao phủ kiểm thử (PICP): ${Number(metrics.picp95).toFixed(1)}%`
                : `Biên độ ±${formatNumberVN(Math.round(metrics.rmse || 0))} ${currentCommodity.unit}`}
            </p>
          </div>

          {/* Card 4 */}
          <div className="p-4">
            <p className="text-xs font-medium text-[#64748B]">Độ chính xác kiểm thử ({selectedModel})</p>
            <p className="mt-1 text-2xl font-bold tabular-nums text-[#2F6F4E]">
              {Number(metrics.accuracy ?? Math.max(0, 100 - (metrics.mape || 0))).toFixed(2)}%
            </p>
            <p className="mt-1 text-xs text-[#64748B] tabular-nums">
              MAPE: {Number(metrics.mape || 0).toFixed(2)}% · R²: {Number(metrics.r2 || 0).toFixed(3)}
            </p>
          </div>
        </section>
      )}

      {/* Main Price & Forecast Chart */}
      <div className="bg-white rounded-xl border border-[#E5E7EB] p-4 sm:p-5 shadow-card space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[#E5E7EB]">
          <div>
            <h2 className="text-[15px] font-bold text-[#1E293B]">
              {chartMode === 'forecast'
                ? `Diễn biến giá ${currentCommodity.name} và dự báo ${forecastDays} ngày tới (${selectedModel})`
                : `Lịch sử giá ${currentCommodity.name}`}
            </h2>
            <p className="text-xs text-[#64748B] mt-0.5 flex flex-wrap items-center gap-1.5">
              <span>
                Đơn vị: {currentCommodity.unit} · Khu vực: <strong className="text-[#334155]">{activeRegionLabel}</strong>
              </span>
              {locationContext && provinceCode !== 'all' && (
                <span
                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold ${
                    locationContext.pricing_mode === 'direct'
                      ? 'bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20'
                      : 'bg-slate-100 text-slate-700 border border-slate-200'
                  }`}
                >
                  <MapPin className="w-3 h-3 shrink-0" />
                  <span>{locationContext.note || locationContext.explanation}</span>
                </span>
              )}
            </p>
            {locationContext?.explanation && provinceCode !== 'all' && (
              <p className="text-[11.5px] text-[#64748B] mt-1">{locationContext.explanation}</p>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs font-medium text-[#334155] shrink-0">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-0.5 bg-[#2F6F4E]" />
              <span>Giá thực tế</span>
            </div>
            {chartMode === 'forecast' && (
              <>
                <div className="flex items-center gap-1.5">
                  <span className="w-3.5 h-0 border-b-2 border-dashed border-[#2563EB]" />
                  <span>Dự báo ({selectedModel})</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-2.5 rounded-xs bg-blue-500/15 border border-blue-500/30" />
                  <span>Khoảng tin cậy 95%</span>
                </div>
              </>
            )}
          </div>
        </div>

        <div className="w-full h-[350px] pt-1">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart
              data={chartSeries}
              margin={{ top: 10, right: 16, left: 4, bottom: 4 }}
            >
              <defs>
                <linearGradient id="ciBandFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#2563EB" stopOpacity={0.14} />
                  <stop offset="100%" stopColor="#2563EB" stopOpacity={0.03} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
              <XAxis
                dataKey="shortDate"
                tickLine={false}
                axisLine={{ stroke: '#E5E7EB' }}
                tick={{ fill: '#64748B', fontSize: 11.5 }}
                dy={6}
                minTickGap={18}
              />
              <YAxis
                domain={yDomain}
                tickLine={false}
                axisLine={false}
                width={64}
                tickFormatter={(val) => formatNumberVN(val)}
                tick={{ fill: '#64748B', fontSize: 11.5 }}
              />
              {lastHistoryPoint && chartMode === 'forecast' && (
                <ReferenceLine
                  x={formatShortDate(lastHistoryPoint.date)}
                  stroke="#CBD5E1"
                  strokeDasharray="3 3"
                />
              )}
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-white text-[#1E293B] px-3.5 py-2.5 rounded-lg border border-[#E5E7EB] shadow-md text-xs space-y-1.5 min-w-[205px]">
                        <div className="font-semibold border-b border-[#E5E7EB] pb-1.5 flex justify-between items-center gap-4">
                          <span className="tabular-nums">{formatDateVN(data.date)}</span>
                          <span
                            className={`text-[10.5px] px-1.5 py-0.5 rounded font-semibold ${
                              data.isForecast
                                ? 'bg-blue-50 text-blue-700'
                                : 'bg-[#F0F7F4] text-[#2F6F4E]'
                            }`}
                          >
                            {data.isForecast ? 'Dự báo' : 'Lịch sử'}
                          </span>
                        </div>
                        {!data.isForecast && data.actualPrice != null && (
                          <div className="flex justify-between items-center gap-4">
                            <span className="text-[#64748B]">Giá thực tế:</span>
                            <span className="tabular-nums font-bold text-[#2F6F4E]">
                              {formatNumberVN(Math.round(data.actualPrice))} {currentCommodity.unit}
                            </span>
                          </div>
                        )}
                        {data.isForecast && data.predictedPrice != null && (
                          <>
                            <div className="flex justify-between items-center gap-4">
                              <span className="text-[#64748B]">Giá dự báo:</span>
                              <span className="tabular-nums font-bold text-blue-600">
                                {formatNumberVN(Math.round(data.predictedPrice))} {currentCommodity.unit}
                              </span>
                            </div>
                            <div className="flex justify-between items-center gap-4 pt-1 border-t border-[#E5E7EB] text-[11px]">
                              <span className="text-[#64748B]">95% CI:</span>
                              <span className="tabular-nums text-[#334155]">
                                {formatNumberVN(Math.round(data.lowerCI))} – {formatNumberVN(Math.round(data.upperCI))} {currentCommodity.unit}
                              </span>
                            </div>
                          </>
                        )}
                      </div>
                    );
                  }
                  return null;
                }}
              />

              {chartMode === 'forecast' && (
                <Area
                  type="monotone"
                  dataKey="ciBand"
                  stroke="#93C5FD"
                  strokeDasharray="3 3"
                  strokeWidth={1}
                  fill="url(#ciBandFill)"
                  baseValue="dataMin"
                  connectNulls={false}
                  isAnimationActive={false}
                />
              )}

              <Line
                type="monotone"
                dataKey="actualLine"
                stroke="#2F6F4E"
                strokeWidth={2.25}
                dot={{ r: 2.5, fill: '#2F6F4E', strokeWidth: 0 }}
                activeDot={{ r: 4.5, fill: '#2F6F4E', stroke: '#FFFFFF', strokeWidth: 2 }}
                connectNulls={false}
                isAnimationActive={false}
              />

              {chartMode === 'forecast' && (
                <Line
                  type="monotone"
                  dataKey="forecastLine"
                  stroke="#2563EB"
                  strokeWidth={2.25}
                  strokeDasharray="5 4"
                  dot={{ r: 2.5, fill: '#2563EB', strokeWidth: 0 }}
                  activeDot={{ r: 4.5, fill: '#2563EB', stroke: '#FFFFFF', strokeWidth: 2 }}
                  connectNulls={false}
                  isAnimationActive={false}
                />
              )}
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Horizontal 2-Tab System below Forecast Chart: [Tab 1: Bảng chi tiết dự báo] | [Tab 2: So sánh 5 mô hình] */}
      {chartMode === 'forecast' && (
        <section className="space-y-3">
          <div className="flex items-center gap-1.5 border-b border-[#E5E7EB] pb-2">
            <button
              type="button"
              onClick={() => setActiveBottomTab('table')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeBottomTab === 'table'
                  ? 'bg-[#2F6F4E] text-white'
                  : 'bg-white text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB]'
              }`}
            >
              Bảng chi tiết dự báo ({forecastDays} ngày)
            </button>
            <button
              type="button"
              onClick={() => setActiveBottomTab('models')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                activeBottomTab === 'models'
                  ? 'bg-[#2F6F4E] text-white'
                  : 'bg-white text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB]'
              }`}
            >
              So sánh 5 mô hình ({comparisonData.length})
            </button>
          </div>

          {/* Tab 1: Forecast Schedule DataGrid (Single Export CSV button inside AgroGrid toolbar) */}
          {activeBottomTab === 'table' && (
            <AgroGrid
              fileName={`du-bao-${currentCommodity.code}-${selectedModel}`}
              pageSize={15}
              height={360}
              data={forecastOnlyData.map((item, idx) => {
                const changeValue = basePrice
                  ? Number((((item.predictedPrice - basePrice) / basePrice) * 100).toFixed(2))
                  : 0;
                return {
                  id: idx + 1,
                  date: item.date,
                  horizonLabel: `Ngày +${idx + 1}`,
                  predictedPrice: Math.round(item.predictedPrice),
                  lowerCI: Math.round(item.lowerCI),
                  upperCI: Math.round(item.upperCI),
                  changePct: changeValue,
                  unit: currentCommodity.unit,
                };
              })}
              columns={[
                { field: 'date', headerText: 'Ngày dự báo', kind: 'date', width: 130 },
                { field: 'horizonLabel', headerText: 'Kỳ hạn', kind: 'text', width: 110 },
                {
                  field: 'predictedPrice',
                  headerText: `Giá dự báo (${currentCommodity.unit})`,
                  kind: 'money',
                  unitField: 'unit',
                  width: 180,
                },
                {
                  field: 'lowerCI',
                  headerText: 'Biên dưới 95% CI',
                  kind: 'money',
                  unitField: 'unit',
                  width: 170,
                },
                {
                  field: 'upperCI',
                  headerText: 'Biên trên 95% CI',
                  kind: 'money',
                  unitField: 'unit',
                  width: 170,
                },
                {
                  field: 'changePct',
                  headerText: 'Thay đổi (%)',
                  kind: 'pct',
                  width: 130,
                  template: (row: Record<string, unknown>) => {
                    const val = Number(row.changePct ?? 0);
                    const isUp = val >= 0;
                    return (
                      <span
                        className={`font-semibold tabular-nums ${
                          isUp ? 'text-[#15803D]' : 'text-[#DC2626]'
                        }`}
                      >
                        {formatPct(val, 2)}
                      </span>
                    );
                  },
                },
              ] as AgroColumn[]}
            />
          )}

          {/* Tab 2: 5-Model Comparison Bar Chart + Summary Metrics Table side by side */}
          {activeBottomTab === 'models' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-stretch">
              {comparisonData.length > 0 && (
                <ModelComparisonChart
                  data={comparisonData}
                  metricToDisplay={metricToDisplay}
                  onMetricChange={(m) => setMetricToDisplay(m)}
                  unit={currentCommodity.unit}
                />
              )}

              <div className="bg-white rounded-xl border border-[#E5E7EB] p-4 sm:p-5 flex flex-col justify-between gap-3">
                <div>
                  <div className="pb-2.5 border-b border-[#E5E7EB] flex items-center justify-between gap-2">
                    <h3 className="text-[14px] font-bold text-[#1E293B]">
                      Bảng tổng hợp chỉ số kiểm thử (Walk-Forward)
                    </h3>
                    <span className="text-xs text-[#64748B]">Đơn vị: {currentCommodity.unit}</span>
                  </div>

                  <div className="overflow-x-auto mt-2">
                    <table className="w-full text-left text-xs border-collapse">
                      <thead className="bg-[#F8FAF9] text-[#64748B] uppercase text-[11px] font-semibold border-b border-[#E5E7EB]">
                        <tr>
                          <th className="py-2 px-2.5">Mô hình</th>
                          <th className="py-2 px-2.5 text-right">Độ chính xác</th>
                          <th className="py-2 px-2.5 text-right">MAPE</th>
                          <th className="py-2 px-2.5 text-right">RMSE</th>
                          <th className="py-2 px-2.5 text-right">R²</th>
                          <th className="py-2 px-2.5 text-right">PICP 95%</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-[#E5E7EB] text-[12.5px]">
                        {comparisonData.map((m) => {
                          const acc = m.accuracy ?? Math.max(0, 100 - (m.mape || 0));
                          return (
                            <tr key={m.modelName} className="hover:bg-[#F8FAF9]">
                              <td className="py-2.5 px-2.5 font-semibold text-[#1E293B]">
                                <div className="flex items-center gap-1.5">
                                  <span>{m.modelName}</span>
                                  {m.isBest && (
                                    <span className="px-1.5 py-0.5 rounded bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20 text-[10px] font-semibold">
                                      Tốt nhất
                                    </span>
                                  )}
                                </div>
                              </td>
                              <td className="py-2.5 px-2.5 text-right tabular-nums font-bold text-[#2F6F4E]">
                                {acc.toFixed(2)}%
                              </td>
                              <td className="py-2.5 px-2.5 text-right tabular-nums text-[#334155]">
                                {m.mape.toFixed(2)}%
                              </td>
                              <td className="py-2.5 px-2.5 text-right tabular-nums text-[#1E293B]">
                                {formatNumberVN(Math.round(m.rmse))}
                              </td>
                              <td className="py-2.5 px-2.5 text-right tabular-nums text-[#334155]">
                                {m.r2.toFixed(3)}
                              </td>
                              <td className="py-2.5 px-2.5 text-right tabular-nums text-[#334155]">
                                {m.picp95 != null ? `${m.picp95.toFixed(1)}%` : '—'}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>

                <p className="text-[11px] text-[#64748B] border-t border-[#E5E7EB] pt-2">
                  Độ chính xác = <span className="font-semibold text-[#334155]">100% − MAPE</span>. Đánh giá trên tập kiểm thử lịch sử (Walk-Forward, không rò rỉ dữ liệu), không cam kết tuyệt đối cho biến động bất thường tương lai.
                </p>
              </div>
            </div>
          )}
        </section>
      )}

      {/* Subtle 1-Line Footnote for Training Dataset Info */}
      {training && (
        <p className="text-xs text-[#64748B] tabular-nums pt-1 flex flex-wrap items-center justify-between gap-2 border-t border-[#E5E7EB]">
          <span>
            Tập huấn luyện: <strong className="text-[#334155]">{formatNumberVN(training.observation_count)}</strong> ngày quan sát ({formatDateVN(training.start_date)} – {formatDateVN(training.end_date)}) · Tập kiểm thử: <strong className="text-[#334155]">{training.test_count}</strong> ngày ({formatDateVN(training.test_start)} → {formatDateVN(training.test_end)})
          </span>
          <Link
            href={`/history?commodity_id=${selectedCommodityId}`}
            className="text-[#2F6F4E] font-semibold hover:underline"
          >
            Xem dữ liệu lịch sử gốc →
          </Link>
        </p>
      )}
    </div>
  );
}
