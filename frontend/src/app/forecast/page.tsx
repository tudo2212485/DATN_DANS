'use client';

import React, { useState, useEffect, useMemo } from 'react';
import TrainingSummary from '@/components/forecast/TrainingSummary';
import {
  TrainingMetadata,
  fetchHistory,
  fetchHistorySources,
  fetchTrainingReadiness,
  HistorySource,
  fetchForecastDashboard,
  fetchModelComparison,
} from '@/lib/api';
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
import { ModelMetrics, ForecastPoint, ModelComparisonMetrics, RegionInfo } from '@/types';
import ModelComparisonChart from '@/components/forecast/ModelComparisonChart';
import XAIFeatureDrivers from '@/components/forecast/XAIFeatureDrivers';
import {
  TrendingUp,
  TrendingDown,
  Download,
  MapPin,
} from 'lucide-react';

type SupportedModel = 'LSTM' | 'Prophet' | 'ARIMA' | 'XGBoost' | 'Random Forest';
type ChartMode = 'forecast' | 'history' | 'periodic' | 'empty';
type ChartPoint = ForecastPoint & { sellingPrice?: number };

function normalizeModelName(name: string): SupportedModel {
  const normalized = name.toLowerCase().replace(/[_\s-]/g, '');
  if (normalized === 'randomforest') return 'Random Forest';
  if (normalized === 'xgboost') return 'XGBoost';
  if (normalized === 'prophet') return 'Prophet';
  if (normalized === 'arima') return 'ARIMA';
  return 'LSTM';
}

function formatShortDate(raw: string): string {
  if (!raw) return '';
  if (/^\d{4}-\d{2}-\d{2}$/.test(raw)) {
    const [, m, d] = raw.split('-');
    return `${d}/${m}`;
  }
  return raw;
}

