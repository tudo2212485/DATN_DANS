'use client';

import React from 'react';
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

interface MarketComparisonChartProps {
  data: ComparisonDataPoint[];
}

export const MarketComparisonChart: React.FC<MarketComparisonChartProps> = ({ data }) => {
  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card flex flex-col justify-between h-full">
      {/* Header & Legends */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div>
          <h2 className="text-base font-bold text-primary-text tracking-tight">
            Tỷ lệ tăng/giảm so với đầu kỳ
          </h2>
          <p className="text-xs text-secondary-text mt-0.5 font-medium">
            Chuẩn hóa từ 01/06/2026 · đơn vị %
          </p>
        </div>

        {/* Legend */}
        <div className="flex items-center flex-wrap gap-4 text-xs font-semibold text-secondary-text">
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-0.5 rounded-full bg-[#4E7152]" />
            <span className="text-primary-text">Lúa gạo</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-0.5 rounded-full bg-[#D97757]" />
            <span className="text-primary-text">Cà phê</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-0.5 rounded-full bg-[#9C6644]" />
            <span className="text-primary-text">Hồ tiêu</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-0.5 rounded-full bg-[#4A69BD]" />
            <span className="text-primary-text">Mía đường</span>
          </div>
        </div>
      </div>

      {/* Main Multi-Line Chart with Gradients */}
      <div className="h-[280px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorRice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4E7152" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#4E7152" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorCoffee" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#D97757" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#D97757" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorPepper" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#9C6644" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#9C6644" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorSugar" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4A69BD" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#4A69BD" stopOpacity={0} />
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
              tickFormatter={(v) => `+${v}%`}
              domain={[0, 12]}
              ticks={[0, 3, 6, 9, 12]}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-white/95 backdrop-blur-md p-3 rounded-xl border border-border-subtle shadow-xl text-xs space-y-1">
                      <div className="font-bold text-primary-text mb-1 border-b border-border-subtle pb-1">
                        Thời điểm: {label}
                      </div>
                      <div className="text-[#4E7152] font-semibold flex justify-between gap-4">
                        <span>Lúa gạo:</span>
                        <span>+{payload[0]?.value}%</span>
                      </div>
                      <div className="text-[#D97757] font-semibold flex justify-between gap-4">
                        <span>Cà phê:</span>
                        <span>+{payload[1]?.value}%</span>
                      </div>
                      <div className="text-[#9C6644] font-semibold flex justify-between gap-4">
                        <span>Hồ tiêu:</span>
                        <span>+{payload[2]?.value}%</span>
                      </div>
                      <div className="text-[#4A69BD] font-semibold flex justify-between gap-4">
                        <span>Mía đường:</span>
                        <span>+{payload[3]?.value}%</span>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Area
              type="monotone"
              dataKey="rice"
              stroke="#4E7152"
              fill="url(#colorRice)"
              strokeWidth={2.2}
              activeDot={{ r: 4, strokeWidth: 0, fill: '#4E7152' }}
            />
            <Area
              type="monotone"
              dataKey="coffee"
              stroke="#D97757"
              fill="url(#colorCoffee)"
              strokeWidth={2.2}
              activeDot={{ r: 4, strokeWidth: 0, fill: '#D97757' }}
            />
            <Area
              type="monotone"
              dataKey="pepper"
              stroke="#9C6644"
              fill="url(#colorPepper)"
              strokeWidth={2.2}
              activeDot={{ r: 4, strokeWidth: 0, fill: '#9C6644' }}
            />
            <Area
              type="monotone"
              dataKey="sugar"
              stroke="#4A69BD"
              fill="url(#colorSugar)"
              strokeWidth={2.2}
              activeDot={{ r: 4, strokeWidth: 0, fill: '#4A69BD' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
export default MarketComparisonChart;
