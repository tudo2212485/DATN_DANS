'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Header from '@/components/layout/Header';
import {
  fetchCommoditiesOverview,
  fetchMarketComparison,
  fetchRegionalPricesApi,
} from '@/lib/api';
import { CommoditySummary, ComparisonDataPoint, RegionalPriceItem } from '@/types';
import {
  formatNumberVN,
  formatPct,
  getCommodityUnit,
  calculatePearsonCorrelation,
} from '@/lib/formatters';
import FinChart from '@/components/ui/FinChart';
import { useLocation } from '@/contexts/LocationContext';
import {
  TrendingUp,
  MapPin,
  ArrowRight,
  RefreshCw,
  Search,
  Download,
  ArrowUpDown,
} from 'lucide-react';
import Link from 'next/link';

interface SeriesMeta {
  key: 'rice' | 'coffee' | 'pepper' | 'sugar' | 'strawberry' | 'potato' | 'sweet_potato' | 'cashew';
  codeMatch: string;
  defaultLabel: string;
  defaultUnit: string;
  color: string;
}

const SERIES_META: SeriesMeta[] = [
  { key: 'rice', codeMatch: 'RICE', defaultLabel: 'Lúa gạo IR50404', defaultUnit: 'VNĐ/kg', color: '#15803D' },
  { key: 'coffee', codeMatch: 'COFFEE', defaultLabel: 'Cà phê Robusta', defaultUnit: 'VNĐ/kg', color: '#1D4ED8' },
  { key: 'pepper', codeMatch: 'PEPPER', defaultLabel: 'Hồ tiêu đen', defaultUnit: 'VNĐ/kg', color: '#7C3AED' },
  { key: 'sugar', codeMatch: 'SUGAR', defaultLabel: 'Mía đường', defaultUnit: 'VNĐ/tấn', color: '#B45309' },
  { key: 'strawberry', codeMatch: 'STRAWBERRY', defaultLabel: 'Dâu tây Đà Lạt', defaultUnit: 'VNĐ/kg', color: '#E11D48' },
  { key: 'potato', codeMatch: 'POTATO', defaultLabel: 'Khoai tây Đà Lạt', defaultUnit: 'VNĐ/kg', color: '#0891B2' },
  { key: 'sweet_potato', codeMatch: 'SWEETPOTATO', defaultLabel: 'Khoai lang tím Vĩnh Long', defaultUnit: 'VNĐ/kg', color: '#9333EA' },
  { key: 'cashew', codeMatch: 'CASHEW', defaultLabel: 'Hạt điều', defaultUnit: 'VNĐ/kg', color: '#EA580C' },
];

type TimeframeKey = '7N' | '14N' | '30N' | '3T' | '1N';

