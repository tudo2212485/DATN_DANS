'use client';

import React from 'react';
import { AreaChart, Area, ResponsiveContainer, YAxis } from 'recharts';
import { CommoditySummary } from '@/types';
import { ArrowUpRight, ArrowDownRight, ChevronRight } from 'lucide-react';

interface CommodityCardProps {
  commodity: CommoditySummary;
}

export const CommodityCard: React.FC<CommodityCardProps> = ({ commodity }) => {
  const isPos = commodity.isPositive;
  const strokeColor = isPos ? '#059669' : '#E11D48';
  const gradientId = `grad-${commodity.code}`;

  const sparkValues =
    commodity.sparkline && commodity.sparkline.length > 0
      ? commodity.sparkline.map((s) => s.value)
      : [commodity.currentPrice];
  const minPrice = Math.min(...sparkValues);
  const maxPrice = Math.max(...sparkValues);
  const current = commodity.currentPrice || sparkValues[sparkValues.length - 1] || 0;

  const previousPrice =
    sparkValues.length > 1
      ? sparkValues[sparkValues.length - 2]
      : current * (1 - commodity.changePct / 100);
  const diffVnd = current - previousPrice;
  const loc = commodity.location_context;
  const showProvinceBadge =
    loc && loc.province_code && loc.province_code !== 'all' && loc.pricing_mode !== 'national_benchmark';

  return (
    <article className="h-full bg-white rounded-xl border border-zinc-200/90 p-5 shadow-[0_1px_2px_rgba(0,0,0,0.02)] hover:border-zinc-300 hover:shadow-sm transition-all duration-200 flex flex-col justify-between group font-sans">
      <div>
        {/* Header: Name, Region & Change Badge */}
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h3 className="text-[15px] font-semibold text-zinc-900 group-hover:text-emerald-700 transition-colors truncate">
              {commodity.name}
            </h3>
            <p className="text-[12px] text-zinc-500 truncate mt-0.5">
              {commodity.region} · {commodity.category}
            </p>
          </div>

          <span
            className={`inline-flex items-center gap-0.5 px-2 py-0.5 rounded text-[12px] font-semibold font-mono shrink-0 ${
              isPos
                ? 'bg-emerald-50 text-emerald-700'
                : 'bg-rose-50 text-rose-700'
            }`}
          >
            {isPos ? (
              <ArrowUpRight className="w-3.5 h-3.5" />
            ) : (
              <ArrowDownRight className="w-3.5 h-3.5" />
            )}
            <span>{isPos ? `+${commodity.changePct}%` : `${commodity.changePct}%`}</span>
          </span>
        </div>

        {/* Transparent Location Pricing Mode Badge (Direct Survey vs Regional Benchmark) */}
        {showProvinceBadge && loc && (
          <div className="mt-2">
            {loc.pricing_mode === 'direct' ? (
              <span
                title={loc.explanation || undefined}
                className="inline-flex items-center px-2 py-0.5 rounded-md bg-[#F0F7F4] text-[#15803D] border border-[#15803D]/20 text-[11px] font-semibold max-w-full truncate"
              >
                Khảo sát tại {loc.province_name}
              </span>
            ) : (
              <span
                title={loc.explanation || undefined}
                className="inline-flex items-center px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-medium max-w-full truncate"
              >
                Tham chiếu {loc.reference_province} (+cước ~{Math.round(loc.distance_km)} km)
              </span>
            )}
          </div>
        )}

        {/* Price & Sparkline Row */}
        <div className="mt-4 flex items-end justify-between gap-3">
          <div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-zinc-900 tracking-tight font-mono leading-none">
                {commodity.formattedPrice}
              </span>
              <span className="text-[12px] font-medium text-zinc-500">
                {commodity.unit}
              </span>
            </div>
            <span
              className={`block mt-1.5 text-[12px] font-medium font-mono tabular-nums ${
                isPos ? 'text-[#15803D]' : 'text-[#DC2626]'
              }`}
            >
              {diffVnd >= 0
                ? `+${Math.round(diffVnd).toLocaleString('vi-VN')} ${commodity.unit}`
                : `${Math.round(diffVnd).toLocaleString('vi-VN')} ${commodity.unit}`}{' '}
              <span className="text-zinc-400 font-sans">so với kỳ trước</span>
            </span>
          </div>

          {/* Mini Sparkline */}
          <div className="h-11 w-24 shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={commodity.sparkline}>
                <defs>
                  <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={strokeColor} stopOpacity={0.2} />
                    <stop offset="100%" stopColor={strokeColor} stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <YAxis hide domain={['dataMin', 'dataMax']} />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke={strokeColor}
                  strokeWidth={1.75}
                  fill={`url(#${gradientId})`}
                  baseValue="dataMin"
                  isAnimationActive={false}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Footer: Min/Max & Action */}
      <div className="mt-4 pt-3 border-t border-zinc-100 flex items-center justify-between gap-2 text-[12px] text-zinc-500">
        <span className="font-mono tabular-nums text-[11.5px] truncate">
          Biên độ: {Math.round(minPrice).toLocaleString('vi-VN')} – {Math.round(maxPrice).toLocaleString('vi-VN')}
        </span>
        <span className="inline-flex items-center gap-0.5 font-medium text-zinc-700 group-hover:text-emerald-700 transition-colors whitespace-nowrap shrink-0">
          Chi tiết <ChevronRight className="w-3.5 h-3.5 shrink-0" />
        </span>
      </div>
    </article>
  );
};

export default CommodityCard;
