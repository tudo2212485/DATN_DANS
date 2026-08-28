'use client';

import React from 'react';
import { AreaChart, Area, ResponsiveContainer, YAxis } from 'recharts';
import { SpotlightSummary } from '@/types';

interface CommoditySpotlightProps {
  spotlight: SpotlightSummary;
}

export const CommoditySpotlight: React.FC<CommoditySpotlightProps> = ({ spotlight }) => {
  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-6 shadow-card flex flex-col justify-between h-full">
      {/* Title & Subtitle */}
      <div className="mb-3">
        <h2 className="text-base font-bold text-primary-text tracking-tight">
          {spotlight.commodityName}
        </h2>
        <p className="text-xs text-secondary-text mt-0.5 font-medium">
          {spotlight.subtitle}
        </p>
      </div>

      {/* Spotlight Area Trend */}
      <div className="h-32 w-full my-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={spotlight.trendData} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="spotlightGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#9C6644" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#9C6644" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <YAxis hide domain={['dataMin - 30', 'dataMax + 20']} />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#9C6644"
              strokeWidth={2.4}
              fillOpacity={1}
              fill="url(#spotlightGrad)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Metrics List */}
      <div className="pt-4 border-t border-border-subtle/80 space-y-2.5 text-xs">
        <div className="flex items-center justify-between">
          <span className="text-secondary-text font-medium">Giá hiện tại</span>
          <span className="font-bold text-[#9C6644] text-sm">
            {spotlight.currentPrice}
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-secondary-text font-medium">Tăng 3 tháng</span>
          <span className="font-bold text-brand text-sm">
            {spotlight.change3Months}
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-secondary-text font-medium">Cao nhất kỳ</span>
          <span className="font-bold text-primary-text text-sm">
            {spotlight.peakPrice}
          </span>
        </div>
      </div>
    </div>
  );
};
export default CommoditySpotlight;
