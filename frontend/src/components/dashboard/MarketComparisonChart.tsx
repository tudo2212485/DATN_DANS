'use client';

import React, { useState, useMemo } from 'react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Cell,
} from 'recharts';
import { ComparisonDataPoint } from '@/types';

interface MarketComparisonChartProps {
  data: ComparisonDataPoint[];
}

interface CommodityToggle {
  key: keyof Omit<ComparisonDataPoint, 'date'>;
  label: string;
  category: 'Lương thực' | 'Công nghiệp' | 'Đặc sản';
  color: string;
  fillGradient: string;
}

const COMMODITIES: CommodityToggle[] = [
  { key: 'rice', label: 'Lúa gạo IR504', category: 'Lương thực', color: '#059669', fillGradient: 'colorRice' },
  { key: 'coffee', label: 'Cà phê Robusta', category: 'Công nghiệp', color: '#2563EB', fillGradient: 'colorCoffee' },
  { key: 'pepper', label: 'Hồ tiêu đen', category: 'Công nghiệp', color: '#7C3AED', fillGradient: 'colorPepper' },
  { key: 'sugar', label: 'Mía đường', category: 'Công nghiệp', color: '#D97706', fillGradient: 'colorSugar' },
  { key: 'strawberry', label: 'Dâu tây Đà Lạt', category: 'Đặc sản', color: '#DB2777', fillGradient: 'colorStrawberry' },
  { key: 'sweet_potato', label: 'Khoai lang tím Vĩnh Long', category: 'Lương thực', color: '#9333EA', fillGradient: 'colorSweetPotato' },
  { key: 'potato', label: 'Khoai tây Đà Lạt', category: 'Lương thực', color: '#CA8A04', fillGradient: 'colorPotato' },
  { key: 'cashew', label: 'Hạt điều thô', category: 'Công nghiệp', color: '#EA580C', fillGradient: 'colorCashew' },
];

