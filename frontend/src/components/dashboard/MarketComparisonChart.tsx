'use client';

import React, { useState } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { ComparisonDataPoint } from '@/types';
import { TrendingUp, Layers } from 'lucide-react';

interface MarketComparisonChartProps {
  data: ComparisonDataPoint[];
}

interface CommodityToggle {
  key: keyof Pick<ComparisonDataPoint, 'rice' | 'coffee' | 'pepper' | 'sugar'>;
  label: string;
  color: string;
  fillGradient: string;
}

const COMMODITIES: CommodityToggle[] = [
  { key: 'rice', label: 'Lúa gạo IR504', color: '#10B981', fillGradient: 'colorRice' },
  { key: 'coffee', label: 'Cà phê Robusta', color: '#527853', fillGradient: 'colorCoffee' },
  { key: 'pepper', label: 'Hồ tiêu đen', color: '#8B5CF6', fillGradient: 'colorPepper' },
  { key: 'sugar', label: 'Mía đường', color: '#F59E0B', fillGradient: 'colorSugar' },
];

export const MarketComparisonChart: React.FC<MarketComparisonChartProps> = ({ data }) => {
  const [activeSeries, setActiveSeries] = useState<Record<string, boolean>>({
    rice: true,
    coffee: true,
    pepper: true,
    sugar: true,
  });

  const toggleSeries = (key: string) => {
    setActiveSeries((prev) => {
      // Ensure at least 1 series remains active
      const next = { ...prev, [key]: !prev[key] };
      if (!Object.values(next).some(Boolean)) return prev;
      return next;
    });
  };

  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-5 sm:p-6 shadow-card flex flex-col justify-between h-full space-y-4">
      {/* Header & Legends with toggle pills */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
        <div>
          <h2 className="text-base font-bold text-primary-text tracking-tight flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-brand" />
            <span>Biểu Đồ Tương Quan Tăng Trưởng Thị Trường (Normalized Growth)</span>
          </h2>
          <p className="text-xs text-secondary-text mt-0.5 font-medium">
            Tỷ lệ tăng/giảm so với mốc đầu kỳ chuẩn hóa (%) · Nhấp thẻ bên phải để bật/tắt từng mặt hàng
          </p>
        </div>

        {/* Commodity Toggle Pills */}
        <div className="flex items-center flex-wrap gap-1.5 bg-canvas p-1 rounded-xl border border-border-subtle">
          {COMMODITIES.map((c) => {
            const isActive = activeSeries[c.key];
            return (
              <button
                key={c.key}
                onClick={() => toggleSeries(c.key)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-white text-primary-text shadow-2xs border border-border-subtle'
                    : 'text-secondary-text/60 hover:text-secondary-text opacity-50'
                }`}
                title={`Nhấp để ${isActive ? 'ẩn' : 'hiện'} ${c.label}`}
              >
                <span
                  className="w-2.5 h-2.5 rounded-full"
                  style={{ backgroundColor: isActive ? c.color : '#C4BDB2' }}
                />
                <span className="text-[11px]">{c.label.split(' ')[0]}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Multi-Line Area Chart with smooth Gradients */}
      <div className="h-[300px] w-full pt-1">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 15, left: -10, bottom: 20 }}>
            <defs>
              <linearGradient id="colorRice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#10B981" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorCoffee" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#527853" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#527853" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorPepper" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorSugar" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#F0ECE4" vertical={false} />

            <XAxis
              dataKey="date"
              stroke="#A89A8B"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#EFECE6' }}
              dy={8}
            />

            {/* Formatted Y-Axis with Percentage strictly */}
            <YAxis
              stroke="#A89A8B"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              domain={['auto', 'auto']}
              tickFormatter={(v: number) => `${v > 0 ? '+' : ''}${Number(v).toFixed(1)}%`}
            />

            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-white/95 backdrop-blur-md p-3.5 rounded-xl border border-border-subtle shadow-xl text-xs space-y-1.5 min-w-[190px]">
                      <div className="font-bold text-primary-text mb-1 border-b border-border-subtle pb-1 flex items-center justify-between">
                        <span>Thời điểm: {label}</span>
                        <Layers className="w-3.5 h-3.5 text-brand" />
                      </div>
                      {payload.map((entry) => {
                        const val = Number(entry.value || 0);
                        const match = COMMODITIES.find((c) => c.key === entry.dataKey);
                        const labelName = match?.label || entry.name;
                        return (
                          <div
                            key={entry.dataKey as string}
                            className="font-semibold flex justify-between gap-3 text-xs"
                            style={{ color: entry.color }}
                          >
                            <span>{labelName}:</span>
                            <span className="font-mono font-extrabold">
                              {val > 0 ? '+' : ''}
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

            {activeSeries.rice && (
              <Area
                type="monotone"
                dataKey="rice"
                name="Lúa gạo IR504"
                stroke="#10B981"
                fill="url(#colorRice)"
                strokeWidth={2.4}
                activeDot={{ r: 4, strokeWidth: 0, fill: '#10B981' }}
              />
            )}
            {activeSeries.coffee && (
              <Area
                type="monotone"
                dataKey="coffee"
                name="Cà phê Robusta"
                stroke="#527853"
                fill="url(#colorCoffee)"
                strokeWidth={2.4}
                activeDot={{ r: 4, strokeWidth: 0, fill: '#527853' }}
              />
            )}
            {activeSeries.pepper && (
              <Area
                type="monotone"
                dataKey="pepper"
                name="Hồ tiêu đen"
                stroke="#8B5CF6"
                fill="url(#colorPepper)"
                strokeWidth={2.4}
                activeDot={{ r: 4, strokeWidth: 0, fill: '#8B5CF6' }}
              />
            )}
            {activeSeries.sugar && (
              <Area
                type="monotone"
                dataKey="sugar"
                name="Mía đường"
                stroke="#F59E0B"
                fill="url(#colorSugar)"
                strokeWidth={2.4}
                activeDot={{ r: 4, strokeWidth: 0, fill: '#F59E0B' }}
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MarketComparisonChart;