export default function ComparePage() {
  const { provinceCode, provinceName } = useLocation();
  const [commodities, setCommodities] = useState<CommoditySummary[]>([]);
  const [comparisonData, setComparisonData] = useState<ComparisonDataPoint[]>([]);
  const [regionalPrices, setRegionalPrices] = useState<RegionalPriceItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [timeframe, setTimeframe] = useState<TimeframeKey>('3T');

  const [activeSeries, setActiveSeries] = useState<Record<string, boolean>>({
    rice: true,
    coffee: true,
    pepper: true,
    sugar: true,
    strawberry: true,
    potato: true,
    sweet_potato: true,
    cashew: true,
  });

  // Enterprise DataGrid state
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedRegionFilter, setSelectedRegionFilter] = useState<string>('ALL');
  const [sortCol, setSortCol] = useState<'commodityName' | 'price' | 'changePct'>('commodityName');
  const [sortDir, setSortDir] = useState<'ascending' | 'descending'>('ascending');
  const [page, setPage] = useState<number>(0);
  const pageSize = 8;

  const loadData = async (targetProvince: string = provinceCode) => {
    setIsLoading(true);
    try {
      const [cData, cmpData, rData] = await Promise.all([
        fetchCommoditiesOverview(targetProvince),
        fetchMarketComparison(targetProvince),
        fetchRegionalPricesApi(targetProvince),
      ]);
      if (cData && cData.length > 0) setCommodities(cData);
      if (cmpData && cmpData.length > 0) setComparisonData(cmpData);
      if (rData && rData.length > 0) setRegionalPrices(rData);
    } catch (err) {
      console.error('Failed to load comparison data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setSelectedRegionFilter('ALL');
    void loadData(provinceCode);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [provinceCode]);

  const toggleSeries = (key: string) => {
    setActiveSeries((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      if (!Object.values(next).some(Boolean)) return prev;
      return next;
    });
  };

  // Bind each series card directly to live database commodity data
  const liveSeriesCards = useMemo(() => {
    return SERIES_META.map((meta) => {
      const found = commodities.find((c) => {
        const up = c.code.toUpperCase().replace(/_/g, '');
        if (meta.key === 'potato') return up === 'POTATO';
        if (meta.key === 'sweet_potato') return up === 'SWEETPOTATO';
        return (
          up.includes(meta.codeMatch) ||
          (meta.key === 'sugar' && c.name.toLowerCase().includes('mía'))
        );
      });
      const unit = getCommodityUnit(found?.name || meta.defaultLabel, found?.unit || meta.defaultUnit);
      const currentPrice = found ? found.currentPrice : 0;
      const latestPoint = comparisonData.length > 0 ? comparisonData[comparisonData.length - 1] : null;
      const growthPct = latestPoint ? Number(latestPoint[meta.key] ?? 0) : (found?.changePct ?? 0);

      return {
        ...meta,
        id: found?.id || 1,
        label: found?.name || meta.defaultLabel,
        region: found?.region || 'Vùng chuyên canh',
        currentPrice,
        formattedPrice: currentPrice > 0 ? `${formatNumberVN(currentPrice)} ${unit}` : 'Đang đồng bộ...',
        unit,
        changePct: found?.changePct ?? 0,
        growthPct,
      };
    });
  }, [commodities, comparisonData]);

  // Slice data according to timeframe selector (7N | 14N | 30N | 3T | 1N) and re-normalize to 0% at period start
  const displayedChartData = useMemo(() => {
    if (!comparisonData || comparisonData.length === 0) return [];
    const countMap: Record<TimeframeKey, number> = {
      '7N': 3,
      '14N': 5,
      '30N': 7,
      '3T': 9,
      '1N': comparisonData.length,
    };
    const sliceCount = Math.min(comparisonData.length, countMap[timeframe] || comparisonData.length);
    const sliced = comparisonData.slice(-sliceCount);
    if (sliced.length === 0) return [];
    const first = sliced[0];
    return sliced.map((pt) => ({
      date: pt.date,
      rice: Number(((Number(pt.rice ?? 0) - Number(first.rice ?? 0))).toFixed(2)),
      coffee: Number(((Number(pt.coffee ?? 0) - Number(first.coffee ?? 0))).toFixed(2)),
      pepper: Number(((Number(pt.pepper ?? 0) - Number(first.pepper ?? 0))).toFixed(2)),
      sugar: Number(((Number(pt.sugar ?? 0) - Number(first.sugar ?? 0))).toFixed(2)),
      strawberry: Number(((Number(pt.strawberry ?? 0) - Number(first.strawberry ?? 0))).toFixed(2)),
      potato: Number(((Number(pt.potato ?? 0) - Number(first.potato ?? 0))).toFixed(2)),
      sweet_potato: Number(((Number(pt.sweet_potato ?? 0) - Number(first.sweet_potato ?? 0))).toFixed(2)),
      cashew: Number(((Number(pt.cashew ?? 0) - Number(first.cashew ?? 0))).toFixed(2)),
    }));
  }, [comparisonData, timeframe]);

  // Summary & Pearson Correlation table
  const correlationSummary = useMemo(() => {
    if (displayedChartData.length < 2) return [];
    const seriesVectors: Record<string, number[]> = {
      rice: displayedChartData.map((d) => d.rice),
      coffee: displayedChartData.map((d) => d.coffee),
      pepper: displayedChartData.map((d) => d.pepper),
      sugar: displayedChartData.map((d) => d.sugar),
      strawberry: displayedChartData.map((d) => d.strawberry),
      potato: displayedChartData.map((d) => d.potato),
      sweet_potato: displayedChartData.map((d) => d.sweet_potato),
      cashew: displayedChartData.map((d) => d.cashew),
    };
    return liveSeriesCards.map((item) => {
      const vec = seriesVectors[item.key] || [0];
      const startToEnd = vec[vec.length - 1] - vec[0];
      const minGrowth = Math.min(...vec);
      const maxGrowth = Math.max(...vec);
      return {
        ...item,
        periodGrowth: Number(startToEnd.toFixed(2)),
        amplitude: Number((maxGrowth - minGrowth).toFixed(2)),
        corrRice: calculatePearsonCorrelation(vec, seriesVectors.rice),
        corrCoffee: calculatePearsonCorrelation(vec, seriesVectors.coffee),
        corrPepper: calculatePearsonCorrelation(vec, seriesVectors.pepper),
        corrSugar: calculatePearsonCorrelation(vec, seriesVectors.sugar),
      };
    });
  }, [displayedChartData, liveSeriesCards]);

  const uniqueRegions = useMemo(() => {
    return Array.from(
      new Set(regionalPrices.map((p) => p.region.split('(')[0].trim()))
    ).filter(Boolean);
  }, [regionalPrices]);

  const filteredAndSortedRegional = useMemo(() => {
    const filtered = regionalPrices.filter((p) => {
      const matchRegion =
        selectedRegionFilter === 'ALL' ||
        p.region.toLowerCase().includes(selectedRegionFilter.toLowerCase());
      const matchQuery =
        searchQuery.trim() === '' ||
        p.commodityName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.region.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.source.toLowerCase().includes(searchQuery.toLowerCase());
      return matchRegion && matchQuery;
    });

    const factor = sortDir === 'ascending' ? 1 : -1;
    const collator = new Intl.Collator('vi', { numeric: true, sensitivity: 'base' });

    return [...filtered].sort((a, b) => {
      if (sortCol === 'commodityName') {
        return factor * collator.compare(a.commodityName, b.commodityName);
      }
      if (sortCol === 'price') {
        const numA = Number(String(a.price).replace(/\./g, '').replace(/,/g, '')) || 0;
        const numB = Number(String(b.price).replace(/\./g, '').replace(/,/g, '')) || 0;
        return factor * (numA - numB);
      }
      return factor * (a.changePct - b.changePct);
    });
  }, [regionalPrices, selectedRegionFilter, searchQuery, sortCol, sortDir]);

  const totalPages = Math.max(1, Math.ceil(filteredAndSortedRegional.length / pageSize));
  const pagedRegional = filteredAndSortedRegional.slice(page * pageSize, (page + 1) * pageSize);

  const handleSort = (col: 'commodityName' | 'price' | 'changePct') => {
    if (sortCol === col) {
      setSortDir((prev) => (prev === 'ascending' ? 'descending' : 'ascending'));
    } else {
      setSortCol(col);
      setSortDir('ascending');
    }
  };

  const handleExportRegionalCsv = () => {
    if (filteredAndSortedRegional.length === 0) return;
    const headers = ['Mặt hàng', 'Địa phương', 'Giá thu mua', 'Đơn vị', 'Biên độ sàn - trần', 'Biến động (%)', 'Nguồn báo giá'];
    const rows = filteredAndSortedRegional.map((item) => {
      const unit = getCommodityUnit(item.commodityName, item.unit);
      return [
        `"${item.commodityName}"`,
        `"${item.region}"`,
        `"${item.price}"`,
        `"${unit}"`,
        `"${item.minMax} ${unit}"`,
        item.changePct.toFixed(2),
        `"${item.source}"`,
      ].join(',');
    });
    const csv = '\uFEFF' + [headers.join(','), ...rows].join('\r\n');
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = 'so-sanh-gia-nong-san-dia-phuong.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-5 pb-10 font-sans">
      <Header
        title="So sánh nông sản & Tương quan biến động giá"
        subtitle={
          provinceCode !== 'all'
            ? `Đang hiển thị tỷ suất biến động & giá tham chiếu theo khu vực: ${provinceName}`
            : 'Đối sánh tỷ suất biến động giá chuẩn hóa (%) và khảo sát giá thu mua tại địa phương'
        }
        showLiveBadge={true}
      />

      {/* Interactive Commodity Selector Cards (100% Real DB Data) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {liveSeriesCards.map((item) => {
          const isActive = activeSeries[item.key];
          const isUp = item.changePct >= 0;
          return (
            <button
              key={item.key}
              type="button"
              onClick={() => toggleSeries(item.key)}
              aria-pressed={isActive}
              className={`p-3.5 rounded-lg border text-left transition-colors cursor-pointer ${
                isActive
                  ? 'bg-white border-[#166534] ring-1 ring-[#166534]/20'
                  : 'bg-white/70 border-[#E2E8F0] opacity-65 hover:opacity-100'
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span
                    className="w-2.5 h-2.5 rounded-full shrink-0"
                    style={{ backgroundColor: isActive ? item.color : '#94A3B8' }}
                  />
                  <span className="text-xs font-bold text-[#0F172A] truncate">{item.label}</span>
                </div>
                <span
                  className={`text-[11px] font-mono tabular-nums font-semibold px-1.5 py-0.5 rounded-md ${
                    isUp ? 'bg-[#15803D]/10 text-[#15803D]' : 'bg-[#DC2626]/10 text-[#DC2626]'
                  }`}
                >
                  {formatPct(item.changePct, 1)}
                </span>
              </div>

              <div className="mt-2 text-base font-bold text-[#0F172A] font-mono tabular-nums">
                {item.formattedPrice}
              </div>

              <div className="mt-1 flex items-center justify-between text-[11px] text-[#64748B]">
                <span className="truncate">{item.region.split('(')[0].trim()}</span>
                <span className="font-medium text-[#475569] shrink-0">
                  {isActive ? 'Đang hiển thị' : 'Đã ẩn'}
                </span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Syncfusion-style Financial Chart: Normalized Growth Curve (%) */}
      <section className="bg-white rounded-lg border border-[#E2E8F0] overflow-hidden">
        {/* Single-Row Chart Control Toolbar */}
        <div className="px-4 py-3 bg-[#F8FAFC] border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-[#166534]" />
            <div>
              <h2 className="text-[14px] font-bold text-[#0F172A] leading-tight">
                Đường cong tăng trưởng chuẩn hóa (Normalized Growth Curve - %)
              </h2>
              <p className="text-[11.5px] text-[#64748B]">
                Tỷ lệ biến động giá (%) của từng mặt hàng so với mốc đầu kỳ (0,0%)
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Timeframe Segmented Control: 7N | 14N | 30N | 3T | 1N */}
            <div className="flex items-center bg-white p-0.5 rounded-md border border-[#E2E8F0]">
              {(['7N', '14N', '30N', '3T', '1N'] as const).map((tf) => (
                <button
                  key={tf}
                  type="button"
                  onClick={() => setTimeframe(tf)}
                  className={`px-2.5 py-1 rounded-md text-xs font-mono tabular-nums font-semibold transition-colors ${
                    timeframe === tf
                      ? 'bg-[#166534] text-white'
                      : 'text-[#475569] hover:text-[#0F172A]'
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>

            <button
              type="button"
              onClick={() => void loadData()}
              disabled={isLoading}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-white hover:bg-[#F8FAFC] text-[#475569] hover:text-[#0F172A] border border-[#E2E8F0] text-xs font-semibold transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Làm mới</span>
            </button>
          </div>
        </div>

        {/* Syncfusion Financial Chart Area */}
        <div className="p-4 sm:p-5">
          <FinChart
            id={`syncfusion-compare-${timeframe}`}
            data={displayedChartData as unknown as Record<string, unknown>[]}
            xName="date"
            height={340}
            showLegend={false}
            sharedTooltip={true}
            showCrosshair={true}
            yFormat={(val: number) => formatPct(val, 1)}
            tooltipFormat={(val: number) => formatPct(val, 2)}
            series={liveSeriesCards.map((item) => ({
              type: 'Line',
              name: item.label,
              yName: item.key,
              color: item.color,
              width: 2.25,
              hidden: !activeSeries[item.key],
              showMarkers: displayedChartData.length <= 35,
            }))}
          />
        </div>
      </section>

      {/* Summary of % Spread & Pearson Correlation Matrix */}
      <section className="bg-white rounded-lg border border-[#E2E8F0] overflow-hidden">
        <div className="px-4 py-3 bg-[#F8FAFC] border-b border-[#E2E8F0] flex items-center justify-between">
          <div>
            <h3 className="text-[13.5px] font-bold text-[#0F172A]">
              Bảng tóm tắt chênh lệch tăng trưởng (%) & Hệ số tương quan Pearson (r)
            </h3>
            <p className="text-[11.5px] text-[#64748B]">
              Đánh giá mức độ đồng pha biến động giá giữa {liveSeriesCards.length} mặt hàng nông sản trong kỳ ({timeframe})
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-[#F8FAFC] text-[#64748B] uppercase text-[11px] font-bold tracking-wider border-b border-[#E2E8F0]">
              <tr>
                <th className="py-2.5 px-3.5">Nông sản</th>
                <th className="py-2.5 px-3.5 text-right">Giá hiện tại</th>
                <th className="py-2.5 px-3.5 text-right">Tăng trưởng kỳ</th>
                <th className="py-2.5 px-3.5 text-right">Biên độ dao động</th>
                <th className="py-2.5 px-3.5 text-right">Tương quan Lúa gạo</th>
                <th className="py-2.5 px-3.5 text-right">Tương quan Cà phê</th>
                <th className="py-2.5 px-3.5 text-right">Tương quan Hồ tiêu</th>
                <th className="py-2.5 px-3.5 text-right">Tương quan Mía đường</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E2E8F0] text-[12.5px]">
              {correlationSummary.map((row) => (
                <tr key={row.key} className="hover:bg-[#F8FAFC] transition-colors">
                  <td className="py-2.5 px-3.5 font-semibold text-[#0F172A] flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: row.color }} />
                    <span>{row.label}</span>
                  </td>
                  <td className="py-2.5 px-3.5 text-right font-mono tabular-nums font-semibold text-[#0F172A]">
                    {row.formattedPrice}
                  </td>
                  <td
                    className={`py-2.5 px-3.5 text-right font-mono tabular-nums font-semibold ${
                      row.periodGrowth >= 0 ? 'text-[#15803D]' : 'text-[#DC2626]'
                    }`}
                  >
                    {formatPct(row.periodGrowth, 2)}
                  </td>
                  <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-[#475569]">
                    {row.amplitude.toLocaleString('vi-VN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%
                  </td>
                  <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-[#0F172A]">{row.corrRice.toFixed(2)}</td>
                  <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-[#0F172A]">{row.corrCoffee.toFixed(2)}</td>
                  <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-[#0F172A]">{row.corrPepper.toFixed(2)}</td>
                  <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-[#0F172A]">{row.corrSugar.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Syncfusion Enterprise DataGrid: Regional Farm-Gate Price Survey */}
      <section className="bg-white rounded-lg border border-[#E2E8F0] overflow-hidden">
        {/* Integrated DataGrid Toolbar */}
        <div className="px-4 py-3 bg-[#F8FAFC] border-b border-[#E2E8F0] flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-[#166534]" />
            <div>
              <h3 className="text-[14px] font-bold text-[#0F172A]">
                Bảng khảo sát giá nông sản bán tại vườn / ruộng các địa phương
              </h3>
              <p className="text-[11.5px] text-[#64748B]">
                Đối chiếu giá thu mua thực tế, biên độ sàn/trần và đơn vị tính chuẩn tại từng huyện chuyên canh
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-[#64748B] absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setPage(0);
                }}
                placeholder="Tìm nông sản, huyện, nguồn..."
                className="pl-8 pr-3 py-1.5 rounded-md bg-white border border-[#E2E8F0] text-xs text-[#0F172A] focus:outline-none focus:border-[#166534] w-52"
              />
            </div>

            <select
              aria-label="Lọc theo địa phương"
              value={selectedRegionFilter}
              onChange={(e) => {
                setSelectedRegionFilter(e.target.value);
                setPage(0);
              }}
              className="bg-white border border-[#E2E8F0] text-[#0F172A] px-2.5 py-1.5 rounded-md text-xs font-medium focus:outline-none focus:border-[#166534]"
            >
              <option value="ALL">Tất cả địa phương ({regionalPrices.length})</option>
              {uniqueRegions.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={handleExportRegionalCsv}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-white hover:bg-[#F8FAFC] text-[#0F172A] border border-[#E2E8F0] text-xs font-semibold transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-[#166534]" />
              <span>Xuất CSV</span>
            </button>
          </div>
        </div>

        {/* DataGrid Table */}
        <div
          tabIndex={0}
          role="region"
          aria-label="Bảng khảo sát giá bán tại vườn các địa phương"
          className="overflow-x-auto max-h-[460px] custom-scrollbar"
        >
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 z-10 bg-[#F8FAFC] text-[#64748B] uppercase text-[11px] font-bold tracking-wider border-b border-[#E2E8F0]">
              <tr>
                <th
                  scope="col"
                  aria-sort={sortCol === 'commodityName' ? sortDir : undefined}
                  className="py-2.5 px-3.5"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('commodityName')}
                    className="inline-flex items-center gap-1 font-bold uppercase tracking-wider text-[#64748B] hover:text-[#0F172A]"
                  >
                    <span>Mặt hàng nông sản</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th scope="col" className="py-2.5 px-3.5">
                  Địa phương (Tại vườn / ruộng)
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'price' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('price')}
                    className="inline-flex items-center justify-end gap-1 font-bold uppercase tracking-wider text-[#64748B] hover:text-[#0F172A] ml-auto"
                  >
                    <span>Giá thu mua</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th scope="col" className="py-2.5 px-3.5 text-right">
                  Biên độ sàn / trần
                </th>
                <th
                  scope="col"
                  aria-sort={sortCol === 'changePct' ? sortDir : undefined}
                  className="py-2.5 px-3.5 text-right"
                >
                  <button
                    type="button"
                    onClick={() => handleSort('changePct')}
                    className="inline-flex items-center justify-end gap-1 font-bold uppercase tracking-wider text-[#64748B] hover:text-[#0F172A] ml-auto"
                  >
                    <span>Biến động</span>
                    <ArrowUpDown className="w-3 h-3" aria-hidden="true" />
                  </button>
                </th>
                <th scope="col" className="py-2.5 px-3.5">
                  Nguồn báo giá
                </th>
                <th scope="col" className="py-2.5 px-3.5 text-right">
                  Thao tác
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E2E8F0] text-[12.5px]">
              {pagedRegional.map((item) => {
                const unit = getCommodityUnit(item.commodityName, item.unit);
                const isUp = item.changePct >= 0;
                return (
                  <tr key={item.id} className="hover:bg-[#F8FAFC] transition-colors">
                    <td className="py-2.5 px-3.5 font-semibold text-[#0F172A]">{item.commodityName}</td>
                    <td className="py-2.5 px-3.5 text-[#475569]">{item.region}</td>
                    <td className="py-2.5 px-3.5 text-right font-mono tabular-nums font-bold text-[#0F172A]">
                      {item.price} <span className="text-[11px] font-normal text-[#64748B]">{unit}</span>
                    </td>
                    <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-[#475569]">
                      {item.minMax} <span className="text-[11px] text-[#64748B]">{unit}</span>
                    </td>
                    <td className="py-2.5 px-3.5 text-right font-mono tabular-nums">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-md font-semibold text-[11.5px] ${
                          isUp ? 'bg-[#15803D]/10 text-[#15803D]' : 'bg-[#DC2626]/10 text-[#DC2626]'
                        }`}
                      >
                        {formatPct(item.changePct, 2)}
                      </span>
                    </td>
                    <td className="py-2.5 px-3.5 text-[11.5px] text-[#475569]">{item.source}</td>
                    <td className="py-2.5 px-3.5 text-right">
                      <Link
                        href={`/forecast?commodity_id=${item.id}`}
                        className="text-[#166534] font-semibold hover:underline inline-flex items-center justify-end gap-1"
                      >
                        <span>Dự báo</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                );
              })}
              {pagedRegional.length === 0 && (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-[#64748B]">
                    Không tìm thấy bản ghi khảo sát phù hợp.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* DataGrid Pagination Footer */}
        <div className="px-4 py-2.5 bg-[#F8FAFC] border-t border-[#E2E8F0] flex items-center justify-between text-xs text-[#475569]">
          <span className="font-mono tabular-nums">
            Hiển thị {pagedRegional.length} / {filteredAndSortedRegional.length} bản ghi
          </span>
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              disabled={page === 0}
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              className="px-2.5 py-1 rounded-md bg-white border border-[#E2E8F0] font-medium disabled:opacity-40"
            >
              Trước
            </button>
            <span className="font-mono tabular-nums px-2">
              Trang {page + 1} / {totalPages}
            </span>
            <button
              type="button"
              disabled={page + 1 >= totalPages}
              onClick={() => setPage((p) => p + 1)}
              className="px-2.5 py-1 rounded-md bg-white border border-[#E2E8F0] font-medium disabled:opacity-40"
            >
              Sau
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