export const MarketComparisonChart: React.FC<MarketComparisonChartProps> = ({ data }) => {
  const [viewMode, setViewMode] = useState<'trend' | 'ranking'>('trend');
  const [categoryFilter, setCategoryFilter] = useState<'ALL' | 'Lương thực' | 'Công nghiệp' | 'Đặc sản'>('ALL');
  const [hoveredCommodity, setHoveredCommodity] = useState<string | null>(null);

  const [activeSeries, setActiveSeries] = useState<Record<string, boolean>>({
    rice: true,
    coffee: true,
    pepper: true,
    sugar: false,
    strawberry: true,
    sweet_potato: false,
    potato: false,
    cashew: false,
  });

  const toggleSeries = (key: string) => {
    setActiveSeries((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      if (!Object.values(next).some(Boolean)) return prev;
      return next;
    });
  };

  const handleSelectGroup = (cat: 'ALL' | 'Lương thực' | 'Công nghiệp' | 'Đặc sản') => {
    setCategoryFilter(cat);
    if (cat === 'ALL') {
      setActiveSeries({
        rice: true,
        coffee: true,
        pepper: true,
        sugar: false,
        strawberry: true,
        sweet_potato: false,
        potato: false,
        cashew: false,
      });
      return;
    }
    const next: Record<string, boolean> = {};
    COMMODITIES.forEach((c) => {
      next[c.key] = c.category === cat;
    });
    setActiveSeries(next);
  };

  const rankingData = useMemo(() => {
    if (!data || data.length === 0) return [];
    const latest = data[data.length - 1];
    return COMMODITIES.map((c) => {
      const val = Number(latest[c.key as keyof ComparisonDataPoint] || 0);
      return {
        key: c.key,
        name: c.label,
        change: Number(val.toFixed(2)),
        color: c.color,
        category: c.category,
      };
    }).sort((a, b) => b.change - a.change);
  }, [data]);

  return (
    <div className="bg-white rounded-xl border border-zinc-200/90 p-5 shadow-[0_1px_2px_rgba(0,0,0,0.02)] flex flex-col justify-between h-full space-y-4 font-sans">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3.5 border-b border-zinc-100">
        <div>
          <h2 className="text-[15px] font-semibold text-zinc-900">
            So sánh tốc độ biến động giá (%)
          </h2>
          <p className="text-[12.5px] text-zinc-500 mt-0.5">
            Tương quan tăng giảm phần trăm so với mốc đầu kỳ
          </p>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center gap-0.5 bg-zinc-100 p-0.5 rounded-lg border border-zinc-200/60 shrink-0 w-fit">
          <button
            onClick={() => setViewMode('trend')}
            className={`px-3 py-1 rounded-md text-[12px] font-medium transition-all cursor-pointer ${
              viewMode === 'trend'
                ? 'bg-white text-zinc-900 shadow-2xs font-semibold'
                : 'text-zinc-500 hover:text-zinc-800'
            }`}
          >
            Đường xu hướng
          </button>
          <button
            onClick={() => setViewMode('ranking')}
            className={`px-3 py-1 rounded-md text-[12px] font-medium transition-all cursor-pointer ${
              viewMode === 'ranking'
                ? 'bg-white text-zinc-900 shadow-2xs font-semibold'
                : 'text-zinc-500 hover:text-zinc-800'
            }`}
          >
            Xếp hạng biến động
          </button>
        </div>
      </div>

      {/* Category & Series Toggles */}
      <div className="space-y-2.5">
        <div className="flex flex-wrap items-center gap-1.5">
          {(['ALL', 'Lương thực', 'Công nghiệp', 'Đặc sản'] as const).map((cat) => (
            <button
              key={cat}
              onClick={() => handleSelectGroup(cat)}
              className={`px-2.5 py-1 rounded-md text-[12px] transition-all cursor-pointer border ${
                categoryFilter === cat
                  ? 'bg-zinc-900 text-white border-zinc-900 font-medium'
                  : 'bg-white text-zinc-600 border-zinc-200/80 hover:border-zinc-300'
              }`}
            >
              {cat === 'ALL' ? 'Mặc định' : cat}
            </button>
          ))}
        </div>

        <div className="flex items-center flex-wrap gap-1.5 pt-1">
          {COMMODITIES.map((c) => {
            const isActive = activeSeries[c.key];
            return (
              <button
                key={c.key}
                onClick={() => toggleSeries(c.key)}
                onMouseEnter={() => setHoveredCommodity(c.key)}
                onMouseLeave={() => setHoveredCommodity(null)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[12px] transition-all select-none cursor-pointer border ${
                  isActive
                    ? 'bg-zinc-50 text-zinc-900 font-medium border-zinc-300'
                    : 'text-zinc-400 bg-transparent border-transparent hover:text-zinc-600'
                }`}
              >
                <span
                  className="w-2 h-2 rounded-full shrink-0"
                  style={{ backgroundColor: isActive ? c.color : '#D4D4D8' }}
                />
                <span className="whitespace-nowrap">{c.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="h-[340px] w-full pt-1">
        {viewMode === 'trend' ? (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 16, left: -12, bottom: 8 }}>
              <defs>
                {COMMODITIES.map((c) => (
                  <linearGradient key={c.fillGradient} id={c.fillGradient} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={c.color} stopOpacity={0.14} />
                    <stop offset="95%" stopColor={c.color} stopOpacity={0.0} />
                  </linearGradient>
                ))}
              </defs>

              <CartesianGrid strokeDasharray="3 3" stroke="#F4F4F5" vertical={false} />
              <ReferenceLine y={0} stroke="#D4D4D8" strokeDasharray="3 3" />

              <XAxis
                dataKey="date"
                stroke="#71717A"
                fontSize={11.5}
                tickLine={false}
                axisLine={{ stroke: '#E4E4E7' }}
                dy={6}
              />

              <YAxis
                stroke="#71717A"
                fontSize={11.5}
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
                tickFormatter={(v: number) => `${v > 0 ? '+' : ''}${Number(v).toFixed(1)}%`}
              />

              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-zinc-900 text-white px-3.5 py-2.5 rounded-lg shadow-xl text-[12px] space-y-1.5 min-w-[210px] z-30">
                        <div className="font-medium text-zinc-300 border-b border-zinc-800 pb-1 flex items-center justify-between">
                          <span>Kỳ: {label}</span>
                          <span className="text-[11px] text-zinc-400">Thay đổi (%)</span>
                        </div>
                        {payload.map((entry) => {
                          const val = Number(entry.value || 0);
                          const match = COMMODITIES.find((c) => c.key === entry.dataKey);
                          const labelName = match?.label || entry.name;
                          const isPos = val >= 0;
                          return (
                            <div
                              key={entry.dataKey as string}
                              className="flex items-center justify-between gap-3 py-0.5"
                            >
                              <div className="flex items-center gap-2 min-w-0">
                                <span
                                  className="w-2 h-2 rounded-full shrink-0"
                                  style={{ backgroundColor: entry.color }}
                                />
                                <span className="text-zinc-200 truncate">{labelName}</span>
                              </div>
                              <span
                                className={`font-mono font-semibold ${
                                  isPos ? 'text-emerald-400' : 'text-rose-400'
                                }`}
                              >
                                {isPos ? '+' : ''}
                                {val.toFixed(2)}%
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    );
                  }
                  return null;
                }}
              />

              {COMMODITIES.map((c) => {
                if (!activeSeries[c.key]) return null;
                const isHovered = hoveredCommodity === c.key;
                const hasHover = hoveredCommodity !== null;
                const opacity = hasHover ? (isHovered ? 1 : 0.2) : 1;
                const strokeWidth = isHovered ? 2.75 : 2;

                return (
                  <Area
                    key={c.key}
                    type="monotone"
                    dataKey={c.key}
                    name={c.label}
                    stroke={c.color}
                    strokeWidth={strokeWidth}
                    fillOpacity={hasHover && !isHovered ? 0.02 : 1}
                    fill={`url(#${c.fillGradient})`}
                    strokeOpacity={opacity}
                    baseValue="dataMin"
                    isAnimationActive={false}
                  />
                );
              })}
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={rankingData}
              layout="vertical"
              margin={{ top: 8, right: 24, left: 20, bottom: 8 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#F4F4F5" horizontal={false} />
              <XAxis
                type="number"
                tickFormatter={(v) => `${v > 0 ? '+' : ''}${v}%`}
                stroke="#71717A"
                fontSize={11.5}
                tickLine={false}
                axisLine={{ stroke: '#E4E4E7' }}
              />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#3F3F46"
                fontSize={12}
                fontWeight={500}
                tickLine={false}
                axisLine={false}
                width={135}
              />
              <ReferenceLine x={0} stroke="#D4D4D8" strokeDasharray="3 3" />
              <Tooltip
                formatter={(val) => [`${Number(val || 0) > 0 ? '+' : ''}${val}%`, 'Biến động']}
                contentStyle={{
                  backgroundColor: '#18181B',
                  color: '#FFFFFF',
                  borderRadius: '8px',
                  border: 'none',
                  fontSize: '12px',
                }}
              />
              <Bar dataKey="change" radius={[0, 4, 4, 0]} barSize={20}>
                {rankingData.map((entry) => (
                  <Cell
                    key={entry.key}
                    fill={entry.change >= 0 ? '#059669' : '#E11D48'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

export default MarketComparisonChart;
