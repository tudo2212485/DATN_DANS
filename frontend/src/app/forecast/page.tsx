'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import TrainingSummary from '@/components/forecast/TrainingSummary';
import {TrainingMetadata, fetchHistory, fetchHistorySources, fetchTrainingReadiness, HistorySource} from '@/lib/api';
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
import { ModelMetrics, ForecastPoint, ModelComparisonMetrics } from '@/types';
import { fetchForecastDashboard, fetchModelComparison } from '@/lib/api';
import ModelComparisonChart from '@/components/forecast/ModelComparisonChart';
import { BrainCircuit, Activity, BarChart3, ShieldCheck, ArrowDownUp, TrendingUp, TrendingDown, Download } from 'lucide-react';

type SupportedModel = 'LSTM' | 'Prophet' | 'ARIMA' | 'XGBoost' | 'Random Forest';
type ChartMode = 'forecast' | 'history' | 'periodic' | 'empty';
type ChartPoint = ForecastPoint & { sellingPrice?: number };

export default function ForecastPage() {
  const [training, setTraining] = useState<TrainingMetadata>();
  const [catalog, setCatalog] = useState<HistorySource[]>([]);
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
        if (active) setSelectedCommodityId(states.find((item) => item.readiness?.ready)?.source.id || sources[0]?.id || 0);
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : 'Không tải được danh mục nông sản');
      }
    }
    initializeCommodity();
    return () => { active = false; };
  }, []);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number>(0);
  const [selectedModel, setSelectedModel] = useState<SupportedModel>('LSTM');
  const [forecastDays, setForecastDays] = useState<number>(10);

  const [metrics, setMetrics] = useState<ModelMetrics>({ modelName: 'LSTM', mae: 0, rmse: 0, mape: 0, r2: 0, trainDate: 'N/A' });
  const [forecastData, setForecastData] = useState<ChartPoint[]>([]);
  const [comparisonData, setComparisonData] = useState<ModelComparisonMetrics[]>([]);
  const [metricToDisplay, setMetricToDisplay] = useState<'mae' | 'rmse' | 'mape' | 'r2'>('mae');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState('');
  const [chartMode, setChartMode] = useState<ChartMode>('empty');

  const currentCommodity =
    catalog.find((c) => c.id === selectedCommodityId) || {name:'Nông sản',unit:'',code:'',kind:'daily' as const};
  const isPeriodic = currentCommodity.kind === 'periodic';
  const isIrregular = currentCommodity.kind === 'irregular';
  const usesPublicationCadence = isPeriodic || isIrregular;
  const cadenceLabel = isPeriodic ? 'kỳ' : isIrregular ? 'mốc công bố' : 'ngày';
  const horizonUnit = 'ngày';

  useEffect(() => {
    if (selectedCommodityId > 0) setForecastDays(10);
  }, [selectedCommodityId]);

  // Fetch forecast data dynamically from FastAPI PostgreSQL backend
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
      setMetrics({modelName:selectedModel, mae:0, rmse:0, mape:0, r2:0, trainDate:'N/A'});
      try {
        const [res, compRes] = await Promise.all([
          fetchForecastDashboard(selectedCommodityId, selectedModel, forecastDays),
          fetchModelComparison(selectedCommodityId)
        ]);
        if (isMounted) {
          if (res?.metrics) setMetrics(res.metrics);
          setTraining(res.training);
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
            end.toISOString().slice(0, 10),
          );
          if (!isMounted) return;
          if (history.records.length > 0) {
            setForecastData(history.records.slice(-180).map((record) => ({
              date: record.date,
              actualPrice: record.price,
              predictedPrice: record.price,
              lowerCI: record.price,
              upperCI: record.price,
              isForecast: false,
            })));
            setChartMode('history');
            setError(`${forecastError} Đang hiển thị dữ liệu lịch sử đã xác minh.`);
          } else if (history.periodic_records.length > 0) {
            setForecastData(history.periodic_records.map((record) => ({
              date: record.published_date,
              actualPrice: record.buying_price,
              sellingPrice: record.selling_price,
              predictedPrice: record.buying_price,
              lowerCI: record.buying_price,
              upperCI: record.buying_price,
              isForecast: false,
            })));
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
  }, [selectedCommodityId, selectedModel, forecastDays]);

  // Format data for Recharts composed chart
  const displayForecastData = forecastData.map((item) => ({
    ...item,
    ciRange: [item.lowerCI, item.upperCI],
  }));

  const forecastOnlyData = displayForecastData.filter(item => item.isForecast);
  const lastHistoryPoint = [...displayForecastData].reverse().find(item => !item.isForecast);
  const basePrice = lastHistoryPoint ? lastHistoryPoint.actualPrice || lastHistoryPoint.predictedPrice : 0;

  const handleExportCSV = () => {
    if (!forecastOnlyData || forecastOnlyData.length === 0) return;
    const headers = ['Ngày', 'Nông sản', 'Mô hình', `Giá dự báo (${currentCommodity.unit})`, 'Ngưỡng dưới ước lượng', 'Ngưỡng trên ước lượng'];
    const rows = forecastOnlyData.map(item => [
      item.date,
      currentCommodity.name,
      selectedModel,
      item.predictedPrice,
      item.lowerCI,
      item.upperCI
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,\uFEFF' 
      + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `Du_bao_${currentCommodity.code}_${selectedModel}_${forecastDays}ngay.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {error && <p role="alert" className={`p-4 rounded-xl border ${chartMode === 'history' || chartMode === 'periodic' ? 'bg-amber-50 text-amber-800 border-amber-200' : 'bg-rose-50 text-rose-700 border-rose-200'}`}>{error}</p>}
      {selectedCommodityId > 0 && <Link className="inline-block text-brand underline" href={`/history?commodity_id=${selectedCommodityId}`}>Xem / thu thập lịch sử giá →</Link>}
      {training && <TrainingSummary training={training} commodityId={selectedCommodityId} rmse={metrics.rmse}/>}
      {/* Header */}
      <Header
        title="Mô hình & Dự báo Giá Nông sản"
        subtitle="Dự báo từ lịch sử có nguồn, kèm dải ước lượng và đánh giá sai số theo thời gian"
        showLiveBadge={false}
      />

      {/* Control Bar: Filters */}
      <div className="bg-card rounded-2xl border border-border-subtle p-4 sm:p-5 shadow-card flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4">
          {/* Commodity Select */}
          <div className="flex flex-col">
            <label className="text-[11px] font-bold text-secondary-text uppercase tracking-wider mb-1.5">
              Chọn nông sản
            </label>
            <select
              value={selectedCommodityId}
              onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
              className="bg-canvas border border-border-subtle text-primary-text text-xs sm:text-sm font-semibold rounded-xl px-3.5 py-2 focus:outline-none focus:ring-2 focus:ring-brand/30 transition-all cursor-pointer"
            >
              {catalog.map((c) => (
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
            <div className="flex flex-wrap items-center gap-1.5 bg-canvas p-1 rounded-xl border border-border-subtle">
              {(['LSTM', 'Prophet', 'ARIMA', 'XGBoost', 'Random Forest'] as const).map((model) => (
                <button
                  key={model}
                  onClick={() => setSelectedModel(model)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    selectedModel === model
                      ? 'bg-brand text-white shadow-xs'
                      : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
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
              {[7, 10, 14, 30].map((days) => (
                <button
                  key={days}
                  onClick={() => setForecastDays(days)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    forecastDays === days
                      ? 'bg-brand text-white shadow-xs font-extrabold'
                      : 'text-secondary-text hover:text-primary-text hover:bg-black/[0.02]'
                  }`}
                >
                  {days} {horizonUnit}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Model Meta Badge */}
        <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-canvas border border-border-subtle text-primary-text text-xs font-semibold">
          <BrainCircuit className="w-4 h-4 text-brand" />
          <span>{loading ? 'Đang tải dữ liệu...' : chartMode === 'forecast' ? `Mô hình: ${metrics.modelName || selectedModel} · huấn luyện ${metrics.trainDate}` : 'Chế độ xem dữ liệu lịch sử'}</span>
        </div>
      </div>

      {/* Metric Cards Row */}
      {chartMode === 'forecast' && forecastData.length > 0 && <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* MAE */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card hover:shadow-hover transition-all">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">MAE (Sai số tuyệt đối)</span>
            <Activity className="w-4 h-4 text-brand" />
          </div>
          <div className="text-2xl font-extrabold text-primary-text font-mono">
            {metrics.mae ? Math.round(metrics.mae).toLocaleString('vi-VN') : '0'} <span className="text-xs font-semibold text-secondary-text font-sans">{currentCommodity.unit}</span>
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Mean Absolute Error (Kiểm thử)</span>
        </div>

        {/* RMSE */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card hover:shadow-hover transition-all">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">RMSE (Căn bậc sai số)</span>
            <BarChart3 className="w-4 h-4 text-amber-600" />
          </div>
          <div className="text-2xl font-extrabold text-primary-text font-mono">
            {metrics.rmse ? Math.round(metrics.rmse).toLocaleString('vi-VN') : '0'} <span className="text-xs font-semibold text-secondary-text font-sans">{currentCommodity.unit}</span>
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Root Mean Squared Error</span>
        </div>

        {/* MAPE */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card hover:shadow-hover transition-all">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">MAPE (% Sai số)</span>
            <span className="text-[10px] font-medium text-secondary-text px-2 py-0.5 rounded bg-canvas border border-border-subtle">
              Tập kiểm thử
            </span>
          </div>
          <div className="text-2xl font-extrabold text-brand font-mono">
            {Number(metrics.mape || 0).toFixed(2)}%
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Mean Absolute Percentage Error</span>
        </div>

        {/* R-Squared */}
        <div className="bg-card rounded-2xl border border-border-subtle p-4 shadow-card hover:shadow-hover transition-all">
          <div className="flex items-center justify-between text-secondary-text mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">R² Score (Hệ số xác định)</span>
            <ShieldCheck className="w-4 h-4 text-brand" />
          </div>
          <div className="text-2xl font-extrabold text-primary-text font-mono">
            {metrics.r2 ? Number(metrics.r2).toFixed(3) : '0.000'}
          </div>
          <span className="text-[11px] text-secondary-text mt-1 block">Goodness of Fit (Tối đa 1.0)</span>
        </div>
      </div>}

      {/* Model Comparison Section */}
      {comparisonData.length > 0 && (
        <ModelComparisonChart
          data={comparisonData}
          metricToDisplay={metricToDisplay}
          onMetricChange={(m) => setMetricToDisplay(m)}
        />
      )}

      {/* Main Forecast Chart with 95% Confidence Interval */}
      <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
          <div>
            <h2 className="text-base font-bold text-primary-text tracking-tight">
              {chartMode === 'forecast' && `Biểu đồ Dự báo ${currentCommodity.name} ${usesPublicationCadence ? `theo ${cadenceLabel}` : ''} & Dải ước lượng (${selectedModel})`}
              {chartMode === 'history' && `Biểu đồ Lịch sử giá ${currentCommodity.name}`}
              {chartMode === 'periodic' && `Biểu đồ Giá mua và Giá bán ${currentCommodity.name} theo kỳ`}
              {chartMode === 'empty' && `Biểu đồ ${currentCommodity.name}`}
            </h2>
            <p className="text-xs text-secondary-text mt-0.5 font-medium">
              {chartMode === 'forecast' && `Đường xanh liền: Giá lịch sử · Đường cam đứt: Dự báo ${selectedModel} · Vùng bóng: Dải ước lượng`}
              {chartMode === 'history' && 'Đường xanh: Giá lịch sử có nguồn xác minh · Chưa vẽ đường dự báo vì chuỗi dữ liệu chưa đủ điều kiện huấn luyện'}
              {chartMode === 'periodic' && 'Đường xanh: Giá mua · Đường tím: Giá bán · Dữ liệu báo cáo theo kỳ, chưa đủ số kỳ để huấn luyện mô hình'}
              {chartMode === 'empty' && 'Chưa có dữ liệu đủ điều kiện để hiển thị'}
            </p>
          </div>

          <div className="flex items-center gap-4 text-xs font-semibold">
            <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-1 rounded bg-[#527853]" />
              <span className="text-secondary-text">{chartMode === 'periodic' ? 'Giá mua' : 'Giá thực tế'}</span>
            </div>
            {chartMode === 'periodic' && <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-1 rounded bg-[#7C3AED]" />
              <span className="text-secondary-text">Giá bán</span>
            </div>}
            {chartMode === 'forecast' && <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-1 rounded bg-[#D97706] border-b border-dashed border-[#D97706]" />
              <span className="text-secondary-text">Dự báo {selectedModel}</span>
            </div>}
            {chartMode === 'forecast' && <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded bg-amber-500/20 border border-amber-500/40" />
              <span className="text-secondary-text">Ước lượng</span>
            </div>}
          </div>
        </div>

        {/* Recharts ComposedChart (~390px) */}
        <div className="w-full h-[390px] pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={displayForecastData.map(p=>({...p,predictedPrice:p.isForecast?p.predictedPrice:null,ciRange:p.isForecast?p.ciRange:null}))} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
              <defs>
                <linearGradient id="forecastCIGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.03} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#EFECE6" />
              <XAxis
                dataKey="date"
                tickLine={false}
                axisLine={{ stroke: '#EFECE6' }}
                tick={{ fill: '#7D6E68', fontSize: 11, fontWeight: 500 }}
                dy={6}
              />
              <YAxis
                domain={['auto', 'auto']}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => `${(val / 1000).toLocaleString('vi-VN')}k`}
                tick={{ fill: '#7D6E68', fontSize: 11, fontWeight: 500 }}
                dx={-4}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-white/95 backdrop-blur-md p-3 rounded-xl border border-border-subtle shadow-xl text-xs space-y-1.5 z-30">
                        <div className="font-bold text-primary-text border-b border-border-subtle/80 pb-1 flex justify-between gap-4">
                          <span>{data.date}</span>
                          <span className="text-[10px] px-1.5 py-0.2 rounded bg-brand-light text-brand">
                            {data.isForecast ? 'Dự báo' : 'Thực tế'}
                          </span>
                        </div>
                        {data.actualPrice != null && (
                          <div className="flex justify-between gap-4 text-emerald-700 font-bold font-mono">
                            <span>{chartMode === 'periodic' ? 'Giá mua:' : 'Giá thực tế:'}</span>
                            <span>{data.actualPrice.toLocaleString('vi-VN')} đ</span>
                          </div>
                        )}
                        {data.sellingPrice != null && (
                          <div className="flex justify-between gap-4 text-violet-700 font-bold font-mono">
                            <span>Giá bán:</span>
                            <span>{data.sellingPrice.toLocaleString('vi-VN')} đ</span>
                          </div>
                        )}
                        {data.isForecast && data.predictedPrice != null && (
                          <div className="flex justify-between gap-4 text-amber-700 font-bold font-mono">
                            <span>Dự báo AI:</span>
                            <span>{data.predictedPrice.toLocaleString('vi-VN')} đ</span>
                          </div>
                        )}
                        {data.isForecast && <div className="text-secondary-text flex justify-between gap-4 pt-1 border-t border-border-subtle/60 text-[11px] font-mono">
                          <span>Ước lượng:</span>
                          <span>
                            [{data.lowerCI.toLocaleString('vi-VN')} - {data.upperCI.toLocaleString('vi-VN')}]
                          </span>
                        </div>}
                      </div>
                    );
                  }
                  return null;
                }}
              />
              {/* Confidence Interval Band */}
              {chartMode === 'forecast' && <Area
                type="monotone"
                dataKey="ciRange"
                stroke="#F59E0B"
                strokeDasharray="4 4"
                strokeWidth={1}
                fill="url(#forecastCIGradient)"
                name="Dải ước lượng"
              />}
              {/* Actual price line (solid olive green) */}
              <Line
                type="monotone"
                dataKey="actualPrice"
                stroke="#527853"
                strokeWidth={3}
                dot={{ r: 4, fill: '#527853', stroke: '#FFFFFF', strokeWidth: 2 }}
                name={chartMode === 'periodic' ? 'Giá mua' : 'Giá thực tế'}
              />
              {chartMode === 'periodic' && <Line
                type="monotone"
                dataKey="sellingPrice"
                stroke="#7C3AED"
                strokeWidth={3}
                dot={{ r: 4, fill: '#7C3AED', stroke: '#FFFFFF', strokeWidth: 2 }}
                name="Giá bán"
              />}
              {/* Forecast price line (dashed amber) */}
              {chartMode === 'forecast' && <Line
                type="monotone"
                dataKey="predictedPrice"
                stroke="#D97706"
                strokeWidth={3}
                strokeDasharray="5 5"
                dot={{ r: 4, fill: '#D97706', stroke: '#FFFFFF', strokeWidth: 2 }}
                name="Dự báo AI"
              />}
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Forecast Details Table with Smooth Vertical Scrollbar & Compact 10-Day Height */}
      {chartMode === 'forecast' && <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3.5">
          <div>
            <h3 className="text-base font-bold text-primary-text flex items-center gap-2">
              <span>Bảng chi tiết giá trị dự báo {forecastDays} {horizonUnit} tới</span>
            </h3>
            <p className="text-xs text-secondary-text mt-0.5 flex items-center gap-1.5">
              <ArrowDownUp className="w-3.5 h-3.5 text-brand" />
              <span>{usesPublicationCadence ? 'Mốc dự báo cách nhau theo nhịp công bố lịch sử, kèm dải ước lượng' : 'Ngày dự báo tính sau mốc lịch sử cuối cùng, kèm dải ước lượng'}</span>
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleExportCSV}
              disabled={forecastOnlyData.length === 0}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-canvas hover:bg-brand/10 text-brand border border-border-subtle hover:border-brand/30 text-xs font-bold transition-all shadow-xs disabled:opacity-50 cursor-pointer"
              title="Xuất dữ liệu dự báo ra file CSV"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Xuất CSV</span>
            </button>
            <span className="text-[11px] font-bold px-2.5 py-1.5 rounded-lg bg-canvas border border-border-subtle text-secondary-text w-fit">
              {forecastOnlyData.length} mốc dự báo
            </span>
          </div>
        </div>

        {/* Scrollable Container with max height displaying ~10 rows neatly with custom scrollbar */}
        <div className="overflow-x-auto overflow-y-auto max-h-[410px] custom-scrollbar rounded-xl border border-border-subtle bg-card shadow-inner">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-[#FAF8F5] border-b border-border-subtle z-10 shadow-2xs backdrop-blur-xs">
              <tr className="text-secondary-text font-bold uppercase tracking-wider">
                <th className="py-3 px-4">Ngày giao dịch</th>
                <th className="py-3 px-4">Mô hình</th>
                <th className="py-3 px-4">Giá dự báo ({currentCommodity.unit})</th>
                <th className="py-3 px-4">Ngưỡng dưới (ước lượng)</th>
                <th className="py-3 px-4">Ngưỡng trên (ước lượng)</th>
                <th className="py-3 px-4 text-right">Biến động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle/80 font-mono text-[11px]">
              {forecastOnlyData.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-secondary-text font-medium font-sans">
                    Chưa có dữ liệu dự báo {selectedModel} cho nông sản này.
                  </td>
                </tr>
              ) : (
                forecastOnlyData.map((item, idx) => {
                  const changeValue = basePrice ? ((item.predictedPrice - basePrice) / basePrice * 100) : 0;
                  const isPositive = changeValue >= 0;
                  return (
                    <tr key={idx} className="hover:bg-canvas/70 transition-colors group">
                      <td className="py-2.5 px-4 font-bold text-primary-text whitespace-nowrap font-sans">
                        {item.date} <span className="text-secondary-text font-normal text-[10px]">(T+{idx + 1})</span>
                      </td>
                      <td className="py-2.5 px-4 whitespace-nowrap font-sans">
                        <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-brand-light text-brand border border-brand/20">
                          {selectedModel}
                        </span>
                      </td>
                      <td className="py-2.5 px-4 font-bold text-primary-text text-sm whitespace-nowrap">
                        {item.predictedPrice.toLocaleString('vi-VN')} đ
                      </td>
                      <td className="py-2.5 px-4 text-secondary-text whitespace-nowrap">
                        {item.lowerCI.toLocaleString('vi-VN')} đ
                      </td>
                      <td className="py-2.5 px-4 text-secondary-text whitespace-nowrap">
                        {item.upperCI.toLocaleString('vi-VN')} đ
                      </td>
                      <td className="py-2.5 px-4 text-right whitespace-nowrap font-sans">
                        <span className={`inline-flex items-center gap-1 font-bold text-xs ${isPositive ? 'text-brand' : 'text-accent-coral'}`}>
                          {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                          {isPositive ? '+' : ''}{changeValue.toFixed(2)}%
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>}
    </div>
  );
}
