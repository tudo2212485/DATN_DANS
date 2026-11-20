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
import { formatPct } from '@/lib/formatters';

interface MarketComparisonChartProps {
  data: ComparisonDataPoint[];
}

interface CommodityToggle {
  key: 'rice' | 'coffee' | 'pepper' | 'sugar';
  label: string;
  color: string;
  fillGradient: string;
}

const COMMODITIES: CommodityToggle[] = [
  { key: 'rice', label: 'Lúa gạo IR50404', color: '#2F6F4E', fillGradient: 'colorRice' },
  { key: 'coffee', label: 'Cà phê Robusta', color: '#2563EB', fillGradient: 'colorCoffee' },
  { key: 'pepper', label: 'Hồ tiêu đen', color: '#7C3AED', fillGradient: 'colorPepper' },
  { key: 'sugar', label: 'Mía đường', color: '#D97706', fillGradient: 'colorSugar' },
];

export const MarketComparisonChart: React.FC<MarketComparisonChartProps> = ({ data }) => {
  const [viewMode, setViewMode] = useState<'trend' | 'ranking'>('trend');
  const [activeSeries, setActiveSeries] = useState<Record<string, boolean>>({
    rice: true,
    coffee: true,
    pepper: true,
    sugar: true,
  });

  const toggleSeries = (key: string) => {
    setActiveSeries((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      if (!Object.values(next).some(Boolean)) return prev;
      return next;
    });
  };

  const rankingData = useMemo(() => {
    if (!data || data.length === 0) return [];
    const latest = data[data.length - 1];
    return COMMODITIES.map((c) => {
      const rawVal = Number(latest[c.key] || 0);
      const val = Math.abs(rawVal) < 0.005 ? 0 : Number(rawVal.toFixed(2));
      return {
        key: c.key,
        name: c.label,
        change: val,
        color: c.color,
      };
    }).sort((a, b) => b.change - a.change);
  }, [data]);

  return (
    <div className="bg-white rounded-xl border border-[#E5E7EB] p-5 shadow-card flex flex-col justify-between h-full space-y-3.5 font-sans">
      {/* Header + View Mode Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pb-3 border-b border-[#E5E7EB]">
        <div>
          <h2 className="text-[15px] font-bold text-[#1E293B]">
            So sánh tốc độ biến động giá (%)
          </h2>
          <p className="text-xs text-[#64748B] mt-0.5">
            Tương quan tăng giảm phần trăm so với mốc đầu kỳ
          </p>
        </div>

        <div className="flex items-center gap-0.5 bg-[#F8FAF9] p-0.5 rounded-lg border border-[#E5E7EB] shrink-0 w-fit">
          <button
            type="button"
            onClick={() => setViewMode('trend')}
            className={`px-3 py-1 rounded-md text-xs font-medium transition-colors cursor-pointer ${
              viewMode === 'trend'
                ? 'bg-[#2F6F4E] text-white font-semibold'
                : 'text-[#334155] hover:text-[#1E293B]'
            }`}
          >
            Đường xu hướng
          </button>
          <button
            type="button"
            onClick={() => setViewMode('ranking')}
            className={`px-3 py-1 rounded-md text-xs font-medium transition-colors cursor-pointer ${
              viewMode === 'ranking'
                ? 'bg-[#2F6F4E] text-white font-semibold'
                : 'text-[#334155] hover:text-[#1E293B]'
            }`}
          >
            Xếp hạng biến động
          </button>
        </div>
      </div>

      {/* Single Horizontal Row of 4 Real Commodity Toggles */}
      <div className="flex items-center flex-wrap gap-2">
        {COMMODITIES.map((c) => {
          const isActive = activeSeries[c.key];
          return (
            <button
              key={c.key}
              type="button"
              onClick={() => toggleSeries(c.key)}
              aria-pressed={isActive}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-colors select-none cursor-pointer border ${
                isActive
                  ? 'bg-[#F0F7F4] text-[#1E293B] font-semibold border-[#2F6F4E]/40'
                  : 'text-[#64748B] bg-white border-[#E5E7EB] opacity-65 hover:opacity-100'
              }`}
            >
              <span
                className="w-2.5 h-2.5 rounded-full shrink-0"
                style={{ backgroundColor: isActive ? c.color : '#CBD5E1' }}
              />
              <span>{c.label}</span>
            </button>
          );
        })}
      </div>

      {/* Chart Canvas */}
      <div className="h-[320px] w-full pt-1">
        {viewMode === 'trend' ? (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 16, left: -10, bottom: 6 }}>
              <defs>
                {COMMODITIES.map((c) => (
                  <linearGradient key={c.fillGradient} id={c.fillGradient} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={c.color} stopOpacity={0.12} />
                    <stop offset="95%" stopColor={c.color} stopOpacity={0.0} />
                  </linearGradient>
                ))}
              </defs>

              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
              <ReferenceLine y={0} stroke="#CBD5E1" strokeDasharray="3 3" />

              <XAxis
                dataKey="date"
                stroke="#64748B"
                fontSize={11.5}
                tickLine={false}
                axisLine={{ stroke: '#E5E7EB' }}
                dy={6}
              />

              <YAxis
                stroke="#64748B"
                fontSize={11.5}
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
                tickFormatter={(v: number) => formatPct(v, 1)}
              />

              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-white text-[#1E293B] px-3.5 py-2.5 rounded-lg border border-[#E5E7EB] shadow-md text-xs space-y-1.5 min-w-[210px]">
                        <div className="font-semibold text-[#1E293B] border-b border-[#E5E7EB] pb-1 flex items-center justify-between">
                          <span>Kỳ: {label}</span>
                          <span className="text-[11px] text-[#64748B]">Thay đổi (%)</span>
                        </div>
                        {payload.map((entry) => {
                          const rawVal = Number(entry.value || 0);
                          const val = Math.abs(rawVal) < 0.005 ? 0 : rawVal;
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
                                <span className="text-[#334155] truncate">{labelName}</span>
                              </div>
                              <span
                                className={`tabular-nums font-semibold ${
                                  isPos ? 'text-[#15803D]' : 'text-[#DC2626]'
                                }`}
                              >
                                {formatPct(val, 2)}
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

              {COMMODITIES.map((c) =>
                activeSeries[c.key] ? (
                  <Area
                    key={c.key}
                    type="monotone"
                    dataKey={c.key}
                    name={c.label}
                    stroke={c.color}
                    strokeWidth={2.25}
                    fill={`url(#${c.fillGradient})`}
                    baseValue="dataMin"
                    isAnimationActive={false}
                  />
                ) : null
              )}
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={rankingData}
              layout="vertical"
              margin={{ top: 8, right: 24, left: 20, bottom: 8 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" horizontal={false} />
              <XAxis
                type="number"
                tickFormatter={(v) => formatPct(Number(v), 1)}
                stroke="#64748B"
                fontSize={11.5}
                tickLine={false}
                axisLine={{ stroke: '#E5E7EB' }}
              />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#1E293B"
                fontSize={12}
                fontWeight={600}
                tickLine={false}
                axisLine={false}
                width={135}
              />
              <ReferenceLine x={0} stroke="#CBD5E1" strokeDasharray="3 3" />
              <Tooltip
                formatter={(val) => [formatPct(Number(val || 0), 2), 'Biến động']}
                contentStyle={{
                  backgroundColor: '#FFFFFF',
                  color: '#1E293B',
                  borderRadius: '8px',
                  border: '1px solid #E5E7EB',
                  fontSize: '12px',
                }}
              />
              <Bar dataKey="change" radius={[0, 4, 4, 0]} barSize={22} isAnimationActive={false}>
                {rankingData.map((entry) => (
                  <Cell
                    key={entry.key}
                    fill={entry.change >= 0 ? '#2F6F4E' : '#DC2626'}
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
