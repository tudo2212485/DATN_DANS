'use client';

import React from 'react';
import { AreaChart, Area, ResponsiveContainer, YAxis } from 'recharts';
import { CommoditySummary } from '@/types';

interface CommodityCardProps {
  commodity: CommoditySummary;
}

export const CommodityCard: React.FC<CommodityCardProps> = ({ commodity }) => {
  const isPos = commodity.isPositive;
  const strokeColor = isPos ? '#4E7152' : '#D97757';
  const gradientId = `grad-${commodity.code}`;

  return (
    <div className="bg-card rounded-2xl border border-border-subtle p-5 shadow-card hover:shadow-hover transition-all duration-300 flex flex-col justify-between">
      {/* Top row: Code & Change % */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-[11px] font-bold text-secondary-text tracking-wider uppercase">
          {commodity.code}
        </span>
        <span
          className={`px-2.5 py-0.5 rounded-full text-xs font-bold tracking-tight ${
            isPos
              ? 'bg-brand-badge text-brand border border-brand/15'
              : 'bg-accent-coralLight text-accent-coral border border-accent-coral/20'
          }`}
        >
          {isPos ? `+${commodity.changePct}%` : `${commodity.changePct}%`}
        </span>
      </div>

      {/* Commodity Name & Price */}
      <div className="mb-4">
        <h3 className="text-xs font-semibold text-secondary-text mb-1.5">
          {commodity.name}
        </h3>
        <div className="flex items-baseline gap-1.5">
          <span className="text-[28px] font-extrabold text-primary-text tracking-tight leading-none">
            {commodity.formattedPrice}
          </span>
          <span className="text-xs font-semibold text-secondary-text">
            {commodity.unit}
          </span>
        </div>
      </div>

      {/* Sparkline Chart */}
      <div className="h-10 w-full mt-auto -mb-1">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={commodity.sparkline} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={strokeColor} stopOpacity={0.25} />
                <stop offset="95%" stopColor={strokeColor} stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <YAxis hide domain={['dataMin - 10', 'dataMax + 10']} />
            <Area
              type="monotone"
              dataKey="value"
              stroke={strokeColor}
              strokeWidth={2}
              fillOpacity={1}
              fill={`url(#${gradientId})`}
              isAnimationActive={true}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
export default CommodityCard;