export default function ForecastPage() {
  const [training, setTraining] = useState<TrainingMetadata>();
  const [catalog, setCatalog] = useState<HistorySource[]>([]);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(0);
  const [selectedModel, setSelectedModel] = useState<SupportedModel>('LSTM');
  const [forecastDays, setForecastDays] = useState<number>(10);
  const [selectedRegion, setSelectedRegion] = useState<string>('all');
  const [availableRegions, setAvailableRegions] = useState<RegionInfo[]>([]);

  const [metrics, setMetrics] = useState<ModelMetrics>({
    modelName: 'LSTM',
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
    initializeCommodity();
    return () => {
      active = false;
    };
  }, []);

  const currentCommodity =
    catalog.find((c) => c.id === selectedCommodityId) || {
      name: 'Nông sản',
      unit: 'VNĐ/kg',
      code: '',
      kind: 'daily' as const,
    };
  const isPeriodic = currentCommodity.kind === 'periodic';
  const isIrregular = currentCommodity.kind === 'irregular';
  const usesPublicationCadence = isPeriodic || isIrregular;
  const horizonUnit = 'ngày';

  useEffect(() => {
    if (selectedCommodityId > 0) {
      setForecastDays(10);
      setSelectedRegion('all');
    }
  }, [selectedCommodityId]);

  useEffect(() => {
    if (selectedCommodityId <= 0) return;
    let isMounted = true;
    async function loadForecast() {
      setLoading(true);
      setError('');
      setForecastData([]);
      setComparisonData([]);
      setTraining(undefined);
      setChartMode('empty');
      setMetrics({ modelName: selectedModel, mae: 0, rmse: 0, mape: 0, r2: 0, trainDate: 'N/A' });
      try {
        const [res, compRes] = await Promise.all([
          fetchForecastDashboard(selectedCommodityId, selectedModel, forecastDays, selectedRegion),
          fetchModelComparison(selectedCommodityId),
        ]);
        if (isMounted) {
          if (res?.metrics) setMetrics(res.metrics);
          setTraining(res.training);
          if (res?.availableRegions) setAvailableRegions(res.availableRegions);
          if (res?.forecastData && res.forecastData.length > 0) {
            setForecastData(res.forecastData);
            setChartMode('forecast');
          }
          if (compRes) setComparisonData(compRes);
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
            end.toISOString().slice(0, 10)
          );
          if (!isMounted) return;
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
          } else if (history.periodic_records.length > 0) {
            setForecastData(
              history.periodic_records.map((record) => ({
                date: record.published_date,
                actualPrice: record.buying_price,
                sellingPrice: record.selling_price,
                predictedPrice: record.buying_price,
                lowerCI: record.buying_price,
                upperCI: record.buying_price,
                isForecast: false,
              }))
            );
            setChartMode('periodic');
            setError(`${forecastError} Đang hiển thị báo cáo giá mua và giá bán theo kỳ.`);
          } else {
            setError(forecastError);
          }
        } catch {
          if (isMounted) setError(forecastError);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    loadForecast();
    return () => {
      isMounted = false;
    };
  }, [selectedCommodityId, selectedModel, forecastDays, selectedRegion]);

  // Connect the last historical point to the first forecast point so the chart line is continuous
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

  // Compute tight Y-axis domain so the chart never squishes to zero
  const yDomain = useMemo<[number, number]>(() => {
    const values: number[] = [];
    for (const p of chartSeries) {
      if (typeof p.actualLine === 'number' && p.actualLine > 0) values.push(p.actualLine);
      if (typeof p.sellingPrice === 'number' && p.sellingPrice > 0) values.push(p.sellingPrice);
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

  const recommendedModel = useMemo(
    () =>
      comparisonData
        .filter((item) => Number.isFinite(item.rmse) && item.rmse > 0)
        .sort((a, b) => a.rmse - b.rmse)[0],
    [comparisonData]
  );

  const activeRegionObj = availableRegions.find((r) => r.id === selectedRegion);

  const handleExportCSV = () => {
    if (!forecastOnlyData || forecastOnlyData.length === 0) return;
    const headers = [
      'Ngày',
      'Nông sản',
      'Khu vực',
      'Mô hình',
      `Giá dự báo (${currentCommodity.unit})`,
      'Ngưỡng dưới',
      'Ngưỡng trên',
    ];
    const rows = forecastOnlyData.map((item) => [
      item.date,
      currentCommodity.name,
      activeRegionObj?.name || 'Bình quân',
      selectedModel,
      Math.round(item.predictedPrice),
      Math.round(item.lowerCI),
      Math.round(item.upperCI),
    ]);
    const csvContent =
      'data:text/csv;charset=utf-8,\uFEFF' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute(
      'download',
      `Du_bao_${currentCommodity.code}_${selectedModel}_${forecastDays}ngay.csv`
    );
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-5 max-w-[1440px] mx-auto pb-12 font-sans">
      <Header
        title="Phân tích & Dự báo giá nông sản tại vườn"
        subtitle="Mô hình dự báo chuỗi thời gian kết hợp chênh lệch giá nông hộ bán ra tại vườn / ruộng từng địa phương"
        showLiveBadge={true}
      />

      {error && (
        <div
          role="alert"
          className={`px-4 py-3 rounded-lg border text-[13px] ${
            chartMode === 'history' || chartMode === 'periodic'
              ? 'bg-amber-50/80 text-amber-900 border-amber-200'
              : 'bg-rose-50/80 text-rose-800 border-rose-200'
          }`}
        >
          {error}
        </div>
      )}

      {/* Unified Instrument & Filter Bar */}
      <div className="bg-white rounded-xl border border-zinc-200/90 shadow-[0_1px_2px_rgba(0,0,0,0.02)] divide-y divide-zinc-100">
        {/* Top Control Row */}
        <div className="p-3.5 sm:px-5 flex flex-wrap items-center justify-between gap-3">
          {/* Left: Commodity Selector */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2">
              <label htmlFor="commodity-select" className="text-[12.5px] font-medium text-zinc-500">
                Mặt hàng:
              </label>
              <select
                id="commodity-select"
                value={selectedCommodityId}
                onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
                className="bg-zinc-50 hover:bg-zinc-100/80 border border-zinc-200 text-zinc-900 text-[13.5px] font-semibold rounded-lg px-3 py-1.5 focus:outline-none focus:border-zinc-400 transition-colors cursor-pointer"
              >
                {catalog.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.unit})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Right: Model & Horizon Segmented Controls */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Algorithm Tabs */}
            <div className="flex items-center gap-2">
              <span className="text-[12.5px] font-medium text-zinc-500 hidden sm:inline">
                Mô hình:
              </span>
              <div className="flex flex-wrap items-center gap-0.5 bg-zinc-100 p-0.5 rounded-lg border border-zinc-200/60">
                {(['LSTM', 'Prophet', 'ARIMA', 'XGBoost', 'Random Forest'] as const).map(
                  (model) => (
                    <button
                      key={model}
                      onClick={() => setSelectedModel(model)}
                      className={`px-2.5 py-1 rounded-md text-[12.5px] transition-all cursor-pointer ${
                        selectedModel === model
                          ? 'bg-white text-zinc-900 font-semibold shadow-2xs'
                          : 'text-zinc-600 font-medium hover:text-zinc-900'
                      }`}
                    >
                      {model}
                    </button>
                  )
                )}
              </div>
            </div>

            {/* Horizon Tabs */}
            <div className="flex items-center gap-2">
              <span className="text-[12.5px] font-medium text-zinc-500 hidden md:inline">
                Kỳ hạn:
              </span>
              <div className="flex items-center gap-0.5 bg-zinc-100 p-0.5 rounded-lg border border-zinc-200/60">
                {[7, 10, 14, 30].map((days) => (
                  <button
                    key={days}
                    onClick={() => setForecastDays(days)}
                    className={`px-2.5 py-1 rounded-md text-[12.5px] transition-all cursor-pointer ${
                      forecastDays === days
                        ? 'bg-white text-zinc-900 font-semibold shadow-2xs'
                        : 'text-zinc-600 font-medium hover:text-zinc-900'
                    }`}
                  >
                    {days} ngày
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Region Row (Spatio-Temporal Selector) */}
        {availableRegions.length > 0 && (
          <div className="px-3.5 py-2.5 sm:px-5 bg-zinc-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-[12px] font-medium text-zinc-500 flex items-center gap-1 mr-1">
                <MapPin className="w-3.5 h-3.5 text-zinc-400" />
                <span>Địa phương (Bán tại vườn/ruộng):</span>
              </span>
              {availableRegions.map((r) => {
                const isSelected = selectedRegion === r.id;
                return (
                  <button
                    key={r.id}
                    onClick={() => setSelectedRegion(r.id)}
                    className={`px-2.5 py-1 rounded-md text-[12px] transition-all flex items-center gap-1.5 cursor-pointer border ${
                      isSelected
                        ? 'bg-zinc-900 text-white border-zinc-900 font-medium'
                        : 'bg-white text-zinc-600 hover:text-zinc-900 border-zinc-200/80 hover:border-zinc-300 font-normal'
                    }`}
                  >
                    <span>{r.name}</span>
                    {r.basisSpread !== 0 && (
                      <span
                        className={`text-[10.5px] font-mono ${
                          isSelected
                            ? 'text-zinc-300'
                            : r.basisSpread > 0
                              ? 'text-emerald-700'
                              : 'text-amber-700'
                        }`}
                      >
                        {r.basisSpread > 0 ? `+${r.basisSpread}` : r.basisSpread}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            {activeRegionObj && (
              <span className="text-[12px] text-zinc-500 shrink-0">
                {activeRegionObj.description}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Unified 4-Column Metric Strip */}
      {chartMode === 'forecast' && forecastData.length > 0 && (
        <section
          aria-label="Chỉ số tổng hợp"
          className="bg-white rounded-xl border border-zinc-200/90 shadow-[0_1px_2px_rgba(0,0,0,0.02)] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200/70"
        >
          {/* Col 1: Current Price */}
          <div className="p-4 sm:p-5">
            <p className="text-[12.5px] font-medium text-zinc-500">Giá bán tại vườn / ruộng</p>
            <div className="mt-2 flex items-baseline gap-1.5">
              <span className="text-2xl font-bold font-mono text-zinc-900 tracking-tight">
                {Math.round(basePrice).toLocaleString('vi-VN')}
              </span>
              <span className="text-[12px] font-medium text-zinc-500">{currentCommodity.unit}</span>
            </div>
            <p className="mt-1.5 text-[12px] text-zinc-500 truncate">
              {activeRegionObj?.name || 'Giá bán trực tiếp tại địa phương'}
            </p>
          </div>

          {/* Col 2: End-of-horizon Forecast */}
          <div className="p-4 sm:p-5">
            <div className="flex items-center justify-between gap-2">
              <p className="text-[12.5px] font-medium text-zinc-500">
                Dự báo sau {forecastDays} {horizonUnit}
              </p>
              <span
                className={`inline-flex items-center gap-0.5 text-[11.5px] font-semibold font-mono px-1.5 py-0.5 rounded ${
                  projectedChange >= 0
                    ? 'bg-emerald-50 text-emerald-700'
                    : 'bg-rose-50 text-rose-700'
                }`}
              >
                {projectedChange >= 0 ? (
                  <TrendingUp className="w-3 h-3" />
                ) : (
                  <TrendingDown className="w-3 h-3" />
                )}
                {projectedChange >= 0 ? '+' : ''}
                {projectedChange.toFixed(2)}%
              </span>
            </div>
            <div className="mt-2 flex items-baseline gap-1.5">
              <span className="text-2xl font-bold font-mono text-zinc-900 tracking-tight">
                {lastForecastPoint
                  ? Math.round(lastForecastPoint.predictedPrice).toLocaleString('vi-VN')
                  : '—'}
              </span>
              <span className="text-[12px] font-medium text-zinc-500">{currentCommodity.unit}</span>
            </div>
            <p className="mt-1.5 text-[12px] text-zinc-500 font-mono">
              {projectedDiffVnd >= 0 ? `+${projectedDiffVnd.toLocaleString('vi-VN')}` : projectedDiffVnd.toLocaleString('vi-VN')} đ · Ngày {lastForecastPoint?.date || '—'}
            </p>
          </div>

          {/* Col 3: Confidence Interval Range */}
          <div className="p-4 sm:p-5">
            <p className="text-[12.5px] font-medium text-zinc-500">Biên độ dao động cuối kỳ</p>
            <div className="mt-2 flex items-baseline gap-1.5 font-mono">
              <span className="text-[19px] font-bold text-zinc-900 tracking-tight">
                {lastForecastPoint
                  ? `${Math.round(lastForecastPoint.lowerCI).toLocaleString('vi-VN')} – ${Math.round(lastForecastPoint.upperCI).toLocaleString('vi-VN')}`
                  : '—'}
              </span>
            </div>
            <p className="mt-1.5 text-[12px] text-zinc-500">
              Khoảng ước lượng theo sai số RMSE (±{Math.round(metrics.rmse || 0).toLocaleString('vi-VN')} đ)
            </p>
          </div>

          {/* Col 4: Model Accuracy & Recommendation */}
          <div className="p-4 sm:p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-2">
                <p className="text-[12.5px] font-medium text-zinc-500">Sai số mô hình (MAPE)</p>
                <span className="text-[11px] font-medium text-zinc-500">
                  Huấn luyện: {metrics.trainDate}
                </span>
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-bold font-mono text-zinc-900 tracking-tight">
                  {Number(metrics.mape || 0).toFixed(2)}%
                </span>
                <span className="text-[12px] text-zinc-500">
                  (MAE: {Math.round(metrics.mae || 0).toLocaleString('vi-VN')} đ)
                </span>
              </div>
            </div>

            {recommendedModel &&
            normalizeModelName(recommendedModel.modelName) !== selectedModel ? (
              <div className="mt-1.5 flex items-center justify-between text-[12px]">
                <span className="text-zinc-500">
                  Tối ưu nhất: <strong className="text-zinc-800">{recommendedModel.modelName}</strong>
                </span>
                <button
                  onClick={() => setSelectedModel(normalizeModelName(recommendedModel.modelName))}
                  className="text-emerald-700 hover:text-emerald-800 font-semibold underline cursor-pointer"
                >
                  Áp dụng
                </button>
              </div>
            ) : (
              <p className="mt-1.5 text-[12px] text-emerald-700 font-medium">
                Đang dùng mô hình có sai số thấp nhất
              </p>
            )}
          </div>
        </section>
      )}

      {/* Main Price & Forecast Chart */}
      <div className="bg-white rounded-xl border border-zinc-200/90 p-5 shadow-[0_1px_2px_rgba(0,0,0,0.02)] space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3.5 border-b border-zinc-100">
          <div>
            <h2 className="text-[15.5px] font-semibold text-zinc-900">
              {chartMode === 'forecast' &&
                `Diễn biến giá ${currentCommodity.name.toLowerCase()} và dự báo ${forecastDays} ngày tới (${selectedModel})`}
              {chartMode === 'history' && `Lịch sử giá ${currentCommodity.name.toLowerCase()}`}
              {chartMode === 'periodic' &&
                `Giá mua và giá bán ${currentCommodity.name.toLowerCase()} theo kỳ`}
              {chartMode === 'empty' && `Biểu đồ giá ${currentCommodity.name.toLowerCase()}`}
            </h2>
            <p className="text-[12.5px] text-zinc-500 mt-0.5">
              {chartMode === 'forecast' &&
                `Đơn vị: ${currentCommodity.unit} · Khu vực: ${activeRegionObj?.name || 'Bình quân'} · Dữ liệu lịch sử 30 mốc gần nhất kết nối trực tiếp với chuỗi dự báo`}
              {chartMode === 'history' &&
                'Hiển thị dữ liệu lịch sử đã xác minh (chưa đủ điều kiện tạo chuỗi dự báo mới)'}
              {chartMode === 'periodic' && 'Dữ liệu thu thập theo kỳ công bố'}
              {chartMode === 'empty' && 'Đang tải hoặc chưa có dữ liệu hiển thị'}
            </p>
          </div>

          {/* Clean Legend */}
          <div className="flex flex-wrap items-center gap-4 text-[12px] font-medium text-zinc-600 shrink-0">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-0.5 bg-[#059669]" />
              <span>{chartMode === 'periodic' ? 'Giá mua' : 'Giá thực tế'}</span>
            </div>
            {chartMode === 'periodic' && (
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-0.5 bg-[#7C3AED]" />
                <span>Giá bán</span>
              </div>
            )}
            {chartMode === 'forecast' && (
              <>
                <div className="flex items-center gap-1.5">
                  <span className="w-3.5 h-0 border-b-2 border-dashed border-[#2563EB]" />
                  <span>Dự báo ({selectedModel})</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-2.5 rounded-xs bg-blue-500/15 border border-blue-500/30" />
                  <span>Vùng ước lượng</span>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Chart Area */}
        <div className="w-full h-[390px] pt-1">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart
              data={chartSeries}
              margin={{ top: 12, right: 16, left: 4, bottom: 4 }}
            >
              <defs>
                <linearGradient id="ciBandFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#2563EB" stopOpacity={0.14} />
                  <stop offset="100%" stopColor="#2563EB" stopOpacity={0.03} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F4F4F5" />
              <XAxis
                dataKey="shortDate"
                tickLine={false}
                axisLine={{ stroke: '#E4E4E7' }}
                tick={{ fill: '#71717A', fontSize: 11.5, fontWeight: 400 }}
                dy={6}
                minTickGap={18}
              />
              <YAxis
                domain={yDomain}
                tickLine={false}
                axisLine={false}
                width={56}
                tickFormatter={(val) =>
                  val >= 1000000
                    ? `${(val / 1000000).toFixed(2)}tr`
                    : val >= 1000
                      ? `${(val / 1000).toLocaleString('vi-VN')}k`
                      : String(val)
                }
                tick={{ fill: '#71717A', fontSize: 11.5, fontWeight: 400 }}
              />
              {lastHistoryPoint && chartMode === 'forecast' && (
                <ReferenceLine
                  x={formatShortDate(lastHistoryPoint.date)}
                  stroke="#D4D4D8"
                  strokeDasharray="3 3"
                />
              )}
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-zinc-900 text-white px-3.5 py-2.5 rounded-lg shadow-xl text-[12px] space-y-1.5 z-30 min-w-[200px]">
                        <div className="font-medium border-b border-zinc-800 pb-1.5 flex justify-between items-center gap-4">
                          <span className="text-zinc-300 font-mono">{data.date}</span>
                          <span
                            className={`text-[10.5px] px-1.5 py-0.5 rounded font-medium ${
                              data.isForecast
                                ? 'bg-blue-500/20 text-blue-300'
                                : 'bg-emerald-500/20 text-emerald-300'
                            }`}
                          >
                            {data.isForecast ? 'Dự báo' : 'Lịch sử'}
                          </span>
                        </div>
                        {!data.isForecast && data.actualPrice != null && (
                          <div className="flex justify-between items-center gap-4">
                            <span className="text-zinc-400">
                              {chartMode === 'periodic' ? 'Giá mua:' : 'Giá thực tế:'}
                            </span>
                            <span className="font-mono font-semibold text-emerald-400">
                              {Math.round(data.actualPrice).toLocaleString('vi-VN')} đ
                            </span>
                          </div>
                        )}
                        {data.sellingPrice != null && (
                          <div className="flex justify-between items-center gap-4">
                            <span className="text-zinc-400">Giá bán:</span>
                            <span className="font-mono font-semibold text-purple-300">
                              {Math.round(data.sellingPrice).toLocaleString('vi-VN')} đ
                            </span>
                          </div>
                        )}
                        {data.isForecast && data.predictedPrice != null && (
                          <>
                            <div className="flex justify-between items-center gap-4">
                              <span className="text-zinc-400">Giá dự báo:</span>
                              <span className="font-mono font-semibold text-blue-400">
                                {Math.round(data.predictedPrice).toLocaleString('vi-VN')} đ
                              </span>
                            </div>
                            <div className="flex justify-between items-center gap-4 pt-1 border-t border-zinc-800 text-[11px]">
                              <span className="text-zinc-400">Biên độ:</span>
                              <span className="font-mono text-zinc-300">
                                {Math.round(data.lowerCI).toLocaleString('vi-VN')} –{' '}
                                {Math.round(data.upperCI).toLocaleString('vi-VN')} đ
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

              {/* Confidence Interval Area */}
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

              {/* Historical Actual Price Line */}
              <Line
                type="monotone"
                dataKey="actualLine"
                stroke="#059669"
                strokeWidth={2.25}
                dot={{ r: 2.5, fill: '#059669', strokeWidth: 0 }}
                activeDot={{ r: 4.5, fill: '#059669', stroke: '#FFFFFF', strokeWidth: 2 }}
                connectNulls={false}
                isAnimationActive={false}
              />

              {/* Periodic Selling Price Line */}
              {chartMode === 'periodic' && (
                <Line
                  type="monotone"
                  dataKey="sellingPrice"
                  stroke="#7C3AED"
                  strokeWidth={2.25}
                  dot={{ r: 2.5, fill: '#7C3AED', strokeWidth: 0 }}
                  isAnimationActive={false}
                />
              )}

              {/* Forecast Price Line */}
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

      {/* Two-Column Analysis Section */}
      {chartMode === 'forecast' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <XAIFeatureDrivers
            commodityCode={currentCommodity.code}
            commodityName={currentCommodity.name}
            modelName={selectedModel}
          />

          <div className="space-y-5 flex flex-col justify-between">
            {comparisonData.length > 0 && (
              <ModelComparisonChart
                data={comparisonData}
                metricToDisplay={metricToDisplay}
                onMetricChange={(m) => setMetricToDisplay(m)}
              />
            )}

            {/* Compact Model Metrics Table */}
            <div className="bg-white rounded-xl border border-zinc-200/90 p-5">
              <div className="flex items-center justify-between pb-3 border-b border-zinc-100">
                <h3 className="text-[14px] font-semibold text-zinc-900">
                  Thông số kiểm định mô hình {selectedModel}
                </h3>
                <span className="text-[11.5px] text-zinc-500">Trên tập dữ liệu kiểm thử</span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-3.5">
                <div>
                  <span className="text-[11.5px] text-zinc-500 block">MAE</span>
                  <span className="text-[15px] font-semibold font-mono text-zinc-900 mt-0.5 block">
                    {metrics.mae ? Math.round(metrics.mae).toLocaleString('vi-VN') : '0'} đ
                  </span>
                </div>
                <div>
                  <span className="text-[11.5px] text-zinc-500 block">RMSE</span>
                  <span className="text-[15px] font-semibold font-mono text-zinc-900 mt-0.5 block">
                    {metrics.rmse ? Math.round(metrics.rmse).toLocaleString('vi-VN') : '0'} đ
                  </span>
                </div>
                <div>
                  <span className="text-[11.5px] text-zinc-500 block">MAPE</span>
                  <span className="text-[15px] font-semibold font-mono text-emerald-700 mt-0.5 block">
                    {Number(metrics.mape || 0).toFixed(2)}%
                  </span>
                </div>
                <div>
                  <span className="text-[11.5px] text-zinc-500 block">Hệ số R²</span>
                  <span className="text-[15px] font-semibold font-mono text-zinc-900 mt-0.5 block">
                    {metrics.r2 ? Number(metrics.r2).toFixed(3) : '0.000'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {training && (
        <TrainingSummary training={training} commodityId={selectedCommodityId} rmse={metrics.rmse} />
      )}

      {/* Forecast Schedule Table */}
      {chartMode === 'forecast' && (
        <div className="bg-white rounded-xl border border-zinc-200/90 overflow-hidden shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
          <div className="px-5 py-4 border-b border-zinc-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="text-[15px] font-semibold text-zinc-900">
                Bảng chi tiết giá dự báo ({forecastDays} {horizonUnit} tới)
              </h3>
              <p className="text-[12.5px] text-zinc-500 mt-0.5">
                {usesPublicationCadence
                  ? 'Các mốc dự báo tiếp nối theo chu kỳ công bố'
                  : `Áp dụng cho khu vực: ${activeRegionObj?.name || 'Bình quân'}`}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleExportCSV}
                disabled={forecastOnlyData.length === 0}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-zinc-50 text-zinc-700 border border-zinc-200 text-[12.5px] font-medium transition-colors disabled:opacity-50 cursor-pointer"
              >
                <Download className="w-3.5 h-3.5 text-zinc-500" />
                <span>Tải xuống CSV</span>
              </button>
            </div>
          </div>

          <div className="overflow-x-auto max-h-[380px] custom-scrollbar">
            <table className="w-full text-left text-[13px] border-collapse">
              <thead className="sticky top-0 bg-zinc-50/95 border-b border-zinc-200/80 z-10">
                <tr className="text-zinc-500 font-medium text-[11.5px]">
                  <th className="py-2.5 px-5 font-medium">Ngày dự báo</th>
                  <th className="py-2.5 px-4 font-medium">Kỳ hạn</th>
                  <th className="py-2.5 px-4 font-medium text-right">
                    Giá dự báo ({currentCommodity.unit})
                  </th>
                  <th className="py-2.5 px-4 font-medium text-right">Biên độ thấp nhất</th>
                  <th className="py-2.5 px-4 font-medium text-right">Biên độ cao nhất</th>
                  <th className="py-2.5 px-5 font-medium text-right">Thay đổi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 font-mono text-[12.5px]">
                {forecastOnlyData.length === 0 ? (
                  <tr>
                    <td
                      colSpan={6}
                      className="py-8 text-center text-zinc-500 font-sans"
                    >
                      Chưa có dữ liệu dự báo cho nông sản này.
                    </td>
                  </tr>
                ) : (
                  forecastOnlyData.map((item, idx) => {
                    const changeValue = basePrice
                      ? ((item.predictedPrice - basePrice) / basePrice) * 100
                      : 0;
                    const isPositive = changeValue >= 0;
                    return (
                      <tr key={idx} className="hover:bg-zinc-50/70 transition-colors">
                        <td className="py-2.5 px-5 font-medium text-zinc-900 whitespace-nowrap">
                          {item.date}
                        </td>
                        <td className="py-2.5 px-4 text-zinc-500 font-sans text-[12px] whitespace-nowrap">
                          Ngày +{idx + 1}
                        </td>
                        <td className="py-2.5 px-4 font-semibold text-zinc-900 text-right whitespace-nowrap">
                          {Math.round(item.predictedPrice).toLocaleString('vi-VN')} đ
                        </td>
                        <td className="py-2.5 px-4 text-zinc-500 text-right whitespace-nowrap">
                          {Math.round(item.lowerCI).toLocaleString('vi-VN')} đ
                        </td>
                        <td className="py-2.5 px-4 text-zinc-500 text-right whitespace-nowrap">
                          {Math.round(item.upperCI).toLocaleString('vi-VN')} đ
                        </td>
                        <td className="py-2.5 px-5 text-right whitespace-nowrap">
                          <span
                            className={`inline-flex items-center font-medium ${
                              isPositive ? 'text-emerald-700' : 'text-rose-600'
                            }`}
                          >
                            {isPositive ? '+' : ''}
                            {changeValue.toFixed(2)}%
                          </span>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
